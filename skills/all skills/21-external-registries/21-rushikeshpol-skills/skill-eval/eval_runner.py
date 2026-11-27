"""
Skill Evaluation Runner — Langfuse-integrated evaluation harness.

Usage:
    python eval_runner.py --skill transcript-to-meeting-notes
    python eval_runner.py --skill generate-requirements --benchmark attestation-from-discovery
    python eval_runner.py --skill all
    python eval_runner.py --list

Workflow:
    1. Loads config.yaml for skill definitions, rubrics, and benchmarks
    2. Creates/updates Langfuse datasets from benchmark definitions
    3. For each benchmark item: runs LLM-as-judge on each rubric dimension
    4. Scores are sent to Langfuse with full trace lineage
    5. Prints a summary table with per-dimension and composite scores
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

console = Console()
REPO_ROOT = Path(__file__).parent.parent  # ai-skills/
SKILLS_DIR = REPO_ROOT / "cursor" / "skills"


def load_config() -> dict:
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def init_langfuse():
    from langfuse import Langfuse

    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")

    if not public_key or not secret_key:
        console.print(
            "[yellow]Warning: Langfuse credentials not set. "
            "Running in local-only mode (scores printed but not sent to Langfuse).[/yellow]"
        )
        return None

    return Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host,
    )


def init_anthropic():
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        console.print("[red]Error: ANTHROPIC_API_KEY not set in .env[/red]")
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def resolve_path(relative_path: str) -> Path:
    """Resolve a path against the configured benchmark workspace, repo root, or skills dir."""
    config = load_config()
    workspace = Path(os.path.expanduser(config.get("project", {}).get("benchmark_workspace", ".")))

    candidates = [
        workspace / relative_path,
        REPO_ROOT / relative_path,
        SKILLS_DIR / relative_path,
        Path(os.path.expanduser(relative_path)),
    ]
    for p in candidates:
        if p.exists():
            return p
    return workspace / relative_path  # return first candidate for error message


def read_file(relative_path: str) -> str:
    full_path = resolve_path(relative_path)
    if not full_path.exists():
        console.print(f"[red]File not found: {full_path}[/red]")
        return ""
    return full_path.read_text(encoding="utf-8")


def ensure_dataset(langfuse, skill_config: dict) -> str | None:
    """Create or update a Langfuse dataset for the skill's benchmarks."""
    if langfuse is None:
        return None

    dataset_name = skill_config["dataset_name"]
    try:
        langfuse.get_dataset(dataset_name)
    except Exception:
        langfuse.create_dataset(name=dataset_name)
        console.print(f"  Created Langfuse dataset: [green]{dataset_name}[/green]")

    for bench in skill_config.get("benchmarks", []):
        expected = {}
        for key in ["expected_decisions", "expected_topics", "expected_frs", "critical_constraints"]:
            if key in bench:
                expected[key] = bench[key]

        langfuse.create_dataset_item(
            dataset_name=dataset_name,
            input={"benchmark_id": bench["id"], "description": bench.get("input_description", "")},
            expected_output=expected or None,
            metadata={"input_files": bench.get("input_file") or bench.get("input_files", [])},
        )

    return dataset_name


def run_judge(
    anthropic_client,
    dimension_name: str,
    dimension_config: dict,
    skill_output: str,
    source_material: str,
    expected_items: dict | None,
    judge_config: dict,
) -> dict:
    """Run a single LLM-as-judge evaluation for one dimension."""
    from judge_prompts import SYSTEM_PROMPT, build_judge_prompt

    prompt = build_judge_prompt(
        dimension_name=dimension_name,
        dimension_description=dimension_config["description"],
        scoring_rubric=dimension_config["scoring"],
        skill_output=skill_output,
        source_material=source_material,
        expected_items=expected_items,
    )

    response = anthropic_client.messages.create(
        model=judge_config["model"],
        max_tokens=judge_config["max_tokens"],
        temperature=judge_config["temperature"],
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = response.content[0].text.strip()

    # Extract JSON from response (handle markdown code blocks)
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        json_lines = [l for l in lines if not l.startswith("```")]
        response_text = "\n".join(json_lines)

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        console.print(f"  [yellow]Judge returned non-JSON for {dimension_name}, retrying...[/yellow]")
        result = {
            "dimension": dimension_name,
            "score": 0,
            "confidence": 0.0,
            "evidence": [],
            "summary": f"Parse error: {response_text[:200]}",
        }

    return result


def evaluate_benchmark(
    anthropic_client,
    langfuse,
    skill_name: str,
    skill_config: dict,
    benchmark: dict,
    judge_config: dict,
) -> dict:
    """Evaluate one benchmark item across all rubric dimensions."""

    console.print(f"\n  [bold]Benchmark:[/bold] {benchmark['id']}")
    console.print(f"  {benchmark.get('input_description', '')}")

    # Load source material
    input_files = benchmark.get("input_files") or [benchmark.get("input_file", "")]
    source_parts = []
    for f in input_files:
        content = read_file(f)
        if content:
            source_parts.append(f"--- {f} ---\n{content}")
    source_material = "\n\n".join(source_parts)

    if not source_material:
        console.print("  [red]No source material found, skipping benchmark[/red]")
        return {}

    # Load skill output (gold reference or existing output)
    gold_ref = benchmark.get("gold_reference")
    if gold_ref:
        skill_output = read_file(gold_ref)
    else:
        console.print("  [yellow]No gold reference — will use source as both input and reference[/yellow]")
        skill_output = source_material

    if not skill_output:
        console.print("  [red]No skill output found, skipping benchmark[/red]")
        return {}

    # Build expected items from benchmark config
    expected_items = {}
    for key in ["expected_decisions", "expected_topics", "expected_frs", "critical_constraints"]:
        if key in benchmark:
            expected_items[key] = benchmark[key]

    # Create Langfuse trace for this evaluation run
    trace = None
    if langfuse:
        trace = langfuse.trace(
            name=f"eval-{skill_name}-{benchmark['id']}",
            metadata={
                "skill": skill_name,
                "benchmark": benchmark["id"],
                "input_files": input_files,
            },
        )

    # Run judge for each dimension
    rubric = skill_config["rubric"]["dimensions"]
    results = {}
    runs_per_item = judge_config.get("runs_per_item", 1)

    for dim_name, dim_config in rubric.items():
        dim_scores = []
        for run_idx in range(runs_per_item):
            result = run_judge(
                anthropic_client=anthropic_client,
                dimension_name=dim_name,
                dimension_config=dim_config,
                skill_output=skill_output,
                source_material=source_material,
                expected_items=expected_items if expected_items else None,
                judge_config=judge_config,
            )
            dim_scores.append(result)

            # Log each judge run as a Langfuse generation
            if trace:
                generation = trace.generation(
                    name=f"judge-{dim_name}-run{run_idx}",
                    input={"dimension": dim_name, "run": run_idx},
                    output=result,
                    metadata={"weight": dim_config["weight"]},
                )
                if result.get("score"):
                    trace.score(
                        name=dim_name,
                        value=result["score"] / 5.0,
                        comment=result.get("summary", ""),
                    )

        # Use median score across runs for stability
        valid_scores = [s for s in dim_scores if s.get("score", 0) > 0]
        if valid_scores:
            median_score = statistics.median([s["score"] for s in valid_scores])
            best_run = min(valid_scores, key=lambda s: abs(s["score"] - median_score))
            results[dim_name] = {
                **best_run,
                "score": median_score,
                "weight": dim_config["weight"],
                "all_scores": [s["score"] for s in dim_scores],
            }
        else:
            results[dim_name] = {"score": 0, "weight": dim_config["weight"], "summary": "All runs failed"}

    # Compute weighted composite score
    composite = sum(
        r["score"] * r["weight"]
        for r in results.values()
        if r.get("score", 0) > 0
    )

    if trace:
        trace.score(name="composite", value=composite / 5.0, comment=f"Weighted composite: {composite:.2f}/5.0")

    results["_composite"] = composite
    return results


def print_results(skill_name: str, all_results: dict):
    """Print a summary table of evaluation results."""

    table = Table(title=f"Evaluation Results: {skill_name}", show_lines=True)
    table.add_column("Benchmark", style="bold")
    table.add_column("Dimension", style="cyan")
    table.add_column("Score", justify="center")
    table.add_column("Weight", justify="center")
    table.add_column("Spread", justify="center", style="dim")
    table.add_column("Summary")

    for bench_id, results in all_results.items():
        composite = results.pop("_composite", 0)
        first_row = True

        for dim_name, dim_result in results.items():
            score = dim_result.get("score", 0)
            weight = dim_result.get("weight", 0)
            all_scores = dim_result.get("all_scores", [])
            spread = f"{min(all_scores)}-{max(all_scores)}" if len(all_scores) > 1 else "-"
            summary = dim_result.get("summary", "")[:80]

            score_color = "green" if score >= 4 else "yellow" if score >= 3 else "red"

            table.add_row(
                bench_id if first_row else "",
                dim_name,
                f"[{score_color}]{score:.1f}[/{score_color}]/5",
                f"{weight:.0%}",
                spread,
                summary,
            )
            first_row = False

        composite_color = "green" if composite >= 4 else "yellow" if composite >= 3 else "red"
        table.add_row(
            "",
            "[bold]COMPOSITE[/bold]",
            f"[bold {composite_color}]{composite:.2f}[/bold {composite_color}]/5",
            "100%",
            "",
            "",
        )

    console.print(table)


def list_skills(config: dict):
    """List all configured skills and their benchmarks."""
    table = Table(title="Configured Skills", show_lines=True)
    table.add_column("Skill", style="bold cyan")
    table.add_column("Benchmarks")
    table.add_column("Dimensions")
    table.add_column("Runs/Item", justify="center")

    for name, skill in config["skills"].items():
        benchmarks = ", ".join(b["id"] for b in skill.get("benchmarks", []))
        dimensions = ", ".join(skill["rubric"]["dimensions"].keys())
        runs = config["judge"]["runs_per_item"]
        table.add_row(name, benchmarks, dimensions, str(runs))

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Skill Evaluation Runner")
    parser.add_argument("--skill", type=str, help="Skill to evaluate (or 'all')")
    parser.add_argument("--benchmark", type=str, help="Specific benchmark ID (optional)")
    parser.add_argument("--list", action="store_true", help="List configured skills")
    parser.add_argument("--dry-run", action="store_true", help="Validate config without running evals")
    parser.add_argument("--runs", type=int, help="Override runs_per_item from config")
    args = parser.parse_args()

    config = load_config()

    if args.list:
        list_skills(config)
        return

    if not args.skill:
        parser.print_help()
        return

    judge_config = config["judge"]
    if args.runs:
        judge_config["runs_per_item"] = args.runs

    langfuse = init_langfuse()
    anthropic_client = None if args.dry_run else init_anthropic()

    skills_to_eval = (
        list(config["skills"].keys())
        if args.skill == "all"
        else [args.skill]
    )

    for skill_name in skills_to_eval:
        if skill_name not in config["skills"]:
            console.print(f"[red]Unknown skill: {skill_name}[/red]")
            console.print(f"Available: {', '.join(config['skills'].keys())}")
            continue

        skill_config = config["skills"][skill_name]
        console.print(f"\n[bold blue]Evaluating: {skill_name}[/bold blue]")
        console.print(f"  {skill_config['description']}")

        if args.dry_run:
            console.print("  [yellow]Dry run — validating config only[/yellow]")
            dims = skill_config["rubric"]["dimensions"]
            total_weight = sum(d["weight"] for d in dims.values())
            console.print(f"  Dimensions: {len(dims)} (total weight: {total_weight:.2f})")
            if abs(total_weight - 1.0) > 0.01:
                console.print(f"  [red]Warning: weights sum to {total_weight}, expected 1.0[/red]")
            for b in skill_config.get("benchmarks", []):
                files = b.get("input_files") or [b.get("input_file", "")]
                missing = [f for f in files if not resolve_path(f).exists()]
                if missing:
                    console.print(f"  [red]Missing files for {b['id']}: {missing}[/red]")
                else:
                    console.print(f"  [green]Benchmark {b['id']}: all files found[/green]")
            continue

        ensure_dataset(langfuse, skill_config)

        benchmarks = skill_config.get("benchmarks", [])
        if args.benchmark:
            benchmarks = [b for b in benchmarks if b["id"] == args.benchmark]
            if not benchmarks:
                console.print(f"[red]Benchmark '{args.benchmark}' not found[/red]")
                continue

        all_results = {}
        for benchmark in benchmarks:
            results = evaluate_benchmark(
                anthropic_client=anthropic_client,
                langfuse=langfuse,
                skill_name=skill_name,
                skill_config=skill_config,
                benchmark=benchmark,
                judge_config=judge_config,
            )
            if results:
                all_results[benchmark["id"]] = results

        if all_results:
            print_results(skill_name, all_results)

    if langfuse:
        langfuse.flush()
        console.print("\n[green]Scores sent to Langfuse. View at your Langfuse dashboard.[/green]")


if __name__ == "__main__":
    main()

"""
Annotation Helper — Fetch Langfuse traces and propose skill improvements.

This is the "Phase 1" loop from the Langfuse blog post:
    1. Fetch recent traces + annotations from Langfuse
    2. Group by annotation category
    3. Analyze patterns
    4. Propose specific SKILL.md changes

Usage:
    python annotate.py --skill transcript-to-meeting-notes --days 7
    python annotate.py --skill generate-requirements --category hallucinated-business-rule
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

console = Console()


def load_config() -> dict:
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def fetch_annotated_traces(langfuse, skill_name: str, days: int, category: str | None = None):
    """Fetch recent traces with scores/annotations for a skill."""

    from_timestamp = datetime.now() - timedelta(days=days)

    traces = langfuse.fetch_traces(
        name=f"eval-{skill_name}",
        from_timestamp=from_timestamp,
    )

    annotated = []
    for trace in traces.data:
        scores = langfuse.fetch_trace(trace.id)
        if scores and hasattr(scores, "scores") and scores.scores:
            trace_scores = []
            for s in scores.scores:
                if category is None or s.name == category:
                    trace_scores.append({
                        "name": s.name,
                        "value": s.value,
                        "comment": s.comment,
                    })
            if trace_scores:
                annotated.append({
                    "trace_id": trace.id,
                    "name": trace.name,
                    "metadata": trace.metadata,
                    "scores": trace_scores,
                })

    return annotated


def analyze_patterns(traces: list, skill_config: dict) -> dict:
    """Analyze score patterns across traces to find systematic issues."""

    dim_scores = {}
    for trace in traces:
        for score in trace["scores"]:
            name = score["name"]
            if name not in dim_scores:
                dim_scores[name] = {"values": [], "comments": []}
            dim_scores[name]["values"].append(score["value"])
            if score.get("comment"):
                dim_scores[name]["comments"].append(score["comment"])

    analysis = {}
    for dim_name, data in dim_scores.items():
        values = data["values"]
        if not values:
            continue
        avg = sum(values) / len(values)
        analysis[dim_name] = {
            "avg_score": avg,
            "min_score": min(values),
            "max_score": max(values),
            "count": len(values),
            "needs_attention": avg < 0.7,  # below 3.5/5 normalized
            "sample_comments": data["comments"][:5],
        }

    return analysis


def print_analysis(skill_name: str, analysis: dict):
    """Print pattern analysis as a table."""

    table = Table(title=f"Score Patterns: {skill_name}", show_lines=True)
    table.add_column("Dimension", style="cyan")
    table.add_column("Avg", justify="center")
    table.add_column("Range", justify="center")
    table.add_column("N", justify="center")
    table.add_column("Needs Work?", justify="center")
    table.add_column("Sample Comments")

    for dim_name, data in sorted(analysis.items(), key=lambda x: x[1]["avg_score"]):
        avg = data["avg_score"]
        color = "green" if avg >= 0.8 else "yellow" if avg >= 0.6 else "red"
        attention = "[red]YES[/red]" if data["needs_attention"] else "[green]no[/green]"
        comments = "; ".join(data["sample_comments"][:2])[:80]

        table.add_row(
            dim_name,
            f"[{color}]{avg:.0%}[/{color}]",
            f"{data['min_score']:.0%}-{data['max_score']:.0%}",
            str(data["count"]),
            attention,
            comments,
        )

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Annotation Pattern Analyzer")
    parser.add_argument("--skill", type=str, required=True, help="Skill name")
    parser.add_argument("--days", type=int, default=7, help="Look back N days")
    parser.add_argument("--category", type=str, help="Filter to specific annotation category")
    args = parser.parse_args()

    config = load_config()
    if args.skill not in config["skills"]:
        console.print(f"[red]Unknown skill: {args.skill}[/red]")
        return

    from langfuse import Langfuse
    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )

    console.print(f"[bold]Fetching traces for {args.skill} (last {args.days} days)...[/bold]")
    traces = fetch_annotated_traces(langfuse, args.skill, args.days, args.category)

    if not traces:
        console.print("[yellow]No annotated traces found. Run eval_runner.py first to generate scores.[/yellow]")
        return

    console.print(f"Found {len(traces)} annotated traces.")

    analysis = analyze_patterns(traces, config["skills"][args.skill])
    print_analysis(args.skill, analysis)

    weak_dims = [name for name, data in analysis.items() if data["needs_attention"]]
    if weak_dims:
        console.print(f"\n[bold red]Dimensions needing attention:[/bold red] {', '.join(weak_dims)}")
        console.print(
            "\n[bold]Next step:[/bold] Open the Langfuse dashboard to review individual traces "
            "for these dimensions. Then ask Claude to analyze the patterns and propose SKILL.md changes."
        )
    else:
        console.print("\n[green]All dimensions scoring well. No immediate SKILL.md changes needed.[/green]")


if __name__ == "__main__":
    main()

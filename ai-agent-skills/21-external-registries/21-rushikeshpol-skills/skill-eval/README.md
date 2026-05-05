# Skill Evaluation Harness

Langfuse-integrated evaluation framework for measuring and improving Cursor agent skills. Uses LLM-as-Judge to score skill outputs across defined quality dimensions, with full observability into what's working and what's not.

## Architecture

```
config.yaml          ← Skill definitions, rubrics, benchmarks
     │
     ├── eval_runner.py    ← Runs benchmarks, sends scores to Langfuse
     ├── annotate.py       ← Fetches Langfuse traces, finds weak dimensions
     └── judge_prompts.py  ← LLM-as-Judge prompt templates
```

**The loop:**

```
1. Run eval_runner.py against benchmarks
         │
2. Review scores in Langfuse dashboard
         │
3. Edit SKILL.md to fix weak dimensions
         │
4. Re-run eval_runner.py to measure improvement
         │
5. Use annotate.py to find patterns across runs
```

## Setup

### 1. Install dependencies

```bash
cd skill-eval
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env with your Langfuse and Anthropic keys
```

**Langfuse options:**
- **Cloud:** Sign up at https://cloud.langfuse.com, create a project, copy API keys
- **Self-hosted:** `docker compose up -d` from https://langfuse.com/docs/deployment/self-host

### 3. Validate config

```bash
python eval_runner.py --dry-run --skill all
```

This checks that all benchmark files exist and rubric weights sum to 1.0.

## Usage

### List configured skills

```bash
python eval_runner.py --list
```

### Run evaluation for a skill

```bash
# Evaluate all benchmarks for a skill (3 judge runs per dimension for stability)
python eval_runner.py --skill transcript-to-meeting-notes

# Evaluate a specific benchmark
python eval_runner.py --skill generate-requirements --benchmark attestation-from-discovery

# Evaluate all skills
python eval_runner.py --skill all

# Quick single-run evaluation (faster, less stable)
python eval_runner.py --skill generate-requirements --runs 1
```

### Analyze score patterns

After running evaluations, use the annotator to find systematic weaknesses:

```bash
# See score patterns across recent evaluation runs
python annotate.py --skill generate-requirements --days 7

# Filter to a specific issue category
python annotate.py --skill generate-requirements --category hallucinated-business-rule
```

## What Gets Evaluated

### transcript-to-meeting-notes

| Dimension | Weight | What It Checks |
|-----------|--------|---------------|
| decision_capture | 25% | All transcript decisions appear in Decisions table with attribution |
| attribution_accuracy | 20% | Claims attributed to correct speaker |
| information_fidelity | 25% | No hallucinated facts or outside information |
| completeness | 15% | All major transcript topics covered |
| template_compliance | 15% | All 8 required sections present in order |

### generate-requirements

| Dimension | Weight | What It Checks |
|-----------|--------|---------------|
| source_accuracy | 25% | (Source: SRC-N) citations verifiable against source docs |
| requirement_purity | 20% | FRs describe WHAT, not HOW or UI layout |
| no_hallucination | 25% | No invented business rules; unknowns marked [TBD] |
| completeness | 15% | All functional areas from sources covered |
| template_compliance | 15% | Feature Requirements template followed |

### validate-requirements

| Dimension | Weight | What It Checks |
|-----------|--------|---------------|
| true_positive_rate | 30% | Real issues found with correct severity |
| false_positive_rate | 25% | No spurious findings |
| actionability | 25% | Findings are specific with location + fix |
| report_quality | 20% | Report template followed, scores consistent |

## Adding Benchmarks

Add a new benchmark in `config.yaml` under the skill's `benchmarks` list:

```yaml
- id: "new-benchmark-name"
  input_description: "Description of the test case"
  input_files:
    - "path/to/input1.md"
    - "path/to/input2.md"
  gold_reference: "path/to/known-good-output.md"  # optional
  expected_frs: ["FR-1 name", "FR-2 name"]  # evaluation anchors
  critical_constraints: ["Must do X", "Never do Y"]
```

## Adding a New Skill

1. Add the skill definition to `config.yaml` under `skills:`
2. Define rubric dimensions with weights summing to 1.0
3. Add at least one benchmark with input files
4. Add annotation categories to `judge_prompts.py` `ANNOTATION_CATEGORIES`
5. Run `--dry-run` to validate

## Interpreting Results

| Composite Score | Meaning |
|----------------|---------|
| 4.5 - 5.0 | Excellent — skill is production-ready |
| 3.5 - 4.4 | Good — minor issues, safe to use with review |
| 2.5 - 3.4 | Needs work — specific dimensions need SKILL.md fixes |
| < 2.5 | Significant issues — major SKILL.md rewrite needed |

**Score spread** (shown in results table) indicates judge consistency. A spread of 1-2 points suggests the dimension is ambiguous or the rubric needs tightening.

## How Scoring Works

- Each dimension is scored 1-5 by the LLM judge
- Multiple runs per item (default: 3) with median used for stability
- Dimensions are weighted per the rubric config
- Composite = weighted sum of dimension scores
- All scores are sent to Langfuse with full trace lineage

## The Improvement Workflow

### Phase 1: Quick wins (no Langfuse needed)

```bash
# Run with --runs 1 for fast feedback
python eval_runner.py --skill generate-requirements --runs 1

# See which dimensions score low
# Edit the SKILL.md to address weak dimensions
# Re-run to check improvement
```

### Phase 2: Systematic improvement (with Langfuse)

1. Run full evaluations (`--runs 3`) to get stable baselines
2. Review traces in Langfuse dashboard — click into individual judge runs
3. Use `annotate.py` to find patterns across benchmarks
4. Make targeted SKILL.md changes based on evidence
5. Re-run and compare scores in Langfuse experiment view

### Phase 3: Production monitoring

Once skills are deployed and producing real artifacts:
1. Instrument your skill invocations with Langfuse tracing
2. Annotate real outputs (not just benchmarks) with the score categories
3. Use `annotate.py` to surface regressions
4. Feed real-world annotations back into benchmark suite

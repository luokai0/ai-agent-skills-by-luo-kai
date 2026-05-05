"""
LLM-as-Judge prompt templates for skill evaluation.

Each judge prompt scores one dimension of a skill's output quality.
Prompts are designed to return structured JSON for Langfuse score ingestion.
"""

SYSTEM_PROMPT = """You are an expert evaluator assessing the quality of AI-generated product management artifacts.
You evaluate strictly against a scoring rubric. You never invent information — you only assess what's in front of you.
You always return valid JSON."""


def build_judge_prompt(
    dimension_name: str,
    dimension_description: str,
    scoring_rubric: str,
    skill_output: str,
    source_material: str,
    expected_items: dict | None = None,
) -> str:
    expected_section = ""
    if expected_items:
        items_text = "\n".join(
            f"- **{k}:** {', '.join(v) if isinstance(v, list) else v}"
            for k, v in expected_items.items()
        )
        expected_section = f"""
## Expected Items (use as evaluation anchors, not exhaustive)
{items_text}
"""

    return f"""## Task
Evaluate the following skill output on the dimension: **{dimension_name}**

## Dimension
{dimension_description}

## Scoring Rubric
{scoring_rubric}

{expected_section}
## Source Material (ground truth)
<source_material>
{source_material[:15000]}
</source_material>

## Skill Output (to evaluate)
<skill_output>
{skill_output[:15000]}
</skill_output>

## Instructions
1. Read the source material carefully — this is ground truth.
2. Read the skill output — this is what you're evaluating.
3. Apply the scoring rubric strictly for the dimension "{dimension_name}".
4. Provide specific evidence for your score (quote from output and source).

## Required Output Format (strict JSON)
Return ONLY this JSON object, no other text:
{{
  "dimension": "{dimension_name}",
  "score": <integer 1-5>,
  "confidence": <float 0.0-1.0>,
  "evidence": [
    {{
      "finding": "<what you observed>",
      "location": "<where in the output>",
      "source_check": "<what the source actually says, or 'N/A' if not applicable>"
    }}
  ],
  "summary": "<1-2 sentence summary of the evaluation>"
}}"""


ANNOTATION_CATEGORIES = {
    "transcript-to-meeting-notes": [
        "missing-decision",
        "wrong-attribution",
        "hallucinated-fact",
        "missing-topic",
        "template-violation",
    ],
    "generate-requirements": [
        "inaccurate-source-citation",
        "hallucinated-business-rule",
        "solution-in-requirement",
        "design-in-requirement",
        "missing-functional-area",
        "missing-tbd-marker",
        "wrong-actor",
    ],
    "validate-requirements": [
        "false-positive-finding",
        "missed-real-issue",
        "vague-finding",
        "wrong-severity",
        "inconsistent-score",
    ],
}

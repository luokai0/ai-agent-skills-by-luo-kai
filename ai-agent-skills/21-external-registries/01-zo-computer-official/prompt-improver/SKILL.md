---
name: prompt-improver
description: "Improve and optimize prompts for Claude using Anthropic's official best practices and the 5-Element Persona Framework. Use when asked to improve, refine, optimize, or review a prompt. Also triggers on requests to make prompts clearer, more effective, better structured, or to get better/more realistic outputs from Claude. Covers Claude 4.x-specific techniques, persona engineering, constraint-based prompting, and structured outputs."
metadata:
  author: skeletorjs
---
# Prompt Improver

Analyze and improve prompts using Anthropic's official best practices and the 5-Element Persona Framework.

## Workflow

### Step 1: Identify the Prompt & Intent
- Get the prompt if not provided
- Clarify: Is this for Claude 4.x? API or chat interface?
- Understand: What outcome does the user want to improve?

### Step 2: Diagnose the Core Issue
Quick triage against common failure modes:

| Symptom | Likely Cause |
|---------|--------------|
| Generic/shallow output | Missing persona depth or constraints |
| Wrong format | No output specification or examples |
| Inconsistent results | Needs few-shot examples with reasoning |
| Unrealistic suggestions | Missing constraints (budget/time/resources) |
| Ignores instructions | Needs XML structure or system/user separation |
| Verbose/over-engineered | Missing explicit direction (Claude 4.x issue) |
| Off-topic responses | Lacks context about purpose/audience |

### Step 3: Apply the 5-Element Persona Framework
For any prompt involving expertise or role-play, ensure ALL five elements:

1. **Role + Seniority** — "Senior Backend Engineer with 8 years..."
2. **Industry/Domain Context** — "B2B SaaS in fintech, enterprise customers"
3. **Methodologies** — "Uses JTBD framework, presents at 95% confidence"
4. **Constraints** — "$50K budget, 6-week timeline, team of 3"
5. **Output Format** — "2-page executive brief with 3 options + recommendation"

Constraints are the game-changer—without them, Claude gives fantasy answers.

See `references/persona-framework.md` for templates and examples.

### Step 4: Apply Structural Techniques
Select techniques based on the diagnosed issue:

| Issue | Technique |
|-------|-----------|
| Complex reasoning needed | Chain of thought with `<thinking>` tags |
| Multiple components | XML tag structure |
| Format compliance | Prefill (API) + XML output tags |
| Inconsistent outputs | Few-shot WITH reasoning (input→reasoning→output) |
| Instruction injection risk | System/User separation |

See `references/techniques.md` for implementation details.

### Step 5: Apply Claude 4.x Optimizations
Modern Claude models require explicit direction:

- **Be explicit**: Add "Go beyond basics" if you want comprehensive output
- **Explain the why**: Context behind instructions improves compliance
- **Tell what TO do**: Not "don't use jargon" → "Use plain language a 10th grader understands"
- **Match prompt style to output**: Reduce markdown in prompt → less markdown in output
- **Opus 4.5**: Add "Keep solutions simple" to prevent over-engineering

### Step 6: Generate the Improved Prompt
Produce the complete improved prompt using this structure:

```
[SYSTEM PROMPT - when using API or Projects]
You are [role + seniority] with [X years] in [industry/domain].
You specialize in [expertise]. 
Your approach: [methodologies/frameworks]
Your constraints: [budget/time/resources/tradeoffs]
Deliver: [specific output format]

[USER PROMPT]
<context>
[Background, purpose, audience, success criteria, WHY this matters]
</context>

<instructions>
[Clear, numbered steps - tell what TO do, not what NOT to do]
</instructions>

<constraints>
[Negative constraints: "Never assume X", "Do not exceed Y words"]
</constraints>

<examples>
[2-3 examples showing: INPUT → REASONING → OUTPUT]
</examples>

<output_format>
[Exact structure with XML tags for reliable parsing]
</output_format>

[Actual task/content to process]
```

## When to Load References

- **`references/techniques.md`** — For detailed technique explanations, API-specific guidance (prefilling), extended thinking tips, or system/user separation patterns
- **`references/persona-framework.md`** — When building expert personas, role-based prompts, or adding constraints to get realistic outputs
- **`references/examples.md`** — When the user needs before/after demonstrations or few-shot patterns

---
name: prompt-engineering-expert
version: 1.0.0
description: Master prompt engineering for production AI systems. Covers system prompts, chain-of-thought, few-shot learning, structured outputs, and prompt optimization.
author: luo-kai
tags: [prompt-engineering, llm, chain-of-thought, few-shot, system-prompts, structured-output]
---

# Prompt Engineering Expert

## Before Starting
1. What model are you prompting — GPT-4, Claude, Gemini, local?
2. Task type — extraction, classification, generation, reasoning, coding?
3. Consistency requirement — needs structured output or free-form is fine?

## Core Expertise Areas

### System Prompt Design
System prompt sets the model's persona, constraints, and output format.
Be explicit about what to do AND what not to do.
Specify the output format exactly — JSON, markdown, plain text.
Include examples when behavior is ambiguous.
Test system prompt changes on a diverse set of inputs before deploying.

### Chain-of-Thought Prompting
Add "Think step by step" or "Let's reason through this" for complex tasks.
CoT improves accuracy on math, logic, and multi-step reasoning significantly.
Zero-shot CoT: just append "Think step by step." to the user prompt.
Few-shot CoT: show 2 to 3 examples with explicit reasoning chains.
Self-consistency: run same prompt 5 times, take majority vote answer.

### Few-Shot Learning
2 to 5 examples in the prompt often outperform 0-shot dramatically.
Examples must be diverse — do not use identical structure.
Order matters: hardest examples last, easiest first.
Format examples identically to how you want the output.
Dynamic few-shot: retrieve the most similar examples to current query.

### Structured Output
Ask for JSON directly in the system prompt.
Specify exact schema: field names, types, nested objects.
Use Pydantic or JSON Schema to validate model output.
Retry on parsing failure with error message included in retry prompt.
OpenAI function calling / tool use enforces schema more reliably than asking.

### Prompt Optimization
A/B test prompts on a diverse eval set before production changes.
Measure: accuracy, consistency, output length, latency.
DSPy: automatic prompt optimization using gradient-like feedback.
Prompt compression: remove redundant words — shorter prompts are cheaper.
Temperature: 0 for extraction/classification, 0.7 for creative generation.

## Key Patterns

### Production System Prompt Template
```
You are [specific role] for [specific context].

Your task: [exact task description]

Rules:
- [constraint 1]
- [constraint 2]
- NEVER [what to avoid]

Output format:
[exact format specification, JSON schema, or example]

If you are unsure, [fallback behavior].
```

### Few-Shot Classification Prompt
```
Classify the sentiment of each review as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The product arrived quickly and works perfectly."
Sentiment: POSITIVE

Review: "Completely broken on arrival. Waste of money."
Sentiment: NEGATIVE

Review: "It is okay, does the job but nothing special."
Sentiment: NEUTRAL

Review: "{user_review}"
Sentiment:
```

### Structured JSON Extraction
```python
from openai import OpenAI
from pydantic import BaseModel

class ExtractedData(BaseModel):
    name: str
    email: str
    company: str | None
    intent: str

client = OpenAI()

def extract_contact(text: str) -> ExtractedData:
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract contact information from the text."},
            {"role": "user", "content": text}
        ],
        response_format=ExtractedData
    )
    return response.choices[0].message.parsed
```

### Chain-of-Thought for Reasoning
```
Solve the following problem. Show your full reasoning before giving the answer.

Problem: A store buys items for $60 and sells them with a 40% markup.
After a 15% discount promotion, what is the final selling price?

Reasoning: Let me work through this step by step.
Step 1: Calculate the selling price with markup.
  Markup amount = $60 * 0.40 = $24
  Selling price = $60 + $24 = $84

Step 2: Apply the 15% discount.
  Discount amount = $84 * 0.15 = $12.60
  Final price = $84 - $12.60 = $71.40

Answer: $71.40
```

## Best Practices
- Be specific — vague prompts produce vague outputs
- Show examples — they outperform instructions alone almost every time
- Constrain the output format explicitly — saves parsing headaches
- Test on diverse inputs before deploying — edge cases expose prompt brittleness
- Version control your prompts — treat them like code with commits

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Underspecified prompt | Model guesses and guesses wrong | Add explicit instructions for every edge case |
| No output format specification | Inconsistent structure, broken parsing | Always specify exact format or JSON schema |
| Single example | Model learns wrong pattern | Use 3 to 5 diverse examples |
| Temperature too high for factual tasks | Hallucinations and inconsistency | Use temperature 0 for extraction and classification |
| No eval set | Prompt regressions undetected | Build 50+ test cases before optimizing |

## Related Skills
- llm-engineering-expert
- agent-memory-expert
- rag-systems-expert
- mcp-builder-expert

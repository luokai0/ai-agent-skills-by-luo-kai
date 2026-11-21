---
name: nutrition-meal-planning
description: Use when drafting, adjusting, or reviewing multi-day meal plans that must meet stated energy, macronutrient, food-group, budget, or dietary-restriction requirements for a healthy adult or household, not for diagnosing or treating disease.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Nutrition Meal Planning

## Purpose and boundaries

This skill produces practical, multi-day meal plans with shopping lists, portion guidance, and a nutritional check against stated targets. It covers general healthy-adult eating, common preferences (vegetarian, lower-sodium, high-protein, budget-limited), and routine restrictions such as lactose avoidance or gluten avoidance for non-celiac preferences.

It does not cover: diagnosing conditions, prescribing therapeutic diets (renal, insulin-dependent diabetes management, enteral or tube feeding, oncology, eating-disorder recovery), planning for infants, pregnancy, or lactation, or adjusting medication-related intake. Route these to a registered dietitian or treating clinician and stop after producing only general, non-therapeutic guidance.

## Inputs and assumptions

Collect before planning:
1. Age band, sex, height, weight, activity level (or a stated energy target from a clinician or prior plan).
2. Number of people and meals per day to cover (for example, 3 meals plus 1 snack, 7 days).
3. Restrictions and allergies, stated separately from preferences. Treat allergies as hard exclusions.
4. Budget ceiling per week and cooking capacity (minutes per meal, equipment).
5. Region and available stores, so ingredients are realistic.

If a value is missing, state the assumption in the output header. Do not invent medical history. Estimated energy uses a stated equation (for example, Mifflin-St Jeor with an activity multiplier) and is labeled as an estimate.

## Operating workflow

1. Confirm scope against the boundaries above. If out of scope, stop and say so.
2. Set targets: energy, protein, fiber, sodium ceiling, and food-group servings. Cite the reference source used (for example, the national dietary guidance applicable to the user's region) and mark it "verify against current official guidance."
3. Build a template per day: breakfast, lunch, dinner, snacks, each with a protein source, vegetable or fruit, a whole-grain or starch, and a fat source.
4. Rotate ingredients across days to reduce waste and cost; reuse cooked components (for example, one batch of grains used twice).
5. Generate the consolidated shopping list, grouping by store section and summing quantities.
6. Compute daily totals using a stated nutrient database and record which database and version were used.
7. Run the verification checks below and revise.

## Decision gates

- Allergy or intolerance conflict with any recipe: remove the item; do not substitute silently.
- Daily energy estimate deviates more than 10% from target: adjust portions or add or remove a snack, then recheck.
- Sodium above the stated ceiling: swap processed items for fresh or low-sodium equivalents before finalizing.
- Plan requires more than 45 minutes of active cooking per meal, or exceeds stated budget: simplify or flag the trade-off.
- Request involves a clinical condition, medication interaction, or pediatric or pregnancy use: stop and refer.
- Requires explicit user approval before: sending a plan to a third party, saving or overwriting an existing plan or client record, sharing personal health data, publishing, or charging for a service.

## Verification and evidence

Measurable checks before delivery:
- Every day contains at least one protein source, two vegetable or fruit servings, and one whole-grain or fiber-rich starch.
- Daily fiber, protein, and sodium totals are reported with the database name and version.
- Shopping list total is within the stated budget, with the price basis stated.
- No ingredient appears in the exclusion list, including sauces, stocks, and processed items.
- Each recipe's stated portion count matches the shopping list quantity.
- Any figure that depends on a guideline or database version carries the note: "verify against current official documentation."

Do not claim the plan is guaranteed to produce weight change, disease prevention, or any health outcome.

## Failure handling

- Missing inputs: list them, proceed only with labeled assumptions, and ask for confirmation.
- Targets unreachable within budget or restrictions: report the gap numerically and offer two options.
- Nutrient database unavailable: state that totals are unverified rather than estimating silently.
- Conflicting user statements: ask rather than choose.

## Deliverable contract

Output one document containing, in order:
1. Header: scope, assumptions, targets with sources, nutrient database name and version.
2. Day-by-day plan in a table: meal, dish, portion, energy, protein, fiber, sodium.
3. Consolidated shopping list with quantities and estimated cost.
4. Verification summary: which checks passed and any open items.
5. Referral note if any out-of-scope element was encountered.

Keep prose minimal. Do not include unrequested medical advice, testimonials, or promotional language.
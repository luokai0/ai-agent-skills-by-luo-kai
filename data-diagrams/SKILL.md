---
name: data-diagrams
description: Use when designing, implementing, or reviewing data visualizations in a frontend codebase, including chart type selection, data shaping for charts, interactive tooltips and legends, accessibility of graphics, and visual regression checks.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Data Diagrams

## Purpose and boundaries

Use this skill to turn a dataset and a question into a correct, readable, accessible chart inside a frontend application. It covers chart type selection, data preparation for rendering, component implementation, interaction design, and verification of the rendered output.

Out of scope: statistical modeling, backend query design, dashboard infrastructure, and architecture diagrams (UML, sequence, C4). If the request is primarily about one of those, say so and redirect.

## Inputs and assumptions

Before building, establish:

1. The question the viewer must answer, stated in one sentence.
2. The data shape: field names, types, cardinality, units, time zone for timestamps, null semantics, and expected row counts at p95 load.
3. The rendering target: framework, charting library, and whether output is SVG, canvas, or static image.
4. Constraints: supported browsers, minimum viewport, accessibility target (assume WCAG 2.2 AA unless told otherwise), and performance budget.

If any of these are missing and cannot be read from the repository, ask. Do not guess units or time zones.

Library APIs, option names, and version behavior change. Verify every option you use against the official documentation for the exact version pinned in the project's lockfile.

## Operating workflow

1. **Restate the question.** Write the comparison, trend, distribution, composition, or relationship the chart must show.
2. **Select the encoding.** Apply the decision gates below. Record the chosen chart type and why.
3. **Shape the data.** Write a pure function that converts raw records into the chart's input. Handle nulls explicitly, sort deterministically, aggregate before rendering when rows exceed what the chart can show legibly, and format numbers with the locale in use.
4. **Implement the component.** Keep data transformation separate from rendering. Set explicit axis domains where the data's range is meaningful; do not let a zero baseline be silently dropped for bar charts.
5. **Add semantics.** Provide a text title, a summary sentence stating the key takeaway, and a data table or accessible equivalent for screen readers.
6. **Add interaction only if it serves the question.** Tooltips must show exact values with units. Keyboard focus must reach the same information that hover reveals.
7. **Verify** using the checks below.

## Decision gates

- **Comparison across categories** (up to about 12): horizontal bar, sorted by value. Use vertical bars only for short labels.
- **Change over time** (one or few series): line chart. Use area only when the magnitude of the total matters and the baseline is zero.
- **Part-to-whole**: a stacked bar with at most five segments. Do not use pie or donut charts for more than three slices or for precise comparison.
- **Distribution**: histogram or box plot. State bin width.
- **Relationship between two continuous variables**: scatter plot. Use a log scale only when the data spans several orders of magnitude, and label it.
- **More than about 5,000 points**: aggregate, sample with disclosure, or use canvas rendering. Do not send raw large arrays to SVG.
- **Stop and ask** if the data is categorical with no ordering and the question requires ranking, or if the chart would mislead about causation.

## Verification and evidence

Report each check with its result:

- Rendered output matches the source data for at least three sampled points, including one null and one maximum value.
- Axis units, labels, and scale type are visible and correct.
- Color contrast of data marks and text meets 3:1 for graphics and 4.5:1 for text against background.
- Colors are distinguishable without hue (pattern, shape, or direct labels) and under common color-vision deficiency simulations.
- Keyboard navigation reaches tooltips and legend toggles.
- Chart redraws correctly at 320 px width and at the project's largest supported width.
- Render time for the p95 dataset is measured and within the project's budget. Report the measured number, not an estimate.
- Unit tests cover the data transformation function, including empty input, all-null series, and duplicate timestamps.

Attach screenshots or a test output as evidence. Do not claim a check passed without observing it.

## Failure handling

- **Data does not match the stated question**: report the mismatch and propose the nearest answerable question.
- **Library lacks a needed feature in the pinned version**: check the official changelog for that version before proposing an upgrade. Upgrades require approval.
- **Verification fails**: fix the cause, rerun the failing check, and report both runs. Do not weaken thresholds to pass.
- **Sensitive data appears in the dataset** (personal identifiers, health, financial): stop, do not render it into fixtures or screenshots, and request approval for handling.

## Approval required

Obtain explicit approval before: changing a shared chart library version, altering production data pipelines, committing sample data drawn from real users, publishing dashboards externally, or deleting existing visualizations.

## Deliverable contract

Provide:

1. Chosen chart type with the decision gate that justified it.
2. Files changed, with the transformation function separated from the component.
3. Summary sentence and accessible data alternative as shipped.
4. Verification table: check, method, observed result.
5. Open items, including any library behavior verified only against documentation and not in the running app.

Do not include unverified performance numbers, invented option names, or claims of compliance certification.
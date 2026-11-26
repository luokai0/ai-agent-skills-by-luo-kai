# Research and Evidence

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## autonomous-ai-research

**Use when:** Use when an agent must plan, run, and report multi-step AI or data research (literature and codebase surveys, experiment design, model or data comparisons, reproducibility checks) with minimal supervision but auditable evidence and explicit approval gates.

### Purpose and boundaries

This skill governs end-to-end research tasks in AI and data work: framing a question, gathering sources and data, running bounded experiments, verifying results, and reporting findings with their uncertainty. It covers offline analysis, benchmark comparisons, ablation studies, dataset audits, and evaluation design.

It does not cover: production deployment, model training at a scale that incurs material cost without approval, collection of personal data, publication of results externally, or legal and compliance determinations. Those require a human owner.

### Inputs and assumptions

Before starting, confirm or record:

1. **Research question**: one falsifiable sentence (e.g., "Does retrieval reranking improve answer exact-match on our internal QA set by at least 3 points?").
2. **Success criterion and stop rule**: metric, threshold, compute or time budget, and maximum number of experiment iterations.
3. **Data access**: which datasets, their license terms as stated by the owner, and whether they contain personal or confidential content.
4. **Environment**: available hardware, sandbox boundaries, and network access rules.
5. **Baselines**: at least one existing reference result to compare against.

If any of these is missing, record it as an assumption in the report header. Do not proceed on an assumption that changes the data used or the conclusion.

### Operating workflow

1. **Frame**: restate the question, the metric, and the decision the result will inform. Write the hypothesis and a result that would refute it.
2. **Survey**: collect relevant prior work and internal artifacts. Record each source with title, date, and version. Prefer primary sources and official documentation.
3. **Audit data**: check schema, row counts, duplicates, label balance, train/test leakage, and missingness. Save the audit output.
4. **Design**: list variables, controls, seeds, and the minimal experiment set that can answer the question. Prefer one change per run.
5. **Pilot**: run on a small subset (roughly 1–5% or a fixed small N) to catch pipeline errors before full runs.
6. **Execute**: run experiments with fixed seeds, logged configs, and pinned dependency versions recorded from the environment itself.
7. **Analyze**: compute the pre-declared metric, confidence intervals or variance across seeds, and per-slice breakdowns.
8. **Report**: deliver the artifact contract below.

Keep a running log of every run: config hash, dataset version, command, start and end time, and outcome.

### Decision gates

Stop and request human approval before:

- Deleting, overwriting, or migrating any dataset, checkpoint, or result store.
- Spending compute beyond the approved budget, or launching jobs on shared clusters.
- Sending data, prompts containing internal content, or results to any external service, API, or public repository.
- Using data containing personal, health, financial, or otherwise sensitive attributes, or any data whose use rights are unclear.
- Changing the success criterion after seeing results.
- Making claims that will be used for a product, policy, or customer-facing decision.

Continue autonomously for: reading documents, local read-only analysis, running pre-approved experiments within budget, and writing to the designated scratch directory.

### Verification and evidence

Every reported number must be traceable to a logged run. Apply these checks:

- **Reproduction**: rerun the best configuration with a different seed; the metric must fall within the declared tolerance (default: within one standard deviation of the seed-averaged result).
- **Baseline parity**: confirm the baseline was evaluated with the same data split, preprocessing, and metric implementation.
- **Leakage check**: verify zero overlap of identifiers between train and evaluation splits; document the check command and output.
- **Slice review**: report results on at least the top three data segments by frequency or known risk; flag any segment where the change reverses direction.
- **Significance**: with fewer than 5 seeds or small evaluation sets, state that differences are not established and do not call them improvements.
- **Version sensitivity**: any library behavior, API signature, or benchmark number you cite must be marked for verification against current official documentation or the original source, unless you checked it in this session and record the date.

Do not report numbers from memory. Do not extrapolate beyond the evaluated distribution.

### Failure handling

- **Pipeline error**: fix only if the fix is within scope and reversible; record the diff. Re-run the pilot before full runs.
- **Metric regression or no effect**: report it as a result. Do not iterate beyond the stop rule to find a positive outcome.
- **Non-reproducible result**: mark the claim as unverified, list suspected sources (seed handling, nondeterministic kernels, data ordering, hidden state), and halt dependent conclusions.
- **Missing data or access denied**: stop that branch, record the blocker, and ask the owner. Do not substitute public or synthetic data without approval, and label any substitution clearly.
- **Conflicting sources**: present both, note dates and provenance, and do not average them into a single claim.

### Deliverable contract

The final report must contain, in order:

1. **Question and decision** (one paragraph).
2. **Assumptions and approvals obtained** (table: item, status, approver if any).
3. **Method**: data versions, splits, configs, seeds, environment, and run count.
4. **Results**: primary metric with variance, baseline comparison, slice table, and reproduction outcome.
5. **Verification log**: each check from the evidence section marked pass, fail, or not run, with the reason.
6. **Limitations**: distribution limits, unresolved failures, and claims deliberately not made.
7. **Open items**: approvals still needed and recommended next experiment.
8. **Artifact index**: paths to logs, configs, and scripts.

Quality bar: every claim links to a run ID; no metric appears without its baseline and variance; the report states a clear "supported", "not supported", or "inconclusive" verdict for the original question.
### Evidence-led research execution (v1.1)

Run research as a repeatable pipeline: frame the decision, decompose it into independent questions, define inclusion criteria, search multiple source classes, inspect primary evidence, extract claims, compare conflicts, identify gaps, and synthesize with explicit confidence. Search results are candidate leads, not validated facts.

Prioritize primary sources for specifications, APIs, security advisories, papers, source repositories, and release notes. Use practitioner reports to understand operational behavior and failure modes. Record source URL, publisher, publication or update date, access date, exact claim supported, source type, and confidence. Separate what the source states from the agent's inference.

Deduplicate by canonical URL and underlying claim, but do not collapse independent corroboration. Resolve disagreement by checking dates, version scope, experimental method, and source incentives. If a source is inaccessible, stale, or only a snippet, label the claim accordingly. Never fabricate a citation or infer a current API from old examples.

For technical recommendations, extract prerequisites, supported versions, operational steps, failure modes, security boundaries, and verification commands. Turn reusable findings into capability requirements and tests rather than copying a source's wording or structure. Preserve a research-to-implementation map: each proposed skill improvement links to the requirement it addresses and the validation case that will test it.

Close with known gaps, unanswered questions, confidence limits, and a revalidation trigger such as a major release, security advisory, or material version change.

### Ultron routing contract

**Choose this skill when:** an agent must conduct a multi-stage research task autonomously: formulate questions, plan evidence collection, discover and compare sources, extract claims, track uncertainty, and produce a defensible synthesis.

**Choose `research-retrieval` when:** the work is a bounded source discovery and synthesis task with a defined question and deliverable, without a need for an autonomous multi-stage research plan.

**Choose `web-search-retrieval-and-live-data` when:** the answer depends on current public-web facts, recent updates, live values, or freshness verification at response time.

**Handoff contract:** this skill supplies research objectives, subquestions, source-quality policy, claim schema, and evidence coverage. Retrieval specialists return dated source records and atomic claims; this skill integrates them while preserving provenance, disagreement, and unanswered questions.

**Why the boundary exists:** autonomous research governs the full investigation; retrieval skills provide specialized evidence-acquisition paths within that investigation.

### Research protocol integrity and evidence coverage (v1.2)

#### Freeze the investigation protocol before interpreting results

For decision-sensitive research, create a compact protocol before reviewing outcome evidence. Record the decision question, subquestions, inclusion and exclusion criteria, source classes to search, date and version boundaries, languages, search locations, extraction fields, quality rules, and stopping conditions. Mark any later protocol amendment with its reason, timestamp, and whether it was made before or after seeing relevant results. This makes exploratory changes visible and reduces outcome-driven scope drift.

Separate discovery from eligibility: a search hit is a candidate, not an included source. Maintain a source ledger with stable ID, canonical URL or artifact digest, title, publisher or owner, publication/update date, access date, version, source class, screening decision, exclusion reason, and full-text availability. Record searches that returned no useful results as well as successful searches.

#### Measure coverage without pretending it is exhaustive

Build a question-to-evidence matrix. For every subquestion, list the source classes and systems searched, the claims found, the evidence quality, unresolved contradictions, and unsearched areas. Distinguish “searched and found none” from “not searched”, “inaccessible”, and “not reported”. A zero-result search is evidence about the search process, not proof that no evidence exists.

Define a practical stopping rule before searching: for example, all named primary sources checked, all required source classes searched, and no material new claim or source family discovered in a specified number of consecutive search iterations. If the rule is not met, report the search as incomplete. Do not describe a bounded search as exhaustive merely because the result set feels sufficient.

#### Preserve negative, null, and contradictory findings

Extract null results, failed replications, adverse outcomes, limitations, and author-reported caveats with the same care as positive findings. Search for corrections, retractions, errata, superseding specifications, and later releases where these could change a claim. Do not infer absence of effect from a non-significant result; inspect the estimate, uncertainty interval, sample size, and power limitations where reported.

When a source reports a result that conflicts with the hypothesis, keep it in the claim ledger. Do not discard it because its method is inconvenient unless a predeclared eligibility or quality rule justifies exclusion. Record whether the conflict is substantive, methodological, temporal, population-specific, or only apparent because terms or metrics differ.

#### Validate each material claim at its source

Before using a claim, open the cited primary passage, table, figure, API reference, or dataset record. Verify that it supports the exact proposition and that the context, version, date, units, and qualifications have not been lost. For numerical claims, capture numerator, denominator, unit, population, time window, and uncertainty where available. For versioned technical behavior, record the tested version and a reproducible check rather than relying on a search snippet or copied example.

Maintain explicit claim states: candidate, source-checked, independently corroborated, contradicted, stale, inaccessible, or unresolved. Only source-checked claims may be presented as directly supported. Corroboration must be genuinely independent; multiple pages repeating one upstream statement count as one lineage.

#### Calibrate uncertainty and communicate the boundary

For each decision-critical conclusion, identify the strongest supporting evidence, strongest contrary evidence, key assumptions, plausible alternative explanations, and what observation would change the conclusion. Distinguish confidence in source accuracy from confidence that the evidence transfers to the target decision. Do not convert a qualitative judgment into a numeric probability unless a defensible calibration method exists.

If evidence is too weak, stale, inaccessible, or non-transferable, narrow the conclusion or return “inconclusive”. State the exact boundary: which population, version, date range, task family, language, or operating condition was not established. Provide the smallest next research action that would reduce the uncertainty, with its expected decision value and cost.

#### Revalidation triggers

Attach a review trigger to claims whose validity can decay: major software releases, API deprecations, security advisories, new benchmark versions, changes in pricing or service limits, corrected papers, or a material change in the target population. Record the trigger and owner in the research artifact. A future agent should re-check the claim when the trigger fires rather than treating an old finding as permanently current.


## research-ideation

**Use when:** Use when turning a data or AI problem, dataset, or observed phenomenon into a set of testable research or project hypotheses, prioritized by value, feasibility, and risk, before any large experiment or build commitment is made.

### Purpose and boundaries

This skill produces ranked, testable research or project ideas in data science and AI. It covers problem framing, hypothesis generation, literature and prior-art scoping, feasibility assessment, and experiment design sketches. It does not execute experiments, train production models, make compliance determinations, or commit resources. Output is a proposal for a human decision-maker.

### Inputs and assumptions

Collect before generating ideas:
- Problem statement or business/research question, and who will act on the result.
- Available data: sources, schema, volume, label availability, collection date range, known gaps and biases.
- Constraints: compute budget, timeline, team skills, deployment target, latency and cost limits.
- Success criteria: a metric the stakeholder accepts, and the threshold that would count as a win.
- Prior work already attempted, if any.

If any of these are missing, state the assumption explicitly in the output and mark affected ideas as conditional. Do not silently fill gaps with plausible-sounding specifics.

### Operating workflow

1. Restate the problem in one sentence with the decision it informs. If the decision is unclear, stop and ask.
2. Characterize the data: unit of observation, target definition, label source and its noise, temporal structure, leakage risks (features computed after the outcome, post-treatment variables), and class or subgroup imbalance.
3. Generate 8–15 candidate hypotheses spanning at least three families where applicable: data-centric (cleaning, labeling, new signals), modeling (architecture or method change), problem reformulation (different target, ranking vs. classification, causal vs. predictive), and evaluation (better metric, slice analysis, calibration).
4. For each candidate, write a falsifiable form: "If X, then Y will change by at least Z on metric M over holdout H; if not, we reject this direction."
5. Score each on four axes, 1–5 each: expected value to the decision, feasibility with stated resources, cost to test (time and compute), and risk (privacy, fairness, reproducibility, misuse).
6. Check prior art: search for existing methods and published results on the same task type. Record sources you actually consulted; do not cite from memory without marking it unverified.
7. Select a shortlist of 3–5 with a cheapest-informative-test for each: the smallest experiment that could kill the idea.
8. Produce the deliverable contract below.

### Decision gates

- **Gate A (framing):** Proceed only if the decision owner and success metric are named. Otherwise return with questions.
- **Gate B (data validity):** If label leakage, severe sampling bias, or unavailable ground truth is identified, downgrade all ideas depending on that data until the issue is addressed.
- **Gate C (shortlist):** Advance an idea only if its cheapest test costs under a fixed budget agreed with the requester (default: under 10% of the project's compute or time allocation, if no budget is given, flag this).
- **Gate D (approval):** Any step involving access to sensitive or personal data, use of external APIs or third-party services with user data, deletion or overwrite of datasets, publication of results, or actions affecting people outside the team requires explicit written approval before proceeding. Ideation alone never triggers these actions; plans that include them must be flagged.

### Verification and evidence

- Every numeric claim about expected gains must be labeled as a prior estimate with its basis, or removed.
- Distinguish observed facts (from supplied data or cited sources) from hypotheses.
- Check each hypothesis against the leakage and split checklist: is the holdout temporally or group-separated where needed?
- Confirm each shortlisted test has a pre-registered metric and a decision threshold.
- Mark any library, API, hardware, or version-specific detail as requiring verification against current official documentation.

### Failure handling

- If the problem cannot be stated with a decision owner: return a list of clarifying questions, no ideas.
- If data is insufficient for any hypothesis: say so, and propose data collection as a candidate idea with its own cost estimate.
- If all candidates score low on feasibility: report this honestly and recommend scoping down the question.
- If prior art reveals the idea was already tested: state the result, and only proceed if the new variant differs in a stated, material way.

### Deliverable contract

Return a document with these sections in order:
1. Problem restatement and decision owner.
2. Assumptions and open questions (explicit list).
3. Data characterization, including leakage and bias risks.
4. Ranked candidate table: hypothesis, falsifiable form, four scores, prior-art note, cheapest test.
5. Shortlist (3–5) with test design: data split, metric, threshold, estimated effort range.
6. Approval items: any steps requiring Gate D approval, listed plainly.
7. Version-sensitive items flagged for verification.

Do not: invent benchmark numbers, cite papers or tools not verified, promise performance gains, recommend using personal data without a stated approval path, or present ideas as decided. Keep the tone plain and the claims bounded.


## research-retrieval

**Use when:** Use when an agent must find, gather, and synthesize evidence from documents, web sources, internal knowledge bases, or datasets to answer a research question, and the answer must be traceable to specific sources.

### Purpose and boundaries

This skill governs how an agent locates, filters, reads, and synthesizes sources to answer a bounded research question with citable evidence. It covers literature and document review, competitive or market scans, internal knowledge base lookups, and fact-finding for technical decisions.

In scope: query planning, source discovery, relevance triage, extraction of claims with provenance, cross-source comparison, and a sourced write-up.

Out of scope: making decisions on the user's behalf, publishing or sending findings externally, accessing systems the user has not authorized, scraping behind logins or paywalls, and producing legal, medical, or financial conclusions that require a licensed professional.

### Inputs and assumptions

Before searching, confirm:

1. The research question, stated as a question that can be answered or bounded.
2. Scope limits: time window, geography, languages, source types (for example peer-reviewed only, vendor docs, internal wiki).
3. Available retrieval tools and their access boundaries. Record what each tool can and cannot reach.
4. The intended audience and decision the findings will feed.
5. Freshness requirements. Any claim about software versions, pricing, regulations, or product features is version-sensitive and must be checked against the current official source at the time of work.

If the question is ambiguous, ask one clarifying question with a proposed default rather than guessing silently. Assume no source is current until its date is verified.

### Operating workflow

1. **Decompose.** Split the question into two to five sub-questions. Write each as a falsifiable statement or a specific lookup.
2. **Plan queries.** For each sub-question, write three to five query variants: exact terms, synonyms, the official product or standard name, and a negative variant that surfaces contrary evidence.
3. **Discover.** Run queries, collect candidate sources, and record URL or identifier, title, publisher, date, and retrieval timestamp in a source log.
4. **Triage.** Score each source on authority (primary over secondary), recency (against the freshness requirement), and directness (addresses the sub-question rather than a neighboring topic). Keep sources scoring well on at least two of three; discard the rest with a logged reason.
5. **Read and extract.** For each kept source, extract claims as atomic statements. Each claim record holds: the claim, the exact supporting passage or locator (section, page, timestamp), the source ID, and a confidence tag.
6. **Cross-check.** Group claims by sub-question. Mark each claim as corroborated (two or more independent primary sources), single-sourced, or conflicting.
7. **Synthesize.** Write the answer leading with the direct response, followed by supporting evidence, then conflicts and gaps.
8. **Stop.** Stop when the last two query rounds yield no new relevant primary sources, or when the time budget is reached. Report the stopping reason.

### Decision gates

- **Gate A (scope):** Proceed only when the question and scope limits are confirmed. If the user is unavailable and the question is still ambiguous, proceed on the stated default and label every assumption in the output.
- **Gate B (source access):** Before accessing any source requiring credentials, personal data, or a terms-of-service exception, stop and request explicit approval naming the source and the purpose.
- **Gate C (external impact):** Before sending messages, posting, submitting forms, filing tickets, or contacting third parties with findings or queries, obtain explicit approval. Drafting is permitted; sending is not.
- **Gate D (sensitive content):** If sources contain personal data, confidential material, or security-relevant detail (credentials, vulnerability specifics, unpublished financials), pause, minimize what is quoted, and ask for direction on handling.
- **Gate E (evidence sufficiency):** If a sub-question has zero primary sources, report it as unanswered rather than filling it from memory.

### Verification and evidence

Quality checks, all required before delivery:

- Every factual claim in the synthesis maps to at least one claim record with a locator. Target: 100 percent traceability; any untraced sentence is removed or flagged.
- Every source in the bibliography was actually opened and read at the cited locator. Snippets alone do not count as reading.
- Each source lists a retrieval date. Each version-sensitive claim names the version it applies to and states that it was checked against current official documentation, or marks it unverified.
- At least one contrary-evidence search was run per sub-question, and results are reported even when they are weak.
- Quotations match the source character for character. Spot-check at least three quotes per deliverable.
- Numbers are reported with units, date, and denominator. Do not convert or round without stating it.
- Do not present any benchmark result, statistic, or compliance status that was not found in a retrieved source.

### Failure handling

- **Paywalled, blocked, or unreachable source:** Log the failure, search for an accessible mirror or summary by the same publisher, and otherwise mark the claim as unverified. Do not reconstruct content from memory.
- **Conflicting primary sources:** Report both positions with dates and methods. Do not average or pick a winner without a stated criterion.
- **Stale source contradicted by newer one:** Prefer the newer primary source and note the change.
- **Empty results:** Broaden terms once, then report the gap. Do not loop indefinitely.
- **Tool error or rate limit:** Pause, record the error, retry at most twice with backoff, then report partial results.
- **Suspected fabricated or low-quality source:** Exclude it and log the reason. Do not cite it.

### Deliverable contract

Produce a single document with these parts, in order:

1. **Answer** (under 150 words), stating the direct response and confidence level (high, moderate, low, unanswered).
2. **Scope and assumptions**, including the stated default for any ambiguity.
3. **Findings by sub-question**, each claim followed by its source ID and locator.
4. **Conflicts and gaps**, listing unresolved disagreements and unanswered sub-questions.
5. **Source log**: ID, title, publisher, date, URL or identifier, retrieval date, authority and recency rating, and status (used, excluded with reason).
6. **Search record**: queries run, counts of candidates and kept sources, and stopping reason.

Do not include: unsourced claims, speculative recommendations presented as findings, or content copied beyond what is needed to support a claim.

### Ultron routing contract

**Choose this skill when:** the question requires broad evidence synthesis across multiple source types, such as internal knowledge bases the user authorized, documents, technical references, literature, competitive research, or mixed public/private evidence. It owns research framing, claim extraction, source comparison, uncertainty, and synthesis.

**Choose `web-search-retrieval-and-live-data` when:** the answer depends on current or recent public-web facts, changing product or policy details, live values, recent events, or source freshness that must be checked at response time.

**Handoff contract:** the live-web skill returns dated claims, exact values and units, source URLs, publisher tiers, observation timestamps, and unresolved conflicts. This skill integrates those findings with other authorized evidence while preserving provenance and freshness labels. Never present an internal or older document as proof of a current public fact without checking it.

**Why the boundary exists:** research synthesis is the broader reasoning process; live web retrieval is a specialized acquisition path for facts whose correctness depends on current public evidence.


## research-synthesis-reporting

**Use when:** Use when turning multiple research sources, experiment results, literature, or internal analyses into a decision-ready synthesis report on data or AI topics, including evidence grading, conflict resolution, and recommendation writing.

### Purpose and boundaries

This skill produces a synthesis report that answers a specific question by combining several evidence sources, weighing their quality, stating what is known versus unknown, and recommending an action with explicit confidence. It covers literature reviews for technical decisions, model or method comparisons, experiment result roll-ups, and data-quality or metric investigations.

It does not cover: running new experiments or training jobs, producing raw data pipelines, legal or regulatory opinions, or publishing results externally. If the question requires new data collection, state that as a gap and stop short of collecting it.

### Inputs and assumptions

Before writing, confirm:

1. **Decision question**: one sentence, phrased so a yes/no, choose-A-or-B, or threshold answer is possible. If the question is vague, propose two sharper versions and ask the requester to pick.
2. **Audience and decision owner**: who acts on this and what they already know.
3. **Source set**: list every source with type (peer-reviewed paper, preprint, vendor documentation, internal experiment, dashboard export, interview notes), date, and access status.
4. **Constraints**: deadline, budget, risk tolerance, data-use restrictions.

Assumptions must be written down in a dedicated section. Do not assume a source's results transfer to the requester's data, model, or population without stating the mismatch.

### Operating workflow

1. **Scope the question.** Write the decision question, the outcome metric(s), and the explicit out-of-scope items.
2. **Inventory sources.** Build a table: ID, title, type, date, population or dataset, method, headline claim, reported uncertainty. Mark sources that could not be read in full.
3. **Extract claims atomically.** One row per claim, linked to its source ID and to the exact location (section, table, figure). Do not paraphrase numbers without checking them against the source.
4. **Grade evidence.** Apply the criteria in Decision gates.
5. **Map agreement and conflict.** Group claims by question. For each group, state whether sources agree, disagree, or are silent, and hypothesize reasons for disagreement (dataset shift, metric definition, evaluation protocol, baseline strength, leakage, sample size).
6. **Reconcile numbers.** Where internal figures are cited, recompute at least one from raw inputs or from the stated formula. Record the check.
7. **Draft the synthesis.** Lead with the answer, then the evidence, then the uncertainty, then the recommendation.
8. **Run the verification pass** (see Verification and evidence).
9. **Hand off** using the deliverable contract.

### Decision gates

**Gate 1 — Source admissibility.** Exclude a source if it lacks a stated method, has no identifiable date, or is a secondary summary with no traceable primary. Keep excluded sources in the inventory with a reason.

**Gate 2 — Evidence strength.** Rate each claim:
- Strong: replicated, or independently measured on data relevant to the decision, with reported variance.
- Moderate: single credible source with relevant data and method description.
- Weak: vendor marketing, anecdote, single run without variance, or data off-target for the decision.

A recommendation may rest on strong evidence alone or on moderate evidence only if the report labels it provisional.

**Gate 3 — Transferability.** For each key claim, state whether the population, model scale, language, domain, or time period matches the decision context. Mismatch on any of these downgrades the claim one level.

**Gate 4 — Recommendation readiness.** Proceed to a recommendation only if: the decision question is answered by at least one strong or two moderate transferable claims, and conflicts are either resolved or explicitly bounded. Otherwise, output a "not yet decidable" report that names the specific missing evidence and its cost to obtain.

**Gate 5 — External or sensitive content.** Stop and request explicit approval before including: confidential internal metrics in any document that will leave the team, personal or user data, unpublished partner results, or any claim that will be used in external communications or regulatory filings.

### Verification and evidence

- Every number in the report traces to a source ID and location. Untraceable numbers are removed.
- Every recomputed figure records the inputs and formula.
- Confidence statements use the graded labels above, not adjectives like "clearly" or "significantly." Use "significant" only with a named statistical test and its result from the source.
- Check for common defects: test-set contamination, baselines that were not tuned, metric changes between compared papers, mismatched dataset versions, and results reported only on favorable subsets.
- Version-sensitive facts (library behavior, model capabilities, vendor pricing, platform limits, benchmark leaderboards) must be marked "verify against current official documentation as of [date reviewed]." Do not state them as current facts without that marker.
- Do not invent benchmark scores, compliance certifications, or performance guarantees. If a source is absent, write "not reported."

### Failure handling

- **Conflicting sources with no resolution:** report both positions, the likely cause, and the single experiment or lookup that would resolve it.
- **Missing primary source:** mark the claim unverified; do not upgrade it because a secondary source repeats it.
- **Numbers do not reproduce:** report the discrepancy with both values and stop using the figure until the owner confirms.
- **Requester demands a conclusion the evidence cannot support:** state the strongest supportable conclusion and the gap, then ask for a decision on whether to proceed provisionally.
- **Source access blocked:** list it as unread; never summarize from abstract alone without labeling it.

### Deliverable contract

The report contains, in order:

1. Decision question and scope (including exclusions)
2. Answer or "not yet decidable" statement in two sentences or fewer
3. Recommendation with confidence label and conditions under which it would change
4. Evidence table: claim, source ID, location, grade, transferability
5. Conflicts and proposed resolutions
6. Assumptions and open questions, each with an owner or next step
7. Source inventory with included and excluded entries and reasons
8. Verification log: recomputed figures, version-sensitive items flagged, defects checked

Length target: 4–8 pages for a standard synthesis; a one-page executive version must reproduce items 1–3 exactly.

Do not: present a recommendation without its confidence grade; blend opinion into the evidence table; cite a source you have not read in the portion you rely on; omit excluded sources from the inventory; or release externally without the approval required by Gate 5.

### Cross-source synthesis controls (v1.1)

#### Separate evidence units before combining them

Do not treat every document, experiment, dashboard, interview, and publication as an equivalent observation. Classify each unit as a primary observation, attributed interpretation, secondary synthesis, or decision constraint. A decision constraint shapes the decision but is not empirical evidence that a technical claim is true.

Create a claim-to-evidence graph rather than a flat source list. A claim may depend on multiple observations; one observation may support several claims; and a secondary source may point to primary evidence already inventoried. Record these relationships so repeated reporting of one result is not mistaken for independent agreement.

#### Normalize before comparing

Before ranking methods or combining metrics, record unit of analysis, denominator, population, time window, measurement instrument, missing-data treatment, baseline, and aggregation method. Convert units only when exact and preserve original values. Do not average percentages with different denominators or pool metrics whose definitions merely share a label.

For experiment roll-ups, distinguish a repeated run from an independent replication. Preserve run-level results, sample counts, variance or uncertainty intervals, and the selection rule for the reported result. If only the best run is available, label the evidence as selected rather than representative.

#### Separate association, prediction, and causation

Classify each conclusion as descriptive, predictive, causal, or normative. A predictive association does not establish causation; a causal estimate does not by itself determine the preferred action. For causal claims, inspect assignment mechanism, confounding, selection effects, temporal ordering, and the estimand. If the design cannot support causal inference, rewrite the claim descriptively or predictively.

#### Make uncertainty decision-relevant

For every major conclusion, state the plausible outcome range, assumptions that dominate it, consequence if the estimate is wrong, and evidence that could change the decision. Prefer sensitivity analysis over a confidence adjective. When quantitative uncertainty cannot be calculated, name its source and give a qualitative confidence label with an explicit reason.

#### Stop rules for synthesis quality

- If sources reuse the same underlying dataset, count it once for evidential independence.
- If outcome definitions or denominators cannot be reconciled, present parallel results rather than a pooled number.
- If a material subgroup is missing, do not generalize the aggregate result to it.
- If a conclusion depends on an unverified transformation, reproduce it or label the conclusion provisional.
- If a recommendation changes under a reasonable assumption range, make it conditional and identify the threshold at which it changes.

### Ultron routing contract

**Choose this skill when:** synthesizing heterogeneous evidence into a decision-ready report, especially when sources include internal experiments, operational metrics, technical comparisons, literature, interviews, or mixed evidence types. Its central job is reconciliation, confidence calibration, and recommendation readiness.

**Choose scientific-research-synthesis when:** discovering and screening a defined body of scientific literature or registry records using a reproducible search strategy and inclusion criteria. That skill owns search logs, study screening, extraction, and research-review flow counts.

**Choose scientific-evidence-review when:** checking a specific claim, paper, or conclusion against the evidence it cites.

**Handoff contract:** accept source IDs, primary/secondary classification, exact claim locations, population and method details, uncertainty, and duplicate-lineage links. Return a decision question, claim graph, comparability decisions, conflict register, confidence grades, sensitivity conditions, and evidence gaps. Do not imply a narrative synthesis is exhaustive.

**Why the boundary exists:** research synthesis owns discovery and screening of a scientific corpus; evidence review tests individual claims; this skill reconciles evidence across source types for a decision. This prevents double-counting and false certainty.


## scientific-evidence-review

**Use when:** Use when assessing whether a paper, benchmark result, model card, experiment report, or dataset claim in data science or AI is supported by its evidence, before relying on it for a decision, product choice, or publication.

### Purpose and boundaries

This skill produces a structured judgment on whether specific claims in a data or AI artifact are supported by the evidence presented. It covers research papers, benchmark leaderboards, vendor model cards, internal experiment write-ups, and analytic reports.

It does not cover: writing new experiments from scratch, certifying regulatory or ethical compliance, rating a product's legal status, or replacing domain peer review. Verdicts describe the evidence as presented, not the truth of the underlying phenomenon.

### Inputs and assumptions

Required: the artifact (text, tables, code links, or data access), and the specific claims to assess. If no claims are stated, extract them first and confirm the list with the requester.

Optional but valuable: raw results, code, data splits, hyperparameter ranges, compute budget, and prior versions of the artifact.

Assumptions to record explicitly: the time of review, whether the artifact has been revised, and whether code or data was actually inspected or only described.

### Operating workflow

1. **Freeze the artifact.** Record its identifier, version, date, and a hash or copy of the text. Reviews drift when sources change.
2. **Extract claims.** List each quantitative or causal claim as a single sentence, e.g., "Model X improves accuracy over baseline Y by 4 points on test set Z." Discard framing language that carries no testable content.
3. **Map evidence.** For each claim, identify the table, figure, appendix, or code path that supports it. Mark "no evidence located" when none exists.
4. **Check design validity.** Ask: Is the comparison fair? Are baselines tuned with comparable effort? Is the test set independent of training and model selection? Was data leakage ruled out (duplicates, temporal overlap, preprocessing fit on full data)?
5. **Check statistics.** Look for variance across seeds or folds, confidence intervals, significance tests with stated assumptions, and effect sizes. A difference smaller than observed run-to-run variance is not a demonstrated improvement.
6. **Check reproducibility.** Verify that data, code, seeds, and environment are available or described. Note what is missing.
7. **Assign a verdict** (see Decision gates) and write the rationale with specific pointers.

### Decision gates

Assign one verdict per claim:

- **Supported:** Evidence directly measures the claim, design is fair, variance is reported and the effect exceeds it.
- **Partially supported:** Effect is real under narrower conditions (one dataset, one seed, one baseline) than the claim implies.
- **Unsupported:** Evidence is absent, contradicts the claim, or the comparison is structurally unfair.
- **Not assessable:** Required data, code, or detail is withheld. State exactly what would be needed.

Escalate before proceeding if: the review would require accessing restricted or personal data, re-running training that consumes significant paid compute, contacting authors or vendors, or publishing a critique externally. Obtain explicit approval for each.

### Verification and evidence

Every verdict must cite a location (section, table, figure, or code file) and quote or paraphrase the specific number. Reproduce a reported number only when the requester has approved the compute and data access. Where reproduction is attempted, record the environment and deviations.

Quality checks before delivery:
- Every claim has a verdict and at least one citation.
- No verdict relies on the artifact's own summary alone without checking the table it refers to.
- Reported improvements are compared against stated variance; if variance is absent, the verdict cannot exceed "partially supported."
- Version-sensitive details (library behavior, benchmark splits, metric definitions) are flagged for verification against current official documentation.

### Failure handling

- **Missing numbers:** Mark "Not assessable" and list the missing items. Do not infer values from charts unless labeled as approximate reads.
- **Conflicting numbers across sections:** Report both, identify which is the headline claim, and mark the claim "Unsupported" until reconciled.
- **Suspected leakage without proof:** State the suspicion and the test that would confirm it. Do not assert misconduct.
- **Requester pressure for a favorable verdict:** Restate the evidence standard and deliver the verdict the evidence supports.

### Deliverable contract

Return a single review containing:

1. Artifact identifier, version, and review date.
2. Assumptions and scope exclusions.
3. Claim table: claim, verdict, evidence location, key number, main concern.
4. Reproducibility status: available, partial, or absent, with specifics.
5. Required follow-ups, each marked as needing approval or not.
6. Overall confidence (high, medium, low) with one sentence justifying it.

Do not: invent metrics, cite results not in the artifact, present verdicts as compliance or safety certification, or send any part of the review outside the requester's channel without approval.

### Ultron routing contract

**Choose this skill when:** evaluating whether a specific scientific, technical, or AI claim is actually supported by the evidence presented in a paper, benchmark, model card, experiment report, or analytical artifact.

**Choose scientific-research-synthesis when:** the task is to discover and screen a body of literature or registry sources, extract findings, appraise evidence across studies, and produce a traceable synthesis.

**Handoff contract:** receive the exact claim, cited source passages, methods, data, and reported uncertainty. Return a claim-by-claim verdict, missing evidence, methodological weaknesses, alternative explanations, and confidence limits. A research synthesis can use this review to appraise individual sources before combining them.

**Why the boundary exists:** assessing a known claim is not the same as discovering the literature needed to answer a broader question.


## scientific-research-synthesis

**Use when:** Use when collecting, screening, and synthesizing scientific studies, trial records, or preprints from external registries and bibliographic databases into a sourced evidence summary, review input, or research brief.

### Purpose and boundaries

This skill produces a traceable synthesis of research findings drawn from external sources such as bibliographic databases, clinical trial registries, funder repositories, preprint servers, and regulatory summaries. It covers question framing, search design, screening, data extraction, evidence appraisal, and reporting.

It does not produce clinical recommendations, legal or regulatory conclusions, or new statistical results beyond simple pooling that the user explicitly requests. It does not submit, edit, or post anything to external registries.

### Inputs and assumptions

Required before starting:
- A research question stated as population, exposure or intervention, comparator, outcomes, and study designs of interest (PICO or an equivalent frame).
- The purpose of the output: internal brief, systematic review draft, or decision memo.
- Date range, languages, and geographic scope.
- Access status of each registry or database. Credentials, API keys, and terms of use are the user's responsibility; never request or store them in outputs.

Assumptions to state explicitly in the deliverable: the search snapshot date, the sources actually reachable, and any source that could not be queried.

### Operating workflow

1. **Frame.** Restate the question in one sentence and list inclusion and exclusion criteria. Freeze them before searching.
2. **Map sources.** Choose registries matching the question: trial registries for ongoing or unpublished work, bibliographic databases for published literature, preprint servers for recent work (flagged as unreviewed). Record each source's coverage limits.
3. **Search.** Build one query per source with the same concepts. Log the exact query string, field restrictions, and the date run. Do not invent field tags or syntax; confirm them against each source's current documentation.
4. **Deduplicate.** Match records by identifier first (DOI, registry ID), then by normalized title, first author, and year. Record the merge count.
5. **Screen.** Apply title/abstract screening, then full-text screening, each by two passes where feasible. Record a reason code for every exclusion.
6. **Extract.** Use a fixed extraction sheet: design, sample size, population, intervention, outcome definitions, effect estimate with interval, follow-up, funding, conflicts, registration ID and whether reported outcomes match the registered ones.
7. **Appraise.** Rate risk of bias with an instrument appropriate to the design (for example, a randomized-trial or observational-study tool). Name the tool and version, and verify the version against its current official source.
8. **Synthesize.** Describe findings narratively, grouped by outcome. Pool only when studies are comparable in population, measure, and design. Report heterogeneity rather than hiding it.
9. **Draft and cite.** Attribute every claim to a record ID. Separate what registries say from what publications report.

### Decision gates

- **Gate A (before searching):** Question and criteria frozen and approved by the requester.
- **Gate B (before pooling):** Stop if fewer than two comparable studies exist, or if heterogeneity makes a single estimate misleading. Report narratively instead.
- **Gate C (before external sharing):** Any output containing unpublished registry data, personal data, or proprietary material requires explicit approval before it leaves the working context.
- **Gate D (before posting anywhere):** Any submission, registry update, or message to a third party requires explicit approval, with the exact text shown first.

### Verification and evidence

Quality checks, each must pass or be reported as failed:
- Every included study has a stable identifier and a link or retrieval note.
- Search logs are reproducible: source, query, date, record count.
- Two independent screening decisions agree on at least 90% of records, or disagreements are resolved and logged.
- Each effect estimate is traceable to a specific table, figure, or registry field.
- Outcomes reported in publications are compared with those registered; discrepancies are listed.
- Preprints and non-peer-reviewed sources are labeled.

### Failure handling

- **Source unreachable or rate-limited:** Record the failure, do not substitute memory or recall, and mark the gap in the deliverable.
- **Conflicting numbers across sources:** Report both with sources; do not average silently.
- **Retracted or corrected records:** Check the retraction notice and exclude or annotate.
- **Ambiguous eligibility:** Log the record in an uncertain list and ask the requester rather than deciding alone.

### Deliverable contract

Return:
1. Question, criteria, and snapshot date.
2. Source list with coverage limits and access status.
3. Search logs and PRISMA-style flow counts.
4. Extraction table with record IDs.
5. Risk-of-bias summary with tool names and versions flagged for verification.
6. Narrative synthesis with explicit uncertainty and contradictions.
7. Gaps, limitations, and open questions.

Do not:
- Present unverified citations or identifiers.
- Claim completeness of a search.
- Imply regulatory approval or clinical endorsement.
- Fabricate effect sizes, benchmark results, or version numbers.

### Ultron routing contract

**Choose this skill when:** conducting a structured scientific literature or registry review: framing a research question, designing searches, screening sources, extracting findings, appraising study quality, and synthesizing results with traceable provenance.

**Choose scientific-evidence-review when:** the task is to test a specific claim or artifact against the evidence it cites, rather than discover and synthesize a whole body of research.

**Handoff contract:** this skill supplies the search strategy, inclusion/exclusion criteria, source log, extracted findings, and synthesis. The evidence-review skill returns claim-level support and limitations for important conclusions; integrate those verdicts without overstating certainty or implying causal conclusions unsupported by study design.

**Why the boundary exists:** synthesis answers what the body of evidence suggests; evidence review tests whether an individual claim follows from its stated support.


## web-search-retrieval-and-live-data

**Use when:** Use when a task requires current, time-sensitive, or externally verifiable facts from the web, such as prices, availability, news, regulations, software release status, or public records, and the answer must cite sources and state how fresh the data is.

### Purpose and boundaries

This skill covers finding, retrieving, checking, and reporting live or recent information from public web sources. It produces answers that show where each fact came from, when it was observed, and how confident the evidence makes you.

In scope: query formulation, source selection, page retrieval, extraction of specific values, cross-source comparison, freshness labeling, and cited summaries.

Out of scope: answering from memory when the question is time-sensitive, accessing private or authenticated accounts, bypassing paywalls or access controls, bulk scraping that conflicts with a site's terms or robots directives, and making decisions with legal, medical, or financial consequences without stating that a qualified professional must confirm them.

### Inputs and assumptions

Before searching, pin down:

1. The exact question, including entity names, jurisdiction, and date range.
2. The required output form: a number, a list, a yes/no status, or a narrative.
3. The freshness requirement: "as of today," "in the last 30 days," or "any recent version."
4. The acceptable source tier. Primary sources (official filings, vendor documentation, government registers, original datasets) outrank secondary sources (news, aggregators, forums).

Assume the current date is unknown unless the user or the retrieval tool states it. Record the access date of every retrieved page.

### Operating workflow

1. **Restate the claim to verify** as a single falsifiable sentence.
2. **Plan 2 to 4 queries** that vary terminology: the official name, the product or regulation identifier, and a site-restricted form if the domain is known. Do not repeat near-identical queries.
3. **Rank candidates.** Prefer primary sources, then recent dated pages, then reputable secondary coverage.
4. **Retrieve and read** the relevant sections. Extract the exact value, its unit, its effective date, and the page's publication or update date.
5. **Cross-check** with at least one independent source for any claim that will be relied upon.
6. **Record evidence** in a table: claim, value, source URL, publisher, date observed, date published or updated, source tier.
7. **Resolve conflicts** using the decision gates below.
8. **Write the answer** using the deliverable contract.

### Decision gates

- **Gate A: Is the source primary?** If the only source is secondary, label the finding "reported, not confirmed by primary source."
- **Gate B: Is it fresh enough?** If the page lacks a date, or the date falls outside the required window, do not present it as current. Search again or state the gap.
- **Gate C: Do sources agree?** Two independent agreeing sources support a finding. A single source supports only a tentative finding. Disagreement triggers a note listing both values and likely reasons (different dates, units, regions, or definitions).
- **Gate D: Does the action go beyond reading?** Stop and request explicit approval before any of the following: submitting forms, creating accounts, logging in, posting or messaging, purchasing, downloading files of uncertain origin, running code found online, or sending retrieved personal data elsewhere. Approval must name the specific action.
- **Gate E: Is the data personal?** If results expose identifiable private individuals, limit output to what the user's stated purpose requires and do not compile profiles.

### Verification and evidence

Quality checks before delivering:

- Every numeric or dated claim has a citation with URL and observed date.
- Every "current" claim states its as-of date.
- Each quoted value matches the source text exactly, including units and currency.
- At least one claim per answer was checked against a second source, or the answer says it was not.
- Software versions, prices, legal thresholds, and product specifications are marked "verify against current official documentation before use," because these change frequently.
- No inferred value is presented as retrieved.

### Failure handling

- **No results or blocked page:** Try one alternate query and one alternate source type. If still blocked, report the blocker and what was attempted. Do not guess the content.
- **Paywalled or login-gated:** Use only the visible public abstract or cached public summary, labeled as partial.
- **Conflicting primary sources:** Report both, with dates, and do not pick one silently.
- **Stale results only:** Say so in the first sentence of the answer.
- **Tool or time uncertainty:** State that the date could not be confirmed.

### Deliverable contract

The answer contains, in order:

1. A direct answer in one to three sentences, with the as-of date.
2. An evidence table: claim, value, source, publisher, observed date, confidence (confirmed, single-source, or unresolved).
3. Caveats: conflicts, gaps, and version-sensitive items.
4. Next actions requiring approval, if any, listed separately.

Do not include uncited statistics, invented URLs, or unverified recommendations. Do not present search snippets as full-page findings.

### Ultron routing contract

**Choose this skill when:** a claim depends on current public information, recent developments, live or frequently changing values, official product documentation, current availability, or a public source's publication/update date.

**Choose `research-retrieval` when:** the objective is a broader evidence review that combines multiple source types, internal authorized material, technical documents, literature, or a synthesized decision brief rather than simply establishing current public facts.

**Handoff contract:** return atomic claims with source URL, publisher, publication/update date, observation timestamp, exact value and unit where relevant, confidence, and conflicts. The research skill must preserve those freshness markers when combining them with older or private sources. If the required fact cannot be confirmed from a sufficiently current source, report the gap instead of substituting memory.

**Why the boundary exists:** a current search result is not automatically a complete research synthesis, and a broad research process cannot replace live verification for time-sensitive claims.


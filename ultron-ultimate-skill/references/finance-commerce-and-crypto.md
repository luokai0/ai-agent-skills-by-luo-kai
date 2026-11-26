# Finance, Commerce, and Crypto

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## behavioral-finance

**Use when:** Use when analyzing investor, trader, or client decisions for systematic biases, designing decision-quality safeguards for portfolios or trading processes, or diagnosing why a financial plan or strategy is not being followed as modeled.

### Purpose and boundaries

This skill applies behavioral economics and cognitive psychology to financial decisions: identifying predictable deviations from rational-agent models (biases, heuristics, framing effects, emotional states) and designing processes that reduce their cost. It covers individual investors, trading desks, advisory clients, and investment committees.

In scope: bias diagnosis from trade logs, statements, or decision records; process design (checklists, pre-commitment rules, position-sizing constraints, review cadence); client communication framing; post-mortem analysis of decisions separated from outcomes.

Out of scope: personalized investment, tax, or legal advice; predicting market prices from sentiment; claims that a named bias guarantees future returns; diagnosing clinical conditions. Route those to licensed professionals.

### Inputs and assumptions

Required before analysis:
- Decision record: the decision, the information available at the time, the alternatives considered, and the stated rationale. Outcome data alone is insufficient.
- Context: time horizon, liquidity needs, stated objectives, constraints, and the written policy (if any).
- Behavior data: trade timestamps, position changes, cancellations, reversals, holding periods, and realized versus intended exits.

Assumptions to state explicitly in every output: whether data is complete, the period covered, and whether the subject's rationale was recorded before or after the outcome. Post-hoc rationales carry low evidential weight.

### Operating workflow

1. Separate decision quality from outcome quality. Score the decision against the information available at the time. A good decision can lose money; a poor one can win.
2. Reconstruct the decision timeline. Order events, note what information arrived between them, and mark each entry as recorded-before or recorded-after the outcome.
3. Screen for candidate biases with observable markers, not labels:
   - Loss aversion: holding losers well past the stated stop while selling winners early; asymmetric position-size changes after drawdowns.
   - Disposition effect: realized-gain-to-realized-loss ratio materially above 1 in the same period, with unrealized losses dominating the book.
   - Overconfidence: turnover above the strategy's documented norm; position sizes rising after a streak of wins without new evidence.
   - Anchoring: revised targets or valuations clustering near a prior price, purchase cost, or analyst figure.
   - Recency and narrow framing: allocation changes that track the last 3 to 6 months of returns; decisions evaluated in isolation rather than at portfolio level.
   - Confirmation: research sources or screens that all point one direction; disconfirming data noted but not weighted.
   - Herding and FOMO: entries following a visible move with no pre-stated trigger.
4. Quantify each flagged pattern with a measure (e.g., count, ratio, average holding period differential, deviation from the written rule). Do not report a bias without a number.
5. Compare against the written process. A deviation is a finding; a deviation with no documented rule is a process gap.
6. Propose one to three controls matched to the observed failure. Each control must be specific, testable, and owned.

### Decision gates

- Gate A (data sufficiency): If fewer than roughly 30 comparable decisions exist, report patterns as anecdotal and do not conclude a bias is systematic.
- Gate B (causal claim): Do not attribute a loss to a bias unless the decision record shows the deviation from process occurred before the outcome.
- Gate C (intervention): Any recommendation that changes client holdings, trading limits, or live order routing requires explicit approval from the accountable party before execution. Present it as a proposal.
- Gate D (sensitive data): Personal financial details, account identifiers, and health or family information must be minimized, redacted in outputs, and not stored beyond the task.

### Verification and evidence

- Re-run each bias metric on a holdout period or split sample; a pattern that disappears should be downgraded.
- Confirm that counted events match source records (reconciliation to trade blotter or statements; discrepancies above zero must be listed).
- Check that proposed controls are measurable: each needs a metric, a threshold, a review date, and a named owner.
- Cross-check market-structure or regulatory references against current official publications; mark any rule, threshold, or product detail as version-sensitive and unverified until confirmed.

### Failure handling

- Missing decision rationale: state that the bias analysis is limited to behavioral markers; do not infer intent.
- Conflicting records: report both versions, do not select the favorable one.
- Outcome-driven pressure to find a culprit: restate the decision-quality versus outcome-quality distinction and proceed with the evidence available.
- Request to predict returns or time markets using behavioral signals: decline the prediction; offer analysis of the process instead.

### Deliverable contract

Produce a structured report with these sections, in order:

1. Scope and data period, with assumptions and gaps.
2. Decision timeline table: date, decision, information available, rationale source (before/after outcome).
3. Bias findings: each with the observable marker, quantified measure, sample size, and confidence (low/medium/high) based on Gate A and holdout results.
4. Process deviations versus written policy.
5. Recommended controls (maximum three): trigger, action, metric, threshold, owner, review date. Mark all as proposals pending approval.
6. Open questions and data requests.

Quality checks before delivery: every bias has a number; no finding relies on post-outcome rationale without a label; no return forecast appears; every control is measurable; version-sensitive regulatory or product details are flagged.

### What not to do

- Do not label a person as irrational, emotional, or unfit based on trade patterns alone.
- Do not present a bias as proven from a single episode.
- Do not recommend leverage, concentration, or product changes as a "fix."
- Do not execute or instruct execution of trades, transfers, or account changes without explicit approval.
- Do not invent statistics, benchmark figures, or regulatory citations.


## commerce-payments-revenue

**Use when:** Use when reconciling, validating, or reporting payment and revenue records sourced from external registries such as payment processors, marketplaces, app stores, or payout ledgers, including settlement matching, refund and chargeback handling, fee attribution, and revenue recognition inputs.

### Purpose and boundaries

This skill covers turning payment and revenue records from external registries into a reconciled, auditable view of gross sales, fees, refunds, disputes, payouts, and net revenue. It applies to exports, reports, and API extracts from processors, marketplaces, app stores, and payout providers.

In scope: matching transactions to settlements, classifying events (sale, refund, chargeback, reversal, fee, adjustment), currency normalization using the rate source the registry itself reports, variance analysis, and producing a reconciliation package.

Out of scope: tax filing, legal revenue-recognition opinions, accounting entries posted to a live ledger, and any action that moves money, changes registry state, or contacts a counterparty. Do not provide compliance certifications or guarantee that outputs satisfy a given accounting standard.

### Inputs and assumptions

Required before starting:
- Source extracts with period boundaries, time zone, and currency stated.
- Registry-native identifiers (transaction, payout, dispute, order IDs).
- Fee schedules or fee lines as reported by the registry.
- The internal order or invoice record, if matching to internal sales.

Assumptions to state explicitly in the output: whether amounts are gross or net of tax, whether refunds posted in the period belong to the original sale period, and which timestamp (authorization, capture, settlement, or payout) defines the period.

Mark any field name, report format, or API behavior as "verify against current official registry documentation" unless you have confirmed it in the supplied files. Do not infer schema from memory.

### Operating workflow

1. Inventory each source: row count, date range, currency set, and control totals reported by the registry. Record them before transforming anything.
2. Normalize: convert amounts to minor units, unify sign conventions (refunds and fees negative), and tag each row with its event type.
3. Match primary keys first: transaction to settlement, settlement to payout. Use exact ID matches before any fuzzy matching on amount, date, or reference text.
4. Attach secondary events: refunds, chargebacks, reversals, and reissued payments link to their original transaction via registry references, not by amount alone.
5. Attribute fees to their parent transaction or to a period-level bucket if the registry does not itemize them. Label unattributed fees explicitly.
6. Compute the bridge: gross sales − refunds − chargebacks − fees ± adjustments = net settled, and net settled − payouts in transit = closing balance difference.
7. Investigate every residual above the tolerance threshold before closing the period.

### Decision gates

- Gate A (source trust): If control totals from the registry do not match the extract row sums, stop and request a re-export. Do not reconcile against a partial file.
- Gate B (currency): If a single settlement mixes currencies without a stated conversion, hold that settlement and escalate. Do not apply a rate you sourced yourself without approval.
- Gate C (tolerance): Residuals at or below the agreed tolerance (default: zero for minor-unit exact matches, with rounding differences listed separately) may be closed with a note. Anything larger requires root cause.
- Gate D (external action): Any request to issue refunds, submit disputes, change payout settings, or send reconciled figures to a counterparty requires explicit written approval from the account owner. Prepare the request; do not execute it.
- Gate E (sensitive data): Mask card fragments, bank account numbers, and personal identifiers in all outputs. Retain only the registry reference IDs needed for traceability.

### Verification and evidence

Quality checks, all required:
- Sum of classified rows equals source control total to the minor unit, per source and per currency.
- Every net-settled amount traces to at least one payout ID or an explicitly listed pending status.
- Zero duplicate transaction IDs after normalization, unless the registry documents legitimate reissues, which must be listed.
- Refund and chargeback totals reconcile to registry-reported dispute and refund summaries.
- Residual count and value reported as a percentage of gross volume; target under 0.1% unless the owner sets another threshold.

Evidence to retain: source file hashes, row counts before and after each step, matching rules applied in order, and a list of every manual override with reason and approver.

### Failure handling

- Missing or duplicate IDs: quarantine the rows, report counts, and request clarification. Do not generate substitute keys silently.
- Control total mismatch: report the delta and the first divergent date or batch; do not force a balance.
- Timezone boundary shifts: test whether moving the cutoff by the stated offset clears the variance; if so, document the cutoff issue rather than adjusting amounts.
- Registry format change: halt parsing, diff the header against the last validated version, and mark outputs as provisional.

### Deliverable contract

Produce one package containing:
1. Summary: period, sources, currencies, gross, net, fees, refunds, disputes, payouts, and residual value with percentage.
2. Reconciliation table by settlement and payout, with status (matched, pending, exception).
3. Exception register: each open item with ID, amount, cause hypothesis, owner, and required approval if any.
4. Assumptions and verification results against each quality check above.
5. Approval requests for any Gate D actions, listed but not executed.

Do not present unverified figures as final. Label provisional outputs clearly.

### Ultron routing contract

**Choose this skill when:** the main deliverable is a financial reconciliation or analytical view derived from payment processors, marketplaces, app stores, or payout-provider records: gross sales, fees, refunds, disputes, settlements, payouts, and net revenue.

**Choose `saas-finance-commerce-automation` when:** the task changes or automates billing operations: subscriptions, plans, pricing, invoices, dunning, payment recovery, refunds/credits, deferred revenue schedules, or corrective actions across billing and ledger systems.

**Handoff contract:** this skill supplies normalized transaction and settlement facts, reconciliation variances, event classifications, and source evidence. The automation skill uses those facts to prepare or execute an approved operational correction, then returns the resulting billing/ledger state for reconciliation. Never treat an unexplained reconciliation difference as permission to issue a refund or alter an invoice.

**Why the boundary exists:** financial reporting establishes what happened to money; finance automation changes the systems and customer obligations that determine what happens next.


## crypto-meme-scout

**Use when:** Use when a user asks to research, screen, or risk-assess a meme token or memecoin launch, including holder concentration, liquidity, contract authority, and social-signal authenticity, and needs a structured evidence-based report rather than a trade recommendation.

### Purpose and boundaries

This skill produces structured due-diligence reports on meme tokens: what can be verified on-chain, what is claimed off-chain, and where the risks concentrate. It supports research and risk awareness. It does not provide buy, sell, or sizing advice, does not predict price, and does not give guarantees of safety or legitimacy. Final decisions belong to the user.

Out of scope: launching or promoting tokens, drafting coordinated social posts, generating fake engagement, wallet or bot operations, identifying private individuals behind wallets, and any help with pump-and-dump or wash-trading schemes. Decline these plainly and offer the research alternative.

### Inputs and assumptions

Required: token contract address and chain, or a project name plus a verified contract address. Optional: the user's stated thesis, time horizon, and sources they have already reviewed.

Assumptions to state in every report: data comes from public sources as accessed at a stated time; explorer and analytics metrics can lag, be mislabeled, or be incomplete; a single data source is insufficient for a conclusion. If the contract address is not provided or cannot be confirmed against two independent sources, stop and request it. Never resolve an ambiguous name to a contract yourself.

### Operating workflow

1. **Identify and confirm.** Record chain, contract address, deployer address, creation time, and name/symbol. Check for duplicate names or lookalike tokens and flag them.
2. **Contract authority.** Using the chain's explorer source-verification status, check whether source is published and verified, and whether the owner or admin roles exist and are renounced, locked, or held by an active address. Note mint functions, pause or blacklist functions, fee-setting functions, and proxy patterns. Verify function names against current explorer documentation before asserting their behavior.
3. **Holder distribution.** Pull the top 20 holders. Separate liquidity pools, burn addresses, exchange custody, and likely team-linked wallets (only where on-chain links are evident, such as shared funding sources). Compute top-10 concentration excluding pools and burns.
4. **Liquidity.** Identify the pool, paired asset, locked or burned LP status with lock contract and expiry, and depth at a stated slippage level.
5. **Deployer history.** List prior token deployments by the same address and their outcomes (abandoned, rugged, live). Report facts only.
6. **Social verification.** Check account creation dates, follower-to-engagement ratios, sudden follower spikes, and whether claims (partnerships, listings, audits) are verifiable at the primary source.
7. **Synthesis.** Write the report per the deliverable contract.

### Decision gates

- **Gate A (proceed):** Contract identity confirmed by two sources. If not, stop.
- **Gate B (escalate):** Any active mint, blacklist, or owner-withdrawal authority, or LP unlocked with expiry under 30 days. Flag as high risk in the first line of the report.
- **Gate C (escalate):** Top-10 non-pool concentration above 50%, or a single non-pool wallet above 10%. Flag as high concentration.
- **Gate D (stop and ask):** The user requests actions that move funds, interact with a contract, post publicly, or contact third parties. Require explicit written approval, state the exact action and its irreversibility, and do not proceed without it.

### Verification and evidence

Every factual claim carries a source label and access time. Unverifiable claims are marked "unverified," not omitted. Re-check holder and liquidity data immediately before the final report, since these shift quickly. Do not state audit results unless the auditor's report is linked and dated. Do not state that a project is "safe," "legitimate," or "compliant"; no such guarantees exist. Mark explorer- and API-specific details as requiring confirmation against current official documentation.

Quality checks before delivery: every number has a source and timestamp; the top-10 concentration calculation is shown with the excluded addresses listed; no sentence implies a price forecast.

### Failure handling

- Explorer unavailable or source unverified: report the gap, mark contract authority as "undetermined," and do not infer safety from absence of evidence.
- Conflicting data between sources: present both values and the discrepancy; do not average them.
- Insufficient data for a gate: state the gate as unresolved and list what would resolve it.
- User pressure toward a conclusion: restate the evidence and the unresolved items.

### Deliverable contract

Output a report with these sections, in order:

1. **Risk summary** (three lines maximum; highest-severity finding first)
2. **Identity** (chain, address, deployer, creation time, duplicates checked)
3. **Contract authority** (findings table: function, status, source)
4. **Holder and liquidity** (concentration figures with exclusions listed; LP lock details)
5. **Deployer history** (facts only)
6. **Social verification** (verified claims, unverified claims, anomalies)
7. **Open items** (what remains unresolved and how to resolve it)
8. **Data timestamp and limitations**

Close with this sentence, verbatim: "This report is research, not investment advice."


## crypto-onchain

**Use when:** Use when analyzing public blockchain data, tracing token or wallet flows, evaluating smart-contract or protocol activity, or producing onchain research for trading, risk, or compliance review.

### Purpose and boundaries

This skill produces evidence-backed onchain analysis: transaction tracing, wallet and contract profiling, token distribution and liquidity reads, protocol flow measurement, and anomaly review. It supports trading research, risk assessment, incident triage, and compliance-oriented investigation.

In scope: reading public chain state and event logs, decoding transactions against verified ABIs, reconciling data across two or more independent sources, quantifying flows in native and USD-equivalent terms, and stating confidence levels.

Out of scope: giving personalized investment advice, executing or signing transactions, handling private keys or seed phrases, attributing wallets to real identities without documented evidence, guaranteeing that a contract is safe, and asserting intent (fraud, manipulation) as fact. Treat findings as indicators, not verdicts.

### Inputs and assumptions

Required inputs before analysis begins:
- Chain name and network (mainnet, testnet, L2 identifier).
- Target identifiers: addresses, token contract, transaction hashes, or protocol name with known contract set.
- Time window in UTC with explicit start and end block or timestamp.
- Question type: distribution, flow tracing, contract behavior, liquidity, incident reconstruction.
- Pricing source and convention for USD values (for example, price at block time versus daily close). Record the choice.

Assumptions to state explicitly in the output: explorer labels are heuristic; token decimals and symbols are not authoritative unless read from the contract; proxy contracts may change implementation; bridged assets represent different risk than native assets.

### Operating workflow

1. Confirm the network and the exact identifiers. Checksum-normalize addresses. Verify that a token contract address matches the expected chain before any query.
2. Resolve the contract: check whether it is a proxy, read the implementation slot where applicable, and retrieve verification status from the explorer. Record both proxy and implementation addresses.
3. Pull raw data first: transactions, internal calls, event logs, and token transfers for the window. Save the query parameters and block range alongside results.
4. Decode events using the verified ABI. Where decoding fails, report the raw topic hash rather than guessing a signature.
5. Aggregate. For distribution work, compute balances at a fixed block height, not at query time. For flow work, separate gross inflow, gross outflow, and net, and exclude internal self-transfers unless the question requires them.
6. Price consistently. Convert to USD using the declared pricing method. Report native-unit figures alongside USD.
7. Cross-check at least two sources (for example, a node read via RPC and an explorer export, or two independent indexers). Log any discrepancy with magnitude.
8. Write findings with a confidence tag per claim: high (directly observed on-chain and reproduced), medium (observed with a heuristic label or single source), low (inferred).

### Decision gates

Stop and request approval before proceeding if any of the following occur:
- The task requires interacting with a wallet, signing, or sending any transaction. Refuse by default; escalate to the user.
- The task asks to deanonymize an individual or link addresses to a named person. Require documented legal basis and a named accountable reviewer.
- The analysis would be shared externally (published report, client delivery, public post). Require explicit approval of the final content.
- Data sources require paid keys, scraping beyond published terms, or third-party uploads of sensitive addresses. Require approval.
- A finding suggests active exploit, unexplained mint, or unauthorized admin action. Escalate immediately; do not publish analysis until the owner of the affected system is notified.

Proceed without a gate for read-only queries against public data within the defined window.

### Verification and evidence

Each conclusion must cite: the block number or transaction hash, the decoded event or raw topic, the query timestamp, and the source. Checks before release:
- Totals reconcile: sum of per-address balances equals total supply within stated tolerance (zero for native-only, rounding tolerance for decimal tokens).
- Decimal handling is verified against the contract's decimals function, not assumed.
- Each cross-source discrepancy above 0.1 percent of the compared value is explained or flagged.
- No USD figure appears without its price source and timestamp.
- Every heuristic label is marked as heuristic.

Version-sensitive details (RPC method names, explorer API endpoints, indexer schemas, token standard extensions, EIP activation status) must be checked against current official documentation before being stated. If verification is unavailable, write "unverified against current documentation" next to the detail.

### Failure handling

- RPC rate limit or timeout: retry with bounded backoff, then narrow the block range. Do not fill gaps silently; report missing ranges.
- Unverified contract: analyze bytecode-level observations only and label behavior claims as unverified.
- Proxy upgraded mid-window: split the analysis at the upgrade block and analyze each implementation separately.
- Reorg suspicion: re-query blocks within the recent confirmation depth before finalizing; state the confirmation depth used.
- Conflicting sources that cannot be reconciled: report both values, state which is primary, and do not average them.

### Deliverable contract

Output a report with these sections in order:
1. Scope: network, identifiers, window (UTC and block range), question.
2. Method: sources, pricing convention, decoding approach, heuristics used.
3. Findings: numbered claims, each with value, confidence tag, and evidence reference.
4. Reconciliation: checks performed and their results.
5. Limitations: unverified items, missing data, label uncertainty.
6. Open actions: items needing approval or further data.

Do not include investment recommendations, price predictions, or statements that a project is or is not a scam. Do not state that any analysis guarantees compliance or security.


## finance-market-analysis

**Use when:** Use when analyzing market data, company financials, or external registry records (securities filings, company registries, exchange listings, market statistics) to produce sourced, reproducible financial findings for an investment, credit, research, or due-diligence question.

### Purpose and boundaries

This skill turns a defined financial question into a sourced, reproducible analysis built from external registries and market data: exchange listings, regulatory filings, corporate registry extracts, index constituents, and published macro or sector statistics.

In scope: ticker and identifier reconciliation, filing-based financial ratio analysis, peer comparison, trend and valuation context, event timelines (earnings, corrections, insider or ownership changes), and data-quality audits of registry records.

Out of scope: personalized investment advice, price targets presented as certainties, trade execution, insider or material non-public information, and legal or tax conclusions. Output is analytical support for a qualified professional's decision.

### Inputs and assumptions

Before starting, confirm:

1. The question: a decision, comparison, or screen with a stated horizon and currency.
2. The universe: named entities identified by legal name plus at least one stable identifier (ISIN, LEI, registry number, CIK-style filer ID, or exchange ticker with venue).
3. The period: fiscal year-end conventions, reporting currency, and whether figures are restated.
4. Data access: which sources are permitted. Record each source's publisher, retrieval date, and document version.

Assumptions must be written down. Default to reported (not adjusted) figures unless the question requires adjustment, and state any adjustment rule.

### Operating workflow

1. **Frame.** Restate the question in one sentence. List the metrics required to answer it and the minimum evidence per metric.
2. **Identify.** Resolve each entity to a primary identifier. Reject matches where name, jurisdiction, and identifier disagree. Log ticker changes, mergers, delistings, and share-class differences.
3. **Collect.** Pull primary documents first (annual and interim filings, registry extracts, exchange notices), then secondary aggregators. Record page or section references for every figure.
4. **Normalize.** Align fiscal periods, currencies (state FX source and date), units, and accounting basis (IFRS versus US GAAP, and whether non-GAAP measures are used). Recompute standard ratios from raw line items rather than trusting pre-computed aggregator fields.
5. **Analyze.** Compute the agreed metrics: growth, margins, leverage, liquidity, cash conversion, returns on capital, and valuation multiples. Compare against peers defined before looking at results. Examine a multi-year window, not a single period.
6. **Contextualize.** Identify drivers: one-off items, accounting changes, debt maturities, index rebalancing, sector cycles. Separate observed facts from interpretation.
7. **Report.** Produce the deliverable contract below.

### Decision gates

- **Identifier gate:** Proceed only if every entity maps to one primary identifier with a consistent jurisdiction. Otherwise, exclude the entity and report why.
- **Source gate:** A figure used in a conclusion must trace to a primary document or a named, dated secondary source. Single unverified aggregator figures cannot drive a conclusion.
- **Consistency gate:** If the same metric differs across two sources by more than 1% of the reported value or by any sign change, reconcile against the filing before continuing. If unreconciled, flag it.
- **Restatement gate:** If a later filing restates a prior period, use the restated figure and note the original.
- **Scope gate:** If the question requires a forecast, a recommendation, or a legal/tax determination, stop and state the limitation; deliver analysis only.
- **Approval gate:** Obtain explicit user approval before any action that is destructive, irreversible, externally visible (publishing, emailing, submitting to a registry or portal), or involves personal data beyond what the question requires, or material non-public information. Do not perform these on inference.

### Verification and evidence

- Recompute at least three headline figures (for example, net debt, free cash flow, operating margin) from line items and confirm agreement within rounding.
- Check balance sheet identity (assets equal liabilities plus equity) and cash flow tie-out to the change in cash for each period used.
- Confirm peer set size is at least five where comparisons are claimed, and document exclusions.
- Every number in the output carries a source reference: document, section, period, and retrieval date.
- Mark any version-sensitive item (accounting standard edition, exchange rule, registry API schema, data field name) as "verify against current official documentation" rather than asserting it.
- Do not state benchmark performance, historical hit rates, or regulatory compliance outcomes unless directly sourced in the session.

### Failure handling

- **Missing filing:** Report the gap and the period affected. Do not interpolate silently; if interpolation is used, label it.
- **Identifier conflict:** Halt that entity, list candidate matches with evidence, and request confirmation.
- **Unit or currency mismatch:** Convert only with a stated rate and date; otherwise report in original currency.
- **Source outage or access restriction:** Use the available primary source, mark the coverage gap, and do not substitute an unverified source.
- **Result contradicts prior assumption:** Report the contradiction first, then revise the frame; do not adjust data to fit the thesis.

### What not to do

- Do not present calculated ratios without their formula and inputs.
- Do not mix fiscal years or currencies in one comparison without normalization.
- Do not treat non-GAAP or adjusted figures as reported figures.
- Do not extrapolate a single quarter into an annual trend.
- Do not invent identifiers, filing dates, or figures to complete a table.

### Deliverable contract

The output must contain, in order:

1. **Question and scope:** one sentence, horizon, currency, universe.
2. **Method and assumptions:** formulas, adjustment rules, peer definition.
3. **Findings table:** metric, entity, period, value, source reference.
4. **Interpretation:** three to six numbered findings, each labeled as fact or inference.
5. **Data-quality log:** exclusions, reconciliations, unresolved conflicts, verification items.
6. **Limitations:** what the evidence cannot support.

Quality check before release: every figure traceable, every ratio reproducible from listed inputs, all gates passed or explicitly flagged, no recommendation phrased as certainty.

### Ultron routing contract

**Choose this skill when:** the financial question depends on issuer and instrument identity, corporate or regulatory filings, financial statement line items, ownership or earnings events, peer fundamentals, valuation context, or reconciling market data to authoritative financial records.

**Choose `market-analysis` when:** the primary objective is to analyze a market or instrument over a defined horizon using price, volume, volatility, spreads, positioning, term structure, or a conditional trading thesis and its invalidation conditions.

**Handoff contract:** this skill supplies verified identifiers, filing dates, normalized financial periods, accounting basis, recomputed ratios, and sourced fundamental events. The market-analysis skill returns horizon-specific market structure, scenario conditions, risk factors, and invalidation signals. Keep fundamental facts distinct from market observations and forecasts.

**Why the boundary exists:** financial records establish what an issuer reported; market analysis studies how an instrument or market behaves. Combining them is useful, but one must not be mistaken for the other.


## fundamentals-valuation

**Use when:** Use when estimating the intrinsic value of a listed or private company from financial statements, building or reviewing DCF, comparable-company, or residual-income models, or checking whether a stated price target is supported by its assumptions.

### Purpose and boundaries

This skill produces a documented, auditable valuation of an operating company (or a specific equity/enterprise claim) from its financial fundamentals. It covers: normalizing historical financials, forecasting free cash flow or residual income, selecting discount rates, cross-checking with relative multiples, and stating a value range with its sensitivities.

It does not cover: trade execution, position sizing, portfolio construction, options or derivatives pricing, real-estate appraisal, bank-regulatory capital analysis, or giving personalized investment advice. Output is analysis for a qualified professional to review; it is not a recommendation to buy or sell.

### Inputs and assumptions

Required inputs, in order of priority:
1. Three to five years of audited annual statements (income statement, balance sheet, cash flow statement) and the most recent interim filing.
2. Share count (basic and diluted), net debt components, and minority interests, preferred equity, and pension deficits.
3. Market data as of a stated date: share price, risk-free rate reference, and peer multiples.
4. Management guidance and consensus estimates, labeled as third-party inputs.

Record every assumption in an assumptions register: value, source, date, and owner. Treat unlabeled numbers as unsupported. If a required input is missing, mark the dependent output "provisional" rather than filling it with an estimate silently.

Do not assume the company's reporting follows a single standard without checking. Flag any reliance on non-GAAP or non-IFRS adjusted measures and reconcile them to statutory figures.

### Operating workflow

1. **Define the claim.** State the value being estimated (equity value per share, enterprise value, or a specific business unit) and the valuation date.
2. **Normalize historicals.** Remove one-offs (impairments, restructuring, litigation, disposal gains). Separate operating from non-operating assets and liabilities. Capitalize or expense leases consistently with the reporting standard in force; verify the treatment against current accounting standard text.
3. **Compute invested capital and returns.** Calculate return on invested capital (NOPAT divided by average invested capital) for each historical year. Use this to test whether growth creates or destroys value.
4. **Build the forecast.** Drive revenue by segment or volume × price where possible. Forecast margins, reinvestment rate (net capex plus working-capital change divided by NOPAT), and the fade toward a terminal state. Link growth to reinvestment: implied growth equals reinvestment rate × return on new capital.
5. **Set the discount rate.** Build cost of capital from a stated risk-free rate, equity risk premium, and beta from a documented method. Show the sensitivity of beta to leverage. Use a target capital structure, not the current one, unless justified.
6. **Compute terminal value.** Use a perpetuity growth rate that does not exceed long-run nominal economic growth for the relevant currency. Cross-check the implied exit multiple against sector history.
7. **Cross-check with relative value.** Select peers by business model, growth, and returns, not by sector label alone. Use normalized multiples (EV/EBITDA after lease treatment, P/E on normalized earnings). Report the median and interquartile range.
8. **Reconcile to per-share value.** Subtract net debt and equity claims, divide by diluted shares using the treasury stock method where options are material.
9. **Run sensitivities.** Vary discount rate, terminal growth, and the margin path. Identify which single input moves value most.
10. **Write the conclusion as a range** with the central case, bear and bull cases, and the assumptions that drive the gap.

### Decision gates

- **Gate A (inputs):** Proceed only if audited statements, share count, and net debt are sourced. Otherwise output "provisional" and list the blocking items.
- **Gate B (normalization):** If one-offs exceed 10% of operating profit in any forecast base year, document each adjustment before forecasting.
- **Gate C (terminal value):** If terminal value exceeds 80% of enterprise value, require an explicit explanation and a sensitivity table with a reduced terminal growth case.
- **Gate D (discount rate):** If the discount rate is below the cost of debt after tax, or the terminal growth rate is at or above the discount rate, stop and correct before reporting.
- **Gate E (external use):** Any valuation intended for distribution to third parties, use in a transaction, fairness opinion, regulatory filing, or client-facing price target requires explicit human approval and review by a credentialed professional. Do not produce such material as final.

### Verification and evidence

Quality checks, each must pass or be explained:
- Forecast reinvestment and growth are internally consistent (implied return on new capital is within a stated, defended range relative to historical ROIC).
- Balance sheet reconciles: forecast net debt roll-forward equals cash flow after distributions.
- Per-share value recomputes from enterprise value within rounding tolerance.
- Peer set has at least five companies with documented selection criteria, or the relative cross-check is labeled weak.
- Sensitivity table covers at least a ±1 percentage point discount rate range and ±0.5 percentage point terminal growth range.
- Every number traces to a source row in the assumptions register.

Tax rates, accounting rules, and regulatory thresholds change. Mark each such detail "verify against current official documentation" with the document name and date checked.

### Failure handling

- **Missing data:** Stop the affected line item, mark it provisional, and list the data request. Do not back-solve figures from the target price.
- **Conflicting sources:** Prefer audited filings over press summaries; prefer the primary filing over derived databases. Record the conflict.
- **Target-price anchoring:** If the result is reached by adjusting inputs toward a known market price or a desired outcome, discard the model and restart from the assumptions register.
- **Sudden model break** (negative invested capital, sign errors, circular references): freeze output, identify the first failing cell or step, and fix before continuing.

### Deliverable contract

Deliver a single document containing, in order:
1. Valuation date, claim, and status (final draft or provisional).
2. Assumptions register table (item, value, source, date).
3. Normalized historical summary with one-off adjustments listed.
4. Forecast table with explicit drivers and reinvestment link.
5. Discount rate build-up.
6. Valuation output: enterprise value, equity value, value per share, with bear/central/bull range.
7. Relative cross-check with peer list and criteria.
8. Sensitivity tables.
9. Open items, gate results, and items marked for verification against current documentation.

Do not include buy, sell, or hold language. Do not present a point estimate without its range and drivers. Do not state that the model is "accurate," "guaranteed," or "compliant."


## saas-finance-commerce-automation

**Use when:** Use when designing, auditing, or operating agent-driven workflows that touch SaaS billing, subscription lifecycle, invoicing, refunds, revenue reconciliation, or commerce order-to-cash data, where an agent reads or proposes changes to financial records.

### Purpose and boundaries

This skill guides an agent through automation of subscription and commerce finance operations: plan and price changes, trial conversions, dunning and payment recovery, invoice generation and corrections, refund and credit handling, deferred revenue schedules, and reconciliation between billing, payment processor, ledger, and CRM records.

In scope: reading financial state, classifying discrepancies, drafting corrective actions, preparing reconciliation reports, and executing pre-approved low-risk operations through an approved integration.

Out of scope: tax filing or tax advice, accounting policy decisions (revenue recognition judgments, reserve estimates), legal interpretation of contracts, credit decisions, and any action that moves money or changes a ledger of record without explicit human approval.

### Inputs and assumptions

Before acting, confirm and record:

1. Source systems: billing platform, payment processor, general ledger, CRM, and their read/write scopes.
2. Accounting period, currency set, and timezone used for cutoffs.
3. Authoritative source for each entity (for example, the billing platform owns subscription state; the processor owns settlement status; the ledger owns posted balances).
4. Pricing and plan catalog version in effect for the period.
5. Approval matrix: who approves refunds, credits, write-offs, and cancellations, and at what thresholds.
6. Whether the environment is sandbox or production. Assume production unless told otherwise.

If any input is missing, stop and request it. Do not infer thresholds or approvers.

### Operating workflow

1. **Snapshot.** Pull read-only data for the defined scope (customer, subscription, or batch window). Record timestamps and record counts. Use a fixed cutoff.
2. **Normalize.** Convert amounts to minor currency units, map statuses to a single internal vocabulary, and tag each record with its source system.
3. **Match.** Join records on stable identifiers (subscription ID, invoice ID, processor charge ID). Never join on email or name alone. Flag unmatched records on both sides.
4. **Classify discrepancies.** Assign each to one category: timing (settlement lag under the agreed window), duplicate, missing invoice, amount mismatch, status mismatch, currency mismatch, or unknown.
5. **Propose actions.** For each discrepancy, draft the smallest corrective step, its expected ledger effect, its reversibility, and its approver.
6. **Simulate.** Where the platform offers a dry-run or preview, use it. Otherwise compute the expected before/after balances in a separate calculation and show the delta.
7. **Request approval.** Present the batch as a table with totals. Wait for explicit approval per action class.
8. **Execute and confirm.** Apply approved actions one at a time or in small idempotent batches. Re-read each changed record and compare to the expected state.
9. **Report.** Return the transaction plan in the required output structure below.

### Decision gates

Stop and obtain human approval before any of the following:

- Any refund, credit note, chargeback response, write-off, or voided invoice.
- Any change to price, plan entitlement, or billing cycle on a live subscription.
- Any cancellation or pause that affects revenue or customer access.
- Any posted ledger entry, journal adjustment, or period reopening.
- Any outbound customer communication about charges, failures, or cancellations.
- Any batch where affected amount exceeds the approval threshold or affected record count exceeds 50 without prior sampling.
- Any action where source systems disagree on the authoritative state.
- Any operation that cannot be reversed by a documented compensating action.

Proceed without a gate only for read-only queries and generation of draft reports.

### Verification and evidence

- Reconciliation balance: for every batch, sum(source amounts) minus sum(target amounts) equals the listed discrepancy total, to the minor unit. Zero unexplained residual is the pass condition.
- Idempotency: re-running the same batch after success produces zero new changes.
- Sampling: before executing any batch over 50 records, manually verify at least 10 percent, minimum 5, against source documents.
- Post-change read-back: each modified record matches the approved expected state.
- Evidence retained: record IDs, pre- and post-state, timestamps, actor identity, and approval reference for every write.
- Version-sensitive details (API endpoints, field names, webhook event types, rate limits, and rounding behavior) must be checked against current official vendor documentation before use. Do not rely on memory for these.

Do not claim compliance with any tax, accounting standard, or payment card rule. State only what was verified in the data.

### Failure handling

- **Partial failure:** stop the batch. Record which actions completed, which failed, and the error text. Do not retry writes automatically unless the operation is confirmed idempotent in current documentation.
- **Ambiguous state:** when a write response is missing or a timeout occurs, re-read the record before any retry. If state is unknown, escalate.
- **Rate limit or auth error:** pause, report, and wait. Do not rotate credentials or widen scopes.
- **Source conflict:** do not resolve by picking the larger or newer value. Escalate with both values and their sources.
- **Compensating action needed:** draft it, mark it as requiring approval, and never apply it silently.

### Deliverable contract

Every run returns:

1. Scope statement: systems, period, cutoff timestamp, record counts per source.
2. Summary table: discrepancy category, count, total amount, status (proposed, approved, executed, failed, escalated).
3. Action log: record ID, action, expected effect, approver, execution result, read-back result.
4. Reconciliation statement showing the residual (must be zero or explicitly listed).
5. Open items: escalations, unmatched records, and verification steps not yet completed.
6. Assumptions and unverified version-sensitive details, listed explicitly.

### What not to do

- Do not issue refunds, credits, or cancellations to resolve a mismatch you have not classified.
- Do not treat processor-reported status as ledger truth without the ledger's posting confirmation.
- Do not batch unrelated customers into a single approval.
- Do not round amounts to hide differences.
- Do not hardcode plan prices, tax rates, or API field names from memory.
- Do not send customer-facing messages about payment failures without approval of the wording and recipient list.
- Do not reopen a closed accounting period.

### Ultron routing contract

**Choose this skill when:** the objective is to operate or improve subscription and commerce finance workflows: plans and prices, trial conversion, invoicing, dunning, payment recovery, refunds, credits, deferred revenue schedules, and billing-to-ledger reconciliation.

**Choose `commerce-payments-revenue` when:** the task is to reconcile processor or marketplace exports and establish the factual transaction, fee, refund, dispute, settlement, payout, or net-revenue position before any corrective action.

**Handoff contract:** receive a reconciled set of transaction IDs, settlement IDs, variance classifications, currencies, and source evidence. Propose the smallest correction, show affected customer/account counts, obtain the required approval, and verify the new billing/ledger state. Return the final transaction state to the reconciliation skill for independent confirmation.

**Why the boundary exists:** an operational correction can create financial and customer impact. It must be based on reconciled facts and separately verified afterward.


## trading-psychology

**Use when:** Use when reviewing a trader's decision process, journal, or behavior patterns; designing pre-trade and post-trade checklists; diagnosing revenge trading, overtrading, or rule drift; or building discipline controls for a discretionary or systematic trading practice.

### Purpose and boundaries

This skill turns trading behavior into observable evidence and then into concrete process changes. It covers: decision-quality review, emotional-state and behavior logging, rule-adherence auditing, pre-trade and post-trade checklists, and written discipline protocols for discretionary or systematic traders.

It does not provide clinical diagnosis, treatment, or mental-health advice. It does not recommend specific securities, entries, exits, position sizes, or return targets. If behavior suggests addiction, severe distress, or self-harm risk, stop the analysis and direct the user to qualified professional support.

### Inputs and assumptions

Request these before analysis:
- Trade log: timestamp, instrument, side, size, entry, exit, stop, target, realized P&L, and the stated reason for entry.
- Rule set: the written plan, including risk per trade, maximum daily loss, allowed setups, and session hours.
- Context notes: market conditions, news exposure, sleep or fatigue notes if the user volunteers them, and any account events (drawdowns, withdrawals, prop-firm limits).
- Time window: at least 30 trades or 20 trading days for pattern claims. Fewer trades support only anecdotal observations; label them as such.

Assume the logs are accurate unless reconciliation shows otherwise. Do not assume intent. Describe behavior, not character.

### Operating workflow

1. Reconcile the log against the rule set. Flag every trade with missing stop, size above the stated risk limit, entry outside allowed setups, or trades after the daily loss limit.
2. Compute process metrics, not just P&L: percent of trades with a predefined stop, percent of trades meeting all entry criteria, average risk per trade versus plan, trades per session, and time from loss to next entry.
3. Segment by state. Compare outcomes for trades taken within 15 minutes of a loss, after two or more consecutive losses, after a winning streak, and in the final hour of the session.
4. Test for specific patterns:
   - Revenge: next-trade size above baseline within 30 minutes of a loss.
   - Overtrading: trade count more than 1.5 times the session median with declining setup quality.
   - Loss aversion: losers held materially longer than winners, or stops moved away from entry.
   - Premature exit: winners closed well before target with no rule trigger.
5. Rank findings by estimated cost (sum of rule-violating losses) and by frequency.
6. Propose at most three interventions, each with a trigger, an action, and a measurable test.

### Decision gates

- Gate A (sample sufficiency): if fewer than 30 trades, report observations only and do not recommend rule changes.
- Gate B (causal caution): describe correlations between state and outcome as associations. Do not claim a feeling caused a loss.
- Gate C (intervention approval): any change to position limits, live-account permissions, risk settings, or broker configuration requires explicit written approval from the account owner before the user applies it. Do not modify live settings yourself.
- Gate D (sensitive content): if the user discloses financial distress, debt, or personal crisis, pause the performance analysis and ask whether they want to address that separately with appropriate professional help.

### Verification and evidence

Every finding must cite the trade IDs or dates supporting it. Provide counts and the calculation used. Before presenting an intervention, check:
- It targets a finding with at least 5 supporting instances.
- It has a binary, loggable trigger (for example, "two consecutive losses" rather than "feeling frustrated").
- It defines a review horizon (for example, 20 sessions) and a success metric (for example, rule-violation rate below 5 percent).

Do not claim statistical significance without naming the test and its assumptions. Do not cite published research findings unless the user supplies the source and you can verify it.

### Failure handling

- Incomplete logs: list missing fields, quantify the affected trades, and exclude them from metrics with a stated count.
- Contradictory data (P&L not reconciling with fills): stop and request broker statements. Do not estimate.
- User requests a guaranteed-profit system or a pitch for a specific instrument: decline that part and continue with the process review.
- User asks for a plan to recover losses quickly: refuse the sizing escalation and redirect to the loss-limit protocol.

### Deliverable contract

Return a report with these sections, in order:
1. Summary (three sentences maximum, stating the highest-cost violation).
2. Data quality (trade count, date range, excluded records).
3. Process metrics table (metric, value, plan target, status).
4. Findings (ranked, each with evidence IDs and calculation).
5. Interventions (maximum three; trigger, action, metric, review date, approval status).
6. Open questions for the user.

Do not include motivational language, guarantees of future performance, or unverified claims about market behavior.


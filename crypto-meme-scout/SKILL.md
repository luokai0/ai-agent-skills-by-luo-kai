---
name: crypto-meme-scout
description: Use when a user asks to research, screen, or risk-assess a meme token or memecoin launch, including holder concentration, liquidity, contract authority, and social-signal authenticity, and needs a structured evidence-based report rather than a trade recommendation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Crypto Meme Scout

## Purpose and boundaries

This skill produces structured due-diligence reports on meme tokens: what can be verified on-chain, what is claimed off-chain, and where the risks concentrate. It supports research and risk awareness. It does not provide buy, sell, or sizing advice, does not predict price, and does not give guarantees of safety or legitimacy. Final decisions belong to the user.

Out of scope: launching or promoting tokens, drafting coordinated social posts, generating fake engagement, wallet or bot operations, identifying private individuals behind wallets, and any help with pump-and-dump or wash-trading schemes. Decline these plainly and offer the research alternative.

## Inputs and assumptions

Required: token contract address and chain, or a project name plus a verified contract address. Optional: the user's stated thesis, time horizon, and sources they have already reviewed.

Assumptions to state in every report: data comes from public sources as accessed at a stated time; explorer and analytics metrics can lag, be mislabeled, or be incomplete; a single data source is insufficient for a conclusion. If the contract address is not provided or cannot be confirmed against two independent sources, stop and request it. Never resolve an ambiguous name to a contract yourself.

## Operating workflow

1. **Identify and confirm.** Record chain, contract address, deployer address, creation time, and name/symbol. Check for duplicate names or lookalike tokens and flag them.
2. **Contract authority.** Using the chain's explorer source-verification status, check whether source is published and verified, and whether the owner or admin roles exist and are renounced, locked, or held by an active address. Note mint functions, pause or blacklist functions, fee-setting functions, and proxy patterns. Verify function names against current explorer documentation before asserting their behavior.
3. **Holder distribution.** Pull the top 20 holders. Separate liquidity pools, burn addresses, exchange custody, and likely team-linked wallets (only where on-chain links are evident, such as shared funding sources). Compute top-10 concentration excluding pools and burns.
4. **Liquidity.** Identify the pool, paired asset, locked or burned LP status with lock contract and expiry, and depth at a stated slippage level.
5. **Deployer history.** List prior token deployments by the same address and their outcomes (abandoned, rugged, live). Report facts only.
6. **Social verification.** Check account creation dates, follower-to-engagement ratios, sudden follower spikes, and whether claims (partnerships, listings, audits) are verifiable at the primary source.
7. **Synthesis.** Write the report per the deliverable contract.

## Decision gates

- **Gate A (proceed):** Contract identity confirmed by two sources. If not, stop.
- **Gate B (escalate):** Any active mint, blacklist, or owner-withdrawal authority, or LP unlocked with expiry under 30 days. Flag as high risk in the first line of the report.
- **Gate C (escalate):** Top-10 non-pool concentration above 50%, or a single non-pool wallet above 10%. Flag as high concentration.
- **Gate D (stop and ask):** The user requests actions that move funds, interact with a contract, post publicly, or contact third parties. Require explicit written approval, state the exact action and its irreversibility, and do not proceed without it.

## Verification and evidence

Every factual claim carries a source label and access time. Unverifiable claims are marked "unverified," not omitted. Re-check holder and liquidity data immediately before the final report, since these shift quickly. Do not state audit results unless the auditor's report is linked and dated. Do not state that a project is "safe," "legitimate," or "compliant"; no such guarantees exist. Mark explorer- and API-specific details as requiring confirmation against current official documentation.

Quality checks before delivery: every number has a source and timestamp; the top-10 concentration calculation is shown with the excluded addresses listed; no sentence implies a price forecast.

## Failure handling

- Explorer unavailable or source unverified: report the gap, mark contract authority as "undetermined," and do not infer safety from absence of evidence.
- Conflicting data between sources: present both values and the discrepancy; do not average them.
- Insufficient data for a gate: state the gate as unresolved and list what would resolve it.
- User pressure toward a conclusion: restate the evidence and the unresolved items.

## Deliverable contract

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
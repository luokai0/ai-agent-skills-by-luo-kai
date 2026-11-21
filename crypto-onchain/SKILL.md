---
name: crypto-onchain
description: Use when analyzing public blockchain data, tracing token or wallet flows, evaluating smart-contract or protocol activity, or producing onchain research for trading, risk, or compliance review.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Crypto Onchain

## Purpose and boundaries

This skill produces evidence-backed onchain analysis: transaction tracing, wallet and contract profiling, token distribution and liquidity reads, protocol flow measurement, and anomaly review. It supports trading research, risk assessment, incident triage, and compliance-oriented investigation.

In scope: reading public chain state and event logs, decoding transactions against verified ABIs, reconciling data across two or more independent sources, quantifying flows in native and USD-equivalent terms, and stating confidence levels.

Out of scope: giving personalized investment advice, executing or signing transactions, handling private keys or seed phrases, attributing wallets to real identities without documented evidence, guaranteeing that a contract is safe, and asserting intent (fraud, manipulation) as fact. Treat findings as indicators, not verdicts.

## Inputs and assumptions

Required inputs before analysis begins:
- Chain name and network (mainnet, testnet, L2 identifier).
- Target identifiers: addresses, token contract, transaction hashes, or protocol name with known contract set.
- Time window in UTC with explicit start and end block or timestamp.
- Question type: distribution, flow tracing, contract behavior, liquidity, incident reconstruction.
- Pricing source and convention for USD values (for example, price at block time versus daily close). Record the choice.

Assumptions to state explicitly in the output: explorer labels are heuristic; token decimals and symbols are not authoritative unless read from the contract; proxy contracts may change implementation; bridged assets represent different risk than native assets.

## Operating workflow

1. Confirm the network and the exact identifiers. Checksum-normalize addresses. Verify that a token contract address matches the expected chain before any query.
2. Resolve the contract: check whether it is a proxy, read the implementation slot where applicable, and retrieve verification status from the explorer. Record both proxy and implementation addresses.
3. Pull raw data first: transactions, internal calls, event logs, and token transfers for the window. Save the query parameters and block range alongside results.
4. Decode events using the verified ABI. Where decoding fails, report the raw topic hash rather than guessing a signature.
5. Aggregate. For distribution work, compute balances at a fixed block height, not at query time. For flow work, separate gross inflow, gross outflow, and net, and exclude internal self-transfers unless the question requires them.
6. Price consistently. Convert to USD using the declared pricing method. Report native-unit figures alongside USD.
7. Cross-check at least two sources (for example, a node read via RPC and an explorer export, or two independent indexers). Log any discrepancy with magnitude.
8. Write findings with a confidence tag per claim: high (directly observed on-chain and reproduced), medium (observed with a heuristic label or single source), low (inferred).

## Decision gates

Stop and request approval before proceeding if any of the following occur:
- The task requires interacting with a wallet, signing, or sending any transaction. Refuse by default; escalate to the user.
- The task asks to deanonymize an individual or link addresses to a named person. Require documented legal basis and a named accountable reviewer.
- The analysis would be shared externally (published report, client delivery, public post). Require explicit approval of the final content.
- Data sources require paid keys, scraping beyond published terms, or third-party uploads of sensitive addresses. Require approval.
- A finding suggests active exploit, unexplained mint, or unauthorized admin action. Escalate immediately; do not publish analysis until the owner of the affected system is notified.

Proceed without a gate for read-only queries against public data within the defined window.

## Verification and evidence

Each conclusion must cite: the block number or transaction hash, the decoded event or raw topic, the query timestamp, and the source. Checks before release:
- Totals reconcile: sum of per-address balances equals total supply within stated tolerance (zero for native-only, rounding tolerance for decimal tokens).
- Decimal handling is verified against the contract's decimals function, not assumed.
- Each cross-source discrepancy above 0.1 percent of the compared value is explained or flagged.
- No USD figure appears without its price source and timestamp.
- Every heuristic label is marked as heuristic.

Version-sensitive details (RPC method names, explorer API endpoints, indexer schemas, token standard extensions, EIP activation status) must be checked against current official documentation before being stated. If verification is unavailable, write "unverified against current documentation" next to the detail.

## Failure handling

- RPC rate limit or timeout: retry with bounded backoff, then narrow the block range. Do not fill gaps silently; report missing ranges.
- Unverified contract: analyze bytecode-level observations only and label behavior claims as unverified.
- Proxy upgraded mid-window: split the analysis at the upgrade block and analyze each implementation separately.
- Reorg suspicion: re-query blocks within the recent confirmation depth before finalizing; state the confirmation depth used.
- Conflicting sources that cannot be reconciled: report both values, state which is primary, and do not average them.

## Deliverable contract

Output a report with these sections in order:
1. Scope: network, identifiers, window (UTC and block range), question.
2. Method: sources, pricing convention, decoding approach, heuristics used.
3. Findings: numbered claims, each with value, confidence tag, and evidence reference.
4. Reconciliation: checks performed and their results.
5. Limitations: unverified items, missing data, label uncertainty.
6. Open actions: items needing approval or further data.

Do not include investment recommendations, price predictions, or statements that a project is or is not a scam. Do not state that any analysis guarantees compliance or security.
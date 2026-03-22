---
name: agent-wallet-expert
version: 1.0.0
description: Set up autonomous agent wallets using Virtuals Protocol ACP, Coinbase AgentKit, and x402 commerce protocol. Covers agent identity, wallet creation, agent-to-agent payments, and earning income from the agent economy without human intervention.
author: lous-creations
tags: [agent-wallet, ACP, x402, coinbase, virtuals-protocol, agent-economy]
---

# Agent Wallet Expert

## Before Starting
1. Which wallet infrastructure? Coinbase AgentKit or Virtuals Protocol ACP?
2. Agent-to-agent payments or human-to-agent payments?
3. Which blockchain? Base is recommended for low fees.

## Core Expertise Areas

### Virtuals Protocol ACP
ACP is the Agent Commerce Protocol — agents earn, spend, and transact autonomously.
CLI commands: setup, wallet, browse, job, token, profile, sell, serve.
Your agent gets its own wallet address and can hold tokens.
Other agents can discover and pay your agent for services via job queue.
Install: npx clawhub install virtuals-protocol-acp

### Coinbase AgentKit
Coinbase infrastructure for autonomous agent wallets.
Wallet creation: agentkit.create_wallet returns address and private key.
Fund wallet: send USDC or ETH to the wallet address.
Transactions: agentkit.transfer sends funds to another address.
MCP server available: connect to any AI agent in minutes.

### x402 Payment Protocol
HTTP 402 payment required header triggers micropayment.
Agent automatically pays to access premium API endpoints.
No human approval needed for payments below threshold.
Useful for: accessing paid data APIs, premium AI services, tool usage.

### Agent Economy Income
List your agent as a service provider on ACP marketplace.
Other agents pay your agent to execute tasks autonomously.
AgentDo task queue: post tasks for agents to pick up and earn.
MoltBook profile: agent-to-agent social network for discovery.

### Security Rules
Never store private key in plaintext config files.
Set maximum transaction limit per day to prevent runaway spending.
Use separate wallet for agent with limited funding.
Monitor wallet balance daily via Telegram alert.

## Best Practices
- Start with small test transactions before enabling autonomous payments
- Set hard daily spending limit before deploying
- Use Base network for low transaction fees
- Monitor all transactions in real time via wallet alerts

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Private key in plaintext | Always use encrypted secrets manager |
| No spending limit | Set hard daily limit before any autonomous spending |
| Wrong network fees | Use Base for low fees, avoid Ethereum mainnet |
| No transaction monitoring | Set up real-time alerts for all wallet activity |

## Related Skills
- openclaw-setup-expert
- agent-income-expert
- mcp-builder-expert

---
name: mcp-builder-expert
version: 1.0.0
description: Build Model Context Protocol servers to connect any API or service to any AI agent. Covers TypeScript and Python implementations, tool design, authentication, deployment, and publishing to MCP registries.
author: lous-creations
tags: [mcp, tools, api, integration, agents, typescript, python]
---

# MCP Builder Expert

## Before Starting
1. Which API or service to connect?
2. TypeScript or Python?
3. What tools should the MCP expose?

## Core Expertise Areas

### MCP Basics
MCP server exposes tools that AI agents can call.
Each tool has: name, description, input schema, handler function.
Transport: stdio for local, SSE for remote and cloud.
The description field is critical — agent decides which tool to call based on it.

### TypeScript Template


### Python Template with FastMCP


### Tool Design Principles
One tool per action, never bundle multiple operations into one tool.
Description must be crystal clear — agent reads description to decide.
Always validate inputs before calling external APIs.
Return structured text the agent can reason over directly.
Handle errors gracefully with descriptive messages not raw stack traces.

### Publishing to Registry
Package as npm or PyPI package for distribution.
List on MCP registry at modelcontextprotocol.io/registry.
ClawHub accepts MCP servers as advanced skills.

## Best Practices
- Write clear tool descriptions, agent uses them to decide which to call
- Keep each tool focused on one single action
- Always validate inputs before calling external APIs
- Handle all errors and return descriptive error messages
- Use environment variables for all API keys never hardcode

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Vague tool descriptions | Be specific about what each tool does and when to use it |
| One tool doing everything | Split into focused single-action tools |
| No error handling | Always catch and return descriptive error messages |
| Hardcoded API keys | Use environment variables for all secrets |

## Related Skills
- openclaw-setup-expert
- clawhub-publisher
- agent-income-expert

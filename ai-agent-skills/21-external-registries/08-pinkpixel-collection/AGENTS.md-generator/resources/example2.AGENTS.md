This is an example of a very thorough and detailed AGENTS.md file. Most codebases would not need this much information, nor would the files be as long, but this is a good reference and covers all areas.

# AGENTS.md example

This file provides guidance to AI coding agents when working with code in this repository: **ReCodeAgent**.

**Your Core Skills**: (.agents/skills/)

- ['ast-grep' Command Line Tool AST-based Code Search and Refactoring Skill](.agents/skills/ast-grep/SKILL.md)
- ['ReCodeAgent-CodexCLI-TB2-Harbor-Evaluate-ENV-Operation'](.agents/skills/ReCodeAgent-TB2-Evaluate/SKILL.md)

**References**:
- (./2510.23564v2.md) Core ReCode Paper!!! MUST READ!!!
- ReCodeAgent-Codex-TB2 Harbor ENV Run terminal-bench-2 BENCHMARK Evaluate TASKs Operation Skill: (.agents/skills/ReCodeAgent-TB2-Evaluate/SKILL.md)
- SPECIFICATION: (dev-spec/)
- DEV-WORKLOGS: (.worklogs/)
- RECODE-PAPER-DEMO: (.dev-docs/)
- CODEX-CLI-Docs: (.knowledge/codex-cli/docs/)
- CODEX-CLI-TypeScript-SDK: (.knowledge/codex-cli/sdk/typescript/)
- RECODE-AGENT-ARCHITECTURE: (dev-spec/architecture/RECODE_ARCHITECTURE_V0.1.0.md)
- ROADMAP: (dev-spec/roadmap/ROADMAP_V2_2025111602.md)
---

## ReCodeAgent -> (codex exec) -> Harbor -> Terminal-Bench 2.0 Evaluate TASKs Run

ReCodeAgent now uses **Harbor Container-Unified Architecture** to run Terminal-Bench 2.0 tasks.

### ReCodeAgent-Codex-TB2 Evolve Task Run Unified Runtime ENV Running Tasks

```bash
# Harbor containerized run (recommended)
cd ~/harbor-workspace
harbor run -d terminal-bench@2.0 -t <task-name> -a recode-agent

# Specify template
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent \
  --agent-kwarg template=recode_tb2_prompt.jinja2
```

### ReCodeAgent-Codex-TB2 Evolve Task cargo run TB2 Test

```bash
cargo run --release --manifest-path recode-core/Cargo.toml -- \
  --task <task-name or none task for random task selection> \
  --prompt <prompt-template-name> \
  --max-steps <max-steps default: 99999>
```

```bash
./scripts/run_tb2_test.sh \
    --task <task-name or none task for random task selection> \
    --prompt <prompt-template-name> \
    --max-steps <max-steps default: 99999>
```

### Key Files

| Purpose | Path |
|---------|------|
| Rust CLI entry | `recode-core/src/main.rs` |
| Python bridge script | `scripts/terminal_bench_bridge.py` |
| Prompt templates | `recode-core/templates/*.jinja2` |
| Harbor environment guide | `.agents/skills/ReCodeAgent-TB2-Evaluate/SKILL.md` |

### Additional References

- Codex CLI Source Code Reference: (~/dev-space/codex-cli)
- TB2 Terminal-Bench 2.0 Benchmark Dataset: (~/dev-space/terminal-bench-2)
- TB2-Harbor Framework Source Code Reference: (~/dev-space/harbor)
- TB2 Harbor Framework Documentation: <https://harborframework.com/docs/running-tbench>
- TB2 Harbor Framework Datasets Documentation: <https://harborframework.com/docs/datasets>

---

## Project Overview

ReCodeAgent is a research project implementing the ReCode paper ([arXiv:2510.23564](https://arxiv.org/abs/2510.23564)) - a novel LLM-based AI agent paradigm that achieves universal granularity control through recursive code generation. The project aims to productionize the academic prototype into a high-performance **Rust Core + Codex CLI** integrated system.

**Core Innovation**: ReCode unifies plans and actions into a single code representation, enabling dynamic granularity control. High-level tasks are represented as placeholder functions that recursively expand into finer-grained subtasks until reaching executable primitive actions.

**Current Status**: Production-ready Rust implementation with Harbor integration for Terminal-Bench 2.0 evaluation.

```tree
recode-core/
├── Cargo.toml
├── Cargo.lock
├── Dockerfile                 # Container image config
│
├── examples/
│   └── terminal_bench_smoke.rs  # Quick local test (10 steps)
│
├── harbor-assets/             # Harbor deployment assets
│   ├── recode-agent           # Linux x86_64 binary
│   └── templates/             # Deployment templates
│
├── templates/                 # Jinja2 ReCodeAgent Prompts templates (source)
│   ├── recode_tb2_agents_md.jinja2      # Default TB2 AGENTS.md template
│   ├── recode_tb2_prompt.jinja2         # Default TB2 terminal-bench-2 task prompt
│   ├── recode_microtexecute_tb2_prompt.jinja2  # Micro-Steps TB2 task version
│   ├── recode_tb2_checkpoint_minimal.jinja2    # Minimal version
│   └── fewshots/              # Few-shot examples (old version, need update)
│
├── src/
│   ├── lib.rs
│   ├── main.rs                # CLI entry (subcommands: run, render-template, execute)
│   │
│   ├── analysis/
│   │   ├── mod.rs
│   │   └── ast_splitter.rs
│   │
│   ├── codex/
│   │   ├── mod.rs
│   │   └── thread_manager.rs  # Codex CLI integration (codex exec --json)
│   │
│   ├── environments/
│   │   ├── mod.rs
│   │   ├── alfworld.rs
│   │   ├── process_bridge.rs
│   │   ├── terminal_bench.rs
│   │   └── webshop.rs
│   │
│   ├── execution/
│   │   ├── mod.rs
│   │   ├── env_adapter.rs
│   │   ├── env_factory.rs
│   │   └── python_executor.rs  # Note: includes import re, os fix
│   │
│   ├── orchestrator/
│   │   ├── mod.rs
│   │   ├── engine.rs          # Codex prompt assembly
│   │   └── runtime.rs         # DFS tree execution + checkpoint mechanism
│   │
│   └── tree/
│       ├── mod.rs
│       ├── context.rs
│       ├── node.rs
│       └── tree.rs
│
└── tests/
    ├── codex_turn_tests.rs
    ├── context_tests.rs
    ├── orchestrator_tests.rs
    └── fixtures/
        └── codex_echo.jsonl
```

---

## Architecture

### Harbor Container-Unified Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                   macOS Development Environment (Host)          │
├─────────────────────────────────────────────────────────────────┤
│  ReCodeAgent Repository                                         │
│  ~/dev-space/ReCodeAgent/                                       │
│  ├── recode-core/src/           # Rust source code              │
│  └── recode-core/templates/     # Jinja2 Prompt templates (src) │
├─────────────────────────────────────────────────────────────────┤
│  Harbor Installation Directory                                  │
│  ~/.local/share/uv/tools/harbor/.../agents/installed/           │
│  ├── recode_agent.py            # Harbor Agent definition       │
│  └── recode-assets/             # Deployment assets             │
│      ├── recode-agent           # Linux x86_64 binary           │
│      ├── templates/             # Jinja2 templates              │
│      └── scripts/               # Python bridge scripts         │
└─────────────────────────────────────────────────────────────────┘
                              │ Docker Volume
                              │ ${HOME}/.codex:/tmp/host-codex:ro
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│             Docker Container (Terminal-Bench 2.0)               │
├─────────────────────────────────────────────────────────────────┤
│  /app/                        # Working directory               │
│  ├── recode-agent             # ReCodeAgent binary              │
│  ├── AGENTS.md                # Rendered system prompt          │
│  │                            # (auto-loaded by Codex)          │
│  ├── instruction.md           # Task instruction                │
│  ├── templates/               # Jinja2 templates                │
│  └── .codex/                  # Codex CLI config                │
│      ├── auth.json            # Auth (copied from host)         │
│      └── config.toml          # Model configuration             │
└─────────────────────────────────────────────────────────────────┘
```

### Execution Flow (Harbor Mode)

```text
harbor run -d terminal-bench@2.0 -t <task> -a recode-agent
    │
    ▼
┌─────────────────┐
│ 1. Upload Assets│  recode-agent binary, templates/, scripts/
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 2. Install Script│  install-recode-agent.sh.j2
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 3. Execute Steps│  command-0 → command-1 → command-2 → command-3
└───────┬─────────┘
        │
        ├──▶ Step 1: Setup Codex auth (copy auth.json, config.toml)
        │
        ├──▶ Step 2: Render AGENTS.md (recode-agent render-template)
        │
        ├──▶ Step 3: Execute task (recode-agent execute + codex exec)
        │             └── DFS tree traversal + checkpoint self-verification
        │
        └──▶ Step 4: Cleanup
```

### CLI Subcommand Structure

```rust
enum Command {
    /// Legacy: Run with explicit bridge configuration
    Run { env_kind, python, bridge, bridge_args, instruction },

    /// Render AGENTS.md template (Harbor Step 2)
    RenderTemplate { template, output, task_name, instruction_path },

    /// Execute task (Harbor Step 3) - Core execution engine
    Execute { task_name, instruction, working_dir, max_steps, codex_home },
}
```

---

## Development Commands

### Harbor Test Run

"(~/harbor-workspace) is the default running harbor workspace path for TB2 test logs."

```bash
cd ~/harbor-workspace

# Basic run
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent

# Specify template
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent \
  --agent-kwarg template=recode_tb2_prompt.jinja2

# Limit steps + debug
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent \
  --agent-kwarg max_steps=50 --debug

# Batch run all tasks
harbor run -d terminal-bench@2.0 -a recode-agent -n 4
```

### Rust Build

```bash
cd ~/dev-space/ReCodeAgent

# Local macOS build (development testing)
cargo build --release --manifest-path recode-core/Cargo.toml

# Linux x86_64 build (Harbor container)
docker build --platform linux/amd64 -f Dockerfile.build-x86 -t recode-builder .
docker create --name tmp recode-builder
docker cp tmp:/build/recode-core/target/release/recode-core ./recode-agent-linux-x86_64
docker rm tmp

# Verify
file ./recode-agent-linux-x86_64
# Should output: ELF 64-bit LSB pie executable, x86-64...
```

### Sync to Harbor

```bash
HARBOR_ASSETS=~/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets

# Sync binary
cp ./recode-agent-linux-x86_64 $HARBOR_ASSETS/recode-agent
chmod +x $HARBOR_ASSETS/recode-agent

# Sync templates
cp -r recode-core/templates/*.jinja2 $HARBOR_ASSETS/templates/

# Sync scripts
cp scripts/terminal_bench_bridge.py $HARBOR_ASSETS/scripts/
```

### Local Quick Test

```bash
# Smoke test (10 steps)
cargo run --example terminal_bench_smoke --release

# CLI subcommand test
cargo run --release --manifest-path recode-core/Cargo.toml -- \
  execute --task-name test --instruction "test" --working-dir /tmp --max-steps 5
```

### View Results

```bash
# Latest task results
ls -lt ~/harbor-workspace/jobs/ | head -3

# Execution logs
cat ~/harbor-workspace/jobs/<job-id>/<task-id>/agent/command-2/stdout.txt | tail -50

# Verification result
cat ~/harbor-workspace/jobs/<job-id>/<task-id>/verifier/reward.txt
```

---

## RECODE Core Methodology

### PRELIMINARY

#### Decision Process of LLM-based AI-Agent

We model the interaction between LLM-based AI-Agent and its environment as a simplified decision process:

$\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{O}, T, R \rangle$

Where:

- $\mathcal{S}$ : **State space**
- $\mathcal{A}$ : **Primitive action space**
- $\mathcal{O}$ : **Observation space**
- $T: \mathcal{S} \times \mathcal{A} \rightarrow \mathcal{S}$ : **Transition function**
- $R: \mathcal{S} \times \mathcal{A} \rightarrow \mathbb{R}$ : **Reward function**

At each step, the AI-Agent receives an observation $o \in \mathcal{O}$ and generates decisions that ultimately translate into executable primitive actions $a \in \mathcal{A}$.

Beyond the primitive action space, we introduce a **plan space** $\mathcal{P}$, which contains **intentions** and **goals** that cannot be directly executed but must be refined into a sequence of primitive actions or intermediate sub-plans with coarser granularity. We define the **decision space** as $\mathcal{D} = \mathcal{A} \cup \mathcal{P}$, representing all possible outputs that AI-Agent can produce at different granularities.

**Decision Granularity**: Real-world tasks require decisions at different granularities. Fine-grained decisions in $\mathcal{A}$ correspond to immediately executable primitive operations, such as `run('crack egg')`, while coarse-grained decisions in $\mathcal{P}$ represent high-level intentions that need decomposition, such as `prepare_breakfast()`.

**The granularity forms a natural hierarchy**: Taking breakfast preparation as an example, the decision "prepare breakfast" is coarser than "cook eggs", which is coarser than "crack egg". Each level contains broader goals and longer time horizons.

### METHOD OVERVIEW

**ReCode** achieves global control over decision granularity through recursive code generation. The core is **unifying plan and action** into the same representation.

**Unify Plan and Action**:
We represent both plans and actions as **Python function calls**. Actions are executable, like `run('click button')`. Plans are represented as placeholder functions, like `prepare_breakfast()` and `get_ingredients()`.

**Recursive Code Generation**:

```pseudocode
Algorithm 1: The ReCode Algorithm

Procedure ReCode(T, π, E, c):
    if c is None:                      // Initialize
        o_0 ← Reset(E)                 // Reset environment
        c ← Text2Code(T, o_0)          // Convert task to root placeholder
    end if

    code block ← π(c)                  // LLM generates child code

    for each child u in code block:
        if IsPrimitive(u):             // Primitive action
            Execute(u, E)
        else:                          // Placeholder function
            ReCode(T, π, E, u)         // Recursive expansion
        end if
    end for
end procedure
```

### IMPLEMENTATION DETAILS

**Task Initialization**: Task instruction → root placeholder function `solve(instruction, observation)`

**Context Management**: Unified variable namespace, persisted across recursion levels

**Error Handling**: Self-correction loop (max_rewrite=5)

**Recursion Control**: Maximum recursion depth 10

**Checkpoint Mechanism** (new): DFS tree completion ≠ task solved, inject checkpoint for agent self-verification

---

## Key Configuration

### Prompt Templates

| Template | Purpose | Default |
|----------|---------|---------|
| `recode_tb2_agents_md.jinja2` | AGENTS.md system prompt | ✓ |
| `recode_tb2_prompt.jinja2` | TB2 task prompt | |
| `recode_microtexecute_tb2_prompt.jinja2` | Codex expansion micro-execution | |
| `recode_tb2_checkpoint_minimal.jinja2` | Checkpoint verification | |

### Harbor Agent Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `template` | string | `recode_tb2_agents_md.jinja2` | Jinja2 template filename |
| `max_steps` | int | 99999 | DFS tree maximum steps |

Usage: `--agent-kwarg template=xxx --agent-kwarg max_steps=<max-steps default: 99999>`

---

## Codex CLI Integration

- Authentication: `~/.codex/auth.json` (copied to container `/app/.codex/`)
- Model config: `~/.codex/config.toml` (default: gpt-5.1-codex-max)
- AGENTS.md: Auto-discovered and loaded (95%+ token savings)
- Command: `codex exec --json` for JSONL event streaming

---

## Quick Reference

```bash
# Run task
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent

# Build Linux binary
docker build --platform linux/amd64 -f Dockerfile.build-x86 -t recode-builder .

# Sync templates (quick)
cp recode-core/templates/*.jinja2 ~/.local/share/uv/tools/harbor/.../recode-assets/templates/

# View latest results
cat ~/harbor-workspace/jobs/$(ls -t ~/harbor-workspace/jobs | head -1)/*/agent/command-2/stdout.txt | tail -50

# Detailed environment guide
cat .agents/skills/ReCodeAgent-TB2-Evaluate/SKILL.md
```
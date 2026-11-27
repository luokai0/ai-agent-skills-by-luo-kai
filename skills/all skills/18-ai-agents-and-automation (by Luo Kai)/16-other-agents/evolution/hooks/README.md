# Makepad Skills Hooks

This folder contains Claude Code hooks to enable automatic triggering of makepad-skills features.

## Quick Setup

The easiest way to install hooks is using the installer:

```bash
curl -fsSL https://raw.githubusercontent.com/ZhangHanDong/makepad-skills/main/install.sh | bash -s -- --with-hooks
```

This will:
1. Copy skills to `.claude/skills/`
2. Copy hooks to `.claude/hooks/`
3. Create `.claude/settings.json` with hook configuration

## Manual Setup

Copy the hooks to `.claude/hooks/` and add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/makepad-skill-router.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/pre-tool.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/post-bash.sh"
          }
        ]
      }
    ]
  }
}
```

## Hooks Overview

| Hook | Trigger | Purpose |
|------|---------|---------|
| `makepad-skill-router.sh` | UserPromptSubmit | Auto-route queries to relevant skills |
| `pre-tool.sh` | Before Bash/Write/Edit | Detect Makepad version, validate dev branch |
| `post-bash.sh` | After Bash command | Detect compilation errors, suggest fixes |
| `session-end.sh` | Session ends | Prompt for evolution review (optional) |

## How It Works

1. **Skill Routing** (`makepad-skill-router.sh`): Analyzes user input and outputs JSON with `systemMessage` telling Claude which skills to load
2. **Version Detection** (`pre-tool.sh`): On first tool use, detects Makepad branch from Cargo.toml
3. **Error Detection** (`post-bash.sh`): Monitors `cargo build/run` output for common Makepad errors
4. **Evolution Prompt** (`session-end.sh`): Reminds to capture learnings at session end

## Output Format

Hooks output JSON that Claude Code interprets:

```json
{
  "continue": true,
  "systemMessage": "[makepad-skills] IMPORTANT: Before responding, you MUST call these skills: Skill(makepad-widgets), Skill(makepad-layout). These skills contain essential Makepad patterns and APIs."
}
```

---

## Optional: UI Specification Checker

The `pre-ui-edit.sh` hook checks UI code completeness to prevent text overlap issues.

### Prerequisites

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt install jq
```

### Setup

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/pre-ui-edit.sh"
          }
        ]
      }
    ]
  }
}
```

### What It Checks

When writing UI code (Button, Label, TextInput, RoundedView), checks for 5 properties:
- `width` - Fit / Fill / number
- `height` - Fit / Fill / number
- `padding` - { left, right, top, bottom } or number
- `draw_text` - { text_style, color }
- `wrap` - Word / Line / Ellipsis

If fewer than 3 properties are present, blocks and shows reminder.

### Technical Details

- Input: JSON via stdin `{"tool_name": "Edit", "tool_input": {...}}`
- Output: JSON with `continue: false` to block
- Exit code: `0` = allow, `2` = block

---
name: skill-validator
description: Validate Agent Skills against the specification. Checks SKILL.md format, frontmatter fields, naming conventions, and directory structure.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - validation
  - compliance
  - tooling
  - quality
---

## Instructions

Use this skill to validate any Agent Skill directory against the specification before publishing. The validator checks:

- **SKILL.md presence** - Required manifest file exists
- **Frontmatter format** - Valid YAML frontmatter with required fields
- **Name validation** - 1-64 chars, lowercase, hyphens only, starts with letter
- **Name-directory match** - Name field matches the directory name
- **Description validation** - 1-1024 characters, non-empty
- **Structure validation** - Valid folder organization

### When to Use

- Before submitting a skill for publication
- After making changes to SKILL.md
- To diagnose why a skill was rejected
- As part of CI/CD pipelines

### How to Use

Validate a skill directory:

```
Validate the skill at /path/to/my-skill
```

Get JSON output for CI integration:

```
python3 validate_skill.py /path/to/my-skill --json
```

### Output

```
✓ Skill Validation Report
  Skill: pdf-tools
  Status: COMPLIANT (100/100)

  Checks:
    ✓ SKILL.md exists
    ✓ Valid frontmatter
    ✓ Name format valid (pdf-tools)
    ✓ Name matches directory
    ✓ Description valid (45 chars)
    ✓ Structure valid

  No issues found.
```

Or if issues are found:

```
✗ Skill Validation Report
  Skill: My-Skill
  Status: NON-COMPLIANT (40/100)

  Checks:
    ✓ SKILL.md exists
    ✓ Valid frontmatter
    ✗ Name format invalid
    ✗ Name doesn't match directory
    ✓ Description valid
    ✓ Structure valid

  Issues:
    - Name must be lowercase with hyphens only (got "My-Skill")
    - Name 'My-Skill' doesn't match directory 'my-skill'
```

## Examples

**Basic validation:**
```
User: Validate the skill at ./document-skills/pdf
Agent: Running validation on ./document-skills/pdf...
       ✓ Skill is compliant (100/100)
```

**Fix validation errors:**
```
User: Why is my skill failing validation?
Agent: Let me check... Running validator...
       The name field uses underscores. Change "pdf_tools" to "pdf-tools".
```

## Limitations

- Does not validate skill functionality (only structure/format)
- Does not run safety scans (use skill-safety-scanner for that)
- Requires local filesystem access to the skill directory

## Dependencies

- Python 3.9+
- PyYAML (optional, falls back to basic parsing)

---
name: skill-publisher
description: Submit Agent Skills to catalogs for publication. Validates, scans, and submits skills via the skillscatalog.ai API.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - publishing
  - catalog
  - api
---

## Instructions

Use this skill to submit Agent Skills for publication to skillscatalog.ai or organization catalogs.

### Prerequisites

1. **Skill Key** - Get your key at https://skillscatalog.ai/settings/skill-keys
2. **Valid Skill** - Your skill must pass validation (run skill-validator first)
3. **Safety Scan** - Skills are automatically scanned before submission

### How to Use

Submit a skill for publication:

```
Submit the skill at /path/to/my-skill for publication
```

Specify a target catalog:

```
python3 publish_skill.py /path/to/my-skill --catalog public
python3 publish_skill.py /path/to/my-skill --catalog org --org-id abc123
```

### Workflow

1. **Validate** - Checks SKILL.md frontmatter and structure
2. **Scan** - Runs safety scan for secrets and dangerous code
3. **Submit** - Sends skill to the API for review
4. **Review** - Wait for catalog maintainer approval

### Output

```
Publishing skill: my-skill
  Validating... OK
  Scanning safety... Grade A (100/100)
  Submitting to public catalog...

  Success! Publication request submitted.
  Request ID: pub_abc123
  Status: pending_review

  Track your submission at:
  https://skillscatalog.ai/my-skills
```

## Examples

**Submit to public catalog:**
```
User: Publish my skill at ./pdf-tools to the catalog
Agent: Running publication workflow...

       Validation: Passed
       Safety Scan: Grade A (100/100)

       Submitted to public catalog.
       Request ID: pub_xyz789
       Status: pending_review
```

**Submit to organization catalog:**
```
User: Publish ./internal-tools to the acme-corp catalog
Agent: Running publication workflow...

       Validation: Passed
       Safety Scan: Grade B (85/100)

       Submitted to acme-corp organization catalog.
       Request ID: pub_abc456
```

## Limitations

- Requires internet connection to submit
- Skills must pass validation before submission
- Skill Key must have publish permissions
- Large skills (>10MB) may be rejected

## Dependencies

- Python 3.9+
- requests library
- skill-validator (for pre-validation)
- skill-safety-scanner (for pre-scan)

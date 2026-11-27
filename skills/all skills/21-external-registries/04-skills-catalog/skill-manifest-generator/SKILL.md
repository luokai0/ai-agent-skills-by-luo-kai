---
name: skill-manifest-generator
description: Generate MANIFEST.json files for Agent Skills, providing content integrity verification, file inventory, and external reference tracking.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - manifest
  - integrity
  - validation
  - tooling
---

## Instructions

Use this skill to generate a MANIFEST.json file for any Agent Skill directory. The manifest provides:

- **Integrity verification** - SHA256 hashes for all files and an overall integrity hash
- **File inventory** - Complete listing of files with sizes and types
- **External URL detection** - URLs found in code that reference external resources
- **Structure analysis** - Folder depth, file counts, and organization

### When to Use

- Before publishing a skill to a catalog
- To verify a skill hasn't been modified
- To audit external dependencies in a skill
- To validate skill structure and compliance

### How to Use

Run the manifest generator on a skill directory:

```
Generate a manifest for the skill at /path/to/my-skill
```

Or to verify an existing manifest:

```
Verify the manifest for /path/to/my-skill
```

### Output

The generator creates a `MANIFEST.json` file in the skill root containing:

```json
{
  "$schema": "https://agentskills.io/schemas/manifest.v1.json",
  "manifestVersion": "1.0",
  "generatedAt": "2025-01-15T10:30:00Z",
  "generator": "skill-manifest-generator/1.0.0",
  "skill": {
    "name": "my-skill",
    "version": "1.0.0"
  },
  "integrity": {
    "algorithm": "sha256",
    "hash": "a1b2c3d4..."
  },
  "files": [...],
  "externalReferences": [...],
  "structure": {...}
}
```

## Examples

**Generate a manifest:**
```
User: Generate a manifest for the skill at ./pdf-tools
Agent: I'll generate a MANIFEST.json for the pdf-tools skill...
       [Runs generate_manifest.py]
       Created MANIFEST.json with:
       - 12 files inventoried
       - Integrity hash: sha256:abc123...
       - 2 external URLs detected
       - Max folder depth: 2
```

**Verify a manifest:**
```
User: Verify the manifest for ./pdf-tools
Agent: I'll verify the MANIFEST.json matches the current files...
       [Runs generate_manifest.py --verify]
       ✓ All 12 files match their recorded hashes
       ✓ No new untracked files found
       ✓ Integrity hash verified
```

## Limitations

- Binary files are hashed but not scanned for URLs
- URL detection uses regex patterns, may have false positives in comments
- Maximum skill size: 50MB total, 10MB per file
- Maximum file count: 1000 files
- Maximum folder depth: 6 levels

## Dependencies

- Python 3.9+
- PyYAML (for SKILL.md frontmatter parsing)
- No other external dependencies (uses Python stdlib)

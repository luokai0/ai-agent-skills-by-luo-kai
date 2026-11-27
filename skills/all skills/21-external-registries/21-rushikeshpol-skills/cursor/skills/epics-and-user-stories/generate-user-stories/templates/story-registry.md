# Story Registry Template

> This template defines the format for `story-registry.md` — the cumulative cross-story tracker created during story generation.

## Format

```markdown
# Story Registry: [Feature Name]

**Feature:** [name]
**Total stories:** [count written] / [count planned]
**Last updated:** [date]

## Conventions
[Established after first story is approved. All subsequent stories must follow.]

- **Key terms:** [term → definition, consistent across all stories]
- **Persona names:** [exact names used, from project-context or requirements]
- **API naming style:** [camelCase/snake_case, endpoint patterns]
- **Date/time format:** [ISO 8601, locale-specific, etc.]
- **Platform conventions:** [FE/BE/Mobile naming patterns]

## Stories

| # | File | Title | Platform | User Statement (short) | Key Fields/Endpoints | Boundary | Status |
|---|------|-------|----------|----------------------|---------------------|----------|--------|
| 1 | [filename] | [title] | FE/BE | [1-line summary] | [fields or endpoints this story owns] | [what this story covers and does NOT cover] | ✅ Approved / 📝 Draft |

## Dependencies

| Story | Depends On | What It Needs |
|-------|-----------|---------------|
| [story #] | [story #] | [specific data/API/behavior needed] |
```

## Rules

1. **One entry per story** — added immediately after story is saved
2. **Boundary column is critical** — prevents overlap between stories. Each story explicitly states what it owns.
3. **Key Fields/Endpoints** — prevents two stories from claiming the same field or endpoint
4. **Conventions section** — established after first story, read by all subsequent sub-agents
5. **Keep compact** — registry must stay under ~500 tokens. If over, summarize older entries (keep boundary + key fields, compress user statement).
6. **Never the source of truth for validation** — `validate-user-stories` always builds a fresh registry from actual files

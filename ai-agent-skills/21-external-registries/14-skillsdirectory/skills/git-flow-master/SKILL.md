---
name: git-flow-master
description: Expert git workflow manager for perfect commits, branches, PR descriptions, merge strategies, and changelogs. Use when managing git repositories, writing commit messages, creating PRs, or resolving merge conflicts.
license: CC0-1.0
compatibility: Works with Cursor, Windsurf, GitHub Copilot, Claude Code, and any AI coding assistant
metadata:
  author: skillsdirectory
  version: "1.0"
  category: coding
  tools: cursor, windsurf, copilot, claude-code
---

# Git Flow Master

You are an expert at git workflows, writing perfect commit messages, and managing branches professionally.

## Commit Messages (Conventional Commits)

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | When |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting (no code change) |
| `refactor` | Code change (no feature/fix) |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `chore` | Build, deps, config |
| `ci` | CI/CD changes |

### Examples
```
✅ feat(auth): add OAuth2 login with Google
✅ fix(cart): prevent duplicate items on rapid clicks
✅ docs(api): add rate limiting section to README
✅ refactor(utils): extract date formatting to shared module

❌ fixed stuff
❌ WIP
❌ update
❌ asdf
```

## Branching Strategy

```
main (production)
├── develop (staging)
│   ├── feature/user-authentication
│   ├── feature/payment-integration
│   ├── bugfix/cart-duplicate-items
│   └── hotfix/security-patch-xss
```

### Branch Naming
- `feature/short-description`
- `bugfix/issue-number-description`
- `hotfix/critical-fix`
- `release/v1.2.0`

## Pull Request Template

```markdown
## What does this PR do?
[1-2 sentence summary]

## Type of change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## How to test
1. Step 1
2. Step 2
3. Expected result

## Screenshots (if UI change)
[Before/After]

## Checklist
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
```

## Merge Strategies
| Strategy | When |
|---|---|
| **Squash & Merge** | Feature branches (clean history) |
| **Merge Commit** | Release branches (preserve history) |
| **Rebase** | Linear history preference |

## Conflict Resolution
1. `git fetch origin`
2. `git rebase origin/main`
3. Fix conflicts file by file
4. `git add .` → `git rebase --continue`
5. Test everything before pushing

# Constraint Registry — Template and Rules

**Referenced by:** All 5 planning skills. Created by `release-sprint-planner`, updated by `meeting-to-plan-integrator`, read by all.

---

## Location

`[release-root]/.meta/constraint-registry.md`

---

## Template

```markdown
# Constraint Registry — [Release Name]

| # | Constraint | Type | Source | Added By | Affects |
|---|-----------|------|--------|----------|---------|
| CR-1 | [Description] | [Timeline/Scope/Technical/Compliance/Team] | [Source document or decision] | [skill-name] | [Which sprints or features] |
```

---

## Rules

1. **Created by** `release-sprint-planner` during Release Definition (T3). Populated with constraints extracted from the release definition sections: timeline, team, scope-out, known constraints.
2. **Updated by** `meeting-to-plan-integrator` when meeting decisions introduce new constraints (e.g., "Chat deferred to Phase 2" becomes a scope constraint).
3. **Read by** all 5 skills before generating output. Load at intake, check during guardrail evaluation.
4. **Guardrails check** generated documents against active constraints. If a generated sprint plan contradicts an active constraint, the guardrail fires.
5. **Never remove** constraints. When a constraint is resolved or no longer applies, mark it `[RESOLVED]` with date and reason:

```markdown
| CR-3 | ~~Chat deferred to Phase 2~~ `[RESOLVED 2026-06-15: moved to Phase 1 per stakeholder request]` | Scope | user decision, May 5 | meeting-to-plan-integrator | All |
```

---

## Constraint Types

| Type | Description | Example |
|------|-------------|---------|
| **Timeline** | Hard dates that cannot move | "Aug 2026 hard deadline" |
| **Scope** | Features or work explicitly included or excluded | "No new features after Sprint 6" |
| **Technical** | Platform, architecture, or integration constraints | "Must support iOS 16+ and Android 12+" |
| **Compliance** | Regulatory, legal, or certification requirements | "PAGA compliance required for meal attestation" |
| **Team** | Staffing, availability, or organizational constraints | "Lead dev on PTO Sprint 3, Week 1" |

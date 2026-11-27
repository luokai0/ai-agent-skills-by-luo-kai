---
name: formal-methods-expert
version: 1.0.0
description: Expert-level formal methods covering formal specification, model checking, theorem proving, type theory, program verification, and formal languages.
author: luo-kai
tags: [formal methods, verification, model checking, type theory, Coq, TLA+]
---

# Formal Methods Expert

## Before Starting
1. Specification, verification, or proof?
2. Hardware, software, or protocol verification?
3. Which tool? (TLA+, Coq, Isabelle, Alloy, Z3)

## Core Expertise Areas

### Formal Specification
TLA+: temporal logic of actions, specifies concurrent and distributed systems.
Alloy: relational modeling, finds counterexamples by bounded model checking.
Z notation: set theory and predicate logic, used in safety-critical systems.
VDM: Vienna Development Method, pre/post conditions and invariants.

### Model Checking
State space exploration: exhaustively check all reachable states.
LTL: linear temporal logic — always, eventually, until, next.
CTL: computation tree logic — for all paths, there exists a path.
BDD: binary decision diagrams — symbolic state space representation.
Counterexample: model checker finds violation trace, useful for debugging.

### Theorem Proving
Coq: dependent types, constructive logic, extract verified code.
Isabelle/HOL: higher-order logic, powerful automation, used in OS verification.
Lean: modern proof assistant, mathlib library, growing adoption.
Interactive vs automated: interactive guides proof, automation handles subgoals.

### Type Theory
Simply typed lambda calculus: types prevent certain errors, Curry-Howard correspondence.
Dependent types: types that depend on values — encode properties in types.
Linear types: track resource usage, ensure resources used exactly once.
Gradual typing: mix static and dynamic typing safely.

### Program Verification
Hoare logic: pre-condition, command, post-condition triples.
Weakest precondition: compute weakest condition that guarantees post-condition.
Loop invariants: property maintained through each iteration.
SMT solvers: Z3, CVC5 — decide satisfiability of logic formulas automatically.

## Best Practices
- Start with lightweight formal methods before full verification
- Use model checking for protocol verification, theorem proving for algorithms
- Write specs before implementation to catch design errors early
- Keep models small enough to be tractable

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| State explosion in model checking | Use abstractions and symmetry reduction |
| Spec that verifies but is wrong | Validate spec against expected behaviors |
| Automation fails on complex goals | Break into lemmas, guide automation |
| Forgetting fairness conditions | Liveness properties require fairness assumptions |

## Related Skills
- mathematical-logic-expert
- compiler-design-expert
- algorithms-cs-expert

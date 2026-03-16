---
name: mathematical-logic-expert
description: Expert-level mathematical logic knowledge. Use when working with propositional logic, first-order logic, proof theory, model theory, computability theory, Godel incompleteness theorems, set theory, type theory, or formal verification. Also use when the user mentions 'formal proof', 'Godel', 'incompleteness', 'Turing machine', 'decidability', 'Zermelo-Fraenkel', 'axiom of choice', 'model theory', 'completeness theorem', 'computability', 'formal language', or 'type theory'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Mathematical Logic Expert

You are a world-class logician with deep expertise in propositional and first-order logic, proof theory, model theory, set theory, computability theory, Godel's theorems, and the foundations of mathematics.

## Before Starting

1. **Topic** — Propositional logic, FOL, set theory, computability, or Godel?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Prove theorem, understand concept, or apply to CS/math foundations?
4. **Context** — Pure logic, foundations of math, theoretical CS, or formal verification?
5. **Approach** — Syntactic (proof theory) or semantic (model theory)?

---

## Core Expertise Areas

- **Propositional Logic**: syntax, semantics, normal forms, resolution
- **First-Order Logic**: terms, formulas, quantifiers, interpretations
- **Proof Theory**: natural deduction, sequent calculus, Hilbert systems
- **Model Theory**: structures, satisfaction, completeness, compactness
- **Set Theory**: ZFC axioms, ordinals, cardinals, forcing
- **Computability**: Turing machines, decidability, reducibility, Rice's theorem
- **Godel's Theorems**: incompleteness, undecidability, implications
- **Type Theory**: simply typed λ-calculus, dependent types, Curry-Howard

---

## Propositional Logic
```
Syntax:
  Atomic propositions: p, q, r, ...
  Connectives: ¬, ∧, ∨, →, ↔
  Formation rules: if φ,ψ formulas then ¬φ, φ∧ψ, φ∨ψ, φ→ψ, φ↔ψ formulas

Semantics:
  Valuation: v: Prop → {T,F}
  Truth conditions:
    v(¬φ) = T iff v(φ) = F
    v(φ∧ψ) = T iff v(φ)=T and v(ψ)=T
    v(φ∨ψ) = T iff v(φ)=T or v(ψ)=T
    v(φ→ψ) = T iff v(φ)=F or v(ψ)=T
    v(φ↔ψ) = T iff v(φ)=v(ψ)

Satisfiability and validity:
  φ satisfiable: ∃v: v(φ)=T
  φ valid (tautology): ∀v: v(φ)=T  (written ⊨φ)
  φ,ψ logically equivalent: φ⊨ψ and ψ⊨φ  (same truth tables)
  Γ⊨φ: semantic entailment (φ true in all models of Γ)

Normal forms:
  CNF (Conjunctive Normal Form): ∧ of (∨ of literals)
  DNF (Disjunctive Normal Form): ∨ of (∧ of literals)
  Every formula has equivalent CNF and DNF
  Conversion: distribute ∧ over ∨ (CNF) or ∨ over ∧ (DNF)

Resolution:
  Rule: (A∨p) ∧ (B∨¬p) → A∨B  (resolvent)
  Resolution refutation: derive ⊥ (empty clause) from Γ∪{¬φ}
  Completeness: Γ⊨φ iff resolution derives ⊥ from Γ∪{¬φ}
  DPLL algorithm: efficient SAT solving with backtracking
```

---

## First-Order Logic
```
Signature: constants c, function symbols f, predicate symbols P
  Arity: number of arguments

Terms:
  Variables x,y,z,... are terms
  If f is n-ary and t₁,...,tₙ are terms: f(t₁,...,tₙ) is a term
  Constants: 0-ary function symbols

Atomic formulas: P(t₁,...,tₙ) for n-ary P, terms tᵢ
  Equality: t₁ = t₂

Formulas:
  Atomic formulas
  ¬φ, φ∧ψ, φ∨ψ, φ→ψ, φ↔ψ
  ∀xφ, ∃xφ  (x bound in φ)

Free and bound variables:
  x free in φ: x occurs unbound
  Sentence: formula with no free variables
  Substitution: φ[t/x] = φ with t replacing free x (avoid capture)

Interpretations/Structures:
  M = (D, Iₜ, Iₚ)
  D: nonempty domain (universe)
  Iₜ: interprets terms (constants → elements, functions → functions on D)
  Iₚ: interprets predicates (n-ary predicates → subsets of Dⁿ)

Satisfaction M⊨φ[s] (s = variable assignment):
  M⊨P(t₁,...,tₙ)[s]: (⟦t₁⟧ₛ,...,⟦tₙ⟧ₛ) ∈ Iₚ(P)
  M⊨¬φ[s]: M⊭φ[s]
  M⊨∀xφ[s]: for all d∈D, M⊨φ[s(x↦d)]
  M⊨∃xφ[s]: there exists d∈D, M⊨φ[s(x↦d)]

Logical consequence: Γ⊨φ  (φ true in all models of Γ)
Theory: set of sentences closed under logical consequence
```

---

## Proof Theory

### Natural Deduction
```
Introduction/elimination rules for each connective:

∧-intro: from φ,ψ derive φ∧ψ
∧-elim: from φ∧ψ derive φ (or ψ)

∨-intro: from φ derive φ∨ψ (or ψ∨φ)
∨-elim: from φ∨ψ, (φ→χ), (ψ→χ) derive χ

→-intro: from [φ]...ψ derive φ→ψ  (discharge assumption φ)
→-elim: from φ→ψ, φ derive ψ  (modus ponens)

¬-intro: from [φ]...⊥ derive ¬φ  (reductio)
¬-elim: from ¬φ,φ derive ⊥
¬¬-elim: from ¬¬φ derive φ  (classical logic)

∀-intro: from φ derive ∀xφ  (x not free in assumptions)
∀-elim: from ∀xφ derive φ[t/x]

∃-intro: from φ[t/x] derive ∃xφ
∃-elim: from ∃xφ, (from [φ]...ψ) derive ψ  (x not in ψ or assumptions)

Sequent calculus (Gentzen):
  Γ⊢Δ: from assumptions Γ can derive some formula in Δ
  Cut rule: Γ⊢Δ,φ  and  φ,Γ⊢Δ  → Γ⊢Δ
  Cut elimination: every proof can be transformed to cut-free proof
```

### Hilbert System
```
Axioms (for classical propositional logic):
  (K): φ→(ψ→φ)
  (S): (φ→(ψ→χ))→((φ→ψ)→(φ→χ))
  (DNE): ¬¬φ→φ

Modus ponens: from φ→ψ and φ derive ψ

Deduction theorem: Γ,φ⊢ψ iff Γ⊢φ→ψ

Soundness: Γ⊢φ → Γ⊨φ  (provable things are true)
Completeness: Γ⊨φ → Γ⊢φ  (true things are provable)
  Propositional: decidable (truth tables)
  First-order: Godel completeness theorem (1929)
```

---

## Model Theory
```
Godel Completeness Theorem:
  Γ⊨φ iff Γ⊢φ  (for first-order logic)
  If Γ is consistent → Γ has a model
  Proof: Henkin construction — build model from maximal consistent set

Lowenheim-Skolem theorems:
  Downward: if T has model of size κ ≥ |T|, has countable model
  Upward: if T has infinite model, has models of every infinite cardinality
  Consequence: no first-order characterization of ℝ (has countable models)
    Nonstandard models of arithmetic, analysis!

Compactness theorem:
  Γ has model iff every finite Γ₀⊆Γ has model
  Proof: from completeness (finite derivations use finitely many hypotheses)
  Applications:
    Nonstandard analysis (add axioms ∃x>n for each n)
    Graph coloring (infinite graphs from finite)
    Transfer principles

Elementary equivalence:
  M≡N: M,N satisfy same sentences  (can't distinguish by FOL)
  ℝ and nonstandard reals are elementarily equivalent!
  Isomorphic → elementary equivalent (converse fails in general)

Types and omitting types:
  Type of tuple ā in M: {φ(x̄): M⊨φ(ā)}
  Omitting types theorem: can build models omitting non-principal types
  Saturated models: realize all types

Quantifier elimination:
  Theory T admits QE: every formula ≡ quantifier-free formula (mod T)
  Examples: dense linear orders (DLO), real closed fields (Tarski)
  Decidability: if T has QE and decidable QF theory → T decidable

Model theoretic algebra:
  Algebraically closed fields: complete, QE in ring language
  Real closed fields: complete, QE (Tarski's theorem)
  Dense linear orders: complete, QE

Stability theory:
  κ-stable: T has ≤κ types over every set of size κ
  ω-stable, superstable, stable, NIP, simple theories (classification)
  Morley categoricity: T categorical in some uncountable κ → categorical in all
```

---

## Set Theory
```
Zermelo-Fraenkel Axioms (ZFC):
  1. Extensionality: sets equal iff same elements
  2. Empty set: ∃∅: ∀x(x∉∅)
  3. Pairing: ∃z: z={x,y} for any x,y
  4. Union: ∃z: z=∪A for any set A
  5. Power set: ∃z: z=P(A) for any set A
  6. Separation: {x∈A: φ(x)} is a set
  7. Replacement: image of set under function is a set
  8. Infinity: ∃ω: ∅∈ω and x∈ω→x∪{x}∈ω
  9. Foundation: every nonempty set has ∈-minimal element
  C. Choice: every family of nonempty sets has choice function

Ordinals:
  Defined as hereditary transitive sets well-ordered by ∈
  0=∅, 1={∅}, 2={∅,{∅}}, 3=2∪{2}, ...
  ω = {0,1,2,...} = natural numbers
  ω+1 = ω∪{ω}, ω·2, ω², ωω, ε₀,...
  Every well-ordered set isomorphic to unique ordinal (Zermelo)

Cardinals:
  |A| = |B|: bijection exists
  Alephs: ℵ₀ = |ℕ|, ℵ₁ = next, ℵ₂, ... (infinite cardinals)
  Continuum: |ℝ| = 2^ℵ₀ = c
  Continuum Hypothesis: 2^ℵ₀ = ℵ₁ (independent of ZFC!)
  König's theorem: cf(κ) > cf(λ) → κ^λ > κ

Axiom of Choice equivalents:
  Zorn's lemma: every chain-complete poset has maximal element
  Well-ordering: every set can be well-ordered
  Tychonoff: product of compact spaces is compact
  All vector spaces have basis
  Every surjection has right inverse

Forcing:
  Cohen's technique to build new set-theoretic universes
  Proves independence of CH from ZFC (1963)
  Add generic sets via partial orders (forcing posets)
  P-names, generic filters, truth in forcing extensions
```

---

## Computability Theory
```python
def computability_theory():
    return {
        'Turing machines': {
            'definition':   'Tape, head, finite control, transition function',
            'DTM':          'Deterministic: one transition per (state,symbol)',
            'NTM':          'Nondeterministic: multiple transitions possible',
            'UTM':          'Universal TM: simulates any TM on any input',
            'Church-Turing': 'Any effective computation = TM computation'
        },
        'Decidability': {
            'decidable':    'TM that halts and accepts/rejects for all inputs',
            'recognizable': 'TM that accepts all instances, may loop on others',
            'co-recognizable':'complement is recognizable',
            'decidable iff': 'Recognizable AND co-recognizable'
        },
        'Halting problem': {
            'statement':    'Does TM M halt on input w? — UNDECIDABLE',
            'proof':        'Diagonalization: assume decider D, construct M using D → contradiction',
            'implication':  'Many problems reduce to halting problem'
        },
        'Rice\'s theorem': {
            'statement':    'Any nontrivial semantic property of TM is undecidable',
            'nontrivial':   'Some TMs have it, some don\'t',
            'semantic':     'Depends on language recognized, not description',
            'examples':     '"Does M accept empty string?" "Does M halt on all inputs?"'
        },
        'Reducibility': {
            'many-one':     'A ≤ₘ B: ∃ computable f: w∈A ↔ f(w)∈B',
            'Turing':       'A ≤_T B: TM with B oracle decides A',
            'complete':     'C-complete: hardest in C under reduction',
            'hierarchy':    'Arithmetical: Σ⁰₁ (recognizable), Π⁰₁, Δ⁰₁ (decidable), Σ⁰₂,...'
        },
        'Complexity classes': {
            'P':            'Polynomial time decidable',
            'NP':           'Nondeterministic polynomial time (or verifiable in poly time)',
            'NP-complete':  'NP-hard and in NP',
            'P vs NP':      'Greatest open problem in CS — likely P ≠ NP',
            'PSPACE':       'Polynomial space',
            'Hierarchy':    'P ⊆ NP ⊆ PSPACE ⊆ EXP (all believed strict)'
        }
    }
```

---

## Godel's Incompleteness Theorems
```
Setup:
  Formal system T: recursive set of axioms, rules of inference
  Sufficiently powerful: can express basic arithmetic (PA or stronger)
  Consistent: cannot prove both φ and ¬φ

First Incompleteness Theorem:
  If T is consistent and sufficiently powerful:
  ∃ sentence φ: T⊬φ and T⊬¬φ  (T is incomplete)
  φ is "true but unprovable" (assuming T is sound)

Proof sketch (Godel 1931):
  Arithmetization: encode formulas as numbers (Godel numbering)
  Representability: provability is expressible in arithmetic
  Self-reference: Diagonal lemma: ∃φ ↔ ¬Provₜ(⌈φ⌉)
    "This statement is not provable in T"
  If T proves φ → T proves Provₜ(φ) → T proves ¬φ → inconsistent
  If T proves ¬φ → T proves Provₜ(φ) is false → contradicts Provₜ being correct
  Therefore T proves neither → incomplete ✓

Second Incompleteness Theorem:
  If T is consistent and sufficiently powerful:
  T⊬Con(T)  (T cannot prove its own consistency)
  Con(T) = "T is consistent" = ¬Provₜ(⌈⊥⌉)
  Consequence: cannot prove safety of formal systems within themselves

Scope and limitations:
  Applies to: PA, ZFC, any sufficiently strong consistent theory
  Doesn't apply to: Presburger arithmetic (addition only), real arithmetic
  Not mystical: about formal provability, not mathematical truth
  Godel sentence φ IS true (in ℕ) if T is sound — just not formally provable in T

Implications:
  Hilbert's program: impossible — cannot finitely axiomatize mathematics with proof of consistency
  Truth ≠ provability in formal systems
  Some mathematical questions genuinely independent of ZFC (CH, large cardinals)
```

---

## Type Theory
```
Simple Type Theory:
  Types: base types (Bool, Nat), function types (A→B), product types (A×B)
  Terms: variables x:A, λx:A.t:B (function), t u (application)
  Typing rules: Γ,x:A ⊢ t:B implies Γ ⊢ λx:A.t : A→B

Curry-Howard Correspondence:
  Types ↔ Propositions
  Terms ↔ Proofs
  A→B ↔ "A implies B"
  A×B ↔ "A and B"
  A+B ↔ "A or B"
  ⊥ ↔ False (empty type)
  ∀x:A.B(x) ↔ "For all x:A, B(x)" (dependent product)
  ∃x:A.B(x) ↔ "There exists x:A, B(x)" (dependent sum)

Dependent type theory:
  Types can depend on terms
  Π-types: Πx:A.B(x) — dependent function type
  Σ-types: Σx:A.B(x) — dependent pair type
  Identity types: Id_A(a,b) — proof that a=b:A

Martin-Löf Type Theory (MLTT):
  Foundation for constructive mathematics and type theory
  Universes: type of types
  W-types: well-founded trees

Homotopy Type Theory (HoTT):
  Identity types as paths in topological space
  Univalence axiom: equivalent types are equal
  Higher inductive types
  Foundations without classical logic

Proof assistants:
  Coq: CIC (Calculus of Inductive Constructions)
  Lean 4: dependent type theory, Mathlib (huge math library)
  Agda: Martin-Löf type theory, homotopy type theory
  Isabelle: HOL (Higher Order Logic)
  Applications: verified software, formalized mathematics
```

---

## Formal Verification
```python
def formal_verification():
    return {
        'Model checking': {
            'idea':         'Automatically verify finite-state system against specification',
            'CTL':          'Computation Tree Logic: branching time temporal logic',
            'LTL':          'Linear Temporal Logic: linear time',
            'operators':    'EX (exists next), AX (all next), EF (exists future), AG (all globally)',
            'algorithm':    'BDD-based or SAT-based symbolic model checking',
            'tools':        'SPIN (LTL), NuSMV (CTL/LTL), UPPAAL (timed automata)'
        },
        'SAT solving': {
            'problem':      'Given CNF formula, find satisfying assignment or prove UNSAT',
            'DPLL':         'Unit propagation + backtracking',
            'CDCL':         'Conflict-driven clause learning (modern SAT solvers)',
            'tools':        'MiniSAT, CaDiCaL, Glucose',
            'applications': 'Hardware verification, planning, combinatorics'
        },
        'Theorem proving': {
            'interactive':  'Human-guided proof (Coq, Lean, Isabelle)',
            'automatic':    'ATP: try to find proof automatically (E, Vampire)',
            'SMT':          'SAT + theories (Z3, CVC5): arithmetic, arrays, strings',
            'achievements': [
                'Four Color Theorem (Gonthier, Coq, 2005)',
                'Kepler Conjecture (Hales, Isabelle+HOL, 2014)',
                'Feit-Thompson (Gonthier et al., Coq, 2012)',
                'Mathlib: >100k theorems in Lean 4'
            ]
        },
        'Program verification': {
            'Hoare logic':  '{P} S {Q}: if P holds before S, Q holds after',
            'WP calculus':  'Weakest precondition: compute P from Q and S',
            'separation':   'Separation logic: reasoning about heap/pointers',
            'tools':        'Dafny, Why3, VeriFast, Frama-C'
        }
    }
```

---

## Key Theorems Summary
```
Soundness: provability → semantic validity (⊢ implies ⊨)
Completeness (Godel 1929): semantic validity → provability (⊨ implies ⊢) for FOL
Compactness: Γ⊨φ iff finite Γ₀⊨φ
Lowenheim-Skolem: FOL cannot characterize uncountable structures uniquely
Godel First Incompleteness: consistent sufficiently strong T has undecidable sentences
Godel Second Incompleteness: T cannot prove Con(T)
Church's thesis: effective computation = Turing computability
Undecidability of halting: ∃ problems TMs cannot decide
Rice's theorem: all nontrivial semantic properties undecidable
P vs NP: central open problem in complexity theory
Cohen independence: CH independent of ZFC
Curry-Howard: proofs = programs, propositions = types
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Incompleteness means math is broken | It limits formal provability, not mathematical truth |
| FOL can characterize ℝ uniquely | By Lowenheim-Skolem: FOL theories have models of all infinite cardinalities |
| Undecidable = not solvable in practice | Undecidable = no algorithm for ALL instances; specific instances may be solved |
| Godel's sentence is unprovable AND false | It's TRUE (in ℕ) but unprovable in T — truth ≠ formal provability |
| ZFC is inconsistent | No known inconsistency; we believe it's consistent but cannot prove it in ZFC |
| Type theory is just programming types | Dependent type theory is a foundation for mathematics, much richer |

---

## Related Skills

- **discrete-mathematics-expert**: Propositional logic applications
- **abstract-algebra-expert**: Algebraic logic, Boolean algebras
- **computability-complexity**: Deeper complexity theory
- **topology-expert**: Topos theory connects topology and logic
- **set-theory**: Advanced set-theoretic methods
- **programming-languages**: Type systems and formal semantics

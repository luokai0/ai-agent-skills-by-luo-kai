---
name: abstract-algebra-expert
description: Expert-level abstract algebra knowledge. Use when working with groups, rings, fields, modules, Galois theory, representation theory, or algebraic structures. Also use when the user mentions 'group', 'ring', 'field', 'homomorphism', 'isomorphism', 'normal subgroup', 'quotient group', 'Sylow theorem', 'Galois theory', 'polynomial ring', 'ideal', 'module', 'vector space', or 'representation theory'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Abstract Algebra Expert

You are a world-class mathematician with deep expertise in abstract algebra covering group theory, ring theory, field theory, Galois theory, module theory, and representation theory.

## Before Starting

1. **Topic** — Groups, rings, fields, Galois theory, or modules?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Prove theorem, solve problem, or understand structure?
4. **Context** — Pure algebra, number theory, geometry, or physics?
5. **Background** — Assumed knowledge of sets, functions, basic proofs?

---

## Core Expertise Areas

- **Group Theory**: subgroups, cosets, quotient groups, homomorphisms, Sylow
- **Ring Theory**: ideals, quotient rings, PIDs, UFDs, polynomial rings
- **Field Theory**: extensions, algebraic closure, finite fields
- **Galois Theory**: Galois group, fundamental theorem, solvability
- **Module Theory**: submodules, free modules, exact sequences
- **Representation Theory**: group representations, characters, Maschke's theorem
- **Category Theory**: functors, natural transformations, universal properties
- **Applications**: coding theory, crystallography, cryptography

---

## Group Theory

### Basic Definitions
```
Group (G, ·):
  Closure:     a,b ∈ G → a·b ∈ G
  Associativity: (a·b)·c = a·(b·c)
  Identity:    ∃e: a·e = e·a = a
  Inverses:    ∀a ∃a⁻¹: a·a⁻¹ = a⁻¹·a = e

Abelian (commutative): a·b = b·a for all a,b ∈ G

Order:
  |G| = order of group (number of elements)
  |a| = order of element a = smallest n>0: aⁿ = e

Examples:
  (ℤ,+): integers under addition (infinite, abelian)
  (ℤₙ,+): integers mod n (finite, abelian, cyclic)
  (ℤₙ*,·): units mod n (finite, abelian)
  Sₙ: symmetric group on n elements (non-abelian for n≥3)
  Aₙ: alternating group (even permutations), |Aₙ| = n!/2
  Dₙ: dihedral group (symmetries of regular n-gon), |Dₙ| = 2n
  GL(n,F): invertible n×n matrices over field F
  SL(n,F): matrices with determinant 1
  Quaternion group Q₈: {±1,±i,±j,±k}
```

### Subgroups & Cosets
```
Subgroup H ≤ G:
  H nonempty, closed under operation and inverses
  One-step test: a,b ∈ H → ab⁻¹ ∈ H
  Two-step test: closed under · and ⁻¹

Lagrange's theorem:
  H ≤ G (G finite): |H| divides |G|
  |G| = |H| · [G:H]  ([G:H] = index = number of cosets)
  Corollary: |a| divides |G|, so aˡᴳˡ = e

Left cosets: aH = {ah: h∈H}
  Cosets partition G (equivalence classes)
  All cosets have same size |H|

Normal subgroup H ⊴ G:
  gHg⁻¹ = H for all g ∈ G
  Equivalently: left and right cosets coincide gH = Hg
  Examples: any subgroup of abelian group, center Z(G)
  Kernel of homomorphism is always normal

Quotient group G/H (H normal):
  Elements: left cosets {aH: a∈G}
  Operation: (aH)(bH) = (ab)H
  |G/H| = |G|/|H| (G finite)
```

### Homomorphisms & Isomorphisms
```
Homomorphism φ: G → H:
  φ(ab) = φ(a)φ(b) for all a,b ∈ G
  Properties: φ(e_G) = e_H, φ(a⁻¹) = φ(a)⁻¹

Kernel: ker(φ) = {g∈G: φ(g) = e_H} ⊴ G  (always normal!)
Image: im(φ) = {φ(g): g∈G} ≤ H

Isomorphism: bijective homomorphism (G ≅ H)
Automorphism: isomorphism from G to itself

First Isomorphism Theorem:
  G/ker(φ) ≅ im(φ)
  Key tool for quotient groups!

Second Isomorphism Theorem:
  H ≤ G, N ⊴ G: HN/N ≅ H/(H∩N)

Third Isomorphism Theorem:
  N ⊴ M ⊴ G: (G/N)/(M/N) ≅ G/M

Correspondence theorem:
  φ: G→G/N: subgroups of G/N ↔ subgroups of G containing N
```

### Cyclic Groups & Permutations
```
Cyclic group ⟨a⟩ = {aⁿ: n∈ℤ}
  Every subgroup of cyclic group is cyclic
  ℤₙ cyclic of order n, ℤ cyclic infinite
  ⟨a⟩ ≅ ℤₙ if |a|=n, ≅ ℤ if |a|=∞

Permutation groups:
  σ ∈ Sₙ: bijection {1,...,n}→{1,...,n}
  Cycle notation: (1 2 3) means 1→2→3→1
  Transposition: 2-cycle (i j)
  Every permutation = product of disjoint cycles (unique up to order)
  |σ| = lcm of cycle lengths
  Sign: sgn(σ) = (-1)^(inversions) = (-1)^(n-c) (c = number of cycles including fixed points)
  Even/odd permutation: sgn = +1/-1

Alternating group Aₙ:
  Even permutations, |Aₙ| = n!/2
  A₅ is simple (no normal subgroups) — smallest non-abelian simple group
  This is why degree 5 polynomial not solvable by radicals!
```

### Sylow Theory
```
Sylow p-subgroup: subgroup of order pᵏ where pᵏ | |G| but p^(k+1) ∤ |G|

Sylow's Theorems (p prime, pᵏ | |G|):
  1st: Sylow p-subgroup exists
  2nd: All Sylow p-subgroups are conjugate (isomorphic)
  3rd: nₚ = number of Sylow p-subgroups
       nₚ ≡ 1 (mod p)
       nₚ | |G|/pᵏ

Applications:
  Classify groups of small order
  Prove group is not simple (show nₚ = 1 → Sylow subgroup normal)
  Example: |G|=15=3·5: n₃|5 and n₃≡1(mod 3) → n₃=1; n₅|3 and n₅≡1(mod 5) → n₅=1
    Both Sylow subgroups normal → G ≅ ℤ₁₅ (cyclic)
```

---

## Ring Theory
```
Ring (R, +, ·):
  (R, +): abelian group
  (R, ·): associative, distributive over +
  Ring with unity: has multiplicative identity 1
  Commutative ring: ab = ba

Examples:
  ℤ, ℚ, ℝ, ℂ: number rings
  ℤₙ: integers mod n
  M_n(R): n×n matrices over R (non-commutative)
  R[x]: polynomial ring over R
  R[x,y]: polynomials in two variables
  ℤ[i]: Gaussian integers {a+bi: a,b∈ℤ}

Types of elements:
  Unit: has multiplicative inverse (a·b=1)
  Zero divisor: a≠0, ∃b≠0: ab=0
  Nilpotent: aⁿ=0 for some n
  Idempotent: a²=a
  Integral domain: commutative, unity, no zero divisors
  Field: commutative, unity, every nonzero element is unit

Ideals:
  Left ideal: RI ⊆ I (rI ⊆ I for all r)
  Right ideal: IR ⊆ I
  Two-sided ideal: left and right
  Kernel of ring homomorphism is always an ideal

Principal ideal: (a) = {ra: r∈R} = aR
  PID (principal ideal domain): integral domain, every ideal principal
  Examples: ℤ, F[x] (polynomial ring over field), ℤ[i]

Prime ideal P: ab∈P → a∈P or b∈P
  In commutative ring: prime ideal ↔ R/P integral domain

Maximal ideal M: no ideal strictly between M and R
  In commutative ring: maximal ↔ R/M is a field

First isomorphism theorem for rings:
  φ: R→S ring homomorphism: R/ker(φ) ≅ im(φ)

Chinese Remainder Theorem for rings:
  I,J coprime ideals (I+J=R): R/(I∩J) ≅ R/I × R/J

UFD (Unique Factorization Domain):
  Integral domain, every element = unit × product of irreducibles (unique)
  PID → UFD (but not conversely)
  Examples: ℤ[x] is UFD but not PID (since (2,x) not principal)
```

---

## Field Theory
```
Field: commutative ring where every nonzero element is a unit
  Examples: ℚ, ℝ, ℂ, ℤₚ (p prime), ℚ(√2), 𝔽₂ₙ

Field extensions:
  F ⊆ K (K contains F as subfield)
  [K:F] = dimₐ(K) = degree of extension
  Tower law: [K:F] = [K:E][E:F]  for F⊆E⊆K

Algebraic elements:
  α algebraic over F: f(α)=0 for some f∈F[x]
  Minimal polynomial: monic irreducible poly of smallest degree
  [F(α):F] = deg(min poly)
  Transcendental: not algebraic (π and e are transcendental over ℚ)

Algebraic extensions:
  F(α): smallest field containing F and α
  If α algebraic, F(α) ≅ F[x]/(min poly of α)

Splitting field:
  Smallest extension where polynomial f splits into linear factors
  Exists and unique up to isomorphism

Algebraic closure:
  F̄: field where every polynomial has a root
  ℂ = algebraic closure of ℝ (Fundamental Theorem of Algebra)

Finite fields:
  Order = pⁿ (p prime, n≥1)
  All fields of order pⁿ are isomorphic → 𝔽_{pⁿ}
  Multiplicative group 𝔽_{pⁿ}* is cyclic
  Subfields: 𝔽_{pᵐ} ⊆ 𝔽_{pⁿ} ↔ m|n
  Frobenius automorphism: x↦xᵖ generates Gal(𝔽_{pⁿ}/𝔽_p) ≅ ℤₙ
```

---

## Galois Theory
```
Galois group:
  Gal(K/F) = Aut_F(K) = field automorphisms fixing F
  |Gal(K/F)| = [K:F] for Galois extensions

Galois extension K/F:
  Normal (splits over F) AND separable (distinct roots)
  Equivalent: |Gal(K/F)| = [K:F]
  Examples: ℚ(√2,√3)/ℚ, splitting fields of separable polynomials
  Non-example: ℚ(∛2)/ℚ (not normal)

Fundamental Theorem of Galois Theory:
  For Galois extension K/F with G = Gal(K/F):
  Correspondence: {subgroups of G} ↔ {intermediate fields F⊆E⊆K}
  H ↦ K^H = {x∈K: σ(x)=x ∀σ∈H}  (fixed field)
  E ↦ Gal(K/E)  (automorphisms fixing E)
  Reverses inclusion: H₁≤H₂ ↔ K^H₁ ⊇ K^H₂
  [K:E] = |Gal(K/E)|, [E:F] = [G:Gal(K/E)]
  E/F Galois ↔ Gal(K/E) ⊴ G, and Gal(E/F) ≅ G/Gal(K/E)

Solvability by radicals:
  f(x) solvable by radicals ↔ Gal(f) is solvable group
  Group G solvable: G = G₀⊃G₁⊃...⊃Gₖ={e} with Gᵢ/Gᵢ₊₁ abelian
  A₅ is not solvable → general degree 5 polynomial not solvable!
  (Abel-Ruffini theorem)

Classical ruler-compass constructions:
  α constructible ↔ [ℚ(α):ℚ] = 2ⁿ
  Squaring circle: impossible (π transcendental)
  Doubling cube: impossible (∛2: degree 3, not power of 2)
  Trisecting angle: usually impossible
  Regular n-gon constructible ↔ n = 2ᵏ·p₁·p₂...pₘ (pᵢ Fermat primes)
```

---

## Module Theory
```
Module M over ring R:
  (M, +): abelian group
  R acts on M: r·m ∈ M with distributivity and associativity
  Vector spaces: modules over a field

Submodule: subgroup closed under R-action
Quotient module: M/N for submodule N
Module homomorphism (R-linear map): f(rm) = rf(m)

Free module: M ≅ R^n (has basis)
  Finitely generated: spanned by finite set
  Free → finitely generated (converse fails over general rings)

Classification of modules over PIDs:
  Finitely generated module M over PID R:
  M ≅ R^r ⊕ R/(d₁) ⊕ R/(d₂) ⊕ ... ⊕ R/(dₖ)
  d₁|d₂|...|dₖ (invariant factors)
  Special case (R=ℤ): finitely generated abelian groups!

Exact sequences:
  0 → A →ᶠ B →ᵍ C → 0  (short exact sequence)
  Exact: im(f) = ker(g)
  Short exact: f injective, g surjective, im(f) = ker(g)
  Split: sequence is "isomorphic" to 0 → A → A⊕C → C → 0

Tensor product:
  M⊗ₐN: universal bilinear map
  R⊗_R M ≅ M
  Hom(M,N): module of R-linear maps

Projective/injective modules:
  Projective: direct summand of free module
  Injective: Hom(-,M) exact
  Flat: M⊗- exact
```

---

## Representation Theory
```
Representation of group G:
  Homomorphism ρ: G → GL(V) for vector space V over field k
  Degree = dim(V)

Subrepresentation: V-subspace invariant under all ρ(g)
Irreducible (simple): no proper nonzero subrepresentation

Maschke's theorem:
  G finite, char(k) ∤ |G|: every representation is completely reducible
  V = V₁ ⊕ V₂ ⊕ ... ⊕ Vₖ (direct sum of irreducibles)

Character:
  χᵥ(g) = Tr(ρ(g)) (trace of representation matrix)
  Class function: χ(hgh⁻¹) = χ(g) (constant on conjugacy classes)
  Characters of irreps: orthogonal basis for class functions
  ⟨χ,ψ⟩ = (1/|G|) Σ χ(g)ψ(g)⁻ = δ_{irreps}

Number of irreps = number of conjugacy classes
Sum of squares of dimensions = |G|: Σ (dim Vᵢ)² = |G|

Character table:
  Rows: irreducible representations
  Columns: conjugacy classes
  Entry: character value χ(g)

Regular representation:
  G acts on k[G] by left multiplication
  Decomposes as direct sum of each irrep with multiplicity = degree
```

---

## Category Theory Basics
```
Category C:
  Objects: collection ob(C)
  Morphisms: for each pair A,B: hom(A,B) (arrows A→B)
  Composition: f:A→B, g:B→C → g∘f:A→C (associative)
  Identities: 1_A: A→A for each A

Examples:
  Set: sets and functions
  Grp: groups and homomorphisms
  Ring: rings and ring homomorphisms
  Top: topological spaces and continuous maps
  Vect_k: vector spaces over k and linear maps

Functor F: C→D:
  Assigns object F(A)∈D to each A∈C
  Assigns morphism F(f) to each morphism f
  Preserves composition and identities
  Covariant: F(g∘f) = F(g)∘F(f)
  Contravariant: reverses arrows

Natural transformation η: F⟹G:
  For each A: η_A: F(A)→G(A) (natural in A)
  Commutes with morphisms

Universal properties:
  Products: A×B with projections π₁,π₂
  Coproducts: A+B with injections i₁,i₂
  Free objects: free group on set S
  Tensor products, kernels, cokernels

Adjoint functors:
  F⊣G: hom(F(A),B) ≅ hom(A,G(B)) (natural bijection)
  Free-forgetful adjunction: free group on S ⊣ underlying set
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Normal subgroup = any subgroup | Normal requires gHg⁻¹ = H; not all subgroups are normal |
| Quotient always exists | G/H only group when H is normal |
| All groups with same order isomorphic | ℤ₄ ≇ ℤ₂×ℤ₂ (same order, different structure) |
| PID implies UFD reversed | UFD does not imply PID (ℤ[x] is UFD but not PID) |
| Galois group order = field degree | Only for Galois extensions; need normal + separable |
| Splitting field degree = n! | Splitting field of degree n poly has [K:F] dividing n!, often less |

---

## Related Skills

- **number-theory-expert**: Algebraic number theory
- **topology-expert**: Algebraic topology uses groups extensively
- **linear-algebra-expert**: Modules generalize vector spaces
- **calculus-expert**: Lie groups connect algebra and analysis
- **cryptography-expert**: Groups and finite fields in crypto
- **physics-quantum-mechanics**: Group representations in physics

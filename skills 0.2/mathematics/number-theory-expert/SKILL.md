---
name: number-theory-expert
description: Expert-level number theory knowledge. Use when working with divisibility, prime numbers, modular arithmetic, congruences, Diophantine equations, cryptography, quadratic residues, or analytic number theory. Also use when the user mentions 'prime', 'divisibility', 'modular arithmetic', 'congruence', 'GCD', 'Euler totient', 'Fermat little theorem', 'Chinese remainder theorem', 'quadratic residue', 'Diophantine equation', 'RSA', or 'prime factorization'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Number Theory Expert

You are a world-class mathematician with deep expertise in number theory covering divisibility, prime numbers, modular arithmetic, Diophantine equations, quadratic residues, analytic number theory, and applications to cryptography.

## Before Starting

1. **Topic** — Divisibility, primes, modular arithmetic, Diophantine equations, or analytic?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Solve problem, prove theorem, or understand concept?
4. **Context** — Pure mathematics or cryptography/applications?
5. **Tools** — Elementary, algebraic, or analytic methods?

---

## Core Expertise Areas

- **Divisibility**: GCD, LCM, Euclidean algorithm, Bezout's identity
- **Prime Numbers**: fundamental theorem, distribution, primality testing
- **Modular Arithmetic**: congruences, residue classes, Chinese Remainder Theorem
- **Arithmetic Functions**: Euler φ, Mobius μ, divisor functions
- **Quadratic Residues**: Legendre symbol, quadratic reciprocity
- **Diophantine Equations**: linear, Pythagorean, Pell, Fermat
- **Analytic Number Theory**: prime number theorem, Riemann zeta function
- **Cryptography**: RSA, Diffie-Hellman, elliptic curves

---

## Divisibility
```
a | b: a divides b means b = ka for some integer k
Properties:
  a|b and b|c → a|c  (transitivity)
  a|b and a|c → a|(mb+nc) for all integers m,n
  a|b and b|a → a = ±b
  a|b → a|bc for all c

Division algorithm:
  For a,b integers, b > 0: unique q,r with a = bq + r, 0 ≤ r < b
  q = quotient, r = remainder

GCD (Greatest Common Divisor):
  gcd(a,b): largest positive integer dividing both a and b
  gcd(a,0) = a, gcd(0,0) = 0
  gcd(a,b) = gcd(b, a mod b)  (Euclidean algorithm)

Euclidean algorithm:
  gcd(48,18): 48=2·18+12, 18=1·12+6, 12=2·6+0 → gcd=6
  Time: O(log(min(a,b)))

Bezout's identity:
  gcd(a,b) = d → ∃x,y: ax + by = d
  Extended Euclidean algorithm computes x,y
  a,b coprime ↔ gcd(a,b)=1 ↔ ∃x,y: ax+by=1

LCM (Least Common Multiple):
  lcm(a,b) = ab/gcd(a,b)  (for positive a,b)
  gcd(a,b)·lcm(a,b) = ab

Fundamental Theorem of Arithmetic:
  Every integer n > 1 has unique prime factorization:
  n = p₁^e₁ · p₂^e₂ · ... · pₖ^eₖ  (primes in increasing order)
  Key tool: if p|ab and p prime → p|a or p|b
```

---

## Prime Numbers
```
Primes: integers > 1 with no positive divisors except 1 and themselves
  2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, ...

Infinitude of primes (Euclid):
  Assume finitely many p₁,...,pₙ
  N = p₁p₂...pₙ + 1: not divisible by any pᵢ → N prime or has new prime factor ↑

Sieve of Eratosthenes:
  To find all primes ≤ n:
  Start with {2,...,n}, repeatedly remove multiples of each prime
  O(n log log n) time

Primality testing:
  Trial division: test divisors up to √n  (O(√n))
  Miller-Rabin: probabilistic, polynomial time
  AKS: deterministic polynomial time (Agrawal-Kayal-Saxena 2002)

Bertrand's postulate:
  For n ≥ 1: there exists prime p with n < p ≤ 2n

Dirichlet's theorem:
  If gcd(a,d) = 1: infinitely many primes p ≡ a (mod d)
  Primes equally distributed among coprime residue classes (asymptotically)

Prime gaps and conjectures:
  Twin prime conjecture: infinitely many pairs (p, p+2) both prime (unproven)
  Goldbach conjecture: every even n > 2 is sum of two primes (unproven)
  Riemann hypothesis: zeros of ζ(s) on Re(s) = 1/2 (unproven, Millennium problem)

Mersenne primes:
  Mₚ = 2ᵖ - 1 (prime only if p prime, but not all)
  M₂=3, M₃=7, M₅=31, M₇=127, M₁₃=8191, ...
  Largest known primes are Mersenne primes (GIMPS project)
```

---

## Modular Arithmetic
```
Congruence: a ≡ b (mod n) means n|(a-b)
  Reflexive: a ≡ a
  Symmetric: a ≡ b → b ≡ a
  Transitive: a ≡ b, b ≡ c → a ≡ c

Operations:
  a ≡ b, c ≡ d (mod n) →
    a+c ≡ b+d (mod n)
    ac ≡ bd (mod n)
    aᵏ ≡ bᵏ (mod n)

Cancellation: ac ≡ bc (mod n) → a ≡ b (mod n/gcd(c,n))
Inverse: a·x ≡ 1 (mod n) exists ↔ gcd(a,n) = 1

Solving ax ≡ b (mod n):
  Solution exists ↔ gcd(a,n) | b
  If gcd(a,n)=1: unique solution x ≡ a⁻¹b (mod n)
  Find a⁻¹ using extended Euclidean algorithm

Chinese Remainder Theorem (CRT):
  n₁,n₂,...,nₖ pairwise coprime
  System: x ≡ a₁ (mod n₁), ..., x ≡ aₖ (mod nₖ)
  Unique solution mod N = n₁n₂...nₖ
  Construction: Nᵢ = N/nᵢ, yᵢ = Nᵢ⁻¹ (mod nᵢ)
  x = Σ aᵢNᵢyᵢ (mod N)
  Example: x≡2(mod 3), x≡3(mod 5), x≡2(mod 7) → x≡23(mod 105)

Fermat's Little Theorem:
  p prime, p∤a: aᵖ⁻¹ ≡ 1 (mod p)
  Equivalent: aᵖ ≡ a (mod p) for all a
  Use: compute large powers mod p quickly

Euler's Theorem:
  gcd(a,n) = 1: a^φ(n) ≡ 1 (mod n)  (generalizes FLT)
  φ(n) = Euler's totient function

Wilson's Theorem:
  p prime ↔ (p-1)! ≡ -1 (mod p)
```

---

## Arithmetic Functions
```python
def arithmetic_functions():
    return {
        'Euler totient φ(n)': {
            'definition':   'Number of integers 1≤k≤n with gcd(k,n)=1',
            'formula':      'φ(n) = n·Π(1-1/p) over prime p|n',
            'examples':     'φ(1)=1, φ(p)=p-1, φ(p²)=p²-p=p(p-1)',
            'multiplicative':'φ(mn) = φ(m)φ(n) if gcd(m,n)=1',
            'sum':          'Σ_{d|n} φ(d) = n'
        },
        'Mobius function μ(n)': {
            'definition': {
                1:          'μ(1) = 1',
                'squarefree':'μ(n) = (-1)^k if n = p₁...pₖ (distinct primes)',
                'else':     'μ(n) = 0 if n has squared prime factor'
            },
            'Mobius inversion':'g(n) = Σ_{d|n} f(d) ↔ f(n) = Σ_{d|n} μ(n/d)g(d)',
            'key identity': 'Σ_{d|n} μ(d) = [n=1] (1 if n=1, else 0)'
        },
        'Divisor functions': {
            'σ₀(n) = d(n)':  'Number of divisors',
            'σ₁(n) = σ(n)':  'Sum of divisors',
            'σₖ(n)':         'Sum of kth powers of divisors',
            'formula':        'σₖ(pᵉ) = (p^(k(e+1))-1)/(pᵏ-1)',
            'perfect':        'n perfect: σ(n) = 2n (6, 28, 496, ...)'
        },
        'Multiplicative functions': {
            'definition':   'f(mn) = f(m)f(n) if gcd(m,n)=1',
            'examples':     'φ, μ, σₖ, d are multiplicative',
            'Dirichlet series':'F(s) = Σ f(n)/nˢ, product formula for multiplicative f'
        }
    }
```

---

## Quadratic Residues
```
Quadratic residue mod p (p odd prime):
  a is QR mod p if x² ≡ a (mod p) has solution
  a is QNR (quadratic non-residue) if not
  p-1)/2 residues, (p-1)/2 non-residues among {1,...,p-1}

Legendre symbol:
  (a/p) = 0 if p|a
         = 1 if a is QR mod p
         = -1 if a is QNR mod p
  Euler's criterion: (a/p) ≡ a^((p-1)/2) (mod p)

Properties:
  (ab/p) = (a/p)(b/p)  (completely multiplicative)
  (a/p) = (b/p) if a ≡ b (mod p)
  (-1/p) = (-1)^((p-1)/2) = 1 if p≡1(mod 4), -1 if p≡3(mod 4)
  (2/p) = (-1)^((p²-1)/8) = 1 if p≡±1(mod 8), -1 if p≡±3(mod 8)

Quadratic Reciprocity (Gauss, 1796):
  p,q distinct odd primes:
  (p/q)(q/p) = (-1)^((p-1)(q-1)/4)
  = 1 if p≡1(mod 4) or q≡1(mod 4)
  = -1 if p≡q≡3(mod 4)

Tonelli-Shanks algorithm:
  Finds x: x² ≡ a (mod p) when (a/p) = 1

Jacobi symbol (a/n):
  Generalization to odd composite n
  Product of Legendre symbols over prime factors
  (a/n) = 1 does NOT imply a is QR mod n
```

---

## Diophantine Equations
```
Linear Diophantine: ax + by = c
  Solution exists ↔ gcd(a,b) | c
  If (x₀,y₀) is one solution: x=x₀+bt/d, y=y₀-at/d (t∈ℤ)

Pythagorean triples: x² + y² = z²
  Primitive triples (gcd=1): x=m²-n², y=2mn, z=m²+n²
  m > n > 0, gcd(m,n)=1, m-n odd
  All: (3,4,5), (5,12,13), (8,15,17), (7,24,25), ...

Pell's equation: x² - Dy² = 1  (D not perfect square)
  Always has infinitely many solutions
  Fundamental solution (x₁,y₁): smallest positive solution
  Recurrence: xₙ + yₙ√D = (x₁+y₁√D)ⁿ
  Found via continued fraction expansion of √D

Sum of squares:
  n = sum of 2 squares ↔ all prime factors p≡3(mod 4) appear even power
  n = sum of 4 squares: always (Lagrange's four-square theorem)
  Fermat two-square theorem: p = a²+b² ↔ p=2 or p≡1(mod 4)

Fermat's Last Theorem:
  xⁿ + yⁿ = zⁿ has no positive integer solutions for n ≥ 3
  Proven by Andrew Wiles, 1995 (using elliptic curves + modular forms)

Catalan's conjecture (Mihailescu 2002):
  xᵃ - yᵇ = 1 with a,b,x,y>1 → only solution: 3² - 2³ = 1
```

---

## Analytic Number Theory
```
Riemann zeta function:
  ζ(s) = Σₙ₌₁^∞ 1/nˢ  for Re(s) > 1
  Euler product: ζ(s) = Π_p 1/(1-p⁻ˢ)  (over all primes)
  Analytic continuation to all s ≠ 1
  Trivial zeros: s = -2,-4,-6,...
  Riemann hypothesis: all non-trivial zeros have Re(s) = 1/2

Prime Number Theorem:
  π(x) ~ x/ln(x)  as x→∞
  π(x) = number of primes ≤ x
  Stronger: π(x) = Li(x) + O(x·exp(-c√ln x))
  Li(x) = ∫₂ˣ dt/ln(t)  (logarithmic integral)
  Proved independently by Hadamard and de la Vallée Poussin, 1896

Dirichlet L-functions:
  L(s,χ) = Σ χ(n)/nˢ  for Dirichlet character χ
  Dirichlet's theorem uses L(1,χ) ≠ 0 for χ ≠ χ₀

Arithmetic progressions:
  π(x;a,d) = #{p≤x: p≡a(mod d)} ~ π(x)/φ(d)  (PNT for progressions)

Bertrand's postulate (proved): for n≥1, prime p with n<p≤2n
```

---

## Cryptography Applications
```python
def number_theory_crypto():
    return {
        'RSA': {
            'key_generation': [
                'Choose large primes p, q',
                'n = pq, φ(n) = (p-1)(q-1)',
                'Choose e: gcd(e,φ(n))=1, typically e=65537',
                'Find d: ed ≡ 1 (mod φ(n)) via extended Euclidean'
            ],
            'encryption':   'c = mᵉ (mod n)',
            'decryption':   'm = cᵈ (mod n)',
            'security':     'Based on hardness of factoring n',
            'theorem':      'm^(ed) ≡ m (mod n) by Euler\'s theorem'
        },
        'Diffie-Hellman': {
            'setup':        'Public: large prime p, generator g',
            'Alice':        'Choose a, send A = gᵃ (mod p)',
            'Bob':          'Choose b, send B = gᵇ (mod p)',
            'shared key':   'K = Bᵃ = Aᵇ = g^(ab) (mod p)',
            'security':     'Based on hardness of discrete log problem'
        },
        'Primality testing (Miller-Rabin)': {
            'input':        'n odd, write n-1 = 2ˢ·d',
            'step':         'Choose random a, compute a^d mod n',
            'check':        'If aᵈ≢1 and a^(2ʲd)≢-1 for all j: n composite',
            'iterations':   'k rounds: P(false composite) ≤ 4⁻ᵏ',
            'deterministic':'For n<3.3·10²⁴, test a=2,3,5,7,11,13,17,19,23,29,31,37'
        },
        'Baby-step Giant-step (discrete log)': {
            'problem':      'Find x: gˣ ≡ h (mod p)',
            'baby_step':    'Compute gʲ for j=0,...,m-1 (m=⌈√p⌉)',
            'giant_step':   'Compute h·(g^(-m))^i for i=0,...,m-1',
            'match':        'When values match: x = im+j',
            'complexity':   'O(√p) time and space'
        },
        'Elliptic Curve Cryptography': {
            'curve':        'y² = x³ + ax + b (mod p)',
            'group':        'Points form abelian group under chord-tangent law',
            'ECDLP':        'Given P, Q=kP, find k (harder than DLP)',
            'key sizes':    '256-bit ECC ≈ 3072-bit RSA security',
            'applications': 'TLS, Bitcoin (secp256k1), signal protocol'
        }
    }
```

---

## Important Theorems Summary
```
Fermat's Little Theorem: aᵖ⁻¹ ≡ 1 (mod p) for p prime, p∤a
Euler's Theorem: a^φ(n) ≡ 1 (mod n) for gcd(a,n)=1
Wilson's Theorem: (p-1)! ≡ -1 (mod p) ↔ p prime
CRT: System of coprime moduli has unique solution mod product
Quadratic Reciprocity: (p/q)(q/p) = (-1)^((p-1)(q-1)/4)
Four Square Theorem: every positive integer is sum of four squares
FLT: xⁿ+yⁿ=zⁿ no positive integer solutions for n≥3 (Wiles 1995)
PNT: π(x) ~ x/ln(x)
Dirichlet: infinitely many primes in arithmetic progression gcd(a,d)=1
Euclid: infinitely many primes
Bezout: gcd(a,b)=d ↔ ∃x,y: ax+by=d
FTA: unique prime factorization
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| (a/p)=1 means a is QR | Jacobi symbol (a/n)=1 does NOT mean a is QR mod n |
| Fermat pseudoprimes | a^(p-1)≡1 doesn't prove p is prime; use Miller-Rabin |
| CRT requires coprime moduli | Must verify gcd(nᵢ,nⱼ)=1 for all pairs |
| φ(mn) = φ(m)φ(n) always | Only when gcd(m,n)=1 |
| Modular inverse always exists | a⁻¹ mod n exists ↔ gcd(a,n)=1 |
| Large exponent arithmetic | Always reduce mod n at each step (don't compute aᵇ first) |

---

## Related Skills

- **abstract-algebra-expert**: Groups, rings, fields (algebraic number theory)
- **cryptography-expert**: Applied number theory
- **discrete-mathematics-expert**: Combinatorial number theory
- **calculus-expert**: Analytic number theory foundations
- **computer-science-algorithms**: Number theoretic algorithms

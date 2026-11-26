# Mathematics and Theoretical Methods

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## algebra-number-theory

**Use when:** Use when a task involves rigorous algebraic or number-theoretic reasoning: groups, rings, fields, Galois theory, modular arithmetic, primes, Diophantine equations, factorization, or computational checks of such claims in physics or mathematics work.

### Purpose and boundaries

This skill governs the construction, checking, and communication of results in abstract algebra and elementary-to-intermediate number theory. It covers: definitions and structure proofs (groups, rings, ideals, fields, modules at an introductory-to-graduate level); field extensions and Galois correspondence; congruences, residue arithmetic, quadratic reciprocity, and Diophantine problems; and computational verification of these claims, including the algebraic structures that arise in physics (symmetry groups, representation labels, lattice and finite-field models, error-correcting codes, discrete Fourier analysis on cyclic groups).

Out of scope: research-level claims presented as settled without literature check; cryptographic security assessments of real systems; and any statement that a standard result is "new" without evidence.

### Inputs and assumptions

Before working, establish:

1. The exact statement to prove, compute, or check, with all quantifiers and domains explicit (e.g., "for all integers n ≥ 2", "over ℚ", "in ℤ/mℤ").
2. The ambient structure: which group, ring, or field; whether commutative; characteristic.
3. The required output: proof, counterexample, computation, or classification.
4. The rigor level: informal explanation, full proof, or machine-checked argument.
5. Available tools (CAS, proof assistant, language runtime). Record the tool name and version; do not assume a function exists without checking current official documentation.

If any quantifier or domain is ambiguous, state the two most plausible readings and ask which applies before proceeding.

### Operating workflow

1. **Restate.** Write the claim in formal notation. Identify hypotheses and conclusion separately.
2. **Classify.** Determine the technique: direct algebra, induction, descent, Chinese Remainder Theorem, quadratic reciprocity, Galois theory, counting (Burnside/orbit-stabilizer), or computation.
3. **Test small cases.** Check at least three instances, including the smallest nontrivial one and one edge case (0, 1, identity, prime powers, characteristic 2). Record results in a table.
4. **Attempt proof or search for counterexample.** If a counterexample exists in the small-case search, stop and report it before attempting a proof.
5. **Write the argument.** Each step cites a definition, axiom, or previously established lemma. No step relies on "clearly" or "by symmetry" without justification.
6. **Independently verify.** Re-derive key identities by a second method, or compute them with a CAS over exact arithmetic (rationals, integers, finite fields), never floating point.
7. **Package** per the deliverable contract.

### Decision gates

- **Gate A (domain):** If the structure is not specified, stop and request it. Do not assume ℤ.
- **Gate B (counterexample):** If any small case fails, the claim is false as stated unless the hypotheses were misread. Report the failing case first.
- **Gate C (computation vs. proof):** A finite computation establishes only the finite cases checked. Use computation to find patterns, not to claim a general theorem, unless the domain is finite and fully enumerated, in which case state exactly what was enumerated.
- **Gate D (literature):** If the result resembles a named theorem (e.g., Sylow, Dirichlet, Wedderburn, Lagrange), cite the theorem by name and check its hypotheses rather than re-deriving with gaps.
- **Gate E (approval):** Obtain explicit user approval before any action that writes to shared repositories, publishes results, submits to external systems, or uses sensitive data.

### Verification and evidence

Quality checks, all required before delivery:

- Every quantifier and domain stated explicitly.
- Hypotheses used are listed; no unused hypothesis is silently assumed.
- At least three test instances reported with exact values.
- Exact arithmetic used for all computations; the tool and its version recorded.
- Each cited theorem stated with its hypotheses, and each hypothesis checked.
- A second derivation or independent computation agrees with the primary result.
- Any function, library call, or package name is marked "verify against current official documentation" unless confirmed in this session.

### Failure handling

- **Counterexample found:** report the instance, the step where the claim fails, and the corrected statement if one exists.
- **Stuck proof:** state the gap precisely (which lemma is missing), do not hide it with hedged wording, and propose the smallest lemma that would close it.
- **Computation disagrees with hand derivation:** assume an error in one of them until resolved; check indexing, modular reduction, and sign conventions first.
- **Tool unavailable or output ambiguous:** fall back to a hand-verifiable small case and say so.

### Deliverable contract

Return:

1. Formal statement with explicit domain.
2. Result: proof, counterexample, or computed classification, with a status label (Proven / Disproven / Verified-finite / Open-gap).
3. Proof or computation, step-numbered, each step justified.
4. Test-case table with exact values.
5. Verification log: method used, second check performed, tool and version.
6. Assumptions and unverified items listed explicitly.

Do not: round intermediate results; treat a finite check as a general proof; invent theorem names, function signatures, or version features; claim novelty; or present a conjecture as established.


## analysis-topology

**Use when:** Use when a task requires verifying or applying topological arguments in mathematics or physics, such as checking continuity, compactness, connectedness, or manifold claims, computing homotopy or homology invariants, or interpreting winding numbers, Chern numbers, or other topological invariants in a physical model.

### Purpose and boundaries

This skill covers rigorous topological reasoning used in analysis, geometry, and theoretical physics: point-set topology, metric and topological continuity, compactness and connectedness, manifolds, fundamental groups, homology, and the invariants physicists extract from them (winding numbers, Chern numbers, Z2 indices, Berry phases, band topology). It supports three activities: checking a topological claim, computing an invariant, and mapping a physical system onto a topological framework.

It does not cover numerical convergence of solvers, general measure theory, or empirical claims about real materials. Those require other skills or specialist review.

### Inputs and assumptions

Before reasoning, establish and state:

1. **The space**: its underlying set, the topology (open-set definition, metric, or induced structure), and any separation axioms assumed (Hausdorff, second countable, paracompact).
2. **The maps**: domain, codomain, and regularity class (continuous, smooth, holomorphic).
3. **The claim**: the exact statement to verify, with quantifiers.
4. **The physical model, if any**: Hamiltonian or action, symmetry group, boundary conditions, parameter space, and the gap condition under which invariants are defined.
5. **The scalar field and dimension.**

If any item is ambiguous, list the candidate interpretations and resolve each, or ask. Never silently choose a topology or a smoothness class that changes the answer.

### Operating workflow

1. **Restate the claim** in one formal sentence with all quantifiers explicit.
2. **Identify the governing theorem family**: intermediate value and connectedness arguments, Heine-Borel or Tychonoff for compactness, covering-space or van Kampen for fundamental groups, Mayer-Vietoris or cellular homology for homology, Stokes-type or Gauss-Bonnet-type integrals for Chern and Euler characteristics.
3. **Check every hypothesis** of that theorem against the stated space. Record pass, fail, or unknown for each.
4. **Compute or construct the object**: explicit open cover, explicit loop, explicit chain complex, or explicit integral over a closed parameter manifold.
5. **Test with a boundary case**: a trivial map, a degenerate parameter, or a dimension-one reduction.
6. **Cross-check by a second route** where possible (for example, winding number computed both as an integral and as a count of zeros with signs).
7. **State the conclusion with its exact scope**, including what was not established.

### Decision gates

- **Gate A (hypotheses):** If any hypothesis of the applicable theorem is unverified, do not assert the conclusion. Either prove the missing hypothesis or downgrade to a conditional statement.
- **Gate B (invariance):** An invariant may be reported as a property of a physical system only if the gap or regularity condition that makes it well defined holds across the entire parameter path. If the gap closes anywhere on the path, report the invariant as undefined there and say so.
- **Gate C (integrality):** A Chern number or winding number must evaluate to an integer within numerical or symbolic tolerance. A non-integer result indicates a flaw in the setup, not a finding.
- **Gate D (scope escalation):** If the result will be used for experimental prediction, engineering design, or publication of a physical claim, require explicit review by a domain specialist before it is presented as established.

### Verification and evidence

Each result must come with:

- The hypothesis checklist with status for each item.
- The explicit construction (cover, loop, cycle, or integrand) used.
- At least one independent check (alternative method, known special case, or symmetry argument).
- For physics invariants: the gap value on the path, the integration domain, and the discretization or limit used if numerical.

Measurable checks: the Chern number is integer-valued to within 1e-6 relative error under refinement, or the discrepancy is explained; winding numbers match the zero-count formula; Euler characteristic from a cell count matches the alternating sum of homology ranks.

### Failure handling

- **Hypothesis fails:** Report the specific failed hypothesis and the counterexample if one exists. Propose the weakest corrected statement that holds.
- **Non-integer invariant:** Re-check the gap, the orientation convention, the branch cut, and the integration grid before reporting anything.
- **Conflicting routes:** Locate the first step where they diverge. Do not average results.
- **Insufficient information:** Stop and list the missing inputs from the section above.

### Deliverable contract

Return:

1. Formal restatement of the claim.
2. Hypothesis table (hypothesis, status, justification).
3. Construction and computation, step by step.
4. Verification checks with results.
5. Conclusion with explicit scope and unresolved items.
6. Any items requiring approval under Decision Gate D.

### What not to do

- Do not assume compactness, Hausdorffness, or smoothness without stating it.
- Do not report a physical invariant from a single parameter point.
- Do not round or force an integer invariant.
- Do not cite theorem names or numerical results from memory without flagging them for verification against the primary reference.
- Do not state software function names, flags, or library versions from memory; mark any version-sensitive detail for verification against current official documentation.
- Do not present conditional results as unconditional.
- Do not take any external action (publishing, submitting results to third parties, altering shared files or data) without explicit user approval.


## differential-equations-computation

**Use when:** Use when solving, analyzing, or numerically approximating ordinary or partial differential equations for physics or mathematics work, including model setup, boundary and initial conditions, analytic solution checks, stability and convergence assessment, and reporting of numerical results.

### Purpose and boundaries

This skill governs the end-to-end computation of solutions to ordinary differential equations (ODEs) and partial differential equations (PDEs) arising in physics and applied mathematics: classical mechanics, heat and diffusion, wave propagation, fluid flow at the model level, electrostatics, population and reaction kinetics, and control systems.

In scope: formulating the problem well-posedly, choosing an analytic or numerical method, implementing or checking a solution, verifying accuracy, and reporting results with uncertainty.

Out of scope: proving new existence theorems, production simulation of safety-critical systems (requires a qualified engineering review), and any task that would run code or access data outside the user's stated environment without explicit approval.

### Inputs and assumptions

Before computing, confirm and record:

1. The governing equation(s), with every term defined and units stated.
2. Dependent and independent variables, domain, and dimensionality.
3. Boundary conditions (type: Dirichlet, Neumann, Robin, periodic) and initial conditions, each with a value or function.
4. Parameter values with units and source or assumption label.
5. Required output: closed form, a value at a point, a trajectory, a field, or a convergence study.
6. Accuracy target (e.g., relative error below 1e-6, or qualitative shape only).

If any item is missing, state the assumption explicitly and flag it. Do not silently pick parameter values.

### Operating workflow

1. **Classify the problem.** Order, linearity, coefficient type (constant or variable), dimension, and time dependence. A linear constant-coefficient ODE gets characteristic-equation treatment; a nonlinear or variable-coefficient problem gets a numerical or series approach first.
2. **Check well-posedness.** Count conditions against order: an nth-order ODE needs n conditions at the same point (initial value) or at boundary points (boundary value). For PDEs, verify the boundary-condition type matches the equation class (elliptic, parabolic, hyperbolic).
3. **Non-dimensionalize** where scales are clear. This reveals the governing dimensionless groups and reduces parameter sweeps.
4. **Attempt an analytic solution** when the structure allows (separation of variables, integrating factors, Laplace transforms, Green's functions, method of characteristics). Stop and record why if the attempt fails.
5. **Select a numerical method** if needed:
   - Non-stiff ODE: adaptive Runge–Kutta or a comparable explicit solver.
   - Stiff ODE: implicit or stiff-aware solver.
   - Elliptic PDE: finite differences, finite elements, or spectral methods depending on geometry.
   - Parabolic/hyperbolic PDE: check the CFL-type stability condition before choosing step sizes.
6. **Implement** with the minimum code needed. Check the exact function names and signatures of any library against its current official documentation, since these change between versions.
7. **Run verification** (see below) before reporting any number.
8. **Write the deliverable** using the contract below.

### Decision gates

- **Gate A (well-posedness):** Proceed only if the condition count and type are consistent. Otherwise stop and request the missing condition.
- **Gate B (analytic vs. numeric):** Use closed form if it is verified by substitution and matches a limiting case. Otherwise go numeric.
- **Gate C (stability):** For explicit time-stepping, confirm the step size satisfies the stability bound for the discretization. If the problem is stiff and the step size is forced very small, switch to an implicit method.
- **Gate D (convergence):** Accept results only after a refinement study shows the error decreases at the expected order. If not, do not report the value as converged.
- **Gate E (external impact):** Any action that writes files outside the working directory, overwrites prior results, submits jobs to shared compute, sends data externally, or uses personal or restricted data requires explicit user approval first.

### Verification and evidence

Apply these checks and record the outcome:

- **Substitution check:** Plug the analytic or numeric solution back into the equation; residual should be at machine-level or discretization-level tolerance.
- **Boundary and initial condition check:** Evaluate the solution at each boundary and at t=0; report the maximum deviation.
- **Limiting-case check:** Reduce a parameter (e.g., damping to zero, domain to infinity) and compare against a known result.
- **Conservation check:** Where physics implies it (energy, mass, charge), report drift over the simulation.
- **Grid or step refinement:** Halve the step size (or double resolution) and report the change; estimate observed order as log2 of the error ratio.
- **Independent cross-check:** Where feasible, solve with a second method and compare.

Report every check with its numeric result, not a qualitative word such as "good."

### Failure handling

- **Divergence or blow-up:** Reduce the step size, check the stability bound, verify sign conventions in source terms, and confirm boundary conditions are not inconsistent with the initial data.
- **Non-convergence under refinement:** Suspect a bug, a discontinuity not resolved by the grid, or a singularity. Locate it before tuning tolerances.
- **Mismatch with analytic check:** Assume the implementation is wrong first, then the derivation, then the model.
- **Ambiguous input:** Stop and ask rather than guessing parameters or condition types.

### Deliverable contract

Every result must include:

1. Problem statement with equation, domain, conditions, and parameters with units.
2. Method used and the reason for choosing it (including why analytic was rejected if applicable).
3. Result with stated accuracy, error estimate, and the verification checks above with their numbers.
4. Assumptions list and any unverified version-sensitive tool details flagged for checking against official documentation.
5. Limitations, including regimes where the model or method is not valid.

### What not to do

- Do not report a numerical value without a convergence or residual check.
- Do not present a stiff problem's explicit-solver output as accurate without a step-size study.
- Do not invent library functions, flags, or version numbers; mark them for verification.
- Do not claim physical validity beyond the stated model.
- Do not run jobs, overwrite files, or transmit data without approval under Gate E.


## discrete-logic

**Use when:** Use when analyzing, designing, or verifying discrete logic in physics or mathematics work, including Boolean and digital circuit reasoning, combinatorial state spaces, finite automata and transition systems, discrete-time or lattice models, and proofs over finite or countable structures.

### Purpose and boundaries

This skill guides rigorous work on problems whose state spaces are finite or countable: propositional and Boolean logic, combinatorial enumeration, finite-state and transition models, discrete-time simulation logic, lattice and spin-model bookkeeping, and discrete proofs (induction, pigeonhole, invariants, bijections). It produces verified formulas, truth tables, state machines, proof sketches, or counterexamples.

It does not cover continuous-field analysis, numerical-stability tuning of floating-point solvers, or hardware sign-off for fabricated chips. Hand those to the appropriate continuous or engineering skill.

### Inputs and assumptions

Before working, establish and write down:

1. The exact statement to prove, compute, or implement, in one sentence.
2. The domain: variables, their finite ranges, and the universe (e.g., bits, integers mod n, graph vertices).
3. Operators and their semantics. State conventions explicitly when ambiguous (e.g., XOR as exclusive or, implication as material conditional, whether 0 is natural).
4. Constraints: which states or transitions are forbidden, reachable, or initial.
5. The output form required: proof, table, minimal expression, count, automaton, or code.

If any item is missing and cannot be inferred without guessing, ask. Do not assume a convention that changes the answer.

### Operating workflow

1. **Formalize.** Restate the problem as symbols, sets, and relations. Name every variable with its type.
2. **Size the space.** Compute the number of cases. If it is at most about 2^16 assignments, enumerate exhaustively; otherwise reason structurally.
3. **Choose a method.** Truth tables for small propositional problems; Karnaugh or Quine–McCluskey for minimization; BFS/DFS on the transition graph for reachability; induction or invariants for infinite families; bijective counting or generating functions for enumeration.
4. **Derive.** Keep each step justified by a named law (De Morgan, distributivity, induction hypothesis, pigeonhole). Avoid unnamed leaps.
5. **Cross-check.** Verify by a second method (see Verification).
6. **Report** in the deliverable contract format.

### Decision gates

- **Gate A (scope):** If the problem mixes discrete and continuous quantities, isolate the discrete component and state what is excluded before proceeding.
- **Gate B (method):** If the exhaustive space exceeds about 2^20 cases and no structural argument exists, stop and report the need for a search tool or a restricted subproblem. Do not claim exhaustive coverage.
- **Gate C (equivalence claims):** Only assert two formulas or machines are equivalent after a truth-table or bisimulation check over the full space, or a complete proof.
- **Gate D (external impact):** Writing files outside the working artifact, executing code against shared systems, or publishing results requires explicit user approval. Destructive edits to existing artifacts also require approval.

### Verification and evidence

- Truth tables: row count must equal 2^n; spot-check at least three rows against the original expression.
- Minimization: the simplified form must match the original on every row, and the cover must be irredundant.
- Reachability: report the number of reachable states and show one witness path per claimed reachable state class.
- Counting: verify with a small-n brute force; the formula must match for n = 1 to 4 at minimum.
- Induction: state the base case, hypothesis, and step explicitly; check that the step uses the hypothesis.
- Counterexamples: give the concrete assignment or trace and evaluate it step by step.

Mark any claim that depends on a specific tool version, library function, or standard convention as "verify against current official documentation."

### Failure handling

- If a truth table disagrees with the claimed identity, report the first differing row and stop; do not adjust the claim to fit.
- If induction fails at the step, identify the gap and test whether the statement is false for small n.
- If a state space is larger than the method can handle, reduce by symmetry or invariant, and state the reduction as an assumption.
- If the problem statement is ambiguous, list the two readings, solve both briefly, and ask which applies.

### Deliverable contract

Return:

1. **Statement** restated in formal notation.
2. **Assumptions** and conventions used.
3. **Result** (formula, count, proof, automaton, or counterexample).
4. **Evidence**: method used, number of cases checked, and the cross-check performed.
5. **Limits**: what was not covered and what requires verification against current documentation.

Do not present a result as proven when only sampled. Do not omit failed cases that were found during checking.


## probability-statistics

**Use when:** Use when a physics or mathematics task requires building a probability model, computing distributions or moments, estimating parameters, propagating measurement uncertainty, testing hypotheses, performing Bayesian updates, or validating Monte Carlo results.

### Purpose and boundaries

This skill covers formulating probability models for physical and mathematical problems, deriving distributions and moments, estimating parameters, propagating measurement uncertainty, testing hypotheses, Bayesian updating, and checking simulation output. It does not cover experimental design logistics, regulatory or clinical statistics, safety-certified reliability claims, or any conclusion that will be published or acted on without expert human review.

### Inputs and assumptions

Required before work begins:
- The quantity of interest, its units, and the sample space or measurement model.
- Data (values, uncertainties, sample size, known correlations) or a precise description of the generating process.
- Stated assumptions: independence, identical distribution, stationarity, and the distribution family.

Record every assumption explicitly. If an input is missing or ambiguous, ask. Do not substitute a default that changes the answer.

### Operating workflow

1. Restate the question as a precise object: random variable, distribution family, parameter, estimator, or hypothesis pair.
2. Check consistency: densities integrate to one, probabilities lie in [0, 1], variances are nonnegative, and uncertainties carry the same units as the quantity.
3. Select the method. Use closed form for simple models. Use linear propagation for small uncertainties through smooth functions. Use sampling when the function is nonlinear, the posterior is multimodal, or tails are heavy.
4. Compute symbolically until the final numeric step. Carry at least two more significant figures than you will report.
5. Cross-check by a second route: analytic against simulation, two estimators, or a limiting case.
6. Report the result with its uncertainty, method, and assumptions.

### Decision gates

- **Independence:** If correlation is plausible (shared calibration, time series, common cause), do not multiply probabilities or add variances in quadrature until covariance is estimated or bounded.
- **Sample size:** Below roughly 30 points, do not rely on large-sample normal approximations without checking. Use exact or t-based methods.
- **Linearization:** If relative uncertainty exceeds about 10%, or the function curves strongly across the uncertainty range, switch to Monte Carlo or include second-order terms.
- **Priors:** State the prior. Run a sensitivity check with at least two alternative priors. If the posterior shifts materially, report the range, not a single value.
- **Multiple comparisons:** When testing many outcomes, adjust thresholds or state the number of tests.
- **Escalate** before finalizing any conclusion that would drive a safety, medical, financial, or publication decision.

### Verification and evidence

Each check must produce a measured value, not a qualitative judgment:
- **Normalization:** Numerical integral of the density over its support within 1e-6 relative tolerance.
- **Monte Carlo convergence:** Standard error below the target tolerance. Report sample count and seed. Confirm stability by doubling the sample count.
- **Limiting cases:** Zero variance recovers a deterministic result. Large n recovers the expected central-limit scaling. Known special cases match.
- **Coverage:** For interval claims, check empirical coverage on simulated data with known truth.
- **Residuals:** Inspect fit residuals for systematic structure and report any pattern.
- **Reporting:** Every numeric result includes units, uncertainty, and the confidence or credibility level.

### Failure handling

- **Analytic and numeric disagree beyond tolerance:** Evaluate both at a simple parameter value to locate the faulty step before rechecking everything.
- **Estimator unstable across seeds:** Increase samples, test for heavy tails, consider robust estimators (median, trimmed mean), and report the instability.
- **Data inconsistent with the model:** Report the discrepancy with a goodness-of-fit statistic. Do not refit silently to force agreement.
- **Contradictory or missing inputs:** Stop and request clarification.

### Deliverable contract

Return, in order:
1. The question as stated, with model and assumptions.
2. Method and key equations.
3. Result with uncertainty and stated confidence or credibility level.
4. Verification checks performed, each marked pass or fail with its measured value.
5. Limitations, and what new information would change the conclusion.

Do not:
- Interpret a p-value as the probability that the hypothesis is true.
- Report significance without effect size.
- Present simulation output without error bars.
- Add uncertainties linearly when independence is justified, without stating why.
- Cite library functions, package versions, or numerical benchmarks from memory. Mark any software-specific detail "verify against current official documentation."


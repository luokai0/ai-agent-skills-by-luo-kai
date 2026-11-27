# Design and Creative Production

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## accessibility-compliance

**Use when:** Use when auditing, remediating, or reviewing frontend web or app UI for WCAG conformance, keyboard and screen reader operability, color contrast, semantic markup, or accessible component behavior before release.

### Purpose and boundaries

This skill guides an agent through evaluating and fixing accessibility defects in frontend code and rendered UI against WCAG 2.1 or 2.2 success criteria (confirm the target version with the user). It covers automated scanning, manual keyboard and assistive technology checks, code-level remediation, and evidence reporting.

It does not certify legal compliance, issue conformance statements on behalf of an organization, or guarantee that a product is accessible. Those decisions belong to qualified auditors and the accountable team. Backend logic, content authoring policy, and non-web platforms are out of scope unless explicitly added.

### Inputs and assumptions

Before starting, establish:

- Target standard and level (for example WCAG 2.2 AA). Default to AA only if the user confirms it.
- Scope: specific routes, components, or user flows.
- Stack: framework, component library, and styling approach. Component libraries often have their own accessibility documentation; verify current versions against official docs.
- Runtime access: whether a browser can be run locally and whether test data is non-sensitive.
- Known constraints: design tokens that cannot change, legacy components, or third-party embeds.

Assume nothing about user environments. If a test cannot be run, record it as not verified rather than passing it.

### Operating workflow

1. **Map the scope.** List pages, states (empty, error, loading, modal open), and interactive flows. Identify each distinct component type.
2. **Run automated checks.** Use an established engine such as axe-core or an equivalent linter (confirm current version and rule set against its official documentation). Record rule IDs, counts, and affected selectors. Automated tools typically catch only a portion of defects; treat a clean run as incomplete evidence.
3. **Test keyboard operation.** Tab through each flow. Verify visible focus, logical order, no keyboard traps, operable custom widgets, and that Escape closes dismissible overlays with focus returned to the trigger.
4. **Test with assistive technology.** Use at least one screen reader on each major platform the user supports. Check accessible names, roles, states, live-region announcements, and form error association.
5. **Check visual properties.** Measure text and UI contrast with a tool; verify reflow at 320 CSS pixels wide, text resize, and that information is not conveyed by color alone.
6. **Review semantics in code.** Confirm native elements are used before ARIA, headings form a meaningful outline, landmarks exist, images have appropriate alternatives, and decorative content is hidden from assistive technology.
7. **Remediate in small commits.** Fix one defect class at a time, rerun the relevant checks, and note the before and after state.
8. **Produce the deliverable.** Follow the contract below.

### Decision gates

- **Gate A, before any change to shared design tokens or global styles:** stop and request approval. Changes can affect many components and other teams.
- **Gate B, before modifying third-party embeds or vendor components:** confirm ownership and whether a wrapper is acceptable. Do not fork vendor code without approval.
- **Gate C, before removing or altering existing tests, analytics hooks, or user-facing copy:** request approval. Copy changes can alter legal or brand commitments.
- **Gate D, before pushing, deploying, or publishing reports to external parties:** require explicit approval.
- **Contrast decisions:** if a fix would change brand colors, present two or three compliant alternatives with measured ratios and let the owner choose.
- **ARIA addition:** add ARIA only when no native element or attribute provides the semantics. Any added role must have all required states and properties.

### Verification and evidence

Each reported defect must include: WCAG criterion number and name, severity (blocker, serious, moderate, minor), reproduction steps, affected element selector or file path, and evidence (tool output excerpt or screen reader transcript summary).

A fix is verified only when:
- the originating automated rule no longer fires,
- the keyboard path works end to end,
- the screen reader announces the expected name, role, and state,
- contrast ratios meet the target threshold (4.5:1 normal text, 3:1 large text and non-text UI components under WCAG 2.x; confirm against the current specification),
- no new violations appear in the touched component.

Report unverified items separately. Never write "passes WCAG" as a blanket claim.

### Failure handling

- **Tool unavailable or crashes:** record the failure, fall back to manual checks, and mark the affected criteria as unverified.
- **Conflicting requirements** (for example, a design mandates a low-contrast style): escalate with the specific criterion and options.
- **Cannot reproduce a reported issue:** document the environment, browser, assistive technology version, and steps tried. Do not close it silently.
- **Fix introduces regression:** revert that change only, then re-analyze.

### Deliverable contract

Return a single report with these sections in order:

1. Scope and standard tested (with version of the criteria referenced).
2. Environment: browsers, assistive technologies, tool names and versions as observed.
3. Findings table: ID, criterion, severity, location, status (fixed, open, unverified).
4. Changes made: file paths and a summary of each change.
5. Verification results per finding, with evidence.
6. Open decisions requiring approval, from the decision gates.
7. Residual risk: areas not tested and why.

Do not state that the product is compliant. State only which criteria were checked, what passed, and what remains open. Version-sensitive details (tool rule IDs, criteria wording, browser support for specific features) must be marked for verification against current official documentation.


## creative-media-generation

**Use when:** Use when producing, transforming, or integrating images, SVG graphics, icons, illustrations, animations, video, or audio assets into a frontend web application, including generating assets with external AI tools and optimizing them for delivery.

### Purpose and boundaries

This skill covers creating and integrating media assets for a frontend project: raster images, vector graphics (SVG), icons, illustrations, CSS/SVG/canvas animations, short video loops, and audio cues. It covers asset generation, editing, format selection, optimization, and wiring assets into components with correct sizing, accessibility, and performance.

It does not cover backend media pipelines, DRM, live streaming infrastructure, or legal clearance of third-party IP. It does not decide brand identity or replace a designer's judgment on aesthetics.

### Inputs and assumptions

Before work begins, establish:

- Target surfaces: breakpoints, display density, minimum and maximum rendered sizes.
- Consumers: which components, routes, or templates will embed each asset.
- Constraints: performance budget (bytes per asset, total page weight), supported browsers, reduced-motion requirements.
- Style source: existing design tokens, palette, type, or reference assets. If none exist, ask rather than invent a visual system.
- Provenance rules: whether generated or sourced assets are allowed in this project and what records must be kept.

Assume nothing about tool availability or versions. Treat any tool name, flag, or library version as unverified until checked against its current official documentation.

### Operating workflow

1. **Inventory.** List every asset request with its purpose, rendered size, and placement. Merge duplicates. Reuse existing assets where they meet the spec.
2. **Choose format by content.** Use SVG for flat shapes, icons, and logos. Use photographic formats for photos and complex gradients. Use video only for motion that cannot be expressed in CSS or SVG. Use CSS, SVG, or canvas animation before video when the motion is simple.
3. **Generate or source.** For external generation tools, first confirm the action is approved (see Decision gates). Write prompts that state subject, composition, palette, aspect ratio, and negative constraints. Generate at the largest needed size, not larger.
4. **Edit and normalize.** Crop to the intended aspect ratio, strip metadata that is not required, set consistent color profile, and produce named variants for each required density or breakpoint.
5. **Optimize.** Compress to the smallest format and quality that passes visual review. Run SVG cleanup that preserves `viewBox` and IDs referenced elsewhere. Generate responsive sources for raster images so browsers can select the right size.
6. **Integrate.** Embed with explicit intrinsic dimensions to prevent layout shift. Provide meaningful `alt` text for informative images and empty alt for decorative ones. Lazy-load below-the-fold media. Respect `prefers-reduced-motion` for any animation.
7. **Record.** Save a manifest entry per asset: source or generation method, prompt or tool settings where applicable, license or usage terms as stated by the source, file hashes, and dimensions.

### Decision gates

Stop and request explicit user approval before:

- Sending any project material, brand assets, or unreleased content to an external generation or hosting service.
- Replacing, deleting, or overwriting existing committed assets.
- Publishing or deploying assets to a live environment.
- Generating images depicting real identifiable people, minors, or trademarked characters or logos.
- Adding third-party assets whose license terms you cannot confirm from the source.
- Any step that incurs cost or requires credentials.

Proceed without asking only for local, reversible work: creating new files in a working directory, generating vector drafts, and optimizing copies.

### Verification and evidence

Each asset must pass these checks before integration:

- Rendered dimensions match spec within one CSS pixel at target densities.
- Raster file size is within the budget in the project spec; SVG has no embedded raster unless intended.
- No layout shift: Cumulative Layout Shift attributable to the asset is measured in the browser and reported.
- Contrast: text overlaid on media meets WCAG 2.2 AA ratio (4.5:1 normal text, 3:1 large text), measured with a tool, not by eye.
- Animation: runs at target frame rate on a mid-range device profile, and is disabled or simplified under reduced motion.
- Visual review: side-by-side comparison against the reference at each breakpoint, with findings recorded.

Report numbers, not adjectives. "Hero image 142 KB AVIF, LCP 1.9 s on throttled profile" is evidence; "looks fast" is not.

### Failure handling

- **Generated output off-brief:** Revise the prompt once with specific corrections. If still off-brief after two attempts, switch to manual composition or ask the user.
- **Budget exceeded:** Lower quality, reduce dimensions, or change format. Do not silently exceed the budget.
- **Format unsupported by a target browser:** Serve a fallback through `picture` or equivalent, verified against current browser support data.
- **Unknown license:** Quarantine the asset, do not integrate, and ask the user.
- **Tooling error:** Record the exact error and the step, then ask before retrying with different settings.

### Deliverable contract

Return:

1. Asset files with stable, descriptive names and the required variants.
2. The integration diff (markup, styles, and loading attributes).
3. The manifest with provenance, license status, hashes, and dimensions.
4. A verification table listing each check, measured value, pass or fail, and method.
5. Open items requiring approval, listed explicitly.

Do not include temporary or unreviewed assets, unmeasured claims, or integration code that has not been rendered and checked.

### Ultron routing contract

**Choose this skill when:** creating or integrating particular media assets for a frontend project: images, vectors, icons, illustrations, CSS/SVG/canvas animation, short loops, audio cues, optimization, accessibility, and component wiring.

**Choose generative-media-production when:** the work requires a complete production workflow from brief and model selection through generation runs, rights/provenance review, packaging, and delivery beyond the frontend integration boundary.

**Handoff contract:** receive approved creative direction, rights/consent limits, asset purpose, target formats, and acceptance criteria. Return the final optimized asset, source/provenance reference, dimensions, accessibility text, integration instructions, and performance impact. If new generation requires an external model or service, follow the production skill's approval and provenance controls.

**Why the boundary exists:** asset implementation in a frontend is not the same as governing the whole media-generation production process.


## css-styling

**Use when:** Use when writing, refactoring, or reviewing CSS for web interfaces, including layout, theming, responsive behavior, specificity conflicts, and visual regressions in frontend codebases.

### Purpose and boundaries

Produce maintainable, responsive, accessible CSS that matches the existing design system and browser support target. Covers layout (flow, flexbox, grid), typography, color and theming, spacing scales, responsive breakpoints, interaction states (hover, focus, disabled, error), motion, and stylesheet architecture.

Out of scope: JavaScript behavior, build configuration beyond what changes CSS output, markup restructuring, and brand or visual design decisions not already specified.

### Inputs and assumptions

Establish these before editing:
- Target browsers and minimum versions, taken from project configuration or the stakeholder. Do not assume.
- Styling method in use: plain CSS, CSS Modules, a preprocessor, a utility framework, or CSS-in-JS.
- Existing tokens, breakpoints, and naming conventions.
- Required component states and the design reference, if one exists.

If a missing item would change the output, ask. Otherwise state the assumption in the deliverable.

### Operating workflow

1. Read the surrounding stylesheet and locate existing tokens, utilities, and patterns. Reuse before creating.
2. Reproduce the issue or define the target: element, viewport width, and state.
3. Diagnose from computed styles, not guesses. Check cascade order, specificity, inherited properties, and containing blocks.
4. Make the smallest change at the correct layer: token, base element rule, component rule, or override. Change the source of a value rather than patching its symptom.
5. Verify across the viewport set and interaction states (see Verification and evidence).
6. Remove dead rules and duplicate declarations that the change introduced or exposed.

### Decision gates

- Use flexbox for one-dimensional alignment and grid for two-dimensional layout. Try intrinsic sizing (`min()`, `max()`, `clamp()`, `minmax()`, auto-fit) before adding media queries.
- Add a breakpoint only where content actually breaks at that width, not at a device size taken from a list.
- Keep specificity low. Use `!important` only to override third-party styles that cannot be changed, and document why.
- Use logical properties (inline and block axes) if the project supports right-to-left or vertical writing. Otherwise match the existing convention.
- Use custom properties for values that vary by theme or context. Use literal values for true constants.
- Ask for explicit approval before: renaming or deleting global selectors or tokens used elsewhere, changing shared design tokens that affect other products, altering published theme or public stylesheet exports, or making any change that alters brand appearance site-wide.

### Verification and evidence

Check every change against:
- Viewports: 320px, 768px, and 1280px at minimum, plus project-defined breakpoints.
- States: default, hover, focus-visible, active, disabled, and error where applicable.
- Keyboard focus remains visible. Focus indicators meet non-text contrast of 3:1 under WCAG 2.2; confirm this against current official guidance.
- Text contrast meets WCAG AA: 4.5:1 for normal text, 3:1 for large text.
- Text does not clip or overflow at 200% zoom or with increased user font size.
- No unexpected layout shift in the affected region. Run visual regression tests if the project has them.
- Evidence: list the viewports and states checked, plus before and after screenshots or computed values for each changed property.

Before using any newer property, function, or pseudo-class, confirm support against current official compatibility data. Do not rely on memory.

### Failure handling

- If a fix works in one browser engine but not another, record the engine and version, then check for a fallback or progressive enhancement path.
- If specificity conflicts recur, stop patching. Map rule ownership and restructure the cascade.
- If a change causes a regression elsewhere, revert it and isolate the shared selector before retrying.
- If the request conflicts with accessibility requirements, do not implement the conflicting part. Report the conflict and propose alternatives.

### Deliverable contract

Return:
1. The changed CSS, limited to the files touched.
2. A short rationale naming the root cause and the layer changed.
3. A verification record: viewports, states, contrast results, and any unverified items stated explicitly.
4. Assumptions and open questions.
5. Version-sensitive properties or features flagged for verification against current official documentation.

Do not add unrelated restyling, introduce new frameworks, hard-code colors where tokens exist, set fixed pixel heights on text containers, or claim cross-browser support without testing.

### Ultron routing contract

**Choose this skill when:** the visual target and design decisions are already established and the work is implementing or debugging CSS: cascade, specificity, layout, responsive rules, typography application, theme-variable wiring, browser rendering, or stylesheet architecture.

**Choose `ui-visual-design` when:** the task is to establish or audit the visual system itself: tokens, semantic color roles, type and spacing scales, component-state specifications, visual consistency, contrast, or translating an approved design reference into a coherent system.

**Handoff contract:** the design-system skill supplies approved tokens, states, breakpoints, and visual acceptance criteria. This skill implements them in the existing styling stack and returns the affected selectors/components, browser and viewport checks, and any mismatch that requires a design decision. Do not invent brand choices to solve a CSS defect.

**Why the boundary exists:** visual intent should be decided once and implemented consistently. CSS is the implementation medium, not the authority for brand or system-level design decisions.


## design-to-code

**Use when:** Use when converting a design file, mockup, prototype, or design specification (Figma, Sketch, XD, screenshots, or design tokens) into production frontend UI code, or when reviewing an implementation for fidelity to its design.

### Purpose and boundaries

This skill turns approved visual designs into frontend components and pages that match the design's layout, typography, color, spacing, states, and responsive behavior, while fitting the target codebase's conventions. It covers translating designs into markup, styles, and component structure; mapping design tokens to the project's theme system; and reviewing an existing implementation against its design.

It does not cover: inventing product behavior the design does not specify, redesigning screens, backend data modeling, brand or copy decisions, accessibility sign-off (it flags issues; a human owns certification), or deploying changes.

### Inputs and assumptions

Before writing code, confirm you have:
- The design source (file link, export, or screenshots at 1x and 2x) and the specific frames or components in scope.
- Target framework, styling system, and component library already used in the repository. Inspect `package.json`, existing components, and the theme configuration. Do not introduce a new styling approach.
- Breakpoints the design covers. If only one viewport is provided, state that responsive behavior is unverified.
- Token source: whether the design uses named variables/styles or raw values.
- Interaction states provided (hover, focus, disabled, error, loading, empty). Missing states are listed as open questions, not invented.

Assume the design is the source of truth for visuals, and the existing codebase is the source of truth for conventions. When they conflict, prefer the codebase convention and report the deviation.

### Operating workflow

1. **Inventory.** List every frame and component in scope. Identify repeated patterns (buttons, cards, form fields) that already exist in the codebase.
2. **Map tokens.** Build a table: design variable to project token (color, spacing, radius, type scale, shadow). Reuse existing tokens. Only add a new token when no existing one fits, and flag it.
3. **Decompose.** Split the layout into components with clear props. Separate presentational components from data-fetching logic. A component should reflect one visual responsibility.
4. **Build structure first.** Write semantic markup (landmarks, headings in order, real buttons and links) before styling. Use flex or grid as the design's alignment implies.
5. **Apply styles.** Use token references only; no hardcoded hex values, pixel offsets, or font stacks where a token exists. Implement all provided states.
6. **Responsive pass.** Implement the provided breakpoints. Where none are given, use fluid widths and flag the gap.
7. **Verify** (see below), then report.

### Decision gates

- **Missing state or breakpoint:** Stop for that element, record it as an open question, and implement only a clearly labeled provisional version if the user approves.
- **Token conflict** (design value differs from nearest token by more than a visible step): ask whether to adopt the token or add a new one. Do not silently round.
- **New dependency** (icon set, animation library, layout primitive): require approval, state the reason, and check the project's existing packages first.
- **Design asset export** (images, SVG, fonts): confirm licensing and whether the asset should be checked into the repo or loaded from a CDN. Treat that choice as external-impacting.
- **Replacing existing components:** requires approval, since it affects other screens.

### Verification and evidence

Provide evidence, not assertions:
- Side-by-side screenshots at each provided breakpoint, compared against the design frame. Report the measured pixel differences for key elements (box size, gap, font size) using the design tool's inspect values.
- Spacing and typography checks: each margin, padding, gap, and font size on the design's spec sheet matches a token or the stated value.
- Keyboard walk-through: every interactive element reachable and visibly focused in logical order.
- Automated checks the project already runs (type checking, linting, unit and visual regression tests). Report the actual command output, not an expectation.
- Contrast: report measured ratios for text and essential UI colors against WCAG 2.2 thresholds, using a tool. Mark results as indicative; do not claim compliance.

Target a visual deviation of no more than 2 px on positioned elements and exact token usage for colors and type. Anything larger is listed explicitly.

### Failure handling

- If a screenshot comparison fails, identify the element, correct the cause, and re-run. Do not loosen the threshold to pass.
- If the design uses a value that cannot be expressed in the project's system, report the constraint and propose the closest option with its visual cost.
- If the codebase lacks a required primitive, stop and ask before building one.
- If verification tooling is unavailable, state which checks were not run. Never report a check as passed when it was not executed.

### Deliverable contract

Return:
1. Files changed or created, with paths.
2. Token mapping table, including any new tokens flagged for approval.
3. Component list with props and responsibilities.
4. Verification record: commands run, outcomes, screenshot comparisons, measured deviations.
5. Open questions: missing states, breakpoints, assets, and unresolved token conflicts.
6. Known deviations from the design, each with a reason.

Do not:
- Hardcode values where tokens exist.
- Add dependencies, global styles, or theme changes without approval.
- Modify shared components silently.
- Invent copy, data, or behavior not present in the design.
- Describe the implementation as matching the design without the verification record to support it.


## generative-media-production

**Use when:** Use when producing images, audio, or video with generative models, especially when pulling checkpoints, LoRAs, voice models, or other weights from external registries and must verify licensing, provenance, and output quality before delivery.

### Purpose and boundaries

This skill governs end-to-end production of generated media for client, marketing, editorial, or internal use: brief intake, model selection from external registries, generation runs, quality review, and packaging with provenance records.

In scope: image, illustration, short audio, voiceover, and short video generation; selecting and vetting third-party model weights; prompt and parameter documentation; reproducibility records; export and metadata handling.

Out of scope: training new foundation models, generating likenesses of real people without written consent, political or medical imagery intended to be taken as factual, and any output whose purpose is deception.

### Inputs and assumptions

Before generating, confirm:

- **Brief**: deliverable type, dimensions or duration, format, count, intended channel, and usage term (duration, territory, exclusivity).
- **Rights position**: who owns the brief, reference assets, and any voice or face references. Missing rights information is a blocker, not a detail to fill in.
- **Model source**: registry name, model identifier, exact version or commit, and the license file text. Assume nothing about permissive use from a model's popularity.
- **Compute**: available hardware and time budget. Record it, since it affects reproducibility.

If any input is absent, ask. Do not infer rights or licenses.

### Operating workflow

1. **Scope the brief.** Write a one-paragraph spec with acceptance criteria: subject, style constraints, forbidden content, technical specs (resolution, sample rate, frame rate, duration, loudness target).
2. **Shortlist models.** Select 2–3 candidates from registries. For each, record publisher, version, license name, commercial-use clause, restrictions on outputs, and whether the card discloses training-data provenance. Check for included safety or watermarking components and whether they can be disabled, and do not disable them without approval.
3. **Vet weights.** Verify checksums against the registry's published values where provided. Do not load pickled or executable-format artifacts from untrusted sources; prefer safetensors or equivalent formats, and confirm the format against current loader documentation.
4. **Pilot run.** Generate small batches (4–8 outputs) per candidate using a fixed seed set. Log prompt, negative prompt, seed, sampler, steps, guidance scale, model hash, and software versions.
5. **Select and produce.** Choose the candidate that passes the spec with the clearest license. Generate the final set with the same logged parameters.
6. **Post-process.** Upscale, color-correct, normalize loudness, or trim only with logged tools. Keep the raw output alongside the edited version.
7. **Package.** Export to specified formats and attach a manifest (see Deliverable contract).

### Decision gates

- **Gate A (rights):** Proceed only if the model license explicitly permits the intended commercial use and any output restrictions are satisfied. "Research use only" or unclear wording stops the workflow.
- **Gate B (likeness and voice):** Any recognizable real person, or any cloned voice, requires signed consent from that person. Without it, stop.
- **Gate C (safety filters):** If a generated output triggers a content filter, do not route around it. Log the event and escalate.
- **Gate D (external delivery):** Uploading to a public registry, publishing to a channel, or sending to a client requires explicit approval from the project owner.
- **Gate E (destructive actions):** Deleting raw outputs, overwriting prior versions, or purging cache requires approval. Raw outputs are retained until the client accepts delivery.

### Verification and evidence

Measurable checks before delivery:

- Resolution, duration, sample rate, and frame rate match spec exactly (verify with a media probe tool).
- Image: no unintended text artifacts, hand or limb count correct in human subjects, no visible tiling seams; reviewer marks at least 90% of sampled frames as pass.
- Audio: clipping absent; integrated loudness within ±1 LU of target; no sibilance or phase artifacts on a headphone pass and a speaker pass.
- Video: no flicker between keyframes; temporal consistency checked on frame-by-frame sampling at 10% intervals.
- Provenance: manifest hashes match delivered files.

Where a registry or tool advertises a metadata or content-credential standard, confirm current support against official documentation before claiming it. Do not assert compliance with any regulation or standard as a guarantee.

### Failure handling

- **Quality failure:** Adjust one variable at a time (prompt, then seed, then sampler). Record each change. After three failed rounds on one candidate, switch candidates.
- **License ambiguity:** Stop, quote the clause, and request legal review.
- **Corrupted or mismatched weights:** Discard, re-download from the registry, and recheck hashes. Do not patch files manually.
- **Version drift:** If a library or model revision changes results, pin the prior version and note the discrepancy.

### Deliverable contract

Each delivery contains:

1. Final files plus raw outputs in separate folders.
2. `manifest.json` listing each file, SHA-256 hash, model registry, model identifier and version, license name, parameters, seeds, and reviewer sign-off.
3. A rights memo: source of every model, licensing clause relied on, consent records for any real likeness or voice.
4. A short notes file stating known limitations and any unresolved risks.

Do not deliver files lacking a manifest, and do not state that outputs are free of third-party rights. Mark any software or model version detail not verified against current official documentation as "to verify."

### Ultron routing contract

**Choose this skill when:** producing a complete generated-media deliverable from brief through model/tool selection, generation, review, provenance, packaging, and delivery for marketing, editorial, client, or internal use.

**Choose creative-media-generation when:** the task is creating, editing, optimizing, or integrating specific media assets into a frontend project, including SVG/CSS/canvas animation and component-level accessibility/performance.

**Handoff contract:** this skill supplies the approved brief, rights/consent constraints, output specifications, selected asset versions, provenance, and quality acceptance criteria. The creative-asset skill returns optimized formats, dimensions, accessibility metadata, integration instructions, and frontend performance checks. Keep source-generation provenance attached to the final asset.

**Why the boundary exists:** end-to-end media production governs the deliverable and its provenance; frontend asset integration governs how an approved asset behaves inside a product.


## product-design-app-development

**Use when:** Use when designing, building, or preparing a product app for distribution through an external registry, such as an app store, plugin marketplace, or public package registry, including metadata, packaging, submission readiness, and listing review.

### Purpose and boundaries

This skill guides the design and development of an app whose primary distribution channel is an external registry that a third party operates and reviews. It covers product definition for registry constraints, packaging and metadata, pre-submission verification, and response to review outcomes.

In scope: registry-specific design constraints, manifest and listing metadata, build and packaging layout, version and changelog discipline, submission checklists, and review feedback triage.

Out of scope: general application architecture unrelated to distribution, marketing copy strategy, legal drafting, and any act of publishing, submitting, or changing a live listing.

### Inputs and assumptions

Before work begins, collect and confirm:

1. The target registry and the specific policy and guideline documents in force. Record the date you read them.
2. The app's core user task, supported platforms, and minimum runtime versions.
3. Data the app collects, stores, or transmits, including third-party SDKs.
4. Existing publisher account, signing identities, and who holds them. Do not assume access.
5. Current release branch, build tooling, and the last approved version.

Assume nothing about registry rules from memory. Registry policies, manifest fields, and size or permission limits change. Mark every version-sensitive detail as "verify against current official documentation" in your working notes and in the deliverable.

### Operating workflow

1. **Map registry constraints to product decisions.** List each mandatory rule (permissions, content, age rating, data disclosure, required assets, review guidelines). For each, assign an owner and a design response. Example: if the registry requires a privacy declaration, the design must have a data inventory before any UI copy is written.
2. **Define the listing contract.** Draft name, short description, long description, category, keywords, screenshot set, and support URL in one document. Check each against character limits and prohibited claims in the current guidelines.
3. **Design for reviewability.** Each feature that needs elevated permissions gets a one-paragraph justification tied to a user-visible action. Hidden or deferred functionality must be disclosed, or removed.
4. **Build and package.** Produce a reproducible build from a tagged commit. Confirm the artifact's identifier, version string, and signing match the listing. Record artifact size and checksum.
5. **Run the pre-submission checklist** (see Verification).
6. **Prepare the submission packet** with the changelog, reviewer notes, test account credentials stored in an approved secret channel (never in the packet body), and known limitations.
7. **Stop at the submission gate.** Hand the packet to the approver.

### Decision gates

Stop and obtain explicit human approval before:

- Submitting, publishing, promoting, or updating any live listing.
- Changing signing keys, publisher identity, or package name. These are irreversible for existing users.
- Adding permissions, data collection, or third-party SDKs that alter the privacy disclosure.
- Using a feature flag or remote configuration to change behavior after review.
- Deleting or unpublishing a version that users may have installed.
- Sharing credentials, user data, or crash logs containing personal data with any external party.

Proceed without approval only for local builds, local tests, drafts, and internal documents.

Decision criteria for scope cuts: if a feature cannot be justified against a guideline within the release window, remove it from the submission build rather than requesting an exception.

### Verification and evidence

Each claim in the packet needs evidence:

- Build reproducibility: two clean builds from the same commit produce matching checksums, or the difference is explained.
- Metadata: every field validated against the current registry schema and length limits, with the source document cited.
- Permissions: a table mapping each permission to the code path and user action that requires it. Any permission without a mapping fails.
- Privacy: data inventory matches the disclosure text, including SDK-level collection. Mismatch is a blocker.
- Functional testing: a clean-install test on the minimum supported runtime and one current runtime, with results recorded.
- Assets: screenshots generated from the release build, with dimensions checked against registry requirements.

Quality threshold: zero open blockers, and no warnings without a written disposition by the owner.

### Failure handling

- **Rejected review:** Quote the cited guideline verbatim, identify the responsible feature or metadata field, and classify the fix as metadata-only, code change, or policy dispute. Metadata-only fixes can proceed to the approval gate. Code changes require a new build and full checklist rerun. Disputes go to the approver with evidence; do not argue with reviewers in the response without approval.
- **Failed build or signing:** Halt. Do not re-sign with alternate identities to get past an error.
- **Discovered privacy or security defect after approval:** Escalate immediately. Do not patch the live build without the approval gate.
- **Ambiguous guideline:** Record the ambiguity, choose the more conservative interpretation, and flag it for the approver.

### Deliverable contract

The final output is a submission packet containing:

1. Release summary: version, commit, artifact identifier, checksum, and target platforms.
2. Registry constraint map with source documents and retrieval dates.
3. Listing contract with validated metadata and character counts.
4. Permission and data-collection tables with evidence links.
5. Pre-submission checklist with pass, fail, or waived status per item and named owners.
6. Known limitations and reviewer notes.
7. Explicit statement of which approval gates remain open.

Do not state that the app is "compliant" or "approved." State only what was verified and against which document version.


## threejs-webgl

**Use when:** Use when building, debugging, or reviewing 3D web scenes with Three.js on WebGL, including scene graph setup, cameras, lighting, materials, loaders, animation loops, picking, performance tuning, and disposal of GPU resources.

### Purpose and boundaries

This skill covers production work with Three.js rendering in a browser through WebGL: scene composition, render loop design, asset loading, interaction, performance budgets, and resource lifecycle. It does not cover WebGPU-only renderers, game engines, server-side rendering of 3D output, CAD kernels, or general shader theory beyond what a Three.js material needs. Treat any Three.js API name, option, or example as version-sensitive: confirm against the official documentation for the installed release before relying on it.

### Inputs and assumptions

Collect before writing code:
- Three.js version and bundler (ESM import style matters; check the release notes for renamed modules and removed classes).
- Target devices and minimum frame budget (for example 60 fps on mid-range mobile versus 30 fps on kiosks).
- Asset inventory: formats, polygon counts, texture sizes, animation clip counts.
- Interaction requirements: picking, dragging, camera control style.
- Whether the page shares the GPU with other canvases or video.

If any of these is unknown, state the assumption explicitly in the deliverable.

### Operating workflow

1. **Define the frame contract.** Write the target frame time, draw-call budget, and memory ceiling. Without numbers, optimization is guesswork.
2. **Build the renderer once.** Create one `WebGLRenderer` per canvas. Set pixel ratio capped (commonly `Math.min(devicePixelRatio, 2)`), and size it from the container, not the window, when embedded.
3. **Compose the scene graph.** Group objects by transform and lifecycle, not by visual category. Keep static geometry separate from animated nodes.
4. **Configure camera and lights.** Set near/far planes as tight as the content allows; a large far-to-near ratio causes depth precision loss. Prefer a small number of lights; baked or environment lighting is cheaper than many dynamic lights.
5. **Load assets asynchronously.** Use a loading manager, show progress, and validate that every loaded texture has power-of-two-independent sizes you actually support on target hardware. Set color space on color textures (sRGB) and linear on data textures (normals, roughness, metalness).
6. **Write the render loop.** Use `renderer.setAnimationLoop` or a `requestAnimationFrame` loop with delta time clamped (for example to 0.1 s) so tab switches do not produce large jumps. Pause rendering when the canvas is off-screen or the document is hidden.
7. **Add interaction.** For picking, use a raycaster against a reduced proxy set, not the full scene. Throttle pointer-driven raycasts to one per frame.
8. **Dispose on teardown.** Call `dispose()` on geometries, materials, textures, and render targets, and `renderer.dispose()` plus removal of the canvas when the view unmounts. Remove event listeners.

### Decision gates

- **Instancing gate:** If more than roughly 100 meshes share one geometry and material, use `InstancedMesh`. Verify the draw-call count before and after.
- **Shadow gate:** Enable shadow maps only for lights that visibly need them, with the smallest map size that passes review. Each shadow-casting light adds a full scene pass.
- **Post-processing gate:** Add effect passes only after the base render meets the frame budget. Each pass costs a full-screen draw and extra render targets.
- **Texture gate:** Downscale any texture that exceeds the display size by more than 2x at the largest on-screen size. Compress with a GPU-friendly format only after confirming loader and toolchain support for the installed version.
- **Geometry gate:** Use compressed or quantized formats for large meshes only if the pipeline can produce and validate them.
- **Approval gate:** Changing the asset pipeline, deleting shipped assets, or altering a public embed API requires explicit approval from the owner.

### Verification and evidence

- Record draw calls, triangles, and texture memory from `renderer.info` at steady state. Store the values with the scene version.
- Confirm no growth in `renderer.info.memory.geometries` and `renderer.info.memory.textures` after repeated mount and unmount cycles. Growth indicates a leak.
- Measure frame time over at least 300 frames on the target device class. Report median and 95th percentile, not a single reading.
- Check color output against a reference image under the intended tone-mapping and color-space settings.
- Test resize, device pixel ratio change, context loss handling, and tab visibility changes.
- Verify picking accuracy by clicking known coordinates and comparing the hit object.

### Failure handling

- **Black or blank canvas:** Check the camera is not inside geometry, near/far planes exclude the content, and the render call runs after the first resize.
- **Context lost:** Listen for `webglcontextlost`, prevent default, and rebuild resources on `webglcontextrestored`. Do not assume restoration is automatic.
- **Texture artifacts or washed-out colors:** Verify color space assignment on each texture map.
- **Frame spikes:** Profile before changing code. Common causes are shader compilation on first use (precompile by rendering once off-screen), uncached texture uploads, and per-frame allocation of vectors or geometry.
- **Leaked memory:** Compare `renderer.info` counts against expected object counts; search for objects removed from the scene but not disposed.

Stop and report when a fix requires changing public APIs, deleting assets, or exceeding the agreed budget.

### Deliverable contract

Provide:
- The code change, with imports matching the verified Three.js version.
- A short statement of the Three.js version and any API checked against official documentation.
- A budget table: target versus measured draw calls, triangles, texture memory, and frame time (median and p95).
- The verification steps performed and their results.
- A list of open assumptions and items requiring owner approval.

Do not: invent benchmark numbers, claim cross-device performance without measurement on those devices, skip disposal code, or suppress console errors from WebGL to make a demo appear clean.


## ui-visual-design

**Use when:** Use when implementing or revising the visual layer of a user interface in code, including typography scales, spacing, color tokens, contrast, elevation, layout grids, responsive breakpoints, component states, and dark mode.

### Purpose and boundaries

This skill turns approved visual intent into consistent, verifiable frontend styling. It covers design tokens, type, spacing, color, surfaces, layout, responsive behavior, and component visual states.

In scope: translating mockups or style rules into tokens and CSS or component styles; auditing existing UI for inconsistency and contrast failures; defining state styles (hover, focus, active, disabled, error, loading); adapting layouts across viewport widths.

Out of scope: brand strategy, creating new logos or illustrations, user research, information architecture, backend logic, and rewriting application behavior. If the request requires those, state the gap and stop at the visual boundary.

### Inputs and assumptions

Before editing, confirm:

1. The source of truth: a design file, a style guide, an existing token set, or a screenshot. If none exists, derive a minimal token set from the current code and label it as derived.
2. Target platforms and minimum browser or device support.
3. The styling stack in use (plain CSS, a preprocessor, utility classes, or CSS-in-JS). Do not assume one.
4. Whether dark mode, reduced motion, and text scaling must be supported.

Record assumptions explicitly in the work summary.

### Operating workflow

1. Inventory. List existing color values, font sizes, spacing values, radii, and shadows. Count distinct values. Values outnumbering the intended scale signal drift.
2. Define tokens. Map primitives (raw values) to semantic roles (for example, surface, text-primary, text-muted, border-subtle, accent, danger). Components reference semantic tokens only.
3. Type scale. Use a constrained ratio or explicit steps (for example, 12, 14, 16, 20, 24, 32, 40 px). Pair size with line height and weight as a unit. Keep body line length near 45 to 85 characters.
4. Spacing. Use one base unit (commonly 4 or 8 px) and derive all gaps and padding from it.
5. Color. Build neutral ramps plus a small number of accent ramps. Verify each text/background pair (see Verification).
6. Components. Implement all states: default, hover, focus-visible, active, disabled, error, loading, empty. Focus indicators must be visible and not removed.
7. Responsive. Adjust layout at a few breakpoints chosen from content, not device names. Test at narrow, medium, and wide widths, plus 200% text zoom.
8. Motion. Keep transitions short and purposeful. Respect the user's reduced-motion preference.
9. Migrate incrementally. Replace hard-coded values screen by screen rather than in one sweeping change.

### Decision gates

- Proceed to tokens only if the source of truth is identified or derived values are accepted by the requester.
- Do not introduce a new color, font, or radius outside the approved set without confirmation.
- Use a new breakpoint only when content breaks at the current set.
- Choose a fixed size only for non-text decoration; text sizes should be relative to user settings where the platform allows.
- Stop and request approval before: changing shared tokens that affect multiple products, deleting or renaming widely used component classes, altering brand assets, modifying production theme configuration, or merging or publishing changes to a shared branch. These are destructive or externally visible and require explicit approval.

### Verification and evidence

Measurable checks, all required before reporting completion:

- Contrast: normal text at least 4.5:1; large text (24 px regular or 18.66 px bold and above) and essential non-text UI boundaries and icons at least 3:1 against adjacent colors, per WCAG 2.2. Report the measured ratios for every changed pair, including dark mode.
- Hard-coded values: zero new raw hex, px, or font-size literals in components where a token exists. Report the count before and after.
- Focus: every interactive element shows a visible focus indicator with at least 3:1 contrast against adjacent colors.
- Layout: no horizontal scrolling at 320 CSS px width; no text clipping at 200% zoom.
- Visual regression: capture before and after screenshots for each changed screen at the chosen breakpoints, and list any intended differences.
- Tooling: run the project's existing linter, type checker, and visual or accessibility checks. Record the commands used. If a tool's current options or versions are uncertain, check its official documentation before relying on them.

Do not claim compliance with any standard or law. Report measured results only.

### Failure handling

- Contrast failure: adjust the semantic token's lightness within its ramp; do not special-case one component unless the exception is documented.
- Token conflicts: if two intents share one value, split the semantic token rather than overloading it.
- Visual regression beyond stated changes: revert the affected selector and isolate the cause.
- Missing design input: produce the derived token set, mark it as provisional, and request confirmation before shipping.

### Deliverable contract

Provide:

1. Changed files and a one-line purpose for each.
2. Token table: primitive, semantic role, value, and light and dark mappings.
3. Verification results: contrast ratios, hard-coded value counts before and after, screenshot comparisons, and commands run with outcomes.
4. Assumptions and open questions.
5. Any actions awaiting approval, listed explicitly, with none executed.

Do not: invent design values, present derived tokens as approved, remove focus styles for appearance, use color alone to convey state, or report unrun checks as passed.

### Ultron routing contract

**Choose this skill when:** the task requires creating, translating, or auditing a consistent visual language: design tokens, typography and spacing scales, color roles, surfaces, responsive composition, component states, contrast, or reduced-motion behavior.

**Choose `css-styling` when:** the visual specification is known and the problem is a concrete stylesheet implementation or browser-specific CSS defect, including cascade, specificity, layout, or responsive rule behavior.

**Handoff contract:** provide semantic tokens, component state definitions, approved breakpoints, reference dimensions, contrast requirements, and acceptance screenshots or measurements. The CSS skill returns implementation evidence and identifies any mismatch that needs a design decision rather than silently changing the visual system.

**Why the boundary exists:** the visual system defines what the interface should communicate; CSS implements that intent in a particular codebase. Mixing the two makes local fixes drift into inconsistent design decisions.


## visual-content-generation

**Use when:** Use when producing, editing, or validating generated images, diagrams, charts, or other visual assets for data and AI work, including dataset illustrations, model-output figures, slide visuals, and synthetic image batches that must meet stated fidelity, labeling, and provenance requirements.

### Purpose and boundaries

This skill covers turning a stated visual need into a verified image, diagram, chart, or synthetic image set. Typical work: figures for technical reports, architecture diagrams, data charts rendered from tabular inputs, illustrative images for model cards, and synthetic image batches for augmentation or evaluation.

In scope: choosing the generation method (code-rendered vector or chart, text-to-image model, image editing, or manual composition), specifying prompts and parameters, checking outputs against requirements, and packaging assets with provenance records.

Out of scope: generating images of real identifiable people without consent, producing content that impersonates real persons or organizations, creating misleading data visualizations, bypassing provider content policies, and making legal claims about image ownership or licensing. Refer those to the appropriate owner.

### Inputs and assumptions

Before starting, establish:

1. **Purpose and audience**: publication, internal review, training data, demo.
2. **Content specification**: exact labels, numbers, entities, relationships, or scene elements. Numbers and labels must come from a source file, never from memory.
3. **Format**: resolution, aspect ratio, file type, color space, transparency, accessibility requirements (alt text, contrast).
4. **Provenance rules**: whether the output must be labeled as synthetic, and the required metadata.
5. **Tooling available**: which generators, editors, or plotting libraries are approved. Confirm their current capabilities and parameter names against official documentation; do not rely on remembered flags.

If any of items 2 through 4 are missing, ask. Do not assume data values or branding.

### Operating workflow

1. **Classify the request.** Data-bound (charts, plots, quantitative diagrams) versus representational (illustrations, scenes, synthetic photos) versus structural (flowcharts, architecture). This determines the method.
2. **Select the method.**
   - Data-bound: render with a plotting or vector tool from the source data. Never ask a generative image model to produce values.
   - Structural: author as diagram source (for example, a text-defined diagram or SVG) so nodes and edges are editable and checkable.
   - Representational: use a generative model, then edit as needed.
3. **Write the specification.** Produce a one-page spec: content list, layout, palette, typography, excluded elements, and the output file name convention.
4. **Generate a first pass.** For generative models, run a small batch (typically 4 or fewer) to explore variance before committing to a parameter set.
5. **Refine.** Change one variable at a time: prompt wording, seed or variation control if available, reference inputs, or crop. Log each change.
6. **Post-process.** Crop, resize, convert color profile, add text overlays in a vector layer rather than inside raster output where possible.
7. **Verify** (see below), then **package** with provenance.

### Decision gates

- **Gate A (method):** If a chart encodes quantities, it must be code-rendered from data. Generative output for quantitative content is rejected.
- **Gate B (text in image):** Generative models frequently misspell or garble text. Any visible text must be added as a vector overlay or verified character-by-character; otherwise use a text-free generation and add labels separately.
- **Gate C (realism):** If the output depicts a real person, real location, or real event, stop and obtain explicit approval and a disclosure plan.
- **Gate D (external use):** Publishing, uploading to a third-party service, or inserting into a shared dataset requires explicit approval from the owner.
- **Gate E (destructive edits):** Overwriting original assets, deleting source files, or replacing an approved figure requires explicit approval. Save new versions alongside originals.

### Verification and evidence

Check each item and record the result:

- **Data fidelity:** Every plotted value matches the source within the stated tolerance (for example, zero difference for displayed labels; recomputed axis ranges match data min and max). Regenerate the chart from the source and diff the exported data where possible.
- **Text accuracy:** Every label string compared against the spec, exact match, including units and capitalization.
- **Dimensions and format:** Pixel dimensions, aspect ratio, color mode, and file format match the requirement. Confirm by reading file metadata, not by visual judgment.
- **Contrast and accessibility:** Text-to-background contrast meets the target standard in the project guide (state the standard used; WCAG AA is a common reference, verify current criteria). Color is not the only encoding for categories.
- **Artifact scan:** At full zoom, check for garbled glyphs, duplicated limbs or objects, hallucinated logos, and stray marks.
- **Provenance record:** A sidecar file stating generator and version, date, prompt or spec hash, seed where available, source data file and its hash, edits applied, and the synthetic-content label.

Attach the verification table to the deliverable.

### Failure handling

- **Garbled text persists after two regenerations:** Remove text from the generated image and overlay it as vector text.
- **Chart values disagree with source:** Discard the figure, locate the transform step causing the mismatch, fix the pipeline, and re-render. Do not hand-edit numbers.
- **Output resembles a real person or protected mark:** Stop, discard the output from shared locations, and escalate under Gate C.
- **Tool unavailable or behavior changed:** Report the discrepancy, check current official documentation, and do not substitute undocumented parameters.
- **Repeated quality failure after reasonable iteration (about five substantive attempts):** Stop and report the blocker with evidence rather than continuing to vary prompts.

### Deliverable contract

Return:

1. The final asset(s) in the requested format and location.
2. A source file for each asset (plotting script, diagram source, or editable layer file) sufficient to regenerate it.
3. The provenance sidecar and verification table.
4. A short statement of method, known limitations, and any gate decisions requiring sign-off.

Do not deliver assets with unverified numbers, unlabeled synthetic imagery where labeling is required, or unresolved gate items.


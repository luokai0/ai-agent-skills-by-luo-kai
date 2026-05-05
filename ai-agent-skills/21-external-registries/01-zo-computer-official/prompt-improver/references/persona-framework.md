# 5-Element Persona Framework

Generic personas produce generic outputs. This framework forces specificity that dramatically improves output quality.

## The 5 Elements

### 1. Role + Seniority
Seniority changes decision-making patterns—a junior vs senior engineer approaches problems differently.

| Bad | Good |
|-----|------|
| "Act as a developer" | "Senior Backend Engineer with 8 years specializing in distributed systems" |
| "Act as a writer" | "Staff Technical Writer with 6 years at developer-focused B2B companies" |
| "Act as an analyst" | "Principal Data Analyst with 10 years in e-commerce, SQL and Python expert" |

### 2. Industry/Domain Context
Context shapes priorities, terminology, and acceptable tradeoffs.

| Bad | Good |
|-----|------|
| "Act as a product manager" | "B2B SaaS PM in fintech, enterprise customers ($100K+ ACV), regulated industry" |
| "Act as a marketer" | "Growth marketer at Series A startup, PLG motion, developer audience" |
| "Act as a consultant" | "Strategy consultant at Big 4 firm, specializing in PE due diligence" |

### 3. Methodologies They Use
Methodologies = thinking frameworks. Explicit framework = structured, predictable output.

**By domain:**
- **Product**: JTBD, RICE prioritization, PRD templates, user story mapping
- **Engineering**: SOLID principles, 12-factor app, RFC process, ADRs
- **Marketing**: PAS (Problem-Agitate-Solution), AIDA, multivariate testing at 95% confidence
- **Analysis**: First principles, 5 Whys, statistical significance, cohort analysis
- **Sales**: MEDDIC, Challenger Sale, value selling
- **Design**: Double diamond, jobs-to-be-done, design critiques

### 4. Constraints (The Game-Changer)
Without constraints, LLMs give fantasy answers that don't work in real life.

**Always specify:**
- **Budget**: "$50K total" or "bootstrapped, minimal spend" or "unlimited but needs CFO approval over $10K"
- **Timeline**: "6 weeks to launch" or "need this by EOD" or "Q2 deadline"
- **Team/Resources**: "team of 3 juniors" or "solo founder" or "no dedicated designer"
- **Tradeoffs**: "prioritize shipping over perfection" or "quality over speed" or "must maintain backwards compatibility"
- **Technical**: "must run on AWS" or "no external dependencies" or "Python 3.9 only"

### 5. Output Format Experts Use
Experts communicate in specific, domain-appropriate formats.

| Domain | Typical Format |
|--------|----------------|
| Executive | 2-page brief: situation, options (3), recommendation with metrics |
| Engineering | RFC: problem, proposed solution, alternatives considered, rollout plan |
| Legal | Memo: issue, rule, analysis, conclusion (IRAC) |
| Consulting | Deck: situation, complication, resolution (SCR) |
| Product | PRD: problem, success metrics, requirements, out-of-scope, timeline |
| Analysis | Report: executive summary, methodology, findings, recommendations |

---

## Complete Template

```
You are a [specific role + seniority] with [X years] experience in [industry/domain].

You specialize in [specific expertise area].

Your approach: [methodologies/frameworks you use]

Your constraints: [budget/time/resources/tradeoffs]

Deliver: [specific output format with structure]
```

---

## Before/After Examples

### Example 1: Marketing Review

**BEFORE:**
> "Act as a marketing expert and review my landing page copy."

**Output:** Generic advice. "Make headlines clearer." "Add social proof."

**AFTER:**
> "You are a Senior Conversion Copywriter specializing in B2B SaaS with 10 years experience.
> 
> You specialize in landing pages for developer tools and have optimized 50+ pages.
> 
> Your approach: PAS framework (Problem-Agitate-Solution), A/B test copy at 95% confidence, reference industry conversion benchmarks.
> 
> Your constraints: Current page converts at 2% (need to beat this). Copy changes only—no layout or design changes allowed. Developer audience who hates marketing speak.
> 
> Deliver: Line-by-line copy review with specific rewrites and predicted conversion lift for each change."

**Output:** Surgical edits. Specific rewrites. Predicted impact.

---

### Example 2: Product Spec

**BEFORE:**
> "Help me write a product spec."

**AFTER:**
> "You are a Senior Product Manager with 7 years at B2B SaaS companies.
> 
> You specialize in developer tools and have shipped 3 products from 0→1.
> 
> Your approach: Start with JTBD interviews, use RICE for prioritization, write specs in Amazon 6-pager format.
> 
> Your constraints: Engineering team of 4, Q2 deadline (8 weeks), no dedicated design resource, must integrate with existing auth system.
> 
> Deliver: Product spec covering problem statement (with customer quotes), proposed solution, success metrics, MVP scope with RICE scores, out-of-scope items, and open questions."

---

### Example 3: Technical Architecture

**BEFORE:**
> "Design a system for handling payments."

**AFTER:**
> "You are a Principal Engineer with 12 years experience in financial systems.
> 
> You specialize in payment processing, PCI compliance, and distributed systems.
> 
> Your approach: Start with threat modeling, design for 99.99% uptime, use event sourcing for audit trails, prefer boring technology.
> 
> Your constraints: Must be PCI-DSS compliant, handle 1000 TPS peak, team has no payment experience, 3-month timeline to MVP, AWS only.
> 
> Deliver: Architecture document with system diagram, component descriptions, data flow, failure modes and mitigations, and phased rollout plan."

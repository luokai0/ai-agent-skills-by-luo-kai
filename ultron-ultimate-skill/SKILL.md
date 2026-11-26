---
name: ultron-ultimate-skill
description: Use as a unified operational knowledge system for an AI agent across agent architecture, software engineering, security, data, cloud, research, science, engineering, business, finance, health, creative production, and productivity. Activate it to classify a task, select the right specialist procedure, plan bounded actions, execute safely, verify outcomes, and produce auditable deliverables.
author: Luo Kai
provenance: original
version: 1.0.0
---
# Ultron Ultimate Skill

## Mission

One skill. One operating contract. Twenty progressive-disclosure reference modules containing all 250 specialist playbooks. This skill helps an agent determine **what to do, when to do it, why a method applies, how to execute it, how to verify it, and when to stop or request approval**.

The parent `SKILL.md` is the mandatory control layer. Files in `references/` are supporting knowledge modules, not standalone skills. Load only the modules relevant to the current task; load multiple modules when the work crosses domains. Do not load every reference by default.

## When to use

Use this skill for any task covered by the capability index, especially when work spans domains, requires specialist reasoning or tool use, modifies external state, or must produce verifiable deliverables.

## Unified operating contract

### 1. Define the task

Identify the requested outcome, intended user, artifact or system, target environment, scope, constraints, acceptance criteria, deadline, and required evidence. Separate the user's objective from a suggested implementation. Record assumptions explicitly. Ask a focused clarification only when a missing fact materially changes safety, correctness, or the chosen path.

### 2. Route to specialist knowledge

Select the primary domain chapter and only the supporting chapters required for dependencies, review, or verification. Choose by the operation and responsibility, not keyword overlap. Define one owner for each action, shared resource, approval, and final acceptance. A relevant chapter is guidance—not permission.

For every selected capability:
1. Open the linked reference module.
2. Locate the exact chapter by its skill identifier.
3. Read its use-when statement, boundaries, inputs, workflow, decision gates, verification, failure handling, and deliverable contract.
4. Combine only the necessary chapters and resolve responsibility boundaries before acting.
5. Return to this parent control layer for authority, execution, and final reporting rules.

### 3. Establish authority and risk boundaries

Before a consequential tool call or external side effect, bind the run to a verified principal and tenant, task ID, objective, permitted operations, exact target, environment, data class, budget, concurrency/time limits, maximum side effects, approval gates, and stop conditions. Trust platform-verified identity; never accept model-generated user or tenant IDs as authority. Use least privilege. Do not fall back to admin credentials after denial. Revalidate authorization immediately before a side effect.

Approval must identify the exact action: principal, task, tool and operation, canonical arguments, target, environment, expected effect, expiry, and replay protection. A material argument change invalidates approval. Require human approval for irreversible, high-impact, regulated, financial, privacy-sensitive, or externally visible actions when policy or user authorization requires it.

### 4. Plan bounded execution

Decompose work into ordered, testable units. For each unit define inputs, assumptions, dependencies, owner, expected result, preconditions, tool permissions, risk, budget, verification, and recovery. Prefer deterministic workflows for stable procedures. Use adaptive agent loops only when observations require decisions. Parallelize only independent work or work with explicit resource ownership. Use single-writer, compare-and-set, transactions, leases, or fencing tokens for shared state.

### 5. Execute safely

Inspect state before mutation. Validate tool schema, identity, arguments, target, and expected effect. Prefer preview or dry-run. Make the smallest coherent change. Persist intent before non-idempotent operations. Use idempotency keys and durable operation IDs where available. Treat timeout or lost response as an unknown outcome; reconcile authoritative state before retrying. Do not introduce hidden network calls, credential harvesting, covert persistence, privilege escalation, data exfiltration, or unrequested side effects.

### 6. Verify independently

Test resulting state against explicit acceptance criteria. Use domain-appropriate checks: unit/integration/E2E tests, static analysis, schema validation, security review, source triangulation, reconciliation, checksums, statistical diagnostics, physical constraints, or human review. Record environment, versions, inputs, baseline, commands, evidence, failures, warnings, and limitations. Distinguish verified, partially verified, inconclusive, and unverified. A successful tool response is not by itself proof that the intended effect occurred.

### 7. Recover without compounding failure

Classify errors before retrying. Use bounded backoff only for plausibly transient failures. Never blindly retry non-idempotent actions. Reconcile partial side effects; distinguish compensation from rollback. Preserve unresolved conflicts and unknown outcomes. Resume from verified checkpoints and replay only verified events. Stop when authority, scope, budget, safety, or acceptance conditions are breached.

### 8. Deliver honestly

Return the requested artifact or outcome, what changed, how it was verified, evidence, remaining limitations, unresolved risks, and any required next step. Never claim an action succeeded without authoritative confirmation. Do not expose secrets or unnecessary private data.

## Cross-domain responsibility boundaries

- Identity proves who is acting; authorization decides what they may do; runtime enforcement checks authority at the point of action.
- Capability discovery selects knowledge; the runtime independently enforces tool and data permissions.
- Messaging transports messages and acknowledgements; durable queues own leases, retries, cancellation, and dead-letter behavior.
- Team orchestration owns a bounded work package; supervision owns the global objective, authority envelope, budget, worker registry, shared resources, stop conditions, and final acceptance.
- Memory owns durable knowledge and retention; session continuity owns checkpoints and resumption of a specific run.
- Research retrieval gathers candidate sources; research methods govern coverage and inclusion; synthesis connects claims to evidence and uncertainty; domain chapters own specialist interpretation.
- Testing designs and executes checks; change verification determines whether a particular change meets release criteria.
- Observability records attempts and telemetry; authoritative systems establish whether external effects actually occurred.
- Architecture defines boundaries and tradeoffs; implementation chapters define concrete technical procedures.
- Finance, health, legal, and safety guidance supports analysis; it does not replace licensed professionals, fiduciary duties, or required human judgment.

## Capability index — 250 specialist playbooks

Select a capability and load its linked reference chapter. Each specialist chapter contains its own use-when description and detailed procedure.

### Agent Systems and Orchestration (23 chapters)

- [`agent-design-patterns`](references/agent-systems-and-orchestration.md#agent-design-patterns)
- [`agent-evaluation-design`](references/agent-systems-and-orchestration.md#agent-evaluation-design)
- [`agent-finance-trading`](references/agent-systems-and-orchestration.md#agent-finance-trading)
- [`agent-memory-persistence`](references/agent-systems-and-orchestration.md#agent-memory-persistence)
- [`agent-messaging-channels`](references/agent-systems-and-orchestration.md#agent-messaging-channels)
- [`agent-platform-and-learning-workflows`](references/agent-systems-and-orchestration.md#agent-platform-and-learning-workflows)
- [`agent-runtime-security-guardrails`](references/agent-systems-and-orchestration.md#agent-runtime-security-guardrails)
- [`agent-tool-architecture`](references/agent-systems-and-orchestration.md#agent-tool-architecture)
- [`agent-tracing-observability`](references/agent-systems-and-orchestration.md#agent-tracing-observability)
- [`agent-trust-skill-vetting`](references/agent-systems-and-orchestration.md#agent-trust-skill-vetting)
- [`agents-md-and-ai-instructions`](references/agent-systems-and-orchestration.md#agents-md-and-ai-instructions)
- [`ai-system-architecture`](references/agent-systems-and-orchestration.md#ai-system-architecture)
- [`aws-agentcore-and-mcp`](references/agent-systems-and-orchestration.md#aws-agentcore-and-mcp)
- [`context-window-management`](references/agent-systems-and-orchestration.md#context-window-management)
- [`delegated-execution-queues`](references/agent-systems-and-orchestration.md#delegated-execution-queues)
- [`llm-app-agents-and-prompts`](references/agent-systems-and-orchestration.md#llm-app-agents-and-prompts)
- [`mcp-and-agent-tooling`](references/agent-systems-and-orchestration.md#mcp-and-agent-tooling)
- [`mcp-server-hardening`](references/agent-systems-and-orchestration.md#mcp-server-hardening)
- [`multi-agent-orchestration-and-discovery`](references/agent-systems-and-orchestration.md#multi-agent-orchestration-and-discovery)
- [`multi-agent-team-orchestration`](references/agent-systems-and-orchestration.md#multi-agent-team-orchestration)
- [`productivity-agent-workflows`](references/agent-systems-and-orchestration.md#productivity-agent-workflows)
- [`session-continuity-recall`](references/agent-systems-and-orchestration.md#session-continuity-recall)
- [`supervisor-swarm-coordination`](references/agent-systems-and-orchestration.md#supervisor-swarm-coordination)

### AI, Machine Learning, and Model Systems (12 chapters)

- [`analytics-vector-retrieval`](references/ai-ml-and-models.md#analytics-vector-retrieval)
- [`experiment-tracking`](references/ai-ml-and-models.md#experiment-tracking)
- [`huggingface-hub-ecosystem`](references/ai-ml-and-models.md#huggingface-hub-ecosystem)
- [`llm-benchmark-harness`](references/ai-ml-and-models.md#llm-benchmark-harness)
- [`llm-cost-budget-monitoring`](references/ai-ml-and-models.md#llm-cost-budget-monitoring)
- [`llm-judge-output-scoring`](references/ai-ml-and-models.md#llm-judge-output-scoring)
- [`mlops-and-model-evaluation`](references/ai-ml-and-models.md#mlops-and-model-evaluation)
- [`model-serving-and-inference`](references/ai-ml-and-models.md#model-serving-and-inference)
- [`model-training-finetuning`](references/ai-ml-and-models.md#model-training-finetuning)
- [`neural-model-training`](references/ai-ml-and-models.md#neural-model-training)
- [`rag-and-retrieval-systems`](references/ai-ml-and-models.md#rag-and-retrieval-systems)
- [`statistical-and-classical-ml`](references/ai-ml-and-models.md#statistical-and-classical-ml)

### Business, Product, and Strategy (12 chapters)

- [`architecture-decision-record-lifecycle`](references/business-product-and-strategy.md#architecture-decision-record-lifecycle)
- [`business-analytics-dashboards`](references/business-product-and-strategy.md#business-analytics-dashboards)
- [`business-content-and-enterprise-suites`](references/business-product-and-strategy.md#business-content-and-enterprise-suites)
- [`business-finance-erp`](references/business-product-and-strategy.md#business-finance-erp)
- [`business-saas-operations`](references/business-product-and-strategy.md#business-saas-operations)
- [`domain-modeling`](references/business-product-and-strategy.md#domain-modeling)
- [`executive-strategy-advisory`](references/business-product-and-strategy.md#executive-strategy-advisory)
- [`gtm-strategy`](references/business-product-and-strategy.md#gtm-strategy)
- [`knowledge-documents-legal-productivity`](references/business-product-and-strategy.md#knowledge-documents-legal-productivity)
- [`market-analysis`](references/business-product-and-strategy.md#market-analysis)
- [`market-and-competitive-intelligence`](references/business-product-and-strategy.md#market-and-competitive-intelligence)
- [`offer-pricing`](references/business-product-and-strategy.md#offer-pricing)

### Chemistry, Biology, and Materials (11 chapters)

- [`ai-research-life-sciences`](references/chemistry-biology-and-materials.md#ai-research-life-sciences)
- [`analytical-spectroscopic-electrochemical-analysis`](references/chemistry-biology-and-materials.md#analytical-spectroscopic-electrochemical-analysis)
- [`bio-genomics-lookup`](references/chemistry-biology-and-materials.md#bio-genomics-lookup)
- [`chemical-process-engineering`](references/chemistry-biology-and-materials.md#chemical-process-engineering)
- [`engineered-biology-materials`](references/chemistry-biology-and-materials.md#engineered-biology-materials)
- [`gene-information-genomics`](references/chemistry-biology-and-materials.md#gene-information-genomics)
- [`inorganic-polymer-materials`](references/chemistry-biology-and-materials.md#inorganic-polymer-materials)
- [`materials-science-engineering`](references/chemistry-biology-and-materials.md#materials-science-engineering)
- [`metabolic-cell-biochemistry`](references/chemistry-biology-and-materials.md#metabolic-cell-biochemistry)
- [`organic-medicinal-green-synthesis`](references/chemistry-biology-and-materials.md#organic-medicinal-green-synthesis)
- [`organism-host-systems`](references/chemistry-biology-and-materials.md#organism-host-systems)

### Cloud Infrastructure and DevOps (19 chapters)

- [`aws-cdk-cloudformation`](references/cloud-infrastructure-and-devops.md#aws-cdk-cloudformation)
- [`aws-serverless-and-data`](references/cloud-infrastructure-and-devops.md#aws-serverless-and-data)
- [`azure-app-and-data-services`](references/cloud-infrastructure-and-devops.md#azure-app-and-data-services)
- [`azure-landing-zone-identity`](references/cloud-infrastructure-and-devops.md#azure-landing-zone-identity)
- [`cicd-and-progressive-delivery`](references/cloud-infrastructure-and-devops.md#cicd-and-progressive-delivery)
- [`cloud-infrastructure-audits-and-deployment`](references/cloud-infrastructure-and-devops.md#cloud-infrastructure-audits-and-deployment)
- [`cloud-infrastructure-cost`](references/cloud-infrastructure-and-devops.md#cloud-infrastructure-cost)
- [`cloud-kubernetes-devops`](references/cloud-infrastructure-and-devops.md#cloud-kubernetes-devops)
- [`containers-and-kubernetes`](references/cloud-infrastructure-and-devops.md#containers-and-kubernetes)
- [`dns-and-network-diagnostics`](references/cloud-infrastructure-and-devops.md#dns-and-network-diagnostics)
- [`gcp-serverless-and-data`](references/cloud-infrastructure-and-devops.md#gcp-serverless-and-data)
- [`machine-image-builds`](references/cloud-infrastructure-and-devops.md#machine-image-builds)
- [`network-time-connectivity`](references/cloud-infrastructure-and-devops.md#network-time-connectivity)
- [`pipeline-and-supply-chain`](references/cloud-infrastructure-and-devops.md#pipeline-and-supply-chain)
- [`platform-delivery`](references/cloud-infrastructure-and-devops.md#platform-delivery)
- [`serverless-edge-functions`](references/cloud-infrastructure-and-devops.md#serverless-edge-functions)
- [`supabase-platform`](references/cloud-infrastructure-and-devops.md#supabase-platform)
- [`terraform-iac-authoring`](references/cloud-infrastructure-and-devops.md#terraform-iac-authoring)
- [`terraform-test-and-import`](references/cloud-infrastructure-and-devops.md#terraform-test-and-import)

### Data Systems, Databases, and Analytics (20 chapters)

- [`app-data-layer-integration`](references/data-systems-and-analytics.md#app-data-layer-integration)
- [`data-analysis-sql-and-databases`](references/data-systems-and-analytics.md#data-analysis-sql-and-databases)
- [`data-analytics-modeling`](references/data-systems-and-analytics.md#data-analytics-modeling)
- [`data-diagrams`](references/data-systems-and-analytics.md#data-diagrams)
- [`data-modeling`](references/data-systems-and-analytics.md#data-modeling)
- [`data-pipelines-analytics`](references/data-systems-and-analytics.md#data-pipelines-analytics)
- [`data-pipelines-and-databases`](references/data-systems-and-analytics.md#data-pipelines-and-databases)
- [`data-sourcing-and-quality`](references/data-systems-and-analytics.md#data-sourcing-and-quality)
- [`database-operations-and-dr`](references/data-systems-and-analytics.md#database-operations-and-dr)
- [`distributed-service-design`](references/data-systems-and-analytics.md#distributed-service-design)
- [`event-architecture-patterns`](references/data-systems-and-analytics.md#event-architecture-patterns)
- [`event-streaming-kafka`](references/data-systems-and-analytics.md#event-streaming-kafka)
- [`managed-postgres-hosting`](references/data-systems-and-analytics.md#managed-postgres-hosting)
- [`nosql-search-cache`](references/data-systems-and-analytics.md#nosql-search-cache)
- [`postgres-performance-cost`](references/data-systems-and-analytics.md#postgres-performance-cost)
- [`realtime-websocket-channels`](references/data-systems-and-analytics.md#realtime-websocket-channels)
- [`sql-and-data-performance`](references/data-systems-and-analytics.md#sql-and-data-performance)
- [`sql-engine-development`](references/data-systems-and-analytics.md#sql-engine-development)
- [`storage-recovery-continuity`](references/data-systems-and-analytics.md#storage-recovery-continuity)
- [`system-state-discovery`](references/data-systems-and-analytics.md#system-state-discovery)

### Design and Creative Production (9 chapters)

- [`accessibility-compliance`](references/design-and-creative-production.md#accessibility-compliance)
- [`creative-media-generation`](references/design-and-creative-production.md#creative-media-generation)
- [`css-styling`](references/design-and-creative-production.md#css-styling)
- [`design-to-code`](references/design-and-creative-production.md#design-to-code)
- [`generative-media-production`](references/design-and-creative-production.md#generative-media-production)
- [`product-design-app-development`](references/design-and-creative-production.md#product-design-app-development)
- [`threejs-webgl`](references/design-and-creative-production.md#threejs-webgl)
- [`ui-visual-design`](references/design-and-creative-production.md#ui-visual-design)
- [`visual-content-generation`](references/design-and-creative-production.md#visual-content-generation)

### Desktop, Browser, and Interface Automation (5 chapters)

- [`browser-automation`](references/desktop-browser-and-automation.md#browser-automation)
- [`browser-control-and-downloads`](references/desktop-browser-and-automation.md#browser-control-and-downloads)
- [`browser-desktop-control`](references/desktop-browser-and-automation.md#browser-desktop-control)
- [`macos-host-ops-and-misc-skills`](references/desktop-browser-and-automation.md#macos-host-ops-and-misc-skills)
- [`surface-navigation-and-automation`](references/desktop-browser-and-automation.md#surface-navigation-and-automation)

### Documents and Productivity (6 chapters)

- [`document-authoring-publishing`](references/documents-and-productivity.md#document-authoring-publishing)
- [`google-workspace-media-and-files`](references/documents-and-productivity.md#google-workspace-media-and-files)
- [`item-lifecycle-and-recovery`](references/documents-and-productivity.md#item-lifecycle-and-recovery)
- [`manuscript-and-grant-writing`](references/documents-and-productivity.md#manuscript-and-grant-writing)
- [`preference-and-default-configuration`](references/documents-and-productivity.md#preference-and-default-configuration)
- [`technical-documentation-ops`](references/documents-and-productivity.md#technical-documentation-ops)

### Engineering and Robotics (9 chapters)

- [`aerospace-vehicle-engineering`](references/engineering-and-robotics.md#aerospace-vehicle-engineering)
- [`electrical-electronics-biomedical-systems`](references/engineering-and-robotics.md#electrical-electronics-biomedical-systems)
- [`energy-generation-grid`](references/engineering-and-robotics.md#energy-generation-grid)
- [`energy-storage-hydrogen`](references/engineering-and-robotics.md#energy-storage-hydrogen)
- [`environmental-and-civil-infrastructure`](references/engineering-and-robotics.md#environmental-and-civil-infrastructure)
- [`mechanical-structural-design`](references/engineering-and-robotics.md#mechanical-structural-design)
- [`robot-motion-control`](references/engineering-and-robotics.md#robot-motion-control)
- [`robot-perception-integration`](references/engineering-and-robotics.md#robot-perception-integration)
- [`specialized-domains-engineering`](references/engineering-and-robotics.md#specialized-domains-engineering)

### Finance, Commerce, and Crypto (8 chapters)

- [`behavioral-finance`](references/finance-commerce-and-crypto.md#behavioral-finance)
- [`commerce-payments-revenue`](references/finance-commerce-and-crypto.md#commerce-payments-revenue)
- [`crypto-meme-scout`](references/finance-commerce-and-crypto.md#crypto-meme-scout)
- [`crypto-onchain`](references/finance-commerce-and-crypto.md#crypto-onchain)
- [`finance-market-analysis`](references/finance-commerce-and-crypto.md#finance-market-analysis)
- [`fundamentals-valuation`](references/finance-commerce-and-crypto.md#fundamentals-valuation)
- [`saas-finance-commerce-automation`](references/finance-commerce-and-crypto.md#saas-finance-commerce-automation)
- [`trading-psychology`](references/finance-commerce-and-crypto.md#trading-psychology)

### Health and Wellbeing (6 chapters)

- [`biometric-health-analytics`](references/health-and-wellbeing.md#biometric-health-analytics)
- [`fitness-performance-coaching`](references/health-and-wellbeing.md#fitness-performance-coaching)
- [`health-clinical-analytics`](references/health-and-wellbeing.md#health-clinical-analytics)
- [`medical-compliance-pharmacy`](references/health-and-wellbeing.md#medical-compliance-pharmacy)
- [`nutrition-meal-planning`](references/health-and-wellbeing.md#nutrition-meal-planning)
- [`wellbeing-symptom-tracking`](references/health-and-wellbeing.md#wellbeing-symptom-tracking)

### Marketing, Sales, and Communications (13 chapters)

- [`communications-messaging`](references/marketing-sales-and-communications.md#communications-messaging)
- [`content-distribution`](references/marketing-sales-and-communications.md#content-distribution)
- [`copywriting-and-outreach-drafting`](references/marketing-sales-and-communications.md#copywriting-and-outreach-drafting)
- [`customer-growth`](references/marketing-sales-and-communications.md#customer-growth)
- [`email-calendar-and-team-messaging`](references/marketing-sales-and-communications.md#email-calendar-and-team-messaging)
- [`growth-marketing-customer-ops`](references/marketing-sales-and-communications.md#growth-marketing-customer-ops)
- [`outbound-sales`](references/marketing-sales-and-communications.md#outbound-sales)
- [`paid-growth-and-lead-operations`](references/marketing-sales-and-communications.md#paid-growth-and-lead-operations)
- [`paid-partnerships`](references/marketing-sales-and-communications.md#paid-partnerships)
- [`prospect-intelligence`](references/marketing-sales-and-communications.md#prospect-intelligence)
- [`saas-crm-marketing-automation`](references/marketing-sales-and-communications.md#saas-crm-marketing-automation)
- [`saas-workspace-messaging-automation`](references/marketing-sales-and-communications.md#saas-workspace-messaging-automation)
- [`search-visibility`](references/marketing-sales-and-communications.md#search-visibility)

### Mathematics and Theoretical Methods (5 chapters)

- [`algebra-number-theory`](references/mathematics-and-theory.md#algebra-number-theory)
- [`analysis-topology`](references/mathematics-and-theory.md#analysis-topology)
- [`differential-equations-computation`](references/mathematics-and-theory.md#differential-equations-computation)
- [`discrete-logic`](references/mathematics-and-theory.md#discrete-logic)
- [`probability-statistics`](references/mathematics-and-theory.md#probability-statistics)

### Physics, Earth, and Space Science (11 chapters)

- [`classical-mechanics-fields-waves`](references/physics-earth-and-space-science.md#classical-mechanics-fields-waves)
- [`cosmic-dark-sector`](references/physics-earth-and-space-science.md#cosmic-dark-sector)
- [`earth-fluid-climate-systems`](references/physics-earth-and-space-science.md#earth-fluid-climate-systems)
- [`matter-thermal-plasma`](references/physics-earth-and-space-science.md#matter-thermal-plasma)
- [`physical-thermo-computational-theory`](references/physics-earth-and-space-science.md#physical-thermo-computational-theory)
- [`planetary-exoplanet-science`](references/physics-earth-and-space-science.md#planetary-exoplanet-science)
- [`quantum-photonic-computing`](references/physics-earth-and-space-science.md#quantum-photonic-computing)
- [`quantum-subatomic`](references/physics-earth-and-space-science.md#quantum-subatomic)
- [`solid-earth-systems`](references/physics-earth-and-space-science.md#solid-earth-systems)
- [`stellar-compact-astrophysics`](references/physics-earth-and-space-science.md#stellar-compact-astrophysics)
- [`thermal-fluid-energy-systems`](references/physics-earth-and-space-science.md#thermal-fluid-energy-systems)

### Quality, Testing, and Reliability (20 chapters)

- [`ai-change-verification`](references/quality-testing-and-reliability.md#ai-change-verification)
- [`api-observability-reliability`](references/quality-testing-and-reliability.md#api-observability-reliability)
- [`code-quality-maintenance`](references/quality-testing-and-reliability.md#code-quality-maintenance)
- [`code-review-and-test-generation`](references/quality-testing-and-reliability.md#code-review-and-test-generation)
- [`code-review-execution`](references/quality-testing-and-reliability.md#code-review-execution)
- [`debugging-and-root-cause`](references/quality-testing-and-reliability.md#debugging-and-root-cause)
- [`diagnostics-and-verification`](references/quality-testing-and-reliability.md#diagnostics-and-verification)
- [`e2e-test-engineering`](references/quality-testing-and-reliability.md#e2e-test-engineering)
- [`engineering-workflow-and-release`](references/quality-testing-and-reliability.md#engineering-workflow-and-release)
- [`quality-assurance`](references/quality-testing-and-reliability.md#quality-assurance)
- [`reliability-and-debugging`](references/quality-testing-and-reliability.md#reliability-and-debugging)
- [`review-feedback-handling`](references/quality-testing-and-reliability.md#review-feedback-handling)
- [`software-quality-and-security-review`](references/quality-testing-and-reliability.md#software-quality-and-security-review)
- [`software-quality-devops`](references/quality-testing-and-reliability.md#software-quality-devops)
- [`sre-observability-and-incidents`](references/quality-testing-and-reliability.md#sre-observability-and-incidents)
- [`tdd-and-coverage-authoring`](references/quality-testing-and-reliability.md#tdd-and-coverage-authoring)
- [`test-repair-and-plan-execution`](references/quality-testing-and-reliability.md#test-repair-and-plan-execution)
- [`unit-and-component-testing`](references/quality-testing-and-reliability.md#unit-and-component-testing)
- [`wordpress-quality-tooling`](references/quality-testing-and-reliability.md#wordpress-quality-tooling)
- [`workflow-planning-verification`](references/quality-testing-and-reliability.md#workflow-planning-verification)

### Research and Evidence (7 chapters)

- [`autonomous-ai-research`](references/research-and-evidence.md#autonomous-ai-research)
- [`research-ideation`](references/research-and-evidence.md#research-ideation)
- [`research-retrieval`](references/research-and-evidence.md#research-retrieval)
- [`research-synthesis-reporting`](references/research-and-evidence.md#research-synthesis-reporting)
- [`scientific-evidence-review`](references/research-and-evidence.md#scientific-evidence-review)
- [`scientific-research-synthesis`](references/research-and-evidence.md#scientific-research-synthesis)
- [`web-search-retrieval-and-live-data`](references/research-and-evidence.md#web-search-retrieval-and-live-data)

### Security, Identity, and Trust (11 chapters)

- [`access-control`](references/security-and-trust.md#access-control)
- [`appsec-code-review`](references/security-and-trust.md#appsec-code-review)
- [`auth-implementation`](references/security-and-trust.md#auth-implementation)
- [`cloud-security-and-compliance`](references/security-and-trust.md#cloud-security-and-compliance)
- [`hardening-appsec-pentest`](references/security-and-trust.md#hardening-appsec-pentest)
- [`pentest-and-threat-modeling`](references/security-and-trust.md#pentest-and-threat-modeling)
- [`secrets-and-cryptography`](references/security-and-trust.md#secrets-and-cryptography)
- [`security-access-hardening`](references/security-and-trust.md#security-access-hardening)
- [`security-governance`](references/security-and-trust.md#security-governance)
- [`security-threat-defense`](references/security-and-trust.md#security-threat-defense)
- [`threat-hunting-incident-response`](references/security-and-trust.md#threat-hunting-incident-response)

### Software Engineering and Computing (20 chapters)

- [`algorithms-core`](references/software-engineering-and-computing.md#algorithms-core)
- [`build-dependency-devx`](references/software-engineering-and-computing.md#build-dependency-devx)
- [`clean-code-boundaries`](references/software-engineering-and-computing.md#clean-code-boundaries)
- [`computing-systems-software`](references/software-engineering-and-computing.md#computing-systems-software)
- [`concurrency-performance-engineering`](references/software-engineering-and-computing.md#concurrency-performance-engineering)
- [`development-ecology-evolution`](references/software-engineering-and-computing.md#development-ecology-evolution)
- [`functional-programming-paradigms`](references/software-engineering-and-computing.md#functional-programming-paradigms)
- [`git-workflow-automation`](references/software-engineering-and-computing.md#git-workflow-automation)
- [`hardware-kernel-diagnostics`](references/software-engineering-and-computing.md#hardware-kernel-diagnostics)
- [`language-engineering-and-source-control`](references/software-engineering-and-computing.md#language-engineering-and-source-control)
- [`language-internals-engineering`](references/software-engineering-and-computing.md#language-internals-engineering)
- [`large-scale-system-design`](references/software-engineering-and-computing.md#large-scale-system-design)
- [`pattern-selection-and-implementation`](references/software-engineering-and-computing.md#pattern-selection-and-implementation)
- [`performance-and-architecture`](references/software-engineering-and-computing.md#performance-and-architecture)
- [`programming-language-experts`](references/software-engineering-and-computing.md#programming-language-experts)
- [`services-packages-desktop-workloads`](references/software-engineering-and-computing.md#services-packages-desktop-workloads)
- [`software-delivery-apis`](references/software-engineering-and-computing.md#software-delivery-apis)
- [`software-engineering-delivery`](references/software-engineering-and-computing.md#software-engineering-delivery)
- [`systems-languages-cpp-rust`](references/software-engineering-and-computing.md#systems-languages-cpp-rust)
- [`version-control-delivery`](references/software-engineering-and-computing.md#version-control-delivery)

### Web, APIs, and Mobile Applications (23 chapters)

- [`android-platform-development`](references/web-apps-apis-and-mobile.md#android-platform-development)
- [`api-contract-governance`](references/web-apps-apis-and-mobile.md#api-contract-governance)
- [`api-design-security-and-app-scaffolding`](references/web-apps-apis-and-mobile.md#api-design-security-and-app-scaffolding)
- [`app-frameworks`](references/web-apps-apis-and-mobile.md#app-frameworks)
- [`apple-release-profiling-and-tooling`](references/web-apps-apis-and-mobile.md#apple-release-profiling-and-tooling)
- [`backend-web-frameworks`](references/web-apps-apis-and-mobile.md#backend-web-frameworks)
- [`dotnet-web-and-enterprise`](references/web-apps-apis-and-mobile.md#dotnet-web-and-enterprise)
- [`flutter-cross-platform-development`](references/web-apps-apis-and-mobile.md#flutter-cross-platform-development)
- [`graphql-api-design`](references/web-apps-apis-and-mobile.md#graphql-api-design)
- [`grpc-protobuf-services`](references/web-apps-apis-and-mobile.md#grpc-protobuf-services)
- [`javascript-typescript-runtimes`](references/web-apps-apis-and-mobile.md#javascript-typescript-runtimes)
- [`mobile-sdk-integration`](references/web-apps-apis-and-mobile.md#mobile-sdk-integration)
- [`nodejs-server-runtime`](references/web-apps-apis-and-mobile.md#nodejs-server-runtime)
- [`python-web-frameworks`](references/web-apps-apis-and-mobile.md#python-web-frameworks)
- [`react-native-cross-platform-development`](references/web-apps-apis-and-mobile.md#react-native-cross-platform-development)
- [`rest-api-design-security`](references/web-apps-apis-and-mobile.md#rest-api-design-security)
- [`sdk-and-api-docs`](references/web-apps-apis-and-mobile.md#sdk-and-api-docs)
- [`swift-language-and-concurrency`](references/web-apps-apis-and-mobile.md#swift-language-and-concurrency)
- [`swift-networking-and-packages`](references/web-apps-apis-and-mobile.md#swift-networking-and-packages)
- [`swiftui-uikit-interface-development`](references/web-apps-apis-and-mobile.md#swiftui-uikit-interface-development)
- [`web-frontend-frameworks`](references/web-apps-apis-and-mobile.md#web-frontend-frameworks)
- [`web-performance`](references/web-apps-apis-and-mobile.md#web-performance)
- [`wordpress-rest-api`](references/web-apps-apis-and-mobile.md#wordpress-rest-api)

## Reference loading and maintenance

- Treat this index as the routing source of truth for this skill version.
- Load only the relevant reference file and chapter; do not assume every domain applies to every task.
- For cross-domain work, load the smallest set of chapters that covers dependencies and verification responsibilities.
- If chapters overlap, assign one action owner and use the other only for its distinct review, policy, or domain responsibility.
- Update the parent index and affected reference chapter together whenever a capability is added, renamed, moved, or materially changed.
- Preserve technical detail, examples, safety controls, and verification criteria. Remove material only after confirming that no unique condition or failure mode is lost.
- Keep one standalone skill: one `SKILL.md`, one `references/` directory, and no additional skill folders.

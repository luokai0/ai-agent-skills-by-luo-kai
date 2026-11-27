# Ultron Ultimate Skill

**One integrated AI-agent skill by Luo Kai, consolidating 250 specialist playbooks into a single installable capability.**

This branch contains exactly one skill directory: [`ultron-ultimate-skill/`](ultron-ultimate-skill/), with one entry point at [`ultron-ultimate-skill/SKILL.md`](ultron-ultimate-skill/SKILL.md). The 28 focused domain modules and one capability index are supporting reference resources—not standalone skills. The former 250 skill directories are not present.

## Package contents

- **1 skill** — `ultron-ultimate-skill`
- **1 entry point** — 112-line `SKILL.md` with the shared operating contract
- **28 focused domain reference modules** — specialist playbooks loaded on demand
- **1 capability index** — 250 chapter names, routing links, and use-when descriptions
- **250 specialist chapters** — their full operational bodies preserved in the reference modules

The package follows the Agent Skills progressive-disclosure structure: activate one skill, select a capability from the index, and load only the reference module and chapter needed for the task. The entry point stays concise while the complete specialist knowledge remains available.

## Capability ownership

The reference chapters use explicit ownership boundaries instead of duplicating entire workflows. Workflow planning owns process logic, dependency meaning, and end-to-end postconditions; delegated execution queues own durable dispatch, worker claims and leases, retries, cancellation, dead-letter handling, and runtime recovery. The workflow owner defines what a delegated result must prove, while the queue owner records and enforces its execution lifecycle. A queue terminal state is not equivalent to workflow acceptance.

## Domain coverage

1. **Agent Architecture and Platform Design** — 7 chapters
2. **Agent Evaluation and Observability** — 2 chapters
3. **Agent Orchestration and Continuity** — 8 chapters
4. **Agent Runtime Security and MCP** — 5 chapters
5. **AI, Machine Learning, and Model Systems** — 12 chapters
6. **API and Backend Development** — 11 chapters
7. **Business, Product, and Strategy** — 12 chapters
8. **Chemistry, Biology, and Materials** — 11 chapters
9. **Cloud Infrastructure and Operations** — 12 chapters
10. **Cloud Platforms and Services** — 7 chapters
11. **Code Quality and Review** — 8 chapters
12. **Data Engineering and Analytics** — 8 chapters
13. **Databases and Distributed Systems** — 12 chapters
14. **Design and Creative Production** — 9 chapters
15. **Desktop, Browser, and Interface Automation** — 5 chapters
16. **Documents and Productivity** — 6 chapters
17. **Engineering and Robotics** — 9 chapters
18. **Finance, Commerce, and Crypto** — 9 chapters
19. **Frontend and Mobile Development** — 12 chapters
20. **Health and Wellbeing** — 6 chapters
21. **Marketing, Sales, and Communications** — 13 chapters
22. **Mathematics and Theoretical Methods** — 5 chapters
23. **Physics, Earth, and Space Science** — 11 chapters
24. **Programming Languages and Delivery** — 10 chapters
25. **Research and Evidence** — 7 chapters
26. **Security, Identity, and Trust** — 11 chapters
27. **Software Architecture and Systems** — 10 chapters
28. **Testing and Operational Reliability** — 12 chapters

## How to use

1. Open [`ultron-ultimate-skill/SKILL.md`](ultron-ultimate-skill/SKILL.md).
2. Open its [capability index](ultron-ultimate-skill/references/capability-index.md).
3. Select the relevant capability and load the linked domain reference chapter.
4. Follow the parent skill's authority, planning, execution, verification, recovery, and delivery contract.
5. For cross-domain work, load only the additional chapters required and define clear ownership boundaries.

## Repository layout

```text
README.md
ultron-ultimate-skill/
  SKILL.md
  references/
    capability-index.md
    28 domain reference modules
```

## Design principles

- Preserve unique specialist procedures, examples, safeguards, and failure modes.
- Use one routing and execution contract across all domains.
- Keep capability selection separate from authorization.
- Verify outcomes against authoritative evidence.
- Load specialist knowledge on demand instead of loading the entire corpus into every run.
- Keep one standalone skill; supporting reference files are part of that skill package.

## Ownership

Original instructional synthesis and skill architecture are authored by Luo Kai. Third-party product, platform, standard, and technology names are used descriptively; their respective owners retain their rights. No third-party ownership is claimed.

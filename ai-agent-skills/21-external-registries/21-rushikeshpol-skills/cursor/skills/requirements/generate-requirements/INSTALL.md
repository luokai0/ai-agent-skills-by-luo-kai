# Installing the generate-requirements Skill

## File Structure

```
generate-requirements/
├── SKILL.md                     ← Entry point (skill description + intake)
├── workflows/
│   ├── 01-synthesize.md         ← Workflow 1: Context synthesis
│   ├── 02-generate.md           ← Workflow 2: Document generation
│   ├── 02b-quality-gate.md      ← Deduplication + inline quality checks
│   └── 03-validate.md           ← Workflow 3: Validation
├── templates/
│   ├── context-summary.md        ← Internal artifact template
│   └── feature-requirements.md   ← Feature Requirements output template
└── archive/
    ├── api-contract.md           ← (archived — API contracts use /rest-api-contract-generator)
    ├── system-flow.md            ← (archived — system flows use a separate skill)
    └── project-context.md        ← (archived — project context uses /project-context)
```

---

## How to Install

Copy the `generate-requirements/` folder (excluding this INSTALL.md) to your Cowork skills directory:

```bash
cp -r _skills/generate-requirements ~/.skills/skills/
```

Or in the Cowork app: use the **Plugin/Skill Manager** to install from a folder.

Once installed, the skill appears as `generate-requirements` in your skill list.

---

## How to Use

In any Cowork session, say:

```
/generate-requirements
```

Or:

```
Generate requirements for [feature name]
```

The skill will:
1. Scan your workspace for PRDs, Swagger files, designs
2. Ask a few intake questions (feature name, mode, inputs)
3. Run Workflow 1 → 2 → 3 automatically, waiting for your approval at each step
4. Save all outputs to the output folder you specify during intake

---

## What Gets Saved

After running, your workspace will contain:

```
[output-folder]/
├── Context-Summary-[Feature].md                        ← Internal analysis (not for sharing)
├── Generated/
│   ├── Internal/
│   │   └── Feature-Requirements-[Feature].md           ← Requirements document
│   └── Report/
│       └── Validation-Report-[Feature].md              ← Quality gate report
```

---

## Tips

- **Quick Mode:** For MVPs and small features. Lightweight analysis (3 contexts).
- **Comprehensive Mode:** For production features with complex interactions, compliance concerns, or integrations. Full analysis (6 contexts).
- **API Contracts and System Flows** are generated separately after requirements are finalized, using `rest-api-contract-generator`.
- **Resume:** If you have an existing Context Summary, you can start from Workflow 2 directly.
- **Design files:** Provide Figma URLs or upload images — analyzed automatically in Workflow 1.
- **Swagger:** Upload your existing OpenAPI spec — patterns extracted and applied to API Contract.

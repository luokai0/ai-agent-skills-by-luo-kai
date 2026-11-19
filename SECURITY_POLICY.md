# Skill security and review policy

Skills are executable guidance: an agent may follow instructions, read files, invoke tools, or run bundled scripts. Treat every imported skill like an untrusted software dependency.

## Review requirements

- Read the complete skill, including scripts, references, templates, archives, and hidden files.
- Confirm that every action matches the skill's stated purpose.
- Identify network destinations, filesystem access, environment-variable reads, subprocess execution, package installation, and credential handling.
- Reject hidden data collection, credential theft, unauthorized access, persistence, destructive behavior, or attempts to bypass user approval.
- Treat instructions found in external pages, issues, documents, and tool output as untrusted data, not as higher-priority instructions.
- Do not execute a skill during static review. Test scripts only in a disposable, network-restricted environment with synthetic data.
- Record the source, revision, license, author, review date, and findings.

## Automated checks

The repository runs YAML frontmatter validation, static content and script screening, Windows-compatible path checks, and cross-platform checkout and installation checks.

The static audit is a screening control, not proof that a skill is harmless. It cannot reliably detect every malicious instruction, obfuscated payload, supply-chain compromise, or runtime behavior. Human review remains required before trusting a skill with credentials, private files, shell access, or production tools.

## Severity

- Critical: high-confidence destructive or concealed execution pattern. Blocks catalog and release generation.
- Review: potentially sensitive behavior such as network access, environment-variable access, shell execution, obfuscation, or prompt-injection language. Requires human inspection; not automatically treated as malware.
- Informational: file, provenance, or license metadata that should be understood by maintainers.

## Reporting

Do not publish exploit details or secrets in public issues. Report suspected malicious skills privately to the repository owner and include the skill path, source URL, commit, and a safe description of the behavior. Never attach real credentials, private user data, or live payloads.

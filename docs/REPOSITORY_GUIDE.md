# Repository guide

This repository is organized around four areas: the skill library, maintainer tooling, GitHub automation, and the public catalog.

## Layout

- .github/SECURITY.md: GitHub security reporting policy.
- .github/workflows/: CI, catalog generation, and GitHub Pages deployment.
- ai-agent-skills/: canonical skill collections and imported source snapshots.
- docs/REPOSITORY_GUIDE.md: this guide.
- scripts/installer/: optional source-ingestion installer.
- scripts/maintenance/: validation, static security screening, and catalog-generation tools.
- index.html: GitHub Pages application.
- skills-index.json: generated public catalog consumed by index.html.
- install_all_skills.py: backward-compatible installer launcher.
- SOURCES.md: upstream source and license register.
- THIRD_PARTY_NOTICES.md: third-party rights and attribution rules.
- README.md: project overview and user guide.

## Maintainer commands

Run these from the repository root:

- Install validator dependency: python -m pip install PyYAML
- Validate skill metadata: python scripts/maintenance/check_skill_frontmatter.py
- Run static screening: python scripts/maintenance/audit_skill_security.py --root . --report audit-report.json
- Check Windows paths: python scripts/maintenance/check_windows_paths.py
- Build catalog and ZIP: python scripts/maintenance/build_skill_catalog.py

The catalog builder resolves the repository root from its own location, so it can be invoked from any working directory. It writes skills-index.json and skills-bundle.zip at the repository root.

The optional source-ingestion installer is located at scripts/installer/install_all_skills.py. The historical root command remains available: python install_all_skills.py.

The installer clones configured public source repositories and pushes changes to the configured Luo Kai repository. It requires GITHUB_TOKEN for the push. Credentials are passed to Git for that process only and are not written into the remote URL or .git/config. Review the configured source list and resulting changes before using it.

## Automation

- cross-platform.yml validates skill metadata and paths on Ubuntu and Windows, performs static screening, checks installer syntax, and tests a Skills CLI install.
- update-skills.yml validates metadata, runs static screening, scans the skill tree with ClamAV, builds the catalog and release bundle, and updates the generated index on main.
- deploy-pages.yml publishes only index.html, skills-index.json, and .nojekyll to GitHub Pages.

## Generated files

skills-index.json is a committed, generated input for the public site. skills-bundle.zip and audit-report.json are build artifacts and should not be committed. The .gitignore rules keep these local outputs out of ordinary commits.

## Change boundaries

- Keep ai-agent-skills/ as the canonical source tree for skill content.
- Keep the public site entry point and its generated JSON at the repository root because GitHub Pages serves them directly.
- Put new maintainer scripts under scripts/maintenance/ and source-ingestion tooling under scripts/installer/.
- Put CI and deployment definitions under .github/workflows/.
- Preserve source-specific licenses and notices. A collection directory name does not establish authorship or grant rights over imported content.

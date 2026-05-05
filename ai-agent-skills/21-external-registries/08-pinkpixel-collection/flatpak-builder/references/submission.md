# Flathub Submission & Maintenance Reference

---

## Pre-Submission Checklist

Before opening a PR, verify all of these:

- [ ] App ID is in correct reverse-DNS format
- [ ] App ID matches across: manifest, MetaInfo `<id>`, desktop filename, icon filename
- [ ] MetaInfo file passes `appstreamcli validate` with zero errors or warnings
- [ ] Desktop file passes `desktop-file-validate`
- [ ] Icons installed at correct paths with correct names (= App ID)
- [ ] At least 128x128 icon provided
- [ ] At least one screenshot in MetaInfo
- [ ] `<content_rating type="oars-1.1">` present
- [ ] `<releases>` with at least one entry
- [ ] License files installed to `/app/share/licenses/$APP_ID/`
- [ ] App builds locally with `flatpak run --command=flathub-build org.flatpak.Builder --install manifest.yaml`
- [ ] App runs correctly with `flatpak run $APP_ID`
- [ ] Linter passes: `flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest manifest.yaml`
- [ ] Repo linter passes: `flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo repo`
- [ ] No network calls during build
- [ ] All sources have correct SHA256 checksums
- [ ] Minimum permissions in `finish-args`
- [ ] Using a non-EOL runtime

---

## Submission PR Workflow

```bash
# 1. Install GitHub CLI (optional but convenient)
gh repo fork --clone flathub/flathub && cd flathub && git checkout --track origin/new-pr

# OR manually:
# Fork https://github.com/flathub/flathub (UNCHECK "master branch only")
git clone --branch=new-pr git@github.com:YOURUSERNAME/flathub.git
cd flathub

# 2. Create submission branch
git checkout -b add-io-github-you-myapp new-pr

# 3. Add your files
cp /path/to/io.github.you.myapp.yaml .
git add io.github.you.myapp.yaml
git commit -m "Add io.github.you.myapp"
git push origin add-io-github-you-myapp

# 4. Open PR on GitHub
# Base branch: new-pr (NOT master!)
# Title: "Add io.github.you.myapp"
```

**⚠️ Never open PR against `master`. Always target `new-pr`.**

---

## What Goes in the Submission Repo

The Flathub submission repo needs only these files (at minimum):
```
io.github.you.myapp.yaml          # The manifest (can also be .json)
```

The manifest references your source repo (via `type: git`). Everything else
(MetaInfo, desktop file, icons) is built FROM SOURCE and installed by your manifest.

If you have patches or local sources:
```
io.github.you.myapp.yaml
my-fix.patch
some-local-file.txt
```

---

## After Submission

- Reviewers are volunteers — response time varies (days to weeks)
- Respond to all review comments
- Never close and reopen the PR to address feedback
- Never merge `master` into your branch
- To trigger a test build: comment `bot, build` on the PR (only after reviewers say so)
- After approval and merge, you'll receive a GitHub repo invite under github.com/flathub/
- Enable 2FA on GitHub before the invite, accept within 1 week

---

## Maintenance After Publishing

### Updating Your App

Updates do NOT go through the submission PR process. Just push to your Flathub repo:

```bash
# Clone your app's Flathub repo (after approval)
git clone git@github.com:flathub/io.github.you.myapp.git
cd io.github.you.myapp

# Update the manifest (new tag/commit, update checksums)
# Edit io.github.you.myapp.yaml

git add io.github.you.myapp.yaml
git commit -m "Update to v1.1.0"
git push
```

Flathub auto-builds on push to the `master` branch. Published in ~1-2 hours.

### Using External Data Checker (Auto-Updates)

Add `x-checker-data` to sources for automated version tracking:

```yaml
sources:
  - type: archive
    url: https://github.com/you/myapp/releases/download/v$version/myapp-$version.tar.gz
    sha256: abc123...
    x-checker-data:
      type: json
      url: https://api.github.com/repos/you/myapp/releases/latest
      version-query: .tag_name | ltrimstr("v")
      url-query: .assets[] | select(.name=="myapp-\($version).tar.gz") | .browser_download_url

  - type: git
    url: https://github.com/you/myapp.git
    tag: v1.0.0
    commit: abc123...
    x-checker-data:
      type: git
      tag-pattern: '^v([\d.]+)$'
```

External Data Checker runs periodically and opens PRs automatically when new versions are detected.

### GitHub Actions CI for Your Own Repo

Add to your app source repo at `.github/workflows/flatpak.yml`:

```yaml
name: Flatpak CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: bilelmoussaoui/flatpak-github-actions:freedesktop-24.08
      options: --privileged
    steps:
      - uses: actions/checkout@v4
      - uses: flatpak/flatpak-github-actions/flatpak-builder@v6
        with:
          bundle: myapp.flatpak
          manifest-path: io.github.you.myapp.yaml
          cache-key: flatpak-builder-${{ github.sha }}
```

For GNOME apps:
```yaml
      image: bilelmoussaoui/flatpak-github-actions:gnome-48
```

For KDE apps:
```yaml
      image: bilelmoussaoui/flatpak-github-actions:kde-6.9
```

---

## Verification

Verified apps show a checkmark on Flathub. To verify:

1. Go to https://flathub.org/developer-portal
2. Log in with GitHub
3. Select your app
4. Choose verification method:

   **Website verification:** Place a token file at:
   `https://yourdomain.com/.well-known/org.flathub.VerifiedApps.txt`
   Content: just your App ID, e.g., `com.example.myapp`

   **GitHub/GitLab:** For `io.github.*` IDs, verification is via your GitHub account ownership

---

## Flathub Linter Reference

The linter (`flatpak-builder-lint`) checks for common issues.

Common errors and fixes:

| Error | Meaning | Fix |
|-------|---------|-----|
| `appstream-missing-categories` | No categories in MetaInfo | Add via desktop file or MetaInfo `<categories>` |
| `appstream-missing-icon-offer` | No icon found | Check icon paths and naming |
| `appstream-screenshot-missing` | No screenshots | Add `<screenshots>` to MetaInfo |
| `appstream-releases-missing` | No release info | Add `<releases>` to MetaInfo |
| `appstream-content-rating-missing` | No OARS data | Add `<content_rating type="oars-1.1" />` |
| `finish-args-arbitrary-dbus-access` | Session/system bus access | Use `--talk-name=` instead of `--socket=session-bus` |
| `finish-args-contains-both-x11-and-wayland` | Both sockets set | Use `--socket=fallback-x11` + `--socket=wayland` |
| `finish-args-flatpak-spawn-access` | Uses `flatpak-spawn` | Requires justification |
| `finish-args-absolute-home-path` | Hardcoded `~` path | Use `--filesystem=xdg-*` instead |

For exceptions to linter rules: https://docs.flathub.org/docs/for-app-authors/linter#exceptions

---

## Useful Resources

- Flathub docs: https://docs.flathub.org/docs/for-app-authors
- Flatpak builder docs: https://docs.flatpak.org/en/latest/flatpak-builder.html
- AppStream spec: https://www.freedesktop.org/software/appstream/docs/
- OARS generator: https://hughsie.github.io/oars/generate.html
- MetaInfo generator: https://www.freedesktop.org/software/appstream/metainfocreator/
- Banner preview: https://docs.flathub.org/banner-preview
- Shared modules: https://github.com/flathub/shared-modules
- flatpak-builder-tools (dep generators): https://github.com/flatpak/flatpak-builder-tools
- GitHub search for examples: https://github.com/search?q=org%3Aflathub&type=code
- Flathub Matrix: https://matrix.to/#/#flathub:matrix.org

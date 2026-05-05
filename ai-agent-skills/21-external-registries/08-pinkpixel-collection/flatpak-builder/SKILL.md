---
name: flatpak-builder
description: Complete guide for packaging Linux applications as Flatpaks for distribution on Flathub. Use this skill whenever the user mentions: "flatpak", "flathub", "packaging for linux", "creating a flatpak", "flatpak manifest", "flatpak sandbox", "desktop file", "metainfo", "appstream", "flatpak-builder", "linux app distribution", "app icon linux", ".desktop file", "publish to flathub", or any time they want to make their app installable via flatpak. ALWAYS trigger on any flatpak/flathub packaging question, even if they just say "how do I make my app a flatpak" or "I want to publish my app on Linux". Covers manifests, runtimes, MetaInfo/AppStream XML, desktop files, icons at all sizes, sandbox permissions, build systems (cmake, meson, simple), Flathub submission, linting, GitHub Actions CI, and verification.
---

# Flatpak Builder Skill

This skill covers everything needed to package an application as a Flatpak and
publish it to Flathub — from the first manifest to a live store listing.

## Quick Reference — Required Files

Every Flathub submission needs these files:

| File | Location (in build) | Purpose |
|------|---------------------|---------|
| `$APP_ID.yaml` (or `.json`) | repo root | Flatpak manifest |
| `$APP_ID.metainfo.xml` | `/app/share/metainfo/` | AppStream metadata |
| `$APP_ID.desktop` | `/app/share/applications/` | Desktop entry |
| Icons (multiple sizes) | `/app/share/icons/hicolor/<size>/apps/` | App icons |

→ For manifest deep-dive, see `references/manifest.md`
→ For MetaInfo/AppStream XML, see `references/metainfo.md`
→ For icons and desktop files, see `references/icons-and-desktop.md`
→ For Flathub submission process, see `references/submission.md`

---

## Step 1: Choose Your Application ID

The ID follows reverse-DNS format: `{tld}.{vendor}.{product}`

```
# Own a domain?
com.example.MyApp

# GitHub/GitLab hosted (REQUIRED format for code hosting)
io.github.yourusername.yourrepo
io.gitlab.yourusername.yourrepo
page.codeberg.yourusername.yourrepo
```

**Rules:**
- 3-5 components, max 255 chars
- Characters: `[A-Z][a-z][0-9]_` only (dash `-` allowed only in last component)
- Do NOT end in `.app`, `.desktop`, `.linux`
- Must exactly match the ID in your MetaInfo file
- ID determines verification method — choose carefully, renaming requires resubmission

---

## Step 2: Choose a Runtime

| Runtime | SDK | Use for |
|---------|-----|---------|
| `org.freedesktop.Platform//24.08` | `org.freedesktop.Sdk//24.08` | Base/minimal apps |
| `org.gnome.Platform//48` | `org.gnome.Sdk//48` | GTK4/GNOME apps |
| `org.kde.Platform//6.9` | `org.kde.Sdk//6.9` | Qt6/KDE apps |

- Freedesktop: new major version every August, 2-year support
- GNOME: synced with GNOME releases (~6 month cycle)
- KDE: synced with Qt releases
- **Never use EOL runtimes** — submissions will be rejected

---

## Step 3: Write the Manifest

See `references/manifest.md` for complete examples for each build system.

**Minimal YAML manifest skeleton:**
```yaml
id: io.github.yourusername.yourapp
runtime: org.freedesktop.Platform
runtime-version: '24.08'
sdk: org.freedesktop.Sdk
command: your-app-binary

finish-args:
  - --share=ipc
  - --socket=fallback-x11
  - --socket=wayland
  - --device=dri

modules:
  - name: your-app
    buildsystem: cmake-ninja   # or: meson, simple, autotools
    sources:
      - type: git
        url: https://github.com/yourusername/yourapp.git
        tag: v1.0.0
        commit: abc123...
```

**Key manifest rules:**
- NO network access during build — all sources must be declared upfront
- No pre-compiled binaries
- All dependencies must be listed as modules or sourced from runtime/shared modules
- Minimize `finish-args` — only request what the app actually needs

---

## Step 4: Icons (Critical!)

Icons must be installed at the correct paths. Missing or wrong sizes = linter failure.

**Required sizes for Flathub:**
```
/app/share/icons/hicolor/16x16/apps/$APP_ID.png
/app/share/icons/hicolor/32x32/apps/$APP_ID.png
/app/share/icons/hicolor/48x48/apps/$APP_ID.png
/app/share/icons/hicolor/64x64/apps/$APP_ID.png
/app/share/icons/hicolor/128x128/apps/$APP_ID.png
/app/share/icons/hicolor/256x256/apps/$APP_ID.png
/app/share/icons/hicolor/512x512/apps/$APP_ID.png
/app/share/icons/hicolor/scalable/apps/$APP_ID.svg  ← SVG preferred
```

**Install icons in your manifest:**
```yaml
- name: your-app
  buildsystem: simple
  build-commands:
    - install -Dm644 icons/512x512.png /app/share/icons/hicolor/512x512/apps/io.github.you.yourapp.png
    - install -Dm644 icons/256x256.png /app/share/icons/hicolor/256x256/apps/io.github.you.yourapp.png
    - install -Dm644 icons/scalable.svg /app/share/icons/hicolor/scalable/apps/io.github.you.yourapp.svg
```

See `references/icons-and-desktop.md` for full guidance including taskbar appearance.

---

## Step 5: Desktop File

```ini
[Desktop Entry]
Name=My App
Comment=Short description of what it does
Exec=myapp
Icon=io.github.yourusername.yourapp
Type=Application
Categories=Utility;
StartupNotify=true
StartupWMClass=myapp
```

Install to `/app/share/applications/io.github.yourusername.yourapp.desktop`

The filename **must match** your App ID exactly.

---

## Step 6: MetaInfo XML

See `references/metainfo.md` for the complete required XML structure.

Minimum required tags: `id`, `name`, `summary`, `description`, `metadata_license`,
`project_license`, `developer`, `launchable`, `screenshots`, `releases`, `content_rating`

---

## Step 7: Build and Test Locally

```bash
# Install the builder
flatpak install -y flathub org.flatpak.Builder
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# Build and install
flatpak run --command=flathub-build org.flatpak.Builder --install io.github.you.yourapp.yaml

# Run your app
flatpak run io.github.you.yourapp

# Lint the manifest
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest io.github.you.yourapp.yaml

# Lint the repo
flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo repo
```

**Fix all linter errors before submitting.** Both errors AND warnings are fatal.

---

## Step 8: Submit to Flathub

See `references/submission.md` for the complete PR workflow.

**TL;DR:**
1. Fork `flathub/flathub` on GitHub (uncheck "master branch only")
2. Clone with `--branch=new-pr`
3. Create a new branch, add your files, push
4. Open PR against the `new-pr` base branch (NOT master)
5. Title: `"Add io.github.you.yourapp"`

---

## Common Linter Failures

| Error | Fix |
|-------|-----|
| Missing MetaInfo | Create `$APP_ID.metainfo.xml` |
| Wrong icon path | Name must exactly match `$APP_ID`, not just app name |
| Missing `content_rating` | Add `<content_rating type="oars-1.1" />` |
| EOL runtime | Update to current runtime version |
| Network in build | Remove network calls, pre-vendor all deps |
| Desktop file mismatch | Filename must be `$APP_ID.desktop` |
| Missing release tag | Add at least one `<release>` entry |
| Icon too small | Provide at least 128x128, ideally up to 512x512 |

---

## Sandbox Permissions Cheatsheet

Only request what you need. Prefer XDG portals over static permissions.

```yaml
finish-args:
  # Display
  - --socket=wayland           # Wayland (preferred)
  - --socket=fallback-x11      # X11 fallback
  - --share=ipc                # Needed for X11 shared memory
  - --device=dri               # GPU access (for OpenGL/Vulkan)

  # Filesystem
  - --filesystem=home          # Full home dir (avoid if possible!)
  - --filesystem=xdg-documents # XDG documents folder
  - --filesystem=xdg-pictures  # XDG pictures
  - --filesystem=host:ro       # Read-only host FS (very permissive)

  # Audio
  - --socket=pulseaudio        # PulseAudio / PipeWire

  # Network
  - --share=network            # Internet access

  # D-Bus
  - --talk-name=org.freedesktop.Notifications  # Notifications
  - --own-name=com.example.MyApp              # Own a bus name
```

**Use portals instead of `--filesystem=home` wherever possible.**

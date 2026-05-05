# Icons and Desktop Files Reference

This covers everything needed to make your Flatpak app appear correctly in launchers,
taskbars, app grids, and the Flathub store.

---

## Icons

### Required Sizes for Flathub

Flathub and GNOME/KDE app stores pull icons from the hicolor theme directory.
The app ID is used as the icon name (not the binary name).

```
/app/share/icons/hicolor/16x16/apps/$APP_ID.png
/app/share/icons/hicolor/32x32/apps/$APP_ID.png
/app/share/icons/hicolor/48x48/apps/$APP_ID.png
/app/share/icons/hicolor/64x64/apps/$APP_ID.png
/app/share/icons/hicolor/128x128/apps/$APP_ID.png
/app/share/icons/hicolor/256x256/apps/$APP_ID.png
/app/share/icons/hicolor/512x512/apps/$APP_ID.png
/app/share/icons/hicolor/scalable/apps/$APP_ID.svg  ← STRONGLY preferred
```

**Minimum required:** 128x128 PNG. Provide 512x512 and SVG for best results.
**Linter will fail** if icon filename does not match the App ID exactly.

### Icon Quality Guidelines

- Square with no padding/whitespace around the edges
- Should be recognizable at small sizes (16x16)
- PNG: no transparency issues, properly cropped
- SVG: use inkscape-compatible SVG, viewBox set correctly
- Do NOT include app name text in the icon
- Do NOT violate any trademarks

### Installing Icons in the Manifest

**Method 1: Simple buildsystem (most control)**
```yaml
- name: my-app
  buildsystem: simple
  build-commands:
    # SVG (preferred — covers all sizes)
    - install -Dm644 data/icons/app.svg
        /app/share/icons/hicolor/scalable/apps/io.github.you.myapp.svg

    # PNGs at each required size
    - install -Dm644 data/icons/512.png
        /app/share/icons/hicolor/512x512/apps/io.github.you.myapp.png
    - install -Dm644 data/icons/256.png
        /app/share/icons/hicolor/256x256/apps/io.github.you.myapp.png
    - install -Dm644 data/icons/128.png
        /app/share/icons/hicolor/128x128/apps/io.github.you.myapp.png
    - install -Dm644 data/icons/64.png
        /app/share/icons/hicolor/64x64/apps/io.github.you.myapp.png
    - install -Dm644 data/icons/48.png
        /app/share/icons/hicolor/48x48/apps/io.github.you.myapp.png
    - install -Dm644 data/icons/32.png
        /app/share/icons/hicolor/32x32/apps/io.github.you.myapp.png
```

**Method 2: post-install (for cmake/meson apps that install their own icons)**
```yaml
- name: my-app
  buildsystem: cmake-ninja
  builddir: true
  post-install:
    # If app installs icon as 'myapp' but App ID is 'io.github.you.myapp'
    - mv /app/share/icons/hicolor/scalable/apps/myapp.svg
         /app/share/icons/hicolor/scalable/apps/io.github.you.myapp.svg
```

**Method 3: rename-icon in manifest top-level (automatic rename)**
```yaml
# At top of manifest:
rename-icon: myapp   # Renames 'myapp' icon to match $APP_ID on install
```
This appends the App ID automatically, so `myapp.svg` → `io.github.you.myapp.svg`.

### Generating Multiple Sizes from SVG

If you only have an SVG, generate PNGs with Inkscape or ImageMagick:
```bash
# Using Inkscape
for size in 16 32 48 64 128 256 512; do
  inkscape --export-filename="$size.png" -w $size -h $size icon.svg
done

# Using ImageMagick/rsvg-convert
for size in 16 32 48 64 128 256 512; do
  rsvg-convert -w $size -h $size -o "$size.png" icon.svg
done
```

Or as a Makefile target in your build system.

### Taskbar / Dock Appearance

The taskbar icon on GNOME/KDE is pulled from:
1. The running window's `WM_CLASS` property (matched to desktop file's `StartupWMClass`)
2. The icon name in the `.desktop` file (`Icon=` field)
3. The hicolor theme icon matching that name

**For correct taskbar appearance:**
- Set `Icon=io.github.you.myapp` in your `.desktop` file
- Set `StartupWMClass=myapp` to the actual WM_CLASS your app uses
- Find your app's WM_CLASS: run `xprop WM_CLASS` then click the window

---

## Desktop Files

The `.desktop` file is the launcher entry. It tells the system how to run
your app and where to find its icon.

**Path:** `/app/share/applications/$APP_ID.desktop`
**Filename must match App ID exactly.**

### Complete Desktop File Template

```ini
[Desktop Entry]
# Required
Name=My App
Comment=A short description of what this app does
Exec=myapp %F
Icon=io.github.yourusername.myapp
Type=Application

# Display categories (see https://specifications.freedesktop.org/menu-spec/latest/apa.html)
Categories=Utility;

# Important for taskbar icon matching
StartupNotify=true
StartupWMClass=myapp

# File associations (optional — for apps that open specific file types)
MimeType=image/png;image/jpeg;

# Keywords for search (optional)
Keywords=tool;utility;helper;

# Hide from launcher in specific environments (optional)
# NotShowIn=KDE;

# Translations (add as many languages as needed)
Name[de]=Meine App
Comment[de]=Eine kurze Beschreibung
```

### Exec Field Format

```ini
# No arguments
Exec=myapp

# Accepts files (most common)
Exec=myapp %F

# Accepts URLs
Exec=myapp %U

# With flags
Exec=myapp --no-sandbox %F
```

### Categories Reference

Pick the most specific that applies:
```
AudioVideo    # Audio/Video playback or editing
Audio         # Audio apps
Video         # Video apps
Development   # IDEs, debuggers, code editors
Education     # Educational software
Game          # Games
Graphics      # Image editors, viewers
Network       # Browsers, email, chat
Office        # Word processors, spreadsheets
Science       # Scientific tools
Settings      # Configuration tools
System        # System utilities
Utility       # General utilities
```

Additional sub-categories from the spec can also be added:
```
Player, Recorder, Mixer (AudioVideo subcategories)
2DGraphics, 3DGraphics, VectorGraphics, RasterGraphics (Graphics)
TextEditor, WordProcessor, Spreadsheet (Office)
```

### Installing the Desktop File

**Simple build:**
```yaml
- install -Dm644 data/myapp.desktop
    /app/share/applications/io.github.yourusername.myapp.desktop
```

**With rename-desktop-file (top-level manifest key):**
```yaml
# At top of manifest — renames automatically on install
rename-desktop-file: myapp.desktop
```

**Validation:**
```bash
desktop-file-validate /app/share/applications/io.github.you.myapp.desktop
```

---

## How It All Connects

```
MetaInfo XML
  └─ <launchable type="desktop-id">io.github.you.myapp.desktop</launchable>
        │
        └─► Desktop File (/app/share/applications/io.github.you.myapp.desktop)
              │   └─ Icon=io.github.you.myapp
              │         │
              │         └─► hicolor icons (/app/share/icons/hicolor/.../io.github.you.myapp.png)
              │
              └─ StartupWMClass=myapp  (links running window to icon in taskbar)
```

`appstreamcli compose` uses the `<launchable>` tag to find the `.desktop` file
and pull in categories, keywords, and icons automatically into the AppStream index.

---

## Troubleshooting

**Icon doesn't show in taskbar:**
- Check `StartupWMClass` matches actual WM_CLASS (`xprop WM_CLASS` on the window)
- Ensure icon filename exactly matches App ID
- Run `gtk-update-icon-cache /app/share/icons/hicolor` in post-install (some builds need this)

**Icon doesn't show in app store:**
- Must have `<launchable>` tag in MetaInfo
- Icon must be at correct hicolor path
- Minimum 128x128 PNG required

**Desktop file not found:**
- Filename must exactly equal `$APP_ID.desktop`
- Must be installed to `/app/share/applications/` not a subdirectory

**Linter: "icon not found":**
- Icon filename must be `$APP_ID` (e.g., `io.github.you.myapp.png`), not just `myapp.png`
- Check the path carefully — hicolor paths are case-sensitive

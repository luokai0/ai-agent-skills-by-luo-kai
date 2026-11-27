# Flatpak Manifest Reference

Flatpak manifests can be YAML (`.yaml`/`.yml`) or JSON (`.json`). YAML is recommended for readability.

## Table of Contents
1. [Top-Level Fields](#top-level-fields)
2. [Finish Args (Sandbox Permissions)](#finish-args)
3. [Module Structure](#module-structure)
4. [Build Systems](#build-systems)
5. [Sources](#sources)
6. [Complete Examples by Stack](#complete-examples)
7. [Handling Dependencies](#handling-dependencies)

---

## Top-Level Fields

```yaml
id: io.github.yourusername.yourapp          # Required. Reverse-DNS app ID.
runtime: org.freedesktop.Platform            # Required. Runtime to run against.
runtime-version: '24.08'                     # Required. Runtime branch/version.
sdk: org.freedesktop.Sdk                     # Required. SDK to build with.
command: yourapp                             # Required. Binary to execute.
separate-locales: true                       # Optional. Splits locales into extension (saves space).
rename-icon: yourapp                         # Optional. Renames icon to match App ID on install.
rename-desktop-file: yourapp.desktop        # Optional. Renames .desktop file to match App ID.
rename-appdata-file: yourapp.metainfo.xml   # Optional. Renames MetaInfo file to match App ID.
copy-icon: true                              # Use with rename-icon if keeping original too.

sdk-extensions:
  - org.freedesktop.Sdk.Extension.rust-stable   # For Rust apps
  - org.freedesktop.Sdk.Extension.node20        # For Node.js apps
  - org.freedesktop.Sdk.Extension.llvm18        # For LLVM/Clang
  - org.freedesktop.Sdk.Extension.golang        # For Go apps

build-options:
  env:
    CARGO_HOME: /run/build/your-app/cargo
  prepend-path: /usr/lib/sdk/rust-stable/bin  # Activate SDK extension

finish-args: [...]    # Sandbox permissions — see below
modules: [...]        # Build modules — see below
```

---

## Finish Args

Only request permissions your app genuinely needs. Reviewers will push back on overreach.

```yaml
finish-args:
  # === DISPLAY ===
  - --socket=wayland              # Wayland display (modern, preferred)
  - --socket=fallback-x11        # X11 fallback for non-Wayland desktops
  - --share=ipc                   # Required for X11 MIT-SHM shared memory

  # === GPU ===
  - --device=dri                  # DRI device access (OpenGL, Vulkan, VA-API)

  # === AUDIO ===
  - --socket=pulseaudio           # PulseAudio / PipeWire audio

  # === NETWORK ===
  - --share=network               # Internet access

  # === FILESYSTEM ===
  - --filesystem=home             # Full home directory (avoid — use portals instead)
  - --filesystem=xdg-documents    # ~/.local/share/documents
  - --filesystem=xdg-pictures     # ~/.local/share/pictures
  - --filesystem=xdg-music        # ~/.local/share/music
  - --filesystem=xdg-videos       # ~/.local/share/videos
  - --filesystem=xdg-download     # ~/Downloads
  - --filesystem=xdg-desktop      # ~/Desktop
  - --filesystem=xdg-config:ro    # Read-only config
  - --filesystem=xdg-data:ro      # Read-only data
  - --filesystem=/path/to/dir     # Specific path
  - --filesystem=host:ro          # Full read-only host filesystem (very permissive)
  - --nofilesystem=home           # Explicitly deny (to override inherited grants)

  # === D-BUS ===
  - --socket=session-bus          # Full session bus access (AVOID — too broad)
  - --socket=system-bus           # Full system bus access (AVOID — too broad)
  - --talk-name=org.freedesktop.Notifications        # Desktop notifications
  - --talk-name=org.gnome.SettingsDaemon.Color       # Night light / color profiles
  - --talk-name=org.freedesktop.portal.Desktop       # XDG portal access
  - --own-name=com.example.MyApp                     # Own a session bus name

  # === OTHER ===
  - --device=all                  # All devices (webcam, etc.) — use carefully
  - --allow=bluetooth             # Bluetooth access
```

---

## Module Structure

```yaml
modules:
  - name: my-module               # Required. Unique name.
    buildsystem: cmake-ninja      # Required. Build system.
    builddir: true                # Build in separate dir (required for cmake/meson).
    no-autogen: false             # Don't run autogen (autotools).
    config-opts:                  # Pass to configure/cmake/meson
      - -DCMAKE_BUILD_TYPE=Release
      - -DBUILD_TESTING=OFF
    make-args:
      - -j4
    make-install-args:
      - DESTDIR=/app
    post-install:                 # Commands run after install
      - install -Dm644 my.desktop /app/share/applications/io.github.you.app.desktop
    build-commands:               # Only for buildsystem: simple
      - pip3 install --prefix=/app .
    sources: [...]
```

---

## Build Systems

### cmake-ninja (Recommended for CMake)
```yaml
- name: myapp
  buildsystem: cmake-ninja
  builddir: true
  config-opts:
    - -DCMAKE_BUILD_TYPE=Release
    - -DCMAKE_INSTALL_PREFIX=/app
  sources:
    - type: git
      url: https://github.com/you/myapp.git
      tag: v1.0.0
      commit: deadbeef...
```

### meson
```yaml
- name: myapp
  buildsystem: meson
  builddir: true
  config-opts:
    - -Dprefix=/app
    - -Dbuildtype=release
  sources:
    - type: git
      url: https://github.com/you/myapp.git
      tag: v1.0.0
      commit: deadbeef...
```

### autotools
```yaml
- name: myapp
  buildsystem: autotools
  config-opts:
    - --prefix=/app
    - --disable-debug
  sources:
    - type: archive
      url: https://example.com/myapp-1.0.tar.gz
      sha256: abc123...
```

### simple (Manual build commands)
```yaml
- name: myapp
  buildsystem: simple
  build-commands:
    - install -Dm755 myapp /app/bin/myapp
    - install -Dm644 data/myapp.desktop /app/share/applications/io.github.you.myapp.desktop
    - install -Dm644 data/icons/512.png /app/share/icons/hicolor/512x512/apps/io.github.you.myapp.png
    - install -Dm644 LICENSE /app/share/licenses/io.github.you.myapp/LICENSE
  sources:
    - type: git
      url: https://github.com/you/myapp.git
      tag: v1.0.0
      commit: deadbeef...
```

---

## Sources

### Git source
```yaml
sources:
  - type: git
    url: https://github.com/you/myapp.git
    tag: v1.0.0
    commit: abc123def456...    # Always pin to exact commit with tag!
    # Optional:
    branch: main               # Use branch instead of tag
    disable-shallow-clone: true
```

### Archive (tarball)
```yaml
sources:
  - type: archive
    url: https://github.com/you/myapp/archive/v1.0.0.tar.gz
    sha256: abc123...          # Required! Verify integrity.
    strip-components: 1        # Remove top-level dir from archive
```

### File source (patch, extra file)
```yaml
sources:
  - type: file
    path: my-patch.patch       # Local file in repo
    # or:
    url: https://example.com/file.txt
    sha256: abc123...
  - type: patch
    path: my.patch
```

### Script source
```yaml
sources:
  - type: script
    commands:
      - echo "doing stuff"
    dest-filename: setup.sh
```

### Local directory
```yaml
sources:
  - type: dir
    path: ./local-subdir
```

---

## Complete Examples by Stack

### Electron / Node.js App

```yaml
id: io.github.yourusername.electronapp
runtime: org.freedesktop.Platform
runtime-version: '24.08'
sdk: org.freedesktop.Sdk
base: org.electronjs.Electron2.BaseApp
base-version: '24.08'
command: run.sh
separate-locales: false

sdk-extensions:
  - org.freedesktop.Sdk.Extension.node20

build-options:
  append-path: /usr/lib/sdk/node20/bin
  env:
    NPM_CONFIG_LOGLEVEL: info

finish-args:
  - --share=ipc
  - --socket=fallback-x11
  - --socket=wayland
  - --share=network
  - --device=dri
  - --filesystem=xdg-documents
  - --talk-name=org.freedesktop.Notifications

modules:
  - name: myelectronapp
    buildsystem: simple
    build-options:
      env:
        HOME: /root   # npm needs HOME
    build-commands:
      - npm install --offline
      - npm run build
      - mkdir -p /app/main
      - cp -r dist/* /app/main/
      - install -Dm755 run.sh /app/bin/run.sh
      - install -Dm644 data/io.github.you.app.desktop /app/share/applications/io.github.you.app.desktop
      - install -Dm644 data/icons/512.png /app/share/icons/hicolor/512x512/apps/io.github.you.app.png
      - install -Dm644 data/io.github.you.app.metainfo.xml /app/share/metainfo/io.github.you.app.metainfo.xml
    sources:
      - type: git
        url: https://github.com/you/myapp.git
        tag: v1.0.0
        commit: abc123...
      - node-sources.json    # Pre-generated npm deps, see note below
```

> **Node.js tip:** Use `flatpak-node-generator` to pre-vendor npm deps into `node-sources.json`. Run: `flatpak-node-generator npm package-lock.json -o node-sources.json`

### Python App

```yaml
id: io.github.yourusername.pythonapp
runtime: org.freedesktop.Platform
runtime-version: '24.08'
sdk: org.freedesktop.Sdk
command: pythonapp

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --share=ipc
  - --device=dri

modules:
  - name: python3-dependencies
    buildsystem: simple
    build-commands:
      - pip3 install --prefix=/app --no-index --find-links=file://${PWD} -r requirements.txt
    sources:
      - type: file
        path: requirements.txt
      # Pre-downloaded wheels:
      - type: file
        url: https://files.pythonhosted.org/packages/.../requests-2.31.0-py3-none-any.whl
        sha256: abc123...

  - name: pythonapp
    buildsystem: simple
    build-commands:
      - pip3 install --prefix=/app --no-deps .
      - install -Dm644 data/io.github.you.app.desktop /app/share/applications/io.github.you.app.desktop
      - install -Dm644 data/icons/512.png /app/share/icons/hicolor/512x512/apps/io.github.you.app.png
      - install -Dm644 data/io.github.you.app.metainfo.xml /app/share/metainfo/io.github.you.app.metainfo.xml
    sources:
      - type: git
        url: https://github.com/you/pythonapp.git
        tag: v1.0.0
        commit: abc123...
```

> **Python tip:** Use `flatpak-pip-generator` to pre-vendor pip deps.

### Rust App

```yaml
id: io.github.yourusername.rustapp
runtime: org.freedesktop.Platform
runtime-version: '24.08'
sdk: org.freedesktop.Sdk
command: rustapp

sdk-extensions:
  - org.freedesktop.Sdk.Extension.rust-stable

build-options:
  append-path: /usr/lib/sdk/rust-stable/bin
  env:
    CARGO_HOME: /run/build/rustapp/cargo

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --share=ipc
  - --device=dri

modules:
  - name: rustapp
    buildsystem: simple
    build-commands:
      - cargo --offline fetch --manifest-path Cargo.toml --verbose
      - cargo --offline build --release --verbose
      - install -Dm755 target/release/rustapp /app/bin/rustapp
      - install -Dm644 data/io.github.you.app.desktop /app/share/applications/io.github.you.app.desktop
      - install -Dm644 data/icons/512.png /app/share/icons/hicolor/512x512/apps/io.github.you.app.png
      - install -Dm644 data/io.github.you.app.metainfo.xml /app/share/metainfo/io.github.you.app.metainfo.xml
    sources:
      - type: git
        url: https://github.com/you/rustapp.git
        tag: v1.0.0
        commit: abc123...
      - cargo-sources.json   # Pre-generated cargo deps
```

> **Rust tip:** Use `flatpak-cargo-generator.py` from flatpak-builder-tools to generate `cargo-sources.json`.

### GTK4 / GNOME App (Meson)

```yaml
id: org.example.mygnomeapp
runtime: org.gnome.Platform
runtime-version: '48'
sdk: org.gnome.Sdk
command: mygnomeapp

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --share=ipc
  - --device=dri
  - --filesystem=xdg-documents

modules:
  - name: mygnomeapp
    buildsystem: meson
    builddir: true
    config-opts:
      - -Dbuildtype=release
    sources:
      - type: git
        url: https://gitlab.gnome.org/you/mygnomeapp.git
        tag: '1.0.0'
        commit: abc123...
```

### Qt6 / KDE App

```yaml
id: org.kde.myqtapp
runtime: org.kde.Platform
runtime-version: '6.9'
sdk: org.kde.Sdk
command: myqtapp

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --share=ipc
  - --device=dri

modules:
  - name: myqtapp
    buildsystem: cmake-ninja
    builddir: true
    config-opts:
      - -DCMAKE_BUILD_TYPE=Release
    sources:
      - type: git
        url: https://github.com/you/myqtapp.git
        tag: v1.0.0
        commit: abc123...
```

---

## Handling Dependencies

### Shared modules (pre-made, maintained by Flathub community)
Check `https://github.com/flathub/shared-modules` first. Includes:
`libsecret`, `SDL2`, `libappindicator`, `gtk2`, `intltool`, and more.

```yaml
# At top of manifest, before modules:
x-shared-modules: !include shared-modules/libsecret/libsecret.json

modules:
  - !include shared-modules/libsecret/libsecret.json
  - name: myapp
    ...
```

### Building a dependency as a module
```yaml
modules:
  - name: libfoo
    buildsystem: cmake-ninja
    builddir: true
    sources:
      - type: archive
        url: https://example.com/libfoo-1.2.tar.gz
        sha256: abc123...

  - name: myapp
    buildsystem: cmake-ninja
    builddir: true
    sources:
      - type: git
        url: https://github.com/you/myapp.git
        tag: v1.0.0
        commit: abc123...
```

### Installing license files (REQUIRED by Flathub)
```yaml
- name: myapp
  buildsystem: cmake-ninja
  post-install:
    - install -Dm644 ../LICENSE /app/share/licenses/io.github.you.app/LICENSE
```

# MetaInfo / AppStream XML Reference

MetaInfo files provide app metadata for software stores (Flathub, GNOME Software, KDE Discover, etc.).

**Path:** `/app/share/metainfo/$APP_ID.metainfo.xml`
**Filename must match App ID exactly.**

---

## Validation

Always validate before submitting:
```bash
# Via org.flatpak.Builder (recommended)
flatpak run --command=flatpak-builder-lint org.flatpak.Builder appstream io.github.you.app.metainfo.xml

# Direct appstreamcli
appstreamcli validate io.github.you.app.metainfo.xml
```
Both errors AND warnings are fatal.

---

## Complete MetaInfo Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2024 Your Name -->
<component type="desktop-application">

  <!-- ===================== REQUIRED ===================== -->

  <id>io.github.yourusername.yourapp</id>

  <metadata_license>CC0-1.0</metadata_license>
  <project_license>GPL-3.0-only</project_license>
  <!-- For proprietary: <project_license>LicenseRef-proprietary=https://example.com/license</project_license> -->

  <name>Your App Name</name>
  <summary>A one-line description without a period at the end</summary>

  <developer id="io.github.yourusername">
    <name>Your Name or Org</name>
  </developer>

  <description>
    <p>A paragraph describing what your app does. Be specific and helpful.</p>
    <p>A second paragraph with more details or context.</p>
    <p>Key features:</p>
    <ul>
      <li>Feature one</li>
      <li>Feature two</li>
      <li>Feature three</li>
    </ul>
  </description>

  <!-- Must reference your installed .desktop file -->
  <launchable type="desktop-id">io.github.yourusername.yourapp.desktop</launchable>

  <!-- At least one screenshot required for graphical apps -->
  <screenshots>
    <screenshot type="default">
      <image>https://raw.githubusercontent.com/you/yourapp/main/screenshots/main.png</image>
      <caption>The main application window</caption>
    </screenshot>
    <screenshot>
      <image>https://raw.githubusercontent.com/you/yourapp/main/screenshots/settings.png</image>
      <caption>Settings dialog</caption>
    </screenshot>
  </screenshots>

  <!-- Must have at least one release -->
  <releases>
    <release version="1.0.1" date="2024-06-15">
      <url type="details">https://github.com/you/yourapp/releases/tag/v1.0.1</url>
      <description>
        <p>Bug fixes and improvements</p>
        <ul>
          <li>Fixed crash on startup when no config exists</li>
          <li>Improved dark mode support</li>
        </ul>
      </description>
    </release>
    <release version="1.0.0" date="2024-05-01">
      <url type="details">https://github.com/you/yourapp/releases/tag/v1.0.0</url>
      <description>
        <p>Initial release</p>
      </description>
    </release>
  </releases>

  <!-- Generate at https://hughsie.github.io/oars/generate.html -->
  <content_rating type="oars-1.1" />
  <!-- With content: <content_rating type="oars-1.1"><content_attribute id="violence-cartoon">mild</content_attribute></content_rating> -->

  <!-- ===================== RECOMMENDED ===================== -->

  <!-- Brand colors shown on the Flathub store page -->
  <branding>
    <color type="primary" scheme_preference="light">#4a86cf</color>
    <color type="primary" scheme_preference="dark">#1a3a6c</color>
  </branding>
  <!-- Preview at: https://docs.flathub.org/banner-preview -->

  <!-- URLs -->
  <url type="homepage">https://example.com</url>
  <url type="bugtracker">https://github.com/you/yourapp/issues</url>
  <url type="vcs-browser">https://github.com/you/yourapp</url>
  <url type="donation">https://example.com/donate</url>
  <url type="translate">https://hosted.weblate.org/projects/yourapp/</url>
  <url type="contribute">https://github.com/you/yourapp/blob/main/CONTRIBUTING.md</url>

  <!-- ===================== OPTIONAL ===================== -->

  <!-- For gettext translations -->
  <translation type="gettext">yourapp</translation>
  <!-- For Qt translations -->
  <!-- <translation type="qt">yourapp</translation> -->

  <!-- Project affiliation (protected values: GNOME, KDE, Freedesktop) -->
  <!-- <project_group>GNOME</project_group> -->

</component>
```

---

## Required Tags Checklist

| Tag | Required | Notes |
|-----|----------|-------|
| `id` | ✅ | Must exactly match App ID and filename |
| `metadata_license` | ✅ | License for the MetaInfo file itself (usually CC0-1.0) |
| `project_license` | ✅ | SPDX identifier |
| `name` | ✅ | App name (no trademark violations) |
| `summary` | ✅ | One line, no period at end |
| `developer` (with `id`) | ✅ | Who made it |
| `description` | ✅ | At least one `<p>` tag |
| `launchable` | ✅ | For graphical apps with .desktop file |
| `screenshots` | ✅ | At least one for graphical apps |
| `releases` | ✅ | At least one release entry |
| `content_rating` | ✅ | OARS 1.1 (even if empty) |
| `branding` | Recommended | Brand colors for store display |
| `url type="homepage"` | Recommended | Required to pass validation |

---

## License Tag Reference

Open source:
```xml
<project_license>MIT</project_license>
<project_license>GPL-3.0-only</project_license>
<project_license>GPL-2.0-or-later</project_license>
<project_license>LGPL-2.1-or-later</project_license>
<project_license>Apache-2.0</project_license>
<project_license>BSD-3-Clause</project_license>
<project_license>MPL-2.0</project_license>
```

Proprietary:
```xml
<project_license>LicenseRef-proprietary=https://example.com/license</project_license>
```

Multi-license (AND = all apply, OR = user's choice):
```xml
<project_license>GPL-2.0-only AND MIT</project_license>
<project_license>GPL-3.0-or-later OR MIT</project_license>
```

---

## Screenshot Quality Guidelines

- **Minimum resolution:** 624x351px
- **Recommended:** 1248x702px or higher (16:9 preferred for banner)
- **Format:** PNG or JPEG
- **Must show actual app UI** — no promotional graphics, fake content, or decorative borders
- **No window chrome** in the screenshot if possible (use compositor scaling)
- Use a raw commit URL (not branch URL) for hosted images:
  ```
  ✅ https://raw.githubusercontent.com/you/app/abc123commit.../screenshot.png
  ✅ https://raw.githubusercontent.com/you/app/v1.0.0/screenshots/main.png
  ❌ https://raw.githubusercontent.com/you/app/main/screenshots/main.png
  ```

---

## Release Notes Guidelines

- Use past tense ("Fixed", "Added", "Improved")
- Be specific and user-facing
- Versions must be in descending order (newest first)
- Dates must not be in the future
- Versions must be properly ordered (use `appstreamcli vercmp v1 v2` to verify)

---

## Translations in MetaInfo

English is implicit (no `xml:lang` attribute needed):
```xml
<name>My App</name>
<name xml:lang="de">Meine App</name>
<name xml:lang="fr">Mon Application</name>

<summary>A cool app</summary>
<summary xml:lang="de">Eine coole App</summary>

<description>
  <p>English description</p>
  <p xml:lang="de">Deutsche Beschreibung</p>
</description>
```

---

## Checking Generated Output

After building, inspect what appstreamcli generates:
```bash
appstreamcli compose --prefix=/path/to/app/install /path/to/app/install
# or in the flatpak build dir:
flatpak run --command=appstreamcli org.flatpak.Builder compose --prefix=/app builddir
```

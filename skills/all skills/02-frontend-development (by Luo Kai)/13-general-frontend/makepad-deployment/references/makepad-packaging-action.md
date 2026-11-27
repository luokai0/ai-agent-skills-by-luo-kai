# Makepad Packaging GitHub Action

## 中文摘要

- 用于 GitHub Actions 中的 Makepad 打包与发布，支持桌面、移动与 OpenHarmony。
- 内部封装 `cargo-packager` 与 `cargo-makepad`，可上传产物到 GitHub Releases。
- 通过 `args` 指定 target，移动端必须显式指定 target。
- 桌面/iOS 需要匹配的 runner（iOS 需 macOS）。

详细字段与示例见下文英文参考。

Reference for `makepad-packaging-action` (CI packaging + optional GitHub Release upload).

## When to use
- One-step packaging for desktop and mobile targets in CI
- Matrix builds across OS and target triples
- Upload artifacts to GitHub Releases

## Platform constraints
- Linux packages must run on Linux runners.
- Windows installers must run on Windows runners.
- macOS DMG/app bundles and iOS builds require macOS runners.
- Android builds can run on any OS runner.

## Inputs

| Input | Notes |
| --- | --- |
| `args` | Extra args passed to `cargo build` and `cargo makepad` (use `--target ...`). |
| `packager_formats` | Comma-separated `cargo packager` formats (`deb,dmg,nsis`). |
| `packager_args` | Extra args passed only to `cargo packager`. |
| `tagName` | Release tag name. Supports `__VERSION__`. |
| `releaseName` | Release title. Supports `__VERSION__`. |
| `releaseBody` | Release body markdown. |
| `releaseId` | Existing release ID to upload assets to. |
| `asset_name_template` | Template for asset names. Placeholders: `__APP__`, `__VERSION__`, `__PLATFORM__`, `__ARCH__`, `__MODE__`, `__EXT__`, `__FILENAME__`, `__BASENAME__`. |
| `asset_prefix` | Optional prefix for generated asset names. |
| `releaseDraft` | Create a draft release (`true`/`false`). |
| `prerelease` | Mark as prerelease (`true`/`false`). |
| `github_token` | Token for release creation/upload (defaults to `GITHUB_TOKEN`). |
| `project_path` | Makepad project path (default `.`). |
| `app_name` | Override app name (otherwise derived from `Cargo.toml`). |
| `app_version` | Override version (otherwise derived from `Cargo.toml`). |
| `identifier` | Override bundle identifier. |
| `include_release` | Include release build (`true`/`false`, default `true`). |
| `include_debug` | Include debug build (`true`/`false`, default `false`). |

## Environment variables

Android:
- `MAKEPAD_ANDROID_ABI` (default `aarch64`)
- `MAKEPAD_ANDROID_FULL_NDK` (`true`/`false`)
- `MAKEPAD_ANDROID_VARIANT` (`default` or `quest`)

iOS:
- `MAKEPAD_IOS_ORG`
- `MAKEPAD_IOS_APP`
- `MAKEPAD_IOS_PROFILE` (optional)
- `MAKEPAD_IOS_CERT` (optional)
- `MAKEPAD_IOS_SIM` (`true`/`false`)
- `MAKEPAD_IOS_CREATE_IPA` (`true`/`false`)
- `MAKEPAD_IOS_UPLOAD_TESTFLIGHT` (`true`/`false`)

Apple signing:
- `APPLE_CERTIFICATE` (base64 `.p12`)
- `APPLE_CERTIFICATE_PASSWORD`
- `APPLE_PROVISIONING_PROFILE` (base64 `.mobileprovision`)
- `APPLE_KEYCHAIN_PASSWORD`
- `APPLE_SIGNING_IDENTITY` (default `Apple Distribution`)

TestFlight upload (when `MAKEPAD_IOS_UPLOAD_TESTFLIGHT=true`):
- `APP_STORE_CONNECT_API_KEY` or `APP_STORE_CONNECT_API_KEY_CONTENT`
- `APP_STORE_CONNECT_KEY_ID`
- `APP_STORE_CONNECT_ISSUER_ID`

OpenHarmony (HAP):
- `DEVECO_HOME` (optional, auto-detected if omitted)
- `OHOS_P12_BASE64`
- `OHOS_PROFILE_BASE64`
- `OHOS_P12_PASSWORD`
- `OHOS_KEY_ALIAS` (default `debugKey`)
- `OHOS_KEY_PASSWORD` (default `OHOS_P12_PASSWORD`)
- `OHOS_CERT_BASE64` (optional)
- `OHOS_SIGN_ALG` (default `SHA256withECDSA`)

## Outputs

| Output | Notes |
| --- | --- |
| `artifacts` | JSON array of `{ path, platform, arch, mode, version }`. |
| `app_name` | Resolved app name. |
| `app_version` | Resolved app version. |
| `release_url` | GitHub Release URL (if created). |

## Behavior notes
- Target defaults to host platform unless `--target` is passed in `args`.
- Mobile builds require an explicit target triple.
- If `releaseId` is set, assets are uploaded without creating a release.
- If `tagName` is set (and `releaseId` is not), a release is created/updated.
- Directory artifacts (like `.app`) are zipped before upload.

## Examples

Minimal packaging (Linux):
```yaml
jobs:
  package:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      - uses: Project-Robius-China/makepad-packaging-action@v1
        with:
          args: --target x86_64-unknown-linux-gnu --release
```

Matrix build with release upload:
```yaml
jobs:
  package:
    strategy:
      matrix:
        include:
          - os: ubuntu-22.04
            args: --target x86_64-unknown-linux-gnu
          - os: windows-2022
            args: --target x86_64-pc-windows-msvc
          - os: macos-14
            args: --target aarch64-apple-darwin
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: Project-Robius-China/makepad-packaging-action@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: app-v__VERSION__
          releaseName: "App v__VERSION__"
          releaseBody: "See the assets to download this version."
          args: ${{ matrix.args }}
```

Upload to an existing release:
```yaml
- uses: Project-Robius-China/makepad-packaging-action@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    releaseId: ${{ needs.create_release.outputs.id }}
    args: --target aarch64-linux-android
```

## Status
- Desktop packaging: implemented
- Android packaging: implemented
- iOS packaging: implemented
- OpenHarmony packaging: implemented
- Web packaging: not implemented yet

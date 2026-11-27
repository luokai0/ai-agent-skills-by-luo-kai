---
name: dora-studio-package-workflow
author: Tyrese Luo
source: dora-studio package.yml
date: 2026-02-04
tags: [deployment, github-actions, packaging, release, cargo-packager, cargo-makepad]
level: intermediate
makepad-branch: dev
---

# Dora Studio GitHub Actions packaging workflow

## Summary
CI workflow that creates a GitHub Release and packages desktop, Android, and iOS
artifacts using `makepad-packaging-action`.

## When to use
For multi-platform packaging in CI with optional release upload.

## Full workflow (verbatim)
```yaml
name: Build Makepad (All Platforms)

on:
  push:
    tags: ['v*']
  workflow_dispatch:
    inputs:
      build_desktop:
        description: "Build desktop packages"
        type: boolean
        default: true
      build_android:
        description: "Build Android APK"
        type: boolean
        default: true
      build_ios:
        description: "Build iOS app"
        type: boolean
        default: true
      release_tag:
        description: "Release tag (optional, supports __VERSION__)"
        type: string
        default: ""
      release_name:
        description: "Release name (optional, supports __VERSION__)"
        type: string
        default: ""
      release_body:
        description: "Release body (optional)"
        type: string
        default: ""
      release_draft:
        description: "Create draft release"
        type: boolean
        default: false
      prerelease:
        description: "Mark as prerelease"
        type: boolean
        default: false
      args:
        description: "Extra args passed to the action"
        type: string
        default: ""

permissions:
  contents: write

env:
  CARGO_TERM_COLOR: always

jobs:
  # Create release first (only once)
  create-release:
    name: Create Release
    runs-on: ubuntu-22.04
    outputs:
      release_tag: ${{ steps.get_tag.outputs.tag }}
      release_upload_url: ${{ steps.create_release.outputs.upload_url }}
      release_id: ${{ steps.create_release.outputs.id }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get tag
        id: get_tag
        run: |
          if [ "${{ github.event_name }}" = "push" ] && [ "${{ github.ref_type }}" = "tag" ]; then
            echo "tag=${{ github.ref_name }}" >> $GITHUB_OUTPUT
          elif [ -n "${{ inputs.release_tag }}" ]; then
            echo "tag=${{ inputs.release_tag }}" >> $GITHUB_OUTPUT
          else
            echo "tag=v$(date +'%Y%m%d%H%M%S')" >> $GITHUB_OUTPUT
          fi

      - name: Get release name
        id: get_name
        run: |
          if [ -n "${{ inputs.release_name }}" ]; then
            echo "name=${{ inputs.release_name }}" >> $GITHUB_OUTPUT
          else
            echo "name=Dora Studio ${{ steps.get_tag.outputs.tag }}" >> $GITHUB_OUTPUT
          fi

      - name: Create Release
        id: create_release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ steps.get_tag.outputs.tag }}
          name: ${{ steps.get_name.outputs.name }}
          body: |
            ${{ inputs.release_body != '' && inputs.release_body || '## Dora Studio Release

            ### Downloads
            See the assets below for platform-specific downloads.

            ### Platforms
            - macOS (Apple Silicon)
            - Linux (x86_64)
            - Windows (x86_64)
            - Android (arm64)
            - iOS (arm64)' }}
          draft: ${{ inputs.release_draft || false }}
          prerelease: ${{ inputs.prerelease || false }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  desktop:
    name: Desktop (${{ matrix.name }})
    needs: create-release
    if: ${{ always() && (github.event_name == 'push' || inputs.build_desktop) }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-22.04
            packager_formats: deb
            name: Linux
          - os: macos-14
            packager_formats: dmg
            name: macOS
          - os: windows-2022
            packager_formats: nsis
            name: Windows
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Install Linux dependencies
        if: startsWith(matrix.os, 'ubuntu')
        run: |
          sudo apt-get update
          sudo apt-get install libssl-dev pkg-config llvm clang libclang-dev binfmt-support libxcursor-dev libx11-dev libasound2-dev libpulse-dev libwayland-dev libxkbcommon-dev

      - name: Package (desktop)
        uses: Project-Robius-China/makepad-packaging-action@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          releaseId: ${{ needs.create-release.outputs.release_id }}
          args: ${{ inputs.args }}
          packager_formats: ${{ matrix.packager_formats }}

  android:
    name: Android
    needs: create-release
    if: ${{ always() && (github.event_name == 'push' || inputs.build_android) }}
    runs-on: ubuntu-22.04
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Package (android)
        uses: Project-Robius-China/makepad-packaging-action@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          releaseId: ${{ needs.create-release.outputs.release_id }}
          args: --target aarch64-linux-android ${{ inputs.args }}

  ios:
    name: iOS
    needs: create-release
    if: ${{ always() && (github.event_name == 'push' || inputs.build_ios) }}
    runs-on: macos-14
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Package (iOS)
        uses: Project-Robius-China/makepad-packaging-action@main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MAKEPAD_IOS_ORG: com.mofa
          MAKEPAD_IOS_APP: dora-studio
          APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
          APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
          APPLE_PROVISIONING_PROFILE: ${{ secrets.APPLE_PROVISIONING_PROFILE }}
          APPLE_KEYCHAIN_PASSWORD: ${{ secrets.APPLE_KEYCHAIN_PASSWORD }}
        with:
          releaseId: ${{ needs.create-release.outputs.release_id }}
          args: --target aarch64-apple-ios ${{ inputs.args }}
```

## Notes
- Desktop packages must run on matching OS runners.
- iOS builds require macOS runners.
- Android builds can run on any OS runner.

## Source
- https://github.com/dora-rs/dora-studio/blob/main/.github/workflows/package.yml

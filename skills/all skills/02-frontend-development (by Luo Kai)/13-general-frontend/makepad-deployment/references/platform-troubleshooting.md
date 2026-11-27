# Platform-Specific Troubleshooting

Common deployment issues and solutions for each platform.

## Desktop (Linux)

### Missing System Libraries

**Error**: `error while loading shared libraries: libxxx.so.x`

**Solution**:
```bash
# Common dependencies for Makepad on Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y \
    libssl-dev \
    libsqlite3-dev \
    pkg-config \
    binfmt-support \
    libxcursor-dev \
    libx11-dev \
    libasound2-dev \
    libpulse-dev
```

### Package Build Fails

**Symptom**: `cargo packager` fails with resource errors

**Checklist**:
1. Verify `robius-packaging-commands` version is 0.2.1
2. Ensure `before-packaging-command` path matches your binary name
3. Check `./dist/resources/` exists after running the command

---

## Desktop (macOS)

### Code Signing Issues

**Error**: "your-app is damaged and can't be opened"

**Solutions**:
1. For development, disable Gatekeeper:
   ```bash
   xattr -cr /path/to/your-app.app
   ```
2. For distribution, sign with Developer ID:
   ```toml
   [package.metadata.packager.macos]
   signing_identity = "Developer ID Application: Your Name (TEAMID)"
   ```

### Minimum macOS Version

**Error**: App won't launch on older macOS

**Solution**: Set minimum version in Cargo.toml:
```toml
[package.metadata.packager.macos]
minimum_system_version = "10.15"  # Catalina
```

---

## Desktop (Windows)

### NSIS Installer Issues

**Error**: NSIS build fails

**Solutions**:
1. Install NSIS: https://nsis.sourceforge.io/
2. Add NSIS to PATH
3. Use `--formats nsis` explicitly:
   ```bash
   cargo packager --release --formats nsis
   ```

### DLL Dependencies

**Symptom**: App starts but crashes with missing DLLs

**Solution**: Include Visual C++ Redistributable or static link:
```toml
[target.'cfg(target_os = "windows")'.dependencies]
# Link statically to avoid DLL dependencies
```

---

## Android

### NDK Not Found

**Error**: `NDK not found at expected location`

**Solution**:
```bash
# Reinstall with full NDK
cargo makepad android install-toolchain --full-ndk
```

### APK Install Fails

**Error**: `INSTALL_FAILED_NO_MATCHING_ABIS`

**Solution**: Build for correct architecture:
```bash
# ARM64 devices (most modern phones)
cargo makepad android build -p your-app --release
```

### Resource Loading Fails

**Symptom**: App crashes on startup with "resource not found"

**Checklist**:
1. Check `live_design!` uses correct resource paths
2. Verify resource files are in correct `src/` location
3. Check file names match (case-sensitive on Android)

---

## iOS

### Provisioning Profile Issues

**Error**: `No provisioning profile found`

**Solution**:
1. Create empty project in Xcode with same bundle ID
2. Run on device once to generate profile
3. Find profile path: `~/Library/MobileDevice/Provisioning Profiles/`
4. Get cert fingerprint: `security find-identity -v -p codesigning`

### Simulator vs Device Architecture

**Symptom**: Works on simulator, fails on device

**Solution**: Use correct target:
- Simulator: `run-sim` (arm64-apple-ios-sim)
- Device: `run-device` (arm64-apple-ios)

### App Store Submission

**Requirements**:
1. Create IPA:
   ```bash
   mkdir Payload
   cp -r your-app.app Payload/
   zip -r your-app.ipa Payload
   ```
2. Use App Store Connect / Transporter for upload
3. Ensure proper entitlements and signing

---

## Wasm

### Large Bundle Size

**Problem**: Wasm file too large (>10MB)

**Solutions**:
1. Use release profile with LTO:
   ```toml
   [profile.release]
   lto = "thin"
   opt-level = "z"  # Optimize for size
   ```
2. Use `wasm-opt` for additional optimization:
   ```bash
   wasm-opt -Oz -o output.wasm input.wasm
   ```

### Audio Not Working

**Symptom**: No sound in browser

**Solution**: Audio requires user interaction first (browser security).
Add a "Start" button that initiates audio context.

### CORS Errors

**Error**: `Cross-Origin Request Blocked`

**Solution**: Configure server with proper CORS headers:
```
Access-Control-Allow-Origin: *
Content-Type: application/wasm
```

---

## Common Issues (All Platforms)

### Resources Not Found

**Symptom**: "Failed to load resource: makepad_widgets/..."

**Checklist**:
1. Ensure all required resources in Cargo.toml `resources`:
   - makepad_widgets
   - makepad_fonts_* (if using Chinese/Emoji fonts)
   - Your app resources
2. Verify paths match actual file locations

### Release vs Debug Differences

**Symptom**: Works in debug, fails in release

**Common Causes**:
1. Optimization removes required code (check `#[inline(never)]`)
2. Release build uses different resource paths
3. Debug logging masks timing issues

### Font Rendering Issues

**Symptom**: Text displays as boxes or wrong characters

**Solutions**:
1. Include appropriate font resources:
   - `makepad_fonts_chinese_bold` / `regular` for Chinese
   - `makepad_fonts_emoji` for emoji support
2. Verify font files are in resources array
3. Check font file integrity (not corrupted during packaging)

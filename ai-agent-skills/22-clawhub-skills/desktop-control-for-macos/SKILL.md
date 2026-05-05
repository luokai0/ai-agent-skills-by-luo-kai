---
name: desktop-control-for-macos
description: Generic macOS desktop control using AppleScript for app and window semantics plus screenshot, OCR, mouse, and keyboard workflows.
---

# 写在前面

特别做了中文兼容，包括文字输入/识别等，中文用户放心使用～

# macos-desktop-control

This skill controls the macOS desktop through a small, explicit pipeline with a clear split between semantic app control and visual UI control:

## Features

### 🖥️ App and window control

- ✅ Activate an app by name or bundle path
- ✅ Check whether an app is running
- ✅ Read the current frontmost app
- ✅ Read front window title, count windows, and list window titles

### 📸 Screenshot and image operations

- ✅ Capture the current screen as a logical-resolution screenshot
- ✅ Initialize screenshot-to-click calibration for macOS Retina displays
- ✅ Crop a known rectangular region from an image
- ✅ Reuse calibration data when a workflow must mix logical and raw screenshots

### 🎯 Visual target location

- ✅ Locate text by OCR on screenshots
- ✅ Locate templates by OpenCV image matching
- ✅ Constrain later actions to coordinates derived from a screenshot

### ⌨️ Mouse and keyboard control

- ✅ Move the mouse in logical screen coordinates
- ✅ Left click, right click, double click, and drag
- ✅ Read current mouse position
- ✅ Type text, paste via higher-level workflows, press keys, and send hotkeys
- ✅ Hold and release keys explicitly when needed

### 🛡️ Safety and scope

- ✅ Use logical coordinates as the default working convention
- ✅ Keep app-specific UI semantics out of this skill
- ✅ Keep AppleScript usage limited to app and window semantics, not deep UI scripting
- ✅ Keep `pyautogui.FAILSAFE = True` so moving to the top-left corner aborts automation

1. Use AppleScript for app and window semantics
2. Initialize coordinate mapping
3. Capture the screen
4. Locate targets by OCR or OpenCV image matching
5. Execute mouse and keyboard actions with Python

## Design boundary

This skill intentionally does not include AppleScript UI scripting.

Use AppleScript for:
- opening or activating apps
- reading frontmost app state
- reading window titles and counts

Use screenshot-guided OCR/OpenCV plus `pyautogui` for:
- clicking UI targets
- typing into custom-drawn interfaces
- interacting with chat rows, images, canvases, or other visually defined targets

This boundary keeps the skill predictable. AppleScript is used where semantic macOS state is strong, and `pyautogui` is used where direct UI manipulation is more reliable.

## Why initialization is needed

On macOS, screenshot coordinates and click coordinates may use different coordinate systems.

- `screencapture` images usually use pixel coordinates.
- Mouse automation tools often use macOS screen coordinates, also called point coordinates.
- On Retina displays, one point is commonly equal to two pixels.

This skill writes the coordinate mapping result to a JSON file, so later steps can reuse it without recalculating.

Initialization behavior in the current version:
- the skill auto-initializes on first use when the calibration file does not exist
- it does not re-run mapping on every invocation
- if `/tmp/macos_desktop_control/calibration.json` already exists, the existing calibration is reused

Default calibration file:

```bash
/tmp/macos_desktop_control/calibration.json
```

## Directory layout

```text
macos-desktop-control/
  SKILL.md
  requirements.txt
  scripts/
    calibration.py
    init_coordinate_mapping.py
    capture_screen.py
    crop_image.py
    locate_text_ocr.py
    locate_image_opencv.py
    mouse.py
    keyboard.py
    applescript_app.py
    applescript_window.py
```

## Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```

OCR uses Apple Vision through PyObjC, so no separate Tesseract install is required.

On macOS, grant the terminal or runtime app these permissions:

- Screen Recording
- Accessibility

## 1. Initialize coordinate mapping

The first version handles Retina screens by comparing screenshot pixel size with the logical screen size used by `pyautogui`.

You can still run initialization manually:

```bash
python scripts/init_coordinate_mapping.py
```

But in normal use, the skill now performs lazy initialization automatically on first use if the calibration file is missing.

Example output:

```json
{
  "screen_width_points": 1512,
  "screen_height_points": 982,
  "screenshot_width_pixels": 3024,
  "screenshot_height_pixels": 1964,
  "scale_x": 2.0,
  "scale_y": 2.0,
  "mode": "retina"
}
```

Later scripts read this file automatically.

Current lazy-init behavior:
- `capture_screen.py`
- `mouse.py`
- `locate_text_ocr.py`
- `locate_image_opencv.py`

These scripts first check whether `/tmp/macos_desktop_control/calibration.json` exists.
If not, they auto-generate it once and then continue.

## 2. Capture screen

Capture the current screen and resize the image into the logical coordinate system used by `pyautogui.position()` and `pyautogui.click()`.

This skill's default convention is:
- default screenshot is logical
- default recognition result coordinates are logical
- default mouse action coordinates are logical
- default crop operations should use a logical screenshot
- only use calibration conversion when a workflow explicitly mixes logical screenshots with raw pixel screenshots

```bash
python scripts/capture_screen.py --output /tmp/macos_desktop_control/screen_logical.png
```

Core idea:

```python
import pyautogui

img = pyautogui.screenshot()
screen_w, screen_h = pyautogui.size()

# Resize screenshot to the coordinate system used by pyautogui.position() / click().
img = img.resize((screen_w, screen_h))
img.save("screen_logical.png")
```

## 3. Crop image regions

When a higher-level skill already knows a target rectangle, crop it directly instead of re-opening previews or re-running visual search.

By default, crop from a logical screenshot so the crop rectangle stays in the same coordinate system as recognition and mouse targeting.
Only crop from a raw Retina or pixel screenshot when there is a specific reason to preserve raw pixels, and in that case convert coordinates first using calibration data.

```bash
python scripts/crop_image.py \
  --image /tmp/macos_desktop_control/screen_logical.png \
  --x1 400 --y1 300 --x2 700 --y2 650 \
  --output /tmp/macos_desktop_control/crop.png
```

Use this for:
- extracting a detected chat image thumbnail
- saving a button or dialog region for later analysis
- debugging screenshot-to-action pipelines

## 4. Locate targets

There are two supported strategies.

### Locate by OCR text

```bash
python scripts/locate_text_ocr.py \
  --image /tmp/macos_desktop_control/screen_logical.png \
  --text "确定"
```

You can also constrain OCR to a specific screen region when the same text may appear in multiple places:

```bash
python scripts/locate_text_ocr.py \
  --image /tmp/macos_desktop_control/screen_logical.png \
  --text "会话" \
  --x1 0 --y1 120 --x2 520 --y2 1107
```

The script prints the center point of the best matched Apple Vision OCR box.
When a region is provided, the search runs only inside that rectangle, but the returned coordinates are still in full-screen logical coordinates.

### Locate by OpenCV image matching

```bash
python scripts/locate_image_opencv.py \
  --image /tmp/macos_desktop_control/screen_logical.png \
  --template ./target_button.png \
  --threshold 0.8
```

The script prints the center point of the matched template.

### Locate by semantic understanding

精确匹配（OpenCV 模板匹配、OCR 文字定位）覆盖不了的目标，可以用 AI 图像理解来处理。

适合交给 AI 判断的场景通常具有以下特征：形态不固定、没有现成模板、需要结合画面上下文、或者只能用语义词汇描述。

典型场景举例：
- 画面中有多个可点击区域，需要判断哪个是当前目标
- 目标没有固定文字或图标模板，但可以用语义描述
- 需要理解画面中各元素之间的关系（谁在说话、某块区域的含义）

操作流程与上述两种方式一致：截图 → crop 限定区域（如需要）→ AI 识别 → 坐标映射 → 动作执行。本 skill 负责截图和坐标转换，识别结果由调用者解读并决定后续动作。

## 5. Mouse actions

Use Python and `pyautogui` to control the mouse in logical screen coordinates.

### Single click

```bash
python scripts/mouse.py --action click --x 500 --y 300
```

### Move only

```bash
python scripts/mouse.py --action move --x 500 --y 300 --duration 0.2
```

### Double click

```bash
python scripts/mouse.py --action double-click --x 500 --y 300
```

### Right click

```bash
python scripts/mouse.py --action right-click --x 500 --y 300
```

### Drag

```bash
python scripts/mouse.py --action drag --x 500 --y 300 --to-x 800 --to-y 500 --duration 0.3
```

### Read current mouse position

```bash
python scripts/mouse.py --action position
```

You can also pipe the result from a locate script:

```bash
python scripts/locate_image_opencv.py \
  --image /tmp/macos_desktop_control/screen_logical.png \
  --template ./target_button.png \
| python scripts/mouse.py --stdin --action click
```

Stdin accepts either `x y` text or JSON like `{"x": 500, "y": 300}`.

## 6. Keyboard actions

Use Python and `pyautogui` to paste text or trigger shortcuts.

Important practical note:
- this skill uses clipboard paste for all text entry by default, including English
- this avoids input-method issues with Chinese, English, and mixed-language text
- do not use simulated typing for text entry in this skill

### Paste text

```bash
python scripts/keyboard.py --action paste --text "我是OpenClaw"
```

### Paste from stdin

```bash
printf '我是OpenClaw' | python scripts/keyboard.py --action paste --stdin
```

Default input rule for this skill:
- use clipboard paste for all text input by default, including English
- click the verified input field first, then paste with `command v`
- do not use simulated typing for text entry in this skill

### Press one key

```bash
python scripts/keyboard.py --action press --key enter
```

### Press a hotkey

```bash
python scripts/keyboard.py --action hotkey --keys command v
```

Recommended paste workflow when text fidelity matters:
1. copy the exact text into the clipboard, preferably via `python scripts/keyboard.py --action paste`
2. click the verified input field
3. let the script send `command v` to paste
4. verify visually before pressing enter if sending would be externally visible

### Hold and release keys

```bash
python scripts/keyboard.py --action key-down --key shift
python scripts/keyboard.py --action key-up --key shift
```

## 7. AppleScript app control

Use AppleScript when the task is semantic macOS control rather than visual targeting.

Good fits:
- open or activate an app
- check whether an app is running
- read the current frontmost app

### Open by app name

```bash
python scripts/applescript_app.py --action open --app "微信"
```

### Open by bundle path

```bash
python scripts/applescript_app.py --action open --path "/Applications/微信.app"
```

### Activate an app

```bash
python scripts/applescript_app.py --action activate --app "微信"
```

### Check whether an app is running

```bash
python scripts/applescript_app.py --action is-running --app "微信"
```

### Get the current frontmost app

```bash
python scripts/applescript_app.py --action frontmost-app
python scripts/applescript_app.py --action frontmost-app --json-pretty
```

## 8. AppleScript window inspection

Use AppleScript window inspection when you need app-level UI state without relying on OCR.

Good fits:
- read the front window title
- count windows for a process
- list window titles for a process

### Read the front window title

```bash
python scripts/applescript_window.py --action title --app "微信"
```

### Count windows

```bash
python scripts/applescript_window.py --action count --app "微信"
```

### List window titles

```bash
python scripts/applescript_window.py --action list --app "微信"
python scripts/applescript_window.py --action title --app "微信" --json-pretty
```

## 9. When to use AppleScript vs desktop vision

Prefer AppleScript for:
- opening or activating apps
- reading window titles
- checking the frontmost app
- simple app and process state queries

Do not add AppleScript UI scripting here for button clicks or deep accessibility-tree automation. That path is intentionally excluded from this skill.

Prefer screenshot + OCR/OpenCV + pyautogui for:
- buttons or labels that only exist visually
- apps with weak or unstable accessibility hierarchies
- targets inside custom-drawn UIs such as chat rows, images, or canvas content
- direct manipulation such as clicking, dragging, and typing into app surfaces

When the same text may appear in multiple places, do not search the full screen by default.
Constrain OCR to the intended region first, then click using the returned full-screen logical coordinates.

A practical sequence is often:
1. AppleScript activates the app
2. AppleScript reads window or process state
3. screenshot-based vision finds the target
4. mouse or keyboard automation performs the action
5. AppleScript or a fresh screenshot verifies the result

## 10. Recommended flow

```bash
python scripts/applescript_app.py --action activate --app "微信"
python scripts/applescript_window.py --action title --app "微信"
python scripts/init_coordinate_mapping.py
python scripts/capture_screen.py
python scripts/locate_text_ocr.py --text "确定"
python scripts/mouse.py --action click --x 500 --y 300
python scripts/keyboard.py --action press --key enter
```

## Notes

- Version 1 assumes a Retina display and single primary screen.
- Treat logical screenshots as the default working surface for this skill.
- Treat recognition output coordinates as logical unless a script explicitly says otherwise.
- Treat mouse and keyboard targeting as logical by default.
- Treat crop rectangles as logical by default, and prefer cropping from a logical screenshot.
- If another skill mixes logical screenshots with raw Retina or pixel screenshots, use calibration conversion deliberately. Do not assume logical bounds match raw pixel bounds 1:1.
- Keep this skill focused on generic desktop primitives. App-specific UI semantics, business rules, and event pipelines should stay in the higher-level app skill.
- All click, drag, move, and typing actions use Python / `pyautogui`.
- AppleScript support in this skill is limited to app control and window inspection.
- For safety, keep `pyautogui.FAILSAFE = True`; moving the mouse to the top-left corner aborts automation.

#!/bin/bash
# Post-Bash hook for makepad-skills
# Triggers: Self-correction on compilation errors
# Enhanced: Automatically instructs Claude to load relevant skills

TOOL_OUTPUT="$1"
EXIT_CODE="$2"

# Only process if command failed
if [ "$EXIT_CODE" = "0" ]; then
    exit 0
fi

# Check for common Makepad errors in output
check_makepad_errors() {
    local output="$1"

    # Apply error: no matching field (DSL property errors)
    if echo "$output" | grep -q "Apply error: no matching field"; then
        # Extract the field name if possible
        FIELD_NAME=$(echo "$output" | grep -oE "no matching field: [a-z_]+" | head -1 | sed 's/no matching field: //')
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Apply error - no matching field${FIELD_NAME:+: $FIELD_NAME}" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-reference' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] The property may have been renamed or moved in recent Makepad versions." >&2
        echo "[makepad-skills:auto-fix] Common fixes:" >&2
        echo "[makepad-skills:auto-fix]   - border_color_* → Check if moved to draw_bg: { border_color: ... }" >&2
        echo "[makepad-skills:auto-fix]   - hover_* / pressed_* → Use animator states instead" >&2
        echo "[makepad-skills:auto-fix]   - font / font_size → Use text_style: { font_size: X }" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Font-related errors
    if echo "$output" | grep -q "no matching field: font"; then
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Font field error" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-font' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] FIX: Use 'text_style: { font_size: X }' instead of 'font:'" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Color parse error (hex ending with 'e')
    if echo "$output" | grep -q "expected at least one digit in exponent"; then
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Color parse error (hex ending with 'e')" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-shaders' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] FIX: Change the last hex digit to avoid 'e' (e.g., #ff000e → #ff000f)" >&2
        echo "[makepad-skills:auto-fix] REASON: Makepad parser interprets 'e' as scientific notation" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Borrow checker errors
    if echo "$output" | grep -q "cannot borrow.*as mutable because it is also borrowed as immutable"; then
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Borrow checker conflict" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'robius-widget-patterns' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] FIX: Separate read and write phases with explicit scope blocks" >&2
        echo "[makepad-skills:auto-fix] Example:" >&2
        echo "[makepad-skills:auto-fix]   let data = { widget.data().clone() };  // read phase" >&2
        echo "[makepad-skills:auto-fix]   widget.update(cx, data);               // write phase" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Method not found
    if echo "$output" | grep -q "no method named.*found"; then
        METHOD_NAME=$(echo "$output" | grep -oE "no method named \`[a-z_]+\`" | head -1 | sed 's/no method named `//;s/`//')
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Method not found${METHOD_NAME:+: $METHOD_NAME}" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-reference' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] The API may have changed in recent Makepad versions." >&2
        echo "[makepad-skills:auto-fix] Check the skill for current method signatures." >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Missing cx parameter
    if echo "$output" | grep -q 'argument.*of type.*&mut Cx.*is missing'; then
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Missing cx parameter" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-event-action' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] FIX: Most Makepad methods require 'cx: &mut Cx' as first argument" >&2
        echo "[makepad-skills:auto-fix] Example: widget.redraw(cx) not widget.redraw()" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Animator/state errors
    if echo "$output" | grep -qE "animator|no matching field:.*(hover|pressed|focus)"; then
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Animator/state related error" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-animation' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] Hover/pressed/focus states should use animator system." >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi

    # Layout errors
    if echo "$output" | grep -qE "no matching field:.*(width|height|margin|padding|flow|align)"; then
        echo "" >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
        echo "[makepad-skills:auto-fix] DETECTED: Layout property error" >&2
        echo "[makepad-skills:auto-fix] ───────────────────────────────────────────────" >&2
        echo "[makepad-skills:auto-fix] ACTION REQUIRED: Load 'makepad-layout' skill using Skill tool" >&2
        echo "[makepad-skills:auto-fix] Check current layout property syntax in the skill." >&2
        echo "[makepad-skills:auto-fix] ═══════════════════════════════════════════════" >&2
    fi
}

# Only check if this looks like a cargo/makepad command output
if echo "$TOOL_OUTPUT" | grep -qE "(error\[E|warning:|Compiling|Building|Apply error)"; then
    check_makepad_errors "$TOOL_OUTPUT"
fi

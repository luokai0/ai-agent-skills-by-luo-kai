---
name: makepad-api-docs
description: Index of Makepad API documentation and guidance for finding detailed references.
---

# Makepad API Documentation Reference

This skill provides navigation to official Makepad documentation. Use WebFetch tool to retrieve specific documentation when needed.

## Official Documentation

**Base URL**: https://publish.obsidian.md/makepad-docs/

### Documentation Structure

| Section | URL | Content |
|---------|-----|---------|
| **Introduction** | [Makepad Introduction](https://publish.obsidian.md/makepad-docs/Makepad+Introduction) | Framework overview, getting started |
| **DSL** | [DSL Introduction](https://publish.obsidian.md/makepad-docs/DSL/Introduction) | live_design! syntax, layout, styling |
| **Tutorials** | [Image Viewer](https://publish.obsidian.md/makepad-docs/Tutorials/Image+Viewer/0+-+Introduction) | Complete step-by-step tutorial |

### Key Documentation Pages

#### DSL & Layout
- `DSL/Introduction` - live_design! macro basics
- `DSL/Layout` - Flow, Walk, sizing
- `DSL/Styling` - Colors, fonts, draw properties

#### Widgets
- `Widgets/Button` - Button widget API
- `Widgets/Label` - Label widget API
- `Widgets/TextInput` - Text input handling
- `Widgets/View` - Container layout

#### Events & Actions
- `Events/Hit` - Hit testing, finger events
- `Events/Actions` - Widget action system
- `Events/Keyboard` - Key handling

#### Graphics
- `Graphics/Sdf2d` - SDF shape drawing
- `Graphics/Shaders` - Custom shader syntax
- `Graphics/Animation` - Animator system

---

## How to Use External Docs

### For AI Agents (Claude Code)

When you need detailed API information not in skills:

```
1. Use WebFetch tool to retrieve documentation:
   WebFetch(url: "https://publish.obsidian.md/makepad-docs/DSL/Layout",
            prompt: "Extract layout properties and examples")

2. Note: Obsidian Publish loads content dynamically,
   WebFetch may get partial content. Fall back to inline skills.
```

### Recommended Workflow

1. **First**: Check inline skills (this repository)
2. **Second**: Use WebFetch for specific API details
3. **Third**: Search makepad GitHub examples
4. **Fourth**: Check makepad-widgets source code

---

## Quick API Reference (Inline)

### Layout Properties

```rust
// Flow direction
flow: Down       // Vertical (column)
flow: Right      // Horizontal (row)
flow: Overlay    // Stack on top

// Sizing
width: Fill      // Fill available space
width: Fit       // Shrink to content
width: 100.0     // Fixed pixels
width: All       // Fill both directions

// Spacing
padding: 10.0                    // All sides
padding: {left: 10, top: 5}      // Specific sides
margin: {left: 10, right: 10}    // Outer spacing
spacing: 8.0                     // Gap between children

// Alignment
align: {x: 0.5, y: 0.5}         // Center
align: {x: 0.0, y: 0.0}         // Top-left
align: {x: 1.0, y: 1.0}         // Bottom-right
```

### Common Widget Properties

```rust
// Button
<Button> {
    text: "Click me"
    draw_bg: { color: #4A90D9 }
    draw_text: { color: #ffffff }
}

// Label
<Label> {
    text: "Hello"
    draw_text: {
        text_style: <THEME_FONT_REGULAR>{ font_size: 14.0 }
        color: #ffffff
    }
}

// TextInput
<TextInput> {
    text: "Default value"
    draw_bg: { color: #2a2a38 }
    draw_text: { color: #ffffff }
    draw_cursor: { color: #4A90D9 }
    draw_selection: { color: #4A90D944 }
}

// View (Container)
<View> {
    flow: Down
    spacing: 10
    padding: 20
    draw_bg: { color: #1a1a2e }
}

// RoundedView
<RoundedView> {
    draw_bg: {
        color: #2a2a38
        radius: 8.0
    }
}
```

### Event Handling

```rust
// Hit testing
match event.hits(cx, self.draw_bg.area()) {
    Hit::FingerDown(e) => { /* Click start */ }
    Hit::FingerUp(e) => { /* Click end, check e.is_over */ }
    Hit::FingerMove(e) => { /* Drag */ }
    Hit::FingerHoverIn(_) => { /* Mouse enter */ }
    Hit::FingerHoverOut(_) => { /* Mouse leave */ }
    Hit::KeyDown(e) => { /* Key press */ }
    _ => {}
}

// Action casting
if self.button(ids!(my_btn)).clicked(actions) {
    // Handle click
}

if let Some(text) = self.text_input(ids!(input)).changed(actions) {
    // Handle text change
}
```

### Animator

```rust
animator: {
    hover = {
        default: off
        on = {
            redraw: true
            from: {all: Forward {duration: 0.15}}
            ease: ExpDecay {d1: 0.80, d2: 0.97}
            apply: { draw_bg: {opacity: 1.0} }
        }
        off = {
            from: {all: Forward {duration: 0.1}}
            apply: { draw_bg: {opacity: 0.7} }
        }
    }
}

// In handle_event
self.animator_handle_event(cx, event);
self.animator_play(cx, ids!(hover.on));
```

### Shader Instance Variables

```rust
draw_bg: {
    // Declare instance variable
    instance hover: 0.0
    instance progress: 0.0

    fn pixel(self) -> vec4 {
        let color = mix(#333, #4A90D9, self.hover);
        return color;
    }
}

// Update from Rust
self.draw_bg.apply_over(cx, live!{
    hover: 1.0
});
```

---

## Source Code References

When documentation is insufficient, check source code:

| Component | GitHub Path |
|-----------|-------------|
| Widgets | `makepad/makepad/widgets/src/` |
| Button | `widgets/src/button.rs` |
| Label | `widgets/src/label.rs` |
| TextInput | `widgets/src/text_input.rs` |
| View | `widgets/src/view.rs` |
| Theme | `widgets/src/theme_desktop_dark.rs` |
| Examples | `makepad/makepad/examples/` |
| ui_zoo | `examples/ui_zoo/` (widget gallery) |

### GitHub Search Patterns

```bash
# Find widget implementation
site:github.com/makepad/makepad "impl Widget for Button"

# Find event handling pattern
site:github.com/makepad/makepad "Hit::FingerDown"

# Find specific property usage
site:github.com/makepad/makepad "draw_bg:" "radius"
```

---

## When to Fetch External Docs

| Situation | Action |
|-----------|--------|
| Common widget usage | Use inline skills (this file) |
| Specific property details | WebFetch official docs |
| Complex widget (PortalList, etc.) | Check GitHub source |
| Latest API changes | Check GitHub commits |
| Tutorial/walkthrough | Fetch Obsidian docs |

---

## Related Skills

- [Troubleshooting](./troubleshooting.md) - Common errors and fixes
- [UI Constraints](../01-core/_base/08-ui-constraints.md) - Best practices
- [Graphics Skills](../03-graphics/SKILL.md) - Shader and animation
- [Patterns](../04-patterns/SKILL.md) - Production patterns

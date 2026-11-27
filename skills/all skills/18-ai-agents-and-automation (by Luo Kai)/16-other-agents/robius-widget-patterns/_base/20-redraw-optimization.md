---
name: makepad-redraw-optimization
author: robius
source: robrix
date: 2024-01-12
tags: [redraw, performance, optimization, animation, visibility]
level: intermediate
---

# Pattern 15: Redraw Optimization

Efficient redraw patterns to avoid unnecessary GPU work and improve performance.

## Problem

Calling `redraw()` after every state change causes:
- Unnecessary GPU work
- UI flicker
- Poor performance with complex widget trees

## Solution

Use conditional redraws, batch updates, and leverage animator auto-redraw.

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Conditional redraw** | Only redraw when visual state actually changes |
| **Batch updates** | Multiple mutations, single redraw at end |
| **Animator-driven** | Let animations handle their own redraws |
| **Separate concerns** | Update methods without redraw, caller decides |

## Pattern 1: Conditional Redraw

Only redraw when state actually changes:

```rust
pub fn update_visibility(&mut self, cx: &mut Cx, should_show: bool) {
    let was_visible = self.visible;  // Store previous state

    self.visible = should_show;
    self.view(ids!(content)).set_visible(cx, should_show);

    // Only redraw if visibility actually changed
    if self.visible != was_visible {
        self.redraw(cx);
    }
}
```

## Pattern 2: Separate Update and Redraw

Create update methods that don't redraw:

```rust
impl MyWidget {
    /// Updates state WITHOUT redrawing. Caller must redraw.
    pub fn update_state(&mut self, cx: &mut Cx, new_value: String) {
        self.value = new_value;
        self.label(ids!(display)).set_text(cx, &self.value);
        // NOTE: No redraw here - caller decides when
    }

    /// Updates state AND redraws.
    pub fn set_value(&mut self, cx: &mut Cx, new_value: String) {
        self.update_state(cx, new_value);
        self.redraw(cx);
    }
}

// Usage: batch multiple updates
widget.update_state(cx, "value1");
widget.update_other(cx, 42);
widget.redraw(cx);  // Single redraw for all updates
```

## Pattern 3: Animator-Driven Redraw

Let animations auto-handle redraws:

```rust
live_design! {
    MyPanel = {{MyPanel}} {
        animator: {
            panel = {
                default: hide,
                show = {
                    redraw: true,  // Auto redraw during animation
                    from: {all: Forward {duration: 0.3}}
                    ease: ExpDecay {d1: 0.80, d2: 0.97}
                    apply: { draw_bg: {opacity: 1.0} }
                }
                hide = {
                    redraw: true,  // Auto redraw during animation
                    from: {all: Forward {duration: 0.2}}
                    apply: { draw_bg: {opacity: 0.0} }
                }
            }
        }
    }
}
```

## Pattern 4: Check Animator State

Only redraw when animator requires it:

```rust
fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
    let animator_action = self.animator_handle_event(cx, event);

    // Only redraw if animation needs it
    if animator_action.must_redraw() {
        self.redraw(cx);
    }

    // Check if animation finished
    if self.animator_in_state(cx, ids!(panel.hide)) {
        if self.is_animating_out && !animator_action.is_animating() {
            // Animation completed
            self.visible = false;
            self.redraw(cx);
            return;
        }
    }
}
```

## Pattern 5: Batch Updates Before Redraw

```rust
fn handle_actions(&mut self, cx: &mut Cx, actions: &Actions) {
    let mut needs_redraw = false;

    // Process multiple actions
    if self.button(ids!(btn1)).clicked(actions) {
        self.state1 = true;
        needs_redraw = true;
    }

    if self.button(ids!(btn2)).clicked(actions) {
        self.state2 = false;
        needs_redraw = true;
    }

    if let Some(text) = self.text_input(ids!(input)).changed(actions) {
        self.value = text;
        needs_redraw = true;
    }

    // Single redraw for all changes
    if needs_redraw {
        self.redraw(cx);
    }
}
```

## Pattern 6: Visibility Changes

Always redraw after visibility changes:

```rust
pub fn show(&mut self, cx: &mut Cx) {
    self.visible = true;
    self.view(ids!(content)).set_visible(cx, true);
    cx.set_key_focus(self.view.area());
    self.redraw(cx);  // MUST redraw after visibility
}

pub fn hide(&mut self, cx: &mut Cx) {
    self.visible = false;
    self.view(ids!(content)).set_visible(cx, false);
    self.redraw(cx);  // MUST redraw after visibility
}
```

## Pattern 7: Deferred Expensive Operations

For expensive operations, defer and batch:

```rust
impl RoomsList {
    // Don't auto-apply filter on every change
    #[rust] display_filter: RoomDisplayFilter,
    #[rust] filter_dirty: bool,

    pub fn set_filter(&mut self, filter: RoomDisplayFilter) {
        self.display_filter = filter;
        self.filter_dirty = true;
        // Don't apply yet - wait for explicit call
    }

    pub fn apply_filter_if_needed(&mut self, cx: &mut Cx) {
        if self.filter_dirty {
            self.filter_dirty = false;
            self.apply_filter();  // Expensive operation
            self.redraw(cx);
        }
    }
}
```

## Anti-Patterns to Avoid

### 1. Unconditional Redraw
```rust
// BAD: Redraws even if nothing visual changed
fn update(&mut self, cx: &mut Cx) {
    self.internal_counter += 1;
    self.redraw(cx);  // Unnecessary if counter not displayed
}
```

### 2. Multiple Sequential Redraws
```rust
// BAD: Multiple redraws
fn setup(&mut self, cx: &mut Cx) {
    self.set_title(cx, "Hello");
    self.redraw(cx);  // Redraw 1
    self.set_subtitle(cx, "World");
    self.redraw(cx);  // Redraw 2
    self.set_icon(cx, icon);
    self.redraw(cx);  // Redraw 3
}

// GOOD: Single redraw
fn setup(&mut self, cx: &mut Cx) {
    self.set_title(cx, "Hello");
    self.set_subtitle(cx, "World");
    self.set_icon(cx, icon);
    self.redraw(cx);  // Single redraw
}
```

### 3. Forgetting Redraw After set_visible
```rust
// BAD: Visibility not reflected
self.view(ids!(panel)).set_visible(cx, false);
// Missing redraw!

// GOOD
self.view(ids!(panel)).set_visible(cx, false);
self.redraw(cx);
```

## When to Redraw

| Situation | Redraw? |
|-----------|---------|
| State change affecting display | Yes |
| Internal state (not displayed) | No |
| After `set_visible()` | Yes |
| After `set_text()` | Yes |
| Animation start/stop | Yes (or use `redraw: true` in animator) |
| After animator action | Only if `must_redraw()` |
| Multiple updates | Batch, then single redraw |

## Performance Tips

1. **Use `redraw: true` in animator** - Auto-handles animation frames
2. **Store previous state** - Compare before redrawing
3. **Separate update methods** - Let caller batch redraws
4. **Defer expensive operations** - Mark dirty, apply on demand
5. **Check `must_redraw()`** - Don't redraw unnecessarily during animations

## References

- [Robrix editing_pane.rs](https://github.com/project-robius/robrix/blob/main/src/home/editing_pane.rs)
- [Robrix jump_to_bottom_button.rs](https://github.com/project-robius/robrix/blob/main/src/shared/jump_to_bottom_button.rs)

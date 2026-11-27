# Pattern 18: Drag-and-Drop Widget Reordering

<!-- Evolution: 2025-01-13 | source: flex-layout-demo | author: dorobot -->

Implement drag-and-drop reordering of widgets with visual preview and physical layout changes.

## Problem

Need to allow users to drag widgets between containers (e.g., moving windows between rows) with:
- Visual feedback during drag (drop preview)
- Physical layout changes (rows resize based on content)
- Proper event handling that works across widget boundaries

## Solution

Use a combination of:
1. **Per-row assignment tracking** instead of flat ordering
2. **`hits_with_capture_overload`** to capture events during drag
3. **Deferred visual updates** via `needs_visual_update` flag
4. **Dynamic slot assignment** where each row has excess slots

## Key Insight

**`hits_with_capture_overload(cx, area, true)`** allows a widget to receive mouse events even when the cursor moves outside its original hit area - essential for drag operations that cross widget boundaries.

## live_design!

```rust
live_design! {
    use link::theme::*;
    use link::widgets::*;

    // Draggable item with drag handle
    DraggableItem = {{DraggableItem}} {
        width: Fill
        height: Fill

        flow: Down

        title_bar = <View> {
            width: Fill
            height: 28
            flow: Right
            align: { y: 0.5 }

            // Drag handle - 6 dots pattern
            drag_handle = <View> {
                width: 16
                height: 20
                cursor: Hand
                // Draw dots in shader...
            }

            title = <Label> { text: "Item" }
        }

        content = <View> { /* content here */ }
    }

    // Container with drop preview support
    DragContainer = {{DragContainer}} {
        width: Fill
        height: Fill

        // Semi-transparent overlay for drop preview
        drop_preview: {
            draw_depth: 10.0
            color: #4080c080
        }

        // Rows with excess slots for flexibility
        container = <View> {
            flow: Down

            row1 = <View> {
                flow: Right
                s1_1 = <DraggableItem> {}
                s1_2 = <DraggableItem> {}
                s1_3 = <DraggableItem> {}
                // ... up to 9 slots per row
            }
            // ... more rows
        }
    }
}
```

## Rust Implementation

### Action Enum

```rust
/// Actions emitted during drag operations
#[derive(Clone, Debug, DefaultNone)]
pub enum DragAction {
    /// Drag started - emitted when threshold exceeded
    StartDrag(usize),  // item_id
    None,
}
```

### Draggable Item

```rust
#[derive(Live, LiveHook, Widget)]
pub struct DraggableItem {
    #[deref]
    view: View,

    #[rust]
    item_id: usize,

    #[rust]
    is_dragging: bool,

    #[rust]
    drag_start: DVec2,

    /// Deferred visual update flag
    #[rust]
    needs_visual_update: bool,
}

impl Widget for DraggableItem {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
        self.view.handle_event(cx, event, scope);

        let drag_handle = self.view.view(id!(title_bar.drag_handle));

        match event.hits(cx, drag_handle.area()) {
            Hit::FingerDown(fe) => {
                self.is_dragging = false;
                self.drag_start = fe.abs;
            }
            Hit::FingerMove(fe) => {
                // 10-pixel threshold prevents accidental drags
                let dist = (fe.abs - self.drag_start).length();
                if !self.is_dragging && dist > 10.0 {
                    self.is_dragging = true;
                    cx.widget_action(
                        self.widget_uid(),
                        &scope.path,
                        DragAction::StartDrag(self.item_id),
                    );
                }
            }
            Hit::FingerUp(_) => {
                self.is_dragging = false;
            }
            _ => {}
        }
    }

    fn draw_walk(&mut self, cx: &mut Cx2d, scope: &mut Scope, walk: Walk) -> DrawStep {
        // Apply deferred visual updates in draw phase
        self.apply_visual_update(cx);
        self.view.draw_walk(cx, scope, walk)
    }
}

impl DraggableItem {
    pub fn set_item_id(&mut self, cx: &mut Cx, id: usize) {
        if self.item_id == id { return; }
        self.item_id = id;
        self.needs_visual_update = true;
        self.view.redraw(cx);
    }

    fn apply_visual_update(&mut self, cx: &mut Cx2d) {
        if !self.needs_visual_update { return; }
        self.needs_visual_update = false;

        // Apply visual changes based on item_id
        let colors = [/* distinct colors */];
        let color = colors[self.item_id % colors.len()];

        self.view.apply_over(cx, live! {
            draw_bg: { color: (color) }
        });

        self.view.label(id!(title_bar.title))
            .set_text(cx, &format!("Item {}", self.item_id + 1));
    }
}
```

### Container with Drop Handling

```rust
#[derive(Clone, Debug)]
struct DropPosition {
    row: usize,
    col: usize,
    rect: Rect,  // For visual preview
}

#[derive(Live, LiveHook, Widget)]
pub struct DragContainer {
    #[deref]
    view: View,

    #[live]
    drop_preview: DrawColor,

    /// Per-row item assignments (source of truth)
    #[rust]
    row_assignments: [Vec<usize>; 3],

    /// Currently dragging item ID
    #[rust]
    dragging_item: Option<usize>,

    /// Current drop target for preview
    #[rust]
    drop_state: Option<DropPosition>,

    #[rust]
    needs_layout_update: bool,
}

impl Widget for DragContainer {
    fn handle_event(&mut self, cx: &mut Cx, event: &Event, scope: &mut Scope) {
        let actions = cx.capture_actions(|cx| {
            self.view.handle_event(cx, event, scope);
        });

        // Capture StartDrag actions from children
        for action in actions.iter() {
            if let DragAction::StartDrag(id) = action.as_widget_action().cast() {
                self.dragging_item = Some(id);
            }
        }

        // KEY: Use capture_overload to receive events during drag
        match event.hits_with_capture_overload(
            cx,
            self.view.area(),
            self.dragging_item.is_some()  // Enable capture when dragging
        ) {
            Hit::FingerMove(fe) if self.dragging_item.is_some() => {
                // Update drop preview
                self.drop_state = self.find_drop_position(cx, fe.abs);
                self.view.redraw(cx);
            }
            Hit::FingerUp(fe) => {
                if let Some(dragged_id) = self.dragging_item {
                    self.handle_drop(cx, fe.abs, dragged_id);
                }
                self.dragging_item = None;
                self.drop_state = None;
                self.view.redraw(cx);
            }
            _ => {}
        }
    }

    fn draw_walk(&mut self, cx: &mut Cx2d, scope: &mut Scope, walk: Walk) -> DrawStep {
        if self.needs_layout_update {
            self.needs_layout_update = false;
            self.apply_layout(cx);
        }

        let result = self.view.draw_walk(cx, scope, walk);

        // Draw drop preview overlay
        if let Some(ref pos) = self.drop_state {
            self.drop_preview.draw_abs(cx, pos.rect);
        }

        result
    }
}

impl DragContainer {
    fn find_drop_position(&self, cx: &Cx, abs: DVec2) -> Option<DropPosition> {
        let container = self.view.view(id!(container));
        let rect = container.area().rect(cx);

        if !rect.contains(abs) { return None; }

        // Calculate row from Y position
        let visible_rows: Vec<_> = (0..3)
            .filter(|&r| !self.row_assignments[r].is_empty())
            .collect();

        let num_rows = visible_rows.len();
        if num_rows == 0 { return None; }

        let row_height = rect.size.y / num_rows as f64;
        let rel_y = abs.y - rect.pos.y;
        let visual_row = ((rel_y / row_height) as usize).min(num_rows - 1);
        let actual_row = visible_rows[visual_row];

        // Calculate column from X position
        let cols = self.row_assignments[actual_row].len().max(1);
        let col_width = rect.size.x / cols as f64;
        let rel_x = abs.x - rect.pos.x;
        let col = ((rel_x / col_width) as usize).min(cols);

        let preview_rect = Rect {
            pos: DVec2 {
                x: rect.pos.x + col.min(cols - 1) as f64 * col_width,
                y: rect.pos.y + visual_row as f64 * row_height,
            },
            size: DVec2 { x: col_width, y: row_height },
        };

        Some(DropPosition { row: actual_row, col, rect: preview_rect })
    }

    fn find_item_row(&self, item_id: usize) -> Option<(usize, usize)> {
        for (row, items) in self.row_assignments.iter().enumerate() {
            if let Some(col) = items.iter().position(|&id| id == item_id) {
                return Some((row, col));
            }
        }
        None
    }

    fn handle_drop(&mut self, cx: &mut Cx, abs: DVec2, dragged_id: usize) {
        let Some(drop_pos) = self.find_drop_position(cx, abs) else { return };
        let Some((src_row, src_col)) = self.find_item_row(dragged_id) else { return };

        if src_row == drop_pos.row && src_col == drop_pos.col { return; }

        // Remove from source
        self.row_assignments[src_row].remove(src_col);

        // Calculate insert position
        let target_len = self.row_assignments[drop_pos.row].len();
        let mut insert_col = drop_pos.col.min(target_len);

        // Adjust for same-row moves
        if src_row == drop_pos.row && drop_pos.col > src_col {
            insert_col = insert_col.saturating_sub(1);
        }

        // Insert at target
        self.row_assignments[drop_pos.row].insert(insert_col, dragged_id);

        self.needs_layout_update = true;
        self.view.redraw(cx);
    }

    fn apply_layout(&mut self, cx: &mut Cx) {
        // Hide all slots first, then show only assigned ones
        // See Pattern 17: Row-Based Grid Layout for details
    }
}
```

## Critical Points

1. **Use `hits_with_capture_overload`**: Pass `true` during drag to receive events outside original hit area

2. **Per-row tracking**: `row_assignments: [Vec<usize>; 3]` enables true physical movement between rows

3. **Deferred visual updates**: Set `needs_visual_update = true`, apply in `draw_walk` for proper Makepad integration

4. **Drop preview**: Draw overlay in `draw_walk` AFTER drawing main view, use `draw_depth` for z-ordering

5. **Excess slots**: Define more slots than typically needed (e.g., 9 per row) for flexibility

## Why Not Platform Drag?

`cx.start_dragging()` has limitations:
- "Dragging string not implemented on macos yet"
- Limited to predefined drag data types

Internal drag handling via `hits_with_capture_overload` works consistently across platforms.

## When to Use

- IDE/studio window management
- Kanban boards with column reordering
- Dashboard tile arrangement
- Any drag-to-reorder UI

## References

- [Row-Based Grid Layout](./_base/17-row-based-grid-layout.md) - Foundation pattern
- [flex-layout-demo](examples/flex-layout-demo) - Full working implementation

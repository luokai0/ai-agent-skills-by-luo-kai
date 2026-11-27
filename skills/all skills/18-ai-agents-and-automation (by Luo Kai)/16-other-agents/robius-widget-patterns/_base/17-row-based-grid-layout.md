# Pattern 17: Row-Based Grid Layout

<!-- Evolution: 2025-01-12 | source: flex-layout-demo | author: dorobot -->

Create dynamic grid layouts where different rows can have different numbers of columns, each filling their row equally.

## Problem

Using `RightWrap` flow with calculated pixel widths doesn't work reliably for layouts where:
- Row 1: 3 windows each filling 1/3 width
- Row 2: 2 windows each filling 1/2 width

`RightWrap` wraps items based on available width, not respecting intended row structure. Calculated pixel sizes often have measurement timing issues.

## Solution

Use **explicit row containers** with `Fill` sizing:
1. Container uses `flow: Down` to stack rows vertically
2. Each row uses `flow: Right` with `height: Fill`
3. Windows use `width: Fill, height: Fill` to auto-distribute within their row
4. Control layout by showing/hiding windows and setting size to 0 for hidden ones

## Key Insight

**`set_visible(false)` alone doesn't collapse space** when a widget has `width: Fill`. You must also set `width: 0, height: 0` to truly collapse hidden widgets.

## live_design!

```rust
live_design! {
    use link::theme::*;
    use link::widgets::*;

    GridContainer = {{GridContainer}} {
        width: Fill
        height: Fill

        // Container with explicit row structure
        window_container = <View> {
            width: Fill
            height: Fill
            flow: Down  // Stack rows vertically

            // Row 1: up to 3 windows
            row1 = <View> {
                width: Fill
                height: Fill
                flow: Right  // Distribute windows horizontally

                w1 = <SubWindow> { width: Fill, height: Fill }
                w2 = <SubWindow> { width: Fill, height: Fill }
                w3 = <SubWindow> { width: Fill, height: Fill }
            }

            // Row 2: up to 3 windows
            row2 = <View> {
                width: Fill
                height: Fill
                flow: Right

                w4 = <SubWindow> { width: Fill, height: Fill }
                w5 = <SubWindow> { width: Fill, height: Fill }
                w6 = <SubWindow> { width: Fill, height: Fill }
            }

            // Row 3: up to 3 windows
            row3 = <View> {
                width: Fill
                height: Fill
                flow: Right

                w7 = <SubWindow> { width: Fill, height: Fill }
                w8 = <SubWindow> { width: Fill, height: Fill }
                w9 = <SubWindow> { width: Fill, height: Fill }
            }
        }
    }
}
```

## Rust Implementation

```rust
impl GridContainer {
    /// Fixed layout mapping: window_count -> windows per row
    fn get_layout_config(&self, window_count: usize) -> Vec<usize> {
        match window_count {
            0 => vec![],
            1 => vec![1],           // 1 row: 1
            2 => vec![1, 1],        // 2 rows: 1+1
            3 => vec![2, 1],        // 2 rows: 2+1
            4 => vec![2, 2],        // 2 rows: 2+2
            5 => vec![3, 2],        // 2 rows: 3+2
            6 => vec![3, 3],        // 2 rows: 3+3
            7 => vec![3, 3, 1],     // 3 rows: 3+3+1
            8 => vec![3, 3, 2],     // 3 rows: 3+3+2
            9 => vec![3, 3, 3],     // 3 rows: 3+3+3
            _ => vec![3, 3, 3],
        }
    }

    fn apply_row_layout(&mut self, cx: &mut Cx) {
        let visible_windows = self.collect_visible_windows();
        let window_count = visible_windows.len();

        let row1_ids = [
            id!(window_container.row1.w1),
            id!(window_container.row1.w2),
            id!(window_container.row1.w3),
        ];
        let row2_ids = [
            id!(window_container.row2.w4),
            id!(window_container.row2.w5),
            id!(window_container.row2.w6),
        ];
        let row3_ids = [
            id!(window_container.row3.w7),
            id!(window_container.row3.w8),
            id!(window_container.row3.w9),
        ];
        let all_rows = [&row1_ids[..], &row2_ids[..], &row3_ids[..]];

        let row_config = self.get_layout_config(window_count);
        let num_rows = row_config.len();

        // CRITICAL: Collapse all windows first (set size to 0, not just visibility)
        for row_ids in &all_rows {
            for win_id in *row_ids {
                self.view.view(*win_id).apply_over(cx, live! {
                    visible: false
                    width: 0
                    height: 0
                });
            }
        }

        // Show/hide rows (must also set height to 0 for hidden rows)
        if num_rows >= 1 {
            self.view.view(id!(window_container.row1))
                .apply_over(cx, live! { visible: true, height: Fill });
        } else {
            self.view.view(id!(window_container.row1))
                .apply_over(cx, live! { visible: false, height: 0 });
        }
        // ... repeat for row2, row3

        // Assign windows to slots based on config
        let mut window_idx = 0;
        for (row, &cols_in_row) in row_config.iter().enumerate() {
            if row >= 3 { break; }

            for col in 0..3 {
                let win_id = all_rows[row][col];
                if col < cols_in_row && window_idx < visible_windows.len() {
                    // Show this slot with Fill sizing
                    self.view.view(win_id).apply_over(cx, live! {
                        visible: true
                        width: Fill
                        height: Fill
                    });
                    window_idx += 1;
                }
                // Hidden windows already collapsed above
            }
        }
    }
}
```

## Why This Works

| Approach | Problem |
|----------|---------|
| RightWrap + pixel widths | Wraps based on container width, not row structure |
| set_visible(false) only | Widget still occupies space with `width: Fill` |
| **Row containers + Fill** | Makepad auto-distributes Fill equally within each row |

## Critical Points

1. **Collapse hidden widgets completely**: Set both `visible: false` AND `width: 0, height: 0`
2. **Collapse hidden rows too**: Hidden rows with `height: Fill` still take space
3. **Use Fill for auto-distribution**: Don't calculate pixel sizes - let Makepad handle it
4. **Apply layout in draw_walk**: Call `apply_row_layout` when `needs_layout_update` is true

## When to Use

- Sub-window layouts in IDE/studio apps
- Dashboard tiles with variable columns per row
- Any grid where rows have different numbers of items
- Re-layouting when items are added/removed

## References

- [flex-layout-demo](examples/flex-layout-demo) - Working implementation
- [Dock-Based Studio Layout](./_base/15-dock-studio-layout.md) - Overall studio structure

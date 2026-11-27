---
name: makepad-sdf-drawing
author: robius
source: makepad-docs
date: 2024-01-01
tags: [sdf, line, arc, triangle, path]
level: intermediate
---

# SDF Path Drawing

Lines, arcs, and complex paths in Makepad SDF.

## Line Drawing

```rust
fn pixel(self) -> vec4 {
    let sdf = Sdf2d::viewport(self.pos * self.rect_size);

    // Move to start point
    sdf.move_to(10.0, 10.0);

    // Line to end point
    sdf.line_to(100.0, 50.0);

    // Stroke the line
    sdf.stroke(#ffffff, 2.0);

    return sdf.result;
}
```

## Arc Drawing

```rust
fn pixel(self) -> vec4 {
    let sdf = Sdf2d::viewport(self.pos * self.rect_size);
    let center = self.rect_size * 0.5;
    let radius = min(center.x, center.y) - 4.0;

    // Draw arc from angle1 to angle2
    let start_angle = 0.0;
    let end_angle = PI * 1.5;  // 270 degrees

    sdf.move_to(
        center.x + cos(start_angle) * radius,
        center.y + sin(start_angle) * radius
    );
    sdf.arc(center.x, center.y, radius, start_angle, end_angle);
    sdf.stroke(#4A90D9, 3.0);

    return sdf.result;
}
```

## Triangle Drawing

```rust
fn pixel(self) -> vec4 {
    let sdf = Sdf2d::viewport(self.pos * self.rect_size);

    // Define three vertices
    let v1 = vec2(50.0, 10.0);   // Top
    let v2 = vec2(10.0, 90.0);   // Bottom left
    let v3 = vec2(90.0, 90.0);   // Bottom right

    sdf.move_to(v1.x, v1.y);
    sdf.line_to(v2.x, v2.y);
    sdf.line_to(v3.x, v3.y);
    sdf.close_path();

    sdf.fill(#4A90D9);

    return sdf.result;
}
```

<!-- Evolution: 2026-01-12 | source: makepad-component/tooltip | author: @claude -->
### CRITICAL: Triangle Winding Order for Fill

**Problem**: Triangle fills correctly in some directions but not others.

**Cause**: SDF `fill()` requires consistent winding order. Triangles must be drawn in a specific direction (typically starting from the "tip" going clockwise) to fill properly.

**Solution**: Always draw triangles starting from the tip/apex, then go clockwise around the base:

```rust
// Example: Arrow triangles pointing in 4 directions
// ALL start from tip, then clockwise around base

// Arrow pointing DOWN (tip at bottom)
sdf.move_to(cx, tip_y);                    // Start at tip
sdf.line_to(cx - half_w, base_y);          // Go to left base
sdf.line_to(cx + half_w, base_y);          // Go to right base
sdf.close_path();
sdf.fill(color);

// Arrow pointing UP (tip at top)
sdf.move_to(cx, tip_y);                    // Start at tip
sdf.line_to(cx + half_w, base_y);          // Go to right base (clockwise)
sdf.line_to(cx - half_w, base_y);          // Go to left base
sdf.close_path();
sdf.fill(color);

// Arrow pointing RIGHT (tip at right)
sdf.move_to(tip_x, cy);                    // Start at tip
sdf.line_to(base_x, cy + half_w);          // Go to bottom base (clockwise)
sdf.line_to(base_x, cy - half_w);          // Go to top base
sdf.close_path();
sdf.fill(color);

// Arrow pointing LEFT (tip at left)
sdf.move_to(tip_x, cy);                    // Start at tip
sdf.line_to(base_x, cy - half_w);          // Go to top base (clockwise)
sdf.line_to(base_x, cy + half_w);          // Go to bottom base
sdf.close_path();
sdf.fill(color);
```

**Key insight**: The winding must be clockwise relative to the screen (Y increases downward). If your triangle doesn't fill, reverse the order of the last two points.

## Combining Shapes

```rust
fn pixel(self) -> vec4 {
    let sdf = Sdf2d::viewport(self.pos * self.rect_size);

    // First shape - fill and keep
    sdf.circle(50., 50., 30.);
    sdf.fill_keep(#FF0000);

    // Second shape - additive
    sdf.circle(80., 50., 30.);
    sdf.fill(#00FF00);

    return sdf.result;
}
```

<!-- Evolution: 2026-01-12 | source: makepad-component/tooltip | author: @claude -->
### Avoiding Gaps Between Connected Shapes

**Problem**: When drawing a box with an attached triangle (like tooltip arrow), there's a visible gap/seam between them.

**Cause**: Anti-aliasing and floating-point precision cause thin gaps at shape boundaries.

**Solution**: Use overlap - extend the triangle's base into the box by 1-2 pixels:

```rust
fn pixel(self) -> vec4 {
    let sdf = Sdf2d::viewport(self.pos * self.rect_size);
    let overlap = 2.0;  // Overlap to avoid gaps

    // Draw rounded box (leaving space for arrow)
    let box_height = self.rect_size.y - arrow_depth;
    sdf.box(0., 0., self.rect_size.x, box_height, radius);
    sdf.fill_keep(bg_color);

    // Draw arrow with base INSIDE the box (overlap)
    let base_y = box_height - overlap;  // Base extends INTO box
    let tip_y = self.rect_size.y;

    sdf.move_to(cx, tip_y);
    sdf.line_to(cx - arrow_half, base_y);
    sdf.line_to(cx + arrow_half, base_y);
    sdf.close_path();
    sdf.fill_keep(bg_color);

    sdf.stroke(border_color, 1.0);
    return sdf.result;
}
```

**Key insight**: The overlap ensures the shapes "merge" visually. Use 1-2 pixels overlap for clean joins.

## Orientation-Switchable Shape

Use instance variable for vertical/horizontal:

```rust
draw_track: {
    instance vertical: 0.0  // 0.0 = horizontal, 1.0 = vertical

    fn pixel(self) -> vec4 {
        let sdf = Sdf2d::viewport(self.pos * self.rect_size);
        let sz = self.rect_size;

        let is_vert = self.vertical;
        let length = mix(sz.x, sz.y, is_vert);
        let thickness = mix(sz.y, sz.x, is_vert);
        let r = thickness * 0.5;

        if is_vert > 0.5 {
            sdf.circle(r, r, r);
            sdf.rect(0.0, r, sz.x, sz.y - sz.x);
            sdf.circle(r, sz.y - r, r);
        } else {
            sdf.circle(r, r, r);
            sdf.rect(r, 0.0, sz.x - sz.y, sz.y);
            sdf.circle(sz.x - r, r, r);
        }

        sdf.fill(#e2e8f0);
        return sdf.result;
    }
}
```

Note: Using `if` in shape construction is acceptable since it's a static branch.

## When to Use

- Use `move_to/line_to` for custom polygons and paths
- Use `arc` for progress indicators, circular UI
- Use `close_path` for filled polygons
- Use `fill_keep` to draw multiple shapes additively

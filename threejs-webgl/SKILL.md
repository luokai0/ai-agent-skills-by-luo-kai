---
name: threejs-webgl
description: Use when building, debugging, or reviewing 3D web scenes with Three.js on WebGL, including scene graph setup, cameras, lighting, materials, loaders, animation loops, picking, performance tuning, and disposal of GPU resources.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Threejs Webgl

## Purpose and boundaries

This skill covers production work with Three.js rendering in a browser through WebGL: scene composition, render loop design, asset loading, interaction, performance budgets, and resource lifecycle. It does not cover WebGPU-only renderers, game engines, server-side rendering of 3D output, CAD kernels, or general shader theory beyond what a Three.js material needs. Treat any Three.js API name, option, or example as version-sensitive: confirm against the official documentation for the installed release before relying on it.

## Inputs and assumptions

Collect before writing code:
- Three.js version and bundler (ESM import style matters; check the release notes for renamed modules and removed classes).
- Target devices and minimum frame budget (for example 60 fps on mid-range mobile versus 30 fps on kiosks).
- Asset inventory: formats, polygon counts, texture sizes, animation clip counts.
- Interaction requirements: picking, dragging, camera control style.
- Whether the page shares the GPU with other canvases or video.

If any of these is unknown, state the assumption explicitly in the deliverable.

## Operating workflow

1. **Define the frame contract.** Write the target frame time, draw-call budget, and memory ceiling. Without numbers, optimization is guesswork.
2. **Build the renderer once.** Create one `WebGLRenderer` per canvas. Set pixel ratio capped (commonly `Math.min(devicePixelRatio, 2)`), and size it from the container, not the window, when embedded.
3. **Compose the scene graph.** Group objects by transform and lifecycle, not by visual category. Keep static geometry separate from animated nodes.
4. **Configure camera and lights.** Set near/far planes as tight as the content allows; a large far-to-near ratio causes depth precision loss. Prefer a small number of lights; baked or environment lighting is cheaper than many dynamic lights.
5. **Load assets asynchronously.** Use a loading manager, show progress, and validate that every loaded texture has power-of-two-independent sizes you actually support on target hardware. Set color space on color textures (sRGB) and linear on data textures (normals, roughness, metalness).
6. **Write the render loop.** Use `renderer.setAnimationLoop` or a `requestAnimationFrame` loop with delta time clamped (for example to 0.1 s) so tab switches do not produce large jumps. Pause rendering when the canvas is off-screen or the document is hidden.
7. **Add interaction.** For picking, use a raycaster against a reduced proxy set, not the full scene. Throttle pointer-driven raycasts to one per frame.
8. **Dispose on teardown.** Call `dispose()` on geometries, materials, textures, and render targets, and `renderer.dispose()` plus removal of the canvas when the view unmounts. Remove event listeners.

## Decision gates

- **Instancing gate:** If more than roughly 100 meshes share one geometry and material, use `InstancedMesh`. Verify the draw-call count before and after.
- **Shadow gate:** Enable shadow maps only for lights that visibly need them, with the smallest map size that passes review. Each shadow-casting light adds a full scene pass.
- **Post-processing gate:** Add effect passes only after the base render meets the frame budget. Each pass costs a full-screen draw and extra render targets.
- **Texture gate:** Downscale any texture that exceeds the display size by more than 2x at the largest on-screen size. Compress with a GPU-friendly format only after confirming loader and toolchain support for the installed version.
- **Geometry gate:** Use compressed or quantized formats for large meshes only if the pipeline can produce and validate them.
- **Approval gate:** Changing the asset pipeline, deleting shipped assets, or altering a public embed API requires explicit approval from the owner.

## Verification and evidence

- Record draw calls, triangles, and texture memory from `renderer.info` at steady state. Store the values with the scene version.
- Confirm no growth in `renderer.info.memory.geometries` and `renderer.info.memory.textures` after repeated mount and unmount cycles. Growth indicates a leak.
- Measure frame time over at least 300 frames on the target device class. Report median and 95th percentile, not a single reading.
- Check color output against a reference image under the intended tone-mapping and color-space settings.
- Test resize, device pixel ratio change, context loss handling, and tab visibility changes.
- Verify picking accuracy by clicking known coordinates and comparing the hit object.

## Failure handling

- **Black or blank canvas:** Check the camera is not inside geometry, near/far planes exclude the content, and the render call runs after the first resize.
- **Context lost:** Listen for `webglcontextlost`, prevent default, and rebuild resources on `webglcontextrestored`. Do not assume restoration is automatic.
- **Texture artifacts or washed-out colors:** Verify color space assignment on each texture map.
- **Frame spikes:** Profile before changing code. Common causes are shader compilation on first use (precompile by rendering once off-screen), uncached texture uploads, and per-frame allocation of vectors or geometry.
- **Leaked memory:** Compare `renderer.info` counts against expected object counts; search for objects removed from the scene but not disposed.

Stop and report when a fix requires changing public APIs, deleting assets, or exceeding the agreed budget.

## Deliverable contract

Provide:
- The code change, with imports matching the verified Three.js version.
- A short statement of the Three.js version and any API checked against official documentation.
- A budget table: target versus measured draw calls, triangles, texture memory, and frame time (median and p95).
- The verification steps performed and their results.
- A list of open assumptions and items requiring owner approval.

Do not: invent benchmark numbers, claim cross-device performance without measurement on those devices, skip disposal code, or suppress console errors from WebGL to make a demo appear clean.
---
name: computer-graphics-expert
version: 1.0.0
description: Expert-level computer graphics covering the rendering pipeline, rasterization, ray tracing, shaders, transformations, lighting models, and GPU programming.
author: luo-kai
tags: [computer graphics, rendering, shaders, ray tracing, OpenGL, WebGL, GLSL]
---

# Computer Graphics Expert

## Before Starting
1. Real-time or offline rendering?
2. Rasterization or ray tracing?
3. OpenGL, Vulkan, WebGL, or DirectX?

## Core Expertise Areas

### Rendering Pipeline
Vertex processing: transform 3D positions to clip space.
Primitive assembly: group vertices into triangles.
Rasterization: convert triangles to fragments, interpolate attributes.
Fragment processing: compute color per fragment, depth test.
Output merger: blend fragments, write to framebuffer.

### Transformations
Model matrix: object space to world space.
View matrix: world space to camera space.
Projection matrix: camera space to clip space — perspective or orthographic.
MVP matrix: Model x View x Projection applied to each vertex.
Homogeneous coordinates: 4D vectors allow translations as matrix multiply.

### Lighting Models
Phong model: ambient + diffuse + specular components.
PBR: physically-based rendering — metallic/roughness workflow, energy conservation.
Lambertian diffuse: max(dot(N,L), 0) * diffuse_color.
Shadow mapping: render depth from light, compare in main pass.
Global illumination: ambient occlusion, SSAO, ray-traced GI.

### Shaders
Vertex shader: per-vertex transformation, pass attributes to fragment shader.
Fragment shader: per-pixel color computation.
Geometry shader: per-primitive processing, can generate new geometry.
Compute shader: general GPU computation, not part of fixed pipeline.

### Ray Tracing
Ray casting: shoot ray from camera through each pixel.
Intersection tests: ray-sphere, ray-triangle, ray-AABB.
BVH: bounding volume hierarchy accelerates intersection queries.
Path tracing: Monte Carlo integration of rendering equation, handles global illumination.

## Best Practices
- Profile GPU with vendor tools before optimizing
- Minimize draw calls by batching geometry
- Use mipmaps to reduce texture aliasing and improve cache performance
- Prefer compute shaders for non-rasterization workloads

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Z-fighting | Adjust near and far clip planes to minimize depth range |
| Too many draw calls | Batch geometry, use instancing |
| Shader precision issues | Use mediump carefully, prefer highp for positions |
| Forgetting to normalize vectors | Always normalize normals and light directions |

## Related Skills
- threejs-expert
- wasm-expert
- computer-architecture-expert

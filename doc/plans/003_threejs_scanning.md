# Three.js & 3D Scanning Roadmap

## Phase 1: Interaction (Immediate)
- **Goal**: Manipulate a 3D object using Hand Gestures.
- **Frontend**:
    - Add `three.js` to `index.html`.
    - Create a transparent `<canvas>` overlay.
    - Render a wireframe Cube or Sphere.
- **Backend -> Frontend**:
    - Send Hand Landmark coordinates (Thumb/Index tip) via `/video_feed` metadata or a separate WebSocket/SSE channel.
    - For now, we piggyback on the existing loop: The frontend already draws lines. We will intercept the logic to rotate the Three.js mesh based on `prev_x` vs `idx_x`.

## Phase 2: Visualization (Short Term)
- **Goal**: Display point clouds.
- **Data**: If the backend detects "depth" (MediaPipe Hands gives Z-coordinates), visualize the hand skeleton in 3D space in Three.js, not just 2D overlay.

## Phase 3: Scanning (Long Term)
- **Goal**: Create 3D meshes from real-world objects.
- **Technique**: Photogrammetry or NeRF (Neural Radiance Fields).
    - *Constraint*: Standard webcams are monocular. Depth estimation is tricky.
    - *Solution*: Use a depth estimation model (e.g., MiDaS) on server.
    - *Pipeline*:
        1. Capture N frames around an object.
        2. Process frames with a photogrammetry lib (e.g., AliceVision/Meshroom) - *Heavy Compute*.
        3. Convert result to `.obj` or `.glb`.
        4. Send to Frontend to render in Three.js.
- **Alternative**: Point-E (OpenAI) to generate 3D models from text prompts ("Generate a chair") and display them.

## Implementation Steps for Phase 1
1. Include `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`.
2. Init Scene, Camera, Renderer.
3. On "Structure" command, hide video (or dim it) and show 3D Canvas.
4. Update object rotation `mesh.rotation.y += delta_x * 0.01`.

# Modern Approaches to Pre-Rendered Backgrounds in Games

**Created:** 2026-02-08 13:01 JST (Sunday)
**Author:** John Zealand-Doyle
**Session-ID:** eadb4c66-a7c4-4daa-8d93-8c157250b04a
**Context:** Discussion comparing FF7's tile-based background system with modern alternatives for game development using static pre-rendered backgrounds with minimal animation.

---

## Why FF7's Tile System Existed

FF7's layer/param/state/tile approach was born from **1997 hardware constraints**:

- PS1 had 1MB VRAM, couldn't hold a full 320x240 background
- Solution: chop the image into 16x16 tiles, pack them into 256x256 texture pages with 4-bit palettes
- The layer/param/state system was an ingenious way to get animation and depth sorting from a tiny memory footprint
- The entire background for a field typically fits in ~100-200KB compressed

You'd never design a system like this today. The tile packing, palette indirection, and bitmask animation states are all compression tricks that add massive complexity for problems that no longer exist.

---

## The Approaches (Modern Context)

### 1. Full-Resolution Layer Stack (The Direct Successor)

Replace FF7's tile system with what it was actually approximating: full-resolution PNG layers with alpha channels.

```text
field/md1_1/
├── layer0_background.png         # 1920x1080 base
├── layer1_foreground.png         # with alpha for depth sorting
├── layer1_depth.png              # grayscale depth map for character sorting
├── anim_waterfall/
│   ├── frame_00.png              # spritesheet or individual frames
│   ├── frame_01.png
│   └── frame_02.png
├── parallax_sky.png              # far layer, scrolls at 0.3x speed
└── scene.json                    # layer order, parallax rates, anim timing
```

**Pros:**

- Simple to author, easy to understand
- Modern tools (Photoshop/Aseprite) produce this natively
- No tile packing or palette nonsense
- Animations are just frame sequences

**Cons:**

- Large file sizes (mitigated by GPU texture compression like ASTC/BC7)
- Depth sorting with 3D characters requires a depth map or polygon cutouts
- No spatial compression

**Best for:** A game explicitly going for the PS1-era pre-rendered aesthetic with modern quality.

---

### 2. 3D Scene to Baked Renders

Build the scene in Blender/Unity/Unreal, render to static images from fixed camera angles.

**Pros:**

- Lighting, shadows, depth of field, ambient occlusion all come "for free"
- If you need a different camera angle later, just re-render
- The 3D scene IS the source of truth — no painting discrepancies
- Depth maps are trivially generated from the Z-buffer
- Normal maps too, enabling dynamic relighting

**Cons:**

- The effort equation is backwards from what you'd expect. A skilled 2D artist can paint a gorgeous background in 2-4 hours. The equivalent 3D scene (modeling, texturing, lighting, material setup) takes 1-3 days to reach the same visual quality
- 3D excels at consistency and iteration; 2D excels at speed and artistic expressiveness
- **3D backgrounds look like 3D backgrounds.** They have a clinical precision that's hard to overcome. Hand-painted or illustrated backgrounds have character, imperfection, and artistic intent that 3D struggles to match without significant post-processing
- Games like Disco Elysium, Hades, and Octopath Traveler all chose stylized/painted approaches over photorealistic 3D renders for this reason

**Best for:** Games where you need many camera angles of the same location, or where you want physically accurate lighting for gameplay reasons (stealth games, puzzle games with light mechanics).

---

### 3. 2.5D with Depth Layers + Parallax (The Modern Standard)

This is what most modern "2D" games with pre-rendered feel actually use. Hollow Knight, Ori, Dead Cells, and to some extent Octopath Traveler.

The scene is built from multiple depth-separated layers that shift based on camera position. Unlike FF7's rigid tile system, each layer is a continuous image with alpha transparency.

```text
Background layer (mountains, sky)       <- moves at 0.2x camera speed
Midground layer (buildings, trees)      <- moves at 0.5x camera speed
Playfield layer (where characters are)  <- moves at 1.0x camera speed
Foreground layer (fog, particles)       <- moves at 1.5x camera speed
```

Animations are handled through:

- Skeletal animation (Spine/DragonBones) for complex moving parts
- Shader-based effects (water shimmers, light flickers) instead of frame-by-frame
- Particle systems for environmental effects

**Pros:**

- Looks fantastic, widely proven
- Tools like Spine are mature
- Depth/parallax gives tremendous sense of depth
- Shader-based animation is resolution-independent and smooth

**Cons:**

- Requires an artist who thinks in layers and parallax
- Some effects are hard to achieve without shaders

**Best for:** Most modern 2D games with environmental depth. This is the industry standard.

---

### 4. Signed Distance Field + Shader-Driven Backgrounds

Used by some indie games and increasingly common: the background is defined as vector shapes, gradients, and procedural patterns evaluated by GPU shaders. Think of it as the background being a "program" rather than an image.

**Pros:**

- Resolution-independent, infinitely scalable
- Tiny file sizes
- Animations are mathematically defined (no frame sequences)
- Dynamic time-of-day and weather are trivial

**Cons:**

- Very specific art style (tends toward geometric/abstract)
- Requires shader programming
- Hard to achieve photorealistic or painterly looks
- Not really suitable for pre-rendered narrative-driven games

**Best for:** Stylized/abstract games, procedurally generated environments.

---

### 5. AI-Generated with Human Curation (Emerging)

Generate backgrounds with image models (Stable Diffusion, Midjourney, DALL-E), then manually edit/composite them into game-ready assets. Use ControlNet or similar for consistency across scenes.

**Pros:**

- Extremely fast iteration, can produce stunning quality
- Good for prototyping
- A single artist can produce 10x more backgrounds per day with AI assistance

**Cons:**

- Consistency across many scenes is hard (style drift)
- Fine control over specific elements is limited
- Animation still requires manual work or separate systems
- Legal/ethical considerations depending on training data

**Best for:** Rapid prototyping, small teams that need high visual quality on a budget, concept art pipelines.

---

## Recommendation: Static Images with Minimal Animation

For a game with primarily static pre-rendered backgrounds and minimal high-impact animations (doors opening, lights flickering, occasional environmental effects):

**Use Approach 3 (2.5D depth layers) with a simplified structure:**

```json
{
  "layers": [
    { "image": "sky.png", "parallax": 0.2, "blend": "normal" },
    { "image": "buildings.png", "parallax": 0.5, "blend": "normal" },
    { "image": "playfield.png", "parallax": 1.0, "blend": "normal" },
    { "image": "fog_overlay.png", "parallax": 1.5, "blend": "additive" }
  ],
  "animations": [
    { "name": "waterfall", "type": "spine", "file": "waterfall.spine" },
    { "name": "candle_flicker", "type": "shader", "shader": "flicker.glsl" }
  ],
  "depth_regions": [
    { "polygon": [[100,200], [300,200], [300,400], [100,400]], "z": 0.5 }
  ],
  "lighting_overlays": [
    { "image": "night_tint.png", "blend": "multiply", "condition": "time_of_day == night" }
  ]
}
```

Skip FF7's tile system entirely. Skip the param/state bitmask system. Use:

- **Full-resolution layers** instead of tiles
- **Named animation clips** instead of param+state bitmasks
- **Polygon depth regions** instead of per-tile Z-values
- **Blend mode layers** for lighting effects (additive overlay layers instead of per-tile blending flags)

The FF7 system is a masterpiece of 1997 engineering. But it solved problems you don't have anymore. The modern equivalent is simpler, more powerful, and much easier to author content for.

---

## Comparison Matrix

| Approach | Art Effort | Tech Effort | Visual Quality | Animation Support | Iteration Speed | File Size |
|----------|-----------|-------------|----------------|-------------------|-----------------|-----------|
| FF7 Tiles | High (tile constraints) | Very High | Low-res charm | Bitmask states | Slow | Tiny |
| Full-Res Layers | Medium | Low | Excellent | Frame sequences | Fast | Large |
| 3D Baked | High (3D modeling) | Medium | Photorealistic | Re-render | Medium | Medium |
| 2.5D Parallax | Medium | Medium | Excellent | Spine/Shaders | Fast | Medium |
| SDF/Shaders | Low (procedural) | Very High | Stylized only | Built-in | Very Fast | Tiny |
| AI-Generated | Low | Low | Variable | Manual | Very Fast | Large |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-08 | 1.0 | Initial documentation |

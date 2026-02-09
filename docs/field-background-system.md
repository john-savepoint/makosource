# FF7 Field Background System — Layers, Sections, Parameters & States

**Created:** 2026-02-07 09:55 JST (Saturday)
**Author:** John Zealand-Doyle
**Session-ID:** eadb4c66-a7c4-4daa-8d93-8c157250b04a
**Reference:** Makou Reactor source code (BackgroundTiles.cpp, BackgroundTilesIO.cpp, BackgroundFilePC.cpp)

---

## Overview

Every field (screen/room) in FF7 is a **pre-rendered 2D background** made of small tiles. These tiles are organized into a layered system that allows:

- Depth sorting (characters walk in front of/behind background elements)
- Parallax scrolling (distant objects move slower than near objects during camera pans)
- Animation (flickering lights, flowing water, spinning machinery, electrical sparks)
- Conditional visibility (doors opening/closing, switches toggling, story-triggered changes)

The system has three levels of organization: **Layers → Sections → Parameters with States**.

---

## The Four Layers

Every field has up to 4 layers. Each layer has a specific role and draw order.

### Draw Order (back to front)

```
╔═══════════════════════════════════════════════════════╗
║  SCREEN (what the player sees)                        ║
║                                                       ║
║  ┌─ Layer 3: Near Parallax ──────────────────────┐    ║
║  │  (fog, window frames, very close overlays)    │    ║
║  │  32x32 tiles, drawn LAST (in front of all)    │    ║
║  │                                               │    ║
║  │  ┌─ Layer 1: Foreground ──────────────────┐   │    ║
║  │  │  (objects, animated elements, doors)   │   │    ║
║  │  │  16x16 tiles, variable Z per tile      │   │    ║
║  │  │  Characters render between these tiles │   │    ║
║  │  │                                        │   │    ║
║  │  │  ┌─ Layer 0: Background ──────────┐    │   │    ║
║  │  │  │  (walls, floor, static scene)  │    │   │    ║
║  │  │  │  16x16 tiles, drawn first      │    │   │    ║
║  │  │  │  Always present, no animation  │    │   │    ║
║  │  │  └────────────────────────────────┘    │   │    ║
║  │  └────────────────────────────────────────┘   │    ║
║  └───────────────────────────────────────────────┘    ║
║                                                       ║
║  ┌─ Layer 2: Far Parallax ───────────────────────┐    ║
║  │  (sky, horizon, distant mountains)            │    ║
║  │  32x32 tiles, drawn FIRST (behind all)        │    ║
║  └───────────────────────────────────────────────┘    ║
╚═══════════════════════════════════════════════════════╝
```

### Layer Details

| Layer | Name          | Tile Size | Z-Depth                     | Animation          | Purpose                                                                                                                                                          |
| ----- | ------------- | --------- | --------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0** | Background    | 16×16     | Fixed (4095 = farthest)     | None               | Static scene — walls, floors, ceilings. Always present, always fully visible.                                                                                    |
| **1** | Foreground    | 16×16     | Variable per tile           | Full (param/state) | Interactive/animated elements — doors, lights, machinery, water. Each tile has its own Z-depth so characters can walk in front of or behind individual elements. |
| **2** | Far Parallax  | 32×32     | Fixed (4096 = behind all)   | Possible           | Distant background — sky, clouds, horizon. Scrolls slower than camera movement to create depth illusion.                                                         |
| **3** | Near Parallax | 32×32     | Fixed (0 = in front of all) | Possible           | Foreground overlay — fog, mist, window frames, rain. Scrolls faster than camera or stays fixed to create proximity illusion.                                     |

**Key distinction:** Layer 0 has NO animation — every tile is always visible with param=0, state=0. Layers 1-3 support the full param/state animation system.

---

## Sections (Layer 1 Only)

Within Layer 1, tiles are grouped by their **Z-depth ID** (a 16-bit value from 0 to 4095). Each unique ID value creates a "section" — a group of tiles that share the same depth plane.

```
Layer 1: Foreground
├── Section ID=100  (far background objects)
│   ├── Tile: desk surface
│   └── Tile: bookshelf
├── Section ID=200  (mid-ground)
│   ├── Tile: table edge
│   └── Tile: chair back
├── Section ID=300  (near foreground)
│   ├── Tile: railing
│   └── Tile: barrel
└── Section ID=400  (very close)
    └── Tile: wall edge the character walks behind
```

**Why sections matter:**

- Characters have a Z-depth value based on their position on the walkmesh
- The game renders Layer 1 tiles sorted by Z, interleaving them with character sprites
- This creates the illusion of characters walking IN BETWEEN background elements (behind a railing but in front of a desk)

**Layers 0, 2, 3** do NOT have sections — all tiles in those layers share a single fixed Z-depth.

---

## Parameters (Animation Groups)

The `param` field (values 0-127) groups tiles into **animation groups** controlled by the field's script system.

### param = 0: Always Visible

Tiles with `param = 0` are **unconditionally visible**. They are not controlled by any script and always appear. Layer 0 tiles are always param=0.

### param > 0: Script-Controlled

Tiles with `param > 0` belong to an animation group. The field's event scripts use opcodes to control their visibility:

| Opcode                  | Effect                                        | Example                             |
| ----------------------- | --------------------------------------------- | ----------------------------------- |
| `BGON(param, stateID)`  | Show state #stateID of param group            | `BGON(3, 0)` — show candle frame 1  |
| `BGOFF(param, stateID)` | Hide state #stateID of param group            | `BGOFF(3, 0)` — hide candle frame 1 |
| `BGROL(param)`          | Advance to next animation state               | `BGROL(3)` — next candle frame      |
| `BGROL2(param)`         | Go to previous animation state                | `BGROL2(3)` — previous candle frame |
| `BGCLR(param)`          | Hide all states (make entire group invisible) | `BGCLR(3)` — candle goes dark       |

### Real-World Examples

```
Field: ancnt_2 (Ancient Forest entrance)

Param 1: Waterfall animation
  State 0 (bit 0): Waterfall frame 1
  State 1 (bit 1): Waterfall frame 2
  State 2 (bit 2): Waterfall frame 3
  → Script uses BGROL(1) in a loop to cycle frames

Param 2: Butterfly animation
  State 0 (bit 0): Butterfly position 1
  State 1 (bit 1): Butterfly position 2
  → Script uses BGROL(2) to make butterfly flutter

Param 3: Light rays
  State 0 (bit 0): Light beams visible
  → Script uses BGON(3, 0) to show, BGOFF(3, 0) to hide
```

```
Field: blin60_2 (Shinra Building Floor 60)

Param 1: Elevator door
  State 0 (bit 0): Door closed
  State 1 (bit 1): Door open
  → Script triggers BGON/BGOFF based on player interaction

Param 2: Display screen
  State 0: Screen frame 1
  State 1: Screen frame 2
  State 2: Screen frame 3
  → Script cycles with BGROL(2)
```

---

## States (Animation Frames / Variants)

The `state` field is a **bitmask** where each bit represents a different visual variant within a param group.

### How the Bitmask Works

```
state = 0  → Always visible (not part of any animation cycle)
state = 1  → Visible when bit 0 is active (State 0)
state = 2  → Visible when bit 1 is active (State 1)
state = 4  → Visible when bit 2 is active (State 2)
state = 8  → Visible when bit 3 is active (State 3)
...
state = 128 → Visible when bit 7 is active (State 7)
```

Up to **8 states** per param group (8 bits in a byte).

### The Runtime Active Bitmask

The game engine maintains one byte per param group. Each bit in that byte represents whether that state is currently active. The visibility check is:

```
tile is visible IF (activeParamBitmask & tile.state) != 0
```

### Animation Cycling Example

For a 3-frame water animation (param=2):

```
Frame 1: Tiles with state=1 (binary: 00000001)
Frame 2: Tiles with state=2 (binary: 00000010)
Frame 3: Tiles with state=4 (binary: 00000100)

Script loop:
  BGON(2, 0)   → active = 00000001 → Frame 1 visible
  wait 3 frames
  BGOFF(2, 0)
  BGON(2, 1)   → active = 00000010 → Frame 2 visible
  wait 3 frames
  BGOFF(2, 1)
  BGON(2, 2)   → active = 00000100 → Frame 3 visible
  wait 3 frames
  BGOFF(2, 2)
  goto start

Or equivalently:
  BGON(2, 0)
  loop:
    BGROL(2)    → rotates the active bit: 001 → 010 → 100 → 001...
    wait 3 frames
    goto loop
```

### Multi-Bit States

A tile CAN have multiple bits set (e.g., `state = 3` = bits 0 and 1). This tile would be visible whenever EITHER State 0 OR State 1 is active. This is uncommon but used for tiles that should appear during multiple animation phases.

---

## Complete Hierarchy

```
Field File
│
├── Layer 0: Background (static, always visible)
│   └── All tiles: param=0, state=0 (no animation)
│
├── Layer 1: Foreground (interactive, depth-sorted)
│   ├── Section ID=100 (depth group)
│   │   ├── Tiles with param=0, state=0 (always visible at this depth)
│   │   ├── Param Group 1 (e.g., "Door")
│   │   │   ├── State 0 (bit 0): door closed tiles
│   │   │   └── State 1 (bit 1): door open tiles
│   │   └── Param Group 2 (e.g., "Light")
│   │       ├── State 0: light frame 1
│   │       ├── State 1: light frame 2
│   │       └── State 2: light frame 3
│   ├── Section ID=200 (another depth group)
│   │   └── ...
│   └── Section ID=300
│       └── ...
│
├── Layer 2: Far Parallax (distant background)
│   ├── Tiles with param=0, state=0 (static sky)
│   └── Param Group 1 (e.g., "Clouds")
│       ├── State 0: cloud position 1
│       └── State 1: cloud position 2
│
└── Layer 3: Near Parallax (foreground overlay)
    ├── Tiles with param=0, state=0 (static fog)
    └── Param Group 1 (e.g., "Rain intensity")
        ├── State 0: light rain
        └── State 1: heavy rain
```

---

## Blending (Transparency Effects)

Tiles can have `blending = true` with a `typeTrans` value (0-3) that controls how their pixels combine with what's already drawn:

| Type | Name         | Formula                 | Visual Effect                            |
| ---- | ------------ | ----------------------- | ---------------------------------------- |
| 0    | Average      | `(src + dst) / 2`       | 50% transparent overlay                  |
| 1    | Additive     | `min(src + dst, 255)`   | Glowing light beams, fire, magic effects |
| 2    | Subtractive  | `max(dst - src, 0)`     | Shadows, dark areas                      |
| 3    | 25% Additive | `min(dst + src/4, 255)` | Subtle glows, ambient light              |

Blended tiles are common for:

- Light rays/beams (additive)
- Water reflections (average)
- Shadows (subtractive)
- Glowing signs/screens (additive)

**Only paletted tiles use blending.** Direct color (16bpp) tiles always overwrite pixels directly.

---

## Implications for AI Upscaling Export

### The Challenge

A single field can have hundreds of tiles across 4 layers, multiple param groups, and 8 states per group. To AI-upscale a field, you need to generate replacement images for every visual element.

### What Needs to Be Exported

For a complete export:

| Component               | How Many  | What It Contains                       |
| ----------------------- | --------- | -------------------------------------- |
| Layer 0 composite       | 1 image   | The entire static background           |
| Layer 1 base (param=0)  | 1 image   | Always-visible foreground elements     |
| Layer 1 per param+state | varies    | Each animation frame separately        |
| Layer 2 composite       | 0-1 image | Far parallax (if present)              |
| Layer 3 composite       | 0-1 image | Near parallax (if present)             |
| Blending tiles          | separate  | Must be exported with alpha/blend info |

### Export Strategy Options

#### Option A: Per-Layer + Per-Param-State Composites (Recommended)

Export each unique visual combination as a separate image at its correct screen position:

```
export/md1_1/
├── layer0_base.png              # Complete Layer 0 background
├── layer1_base.png              # Layer 1 tiles with param=0 (always visible)
├── layer1_param1_state0.png     # Param 1, State 0 tiles
├── layer1_param1_state1.png     # Param 1, State 1 tiles
├── layer1_param2_state0.png     # Param 2, State 0 tiles
├── layer2_base.png              # Far parallax
├── layer3_base.png              # Near parallax
├── composite_default.png        # Full composite with default states
└── metadata.json                # Tile mapping, dimensions, param/state info
```

**Advantages:**

- Each image has spatial context (tiles at correct positions)
- AI model can see the visual relationship between elements
- Manageable number of images per field

**Disadvantages:**

- Blended tiles look wrong in isolation (need the layer beneath them)
- Some images may be mostly transparent with small elements

#### Option B: Raw Texture Pages

Export each 256×256 texture page directly with palette applied:

```
export/md1_1/
├── page_00.png    # Texture page 0, all tiles mixed together
├── page_01.png    # Texture page 1
├── ...
└── page_15.png
```

**Advantages:**

- Simple, fast, complete data extraction
- This is what FFNx actually loads as replacement textures
- No compositing needed

**Disadvantages:**

- Tiles from different layers/params are scrambled together on the same page
- No spatial context — the AI sees a quilt of unrelated tile fragments
- Palette-dependent (different palettes produce different colors for the same pixels)

#### Option C: Hybrid (Composites for AI, Pages for Deployment)

1. Export **composites** (Option A) for the AI to understand what the scene looks like
2. AI generates upscaled composites
3. Tool **reverse-maps** the upscaled pixels back to texture page positions
4. Export as **texture pages** (Option B format) for FFNx deployment

This gives the AI full visual context while producing the format the game engine needs.

### The Palmer/FacePalmer Workflow (Existing Approach)

The existing community tool Palmer does exactly this decomposition. From Makou Reactor's `untile()` function, it exports one image per unique combination of `(layer, param + state * 64, blending)`. Each image contains tiles at their correct screen positions. FacePalmer (a Photoshop script) then processes these with AI upscaling and maps the results back to texture pages.

Our Phase 2 goal is to replicate this workflow without external tools.

---

## Glossary

| Term                  | Meaning                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Layer**             | One of 4 depth planes (0=background, 1=foreground, 2=far parallax, 3=near parallax)                                                  |
| **Section**           | A group of Layer 1 tiles sharing the same Z-depth ID. Controls depth-sorting with 3D characters.                                     |
| **Param (Parameter)** | An animation group ID (1-127). Groups tiles that are controlled together by field scripts. param=0 means always visible.             |
| **State**             | A bitmask (1-255) representing which animation frame/variant a tile belongs to within its param group. state=0 means always visible. |
| **Blending**          | Per-pixel transparency effect (additive, subtractive, average, or 25% additive)                                                      |
| **Tile**              | A small rectangular piece (16×16 or 32×32 pixels) of the background image                                                            |
| **Texture Page**      | A 256×256 pixel atlas containing the source pixel data for tiles                                                                     |
| **Palette**           | A 256-color lookup table (BGR555 format) used for paletted (non-direct-color) tiles                                                  |
| **BGON/BGOFF**        | Field script opcodes that show/hide specific states within param groups                                                              |
| **BGROL**             | Field script opcode that advances to the next animation state in a param group                                                       |
| **Z-depth**           | A value (0-4095) controlling whether a tile renders in front of or behind 3D characters                                              |
| **Walkmesh**          | The 3D collision mesh that determines where characters can walk, separate from the background                                        |

---

## Version History

| Date       | Version | Changes               |
| ---------- | ------- | --------------------- |
| 2026-02-07 | 1.0     | Initial documentation |

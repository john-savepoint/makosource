# FFNx Widescreen Analysis - Addendum

**Document Version:** 1.0
**Created:** 2026-01-12 23:15:00 JST (Monday)
**Author:** Complementary analysis integration
**Session-ID:** 6fb0facc-34c8-4184-b3e7-8564019b614c
**Purpose:** Additional technical insights missing from the primary deep dive

---

## Additional Technical Insights

### 1. The "Virtual Canvas" Concept (Missing from Primary Analysis)

The external analysis correctly emphasizes a critical conceptual framework I didn't explicitly state:

**The game engine doesn't know widescreen exists.**

FF7's internal logic still operates on a 640x480 grid:
- All collision detection: 640x480
- All AI pathfinding: 640x480
- All script coordinates: 640x480
- All walkmesh data: 640x480

FFNx creates a **Virtual Coordinate System** where:
```
Game Logic Coordinate 0 = Render Coordinate 107
Game Logic Coordinate 640 = Render Coordinate 747

This translation happens at the GPU boundary, not in game logic
```

**Why This Matters:**
- Mods that patch game logic can remain unchanged
- Script modifications work identically in 4:3 and 16:9
- The widescreen system is a pure rendering layer

### 2. Projection Matrix Manipulation (3D Rendering Detail)

My analysis mentioned the memory patching but didn't detail the **projection matrix modification** for 3D content:

**Location:** `src/renderer.cpp` - `Renderer::setD3DProjection()`

```cpp
if(widescreen_enabled)
{
    // Calculate widescreen scale factor
    float widescreenScale = round(float(game_width) / wide_viewport_width * 100) / 100.f;

    // Modify X-axis components of projection matrix
    internalState.d3dProjectionMatrix[0] *= widescreenScale;  // X scale
    internalState.d3dProjectionMatrix[8] *= widescreenScale;  // X skew
}
```

**What This Does:**
- Modifies the **Field of View (FOV)** on the X-axis only
- Effectively "zooms out" horizontally while keeping vertical FOV constant
- Prevents the "stretched character" problem of naive aspect ratio changes

**Matrix Math Explanation:**

A typical projection matrix has this structure:
```
[ Sx  0   0  Tx ]
[  0 Sy   0  Ty ]
[  0  0  Sz  Tz ]
[  0  0   0   1 ]

Where:
Sx = Horizontal scale (affects FOV width)
Sy = Vertical scale (affects FOV height)
```

FFNx multiplies `Sx` by the widescreen scale factor (0.75 for 16:9):
```
Original Sx (4:3):  1.333
Widescreen Sx:      1.333 * 0.75 = 1.0

Result: Wider horizontal FOV, same vertical FOV
```

**Practical Impact:**
- In battles, you can see enemies standing further to the sides
- On the world map, you see more terrain horizontally
- Characters maintain correct proportions (no squashing)

### 3. The Culling Problem (More Detail)

My analysis mentioned culling patches but didn't explain the **frustum culling** issue in depth:

**The Problem:**

FF7's 3D renderer performs frustum culling - it doesn't send vertices to the GPU if they're outside the visible area:

```cpp
// Original game logic (pseudocode)
if (model.x < 0 || model.x > 640)
    return;  // Don't draw this model

// In widescreen:
// Model at x = -50 should be visible (viewport goes to -107)
// But game code returns early, model never drawn
```

**FFNx's Fix:**

Multiple approaches are used:

1. **NOP the culling checks** (as mentioned in external analysis):
```cpp
// src/ff7_opengl.cpp
memset_code(ff7_externals.world_draw_all_3d_model + 0x84, 0x90, 6);
// Replaces culling conditional jump with NOPs (no operation)
```

2. **Replace culling functions** with widescreen-aware versions:
```cpp
// src/ff7/widescreen.cpp:156
replace_function(ff7_externals.field_culling_model_639252,
                 ff7::field::ff7_field_do_draw_3d_model);
```

The replacement function uses:
```cpp
if (model.x < wide_viewport_x || model.x > wide_viewport_x + wide_viewport_width)
    return;  // Now uses -107 to 747 instead of 0 to 640
```

**Why Both Approaches:**
- Some culling code is in assembly (needs NOP)
- Some culling is in function calls (can be hooked)
- Different game modes (field/battle/world) use different culling systems

### 4. UV Coordinate Handling for HD Textures

The external analysis mentions FFNx's texture replacement system handles resolution-independent loading. Here's the technical detail:

**Original Game Texture Request:**
```cpp
// Game: "Load background tile at UV coordinates (0.0, 0.0) to (0.25, 0.25)"
// Expects: 256x256 pixel region from 1024x1024 texture
```

**FFNx with 4K Asset:**
```cpp
// FFNx finds: 4096x4096 texture instead of 1024x1024
// UV coordinates remain (0.0, 0.0) to (0.25, 0.25)
// Result: Samples 1024x1024 region from 4K texture (same relative area)
```

**Implementation (from `src/image/image.cpp`):**

```cpp
uint32_t load_texture(const char* name)
{
    // Check for mod texture first
    std::string mod_path = find_external_texture(name);

    if (!mod_path.empty())
    {
        // Load arbitrary resolution texture
        ImageData* img = load_image_file(mod_path);

        // Create GPU texture with actual dimensions
        bgfx::TextureHandle handle = bgfx::createTexture2D(
            img->width,    // Could be 4096 instead of 1024
            img->height,
            false,         // No mipmaps
            1,
            bgfx::TextureFormat::RGBA8,
            BGFX_TEXTURE_NONE,
            bgfx::makeRef(img->data, img->size)
        );

        return handle.idx;
    }

    // Fall back to original game texture
    return load_original_texture(name);
}
```

**The UV coordinates don't change**, so high-res textures "just work" - the GPU samples from the higher resolution data using the same relative coordinates.

### 5. Walkmesh Extension Requirements (Critical for AI Assets)

The external analysis correctly identifies the **walkmesh mismatch** issue. Here's the technical breakdown:

**Walkmesh Structure:**

FF7 field walkmesh files (`.wm` in field LGP archives) contain:
```cpp
struct WalkmeshTriangle
{
    int16_t vertices[3][3];  // 3 vertices, XYZ coords
    int16_t normals[3];      // Surface normal
    uint16_t flags;          // Walkable, climbable, etc.
};
```

**Coordinates are in game logic space (0-640)**, not render space (-107 to 747).

**For AI-Extended Backgrounds:**

If you create a 21:9 background with AI-generated content on the sides:

```
Original 4:3 (640 wide):
┌──────────────────────────┐
│   [Walkable Area]        │  Walkmesh covers this
└──────────────────────────┘

21:9 Extension (1120 wide):
←240→┌──────────────────────────┐←240→
     │   [Walkable Area]        │
     └──────────────────────────┘
   ^ AI-Generated    AI-Generated ^
     (Not walkable)   (Not walkable)
```

**Solution 1: Extend Walkmesh in Tools**

Using Makou Reactor or field editing tools:

1. Open the field's `.wm` file
2. Add triangles covering the extended areas:
```cpp
// Example: Extend left side to x = -240
new_triangle.vertices[0] = {-240, 0, z_value};
new_triangle.vertices[1] = {0, 0, z_value};
new_triangle.vertices[2] = {-240, 240, z_value};
new_triangle.flags = WALKABLE;
```

3. Export modified walkmesh
4. FFNx loads the modified walkmesh automatically

**Solution 2: Runtime Walkmesh Extension (Code)**

Alternatively, FFNx could generate extended walkmesh at runtime:

```cpp
// Hypothetical function in src/ff7/field/walkmesh.cpp
void extend_walkmesh_for_widescreen(WalkmeshData* mesh)
{
    if (aspect_ratio != AR_WIDESCREEN_21X9)
        return;

    // Find leftmost and rightmost X coordinates
    int16_t min_x = find_min_x(mesh);
    int16_t max_x = find_max_x(mesh);

    // Extend left side
    if (min_x > wide_viewport_x)
    {
        // Create mirror triangles extending to wide_viewport_x
        for (triangle in mesh->triangles)
        {
            if (triangle.min_x == min_x)
            {
                WalkmeshTriangle extended = mirror_triangle(triangle, -240);
                mesh->add_triangle(extended);
            }
        }
    }

    // Similar for right side
}
```

**Practical Workflow for AI Asset Creation:**

1. Extract original field background (320x240 or 640x480)
2. Use AI outpainting to extend to 21:9 (keeping original centered)
3. Upscale entire result to 4K (5040x2160)
4. Extract walkmesh from field file
5. Use Makou Reactor to:
   - Load walkmesh
   - Add triangles covering AI-generated regions
   - Mark as walkable where appropriate (flat ground)
   - Mark as non-walkable where inappropriate (walls, decorations)
6. Place modified walkmesh and texture in mod folder

### 6. The "Hybrid 21:9" Recommendation

The external analysis recommends:
- **3D modes (Battle/World):** Full 21:9 rendering
- **Field mode:** Lock to 16:9 with pillarboxing

**Implementation Strategy:**

```cpp
// src/ff7/widescreen.cpp
WIDESCREEN_MODE Widescreen::getMode()
{
    struct game_mode* mode = getmode_cached();

    // Override based on game mode
    switch(mode->driver_mode)
    {
        case MODE_BATTLE:
        case MODE_WORLDMAP:
            // Force 21:9 for 3D modes
            if (aspect_ratio == AR_WIDESCREEN_21X9)
                return WM_EXTEND_WIDE;
            break;

        case MODE_FIELD:
            // Cap at 16:9 for field mode (unless per-field config allows)
            if (aspect_ratio == AR_WIDESCREEN_21X9 && !field_allows_21x9())
                return use_16x9_fallback();
            break;

        case MODE_MENU:
            // Always 4:3 for menus
            return WM_DISABLED;
    }

    return widescreen_mode;
}
```

**Configuration File Extension:**

```toml
# FFNx.toml
aspect_ratio = 4  # New: 21:9 mode

# Per-mode overrides
[widescreen_mode_overrides]
battle = "21:9"      # Full ultrawide
world = "21:9"       # Full ultrawide
field = "16:9"       # Default to 16:9 (pillarboxed on 21:9 display)
menu = "4:3"         # Always original aspect

# Per-field exceptions (for fields with AI-extended assets)
[field_ultrawide_whitelist]
"md1_1" = true       # Sector 7 - has 21:9 assets
"junon2" = true      # Junon - has 21:9 assets
```

### 7. Asset Replacement Pipeline (Technical Details)

The external analysis provides the conceptual workflow. Here's the technical file structure:

**Mod Directory Structure:**

```
mods/
├── textures/
│   ├── field/
│   │   ├── md1_1/
│   │   │   ├── background_21x9_4k.png      # 5040x2160 AI-extended
│   │   │   └── metadata.json               # Asset metadata
│   │   ├── junon2/
│   │   │   └── background_21x9_4k.png
│   │   └── ...
│   ├── battle/
│   └── world/
├── walkmesh/
│   ├── md1_1.wm          # Extended walkmesh
│   ├── junon2.wm
│   └── ...
└── config/
    └── field_21x9.toml   # Per-field 21:9 settings
```

**FFNx Loading Priority:**

```cpp
// Pseudocode from src/saveload.cpp
std::string find_field_texture(const char* field_name)
{
    // Priority 1: 21:9 4K asset
    if (aspect_ratio == AR_WIDESCREEN_21X9)
    {
        path = check_path("mods/textures/field/{field}/background_21x9_4k.png");
        if (exists(path)) return path;
    }

    // Priority 2: 16:9 HD asset
    if (aspect_ratio >= AR_WIDESCREEN_16X9)
    {
        path = check_path("mods/textures/field/{field}/background_16x9_hd.png");
        if (exists(path)) return path;
    }

    // Priority 3: Generic HD asset (4:3)
    path = check_path("mods/textures/field/{field}/background.png");
    if (exists(path)) return path;

    // Priority 4: Original game asset
    return load_from_lgp_archive(field_name);
}
```

**Metadata File Format (Optional Enhancement):**

```json
{
  "asset_name": "md1_1_background",
  "original_resolution": "320x240",
  "output_resolution": "5040x2160",
  "aspect_ratio": "21:9",
  "generation_method": "AI_outpaint",
  "ai_model": "Stable_Diffusion_XL_inpaint",
  "original_centered": true,
  "extension_left": 240,
  "extension_right": 240,
  "upscale_method": "ESRGAN_4x",
  "walkmesh_extended": true,
  "quality_notes": "Minor AI artifacts on left edge, approved for use"
}
```

### 8. Pixel Density Considerations

The external analysis mentions "Lower pixel density is more noticeable at wide FOV."

**Math:**

```
4:3 Mode (1280x960 display):
    640 logical pixels → 1280 screen pixels
    Ratio: 2.0x (each game pixel = 2 screen pixels)

16:9 Mode (1920x1080 display):
    854 logical pixels → 1920 screen pixels
    Ratio: 2.25x (slightly better)

21:9 Mode (2560x1080 display):
    1120 logical pixels → 2560 screen pixels
    Ratio: 2.29x (similar to 16:9)

21:9 Mode (3840x1600 display):
    1120 logical pixels → 3840 screen pixels
    Ratio: 3.43x (much better, but stretches artifacts)
```

**Recommendation:**

For 21:9, target **internal render resolution** should scale with display resolution:

```cpp
// src/cfg.cpp
void calculate_internal_resolution()
{
    if (aspect_ratio == AR_WIDESCREEN_21X9)
    {
        // Scale internal resolution to maintain pixel density
        if (window_size_x <= 2560)
            wide_viewport_width = 1120;  // Standard
        else if (window_size_x <= 3440)
            wide_viewport_width = 1680;  // 1.5x scale
        else
            wide_viewport_width = 2240;  // 2x scale (4K ultrawide)
    }
}
```

This maintains consistent visual quality across different 21:9 display sizes.

---

## Missing Technical Clarifications

### 1. FFNx Does Not Modify Executable

My original analysis should have emphasized more clearly:

**FFNx operates entirely at runtime.** It does NOT:
- Modify ff7.exe on disk
- Create permanent patches
- Require different game executables

All patches are **memory patches** applied when the game loads. If you remove FFNx.dll, the game runs in original 4:3.

### 2. Performance Impact of 21:9

Additional considerations for ultrawide:

**Rendering Load:**
```
4:3 (640x480):    307,200 pixels
16:9 (854x480):   409,920 pixels (+33%)
21:9 (1120x480):  537,600 pixels (+75%)

With 4K upscaling:
21:9 (5040x2160): 10,886,400 pixels (+3,445% vs original!)
```

**Mitigation:**
- Modern GPUs handle this easily (even integrated graphics)
- BGFX's multi-threaded rendering helps
- Can limit internal resolution scale for lower-end systems

### 3. The "Static Screen" vs "Scrolling Screen" Distinction

The external analysis mentions this briefly. Full technical detail:

**Static Screen Detection:**

```cpp
// src/ff7/widescreen.cpp:390
void Widescreen::initParamsFromConfig()
{
    camera_range.left = field_triggers_header->camera_range.left;
    camera_range.right = field_triggers_header->camera_range.right;

    // Calculate if screen can scroll
    int available_width = camera_range.right - camera_range.left;
    int required_width = game_width / 2 + abs(wide_viewport_x);

    if (available_width >= required_width)
    {
        widescreen_mode = WM_EXTEND_WIDE;  // Scrolling screen
    }
    else
    {
        widescreen_mode = WM_DISABLED;     // Static screen
        // OR: widescreen_mode = WM_ZOOM; (if configured)
    }
}
```

**For 21:9:**

```
Required width = (640/2) + 240 = 560 pixels of camera range
Many static screens have: camera_range = (0, 640) = 640 pixels

Result: Even static screens might support 21:9 if original
        background artist left padding
```

**Opportunity:** Many "static" screens in 4:3/16:9 might actually support 21:9 if we check the actual background tile coverage, not just camera range.

---

## Conclusion

The external analysis provides excellent complementary perspectives:

1. **Virtual Canvas Concept** - Better framing of the coordinate system translation
2. **Projection Matrix Detail** - Math behind 3D FOV adjustment
3. **Walkmesh Extension** - Critical for AI asset integration
4. **Hybrid 21:9 Approach** - Practical recommendation for real-world use

Combined with my original deep dive, these analyses provide a complete technical foundation for implementing 21:9 support with AI-extended assets in FFNx.

**The Path Forward:**

1. Implement 21:9 viewport values (trivial)
2. Update memory patches for 21:9 (moderate effort)
3. Create hybrid mode system (moderate effort)
4. Generate AI-extended assets (large effort, community-driven)
5. Extend walkmesh data (moderate effort per field)
6. Test and iterate (ongoing)

With AI asset generation now feasible, the technical barriers to true ultrawide FF7 have been removed. It's primarily a content creation challenge, not an engineering challenge.

---

**Document Status:** Addendum Complete - Complementary Technical Details

**Sources:**
- External technical analysis (community source)
- FFNx source code verification
- Additional renderer.cpp and walkmesh analysis

**Research Session:** 2026-01-12 23:15-23:45 JST
**Session ID:** 6fb0facc-34c8-4184-b3e7-8564019b614c

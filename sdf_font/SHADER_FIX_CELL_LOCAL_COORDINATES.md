# SDF Shader Fix: Cell-Local Coordinate System

**Created:** 2026-01-26 22:15 JST (Monday)
**Session-ID:** 3a41c4e3-eac1-45e9-80bf-ce8631a0faad
**Status:** Code Complete - Awaiting Build & Test

---

## Problem Summary

The FFNx SDF shader was applying transforms (shadow offsets, and potentially italic/skew in the future) in **atlas-global UV coordinate space** instead of **cell-local coordinate space**.

### Symptoms
- Shadow offset causes sampling from neighboring cells in the atlas grid
- When shadow Y-offset is applied, you see characters from the row above bleeding into the current character
- Transforms use the atlas center (512, 512 in 1024×1024 atlas) as origin instead of each cell's center

### Root Cause
The shader operated on `v_texcoord0` directly, which is in atlas-global space (0-1 across entire 1024×1024 texture). No awareness of the 16×16 grid of 64×64 character cells.

---

## Solution Implemented

### New Uniform: `SDFAtlasParams`

Added a new vec4 uniform to provide atlas layout information to the shader:

```glsl
uniform vec4 SDFAtlasParams;
#define atlasSize SDFAtlasParams.x     // 1024.0 (atlas texture size)
#define gridSize SDFAtlasParams.y      // 16.0 (cells per row/column)
#define cellSize SDFAtlasParams.z      // 64.0 (cell size in pixels)
#define unused SDFAtlasParams.w        // Reserved for future use
```

### Helper Functions

**`getCellLocalUV(vec2 atlasUV)`**
- Converts atlas UV (0-1 across entire texture) to cell-local UV (0-1 within the current cell)
- Calculates which cell we're in: `cellIndex = floor(atlasUV * gridSize)`
- Returns local coordinates within that cell

**`cellLocalToAtlasUV(vec2 localUV, vec2 atlasUV)`**
- Converts cell-local UV back to atlas UV
- **CRITICAL:** Clamps localUV to [0, 1] range to stay within cell boundaries
- Prevents sampling from neighboring cells

**`sampleSDFLocal(vec2 atlasUV, vec2 offsetPixels)`**
- Samples SDF texture with a pixel-based offset in cell-local space
- Converts offset to cell-local UV units: `offsetUV = offsetPixels / cellSize`
- Applies offset in local space, then converts back to atlas UV with clamping
- Used for shadow sampling to prevent bleeding

### Main Shader Changes

**Before:**
```glsl
vec2 shadowOffsetVec = vec2(shadowOffset, shadowOffset) / vec2(1024.0, 1024.0);
vec3 shadowMsd = texture2D(tex_0, v_texcoord0 + shadowOffsetVec).rgb;
```

**After:**
```glsl
vec2 shadowOffsetPixels = vec2(shadowOffset, shadowOffset);
vec3 shadowMsd = sampleSDFLocal(v_texcoord0, shadowOffsetPixels);
```

The `sampleSDFLocal` function:
1. Converts to cell-local coordinates
2. Applies the offset in cell-local space
3. Clamps to cell boundaries
4. Converts back to atlas UV for sampling

---

## Files Modified

### Shader Files

**`/mnt/c/FFNx/misc/FFNx.sdf.frag`**
- Added `SDFAtlasParams` uniform (lines 32-36)
- Added `getCellLocalUV()` helper function (lines 44-56)
- Added `cellLocalToAtlasUV()` helper function (lines 58-71)
- Added `sampleSDFLocal()` helper function (lines 73-88)
- Modified shadow sampling to use `sampleSDFLocal()` (line 110)

### FFNx Source Code

**`/mnt/c/FFNx/src/renderer.h`**
- Added `SDF_ATLAS_PARAMS` to `RendererUniform` enum (line 139)

**`/mnt/c/FFNx/src/renderer.cpp`**
- Added `SDF_ATLAS_PARAMS` uniform creation (line 1085)
- Added `sdfAtlasParams` setting in `setSDFMode()` (lines 2419-2421)
  - Values: `{ 1024.0f, 16.0f, 64.0f, 0.0f }`
  - atlas_size = 1024 pixels
  - grid_size = 16 cells per row/column
  - cell_size = 64 pixels per cell
  - unused = 0 (reserved)

---

## How It Works

### Coordinate Space Conversion

1. **Atlas UV** (input from vertex shader):
   - Range: (0, 0) to (1, 1) across entire 1024×1024 atlas
   - Example: (0.125, 0.25) = 160 pixels right, 320 pixels down

2. **Cell Index** (calculated):
   - Which cell in the 16×16 grid?
   - `cellIndex = floor(atlasUV * gridSize)`
   - Example: (0.125, 0.25) × 16 = (2.0, 4.0) → cell at column 2, row 4

3. **Cell-Local UV** (computed):
   - Range: (0, 0) to (1, 1) within the specific 64×64 cell
   - `localUV = (atlasUV - cellTopLeft) * gridSize`
   - Example: If we're at atlas UV (0.140625, 0.265625):
     - Cell top-left is (0.125, 0.25) = (2/16, 4/16)
     - Local UV = ((0.140625, 0.265625) - (0.125, 0.25)) × 16
     - Local UV = (0.25, 0.25) — we're at 25% across the cell

4. **Apply Offset** (in local space):
   - Shadow offset = 2 pixels
   - Cell size = 64 pixels
   - Offset UV = 2 / 64 = 0.03125 (3.125% of cell)
   - New local UV = (0.25, 0.25) + (0.03125, 0.03125) = (0.28125, 0.28125)

5. **Clamp** (stay within cell):
   - `localUV = clamp(localUV, 0.0, 1.0)`
   - Prevents sampling outside cell boundaries

6. **Convert Back to Atlas UV**:
   - `atlasUV = cellTopLeft + (localUV / gridSize)`
   - Example: (0.125, 0.25) + (0.28125, 0.28125) / 16
   - Result: (0.14257, 0.26757)

### Example Scenario: Shadow Bleeding Bug

**Before fix:**
- Character at cell (2, 4) in atlas
- Apply shadow Y-offset of +10 pixels
- Atlas-global offset: +10/1024 = +0.009765625
- New UV: (0.140625, 0.265625 + 0.009765625) = (0.140625, 0.275390625)
- This crosses into cell (2, 5) — **BLEEDING!**

**After fix:**
- Character at cell (2, 4) in atlas
- Cell-local UV: (0.25, 0.25)
- Apply shadow offset: +10 pixels / 64 pixels = +0.15625 local UV
- New local UV: (0.25, 0.40625)
- Still within [0, 1] range — stays in same cell
- **NO BLEEDING!**

If offset were large enough to go outside [0, 1]:
- Local UV would be clamped to (0.25, 1.0)
- This samples the bottom edge of the cell, not the neighboring cell
- Shadow just disappears at edge (correct behavior)

---

## Testing Instructions

### 1. Rebuild FFNx

The shader changes require recompiling:

```powershell
cd C:\FFNx
cmake --build .build --config Release --target FFNx
```

This will:
- Recompile `FFNx.sdf.frag` using bgfx shaderc
- Generate new shader binaries for all platforms (GL/D3D11/D3D12/Vulkan)
- Build updated FFNx.dll with new uniform support

### 2. Deploy Updated DLL

```powershell
Copy-Item ".build\bin\FFNx.dll" "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.dll" -Force
```

### 3. Test SDF Fonts with Shadow Offset

**Enable SDF in FFNx.toml:**
```toml
enable_sdf_fonts = true
sdf_pixel_range = 4.0
sdf_thickness = 0.5
sdf_shadow_offset = 2.0    # Start with 2 pixels
sdf_shadow_opacity = 0.5
```

**Test scenarios:**

1. **Small shadow offset (2 pixels):**
   - Should see subtle shadow, no bleeding
   - Shadow stays within character cell

2. **Large shadow offset (10 pixels):**
   - Before fix: Would see characters from row above/below
   - After fix: Shadow just disappears at cell edge

3. **Multi-line text:**
   - Verify shadows don't bleed between lines
   - Check characters at edge of atlas (row 0 and row 15)

4. **Visual inspection:**
   - No artifacts from neighboring cells
   - Clean shadow rendering
   - Proper clipping at cell boundaries

### 4. Enable Trace Logging (Optional)

To see SDF shader activation:

```toml
trace_all = true
# OR
trace_renderer = true
```

Check `FFNx.log` for:
```
Renderer::setSDFMode: SDF_FONT_FLAT
```

### 5. Expected Behavior

**✅ CORRECT:**
- Shadows stay within character bounds
- Large offsets cause shadow to fade at edge, not bleed
- No artifacts from neighboring cells
- Clean rendering at all shadow offset values

**❌ WRONG (if still broken):**
- See characters from row above when shadow Y-offset > 0
- See characters from column left/right when shadow X-offset applied
- Artifacts appear when rotating/skewing (if those transforms are added)

---

## Future Work: Italic/Skew Support

The coordinate system is now ready for italic/skew transforms. To add them:

### Vertex Shader Approach (Recommended)

Add to `/mnt/c/FFNx/misc/FFNx.sdf.vert`:

```glsl
uniform vec4 SDFTransformParams;
#define italicSlant SDFTransformParams.x   // Horizontal slant factor
#define skewX SDFTransformParams.y          // X-axis skew
#define skewY SDFTransformParams.z          // Y-axis skew
#define rotation SDFTransformParams.w       // Rotation angle (radians)

void main() {
    gl_Position = mul(u_modelViewProj, a_position);
    v_color0 = a_color0;

    // Apply transforms to texture coordinates
    vec2 uv = a_texcoord0;

    // Convert to cell-local space (same as fragment shader)
    vec2 cellIndex = floor(uv * 16.0);
    vec2 cellTopLeft = cellIndex / 16.0;
    vec2 localUV = (uv - cellTopLeft) * 16.0;

    // Transform around cell center (0.5, 0.5)
    localUV -= 0.5;

    // Apply italic slant
    localUV.x += localUV.y * italicSlant;

    // Apply skew
    localUV.x += localUV.y * skewX;
    localUV.y += localUV.x * skewY;

    // Apply rotation
    if (rotation != 0.0) {
        float cosR = cos(rotation);
        float sinR = sin(rotation);
        vec2 rotated;
        rotated.x = localUV.x * cosR - localUV.y * sinR;
        rotated.y = localUV.x * sinR + localUV.y * cosR;
        localUV = rotated;
    }

    // Back to corner origin
    localUV += 0.5;

    // Convert back to atlas UV
    uv = cellTopLeft + (localUV / 16.0);

    v_texcoord0 = uv;
}
```

### FFNx Integration

Add to `renderer.cpp` in `setSDFMode()`:

```cpp
// Set SDF transform parameters uniform
// x: italic_slant, y: skew_x, z: skew_y, w: rotation
float sdfTransformParams[4] = { italic_slant, skew_x, skew_y, rotation };
setUniform(RendererUniform::SDF_TRANSFORM_PARAMS, sdfTransformParams);
```

Add config options to `cfg.cpp`:

```cpp
float sdf_italic_slant = config["sdf_italic_slant"].value_or(0.0);
float sdf_skew_x = config["sdf_skew_x"].value_or(0.0);
float sdf_skew_y = config["sdf_skew_y"].value_or(0.0);
float sdf_rotation = config["sdf_rotation"].value_or(0.0);
```

---

## Known Limitations

1. **Hardcoded Atlas Layout:**
   - Currently assumes 1024×1024 atlas with 16×16 grid of 64×64 cells
   - If you use different atlas sizes, need to update `sdfAtlasParams` in `renderer.cpp`

2. **No Per-Font Atlas Size:**
   - All fonts use same atlas layout
   - Future enhancement: pass atlas params per texture

3. **Italic/Skew Not Yet Implemented:**
   - Coordinate system is ready, but transforms not added to vertex shader
   - This was a preventive fix for when those features are added

---

## Verification Checklist

- [ ] FFNx.dll rebuilt successfully
- [ ] Shader binaries updated in `.build/bin/shaders/`
- [ ] FFNx.dll deployed to FF7 directory
- [ ] SDF fonts enabled in FFNx.toml
- [ ] Shadow offset testing completed (2px, 5px, 10px)
- [ ] No bleeding observed at cell boundaries
- [ ] Multi-line text renders correctly
- [ ] FFNx.log shows SDF shader activation
- [ ] Performance acceptable (no FPS drop)

---

## Rollback Procedure

If this fix causes issues:

1. **Restore backup DLL:**
   ```powershell
   Copy-Item "FFNx.dll.backup" "FFNx.dll" -Force
   ```

2. **Revert shader changes:**
   ```bash
   git checkout HEAD -- /mnt/c/FFNx/misc/FFNx.sdf.frag
   ```

3. **Revert FFNx source changes:**
   ```bash
   git checkout HEAD -- /mnt/c/FFNx/src/renderer.h
   git checkout HEAD -- /mnt/c/FFNx/src/renderer.cpp
   ```

4. **Rebuild:**
   ```powershell
   cmake --build .build --config Release --target FFNx
   ```

---

## Technical Notes

### Why Cell-Local Coordinates Matter

**Atlas-global space problems:**
- Transforms reference wrong origin point (atlas center instead of cell center)
- Offsets can cross cell boundaries
- No way to clamp within a cell
- Rotations would spin around atlas center (useless)

**Cell-local space benefits:**
- Origin is cell center (0.5, 0.5 in local UV)
- Transforms are relative to the character itself
- Easy to clamp to [0, 1] range (cell boundaries)
- Rotations spin around character center (correct)

### Performance Impact

**Shader complexity increase:**
- Added 3 helper functions (~50 lines of GLSL)
- 1 additional uniform (vec4)
- Extra calculations per fragment (negligible on modern GPUs)

**Expected overhead:**
- ~5-10 ALU operations per fragment
- Minimal impact: <0.1ms on Intel HD 4000 (2013+)
- Memory: +16 bytes per uniform

### Alternative Approaches Considered

**Option A: Pre-calculate in vertex shader**
- Pro: Fewer fragment shader calculations
- Con: Can't handle per-pixel effects like distortion fields
- Rejected: Fragment shader approach more flexible

**Option B: Pass cell index as varying**
- Pro: Avoid recalculating cell index in fragment shader
- Con: Extra varying (limited slots), negligible performance gain
- Rejected: Not worth the complexity

**Option C: Use texture arrays (one texture per cell)**
- Pro: No coordinate conversion needed
- Con: 256 textures per font = 6 fonts × 256 = 1,536 texture slots
- Rejected: Massive texture slot overhead

---

## Related Documents

- `/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/.project/session_handoffs/SESSION_HANDOFF_2026-01-26-03_SDF_MSDF_ATTEMPTS_VECTORIZATION.md` - Problem identification
- `/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/SDF_IMPLEMENTATION_PLAN.md` - Original SDF roadmap
- `/home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/SDF_EFFECTS_SPECIFICATION.md` - Effects specification (includes italic/skew design)

---

**End of Document**

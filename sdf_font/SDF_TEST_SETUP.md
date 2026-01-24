# SDF Font System - Test Setup Guide

**Date:** 2026-01-24 15:36 JST (Saturday)
**Session:** 1a021af6-6736-45cb-9669-eeb60f2a2030
**Status:** Ready for Testing

---

## Test Files Prepared

### Japanese Character SDF Textures

All test files have been generated and copied to FFNx textures directory:

**Location:** `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/mods/Textures/`

**Files:**
1. `char_hiragana_a_sdf.png` (1,298 bytes)
   - Source: Japanese hiragana character 'あ'
   - Original: 64×64 bitmap
   - SDF: 64×64, 4-pixel range

2. `char_kanji_1_sdf.png` (1,190 bytes)
   - Source: Japanese kanji character
   - Original: 64×64 bitmap
   - SDF: 64×64, 4-pixel range

3. `char_kanji_2_sdf.png` (1,158 bytes)
   - Source: Japanese kanji character
   - Original: 64×64 bitmap
   - SDF: 64×64, 4-pixel range

### Configuration

**FFNx.toml Location:** `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/FFNx.toml`

**Added Configuration:**
```toml
# SDF Font Rendering (Phase 1 Proof of Concept)
enable_sdf_fonts = true
sdf_pixel_range = 4.0
```

---

## Build Status

**Code Changes Committed:**
- ✅ Configuration system (enable_sdf_fonts, sdf_pixel_range)
- ✅ Shader compilation (all platforms)
- ✅ Renderer integration (programs, uniforms)
- ✅ Texture detection ("_sdf" in filename)
- ✅ Automatic shader selection
- ✅ SDF_PARAMS uniform setting

**Commits:**
- FFNx repo commit `769a551`: Shader compilation
- FFNx repo commit `7565dd1`: Renderer integration
- FFNx repo commit `0db0130`: Texture detection & selection

**Build Required:**
FFNx must be rebuilt with the latest changes for the SDF system to be active:
```bash
cd /mnt/c/FFNx
cmake --build .build --config Release --target FFNx
```

Then copy the new `FFNx.dll` to the FF7 installation:
```bash
cp /mnt/c/FFNx/.build/bin/FFNx.dll "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/"
```

---

## Expected Behavior

### When SDF System is Active

**1. Texture Loading:**
When FFNx loads a texture with "_sdf" in the filename:
```
FFNx.log: Created external SDF texture: [ID] from ...char_hiragana_a_sdf.png
FFNx.log: gl_set_texture: enabled SDF mode for texture [ID]
```

**2. Shader Selection:**
When rendering an SDF texture:
```
FFNx.log: Renderer::setSDFMode: SDF_FONT_SMOOTH
  (or SDF_FONT_FLAT depending on interpolation quality)
```

**3. Visual Quality:**
- **At native resolution (64×64):** Identical to bitmap
- **Scaled up (128×128, 256×256):** Sharp, smooth edges with anti-aliasing
- **Scaled down (32×32, 16×16):** Maintains detail better than bitmap

**4. Performance:**
- Minimal overhead (SDF shader ~10 ALU operations)
- Expected impact: <0.1ms per frame
- VRAM: Same or slightly less than bitmap

---

## Testing Procedure

### Option 1: Modify Japanese Font Texture (Recommended)

Replace an existing Japanese font character with our SDF version:

**Find the Japanese font texture:**
```bash
ls -la "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/"jafont*
```

**Create SDF version:**
```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font
python3 png_to_sdf.py jafont_1.png jafont_1_sdf.png 4
```

**Copy to mods directory:**
```bash
cp jafont_1_sdf.png "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/mods/Textures/"
```

### Option 2: Direct Test with Menu Characters

The SDF test characters are already in place. To verify:

1. **Launch FF7**
2. **Enable trace logging** (in FFNx.toml):
   ```toml
   trace_all = true
   ```
3. **Check FFNx.log** for SDF detection messages
4. **Look for visual differences** when SDF textures are used

---

## Verification Checklist

- [ ] FFNx rebuilt with SDF changes (commits 769a551, 7565dd1, 0db0130)
- [ ] FFNx.dll copied to FF7 installation directory
- [ ] SDF test textures present in `mods/Textures/`
- [ ] `enable_sdf_fonts = true` in FFNx.toml
- [ ] `sdf_pixel_range = 4.0` in FFNx.toml
- [ ] FFNx.log contains "Created external SDF texture" messages
- [ ] FFNx.log contains "enabled SDF mode" messages
- [ ] FFNx.log contains "setSDFMode: SDF_FONT" messages
- [ ] Visual quality improved at non-native scales

---

## Next Steps

### If Test Succeeds:
1. Convert all Japanese font sheets (jafont_1-6) to SDF
2. Test with actual in-game text rendering
3. Measure performance impact
4. Document visual quality improvements
5. Proceed to Phase 2 (full Japanese font conversion)

### If Test Fails:
1. Check FFNx.log for errors
2. Verify shader compilation succeeded
3. Verify texture detection is working
4. Debug shader selection logic
5. Check uniform values are being set correctly

---

## Files Created This Session

**Test Assets:**
- `test_japanese/char_hiragana_a.png` (source bitmap)
- `test_japanese/char_hiragana_a_sdf.png` (SDF texture)
- `test_japanese/char_kanji_1.png` (source bitmap)
- `test_japanese/char_kanji_1_sdf.png` (SDF texture)
- `test_japanese/char_kanji_2.png` (source bitmap)
- `test_japanese/char_kanji_2_sdf.png` (SDF texture)

**Deployed:**
- All `*_sdf.png` files copied to FFNx textures directory
- FFNx.toml updated with SDF configuration

**Documentation:**
- This file: `SDF_TEST_SETUP.md`

---

## Technical Notes

### SDF Detection Pattern
Filename must contain "_sdf" substring (case-sensitive).

Examples:
- ✅ `char_hiragana_a_sdf.png` → Detected as SDF
- ✅ `jafont_1_sdf.png` → Detected as SDF
- ❌ `char_hiragana_a.png` → Not detected (standard bitmap)
- ❌ `char_SDF.png` → Not detected (case-sensitive)

### Shader Program Selection
Based on current interpolation qualifier:
- `FLAT` → `SDF_FONT_FLAT`
- `SMOOTH` → `SDF_FONT_SMOOTH`

### SDF Parameters
Uniform `SDFParams` is set to:
```cpp
float sdfParams[4] = { 4.0, 0.0, 0.0, 0.0 };
// sdfParams.x = pxRange (distance field spread in pixels)
```

---

**Status:** Test environment prepared. Awaiting FFNx rebuild and deployment.

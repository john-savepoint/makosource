# FF7 SDF Font Implementation Plan

**Created:** 2026-01-23 13:50:00 JST (Friday)
**Session ID:** 1a021af6-6736-45cb-9669-eeb60f2a2030
**Author:** Claude Code
**Status:** Planning Phase
**Related:** SDF_INVESTIGATION_FINDINGS.md

---

## Overview

This document outlines the complete implementation plan for converting Final Fantasy VII's font system from bitmap textures to Signed Distance Fields (SDF). This plan is based on the findings documented in `SDF_INVESTIGATION_FINDINGS.md`.

---

## Implementation Phases

### Phase 1: Proof of Concept (2 weeks)

**Goal:** Verify SDF rendering works with FFNx and looks good

**Tasks:**

1. **Environment Setup** (Day 1-2)
   ```bash
   # Install msdfgen
   git clone https://github.com/Chlumsky/msdfgen.git
   cd msdfgen
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release
   cmake --build .

   # Install msdf-bmfont-xml
   npm install -g msdf-bmfont-xml
   ```

2. **Test SDF Generation** (Day 3-4)
   ```bash
   # Extract single character for testing
   python extract_char.py jafont_1.png --char 0x42 --output test_char.png

   # Generate SDF
   msdf-bmfont-xml test_char.png \
     --output test_char_sdf.png \
     --field-type msdf \
     --texture-size 32 32 \
     --distance-range 4

   # Visual verification
   open test_char_sdf.png  # Check RGB channels
   ```

3. **Create SDF Fragment Shader** (Day 5-6)
   ```glsl
   // misc/FFNx.sdf.frag

   $input v_color0, v_texcoord0

   #include "common.sh"

   SAMPLER2D(tex_sdf, 0);

   uniform vec4 SDFParams;
   #define pxRange SDFParams.x  // 4.0 default

   float median(float r, float g, float b) {
       return max(min(r, g), min(max(r, g), b));
   }

   void main() {
       vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
       float sd = median(msd.r, msd.g, msd.b);
       float screenPxDistance = pxRange * (sd - 0.5);
       float opacity = clamp(screenPxDistance + 0.5, 0.0, 1.0);
       gl_FragColor = vec4(v_color0.rgb, v_color0.a * opacity);
   }
   ```

4. **Minimal FFNx Integration** (Day 7-8)
   ```cpp
   // src/gl/texture.cpp - Add detection

   bool is_sdf_texture(const char* filename) {
       return strstr(filename, "_sdf") != NULL;
   }

   void gl_upload_texture(/*...*/) {
       // ... existing code ...

       if (is_sdf_texture(texture_filename)) {
           VRASS(texture_set, ogl.gl_set->use_sdf_shader, true);
           ffnx_info("SDF texture detected: %s\n", texture_filename);
       }
   }
   ```

5. **Single Character Test** (Day 9-10)
   - Modify japanese_text.cpp to use test_char_sdf.png
   - Render single character at multiple scales:
     - 8×8 pixels (0.5× scale)
     - 16×16 pixels (1× scale)
     - 32×32 pixels (2× scale)
     - 64×64 pixels (4× scale)
   - Visual quality assessment
   - Performance measurement

**Deliverables:**
- ✅ Working SDF shader
- ✅ Single character rendering at multiple scales
- ✅ Quality validation (smooth edges, sharp at all sizes)
- ✅ Performance baseline (<0.1ms overhead)

**Success Criteria:**
- SDF character visibly sharper than bitmap at 2× scale
- No jagged edges at any scale
- FPS impact <5%

---

### Phase 2: Full Japanese Font Conversion (2 weeks)

**Goal:** Convert all 6 Japanese font sheets to SDF

**Tasks:**

1. **Character Cell Extraction Script** (Day 1-2)
   ```python
   # scripts/extract_font_cells.py

   import numpy as np
   from PIL import Image

   def extract_cells(font_image, grid_size=16, cell_size=32):
       """Extract individual character cells from font sheet"""
       img = Image.open(font_image)
       cells = []

       for row in range(grid_size):
           for col in range(grid_size):
               x = col * cell_size
               y = row * cell_size
               cell = img.crop((x, y, x + cell_size, y + cell_size))
               cells.append(cell)

       return cells

   # Extract all cells from jafont_1.png
   cells = extract_cells('jafont_1.png')
   for i, cell in enumerate(cells):
       cell.save(f'cells/jafont_1_char_{i:03d}.png')
   ```

2. **Batch SDF Generation** (Day 3-5)
   ```bash
   # scripts/batch_sdf_convert.sh

   #!/bin/bash

   for font in {1..6}; do
       echo "Converting jafont_$font..."

       # Generate MSDF for entire font sheet
       msdf-bmfont-xml "jafont_${font}.png" \
         --output "jafont_${font}_sdf.png" \
         --field-type msdf \
         --texture-size 256 256 \
         --font-size 32 \
         --distance-range 4 \
         --smart-size

       echo "✅ jafont_$font converted"
   done
   ```

3. **Grid Layout Preservation** (Day 6-7)
   ```python
   # scripts/pack_sdf_atlas.py

   def pack_sdf_atlas(cells, output_size=256, grid_size=16):
       """Pack SDF cells into 16×16 grid atlas"""
       cell_size = output_size // grid_size  # 16 pixels per cell

       atlas = Image.new('RGB', (output_size, output_size))

       for i, cell_sdf in enumerate(cells):
           row = i // grid_size
           col = i % grid_size
           x = col * cell_size
           y = row * cell_size

           # Resize cell to fit grid
           cell_resized = cell_sdf.resize((cell_size, cell_size))
           atlas.paste(cell_resized, (x, y))

       return atlas
   ```

4. **Quality Validation** (Day 8-9)
   ```python
   # scripts/validate_sdf_quality.py

   def validate_sdf(original, sdf, threshold=0.9):
       """Compare SDF quality against original at multiple scales"""
       scales = [0.5, 1.0, 2.0, 4.0]
       scores = []

       for scale in scales:
           # Render both at scale
           orig_rendered = render_bitmap(original, scale)
           sdf_rendered = render_sdf(sdf, scale)

           # Compare (SSIM or PSNR)
           score = compare_images(orig_rendered, sdf_rendered)
           scores.append((scale, score))

       return scores
   ```

5. **Integration with FFNx** (Day 10)
   - Place SDF textures in `mods/Textures/`
   - Test loading all 6 fonts
   - Verify memory usage (should be ~1.15MB)
   - Profile VRAM allocation

**Deliverables:**
- ✅ 6 SDF font sheets (jafont_1_sdf.png through jafont_6_sdf.png)
- ✅ Automated conversion pipeline
- ✅ Quality validation report
- ✅ VRAM usage confirmation

**Success Criteria:**
- All 256 characters per font rendered correctly
- <5% quality loss vs original (measured by SSIM)
- 81% VRAM reduction confirmed

---

### Phase 3: FFNx Integration & Config (2 weeks)

**Goal:** Full integration into FFNx with user controls

**Tasks:**

1. **Texture Loader Modification** (Day 1-2)
   ```cpp
   // src/gl/texture.cpp

   struct gl_texture_set {
       // ... existing fields ...
       bool use_sdf_shader;  // NEW
       float sdf_px_range;   // NEW: tunable spread
   };

   void gl_upload_texture(struct texture_set *texture_set,
                          uint32_t palette_index,
                          void *image_data,
                          uint32_t format)
   {
       // ... existing code ...

       // Detect SDF texture
       if (is_sdf_texture(texture_filename)) {
           VRASS(texture_set, ogl.gl_set->use_sdf_shader, true);
           VRASS(texture_set, ogl.gl_set->sdf_px_range,
                 sdf_pixel_range);  // From config

           if (trace_all || trace_loaders) {
               ffnx_info("SDF texture loaded: %s (range: %.1f)\n",
                        texture_filename, sdf_pixel_range);
           }
       }

       // ... rest unchanged ...
   }
   ```

2. **Shader Selection Logic** (Day 3-4)
   ```cpp
   // src/gl/gl.cpp

   void gl_bind_texture_set(struct texture_set *_texture_set)
   {
       VOBJ(texture_set, texture_set, _texture_set);

       if (VPTR(texture_set)) {
           struct gl_texture_set* gl_set = VREF(texture_set, ogl.gl_set);

           // Select appropriate shader
           if (gl_set->use_sdf_shader) {
               newRenderer.setProgram(sdf_shader_program);

               // Set SDF uniforms
               float params[4] = {
                   gl_set->sdf_px_range,  // pxRange
                   0.0f, 0.0f, 0.0f       // Reserved for future
               };
               newRenderer.setUniform("SDFParams", params, 4);
           } else {
               newRenderer.setProgram(standard_shader_program);
           }

           // ... rest of binding ...
       }
   }
   ```

3. **Configuration System** (Day 5)
   ```cpp
   // src/cfg.h
   extern bool use_sdf_fonts;
   extern float sdf_pixel_range;
   extern bool sdf_debug_mode;

   // src/cfg.cpp
   bool use_sdf_fonts = false;
   float sdf_pixel_range = 4.0f;
   bool sdf_debug_mode = false;

   void read_cfg()
   {
       // ... existing config ...

       use_sdf_fonts = config["use_sdf_fonts"].value_or(false);
       sdf_pixel_range = config["sdf_pixel_range"].value_or(4.0f);
       sdf_debug_mode = config["sdf_debug_mode"].value_or(false);

       if (use_sdf_fonts) {
           ffnx_info("SDF fonts enabled (range: %.1f)\n", sdf_pixel_range);
       }
   }
   ```

4. **FFNx.toml Configuration** (Day 5)
   ```toml
   ###############################################################################
   # SDF Font Rendering
   ###############################################################################

   # Enable signed distance field fonts
   # Provides sharp, resolution-independent text rendering
   # Requires SDF font textures (*_sdf.png) in mods/Textures/
   use_sdf_fonts = false

   # SDF pixel range (distance field spread)
   # Higher values = smoother edges, but may blur fine details
   # Lower values = sharper edges, but may show artifacts
   # Recommended: 4.0 for most fonts
   sdf_pixel_range = 4.0

   # Enable SDF debug visualization
   # Shows distance field heatmap instead of rendered glyphs
   sdf_debug_mode = false
   ```

5. **Fallback Logic** (Day 6)
   ```cpp
   // src/ff7/japanese_text.cpp

   std::string get_font_texture_path(int page_num) {
       if (use_sdf_fonts) {
           char sdf_path[256];
           snprintf(sdf_path, sizeof(sdf_path),
                   "jafont_%d_sdf.png", page_num);

           if (file_exists_in_mod_path(sdf_path)) {
               ffnx_info("Using SDF font: %s\n", sdf_path);
               return sdf_path;
           } else {
               ffnx_warning("SDF font not found, falling back to bitmap: %s\n",
                          sdf_path);
           }
       }

       // Fallback to original TIM
       char tim_path[256];
       snprintf(tim_path, sizeof(tim_path), "jafont_%d.tim", page_num);
       return tim_path;
   }
   ```

6. **Debug Visualization** (Day 7-8)
   ```glsl
   // misc/FFNx.sdf.frag - Add debug mode

   uniform vec4 SDFDebugFlags;
   #define isDebugMode SDFDebugFlags.x > 0.0

   void main() {
       vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;

       if (isDebugMode) {
           // Visualize distance field as heatmap
           float sd = median(msd.r, msd.g, msd.b);
           vec3 heatmap = vec3(
               sd < 0.5 ? (0.5 - sd) * 2.0 : 0.0,  // Red outside
               sd > 0.5 ? (sd - 0.5) * 2.0 : 0.0,  // Green inside
               abs(sd - 0.5) < 0.1 ? 1.0 : 0.0     // Blue on edge
           );
           gl_FragColor = vec4(heatmap, 1.0);
       } else {
           // Normal SDF rendering
           float sd = median(msd.r, msd.g, msd.b);
           float screenPxDistance = pxRange * (sd - 0.5);
           float opacity = clamp(screenPxDistance + 0.5, 0.0, 1.0);
           gl_FragColor = vec4(v_color0.rgb, v_color0.a * opacity);
       }
   }
   ```

7. **Testing Matrix** (Day 9-10)
   - Test all text contexts:
     - [ ] Field dialogue
     - [ ] Menu text
     - [ ] Battle text
     - [ ] Name entry screen
     - [ ] Save/load screens
   - Test with SDF enabled/disabled
   - Test fallback when SDF files missing
   - Performance profiling in all contexts

**Deliverables:**
- ✅ Complete FFNx integration
- ✅ User-friendly configuration
- ✅ Fallback system working
- ✅ Debug visualization mode
- ✅ Test coverage report

**Success Criteria:**
- Config toggle works
- Fallback to bitmap seamless
- No crashes in any text context
- <5% FPS impact

---

### Phase 4: PS1 TEX System (4 weeks)

**Goal:** Support SDF for English/European palette-based fonts

**Tasks:**

1. **IDA Analysis** (Week 1: Day 1-5)
   ```python
   # Use IDA MCP to analyze TEX format

   # Find TEX loading function
   functions = mcp__ida_pro_mcp__lookup_funcs({"queries": ["load_tex"]})

   # Decompile key functions
   tex_loader = mcp__ida_pro_mcp__decompile({"addr": "0x688415"})
   palette_creator = mcp__ida_pro_mcp__decompile({"addr": "TBD"})

   # Find TEX file format signature
   tex_files = mcp__ida_pro_mcp__find_bytes({
       "patterns": "54 45 58 00"  # "TEX\0" header
   })

   # Analyze structure
   # Document findings in IDA_TEX_FORMAT_ANALYSIS.md
   ```

2. **TEX → RGBA Converter** (Week 1: Day 6-7, Week 2: Day 1-3)
   ```python
   # scripts/tex_to_rgba.py

   import struct

   class TexHeader:
       def __init__(self, data):
           self.version = struct.unpack('<I', data[0:4])[0]
           self.color_key = struct.unpack('<I', data[8:12])[0]
           self.palettes = struct.unpack('<I', data[44:48])[0]
           self.palette_entries = struct.unpack('<I', data[48:52])[0]
           self.bpp = struct.unpack('<I', data[52:56])[0]
           # ... parse full header based on IDA findings

   def tex_to_rgba(tex_file):
       with open(tex_file, 'rb') as f:
           data = f.read()

       header = TexHeader(data)

       # Extract palette
       palette_offset = # ... from header
       palette = parse_palette(data[palette_offset:],
                              header.palette_entries)

       # Extract indexed image data
       image_offset = # ... from header
       image_data = data[image_offset:]

       # Convert to RGBA
       rgba = np.zeros((header.height, header.width, 4), dtype=np.uint8)
       for y in range(header.height):
           for x in range(header.width):
               if header.bpp == 8:
                   idx = image_data[y * header.width + x]
               elif header.bpp == 4:
                   byte = image_data[(y * header.width + x) // 2]
                   idx = (byte >> ((x % 2) * 4)) & 0xF

               rgba[y, x] = palette[idx]

       return rgba
   ```

3. **RGBA → SDF Conversion** (Week 2: Day 4-7)
   ```python
   # scripts/rgba_to_sdf.py

   import subprocess

   def rgba_to_sdf(rgba_image, output_path):
       """Convert RGBA bitmap to MSDF"""

       # Save RGBA as temporary PNG
       temp_png = "temp_rgba.png"
       Image.fromarray(rgba_image).save(temp_png)

       # Generate MSDF
       subprocess.run([
           'msdf-bmfont-xml', temp_png,
           '--output', output_path,
           '--field-type', 'msdf',
           '--texture-size', '256', '256',
           '--distance-range', '4'
       ])

       # Clean up
       os.remove(temp_png)
   ```

4. **Hybrid SDF+Palette System** (Week 3)
   ```cpp
   // Strategy: Store SDF in RGB, palette hints in Alpha

   struct sdf_palette_texture {
       vec3 sdf;           // Multi-channel distance field
       uint8_t palette_id; // Which palette this uses (for effects)
   };

   // Shader approach
   vec4 sample = texture2D(tex_sdf_hybrid, v_texcoord0);
   vec3 msd = sample.rgb;        // Distance field
   float palette_hint = sample.a; // Palette ID (0-255)

   // Use palette_hint for special effects
   // (color cycling, palette swaps, etc.)
   ```

5. **English Font Conversion** (Week 3-4)
   - Extract usfont.tex from menu_us.lgp
   - Convert to RGBA using tex_to_rgba.py
   - Generate SDF using rgba_to_sdf.py
   - Test with English game version
   - Validate all menu/field text

6. **Multi-language Support** (Week 4)
   - French (menu_fr.lgp)
   - German (menu_de.lgp)
   - Spanish (menu_es.lgp)
   - Test language switching
   - Validate special characters (ü, é, ñ, etc.)

**Deliverables:**
- ✅ TEX format documentation (IDA analysis)
- ✅ TEX → RGBA converter
- ✅ RGBA → SDF pipeline
- ✅ English/FR/DE/ES SDF fonts
- ✅ Palette preservation system

**Success Criteria:**
- All Latin characters render correctly
- Special characters (accents) preserved
- Palette system compatible
- <10% quality loss vs original

---

### Phase 5: Advanced Features & Effects (2 weeks)

**Goal:** Implement SDF shader effects for enhanced visuals

**Tasks:**

1. **Outline Effects** (Day 1-3)
   ```glsl
   // Outline shader extension

   uniform vec4 OutlineParams;
   #define outlineWidth OutlineParams.x
   #define outlineColor OutlineParams.yzw

   void main() {
       vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
       float sd = median(msd.r, msd.g, msd.b);

       // Inner glyph
       float screenPxDist = pxRange * (sd - 0.5);
       float opacity = clamp(screenPxDist + 0.5, 0.0, 1.0);

       // Outline (distance from edge)
       float outlineDist = pxRange * (sd - (0.5 - outlineWidth));
       float outlineOpacity = clamp(outlineDist + 0.5, 0.0, 1.0);

       // Composite
       vec3 finalColor = mix(outlineColor, v_color0.rgb, opacity);
       float finalAlpha = max(opacity, outlineOpacity);

       gl_FragColor = vec4(finalColor, finalAlpha * v_color0.a);
   }
   ```

2. **Shadow/Glow Effects** (Day 4-6)
   ```glsl
   // Shadow shader extension

   uniform vec4 ShadowParams;
   #define shadowOffset ShadowParams.xy
   #define shadowColor ShadowParams.z
   #define shadowSoftness ShadowParams.w

   void main() {
       // Sample main glyph
       vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
       float sd = median(msd.r, msd.g, msd.b);
       float opacity = clamp(pxRange * (sd - 0.5) + 0.5, 0.0, 1.0);

       // Sample shadow (offset UV)
       vec2 shadowUV = v_texcoord0 + shadowOffset;
       vec3 shadowMsd = texture2D(tex_sdf, shadowUV).rgb;
       float shadowSd = median(shadowMsd.r, shadowMsd.g, shadowMsd.b);
       float shadowOpacity = clamp(pxRange * (shadowSd - 0.5) + 0.5, 0.0, 1.0);
       shadowOpacity *= shadowSoftness;

       // Composite (shadow behind glyph)
       vec3 finalColor = mix(
           vec3(shadowColor),
           v_color0.rgb,
           opacity
       );
       float finalAlpha = max(opacity, shadowOpacity);

       gl_FragColor = vec4(finalColor, finalAlpha * v_color0.a);
   }
   ```

3. **Weight/Bold Adjustment** (Day 7)
   ```glsl
   // Weight adjustment shader

   uniform vec4 WeightParams;
   #define weightBias WeightParams.x  // -0.1 to +0.1

   void main() {
       vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
       float sd = median(msd.r, msd.g, msd.b);

       // Adjust threshold for bold/thin
       float adjustedSd = sd + weightBias;
       float screenPxDist = pxRange * (adjustedSd - 0.5);
       float opacity = clamp(screenPxDist + 0.5, 0.0, 1.0);

       gl_FragColor = vec4(v_color0.rgb, v_color0.a * opacity);
   }
   ```

4. **Integration with FF7 Text System** (Day 8-10)
   ```cpp
   // Modify japanese_text.cpp to support effects

   struct TextEffectParams {
       bool enable_outline;
       float outline_width;
       float outline_color[3];

       bool enable_shadow;
       float shadow_offset[2];
       float shadow_color;
       float shadow_softness;

       float weight_bias;  // -0.1 to +0.1 for bold/thin
   };

   void set_text_effect_uniforms(TextEffectParams* params) {
       if (params->enable_outline) {
           float outlineParams[4] = {
               params->outline_width,
               params->outline_color[0],
               params->outline_color[1],
               params->outline_color[2]
           };
           newRenderer.setUniform("OutlineParams", outlineParams, 4);
       }

       // ... similar for shadow, weight, etc.
   }
   ```

**Deliverables:**
- ✅ Outline effect shader
- ✅ Shadow/glow effect shader
- ✅ Weight adjustment shader
- ✅ FFNx integration for effects
- ✅ Configuration API

**Success Criteria:**
- Effects render correctly
- Configurable via FFNx API
- <10% performance impact
- Effects work with all fonts

---

## File Structure

```
sdf_font/
├── docs/
│   ├── SDF_INVESTIGATION_FINDINGS.md     (✅ Created)
│   ├── SDF_IMPLEMENTATION_PLAN.md        (✅ This file)
│   ├── SDF_EFFECTS_SPECIFICATION.md      (Pending)
│   └── IDA_TEX_FORMAT_ANALYSIS.md        (Phase 4)
│
├── scripts/
│   ├── extract_font_cells.py
│   ├── batch_sdf_convert.sh
│   ├── pack_sdf_atlas.py
│   ├── validate_sdf_quality.py
│   ├── tex_to_rgba.py
│   └── rgba_to_sdf.py
│
├── shaders/
│   ├── FFNx.sdf.frag                     (Core SDF shader)
│   ├── FFNx.sdf_outline.frag             (With outline)
│   ├── FFNx.sdf_shadow.frag              (With shadow)
│   └── FFNx.sdf_effects.frag             (All effects)
│
├── textures/
│   ├── jafont_1_sdf.png
│   ├── jafont_2_sdf.png
│   ├── jafont_3_sdf.png
│   ├── jafont_4_sdf.png
│   ├── jafont_5_sdf.png
│   ├── jafont_6_sdf.png
│   └── usfont_sdf.png
│
└── tests/
    ├── test_sdf_rendering.cpp
    ├── test_quality_validation.py
    └── test_performance_benchmark.cpp
```

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| **Phase 1: Proof of Concept** | 2 weeks | Working SDF shader + single character |
| **Phase 2: Japanese Fonts** | 2 weeks | All 6 SDF font sheets |
| **Phase 3: FFNx Integration** | 2 weeks | Config, fallback, full integration |
| **Phase 4: PS1 TEX System** | 4 weeks | English/FR/DE/ES SDF fonts |
| **Phase 5: Advanced Effects** | 2 weeks | Outline, shadow, weight shaders |
| **Total** | **12 weeks** | Production-ready SDF font system |

---

## Risk Mitigation

### Risk: Quality Loss
- **Mitigation:** Automated quality validation (SSIM >0.95)
- **Fallback:** Increase texture resolution to 512×512 if needed

### Risk: Performance Issues
- **Mitigation:** Profiling at each phase
- **Fallback:** Optimize shader, reduce pxRange, or disable SDF

### Risk: TEX Format Unknown
- **Mitigation:** IDA MCP analysis in Phase 4
- **Fallback:** Manual reverse engineering, community knowledge

### Risk: Breaking Mods
- **Mitigation:** Backward compatibility fallback
- **Fallback:** Keep bitmap support indefinitely

---

## Success Metrics

### Quality Metrics:
- ✅ SSIM ≥ 0.95 vs original at native scale
- ✅ Sharp edges at 4× scale
- ✅ No jagged edges at any scale
- ✅ Smooth anti-aliasing

### Performance Metrics:
- ✅ <5% FPS impact
- ✅ 75%+ VRAM reduction
- ✅ <0.1ms fragment shader overhead

### User Experience:
- ✅ One-line config toggle
- ✅ Automatic fallback
- ✅ No crashes or visual glitches
- ✅ Works with all text contexts

---

## Next Steps

1. **Approve Plan** - Review and approve this implementation plan
2. **Phase 1 Start** - Begin proof of concept (Week 1-2)
3. **Progress Tracking** - Weekly status updates
4. **Phase Gates** - Quality review after each phase

---

**End of Implementation Plan**

**Status:** Ready for Approval
**Estimated Effort:** 12 weeks
**Resource Requirements:** 1 developer, IDA MCP access, test hardware

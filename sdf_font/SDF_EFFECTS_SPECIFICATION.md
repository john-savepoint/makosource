# FF7 SDF Font Effects - Technical Specification

**Created:** 2026-01-23 14:55:00 JST (Friday)
**Session ID:** 1a021af6-6736-45cb-9669-eeb60f2a2030
**Author:** Claude Code
**Status:** Specification Draft
**Related:** SDF_INVESTIGATION_FINDINGS.md, SDF_IMPLEMENTATION_PLAN.md

---

## Executive Summary

This document specifies the complete shader effects system for FF7's SDF font implementation. It covers both **preservation of existing effects** (rainbow cycling, blinking, colored text) and **new capabilities** unlocked by SDF rendering (outlines, shadows, glows, weight variations).

---

## Part 1: Existing FF7 Effects (Preservation)

### 1.1 Control Code System

FF7 embeds control codes in dialogue strings:

| Control Code | Effect | Color/Behavior |
|--------------|--------|----------------|
| `FE D2` | Static Color | Gray (106, 106, 106) |
| `FE D3` | Static Color | Orange (189, 98, 7) |
| `FE D4` | Static Color | Blue (10, 0, 189) |
| `FE D5` | Static Color | Magenta (230, 10, 230) |
| `FE D6` | Static Color | Green (124, 230, 90) |
| `FE D7` | Static Color | Yellow (230, 230, 10) |
| `FE D8` | Static Color | Cyan (10, 230, 230) |
| `FE D9` | Static Color | White (230, 230, 230) |
| `FE DA` | Animation | Blinking (67ms on/off) |
| `FE DB` | Animation | Rainbow cycle (533ms cycle) |

### 1.2 Current Implementation (CPU-Based)

**Per-Frame Animation Logic:**
```cpp
// Frame counter incremented globally (60fps)
frame_counter++;

// For each character
if (rainbow_enabled) {
    color_index = ((frame_counter >> 2) - char_position) & 7;
}
else if (blink_enabled) {
    color_index = ((frame_counter >> 2) & 1) ? static_color : 0;
}
else {
    color_index = static_color;
}

// Apply to vertices
vertex.color = color_palette[color_index];
```

**Timing:**
- **Blink:** 4 frames on + 4 frames off = 133ms cycle
- **Rainbow:** 4 frames per color × 8 colors = 533ms full cycle
- **Stagger:** Each character offset by 1 position (wave effect)

### 1.3 SDF Shader Approach (GPU-Based)

**Option A: CPU Pre-Calculation (Identical Behavior)**
- Keep existing CPU animation logic
- Pass computed color to shader via vertex attribute
- Shader receives `v_color0` already animated
- **Pro:** Zero code changes to animation system
- **Con:** CPU still doing per-frame work

**Option B: GPU Animation (Modern Approach)**
- Move animation logic into fragment shader
- Pass uniforms: `uFrameCounter`, `uEffectMode`, `uColorID`
- Shader computes color_index dynamically
- **Pro:** CPU-free, real-time, flexible
- **Con:** Requires shader modification

### 1.4 Recommended Approach: Hybrid

**For Initial Implementation (Phase 1-3):**
- Use Option A (CPU pre-calculation)
- Ensures 100% identical behavior
- Minimal code changes
- Easy testing/validation

**For Phase 5 (Advanced Features):**
- Add Option B (GPU animation) as alternative mode
- Config toggle: `use_gpu_text_animation = true`
- Enables advanced effects (per-pixel color gradients, etc.)

---

## Part 2: New SDF Effects Capabilities

### 2.1 Outline/Stroke Effects

**Description:** Add solid or gradient outline around characters

**Shader Implementation:**
```glsl
// Outline shader extension

uniform vec4 uOutlineParams;
#define outlineWidth uOutlineParams.x       // 0.0 to 0.2
#define outlineColor uOutlineParams.yzw     // RGB

void main() {
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);

    // Inner glyph (normal distance threshold)
    float innerDist = pxRange * (sd - 0.5);
    float innerAlpha = clamp(innerDist + 0.5, 0.0, 1.0);

    // Outer outline (extended distance threshold)
    float outerDist = pxRange * (sd - (0.5 - outlineWidth));
    float outerAlpha = clamp(outerDist + 0.5, 0.0, 1.0);

    // Outline alpha = difference
    float outlineAlpha = outerAlpha - innerAlpha;

    // Composite (outline behind glyph)
    vec3 finalColor = mix(outlineColor, v_color0.rgb, innerAlpha);
    float finalAlpha = max(innerAlpha, outlineAlpha);

    gl_FragColor = vec4(finalColor, finalAlpha * v_color0.a);
}
```

**Parameters:**
- `outlineWidth`: 0.0 to 0.2 (normalized distance)
  - 0.05 = thin outline (~2 pixels at 16px font)
  - 0.1 = medium outline (~4 pixels)
  - 0.2 = thick outline (~8 pixels)
- `outlineColor`: RGB (0.0-1.0 per channel)

**Use Cases:**
- High-contrast dialogue in bright areas
- Title text emphasis
- Important NPC names
- Menu headers

**Performance:** +5 ALU ops per pixel (~0.05ms at 720p)

---

### 2.2 Shadow Effects

**Description:** Offset drop shadow beneath characters

**Shader Implementation:**
```glsl
// Shadow shader extension

uniform vec4 uShadowParams;
#define shadowOffset uShadowParams.xy      // UV offset
#define shadowColor uShadowParams.z        // Grayscale
#define shadowSoftness uShadowParams.w     // 0.0 to 1.0

void main() {
    // Sample main glyph
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);
    float glyphAlpha = clamp(pxRange * (sd - 0.5) + 0.5, 0.0, 1.0);

    // Sample shadow (offset sampling)
    vec2 shadowUV = v_texcoord0 + shadowOffset / vec2(textureSize);
    vec3 shadowMsd = texture2D(tex_sdf, shadowUV).rgb;
    float shadowSd = median(shadowMsd.r, shadowMsd.g, shadowMsd.b);
    float shadowAlpha = clamp(pxRange * (shadowSd - 0.5) + 0.5, 0.0, 1.0);
    shadowAlpha *= shadowSoftness;

    // Composite (shadow behind glyph)
    vec3 shadowRGB = vec3(shadowColor);
    vec3 finalColor = mix(shadowRGB, v_color0.rgb, glyphAlpha);
    float finalAlpha = max(glyphAlpha, shadowAlpha);

    gl_FragColor = vec4(finalColor, finalAlpha * v_color0.a);
}
```

**Parameters:**
- `shadowOffset`: (x, y) in UV space
  - (0.01, 0.01) = subtle drop shadow
  - (0.02, 0.02) = pronounced shadow
  - Negative values for top/left shadow
- `shadowColor`: 0.0 (black) to 1.0 (white)
- `shadowSoftness`: 0.5 to 1.0
  - 0.5 = hard edge
  - 1.0 = fully visible

**Use Cases:**
- Dialogue over bright backgrounds
- Depth perception for layered UI
- Subtitle-style readability

**Performance:** +8 ALU ops + 1 texture sample (~0.1ms at 720p)

---

### 2.3 Glow/Halo Effects

**Description:** Soft luminous halo around characters

**Shader Implementation:**
```glsl
// Glow shader extension

uniform vec4 uGlowParams;
#define glowRadius uGlowParams.x          // 0.0 to 0.3
#define glowIntensity uGlowParams.y       // 0.0 to 2.0
#define glowColor uGlowParams.zw          // RG (B from v_color0)

void main() {
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);

    // Inner glyph
    float glyphDist = pxRange * (sd - 0.5);
    float glyphAlpha = clamp(glyphDist + 0.5, 0.0, 1.0);

    // Outer glow (soft falloff)
    float glowDist = pxRange * (sd - (0.5 - glowRadius));
    float glowAlpha = clamp(glowDist + 0.5, 0.0, 1.0);
    glowAlpha = pow(glowAlpha, 2.0) * glowIntensity;  // Soft curve

    // Glow color (blend with glyph color)
    vec3 glowRGB = vec3(glowColor, v_color0.b);
    vec3 finalColor = mix(glowRGB, v_color0.rgb, glyphAlpha);
    float finalAlpha = max(glyphAlpha, glowAlpha);

    gl_FragColor = vec4(finalColor, finalAlpha * v_color0.a);
}
```

**Parameters:**
- `glowRadius`: 0.05 to 0.3
  - 0.1 = subtle halo
  - 0.3 = dramatic glow
- `glowIntensity`: 0.5 to 2.0
  - 1.0 = normal brightness
  - 2.0 = bloom effect
- `glowColor`: RGB (can match or complement glyph)

**Use Cases:**
- Magical/mystical dialogue (Aerith, Sephiroth)
- Materia names in menus
- Special item descriptions
- Boss name reveals

**Performance:** +6 ALU ops per pixel (~0.08ms at 720p)

---

### 2.4 Weight/Bold Adjustment

**Description:** Dynamically adjust glyph thickness

**Shader Implementation:**
```glsl
// Weight adjustment shader

uniform vec4 uWeightParams;
#define weightBias uWeightParams.x  // -0.15 to +0.15

void main() {
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);

    // Adjust distance threshold
    float adjustedSd = sd + weightBias;
    float screenPxDist = pxRange * (adjustedSd - 0.5);
    float opacity = clamp(screenPxDist + 0.5, 0.0, 1.0);

    gl_FragColor = vec4(v_color0.rgb, v_color0.a * opacity);
}
```

**Parameters:**
- `weightBias`: -0.15 (thin) to +0.15 (bold)
  - -0.1 = light weight
  - 0.0 = normal (no adjustment)
  - +0.1 = bold weight
  - +0.15 = ultra-bold

**Use Cases:**
- Emphasized dialogue (shouting)
- Different character personalities (thin = timid, bold = aggressive)
- Menu hierarchy (bold headers, normal items)
- Accessibility (user-adjustable weight)

**Performance:** +2 ALU ops per pixel (~0.02ms at 720p)

---

### 2.5 Multi-Effect Combinations

**All Effects Simultaneously:**
```glsl
// Combined effects shader

void main() {
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);
    sd += weightBias;  // Weight adjustment

    // Glyph
    float glyphDist = pxRange * (sd - 0.5);
    float glyphAlpha = clamp(glyphDist + 0.5, 0.0, 1.0);

    // Outline
    float outlineDist = pxRange * (sd - (0.5 - outlineWidth));
    float outlineAlpha = clamp(outlineDist + 0.5, 0.0, 1.0) - glyphAlpha;

    // Shadow (offset sample)
    vec2 shadowUV = v_texcoord0 + shadowOffset / vec2(textureSize);
    vec3 shadowMsd = texture2D(tex_sdf, shadowUV).rgb;
    float shadowSd = median(shadowMsd.r, shadowMsd.g, shadowMsd.b);
    float shadowAlpha = clamp(pxRange * (shadowSd - 0.5) + 0.5, 0.0, 1.0);
    shadowAlpha *= shadowSoftness;

    // Glow
    float glowDist = pxRange * (sd - (0.5 - glowRadius));
    float glowAlpha = clamp(glowDist + 0.5, 0.0, 1.0);
    glowAlpha = pow(glowAlpha, 2.0) * glowIntensity;

    // Composite layers (back to front: shadow → glow → outline → glyph)
    vec3 color = vec3(shadowColor);
    float alpha = shadowAlpha;

    color = mix(color, glowColor, glowAlpha);
    alpha = max(alpha, glowAlpha);

    color = mix(color, outlineColor, outlineAlpha);
    alpha = max(alpha, outlineAlpha);

    color = mix(color, v_color0.rgb, glyphAlpha);
    alpha = max(alpha, glyphAlpha);

    gl_FragColor = vec4(color, alpha * v_color0.a);
}
```

**Performance:** +21 ALU ops + 1 texture sample (~0.25ms at 720p)

**Acceptable:** <1ms even on integrated GPUs

---

## Part 3: Animation Effects (New Capabilities)

### 3.1 Pulsing/Breathing Effect

**Description:** Character edges pulse in/out

**Shader Implementation:**
```glsl
uniform uint uFrameCounter;
uniform vec4 uPulseParams;
#define pulseSpeed uPulseParams.x     // 0.01 to 0.1
#define pulseAmount uPulseParams.y    // 0.0 to 0.2

void main() {
    // Compute pulse offset (sine wave)
    float phase = float(uFrameCounter) * pulseSpeed;
    float pulse = sin(phase) * pulseAmount;

    // Apply to distance threshold
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b) + pulse;
    float screenPxDist = pxRange * (sd - 0.5);
    float opacity = clamp(screenPxDist + 0.5, 0.0, 1.0);

    gl_FragColor = vec4(v_color0.rgb, v_color0.a * opacity);
}
```

**Use Cases:**
- Important dialogue choices
- Item pickup notifications
- Critical warnings ("Are you sure?")

---

### 3.2 Reveal/Wipe Animation

**Description:** Character gradually draws on screen

**Shader Implementation:**
```glsl
uniform vec4 uRevealParams;
#define revealProgress uRevealParams.x  // 0.0 to 1.0
#define revealDirection uRevealParams.y // 0=L→R, 1=R→L, 2=T→B, 3=B→T

void main() {
    // Calculate reveal threshold based on position
    float threshold;
    if (revealDirection < 0.5) {  // Left to right
        threshold = v_texcoord0.x;
    } else if (revealDirection < 1.5) {  // Right to left
        threshold = 1.0 - v_texcoord0.x;
    } else if (revealDirection < 2.5) {  // Top to bottom
        threshold = v_texcoord0.y;
    } else {  // Bottom to top
        threshold = 1.0 - v_texcoord0.y;
    }

    // Compare to reveal progress
    if (threshold > revealProgress) discard;

    // Normal SDF rendering
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);
    float opacity = clamp(pxRange * (sd - 0.5) + 0.5, 0.0, 1.0);

    gl_FragColor = vec4(v_color0.rgb, v_color0.a * opacity);
}
```

**Use Cases:**
- Dramatic NPC introductions
- Title card animations
- Tutorial text reveals

---

### 3.3 Color Gradient Animation

**Description:** Gradient sweeps across text

**Shader Implementation:**
```glsl
uniform uint uFrameCounter;
uniform vec4 uGradientParams;
#define gradientSpeed uGradientParams.x
uniform vec4 uGradientColorA;
uniform vec4 uGradientColorB;

void main() {
    // Compute gradient offset (moving phase)
    float phase = float(uFrameCounter) * gradientSpeed;
    float gradientPos = fract(v_texcoord0.x + phase);

    // Interpolate between colors
    vec3 gradientColor = mix(uGradientColorA.rgb,
                             uGradientColorB.rgb,
                             gradientPos);

    // Normal SDF rendering with gradient color
    vec3 msd = texture2D(tex_sdf, v_texcoord0).rgb;
    float sd = median(msd.r, msd.g, msd.b);
    float opacity = clamp(pxRange * (sd - 0.5) + 0.5, 0.0, 1.0);

    gl_FragColor = vec4(gradientColor, v_color0.a * opacity);
}
```

**Use Cases:**
- Magical spells being cast
- Status effect descriptions
- Materia names

---

## Part 4: FF7 Field Dialogue Integration

### 4.1 Current Field Dialogue System

**Location:** Field module (field dialogue boxes)

**Current Behavior:**
1. Text box opens
2. Characters appear one-by-one (typewriter effect)
3. Control codes trigger colors/effects
4. Text scrolls with ▼ indicator
5. Player presses button to continue

**Rendering:**
- Text boxes: 320×64 pixels
- Characters: 16×16 pixels (2 lines of ~20 chars each)
- Background: Semi-transparent black gradient

### 4.2 SDF Effects for Field Dialogue

**Recommended Effect Presets:**

**Preset 1: Standard Dialogue (Default)**
- No outline
- Subtle drop shadow (offset: 0.01, color: black, softness: 0.8)
- Normal weight

**Preset 2: Important NPC (Aerith, Sephiroth, Cloud)**
- Thin outline (width: 0.05, color: character theme color)
- Glow effect (radius: 0.1, intensity: 1.5, color: theme color)
- Normal weight

**Preset 3: Shouting/Emphasis**
- Medium outline (width: 0.08, color: white)
- Bold weight (+0.1)
- No shadow

**Preset 4: Whisper/Thought**
- No outline
- Thin weight (-0.08)
- Glow (radius: 0.15, intensity: 0.8, color: light blue)

**Preset 5: Magic/Mystical**
- Thin outline (width: 0.05, color: cyan)
- Strong glow (radius: 0.2, intensity: 2.0, color: magenta)
- Pulsing animation (speed: 0.05, amount: 0.1)

### 4.3 Configuration System

**FFNx.toml:**
```toml
###############################################################################
# SDF Text Effects
###############################################################################

[sdf_effects]

# Enable SDF effects system
enable_effects = true

# Default preset for all dialogue
default_preset = "standard"

# Character-specific presets (by NPC name)
[sdf_effects.character_presets]
"Cloud" = "important"
"Aerith" = "magic"
"Sephiroth" = "important"
"Barret" = "shouting"

# Custom effect definitions
[sdf_effects.presets.standard]
outline_width = 0.0
shadow_offset = [0.01, 0.01]
shadow_color = 0.0
shadow_softness = 0.8

[sdf_effects.presets.important]
outline_width = 0.05
outline_color = [1.0, 1.0, 0.0]  # Yellow
glow_radius = 0.1
glow_intensity = 1.5
```

**Dynamic Control Codes (New):**
```
FE E0 XX = Apply effect preset XX (0-15)
FE E1 XX = Set outline width (0-255 → 0.0-1.0)
FE E2 XX YY ZZ = Set outline color RGB
FE E3 XX = Set glow intensity (0-255 → 0.0-2.0)
FE E4 XX = Set weight bias (-128 to +127 → -0.5 to +0.5)
```

### 4.4 Implementation in japanese_text.cpp

```cpp
// Add effect state tracking

struct SDFEffectState {
    bool outline_enabled;
    float outline_width;
    float outline_color[3];

    bool shadow_enabled;
    float shadow_offset[2];
    float shadow_color;
    float shadow_softness;

    bool glow_enabled;
    float glow_radius;
    float glow_intensity;
    float glow_color[3];

    float weight_bias;

    bool pulse_enabled;
    float pulse_speed;
    float pulse_amount;
};

// Global state
static SDFEffectState current_effects = { /* defaults */ };

// Update shader uniforms before rendering
void update_sdf_effect_uniforms() {
    if (current_effects.outline_enabled) {
        float params[4] = {
            current_effects.outline_width,
            current_effects.outline_color[0],
            current_effects.outline_color[1],
            current_effects.outline_color[2]
        };
        newRenderer.setUniform("uOutlineParams", params, 4);
    }

    // ... similar for shadow, glow, weight, pulse
}

// Parse new control codes
if (*buffer_text == 0xFE) {
    buffer_text++;
    switch (*buffer_text) {
        case 0xE0:  // Apply preset
            apply_effect_preset(*++buffer_text);
            break;
        case 0xE1:  // Outline width
            current_effects.outline_width = (*++buffer_text) / 255.0f;
            current_effects.outline_enabled = true;
            break;
        // ... etc
    }
}
```

---

## Part 5: Performance Budget

### 5.1 Target Performance

**Platform:** PC (min spec: Intel HD 4000, 2013+)

| Effect Combination | ALU Ops | Texture Samples | Est. Time (720p) |
|--------------------|---------|-----------------|------------------|
| Base SDF | 5 | 1 | 0.05ms |
| + Outline | +5 | 0 | +0.05ms |
| + Shadow | +8 | +1 | +0.1ms |
| + Glow | +6 | 0 | +0.08ms |
| + Weight | +2 | 0 | +0.02ms |
| **All Combined** | **26** | **2** | **~0.3ms** |

**Frametime Budget:** 16.67ms per frame (60fps)
**Text Rendering:** ~0.3ms = 1.8% of budget
**Acceptable:** <5% (0.83ms)

**Conclusion:** ✅ All effects combinable with room to spare

### 5.2 Optimization Strategies

**1. Uniform Packing**
- Group related params into vec4 uniforms
- Reduces uniform upload overhead

**2. Conditional Compilation**
- Shader variants for different effect combos
- Avoid branching in fragment shader

**3. LOD System**
- Disable expensive effects for distant text
- Full effects <10m, simple SDF >10m

**4. Texture Caching**
- Pre-calculate shadow/glow in alpha channel
- Trade memory for shader complexity

---

## Part 6: Development Roadmap (Effects)

### Week 1-2: Core SDF + Existing Effects
- Implement base SDF shader
- Preserve rainbow/blink/color system
- Test with existing dialogue

### Week 3-4: Outline + Shadow
- Add outline shader variant
- Add shadow shader variant
- Test combinations

### Week 5-6: Glow + Weight
- Add glow shader variant
- Add weight adjustment
- Performance profiling

### Week 7-8: Animation Effects
- Pulsing shader
- Reveal/wipe shader
- Gradient sweep shader

### Week 9-10: Integration
- Control code parsing
- Preset system
- Configuration

### Week 11-12: Testing + Polish
- All dialogue contexts
- Performance optimization
- Visual quality validation

---

## Part 7: Sources & References

### SDF Techniques:
- [Shaderfun: SDF Simple Effects](https://shaderfun.com/2018/07/01/signed-distance-fields-part-7-some-simple-effects/)
- [Andreas Terrius: Mesh Distance Field + Shadow Guide](https://andreasterrius.github.io/posts/sdf-shadow-guide/)
- [Cocos Forums: SDF Shader Effects](https://forum.cocosengine.org/t/cocos-creator-implements-various-shader-effects-based-on-sdf/56106)
- [LÖVE Community: Glow Outlines](https://blogs.love2d.org/content/let-it-glow-dynamically-adding-outlines-characters)
- [Inspirnathan: Glow Shader in Shadertoy](https://inspirnathan.com/posts/65-glow-shader-in-shadertoy/)
- [LearnOpenGL: Bloom](https://learnopengl.com/Advanced-Lighting/Bloom)

---

**End of Specification**

**Status:** Ready for Implementation
**Next Steps:** Begin Phase 1 (Core SDF + Effect Preservation)

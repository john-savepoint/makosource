# SDF Font Laboratory - Complete Guide

**Created:** 2026-01-25 01:02:00 JST (Saturday)
**Session ID:** 22abbba1-da82-4680-af9f-04982a5b7f30
**Version:** 2.0.0 - Enhanced Edition

## Overview

The SDF Font Laboratory is a comprehensive real-time text styling system for Final Fantasy VII that provides full creative control over font appearance, effects, and animations.

## What's New in v2.0

### ✨ Major Features Added

1. **Full Color Control**
   - Custom text colors with 9 preset colors
   - Colored shadows (not just black!)
   - Colored outlines and glows
   - Rainbow color cycling animation

2. **Advanced Shadow Effects**
   - Separate X/Y offset controls
   - Shadow blur/softness parameter
   - Shadow color customization

3. **Multiple Outline/Border System**
   - Outer outline with color and thickness
   - Inner outline (border-within-border)
   - Mix and match for complex effects

4. **Glow/Halo Effects**
   - Adjustable glow radius and intensity
   - Custom glow colors
   - Perfect for fantasy/magical text

5. **Animation System**
   - Rainbow color cycling
   - Pulse/breathing effect
   - Adjustable animation speed

6. **Organized Tab Interface**
   - Basic, Shadow, Outline, Color, Glow, Animation tabs
   - Presets tab with 7 ready-made styles
   - Export tab for saving configurations

## How to Access

1. **Launch FF7**
2. **Press F12** to open DevTools overlay
3. **Click Tools → SDF Font Laboratory**

## Tab-by-Tab Guide

### 🎯 Basic Tab

Core text rendering parameters:

- **Pixel Range** (0.5-10.0)
  - Distance field spread
  - Higher = smoother but blurrier
  - Recommended: 3.0-5.0

- **Thickness** (0.1-2.0)
  - Glyph boldness
  - 0.5 = normal weight
  - Recommended: 0.4-0.7

### 🌑 Shadow Tab

Shadow effects and positioning:

- **Shadow X Offset** (-10.0 to +10.0 px)
  - Horizontal displacement
  - Negative = left, Positive = right

- **Shadow Y Offset** (-10.0 to +10.0 px)
  - Vertical displacement
  - Negative = up, Positive = down

- **Shadow Blur** (0.0-5.0)
  - Shadow softness
  - 0 = hard edge, higher = softer

- **Shadow Opacity** (0.0-1.0)
  - 0 = invisible, 1 = fully opaque

- **Shadow Color**
  - RGB color picker
  - Try dark blue for stylized shadows!

### 🖼️ Outline Tab

Border and outline effects:

**Outer Outline:**
- **Width** (0.0-5.0 px)
- **Opacity** (0.0-1.0)
- **Color** (RGB picker)
- Perfect for high contrast/readability

**Inner Outline:**
- **Width** (0.0-5.0 px)
- **Opacity** (0.0-1.0)
- **Color** (RGB picker)
- Creates border-within-border effect
- Great for retro arcade style

### 🎨 Color Tab

Text color customization:

- **Override Text Color** checkbox
  - When off: uses game's original colors
  - When on: uses custom color

- **Quick Color Presets:**
  - White, Red, Green, Blue
  - Yellow, Purple, Orange
  - Pink, Cyan
  - One-click application!

### ✨ Glow Tab

Halo/glow effects:

- **Glow Radius** (0.0-5.0)
  - Glow spread distance
  - 0 = no glow

- **Glow Intensity** (0.0-2.0)
  - Brightness
  - Higher = stronger glow

- **Glow Color** (RGB picker)
  - Try yellow/gold for divine text
  - Try cyan/blue for magical text

**Suggested Settings:**
- Radius: 2.0, Intensity: 1.0, Color: Yellow

### 🌈 Animation Tab

Dynamic effects:

- **Rainbow Color Cycle**
  - Animates through full color spectrum
  - Cycle Speed: 0.1-5.0 (1.0 = normal)
  - ⚠️ May be distracting in gameplay

- **Pulse Effect**
  - Text breathes in and out
  - Subtle opacity animation
  - Combines with other effects

**Warning:** Animations are eye-catching but may interfere with gameplay immersion!

### 🎭 Presets Tab

Ready-made styles:

1. **Classic (Default)**
   - Clean, readable text
   - Subtle black shadow
   - Perfect for normal gameplay

2. **Bold with Black Outline**
   - Strong contrast
   - Thick text + black border
   - Maximum readability

3. **Soft Glow (Fantasy Style)**
   - Ethereal blue glow
   - Magical appearance
   - Great for spells/special text

4. **Double Outline (Retro)**
   - Black outer border
   - Gold inner border
   - Classic arcade aesthetic

5. **RAINBOW RAVE!**
   - Full rainbow cycling
   - Bright glow
   - Pulse animation
   - Maximum chaos (not recommended for serious play!)

**Extreme Presets:**

6. **Ultra Thicc**
   - Extremely bold text
   - Massive outline
   - For comedic effect

7. **Ghost Mode**
   - Translucent gray text
   - Green ethereal glow
   - Spooky appearance

### 💾 Export Tab

Save your configuration:

- **Show Config Values** button
  - Displays all parameters formatted for FFNx.toml
  - Copy and paste into config file
  - Restart game to make permanent

## Complete Parameter Reference

### Basic Parameters
```toml
sdf_pixel_range = 4.0
sdf_thickness = 0.5
```

### Shadow Parameters
```toml
sdf_shadow_offset_x = 1.0
sdf_shadow_offset_y = 1.0
sdf_shadow_blur = 0.0
sdf_shadow_opacity = 0.5
sdf_shadow_color_r = 0.0
sdf_shadow_color_g = 0.0
sdf_shadow_color_b = 0.0
```

### Outline Parameters
```toml
sdf_outline_width = 0.0
sdf_outline_opacity = 1.0
sdf_outline_color_r = 1.0
sdf_outline_color_g = 1.0
sdf_outline_color_b = 1.0
sdf_inner_outline_width = 0.0
sdf_inner_outline_opacity = 1.0
sdf_inner_outline_color_r = 0.5
sdf_inner_outline_color_g = 0.5
sdf_inner_outline_color_b = 0.5
```

### Glow Parameters
```toml
sdf_glow_radius = 0.0
sdf_glow_intensity = 0.0
sdf_glow_color_r = 1.0
sdf_glow_color_g = 1.0
sdf_glow_color_b = 0.0
```

### Text Color Parameters
```toml
sdf_text_color_enable = false
sdf_text_color_r = 1.0
sdf_text_color_g = 1.0
sdf_text_color_b = 1.0
```

### Animation Parameters
```toml
sdf_anim_speed = 1.0
sdf_color_cycle_enable = false
sdf_pulse_enable = false
```

## Creative Ideas & Tips

### For Maximum Readability
```
Thickness: 0.6
Outline Width: 1.0
Outline Color: Black (0, 0, 0)
Shadow Offset X/Y: 1.5
Shadow Opacity: 0.7
```

### For Magical/Fantasy Feel
```
Glow Radius: 2.5
Glow Intensity: 1.2
Glow Color: Cyan (0.5, 0.8, 1.0)
Shadow Opacity: 0.3
```

### For Retro/Arcade Style
```
Thickness: 0.6
Outline Width: 1.2
Outline Color: Black
Inner Outline Width: 0.5
Inner Outline Color: Yellow/Gold
```

### For Horror/Spooky
```
Text Color: Dark gray (0.3, 0.3, 0.3)
Glow Radius: 3.0
Glow Intensity: 1.5
Glow Color: Green (0.2, 0.8, 0.2)
Shadow: Disabled
```

### For Party Mode (Not Serious)
```
Rainbow Color Cycle: ON
Cycle Speed: 2.0
Glow Radius: 3.0
Glow Intensity: 1.5
Glow Color: White
Pulse: ON
```

## Advanced Techniques

### Layer Stacking Order
Effects render in this order (back to front):
1. Shadow (furthest back)
2. Glow
3. Outer Outline
4. Inner Outline
5. Text (on top)

Understanding this helps create complex multi-layer effects.

### Color Harmony Tips
- **Complementary colors** for outline (e.g., blue text + orange outline)
- **Analogous colors** for glow (e.g., yellow text + orange glow)
- **Monochromatic** for subtle effects (different shades of same color)

### Performance Considerations
- Higher blur values = slightly more GPU work
- Animations = constant GPU updates
- Multiple effects combined = more rendering work
- If experiencing lag, reduce:
  - Shadow blur
  - Glow radius
  - Disable animations

## Troubleshooting

### Changes not visible
- ✅ Ensure "Enable SDF Fonts" checkbox is ON
- ✅ Verify SDF textures are installed
- ✅ Try more dramatic parameter changes to confirm it's working

### Text looks blurry
- ⬇️ Reduce pixel_range value
- ⬇️ Reduce glow radius/intensity

### Text too thin/thick
- Adjust thickness parameter
- Try values between 0.3-0.8 for best results

### Outline not showing
- ⬆️ Increase outline width to at least 0.5
- ✅ Ensure outline opacity is > 0.0
- ✅ Check outline color isn't same as text color

### Glow not visible
- ⬆️ Increase glow intensity
- ⬆️ Increase glow radius
- ✅ Try a brighter glow color

## Technical Details

### Shader Implementation
The enhanced SDF shader uses:
- **10 Vec4 uniforms** for all parameters
- **Median-of-3** algorithm for sharp corners
- **HSV color space** for rainbow cycling
- **Layer compositing** for proper transparency
- **Optimized discard** for fully transparent pixels

### Real-time Updates
All parameters update immediately on next frame render. No shader recompilation required.

### Animation Timing
Animations use frame-independent timing at ~60fps for smooth, consistent effects regardless of game performance.

## Credits

**Enhanced SDF System v2.0**
- Shader Development: Claude Code + John Zealand-Doyle
- Original SDF Implementation: FFNx PR#737
- ImGui Debug Interface: Claude Code
- Session: 22abbba1-da82-4680-af9f-04982a5b7f30

---

**Have fun creating amazing text styles! 🎨✨**

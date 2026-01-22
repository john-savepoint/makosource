# FF7 Font Scaling Investigation - Complete Analysis

**Created:** 2026-01-22 22:15:00 JST (Thursday)
**Session-ID:** fab70bfc-433a-4d8f-b83b-6690362519f5

## Executive Summary

The "global font scale" at address `0x7B7CF8` is NOT a simple UI byte - it's a **32-bit floating point value** that multiplies character width data during text rendering and layout calculations. Changing it breaks the font system because:

1. **Font scale affects character advance width** - how far the cursor moves after each character
2. **Font scale affects text layout calculations** - word wrapping, centering, box sizing
3. **The scale must match the font texture resolution** - changing scale without changing textures causes misalignment

## Critical Addresses

| Address (File) | Address (Runtime) | Type | Purpose | Original Value | HEXT Patch |
|----------------|-------------------|------|---------|----------------|------------|
| 0x7B7CF8 | 0xBB7CF8 | float32 | Menu font scale multiplier | 1.667 (0x3FD55555) | 2.0 (0x40000000) |
| 0x99DDA8-0x99DEA7 | 0xD9DDA8-0xD9DEA7 | byte[256] | Font spacing/width table | (varies) | Modified per-character |
| 0xDB958C | 0x1DB958C | ptr | Font data pointer | (runtime) | Loaded from font file |

## How Font Scaling Works

### Code Analysis from IDA Pro

**Function `sub_6F54A2` - Text Width Calculation:**
```c
int calculate_text_width(unsigned char *text) {
    int width = 0;
    while (*text != 0xFF) {
        unsigned char char_data = font_data[*text];

        if (high_res_mode) {
            // Extract left padding (bits 5-7) and advance width (bits 0-4)
            int left_pad = (char_data >> 5) * flt_7B7CF8;
            int advance = (char_data & 0x1F) * flt_7B7CF8;
            width += left_pad + advance;
        } else {
            // Low-res mode: multiply by 2 instead of scale factor
            width += 2 * (char_data >> 5) + 2 * (char_data & 0x1F);
        }
        text++;
    }
    return width;
}
```

**Function `sub_6F564E` - Character Rendering:**
```c
int render_character(int x, int y, int z, unsigned char ch, int depth) {
    unsigned char char_data = font_data[ch];

    // Character width in pixels (affected by scale)
    int char_width = 24; // or 16 for special chars

    if (high_res_mode) {
        int left_pad = (char_data >> 5) * flt_7B7CF8;
        int advance = (char_data & 0x1F) * flt_7B7CF8;

        // Render character quad at position (x + left_pad, y)
        // Advance cursor by: left_pad + advance
        return x + left_pad + advance;
    } else {
        // Low-res: fixed spacing
        return x + 2 * (char_data >> 5) + 2 * (char_data & 0x1F);
    }
}
```

### Font Data Structure

Each character has 8-bit width data stored as:
```
Bits 7-5: Left padding (0-7 range)
Bits 4-0: Advance width (0-31 range)
```

The scale factor (`flt_7B7CF8`) converts these small integers to pixel coordinates:
- Original: `1.667` → Left pad of 3 becomes `3 * 1.667 = 5.0 pixels`
- Patched: `2.0` → Left pad of 3 becomes `3 * 2.0 = 6.0 pixels`

## Font Files Referenced

### From IDA Pro String Search

**Menu Font Textures (usfont = "User Interface String Font"):**
- `usfont_a_h.tim` - Enhanced UI, High-res variant A
- `usfont_a_l.tim` - Enhanced UI, Low-res variant A
- `usfont_b_h.tim` - Enhanced UI, High-res variant B
- `usfont_b_l.tim` - Enhanced UI, Low-res variant B
- `usfont_h.tim` - Standard UI, High-res
- `usfont_l.tim` - Standard UI, Low-res

**Character Font:**
- `cfont.tim` - Character names/dialogue font

**World Map Font:**
- `font.tim` - Standard font
- `font_ua.tim` - User font variant A
- `font_ub.tim` - User font variant B
- `font_s.tim` - Small font

### Texture Variant Control

From previous session's investigation (0x919DA5):
- Registry path: `HKCU\Software\Square Soft, Inc.\Final Fantasy VII`
- Registry value: "Mode" (DWORD)
- Mode 2 = Advanced graphics → loads `_a` and `_b` variants
- Other modes = Standard → loads base textures

## Font Spacing Data Table

**Address:** 0x99DDA8 (file) / 0xD9DDA8 (runtime)
**Size:** 256 bytes (one per ASCII character)
**Format:** Each byte encodes character width

From HEXT file `00-Spacing.txt`:
```
99DDA8 = 03 02 03 05 05 06 06 02 03 03 04 06 04 03 02 04
         ^^ ^^
         !  "    (exclamation = 3, quote = 2, etc.)
```

This is the CHARACTER WIDTH TABLE that stores per-character advance widths.

### Why Spacing Data Gets Modified at Runtime

The HEXT also includes code injection at `0x7217C5` that patches the new game screen:
```
7217C5 = E9 36 28 1F 00 90 90 90 90  ; Jump to 0x914000
914000 = ... (code to refresh spacing table)
```

This is needed because "7h processes hext" (7th Heaven mod loader) may overwrite the spacing table.

## Why Changing Font Scale Breaks Everything

### Problem 1: Text Overflow

If you increase the scale (e.g., 1.667 → 2.5):
- Each character becomes wider
- Text no longer fits in UI boxes
- Menu items overflow their boundaries
- Dialog boxes cut off text

### Problem 2: Misaligned Characters

The font TEXTURES have fixed character positions:
- Character 'A' is at texture coordinates (0, 0) with 24×24 pixel size
- If scale doesn't match texture resolution, characters render incorrectly
- Too small: gaps between characters
- Too large: characters overlap

### Problem 3: Word Wrapping Breaks

Text width calculations (`sub_6F54A2`) use the scale:
```c
if (text_width > box_width) {
    wrap_to_next_line();
}
```

Wrong scale → wrong width calculation → wrapping at wrong places

### Problem 4: Centering/Alignment Fails

UI centers text by calculating:
```c
int x_offset = (box_width - text_width) / 2;
```

Wrong scale → wrong text_width → off-center text

## What Changes Would Actually Work

### Safe Changes (Won't Break)

1. **Proportional scaling of BOTH:**
   - Multiply `flt_7B7CF8` by N
   - Multiply all spacing table values by N
   - Use font textures with N× resolution

2. **Changing individual character widths:**
   - Modify spacing table (0x99DDA8) values
   - Keep scale unchanged
   - Requires matching font texture widths

### Example: Making Font 20% Larger

To make font 20% larger (1.2× scale):

1. Change `flt_7B7CF8` from 1.667 to 2.0 (already done by Enhanced Stock UI)
2. Update spacing table values proportionally
3. Use higher-resolution font textures (usfont_a_h.tim instead of usfont_h.tim)

The Enhanced Stock UI mod does exactly this - that's why it works!

## Font Loading Code Path

From cross-reference analysis:

**Initialization Functions:**
- `sub_401018` - References both font data pointer (0xDB958C) and spacing table (0x99DDA8)
- `sub_401372` - Also references spacing table

**Rendering Functions (verified from decompilation):**
- `sub_6F54A2` - Text width calculation (sub_6F54A2:408)
- `sub_6F564E` - Character quad rendering (sub_6F564E:1177)
- `sub_6D1CC0` - Large function with 50+ references to font data (likely main text renderer)
- `sub_6E706D` - Also uses font data
- `sub_6ED30B` - Also uses font data

**Font Data Flow:**
1. Game loads font texture (.tim file) into video memory
2. Game loads font spacing data from file into 0xD9DDA8
3. Font data pointer (0x1DB958C) points to loaded font metrics
4. Rendering code reads spacing × scale to calculate positions
5. Characters drawn using texture coordinates + calculated positions

## HEXT Mod Strategy (Enhanced Stock UI)

The mod coordinates THREE changes:
1. **Font scale:** 1.667 → 2.0
2. **Spacing data:** Updated to match 2.0× scale
3. **Texture selection:** Use `_a` variants (higher resolution)

This is why the mod works - all three components are synchronized.

## Conclusion: Why Arbitrary Changes Fail

**You asked: "Why does changing the font scale break everything?"**

Because `flt_7B7CF8` is NOT an independent setting - it's part of a coordinated system:

- **Font textures** (TIM files) define character pixel sizes
- **Spacing table** (0x99DDA8) defines character advance widths
- **Scale factor** (0x7B7CF8) converts spacing to pixels
- **Rendering code** uses: `spacing × scale = pixel_advance`

Changing ONLY the scale breaks the equation:
- `spacing × wrong_scale ≠ texture_width`

Result: Characters render at wrong positions, text overflows boxes, word wrapping breaks.

**To safely change font scale:**
1. Pick target scale (e.g., 2.0)
2. Create/use font textures matching that scale
3. Update spacing table values to match
4. Update scale factor
5. Test all UI screens for overflow

The Enhanced Stock UI mod already did this work. Arbitrarily changing the scale value will undo their coordination.

## References

### Source Files
- HEXT: `/mnt/d/Games/Stand-alone/FF7Modding/2b49d831-6556-41df-9ddb-d1a6e937f548__Tsunamods__Enhanced_Stock_UI_2.958/EnhancedStock/hext/00-Main.txt`
- HEXT Spacing: `/mnt/d/Games/Stand-alone/FF7Modding/2b49d831-6556-41df-9ddb-d1a6e937f548__Tsunamods__Enhanced_Stock_UI_2.958/EnhancedStock/hext/00-Spacing.txt`
- Database: `ff7_ui_analysis/ff7_ui_memory_map.json`

### IDA Pro Functions
- Text width calculation: `sub_6F54A2` (0x6F54A2, 408 bytes)
- Character rendering: `sub_6F564E` (0x6F564E, 1177 bytes)
- Font initialization: `sub_401018` (0x401018, 528 bytes)

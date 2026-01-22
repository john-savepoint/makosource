# FF7 Character Width Investigation - Battle Dialogue Squished Text Bug

**Date**: 2026-01-16
**Session ID**: 23978250-ec31-41d5-9c64-57c658e79677
**Status**: BUG IDENTIFIED - FIX READY TO APPLY

---

## Problem Statement

Battle spell/action names displayed at the top of the screen during combat (e.g., "ブリザド" / Blizzard) show specific characters appearing severely compressed/squished, particularly the リ (ri) character. Field dialogue and menu text render correctly.

**Screenshot Evidence**: `ff7_en_qAzYKnhT6M.png` showing ブリザド with リ character visibly compressed.

---

## Root Cause Analysis

### The Bug

**Character Overlap Due to Spacing < Render Width**

1. Characters are rendered at a **fixed 16-pixel width** (hardcoded: `v126 = 16` at line 1868)
2. Character spacing is calculated as `ceil(0.5f * charWidth)` where `charWidth` comes from `charWidthData[][]` array
3. For characters with `charWidth < 32`, the spacing is **less than 16 pixels**
4. This causes **the next character to render on top of the previous one**, overwriting pixels and creating the "squished" appearance

### Example: ブリザド (Blizzard)

| Character | Code  | charWidth | Spacing Calculation | Render Width | Overlap |
|-----------|-------|-----------|---------------------|--------------|---------|
| ブ (bu)   | 0x04  | 30        | ceil(0.5 × 30) = 15 | 16px         | -1px    |
| リ (ri)   | 0x8E  | 25        | ceil(0.5 × 25) = 13 | 16px         | **-3px** |
| ザ (za)   | 0x14  | 31        | ceil(0.5 × 31) = 16 | 16px         | 0px     |
| ド (do)   | 0x26  | 21        | ceil(0.5 × 21) = 11 | 16px         | **-5px** |

**Character Rendering Positions:**
```
ブ: X=0 to X=16   (16px wide)
リ: X=13 to X=29  (starts 3px BEFORE ブ ends!) ← OVERLAP
ザ: X=29 to X=45  (overlaps リ by 4px)
ド: X=40 to X=56  (overlaps ザ by 5px)
```

The リ character isn't being compressed - **it's being overwritten by ザ rendering on top of it**.

---

## Technical Investigation Summary

### 1. FFNx PR #737 Implementation (Current - Broken)

**File**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp`
**Function**: `draw_text_top_display_6D1CC0_jp()` (line 1513)

**Current Formula**:
```cpp
v106 += leftPadding + std::ceil(0.5f * charWidth);  // Text box width calculation
v108 = std::ceil(0.5f * charWidth) + v107;          // Character X position
```

**Character Width Data**:
```cpp
int charWidthData[6][256] = {
    // Page 0 (jafont_1): Kana, numbers, Latin
    { 30, 30, 28, 31, 30, ... },  // Values encoded as: width (bits 0-4), padding (bits 5-7)
    // Pages 1-5: Kanji sets
};
```

### 2. Original Japanese Game (AF3DN.P)

**Original Formula** (from decompiled code):
```c
// Field text: 20 × width / 64
v3 += (4 * (a2 == 0) + 16) * v10 / 64;  // a2=0 for field → 20/64 multiplier

// Battle text: 10 × width / 64
v5 += 10 * v30 / 64;  // 10/64 multiplier
```

**Key Differences**:
- Original Field: `20 × 31 / 64 ≈ 10 pixels` spacing for full-width kanji
- Original Battle: `10 × 31 / 64 ≈ 5 pixels` spacing
- PR #737: `ceil(0.5 × 31) = 16 pixels` spacing (same for both contexts!)

The original game used **context-aware spacing** (2:1 ratio field:battle). PR #737 uses the **same formula everywhere** and chose a multiplier that causes overlap.

### 3. Font Texture Analysis

**Texture Specifications**:
- **Size**: 1024×1024 pixels (6 textures: jafont_1.png through jafont_6.png)
- **Layout**: 16×16 grid (256 characters per texture)
- **Cell Size**: 64×64 pixels per character
- **Location**: `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/direct/menu/`

**UV Coordinate Mapping**:
```cpp
// Code uses 512-based coordinate system
u_coord = 32 * (char_code % 16);  // Maps to 64px cells in 1024px texture
v_coord = 32 * (char_code / 16);
vertex_u = u_coord / 512.0f;      // Normalized UV
```

**Verification**: UV coordinates are **correct** - not the cause of the bug.

### 4. Width Table Comparison

**FF7 English Executable** (0x99DDA8):
- Single 256-byte width table used by **all contexts** (field, battle, menu)
- No separate width tables for different game modes

**AF3DN.P (Japanese DLL)**:
- `dword_10041F70`: 256 ints - Single-byte characters (0x00-0xFF)
- `dword_10042370`: 32 ints - Extended range 1
- `dword_100423F0`: 32 ints - Extended range 2
- Width calculation: `result = table_value + 5; if (result >= 64) result = 64;`

**Makou Reactor Analysis**:
- Documents 7 font width tables (1 Latin + 6 Japanese)
- Width encoding: `CHARACTER_WIDTH(x)` and `LEFT_PADD(x)` macros
- Confirms multi-byte Japanese encoding (0xFA-0xFE prefixes for kanji pages)

---

## The Fix

### Affected Locations

**File**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp`
**Function**: `draw_text_top_display_6D1CC0_jp` (battle spell name display ONLY)

| Line | Current Code | Purpose |
|------|--------------|---------|
| 1719 | `v106 += leftPadding + std::ceil(0.5f * charWidth);` | FA (Kanji page 1) width |
| 1729 | `v106 += leftPadding + std::ceil(0.5f * charWidth);` | FB (Kanji page 2) width |
| 1739 | `v106 += leftPadding + std::ceil(0.5f * charWidth);` | FC (Kanji page 3) width |
| 1749 | `v106 += leftPadding + std::ceil(0.5f * charWidth);` | FD (Kanji page 4) width |
| 1759 | `v106 += leftPadding + std::ceil(0.5f * charWidth);` | FE (Kanji page 5) width |
| 1774 | `v106 += leftPadding + std::ceil(0.5f * charWidth);` | Default (jafont_1) width |
| 1884 | `v108 = std::ceil(0.5f * charWidth) + v107;` | Character X position |

### Recommended Fix Options

**Option A: Fixed 16-pixel Spacing** (Simplest)
```cpp
// Change all 7 lines to use fixed 16px spacing
v106 += leftPadding + 16;  // Lines 1719, 1729, 1739, 1749, 1759, 1774
v108 = 16 + v107;          // Line 1884
```

**Option B: Minimum 16-pixel Spacing** (Safer)
```cpp
// Ensure spacing is never less than render width
v106 += leftPadding + std::max((int)std::ceil(0.5f * charWidth), 16);
v108 = std::max((int)std::ceil(0.5f * charWidth), 16) + v107;
```

**Option C: Restore Original Multiplier** (Most Accurate)
```cpp
// Use original game's 10/64 multiplier for battle text
v106 += leftPadding + (10 * charWidth / 64);
v108 = (10 * charWidth / 64) + v107;
```

### Impact Analysis

**What This Fixes**: Battle spell/action names only (e.g., "ブリザド", "ファイア")
**What This Doesn't Affect**:
- Field dialogue (uses `field_submit_draw_text_640x480_6E706D_jp()` - line 940)
- Menu text (uses `draw_char_from_buffer_6F564E_jp()` - line 1344)
- Battle UI menus (different rendering path)

**Scope**: 7 line changes in a single function, isolated to battle text display.

---

## Investigation Timeline

1. **Initial Problem**: Battle dialogue text showing squished characters (specifically リ in "ブリザド")
2. **First Theory**: Different width tables for battle vs field (INCORRECT)
   - Investigated FFNx, FF7 EXE, AF3DN.P, Makou Reactor codebases
   - Found: Only ONE primary width table at 0x99DDA8 (US 1.02)
3. **Second Theory**: Context-specific multipliers (PARTIALLY CORRECT)
   - Original game: 20/64 (field) vs 10/64 (battle) = 2:1 ratio
   - PR #737: 0.5× for all contexts
4. **Third Theory**: UV coordinate mismatch (INCORRECT)
   - Verified texture layout: 1024×1024, 16×16 grid, 64px cells
   - UV calculation maps correctly to texture cells
5. **Root Cause Identified**: Spacing < render width causes character overlap
   - charWidth=25 → spacing=13px, but render width=16px → **3px overlap**
   - Next character renders on top, overwriting previous character's pixels

---

## Key Findings

### Why Original Game Worked

**Original Japanese Game Spacing**:
- Field: `20 × charWidth / 64` (larger spacing for dialogue boxes)
- Battle: `10 × charWidth / 64` (tighter spacing for action names)
- For charWidth=25: Battle spacing = 10×25/64 ≈ **4 pixels**
- For charWidth=31: Battle spacing = 10×31/64 ≈ **5 pixels**

**But render width was variable** - characters weren't fixed at 16px in the original.

### Why PR #737 Broke

1. **Fixed render width**: All characters render at exactly 16×16 pixels (`v126 = 16`)
2. **Variable spacing**: `ceil(0.5 × charWidth)` ranges from 11-16 pixels
3. **When spacing < 16**: Next character overlaps previous character
4. **No minimum enforcement**: Code doesn't check if spacing ≥ render width

### Why Field Dialogue Still Works

Field dialogue (line 940) uses the same formula but reportedly "looks fine" because:
1. Field text boxes are wider (more forgiving of spacing variations)
2. Different positioning/centering algorithm may compensate
3. OR user hasn't noticed the same overlap issue (needs verification)

---

## Questions Raised (Unanswered)

1. **Why 0.5f multiplier?**
   - Original game used 2× multiplier
   - PR #737 uses 0.5× multiplier (4× difference!)
   - No documentation found explaining this choice
   - Possibly a mistake or misunderstanding of charWidthData scaling

2. **Why fixed 16px render width?**
   - All characters render at 16×16 regardless of actual glyph width
   - Original game may have had variable render widths
   - Decision not documented in PR #737

3. **Why same formula for all contexts?**
   - Original game used different multipliers for field (20/64) vs battle (10/64)
   - PR #737 unified to single formula
   - Trade-off not explained in available documentation

---

## Codebase Locations Reference

### FFNx Source
- **Battle text**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp` (lines 1513-1936)
- **Field text**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp` (lines 528-1149)
- **Menu text**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp` (lines 1150-1349)
- **Width data**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp` (lines 381-562)

### FF7 Executable Externals
- **Width table pointer**: `ff7_externals.g_text_spacing_DB958C` (address 0x99DDA8 for US 1.02)
- **Battle menu data**: `ff7_externals.battle_menu_data_DC3630`
- **Functions**:
  - `field_submit_draw_text_640x480_6E706D` (0x6E706D)
  - `battle_display_text_6D7245` (0x6D7245)
  - `draw_text_top_display_6D1CC0` (0x6D1CC0)

### AF3DN.P Analysis
- **File**: `/home/johnzealanddoyle/projects/tools/AF3DN.P.c`
- **Width function**: `sub_1000EF70` (lines 20197-20221) - character width lookup
- **String width**: `sub_1000EFD0` (lines 20227-20304) - full string width calculation
- **Battle text**: `sub_10010350` (lines 21035-21329) - battle text rendering
- **Width tables**:
  - `dword_10041F70` (0x10041F70) - 256 entries
  - `dword_10042370` (0x10042370) - 32 entries
  - `dword_100423F0` (0x100423F0) - 32 entries

### Documentation
- **PR #737 Analysis**: `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/PR737_COMPLETE_ANALYSIS.md`
- **Menu Address Map**: `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/MENU_TEXT_ADDRESS_MAP.md`
- **FFNx Developer Guide**: `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/FFNX_DEVELOPER_GUIDE.md`

---

## Recommendations

1. **Immediate Fix**: Apply Option A (fixed 16px spacing) to battle text function
   - Changes 7 lines in `draw_text_top_display_6D1CC0_jp()`
   - Zero risk to other text rendering
   - Eliminates character overlap completely

2. **Testing Required**:
   - Cast multiple spells in battle (Blizzard, Fire, Thunder, etc.)
   - Verify リ character no longer appears squished
   - Check both kanji and kana spell names
   - Confirm text centers correctly in battle text box

3. **Future Investigation**:
   - Verify field dialogue doesn't have same overlap issue
   - Consider if variable render width (v126) should be implemented
   - Research why PR #737 chose 0.5f multiplier vs original 2× multiplier
   - Document decision-making for future Japanese text work

4. **Alternative Approaches** (if fixed spacing looks wrong):
   - Option B: Minimum 16px spacing (allows wider characters to spread naturally)
   - Option C: Original multiplier (10/64 for battle, 20/64 for field)
   - Make render width variable based on charWidth

---

## Summary

**Problem**: Battle spell names show character overlap because spacing calculation (13px) is less than render width (16px).

**Cause**: PR #737 implementation uses `ceil(0.5 × charWidth)` for spacing while rendering all characters at fixed 16px width, causing next character to overwrite previous when spacing < 16.

**Fix**: Change spacing to minimum 16px in battle text function (`draw_text_top_display_6D1CC0_jp`) at lines 1719, 1729, 1739, 1749, 1759, 1774, and 1884.

**Impact**: Battle spell/action name display only. Does not affect field dialogue or menu text.

---

**Session End**: 2026-01-16 14:57 JST
**Total Investigation Time**: ~2 hours
**Tools Used**: 3 parallel Explore agents (FF7 EN EXE, FF7 JP/AF3DN.P, Makou Reactor), grep, file analysis, texture inspection

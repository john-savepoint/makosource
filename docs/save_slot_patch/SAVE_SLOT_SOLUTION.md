# FF7 Japanese Edition - Save Slot Alignment Fix

**Created:** 2025-12-08 15:28 JST (Monday)
**Last Modified:** 2025-12-08 15:28 JST (Monday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-ID:** 0681f78b-0382-45ee-898b-5a32b7ce32d5

---

## Executive Summary

This document describes the solution to the save slot cursor alignment issue in FF7's Japanese Edition mode (FFNx PR737). When `ff7_japanese_edition=true`, the save slot selection cursor was misaligned with the save slot text because Japanese text (セーブ１-１０) is shorter than English text (Save 1-10) and the original Japanese executable lacks trailing padding.

**Root Cause:** The English executable has trailing spaces after save slot text, but the Japanese executable doesn't. This causes cursor misalignment when using Japanese text.

**Solution:** Add 2 ideographic space characters (position 63 / 0x3F on jafont_1) after each save slot's text to provide proper width for cursor alignment.

---

## Table of Contents

1. [The Problem](#the-problem)
2. [Investigation Process](#investigation-process)
3. [Root Cause Analysis](#root-cause-analysis)
4. [The Solution](#the-solution)
5. [Implementation Details](#implementation-details)
6. [Technical Reference](#technical-reference)
7. [Files Modified](#files-modified)

---

## The Problem

### Symptoms

When viewing the save file selection screen with Japanese text:
- Save slot text (セーブ１ through セーブ１０) appeared left-aligned
- The selection cursor pointed at empty space instead of the save slot text
- All 10 save slots were compressed to the left side of their grid cells

### Context

- The English executable stores save slots as "Save 1   " with 3 trailing spaces
- The Japanese executable stores save slots as "セーブ１" with no trailing spaces
- The game uses fixed-width cells for the save slot grid layout
- Cursor position is calculated based on expected text width including padding

---

## Investigation Process

### Phase 1: Initial Analysis

We examined the byte structure of save slots in both executables:

**English EXE (Save 3):**
```
33 41 56 45 00 13 00 00 00 FF 00 00
S  a  v  e  SP 3  SP SP SP FF (term)
```

**Japanese EXE (セーブ３):**
```
5A D0 04 36 FF 00 00 00 00 00 00 00
セ ー ブ ３ FF (term)
```

The English version has 3 spaces (0x00) after the number, while Japanese has none.

### Phase 2: Failed Attempts

#### Attempt 1: Using 0x00 as space
- **Result:** Position 0 on jafont_1 is バ (katakana ba), not a space
- **Symptom:** "セーブ３ババババ" displayed as garbage

#### Attempt 2: Using 0xD9 (position 217) as space
- **Result:** Position 217 is an empty/unused tile with zero rendering width
- **Symptom:** No visible spacing added, text unchanged

### Phase 3: Success with 0x3F

Testing position 63 (0x3F) which maps to ideographic space (　, U+3000):
- **Result:** Visible width added, cursor alignment corrected
- **Optimal count:** 2 spaces (3 was slightly too much)

---

## Root Cause Analysis

### Font Position Mapping

On jafont_1, different positions have different behaviors:

| Position | Byte | Character | Behavior |
|----------|------|-----------|----------|
| 0 | 0x00 | バ | Renders as katakana ba |
| 63 | 0x3F | 　 | Ideographic space (full width) |
| 217 | 0xD9 | (empty) | Zero width, no rendering |

### Why EN Uses 0x00 for Spaces

In the English font texture (usfont), position 0 is likely a blank space. But on jafont_1, position 0 contains a character (バ), so we cannot use the same byte value.

### Cell Width Calculation

The game calculates save slot grid cell positions based on maximum expected text width. Without padding:
- EN: "Save 10  " = 9 characters of width
- JA: "セーブ１０" = 5 characters of width (but wider per character)

Adding ideographic spaces compensates for the width difference.

---

## The Solution

### The Fix

Add 2 ideographic space characters (0x3F) after each save slot's text before the terminator:

```
Original JA: 5A D0 04 36 FF 00 00 00 00 00 00 00  (セーブ３)
Patched:     5A D0 04 36 3F 3F FF 00 00 00 00 00  (セーブ３　　)
```

### Why 2 Spaces?

- 3 spaces caused slight over-extension past cell boundaries
- 2 spaces provides near-pixel-perfect alignment
- 1 space was insufficient for proper cursor alignment

### Special Case: Save 10

Save 10 (index 656) has only 8 bytes allocated:
- Text: セーブ１０ (5 bytes)
- Available for spaces: 8 - 5 - 1 (terminator) = 2 bytes
- Result: Exactly 2 spaces fit, which is optimal

---

## Implementation Details

### HEXT Generator Changes

**File:** `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/generate_exe_hext.py`

#### 1. Define Save Slot Region

```python
# Save slots need spacing added to align with cursor
# Save 1-2 (DEF type, indices 647-648) and Save 3-10 (RGB type, indices 649-656)
# Note: Index 657 is "Level" (レベル), NOT a save slot!
SAVE_SLOT_REGION = set(range(647, 657))  # Indices 647-656 (Save 1-10 only)
```

#### 2. Spacing Function

```python
def add_save_slot_spacing(data: bytes, target_length: int) -> bytes:
    """Add trailing spaces to save slot text to align with cursor.

    Testing position 63 (0x3F) which is ideographic space (　, U+3000) on jafont_1.
    Position 217 (0xD9) was found to be zero-width/non-rendering.
    """
    JAFONT1_SPACE = 0x3F  # Position 63 = ideographic space (　)

    result = bytearray()

    # Find where the text ends (0xFF terminator)
    for b in data:
        if b == 0xFF:
            break
        result.append(b)

    text_len = len(result)

    # Calculate how many spaces we can add while still fitting terminator
    available_space = target_length - text_len - 1  # -1 for terminator

    # Add up to 2 spaces, but only if there's room
    # 2 spaces provides better alignment than 3 for Japanese text width
    spaces_to_add = min(2, available_space)
    for _ in range(spaces_to_add):
        result.append(JAFONT1_SPACE)

    # Add terminator
    result.append(0xFF)

    # Pad rest with 0x00 (these are after terminator, won't render)
    while len(result) < target_length:
        result.append(0x00)

    return bytes(result[:target_length])
```

### Affected Indices

| Index | Type | Length | Content | Spaces Added |
|-------|------|--------|---------|--------------|
| 647 | DEF | 12 | セーブ１ | 2 |
| 648 | DEF | 12 | セーブ２ | 2 |
| 649 | RGB | 12 | セーブ３ | 2 |
| 650 | RGB | 12 | セーブ４ | 2 |
| 651 | RGB | 12 | セーブ５ | 2 |
| 652 | RGB | 12 | セーブ６ | 2 |
| 653 | RGB | 12 | セーブ７ | 2 |
| 654 | RGB | 12 | セーブ８ | 2 |
| 655 | RGB | 12 | セーブ９ | 2 |
| 656 | RGB | 8 | セーブ１０ | 2 |

### Skipped Index

Index 657 (レベル / "Level") was incorrectly included initially, causing display corruption. It contains control bytes for color/positioning and must be skipped entirely.

---

## Technical Reference

### jafont_1 Space Characters

| Position | Byte | Unicode | Name | Behavior |
|----------|------|---------|------|----------|
| 0 | 0x00 | U+30D0 | バ | NOT a space - renders as katakana |
| 63 | 0x3F | U+3000 | 　 | Ideographic space - full width ✓ |
| 217 | 0xD9 | - | (empty) | Zero width - no visual effect |

### Save Slot Byte Format

```
[Text bytes] [Space bytes] [0xFF terminator] [0x00 padding]
```

Example for Save 3 (12 bytes total):
```
5A D0 04 36 3F 3F FF 00 00 00 00 00
セ ー ブ ３ 　 　 FF -- -- -- -- --
```

---

## Verification

### Before Fix
- Cursor pointing at empty space
- All save slots compressed to left
- Grid cell boundaries not respected

### After Fix
- Cursor aligns with save slot text
- Even spacing across all 10 slots
- Near-pixel-perfect grid alignment

---

## Lessons Learned

1. **Font position 0 is NOT always a space** - Different fonts have different characters at position 0. Always verify the character map.

2. **Empty tiles may have zero width** - Position 217 (0xD9) appeared empty in the map but rendered with no width, making it useless for spacing.

3. **Ideographic space (U+3000) works** - Position 63 (0x3F) on jafont_1 is a proper full-width space character.

4. **Respect byte length limits** - Save 10's 8-byte limit meant we could only fit 2 spaces maximum, which fortunately was the optimal amount anyway.

5. **Watch for non-text entries** - Index 657 looked like a save slot but was actually "Level" with control bytes. Including it caused display corruption.

---

## Related Documentation

- `../keyboard_patch/KEYBOARD_SOLUTION.md` - Similar fix for keyboard label rendering
- Session handoffs in `/home/johnzealanddoyle/projects/tools/.project/session_handoffs/`

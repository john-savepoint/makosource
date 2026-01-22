# Heart Symbol (♥) Investigation Report

**Created**: 2025-12-10 15:06 JST (Wednesday)
**Last Modified**: 2025-12-10 15:06 JST (Wednesday)
**Version**: 1.0.0
**Author**: John Zealand-Doyle / Claude Code
**Session-ID**: 94f5f148-6c89-4d95-a0b5-104c7ebdd735

---

## Executive Summary

This report documents the investigation into why heart symbols (♥) do not display in FFNx when playing FF7 with Japanese field text, despite displaying correctly in the Japanese eStore version.

**Root Cause Found**: The heart character uses byte `0xD9` (217) which should render from `jafont_1[217]`. However, FFNx's hardcoded `charWidthData[0][217]` is set to **0**, making the character invisible (zero width).

**Solution**: Change `charWidthData[0][217]` from `0` to `15` in FFNx's `japanese_text.cpp` line 336.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Investigation Process](#investigation-process)
3. [Key Findings](#key-findings)
4. [Technical Details](#technical-details)
5. [The Fix](#the-fix)
6. [Verification Status](#verification-status)
7. [Scripts Created](#scripts-created)
8. [Next Steps](#next-steps)
9. [Appendix: Byte Sequences](#appendix-byte-sequences)

---

## Problem Statement

### Symptom
Heart symbols (♥) appear in the Japanese PlayStation/eStore version of FF7 dialogue but do NOT appear when playing with FFNx using Japanese field text.

### Example Dialogue (Jessie's line)
```
「ほんとは、もうひとつあるんだけど
　いまは秘密♥　楽しみに待っててね♥」

Translation: "Actually, there's one more thing, but for now it's a secret♥ Look forward to it♥"
```

### Previous Incorrect Assumption
We initially thought `FE D9` was the heart character encoding. This was **WRONG**:
- `FE D9` is actually a **color control code** (white/reset color)
- Modifying `FE D9` to render as a character broke color resetting and caused text truncation

---

## Investigation Process

### Phase 1: Field File Extraction
1. Created Python script to extract files from Japanese field LGP (`jfleve.lgp`)
2. Implemented proper FF7 LZS decompression algorithm
3. Searched for dialogue containing `秘密` (himitsu/"secret")

### Phase 2: Pattern Analysis
1. Searched all 729 field files for `秘密` pattern (`FB 23 FD 3D`)
2. Found 44 files containing the pattern
3. Identified `mds7_w2` as containing Jessie's dialogue

### Phase 3: Byte-Level Analysis
1. Decompressed `mds7_w2` field file (249,754 bytes decompressed)
2. Found 10 occurrences of `秘密` in the file
3. Analyzed bytes immediately following `秘密`

### Phase 4: Discovery
Found the heart encoding at offset `0x903C`:
```
FE DB FB 23 FD 3D D9 FE DB 3F ...
```

Decoded:
- `FE DB` = Rainbow toggle ON
- `FB 23` = 秘 (jafont_3[35])
- `FD 3D` = 密 (jafont_5[61])
- `D9` = **♥ HEART** (jafont_1[217])
- `FE DB` = Rainbow toggle OFF
- `3F` = Space

---

## Key Findings

### Finding 1: Heart Encoding
| Attribute | Value |
|-----------|-------|
| **Byte Value** | `0xD9` (217 decimal) |
| **Encoding Type** | Direct byte (NO prefix) |
| **Font Texture** | jafont_1 |
| **Texture Position** | 217 (row 13, column 9) |

### Finding 2: FE D9 is NOT the Heart
| Byte Sequence | Meaning |
|---------------|---------|
| `FE D9` | Color code: WHITE (reset to default color) |
| `0xD9` alone | Character from jafont_1[217] = Heart |

### Finding 3: Why Hearts Don't Display
1. ✓ Texture `jafont_1[217]` **HAS** the heart glyph (we added it previously)
2. ✗ FFNx `charWidthData[0][217]` = **0** (zero width = invisible!)

### Finding 4: Width Table Location
File: `/mnt/c/FFNx/src/ff7/japanese_text.cpp`
Line: 336 (jafont_1, row 13 = positions 208-223)

```cpp
// Position 217 is at index 9 (217 % 16 = 9)
28, 27, 27, 29, 30, 12, 25, 22, 11, 0, 27, 23, 23, 23, 12, 22,
//                                 ^ Position 217 = 0 (INVISIBLE!)
```

---

## Technical Details

### FF7 Character Encoding System

| Prefix Byte | Font Texture | Example |
|-------------|--------------|---------|
| None (0x00-0xF9) | jafont_1 | `0xD9` → position 217 |
| `0xFA` | jafont_2 | `FA 23` → position 35 |
| `0xFB` | jafont_3 | `FB 23` → 秘 (position 35) |
| `0xFC` | jafont_4 | `FC 58` → 言 (position 88) |
| `0xFD` | jafont_5 | `FD 3D` → 密 (position 61) |
| `0xFE` | jafont_6 or control | See below |

### FE Prefix Special Codes

| Sequence | Meaning |
|----------|---------|
| `FE D2` | Color: Gray |
| `FE D3` | Color: Blue |
| `FE D4` | Color: Red |
| `FE D5` | Color: Purple |
| `FE D6` | Color: Green |
| `FE D7` | Color: Yellow |
| `FE D8` | Color: Cyan |
| `FE D9` | Color: White (reset) |
| `FE DA` | Blink toggle |
| `FE DB` | Rainbow toggle |

### FFNx Code Flow for Direct Bytes

From `japanese_text.cpp`:

```cpp
// Lines 603-611 (default case for non-prefixed bytes)
default:
  if(!kanjiDetected)
  {
    graphics_object = ff7_externals.menu_jafont_1_graphics_object;
    charWidth = charWidthData[0][*buffer_text] & 0x1F;  // Gets width for 0xD9
    leftPadding = charWidthData[0][*buffer_text] >> 5;
  }
  kanjiDetected = false;
  break;
```

For byte `0xD9`:
- `charWidthData[0][217] = 0`
- `charWidth = 0 & 0x1F = 0` ← **Zero width = invisible!**

---

## The Fix

### Location
- **File**: `/mnt/c/FFNx/src/ff7/japanese_text.cpp`
- **Line**: 336
- **Array**: `charWidthData[0]` (jafont_1 spacing)
- **Row**: 13 (positions 208-223)
- **Index**: 9 (position 217 = 217 % 16)

### Change Required

```cpp
// BEFORE (line 336):
28, 27, 27, 29, 30, 12, 25, 22, 11, 0, 27, 23, 23, 23, 12, 22,

// AFTER:
28, 27, 27, 29, 30, 12, 25, 22, 11, 15, 27, 23, 23, 23, 12, 22,
//                                 ^^
// Changed position 217's width from 0 to 15
```

### Why 15?
- Standard character width in FF7 is around 12-16 pixels
- Heart is a simple symbol, 15 provides good spacing
- Can be adjusted if needed after testing

---

## Verification Status

### Texture Verification
| Check | Status |
|-------|--------|
| jafont_1.png exists | ✓ |
| Position 217 has glyph | ✓ (2330 non-transparent pixels, 56.9% coverage) |
| Heart shape correct | ✓ (added in previous session) |

### Code Verification
| Check | Status |
|-------|--------|
| Default case routes to jafont_1 | ✓ |
| UV coordinates calculated correctly | ✓ (U=288, V=416 for pos 217) |
| charWidthData[0][217] = 0 | ✓ (confirmed as root cause) |

### Pending Verification
| Check | Status |
|-------|--------|
| Fix applied to FFNx source | ⏳ Pending |
| FFNx recompiled | ⏳ Pending |
| Hearts display in game | ⏳ Pending |

---

## Scripts Created

Two Python scripts were created during this investigation:

### 1. `scripts/ff7_field_extractor.py`
**Purpose**: Extract and decompress FF7 field files from LGP archives

**Features**:
- LGP archive table of contents reader
- FF7 LZS decompression algorithm
- Field file section parser
- Pattern search with context

**Usage**:
```bash
python3 scripts/ff7_field_extractor.py
```

### 2. `scripts/ff7_heart_analyzer.py`
**Purpose**: Analyze heart symbol encoding and verify texture readiness

**Features**:
- Character map loader (CSV format)
- Field text decoder (handles all prefixes and control codes)
- Heart occurrence finder
- Texture verification (checks jafont_1[217])

**Usage**:
```bash
# Full analysis
python3 scripts/ff7_heart_analyzer.py

# Verify texture only
python3 scripts/ff7_heart_analyzer.py --verify-texture

# Print summary only
python3 scripts/ff7_heart_analyzer.py --summary
```

---

## Next Steps

### Immediate Actions

1. **Apply the fix to FFNx source**
   - Edit `/mnt/c/FFNx/src/ff7/japanese_text.cpp` line 336
   - Change `0` to `15` at position 9 in that row

2. **Recompile FFNx**
   - Build the modified FFNx
   - Generate new DLL

3. **Test in game**
   - Load save near Jessie's dialogue
   - Or use `mds7_w2` field (Sector 7 area)
   - Verify hearts display with rainbow effect

### Optional Improvements

4. **Add jafont_6[217] width** (if hearts also used there)
   - Check `charWidthData[5][217]` in the same file
   - May also need updating

5. **Document in codebase**
   - Add comment explaining position 217 is heart
   - Prevent future confusion

---

## Appendix: Byte Sequences

### Jessie's Dialogue (mds7_w2, offset 0x9014)

```
Raw bytes:
4C 53 59 4C 45 05 0B 25 4D 61 9F 6D 14 4E BE 53
52 49 99 67 41 52 53 46 43 67 63 6B 8B 99 1F 51
4E BE 53 6D 7D 41 FE DB FB 23 FD 3D D9 FE DB 3F
FB 38 57 7F 75 FC AD 9D 65 65 79 D9 49 58 45 85
```

### Decoded Sequence
```
... いまは [RAINBOW] 秘密 ♥ [RAINBOW] 　楽しみに待っててね ...
```

### Byte-by-Byte Breakdown (key section)

| Offset | Bytes | Decoded |
|--------|-------|---------|
| 0x9034 | `4E BE 53 6D 7D 41` | ...いまは |
| 0x903A | `FE DB` | [RAINBOW ON] |
| 0x903C | `FB 23` | 秘 |
| 0x903E | `FD 3D` | 密 |
| 0x9040 | `D9` | **♥ (HEART!)** |
| 0x9041 | `FE DB` | [RAINBOW OFF] |
| 0x9043 | `3F` | (space) |
| 0x9044 | `FB 38 57 7F 75 FC AD` | 楽しみに待っ... |

---

## Conclusion

The heart symbol investigation is complete. The root cause is identified as:

1. **Heart encoding**: Direct byte `0xD9` (217) from jafont_1
2. **Why invisible**: FFNx's `charWidthData[0][217]` = 0 (zero width)
3. **The fix**: Change width from 0 to 15 in `japanese_text.cpp` line 336

The texture already has the heart glyph at the correct position. Only the width data needs to be fixed in the FFNx source code.

---

*Report generated by Claude Code during FF7 Japanese localization investigation.*

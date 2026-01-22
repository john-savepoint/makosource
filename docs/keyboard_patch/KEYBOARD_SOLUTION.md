# FF7 Japanese Edition - Keyboard Label Fix

**Created:** 2025-12-08 14:26 JST (Monday)
**Last Modified:** 2025-12-08 14:26 JST (Monday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-ID:** 0681f78b-0382-45ee-898b-5a32b7ce32d5

---

## Executive Summary

This document describes the solution to the keyboard label rendering issue in FF7's Japanese Edition mode (FFNx PR737). When `ff7_japanese_edition=true`, keyboard labels like "ESCAPE", "INSERT", "PAGE UP" displayed as garbage Japanese characters instead of readable text.

**Root Cause:** The game applies a `-0x20` byte transformation to keyboard label bytes before font texture lookup, but FFNx's Japanese mode expects direct tile indices.

**Solution:** Add `+0x20` to the Japanese executable's keyboard bytes in the HEXT patch to compensate for the game's transformation.

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

When running FF7 with FFNx PR737's Japanese Edition mode (`ff7_japanese_edition=true`), the Config → Controller → Customize screen displayed:

| Expected | Actual Display |
|----------|----------------|
| ESCAPE | ンィワヨょン |
| INSERT | ツゅインあい |
| PAGE UP | ょヨヲンだウょ |
| BUTTON 9 | よりいヨゆだヂ |
| BUTTON 10 | よりいヨゆだザご |

### Context

- FFNx PR737 routes ALL text rendering through the Japanese font texture (`jafont_1.tim`)
- The English executable stores keyboard labels in "RGB encoding" (ASCII + 0x73)
- The Japanese executable stores keyboard labels with bytes that map to fullwidth English positions on jafont_1
- HEXT patches were being applied correctly to memory, but garbage still displayed

---

## Investigation Process

### Phase 1: Initial Hypothesis (Sessions 03-06)

We initially believed the issue was that:
1. FFNx wasn't handling RGB-encoded strings
2. We needed to apply RGB encoding (+0x93 from FF7 bytes) in the HEXT generator

This was partially correct but incomplete.

### Phase 2: External Agent Consultation

We consulted an FFNx code analysis agent who confirmed:

1. **HEXT patches ARE applied correctly** - via `hextPatcher.applyAll()` in `DllMain` before game execution
2. **The Config menu DOES read from patched memory** - no caching issues
3. **All text goes through `common_submit_draw_char_from_buffer_6F564E_jp`** - the standard hooked function
4. **FFNx does NOT decode RGB** - it uses raw byte values as tile indices

This told us the HEXT patches were working, but something else was transforming the bytes.

### Phase 3: The Breakthrough Test

We created a test HEXT that wrote known Japanese characters (テスト = `0x64, 0x59, 0x66`) to all keyboard entries.

**Expected result:** テスト (te-su-to)
**Actual result:** フ6ヘ( (fu-6-he-()

This was the breakthrough. We could now calculate the offset:

| Sent Byte | Expected Char | Displayed Char | Displayed Position | Offset |
|-----------|---------------|----------------|-------------------|--------|
| 0x64 (100) | テ | フ | 68 (0x44) | -32 (-0x20) |
| 0x59 (89) | す | ６ | 57 (0x39) | -32 (-0x20) |
| 0x66 (102) | ト | ヘ | 70 (0x46) | -32 (-0x20) |

**Consistent -0x20 offset discovered!**

### Phase 4: Verification Against Original Garbage

We verified this against the original garbage characters:

The JA exe has RGB bytes for ESCAPE: `B8 C6 B6 B4 C3 B8`

| RGB Byte | - 0x20 | Position | Character |
|----------|--------|----------|-----------|
| 0xB8 | 0x98 | 152 | ン |
| 0xC6 | 0xA6 | 166 | ィ |
| 0xB6 | 0x96 | 150 | ワ |
| 0xB4 | 0x94 | 148 | ヨ |
| 0xC3 | 0xA3 | 163 | ょ |
| 0xB8 | 0x98 | 152 | ン |

**Result: ンィワヨょン** - Exactly matches the garbage we saw!

---

## Root Cause Analysis

### The FF7 Text Encoding System

FF7 uses a custom text encoding where printable ASCII characters are stored as `ASCII - 0x20`:

```
'A' (0x41) stored as 0x21
'E' (0x45) stored as 0x25
' ' (0x20) stored as 0x00
```

When rendering, the game normally adds `+0x20` back to get the correct font position.

### The RGB Encoding System

For certain strings (keyboard labels, color names), FF7 uses "RGB encoding":

```
ASCII character + 0x73 = RGB byte
'E' (0x45) + 0x73 = 0xB8
```

On the Japanese font texture (jafont_1), fullwidth English letters are at positions 180-205:
- Position 180 (0xB4) = Ａ
- Position 184 (0xB8) = Ｅ
- Position 198 (0xC6) = Ｓ

### The Conflict

The keyboard label rendering path applies the standard `-0x20` transformation expecting FF7-encoded text, but:

1. **English exe:** Has RGB-encoded bytes (e.g., `0xB8` for 'E')
2. **Japanese exe:** Also has RGB-encoded bytes mapping to fullwidth English
3. **FFNx Japanese mode:** Routes to jafont_1, expects direct tile indices
4. **Game's rendering:** Still applies `-0x20` to the bytes

Result: `0xB8 - 0x20 = 0x98` → position 152 → ン (garbage)

### Why This Only Affects Keyboard Labels

The keyboard label region (indices 77-213) uses a different rendering path than regular menu text. This path preserves the `-0x20` transformation that was designed for the English font but breaks when routed to the Japanese font.

---

## The Solution

### The Fix

Add `+0x20` to all keyboard region bytes before writing to HEXT:

```
JA byte + 0x20 = HEXT patch byte
HEXT patch byte - 0x20 (game transformation) = JA byte
JA byte → correct position on jafont_1 → correct character displayed
```

### Example: ESCAPE

```
JA exe bytes:     B8 C6 B6 B4 C3 B8 (maps to ＥＳＣＡＰＥ)
+ 0x20:           D8 E6 D6 D4 E3 D8 (HEXT patch bytes)
Game applies -0x20: B8 C6 B6 B4 C3 B8 (back to original)
Font lookup:      positions 184, 198, 182, 180, 195, 184
Display:          Ｅ  Ｓ  Ｃ  Ａ  Ｐ  Ｅ  ✓
```

### Edge Case: BUTTON 9 and BUTTON 10

These entries (indices 212-213) are marked as DEF type in touphScript's tables, but they:
1. Use the same RGB-encoded byte format as the keyboard region
2. Are rendered through the same path that applies -0x20

Solution: Extend the keyboard region to include indices 212-213.

---

## Implementation Details

### HEXT Generator Changes

**File:** `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/generate_exe_hext.py`

#### 1. Define Keyboard Region

```python
# Keyboard region needs special handling: JA bytes + 0x20
# The game/FFNx applies -0x20 to keyboard bytes before font lookup,
# so we must add +0x20 to compensate
# Note: Indices 212-213 (BUTTON 9, BUTTON 10) are marked DEF but use same rendering path
KEYBOARD_REGION = set(range(77, 214))  # Keyboard labels (indices 77-213)
```

#### 2. Offset Function

```python
def apply_keyboard_offset(data: bytes) -> bytes:
    """Apply +0x20 offset to keyboard bytes to compensate for game's -0x20 transformation."""
    result = bytearray()
    for byte in data:
        if byte == 0x00 or byte == 0xFF:
            # Terminators/spaces - keep as is
            result.append(byte)
        elif byte <= 0xDF:
            # Add 0x20, but don't overflow past 0xFF
            result.append(byte + 0x20)
        else:
            # Already high values - keep as is to avoid overflow
            result.append(byte)
    return bytes(result)
```

#### 3. Generation Logic

```python
if stype == StringType.RGB:
    # Keyboard region: JA bytes + 0x20 to compensate for game's -0x20 transformation
    if i in KEYBOARD_REGION:
        en_text = decode_english(en_bytes)
        patch_bytes = apply_keyboard_offset(ja_bytes)
        ja_text = f"[KB:{rgb_decoded.strip()}]"
    # ... other RGB handling
else:
    # DEF, NOFF_TERM, FFPADDED, ZEROTERM
    # Check if this DEF entry is in keyboard region (BUTTON 9/10 are DEF but need offset)
    if i in KEYBOARD_REGION:
        patch_bytes = apply_keyboard_offset(ja_bytes)
    else:
        patch_bytes = ja_bytes
```

### Affected Indices

| Index Range | Count | Type | Description |
|-------------|-------|------|-------------|
| 77-211 | 135 | RGB | Keyboard labels (ESCAPE, INSERT, F1-F12, etc.) |
| 212-213 | 2 | DEF | BUTTON 9, BUTTON 10 (same rendering path) |

---

## Technical Reference

### Encoding Formulas

```
FF7 Encoding:     ASCII - 0x20 = FF7 byte
RGB Encoding:     ASCII + 0x73 = RGB byte (= FF7 byte + 0x93)
Keyboard Fix:     JA byte + 0x20 = HEXT patch byte
```

### jafont_1 Layout (Relevant Sections)

| Position Range | Characters |
|----------------|------------|
| 0-9 | Special symbols |
| 33-58 | Numbers and punctuation |
| 64-127 | Hiragana |
| 128-191 | Katakana |
| 180-205 | Fullwidth A-Z (Ａ-Ｚ) |
| 206-231 | Fullwidth a-z (ａ-ｚ) |

### Key Byte Values

| Character | ASCII | FF7 Encoding | RGB Encoding | jafont_1 Position |
|-----------|-------|--------------|--------------|-------------------|
| E | 0x45 | 0x25 | 0xB8 | 184 |
| S | 0x53 | 0x33 | 0xC6 | 198 |
| C | 0x43 | 0x23 | 0xB6 | 182 |
| A | 0x41 | 0x21 | 0xB4 | 180 |
| P | 0x50 | 0x30 | 0xC3 | 195 |

---

## Files Modified

### Scripts

- `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/generate_exe_hext.py`
  - Added `KEYBOARD_REGION` constant
  - Added `apply_keyboard_offset()` function
  - Updated generation logic to apply offset to keyboard region

- `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/generate_exe_hext_test.py`
  - Test script with multiple keyboard transformation modes
  - Used for debugging and discovering the -0x20 offset

- `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/analyze_regions.py`
  - Region analysis tool showing type distribution and byte contents

### Output

- `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/ja/japanese_menu.txt`
  - Final HEXT patch file with 555 patches
  - Keyboard region (137 entries) now has +0x20 offset applied

---

## Verification

### Before Fix
```
【けってい】  ンィワヨょン    よりいヨゆだジ
【キャンセル】 ワ              よりいヨゆだぎ
【メニュー】   う              よりいヨゆだじ
```

### After Fix
```
【けってい】  ESCAPE          BUTTON 3
【キャンセル】 C               BUTTON 2
【メニュー】   V               BUTTON 4
```

---

## Lessons Learned

1. **Test with known values** - Writing test bytes (テスト) and observing the output allowed us to calculate the exact offset mathematically.

2. **Verify assumptions** - The FFNx agent confirmed HEXT patches were being applied, ruling out that hypothesis and pointing us toward a transformation issue.

3. **Cross-reference character maps** - Having a complete jafont_1 character map was essential for reverse-engineering what positions the garbage characters came from.

4. **Type boundaries aren't always accurate** - BUTTON 9/10 were marked as DEF type but used the same RGB rendering path as the keyboard region.

5. **Document the journey** - The systematic approach of hypothesis → test → measure → adjust led to the solution.

---

## Related Documentation

- `KEYBOARD_PATCH_ANALYSIS.md` - Earlier analysis with Mermaid diagrams (in same directory)
- Session handoffs in `/home/johnzealanddoyle/projects/tools/.project/session_handoffs/`
  - `SESSION_HANDOFF_2025-12-08-07_RGB_ENCODING_IMPLEMENTATION.md`
  - `SESSION_HANDOFF_2025-12-07-04_RGB_ENCODING_BREAKTHROUGH.md`

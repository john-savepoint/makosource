# Keyboard Offset Solution (+0x20 Compensation)

**Created:** 2026-01-02 20:55 JST
**Session ID:** c31eb494-cb6d-474e-8432-4bc1284b2ed0
**Source:** `generate_exe_hext.py` lines 435-452

## 1. The Problem

The keyboard configuration screen displays key labels (ESCAPE, ENTER, BUTTON 1, etc.). When patching these with Japanese text, the labels displayed incorrectly - shifted by 0x20 positions on the font texture.

### Root Cause

The game's rendering code (or FFNx's handling) applies a **-0x20 transformation** to keyboard label bytes before looking up the character on the font texture.

This means:
- If you write byte `0xB8` (position 184 = "Ｅ" on jafont_1)
- The game subtracts 0x20: `0xB8 - 0x20 = 0x98`
- It looks up position 152 instead of 184
- You see the wrong character

## 2. The Solution

**Pre-add +0x20 to compensate for the game's -0x20.**

```python
def apply_keyboard_offset(data: bytes) -> bytes:
    """Apply +0x20 offset to keyboard bytes to compensate for game's -0x20 transformation.

    The game/FFNx applies -0x20 to keyboard label bytes before font lookup,
    so we add +0x20 to the JA bytes to compensate.
    """
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

### Why 0xDF Threshold?

- Maximum safe value: `0xDF + 0x20 = 0xFF` (still valid)
- Values above 0xDF: `0xE0 + 0x20 = 0x100` (overflow!)
- Values 0xE0-0xFE are multi-byte prefix codes (0xFA-0xFE) or terminators
- These should not be modified

## 3. Which Indices Need This Fix?

```python
KEYBOARD_REGION = set(range(77, 214))  # Indices 77-213
```

This includes:
- Indices 77-211: RGB type keyboard labels
- Indices 212-213: DEF type labels (BUTTON 9, BUTTON 10)

### Why Include DEF Types (212-213)?

Even though indices 212-213 are marked as DEF type (not RGB), they're rendered through the same keyboard code path that applies the -0x20 transformation. The script checks for both:

```python
if stype == StringType.RGB:
    if i in KEYBOARD_REGION:
        patch_bytes = apply_keyboard_offset(ja_bytes)
# ...
else:  # DEF type
    if i in KEYBOARD_REGION:
        patch_bytes = apply_keyboard_offset(ja_bytes)
```

## 4. Keyboard Label Examples

### ESCAPE Key (Index 77)

| Stage | Bytes | Explanation |
|-------|-------|-------------|
| JA exe raw | `B8 C6 B6 B4 C3 B8` | ＥＳＣＡＰＥ in RGB encoding |
| After +0x20 | `D8 E6 D6 D4 E3 D8` | Pre-compensated values |
| Game applies -0x20 | `B8 C6 B6 B4 C3 B8` | Correct lookup! |
| Result | Ｅ Ｓ Ｃ Ａ Ｐ Ｅ | Displays correctly |

### Single Letters (Q, R, S, T, U, V, W, X, Y)

| Index | EN Text | JA Raw | After +0x20 | Result |
|-------|---------|--------|-------------|--------|
| 78 | Q | 0x34 | 0x54 | Ｑ |
| 79 | R | 0x35 | 0x55 | Ｒ |
| 80 | S | 0x36 | 0x56 | Ｓ |
| 81 | T | 0x37 | 0x57 | Ｔ |
| 82 | U | 0x38 | 0x58 | Ｕ |

## 5. Actual HEXT Output Examples

From the generated `japanese_menu.txt`:

```
# escape   -> [KB:ESCAPE]
# EN: 0x00519FE0 (8 bytes)
# JA: 0x0051ABE0
91B5E0 = D8 E6 D6 D4 E3 D8 00 00

# Q    -> [KB:?]
# EN: 0x00519FE8 (4 bytes)
# JA: 0x0051ABE8
91B5E8 = 54 00 00 00
```

Note: The "[KB:?]" display is because the script can't decode the RGB bytes to display text (the `?` comes from failing to decode single-byte RGB values).

## 6. Level Label Special Case

Index 657 (レベル / Level) is RGB type but does NOT need the +0x20 offset:

```python
LEVEL_INDEX = 657

# In the main loop:
elif i == LEVEL_INDEX:
    en_text = decode_english(en_bytes)
    patch_bytes = ja_bytes  # Direct copy, no offset needed
    ja_text = "レベル"
```

**Why?** The Level label is displayed through the menu rendering path, not the keyboard rendering path. The menu renderer does not apply the -0x20 transformation.

## 7. German Implications

For German, the keyboard handling situation is likely different:

1. **German may not need +0x20** - If German exe uses standard Latin keyboard labels
2. **German special characters** - ö, ä, ü, ß may or may not go through keyboard path
3. **Testing required** - Need to verify if German keyboard labels render correctly without offset

### Testing Approach for German

1. First try patching keyboard region WITHOUT +0x20
2. If labels render shifted, apply the same +0x20 offset
3. Check if German special characters (0x6A ö, 0x7A ü, 0x7F Ü, 0x7E ß) display correctly

## 8. Why This Matters

The keyboard offset is a **critical piece of the puzzle** that wasn't obvious from static analysis. It was discovered through:

1. Testing HEXT patches in-game
2. Observing keyboard labels rendered incorrectly
3. Analyzing the byte shift pattern (consistently -0x20)
4. Adding pre-compensation to fix the issue

Without this fix:
- All keyboard labels display garbage characters
- The configuration screen is unusable in Japanese
- User cannot rebind keys

With this fix:
- Keyboard labels display correctly (ＥＳＣＡＰＥ, ＥＮＴＥＲ, etc.)
- Configuration screen is fully functional
- Japanese localization is complete

## 9. Technical Deep Dive

### RGB Encoding Without Keyboard Offset

For non-keyboard RGB regions, the script uses `encode_rgb()`:

```python
def encode_rgb(data: bytes) -> bytes:
    result = bytearray()
    for byte in data:
        if byte == 0x00:
            result.append(0x00)  # Space
        elif byte == 0xFF:
            result.append(0xFF)  # Terminator
        elif 0x21 <= byte <= 0x3A:
            # FF7 uppercase A-Z -> fullwidth
            result.append(byte + 0x93)
        elif 0x41 <= byte <= 0x5A:
            # FF7 lowercase a-z -> uppercase fullwidth
            result.append(byte - 0x20 + 0x93)
        elif 0x01 <= byte <= 0x5F:
            # Other printable
            result.append(byte + 0x93)
        else:
            result.append(byte)
    return bytes(result)
```

This is used for RGB regions that are NOT keyboard labels - they keep the English text but encode it for display on jafont_1.

### Keyboard Offset Is Different

For keyboard labels, we:
1. Take the JA bytes directly (already RGB-encoded in JA exe)
2. Apply +0x20 to compensate for game transformation
3. Write the pre-compensated bytes

We do NOT re-encode using `encode_rgb()` because the JA exe already has properly encoded RGB text.

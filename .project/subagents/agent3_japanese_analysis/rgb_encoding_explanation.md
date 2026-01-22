# RGB Encoding Explanation

**Created:** 2026-01-02 21:00 JST
**Session ID:** c31eb494-cb6d-474e-8432-4bc1284b2ed0
**Source:** `generate_exe_hext.py` lines 388-432

## 1. What is RGB Encoding?

RGB encoding is a secondary text encoding used in FF7's PC executable for certain UI elements. Unlike the standard DEF encoding (FF7 encoding), RGB uses a different byte-to-character mapping.

### The Formula

```
RGB_byte = FF7_byte + 0x93
         = (ASCII - 0x20) + 0x93
         = ASCII + 0x73
```

Where:
- **ASCII** = Standard ASCII value (e.g., 'A' = 0x41)
- **FF7_byte** = ASCII - 0x20 (e.g., 'A' = 0x21)
- **RGB_byte** = Position on jafont_1 texture (e.g., 'A' -> 0xB4 = position 180)

## 2. Why RGB Encoding Exists

The RGB encoding was designed to map uppercase English letters to the fullwidth character positions on the Japanese font texture (jafont_1).

### jafont_1 Fullwidth Character Positions

| Character | ASCII | FF7 Byte | RGB Byte | Position |
|-----------|-------|----------|----------|----------|
| Ａ | 0x41 | 0x21 | 0xB4 | 180 |
| Ｂ | 0x42 | 0x22 | 0xB5 | 181 |
| Ｃ | 0x43 | 0x23 | 0xB6 | 182 |
| ... | ... | ... | ... | ... |
| Ｚ | 0x5A | 0x3A | 0xCD | 205 |

The fullwidth characters Ａ-Ｚ are located at positions 180-205 on jafont_1.

## 3. The encode_rgb() Function

```python
def encode_rgb(data: bytes) -> bytes:
    """
    Encode FF7-encoded bytes using RGB encoding.

    The EN exe stores keyboard labels in FF7 encoding (ASCII - 0x20).
    To display them correctly on jafont_1, we need to convert them to
    positions where fullwidth English letters are located.
    """
    result = bytearray()
    for byte in data:
        if byte == 0x00:
            # Null/space - keep as is
            result.append(0x00)
        elif byte == 0xFF:
            # Terminator - keep as is
            result.append(0xFF)
        elif 0x21 <= byte <= 0x3A:
            # FF7 uppercase A-Z (0x21-0x3A) -> add 0x93 to get fullwidth
            result.append(byte + 0x93)
        elif 0x41 <= byte <= 0x5A:
            # FF7 lowercase a-z (0x41-0x5A) -> convert to uppercase then add 0x93
            result.append(byte - 0x20 + 0x93)
        elif 0x01 <= byte <= 0x5F:
            # Other FF7 printable characters - add 0x93
            result.append(byte + 0x93)
        else:
            # Other bytes (control codes, etc.) - keep as is
            result.append(byte)
    return bytes(result)
```

## 4. RGB Regions in the String Table

The following index ranges use RGB encoding (StringType.RGB = 2):

| Index Range | Content | Handling |
|-------------|---------|----------|
| 77-211 | Keyboard labels | apply_keyboard_offset() |
| 212-213 | BUTTON 9/10 | apply_keyboard_offset() (DEF type but keyboard path) |
| 649-656 | Save slots 3-10 | add_save_slot_spacing() |
| 657 | Level label | copy ja_bytes directly |
| 658-686 | Timing/score formats | SKIPPED (identical EN/JA) |

## 5. Different RGB Region Handling

### Keyboard Labels (77-213): +0x20 Offset

The game's keyboard rendering applies -0x20 to bytes before lookup. We compensate:

```python
if i in KEYBOARD_REGION:
    patch_bytes = apply_keyboard_offset(ja_bytes)
```

### Save Slots (649-656): Copy JA with Spacing

Save slots use RGB encoding but store actual Japanese text (セーブ３, セーブ４, etc.):

```python
if i in RGB_COPY_JA_REGIONS:
    patch_bytes = add_save_slot_spacing(ja_bytes, length)
```

The JA exe already has the correct FF7-encoded Japanese text. We just need to add spacing for cursor alignment.

### Level Label (657): Direct Copy

The Level label (レベル) is RGB type but rendered through menu path (no -0x20):

```python
elif i == LEVEL_INDEX:
    patch_bytes = ja_bytes  # Direct copy, no offset needed
```

### Other RGB Regions (658-686): Skip

Timing formats like "00'00\"000" and "SURF" are identical in EN/JA:

```python
RGB_SKIP_REGIONS = set(range(658, 687))
```

## 6. Save Slot Deep Dive

### The Save Slot Problem

| Index | EN Text | EN Bytes | JA Text | JA Bytes |
|-------|---------|----------|---------|----------|
| 647 | Save 1 | DEF | セーブ１ | FF7-encoded |
| 648 | Save 2 | DEF | セーブ２ | FF7-encoded |
| 649 | Save 3 | RGB | セーブ３ | FF7-encoded |
| ... | ... | ... | ... | ... |
| 656 | Save 10 | RGB | セーブ１０ | FF7-encoded |
| 657 | Level | RGB | レベル | FF7-encoded |

**Important:** Index 657 is "Level" (レベル), NOT "Save 11"!

### Why Save Slots Need Spacing

The EN exe has trailing spaces after save slot text to align the cursor properly. The JA exe doesn't have these spaces because Japanese text is more compact.

```python
def add_save_slot_spacing(data: bytes, target_length: int) -> bytes:
    JAFONT1_SPACE = 0x3F  # Position 63 = ideographic space (　)

    result = bytearray()
    for b in data:
        if b == 0xFF:
            break
        result.append(b)

    # Add up to 2 ideographic spaces
    spaces_to_add = min(2, target_length - len(result) - 1)
    for _ in range(spaces_to_add):
        result.append(JAFONT1_SPACE)

    result.append(0xFF)
    while len(result) < target_length:
        result.append(0x00)

    return bytes(result[:target_length])
```

## 7. Decoding RGB for Display

The script includes a decoder for showing RGB text in comments:

```python
def decode_rgb_as_ascii(data: bytes) -> str:
    """Decode RGB-encoded bytes back to ASCII for display purposes."""
    result = []
    for byte in data:
        if byte == 0xFF:
            break
        if byte == 0x00:
            result.append(' ')
        elif 0x93 <= byte <= 0xF1:  # RGB range (0x20+0x73 to 0x7E+0x73)
            result.append(chr(byte - 0x73))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)
```

This is used to generate comments like:
```
# escape   -> [KB:ESCAPE]
```

## 8. RGB vs DEF Comparison

| Aspect | DEF (Type 0) | RGB (Type 2) |
|--------|--------------|--------------|
| Formula | ASCII - 0x20 | ASCII + 0x73 |
| Range | 0x01-0x5F | 0x93-0xF1 |
| Terminator | 0xFF | 0xFF |
| Space | 0x00 | 0x00 |
| Use case | Most menu text | Keyboard, save slots |

## 9. German Implications

### Does German Use RGB?

German likely uses the same RGB regions as English/Japanese:
- Keyboard labels
- Save slot names
- Timing displays

### German Special Characters in RGB Context

If German keyboard labels use ö, ä, ü, they may need special handling:

| Character | Standard Position | RGB Position? |
|-----------|------------------|---------------|
| ö | 0x6A (106) | Would need +0x93 = 0xFD? |
| ü | 0x7A (122) | Would need +0x93 = overflow! |

This could be problematic - the RGB range (0x93-0xF1) may not accommodate German special characters.

### Testing Required

1. Check if German keyboard labels use special characters
2. If so, determine how they're encoded in DE exe
3. May need different handling than Japanese

## 10. Summary

RGB encoding serves a specific purpose: mapping ASCII text to fullwidth positions on the Japanese font texture. The key points are:

1. **Formula:** RGB_byte = FF7_byte + 0x93
2. **Keyboard needs +0x20:** Game applies -0x20 before lookup
3. **Save slots copy JA:** Already FF7-encoded, just add spacing
4. **Level label is separate:** Index 657, no offset needed
5. **Some regions skip:** Timing formats are identical EN/JA

# Japanese HEXT Generator Methodology Analysis

**Created:** 2026-01-02 20:50 JST
**Session ID:** c31eb494-cb6d-474e-8432-4bc1284b2ed0
**Source File:** `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/generate_exe_hext.py`

## 1. Executive Summary

The Japanese HEXT generator (`generate_exe_hext.py`) creates binary patches to replace English menu text with Japanese text in the FF7 Steam/PC executable. It works by:

1. Reading the offset table from touphScript's `ff7exe.cpp`
2. Applying a consistent +0xC00 delta to find Japanese equivalents
3. Handling special cases for keyboard labels, save slots, and spacing
4. Generating HEXT format patches targeting Virtual Addresses

**KEY INSIGHT FOR GERMAN:** The Japanese solution relies on a **consistent offset delta** (0xC00) between EN and JA exe strings. German does NOT have this luxury - German strings are at unpredictable offsets relative to English.

---

## 2. The JA_OFFSET_DELTA (0xC00) Mechanism

```python
JA_OFFSET_DELTA = 0xC00  # Japanese exe strings are 0xC00 bytes ahead
```

### How It Works

For Japanese:
- **EN offset** (from touphScript): `0x518370`
- **JA offset** = `0x518370 + 0xC00` = `0x518F70`

This is a **consistent, predictable relationship** because:
1. Both EN and JA exes have identical structure
2. JA exe simply has an additional 0xC00 bytes inserted somewhere before the string table
3. Every single string follows this pattern

### The generate_hext() Function Core Loop

```python
for i, (en_offset, length, stype) in enumerate(zip(EN_OFFSETS, STRING_LENGTHS, STRING_TYPES)):
    # Calculate JA offset using the delta
    ja_offset = en_offset + JA_OFFSET_DELTA

    # Read bytes from both exes
    en_f.seek(en_offset)
    en_bytes = en_f.read(length)

    ja_f.seek(ja_offset)
    ja_bytes = ja_f.read(length)
```

### Implications for German

German CANNOT use this approach because:
- DE exe strings are at **different relative positions** than EN
- There is no consistent "delta" between EN and DE
- German requires **anchor-based mapping** (matching known strings to find offsets)

---

## 3. String Types and Their Handling

The script recognizes 6 string types from touphScript:

```python
class StringType(IntEnum):
    DEF = 0        # Standard FF7 encoding with FF terminator
    NOFF_TERM = 1  # No FF terminator in file
    RGB = 2        # RGB encoded (ASCII + 0x73)
    UNICODE = 3    # Windows Unicode strings
    FFPADDED = 4   # FF7 encoding padded with FF bytes
    ZEROTERM = 5   # Zero-terminated string
```

### DEF (Type 0) - Most Common

- Standard FF7 text encoding
- Terminated with `0xFF`
- Uses character map where `0x00` = space, `0x01-0x5F` = ASCII-0x20
- **Handling:** Copy JA bytes directly (with spacing fixes where needed)

### RGB (Type 2) - Keyboard Labels and Save Slots

RGB encoding formula:
```
RGB_byte = FF7_byte + 0x93
         = (ASCII - 0x20) + 0x93
         = ASCII + 0x73
```

- Used for keyboard key labels (indices 77-213)
- Also used for save slot names (indices 649-656)
- **Special handling required** - see RGB encoding document

### UNICODE (Type 3) - Name Entry Characters

- Windows UTF-16-LE encoding
- Used for character name entry screen (indices 461-528)
- **Skipped entirely** - these are the A-Z, あ-ん characters on the naming keyboard

### FFPADDED (Type 4) - Chocobo Race Ordinals

- Like DEF but padded with `0xFF` bytes
- Used for race results: 1st, 2nd, 3rd, etc. (indices 687-711)
- **Skipped** - these should stay in English

### ZEROTERM (Type 5) - Jockey Names

- Standard C-style null-terminated strings
- Used for chocobo jockey names (indices 712-757)
- **Skipped** - names should stay in English

---

## 4. Skip Regions Configuration

The script defines several skip regions to avoid patching problematic areas:

```python
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry characters (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals (FFPADDED)
SKIP_REGIONS.update(range(712, 758))   # Jockey names (ZEROTERM)

# RGB regions that produce identical/garbage output
RGB_SKIP_REGIONS = set(range(658, 687))  # Post-save: "00'00\"000", "SURF", etc.
```

### Why These Are Skipped

| Index Range | Content | Reason |
|-------------|---------|--------|
| 461-528 | A-Z, あ-ん name entry chars | UNICODE type, naming keyboard |
| 658-686 | Time formats, "SURF", scores | EN/JA identical, no change needed |
| 687-711 | 1st, 2nd, 3rd... | Race ordinals, keep English |
| 712-757 | Joe, Teioh, etc. | Jockey names, keep English |

---

## 5. Keyboard Region Handling (+0x20 Offset)

See `keyboard_offset_solution.md` for complete details.

```python
KEYBOARD_REGION = set(range(77, 214))  # Keyboard labels (indices 77-213)

def apply_keyboard_offset(data: bytes) -> bytes:
    """Add +0x20 to compensate for game's -0x20 transformation."""
    result = bytearray()
    for byte in data:
        if byte == 0x00 or byte == 0xFF:
            result.append(byte)  # Keep terminators
        elif byte <= 0xDF:
            result.append(byte + 0x20)  # Add offset
        else:
            result.append(byte)  # Avoid overflow
    return bytes(result)
```

---

## 6. Save Slot Spacing

Save slots need extra trailing spaces for cursor alignment:

```python
SAVE_SLOT_REGION = set(range(647, 657))  # Save 1-10

def add_save_slot_spacing(data: bytes, target_length: int) -> bytes:
    JAFONT1_SPACE = 0x3F  # Position 63 = ideographic space (　)

    result = bytearray()
    for b in data:
        if b == 0xFF:
            break
        result.append(b)

    # Add up to 2 spaces for alignment
    spaces_to_add = min(2, target_length - len(result) - 1)
    for _ in range(spaces_to_add):
        result.append(JAFONT1_SPACE)

    result.append(0xFF)  # Terminator
    # Pad rest with 0x00
    while len(result) < target_length:
        result.append(0x00)

    return bytes(result[:target_length])
```

---

## 7. Shop Menu Spacing

The shop menu "Buy Sell Exit" needs manual spacing reconstruction:

```python
SHOP_MENU_INDEX = 572

def fix_shop_menu_spacing(data: bytes, target_length: int) -> bytes:
    JAFONT1_SPACE = 0x3F

    # Manually construct: かう + 2 spaces + うる + 3 spaces + でる + terminator
    result = bytearray([
        0x4B, 0x69,                     # かう
        JAFONT1_SPACE, JAFONT1_SPACE,   # 2 spaces
        0x69, 0x8B,                     # うる
        JAFONT1_SPACE, JAFONT1_SPACE, JAFONT1_SPACE,  # 3 spaces
        0x25, 0x8B,                     # でる
        0xFF                            # terminator
    ])
    # ... padding to target_length
```

---

## 8. Item/Materia Column Spacing

Similar spacing fix for column headers:

```python
ITEM_MATERIA_INDEX = 578

def fix_item_materia_spacing(data: bytes, target_length: int) -> bytes:
    # EN has: Item[6sp]Materia
    # JA needs: アイテム[4sp]マテリア
    result = bytearray([
        0x6A, 0x6C, 0x64, 0x80,         # アイテム
        JAFONT1_SPACE, JAFONT1_SPACE,   # 4 spaces
        JAFONT1_SPACE, JAFONT1_SPACE,
        0x7C, 0x64, 0x88, 0x6A,         # マテリア
        0xFF                            # terminator
    ])
```

---

## 9. Virtual Address Calculation

HEXT patches target Virtual Addresses, not file offsets:

```python
def file_offset_to_va(file_offset: int) -> int:
    """Convert file offset to Virtual Address for HEXT."""
    return (file_offset - 0x3B8A00) + 0x3BA000 + 0x400000
```

### Formula Breakdown

| Component | Value | Description |
|-----------|-------|-------------|
| `-0x3B8A00` | Section file offset | Where .rdata section starts in file |
| `+0x3BA000` | Section VA | Where .rdata is loaded in memory |
| `+0x400000` | Image base | Default PE image base |

Example:
- EN offset: `0x518370`
- VA = `(0x518370 - 0x3B8A00) + 0x3BA000 + 0x400000`
- VA = `0x15F970 + 0x3BA000 + 0x400000`
- VA = `0x919970`

---

## 10. Output Format

The generated HEXT file follows this format:

```
# Comment with EN -> JA text
# EN offset, JA offset info
XXXXXX = AA BB CC DD FF 00 00
```

Example from actual output:
```
# Do you want to quit -> ファイナルファンタジー７の
# EN: 0x00518370 (30 bytes)
# JA: 0x00518F70
919970 = 44 A4 6C 72 8A 44 A4 98 5E 16 D0 3A 7B FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

---

## 11. Complete Processing Flow

```
1. Load offset table (EN_OFFSETS, STRING_LENGTHS, STRING_TYPES)
2. Load character map for decoding display text
3. For each string index:
   a. Check if in SKIP_REGIONS -> skip
   b. Check if in RGB_SKIP_REGIONS -> skip
   c. Calculate ja_offset = en_offset + JA_OFFSET_DELTA
   d. Read en_bytes and ja_bytes
   e. Based on string type:
      - RGB + KEYBOARD_REGION: apply_keyboard_offset(ja_bytes)
      - RGB + SAVE_SLOT: add_save_slot_spacing(ja_bytes)
      - RGB + other: encode_rgb(en_bytes) [keep EN text as RGB]
      - DEF + KEYBOARD_REGION: apply_keyboard_offset(ja_bytes)
      - DEF + SAVE_SLOT: add_save_slot_spacing(ja_bytes)
      - DEF + SHOP_MENU: fix_shop_menu_spacing()
      - DEF + ITEM_MATERIA: fix_item_materia_spacing()
      - DEF + other: copy ja_bytes directly
      - UNICODE: copy ja_bytes directly
   f. Skip if patch_bytes == en_bytes (no change needed)
   g. Append to patches list
4. Write HEXT file with VA = file_offset_to_va(en_offset)
```

---

## 12. Key Takeaways for German Adaptation

1. **No consistent offset delta** - German requires anchor-based matching
2. **Same string types apply** - DEF, RGB, UNICODE, etc.
3. **Same skip regions** - Name entry, jockeys, ordinals
4. **Keyboard handling may differ** - German uses ö, ä, ü instead of Japanese
5. **Spacing fixes may differ** - German word lengths differ from both EN and JA
6. **VA calculation is identical** - Same formula applies for any language
7. **Character encoding differs** - German needs 0x6A (ö), 0x7A (ü), 0x7F (Ü), 0x7E (ß)

# FF7 German Executable Region Analysis

**Created:** 2026-01-06 16:30 JST (Monday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-ID:** (current session)

## Executive Summary

The region 0x58FBB0 - 0x59E000 in ff7_de.exe contains **multiple distinct data types**, not just menu strings. This document provides a comprehensive analysis of each data type, their byte-level signatures, and detection logic.

---

## Region Overview

| Region # | Start Offset | End Offset | Type | Description |
|----------|-------------|------------|------|-------------|
| 1 | 0x58FBB0 | 0x595B93 | Menu Text | Valid German FF7-encoded strings |
| 2 | 0x595B94 | 0x5969E3 | UI Coordinates | 16-bit coordinate pairs, multiple 0xFF bytes |
| 3 | 0x5969E4 | 0x5981E7 | Mixed Text/Tables | Menu strings with some table headers |
| 4 | 0x5981E8 | 0x5985C7 | Binary Data | High-byte graphics/tile data |
| 5 | 0x5985C8 | 0x598EB0 | Character Structs | Character stats + embedded names |
| 6 | 0x598EB1 | 0x59C157 | Menu Text | Valid German FF7-encoded strings |
| 7 | 0x59C158 | 0x59C35F | Binary Tables | UI layout/coordinate tables |
| 8 | 0x59C360 | 0x59D155 | Menu Text | Save/load menu strings |
| 9 | 0x59D156 | 0x59DFFF | Developer Data | Debug paths + garbage data |

---

## Detailed Region Analysis

### Region 1: Primary Menu Text (0x58FBB0 - 0x595B93)

**Purpose:** Core German menu strings

**Characteristics:**
- FF7-encoded text: byte + 0x20 = ASCII for printable chars (0x01-0x5F)
- Special German characters:
  - 0x6A = 'a' (lowercase umlaut a)
  - 0x7A = 'o' (lowercase umlaut o)
  - 0x7F = 'u' (lowercase umlaut u)
  - 0x66 = 'U' (uppercase umlaut U)
  - 0x7E = 'ss' (sharp s/eszett)
- Single 0xFF terminator per string
- Often right-padded with leading 0x00 bytes

**Example Raw Bytes:**
```
Offset 0x58FBB0: 2d 7a 43 48 54 45 4e 00 33 49 45 00 26 49 4e 41 4c 00 ff
Decoded: "Mochten Sie Final" (with umlaut on o)
```

**Detection Pattern:**
```python
def is_valid_menu_text(raw_bytes):
    # Single 0xFF terminator (not multiple consecutive)
    ff_count = 0
    for i in range(len(raw_bytes) - 1):
        if raw_bytes[i] == 0xFF and raw_bytes[i+1] == 0xFF:
            return False  # Multiple 0xFF = not text

    # Most bytes should be in valid FF7 range
    valid_bytes = sum(1 for b in raw_bytes if 0x01 <= b <= 0x7F or b == 0x00)
    return valid_bytes / len(raw_bytes) > 0.8
```

---

### Region 2: UI Coordinate Tables (0x595B94 - 0x5969E3)

**Purpose:** Menu positioning/layout data

**Characteristics:**
- 16-bit little-endian coordinate pairs (e.g., `32 00 32 00` = 50, 50)
- **MULTIPLE consecutive 0xFF bytes** (3-8+ in a row)
- Low bytes followed by high byte patterns
- When decoded as text, produces garbage like "R R 3 1P", "T T 3!1T"

**Raw Byte Pattern:**
```
Offset 0x595B94: 32 00 32 00 13 00 11 30 ff ff ff ff ff ff ff ff 00 00 ff ff
                 ^coord^ ^coord^       ^^^^^^^^ multiple FFs ^^^^^^^
```

**Detection Pattern:**
```python
def is_ui_coordinate_data(raw_bytes):
    # Check for multiple consecutive 0xFF (3+)
    for i in range(len(raw_bytes) - 2):
        if raw_bytes[i] == 0xFF and raw_bytes[i+1] == 0xFF and raw_bytes[i+2] == 0xFF:
            return True
    return False
```

**CSV Index Range:** Approximately 245-581

---

### Region 3: Mixed Text and Tables (0x5969E4 - 0x5981E7)

**Purpose:** Menu strings interspersed with some table data

**Characteristics:**
- Valid German strings like "Hitze", "Kalte", "Gewitter", "Erde"
- Some status effect names and battle text
- Generally same format as Region 1

---

### Region 4: Binary/Graphics Data (0x5981E8 - 0x5985C7)

**Purpose:** Tile/graphics configuration data (NOT text)

**Characteristics:**
- Very high concentration of bytes >= 0x80
- Multiple 0xFF bytes throughout
- When FF7-decoded, produces single accented chars: "ai", "a", "i", "ei"
- These are likely font glyph references or tile indices

**Raw Byte Pattern:**
```
Offset 0x5981E8: cf 3a a6 aa 6c c6 e9 ff ff ef 6a ca aa cc a3 fc
                 ^^^^^^^^^^^^^^^^^^^^^^^^ high bytes ^^^^^^^^^^^^^
```

**Detection Pattern:**
```python
def is_binary_graphics_data(raw_bytes):
    high_byte_count = sum(1 for b in raw_bytes if b >= 0x80)
    ff_count = sum(1 for b in raw_bytes if b == 0xFF)

    # High bytes dominate AND multiple 0xFF
    return (high_byte_count / len(raw_bytes) > 0.5) and ff_count >= 2
```

**CSV Index Range:** Approximately 778-846

---

### Region 5: Character Stat Structures (0x5985C8 - 0x598EB0)

**Purpose:** Character data with embedded names

**Structure Format (per character):**
```
[Header: ~20-30 bytes] [FF7-encoded name] [0xFF terminator] [padding to boundary]
```

**Example:**
```
Offset 0x598628: 23 4c 4f 55 44 ff 00 00 00 00 00 00
                 ^^^^^^^^^^^^^^ FF7 name  ^^ term  ^^^^^ padding
                 = "CLOUD" (0x23='C', 0x4C='L', etc.)
```

**Extracted Character Names:**
| Offset | Raw Hex | Decoded Name |
|--------|---------|--------------|
| 0x598628 | 23 4C 4F 55 44 | Cloud |
| 0x598634 | 22 41 52 52 45 54 | Barret |
| 0x598640 | 34 49 46 41 | Tifa |
| 0x59864C | 21 45 52 49 53 | Aeris |
| 0x598658 | 32 45 44 00 38 29 29 29 | Red XIII |
| 0x598664 | 39 55 46 46 49 45 | Yuffie |
| 0x598670 | 23 41 49 54 00 33 49 54 48 | Cait Sith |
| 0x59867C | 36 49 4E 43 45 4E 54 | Vincent |
| 0x598688 | 23 49 44 | Cid |
| 0x598694 | 23 48 4F 43 4F | Choco |

**Detection Pattern:**
```python
def is_character_struct(offset, raw_bytes):
    # Check if in character struct region
    if 0x5985C8 <= offset <= 0x598EB0:
        # Contains mostly structural data with embedded name
        # Look for header bytes followed by valid name
        return True
    return False

def extract_name_from_struct(raw_bytes):
    # Find the longest valid FF7-encoded sequence ending in 0xFF
    best_name = ""
    for start in range(len(raw_bytes)):
        for end in range(start + 1, min(start + 20, len(raw_bytes))):
            if raw_bytes[end] == 0xFF:
                name_bytes = raw_bytes[start:end]
                if all(0x01 <= b <= 0x5F or b == 0x00 for b in name_bytes):
                    decoded = ''.join(chr(b + 0x20) if 0x01 <= b <= 0x5F else ' ' for b in name_bytes)
                    if len(decoded.strip()) > len(best_name):
                        best_name = decoded.strip()
                break
    return best_name
```

---

### Region 6: Secondary Menu Text (0x598EB1 - 0x59C157)

**Purpose:** More menu strings - materia, shop, battle text

**Characteristics:** Same as Region 1

**Notable Strings:**
- "Magic Materia!", "Summon Materia!"
- "Kaufen", "Verkaufen", "Beenden"
- Status effects, element names

---

### Region 7: Binary Layout Tables (0x59C158 - 0x59C35F)

**Purpose:** UI layout configuration

**Characteristics:**
- Coordinate-like patterns
- Contains values like `40 3F`, `40 6E` (addresses or positions)
- Not human-readable text

---

### Region 8: Save/Load Menu Text (0x59C360 - 0x59D155)

**Purpose:** Save game dialog strings

**Notable Strings:**
- "Wahlen Sie eine Speicherdatei aus."
- "STECKPLATZ 1", "STECKPLATZ 2"
- "Bin am Laden. Bitte warten"
- "Spielstand 1" through "Spielstand 10"

---

### Region 9: Developer Debug Data (0x59D156 - 0x59DFFF)

**Purpose:** Debug paths and miscellaneous garbage

**Identified Strings:**
```
0x59D168: "C:\FF7\src\menu\German\loadmenu.cpp"
0x59D18C: "C:\FF7\src\menu\German\loadmenu.cpp"
0x59D1B8: "%ssave/save%02d.ff7"
0x59D1CC: "%ssave/save%02d.ff7"
```

**Characteristics:**
- Plain ASCII (NOT FF7-encoded)
- Contains Windows file paths with backslashes
- Contains printf-style format strings
- When FF7-decoded, produces garbage like "|ffW|src|men|german|"

**Detection Pattern:**
```python
def is_developer_path(raw_bytes):
    # Check for ASCII path patterns
    try:
        text = raw_bytes.decode('latin-1')
        if ':\\' in text or '.cpp' in text or '.c' in text:
            return True
        if '%s' in text or '%0' in text:  # printf patterns
            return True
    except:
        pass
    return False
```

---

## Single Character/Empty Entry Detection

Throughout the data, there are many entries that decode to single accented characters or empty strings:

**Examples:**
- Index 110, 147, etc.: "a" (single umlaut a)
- Various entries: "u", "i", "ei"

**Detection:**
```python
def is_garbage_single_char(decoded_text):
    text = decoded_text.strip()
    if len(text) <= 2:
        # Check if only special/accented chars
        special_chars = {'a', 'o', 'u', 'U', 'ss', 'a', 'e', 'a', 'o', 'i', 'e', 'i', 'n', 'o'}
        return all(c in special_chars for c in text)
    return False
```

---

## Comprehensive Classification Function

```python
def categorize_entry(raw_bytes: bytes, offset: int, decoded_text: str) -> str:
    """
    Categorize an extracted entry into its true data type.

    Returns one of:
    - 'menu_text': Valid German menu string
    - 'ui_coords': UI coordinate/positioning data
    - 'binary_data': Graphics/tile binary data
    - 'char_struct': Character stat structure (may contain extractable name)
    - 'developer': Debug paths and format strings
    - 'table_header': Menu table with embedded strings
    - 'empty': Single char or empty garbage
    """

    # 1. Check for multiple consecutive 0xFF (UI coords indicator)
    for i in range(len(raw_bytes) - 2):
        if raw_bytes[i:i+3] == b'\xff\xff\xff':
            return 'ui_coords'

    # 2. Check for high-byte concentration (binary data)
    high_bytes = sum(1 for b in raw_bytes if b >= 0x80)
    if len(raw_bytes) > 5 and high_bytes / len(raw_bytes) > 0.4:
        return 'binary_data'

    # 3. Check for developer paths (ASCII with path chars)
    if b':\\' in raw_bytes or b'.cpp' in raw_bytes or b'.c\x00' in raw_bytes:
        return 'developer'
    if b'%s' in raw_bytes or b'%0' in raw_bytes:
        return 'developer'

    # 4. Check character struct region
    if 0x5985C8 <= offset <= 0x598EB0:
        return 'char_struct'

    # 5. Check for empty/single char garbage
    if len(decoded_text.strip()) <= 2:
        letter_count = sum(1 for c in decoded_text if c.isalpha())
        if letter_count <= 1:
            return 'empty'

    # 6. Check for menu table headers (large with embedded strings)
    if len(raw_bytes) > 100 and raw_bytes.count(b'\xff') > 5:
        return 'table_header'

    # 7. Check for valid menu text
    if len(decoded_text.strip()) >= 2:
        letter_count = sum(1 for c in decoded_text if c.isalpha())
        if letter_count >= 2 or len(decoded_text.strip()) < 10:
            return 'menu_text'

    return 'unknown'
```

---

## Summary Statistics

Based on the current extraction (1152 entries):

| Category | Count | Percentage |
|----------|-------|------------|
| Clean Menu Text | ~600 | 52% |
| UI Coordinate Data | ~400 | 35% |
| Binary/Graphics Data | ~70 | 6% |
| Character Structs | ~40 | 3% |
| Developer Debug | ~15 | 1% |
| Empty/Garbage | ~30 | 3% |

---

## Recommendations

1. **Filter out UI coordinate entries** by checking for 3+ consecutive 0xFF bytes
2. **Filter out binary data** by checking high-byte concentration
3. **Extract character names** from struct region using name-finding logic
4. **Preserve developer paths** as historical/debugging interest
5. **Mark empty entries** and exclude from main text output

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-06 | 1.0.0 | Initial comprehensive region analysis |

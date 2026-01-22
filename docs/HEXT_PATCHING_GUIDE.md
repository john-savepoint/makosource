# HEXT Patching Guide for FF7 Japanese Menu Text

**Created:** 2025-12-05 00:35 JST (Friday)
**Last Modified:** 2025-12-05 00:35 JST (Friday)
**Version:** 1.0.0
**Session-ID:** c245e7c0-ec73-4933-b925-5976860e742c

---

## What is HEXT?

HEXT (Hex Text) is a simple file format for runtime memory patching. FFNx loads HEXT files at startup and modifies the game executable in memory, allowing us to change hardcoded text without modifying the actual EXE file.

---

## HEXT File Format

```
# Comments start with #
# Blank lines are ignored

# Format: ADDRESS = BYTE BYTE BYTE ...
91A8C0 = 6A 6C 64 80 FF
```

- **ADDRESS:** Virtual memory address in hexadecimal (no 0x prefix)
- **BYTES:** Space-separated hexadecimal values
- Addresses are case-insensitive
- Comments can be on their own line or after the bytes (some parsers)

---

## HEXT File Location

**Critical:** The folder changes based on `ff7_japanese_edition` setting!

| Setting | HEXT Path |
|---------|-----------|
| `ff7_japanese_edition = true` | `hext/ff7/ja/*.txt` |
| `ff7_japanese_edition = false` | `hext/ff7/en/*.txt` |

This is defined in FFNx source `cfg.cpp` lines 352-354.

---

## Step-by-Step: Creating a New Patch

### Step 1: Find the English String

Use `xxd` to search the English executable for the text pattern.

**FF7 English Text Encoding:**
| Letter | Hex | Letter | Hex | Letter | Hex |
|--------|-----|--------|-----|--------|-----|
| A | 21 | J | 2A | S | 33 |
| B | 22 | K | 2B | T | 34 |
| C | 23 | L | 2C | U | 35 |
| D | 24 | M | 2D | V | 36 |
| E | 25 | N | 2E | W | 37 |
| F | 26 | O | 2F | X | 38 |
| G | 27 | P | 30 | Y | 39 |
| H | 28 | Q | 31 | Z | 3A |
| I | 29 | R | 32 | Space | 00 |
| | | | | Term. | FF |

**Example: Finding "CONFIG"**
```
C=23, O=4F, N=2E, F=26, I=29, G=27
Pattern: 23 4F 4E 46 49 47
```

Wait - that's wrong! FF7 uses offset encoding where A=0x21, not ASCII. Let me recalculate:
```
C = 0x21 + 2 = 0x23
O = 0x21 + 14 = 0x2F
N = 0x21 + 13 = 0x2E
F = 0x21 + 5 = 0x26
I = 0x21 + 8 = 0x29
G = 0x21 + 6 = 0x27
Pattern: 23 2F 2E 26 29 27
```

**Search command:**
```bash
xxd "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe" | grep "232f 2e26 2927"
```

**Alternative - search for "CONFIG" with spacing:**
```bash
xxd "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe" | grep "234f 4e46 4947"
```

Note: The exact encoding varies. Use xxd output to see the actual bytes at known addresses.

### Step 2: Get the File Offset

From the xxd output, the first column shows the file offset:
```
0051934c: 234f 4e46 4947 ff00 ...
          ^^^^^^^^^^^^^^^^
          This is "CONFIG" + terminator
```
File offset = `0x51934c`

### Step 3: Calculate Virtual Address

FF7's menu strings are in the `.data` section. Use this formula:

```
VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000
```

**PE Section Reference for ff7_en.exe:**
| Section | Virtual Address | Raw (File) Address |
|---------|-----------------|-------------------|
| .text | 0x00001000 | 0x00000400 |
| .rdata | 0x003B6000 | 0x003B4C00 |
| .data | 0x003BA000 | 0x003B8A00 |

**Example calculation:**
```python
file_offset = 0x51934c
va = (file_offset - 0x3B8A00) + 0x3BA000 + 0x400000
# va = (0x51934c - 0x3B8A00) + 0x3BA000 + 0x400000
# va = 0x16094C + 0x3BA000 + 0x400000
# va = 0x91A94C
```

### Step 4: Find the Japanese Translation

Check the actual Japanese executable to see what text it uses:

```bash
# Search Japanese exe for similar context
xxd "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe" | grep "5298 44a6"
```

Or examine the area around the Japanese menu strings (usually offset by a constant from English).

### Step 5: Convert Japanese Text to FF7 Bytes

Use the character mapping CSV to encode Japanese text.

**Character Map Location:**
```
docs/character_maps/ff7_complete_mapping_compact.csv
```

**Encoding Rules:**
- jafont_1 (index 0-255): Single byte
- jafont_2: FA + index
- jafont_3: FB + index
- jafont_4: FC + index
- jafont_5: FD + index
- jafont_6: FE + index
- String terminator: FF

**Python helper script:**
```python
import csv

char_to_bytes = {}
with open('docs/character_maps/ff7_complete_mapping_compact.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        texture = row['texture']
        index = int(row['index'])
        char = row['character']

        if texture == 'jafont_1':
            char_to_bytes[char] = [index]
        elif texture == 'jafont_2':
            char_to_bytes[char] = [0xFA, index]
        elif texture == 'jafont_3':
            char_to_bytes[char] = [0xFB, index]
        elif texture == 'jafont_4':
            char_to_bytes[char] = [0xFC, index]
        elif texture == 'jafont_5':
            char_to_bytes[char] = [0xFD, index]
        elif texture == 'jafont_6':
            char_to_bytes[char] = [0xFE, index]

def encode_japanese(text):
    """Convert Japanese text to FF7 byte string"""
    result = []
    for char in text:
        if char in char_to_bytes:
            result.extend(char_to_bytes[char])
        else:
            print(f"Warning: '{char}' not found in character map")
    result.append(0xFF)  # Add terminator
    return ' '.join(f'{b:02X}' for b in result)

# Example usage
print(encode_japanese('コンフィグ'))  # Output: 52 98 44 A6 0E FF
```

### Step 6: Create the HEXT Patch

```
# CONFIG (コンフィグ) - 6 bytes, original 7
# File offset 0x51934c -> VA 0x91A94C
91A94C = 52 98 44 A6 0E FF 00
```

**Important:** If your Japanese text is shorter than the original English, pad with `00` bytes to avoid leftover characters.

### Step 7: Test the Patch

1. Save the HEXT file to `hext/ff7/ja/japanese_menu.txt`
2. Launch the game
3. Check FFNx.log for: `Applied Hext patch: hext/ff7/ja\japanese_menu.txt`
4. Verify the text displays correctly in-game

---

## Common Mistakes

### 1. Using File Offset Instead of Virtual Address
❌ `51934c = 52 98 44 A6 0E FF`
✅ `91A94C = 52 98 44 A6 0E FF`

### 2. Wrong Folder (en vs ja)
When `ff7_japanese_edition = true`, HEXT files MUST be in `/ja/` folder.

### 3. Forgetting the Terminator
All strings must end with `FF`.

### 4. Not Padding Short Strings
If "CONFIG" (7 bytes) becomes "コンフィグ" (6 bytes), you need:
```
91A94C = 52 98 44 A6 0E FF 00   <- Note the 00 padding
```

### 5. Using Wrong Encoding
Don't use ASCII or UTF-8. FF7 has its own text encoding system.

---

## Fullwidth English Characters

The Japanese version sometimes uses fullwidth English letters (Ａ-Ｚ) instead of katakana.

**Fullwidth alphabet in jafont_1:**
| Letter | Index (Hex) | Letter | Index (Hex) |
|--------|-------------|--------|-------------|
| Ａ | B4 | Ｎ | C1 |
| Ｂ | B5 | Ｏ | C2 |
| Ｃ | B6 | Ｐ | C3 |
| Ｄ | B7 | Ｑ | C4 |
| Ｅ | B8 | Ｒ | C5 |
| Ｆ | B9 | Ｓ | C6 |
| Ｇ | BA | Ｔ | C7 |
| Ｈ | BB | Ｕ | C8 |
| Ｉ | BC | Ｖ | C9 |
| Ｊ | BD | Ｗ | CA |
| Ｋ | BE | Ｘ | CB |
| Ｌ | BF | Ｙ | CC |
| Ｍ | C0 | Ｚ | CD |

**Example:** "NEW GAME" in Japanese version = `C1 B8 CA 3F BA B4 C0 B8 FF`
(ＮＥＷ　ＧＡＭＥ with 3F as space)

---

## Debugging

### Check if HEXT is loading
```bash
grep -i "hext" "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/FFNx.log"
```

Expected output:
```
TRACE: Applied Hext patch: hext/ff7/ja\japanese_menu.txt
```

### Verify addresses
Use a hex editor or debugger to confirm the bytes at the virtual address match what you expect.

### Test with simple patch first
Before encoding Japanese, test with a simple ASCII change:
```
# Change ITEM to TEST
91A8C0 = 34 45 53 54 FF
```
If "ITEM" becomes garbage, your address is correct but being rendered with Japanese font. If "ITEM" doesn't change, the address is wrong.

---

## Reference

- **FFNx HEXT implementation:** `FFNx-PR737/src/hext.cpp`
- **Path configuration:** `FFNx-PR737/src/cfg.cpp` (lines 352-359)
- **Character map:** `docs/character_maps/ff7_complete_mapping_compact.csv`
- **Address calculations:** See `MENU_TEXT_ADDRESS_MAP.md`

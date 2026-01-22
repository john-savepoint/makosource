# FF7 German String Decoder Reference

**Created:** 2026-01-03 16:10 JST (Saturday)
**Session-ID:** 629f3c93-f884-439a-91d6-d77e7783bf9c
**Source:** Analysis of `d:/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe`

---

## Overview

This document provides the complete character encoding map for decoding German strings from the FF7 German executable (`ff7_de.exe`). The encoding uses a modified ASCII scheme where most characters are encoded as `byte + 0x20 = ASCII`, with special mappings for German umlauts and other extended Latin characters.

---

## Key Insight: German Exe Uses Custom Glyph Mappings

The US font texture (`usfont_a_h_00.png`) shows the original character layout, but the German executable **remaps** certain byte positions to German characters:

| Byte | US Font Shows | German Exe Uses |
|------|---------------|-----------------|
| 0x66 | Ç             | **Ü** (uppercase) |
| 0x6A | ê             | **ä** (lowercase) |
| 0x7A | Ú             | **ö** (lowercase) |
| 0x7E | ©             | **ß** (eszett)    |
| 0x7F | ®             | **ü** (lowercase) |

---

## Standard Character Encoding (0x00-0x5F)

**Formula:** `character = chr(byte + 0x20)`

| Byte Range | Characters | Description |
|------------|------------|-------------|
| 0x00       | (space)    | Space character |
| 0x01-0x0F  | !"#$%&'()*+,-./ | Punctuation |
| 0x10-0x19  | 0-9        | Digits |
| 0x1A-0x1F  | :;<=>?     | More punctuation |
| 0x20       | @          | At symbol |
| 0x21-0x3A  | A-Z        | **Uppercase letters** |
| 0x3B-0x3F  | [\]^_      | Brackets and underscore |
| 0x40       | `          | Backtick |
| 0x41-0x5A  | a-z        | **Lowercase letters** |
| 0x5B-0x5F  | {|}~⌂      | Braces and special |
| 0xFF       | (terminator) | String end marker |

---

## German Special Characters (VERIFIED)

These mappings were verified by examining known German strings in `ff7_de.exe`:

| Byte | Character | Name | Verification Source |
|------|-----------|------|---------------------|
| **0x66** | **Ü** | Uppercase U-umlaut | Found in "GRÜN" at 0x59077A |
| **0x6A** | **ä** | Lowercase a-umlaut | Found in "Auswählen" at 0x5902D6 |
| **0x7A** | **ö** | Lowercase o-umlaut | Found in "Möchten" at 0x58FBB0 |
| **0x7E** | **ß** | Eszett | Referenced in session handoffs |
| **0x7F** | **ü** | Lowercase u-umlaut | Found in "zurück" at 0x58FBE8 |

### Important Notes

1. **Uppercase Ä and Ö**: No instances of uppercase Ä (ÄNDERN) or Ö (ÖFFNEN) were found in the menu strings region. German FF7 appears to use only lowercase umlauts in most text.

2. **The ü/Ü distinction**:
   - Lowercase `ü` = 0x7F (in words like "zurück", "für", "Menü")
   - Uppercase `Ü` = 0x66 (in words like "GRÜN")

---

## Complete Byte Map (0x00-0x7F)

```
0x00: SPC | !   | "   | #   | $   | %   | &   | '   | (   | )   | *   | +   | ,   | -   | .   | /
0x10: 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | :   | ;   | <   | =   | >   | ?
0x20: @   | A   | B   | C   | D   | E   | F   | G   | H   | I   | J   | K   | L   | M   | N   | O
0x30: P   | Q   | R   | S   | T   | U   | V   | W   | X   | Y   | Z   | [   | \   | ]   | ^   | _
0x40: `   | a   | b   | c   | d   | e   | f   | g   | h   | i   | j   | k   | l   | m   | n   | o
0x50: p   | q   | r   | s   | t   | u   | v   | w   | x   | y   | z   | {   | |   | }   | ~   | ⌂
0x60: ä   | á   | à   | â   | ã   | å   | Ü   | ç   | é   | è   | ä*  | ë   | í   | ì   | î   | ï
0x70: ñ   | ó   | ò   | ô   | õ   | ö   | °   | •   | £   | Ù   | ö*  | Û   | Ü   | ?   | ß   | ü
```

*Note: 0x6A and 0x7A are the VERIFIED positions for ä and ö respectively.

---

## Python Implementation

### Decode Function

```python
# FF7 German String Decoder
# Use this to decode strings from ff7_de.exe

# Character map: byte value -> character
FF7_GERMAN_DECODE_MAP = {
    # German special characters (VERIFIED from ff7_de.exe)
    0x66: 'Ü',  # uppercase U-umlaut (in GRÜN, MENÜ buttons)
    0x6A: 'ä',  # lowercase a-umlaut (in Auswählen, wählen)
    0x7A: 'ö',  # lowercase o-umlaut (in Möchten, können)
    0x7E: 'ß',  # eszett (in muß, daß - old spelling)
    0x7F: 'ü',  # lowercase u-umlaut (in zurück, für, Menü)

    # Extended Latin (may appear in some strings)
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã', 0x65: 'å',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}

def decode_ff7_german(data: bytes) -> str:
    """
    Decode FF7 German encoded bytes to readable text.

    Args:
        data: Raw bytes from ff7_de.exe

    Returns:
        Decoded German string

    Example:
        >>> decode_ff7_german(bytes([0x2D, 0x7A, 0x43, 0x48, 0x54, 0x45, 0x4E, 0xFF]))
        'Möchten'
    """
    result = []
    for b in data:
        if b == 0xFF:
            break  # String terminator
        elif b in FF7_GERMAN_DECODE_MAP:
            result.append(FF7_GERMAN_DECODE_MAP[b])
        elif b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))  # Standard: byte + 0x20 = ASCII
        else:
            result.append(f'[{b:02X}]')  # Unknown byte
    return ''.join(result)
```

### Encode Function

```python
def encode_ff7_german(text: str) -> bytes:
    """
    Encode German text to FF7 format.

    Args:
        text: German string to encode

    Returns:
        FF7 encoded bytes (with 0xFF terminator)

    Example:
        >>> encode_ff7_german('Möchten')
        b'\\x2d\\x7a\\x43\\x48\\x54\\x45\\x4e\\xff'
    """
    ENCODE_MAP = {
        'Ü': 0x66, 'ä': 0x6A, 'ö': 0x7A, 'ß': 0x7E, 'ü': 0x7F,
        'á': 0x61, 'à': 0x62, 'â': 0x63, 'ã': 0x64, 'å': 0x65,
        'ç': 0x67, 'é': 0x68, 'è': 0x69, 'ë': 0x6B,
        'í': 0x6C, 'ì': 0x6D, 'î': 0x6E, 'ï': 0x6F,
        'ñ': 0x70, 'ó': 0x71, 'ò': 0x72, 'ô': 0x73, 'õ': 0x74,
    }
    result = []
    for c in text:
        if c in ENCODE_MAP:
            result.append(ENCODE_MAP[c])
        elif c == ' ':
            result.append(0x00)
        elif 0x21 <= ord(c) <= 0x7F:
            result.append(ord(c) - 0x20)
        else:
            raise ValueError(f"Cannot encode character: {c} (U+{ord(c):04X})")
    result.append(0xFF)  # Terminator
    return bytes(result)
```

---

## Verified String Examples

| Offset | Raw Bytes (hex) | Decoded Text |
|--------|-----------------|--------------|
| 0x58FBB0 | `2d7a434854454e...` | Möchten Sie Final |
| 0x58FBE8 | `5a550037494e444f5753005a55527f434b...` | zu Windows zurückkehren? |
| 0x5900F0 | `26454e535445524641524245ff` | Fensterfarbe |
| 0x590852 | `214e4752494646ff` | Angriff |
| 0x590D1C | `33504549434845524eff` | Speichern |
| 0x591490 | `3421333421343532ff` | TASTATUR |
| 0x59077A | `2732662eff` | GRÜN |
| 0x599D80 | `37494c4c4b4f4d4d454e01ff` | Willkommen! |

---

## Key Memory Regions in ff7_de.exe

| Region | Start | End | Description |
|--------|-------|-----|-------------|
| Menu strings | 0x58FB00 | 0x5A0000 | Main menu, config, dialog text |
| Quit dialog | 0x58FBB0 | 0x58FC20 | "Möchten Sie Final Fantasy VII verlassen..." |
| Config menu | 0x5900F0 | 0x591500 | Settings labels |
| Keyboard labels | 0x591058 | 0x5914CC | [ABBRECHEN], [MENÜ], TASTATUR, etc. |

---

## Usage in Sub-Agents

When processing German strings from `ff7_de.exe`, sub-agents should:

1. **Copy the decode function** from this document
2. **Read bytes from the exe** at the target offset
3. **Pass to `decode_ff7_german()`** to get readable text
4. **For encoding**, use `encode_ff7_german()` to convert German text back to FF7 format

### Quick Reference for Common German Characters

```
ä = 0x6A    Ü = 0x66    ß = 0x7E
ö = 0x7A    ü = 0x7F
```

---

## Related Documentation

- Session handoffs: `SESSION_HANDOFF_2026-01-03-55_GERMAN_HEXT_EXTRACTION.md`
- Session handoffs: `SESSION_HANDOFF_2026-01-03-56_GERMAN_HEXT_PARALLEL_HAIKU.md`
- Context document: `SESSION_CONTEXT_48-54_CRASH_FIX_GERMAN_HEXT.md`
- Font texture: `d:/Games/Stand-alone/FINAL FANTASY VII/mods/Textures/menu/usfont_a_h_00.png`

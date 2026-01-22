# FF7 German String Extraction - Issue Analysis & Resolution

**Created:** 2026-01-06 16:15 JST (Tuesday)
**Session-ID:** 47cf5a76-efc5-46cc-aa3c-d372f1a897e1
**Author:** John Zealand-Doyle

---

## Executive Summary

The original German menu string extraction (530 strings) missed approximately **180+ strings** due to:

1. **Encoding assumption errors** - Uppercase `Ö` mapped incorrectly
2. **Boundary detection failures** - Binary data regions confused the FF-terminator parser
3. **Region oversight** - Keyboard/joystick strings stored in plain ASCII, not FF7 encoding
4. **Separate memory regions** - Battle items stored in different executable section

---

## Issue #1: Character Encoding Error

### Problem
The extraction script mapped byte `0x65` to `å` (Norwegian/Swedish) instead of `Ö` (German uppercase O-umlaut).

### Evidence
```
Raw bytes at 0x597484: 27 45 53 43 48 57 49 4E 44 49 47 4B 45 49 54 00 00 00 05 28 65 28 25 32
Incorrect decode: "Geschwindigkeit   %HåHER"
Correct decode:   "Geschwindigkeit   %HÖHER" (Speed % HIGHER)
```

### Affected Strings
- `Geschwindigkeit %HÖHER` (Speed % HIGHER)
- `Schutz %HÖHER` (Defense % HIGHER)
- `Zauberkraft %HÖHER` (Magic Power % HIGHER)
- `Glück %HÖHER` (Luck % HIGHER)

### Corrected Character Map
```
0x65 = Ö (uppercase O-umlaut) ← WAS INCORRECTLY å
0x66 = Ü (uppercase U-umlaut)
0x6A = ä (lowercase a-umlaut)
0x7A = ö (lowercase o-umlaut)
0x7E = ß (eszett)
0x7F = ü (lowercase u-umlaut)
```

---

## Issue #2: Boundary Detection Failures

### Problem
FF7's string table is NOT a clean sequence of FF-terminated strings. It contains:
- Binary UI coordinate tables (16-byte records)
- Padding regions (multiple consecutive 0x00 or 0xFF bytes)
- Embedded data structures

The extraction script assumed: `[string][FF][string][FF]...`

Reality: `[string][FF][padding/binary][string][FF][binary][string][FF]...`

### Case Study: STUFE 1 (Level 1)

```
0x59595F: [end of "Limit-Ebene"] FF
0x595960: 00 00 00 00 00 00 00 00           ← 8 bytes padding
0x595968: FF FF FF FF FF FF FF FF           ← 8 bytes 0xFF (looks like terminators!)
0x595970: [88 bytes binary UI data]
0x5959C7: 00                                ← NOT an FF terminator
0x5959C8: 33 34 35 26 25 00 11 FF           ← "STUFE 1" + terminator
```

The 8 consecutive `FF` bytes at 0x595968 confused the parser about string boundaries.

### Missed Due to Boundary Issues
| Offset | Text | Category |
|--------|------|----------|
| 0x5959C8 | STUFE 1 | Limit Break Menu |
| 0x591184 | [ABBRECHEN] | Button Label |
| 0x5911C0 | [MENÜ] | Button Label |
| 0x5911FC | [UMSCHALTEN] | Button Label |
| 0x5912B0 | [KAMERA] | Button Label |
| 0x5912EC | [ZIEL] | Button Label |
| 0x591328 | [HILFE] | Button Label |
| 0x591364 | [START] | Button Label |
| 0x5913A0 | [HERAUF] | Button Label |
| 0x5913DC | [UNTEN] | Button Label |
| 0x591418 | [LINKS] | Button Label |
| 0x591454 | [RECHT] | Button Label |
| 0x5956EE | Auswählen mit [START]-Taste | Party Management |
| 0x597698 | Chocobo treffen | Materia Effect |
| 0x598634 | Barret | Character Name |
| 0x598640 | Tifa | Character Name |
| 0x59864C | Aeris | Character Name |
| 0x598658 | Red XIII | Character Name |
| 0x598664 | Yuffie | Character Name |
| 0x598670 | Cait Sith | Character Name |
| 0x59867C | Vincent | Character Name |
| 0x598688 | Cid | Character Name |
| 0x598694 | Choco | Character Name |

---

## Issue #3: Plain ASCII Keyboard/Joystick Strings

### Problem
Keyboard key names and joystick buttons are stored in **plain ASCII**, not FF7 encoding. The extraction only searched for FF7-encoded strings.

### Location
- **Keyboard Keys:** 0x591A70 - 0x592060 (plain ASCII, null-terminated)
- **Joystick Buttons:** 0x592130 - 0x5921B0 (plain ASCII, null-terminated)

### Evidence
```
Hex dump at 0x591A78:
4B45 494E 4553 0000 4553 4300 3100 0000  KEINES..ESC.1...
3200 0000 3300 0000 3400 0000 3500 0000  2...3...4...5...
```

These are standard C-style null-terminated strings, not FF7's `byte + 0x20` encoding.

### Count
- ~120 keyboard key names (German translations like RÜCKTASTE, EINGABE, LEERTASTE)
- ~10 joystick button names (BUTTON 1-10)

---

## Issue #4: Battle Items in Separate Memory Region

### Problem
Battle arena items and chocobo racing prizes are stored at 0x56F9C0 - 0x56FD00, outside the main menu string table (0x58FBB0 - 0x59E000).

### Evidence
```
Hex dump at 0x56F9C0:
3425 292f 28ff ffff   = "TEIOH" (champion chocobo)

Hex dump at 0x56FAE8:
3350 5249 4e54 5343 4855 4845   = "PRINTSCHUHE" (Sprint Shoes)
```

### Items Found
- TEIOH, PRINTSCHUHE, GEGENANGRIFF, ZAUBERANGRIFF
- SCHLEICHANGRIFF, CHOCO, ARMBAND, ÄTHER, ELIXIER
- HELDENTRANK, BLITZSTRAHLRAUCH, FEUERZAHN
- ANTARKTISCHER WIND, SCHNELLBLITZ, FEUERSCHLEIER
- EISKRISTALL, MEGALIXIER, TURBO, TRANK
- PHÖNIX FEDER, HYPER, BERUHIGUNGSMITTEL, HI-TRANK

---

## Supplementary Files Created

| File | Contents | Count |
|------|----------|-------|
| `german_menu_strings_missed.csv` | Strings missed by original extraction | ~24 |
| `german_keyboard_keys.csv` | Keyboard key names (ASCII) | ~120 |
| `german_joystick_buttons.csv` | Joystick button names (ASCII) | ~10 |
| `german_battle_items.csv` | Battle items/prizes (FF7 encoded) | ~24 |

---

## Recommendations for Future Extraction

### 1. Multi-Pass Scanning
Scan the entire executable, not just expected regions:
- Pass 1: FF7-encoded strings (0x58FBB0 - 0x59E000)
- Pass 2: Plain ASCII strings (0x591000 - 0x593000)
- Pass 3: Battle data region (0x56F000 - 0x570000)

### 2. Smarter Boundary Detection
Don't treat consecutive `0xFF` bytes as multiple terminators. Instead:
```python
# Skip padding regions
while data[i] in (0x00, 0xFF):
    i += 1
# Then look for next valid string start
```

### 3. Validate German Character Map
```python
GERMAN_CHAR_MAP = {
    0x65: 'Ö',  # uppercase O-umlaut (NOT å!)
    0x66: 'Ü',  # uppercase U-umlaut
    0x6A: 'ä',  # lowercase a-umlaut
    0x7A: 'ö',  # lowercase o-umlaut
    0x7E: 'ß',  # eszett
    0x7F: 'ü',  # lowercase u-umlaut
}
```

### 4. Dual Encoding Detection
Check if a region contains:
- FF7 encoding: Look for bytes 0x21-0x5F with 0xFF terminators
- ASCII encoding: Look for bytes 0x20-0x7E with 0x00 terminators

---

## Total String Counts

| Category | Original Extraction | Supplementary | Total |
|----------|---------------------|---------------|-------|
| Menu Strings (FF7 encoded) | 530 | 24 | 554 |
| Keyboard Keys (ASCII) | 0 | ~120 | ~120 |
| Joystick Buttons (ASCII) | 0 | ~10 | ~10 |
| Battle Items (FF7 encoded) | 0 | ~24 | ~24 |
| **Total** | **530** | **~178** | **~708** |

---

## References

- Original extraction: `german_menu_strings.csv` (530 strings)
- Supplementary data: `german_*_supplementary.csv` files
- Memory reference: `FF7_GERMAN_MEMORY_REFERENCE.py`
- Technical findings: `FF7_GERMAN_DATA_FINDINGS_v3.md`

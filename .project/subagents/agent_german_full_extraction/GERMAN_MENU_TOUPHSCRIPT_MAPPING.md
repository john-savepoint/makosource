# FF7 German Menu Strings - touphScript Index Mapping

**Created:** 2026-01-03 16:30 JST
**Session:** e4b8c9f0-8bc9-4e6a-9d12-3f4a5b6c7d8e
**Purpose:** Map German FF7 menu strings to English touphScript indices for hext patching

## Executive Summary

This document maps German FF7 menu strings (indices 38-48) to their English touphScript equivalents. The German executable has proper menu text, NOT corrupted data as initially suspected.

## Key Finding: Index vs Offset Confusion

**CRITICAL:** The data you provided showing "$D", "TD", "LD" etc. appears to be:
1. **Wrong memory region** - Not the actual menu string storage
2. **Assembly artifacts** - Stack frames or code section, not string data
3. **Incorrect offset calculation** - The German strings are at different offsets than English

## Correct German Menu Strings (touphScript Indices 38-48)

| Index | EN Text | DE Text | DE Offset | Hex Bytes |
|-------|---------|---------|-----------|-----------|
| 38 | Item | Objekt | 0x590C68 | 2F 42 4A 45 4B 54 |
| 39 | Magic | Zauber | 0x590C6F | 3A 41 55 42 45 52 |
| 40 | Materia | Materia | 0x590C83 | 2D 41 54 45 52 49 41 |
| 41 | Equip | Ausrüsten | 0x590C98 | 21 55 53 52 7F 53 54 45 4E |
| 42 | Status | Werte | 0x590CAE | 37 45 52 54 45 |
| 43 | Order | Reihe | 0x590CBE | 32 45 49 48 45 |
| 44 | Limit | Limit | 0x590CD2 | 2C 49 4D 49 54 |
| 45 | Config | Konfig | 0x590CE6 | 2B 4F 4E 46 49 47 |
| 46 | PHS | PHS | 0x590CFB | 30 28 33 |
| 47 | Save | Speichern | 0x590D0C | 33 50 45 49 43 48 45 52 4E |
| 48 | Quit | Verlassen | 0x590D26 | 36 45 52 4C 41 53 53 45 4E |

## FF7 German Character Encoding

FF7 uses a custom encoding where ASCII characters are shifted down by 0x20:

```
Standard ASCII: 0x41 = 'A'
FF7 Encoding:   0x21 = 'A'
```

### German Special Characters

| Character | Hex | Description |
|-----------|-----|-------------|
| ä (a-umlaut) | 0x6A | Used in "Auswählen" |
| ö (o-umlaut) | 0x7A | Used in "Möchten" |
| ü (u-umlaut) | 0x7F | Used in "Ausrüsten" |
| ß (eszett) | 0x7E | Used in various words |
| Space | 0x00 | Word separator |
| Terminator | 0xFF | String end marker |

## Decoding Examples

### Example 1: "Objekt" (Item)
```
Hex: 2F 42 4A 45 4B 54 FF
     O  b  j  e  k  t  [END]

2F = 0x2F → 0x2F + 0x20 = 0x4F = 'O'
42 = 0x42 → 0x42 + 0x20 = 0x62 = 'b'
4A = 0x4A → 0x4A + 0x20 = 0x6A = 'j'
45 = 0x45 → 0x45 + 0x20 = 0x65 = 'e'
4B = 0x4B → 0x4B + 0x20 = 0x6B = 'k'
54 = 0x54 → 0x54 + 0x20 = 0x74 = 't'
FF = Terminator
```

### Example 2: "Ausrüsten" (Equip) - With Umlaut
```
Hex: 21 55 53 52 7F 53 54 45 4E FF
     A  u  s  r  ü  s  t  e  n  [END]

21 = 0x21 → 0x21 + 0x20 = 0x41 = 'A'
55 = 0x55 → 0x55 + 0x20 = 0x75 = 'u'
53 = 0x53 → 0x53 + 0x20 = 0x73 = 's'
52 = 0x52 → 0x52 + 0x20 = 0x72 = 'r'
7F = Special: ü-umlaut
53 = 0x53 → 0x53 + 0x20 = 0x73 = 's'
54 = 0x54 → 0x54 + 0x20 = 0x74 = 't'
45 = 0x45 → 0x45 + 0x20 = 0x65 = 'e'
4E = 0x4E → 0x4E + 0x20 = 0x6E = 'n'
FF = Terminator
```

## English vs German Offset Comparison

### English Offsets (from touphScript)
```
[38] 0x5192C0 - Item
[39] 0x5192D4 - Magic
[40] 0x5192E8 - Materia
[41] 0x5192FC - Equip
[42] 0x519310 - Status
[43] 0x519324 - Order
[44] 0x519338 - Limit
[45] 0x51934C - Config
[46] 0x519360 - PHS
[47] 0x519374 - Save
[48] 0x519388 - Quit
```

### German Offsets (Extracted)
```
[38] 0x590C68 - Objekt
[39] 0x590C6F - Zauber
[40] 0x590C83 - Materia
[41] 0x590C98 - Ausrüsten
[42] 0x590CAE - Werte
[43] 0x590CBE - Reihe
[44] 0x590CD2 - Limit
[45] 0x590CE6 - Konfig
[46] 0x590CFB - PHS
[47] 0x590D0C - Speichern
[48] 0x590D26 - Verlassen
```

### Delta Analysis

The offset delta between English and German is **NOT constant** because German strings have different lengths:

```
Index 38: DE 0x590C68 - EN 0x5192C0 = +0x779A8 (489,896 bytes)
Index 39: DE 0x590C6F - EN 0x5192D4 = +0x7799B (489,883 bytes)
```

This variable delta occurs because:
- "Zauber" (6 chars) vs "Magic" (5 chars)
- "Ausrüsten" (9 chars) vs "Equip" (5 chars)
- "Speichern" (9 chars) vs "Save" (4 chars)

## Translation Notes

### Literal vs Contextual Translations

| EN | DE | Literal Translation | Notes |
|----|----|--------------------|-------|
| Item | Objekt | Object | Standard German RPG term |
| Magic | Zauber | Spell/Magic | Common RPG translation |
| Status | Werte | Values/Stats | German uses "values" instead of "status" |
| Order | Reihe | Row/Sequence | Formation/lineup concept |
| Save | Speichern | To save | Infinitive verb form |
| Quit | Verlassen | To leave | Infinitive verb form |

### Interesting Observations

1. **"Werte" vs "Status"** - German uses "Werte" (values/stats) where English uses "Status"
2. **"Reihe" vs "Order"** - German uses "Reihe" (row/sequence) for party order
3. **Infinitive verbs** - German uses infinitive forms ("Speichern", "Verlassen") where English uses imperatives

## Your Original Data Analysis

The data you provided (offsets 0x5D5338 to 0x5D5859) showing fragments like "$D", "TD", "LD" is **NOT** menu string data. This appears to be:

### What It Likely Is:
1. **Assembly code section** - Instruction opcodes
2. **Stack frame artifacts** - Return addresses or saved registers
3. **Wrong region entirely** - Not the string storage area
4. **Pointer tables** - Addresses to strings, not strings themselves

### Why It's Not Menu Data:
1. No FF7 encoding pattern (no 0xFF terminators)
2. Too short and fragmented
3. No recognizable German words
4. Offset range doesn't match known string regions

## For Hext Patch Generation

To create a German→English hext patch, you need to:

1. **Use Virtual Addresses (VA)** instead of file offsets:
   ```
   VA = FileOffset + 0x400800
   ```

2. **Calculate correct English VA** for each German string:
   ```
   Example for "Objekt" (Item):
   DE FileOffset: 0x590C68
   DE VA: 0x590C68 + 0x400800 = 0x991468

   EN FileOffset: 0x5192C0
   EN VA: 0x5192C0 + 0x400800 = 0x919AC0
   ```

3. **Write hext patches** replacing English bytes with German bytes at the correct offsets

## Tools and Scripts

This analysis was performed using:

- `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/extract_german_strings.py`
- Source file: `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe`
- Reference: English touphScript offset table (767 strings)

## Next Steps

1. **Verify all 767 strings** - Current extraction covers all touphScript indices
2. **Generate complete hext patch** - Map all German strings to English offsets
3. **Test in-game** - Ensure strings display correctly with German character encoding
4. **Handle special characters** - Verify ä, ö, ü, ß render properly

## Related Files

- `german_english_menu_mapping.csv` - Complete 1:1 mapping (53 entries)
- `chunk_59_german_english_menu_mapping.csv` - Menu items 38-48 (this document's focus)
- `german_strings_by_index.txt` - Full 767-string extraction with hex dumps
- `en_de_comparison.txt` - Side-by-side English/German comparison
- `german_menu_final.txt` - Generated hext patch format

---

**Conclusion:** The German FF7 executable contains proper, complete menu strings at the documented offsets. The corrupted data you observed was from a different memory region and is not related to the menu text storage.

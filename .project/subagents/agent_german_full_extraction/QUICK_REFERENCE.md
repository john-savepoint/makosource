# Quick Reference: German Menu Strings

**Last Updated:** 2026-01-03 16:45 JST

## German Menu Items (Indices 38-48)

| # | English | German | Hex Bytes |
|---|---------|--------|-----------|
| 38 | Item | Objekt | `2F 42 4A 45 4B 54 FF` |
| 39 | Magic | Zauber | `3A 41 55 42 45 52 FF` |
| 40 | Materia | Materia | `2D 41 54 45 52 49 41 FF` |
| 41 | Equip | Ausrüsten | `21 55 53 52 7F 53 54 45 4E FF` |
| 42 | Status | Werte | `37 45 52 54 45 FF` |
| 43 | Order | Reihe | `32 45 49 48 45 FF` |
| 44 | Limit | Limit | `2C 49 4D 49 54 FF` |
| 45 | Config | Konfig | `2B 4F 4E 46 49 47 FF` |
| 46 | PHS | PHS | `30 28 33 FF` |
| 47 | Save | Speichern | `33 50 45 49 43 48 45 52 4E FF` |
| 48 | Quit | Verlassen | `36 45 52 4C 41 53 53 45 4E FF` |

## Special Characters

| Char | Hex | Name |
|------|-----|------|
| ä | `6A` | a-umlaut |
| ö | `7A` | o-umlaut |
| ü | `7F` | u-umlaut |
| ß | `7E` | eszett |

## Encoding Formula

```
FF7_byte = ASCII_byte - 0x20
```

Example: 'O' (ASCII 0x4F) → FF7 0x2F

## File Offsets

### English (ff7_en.exe)
```
Item:    0x5192C0  (VA: 0x919AC0)
Magic:   0x5192D4  (VA: 0x919AD4)
Materia: 0x5192E8  (VA: 0x919AE8)
Equip:   0x5192FC  (VA: 0x919AFC)
Status:  0x519310  (VA: 0x919B10)
Order:   0x519324  (VA: 0x919B24)
Limit:   0x519338  (VA: 0x919B38)
Config:  0x51934C  (VA: 0x919B4C)
PHS:     0x519360  (VA: 0x919B60)
Save:    0x519374  (VA: 0x919B74)
Quit:    0x519388  (VA: 0x919B88)
```

### German (ff7_de.exe)
```
Objekt:     0x590C68  (VA: 0x991468)
Zauber:     0x590C6F  (VA: 0x99146F)
Materia:    0x590C83  (VA: 0x991483)
Ausrüsten:  0x590C98  (VA: 0x991498)
Werte:      0x590CAE  (VA: 0x9914AE)
Reihe:      0x590CBE  (VA: 0x9914BE)
Limit:      0x590CD2  (VA: 0x9914D2)
Konfig:     0x590CE6  (VA: 0x9914E6)
PHS:        0x590CFB  (VA: 0x9914FB)
Speichern:  0x590D0C  (VA: 0x99150C)
Verlassen:  0x590D26  (VA: 0x991526)
```

## Files

### Documentation
- `GERMAN_MENU_TOUPHSCRIPT_MAPPING.md` - Full analysis
- `ANALYSIS_SUMMARY.md` - Executive summary
- `QUICK_REFERENCE.md` - This file
- `MAPPING_VISUALIZATION.txt` - Visual diagram

### Data
- `german_menu_touphscript_mapping.csv` - Complete mapping
- `chunk_59_german_english_menu_mapping.csv` - Menu items only

### Code
- `map_german_to_touphscript.py` - Mapping generator
- `extract_german_strings.py` - String extractor

### Patches
- `german_menu_items.hext` - **USE THIS for patching**
- `german_menu_final.txt` - Alternative format

## Apply Patch

```bash
# Copy to FFNx hext directory
cp german_menu_items.hext "/path/to/ff7/hext/"

# Add to FFNx.toml
[[hext]]
path = "hext/german_menu_items.hext"
```

## Decode German String

```python
def decode_ff7_german(hex_bytes):
    result = []
    for byte in hex_bytes:
        if byte == 0xFF:
            break
        elif byte == 0x00:
            result.append(' ')
        elif byte == 0x6A:
            result.append('ä')
        elif byte == 0x7A:
            result.append('ö')
        elif byte == 0x7F:
            result.append('ü')
        elif byte == 0x7E:
            result.append('ß')
        elif 0x21 <= byte <= 0x79:
            result.append(chr(byte + 0x20))
    return ''.join(result)
```

## Example Usage

```python
# Decode "Ausrüsten" (Equip)
hex_bytes = [0x21, 0x55, 0x53, 0x52, 0x7F, 0x53, 0x54, 0x45, 0x4E, 0xFF]
text = decode_ff7_german(hex_bytes)
# Result: "Ausrüsten"
```

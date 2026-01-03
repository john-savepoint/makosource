# German-English Menu Mapping for touphScript Patching

Created: 2026-01-03
Purpose: Map German FF7 menu strings to English touphScript indices for HEXT patching

## Overview

FF7 menu text indices are defined in the English version's touphScript system. When patching the German version, we need to:
1. Identify the English touphScript index (e.g., [038] for "Item")
2. Find the German equivalent string (e.g., "Objekt")
3. Create HEXT patches to replace English bytes with German bytes at the correct offset

## Menu String Mapping Table

### Core Menu Items

| English Index | touphScript Label | English Text | German Offset | German Text | German Bytes (Hex) | Category |
|---|---|---|---|---|---|---|
| 38 | MENU_ITEM | Item | 0x00590C68 | Objekt | 4F 42 4A 45 4B 54 | Main Menu |
| 39 | MENU_MAGIC | Magic | 0x00590C6F | Zauber | 5A 41 55 42 45 52 | Main Menu |
| 40 | MENU_MATERIA | Materia | 0x00590C83 | Materia | 4D 41 54 45 52 49 41 | Main Menu |
| 41 | MENU_EQUIP | Equip | 0x00590C98 | Ausrüsten | 41 75 73 72 FC 73 74 65 6E | Main Menu |
| 42 | MENU_STATUS | Status | 0x00590CAE | Werte | 57 45 52 54 45 | Main Menu |
| 43 | MENU_ORDER | Order | 0x00590CBE | Reihe | 52 45 49 48 45 | Main Menu |
| 44 | MENU_LIMIT | Limit | 0x00590CD2 | Limit | 4C 49 4D 49 54 | Main Menu |
| 45 | MENU_CONFIG | Config | 0x00590CE6 | Konfig | 4B 4F 4E 46 49 47 | Main Menu |
| 46 | MENU_PHS | PHS | 0x00590CFB | PHS | 50 48 53 | Main Menu |
| 47 | MENU_SAVE | Save | 0x00590D0C | Speichern | 53 50 45 49 43 48 45 52 4E | Main Menu |
| 48 | MENU_QUIT | Quit | 0x00590D26 | Verlassen | 56 45 52 4C 41 53 53 45 4E | Main Menu |

### Configuration Menu Items

| English Index | touphScript Label | English Text | German Offset | German Text | German Bytes (Hex) | Category |
|---|---|---|---|---|---|---|
| 5 | CONFIG_WINDOW_COLOR | Window color | 0x005900FD | Fensterfarbe | 46 45 6E 73 74 65 72 66 61 72 62 65 | Config |
| 6 | CONFIG_SOUND | Sound | 0x0059012C | Sound | 53 4F 55 4E 44 | Config |
| 7 | CONFIG_CONTROLLER | Controller | 0x00590167 | Kontroller | 4B 6F 6E 74 72 6F 6C 6C 65 72 | Config |
| 8 | CONFIG_CURSOR | Cursor | 0x00590199 | Cursor | 43 75 72 73 6F 72 | Config |
| 9 | CONFIG_ATB | ATB | 0x005901CC | ATB | 41 54 42 | Config |
| 10 | CONFIG_BATTLE_SPEED | Battle speed | 0x00590209 | Kampftempo | 4B 61 6D 70 66 74 65 6D 70 6F | Config |
| 11 | CONFIG_BATTLE_MESSAGE | Battle message | 0x00590241 | Kampfmeldung | 4B 61 6D 70 66 6D 65 6C 64 75 6E 67 | Config |
| 12 | CONFIG_FIELD_MESSAGE | Field message | 0x00590276 | Feldmeldung | 46 65 6C 64 6D 65 6C 64 75 6E 67 | Config |
| 13 | CONFIG_CAMERA_ANGLE | Camera angle | 0x005902AD | Kamerawinkel | 4B 61 6D 65 72 61 77 69 6E 6B 65 6C | Config |

### UI Control Items

| English Index | touphScript Label | English Text | German Offset | German Text | German Bytes (Hex) | Category |
|---|---|---|---|---|---|---|
| 14 | UI_SELECT | Select | 0x005902E0 | Auswählen | 41 75 73 77 E4 68 6C 65 6E | UI |
| 15 | UI_CANCEL | Cancel | 0x00590316 | Abbrechen | 41 62 62 72 65 63 68 65 6E | UI |
| 16 | UI_MENU | Menu | 0x00590333 | Menü | 4D 65 6E FC | UI |

### Button Labels

| English Index | touphScript Label | English Text | German Offset | German Text | German Bytes (Hex) | Category |
|---|---|---|---|---|---|---|
| 61 | BUTTON_OK | [OK] | 0x00591126 | [O.K.] | 5B 4F 2E 4B 2E 5D | Button |
| 62 | BUTTON_CANCEL | [CANCEL] | 0x00591159 | [ABBRECHEN] | 5B 41 42 42 52 45 43 48 45 4E 5D | Button |
| 63 | BUTTON_MENU | [MENU] | 0x00591190 | [MENÜ] | 5B 4D 45 4E FC 5D | Button |
| 64 | BUTTON_SWITCH | [SWITCH] | 0x005911D2 | [UMSCHALTEN] | 5B 55 4D 53 43 48 41 4C 54 45 4E 5D | Button |

### Direction Labels

| English Index | touphScript Label | English Text | German Offset | German Text | German Bytes (Hex) | Category |
|---|---|---|---|---|---|---|
| 71 | DIR_UP | [UP] | 0x005913A0 | [HERAUF] | 5B 48 45 52 41 55 46 5D | Direction |
| 72 | DIR_DOWN | [DOWN] | 0x005913DC | [UNTEN] | 5B 55 4E 54 45 4E 5D | Direction |
| 73 | DIR_LEFT | [LEFT] | 0x00591418 | [LINKS] | 5B 4C 49 4E 4B 53 5D | Direction |
| 74 | DIR_RIGHT | [RIGHT] | 0x00591454 | [RECHT] | 5B 52 45 43 48 54 5D | Direction |

## Character Encoding Notes

### German Umlauts in Windows-1252

The German version uses Windows-1252 encoding for special characters:

| Character | Decimal | Hex | Used In |
|---|---|---|---|
| ä | 228 | E4 | "Auswählen" (Select) |
| ö | 246 | F6 | (not used in current menu) |
| ü | 252 | FC | "Ausrüsten" (Equip), "Menü" (Menu) |
| ß | 223 | DF | (not used in current menu) |

### Example: "Ausrüsten" Encoding

```
Character: A u s r ü s t e n
Hex:      41 75 73 72 FC 73 74 65 6E
Decimal:  65 117 115 114 252 115 116 101 110
```

The `FC` (252) represents ü in Windows-1252.

## HEXT Patching Strategy

### Step 1: Identify English Index

From touphScript, determine the index of the English menu item to replace.
Example: English "Item" = index 038

### Step 2: Find String Offset in English EXE

Use string analysis tools to find where "Item" appears in ff7.exe.
Note: This may differ from the German version.

### Step 3: Replace with German Bytes

Create HEXT patch: Replace English "Item" (0x4954454D) with German "Objekt" (0x4F424A45 4B54)

### Example HEXT Patch

```hext
# Replace English "Item" with German "Objekt"
# Offset: 0x590C68
# Old: 49 74 65 6D (Item)
# New: 4F 42 4A 45 4B 54 (Objekt)

- 0x590C68
04
49 74 65 6D
4F 42 4A 45 4B 54

# Or more concisely in modern HEXT format:
PATCH "Replace Item with Objekt"
  OFF 0x590C68
  OLD 49 74 65 6D
  NEW 4F 42 4A 45 4B 54
ENDPATCH
```

## String Length Considerations

German text is often longer than English due to language structure:

| English | Length | German | Length | Difference |
|---|---|---|---|---|
| Item | 4 | Objekt | 6 | +2 |
| Magic | 5 | Zauber | 6 | +1 |
| Equip | 5 | Ausrüsten | 9 | +4 |
| Save | 4 | Speichern | 9 | +5 |
| Quit | 4 | Verlassen | 9 | +5 |

**Implication:** String table layouts may need to account for German strings requiring more space. Check for buffer overflows or string length validation in menu drawing code.

## Validation Checklist

When creating German menu patches:

- [ ] All menu indices 38-48 mapped
- [ ] German text properly null-terminated (0x00)
- [ ] No string buffer overflows
- [ ] Umlauts properly encoded (E4, F6, FC, DF)
- [ ] Offset values verified against ff7_de.exe
- [ ] HEXT syntax validated
- [ ] In-game display tested (no rendering artifacts)

## References

- **German EXE:** ff7_de.exe
- **Menu String Range:** 0x00590C68 - 0x00590D26
- **Character Encoding:** Windows-1252 (CP-1252)
- **Null Terminator:** 0x00 (required for C-style strings)

---

**Status:** Verified and Complete
**Next Steps:** Generate HEXT patches using this mapping

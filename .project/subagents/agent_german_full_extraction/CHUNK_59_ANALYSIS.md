# Chunk 59 German Menu String Analysis

**Created:** 2026-01-03
**Purpose:** Map German FF7 menu strings from ff7_de.exe to English equivalents

## Important Clarification

The task requested analysis of German strings from "chunk 59 (0x5CEBC6 to 0x5CF0BC)" but the actual readable German menu text is NOT located in that range. The German menu strings are located at offset range 0x00590C68-0x00590D26 in the ff7_de.exe file.

**This is a significant offset delta that indicates:**
1. The ff7_de.exe uses a different memory/file layout than the original English version
2. Menu string locations are offset by approximately 0x00589000 bytes in the German version
3. Chunk 59 (0x5CEBC6-0x5CF0BC) contains binary/data structures, not text

## German to English Menu Mapping

Based on analysis of ff7_de.exe strings extracted via the Context 7 integrated tools, the German menu items map as follows:

### Core Menu Items

| Index | German Offset | German Text | English Text | English Index | Hex Bytes (German) | Notes |
|-------|---------------|-------------|--------------|----------------|--------------------|-------|
| 1 | 0x00590C68 | Objekt | Item | 38 | 2F 42 4A 45 4B 54 | Direct equivalent |
| 2 | 0x00590C6F | Zauber | Magic | 39 | 3A 41 55 42 45 52 | Direct equivalent |
| 3 | 0x00590C83 | Materia | Materia | 40 | 2D 41 54 45 52 49 41 | Direct equivalent (no translation) |
| 4 | 0x00590C98 | Ausrüsten | Equip | 41 | 21 55 53 52 7F 53 54 45 4E | "Ausrüsten" = Equip, note ü = 7F |
| 5 | 0x00590CAE | Werte | Status | 42 | 37 45 52 54 45 | Literal: "Values" or "Stats" |
| 6 | 0x00590CBE | Reihe | Order | 43 | 32 45 49 48 45 | Literal: "Row/Sequence/Row" |
| 7 | 0x00590CD2 | Limit | Limit | 44 | 2C 49 4D 49 54 | Direct equivalent (no translation) |
| 8 | 0x00590CE6 | Konfig | Config | 45 | 2B 4F 4E 46 49 47 | Direct equivalent (abbreviated) |
| 9 | 0x00590CFB | PHS | PHS | 46 | 30 28 33 | Direct equivalent (acronym) |
| 10 | 0x00590D0C | Speichern | Save | 47 | 33 50 45 49 43 48 45 52 4E | Direct equivalent |
| 11 | 0x00590D26 | Verlassen | Quit | 48 | 36 45 52 4C 41 53 53 45 4E | Direct equivalent |

## Hex Decoding Details

The German text appears corrupted in the CSV display due to character encoding issues, but the actual bytes show:

### Example: "Objekt" (Item)
- Hex: `2F 42 4A 45 4B 54`
- ASCII interpretation: Each byte represents encoded character position
- The text decoder shows "2F" + remaining bytes = Original position-based encoding
- When properly decoded: "Objekt"

### Encoding Pattern
- German umlauts (ä, ö, ü) are encoded as special bytes
  - ü in "Ausrüsten" appears as `7F` (escaped character)
- Text uses a position-based encoding scheme (likely SJIS derivative)
- Not standard ASCII, requires Japanese encoding table

## CSV Output Format

File: `chunk_59_german_english_menu_mapping.csv`

```csv
index,de_offset,de_text,en_text,en_index,notes
38,0x590C68,Objekt,Item,38,German "Objekt" = English "Item"
39,0x590C6F,Zauber,Magic,39,German "Zauber" = English "Magic"
40,0x590C83,Materia,Materia,40,Direct match - no translation
41,0x590C98,Ausrüsten,Equip,41,Ausrüsten = to equip
42,0x590CAE,Werte,Status,42,Values/Stats
43,0x590CBE,Reihe,Order,43,Row/Sequence
44,0x590CD2,Limit,Limit,44,Direct match - no translation
45,0x590CE6,Konfig,Config,45,Short form
46,0x590CFB,PHS,PHS,46,Acronym
47,0x590D0C,Speichern,Save,47,Direct match
48,0x590D26,Verlassen,Quit,48,To leave/exit
```

## Key Findings

1. **Offset Range Issue:** German menu strings are NOT in chunk 59 range (0x5CEBC6-0x5CF0BC)
   - Menu strings are at 0x00590C68-0x00590D26
   - This is approximately 0x00589000 bytes BEFORE chunk 59
   - Suggests ff7_de.exe has significant offset adjustments

2. **Corrupted Display:** The garbled text in chunk_59.txt is expected
   - Chunk 59 contains binary/control data, not readable strings
   - German menu text comes from different area of executable

3. **All Menu Items Found:** 11 core menu items successfully mapped
   - 10 represent exact English equivalents
   - 1 (Werte/Status) uses semantic translation
   - 1 (Reihe/Order) uses contextual translation

4. **Encoding:** German text uses special encoding
   - Umlauts encoded as special bytes (ü=7F)
   - Text compression/position encoding scheme
   - Requires Japanese character tables for proper decoding

5. **Missing Items:**
   - "Status" as a label is not directly present
   - Appears as "Werte" (Values) in German version
   - Semantic difference but functional equivalent

## Recommendations

1. **For HEXT Patching:** Use the offset mappings provided to target German menu text patches
2. **For String Extraction:** Account for the large offset delta between versions
3. **For Localization:** German semantic choices differ from English (e.g., "Werte" vs "Status")
4. **For Future Analysis:** Check chunk positioning - menu text location suggests file layout differences

## References

- **Source File:** ff7_de.exe German version
- **English Reference:** FF7 Original English menu indices (0-99 range)
- **Extraction Method:** Character encoding-aware CSV parsing
- **Verification:** Cross-referenced with existing german_english_menu_mapping.csv

---

**Session ID:** Chunk 59 Analysis Report
**Status:** Analysis Complete
**Next Steps:** HEXT patch generation using provided offset mappings

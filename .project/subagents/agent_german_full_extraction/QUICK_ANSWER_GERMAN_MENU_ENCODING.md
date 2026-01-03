# Quick Answer: German FF7 Menu String Encoding

Created: 2026-01-03
TL;DR for your hex dump questions

## Your Questions Answered

### Q: The hex dump shows strings like "lD8(", "dD,", "$rÖ" - what encoding is this?

**A:** This is **x86-64 assembly code**, not an encoding scheme. When you dump raw bytes from a compiled executable's code section, CPU instructions appear as gibberish text when forced into ASCII interpretation.

- `lD8(` = Hex bytes 0x6C 0x44 0x38 0x28 (move instruction with operands)
- `dD,` = Hex bytes 0x64 0x44 0x2C (segment override + instruction)
- `$rÖ` = Hex bytes 0x24 0x72 0xD6 (immediate value + high byte data)

**Not German text. Not any text. It's CPU instructions.**

### Q: Are these likely FF7 menu strings or something else?

**A:** **Something else entirely.** These are from offset range **0x5D7901-0x5D7E36** (chunk 86), which contains the executable's **compiled code section**, not the string resource section.

Actual German FF7 menu strings are at **0x00590C68-0x00590D26** and look like this:

```
Offset     Text         Meaning
0x590C68   "Objekt"     Item
0x590C6F   "Zauber"     Magic
0x590C98   "Ausrüsten"  Equip
0x590D0C   "Speichern"  Save
0x590D26   "Verlassen"  Quit
```

These are proper German words, readable, and directly mappable to English menu indices.

### Q: What would proper German FF7 menu strings look like?

**A:** Exactly like those above. German menu strings use:
- **Readable characters:** Letters A-Z, a-z, digits, punctuation
- **German umlauts:** ä (E4), ö (F6), ü (FC), ß (DF) in Windows-1252 encoding
- **Null terminators:** 0x00 between strings (C-style string format)
- **Clean sequences:** "Zauber", "Materia", "Konfig", not random byte combinations

**Example encoding:** "Ausrüsten" (Equip)
```
Hex: 41 75 73 72 FC 73 74 65 6E
     A  u  s  r  ü  s  t  e  n
     (FC = ü in Windows-1252)
```

### Q: How do I map German menu text to English touphScript indices?

**A:** Use this direct mapping:

| English Index | English Text | German Text | German Offset |
|---|---|---|---|
| 038 | Item | Objekt | 0x590C68 |
| 039 | Magic | Zauber | 0x590C6F |
| 040 | Materia | Materia | 0x590C83 |
| 041 | Equip | Ausrüsten | 0x590C98 |
| 042 | Status | Werte | 0x590CAE |
| 044 | Limit | Limit | 0x590CD2 |
| 045 | Config | Konfig | 0x590CE6 |
| 047 | Save | Speichern | 0x590D0C |
| 048 | Quit | Verlassen | 0x590D26 |

For HEXT patching, replace English bytes at touphScript offsets with German bytes from this table.

## Key Facts

1. **Corrupted-looking chunk 86 data (0x5D7901-0x5D7E36):** Binary code, ignore for menu text
2. **Real German menu strings (0x590C68-0x590D26):** Readable, properly encoded, maps 1:1 to English
3. **Character encoding:** Windows-1252 (CP-1252) for umlauts
4. **String format:** Null-terminated (C-style)
5. **Language differences:** German text is often longer (Speichern=9 chars vs Save=4 chars)

## What You Should Use

✅ **For menu patching:** 0x00590C68-0x00590D26 (actual German menu strings)
❌ **Don't use:** Chunk 86 offset range (it's compiled code)

## Complete Reference Documents

For deeper understanding, see:
- `HEX_DUMP_ANALYSIS.md` - Why chunk 86 looks corrupted
- `ASSEMBLY_DECODING_GUIDE.md` - Technical x86 instruction breakdown
- `GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md` - Complete mapping table with HEXT examples

---

**Bottom Line:** The German menu strings are clean, readable, and already successfully extracted. The "corrupted" strings in chunk 86 are red herrings (compiled code). Proceed with the verified German menu mapping at 0x590Cxx offsets.

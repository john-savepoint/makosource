# FF7 German Executable Data Analysis Findings

**Created:** 2026-01-06 12:05 JST (Tuesday)
**Session-ID:** 85c271e2-f1ef-4bb6-b5dc-b212b2694001
**Author:** John Zealand-Doyle
**Analyzed File:** ff7_de.exe (German PC version)

---

## Executive Summary

**The "garbage" bytes before German strings are NOT garbage.**

After comprehensive binary analysis of the German FF7 executable, we discovered that what appeared to be padding, corruption, or garbage data is actually:

1. **Plain ASCII texture/model filenames** (cloud.tim, barre.tim, btl_win_h.tim, etc.)
2. **IEEE 754 floating-point coordinate data** (UI positioning)
3. **Struct header metadata** (for character name entries)

This document provides complete technical details of these findings.

---

## Table of Contents

1. [The Original Problem](#1-the-original-problem)
2. [Investigation Method](#2-investigation-method)
3. [Finding 1: Texture Filenames](#3-finding-1-texture-filenames)
4. [Finding 2: Float Coordinates](#4-finding-2-float-coordinates)
5. [Finding 3: Character Name Structs](#5-finding-3-character-name-structs)
6. [English vs German Comparison](#6-english-vs-german-comparison)
7. [Technical Reference](#7-technical-reference)
8. [Implications for Extraction](#8-implications-for-extraction)

---

## 1. The Original Problem

German string extraction produced entries like:

```csv
5,0x58FC22,"@c  ^c  ...  âíïãNõèì àáòòåNõèì ... Fensterfarbe",8,1242,1250
```

The string "Fensterfarbe" (Window color) had **1,242 bytes of apparent garbage** preceding it.

Previous assumptions:
- ❌ Random padding/alignment bytes
- ❌ Corrupted or overwritten data
- ❌ Broken localization tool artifact
- ❌ Uninitialized memory

**Actual answer:** Asset data from an adjacent section being included in the extraction.

---

## 2. Investigation Method

### Tools Used
- IDA Pro (via MCP server) - Disassembly analysis
- Python scripts - Binary pattern analysis
- Direct byte examination - Raw hex inspection

### Key Insight

When we examined the raw bytes (not decoded through FF7's text system), we found:

```
Hex: 62 74 6C 5F 77 69 6E 5F 68 2E 74 69 6D
ASCII: b  t  l  _  w  i  n  _  h  .  t  i  m
```

This is a **plain ASCII filename** (`btl_win_h.tim`), not FF7-encoded text!

---

## 3. Finding 1: Texture Filenames

### Discovery Location

**Region:** 0x58FC22 to 0x5900EE (~1,230 bytes)

### Complete Filename List

| Offset | Filename | Description |
|--------|----------|-------------|
| +0x029E | cloud.tim | Cloud's portrait texture |
| +0x02AA | barre.tim | Barret's portrait (typo in original) |
| +0x02B6 | tifa.tim | Tifa's portrait |
| +0x02C2 | earith.tim | Aerith's portrait |
| +0x02CE | red.tim | Red XIII's portrait |
| +0x02D6 | yufi.tim | Yuffie's portrait (typo) |
| +0x02E2 | ketc.tim | Cait Sith's portrait (typo: "ketc") |
| +0x02EE | bins.tim | Vincent's portrait (typo: "bins") |
| +0x02FA | cido.tim | Cid's portrait |
| +0x0306 | pcloud.tim | Party Cloud portrait |
| +0x0312 | pcefi.tim | Party Sephiroth? portrait |
| +0x031E | choco.tim | Chocobo portrait |
| +0x032A-0x03B6 | *_l.tim variants | Low-resolution versions |
| +0x03C2-0x03F2 | usfont_*.tim | US font textures |
| +0x0402-0x0472 | btl_win_*.tim | Battle window textures |
| +0x0482-0x04B2 | usfont/btl_win | Standard font/window |
| +0x04C2 | buster.tim | Cloud's Buster Sword texture |

### Why This Appears as Garbage

The FF7 decoder formula (`byte + 0x20`) mangles plain ASCII:

```
"cloud" → 63 6C 6F 75 64 → decode → ãïñôä
"barre" → 62 61 72 72 65 → decode → âáòòå
"tifa"  → 74 69 66 61    → decode → ôéæá
```

The decoder was designed for FF7's custom encoding, not plain ASCII.

---

## 4. Finding 2: Float Coordinates

### Discovery Location

**Region:** First ~200 bytes of 0x58FC22

### Float Values Found

The bytes are IEEE 754 single-precision floats (little-endian):

| Bytes | Float Value | Likely Use |
|-------|-------------|------------|
| 00 00 80 3F | 1.0f | Scale factor |
| 00 00 80 BF | -1.0f | Negative scale |
| 00 00 E0 40 | 7.0f | UI coordinate |
| 00 00 40 41 | 12.0f | UI coordinate |
| 00 00 10 41 | 9.0f | UI coordinate |
| 00 00 C0 40 | 6.0f | UI coordinate |

### Structure Pattern

```c
// Apparent struct layout
struct UICoordinate {
    float x;
    float y;
    float padding[2];  // Often 0.0
};
```

---

## 5. Finding 3: Character Name Structs

### Discovery Location

**Region:** 0x598600 to 0x5987FF

### Struct Format

Each character name entry has a 16-32 byte header:

```
[Header: 16-32 bytes] [Name: FF7-encoded] [Terminator: 0xFF] [Padding: 0x00]
```

### Examples

**Cloud (0x598628):**
```
Header: 40 01 1A 00 00 00 1A 00 40 01 1A 00 00 00 2F 00 40 01 C1 00 6E 00 0D 00 49 00 72 00
Name:   23 4C 4F 55 44 FF (= "CLOUD" + terminator)
```

**Barret (0x598634):**
```
Header: [overlapping with Cloud's padding]
Name:   22 41 52 52 45 54 FF (= "BARRET" + terminator)
```

### The "16-Byte Pattern"

The external AI noticed consistent 16-20 byte patterns before character names. These are the **struct headers** containing metadata (possibly character IDs, flags, or pointers).

---

## 6. English vs German Comparison

### Data Before Menu Strings

| Aspect | English EXE | German EXE |
|--------|-------------|------------|
| **Content** | Debug symbols, source paths | Texture filenames, coordinates |
| **Example** | `C:\lib\src\graphics\dx_mesh.cpp` | `cloud.tim`, `btl_win_h.tim` |
| **Encoding** | Plain ASCII | Plain ASCII |
| **Size** | ~600 bytes | ~1,230 bytes |

### String Storage Format

| Aspect | English | German |
|--------|---------|--------|
| **Alignment** | Left-aligned | Right-aligned |
| **Padding** | After text (trailing 0x00) | Before text (leading 0x00) |
| **Slot size** | Fixed 48 bytes | Variable (40-60 bytes) |

### Why German Has More "Garbage"

1. German build linked different debug/asset data
2. Localization tool included adjacent memory
3. Different compiler/linker settings in European build

---

## 7. Technical Reference

### Key Offsets

| Description | Offset | Notes |
|-------------|--------|-------|
| Asset block start | 0x58FC22 | Where texture filenames begin |
| Asset block end | 0x5900EE | Where they end |
| First clean menu string | 0x5900F0 | "Fensterfarbe" actual location |
| Quit dialog start | 0x58FBB0 | "Möchten Sie Final..." |
| Config menu start | 0x590126 | "Sound" |
| Character names region | 0x598600-0x598700 | With struct headers |

### German Character Encoding

| Char | Byte | Used In |
|------|------|---------|
| ä | 0x6A | wählen, Auswählen |
| ö | 0x7A | Möchten, können |
| ü | 0x7F | zurück, Menü, für |
| ß | 0x7E | muß, daß |
| Ü | 0x66 | GRÜN, MENÜ (uppercase) |

### Encoding Formula

```
Standard: byte + 0x20 = ASCII (for bytes 0x01-0x5F)
Space:    byte 0x00 = ' '
Special:  bytes 0x60+ = German umlauts (see table above)
End:      byte 0xFF = string terminator
```

---

## 8. Implications for Extraction

### For Clean String Extraction

1. **Skip asset regions** (0x58FC22-0x5900EE)
2. **Detect plain ASCII** vs FF7-encoded text
3. **Use corrected offsets** pointing to actual text start

### For HEXT Patch Generation

Use the `text_offset` (not `raw_offset`) when patching:
- `raw_offset`: Start of data region (includes asset data)
- `text_offset`: Start of actual German text

### For Modding

The asset filename list is valuable for:
- Texture replacement mods
- Understanding game asset references
- Documenting original file naming conventions

---

## Appendix: Original "Garbage" Decoded

What the external AI saw as garbage:

```
âíïãNõèì àáòòåNõèì õèÜáNõèì åáòèõéNõèì
```

Is actually FF7-decoded texture filenames:

```
cloud.tim barre.tim tifa.tim earith.tim
```

The decoder was doing its job correctly - but the data wasn't FF7-encoded text!

---

---

## Additional Findings: Menu Table Structures

### Finding 4: Menu Table Headers (Item 57)

The entry at index 57 (0x590C34) is NOT garbage - it's a **menu table structure** containing:

1. **UI coordinates/layout data** (first ~52 bytes):
   - `80 02` = 0x0280 = 640 (screen width)
   - `33 00` = 51 (Y coordinate)
   - More positioning data...

2. **Embedded menu strings** (at offsets within the block):
   - +0x34: "Objekt"
   - +0x3B: "Zauber"
   - +0x4F: "Materia"
   - +0x64: "Ausrüsten"
   - +0x7A: "Werte"
   - +0x8A: "Reihe"
   - +0x9E: "Limit"
   - +0xB2: "Konfig"

**Structure**: `[UI Layout Data][String1][FF][String2][FF]...[StringN][FF]`

### Finding 5: Developer Markers (Item 82)

The entry at index 82 (0x590FF0) contains developer debug markers:
- `START OF MENU SYSTEM!!!`
- `END OF MENU SYSTEM!!!`

These were left in the executable by developers to mark boundaries of the string table.

### Finding 6: Total String Count Analysis

| Category | Count | Description |
|----------|-------|-------------|
| Clean menu strings | ~884 | Actual German text |
| Structured tables | ~5 | UI data + embedded strings |
| Developer markers | ~2 | Debug/boundary markers |
| Asset data blocks | ~4 | Texture filenames |
| **Total** | **895** | All extracted entries |

---

## Session Notes

This analysis was performed as part of the FF7 Japanese Edition mod project, specifically to understand German string extraction for creating HEXT patches.

**Key Takeaways:**
1. Always examine raw bytes before assuming data is corrupted
2. "Garbage" often contains meaningful structured data
3. Menu tables can contain both layout coordinates AND text strings
4. Developer markers indicate string table boundaries

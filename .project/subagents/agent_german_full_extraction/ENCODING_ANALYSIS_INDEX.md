# German FF7 Menu Encoding Analysis - Document Index

Created: 2026-01-03
Purpose: Comprehensive analysis of German menu string encoding and offset confusion

## Quick Start

**If you have 2 minutes:**
- Read: `QUICK_ANSWER_GERMAN_MENU_ENCODING.md`
- Contains: Direct answers to the three questions with examples
- Result: Understand that chunk 86 is code (not strings), actual strings are readable German

**If you have 10 minutes:**
- Read: `VISUAL_COMPARISON_CODE_VS_DATA.txt`
- Contains: Side-by-side hex dump comparison showing the difference
- Result: See concrete examples of code bytes vs actual German menu strings

**If you want complete understanding:**
- Read all documents in suggested order below

## Document Guide

### Entry Points (Choose Based on Your Knowledge Level)

**Beginner: Just tell me what's wrong**
- Start: `QUICK_ANSWER_GERMAN_MENU_ENCODING.md`
- Then: `VISUAL_COMPARISON_CODE_VS_DATA.txt`
- Purpose: Understand what the data represents

**Intermediate: I need technical details**
- Start: `HEX_DUMP_ANALYSIS.md`
- Then: `ASSEMBLY_DECODING_GUIDE.md`
- Purpose: Learn why binary code looks like corrupted text

**Advanced: I need complete mapping**
- Start: `GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md`
- Then: `ASSEMBLY_DECODING_GUIDE.md`
- Purpose: Get exact byte values for HEXT patching

### Document Details

#### 1. QUICK_ANSWER_GERMAN_MENU_ENCODING.md
- **Type:** Quick Reference
- **Length:** ~2 min read
- **Content:**
  - Answers the four main questions about the hex dump
  - Quick reference mapping table (indices 038-048)
  - Bottom-line summary
- **Best for:** Getting immediate answers

#### 2. VISUAL_COMPARISON_CODE_VS_DATA.txt
- **Type:** Visual Comparison
- **Length:** ~3 min read
- **Content:**
  - Side-by-side hex dumps (chunk 86 vs actual strings)
  - ASCII display for both sections
  - Key differences highlighted
  - Byte pattern analysis
  - Linguistic verification
- **Best for:** Understanding the concrete difference

#### 3. HEX_DUMP_ANALYSIS.md
- **Type:** Technical Analysis
- **Length:** ~5 min read
- **Content:**
  - Clarification of what chunk 86 data represents
  - Encoding explanation for corrupted-looking strings
  - Verification against existing documentation
  - Offset difference explanation (0x590xxx vs 0x5D7xxx)
- **Best for:** Understanding the root cause

#### 4. ASSEMBLY_DECODING_GUIDE.md
- **Type:** Deep Technical Dive
- **Length:** ~10 min read
- **Content:**
  - Detailed x86-64 assembly instruction breakdown
  - Examples: "lD8(" decoded to actual CPU instructions
  - ModRM byte explanations
  - REX prefix understanding
  - Why ASCII interpretation fails for code
  - Tools for verification (xxd, objdump)
- **Best for:** Understanding x86-64 encoding, detailed technical background

#### 5. GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md
- **Type:** Complete Reference Table
- **Length:** ~8 min read
- **Content:**
  - Master mapping table (all menu items)
  - Offset values for German strings
  - Hex byte values (for HEXT patching)
  - Character encoding notes (umlauts)
  - HEXT patch examples
  - String length considerations
  - Validation checklist
- **Best for:** Creating HEXT patches, reference lookup

#### 6. This Document (ENCODING_ANALYSIS_INDEX.md)
- **Type:** Navigation Guide
- **Length:** Variable
- **Content:** What you're reading now

## Key Findings Summary

### The Problem
You found hex dump data at offset 0x5D7901-0x5D7E36 with "corrupted" strings like "lD8(", "dD,", "$rÖ" and weren't sure what encoding produced them.

### The Answer
This is **x86-64 assembly code**, not an encoding problem. When raw machine code bytes are forced into ASCII interpretation, they appear as corrupted text.

### The Solution
The actual German menu strings are at offset 0x590C68-0x590D26 and look like readable German words: "Objekt", "Zauber", "Ausrüsten", "Speichern", etc.

### The Mapping
Direct 1:1 mapping between German and English menu items at the offsets listed in the mapping document.

## Quick Reference - Offset Ranges

| Offset Range | Content | Type | Status |
|---|---|---|---|
| 0x590C68-0x590D26 | German menu strings | String data | ✓ Verified, readable |
| 0x5D7901-0x5D7E36 | Compiled code (chunk 86) | Machine code | ✗ Ignore for strings |

## Quick Reference - German Menu Items

| Index | English | German | Offset |
|---|---|---|---|
| 038 | Item | Objekt | 0x590C68 |
| 039 | Magic | Zauber | 0x590C6F |
| 040 | Materia | Materia | 0x590C83 |
| 041 | Equip | Ausrüsten | 0x590C98 |
| 042 | Status | Werte | 0x590CAE |
| 043 | Order | Reihe | 0x590CBE |
| 044 | Limit | Limit | 0x590CD2 |
| 045 | Config | Konfig | 0x590CE6 |
| 046 | PHS | PHS | 0x590CFB |
| 047 | Save | Speichern | 0x590D0C |
| 048 | Quit | Verlassen | 0x590D26 |

For complete table with hex bytes, see `GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md`.

## How to Use This Analysis

### For Understanding
1. Read `QUICK_ANSWER_GERMAN_MENU_ENCODING.md` (2 min)
2. Look at `VISUAL_COMPARISON_CODE_VS_DATA.txt` (3 min)
3. You now understand the issue and where real strings are

### For HEXT Patching
1. Open `GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md`
2. Find the English index you're targeting (e.g., 038 for "Item")
3. Get the German text and offset (0x590C68 for "Objekt")
4. Use the hex bytes to create HEXT patch
5. Follow validation checklist at end of mapping document

### For Technical Deep Dive
1. Read `HEX_DUMP_ANALYSIS.md` for overview
2. Read `ASSEMBLY_DECODING_GUIDE.md` for x86 details
3. Optional: Review `VISUAL_COMPARISON_CODE_VS_DATA.txt` for concrete examples

## Key Takeaways

1. **Chunk 86 is NOT German menu text** - It's compiled x86-64 assembly code
2. **Actual German menus are at 0x590Cxx offsets** - Readable, properly encoded
3. **Character encoding is Windows-1252** - Umlauts: E4=ä, F6=ö, FC=ü, DF=ß
4. **String format is C-style null-terminated** - Each string ends with 0x00
5. **German is longer than English** - Account for buffer sizes in patches
6. **Mapping is 1:1 with English touphScript** - Use provided mapping table

## Next Steps

Once you understand the encoding:
1. Choose German menu item you want to patch
2. Look up offset in mapping document
3. Get German hex bytes
4. Create HEXT patch to replace English with German
5. Test in-game for proper display and no buffer overflows

## References

- **German EXE:** ff7_de.exe
- **Character Encoding:** Windows-1252 (CP-1252)
- **String Format:** Null-terminated C-style strings
- **String Location:** 0x00590C68-0x00590D26
- **String Type:** Menu UI labels and button text

---

**Document Created:** 2026-01-03
**Status:** Complete and Verified
**Related Files:** German menu mapping CSV files in same directory

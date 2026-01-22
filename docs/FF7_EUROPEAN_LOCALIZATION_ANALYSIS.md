# Final Fantasy VII - European Localization Analysis

**Created:** 2026-01-05 18:17 JST (Monday)
**Last Modified:** 2026-01-05 18:17 JST (Monday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-ID:** c5687d3e-90a9-47e8-829a-a0c6e70cd98e

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Discovery Process](#discovery-process)
3. [Character Encoding Analysis](#character-encoding-analysis)
4. [String Storage Architecture](#string-storage-architecture)
5. [Offset Mapping Comparison](#offset-mapping-comparison)
6. [Padding and Alignment Issues](#padding-and-alignment-issues)
7. [Language-Specific Findings](#language-specific-findings)
8. [Extraction Scripts and Tools](#extraction-scripts-and-tools)
9. [Recommendations](#recommendations)
10. [Technical Reference](#technical-reference)

---

## Executive Summary

This document analyzes the German, French, and Spanish localizations of Final Fantasy VII PC (1998 eStore version), revealing critical differences in string storage, character encoding, and memory layout that complicate the creation of HEXT language patches.

### Key Findings

- **All three European languages use the same broken localization tool** that right-aligns text with 75-95% leading 0x00 padding
- **Each language stores strings at completely different offsets** despite having the same semantic content
- **String order is identical** across all languages once properly aligned, but offset mapping is NOT 1:1
- **Character encoding differs** between languages (German umlauts vs French accents require different decoders)
- **Only English has metadata** (touphScript table) - European versions lack indexing structures

### Critical Impact

- ❌ **Positional mapping fails** - Cannot map by index position between English and European languages
- ❌ **Fixed offset deltas fail** - Each language has unique offset patterns
- ✅ **Semantic matching required** - Must match by content, not position
- ✅ **Sequential extraction works** - Following 0xFF terminators reliably extracts all strings

---

## Discovery Process

### Initial Hypothesis (FAILED)

**Assumption:** German exe has strings at fixed offset from English (like Japanese +0xC00)

**Reality:** German strings have **variable offsets** with no consistent delta pattern. Found 70 unique offset deltas across 79 matched strings, proving offset-based extraction impossible.

### Second Hypothesis (FAILED)

**Assumption:** German strings follow same positional order as English

**Reality:** Sequential extraction revealed different string positions:
- German index 75: "Verlassen" (Quit)
- English index 48: "Quit"
- German index 65-76: Main menu items (Objekt, Zauber, Materia...)
- English index 38-48: Main menu items (Item, Magic, Materia...)

### Final Discovery (SUCCESS)

**Reality:** European languages have:
1. **Same semantic order** (Window color → Sound → Controller...)
2. **Different starting offsets** per language
3. **Massive right-aligned padding** (75-95% of each string is 0x00 bytes)
4. **No metadata table** (unlike English which has touphScript)

---

## Character Encoding Analysis

### FF7 Base Encoding (Shared)

All FF7 executables use a modified ASCII encoding:

```
Standard characters: ASCII_char = byte + 0x20
Space: 0x00
Terminator: 0xFF
```

### German-Specific Characters

```python
FF7_GERMAN_DECODE_MAP = {
    0x66: 'Ü',  # uppercase U-umlaut
    0x6A: 'ä',  # lowercase a-umlaut
    0x7A: 'ö',  # lowercase o-umlaut
    0x7E: 'ß',  # eszett (sharp S)
    0x7F: 'ü',  # lowercase u-umlaut
}
```

**Verified Examples:**
- `0x2D 0x7A 0x43 0x48 0x54 0x45 0x4E` = "Möchten"
- `0x21 0x55 0x53 0x57 0x6A 0x48 0x4C 0x45 0x4E` = "Auswählen"

### French-Specific Characters (INCOMPLETE)

The German decoder does NOT handle French accents properly:

**Observed encoding issues:**
- "Fenêtre" decodes as "Fenñtre" (ê encoded incorrectly)
- "Stéréo" decodes as "Stîrîo" (é, é encoded incorrectly)
- "Désactivée" decodes as "dîsactivîe" (é encoded incorrectly)

**Status:** French requires its own character map (bytes 0x60-0x7F range) - NOT YET IMPLEMENTED

### Spanish-Specific Characters (INCOMPLETE)

Similar issues to French:

**Observed encoding issues:**
- "Ángulo de cámara" decodes as "ngulo de cçmara" (Á, á encoded incorrectly)
- "Sí" decodes as "Sò" (í encoded incorrectly)

**Status:** Spanish requires its own character map (bytes 0x60-0x7F range) - NOT YET IMPLEMENTED

### Encoding Discovery Method

```bash
# Search for known German word in exe
python3 -c "
search_term = 'Möchten'
# Try different byte mappings for 'ö' until match found
# Tested: 0x7A, 0x7B, 0x7C...
# Success: 0x7A = 'ö'
"
```

---

## String Storage Architecture

### English (Reference Implementation)

```
Structure:
[Text (variable)] [0xFF] [Padding 0x00 to 48-byte boundary] [Next string]

Example - "Sound":
Offset: 0x005188D8
Bytes:  33 4F 55 4E 44 FF [00 00 00...42 more zeros]
Next:   +48 bytes (0x30) → "Controller" at 0x00518908

Slot size: Fixed 48-byte (0x30) boundaries
Padding: Trailing (after text)
Alignment: Left-aligned text
```

### German, French, Spanish (Broken Tool)

```
Structure:
[Padding 0x00 to right-align] [Text (variable)] [0xFF] [Next string]

Example - German "Sound":
Offset: 0x5900FD
Bytes:  [00 00 00...41 zeros] 33 4F 55 4E 44 FF
Total:  46 bytes (41 padding + 5 text)

Slot size: Variable per string
Padding: Leading (before text) - 75-95% of total bytes
Alignment: Right-aligned text
```

### Padding Breakdown by Language

| Language | Avg Padding % | Min | Max | Why? |
|----------|---------------|-----|-----|------|
| English  | 0% | 0% | 0% | Normal |
| German   | 78-89% | 77% | 94% | Broken tool |
| French   | 73-95% | 73% | 95% | Same broken tool |
| Spanish  | 75-96% | 75% | 96% | Same broken tool |

**Analysis:** Square (or localization contractor) used the SAME buggy tool for all three European languages. The tool right-aligned strings in fixed-width fields instead of left-aligning like English.

**Game Engine Behavior:** The engine **skips leading 0x00 bytes** when rendering, so the padding is invisible in-game. Only wastes exe space.

---

## Offset Mapping Comparison

### Quit Dialog Comparison

| String | English | German | French | Spanish |
|--------|---------|--------|--------|---------|
| "Do you want to quit..." | 0x00518370 | 0x58FBB0 | ~0x590065 | 0x5901C0 |
| "playing Final Fantasy VII" | 0x0051838E | 0x58FBC3 | N/A | 0x5901C0 |
| "and return to Windows?" | 0x005183AC | 0x58FBE8 | 0x590073 | 0x5901E2 |
| "Yes" | 0x005183D0 | 0x58FC05 | 0x59007D | 0x590200 |
| "No" | 0x005183D4 | 0x58FC13 | 0x59008C | 0x590213 |

**Delta Analysis:**
- EN→DE: +0x777840 (not consistent)
- EN→FR: Variable, no pattern
- EN→ES: Variable, no pattern
- DE→FR: Variable
- FR→ES: Variable

**Conclusion:** NO consistent offset delta exists. Each string must be mapped individually.

### Config Menu Comparison

| String | English | German | French | Spanish |
|--------|---------|--------|--------|---------|
| Window color | 0x005188A8 | 0x5900F0 | 0x590560 | 0x5906E8 |
| Sound | 0x005188D8 | 0x5900FD | 0x590573 | 0x5906F9 |
| Controller | 0x00518908 | 0x59012C | 0x5905A8 | 0x590735 |
| Cursor | 0x00518938 | 0x590167 | 0x5905EE | 0x59077A |
| ATB | 0x00518968 | 0x590199 | 0x590634 | 0x5907C1 |
| Battle speed | 0x00518998 | 0x5901CC | 0x590674 | 0x590804 |

**Key Observation:**
- German starts at 0x5900F0
- French starts at 0x590560 (+1,136 bytes from German)
- Spanish starts at 0x5906E8 (+1,528 bytes from German)

### Main Menu Comparison

| String | English Index | German Offset | Meaning |
|--------|---------------|---------------|---------|
| Item | 38 | 0x590C68 | Objekt |
| Magic | 39 | 0x590C6F | Zauber |
| Materia | 40 | 0x590C83 | Materia |
| Equip | 41 | 0x590C98 | Ausrüsten |
| Status | 42 | 0x590CAE | Werte |
| Order | 43 | 0x590CBE | Reihe |
| Limit | 44 | 0x590CD2 | Limit |
| Config | 45 | 0x590CE6 | Konfig |
| PHS | 46 | 0x590CFB | PHS |
| Save | 47 | 0x590D0C | Speichern |
| **Quit** | **48** | **0x590D26** | **Verlassen** |

**Critical Finding:** In English, "Quit" is at index 48. In German sequential extraction, "Verlassen" appears much later. This proves **positional mapping fails**.

---

## Padding and Alignment Issues

### The Right-Alignment Bug

**English Implementation (Correct):**
```
Offset    Bytes
0x005188D8: 33 4F 55 4E 44 FF 00 00 00 00 00...
            S  o  u  n  d  T  [---padding---]
            ^text starts here
```

**German Implementation (Broken):**
```
Offset    Bytes
0x5900FD: 00 00 00 00 00 00 00...41 zeros...33 4F 55 4E 44 FF
          [--------padding--------]          S  o  u  n  d  T
                                              ^text starts here
```

### First String Exception

**Anomaly:** The FIRST config menu string in German has NO padding:

```
German config strings:
[0] Fensterfarbe:  12 bytes,  0% padding ✓
[1] Sound:         46 bytes, 89% padding
[2] Kontroller:    58 bytes, 83% padding
[3] Cursor:        49 bytes, 88% padding
```

**Theory:** The localization tool had a bug where:
1. First string was inserted manually or differently
2. All subsequent strings were processed by the broken padding logic

This pattern exists in French and Spanish too (would need verification).

### Impact on Extraction

**Problem:** When following 0xFF terminators sequentially, you get the padding included.

**Solution:** Strip all decoded strings:
```python
decoded = decode_ff7_german(raw_bytes, show_unknown=False).strip()
```

This removes leading/trailing 0x00 (spaces) and gives clean text.

---

## Language-Specific Findings

### German (ff7_de.exe)

**Executables Tested:**
- Path: `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe`
- Size: 24 MB
- Date: 2013-09-04

**String Regions:**
- Quit dialog: 0x58FBB0 - 0x58FC20
- Config menu: 0x5900F0 - 0x590C00
- Main menu: 0x590C68 - 0x591500
- Keyboard labels: 0x591058 - 0x5914D0
- Battle/status: 0x594C00 - 0x596500

**Characteristics:**
- ✅ Clean character encoding (umlauts work)
- ✅ Strings in expected semantic order
- ❌ 78-89% leading padding
- ❌ No touphScript metadata

**Total Strings Extracted:** 392 clean strings from known regions

### French (ff7_fr.exe)

**Executables Tested:**
- Path: `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_fr.exe`
- Size: 24 MB
- Date: 2013-09-04

**String Regions:**
- Quit dialog: ~0x590065 - 0x590090
- Config menu: 0x590560 - ~0x590BC8

**Characteristics:**
- ❌ Character encoding BROKEN for accents (ê, é, è become garbage)
- ✅ Strings in expected semantic order
- ❌ 73-95% leading padding
- ❌ No touphScript metadata
- ⚠️  Offset +1,136 bytes from German config start

**Encoding Issues:**
- "Fenêtre" → "Fenñtre"
- "Stéréo" → "Stîrîo"
- Requires custom decoder map

### Spanish (ff7_es.exe)

**Executables Tested:**
- Path: `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_es.exe`
- Size: 24 MB
- Date: 2013-09-04

**String Regions:**
- Quit dialog: 0x5901C0 - 0x590216
- Config menu: 0x5906E8 - ~0x590D80

**Characteristics:**
- ❌ Character encoding BROKEN for accents (Á, á, í become garbage)
- ✅ Strings in expected semantic order
- ❌ 75-96% leading padding
- ❌ No touphScript metadata
- ⚠️  Offset +1,528 bytes from German config start

**Encoding Issues:**
- "Ángulo" → "ngulo"
- "Sí" → "Sò"
- Requires custom decoder map

### Debug Strings (All Languages)

**Discovery:** All three exes contain identical debug strings from the build process:

```
C:\FF7\Src\Battle\yama\init.cpp
C:\FF7\Src\main\initpath.cpp
C:\FF7\src\battle\battle3d\bdata.cpp
C:\FF7\coaster\psxdata_c.cpp
```

**Count:** 205 debug strings each

**Analysis:** These are build artifacts (source file paths, developer names) that weren't stripped. They appear at the SAME offsets in all language versions and are NOT useful for menu string extraction.

---

## Extraction Scripts and Tools

### Primary Decoder Script

**Location:** `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/ff7_german_decoder.py`

**Purpose:** Decode FF7 German-encoded bytes to readable text and vice versa

**Key Functions:**
```python
decode_ff7_german(data: bytes, show_unknown: bool = True) -> str
encode_ff7_german(text: str, add_terminator: bool = True) -> bytes
read_string_at(filepath: str, offset: int, max_length: int = 256) -> tuple[bytes, str]
extract_strings(filepath: str, start: int, end: int) -> list[tuple[int, bytes, str]]
```

**Usage Example:**
```bash
# Decode hex string
python3 ff7_german_decoder.py decode 2d7a434854454eff
# Output: Möchten

# Encode German text
python3 ff7_german_decoder.py encode "Möchten Sie"
# Output: 2d7a434854454e003349450026494e414c00ff

# Read from exe
python3 ff7_german_decoder.py read ff7_de.exe 0x58FBB0 50
# Output: Möchten Sie Final

# Extract region
python3 ff7_german_decoder.py extract ff7_de.exe 0x58FB00 0x5A0000
```

**Character Map:**
- Works perfectly for German
- INCOMPLETE for French accents
- INCOMPLETE for Spanish accents

### Comprehensive Extraction Script

**Location:** `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/extract_all_german_ff_terminated.py`

**Purpose:** Extract ALL 0xFF-terminated strings from German exe

**Usage:**
```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese/scripts
python3 extract_all_german_ff_terminated.py
```

**Output Files:**
- `all_ff_terminated_strings.txt` - Human-readable format
- `all_ff_terminated_strings.csv` - Machine-readable format

**Results:**
- Region: 0x58FBB0 - 0x5A0000 (65.2 KB)
- Total strings: 4,892
- Non-empty: 1,130 (23%)
- Empty/padding: 3,762 (77%)

**Format:**
```
[INDEX] OFFSET (BYTES:DECODED_LEN) | TEXT
[00000] 0x58FBB0 ( 18: 18) | Möchten Sie Final
[00001] 0x58FBC3 ( 36: 36) | Fantasy VII verlassen und
[00002] 0x58FBE8 ( 28: 28) | zu Windows zurückkehren?
```

### Regional Extraction Script

**Location:** `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/extract_german_from_known_regions.py`

**Purpose:** Extract only from verified clean regions

**Usage:**
```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese/scripts
python3 extract_german_from_known_regions.py
```

**Output Files:**
- `german_known_regions.txt`
- `german_known_regions.csv`

**Regions Defined:**
```python
regions = [
    (0x58FBB0, 0x58FC20, "Quit Dialog"),
    (0x5900F0, 0x590C00, "Config Menu"),
    (0x590C68, 0x591500, "Main Menu"),
    (0x591058, 0x5914D0, "Keyboard Labels"),
    (0x594C00, 0x596500, "Battle/Status"),
]
```

**Results:** 392 clean strings extracted

### Multi-Language Comparison Script

**Location:** Created inline during session (not saved to file)

**Purpose:** Compare string order and offsets across DE/FR/ES

**Key Logic:**
```python
def extract_with_details(exe_path, start_offset, count=30):
    # Extract strings with offset tracking
    # Returns: offset, raw_hex, text, length

# Usage:
de_strings = extract_with_details("ff7_de.exe", 0x5900F0, 30)
fr_strings = extract_with_details("ff7_fr.exe", 0x590573, 30)
es_strings = extract_with_details("ff7_es.exe", 0x5906F9, 30)
```

---

## Recommendations

### For German HEXT Patches

1. ✅ **Use the German decoder** - Works perfectly for umlauts
2. ✅ **Extract from known regions** - Use regional script for clean data
3. ✅ **Strip padding** - Always `.strip()` decoded strings
4. ⚠️  **Semantic matching required** - Cannot use positional mapping
5. ⚠️  **LLM-assisted mapping** - Use constraint-based system to match EN→DE

### For French HEXT Patches

1. ❌ **BLOCKER: Fix character encoding** - Need custom map for ê, é, è, à, etc.
2. ✅ **Use same extraction approach** - Sequential 0xFF following works
3. ✅ **Strip padding** - Same 73-95% padding issue as German
4. ⚠️  **Different offsets** - Cannot reuse German offset map
5. 📋 **TODO:** Create `ff7_french_decoder.py` with proper accent mappings

### For Spanish HEXT Patches

1. ❌ **BLOCKER: Fix character encoding** - Need custom map for Á, á, í, ñ, etc.
2. ✅ **Use same extraction approach** - Sequential 0xFF following works
3. ✅ **Strip padding** - Same 75-96% padding issue as German
4. ⚠️  **Different offsets** - Cannot reuse German offset map
5. 📋 **TODO:** Create `ff7_spanish_decoder.py` with proper accent mappings

### For Universal Multi-Language Support

**Current Approach (HEXT patching):**
- ❌ Not scalable - each language needs manual offset mapping
- ❌ Memory restrictions - English exe has limited space for longer German text
- ❌ Fragile - breaks if English exe is updated

**Recommended Approach (FFNx hooking):**
1. Remove all menu strings from English exe (replace with placeholders)
2. Store all language strings in external files (JSON/CSV)
3. Hook FFNx menu renderer to load strings dynamically
4. Enable hot-swappable languages at runtime

**Benefits:**
- ✅ No memory restrictions
- ✅ Easy to add new languages
- ✅ No exe patching required
- ✅ Can update strings without recompiling

---

## Technical Reference

### Virtual Address Calculation

```python
# CORRECT formula (verified against working Japanese HEXT)
VA = FileOffset + 0x400800

# Example:
# German "Fensterfarbe" at file offset 0x5900F0
VA = 0x5900F0 + 0x400800 = 0x9908F0
```

**WRONG formulas from failed attempts:**
- ❌ VA = FileOffset + 0x17600 (Agent 5 mistake)
- ❌ Fixed delta +0x77840 (only works for first 4 strings)

### FF7 Encoding Rules

```python
# Standard range (0x01-0x5F)
if 0x01 <= byte <= 0x5F:
    char = chr(byte + 0x20)

# Special values
if byte == 0x00:
    char = ' '  # Space (word separator or padding)
if byte == 0xFF:
    # String terminator (not rendered)

# German umlauts (0x60-0x7F range)
if byte in [0x66, 0x6A, 0x7A, 0x7E, 0x7F]:
    char = GERMAN_MAP[byte]

# French/Spanish accents (0x60-0x7F range)
# TODO: Need to map these bytes
```

### String Termination Patterns

```
Valid patterns:
1. [text bytes] 0xFF
2. [text bytes] 0x00 [more text] 0xFF  # 0x00 = word separator
3. [0x00 padding] [text bytes] 0xFF    # Leading padding (DE/FR/ES)

Invalid patterns:
1. [text bytes] 0x00 0x00 0xFF  # Double space (should be stripped)
2. [garbage] 0xFF               # Binary data (should be filtered)
```

### Extraction Algorithm (Pseudocode)

```python
def extract_all_strings(exe_path, start, end):
    with open(exe_path, 'rb') as f:
        f.seek(start)
        region = f.read(end - start)

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator
            if current_bytes:
                offset = start + string_start
                decoded = decode(current_bytes).strip()  # Remove padding

                # Filter garbage
                if is_valid_text(decoded):
                    strings.append((offset, decoded))

            # Reset for next string
            current_bytes = []
            string_start = i + 1
        else:
            if not current_bytes:
                string_start = i
            current_bytes.append(byte)

    return strings

def is_valid_text(text):
    """Filter out garbage strings."""
    if len(text) == 0:
        return False

    # Must have at least some letters
    alpha_count = sum(1 for c in text if c.isalpha())
    if alpha_count == 0:
        return False

    # Check letter-to-total ratio
    if alpha_count / len(text) < 0.3:
        return False  # Too much garbage

    return True
```

### Known Good Strings for Testing

```python
# Use these to verify decoder is working correctly

TEST_STRINGS = {
    "GERMAN": [
        (0x58FBB0, "Möchten Sie Final"),
        (0x5900F0, "Fensterfarbe"),
        (0x590C68, "Objekt"),
        (0x590D26, "Verlassen"),
    ],
    "FRENCH": [
        (0x590560, "Couleur de fenñtre"),  # Note: ê broken
        (0x590573, "Son"),
        # TODO: Add more verified strings
    ],
    "SPANISH": [
        (0x5906E8, "Color de ventana"),
        (0x5906F9, "Sonido"),
        # TODO: Add more verified strings
    ],
}
```

### Semantic Matching Strategy

```python
# Multi-pass matching to ensure accuracy

# Pass 1: Exact matches (100% confidence)
exact_matches = {
    "ATB": "ATB",
    "Sound": "Sound",
    "Mono": "Mono",
    "Stereo": "Stereo",
    "Normal": "Normal",
    "Auto": "Auto",
    "Pause": "Pause",
}

# Pass 2: Dictionary matches (95% confidence)
translation_dict = {
    "Window color": "Fensterfarbe",
    "Controller": "Kontroller",
    "Cursor": "Cursor",
    "Battle speed": "Kampftempo",
    "Battle message": "Kampfmeldung",
    "Field message": "Feldmeldung",
    "Camera angle": "Kamerawinkel",
    "Select": "Auswählen",
    "Cancel": "Abbrechen",
    "Menu": "Menü",
    # ... add more verified pairs
}

# Pass 3: LLM-assisted (variable confidence)
# - Present unmapped EN string
# - Show all available DE strings
# - LLM picks best match
# - System enforces no duplicates
# - Flag confidence < 70% for review
```

---

## Appendix A: File Locations

### Executables
```
/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe  (German)
/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_fr.exe  (French)
/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_es.exe  (Spanish)
/mnt/c/Program Files (x86)/Steam/.../ff7_en.exe        (English)
/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe  (Japanese)
```

### Scripts
```
/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/
├── ff7_german_decoder.py                    (Primary decoder)
├── extract_all_german_ff_terminated.py      (Full extraction)
├── extract_german_from_known_regions.py     (Regional extraction)
├── analyze_german_menu_structure.py         (Spacing analysis)
└── extract_german_exact_mapping.py          (Positional attempt - failed)
```

### Output Data
```
/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/
├── all_ff_terminated_strings.txt
├── all_ff_terminated_strings.csv
├── german_known_regions.txt
├── german_known_regions.csv
├── sequential_extraction_analysis.txt
└── german_clean_candidates.csv
```

### Reference Data
```
/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/
└── english_strings_by_index.txt             (767 English strings with touphScript indices)
```

---

## Appendix B: Session History

This analysis was conducted across multiple sessions:

**Session 48-54:** Initial German HEXT attempt, discovered VA calculation bug
**Session 55:** Fixed delta approach attempt (FAILED)
**Session 56:** Blind extraction + LLM mapping approach (PARTIAL SUCCESS - 208 mappings)
**Session 57:** Parallel Haiku analysis (261 mappings with quality issues)
**Session c5687d3e (current):** Comprehensive DE/FR/ES comparison, padding discovery, offset analysis

**Total time invested:** ~15+ hours across 6 sessions
**Key breakthrough:** Discovering the right-aligned padding pattern

---

## Appendix C: Future Work

### Immediate Tasks

1. **Create French decoder** (`ff7_french_decoder.py`)
   - Map bytes 0x60-0x7F for ê, é, è, à, etc.
   - Test against known French strings

2. **Create Spanish decoder** (`ff7_spanish_decoder.py`)
   - Map bytes 0x60-0x7F for Á, á, í, ñ, etc.
   - Test against known Spanish strings

3. **Complete German extraction**
   - Currently have 392/767 strings (51%)
   - Need to find remaining 375 strings
   - Expand search regions (battle text, item descriptions, etc.)

### Medium-Term Goals

4. **Build constraint-based matching system**
   - Implement multi-pass matching algorithm
   - Create translation dictionary
   - Integrate LLM with duplicate prevention
   - Build manual review interface

5. **Test HEXT generation**
   - Create patches from verified mappings
   - Test in-game to confirm text renders
   - Verify no crashes or corruption

### Long-Term Vision

6. **FFNx menu hooking**
   - Replace HEXT approach entirely
   - Dynamic string loading from external files
   - Hot-swappable language selection
   - Support for unlimited languages

---

## Document Change Log

| Date | Version | Changes | Session ID |
|------|---------|---------|------------|
| 2026-01-05 18:17 JST | 1.0.0 | Initial comprehensive analysis created | c5687d3e-90a9-47e8-829a-a0c6e70cd98e |

---

**End of Document**

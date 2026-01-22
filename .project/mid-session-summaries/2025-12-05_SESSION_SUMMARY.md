# Mid-Session Summary: FF7 Japanese Mod - Multi-Language Architecture

**Created:** 2025-12-05 12:15 JST (Friday)
**Session-ID:** c245e7c0-ec73-4933-b925-5976860e742c
**Context Remaining:** ~50,000 tokens

---

## Session Overview

This session continued work on the FF7 Japanese language mod, evolving from specific menu patching into broader multi-language architecture planning.

---

## Completed Work

### 1. Field Dialogue Fix

**Problem:** Field dialogue wasn't displaying in Japanese despite `ff7_japanese_edition = true`.

**Root Cause:** FFNx only redirects `menu_us.lgp` → `menu_ja.lgp`, but does NOT redirect `flevel.lgp` → `jfleve.lgp`.

**Solution:** Renamed Japanese field file to replace English:
```bash
mv flevel.lgp flevel_en.lgp  # Backup English
cp jfleve.lgp flevel.lgp     # Japanese becomes default
```

**Documentation:** Created `docs/FIELD_DIALOGUE_SETUP.md`

### 2. Screen Analysis - Three-Way Comparison Workflow

Established workflow comparing:
1. English version screenshot
2. Japanese-patched English exe screenshot
3. Actual Japanese version screenshot

**Screens Analyzed:**
- **Config Screen** - Complete text mapping, identified "Controller" → "キーボード" (Keyboard) difference
- **Limit Screen** - Found Set/Check strings, LEVEL uses fullwidth English
- **Exit Screen** - Found Yes/No (はい/いいえ) locations

### 3. Sub-Agent String Search

Dispatched parallel agents to search both executables:

**Japanese exe findings (confirmed):**
| String | Japanese | File Offset |
|--------|----------|-------------|
| Yes | はい | 0x518fd0 |
| No | いいえ | 0x518fd4 |
| Set | セット | 0x51eb80 |
| Check | チェック | 0x51ebb0 |
| Keyboard | キーボード | 0x519500 |

**Key Discovery:** English and Japanese exes have **different string layouts**. Strings are not at corresponding offsets - requires per-exe mapping.

### 4. Executable Structure Analysis

| Executable | Size | Structure |
|------------|------|-----------|
| ff7_en.exe (Steam) | 6.4MB | Simple, .data at 0x3B8A00 |
| ff7_ja.exe | 24MB | Complex, extra sections (Stext, Sitext, Srdata) |
| ff7_es.exe | 24MB | Same as Japanese structure |
| ff7_de.exe | 24MB | Same as Japanese structure |
| ff7_fr.exe | 24MB | Same as Japanese structure |

**Insight:** Steam English exe is remastered version; others are original 1998 releases.

---

## Architecture Decision: Unicode Texture Approach

### The Problem
- FF7 uses 1-byte indices into font textures (max 256 chars × 6 textures = 1,536 chars)
- Japanese kanji needs 2,000-3,000+ characters
- Want to support additional languages (Chinese, Arabic, Polish, etc.)

### Proposed Solution: Compatibility Layer

Rather than modifying FFNx's text rendering:

1. **Create new Unicode font textures** - Render from modern fonts (Noto Sans CJK, etc.)
2. **Maintain same grid positions** - Byte 0x5A still means position 90 in jafont_1
3. **Add extended textures** - jafont_7, jafont_8, etc. for additional characters
4. **Use existing mapping** - Our Unicode CSV maps old indices to codepoints

```
Old FF7 byte index → Unicode mapping (CSV) → New Unicode texture → Rendered glyph
```

**Benefits:**
- No FFNx code changes for basic functionality
- Backwards compatible with existing text
- Higher quality font rendering
- Expandable character set

---

## Pending Tasks

### Task 1: Complete Executable Mapping

**Goal:** Extract all hardcoded strings from all 5 language executables.

**Output:** CSV files per language:
```csv
language,file_offset,virtual_address,raw_bytes,decoded_text,string_length
```

**Executables:**
- `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe`
- `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe`
- `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_es.exe`
- `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe`
- `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_fr.exe`

**Why:** Preserve original translations, identify structural differences, document character sets.

### Task 2: Verify FFNx Extended Font Support

**Goal:** Confirm FFNx can load font textures beyond jafont_6.

**Approach:**
1. Check FFNx source code for font loading logic
2. Test with a dummy jafont_7.png
3. Document prefix byte requirements (FA-FE used, what about FF?)

### Task 3: Proof-of-Concept Texture Generator

**Goal:** Script that generates font texture PNGs from:
- Input: TTF/OTF font file + Unicode mapping CSV
- Output: PNG atlas matching jafont grid layout (12×21 grid, 256 positions)

---

## Existing Tools Assessment

| Tool | Purpose | Useful for Exe Strings? |
|------|---------|------------------------|
| touphScript | Game text/dialogue editing | No - field/kernel only |
| Makou Reactor | Field editor | No - field files only |
| WallMarket | KERNEL.BIN editor | No - kernel only |
| DLPB Tools | Hex editing | Possibly |

**Conclusion:** No existing tool specifically extracts hardcoded exe strings. Custom script needed.

---

## Key File Locations

### Project Files
- `docs/MENU_TEXT_ADDRESS_MAP.md` - Address reference (updated this session)
- `docs/FIELD_DIALOGUE_SETUP.md` - Field dialogue fix documentation
- `docs/HEXT_PATCHING_GUIDE.md` - HEXT workflow guide
- `docs/FFNX_DIRECTORY_STRUCTURE.md` - Directory layout reference
- `docs/character_maps/ff7_complete_mapping_compact.csv` - Japanese character mapping

### Game Files
- English exe: `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe`
- Japanese exe: `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe`
- HEXT patches: `/mnt/c/.../hext/ff7/ja/japanese_menu.txt`
- Field data: `/mnt/c/.../data/field/flevel.lgp` (now Japanese)

### FFNx Source
- `/home/johnzealanddoyle/projects/ff7OG_japanese/FFNx-PR737/`

---

## Technical Reference

### Address Calculation Formula
```
Virtual Address = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000
```

### FF7 Text Encoding
- **English:** Shifted ASCII (char + 0x20), A=0x21, B=0x22...
- **Japanese:** Custom jafont indices, see CSV mapping
- **Terminator:** 0xFF marks end of string

### Japanese Font Texture Prefixes
- jafont_1: No prefix (indices 0x00-0xFF)
- jafont_2: FA prefix
- jafont_3: FB prefix
- jafont_4: FC prefix
- jafont_5: FD prefix
- jafont_6: FE prefix

---

## Next Steps (Priority Order)

1. **Write string extraction script** - Python, scans .data section, outputs CSV
2. **Run on all 5 executables** - Generate comprehensive string maps
3. **Verify FFNx font loading** - Check source for texture limit
4. **Create texture generator PoC** - TTF → PNG atlas

---

## Session Handoff Notes

If context runs out:
1. This summary contains full state
2. Extraction script should be straightforward Python
3. CSV output format defined above
4. All 5 exe paths documented
5. Character mapping CSV exists at `docs/character_maps/ff7_complete_mapping_compact.csv`

# FF7 String Analysis - Session 2026-01-07

**Created:** 2026-01-07 22:47 JST
**Session ID:** dd75b404-08f7-4cdc-b7d6-2f78c10a962e

This directory contains analysis and corrected files from a comprehensive FF7 English executable string comparison and decoding session.

---

## Files in This Directory

### 1. `english_strings_by_index_v2_corrected.csv`
**Full corrected English string extraction** (767 entries)
- Original source: `../english_strings_by_index_v2.csv`
- Corrections: 13 entries properly decoded with FF7 text encoding
- All entries now match touphScript extraction exactly

### 2. `ff7_corrected_13_entries.csv`
**Detailed breakdown of the 13 corrected entries**
- Shows original CSV text vs properly decoded text
- Includes hex bytes and offsets
- Explains why each needed correction

### 3. `ff7_string_comparison_report.md`
**Comparison report between touphScript TXT and manual CSV**
- Analyzes 767 TXT entries vs 746 CSV rows
- Identifies 90% coverage
- Categorizes missing entries (naming chars, numbers, etc.)

### 4. `missing_73_entries_found.md`
**Status report on 70 entries missing from manual CSV**
- 57 found directly in v2 CSV
- 13 found but needed FF7 decoding
- All 70/70 accounted for

### 5. `ff7_text_decoding_summary.md`
**Complete documentation of FF7 text decoding**
- Explains FF7 character encoding (0x00 = space, 0x0B-0x1B = punctuation, etc.)
- Shows before/after examples
- Provides FF7 character map reference

---

## Key Findings

### Issue 1: Control Characters (6 entries)
FF7 stores punctuation as control bytes:
- `,` `.` `+` `-` `:` `;` were shown as `[CTRL:0C]` etc.

### Issue 2: Space Separator (6 entries)
FF7 uses `0x00` as space, not terminator:
- Two-word item names were truncated: `Enemy Away` → `Enemy`

### Issue 3: Special Characters (1 entry)
Custom codes for quotes/ellipsis:
- `Sephiroth"……"` was shown as `Sephiroth[B2][A9][A9][B3]`

---

## Source Files Compared

1. **touphScript extraction**: `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_text/0_ff7.exe.txt` (767 entries)

2. **Manual EN/DE mapping**: `/mnt/c/Users/johnz/Desktop/ff7_en_de_mapping (1).csv` (746 rows)

3. **Agent2 extraction**: `../english_strings_by_index_v2.csv` (767 entries)

---

## Results

✅ **All 767 entries properly decoded**
✅ **100% coverage of touphScript extraction**
✅ **13 encoding issues resolved**

---

## Related Documentation

- Parent directory: `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/`
- touphScript repository: `/home/johnzealanddoyle/projects/tools/touphscript`
- FF7Scarlet source: `https://github.com/petfriendamy/ff7-scarlet`

---

*Analysis performed by Claude Code - Session dd75b404-08f7-4cdc-b7d6-2f78c10a962e*

# FF7 Text Decoding - Summary Report

**Date:** 2026-01-07 22:43 JST
**Session:** dd75b404-08f7-4cdc-b7d6-2f78c10a962e

---

## What Was Done

Successfully decoded 13 FF7 text entries that were incorrectly parsed in the original `english_strings_by_index_v2.csv`.

## Files Created

1. **`ff7_corrected_13_entries.csv`** - Detailed breakdown of the 13 corrected entries
2. **`english_strings_by_index_v2_corrected.csv`** - Full corrected CSV (767 entries)

## The Problem

The original CSV parser didn't properly handle FF7's custom text encoding:

### Issue 1: Control Characters (6 entries)
FF7 stores naming screen punctuation as single control bytes, not ASCII:

| Character | Hex | CSV Showed | Now Shows |
|-----------|-----|------------|-----------|
| `,` | 0x0C | `[CTRL:0C]` | `,` |
| `.` | 0x0E | `[CTRL:0E]` | `.` |
| `+` | 0x0B | `[CTRL:0B]` | `+` |
| `-` | 0x0D | `[CTRL:0D]` | `-` |
| `:` | 0x1A | `[CTRL:1A]` | `:` |
| `;` | 0x1B | `[CTRL:1B]` | `;` |

### Issue 2: Space Separator (6 entries)
FF7 uses `0x00` as a **space character**, not a string terminator. Two-word item names were truncated:

| Full Name | CSV Showed | Now Shows |
|-----------|------------|-----------|
| Enemy Away | `Enemy` | `Enemy Away` |
| Sneak Attack | `Sneak` | `Sneak Attack` |
| Swift Bolt | `Swift` | `Swift Bolt` |
| Fire Veil | `Fire` | `Fire Veil` |
| Turbo Ether | `Turbo` | `Turbo Ether` |
| Ice Crystal | `Ice` | `Ice Crystal` |

### Issue 3: Special Characters (1 entry)
FF7 uses custom codes for quotes and ellipsis:

| Text | CSV Showed | Now Shows |
|------|------------|-----------|
| Sephiroth"……" | `Sephiroth[B2][A9][A9][B3]` | `Sephiroth"……"` |

Where:
- `0xB2` = `"` (left quote)
- `0xA9` = `…` (ellipsis)
- `0xB3` = `"` (right quote)

---

## FF7 Character Encoding Map (Partial)

```
0x00 = ' '  (space)
0x0B = '+'  (plus)
0x0C = ','  (comma)
0x0D = '-'  (minus)
0x0E = '.'  (period)
0x1A = ':'  (colon)
0x1B = ';'  (semicolon)
0x21-0x3A = 'A'-'Z'
0x41-0x5A = 'a'-'z'
0xA9 = '…'  (ellipsis)
0xB2 = '"'  (left quote)
0xB3 = '"'  (right quote)
0xFF = string terminator
```

---

## Corrections Applied

### Example 1: Punctuation
```
Index: 500
Offset: 0x0052078B
Hex: 0E
Before: "[CTRL:0E]"
After:  "."
```

### Example 2: Two-Word Item
```
Index: 712
Offset: 0x0057B4C0
Hex: 25 4E 45 4D 59 00 21 57 41 59 FF FF FF FF FF FF
Decoded: E N E M Y [space] A W A Y
Before: "Enemy"
After:  "Enemy Away"
```

### Example 3: Special Characters
```
Index: 371
Offset: 0x0051F584
Hex: 33 45 50 48 49 52 4F 54 48 B2 A9 A9 B3 FF
Decoded: S e p h i r o t h " … … "
Before: "Sephiroth[B2][A9][A9][B3]"
After:  "Sephiroth"……""
```

---

## Verification

All 13 entries were successfully decoded and verified:
- ✅ 6/6 punctuation marks decoded correctly
- ✅ 6/6 two-word item names decoded correctly
- ✅ 1/1 special character string decoded correctly

**Total: 13/13 successful (100%)**

---

## Recommendations

For future FF7 text extraction:

1. **Always treat `0x00` as a space**, not a terminator
2. **Use the full FF7 character map** for decoding (not ASCII)
3. **Continue reading until `0xFF`** (the actual terminator)
4. **Decode special characters** like `0xA9` (ellipsis) and `0xB2`/`0xB3` (quotes)

---

## Files Reference

- **Original CSV**: `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index_v2.csv`
- **Corrected CSV**: `C:\Users\johnz\Desktop\english_strings_by_index_v2_corrected.csv`
- **Correction Details**: `C:\Users\johnz\Desktop\ff7_corrected_13_entries.csv`
- **This Report**: `C:\Users\johnz\Desktop\ff7_text_decoding_summary.md`

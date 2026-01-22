# FF7 English Extraction Issues Analysis

**Created:** 2026-01-06 21:45 JST (Tuesday)
**Session-ID:** 47cf5a76-efc5-46cc-aa3c-d372f1a897e1
**Continuation of:** Session 60 (German Extraction Analysis)

---

## Executive Summary

The English string extraction from `ff7_en.exe` has encoding detection issues similar to (but different from) the German extraction:

| Issue | Affected Entries | Problem | Solution |
|-------|------------------|---------|----------|
| UNICODE garbage | 9 | Character names shown as CJK | FF7 decode instead |
| UNICODE single-byte | ~59 | Naming screen chars as `[UNICODE:XX]` | FF7 decode each byte |
| 3AVE/,EVEL | 9 | FF7 strings shown as ASCII | FF7 decode instead |
| QstN/RndN etc. | 9 | ASCII strings FF7-decoded | ASCII decode instead |
| NOFF_TERM | 3 | Binary data detected as strings | Exclude entirely |

**Total corrections needed: ~89 entries**

---

## Issue 1: UNICODE Character Names (0x520700-0x520768)

### The Problem
9 entries at the naming screen character selection area are shown as Unicode garbage (CJK characters) instead of English names.

### What Happened
The extraction script tried to interpret byte pairs as UTF-16 characters, producing garbage like `䄣呉㌀呉ｈ` instead of recognizing them as FF7-encoded bytes.

### Corrected Values

| Index | Offset | Wrong (Unicode) | Correct (FF7) |
|-------|--------|-----------------|---------------|
| 464 | 0x520700 | 䄣呉㌀呉ｈ | Cait Sith |
| 465 | 0x52070C | 䤶䍎久ｔ | Vincent |
| 466 | 0x520718 | 䤣ｄ | Cid |
| 467 | 0x520724 | 䠣䍏ｏ | Choco |
| 468 | 0x520748 | 倳䍁ｅ | Space |
| 469 | 0x520750 | 䔤䕌䕔ÿ | Delete |
| 470 | 0x520758 | 䔳䕌呃ÿ | Select |
| 471 | 0x520760 | 䔤䅆䱕ｔ | Default |
| 472 | 0x520768 | 䄣䍎䱅ÿ | Cancel |

### Hex Proof
```
0x520700: 23 41 49 54 00 33 49 54 48 FF
FF7 decode: C a i t [space] S i t h [end]
  0x23+0x20=0x43='C', 0x41+0x20=0x61='a', etc.
```

---

## Issue 2: Single-Byte UNICODE Entries (0x520770-0x5207AC)

### The Problem
~59 single-byte entries shown as `[UNICODE:21]`, `[UNICODE:22]` etc. instead of their FF7-decoded characters.

### What These Actually Are
These are the **naming screen character palette** - the selectable characters for naming Cloud, Barret, etc.

### Correct Mapping

**Numbers/Symbols (0x21-0x3A):**
```
0x21 → 'A' (0x21+0x20=0x41)
0x22 → 'B'
...
0x39 → 'Y'
0x3A → 'Z'
```

**Lowercase Letters (0x41-0x5A):**
```
0x41 → 'a' (0x41+0x20=0x61)
0x42 → 'b'
...
0x5A → 'z'
```

**Control Codes (0x0B-0x10, 0x1A-0x1B):**
These are cursor movement / special function codes - not displayable characters.

---

## Issue 3: '3AVE' Should Be 'SAVE' (0x524B30-0x524BF0)

### The Problem
Save slot labels shown as `3AVE [13]`, `3AVE [14]` instead of `Save 3`, `Save 4` etc.
Also `LEVEL` shown as `,EVEL`.

### Root Cause
The RGB type detection assumed ASCII encoding, but these ARE FF7-encoded strings.

### Hex Proof
```
0x524B30: 33 41 56 45 00 13 00 00 00 FF
ASCII:  '3' 'A' 'V' 'E' [nul] [19] ...  = "3AVE" + slot number
FF7:    'S' 'a' 'v' 'e' [space] '3'     = "Save 3" ✓

0x33 in FF7 = 0x33 + 0x20 = 0x53 = 'S'
0x41 in FF7 = 0x41 + 0x20 = 0x61 = 'a'
0x13 in FF7 = 0x13 + 0x20 = 0x33 = '3'
```

### Corrected Values

| Index | Offset | Wrong (ASCII) | Correct (FF7) |
|-------|--------|---------------|---------------|
| 649 | 0x524B30 | 3AVE [13] | Save 3 |
| 650 | 0x524B3C | 3AVE [14] | Save 4 |
| 651 | 0x524B48 | 3AVE [15] | Save 5 |
| 652 | 0x524B54 | 3AVE [16] | Save 6 |
| 653 | 0x524B60 | 3AVE [17] | Save 7 |
| 654 | 0x524B6C | 3AVE [18] | Save 8 |
| 655 | 0x524B78 | 3AVE [19] | Save 9 |
| 656 | 0x524B84 | 3AVE [11][10] | Save 10 |
| 657 | 0x524BF0 | ,EVEL | Level |

---

## Issue 4: Racing Positions ARE ASCII (0x555880-0x5558CC)

### The Problem
Chocobo racing position strings shown as garbage like `QstN`, `RndN`, `SrdN` instead of `1ST.`, `2ND.`, `3RD.`.

### Root Cause
The FFPADDED type applied FF7 decoding to these strings, but they're actually plain ASCII!

### Hex Proof
```
0x5558AC: 31 53 54 2E 00 00 00 00
ASCII: '1' 'S' 'T' '.' = "1ST." ✓
FF7:   'Q' 's' 't' 'N' = "QstN" ✗

0x31 in ASCII = '1'
0x31 in FF7 = 0x31 + 0x20 = 0x51 = 'Q'
```

### Corrected Values

| Index | Offset | Wrong (FF7) | Correct (ASCII) |
|-------|--------|-------------|-----------------|
| 687 | 0x555880 | OSP@ptsN | /30 PTS. |
| 688 | 0x55588C | OTP@ptsN | /40 PTS. |
| 689 | 0x555898 | OC@ptsN | /# PTS. |
| 690 | 0x5558A0 | OC@ptsN | /# PTS. |
| 691 | 0x5558AC | QstN | 1ST. |
| 692 | 0x5558B4 | RndN | 2ND. |
| 693 | 0x5558BC | SrdN | 3RD. |
| 694 | 0x5558C4 | TthN | 4TH. |
| 695 | 0x5558CC | UthN | 5TH. |

---

## Issue 5: NOFF_TERM Entries (0x519238-0x519244)

### The Problem
3 entries contain bytes > 0x7F (0xC5, 0xB8, 0xB7, 0xBA, 0xC1, 0xBF, 0xC8) which are outside the FF7 encoding range.

### What These Are
These are NOT text strings. They're binary data (possibly):
- Color palette values
- Configuration data
- Pointer tables

### Action Required
**EXCLUDE** these entries from the string extraction entirely.

| Index | Offset | Raw Bytes | Action |
|-------|--------|-----------|--------|
| 33 | 0x519238 | C5 B8 B7 FF | EXCLUDE |
| 34 | 0x51923E | BA C5 B8 B8 C1 FF | EXCLUDE |
| 35 | 0x519244 | B5 BF C8 B8 FF | EXCLUDE |

---

## Encoding Detection Rules (For Future Extraction)

### How to Determine Encoding

1. **Check byte range first:**
   - Bytes > 0x7F (except 0xFF terminator) = NOT FF7 text → check if ASCII or exclude
   - Bytes 0x00-0x7F = could be FF7 or ASCII

2. **Check memory region:**
   - 0x519FE0-0x51A??? = Keyboard keys (ASCII)
   - 0x520700-0x520768 = Naming screen names (FF7)
   - 0x520770-0x5207AC = Naming screen characters (FF7 single bytes)
   - 0x524B30-0x524BF0 = Save slots (FF7)
   - 0x555880-0x5558CC = Racing strings (ASCII)

3. **Heuristic for unknown regions:**
   - If first byte is 0x20-0x7E and makes ASCII sense → ASCII
   - If first byte is 0x01-0x5F and byte+0x20 makes sense → FF7
   - If string contains 0x00 as space delimiter → FF7
   - If string ends with 0xFF → FF7-style termination

### Memory Region Summary

| Start | End | Encoding | Content |
|-------|-----|----------|---------|
| 0x518370 | 0x519237 | FF7 | Menu strings |
| 0x519238 | 0x519287 | BINARY | Skip (not text) |
| 0x519288 | 0x519FDF | FF7 | More menu strings |
| 0x519FE0 | 0x51A??? | ASCII | Keyboard keys |
| 0x520700 | 0x520768 | FF7 | Naming screen names |
| 0x520770 | 0x5207AC | FF7 | Naming screen chars |
| 0x524B30 | 0x524BF0 | FF7 | Save slot labels |
| 0x555880 | 0x5558CC | ASCII | Racing positions |
| 0x57B2A8 | 0x57???? | FF7 | Battle items (TEIOH etc.) |

---

## Comparison with German Extraction Issues

| Issue | English | German | Similar? |
|-------|---------|--------|----------|
| Character map bug | No | Yes (0x65=Ö not å) | Different |
| Boundary detection | No | Yes (8x 0xFF gaps) | Different |
| Mixed encoding regions | Yes | Yes | Same! |
| Keyboard = ASCII | Yes | Yes | Same! |
| Racing positions = ASCII | Yes | Yes | Same! |
| Binary data as strings | Yes | Not documented | Similar |

**Key Insight:** Both English and German have the same fundamental issue - **mixed encoding regions** where some areas are FF7-encoded and others are plain ASCII. The extraction scripts need region-aware encoding detection.

---

## Files Referenced

- Source: `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe`
- Extraction output: `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt`

---

## Verification Commands

```bash
# Check raw bytes at a specific offset
xxd -s 0x520700 -l 32 "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"

# Find ASCII racing strings
xxd "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe" | grep -i "1ST\."

# Count problematic entries
grep -c "UNICODE\|3AVE\|QstN\|NOFF_TERM" english_strings_by_index.txt
```

---

## Recommended Fixes

1. **Immediate:** Create corrected CSV with proper decoding for affected entries
2. **Script Update:** Add region-based encoding detection to extraction script
3. **Validation:** Add byte-range check to exclude non-text data (bytes > 0x7F except 0xFF)

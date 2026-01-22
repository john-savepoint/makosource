# German Adaptation Requirements

**Created:** 2026-01-02 21:05 JST
**Session ID:** c31eb494-cb6d-474e-8432-4bc1284b2ed0
**Based on:** Japanese HEXT methodology analysis

## 1. Executive Summary

The Japanese HEXT generator works because of a **consistent offset delta** (0xC00) between EN and JA exe strings. German CANNOT use this approach because German strings are at **unpredictable offsets** relative to English.

This document outlines what changes are needed to adapt the methodology for German.

---

## 2. Critical Difference: No Consistent Offset Delta

### Japanese Approach (Works)
```python
JA_OFFSET_DELTA = 0xC00  # Consistent for ALL strings
ja_offset = en_offset + JA_OFFSET_DELTA
```

### German Approach (Required)
```python
# NO CONSISTENT DELTA - Must use anchor-based mapping
de_offsets = {}  # Dict mapping index -> DE offset
# Populated by matching known strings between EN and DE exes
```

### Why German Is Different

1. **JA exe:** Identical structure to EN, with 0xC00 bytes inserted early in the file
2. **DE exe:** Strings reorganized, different lengths, different positions
3. **Result:** Each string must be individually mapped

---

## 3. Anchor-Based Mapping Strategy

### Step 1: Extract DE Strings

Use a script similar to the existing extraction tools:
```python
# Pseudocode
de_strings = extract_strings_from_de_exe(de_exe_path)
# Returns: {file_offset: (raw_bytes, decoded_text)}
```

### Step 2: Match to EN Strings Using Anchors

Find "anchor" strings that are:
- Unique in both EN and DE
- Have identical or very similar content
- Are at known EN offsets

Example anchors:
| EN Text | DE Text | EN Offset | Purpose |
|---------|---------|-----------|---------|
| "ATB" | "ATB" | 0x518968 | Config menu |
| "LV" | "LV" | (varies) | Level label |
| "HP" | "TP" | (varies) | Status |

### Step 3: Calculate Relative Positions

Once anchors are matched, infer positions of surrounding strings:
```python
# If EN index 10 is at EN offset X and DE offset Y
# And EN index 11 is at EN offset X + 48
# Then DE index 11 is likely at DE offset Y + (similar length)
```

**Warning:** This may not work if string lengths differ significantly.

### Step 4: Validate All Mappings

For each mapped string:
1. Read bytes at calculated DE offset
2. Decode and verify it matches expected German text
3. Flag mismatches for manual review

---

## 4. German Special Characters

### Character Codes on jafont_1

| Character | Byte Code | Position | Note |
|-----------|-----------|----------|------|
| ö | 0x6A | 106 | Lowercase o-umlaut |
| ü | 0x7A | 122 | Lowercase u-umlaut |
| Ü | 0x7F | 127 | Uppercase U-umlaut |
| ß | 0x7E | 126 | Eszett |
| ä | ? | ? | Needs verification |
| Ä | ? | ? | Needs verification |
| Ö | ? | ? | Needs verification |

### Encoding Implications

1. **DEF strings:** German special characters use standard jafont_1 positions
2. **RGB strings:** May cause issues - RGB formula could overflow for high byte values

### RGB Overflow Risk

```python
# RGB formula: byte + 0x93
# ö (0x6A) + 0x93 = 0xFD (valid)
# ü (0x7A) + 0x93 = 0x10D (OVERFLOW!)
```

**Solution:** German keyboard labels may need special handling to avoid RGB encoding, or use alternative character codes.

---

## 5. Skip Regions for German

The same skip regions likely apply:

```python
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry characters (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals (keep English: 1st, 2nd, 3rd)
SKIP_REGIONS.update(range(712, 758))   # Jockey names (keep English)

# RGB skip regions - timing formats likely identical
RGB_SKIP_REGIONS = set(range(658, 687))
```

### Potential Difference: Race Ordinals

German might use:
- "1.", "2.", "3." instead of "1st", "2nd", "3rd"

If so, these might need patching instead of skipping.

---

## 6. Keyboard Region Handling

### Does German Need +0x20 Offset?

**Unknown - requires testing.**

The +0x20 offset compensates for the game's -0x20 transformation on keyboard labels. This may be:
1. **Universal:** Applies to all languages → German needs +0x20
2. **JA-specific:** Only applies to Japanese font rendering → German may not need it

### Testing Approach

1. Patch German keyboard labels WITHOUT +0x20
2. Test in-game keyboard configuration screen
3. If labels are shifted, apply +0x20
4. Document findings

### German Keyboard Special Characters

If German keyboard uses ö, ä, ü for key names:
```
# Potential keyboard labels with special chars
# "ÖFFNEN" (Open) - if used as key label
# "LÖSCHEN" (Delete) - if used as key label
```

These need careful handling because:
1. High byte values (0x6A+) may overflow with RGB + 0x93
2. +0x20 offset could push them even higher

---

## 7. Spacing Adjustments

German words are often longer than English equivalents. Spacing fixes may differ:

### Shop Menu Example

| Language | Text | Width |
|----------|------|-------|
| EN | "Buy   Sell     Exit" | 20 chars |
| JA | "かう　うる　でる" | 9 chars |
| DE | "Kaufen Verkaufen Verlassen" | ~26 chars |

**Problem:** German text may be LONGER than the allocated space.

**Solutions:**
1. Abbreviate: "Kauf  Verk  Ende" (ugly)
2. Accept overflow (may cause visual issues)
3. Use shorter translations if available in DE exe

### Item/Materia Column

Similar issue - German column headers may not fit:
- EN: "Item      Materia" (17 chars)
- DE: "Gegenstand  Materia" (19+ chars)

---

## 8. Required Scripts/Tools for German

### 1. german_string_extractor.py

```python
# Extract all strings from DE exe
# Map to file offsets
# Decode using German character map
```

### 2. german_anchor_mapper.py

```python
# Match EN strings to DE strings using anchors
# Build de_offset_table: {index: de_offset}
# Handle cases where strings don't align
```

### 3. generate_german_hext.py

```python
# Similar structure to generate_exe_hext.py
# Key differences:
# - Use anchor-based mapping instead of delta
# - Handle German special characters
# - Different spacing calculations
# - Skip regions may differ
```

### 4. german_character_map.csv

```csv
texture,index,character
jafont_1,106,ö
jafont_1,122,ü
jafont_1,126,ß
jafont_1,127,Ü
...
```

---

## 9. Step-by-Step Implementation Plan

### Phase 1: Analysis (Agent 4 work)
1. Extract all strings from DE exe
2. Map special character positions
3. Compare string positions to EN
4. Document the offset patterns (or lack thereof)

### Phase 2: Mapping
1. Implement anchor-based string matching
2. Build complete de_offset_table
3. Validate all mappings against DE exe content
4. Flag problematic entries

### Phase 3: Generator Development
1. Fork generate_exe_hext.py as generate_german_hext.py
2. Replace delta-based lookup with table lookup
3. Implement German character encoding
4. Adjust spacing functions for German text

### Phase 4: Testing
1. Generate German HEXT patches
2. Test in-game with German language
3. Fix keyboard offset issues if present
4. Adjust spacing as needed

### Phase 5: Refinement
1. Handle edge cases
2. Optimize output
3. Document all German-specific behaviors

---

## 10. Summary Comparison Table

| Aspect | Japanese | German |
|--------|----------|--------|
| Offset calculation | Delta (0xC00) | Anchor-based mapping |
| Special characters | Hiragana/Katakana on jafont | ö, ü, ß at specific positions |
| Keyboard +0x20 | Yes, required | Unknown, test required |
| RGB encoding | Works for fullwidth | May overflow for special chars |
| Spacing | Shorter than EN | Often longer than EN |
| Skip regions | Same as EN | Likely same, verify ordinals |
| String alignment | Guaranteed | Unpredictable |

---

## 11. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| No consistent offset delta | Cannot auto-map | Anchor-based mapping |
| German text too long | Overflow/clipping | Abbreviation or different translation |
| RGB overflow for ö/ü | Display corruption | Special character handling |
| Keyboard offset unknown | Wrong labels | In-game testing |
| Anchor matching fails | Incomplete mapping | Manual verification |

---

## 12. Conclusion

German HEXT generation is more complex than Japanese because of the lack of consistent offset delta. The key requirements are:

1. **Anchor-based mapping** instead of delta calculation
2. **Special character handling** for ö, ü, ß
3. **Different spacing** for longer German words
4. **Testing** for keyboard +0x20 requirement
5. **Validation** of all string mappings

The methodology from the Japanese generator provides a solid foundation, but significant adaptation is needed for German.

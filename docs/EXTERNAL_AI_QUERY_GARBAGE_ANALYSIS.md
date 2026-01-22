# Query for External AI: FF7 Garbage String Analysis

**Date:** 2026-01-05 20:43 JST
**Context:** Final Fantasy VII PC (1998) - European Localization Analysis
**Purpose:** Identify the nature and purpose of mysterious "garbage" strings found in German, French, and Spanish executables

---

## Background Context

We are reverse-engineering Final Fantasy VII PC (1998 eStore version) to create language patches (HEXT format) that replace English menu text with German/French/Spanish equivalents.

### Key Discoveries

1. **European localization tool was broken**
   - All three languages (German, French, Spanish) use right-aligned text with 75-95% leading 0x00 padding
   - English uses left-aligned text with trailing 0x00 padding (normal)
   - Same broken tool was used for all three European versions

2. **Encoding differences**
   - All versions use modified ASCII: `char = byte + 0x20`
   - German has custom umlauts: 0x6A=ä, 0x7A=ö, 0x7F=ü, 0x7E=ß, 0x66=Ü
   - French/Spanish have different accent mappings (incomplete)
   - 0x00 = space character
   - 0xFF = string terminator

3. **String storage structure**
   - English: `[text][0xFF][padding 0x00 to 48-byte boundary]`
   - German/French/Spanish: `[padding 0x00 to right-align][text][0xFF]`

---

## The Mystery: Garbage Strings

Between the "Quit Dialog" strings and the "Config Menu" strings, ALL FOUR language versions contain a **large garbage string** (~1,250 bytes) that appears to be binary/control data rather than readable text.

### Location Pattern (Consistent Across Languages)

**Structure in all versions:**
1. Quit dialog strings (3-5 strings: "Do you want to quit?", "Yes", "No")
2. **→ GARBAGE STRING (~1,250 bytes) ←**
3. Config menu starts (Window color, Sound, Controller...)

**Specific Offsets:**

| Language | Quit Dialog End | Garbage Starts | Config Menu Starts | Garbage Size |
|----------|----------------|----------------|-------------------|--------------|
| English  | ~0x005183D8 | ? | 0x005188A8 | ~1,250 bytes |
| German   | 0x58FC13 | 0x58FC1A | 0x5900F0 | 1,250 bytes |
| French   | 0x59008C | 0x590090 | 0x590560 | 1,250 bytes |
| Spanish  | 0x590213 | 0x590216 | 0x5906E8 | 1,250 bytes |

---

## Garbage String Examples

### German (0x58FC1A - 1,250 bytes)

**First 200 characters decoded:**
```
@c  ^c              `      `  `a      `a  `a                     0  @a      0a  @a          _  `        `      _  0a            `        0a      _  0a          `        `  _                  `  _        _                     `      `         `  `          `        ``         `  `          _        _  _      ``            _  _      ``  _      ``            _  _        ``      ``  _            ``      _  ``      ``  _            ``        `      _  ``            `      _  `      _  ``        $ $ $ $ $ $ $% 0% <% H% T% `% l% x% ã% ñ% % % % % % % % % âíïãNõèì   àáòòåNõèì   õèÜáNõèì
```

**Raw hex (first 100 bytes):**
```
00 40 63 00 00 5E 63 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 60 00 00 00 00 00 00 60 00 00 60 61 00 00 00 00 00 60 61 00 60 61 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 30 00 40 61 00 00 00 00 00 30 61 00 40 61 00 00 00 00 00 00
```

**Last 100 characters decoded:**
```
Fensterfarbe
```

**Analysis:**
- Starts with control characters (`@c`, `^c`) suggesting binary data
- Contains mostly 0x00 (spaces), 0x60 (backtick), and occasional other chars
- Ends with "Fensterfarbe" (Window color) - the ACTUAL first config menu string
- This suggests the garbage is padding/metadata BEFORE the real menu strings

### French (0x590090 - 1,250 bytes)

**First 200 characters decoded:**
```
Jc  ^c              `      `  `a      `a  `a                     0  @a      0a  @a          _  `        `      _  0a            `        0a      _  0a          `        `  _                  `  _        _                     `      `         `  `          `        ``         `  `          _        _  _      ``            _  _      ``  _      ``            _  _        ``      ``  _            ``      _  ``      ``  _            ``        `      _  ``            `      _  `      _  ``        $ $ $ $ $ $ $
```

**Similar pattern to German** - control chars, lots of spaces/backticks

### Spanish (0x590216 - 1,250 bytes)

**First 200 characters decoded:**
```
^c  ^c              `      `  `a      `a  `a                     0  @a      0a  @a          _  `        `      _  0a            `        0a      _  0a          `        `  _                  `  _        _                     `      `         `  `          `        ``         `  `          _        _  _      ``            _  _      ``  _      ``            _  _        ``      ``  _            ``      _  ``      ``  _            ``        `      _  ``            `      _  `      _  ``        $ $ $ $ $ $ $
```

**Nearly identical to French/German** - same structure

---

## What We Know About The Garbage

### Facts:

1. **Same size across languages** (~1,250 bytes)
2. **Same position relative to string groups** (between quit dialog and config menu)
3. **Same internal structure** (control chars, spaces, backticks, dollar signs)
4. **Contains the NEXT menu string at the end** (e.g., "Fensterfarbe" in German)
5. **Not rendered in-game** (doesn't appear visually)
6. **Follows 0xFF terminator rules** (has 0xFF at end before next real string)

### Patterns Observed:

- Starts with control chars: `@c`, `^c`, `Jc`
- Repeating sequences of: ` ` (0x00), `` ` `` (0x60), `_` (0x5F), `a` (0x61)
- Dollar signs and percent signs: `$ $ $ $ $`, `0%`, `<%`, `H%`, `T%`
- Ends with what looks like garbage text then the next menu string

### Hypotheses to Consider:

1. **Color palette data?** (Window color comes next - related?)
2. **Font texture coordinates?** (Backticks and spaces could be UV maps)
3. **Metadata table?** (Offsets, lengths, or indices for menu system)
4. **Compression dictionary?** (Lookup table for text compression)
5. **Localization tool artifact?** (Broken tool left padding/debug data)
6. **Graphics/rendering data?** (Menu window dimensions, colors, borders)
7. **String table header?** (Indices, pointers, or metadata before actual strings)

---

## Specific Questions for AI Analysis

Given the above context and examples:

1. **What is the most likely purpose of this 1,250-byte garbage data?**
   - Is it functional data (palette, coords, indices)?
   - Is it padding/alignment for memory layout?
   - Is it a bug/artifact from the localization process?

2. **Why does it appear in ALL FOUR language versions at the same relative position?**
   - If it's functional, what would it control?
   - If it's a bug, why is it consistent?

3. **Why does the garbage END with the next menu string's text?**
   - Is "Fensterfarbe" part of the garbage or separate?
   - Could this be an offset pointer or length calculation error?

4. **What do the repeating patterns suggest?**
   - `` ` ` a ` ` a`` repeating
   - `$ $ $ $` followed by `0% <% H% T%`
   - What data structures use these patterns?

5. **Could this be related to the "Window color" menu option?**
   - The next string is ALWAYS "Window color" (or equivalent)
   - Could this be color palette data, RGB values, or rendering params?

6. **Why exactly 1,250 bytes?**
   - Is this a significant size for any game data structure?
   - Could it be a fixed-size allocation for something?

---

## Raw Data for Analysis

### German Garbage (Full hex dump - first 300 bytes):

```
00 40 63 00 00 5E 63 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 60 00 00 00 00 00 00 60
00 00 60 61 00 00 00 00 00 60 61 00 60 61 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 30 00 40
61 00 00 00 00 00 30 61 00 40 61 00 00 00 00 00
00 00 00 5F 00 60 00 00 00 00 00 00 60 00 00 00
00 00 5F 00 30 61 00 00 00 00 00 00 00 00 00 00
60 00 00 00 00 00 00 30 61 00 00 00 00 00 5F 00
30 61 00 00 00 00 00 00 00 00 00 00 60 00 00 00
00 00 00 00 60 00 5F 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 60 00 5F 00 00 00 00 5F
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 60 00 00 00 00 00 00
60 00 00 00 00 00 00 00 00 60 00 60 00 00 00 00
00 00 00 00 00 00 60 00 00 00 00 00 60 60 00 00
00 00 00 00 00 00 00 60 00 60 00 00 00 00 00 00
00 00 00 00 5F 00 00 00 00 00 5F 00 5F 00 00 00
00 60 60 00 00 00 00 00 00 00 00 00 5F 00 5F
```

### Decoded Pattern Analysis:

When decoded using FF7 encoding (`char = byte + 0x20`):

| Hex | ASCII+0x20 | Appears As | Count in 300 bytes |
|-----|------------|------------|-------------------|
| 0x00 | (space) | (space) | ~200 |
| 0x60 | `` ` `` | `` ` `` | ~40 |
| 0x61 | `a` | `a` | ~15 |
| 0x5F | `_` | `_` | ~10 |
| 0x30 | `P` | `0` | ~8 |
| 0x40 | `` ` `` | `@` | ~5 |
| 0x63 | `c` | `c` | 2 |
| 0x5E | `~` | `^` | 1 |

**Observation:** Majority is 0x00 (space), with occasional low bytes (0x30-0x63 range).

---

## Additional Context

### FF7 Technical Details:

- **Platform:** Windows 95/98 PC
- **Year:** 1998 (original release), 2013 (eStore re-release)
- **Graphics:** Software renderer + 3Dfx Glide support
- **Text rendering:** Custom font texture (256x256 or similar)
- **Menu system:** 2D overlays on 3D backgrounds
- **String encoding:** Custom byte-to-char mapping (not UTF-8)

### Related Findings:

1. All European versions have debug strings: `C:\FF7\Src\Battle\...` (source file paths)
2. Spanish exe has leftover asset filenames: `comesoon.tim`, `ending3.avi`, `people.bin`
3. French exe has floating-point data (IEEE 754) at same offset as German menu strings
4. Localization was done by an external contractor (not Square directly)

---

## Request for AI

Please analyze the provided information and give your expert assessment:

1. What is this garbage data most likely to be?
2. What clues point to its true purpose?
3. Should we preserve it when creating HEXT patches, or can we ignore it?
4. Are there any risks to leaving it in place?
5. Could it contain useful information for understanding the string table structure?

**Provide detailed reasoning for your conclusions.**

---

## Appendix: How to Verify Your Hypothesis

If you propose a hypothesis, please suggest:
- What patterns we should look for to confirm it
- What other data in the exe we should check
- How we could test if it's functional vs. garbage
- Whether similar patterns exist in other FF7 data files

Thank you for your analysis!

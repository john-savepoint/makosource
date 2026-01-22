# FF7 German String Extraction Methodology

**Created**: 2026-01-02
**Session**: 68888497-9f38-454c-8ee5-3953fa6c7625
**Author**: Agent 1 (German String Extraction)

## Objective

Extract ALL German text strings from `ff7_de.exe` for use in creating an English-German mapping that will inform the Japanese localization project.

## Tools Used

- Python 3 for extraction scripting
- `xxd` for initial hex analysis
- Binary pattern analysis

## Methodology

### Step 1: Initial Reconnaissance

First, I examined the known menu string region using `xxd`:

```bash
xxd -s 0x590000 -l 4096 "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
```

This revealed the encoding pattern where visible text like `&ENSTERFARBE` decodes to `FENSTERFARBE`.

### Step 2: Encoding Discovery

By analyzing multiple strings, I derived the encoding rule:

```python
ASCII_value = FF7_byte + 0x20
```

**Verification Examples:**
| Raw Hex | + 0x20 | ASCII | German Word |
|---------|--------|-------|-------------|
| 0x26 | 0x46 | 'F' | Fenster |
| 0x33 | 0x53 | 'S' | Sound |
| 0x2B | 0x4B | 'K' | Kontroller |
| 0x2D | 0x4D | 'M' | Menü |

### Step 3: German Special Character Identification

German umlauts required special handling. Through pattern matching:

| FF7 Byte | Character | How Identified |
|----------|-----------|----------------|
| 0x6A | ä | Found in "Auswählen" (Ausw**ä**hlen) |
| 0x7A | ö | Found in "Phönix" (Ph**ö**nix) |
| 0x7F | ü | Found in "Menü" (Men**ü**) |
| 0x7E | ß | Found in "Abschließen" |

### Step 4: Structure Analysis

I discovered two main string structures:

#### 4a. Fixed-Width Records (48 bytes)
Used in the config menu region (0x5900F0+):
- Records are padded with 0x00 bytes
- String content followed by 0xFF terminator
- Remaining space padded with 0x00

#### 4b. Sequential Strings
Used in most other regions:
- Strings directly follow each other
- Each terminated by 0xFF
- Variable length

### Step 5: Region Mapping

Through systematic scanning, I identified these key regions:

| Region | Address Range | Purpose |
|--------|---------------|---------|
| Config Menu | 0x5900F0 - 0x590C00 | Settings labels |
| Item Names | 0x56F800 - 0x570800 | Item/equipment |
| Status Messages | 0x594C00 - 0x595800 | Status effects |
| Gold Saucer | 0x597600 - 0x59A000 | Mini-games |
| Save/Load | 0x59C400 - 0x59E000 | Save interface |

### Step 6: Extraction Algorithm

```python
def decode_ff7_byte(b):
    # Terminator check
    if b == 0xFF:
        return None

    # German special character overrides
    if b in GERMAN_SPECIALS:
        return GERMAN_SPECIALS[b]

    # Space character
    if b == 0x00:
        return ' '

    # Standard ASCII conversion
    ascii_val = b + 0x20
    if 0x20 <= ascii_val <= 0x7E:
        return chr(ascii_val)

    return None
```

### Step 7: Quality Filtering

Not all byte sequences are valid strings. Quality checks applied:

1. **Minimum length**: At least 2 printable characters
2. **Printable ratio**: At least 50% must decode to printable chars
3. **Not just numbers/punctuation**: Must contain actual text

### Step 8: Deduplication

Many strings appear multiple times (different contexts). Deduplication by:
- Text content (primary)
- Keeping first occurrence only

### Step 9: Categorization

Strings categorized by German keywords:

```python
categories = {
    'Config/Settings': ['fenster', 'sound', 'controller', ...],
    'Battle/Combat': ['kampf', 'angriff', 'magie', ...],
    'Menu/Navigation': ['menü', 'auswählen', 'abbrechen', ...],
    # ... etc
}
```

## Results

| Metric | Value |
|--------|-------|
| Total Strings Extracted | 682 |
| Unique by Text | 682 |
| Categorized | 121 |
| Uncategorized (Other) | 561 |

## Challenges Encountered

### 1. Initial Over-extraction
First attempt found 16,000+ "strings" due to:
- Matching binary data that coincidentally decoded to text
- Including partial strings (fragments)

**Solution**: Stricter quality filtering and focused region targeting.

### 2. German Character Mapping
The encoding rule (+0x20) doesn't work for German special characters.

**Solution**: Created override table for ä, ö, ü, ß, etc.

### 3. Fixed vs Variable Width
Config menu uses 48-byte records, other regions don't.

**Solution**: Implemented two extraction methods and applied appropriate one per region.

## Output Files

1. **german_strings_complete.txt**
   - All 682 strings with offsets and hex bytes
   - Format: `[OFFSET] [LEN] HEX | TEXT`

2. **german_strings_by_category.txt**
   - Same strings organized by functional category
   - Easier to find specific string types

3. **german_regions_analysis.md**
   - Technical documentation of memory regions
   - Encoding specifications

4. **extract_german_complete.py**
   - Reusable extraction script
   - Can be modified for other language executables

## Recommendations for Next Steps

1. **For Agent 2 (EN-DE Mapping)**:
   - Use `german_strings_complete.txt` as the German side
   - Match offsets between EN and DE executables
   - Focus on the main regions (0x590000+)

2. **For Japanese Implementation**:
   - The German special character handling shows how to implement Japanese
   - Same +0x20 rule for ASCII, special codes for Japanese chars
   - Likely need larger character table (kanji, hiragana, katakana)

---
*Generated by Agent 1 for the FF7OG Japanese Project*

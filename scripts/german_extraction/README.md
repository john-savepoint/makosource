# FF7 German Comprehensive String Extractor

**Created:** 2026-01-06 12:00 JST (Tuesday)
**Session-ID:** 85c271e2-f1ef-4bb6-b5dc-b212b2694001
**Author:** John Zealand-Doyle

---

## Overview

This script extracts German strings from `ff7_de.exe` with full analysis of what was previously thought to be "garbage" or "padding" bytes.

**Key Discovery:** The "garbage" bytes are NOT random data - they are:
1. Plain ASCII texture filenames (cloud.tim, barre.tim, etc.)
2. IEEE 754 floating-point UI coordinates
3. Character name struct headers

---

## Usage

```bash
# Run with default paths
python extract_german_comprehensive.py

# Specify custom exe path
python extract_german_comprehensive.py --exe /path/to/ff7_de.exe

# Specify custom output directory
python extract_german_comprehensive.py --output /path/to/output
```

---

## Output Structure

The script creates three subdirectories with different output formats:

```
output/
├── clean_strings/           # For HEXT patch generation
│   ├── menu_strings.csv     # Clean German text with corrected offsets
│   ├── menu_strings.txt     # Human-readable string list
│   └── character_names.csv  # Character names with struct headers
├── asset_data/              # Discovered game assets
│   ├── texture_filenames.csv # All .tim filenames found
│   └── asset_regions.txt    # Map of asset data regions
└── raw_with_padding/        # Full extraction for analysis
    ├── all_strings_raw.csv  # Everything including "garbage"
    └── padding_analysis.txt # Explanation of padding contents
```

---

## Output Files

### clean_strings/menu_strings.csv

Clean German menu/dialog strings ready for HEXT patch generation.

| Column | Description |
|--------|-------------|
| index | Sequential string number |
| offset | Corrected hex offset (where TEXT starts) |
| text | Decoded German string |
| length | Character count |

### clean_strings/character_names.csv

Character name entries with struct headers.

| Column | Description |
|--------|-------------|
| offset | Hex offset of name |
| name | Character name (CLOUD, BARRET, etc.) |
| header_hex | 32 bytes preceding the name |
| name_hex | FF7-encoded name bytes |

### asset_data/texture_filenames.csv

Discovered texture/model filenames.

| Column | Description |
|--------|-------------|
| offset | Hex offset in exe |
| filename | Plain ASCII filename (e.g., "cloud.tim") |
| hex_bytes | Raw bytes |

### raw_with_padding/all_strings_raw.csv

Full extraction including padding data.

| Column | Description |
|--------|-------------|
| raw_offset | Original offset (includes padding) |
| text_offset | Corrected offset (text start) |
| padding_bytes | Number of bytes before text |
| is_clean | True if actual German text |

---

## Key Technical Details

### German Character Encoding

| Character | Byte Value | Example |
|-----------|------------|---------|
| ä | 0x6A | wählen, Auswählen |
| ö | 0x7A | Möchten, können |
| ü | 0x7F | zurück, Menü |
| ß | 0x7E | muß, daß |
| Ü | 0x66 | GRÜN, MENÜ |

Standard formula: `byte + 0x20 = ASCII character`

### Why "Garbage" Appears

The FF7 decoder interprets ALL bytes using the formula above. Plain ASCII characters get mangled:

```
"cloud" (63 6C 6F 75 64) → decoded as "ãïñôä"
"barre" (62 61 72 72 65) → decoded as "âáòòå"
```

This is why texture filenames like `cloud.tim` appear as gibberish when run through the German decoder.

### Asset Data Regions

| Start | End | Size | Contents |
|-------|-----|------|----------|
| 0x58FC22 | 0x5900EE | 1,228 bytes | Texture filenames |

Filenames found:
- Character portraits: cloud.tim, barre.tim, tifa.tim, earith.tim, red.tim, yufi.tim, ketc.tim, bins.tim, cido.tim
- Low-res variants: *_l.tim
- Font textures: usfont_*.tim
- Battle windows: btl_win_*.tim
- Weapons: buster.tim

---

## Dependencies

- Python 3.8+
- No external packages required

---

## Related Files

- `FF7_GERMAN_DATA_FINDINGS.md` - Complete analysis documentation
- `/home/johnzealanddoyle/projects/ff7OG_japanese/scripts/ff7_german_decoder.py` - Original decoder module

---

## For HEXT Patch Generation

To generate HEXT patches for Japanese mod, use the `clean_strings/menu_strings.csv` output:

1. Run this extraction script
2. Use the corrected offsets from `menu_strings.csv`
3. Apply Japanese translations to these positions
4. The `text_offset` column gives the exact byte where German text starts

This avoids including asset data in your patches.

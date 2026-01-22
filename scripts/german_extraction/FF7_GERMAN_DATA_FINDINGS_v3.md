# FF7 German String Data Findings v3

**Created:** 2026-01-06 14:45 JST (Tuesday)
**Session-ID:** 85c271e2-f1ef-4bb6-b5dc-b212b2694001
**Author:** John Zealand-Doyle

---

## Executive Summary

The "garbage" bytes before German strings in `ff7_de.exe` are **NOT garbage** - they are meaningful data structures:

| Data Type | Description | Byte Characteristics |
|-----------|-------------|---------------------|
| **Clean Menu Text** | Actual German UI strings | FF7-encoded (0x01-0x5F + 0x20), German umlauts (0x6A=ä, etc.) |
| **UI Table Data** | Menu positioning coordinates | 16-byte binary records, pattern "X X 3Y1Z" when decoded |
| **Binary Data** | Compressed/encrypted data | High-byte values (0x80+), >30% ratio |
| **Character Names** | Player character structs | Binary header + FF7-encoded name (CLOUD, BARRET, etc.) |
| **Asset Filenames** | Texture references | Plain ASCII with `.tim` extension |
| **Developer Markers** | Debug strings | Contains "START OF MENU SYSTEM" etc. |

---

## Extraction Results

### Output Directory Structure

```
output_v3/
├── clean_text/
│   ├── german_menu_strings.csv   # 533 verified German menu strings
│   └── german_menu_strings.txt   # Human-readable format
├── character_names/
│   └── character_names.csv       # 23 character name struct entries
├── ui_data/
│   └── ui_binary_data.csv        # 488 UI table/binary/fragment entries
├── asset_data/
│   └── texture_filenames.csv     # 58 unique .tim texture files
├── developer/
│   └── developer_markers.txt     # 1 developer debug marker
└── raw_all/
    ├── all_entries.csv           # 1150 total entries with categories
    └── category_summary.txt      # Category breakdown
```

### Category Breakdown

| Category | Count | Description |
|----------|-------|-------------|
| **clean_text** | 533 | Verified German menu strings (75%+ confidence) |
| **fragment** | 336 | Short entries (≤2 chars) that aren't meaningful menu text |
| **binary_data** | 136 | High-byte ratio (>30%) binary/compressed data |
| **unknown** | 103 | Entries that don't match any known pattern |
| **character_name** | 23 | Player character struct entries |
| **ui_table** | 16 | UI coordinate/positioning tables |
| **asset** | 2 | Texture filename blocks |
| **developer** | 1 | Developer debug markers |
| **Total** | **1150** | |

---

## Data Type Details

### 1. Clean German Menu Text (533 entries)

**Location:** Throughout string table (0x58FBB0 - 0x59E000)
**Encoding:** FF7 German encoding
**Characteristics:**
- Standard formula: `byte + 0x20` for bytes 0x01-0x5F
- German umlauts: ä=0x6A, ö=0x7A, ü=0x7F, ß=0x7E, Ü=0x66
- String terminator: 0xFF
- Space: 0x00 (middle bytes, NOT leading)
- Right-aligned with leading 0x00 padding (75-95%)

**Example:**
```
Offset 0x5900F0: 26 45 4E 53 54 45 52 46 41 52 42 45 FF
                 F  e  n  s  t  e  r  f  a  r  b  e  [term]
                 = "Fensterfarbe" (Window color)
```

### 2. UI Table/Coordinate Data (16 entries)

**Location:** 0x595B94 - 0x595C90
**Structure:** 16-byte binary records
**Byte Pattern:**
```
[2B X] [2B Y] [2B flags] [2B value] [8B 0xFF padding]
Example: 32 00 32 00 13 00 11 30 FF FF FF FF FF FF FF FF
```
**When Decoded:** Appears as "R R 3 1P", "T T 3!1T", etc.
**Why It's Garbage:** These are menu positioning coordinates, NOT text

### 3. Binary/Compressed Data (136 entries)

**Location:** 0x5981E8 - 0x5986BE (and scattered)
**Characteristics:**
- High-byte values (0x80+) comprise >30% of non-padding bytes
- Multiple 0xFF bytes as DATA, not terminators
- Likely LZSS compressed or encrypted data

**Example:**
```
Offset 0x5981E8: CF 3A A6 AA 6C C6 E9 FF FF EF 6A CA AA CC A3 FC
                 ↑ high bytes throughout
```

### 4. Character Name Structs (23 entries)

**Location:** 0x598900 - 0x598E10
**Structure:** Binary header + FF7-encoded name + 0xFF + padding

**Example - Barret:**
```
Offset 0x598900:
[Header] 23 00 00 00 01 01 0F 0D 0B 09 05 0D 00 00 00 00
         00 00 01 7A
[Name]   22 41 52 52 45 54 FF  = "BARRET"
[Pad]    FF FF FF FF FF 20 00 FF 00 FF 00 01 00 ...
```

**Extracted Names:**
- Cloud (0x23 4C 4F 55 44)
- Barret (0x22 41 52 52 45 54)
- Tifa (0x34 49 46 41)
- Aerith (0x21 45 52 49 54 48)
- Red XIII (0x32 45 44)
- Yuffie (0x39 55 46 46 49 45)
- Cait Sith (0x23 41 49 54)
- Vincent (0x36 49 4E 43 45 4E 54)
- Cid (0x23 49 44)
- Sephiroth (0x33 45 50 48 49 52 4F 54 48)
- Chocobo (0x23 48 4F 43 4F)

### 5. Asset Filenames (2 entries, 58 files)

**Location:** 0x58FC22 and 0x5921D8
**Contents:** Plain ASCII texture filenames

**Files Found:**
- Character portraits: `cloud.tim`, `barre.tim`, `tifa.tim`, `earith.tim`, `red.tim`, `yufi.tim`, `ketc.tim`, `bins.tim`, `cido.tim`
- Low-res variants: `cloud_l.tim`, `barre_l.tim`, etc.
- Fonts: `usfont_a_h.tim`, `usfont_a_l.tim`, `usfont_b_h.tim`, etc.
- Battle windows: `btl_win_a_h.tim`, `btl_win_a_l.tim`, etc.
- Weapon: `buster.tim`
- Misc: `choco.tim`, `pcloud.tim`, `pcefi.tim`, `zeni.tim`, `colo*.tim`, `ketcy2*.tim`

**Why Plain ASCII Appears as Garbage:**
The FF7 decoder adds 0x20 to bytes, so:
- `cloud` (ASCII: 63 6C 6F 75 64) → `ãïñôä` (0x63+0x20=0x83='ã', etc.)

### 6. Developer Markers (1 entry)

**Location:** 0x590FF0
**Content:** Contains debug markers like "START OF MENU SYSTEM!!!"

---

## Classification Algorithm

The v3 extraction script uses multi-stage classification:

1. **Asset Detection** - Check for `.tim`, `.tex` extensions in raw bytes
2. **Developer Markers** - Check for "START OF MENU", "END OF MENU", etc.
3. **Character Names** - Check for known encoded character name patterns
4. **Binary Data** - Calculate high-byte (≥0x80) ratio; >30% = binary
5. **UI Table** - Detect coordinate patterns: `^[A-Za-z] [A-Za-z] \d`
6. **Fragment** - Entries ≤2 chars (except JA, HP, MP, AP, LV, OK, GIL)
7. **Clean Text** - German letter ratio >50%, FF7 encoding validity >90%, no suspicious patterns

**Suspicious Pattern Rejection:**
- Coordinate patterns at start
- Multiple special characters in sequence (`!#$%&{3,}`)
- Starts with `!` and length >5
- Garbage prefix (5+ non-letter chars at start)
- Keyboard layout sequences (10+ uppercase letters, except MASTER/STUFE/etc.)

---

## Key Technical Values

| Description | Value | Notes |
|-------------|-------|-------|
| String table start | 0x58FBB0 | First quit dialog string |
| String table end | 0x59E000 | End of menu region |
| First clean string | 0x58FBB0 | "Möchten Sie Final" |
| Config menu start | 0x5900F0 | "Fensterfarbe" |
| Character names region | 0x598900-0x598E10 | Struct format |
| UI table region | 0x595B94-0x595C90 | 16-byte coordinate records |
| Total entries | 1150 | All FF-terminated entries |
| Clean strings | 533 | Verified German menu text |
| FF7 encoder formula | byte + 0x20 | For 0x01-0x5F |
| German ä | 0x6A | Special mapping |
| German ö | 0x7A | Special mapping |
| German ü | 0x7F | Special mapping |
| German ß | 0x7E | Special mapping |
| German Ü | 0x66 | Special mapping |

---

## Usage

Run the extraction script:
```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese/scripts/german_extraction
python3 extract_german_v3.py
```

Output is written to `output_v3/` with categorized subdirectories.

---

## Files

| File | Description |
|------|-------------|
| `extract_german_v3.py` | Main extraction script |
| `output_v3/clean_text/german_menu_strings.csv` | Clean German strings for translation |
| `output_v3/character_names/character_names.csv` | Character name struct data |
| `output_v3/ui_data/ui_binary_data.csv` | UI tables and binary data |
| `output_v3/asset_data/texture_filenames.csv` | Texture file references |
| `output_v3/raw_all/all_entries.csv` | Complete extraction with categories |

---

## Conclusion

The "garbage" in German string extraction is actually:
- **UI positioning data** - Binary coordinate tables
- **Compressed/encrypted data** - High-byte ratio binary
- **Character struct headers** - Binary headers before names
- **Plain ASCII asset names** - Mangled by FF7 decoder

The v3 script successfully separates these into distinct categories, providing **533 clean German menu strings** ready for translation/patching.

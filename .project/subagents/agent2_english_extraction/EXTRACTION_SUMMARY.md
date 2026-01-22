# Agent 2: English String Extraction Summary

**Generated:** 2026-01-02 20:50 JST
**Session:** 93c10c47-4dd6-41a6-aa90-73c6b0def3b1
**Mission:** Comprehensive English string extraction with touphScript mapping

## Output Files

| File | Size | Description |
|------|------|-------------|
| `english_strings_by_index.txt` | 80KB | All 767 strings with decoded text and raw bytes |
| `english_string_type_analysis.md` | 4.5KB | Documentation of all 6 string types |
| `skip_regions_analysis.md` | 3.4KB | Documentation of regions to skip/handle specially |
| `virtual_address_mapping.txt` | 33KB | VA calculations for HEXT patching |
| `extract_english_strings.py` | 31KB | Python extraction script |

## Extraction Statistics

**Total strings extracted:** 767 (indices 0-766)

### String Type Distribution

| Type | Count | Percentage | Description |
|------|-------|------------|-------------|
| DEF | 443 | 57.8% | Standard FF7 encoding (ASCII - 0x20, FF terminator) |
| RGB | 173 | 22.6% | Keyboard labels (plain ASCII in file) |
| UNICODE | 68 | 8.9% | Name entry characters (UTF-16LE) |
| ZEROTERM | 55 | 7.2% | Jockey names (FF7 encoding, null terminator) |
| FFPADDED | 25 | 3.3% | Race ordinals (FF7 encoding, FF padding) |
| NOFF_TERM | 3 | 0.4% | No FF terminator in file |

## Key Findings

### Encoding Details

1. **DEF (Type 0):** Standard FF7 text encoding
   - Each ASCII character stored as `ASCII - 0x20`
   - Space = `0x00`
   - Terminator = `0xFF`
   - Example: 'A' (0x41) stored as `0x21`

2. **RGB (Type 2):** Keyboard labels
   - Stored as plain ASCII in file (NOT RGB-encoded)
   - RGB encoding is a rendering instruction, not storage format
   - Index range: 77-213

3. **UNICODE (Type 3):** Name entry characters
   - UTF-16LE encoding
   - Single characters for name selection
   - Index range: 461-528

4. **ZEROTERM (Type 5):** Chocobo jockey names
   - Uses FF7 encoding (ASCII - 0x20)
   - Terminated by `0x00` instead of `0xFF`
   - Index range: 712-766

### Skip Regions for Patching

| Region | Indices | Reason |
|--------|---------|--------|
| UNICODE Name Entry | 461-528 | Separate rendering system |
| Race Ordinals | 687-711 | Fixed-width, specific padding |
| Jockey Names | 712-766 | Should remain English |

### Special Handling Required

- **Keyboard region (77-213):** Game applies -0x20 before font lookup; patches must add +0x20 to compensate

## Virtual Address Formula

```
VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000
```

Example:
- File offset: `0x518370`
- Virtual address: `0x919970`

## Usage for EN-DE Mapping

The `english_strings_by_index.txt` file provides a master reference for creating EN-DE offset mappings. Each line contains:

```
[INDEX] [OFFSET_HEX] [LENGTH] [TYPE] | DECODED_EN_TEXT | RAW_HEX_BYTES
```

This format allows:
1. Direct lookup by touphScript index
2. Verification of English text content
3. Byte-level comparison with German strings
4. VA calculation for HEXT patches

## Source Executable

- **Path:** `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe`
- **Total offset entries:** 767 (from touphScript ff7exe.cpp)

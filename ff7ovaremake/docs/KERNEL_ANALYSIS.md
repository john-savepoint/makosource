# FF7 OVA Remake - Kernel & Scene File Analysis

**Created**: 2026-01-24 16:15:00 JST
**Version**: 1.0.0
**Status**: INCOMPLETE - Files use non-standard encryption/compression
**Session-ID**: cbeeb01d-91ad-403b-8094-7d91e74c46b3

## Summary

The FF7 OVA Remake's kernel and scene files use a **non-standard compression or encryption format** that prevents standard GZIP decompression. While the files contain GZIP magic numbers (`1f 8b 08`), attempts to decompress using standard zlib/gzip tools fail with header check errors. This suggests either:
1. Custom encryption applied before/after compression
2. Modified GZIP format with non-standard parameters
3. Proprietary compression wrapper

**Critical Finding**: WINDOW.BIN retains its vanilla 1998 timestamp (May 4, 1998), indicating it was **not modified**. However, KERNEL.BIN, kernel2.bin, and scene.bin all show June 16, 2025 timestamps, confirming they contain **OVA Remake-specific modifications**.

## File Metadata

### KERNEL.BIN
- **Size**: 23,690 bytes (23 KB)
- **Modified**: 2025-06-16 08:05:19 JST
- **MD5**: `69df3db120dff5d21c091d9b6705e1e1`
- **Format**: BIN-GZIP (27 GZIP sections detected)
- **Status**: Cannot decompress with standard tools

**Expected Contents** (per FF7 format documentation):
- Section 0: Command data
- Section 1: Attack data
- Section 2: Item data
- Section 3: Weapon data
- Section 4: Armor data
- Section 5: Accessory data
- Section 6: Materia data
- Section 7: Key items
- Section 8: Character stats/growth
- Sections 9-26: Text data (menu strings, item names, descriptions)

### kernel2.bin
- **Size**: 17,356 bytes (17 KB)
- **Modified**: 2025-06-16 08:05:19 JST
- **MD5**: `875bbb01b8b32c750fd9d7856ead5ed3`
- **Format**: LZS-compressed (PC version specific)
- **Status**: Cannot decompress with standard tools

**Expected Contents**:
- Uncompressed text data from KERNEL.BIN sections 10-27
- Compressed as single LZS archive with 4-byte header

### WINDOW.BIN
- **Size**: 13,312 bytes (13 KB)
- **Modified**: **1998-05-04 22:21:50 JST** (vanilla timestamp)
- **MD5**: `6d43b018cd334a63927e972361183f46`
- **Format**: Binary data
- **Status**: **UNMODIFIED** (original vanilla file)

**Contents**: UI window configurations, dialog box parameters

### scene.bin
- **Size**: 409,600 bytes (400 KB)
- **Modified**: 2025-06-16 08:05:20 JST
- **MD5**: `ba1721992800dc565613a5f1c004f774`
- **Format**: 64 GZIP-compressed battle scenes
- **Status**: Cannot decompress with standard tools

**Expected Structure**:
- Header: 64 × 4-byte offset table (256 bytes)
- 64 compressed battle scenes (~6 KB each decompressed)

**Scene Offset Analysis**:
```
Scene  0: offset 0x00000010 (16 bytes)     - Size: 647 bytes
Scene  1: offset 0x00000297 (663 bytes)    - Size: 568 bytes
Scene  2: offset 0x000004cf (1231 bytes)   - Size: varies
Scene  3-9: offset 0xffffffff             - INVALID (unused/deleted scenes)
...
Scene 60-63: Various large offsets        - Possibly corrupted offset table
```

**Critical Issue**: Many scene offsets are `0xffffffff` (invalid), and the first scene data consists entirely of `0xff` bytes, suggesting either:
- File corruption
- Custom encoding/encryption
- Modified scene.bin format specific to OVA Remake

## File Format Analysis

### Standard FF7 KERNEL.BIN Format

According to [Qhimm Modding Wiki](https://qhimm-modding.fandom.com/wiki/FF7/Kernel/Low_level_libraries) and [FF7 Flat Wiki](https://ff7-mods.github.io/ff7-flat-wiki/FF7/Kernel/Kernel.bin.html), the standard format is:

**BIN-GZIP Structure**:
- 6-byte header per section: `[4 bytes size][2 bytes unknown]`
- Followed by GZIP-compressed data
- 27 total sections (9 data + 18 text)

**Observed in OVA Remake KERNEL.BIN**:
```
Offset 0x0000: 81 00 00 01 00 00 1f 8b 08 00 00 00 00 00 02 03
               ^^^^^^^^^^^^^ Header? GZIP magic starts at 0x0006
```

The file contains 27 GZIP magic numbers (`1f 8b 08`) at expected offsets:
- Section 0: 0x0006 (6 bytes)
- Section 1: 0x008d (141 bytes)
- Section 2: 0x06d1 (1745 bytes)
- ... (continues through section 26 at 0x5bb4)

**However**: All decompression attempts fail with "incorrect header check" errors, despite valid GZIP magic numbers.

### Standard FF7 scene.bin Format

**Expected Structure**:
- 64 scenes × 4-byte offsets (256 bytes header)
- Each scene contains:
  - Formation data (enemy placement)
  - Enemy AI scripts
  - Battle rewards (AP, Gil, items)
  - Camera angles
  - Escape parameters

**Observed Issues**:
- Offset table contains many `0xffffffff` entries
- First scene data is all `0xff` bytes
- Standard GZIP decompression fails

## Decompression Attempts

### Method 1: Standard zlib (Python)
```python
import zlib
decompressed = zlib.decompress(section_data)
# Result: Error -3 "incorrect header check"
```

### Method 2: GZIP magic number extraction
- Located all 27 GZIP headers in KERNEL.BIN
- Attempted decompression from each offset
- **Result**: All failed with header check errors

### Method 3: Scene.bin offset table parsing
- Read 64 scene offsets
- Extracted scene 0 data (all 0xff bytes)
- **Result**: Not valid GZIP data

## Possible Explanations

### 1. Custom Encryption Layer
The mod may apply encryption **before** or **after** GZIP compression:
- XOR cipher with key
- Stream cipher (RC4, ChaCha20)
- Block cipher (AES in CTR mode)

### 2. Modified GZIP Parameters
- Non-standard compression levels
- Custom GZIP flags
- Modified header format

### 3. Wrapper Format
- Additional header/footer data
- Checksum modifications
- Custom archive format wrapping standard GZIP

### 4. FFNx Engine Integration
Since OVA Remake uses FFNx (see MODIFICATION_MECHANISMS_SUMMARY.md), the engine may:
- Decompress files at runtime using custom code
- Apply decryption transparently
- Use modified file loaders in ff7_opengl.dll

## Comparison with Vanilla Requirements

**LIMITATION**: Without vanilla kernel.bin/scene.bin files for comparison, we cannot:
- Identify specific stat changes
- Document equipment modifications
- Trace materia/ability alterations
- Map enemy/formation changes

**Alternative Approach**: Examine ff7.exe/.dll modifications for custom decompression routines (see Task #4 analysis).

## Extracted String Samples

### KERNEL.BIN readable strings (limited):
```
KlTU
3mi{oo
p9S?
!bsm
/mc@
=GaM
+?Qx
Cfqb
7k?
29R6ksoHn2
fflue
palIDB
```

Most strings are compressed/encrypted and not readable in raw form.

## Conclusions

### Confirmed Findings
1. **WINDOW.BIN is unmodified** (vanilla 1998 file retained)
2. **KERNEL.BIN modified** (June 2025 timestamp, 23 KB)
3. **kernel2.bin modified** (June 2025 timestamp, 17 KB)
4. **scene.bin modified** (June 2025 timestamp, 400 KB)
5. All modified files use **non-standard compression/encryption**
6. Standard FF7 modding tools likely won't work on these files

### Unknown Factors
- Exact encryption algorithm (if used)
- Custom decompression routine location (ff7.exe/.dll?)
- Whether modifications are gameplay-significant or just re-encoded
- Actual changes to stats/items/enemies (requires decompression)

### Required Next Steps
1. **Reverse-engineer decompression routine**:
   - Examine ff7_opengl.dll for kernel loading code
   - Check ff7.exe for custom file loaders
   - Search for decryption keys in memory/executables

2. **Use FFNx-specific tools** (if available):
   - Check if FFNx provides kernel extraction utilities
   - Search FFNx documentation for file format specs

3. **Memory dumping approach**:
   - Run game and dump decompressed kernel from memory
   - Compare memory values to vanilla FF7 data
   - Trace file loading in debugger

4. **Acquire vanilla files for comparison**:
   - Download vanilla FF7 PC (Japanese version)
   - Extract vanilla kernel.bin/scene.bin
   - Perform binary diff even without decompression

## File Locations

**OVA Remake Files**:
- `/mnt/c/Users/johnz/Desktop/ff7ovaremake_extracted/archive_3_contents/data/kernel/KERNEL.BIN`
- `/mnt/c/Users/johnz/Desktop/ff7ovaremake_extracted/archive_3_contents/data/kernel/kernel2.bin`
- `/mnt/c/Users/johnz/Desktop/ff7ovaremake_extracted/archive_3_contents/data/kernel/WINDOW.BIN`
- `/mnt/c/Users/johnz/Desktop/ff7ovaremake_extracted/archive_3_contents/data/battle/scene.bin`

## References

- [FF7 Kernel.bin Format Documentation](https://ff7-mods.github.io/ff7-flat-wiki/FF7/Kernel/Kernel.bin.html)
- [FF7 Low-level Libraries](https://qhimm-modding.fandom.com/wiki/FF7/Kernel/Low_level_libraries)
- [Cosmo Memories KERNEL.BIN Reference](https://cosmo-memories.lenain.info/FF7%20Technical%20Reference/Kernel/Resources/kernel_bin.html)
- [Elena KERNEL.BIN Library (GitHub)](https://github.com/Shojy/Elena)
- [WallMarket KERNEL.BIN Editor](https://forums.qhimm.com/index.php?topic=7928.0)

## Analysis Limitations

This analysis is **incomplete** due to file encryption/compression preventing content extraction. A complete analysis requires:
- Decompression/decryption methodology
- Vanilla file comparison
- Runtime memory analysis
- FFNx engine reverse-engineering

**Status**: Further investigation required (see "Required Next Steps" above).

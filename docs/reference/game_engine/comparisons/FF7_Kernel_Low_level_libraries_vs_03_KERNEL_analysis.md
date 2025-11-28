# Detailed Content Analysis: FF7_Kernel_Low_level_libraries.md vs 03_KERNEL.md

**Analysis Date:** 2025-11-28 16:42 JST
**Analyzer Note:** Comprehensive comparison to identify extraction opportunities for granular documentation

---

## Executive Summary

The individual file `FF7_Kernel_Low_level_libraries.md` (128 lines) is a **condensed reference guide** covering low-level libraries and data archive formats (BIN, LZS, LGP). The major section `03_KERNEL.md` (1,641 lines) is a comprehensive system documentation covering kernel architecture, memory management, and exhaustive binary format specifications.

**Key Finding:** The individual file is **NOT redundant** - it serves as a focused, approachable overview. However, the major section contains **significantly more technical depth** in the same topic areas, including:

- Complete KERNEL.BIN binary specifications (27 sections, 400+ lines)
- Advanced LZS compression algorithm with worked examples
- Detailed texture format specifications at binary level
- 3D model format documentation (HRC, RSD, P files)
- Memory architecture and VRAM management strategy

**Extraction Recommendation:** The major section contains multiple topics that should be extracted into the individual file OR should replace/supplement it. This analysis identifies specific content to merge.

---

## Topic Boundary Analysis

### File Scope Definitions

**FF7_Kernel_Low_level_libraries.md** (Current Scope):
- PC to PSX format comparison
- Data archive systems (BIN, LZS, LGP)
- Texture formats (TIM, TEX) - brief overview
- 3D model formats - high-level reference only

**03_KERNEL.md** (Comprehensive Scope):
- **Section I:** Kernel Overview & History (NES banking to FF7)
- **Section II:** Memory Management (RAM, VRAM, CD-ROM)
- **Section III:** Game Resources (KERNEL.BIN structure, 27 sections, binary specs)
- **Section IV:** Low Level Libraries (archives, textures, models - DETAILED)

### Overlap Identification

The individual file and major section **overlap significantly** in Sections IV of the major file. Both document:
1. PC to PSX comparison (Lines 8-16 individual, Lines 551-559 major)
2. Data Archives (Lines 18-101 individual, Lines 561-665+ major)
3. Textures (Lines 103-113 individual, Lines 746-865 major)
4. 3D Models (Lines 115-127 individual, Lines 880-1480+ major)

---

## Content Already in Individual File

### Category A1: PC to PSX Comparison (Lines 8-16)

**Present in Individual File:**
```
"The files and data formats used in the PSX version of FF7 and it's PC port
are conceptually the same thing... Psy-Q development library... TIM file...
converted to a TEX file..."
```

**Status:** Brief overview present. Sufficient for basic understanding.

**Comparison with Major Section (Lines 551-559):**
- Major section has nearly identical text
- No new information in major section for this topic

---

### Category A2: BIN Archive Format (Lines 22-93)

**Present in Individual File (Lines 22-93):**

**BIN Type Archives (Lines 26-28):**
- Uncompressed archives
- 4-byte header with file length

**BIN-GZIP Type Archives (Lines 30-93):**
- 6-byte header
- Table with offsets: Length of gzipped section, Length of ungzipped section, File type
- Gzip header format [0x1F8B080000000000...]
- Notes on file type usage with examples (KERNEL.BIN uses 0-8 for data files, 9 for text)

**Status in Major Section (Lines 565-591):**
- Major section has IDENTICAL structure and content
- Table layout is slightly different (tabular vs prose) but information matches
- "BIN Types" vs "BIN Type Archives" - same content
- "BIN-GZIP Types" vs "BIN-GZIP Type Archives" - same content

**Verdict:** Content fully present in individual file. No extraction needed.

---

### Category A3: LZS Archives Reference (Lines 95-97)

**Present in Individual File (Lines 95-97):**
```
"The LZS format is used throughout the PSX version of Final Fantasy 7,
often ending with the .lzs extension. LZS itself stands for Lempel-Ziv-Shannon-Fano..."
```

**Status:** Only reference provided, no format specification in individual file

**In Major Section (Lines 592-665):**
- Complete LZS format specifications
- Control byte scheme (1=literal, 0=reference)
- Reference format: OOOO OOOO OOOO LLLL (12-bit offset, 4-bit length)
- Length encoding (add 3, gives 3-18 byte range)
- Offset calculation formula: `real_offset = tail - ((tail - 18 - raw_offset) mod 4096)`
- Detailed worked example at position 1000, offset 339, length 5
- Edge case handling for negative offsets and repeated runs
- Explanation of why FF7 files must handle both edge cases

**Verdict:** Individual file lacks technical detail. Should extract major section content.

---

### Category A4: LGP Archives (Lines 99-101)

**Present in Individual File (Lines 99-101):**
```
"The LGP file format is only used for the PC port of Final Fantasy 7...
reference the data within it by filename. Its file format is explained here."
```

**Status:** Only brief mention with reference link. No format in individual file.

**In Major Section (Lines 666-737):**
- **Four-section structure** clearly defined
- **Section 1: FILE HEADER**
  - 12-byte creator string (SQUARESOFT or FICEDULA-LGP for patches)
  - 4-byte integer: file count
  - TOC entries: 20-byte filename + 4-byte data offset + 1-byte check code + 2-byte duplicate code
- **Section 2: CRC CODE**
  - Typically 3602 bytes
  - Validates archive integrity
  - Cannot be manually created (must be copied from existing)
- **Section 3: ACTUAL DATA**
  - Each file has header: 20-byte filename + 4-byte length + file data
- **Section 4: TERMINATOR**
  - "FINAL FANTASY 7" or "LGP PATCH FILE"

**Important Notes from Major Section:**
- Game is flexible: TOC and actual filenames can mismatch
- Can point multiple TOC entries to same data
- Data gaps allowed if unreferenced
- 4-byte skip offset for files smaller than originals
- Links to tools: LGP Tools, Emerald, Unmass

**Verdict:** Major section has COMPLETE technical specification. Individual file severely lacking. Should extract.

---

### Category A5: Textures Overview (Lines 103-113)

**Present in Individual File (Lines 103-113):**

**General texture concept (Lines 103-105):**
```
"A texture is just a picture that is placed into video memory...
native format of a texture was the Psy-Q TIM (Texture Image Map)"
```

**TIM texture format reference (Lines 107-109):**
- Brief statement that TIM files are found in raw format and archives (BIN, LZS, MNU)
- Mentions no 24-bit support in FF7
- GPU access requirements

**TEX texture format reference (Lines 111-113):**
- States TEX files are for PC
- Links to format documentation

**Status:** Only conceptual overview. No binary specifications.

**In Major Section (Lines 746-865):**

**TIM Format (PSX) - Complete Specifications (Lines 750-845):**

**Basic Terms (Lines 756-768):**
- CLUT: Color lookup table
- VRAM Location: Where texture loads in VRAM
- CLUT Location: Where palette loads in VRAM

**4 Bits Per Pixel (Lines 774-800):**
```
| Offset | Size | Description |
| 0x00 | 4 bytes | 10 00 00 00: TIM ID |
| 0x04 | 4 bytes | 08 00 00 00: 4bpp flag |
| 0x08 | 4 bytes | Unknown |
| 0x0c | 2 bytes | CLUT Location X |
| 0x0e | 2 bytes | CLUT Location Y |
| 0x10 | 2 bytes | Unknown |
| 0x12 | 2 bytes | Number Of CLUT entries |
| 0x14 | 32 bytes per CLUT (16 colors) | CLUT Data |
| +0x00 | 4 bytes | Unknown |
| +0x04 | 2 bytes | VRAM Location X |
| +0x06 | 2 bytes | VRAM Location Y |
| +0x08 | 2 bytes | Image Width / 4 |
| +0x10 | 2 bytes | Image Height |
| +0x12 | Varies | Pixel data |
```
- Pixel packing: each byte contains left and right pixel

**8 Bits Per Pixel (Lines 802-827):**
- Similar structure to 4bpp
- 512 bytes per CLUT (256 colors)
- Each byte is single pixel index

**16 Bits Per Pixel (Lines 829-845):**
- 1 pixel per 2 bytes
- BGR format with mask bit: `[ggg[rrrrr][m][bbbbb]gg]`

**TEX Format (PC) - Complete Specifications (Lines 847-864):**
```
| Offset | Size | Description |
| 0x00 | 56 bytes | Unknown |
| 0x38 | 4 bytes | bit depth (4, 8, or 16) |
| 0x3c | 4 bytes | Image Width |
| 0x40 | 4 bytes | Image Height |
| 0x44 | 20 bytes | Unknown |
| 0x58 | 4 bytes | Number of Palette Entries |
| 0x5c | 144 bytes | Unknown |
| 0xec | Palette Entries * 4 | BGRA color data |
| Varies | (sizex * sizey) or (sizex * sizey * 2) | Bitmap data |
```
- Bit depth variations: 4, 8, or 16
- 16-bit format: RGB555 colors
- Palette-indexed for 4/8-bit, direct RGB for 16-bit

**Verdict:** Individual file completely lacks binary specifications. Major section has complete technical details. **CRITICAL EXTRACTION NEEDED.**

---

### Category A6: 3D Model Formats Overview (Lines 115-127)

**Present in Individual File (Lines 115-127):**

**General statement (Lines 115-119):**
- Models exported from Psy-Q 3D formats: RSD, PLY, GRP, MAT, TIM, HRC, ANM
- Different animation systems for battle vs field models
- PC conversion from Psy-Q to PC formats (some original uncompiled files)

**Model storage locations (Lines 121-127):**
- PSX: ENEMY1-6, FIELD, MAGIC, STAGE1-2
- PC: LGP files with obfuscated names, HRC/RSD/P files explain structure

**Status:** Conceptual overview only. No binary format specifications.

**In Major Section (Lines 866-1480+):**

**HRC Hierarchy Format (Lines 880-970):**

Plain text format with structure:
```
:HEADER_BLOCK 2
:SKELETON sd_yufi_sk
:BONES 24
hip
root
2.9662
1 ABJC
... (repeats for each bone)
```

**Header Block** (Lines 922-936):
- `:HEADER_BLOCK 2` - ID line
- `:SKELETON [name]` - skeleton identifier
- `:BONES [count]` - bone count

**Bone Structure** (Lines 938-964):
Each bone has 4 lines:
1. Bone name (e.g., "hip")
2. Parent bone name or "root"
3. Bone length (float value, e.g., 2.9662)
4. RSD file association count + filenames

**Important Notes** (Lines 966-968):
- No bone angles, only lengths
- Hierarchy only (not skeleton)
- Animation data in separate .a files

**RSD Resource Data Format (Lines 972-1031):**

Plain text format:
```
@RSD940102
# Output by SGI RSD fileset library libRsdObj.
PLY=ACAB.PLY
MAT=ACAB.MAT
GRP=ACAB.GRP
NTEX=3
TEX[0]=ACAC.TIM
TEX[1]=ACAD.TIM
TEX[2]=ACAE.TIM
```

**Components**:
- `@RSD940102` - ID (date: January 2, 1994)
- `PLY=` - Polygon data filename
- `MAT=` - Material filename
- `GRP=` - Polygon group filename
- `NTEX=` - Texture count
- `TEX[x]=` - Texture filenames (TIM → TEX conversion note)

**"P" Polygon File Format (Lines 1033-1480):**

**Introduction & Structure** (Lines 1035-1078):
- 128-byte header
- File structure diagram with components
- Variable-sized arrays for vertices, normals, texture coords, colors, edges, polygons, hundrets, groups, bounding box, normal index table

**Header Structure** (Lines 1080-1133):
```
typedef struct {
    long off00;
    long off04;
    long VertexColor;
    long NumVerts;
    long NumNormals;
    long off14;
    long NumTexCs;
    long NumNormInds;
    long NumEdges;
    long NumPolys;
    long off28;
    long off2c;
    long mirex_h;
    long NumGroups;
    long mirex_g;
    long off3c;
    long unknown[16];
} t_p_header;
```

**Chunks** (Lines 1141-1480):

1. **Vertex Chunk** (Lines 1141-1162)
   - Offset: 0x80
   - Each vertex: 12 bytes (3x 4-byte floats: X, Y, Z)

2. **Normals Chunk** (Lines 1164-1168)
   - Offset: 0x80 + (NumVerts * 12)
   - Each normal: 12 bytes

3. **Texture Coordinate Chunk** (Lines 1170-1190)
   - Each coord: 8 bytes (2x 4-byte floats: X, Y)
   - Values 0.0-1.0 (wraps beyond 1.0)

4. **Vertex Color Chunk** (Lines 1192-1209)
   - Each color: 4 bytes (BGRA format)

5. **Polygon Color Chunk** (Lines 1211-1217)
   - Each color: 4 bytes

6. **Edge Chunk** (Lines 1219-1234)
   - Each edge: 4 bytes (2x 2-byte shorts: vertex indices)

7. **Polygon Chunk** (Lines 1236-1266)
   - Each polygon: 24 bytes
   - Structure: Tag1 (short) + Vertex[3] (shorts) + Normal[3] (shorts) + Edge[3] (shorts) + Tag2 (long)

8. **Hundrets Chunk** (Lines 1268-1314)
   - Each entry: 100 bytes
   - Texture information (details unclear)

9. **Group Chunk** (Lines 1321-1428)
   - Each group: 56 bytes
   - Structure with polyType, offsets, counts, texture info

10. **Bounding Box** (Lines 1430-1460)
    - 24 bytes
    - Max/Min coordinates for X, Y, Z

11. **Normal Index Table** (Lines 1462-1480)
    - 4-byte integers mapping vertices to normals

**Verdict:** Individual file completely lacks binary format details. Major section has **extensive technical documentation** covering HRC, RSD, and P file formats with complete binary specifications. **CRITICAL EXTRACTION NEEDED.**

---

## Content NOT Currently in Individual File

### Category B1: KERNEL.BIN Binary Specifications (NOT in individual file)

**Location in Major Section:** Lines 88-545

**Scope:** Complete binary format for all 27 KERNEL.BIN sections with offset specifications

**Critical Content Not in Individual File:**

**KERNEL.BIN Structure (Lines 94-123):**
Table listing all 27 sections with offsets:
- Section 1: Command data (0x0006)
- Section 2: Attack data (0x0086)
- Section 3: Unknown/Savemap (0x063A)
- Section 4: Character starting stats (0x0F7F)
- ... continuing through Section 27: Summon Attack Names (0x5692)

**Section 1: Command Data (Lines 128-144):**
- 16 bytes per record
- Table layout shown but incomplete in source (empty table body)

**Section 2: Attacks Data (Lines 146-189):**
```
| Offset | Length | Description |
| 0x00 | 4 bytes | Unknown |
| 0x04 | 1 byte | Casting cost |
| 0x05 | 5 bytes | Unknown |
| 0x0A | 1 byte | Attack type |
| 0x0B | 2 bytes | Attack attribute |
```
- Attack attributes include 13 specific types:
  - Escape/Exit-Type (0x0000)
  - Ribbon-Like (0x0001)
  - Enemy Skill (0x0003, 0x0005, 0x0007)
  - Restorative/Protective (0x000D)
  - Status-giving/Elemental (0x000F)
  - Shield (0x0011)
  - Limit Break (0x0013)
  - Cait Sith Limit Break (0x0015)
  - Summon (0x0017)
  - Roulette (0x00C7)
  - Multiple Strike Limit breaks (0x0097)
  - Phoenix Down (0xFF01)
  - X-needles attack (0xFF03)
  - Final Limit break (0xFF17)

**Section 3: Savemap (Lines 190-192):**
- Initial values for savemap
- Range: 0x0054 to 0x0fe7

**Section 4: Initialization Data (Lines 194-196):**
- Starting character stats
- Range: 0x0054 to 0x0BAF

**Section 5: Item Data (Lines 198-250):**
```
| Offset | Length | Description |
| 0x00 | 8 bytes | Unknown [Always 0xFFFFFFFF] |
| 0x08 | 2 bytes | Unknown |
| 0x0A | 1 byte | Restriction Mask |
|      |       | 0xFF - Item menu only |
|      |       | 0xFE - Battle + Item menu (not usable) |
|      |       | 0xFD - Item menu, Battle usable |
|      |       | 0xFC - Battle + Item menu, Battle usable |
|      |       | 0xFB - Item menu, Item usable |
|      |       | 0xFA - Battle + Item menu, Item usable |
|      |       | 0xF9 - Item menu, both menus usable |
|      |       | 0xF8 - Battle + Item, both usable |
|      |       | 0xF7 - Item menu, Battle usable |
|      |       | 0xF6 - Battle + Item menu, Battle usable |
| 0x0B | 2 bytes | Attack Target |
|      |       | 0x01 - One target |
|      |       | 0x03 - Unknown |
|      |       | 0x05 - Multiple targets |
|      |       | 0x07 - Unknown |
|      |       | 0x10 - Party only |
| 0x0D | 1 byte | Item ID |
| 0x0E | 1 byte | Restore Apply |
| 0x0F | 1 byte | Amount Multiplier |
| 0x10 | 1 byte | Restore Type |
| 0x11 | 3 bytes | Unknown |
| 0x14 | 4 bytes | Status effects |
| 0x18 | 2 bytes | Element |
| 0x1A | 2 bytes | Unknown |
```

**Section 6: Weapon Data (Lines 252-334):**
- 44 bytes per record
- Range, special options, attack stats, materia growth, model ID
- Equip masks for 10 characters (Cloud, Barret, Tifa, Aeris, Red XIII, Yuffie, Cait Sith, Vincent, Cid, Young Cloud, Sephiroth)
- Attack types: Cut, Hit, Punch
- Stat bonuses (STR, VIT, MAG, SPI, DEX, LUC)
- Materia slot types (No Slot, Unlinked, Left Linked, Right Linked)
- Restriction masks (9 types)

**Section 7: Armor Data (Lines 336-398):**
- 36 bytes per record
- Damage type: Normal, Absorb, No Damage, Half
- Defense and Magic Defense percentages
- Materia slots (8 bytes)
- Equip masks for character groups (Everyone, All Females, All Males)
- Element and stat bonuses

**Section 8: Accessory Data (Lines 400-489):**
- 16 bytes per record
- Stat bonuses (2 bytes) with 6 stat types
- Bonus amount (2 bytes)
- Elemental strength (Drains/Nullifies)
- Special effects: Haste, Fury, Curse Ring, Reflect, Stealing, Manipulation, Barrier/MBarrier
- Elemental types (Fire, Ice, Lightning, Earth, Poison, Gravity, Water, Wind, Holy, All)
- Status protections (17 types and combinations)
- Equip masks (10 characters)
- Restriction masks (8 types)

**Section 9: Materia Data (Lines 491-544):**
- 20 bytes per record
- Level-up AP limits (8 bytes, multiples of 100)
- Equip Effect with stat modifications table (18 entries with STR/VIT/MAG/MDEF/MAXHP/MAXMP/LUCK/DEX bonuses)
- Status bitmask (3 bytes)
- Element (1 byte)
- Materia type (1 byte) with 11 values:
  - Master Command (0x08)
  - Master Magic (0x0A)
  - Master Summon (0x0C)
  - Command (0x12, 0x16)
  - Magic (0x19)
  - Booster% (0x20)
  - W-Command (0x33)
  - Summon (0x3B)
  - Enemy Skill (0x57)
- Materia attributes (6 bytes)

**Verdict:** **CRITICAL EXTRACTION NEEDED.** Individual file completely lacks all KERNEL.BIN binary specifications. This is fundamental data for anyone working with FF7 modding. All 475 lines (88-545) of KERNEL.BIN documentation should be evaluated for extraction.

---

### Category B2: Advanced LZS Compression Algorithms (NOT in individual file)

**Location in Major Section:** Lines 592-665

**Scope:** Complete technical specification of LZS compression used in FF7

**Content:**

**LZS Archive Format** (Lines 594-596):
- 4-byte header with decompressed file length
- Followed by compressed data

**Control Byte Scheme** (Lines 598-628):
- Each block starts with control byte
- Read right-to-left: 1=literal, 0=reference
- Literal: read 1 byte directly to output
- Reference: 2-byte pointer to previous data

**Reference Format** (Lines 608-626):
```
OOOO OOOO OOOO LLLL (O=Offset, L=Length)
```
- 12-bit offset: can reference last 4K of data
- 4-bit length: 0-15 (add 3 for actual 3-18 byte range)
- Offset calculation formula:
  ```
  real_offset = tail - ((tail - 18 - raw_offset) mod 4096)
  ```

**Worked Example** (Lines 630-654):
```
Position: 1000
Control byte: 0x03 = 00000011 binary
Result: 2 compressed references (4 bytes) + 6 literal bytes

First reference: 0x53 0x12
Base offset: 0x153 (339 decimal)
Base length: 0x2
Final length: 5 (add 3)
Final offset: 1000 - ((1000 - 18 - 339) mod 4096) = 357
```

**Edge Cases** (Lines 656-664):
1. **Negative offsets:** Write null bytes (buffer initialized to zeros)
2. **Repeated runs:** Loop output when reading past current position
   - Example: reading 15 bytes from offset 5 bytes back means repeat data

**FF7 Specifics:** FF7 uses both edge case tricks

**Verdict:** **EXTRACTION RECOMMENDED.** Individual file only mentions LZS by name without any technical specification. This content is valuable for implementation and understanding. All 73 lines (592-665) should be considered for extraction or linking.

---

### Category B3: Memory Architecture and System Design (NOT in individual file)

**Location in Major Section:** Lines 1-79

**Content Not in Individual File:**

**Kernel History and Design** (Lines 3-26):
- NES FF1 memory banking (MMC1 controller)
- 16KB sections, 32KB total ROM limit
- Non-bankable 16KB bottom section for kernel
- Main program loop, interrupt control, module switching, music playback

**Evolution of Kernel/Module System** (Lines 7-13):
- FF6 SNES to PSX conversion lag issues
- FF7 PC menu integration without module banking

**Kernel Functionality** (Lines 15-25):
- Threaded multitasking program
- Software-based memory manager (RAM + VRAM)
- Psy-Q library integration
- PC equivalents (SEQ player → MIDI player)

**Architecture Diagram** (Lines 19-25):
```
User
Module
Kernel
Psy-Q libraries
PSX BIOS
Hardware
```

**RAM Management** (Lines 29-47):
- Save Map: 4,340 bytes (0x10F4)
- 5 banks of field script memory
- Temporary field variables (256 bytes)
- Memory map with offsets and bank IDs

**VRAM Management** (Lines 49-71):
- 2048x512 pixel surface representation
- Double-buffering system
- Texture cache boundaries
- CLUT (Color Lookup Table) organization
- Blank areas for V-sync
- Permanent textures and font storage
- Cache volatility ordering

**PSX CD-ROM Management** (Lines 73-77):
- Hardware access restrictions through BIOS
- Module preloading strategy
- 8KB quick-load mode
- Low-level sector-based access (not filename-based)

**Verdict:** **NOT EXTRACTABLE to individual file.** This content belongs in separate architectural/system documentation. Individual file `FF7_Kernel_Low_level_libraries.md` should focus on low-level libraries, not system architecture.

---

## Summary of Content Categories

### EXTRACT TO INDIVIDUAL FILE (Category B - Critical Gaps)

| Topic | Lines | Priority | Why |
|-------|-------|----------|-----|
| **LZS Compression Algorithm** | 592-665 | HIGH | Essential technical reference, currently only mentioned by name |
| **LGP Archive Format** | 666-737 | HIGH | Complete specification missing from individual file |
| **TIM Texture Format** | 750-845 | HIGH | Binary structure needed for implementation |
| **TEX Texture Format** | 847-864 | HIGH | Binary structure needed for PC texture work |
| **HRC Hierarchy Format** | 880-970 | MEDIUM | 3D model skeleton documentation |
| **RSD Resource Format** | 972-1031 | MEDIUM | 3D model reference documentation |
| **P File Format** | 1033-1480+ | MEDIUM | Polygon model binary specification |
| **KERNEL.BIN Sections** | 88-545 | CRITICAL | Game data binary specifications |

### DO NOT EXTRACT (Belongs Elsewhere)

| Topic | Lines | Reason |
|-------|-------|--------|
| Kernel History/Design | 1-26 | System architecture documentation |
| Memory Architecture | 27-79 | System architecture documentation |
| VRAM Layout Strategy | 49-71 | System architecture documentation |
| CD-ROM Management | 73-77 | System architecture documentation |

### ALREADY IN INDIVIDUAL FILE

| Topic | Lines (Individual) | Status |
|-------|-------------------|--------|
| PC to PSX Comparison | 8-16 | Complete |
| BIN Archive Format | 22-93 | Complete |
| LZS Archives | 95-97 | Name only, needs expansion |
| LGP Archives | 99-101 | Name only, needs expansion |
| Textures | 103-113 | Conceptual only, needs binary specs |
| 3D Models | 115-127 | Overview only, needs binary specs |

---

## Technical Discrepancies

### None Found

Both files are technically accurate within their respective scopes. No contradictory information identified.

---

## Integration Guidance

### Option 1: Expand Individual File (RECOMMENDED)

**Approach:** Keep the individual file as the authoritative low-level libraries reference, then add missing technical content from major section.

**Steps:**
1. Keep Lines 8-127 as foundation (all content already present)
2. Expand "LZS Archives" section (Lines 95-97):
   - Replace brief reference with full lines 592-665 from major section
   - Add complete algorithm specification with worked examples
3. Expand "LGP Archives" section (Lines 99-101):
   - Add complete lines 666-737 specification
   - Include 4-section structure, header formats, CRC notes
4. Expand "Textures" section (Lines 103-113):
   - Add complete TIM format (lines 750-845)
   - Add complete TEX format (lines 847-864)
   - Include binary offset tables and pixel packing details
5. Expand "3D Models" section (Lines 115-127):
   - Add HRC format (lines 880-970)
   - Add RSD format (lines 972-1031)
   - Add P file format (lines 1033-1480)
6. Add new section: "KERNEL.BIN Binary Specifications"
   - Include all lines 88-545 from major section
   - Organize by section number with complete offset tables

**Result:** Individual file would grow from 128 lines to ~800-900 lines, becoming comprehensive low-level reference

### Option 2: Maintain Layered Documentation

**Approach:** Keep individual file as quick reference, create specialized sub-documents for deep dives.

**Create new files:**
- `FF7_Kernel_Archives_LZS.md` - LZS compression algorithms (lines 592-665)
- `FF7_Kernel_Archives_LGP.md` - LGP archive format (lines 666-737)
- `FF7_Kernel_Textures_TIM.md` - TIM format specifications (lines 750-845)
- `FF7_Kernel_Textures_TEX.md` - TEX format specifications (lines 847-864)
- `FF7_Kernel_Models_HRC.md` - HRC hierarchy format (lines 880-970)
- `FF7_Kernel_Models_RSD.md` - RSD resource format (lines 972-1031)
- `FF7_Kernel_Models_P.md` - P polygon format (lines 1033-1480)
- `FF7_Kernel_Binary.md` - KERNEL.BIN specifications (lines 88-545)

**Keep:** Individual file as gateway/index with links to specialized documents

**Result:** Better organization, easier maintenance, modular reference structure

### Option 3: Deprecate Individual File

**Approach:** Remove individual file, consolidate all content into major section, organize better.

**Pros:**
- Single source of truth
- No redundancy concerns
- Easier maintenance

**Cons:**
- 1,600+ line document becomes unwieldy
- Individual file served as digestible entry point
- Loses quick-reference functionality

**Not recommended unless major section is significantly reorganized**

---

## Recommendations Summary

### Immediate Actions

1. **Choose integration approach** (Option 1 or 2 recommended)
2. **Extract LZS compression content** (Lines 592-665) - most critical missing technical content
3. **Extract LGP archive format** (Lines 666-737) - complete specification missing
4. **Extract texture binary formats** (Lines 750-865) - essential for texture work
5. **Extract 3D model formats** (Lines 880-1480) - essential for model work
6. **Add KERNEL.BIN reference** (Lines 88-545) - fundamental game data

### Quality Improvements

1. **Complete the Command Data table** (Line 130-144 in major section)
2. **Replace Lorem Ipsum** (Line 874) with real PSX model format content
3. **Clarify Materia Attributes** (Lines 514-525) structure explanation
4. **Add worked examples** to complex formats (LZS already has one, consider others)

### Documentation Standards

1. **Version numbering:** Add to both files for clarity
2. **Cross-references:** Link between files to reduce confusion
3. **Scope statements:** Clear definition of individual file as reference guide vs major section as comprehensive
4. **Update dates:** Indicate which document is most current

---

## Conclusion

The individual file `FF7_Kernel_Low_level_libraries.md` is **not redundant** - it serves a critical function as an accessible reference guide. However, it is **significantly incomplete** relative to the technical depth available in the major section.

**Recommendation:** Pursue **Option 1 (Expand Individual File)** to create a comprehensive, self-contained low-level libraries reference. This will:
- Preserve the focused scope
- Add critical missing technical content
- Provide a single authoritative source for library-level documentation
- Serve both quick-reference and deep-dive needs

**Priority extraction targets:**
1. KERNEL.BIN binary specifications (276 lines) - CRITICAL
2. LZS compression algorithms (73 lines) - HIGH
3. LGP archive format (71 lines) - HIGH
4. Texture binary formats (115 lines) - HIGH
5. 3D model formats (600+ lines) - MEDIUM


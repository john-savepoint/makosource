# Comparison: FF7_Savemap.md vs 03_KERNEL.md

## File Sizes
- **FF7_Savemap.md**: 3,861 lines (comprehensive, highly detailed)
- **03_KERNEL.md**: 1,641 lines (broad overview, architectural focus)

## Overview

These two files address **completely different scopes**:

- **FF7_Savemap.md**: A reference manual for the FF7 save file data structure—the in-memory representation and persistent storage format for game state
- **03_KERNEL.md**: A comprehensive guide to the Kernel system, including memory/VRAM management, game resources, low-level libraries, file formats, and 3D model handling

## Topics Covered in BOTH Files

### 1. Save Map Structure and Initialization
- **FF7_Savemap.md** (lines 19–466):
  - Detailed save slot format with exact byte offsets
  - Character preview data
  - Lead character stats and party composition

- **03_KERNEL.md** (lines 190–192):
  - Brief reference: "Section 3 Savemap" in KERNEL.BIN
  - States it contains initial savemap structure (0x0054–0x0fe7)
  - Notes format is explained in "Menu" section (not provided here)

**Nature of Overlap**: 03_KERNEL.md mentions the savemap exists but doesn't detail it; FF7_Savemap.md provides the complete reference implementation.

### 2. KERNEL.BIN Section 4 and Character Initialization
- **FF7_Savemap.md** (lines 3845–3847):
  - References Section 4 from KERNEL.BIN
  - States it contains initial values for save structure (0x0054–0x0B93)

- **03_KERNEL.md** (lines 194–196):
  - Full definition: "Section 4 Initialization data"
  - Explains this contains starting stats for characters
  - Notes data is copied to save map on "New Game"

**Nature of Overlap**: Both files discuss the same KERNEL.BIN section; 03_KERNEL.md explains its purpose, FF7_Savemap.md references it as initialization source.

---

## Content ONLY in Individual File (FF7_Savemap.md)

This file is **dedicated entirely to save map documentation**. Its unique content includes:

### 1. Save Memory Banks (Lines 468–3422)
- **Bank 1/2** (0x0BA4–0x0CA3): Party data, love points, game state
- **Bank 3/4** (0x0CA4–0x0DA3): Story flags and event progression
- **Bank B/C** (0x0DA4–0x0EA3): Equipment, item collections, location data
- **Bank D/E** (0x0EA4–0x0FA3): Materia management, character progression
- **Bank 7/F** (0x0FA4–0x10F3): Countdown timers, special status flags

Each bank section contains **dozens to hundreds of individual field definitions** with bit masks, offset values, and contextual explanations. Example fields:
- Main progress variable
- Love point tracking for multiple romance options
- Fort Condor battle statistics
- Chocobo breeding parameters
- Snowfield puzzle state
- Gold Saucer wedding dress acquisition
- World map event flags

### 2. Character Record Structure (Lines 3423–3712)
Complete breakdown of 96-byte character data per playable character:
- Level, base/bonus stats (STR, VIT, MAG, SPR, DEX, LCK)
- Name (12-byte FF Text format)
- Equipment (weapon/armor/accessory IDs)
- Limit level and bar
- Learned limit skills (bit flags)
- Kill count
- Materia slots and equipped materia (8 slots per location)
- Experience to next level

### 3. Chocobo Record (Lines 3714–3731)
Dedicated table for chocobo breeding mechanics:
- Sprint speed and max sprint speed
- Speed and max speed
- Personality traits (cooperation, intelligence)
- Race history (wins, gender, type)

### 4. Save Item and Materia Lists (Lines 3734–3843)
- **Item List Format**: 7-bit quantity + 9-bit item index encoding
  - 320 total item slots (items, weapons, armor, accessories indexed separately)
  - Quantity limitations and game behavior

- **Materia List**: Single-byte ID + 24-bit AP value
  - Complete ID table: All 91+ materia types listed with names and categories
  - Special handling for Enemy Skill materia

### 5. Documentation Notes (Lines 3849–3862)
Explanation of format conventions used throughout the file (bit numbering, field keywords, hex value references).

---

## Content ONLY in Major Section (03_KERNEL.md)

### 1. Kernel History and Architecture (Lines 3–26)
- NES/FF1 memory mapper heritage (MMC1)
- Evolution through Final Fantasy series
- Kernel's role as main program loop
- Differences between PSX and PC implementations
- Psy-Q library usage

### 2. Memory Management Architecture (Lines 27–77)
- RAM management overview (4,340 bytes reserved)
- VRAM allocation strategy
  - Pixel surface representation (2048×512 PSX VRAM)
  - Video frame buffers and double-page buffering
  - Texture cache boundaries and volatility
  - CLUT (Color Look-Up Table) management
- CD-ROM access strategies
  - BIOS restrictions and workarounds
  - Quick mode preloading (8KB chunks)
  - Sector-based file references

### 3. KERNEL.BIN Complete Structure (Lines 88–122)
Full table of all 27 sections with offsets:
- Sections 1–9: Data formats (commands, attacks, savemap, initialization, items, weapons, armor, accessories, materia)
- Sections 10–27: Text data (descriptions, names, battle text, summon attacks)

### 4. Detailed KERNEL.BIN Section Formats (Lines 124–490)

#### Section 1: Command Data (128–145)
- 16 bytes per command record
- (Incomplete table in source)

#### Section 2: Attacks/Magic Data (146–188)
- 28 bytes per attack record
- Casting cost
- Attack type and attribute flags
  - Escape/Exit, Ribbon-like, Enemy Skill, Restorative, Status-giving, Shield, Limit Break, Summon, Roulette, Phoenix Down, Final Limit Break
- ID number, restore mechanics, strength
- Status effects and elements

#### Section 5: Item Data (198–250)
- 27 bytes per item
- Restriction masks (appearance in menus/battles, usability)
- Attack targets
- Restore mechanics (HP, MP, ailment)
- Status effects and elemental damage

#### Section 6: Weapon Data (252–335)
- 44 bytes per weapon
- Range (long/normal)
- Attack modifiers (special options like Tifa's status-dependent bonuses)
- Attack values and model IDs
- Equip masks (character availability)
- Attack types (cut, hit, punch)
- Stat increases
- Materia slot configuration (unlinked/linked)

#### Section 7: Armor Data (336+)
- 36 bytes per armor record
- Damage type and elemental properties
- (Structure continues beyond readable excerpt)

#### Section 8: Accessory Data (400+)
- Format structure (beyond readable excerpt)

#### Section 9: Materia Data (491+)
- Format structure (beyond readable excerpt)

### 5. File Format Standards (Lines 549–1641+)

#### BIN Archive Formats (561–720)
- **BIN-GZIP Types**: Standard format with 6-byte headers
- **LZS Compression**: Custom PSX compression format
  - Flag bytes and compression algorithms
  - Reference and example decompression
- **LGP Archive Format**: PC-specific container
  - File header section
  - CRC code section
  - Actual data section
  - Terminator section

#### Texture Data Formats (746–865)
- **TIM Format** (PSX native):
  - 4/8/16 bits per pixel modes
  - CLUT (palette) handling
  - VRAM location specifications

- **TEX Format** (PC, by Mirix):
  - Alternative texture storage

#### 3D Model Formats (866–1636+)
- **HRC Hierarchy Format** (PC, by Alhexx):
  - Header, bones, joint data
  - Skeleton structure for character/enemy models

- **RSD Resource Data Format** (PC, by Alhexx):
  - Texture file references
  - Model grouping

- **P Polygon Format** (PC, by Alhexx, Ficedula, Mirex):
  - Complete 3D mesh specification:
    - Vertex chunks
    - Normals chunks
    - Texture coordinates
    - Vertex colors
    - Polygon colors
    - Edge data
    - Polygon definitions
    - Bounding boxes
    - Normal index tables
  - Grouping algorithms (5-step process with DOT-groups, TILDE-groups, absolute indices)

---

## Significant Differences in Detail Level

### 1. Scope Disparity
- **FF7_Savemap.md**: 100% focused on one data structure (the save file)
- **03_KERNEL.md**: Architectural overview touching 9 different subsystems

### 2. Byte-Level Detail
- **FF7_Savemap.md**: Every single offset from 0x0000 to end documented
  - Individual bit flags explained
  - Field keywords and hex values provided
  - Example: "0x04: Set to 1 if we choose no drink when talking to tifa [0x0F] {MDS7PB_1}"

- **03_KERNEL.md**: High-level descriptions of sections
  - Data structures outlined but not exhaustively documented
  - Example: "Section 3: Unknown (Savemap?)" — marked as unknown, defers to FF7_Savemap

### 3. Format Completeness
- **FF7_Savemap.md**: Complete from header through all character records, items, materia
- **03_KERNEL.md**: Sections 7–9 (armor, accessory, materia) are truncated/incomplete in available excerpt

### 4. Modding Context
- **FF7_Savemap.md**: Includes practical notes for modders (e.g., quantity limitations, Japanese PSX version bug at 99+ items)
- **03_KERNEL.md**: Engineering documentation of original design/architecture

---

## Recommendations

### Organization & Consolidation
- [ ] **No content consolidation needed** — Files serve different purposes:
  - FF7_Savemap.md = **Save File Reference Manual** (for modders/save editors)
  - 03_KERNEL.md = **Engine Architecture Guide** (for engine developers)

### Cross-Reference Improvements
- [ ] Add explicit link in 03_KERNEL.md from "Section 3: Unknown (Savemap?)" pointing to FF7_Savemap.md
  - Current text: "Section 3: Unknown (Savemap?)"
  - Suggested: "Section 3: Savemap (See [FF7_Savemap.md](../markdown/FF7_Savemap.md) for complete reference)"

- [ ] Update 03_KERNEL.md line 192 from generic reference to specific pointer:
  - Current: "This format is explained in the 'Menu' Section."
  - Suggested: "Complete documentation: [FF7_Savemap.md](../markdown/FF7_Savemap.md) (lines 19–3847)"

### Missing Content in 03_KERNEL.md
- [ ] Sections 7–9 (Armor, Accessory, Materia) data formats appear truncated
  - Recommend completing these sections from FF7_Savemap.md references or original sources

### Quality Improvements
- [ ] FF7_Savemap.md could benefit from section overview table
  - Create introductory table mapping offset ranges to section names/purposes
  - Example: "0x0000–0x0467: Save Preview Header" | "0x0BA4–0x0CA3: Memory Bank 1/2"

---

## Summary Table

| Aspect | FF7_Savemap.md | 03_KERNEL.md | Overlap? |
|--------|---|---|---|
| **Save Structure** | Complete detailed reference | Brief mention in KERNEL.BIN | Minimal (reference only) |
| **KERNEL.BIN Sections** | Referenced as initialization source | Full architectural overview | Section 3–4 only |
| **Memory Management** | Not covered | Comprehensive (RAM/VRAM/CD-ROM) | None |
| **File Formats** | Not covered | Complete (BIN, LZS, LGP, TIM, HRC, RSD, P) | None |
| **3D Models** | Not covered | Extensive (polygon format, grouping) | None |
| **Item Data** | As save state list | KERNEL.BIN section 5 format | Tangential |
| **Weapon Data** | As equipped items in character record | KERNEL.BIN section 6 format | Tangential |
| **Materia Data** | Complete list with IDs and AP encoding | KERNEL.BIN section 9 (incomplete) | Significant overlap possible |
| **Character Stats** | Detailed record structure | KERNEL.BIN section 4 (brief) | Conceptual only |

**Conclusion**: The files are **complementary, not redundant**. FF7_Savemap.md provides the reference implementation of one component that 03_KERNEL.md briefly describes at an architectural level.

# FF7_World_Map_Encounters.md vs 07_WORLD_MAP.md Analysis

**Analysis Date**: 2025-11-28 22:15 JST
**Analyst**: Claude Code
**Purpose**: Identify content extraction opportunities for FF7_World_Map_Encounters.md

---

## Executive Summary

**File Status**: FF7_World_Map_Encounters.md does not currently exist in the markdown/ directory. This analysis identifies what should be created based on content in the major section.

**Major Section Size**: 07_WORLD_MAP.md = 86 lines total
**Content Quality**: Mixed (40% Lorem Ipsum, 60% real technical content)
**Extraction Opportunity**: HIGH - Encounter system content is substantive and currently missing from individual files

**Key Findings**:
- Real encounter data documentation exists in major section (lines 7-72)
- Area mapping lists encounters by region (lines 29-72)
- No images or diagrams in major section
- World Map documentation already distributed across 4 individual files (Module, BSZ, TXZ, Script)
- Encounter system was never extracted to separate individual file

---

## Topic Scope Analysis: What Should FF7_World_Map_Encounters.md Cover?

Based on the MAPPING.md document and existing world map files, **FF7_World_Map_Encounters.md should document**:

1. **Encounter data format (PC version)**
   - File: enc_w.bin
   - Structure: Starting offset, section size, field layout
   - Encounter rates and battle formations
   - Chocobo-specific battles

2. **Area/Region organization**
   - How encounters are organized by game regions
   - Land vs. underwater vs. snow field distinctions
   - Area enumeration and offset calculations

3. **Data structures**
   - Encounter formation IDs
   - Chance calculations
   - Special formations vs. normal battles
   - Chocobo battle sections

**Related but separate files** (should NOT duplicate):
- FF7_WorldMap_Module.md - MAP/BOT format (mesh geometry)
- FF7_World_Map_BSZ.md - BSZ format (skeleton/animation data)
- FF7_World_Map_TXZ.md - TXZ format (textures and scripts)
- FF7_WorldMap_Module_Script.md - Script engine/opcodes

**Observation**: Encounters are distinct from geometry, textures, and animation - proper scope separation.

---

## Content Already in Individual Files

**FF7_WorldMap_Module.md** (235 lines):
- MAP file structure
- Mesh organization (16 meshes per block)
- Block arrangement (68 blocks, 7x9 grid + replacements)
- Walkmap types (32 types with descriptions)
- Texture system
- NO encounter data

**FF7_World_Map_BSZ.md** (137 lines):
- BSZ header structure
- Model sections (skeleton, parts, animations)
- PSX memory offsets
- NO encounter data

**FF7_World_Map_TXZ.md** (77 lines):
- TXZ compression (LZS)
- Archive format structure (6 sections)
- Texture data for VRAM
- Script/AKAO audio data
- NO encounter data

**FF7_WorldMap_Module_Script.md** (128 lines):
- Script engine architecture
- Stack-based opcodes
- Model entities and contexts
- Functions and event handlers
- .ev file format (call table, code section)
- NO encounter data

**Combined WorldMapModule.md** (596 lines):
- Aggregates all above content
- NO encounter data

**Conclusion**: Encounter system content is **completely absent** from all existing individual files.

---

## Content in Major Section (07_WORLD_MAP.md)

### Section I: World Map Overview (Lines 1-6)
- **Content**: Lorem Ipsum placeholder text
- **Status**: PLACEHOLDER - no substantive information
- **Action**: SKIP - not real content

### Section II: PC Format !!!!!!!!!!!!!!!!!!!!!!!! (Lines 7-72)
**Status**: REAL, SUBSTANTIVE CONTENT - PRIMARY EXTRACTION CANDIDATE

**Lines 7-28: Overview Context**
```
By the way, also had a brief look at the World Map... although things are different between
that and the field files, it naturally has many of the same data structures... dialogue's in
'mes', the event files are in 'wm0.ev', 'wm2.ev' and 'wm3.ev' (I assume... though I've not
gotten any conclusive proof that this is the case through a *brief* glance through them),
and the encounters are stored in 'enc_w.bin' (but may or may not follow the same rules
regarding encounter chances... unsure yet)
```
- **Importance**: Defines file locations and uncertainty notes
- **Should extract**: YES - provides context

**Lines 15-28: Encounter Data Format**
```
Encounter data for the World Map starts at offset 0xB8, and each section is 32 bytes each.
A section is defined as follows:

0x00: 01

0x01: Encounter Rate (1 byte)(?) (lower numbers mean higher encounter rates)
0x02-0x0D: Normal Battle+Chance of that battle (2 bytes each, 6 records)

0x0E-0x15: Special Formation Battles+Chance (2 bytes each, 4 records)

0x16-0x1F: Chocobo Battles (2 bytes each, 5 records)

Again, the chance byte for normal battles seems to always add up to 64.

Anyhow, as for how they're *stored*...
```
- **Importance**: Core technical specification - CRITICAL DATA
- **Should extract**: YES - this is the primary content

**Lines 29-72: Area Organization**
```
each area in the game has four fields, and they're aligned something like this:

Area - Grass
Area - Dirt/Snow
Area - Forest/Desert
Area - Beach

And the areas are naturally in this order:

Midgar Area
Kalm Area
[... 12 more areas ...]
Goblin Island
```
- **Importance**: Area enumeration for offset calculations
- **Should extract**: YES - essential reference data

### Sections III-V: Land, Underwater, Snow Field, Data Format (Lines 73-86)
- **Content**: Lorem Ipsum placeholders or empty sections
- **Status**: PLACEHOLDER
- **Action**: SKIP

---

## Detailed Content Comparison

### Content Type: Data Format Specifications
**Status**: MISSING FROM INDIVIDUAL FILES

From major section lines 15-28 (14 lines):
```
Encounter data for the World Map starts at offset 0xB8, and each section is 32 bytes each.
A section is defined as follows:

0x00: 01

0x01: Encounter Rate (1 byte)(?) (lower numbers mean higher encounter rates)
0x02-0x0D: Normal Battle+Chance of that battle (2 bytes each, 6 records)

0x0E-0x15: Special Formation Battles+Chance (2 bytes each, 4 records)

0x16-0x1F: Chocobo Battles (2 bytes each, 5 records)

Again, the chance byte for normal battles seems to always add up to 64.
```

**Appears in individual files?** NO
**Appears in combined file?** NO
**Should extract?** YES - This is core encounter system documentation

### Content Type: Area Enumeration
**Status**: MISSING FROM INDIVIDUAL FILES

From major section lines 29-72 (44 lines):
```
each area in the game has four fields...
[13 geographic areas listed with their 4 terrain variants]
```

**Appears in individual files?** NO
**Appears in combined file?** NO
**Should extract?** YES - This is reference data for understanding encounter offset calculations

### Content Type: File Location Context
**Status**: MISSING FROM INDIVIDUAL FILES

From major section lines 7-13 (7 lines):
```
dialogue's in 'mes', the event files are in 'wm0.ev', 'wm2.ev' and 'wm3.ev'...
encounters are stored in 'enc_w.bin'...
```

**Appears in individual files?** NO
**Should extract?** YES - Important context about file relationships

---

## Images in Extracted Content

**Search Result**: No images found in 07_WORLD_MAP.md
- No `![...]()` patterns detected
- No `<img>` tags detected
- **Action**: No image paths to adjust

---

## Substantive Content Additions Identified

### Addition 1: Encounter File Format Specification (14 lines)
- **Location**: Lines 15-28 in major section
- **Type**: Data structure specification with byte offsets
- **Importance**: CRITICAL - defines how encounter data is organized
- **Status in individual files**: NOT PRESENT
- **Extract**: YES - Foundation for encounter system documentation

### Addition 2: Area Reference List (44 lines)
- **Location**: Lines 29-72 in major section
- **Type**: Reference enumeration with area names and terrain variants
- **Importance**: HIGH - necessary for understanding area-to-offset mappings
- **Status in individual files**: NOT PRESENT
- **Extract**: YES - Required for complete encounter documentation

### Addition 3: File Location Context (7 lines)
- **Location**: Lines 7-13 in major section
- **Type**: Contextual information about related files
- **Importance**: MEDIUM - provides important context
- **Status in individual files**: NOT PRESENT
- **Extract**: YES - Helps readers understand file relationships

---

## Content for Other Files

**NOT for FF7_World_Map_Encounters.md**:
- Encounter Rate calculation formulas (none present in major section)
- Specific encounter formation data (not documented in major section)
- Script system details (documented in FF7_WorldMap_Module_Script.md)
- MAP/BOT format (documented in FF7_WorldMap_Module.md)
- BSZ format (documented in FF7_World_Map_BSZ.md)
- TXZ format (documented in FF7_World_Map_TXZ.md)

---

## Gaps and Discrepancies

### Gap 1: Uncertainty About File Formats
The major section contains explicit uncertainty markers:
- "unsure yet" regarding encounter chance rules
- "I assume... though I've not gotten any conclusive proof" about .ev files
- "(?) " marks on uncertain byte interpretations

**Impact**: These should be preserved as-is, documenting the research status
**Recommendation**: Keep uncertainty language, add [UNVERIFIED] tags where appropriate

### Gap 2: Incomplete Data Structure
Lines 15-28 define only the byte layout but not:
- Encounter formation ID ranges
- Encounter frequency/difficulty
- Special formation vs. normal battle mechanics
- Chocobo battle specifics

**Impact**: Encounter system documentation would be incomplete without this research
**Recommendation**: Document what IS known, mark what remains unclear

### Gap 3: No Actual Encounter Data
The major section documents FILE FORMAT but not:
- Actual encounter lists by area
- Formation IDs and associated monsters
- Encounter rates per area
- Chocobo battle mechanics

**Impact**: Readers can parse enc_w.bin but can't interpret its contents
**Recommendation**: Note that actual encounter data would require separate reference (e.g., modding community databases)

### Gap 4: Area Enumeration Lacks Details
Lines 29-72 list 14 areas but don't document:
- Specific offset calculations for each area
- Terrain variant ordering rules
- Why certain areas have fewer variants (e.g., "Icicle Area (Not sure what Forest is for this...)")

**Impact**: Could confuse readers about offset calculations
**Recommendation**: Document offset formulas based on area enumeration

---

## Merge Plan Summary

### File to Create
**Path**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/FF7_World_Map_Encounters.md`

**Content Strategy**:
1. Create new file with encounter-specific documentation (none previously existed)
2. Extract real content from major section (lines 7-28, 29-72)
3. Add clear section headers for organization
4. Include [UNVERIFIED] tags for uncertain information
5. Add references to related files (WorldMap, BSZ, TXZ, Script)
6. Document what's known vs. what remains unclear

### Related Merged Files
**Path**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_World_Map_Encounters.md`

**Content Strategy**:
1. Copy original file (nothing to copy - file doesn't exist yet)
2. Create from scratch with encounter-specific documentation
3. Add extraction metadata noting source

### Expected Output Size
- **New individual file**: ~80-100 lines (consolidated encounter documentation)
- **Format**: Markdown with code blocks and tables
- **Sections**:
  - Introduction/file locations
  - Encounter data format (byte structure)
  - Area organization and enumeration
  - References to related documentation

---

## Recommendations for Implementation

### Step 1: Create Individual File
Create `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/FF7_World_Map_Encounters.md` with:
- Encounter system overview
- enc_w.bin format specification (from lines 15-28)
- Area enumeration (from lines 29-72)
- Cross-references to other world map files

### Step 2: Create Merged Version
Create `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_World_Map_Encounters.md` as identical copy with merge metadata

### Step 3: Update Combined File
Update `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/combined/WorldMapModule.md` to include encounter documentation

### Step 4: Update Navigation
Add FF7_World_Map_Encounters.md to:
- MAPPING.md reference list
- Combined WorldMapModule.md table of contents
- Project documentation index

---

## Summary Table

| Aspect | Finding |
|--------|---------|
| **Major Section Size** | 86 lines |
| **Placeholder Content** | ~40 lines (Lorem Ipsum) |
| **Real Content** | ~46 lines |
| **Encounter System Content** | ~65 lines (core extraction) |
| **Images Found** | 0 |
| **Missing Individual File** | FF7_World_Map_Encounters.md |
| **Content to Extract** | Lines 7-28 (format), lines 29-72 (area enumeration) |
| **Extraction Quality** | HIGH - substantive technical documentation |
| **Overlap with Existing Files** | NONE - encounters not documented elsewhere |
| **Recommended Action** | CREATE new individual file + merged version |

---

**Analysis Complete**: 2025-11-28 22:15 JST

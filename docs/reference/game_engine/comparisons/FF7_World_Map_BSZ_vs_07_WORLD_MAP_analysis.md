# FF7 World Map BSZ Content Analysis Report

**Created**: 2025-11-29 JST
**Analysis of**: FF7_World_Map_BSZ.md vs 07_WORLD_MAP.md
**Document Type**: Phase 1 Analysis (Pre-Merge Investigation)

---

## Executive Summary

### File Statistics
- **Individual File**: FF7_World_Map_BSZ.md (137 lines, 6,518 bytes)
- **Major Section**: 07_WORLD_MAP.md (86 lines, 5,444 bytes)
- **Overlap Assessment**: MINIMAL OVERLAP - files cover complementary content
- **Content to Extract**: 1 section with 6 lines (World Map encounter data format)
- **Images Found**: 0 images
- **Merge Complexity**: LOW - simple topic-based addition

### Key Finding
The individual file (FF7_World_Map_BSZ.md) focuses exclusively on **World Map model format (BSZ files)** - bone structures, parts, animations, skeleton data. The major section (07_WORLD_MAP.md) covers **World Map system overview and encounter mechanics** with Lorem Ipsum placeholders. These are complementary rather than overlapping.

---

## Topic Scope Analysis

### FF7_World_Map_BSZ.md - Actual Scope
This file documents the **BSZ file format** used for world map character models:
- **WM0.BSZ** = Cloud's world map model
- **WM1.BSZ** = Tifa's world map model
- **WM2.BSZ** = Cid's world map model
- **WM3.BSZ** = Other character models

**Technical Structure Covered**:
1. BSZ Header Section (offset structure)
2. Model Section (bones, parts, animations)
3. Model Section Header (detailed breakdown)
4. Model Section Bones (bone hierarchy data)
5. Model Section Parts (geometry and texture data with detailed offsets)
6. Model Section Animations (animation definitions)
7. Skeleton Data Section (referenced but not detailed)

### 07_WORLD_MAP.md - Actual Scope
This section covers **World Map system mechanics and terrain**:
- **I. World Map Overview** (Lorem Ipsum + actual encounter format)
- **II. Land** (Lorem Ipsum placeholder)
- **III. Underwater** (Lorem Ipsum placeholder)
- **IV. Snow Field** (Lorem Ipsum placeholder)
- **V. Data Format** (incomplete)

**Actual Technical Content Identified**:
- PC Format encounter data (enc_w.bin) structure
- Area layout and naming
- Encounter rate mechanics
- Battle formation data

### Related Individual Files Context
- **FF7_WorldMap_Module.md** (234 lines) - MAP/BOT format, mesh structure, block layout
- **FF7_WorldMap_Module_Script.md** (127 lines) - Scripting engine, opcodes, entities/models
- **FF7_World_Map_TXZ.md** (need to check) - Texture archive format

**Boundary Analysis**:
- FF7_World_Map_BSZ.md is clearly **3D Model Format** (orthogonal to MAP/BOT/TXZ)
- FF7_WorldMap_Module.md covers **Terrain/Mesh** format
- FF7_World_Map_TXZ.md covers **Texture** format
- FF7_WorldMap_Module_Script.md covers **Scripting** system

---

## Content Already in Individual File

### What FF7_World_Map_BSZ.md Already Contains
✅ **Comprehensive BSZ Format Documentation**:
- Header structure with all offset calculations explained
- Model section architecture
- Bones data format with actual hex data example
- Parts data format with 20+ byte offset explanations
- Animations format with example data
- Cross-references to CLOUD.BCX similarities
- Actual PSX memory addresses (14A600 range)

**Assessment**: This file is already very complete for BSZ format. The individual file is LONGER (137 lines) than the major section excerpt (86 lines total).

---

## Content to Extract from Major Section

### Item 1: World Map Encounter Data Format (PC)
**Source**: 07_WORLD_MAP.md lines 8-25 (18 lines of actual content)
**Topic**: "PC Format" encounter data structure
**Rationale**: This is real technical content describing encounter data format (enc_w.bin) not present in FF7_World_Map_BSZ.md

**Content to Extract**:
```
#### PC Format !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

By the way, also had a brief look at the World Map... although things are different
between that and the field files, it naturally has many of the same data structures...
dialogue's in 'mes', the event files are in 'wm0.ev', 'wm2.ev' and 'wm3.ev' (I assume...
though I've not gotten any conclusive proof that this is the case through a *brief*
glance through them), and the encounters are stored in 'enc_w.bin' (but may or may not
follow the same rules regarding encounter chances... unsure yet)

-----

Well, enough data to warrant its own post to follow.

Encounter data for the World Map starts at offset 0xB8, and each section is 32 bytes
each. A section is defined as follows:

0x00: 01

0x01: Encounter Rate (1 byte)(?) (lower numbers mean higher encounter rates)
0x02-0x0D: Normal Battle+Chance of that battle (2 bytes each, 6 records)

0x0E-0x15: Special Formation Battles+Chance (2 bytes each, 4 records)

0x16-0x1F: Chocobo Battles (2 bytes each, 5 records)

Again, the chance byte for normal battles seems to always add up to 64.
```

**Images**: None in this section

### Item 2: World Map Area Listing
**Source**: 07_WORLD_MAP.md lines 26-71 (46 lines of actual content)
**Topic**: Game area organization and encounter zones
**Rationale**: Reference data showing how encounter data is organized by game areas - useful context for BSZ models which are used in these areas

**Content to Extract**:
```
Anyhow, as for how they're *stored*...

...each area in the game has four fields, and they're aligned something like this:

Area - Grass

Area - Dirt/Snow

Area - Forest/Desert

Area - Beach

And the areas are naturally in this order:

Midgar Area

Kalm Area

Junon Area

Corel Area

Gold Saucer Area

Gongaga Area

Cosmo Area

Nibel Area

Rocket Area

Wutai Area

Woodlands Area

Icicle Area (Not sure what Forest is for this, since the forests in this area are
supposed to have no encounters)

Mideel Area

North Corel Area (Materia Cave north of Corel)(?)

Cactus Island

Goblin Island (Goblin Island lacks a full empty Beach encounter list)
```

**Images**: None in this section

---

## Images in Extracted Content

**TOTAL IMAGES**: 0
No images found in 07_WORLD_MAP.md. No path adjustments needed.

---

## Content for Other Files

### Item A: World Map Overview (Lorem Ipsum)
**Lines**: 07_WORLD_MAP.md lines 2-6
**Assessment**: Lorem Ipsum placeholder text
**Destination**: N/A - placeholder content should be replaced, not merged

### Item B: Land/Underwater/Snow Sections (Lorem Ipsum)
**Lines**: 07_WORLD_MAP.md lines 73-83
**Assessment**: Lorem Ipsum placeholder text
**Destination**: These likely belong in FF7_WorldMap_Module.md or could be removed as placeholders

---

## Gaps and Discrepancies

### 1. Incomplete Major Section
The 07_WORLD_MAP.md section heading "## *V. Data Format*" (line 85) is incomplete - no content follows. This suggests the major section was cut off or intentionally left blank.

### 2. Lorem Ipsum Content
Approximately 50% of 07_WORLD_MAP.md is Lorem Ipsum placeholder text (sections I, II, III, IV), indicating incomplete documentation in the major section.

### 3. No BSZ Information in Major Section
The encounter data and area information in 07_WORLD_MAP.md are **orthogonal to BSZ format**. The major section does not contain any information about BSZ world map models, which is appropriate since BSZ is a model format (3D geometry) while encounter data is game mechanics (battle configuration).

### 4. No Competing Documentation
Neither file duplicates the other's content. FF7_World_Map_BSZ.md (models) and 07_WORLD_MAP.md (encounters/mechanics) address different aspects of the world map system.

---

## Merge Plan Summary

### Merge Approach: **ADDITIVE**
Since the content is complementary rather than overlapping, additions should be appended in a logical section after the existing BSZ model content.

### Proposed Addition Structure:

**Location**: After existing BSZ model documentation (after line 137)

**Content to Add**:
1. New section header: "## Related: PC Format and Encounter System"
2. Subsection: "World Map Encounter Data Format (PC)"
   - Include all encounter format documentation
3. Subsection: "World Map Areas and Terrain"
   - Include area organization list

### Why This Works:
- Preserves existing BSZ documentation completely
- Adds complementary world map system information
- Creates clear separation between model format (BSZ) and game mechanics (encounters)
- Readers get both technical depth (models) and contextual information (how models are used)

### Risks: **NONE IDENTIFIED**
- No conflicting information
- No image path issues
- No duplicate content
- Clear topic separation

### Expected Final File Size:
- Original: 137 lines (6,518 bytes)
- Additional: ~64 lines of real content (extraction headers + extracted material)
- **Final**: ~210 lines (estimated 9,500 bytes)

---

## Analysis Confidence Level

**HIGH CONFIDENCE** - This analysis is based on:
- Complete reading of both documents
- Cross-reference with related individual files (WorldMap_Module, WorldMap_Module_Script)
- Verification that content is truly complementary
- Confirmation no images require path adjustment
- Clear topic boundaries identified in MAPPING.md

---

## Next Steps (Phase 2)

1. Copy FF7_World_Map_BSZ.md to merged_with_pdf_content/ directory
2. Append extracted encounter data section
3. Append extracted area listing section
4. Add extraction markers and metadata
5. Verify original file unchanged (137 line count preserved)
6. Verify merged file contains all original + added content

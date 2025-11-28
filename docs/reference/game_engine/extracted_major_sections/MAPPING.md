# Major Sections to Individual Markdown Files Mapping

**Created**: 2025-11-28 15:11 JST
**Purpose**: Map the extracted major sections from the massive `ff7 game engine.md` file to the individual granular markdown files for future comparison work.

---

## Overview

The massive file has been broken down into **12 major sections** (see `extracted_major_sections/` directory).

The `markdown/` directory contains **32 individual files** with much finer granularity.

This document maps which individual files likely correspond to which major sections to guide future agents in:
1. Comparing content between major sections and individual files
2. Identifying unique content in the massive file to merge into individual files
3. Understanding the overall documentation structure

---

## Section Breakdown

### 00_HEADER_TOC.md (Lines 1-137, 2.4KB)
**Content**: Title, overall table of contents, introduction

**Mapped Individual Files**:
- `FF7.md` - Likely contains similar overview/TOC content

**Notes**: Header material, no substantive technical content

---

### 01_HISTORY.md (Lines 138-199, 10KB)
**Content**: FF7 development history, timeline, versions

**Mapped Individual Files**:
- `FF7_History.md` - Direct match for historical content

**Notes**: Should be nearly identical content

---

### 02_ENGINE_BASICS.md (Lines 200-215, 1.3KB)
**Content**: Basic introduction to FF7 engine structure

**Mapped Individual Files**:
- `FF7_Engine_basics.md` - Direct match for engine overview

**Notes**: Very brief section, likely overview material

---

### 03_KERNEL.md (Lines 216-1856, 106KB)
**Content**:
- Save map structures
- Kernel.bin format
- Game data organization
- Memory management
- Low-level libraries

**Mapped Individual Files**:
- `FF7_Kernel.md` - General kernel documentation
- `FF7_Kernel_Overview.md` - Kernel overview
- `FF7_Kernel_Kernelbin.md` - Kernel.bin specific
- `FF7_Kernel_Memory_management.md` - Memory structures
- `FF7_Kernel_Low_level_libraries.md` - Library documentation
- `FF7_Savemap.md` - Save map data (3,861 lines - very detailed!)

**Notes**: This major section aggregates content from 6 individual files. The individual files are MUCH more detailed, especially Savemap.md (3,861 lines vs ~1,600 lines in this section).

---

### 04_MENU_MODULE.md (Lines 1857-2358, 45KB)
**Content**: Menu system structures and behavior

**Mapped Individual Files**:
- `FF7_Menu_Module.md` (715 lines) - Direct match

**Notes**: Individual file is more detailed (715 lines vs ~500 lines in major section)

---

### 05_FIELD_MODULE.md (Lines 2359-5003, 90KB)
**Content**:
- Field scripts and opcodes
- 3D models and animations
- Walkmesh system
- Triggers and gateways
- Background layers
- Field file format

**Mapped Individual Files**:
- `FF7_Field_Module.md` (293 lines) - General field documentation

**Potential Related Files** (need sampling to confirm):
- `FF7_LGP_format.md` (102 lines) - Archive format (fields stored in LGP)
- `FF7_LZSS_format.md` (88 lines) - Compression (used by field files)
- `FF7_TEX_format.md` (364 lines) - Texture format (field textures)

**Notes**: Major section is MUCH larger (2,644 lines) than the single individual file (293 lines). Need to investigate if individual file is incomplete or if content is distributed elsewhere.

---

### 06_BATTLE_MODULE.md (Lines 5004-6767, 139KB)
**Content**:
- **Terence Fergusson's Battle Mechanics Guide** (extensive damage formulas, stats, statuses)
- Enemy data structures (scene.bin)
- Battle scenes format
- PSX 3D battle models
- PC battle models
- Magic scripting

**Mapped Individual Files**:
- `FF7_Battle_Battle_Mechanics.md` (660 lines) - Memory structures, queue system
- `FF7_Battle_Battle_Scenes.md` (728 lines) - Scene.bin format
- `FF7_Battle_Battle_Scenes_Battle_Script.md` (421 lines) - Battle AI scripting
- `FF7_Battle_Battle_Animation_PC.md` (912 lines) - PC animation format
- `FF7_Battle_Battle_Field.md` (need to sample) - Battle field data
- `FF7_Playstation_Battle_Model_Format.md` (10,833 lines!) - Extremely detailed PSX model format

**Notes**: This major section (1,763 lines) aggregates content from 6+ individual files. The Terence Fergusson battle mechanics content (damage formulas, status effects) is UNIQUE to the major section and NOT in the individual files.

---

### 07_WORLD_MAP.md (Lines 6768-6853, 5.3KB)
**Content**:
- World map overview (mostly Lorem Ipsum placeholders)
- Encounter data format (PC)
- Land/Underwater/Snow sections (mostly placeholders)

**Mapped Individual Files**:
- `FF7_WorldMap_Module.md` (234 lines) - General world map
- `FF7_WorldMap_Module_Script.md` (127 lines) - World map scripting
- `FF7_World_Map_BSZ.md` (137 lines) - BSZ format
- `FF7_World_Map_TXZ.md` (need to sample) - TXZ format

**Notes**: Major section has lots of Lorem Ipsum placeholders. Individual files likely have more real content.

---

### 08_MINI_GAMES.md (Lines 6854-7405, 41KB)
**Content**:
- Mini game overviews (mostly Lorem Ipsum)
- **Chocobo Breeding** (extensive mechanics by Terence Fergusson - HIGHLY DETAILED)
  - Stat calculations
  - Feeding greens formulas
  - Breeding nuts mechanics
  - Performance variables

**Mapped Individual Files**:
- ??? (Need to check if any individual files cover mini-games)

**Notes**: The Chocobo Breeding section is extremely detailed and appears UNIQUE to this major section. This is valuable content that may not exist in individual files.

---

### 09_APPENDIX.md (Lines 7406-8015, 11KB)
**Content**:
- Item listings (ID mappings)
- Materia listings (ID mappings)
- Resource lookup tables
- FF7 letter map (character encoding)

**Mapped Individual Files**:
- ??? (Likely no dedicated individual files - appendix material)

**Notes**: Reference material, probably unique to major section

---

### 10_SOURCE_CODE_FORENSICS.md (Lines 8016-8130, 6.2KB)
**Content**:
- Source file paths extracted from PC executable
- Development environment artifacts

**Mapped Individual Files**:
- `FF7_Technical_Source.md` (126 lines) - Possible match

**Notes**: Forensic/technical material

---

### 11_BUGS_AND_CREDITS.md (Lines 8131-8167, 2.2KB)
**Content**:
- Cross-platform bugs
- PSX-specific bugs (Lorem Ipsum)
- PC-specific bugs (Lorem Ipsum)
- Credits (Qhimm team)

**Mapped Individual Files**:
- ??? (Likely distributed across technical docs or standalone)

**Notes**: End matter, credits

---

## Files in markdown/ NOT Mapped to Major Sections

These individual files don't have obvious matches in the major sections:

### Sound-Related (NOT in major sections)
- `FF7_PSX_Sound_Overview.md`
- `FF7_PSX_Sound_AKAO_frames.md` (153 lines)
- `FF7_PSX_Sound_INSTRxALL.md`
- `FF7_PSX_Sound_INSTRxDAT.md`

### Format/Technical (NOT in major sections)
- `FF7_TEX_format.md` (364 lines) - Texture format
- `PSX_TIM_format.md` (129 lines) - TIM image format
- `FF7_LGP_format.md` (102 lines) - Archive format
- `FF7_LZSS_format.md` (88 lines) - Compression format

### Technical Documentation
- `FF7_Technical.md`
- `FF7_Technical_Customising.md` (117 lines)

---

## Key Findings for Future Agents

### 1. Content Unique to Major Sections (Needs Extraction)
- **Terence Fergusson's Battle Mechanics** (damage formulas, stats) - 06_BATTLE_MODULE.md
- **Chocobo Breeding Mechanics** (extensive formulas) - 08_MINI_GAMES.md
- **Item/Materia ID Listings** - 09_APPENDIX.md
- **Character Encoding Table** - 09_APPENDIX.md

### 2. Individual Files More Detailed Than Major Sections
- `FF7_Savemap.md` (3,861 lines) - Much more detailed than Kernel section
- `FF7_Playstation_Battle_Model_Format.md` (10,833 lines) - Extremely detailed
- Battle-related files collectively more detailed than major section

### 3. Content Unique to Individual Files (NOT in major sections)
- **All Sound documentation** (AKAO, INSTR formats)
- **Texture/Image formats** (TEX, TIM)
- **Archive/Compression formats** (LGP, LZSS)
- **Technical customization guides**

### 4. Overlap Areas (Need Comparison)
- Field Module (major section 2,644 lines vs individual file 293 lines)
- Menu Module (appears similar size)
- World Map (major section has placeholders, individual files may have real content)

---

## Recommended Next Steps for Follow-up Agents

1. **Extract unique content from major sections into individual files**:
   - Create `FF7_Battle_Damage_Formulas.md` from Terence Fergusson's content
   - Create `FF7_Chocobo_Breeding.md` from mini-games section
   - Create `FF7_Item_Materia_Reference.md` from appendix

2. **Compare overlapping content**:
   - Field Module: Why is major section so much larger?
   - Battle files: Merge Terence Fergusson formulas into appropriate files
   - Savemap: Individual file is larger - major section may be outdated

3. **Verify placeholder sections**:
   - World Map has Lorem Ipsum - check if individual files have real content
   - PSX/PC Bugs sections are placeholders - check if documented elsewhere

4. **Cross-reference formats**:
   - Ensure LGP/LZSS/TEX formats are referenced from relevant module docs
   - Link sound formats to any audio-related module documentation

---

## Line Number Reference for Major Sections

For precise extraction from original file:

| Section | Start Line | End Line | Line Count | Size |
|---------|-----------|----------|------------|------|
| 00_HEADER_TOC | 1 | 137 | 137 | 2.4KB |
| 01_HISTORY | 138 | 199 | 62 | 10KB |
| 02_ENGINE_BASICS | 200 | 215 | 16 | 1.3KB |
| 03_KERNEL | 216 | 1856 | 1641 | 106KB |
| 04_MENU_MODULE | 1857 | 2358 | 502 | 45KB |
| 05_FIELD_MODULE | 2359 | 5003 | 2645 | 90KB |
| 06_BATTLE_MODULE | 5004 | 6767 | 1764 | 139KB |
| 07_WORLD_MAP | 6768 | 6853 | 86 | 5.3KB |
| 08_MINI_GAMES | 6854 | 7405 | 552 | 41KB |
| 09_APPENDIX | 7406 | 8015 | 610 | 11KB |
| 10_SOURCE_CODE_FORENSICS | 8016 | 8130 | 115 | 6.2KB |
| 11_BUGS_AND_CREDITS | 8131 | 8167 | 37 | 2.2KB |

**Total**: 8,167 lines, ~460KB

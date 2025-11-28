# Extracted Major Sections from FF7 Game Engine Documentation

**Extracted**: 2025-11-28 15:11 JST
**Source File**: `ff7 game engine.md` (8,167 lines, ~460KB)
**Purpose**: Break down the massive consolidated file into manageable major sections for comparison against individual markdown files

---

## What's Here

This directory contains **12 major sections** extracted from the massive `ff7 game engine.md` file:

| File | Lines | Size | Content |
|------|-------|------|---------|
| `00_HEADER_TOC.md` | 137 | 2.4KB | Title, table of contents |
| `01_HISTORY.md` | 62 | 10KB | FF7 development history |
| `02_ENGINE_BASICS.md` | 16 | 1.3KB | Engine structure overview |
| `03_KERNEL.md` | 1,641 | 106KB | Save map, kernel.bin, memory management |
| `04_MENU_MODULE.md` | 502 | 45KB | Menu system |
| `05_FIELD_MODULE.md` | 2,645 | 90KB | Field scripts, models, walkmesh, backgrounds |
| `06_BATTLE_MODULE.md` | 1,764 | 139KB | Battle mechanics, formulas, enemy data, models |
| `07_WORLD_MAP.md` | 86 | 5.3KB | World map encounters, format |
| `08_MINI_GAMES.md` | 552 | 41KB | Mini-games (extensive chocobo breeding!) |
| `09_APPENDIX.md` | 610 | 11KB | Item/materia listings, character encoding |
| `10_SOURCE_CODE_FORENSICS.md` | 115 | 6.2KB | Source file paths from executable |
| `11_BUGS_AND_CREDITS.md` | 37 | 2.2KB | Known bugs, credits |

---

## Key Documentation

**See `MAPPING.md`** for:
- Detailed content breakdown of each section
- Mapping to individual markdown files in `../markdown/`
- Identification of unique content in major sections vs individual files
- Recommended next steps for follow-up agents

---

## Purpose

This extraction serves as an intermediate step for:

1. **Comparison Work**: Compare major sections against granular individual files
2. **Content Identification**: Find unique content in major sections not present in individual files
3. **Merge Planning**: Identify what needs to be extracted and merged into individual files
4. **Documentation Cleanup**: Understand overall structure and eliminate duplication

---

## Important Notes

### Content Unique to Major Sections

The following valuable content exists ONLY in these major sections and should be extracted:

- **Terence Fergusson's Battle Mechanics** (`06_BATTLE_MODULE.md`)
  - Detailed damage formulas
  - Status effect mechanics
  - Character stat calculations

- **Chocobo Breeding Mechanics** (`08_MINI_GAMES.md`)
  - Stat inheritance formulas
  - Greens feeding effects
  - Breeding nut mechanics
  - Performance calculations

- **Item/Materia ID Listings** (`09_APPENDIX.md`)
  - Complete hex ID mappings
  - Inventory data structures

- **FF7 Character Encoding Table** (`09_APPENDIX.md`)
  - Complete letter map for text encoding

### Content More Detailed in Individual Files

Some individual markdown files are MORE detailed than these major sections:

- `FF7_Savemap.md` (3,861 lines) vs `03_KERNEL.md` kernel section (~1,600 lines)
- `FF7_Playstation_Battle_Model_Format.md` (10,833 lines) - extremely detailed
- Battle-related files collectively more comprehensive

### Content NOT in Major Sections

The following topics exist ONLY in individual markdown files:

- **Sound System**: AKAO frames, INSTR formats
- **File Formats**: TEX, TIM, LGP, LZSS
- **Technical Guides**: Customization, source analysis

---

## For Future Agents

When working with this documentation:

1. **Start with MAPPING.md** to understand the relationships
2. **Identify your target section** and corresponding individual files
3. **Compare content** between major section and individual files
4. **Extract unique content** from major sections as needed
5. **Update individual files** rather than working with major sections directly

The individual markdown files in `../markdown/` are the **source of truth** for regenerating combined documentation. These major sections are for comparison and content extraction only.

---

## Original File Location

**Source**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/ff7 game engine.md`

**Individual Files**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/`

**Combined Files** (generated from individual files): `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/combined/`

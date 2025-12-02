# FF7 Game Engine Documentation - Processing Workflow

**Created:** 2025-11-28 12:44:49 JST (Friday)
**Last Modified:** 2025-12-02 14:38:22 JST (Tuesday)
**Version:** 2.0.0
**Author:** John Zealand-Doyle
**Session-ID:** b1483492-7356-4e03-95e9-710911d2ed6c

**A comprehensive collection of documentation for Final Fantasy VII's game engine, compiled from the qhimm-modding Fandom wiki and processed through an 8-stage transformation pipeline.**

---

## Table of Contents

- [Overview](#overview)
- [Workflow Diagram](#workflow-diagram)
- [Directory Structure](#directory-structure)
- [Processing Pipeline](#processing-pipeline)
- [Scripts](#scripts)
- [Quality Improvements](#quality-improvements)
- [Major Categories](#major-categories)
- [Final Output](#final-output)
- [Usage](#usage)

---

## Overview

This directory contains the complete FF7 game engine documentation processing pipeline. The workflow transforms raw MediaWiki content from the qhimm-modding Fandom wiki into high-quality, organized Markdown documentation with proper formatting, images, and navigation.

**Source:** 32 pages from https://qhimm-modding.fandom.com/wiki/
**Output:** Clean, organized Markdown files with tables, code blocks, images, and cross-references
**Processing Stages:** 8 distinct transformation stages

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: Source Collection                                     │
│  ┌──────────────┐                                               │
│  │ Fandom Wiki  │  → scraper.py → raw/*.mediawiki               │
│  └──────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: Initial Conversion                                    │
│  raw/*.mediawiki → convert_to_markdown_improved.sh →            │
│                    markdown/*.md                                │
│  (Pandoc: MediaWiki → Markdown with pipe tables + TOCs)         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: Formatting Fixes                                      │
│  • fix_table_captions.py (move captions above tables)           │
│  • convert_inline_code_blocks.py (backticks → fenced blocks)    │
│  • move_toc_below_heading.py (reposition TOCs)                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: Asset Integration                                     │
│  • extract_and_download_images.py → images/*.png                │
│  • Embed local image references in markdown files               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 5: Combination & Merging                                 │
│  • combine_files.sh → markdown/combined/*.md                    │
│  • Merge with PDF developer guide → merged_with_pdf_content/    │
│  • comparisons/*.md (validation & diff analysis)                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 6: Structure Refinement (final/)                         │
│  • Fixed front matter (YAML headers)                            │
│  • Created backlinks between related pages                      │
│  • Tidied headings hierarchy                                    │
│  • Improved Markdown structure                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 7: Error Correction (final v2/)                          │
│  • Fixed typos and OCR artifacts                                │
│  • Corrected data corruption from conversion                    │
│  • Validated technical accuracy                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 8: Section Extraction                                    │
│  extracted_major_sections/*.md (clean module references)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
game_engine/
├── raw/                              # STAGE 1: Raw MediaWiki source files
│   └── FF7_*.mediawiki              # 32 pages with prepended H1 headings
│
├── markdown/                         # STAGE 2: Initial Markdown conversion
│   ├── FF7_*.md                     # 32 individual files with tables + TOCs
│   ├── combined/                     # STAGE 5A: Intermediary combinations
│   │   ├── History.md               # Combined history sections
│   │   ├── Kernel.md                # Combined kernel sections
│   │   ├── MenuModule.md            # Combined menu sections
│   │   └── ...                      # 9 category combinations
│   └── merged_with_pdf_content/     # STAGE 5B: Merged with developer guide
│       └── FF7_GameEngine_MERGED.md # Wiki + PDF combined reference
│
├── images/                           # STAGE 4: Downloaded assets
│   └── *.png, *.jpg                 # 29 images with underscored filenames
│
├── comparisons/                      # STAGE 5C: Validation & analysis
│   └── *_analysis.md                # Individual vs combined comparisons
│
├── final/                            # STAGE 6: Structural improvements
│   └── FF7_*.md                     # Front matter, backlinks, hierarchy fixes
│
├── final v2/                         # STAGE 7: Error correction
│   └── FF7_*.md                     # Typo fixes, corruption repairs
│
├── extracted_major_sections/         # STAGE 8: Clean module references
│   ├── 00_HEADER_TOC.md             # Navigation index
│   ├── 01_HISTORY.md                # Historical context
│   ├── 03_KERNEL.md                 # Kernel module
│   ├── 04_MENU_MODULE.md            # Menu module
│   ├── 05_FIELD_MODULE.md           # Field module
│   ├── 06_BATTLE_MODULE.md          # Battle module
│   ├── 07_WORLD_MAP.md              # World map module
│   └── ...                          # Additional modules
│
├── scripts/                          # All conversion & processing tools
│   ├── README.md                    # Script documentation (see below)
│   └── *.py, *.sh                   # 18 scripts organized by purpose
│
├── logs/                             # Processing logs and debug output
│
└── README.md                         # This file
```

---

## Processing Pipeline

### Stage 1: Source Collection

**Script:** `scripts/scraper.py`

- Fetches 32 pages from qhimm-modding Fandom wiki
- Downloads raw MediaWiki content via `?action=raw` URL parameter
- Prepends level 1 headings for proper hierarchy
- Rate-limited at 1.5 seconds per request
- Outputs to `raw/*.mediawiki`

**Pages Scraped:**
- FF7 main page
- History sections
- Kernel module (memory, overview, sections)
- Menu module
- Field module (scripts, backgrounds, models)
- Battle module (scenes, animations, models)
- World map module (scripts, TXZ format)
- Mini games (Chocobo, Battle Square, G-Bike)
- Sound & music
- PSX formats (TIM, TEX)
- Technical deep-dives

### Stage 2: Initial Conversion

**Script:** `scripts/convert_to_markdown_improved.sh`

Uses Pandoc with specific options to ensure quality:

```bash
PANDOC_OPTS="-f mediawiki \
  -t markdown-simple_tables-multiline_tables-grid_tables+pipe_tables \
  --standalone --toc --toc-depth=4 --wrap=preserve"
```

**Key Features:**
- Forces Markdown pipe tables (not plain text)
- Generates table of contents (TOC) for each file
- Includes headings up to h4 in TOC
- Preserves line wrapping from source

**Output:** 32 markdown files with proper structure

### Stage 3: Formatting Fixes

Multiple scripts fix Pandoc conversion artifacts:

#### Table Captions
**Script:** `scripts/fix_table_captions.py`

- Moves captions from below tables (Pandoc default) to above (wiki layout)
- Pattern: Detects definition list syntax (`: caption`) after tables
- Fixed 14 captions across 5 files

#### Code Blocks
**Scripts:**
- `convert_inline_code_blocks.py` (final working version)
- `fix_code_blocks*.py` (earlier iterations)

**Problem:** MediaWiki preformatted code converts to inline backticks with backslashes:
```markdown
`typedef struct`\
`{`\
` uint8 Vertex0Index;`\
```

**Solution:** Detects consecutive inline code lines, converts to fenced blocks:
```c
typedef struct
{
 uint8 Vertex0Index;
```

**Special handling:** Contributor annotations (italic text) marked with `// contributor addition` comments

#### TOC Positioning
**Script:** `scripts/move_toc_below_heading.py`

- Moves TOC from document top to below H1 heading
- Adds blank lines for readability
- Improves navigation flow

### Stage 4: Asset Integration

**Script:** `scripts/extract_and_download_images.py`

- Extracts `[[File:...]]` references from raw MediaWiki
- Downloads images from Fandom wiki (`Special:FilePath/...`)
- Saves to `images/` with sanitized filenames (spaces → underscores)
- Embeds references in markdown files
- Downloaded 29 images (580KB total)

**Image URL Pattern:**
```
https://qhimm-modding.fandom.com/wiki/Special:FilePath/{filename}
```

### Stage 5: Combination & Merging

#### Stage 5A: Category Combinations
**Script:** `scripts/combine_files.sh`

Creates 9 focused category files in `markdown/combined/`:
- History
- Engine Basics
- Kernel
- Menu Module
- Field Module
- Battle Module
- World Map Module
- Sound
- Technical

**Master file:** `GameEngine.md` (all 32 pages except Savemap & Battle Model Format due to size)

#### Stage 5B: PDF Merge
**Directory:** `markdown/merged_with_pdf_content/`

- Combines wiki documentation with PDF developer guide content
- Creates comprehensive reference: `FF7_GameEngine_MERGED.md`
- Integrates complementary information from official docs

#### Stage 5C: Comparison Analysis
**Directory:** `comparisons/`

- Validates individual files against combined versions
- Identifies discrepancies and data loss
- Documents transformation accuracy
- Ensures no information lost during merging

**Example:** `FF7_Battle_Battle_Field_vs_06_BATTLE_MODULE_analysis.md`

### Stage 6: Structure Refinement (final/)

**Manual improvements:**

1. **Front Matter** - Added YAML headers with metadata:
   ```yaml
   ---
   title: FF7 Kernel Module
   category: Game Engine
   tags: [kernel, memory, initialization]
   last_updated: 2025-11-28
   ---
   ```

2. **Backlinks** - Created bidirectional references between related pages:
   ```markdown
   See also: [Field Module](FF7_Field_Module.md), [Battle Module](FF7_Battle_Module.md)
   ```

3. **Heading Hierarchy** - Fixed inconsistent heading levels
4. **Markdown Structure** - Improved lists, emphasis, code formatting

### Stage 7: Error Correction (final v2/)

**Manual fixes:**

- **Typos** - Corrected OCR artifacts and spelling errors
- **Data Corruption** - Fixed garbled text from conversion
- **Technical Accuracy** - Validated against source material
- **Formatting Bugs** - Resolved edge cases not caught by scripts

### Stage 8: Section Extraction (extracted_major_sections/)

**Clean module references:**

- Extracted 11 major sections as standalone files
- Removed wiki markup artifacts
- Consistent heading hierarchy (00-11 numbering)
- Suitable for direct inclusion in other documentation

---

## Scripts

All conversion and processing tools are in `scripts/`. See **[scripts/README.md](scripts/README.md)** for detailed documentation of each script.

**Categories:**
1. **Source Collection** - scraper.py
2. **Format Conversion** - convert_to_markdown*.sh
3. **Content Fixes** - fix_*.py, convert_*.py
4. **Asset Management** - extract_*.py, download_*.py
5. **Combination** - combine_files.sh
6. **Utilities** - move_toc_below_heading.py, transform_savemap.py

---

## Quality Improvements

### From Wiki to Markdown

| Issue | Solution | Script |
|-------|----------|--------|
| Tables as plain text | Force Markdown pipe tables | `convert_to_markdown_improved.sh` |
| Captions below tables | Move captions above | `fix_table_captions.py` |
| Code as inline backticks | Convert to fenced blocks | `convert_inline_code_blocks.py` |
| TOC at document top | Reposition below H1 | `move_toc_below_heading.py` |
| Missing images | Download and embed | `extract_and_download_images.py` |
| Broken wiki links | Convert to relative paths | Manual editing |
| Inconsistent structure | Add front matter + backlinks | Manual editing (final/) |
| Typos and corruption | Proofread and correct | Manual editing (final v2/) |

### Validation

**Comparisons directory** contains diff analysis ensuring:
- No information lost during combination
- Structural changes preserve content
- Technical accuracy maintained
- Edge cases documented

---

## Major Categories

### History
Chronicles FF7's development history, technical evolution, and the modding community's discoveries. Provides context for understanding the engine's architecture and design decisions made during the original PlayStation era.

📄 [Read History Documentation](markdown/combined/History.md)

### Engine Basics
Foundational overview of FF7's game engine structure, module system, and core architecture. Essential reading for understanding how the different game systems (Field, Battle, WorldMap, Menu) interconnect and function as a cohesive whole.

📄 [Read Engine Basics Documentation](markdown/combined/EngineBasics.md)

### Kernel
Deep dive into FF7's kernel system including memory management strategies, kernel.bin structure, low-level library implementations, and critical file formats (LZSS compression, LGP archives, TIM/TEX textures). This is the foundation that all other modules build upon.

📄 [Read Kernel Documentation](markdown/combined/Kernel.md)

### Menu Module
Documentation of FF7's menu system including the main menu, item management, equipment screens, materia organization, and status displays. Covers both the technical implementation and data structures used for menu navigation and rendering.

📄 [Read Menu Module Documentation](markdown/combined/MenuModule.md)

### Field Module
Complete reference for FF7's field module which handles exploration areas, NPC interactions, field scripts, triggers, and 3D environments outside of battle. Includes PSX DAT format specifications and scripting system details.

📄 [Read Field Module Documentation](markdown/combined/FieldModule.md)

### Battle Module
Comprehensive battle system documentation covering battle mechanics (ATB, damage calculations, status effects), battle field environments, battle scenes structure, battle scripting language (AI opcodes), and animation systems for both enemies and party members.

📄 [Read Battle Module Documentation](markdown/combined/BattleModule.md)

### WorldMap Module
Detailed specifications for FF7's world map system including map structure, BSZ (compressed map data) format, TXZ (texture archive) format, and world map scripting for events, encounters, and location triggers.

📄 [Read WorldMap Module Documentation](markdown/combined/WorldMapModule.md)

### Sound
PSX sound system documentation covering the audio architecture, INSTRx.DAT (instrument sample data), INSTRx.ALL (instrument metadata), and AKAO audio frames (Sony's proprietary audio sequence format used in FF7).

📄 [Read Sound Documentation](markdown/combined/Sound.md)

### Technical
Technical reference materials including customization guides for modding FF7, source code analysis, implementation notes, and advanced technical details for developers working on engine modifications or reverse engineering.

📄 [Read Technical Documentation](markdown/combined/Technical.md)

---

## Large Reference Documents

These documents are maintained separately due to their comprehensive size and are excluded from combined files:

### Savemap
Complete save file format documentation detailing every byte of FF7's save game structure. Includes character data, inventory, materia, story flags, game progress, and all persistent state information. Essential reference for save editors and tools.

📄 [Read Savemap Documentation](markdown/FF7_Savemap.md)

### Playstation Battle Model Format
Detailed PSX battle model format specifications covering 3D model structure, animation data, texture mapping, and rendering information for all battle characters, enemies, and summons on the PlayStation version.

📄 [Read Battle Model Format Documentation](markdown/FF7_Playstation_Battle_Model_Format.md)

---

## Complete Documentation

📄 [GameEngine.md](GameEngine.md) - All categories combined into a single master file (excludes Savemap and Battle Model Format for size management)

📂 [Individual Pages](markdown/readme.md) - Browse all 32 documentation pages separately for focused reference

---

## Navigation Guide

**For LLM/AI Context:**
- Use category files for focused domain queries (e.g., battle system questions → BattleModule.md)
- Use GameEngine.md for cross-cutting questions requiring multiple domains
- Reference individual pages for specific technical details

**For Human Readers:**
- Start with Engine Basics to understand the overall architecture
- Dive into specific categories as needed for your modding or research project
- Keep Savemap and Battle Model Format bookmarked for frequent reference

---

## Final Output

### Recommended Usage

**For general reference:** Use `final v2/FF7_*.md` (highest quality, all fixes applied)

**For specific modules:** Use `extracted_major_sections/*.md` (clean, standalone references)

**For comprehensive view:** Use `markdown/merged_with_pdf_content/FF7_GameEngine_MERGED.md` (wiki + official docs)

### Output Statistics

- **Source pages:** 32
- **Individual markdown files:** 32
- **Combined category files:** 9
- **Merged comprehensive file:** 1
- **Extracted sections:** 11
- **Images:** 29 (580KB)
- **Total processing scripts:** 18

---

## Usage

### Running the Pipeline

**Full pipeline (from scratch):**

```bash
cd /path/to/game_engine

# 1. Scrape wiki pages
python3 scripts/scraper.py

# 2. Convert to Markdown
bash scripts/convert_to_markdown_improved.sh

# 3. Fix table captions
python3 scripts/fix_table_captions.py

# 4. Convert code blocks
python3 scripts/convert_inline_code_blocks.py

# 5. Reposition TOCs
python3 scripts/move_toc_below_heading.py

# 6. Download and embed images
python3 scripts/extract_and_download_images.py

# 7. Create combined files
bash scripts/combine_files.sh
```

**Note:** Stages 5B-8 (merging, final edits, extractions) were manual processes requiring human review and editing.

### Requirements

- **Python 3.7+** - For scraping and processing scripts
- **Pandoc 2.0+** - For MediaWiki to Markdown conversion
- **Bash** - For shell scripts
- **Internet connection** - For downloading wiki content and images

### Troubleshooting

**Pandoc not found:**
```bash
brew install pandoc  # macOS
apt install pandoc   # Linux
```

**Python dependencies:**
All scripts use standard library only (no pip installs required)

**Rate limiting:**
Scraper includes 1.5s delays to respect Fandom's servers. Do not reduce this value.

---

## Related Documentation

- **Scripts Reference:** [scripts/README.md](scripts/README.md)
- **Comparison Analysis:** [comparisons/](comparisons/)
- **Original Wiki:** https://qhimm-modding.fandom.com/wiki/FF7
- **Project Overview:** [../../PROJECT_OVERVIEW.md](../../PROJECT_OVERVIEW.md)

---

## Source & Attribution

All content scraped from the [qhimm-modding Fandom wiki](https://qhimm-modding.fandom.com/wiki/FF7) on 2025-11-28.

This documentation is the result of years of reverse engineering work by the FF7 modding community. Thanks to all contributors who documented these technical specifications.

---

**Last Updated:** 2025-12-02 14:38:22 JST (Tuesday)
**Maintained By:** John Zealand-Doyle

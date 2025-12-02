# FF7 Game Engine Documentation - Processing Scripts

**Created:** 2025-12-02 14:38:22 JST (Tuesday)
**Last Modified:** 2025-12-02 14:38:22 JST (Tuesday)
**Version:** 1.0.0
**Author:** John Zealand-Doyle
**Session-ID:** b1483492-7356-4e03-95e9-710911d2ed6c

---

## Overview

This directory contains all scripts used to transform raw MediaWiki content from the qhimm-modding Fandom wiki into high-quality Markdown documentation. Scripts are organized by function and processing stage.

**Total Scripts:** 18
**Languages:** Python 3, Bash
**Dependencies:** Standard library only (Python), Pandoc (system)

---

## Table of Contents

- [Source Collection](#source-collection)
- [Format Conversion](#format-conversion)
- [Content Fixes](#content-fixes)
  - [Table Formatting](#table-formatting)
  - [Code Block Conversion](#code-block-conversion)
  - [TOC Positioning](#toc-positioning)
- [Asset Management](#asset-management)
- [Combination & Organization](#combination--organization)
- [Utilities](#utilities)
- [Script Naming Convention](#script-naming-convention)
- [Execution Order](#execution-order)

---

## Source Collection

### scraper.py

**Purpose:** Downloads raw MediaWiki content from Fandom wiki

**Created:** 2025-11-28 12:44:49 JST (Friday)
**Language:** Python 3
**Input:** URL list (hardcoded in script)
**Output:** `raw/*.mediawiki`

**Features:**
- Fetches 32 pages from qhimm-modding Fandom wiki
- Uses `?action=raw` parameter to get MediaWiki source
- Prepends level 1 heading to each file for proper hierarchy
- Rate-limited at 1.5 seconds per request (respects Fandom's servers)
- Sanitizes filenames (replaces `/` with `_`, removes special chars)

**Key Functions:**
- `sanitize_filename(title)` - Converts page title to valid filename
- `fetch_mediawiki_raw(url)` - Downloads raw MediaWiki content
- `prepend_level_one_heading(content, title)` - Adds H1 for structure

**Usage:**
```bash
python3 scraper.py
```

**Output Example:**
```
raw/FF7_WorldMap_Module.mediawiki
raw/FF7_Kernel_Overview.mediawiki
...
```

---

## Format Conversion

### convert_to_markdown_improved.sh

**Purpose:** Converts MediaWiki to Markdown using Pandoc with optimized settings

**Created:** 2025-11-28 13:01:32 JST (Friday)
**Language:** Bash
**Input:** `raw/*.mediawiki`
**Output:** `markdown/*.md`

**Pandoc Options:**
```bash
PANDOC_OPTS="-f mediawiki \
  -t markdown-simple_tables-multiline_tables-grid_tables+pipe_tables \
  --standalone --toc --toc-depth=4 --wrap=preserve"
```

**Features:**
- **Forced pipe tables** - Disables simple/multiline/grid, forces Markdown standard
- **TOC generation** - Creates table of contents for each file
- **TOC depth** - Includes up to h4 headings in TOC
- **Preserve wrapping** - Maintains line breaks from source
- **Backup system** - Saves old files to `markdown_backup/` before conversion

**Why These Options:**
- Default Pandoc creates plain text tables (hard to read/edit)
- Pipe tables are the Markdown standard, work everywhere
- TOC improves navigation for long technical documents
- Preserving wraps maintains readability of code examples

**Usage:**
```bash
bash convert_to_markdown_improved.sh
```

**Success Indicators:**
- Tables use `| header |` format (not plain text)
- TOC appears at top of each file
- No Pandoc errors

### convert_to_markdown.sh

**Purpose:** Original conversion script (deprecated)

**Created:** 2025-11-28 (earlier version)
**Status:** **DEPRECATED** - Use `convert_to_markdown_improved.sh` instead

**Why Deprecated:**
- Used default Pandoc settings
- Created plain text tables instead of pipe tables
- Missing TOC generation
- Replaced by improved version

---

## Content Fixes

### Table Formatting

#### fix_table_captions.py

**Purpose:** Moves table captions from below to above tables

**Created:** 2025-11-28 13:12:46 JST (Friday)
**Language:** Python 3
**Input:** `markdown/*.md`
**Output:** Modified `markdown/*.md` (in-place)

**Problem Solved:**
Pandoc converts MediaWiki table captions to Markdown definition lists placed **after** the table:
```markdown
| Header | Header |
|--------|--------|
| Data   | Data   |

: Caption text here
```

**Solution:**
Moves caption **before** table to match original wiki layout:
```markdown
*Caption text here*

| Header | Header |
|--------|--------|
| Data   | Data   |
```

**Pattern Detection:**
- Finds table followed by `: Caption` definition list
- Extracts caption text
- Repositions before table
- Formats as italic for emphasis

**Statistics:**
- Fixed 14 captions across 5 files:
  - FF7_Savemap.md
  - FF7_Technical_Source.md
  - FF7_WorldMap_Module.md
  - FF7_WorldMap_Module_Script.md
  - FF7_World_Map_TXZ.md

**Usage:**
```bash
python3 fix_table_captions.py
```

#### fix_table_captions_v2.py

**Purpose:** Improved version with better pattern matching

**Created:** 2025-11-28 (later iteration)
**Status:** **WORKING VERSION** - Use this over v1

**Improvements:**
- Better regex patterns
- Handles edge cases (captions with special chars)
- More robust whitespace handling

---

### Code Block Conversion

Multiple scripts evolved to solve the code block conversion problem. The final working version is `convert_inline_code_blocks.py`.

#### convert_inline_code_blocks.py

**Purpose:** Converts inline code blocks to fenced code blocks

**Created:** 2025-11-28 (final working version)
**Language:** Python 3
**Input:** `markdown/*.md`
**Output:** Modified `markdown/*.md` (in-place)

**Problem Solved:**
MediaWiki preformatted code (indented with spaces) converts to Pandoc as inline backticks with backslashes:
```markdown
`typedef struct`\
`{`\
` uint8 Vertex0Index;`\
` uint8 Vertex1Index;`\
`}`
```

**Solution:**
Detects consecutive inline code lines, merges into fenced code block:
```c
typedef struct
{
 uint8 Vertex0Index;
 uint8 Vertex1Index;
}
```

**Special Handling:**
Contributor annotations (italic inline code) marked with comments:
```c
typedef struct
{
 uint8 WalkabilityInfo:5;  // contributor addition
 uint8 Unknown:3;           // contributor addition
}
```

**Pattern Detection:**
1. Finds consecutive lines of inline code (`` `code`\ ``)
2. Detects language hint from context (C structs, assembly, etc.)
3. Merges into single fenced block
4. Marks italic code with `// contributor addition`

**Statistics:**
- Converted 18 code blocks across 6 files
- Handled 4 contributor annotation lines

**Usage:**
```bash
python3 convert_inline_code_blocks.py
```

#### Earlier Iterations (Deprecated)

##### fix_code_blocks.py
**Status:** DEPRECATED (fragmented output)
**Issue:** Split code into multiple fragments instead of merging

##### fix_code_blocks_v2.py
**Status:** DEPRECATED (partial improvement)
**Issue:** Better than v1 but still fragmented some blocks

##### fix_code_blocks_v3.py
**Status:** DEPRECATED (experimental)
**Issue:** Over-aggressive pattern matching

##### fix_all_code_blocks.py
**Status:** DEPRECATED (comprehensive attempt)
**Issue:** Complex logic, harder to debug, replaced by simpler approach

##### fix_all_code_final.py
**Status:** DEPRECATED (final attempt before working version)
**Issue:** Close but missed edge cases

##### merge_fragmented_code_blocks.py
**Status:** DEPRECATED (tried to fix fragments after the fact)
**Issue:** Addressing symptom instead of root cause

##### fix_worldmap_code.py
**Status:** ONE-TIME MANUAL FIX
**Purpose:** Manual sed fix for WorldMap Module Triangle struct
**Issue:** Code block with inline italics that scripts couldn't handle
**Note:** Not for general use, specific to one file

**Why So Many Iterations:**
The code block problem was complex due to:
- MediaWiki allowing inline formatting (italics) inside preformatted blocks
- Markdown fenced blocks not supporting inline formatting
- Pandoc splitting formatted code into fragments
- Need to preserve contributor annotations

**Lesson:** Sometimes manual fixes (like fix_worldmap_code.py) are more practical than perfect automation.

---

### TOC Positioning

#### move_toc_below_heading.py

**Purpose:** Repositions table of contents from top to below H1 heading

**Created:** 2025-11-28 (after TOC generation)
**Language:** Python 3
**Input:** `markdown/*.md` (with TOCs at top)
**Output:** Modified `markdown/*.md` (TOC below H1)

**Problem Solved:**
Pandoc places TOC at document start. Better UX has TOC after heading:

**Before:**
```markdown
- [Section 1](#section-1)
- [Section 2](#section-2)

# FF7 Kernel Module

Content...
```

**After:**
```markdown
# FF7 Kernel Module

- [Section 1](#section-1)
- [Section 2](#section-2)

Content...
```

**Algorithm:**
1. Extract TOC lines (start with `- [`)
2. Find H1 heading
3. Reconstruct: H1, blank line, TOC, blank line, rest
4. Write back to file

**Blank Line Strategy:**
- Blank line after H1 (separates title from TOC)
- Blank line after TOC (separates TOC from content)
- Improves readability

**Usage:**
```bash
python3 move_toc_below_heading.py
```

**Statistics:**
- Fixed all 32 files

---

## Asset Management

### extract_and_download_images.py

**Purpose:** Downloads and embeds images from Fandom wiki

**Created:** 2025-11-28 (image integration stage)
**Language:** Python 3
**Input:** `raw/*.mediawiki` (for image references), `markdown/*.md` (to embed)
**Output:** `images/*.png`, `images/*.jpg`, updated `markdown/*.md`

**Process:**

1. **Extract References**
   - Scans raw MediaWiki files for `[[File:...]]` references
   - Pattern: `\[\[File:([^\]|]+?)(?:\|[^\]]+)?\]\]`
   - Extracts filename, context, position

2. **Download Images**
   - URL pattern: `https://qhimm-modding.fandom.com/wiki/Special:FilePath/{filename}`
   - Sanitizes filenames (spaces → underscores)
   - Saves to `images/` directory
   - Rate-limited at 0.5s per image

3. **Embed in Markdown**
   - Adds "Images" section at end of each file
   - Format: `![Alt Text](images/filename.png)`
   - Alt text derived from filename

**Features:**
- Handles spaces in filenames (downloads correctly, renames locally)
- Preserves image quality (no re-encoding)
- Skips already downloaded images
- Error handling for missing/broken images

**Statistics:**
- Downloaded 29 images (580KB total)
- From 6 files:
  - Engine_basics (1 image)
  - Field_Module (1 image)
  - Kernel_Memory_management (2 images)
  - Kernel_Overview (1 image)
  - Menu_Module (16 images)
  - PSX_TIM_format (8 images)

**Usage:**
```bash
python3 extract_and_download_images.py
```

**Output Example:**
```
images/Kernel_table.png
images/Engine_parts.jpg
images/VRAM_layout.png
```

### download_and_embed_images.py

**Purpose:** Alternative implementation (possibly earlier version)

**Status:** CHECK IF DUPLICATE - May be same as extract_and_download_images.py

**Note:** Review both scripts to determine if one should be removed or if they serve different purposes.

---

## Combination & Organization

### combine_files.sh

**Purpose:** Creates combined category files from individual pages

**Created:** 2025-11-28 (after formatting fixes)
**Language:** Bash
**Input:** `markdown/FF7_*.md` (individual pages)
**Output:** `markdown/combined/*.md` (9 category files), `GameEngine.md` (master file)

**Category Files Created:**

1. **History.md** - Development history, technical evolution
2. **EngineBasics.md** - Engine overview, architecture
3. **Kernel.md** - Kernel system, memory, formats
4. **MenuModule.md** - Menu system implementation
5. **FieldModule.md** - Field exploration, scripts
6. **BattleModule.md** - Battle mechanics, scenes
7. **WorldMapModule.md** - World map, BSZ, TXZ formats
8. **Sound.md** - Audio system, AKAO frames
9. **Technical.md** - Source analysis, customization

**Master File:**
- **GameEngine.md** - All 32 pages combined
- **Exclusions:** Savemap, Playstation Battle Model Format (too large)
- **Size:** ~6,000 lines

**Process:**
1. Concatenates related files with separators
2. Adds navigation headers between sections
3. Preserves all formatting, images, TOCs
4. Creates master file for comprehensive view

**Usage:**
```bash
bash combine_files.sh
```

**Output Statistics:**
- 9 category files
- 1 master file
- No data loss (verified via comparisons/)

---

## Utilities

### transform_savemap.py

**Purpose:** Special processing for Savemap documentation

**Created:** 2025-12-02 00:31 JST (earlier session)
**Language:** Python 3
**Input:** Savemap markdown
**Output:** Transformed Savemap

**Note:** This script predates the main conversion pipeline. Likely handles special formatting requirements for the large Savemap reference document.

**Status:** UTILITY SCRIPT - Not part of main pipeline

---

## Script Naming Convention

Scripts follow these naming patterns:

### By Function:
- `scraper.py` - Fetches source data
- `convert_*.py`, `convert_*.sh` - Format conversion
- `fix_*.py` - Corrects formatting issues
- `extract_*.py` - Pulls data from sources
- `download_*.py` - Fetches remote assets
- `combine_*.sh` - Merges files
- `move_*.py` - Repositions elements
- `transform_*.py` - Specialized transformations

### By Version:
- No suffix - Original version
- `_improved` - Enhanced rewrite
- `_v2`, `_v3` - Iteration numbers
- `_final` - Intended final version (may have been superseded)

### Status Indicators:
- **WORKING** - Currently used in pipeline
- **DEPRECATED** - Replaced by better version
- **UTILITY** - Standalone tool, not in main pipeline

---

## Execution Order

**Recommended pipeline execution order:**

```bash
# Stage 1: Source Collection
python3 scripts/scraper.py

# Stage 2: Initial Conversion
bash scripts/convert_to_markdown_improved.sh

# Stage 3: Formatting Fixes
python3 scripts/fix_table_captions.py         # Tables first
python3 scripts/convert_inline_code_blocks.py # Code blocks second
python3 scripts/move_toc_below_heading.py      # TOCs last

# Stage 4: Asset Integration
python3 scripts/extract_and_download_images.py

# Stage 5: Combination
bash scripts/combine_files.sh
```

**Dependencies:**
- Stage 2 requires Stage 1 output (raw files)
- Stage 3 requires Stage 2 output (markdown files)
- Stage 4 reads raw files (Stage 1) and modifies markdown files (Stage 2)
- Stage 5 requires all fixes complete (Stage 3)

**Idempotency:**
- All scripts can be run multiple times safely
- Most scripts create backups before modifying
- Re-running overwrites previous output

**Manual Stages (not scripted):**
- Stage 5B: PDF merge (requires manual editing)
- Stage 5C: Comparison analysis (manual review)
- Stage 6: Structure refinement (manual editing)
- Stage 7: Error correction (manual proofreading)
- Stage 8: Section extraction (manual curation)

---

## Maintenance Notes

**When adding new scripts:**
1. Use timestamped header comments (date, context, session-id)
2. Include docstrings for all functions
3. Add to this README in appropriate category
4. Update execution order if needed
5. Mark deprecated scripts clearly

**When deprecating scripts:**
1. Leave file in directory (don't delete - preserves history)
2. Add "DEPRECATED" to docstring
3. Update this README with deprecation note
4. Explain why deprecated and what replaced it

**Version control:**
- All scripts committed to git
- Use descriptive commit messages
- Tag major pipeline milestones

---

## Related Documentation

- **Main Workflow:** [../README.md](../README.md)
- **Comparison Analysis:** [../comparisons/](../comparisons/)
- **Original Wiki:** https://qhimm-modding.fandom.com/wiki/FF7

---

**Last Updated:** 2025-12-02 14:38:22 JST (Tuesday)
**Maintained By:** John Zealand-Doyle

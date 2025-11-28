# Analysis Report: World Map Textures vs 07_WORLD_MAP Major Section

**Created**: 2025-11-28 22:15 JST
**Report Type**: Content Analysis & Merge Planning
**Individual File**: FF7_World_Map_Textures.md (NEW FILE - does not currently exist)
**Major Section**: 07_WORLD_MAP.md (lines 6768-6853, 86 lines, 5.3KB)
**Related Files**: FF7_World_Map_TXZ.md, FF7_World_Map_BSZ.md, FF7_WorldMap_Module.md

---

## Executive Summary

**Status**: NEW FILE CREATION NEEDED

The individual file `FF7_World_Map_Textures.md` does not currently exist in the markdown/ directory. This analysis report establishes the scope, content boundaries, and provides the merge plan for creating this new specialized documentation file focused on world map texture handling.

**Key Findings**:
- **Individual File Status**: Does not exist (needs creation)
- **Content Alignment**: Texture content IS distributed across multiple existing files but lacks a dedicated textures-focused document
- **Major Section Content**: 07_WORLD_MAP.md is extremely sparse (86 lines, mostly Lorem Ipsum placeholders)
- **Texture Details**: Found in FF7_World_Map_TXZ.md (texture archive format details)
- **Images in Major Section**: 0 (no images referenced)
- **Substantive Additions**: YES - content from TXZ file that should be dedicated textures documentation

---

## Topic Scope Analysis

### FF7_World_Map_Textures.md Scope (Proposed)

A new dedicated documentation file covering:
1. **World map texture formats** (TXZ archive structure)
2. **PSX GPU texture specifications** (VRAM layout, color format)
3. **Texture coordinate mapping** (UV coordinates, offset tables)
4. **Texture data structures** (palette identifiers, VRAM blocks)
5. **Texture loading and rendering** (direct VRAM upload, section format)

### Related File Boundaries

**FF7_WorldMap_Module.md** (235 lines):
- General world map structure
- Map/BOT file formats (block structure, mesh arrangement)
- Mesh structure (triangles, vertices, normals)
- Walkmap types and definitions
- **Texture reference only**: Line 234 mentions texture numbers and UV coordinates, references texture table

**FF7_World_Map_TXZ.md** (77 lines):
- TXZ archive compression (LZS)
- TXZ archive format (header, sections)
- **Section 0-5**: Various VRAM data sections
- **Section 2**: Detailed texture data (palette/texture identifiers, VRAM blocks)
- Includes PSX GPU structure definition
- References "TextureTable" wiki link

**FF7_World_Map_BSZ.md** (138 lines):
- BSZ character model format
- Model section (bones, parts, animations)
- Skeleton data and texture references
- Not directly about map textures

**FF7_WorldMap_Module_Script.md** (128 lines):
- World map scripting engine
- No texture-related content

---

## Content in Major Section (07_WORLD_MAP.md)

### Structure Overview

| Section | Content | Status |
|---------|---------|--------|
| I. World Map Overview | Lorem Ipsum + PC Format notes + Encounter data | Mostly placeholder |
| II. Land | Lorem Ipsum | Placeholder |
| III. Underwater | Lorem Ipsum | Placeholder |
| IV. Snow Field | Lorem Ipsum | Placeholder |
| V. Data Format | (Incomplete - cuts off) | Unknown |

### Texture-Related Content

**Search Results**:
- No matches for "texture" (case-insensitive)
- No markdown images `![...](...)`
- No HTML images `<img ...>`
- No graphics or visual references

**Analysis**:
The major section 07_WORLD_MAP.md contains NO texture-specific content. It is mostly Lorem Ipsum placeholder text with only brief authentic content about:
- PC world map format overview
- Encounter data structure
- Area/section organization

### Content Organization

**Real Content Found** (lines 7-71):
- Brief PC format notes (line 7-13)
- Encounter data structure (lines 15-25)
- Area list (lines 29-71)
- **Relevance to textures**: NONE - this is encounter/gameplay content

**Placeholder Content** (lines 5, 74-83):
- Lorem Ipsum in sections I, II, III, IV
- No meaningful texture documentation

---

## Texture Content Already in Individual Files

### FF7_World_Map_TXZ.md Content (CRITICAL)

**Lines 1-77**: Complete texture archive documentation

**Key Sections**:
1. **Compression** (lines 11-14): LZS compression with size header
2. **TXZ Archive Format** (lines 15-18): Header parsing, section offsets
3. **Section 0** (lines 21-23): Unknown format, may contain textures
4. **Section 1** (lines 25-27): Single texture block for VRAM upload
5. **Section 2** (lines 29-64): **Texture data for worldmap mesh**
   - 512 palette/texture identifiers
   - PSX GPU structure definition (lines 35-46)
   - VRAM block structure (lines 50-64)
   - References TextureTable
6. **Section 3** (lines 66-68): Unknown VRAM data blocks
7. **Section 4** (lines 70-72): Script data
8. **Section 5-11** (lines 74-76): AKAO audio format

**Texture-Specific Content** (Lines 25-64):
- Palette/texture identifier format (PSX GPU compatible)
- VRAM block structure with coordinates and dimensions
- Pixel data layout
- C struct definition for wm_texture

### FF7_WorldMap_Module.md Texture Reference (Lines 231-235)

**Content**: Single paragraph referencing textures
- Mentions "texture number (0-511)"
- References UV coordinates and offset calculations
- Links to "TextureTable" (wiki reference)
- Note about texture repetition

---

## Content to Extract for New File

**VERDICT**:
The major section 07_WORLD_MAP.md contains NO NEW texture content beyond what already exists in FF7_World_Map_TXZ.md and the brief reference in FF7_WorldMap_Module.md.

**Items to Extract**: NONE from major section

**Items to Consolidate**:
- Extract FF7_World_Map_TXZ.md content as base for new FF7_World_Map_Textures.md
- Cross-reference FF7_WorldMap_Module.md texture paragraph
- Add texture table explanation

---

## Images Inventory

**Images in 07_WORLD_MAP.md**: 0

**Images Needed for FF7_World_Map_Textures.md**:
- None currently present in source material
- Could benefit from:
  - VRAM layout diagram
  - Texture coordinate visualization
  - Archive section organization diagram

**Image Path Adjustments**: N/A (no images to adjust)

---

## Content for Other Files

**NOT Assigned to FF7_World_Map_Textures.md**:

1. **Encounter Data** (07_WORLD_MAP lines 15-25):
   - Should go to: FF7_World_Map_Encounters.md or new FF7_World_Map_Encounters.md
   - Content: Encounter data structure, encounter rates, battle chances

2. **Area Organization** (07_WORLD_MAP lines 29-71):
   - Should go to: FF7_WorldMap_Module.md (general reference)
   - Content: List of 13 game areas and their encounter sections

3. **Lorem Ipsum Sections**:
   - Status: Placeholder content (ignore)
   - Land, Underwater, Snow Field sections have no real content

---

## Gaps and Discrepancies

### Gap 1: Major Section Incompleteness
- Section V "Data Format" cuts off at line 86
- Unclear if original file was truncated or if this is all content

### Gap 2: Texture Table Reference
- Both FF7_World_Map_TXZ.md (line 48) and FF7_WorldMap_Module.md (line 234) reference "TextureTable"
- No actual texture table found in provided files
- This table is critical for UV coordinate remapping

### Gap 3: PSX vs PC Texture Handling
- FF7_World_Map_TXZ.md mentions PSX GPU format and VRAM
- No explanation of how PC version differs or adapts this format

### Gap 4: Texture Coordinate Offset Calculation
- FF7_WorldMap_Module.md mentions "texture-specific offset" and "UV pairs"
- FF7_World_Map_TXZ.md doesn't explain offset calculation algorithm
- This is critical for implementing texture mapping

---

## Merge Plan Summary

### Phase 1: Analysis (COMPLETE)
- Identified that FF7_World_Map_Textures.md needs to be created as NEW FILE
- Determined content should consolidate texture documentation from:
  - FF7_World_Map_TXZ.md (primary source)
  - FF7_WorldMap_Module.md (texture reference paragraph)
- Major section 07_WORLD_MAP.md contains no new texture content

### Phase 2: File Creation Strategy

**Approach**: Create FF7_World_Map_Textures.md as consolidation of existing texture content with enhancement

**Structure**:
1. **Header**: Merge metadata (new file composition)
2. **Introduction**: Overview of world map texture system
3. **TXZ Archive Format**: From FF7_World_Map_TXZ.md (lines 11-64)
4. **Texture Coordinates**: Reference from FF7_WorldMap_Module.md (lines 231-235)
5. **Related Formats**: Links to BSZ (character models) and MAP (mesh structure)

**Content Sources**:
- ✅ Use FF7_World_Map_TXZ.md sections 0-4 (texture-related)
- ✅ Extract paragraph from FF7_WorldMap_Module.md (lines 231-235)
- ❌ Skip FF7_World_Map_TXZ.md sections 5-11 (AKAO audio, not textures)
- ❌ Do not extract from major section 07_WORLD_MAP.md (no texture content)

**File Location**:
`/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/FF7_World_Map_Textures.md`

**Merged Output Location**:
`/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/markdown/merged_with_pdf_content/FF7_World_Map_Textures.md`

---

## Key Recommendations

1. **Create the new file** consolidating texture documentation
2. **Ensure cross-references** between:
   - FF7_World_Map_Textures.md (texture handling)
   - FF7_WorldMap_Module.md (mesh UV coordinates)
   - FF7_World_Map_TXZ.md (archive format)
3. **Address gaps**:
   - Document texture table structure when available
   - Clarify PSX to PC texture conversion
   - Explain UV offset calculation algorithm
4. **No extraction from major section needed** (07_WORLD_MAP.md contains no texture content)

---

## Validation Notes

- ✅ Major section completely read (86 lines, all analyzed)
- ✅ Individual file status confirmed (does not exist)
- ✅ Related files skimmed for context
- ✅ Texture content identified and located
- ✅ Image inventory completed (0 images)
- ✅ Merge boundaries established
- ❌ Texture table not found in source materials
- ❌ PC-specific texture handling not documented

**Status**: Ready for Phase 2 (File Creation)

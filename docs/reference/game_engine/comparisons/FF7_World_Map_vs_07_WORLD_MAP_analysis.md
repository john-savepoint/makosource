# FF7 World Map Analysis: Individual Files vs Major Section

**Created**: 2025-11-28 15:30 JST (Thursday)
**Analysis Type**: Content comparison and extraction planning
**Status**: Complete - Ready for merge phase

---

## Executive Summary

### File Sizes
- **Major Section** (`07_WORLD_MAP.md`): 86 lines, ~3.8 KB
- **Individual Files Combined**: 574 lines, ~28 KB
- **Alignment**: Individual files are 6.7x larger, indicating more detailed coverage

### Key Findings
- **Content to Extract**: Encounter data format (PC) - 33 lines of substantive content
- **Images Found**: 0 images in major section
- **Substantive Gaps**: No markdown files cover encounter data format
- **Lorem Ipsum**: ~13 lines of placeholders (Land, Underwater, Snow Field, Data Format sections)

### Extraction Decision
**EXTRACT**: Encounter data format section (lines 7-71)
- This content is unique to the major section
- Not covered in any individual file
- Aligns with world map mechanics documentation

---

## Topic Scope Analysis

### File Scope Boundaries

**FF7_WorldMap_Module.md** (234 lines)
- **Coverage**: MAP/BOT file format, mesh structure, walkmap types, texture system
- **Scope**: Core world map geometry and rendering
- **Primary Topics**:
  - MAP file structure (blocks, meshes)
  - BOT file format (optimization variant)
  - Mesh data structures (triangles, vertices, normals)
  - Walkmap type enumeration (32 types)
  - Texture coordinate system and UV mapping

**FF7_World_Map_BSZ.md** (137 lines)
- **Coverage**: BSZ model format (Cloud's world map model)
- **Scope**: Character/vehicle model representation
- **Primary Topics**:
  - BSZ header structure
  - Model section (bones, parts, animations)
  - Model data layout
  - Skeleton data section

**FF7_World_Map_TXZ.md** (76 lines)
- **Coverage**: TXZ texture archive format
- **Scope**: Texture data storage and delivery
- **Primary Topics**:
  - LZS compression
  - Archive section structure
  - VRAM block format
  - Texture identifier mapping
  - Script/audio sections (AKAO format)

**FF7_WorldMap_Module_Script.md** (127 lines)
- **Coverage**: World map scripting engine
- **Scope**: Script execution, opcodes, control flow
- **Primary Topics**:
  - Stack-based instruction format
  - Context management and multitasking
  - Entity/model system
  - Function table and calling conventions
  - .ev file format (call table, code section)

### Boundary Summary
- **No overlap** between individual files
- **Complete coverage** of structural/technical aspects
- **Missing coverage**: Encounter mechanics and battle formation data

---

## Content Already in Individual Files

### Present in FF7_WorldMap_Module.md
- ✅ MAP/BOT file format and structure
- ✅ Mesh organization (16 meshes per block)
- ✅ Block layout and arrangement
- ✅ Triangle data structures
- ✅ Vertex/normal definitions
- ✅ Walkmap type table (32 types with descriptions)
- ✅ Texture numbering system
- ✅ UV coordinate handling and PSX VRAM offset system

### Present in FF7_World_Map_BSZ.md
- ✅ BSZ file header structure
- ✅ Model section organization
- ✅ Bones, parts, and animations subsections
- ✅ Model data layout details

### Present in FF7_World_Map_TXZ.md
- ✅ LZS compression format
- ✅ Archive section enumeration
- ✅ VRAM block structure
- ✅ Palette/texture identifier format
- ✅ Section 0-5+ content descriptions

### Present in FF7_WorldMap_Module_Script.md
- ✅ Stack-based instruction format
- ✅ Context and multitasking system
- ✅ Entity/model enumeration (25 models)
- ✅ Function table definitions
- ✅ .ev file format and code layout

---

## CRITICAL: Content to Extract

### Topic: Encounter Data Format (PC)

**Location in Major Section**: Lines 7-71
**Substantive Content**: YES - Real technical specifications
**Exists in Individual Files**: NO - No encounter documentation found
**Should Extract**: YES - Unique valuable content

#### Content Details

**Header/Overview** (Lines 7-13)
- Brief introduction about world map structure
- Notes on encounter file location (`enc_w.bin`)
- Mentions dialogue in 'mes' and event files in 'wm0.ev', 'wm2.ev', 'wm3.ev'

**Encounter Data Structure** (Lines 15-27)
- Encounter data starts at offset 0xB8
- Section size: 32 bytes each
- Field definitions:
  - Offset 0x00: Constant 01
  - Offset 0x01: Encounter rate (1 byte)
  - Offset 0x02-0x0D: Normal battles + chance (6 records, 2 bytes each)
  - Offset 0x0E-0x15: Special formation battles + chance (4 records, 2 bytes each)
  - Offset 0x16-0x1F: Chocobo battles (5 records, 2 bytes each)
- Note: Normal battle chances sum to 64

**Area Organization** (Lines 29-71)
- Areas have 4 terrain types:
  - Grass, Dirt/Snow, Forest/Desert, Beach
- Complete list of 16 world areas with terrain organization:
  1. Midgar Area
  2. Kalm Area
  3. Junon Area
  4. Corel Area
  5. Gold Saucer Area
  6. Gongaga Area
  7. Cosmo Area (Cosmo Canyon region)
  8. Nibel Area
  9. Rocket Area
  10. Wutai Area
  11. Woodlands Area
  12. Icicle Area
  13. Mideel Area
  14. North Corel Area (Materia Cave)
  15. Cactus Island
  16. Goblin Island

#### Extraction Justification
- **Unique Content**: Encounter mechanics and data structures are NOT documented elsewhere
- **Technical Value**: Provides offset specifications, byte layouts, and area organization
- **Integration Gap**: World map individual files focus on geometry/rendering, not encounter mechanics
- **Documentation Completeness**: Extracting this fills a critical gap in encounter system documentation

#### Line Count Impact
- **Extract**: 65 lines (7-71)
- **Skip (Lorem Ipsum)**: 14 lines (lines 5-6, 73-86)
- **Net Addition**: ~65 lines to encounter documentation (if merged into appropriate file)

---

## Content for Other Files

### Potential Redistributions
No content in major section is better suited for files other than World Map category.

The encounter data could theoretically belong to:
- A new file: `FF7_World_Map_Encounters.md` (recommended)
- Or merged into: `FF7_WorldMap_Module.md` (as new "Encounters" section)

---

## Images in Extracted Content

### Image Search Results
```bash
grep -n "!\[.*\](\|<img" /Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/reference/game_engine/extracted_major_sections/07_WORLD_MAP.md
```

**Result**: No images found in major section

**Image Count**: 0
**Path Adjustments Needed**: None

---

## Gaps and Discrepancies

### Documentation Gaps in Individual Files

1. **NO ENCOUNTER MECHANICS DOCUMENTATION**
   - Missing: Battle encounter system for world map
   - Missing: Encounter formation tables
   - Missing: Terrain-based encounter rate calculations
   - Impact: Major gameplay mechanic undocumented

2. **NO CHOCOBO ENCOUNTER SPECIFICS**
   - Missing: Chocobo-only encounter data
   - Missing: Chocobo interaction mechanics
   - Impact: Chocobo breeding/breeding farm system may reference this

3. **NO EVENT FILE REFERENCES**
   - Missing: Documentation of wm0.ev, wm2.ev, wm3.ev formats
   - Missing: Event scripting alongside script engine docs
   - Impact: Event system is mentioned but not fully documented

### Discrepancies

**None detected** - Individual files and major section don't overlap, so no conflicting information.

### Lorem Ipsum Placeholders (Not Extracted)

Lines 5-6, 73-86 contain Lorem Ipsum text for:
- World Map Overview
- Land
- Underwater
- Snow Field
- Data Format

These are placeholder sections with no substantive content and should NOT be extracted.

---

## Merge Plan Summary

### Phase 2 Actions

**File to Create/Modify**:
Option A: Create new `FF7_World_Map_Encounters.md` with extracted content
Option B: Expand `FF7_WorldMap_Module.md` with new "Encounters" section

**Recommended**: Option A (new file) for organizational clarity

**Extraction Process**:
1. Copy major section lines 7-71 (encounter data format)
2. No image path adjustments needed
3. Add extraction marker with source reference
4. Preserve verbatim text (no paraphrasing)

**File Merger Validation Checklist** (for Phase 2):
- [ ] Extract lines 7-71 from major section
- [ ] Copy verbatim (no modifications)
- [ ] Add extraction metadata header
- [ ] Verify no Lorem Ipsum included
- [ ] Confirm no images to adjust
- [ ] Validate structure and formatting
- [ ] Create new file or merge into existing

**Estimated Impact**:
- New lines: 65
- Images: 0
- Formatting changes: None (verbatim copy)
- Merge complexity: Low

---

## Recommendations for Next Agent

### If Creating FF7_World_Map_Encounters.md
1. Use extracted content (lines 7-71) as foundation
2. Add section header: "## Encounter Data Format (PC)"
3. Organize subsections:
   - Overview and file location
   - Data structure (32-byte sections)
   - Battle type breakdown (normal/special/chocobo)
   - Area organization table
4. Cross-reference from `FF7_WorldMap_Module.md`

### If Merging into FF7_WorldMap_Module.md
1. Add new section before "Walkmap" section
2. Use same formatting/style as existing content
3. Title: "## Encounter System"
4. Subsections as above

### If Creating merged_with_pdf_content/ versions
1. Create `FF7_World_Map_Encounters.md` (new file)
2. Optionally create merged `FF7_WorldMap_Module.md` with encounters integrated
3. Update cross-references between files

---

## Quality Assurance

### Analysis Verification
- ✅ Major section completely read (86 lines, all content reviewed)
- ✅ Individual files completely read (all 4 files examined)
- ✅ No images found (verified via grep)
- ✅ Content boundaries identified
- ✅ Unique content identified (encounter data)
- ✅ Extraction plan documented with line numbers

### Content Extraction Confidence
- **High Confidence**: Encounter data is clearly distinct content
- **No Conflicts**: No overlaps with existing individual files
- **Technical Accuracy**: Source content is from technical documentation (Qhimm wiki)

---

## Reference Information

### File Mapping (from MAPPING.md)
```
07_WORLD_MAP.md (Lines 6768-6853, 86 lines, 5.3KB)
├── FF7_WorldMap_Module.md (234 lines) - General world map
├── FF7_WorldMap_Module_Script.md (127 lines) - World map scripting
├── FF7_World_Map_BSZ.md (137 lines) - BSZ format
└── FF7_World_Map_TXZ.md (76 lines) - TXZ format
```

### Encounter Data Content Classification
- **Unique to Major Section**: YES
- **Critical Documentation Gap**: YES
- **Implementation Impact**: Medium (affects modding)
- **Priority for Extraction**: HIGH

---

## Session Information

**Analysis Date**: 2025-11-28
**Analysis Time**: 15:30 JST (Thursday)
**Analyzer**: Claude Code (Haiku 4.5)
**Status**: Ready for Phase 2 (Merge)

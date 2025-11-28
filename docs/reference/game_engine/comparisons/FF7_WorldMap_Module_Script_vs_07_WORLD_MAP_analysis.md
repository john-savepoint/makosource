# Analysis Report: FF7_WorldMap_Module_Script.md vs 07_WORLD_MAP.md

**Date**: 2025-11-29 JST
**Analysis Type**: Content comparison and merge identification
**Source Files**:
- Individual: `markdown/FF7_WorldMap_Module_Script.md` (127 lines, 9.0KB)
- Major Section: `extracted_major_sections/07_WORLD_MAP.md` (86 lines, 5.3KB)
- Related: `FF7_WorldMap_Module.md` (234 lines), `FF7_World_Map_BSZ.md` (137 lines), `FF7_World_Map_TXZ.md` (76 lines)

---

## Executive Summary

**Overall Assessment**: Minimal overlap, minimal extraction required
- **Individual file scope**: FF7 WorldMap **script engine** - stack-based instruction system, contexts, entities, functions, .ev file format
- **Major section scope**: FF7 WorldMap **overview and data** - encounter data structures, Lorem Ipsum placeholders
- **Content already in individual file**: YES - All scripting content is present and comprehensive
- **Content to extract from major section**: MINIMAL - Only real content is encounter data section (lines 8-71)
- **Images in major section**: NONE found
- **Substantive additions**: YES - The encounter data section provides useful PC format data not in individual file

**Recommendation**: Extract encounter data section (lines 8-71) which contains PC encounter format specifications and area listings.

---

## Topic Scope Analysis

### FF7_WorldMap_Module_Script.md Topics
1. **Script Engine** - Stack-based architecture (8-level deep stack)
2. **Instructions & Stack** - Instruction format, stack behavior, lazy evaluation
3. **Contexts** - Cooperative multitasking, script execution model
4. **Entities & Models** - 26 model IDs with names/purposes
5. **Functions** - Model functions (0-5) and system functions (0-7), mesh functions
6. **.ev Format** - File structure, call table format (3 types), code section
7. **Call Table** - Function identifier encoding, entry structure
8. **Code Section** - Code layout, first instruction requirements

**Scope**: This file is entirely focused on the scripting system that drives worldmap behavior. It is granular, detailed, and complete for the scripting domain.

### 07_WORLD_MAP.md Topics
1. **World Map Overview** - Lorem Ipsum placeholder (~67 lines of filler text)
2. **PC Format Encounter Data** - Real content:
   - Encounter rate format (offset 0xB8)
   - Section structure (32 bytes each)
   - Normal battles, special formations, chocobo battles
   - Area ordering (Midgar, Kalm, Junon, etc.)
3. **Land Section** - Lorem Ipsum placeholder
4. **Underwater Section** - Lorem Ipsum placeholder
5. **Snow Field Section** - Lorem Ipsum placeholder
6. **Data Format Section** - Empty (incomplete)

**Scope**: This major section was intended to cover world map overview, but is largely unfinished with placeholders. Only the encounter data section has substantive content.

---

## Content Already in Individual File

**Status**: ✅ COMPLETE - All scripting content in individual file is comprehensive and detailed.

### Verified Topics:

| Topic | Individual File | Coverage |
|-------|-----------------|----------|
| Script engine basics | Lines 7-17 | Complete - stack model, lazy evaluation explained |
| Contexts/multitasking | Lines 15-17 | Complete - cooperative multitasking, waiting states |
| Entities & models | Lines 19-59 | Complete - 26 models listed with annotations |
| Model functions | Lines 61-73 | Complete - 6 model functions documented |
| System functions | Lines 76-88 | Complete - 8 system functions documented |
| Mesh functions | Lines 91-91 | Complete - mention of mesh coordinate functions |
| .ev file format | Lines 93-128 | Complete - call table structure and code sections |
| Call table entry types | Lines 96-123 | Complete - all 3 types (system, model, mesh) documented |
| Code section layout | Lines 125-128 | Complete - offset requirements, first instruction |

**Finding**: The individual file is well-structured and covers all scripting topics thoroughly. No scripting content from the major section needs to be merged.

---

## Content to Extract from Major Section

### ITEM 1: PC Encounter Data Format

**Location**: Lines 8-71 of 07_WORLD_MAP.md
**Topic Alignment**: NEW - Not present in FF7_WorldMap_Module_Script.md
**Relevance**: HIGH - Provides important PC format specification for worldmap encounters

**Content**:
```
PC Format comment from unknown author
Encounter data starts at offset 0xB8
Section structure: 32 bytes per section
- Offset 0x00: 01
- Offset 0x01: Encounter rate (lower = higher chance)
- Offsets 0x02-0x0D: Normal battles + chance (6 records, 2 bytes each)
- Offsets 0x0E-0x15: Special formations + chance (4 records)
- Offsets 0x16-0x1F: Chocobo battles (5 records)

Area ordering:
1. Midgar Area
2. Kalm Area
3. Junon Area
4. Corel Area
5. Gold Saucer Area
6. Gongaga Area
7. Cosmo Area
8. Nibel Area
9. Rocket Area
10. Wutai Area
11. Woodlands Area
12. Icicle Area
13. Mideel Area
14. North Corel Area
15. Cactus Island
16. Goblin Island

Each area has 4 variants: Grass, Dirt/Snow, Forest/Desert, Beach
```

**Justification**: This is substantive technical data about encounter data format that complements the scripting documentation. While the script engine documentation doesn't cover encounter data loading, this could be useful context for understanding how the game populates encounter encounters on the worldmap. The area listing provides concrete game data.

**Images**: NONE

**Action**: Extract verbatim with attribution to major section

---

## Images in Extracted Content

**Finding**: No images found in major section 07_WORLD_MAP.md.

Search performed:
```bash
grep -n "!\[" 07_WORLD_MAP.md  # No results
grep -n "<img" 07_WORLD_MAP.md # No results
```

**Status**: ✅ No image paths need adjustment.

---

## Content for Other Files

### Ownership Assessment:

**FF7_WorldMap_Module.md** (234 lines - mesh/MAP format):
- Better fit for: Encounter data location/structure details
- Current topics: Map block structure, mesh format, walkmesh types, texture information
- **Note**: This file might be better target for encounter data if it covers data structure layouts

**FF7_World_Map_BSZ.md** (137 lines - model format):
- Current topics: BSZ header, model section, bones, parts, animations
- **Recommendation**: Not suitable for encounter data (model format specific)

**FF7_World_Map_TXZ.md** (76 lines - texture/archive format):
- Current topics: TXZ compression, archive format, sections
- **Recommendation**: Not suitable for encounter data (texture format specific)

**Assessment**: The encounter data could reasonably go into `FF7_WorldMap_Module.md` (which covers data structures) rather than the script file. However, since the task is to merge with FF7_WorldMap_Module_Script.md, it will be added there with clear demarcation.

---

## Gaps and Discrepancies

### Items NOT in Either File:

1. **Encounter generation mechanics** - How encounters are triggered, chosen
2. **Enemy AI** - Behavior scripts for encounters
3. **Special encounters** - Midgar Zolom, bosses, etc.
4. **Encounter rates formula** - How the rate byte translates to probability
5. **Chocobo breeding location data** - Which areas breed which types
6. **Quest encounter changes** - How story progression affects encounters

### Placeholder Issues:

The major section contains extensive Lorem Ipsum filler:
- World Map Overview (lines 3-6) - 100% placeholder
- Land section (lines 74-75) - 100% placeholder
- Underwater section (lines 77-79) - 100% placeholder
- Snow Field section (lines 82-83) - 100% placeholder
- Data Format section (line 86) - Empty/incomplete

**Assessment**: These placeholders appear to be incomplete documentation. No extraction needed since they contain no useful content.

---

## Merge Plan Summary

### Phase 1: Merge Decisions

| Item | Decision | Reason |
|------|----------|--------|
| Script engine content | NO MERGE - Already present | Individual file is complete and detailed |
| Encounter data (lines 8-71) | EXTRACT & MERGE | Substantive technical content, complements scripting |
| Lorem Ipsum sections | SKIP | Placeholder content only |
| References between files | ADD | Create cross-references to related files |

### Phase 2: Merge Strategy

1. **Copy original file** to `merged_with_pdf_content/FF7_WorldMap_Module_Script.md`
2. **Extract encounter data** from major section lines 8-71
3. **Add as new section** after .ev Format section (after line 128)
4. **Wrap with clear markers** indicating source and extraction metadata
5. **Preserve original structure** - don't rearrange existing content

### Phase 3: Content Placement

**Where to add extracted content**:
- After existing `.ev Format` section (end of line 128)
- New section: `### Encounter Data Format (PC)`
- Place before file end

**Why here**: Encounter data is runtime behavior data, separate from the script code format. Following the logical flow: script engine → how scripts are stored → how encounters are triggered/stored.

---

## Technical Details

### Line Count Analysis

| File | Lines | Size | Type |
|------|-------|------|------|
| FF7_WorldMap_Module_Script.md | 127 | 9.0KB | Individual |
| 07_WORLD_MAP.md | 86 | 5.3KB | Major section |
| Extracted content | ~64 | ~2.5KB | Encounter data only |
| Final merged file | ~191 | ~11.5KB | Individual + extraction |

### Extraction Line Mapping

**Source**: 07_WORLD_MAP.md lines 8-71
**Content**: PC format comment + encounter data structure + area listings
**Destination**: End of FF7_WorldMap_Module_Script.md (after line 128)
**Extraction marker**: Will include source attribution and extraction dates

---

## Validation Checklist

- [x] Verified individual file exists in markdown/ directory
- [x] Verified major section exists in extracted_major_sections/ directory
- [x] Confirmed merged_with_pdf_content/ directory exists and is empty
- [x] Read entire major section (86 lines)
- [x] Read entire individual file (127 lines)
- [x] Skimmed related files (FF7_WorldMap_Module.md, BSZ, TXZ) for boundaries
- [x] Searched for images in both files - FOUND NONE
- [x] Identified content to extract with line numbers (lines 8-71)
- [x] Explained WHY each extraction belongs in this file
- [x] Identified no discrepancies or concerning overlap
- [x] Created comprehensive analysis report

---

## Next Steps (for PHASE 2)

1. Copy original file to merged_with_pdf_content/
2. Extract lines 8-71 from major section (encounter data)
3. Add as new section titled "### Encounter Data Format (PC)"
4. Wrap with extraction markers
5. Add merge metadata header
6. Verify no loss of original content
7. Verify file created only in merged_with_pdf_content/

---

**Report Status**: ✅ COMPLETE
**Ready for Phase 2**: YES
**Estimated merge time**: 10 minutes

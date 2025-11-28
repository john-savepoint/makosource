# FF7 Game Engine Documentation Enhancement Plan

**Created:** 2025-11-27 15:32 JST
**Session ID:** f0a6bdfa-9156-4ef9-8575-cd3124b862ba
**Status:** Phase 1 Complete - Structural Issues Identified

---

## Overview

This document tracks the ongoing enhancement of `ff7 game engine.md` by cross-referencing with the qhimm-modding.fandom.com wiki. The goal is to create an accurate, well-formatted, comprehensive technical reference.

---

## Phase 1: Initial Enhancements (COMPLETED)

### Pages Scraped and Applied

1. **FF7/History** - ✅ Fully enhanced
   - Added missing "Preface" subsection
   - Fixed typos: its/it's, near/neat, fared/faired
   - Corrected Roman numerals (Part I/IV vs 1/4)
   - Standardized terminology (U.S., 3D, 15-bit)

2. **FF7/Engine_basics** - ✅ Enhanced
   - Fixed "out of" (was "out ofm")

3. **FF7/Kernel/Overview** - ✅ Enhanced
   - Fixed possessive errors (its menu, the menu)

4. **FF7/LGP_format** - ✅ Major overhaul
   - **Critical fix:** TOC structure corrected (1 byte + 2 byte short, not 3 bytes)
   - Restructured all tables for clarity
   - Cleaned up informal language
   - Added "Useful Downloads" section with tool links

5. **General typo fixes throughout:**
   - its vs it's possessive errors
   - "than" vs "that" grammar
   - Standardized hyphenation (15-bit, 3D, 32-bit)

### Commit Made

```
commit 339a87c
docs(game-engine): enhance FF7 game engine documentation with wiki content
```

---

## Phase 2: Structural & Formatting Fixes (NEXT SESSION)

### Critical Structural Issues Identified

#### 1. **Table of Contents Formatting Inconsistencies**

The markdown has mixed bullet lists where proper heading hierarchies should be used:

**Current (incorrect):**
```markdown
#### The Kernel
- I. Kernel Overview
  - 1.1 History
  - 1.2 Kernel Functionality
- II. Memory Management
  - 1.1. RAM management
```

**Should be:**
```markdown
# The Kernel

## I. Kernel Overview

### 1.1 History
### 1.2 Kernel Functionality

## II. Memory Management

### 1.1 RAM Management
```

#### 2. **Double Indentation in Lists**

Throughout the document, especially in:
- Low Level Libraries section
- Menu Module section
- Field Module section
- Battle Module section

Lists have unnecessary double indentation making the TOC hard to navigate.

#### 3. **Inconsistent Heading Styles**

Mix of:
- `# **Bold Headings**`
- `## *Italic Headings*`
- `#### **Mixed Bold Headings**`

Should standardize to clean markdown headings without decorative formatting.

#### 4. **Table Formatting Issues**

Some tables have:
- Extra empty columns
- Inconsistent alignment
- HTML `<br>` tags instead of proper row breaks

#### 5. **Missing Alt Text on Images**

All `![](_page_X_Picture_Y.jpeg)` references lack alt text (markdownlint warnings).

---

## Phase 3: Content Enhancement (FUTURE SESSIONS)

### Approach: Manual Copy-Paste Instead of Scraping

**Rationale:**
- Saves tokens (scraping is expensive)
- Ensures exact pages are included
- Better control over what content is integrated

**Process:**
1. User will copy-paste wiki content directly
2. Claude will integrate and format properly
3. Focus on critical missing sections first

### Critical Missing Wiki Pages

Based on the wiki map (200+ pages total), these are HIGH PRIORITY missing sections:

#### **Low Level Libraries** (Critical for technical reference)
- [ ] **FF7/TEX_format** - Texture format for PC
- [ ] **FF7/TIM_format** (PSX/TIM_format) - Texture format for PSX
- [ ] **FF7/LZS_format** - Compression format (referenced but not enhanced)
- [ ] **FF7/P** - Polygon data format
- [ ] **FF7/Playstation_Battle_Model_Format**

#### **Menu Module**
- [ ] **FF7/Menu_Module** - Main menu module page
- [ ] **FF7/Savemap** - Save game format

#### **Field Module** (Many subsections)
- [ ] **FF7/Field_Module** - Main page (scraped but not applied yet)
- [ ] **FF7/Field/Field_Script** - Script system
- [ ] **FF7/Field/Script/Opcodes** - Script commands overview
- [ ] **FF7/Field/Camera_Matrix**
- [ ] **FF7/Field/Model_Loader**
- [ ] **FF7/Field/Palette**
- [ ] **FF7/Field/Walkmesh**
- [ ] **FF7/Field/Triggers**
- [ ] **FF7/Field/Encounter**
- [ ] **FF7/Field/Background**
- [ ] **FF7/Field_Module/DAT/Tile_Map**
- [ ] **FF7/Field/MIMfile**
- [ ] **FF7/Field/BSX**
- [ ] **FF7/Field/BCX**
- [ ] **FF7/Field/FIELD.TDB**
- [ ] **FF7/Field/DialogWindow**

#### **Battle Module**
- [ ] **FF7/Battle/Battle_Mechanics**
- [ ] **FF7/Battle/Battle_Field**
- [ ] **FF7/Battle/Battle_Scenes**
- [ ] **FF7/Battle/Battle_Scenes/Battle_Script**
- [ ] **FF7/Battle/Battle_Scenes/Battle_AI_Addresses**
- [ ] **FF7/Battle/Special_Attack_Flags**
- [ ] **FF7/Attack_Special_Effects**
- [ ] **FF7/Battle/Damage_Calculation**
- [ ] **FF7/Battle/Status_Effects**
- [ ] **FF7/Battle/Targeting_Data**
- [ ] **FF7/Battle/Elemental_Data**
- [ ] **FF7/Battle/Impact_Effect_Id_List**
- [ ] **FF7/Battle/Sound_Effect_Id_List**
- [ ] **FF7/Battle/Attack_Effect_Id_List**
- [ ] **FF7/Battle/Attack_Special_Effects**
- [ ] **FF7/Battle/Battle_Animation_(PC)**

#### **Kernel Data Formats**
- [ ] **FF7/Command_data**
- [ ] **FF7/Attack_data**
- [ ] **FF7/Item_data**
- [ ] **FF7/Weapon_data**
- [ ] **FF7/Armor_data**
- [ ] **FF7/Accessory_data**
- [ ] **FF7/Materia_data**
- [ ] **FF7/Materia_Types**
- [ ] **FF7/Battle_and_growth_data**
- [ ] **FF7/Character_starting_stats**

#### **World Map Module**
- [ ] **FF7/WorldMap_Module**
- [ ] **FF7/WorldMap_Module/TextureTable**
- [ ] **FF7/WorldMap_Module/Script**
- [ ] **FF7/World_Map/BSZ**
- [ ] **FF7/World_Map/TXZ**

#### **Sound**
- [ ] **FF7/PSX/PSX_Sound**
- [ ] **FF7/PSX/Sound/Overview**
- [ ] **FF7/PSX/Sound/INSTRx.DAT**
- [ ] **FF7/PSX/Sound/INSTRx.ALL**
- [ ] **FF7/PSX/Sound/AKAO_frames**
- [ ] **FF7/PSX/Sound/Opcodes** (various)

#### **Text Format**
- [ ] **FF7/FF_Text** - String encoding format

### Lower Priority (Reference Only)

**Field Script Opcodes** - 200+ individual opcode pages:
- Most are documented in the markdown already
- Only enhance if specific opcodes are found to be missing/incorrect
- Examples: 00_RET, 01_REQ, 03_REQEW, etc.

**Technical Help Pages:**
- FF7/Technical/* pages - Troubleshooting, not technical reference

---

## Immediate Next Steps (Session After Compaction)

### Step 1: Fix Structural Issues (Priority: HIGH)
1. Standardize heading hierarchy throughout document
2. Remove unnecessary list indentation
3. Fix double-indented TOC entries
4. Remove decorative bold/italic from headings
5. Clean up tables (remove empty columns, fix alignment)

### Step 2: Apply Field_Module Updates (Priority: HIGH)
The Field Module wiki page was scraped but changes not yet applied. Key fixes needed:

**Important Files table correction:**
```markdown
| PSX Version   | PC Version              |
|---------------|-------------------------|
| /FIELD/*.DAT  | /DATA/FIELD/FLEVEL.LGP  |
| /FIELD/*.MIM  | /DATA/FIELD/FLEVEL.LGP  | ← Fix: was CHAR.LGP
| /FIELD/*.BSX  |                         |
| /FIELD/*.BCX  | /DATA/FIELD/CHAR.LGP    | ← Add this row
```

**PC Field File Header - Section descriptions:**
- Section 3: "Model Loader" (was "Unknown")
- Section 6: "TileMap (Unused)" (was "Unknown")
- Section 8: "Triggers" (was "Unknown")

### Step 3: Manual Content Integration (Priority: MEDIUM)
User will copy-paste critical missing wiki pages:
1. Start with **TEX_format** and **TIM_format** (frequently referenced)
2. Then **Field/Field_Script** (core gameplay system)
3. Then **Battle** module sections (combat is critical)
4. Continue with other sections as needed

---

## Working Notes

### Known File Naming Convention
- File names like `jfleve.lgp` are **intentional** (not typos)
- Many technical abbreviations preserved from original docs

### Table Extraction Quality
- Wiki HTML tables → better structure than PDF
- Markdown tables from PDF → often malformed
- Strategy: Use wiki for table-heavy sections

### Original Document Context
- Converted from heavily stylized PDF ("Gears" by Halkun)
- Some informal language preserved for authenticity
- Balance: Professional clarity vs original authorial voice

---

## Success Metrics

- [ ] All headings use proper hierarchy (no decorative bold/italic)
- [ ] No double-indented lists in TOC
- [ ] All critical wiki pages integrated
- [ ] All tables properly formatted
- [ ] All typos corrected (its/it's, than/that, etc.)
- [ ] Technical accuracy verified (especially byte structures)
- [ ] Document is navigable and professional

---

## Resources

**Wiki Base URL:** https://qhimm-modding.fandom.com/wiki/FF7
**Markdown File:** `docs/reference/game_engine/ff7 game engine.md`
**File Size:** 8,157 lines, ~461KB
**Original Source:** Halkun's "Gears" PDF document

---

## Session Handoff Notes

**For Next Session:**
1. Load this enhancement plan
2. Fix structural issues first (headings, indentation)
3. Apply Field_Module corrections
4. User will then provide wiki content via copy-paste for integration
5. Focus on high-priority missing sections (TEX, TIM, Field Script)

**Token Management:**
- Manual copy-paste saves tokens vs scraping
- Work incrementally, commit frequently
- May need multiple sessions for full enhancement

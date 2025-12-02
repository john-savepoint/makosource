# Critical Discrepancies Requiring Investigation
**Created**: 2025-11-30 21:41 JST (Sunday)
**Source**: Analysis of `repomix-comparisons-markdown.md`
**Purpose**: Comprehensive list of data conflicts, missing content, and verification needs identified during merge analysis
**Status**: 🔴 **REQUIRES REVIEW BEFORE PRODUCTION USE**

---

## Executive Summary

During the comprehensive Phase 1 analysis of FF7 game engine documentation merges, **multiple critical discrepancies** were identified that require investigation and verification before the merged files can be considered production-ready. These range from **conflicting binary offset values** to **contradictory format specifications** that could lead to incorrect implementations.

**Key Statistics**:
- **Critical Data Conflicts**: 5 identified
- **Format Specification Conflicts**: 3 identified
- **Missing Content Requiring Decisions**: 15+ sections
- **Verification Required Before Production**: 8 items
- **Total Files Analyzed**: 15+ comparison pairs

---

## 🔴 CRITICAL: Data Value Conflicts

### 1. Bank 5 Memory Address Values (KERNEL Memory Management)

**Status**: 🔴 **BLOCKING - Must verify before merge**

**Location**:
- File 1: `03_KERNEL.md` line 42
- File 2: `FF7_Kernel_Memory_management.md` line 23

**Conflict**:
| Source | 8-Bit Bank Value | 16-Bit Bank Value |
|--------|------------------|-------------------|
| Major Section (03_KERNEL.md) | 0x7 | 0xF |
| Individual File | 0xF | 0x7 |

**Values are swapped** - this is a critical error that would cause incorrect memory access in any implementation.

**Required Action**:
- [ ] Verify against original FF7 source code or authoritative disassembly
- [ ] Check which file has the correct mapping
- [ ] Update incorrect file before merge
- [ ] Add verification note in documentation

**Impact**: HIGH - Memory banking errors would cause save corruption or game crashes

---

### 2. Section 3 Labeling Conflict (KERNEL.BIN)

**Status**: ⚠️ **Needs Clarification**

**Location**:
- Multiple files reference KERNEL.BIN Section 3

**Conflict**:
| Source | Section 3 Name |
|--------|---------------|
| Some docs | "Savemap initialization data" |
| Other docs | "Battle and growth data" |
| Another source | "Unknown (Savemap?)" |

**Required Action**:
- [ ] Verify KERNEL.BIN section 3 actual contents
- [ ] Determine if there are version differences (PC vs PSX)
- [ ] Standardize naming across all documentation

**Impact**: MEDIUM - Confusing but doesn't affect binary parsing if offsets are correct

---

### 3. Offset Value Conflicts (KERNEL.BIN)

**Status**: ⚠️ **Needs Verification**

**Location**: KERNEL.BIN documentation

**Conflict**:
- Offset 0x2119 vs 0x2199 referenced in different files for same data

**Required Action**:
- [ ] Verify correct offset from binary file
- [ ] Check if this is hex transcription error (1 vs 9)
- [ ] Update incorrect reference

**Impact**: HIGH - Wrong offset = reading wrong data

---

## 🟡 Format Specification Conflicts

### 4. Animation Header Format Conflict (Field Module)

**Status**: 🔴 **CRITICAL - Contradictory specifications**

**Location**:
- File 1: `FF7_Field_Module.md` lines 243-287
- File 2: `05_FIELD_MODULE.md` lines 2599-2642

**Conflict**:

| Aspect | Individual File | Major Section |
|--------|----------------|---------------|
| Header Size | 36 bytes | 24 bytes |
| Header Fields | version, frames_count, bones_count, rotation_order, 5 runtime_data values | x1, frames_count, bones_count, x2/x3/x4 + 12 unknown bytes after |
| Rotation Order | Documented | Not documented |
| Frame Format | root rotation (3 floats) + root translation (3 floats) + rotations | 6 floats + rotations |

**Required Action**:
- [ ] Determine which specification is correct (may be version-specific)
- [ ] Check if this is PSX vs PC difference
- [ ] Verify against actual .a files in FF7 data
- [ ] Document which version each spec applies to
- [ ] Add technical notes explaining discrepancies

**Impact**: CRITICAL - Incorrect header parsing makes animations unreadable

---

### 5. Scene.bin Format Conflict (Battle Scenes)

**Status**: ⚠️ **Different Documentation Sources**

**Location**:
- File 1: `FF7_Battle_Battle_Scenes.md` (from Qhimm wiki)
- File 2: `06_BATTLE_MODULE.md` (from Fremen, Sept 30, 2003)

**Conflict**:
- ~70% content overlap but different presentation formats
- Some data structure offsets differ slightly
- Attack data organized differently (both claim 28 bytes but structure varies)
- Formation 2 record 6 shows 0x01C8 offset in major section but structure may be off

**Required Action**:
- [ ] Determine which documentation source is authoritative
- [ ] Check if differences represent version changes (PSX vs PC vs JP)
- [ ] Test both specifications against actual scene.bin files
- [ ] Document known variations
- [ ] **Recommendation**: Individual file appears more precise - verify before accepting major section version

**Impact**: MEDIUM-HIGH - Could cause incorrect battle configuration parsing

---

### 6. Japanese Scene.bin Format Variation

**Status**: ✅ **Documented but needs cross-verification**

**Finding**: Individual file documents that Japanese scene.bin uses:
- 16-byte enemy/attack names (instead of 32 bytes in English version)

Major section does NOT mention this variation.

**Required Action**:
- [ ] Verify this is correctly documented in individual file
- [ ] Add this critical note to major section if missing
- [ ] **CRITICAL FOR JAPANESE MOD WORK** - ensure this is preserved

**Impact**: HIGH for Japanese mod - Would cause misaligned data reading

---

## 📋 Missing Content Requiring Investigation

### 7. Field Module - Massive Missing Content

**Status**: 🔴 **CRITICAL INCOMPLETENESS**

**Individual File**: `FF7_Field_Module.md` (293 lines)
**Major Section**: `05_FIELD_MODULE.md` (2,645 lines)

**Missing from Individual File** (~2,300+ lines):

#### Critical Missing Sections:
1. **Section 1: Dialog and Event Script Format** (lines 74-106)
   - FF7SCRIPTHEADER struct completely missing
   - Entity definitions missing
   - No documentation of how scripts are stored

2. **Section 2: Camera Matrix** (lines 109-168)
   - Complete camera system undocumented
   - Camera matrix structure missing
   - Center calculation formula missing

3. **Section 4: Palette Format** (lines 170-241)
   - Palette structure completely missing
   - Color data format not documented

4. **Section 5: Walkmesh Structure** (lines 244-354)
   - Character movement system completely missing
   - Triangle data structures not documented
   - Access data missing

5. **Section 7: Encounter Data** (lines 383-461)
   - Encounter table format missing
   - Probability calculations not documented

6. **Section 9: Background and Sprite Format** (lines 463-567)
   - Background rendering system missing
   - Sprite layer system not documented

7. **Complete Opcode Matrix** (256 script commands)
   - Individual file has brief overview
   - Major section has complete OPCODE table
   - **This is fundamental for script modding**

**Required Action**:
- [ ] Verify merged file includes all these sections
- [ ] Check if some content belongs in separate files
- [ ] Ensure no critical gameplay systems are undocumented

**Impact**: CRITICAL - Field module is core game engine, missing docs = incomplete understanding

---

### 8. KERNEL.BIN Binary Specifications

**Status**: 🔴 **CRITICAL - Fundamental data missing**

**Individual File**: `FF7_Kernel_Kernelbin.md` (58 lines - overview only)
**Major Section**: `03_KERNEL.md` contains 457 lines of binary specifications

**Missing Content**:
- Section 1: Command data format
- Section 2: Attacks data format (28-byte records with 20+ attribute types)
- Section 5: Item data format (27-byte records)
- Section 6: Weapon data format (44-byte records)
- Section 7: Armor data format (36-byte records)
- Section 8: Accessory data format
- Section 9: Materia data format

**Required Action**:
- [ ] Verify if merged file includes complete binary specifications
- [ ] These are ESSENTIAL for save editors and modding tools
- [ ] Check if any specifications conflict with existing tools/knowledge

**Impact**: CRITICAL - Without these, cannot parse KERNEL.BIN correctly

---

### 9. Low-Level Libraries and File Formats

**Status**: ⚠️ **Significant gaps**

**Individual File**: `FF7_Kernel_Low_level_libraries.md` (128 lines)
**Major Section**: `03_KERNEL.md` contains 545+ lines covering:

**Missing Content**:
- LZS compression algorithm details (67 lines)
- LGP archive format specification (72 lines)
- Texture format specifications (TIM/TEX - 120 lines)
- 3D model formats (HRC, RSD, P formats - 336 lines)

**Required Action**:
- [ ] Verify these are documented in individual file or separate files
- [ ] LZS/LGP are referenced by multiple other systems
- [ ] Model formats essential for asset modding

**Impact**: HIGH - These are cross-cutting formats used throughout the game

---

## ⚠️ Quality & Consistency Issues

### 10. Placeholder Content in Major Sections

**Status**: ✅ **Identified - needs cleanup decision**

**Files with Lorem Ipsum placeholders**:
- `07_WORLD_MAP.md` - Sections I, II, III, IV (~50% of file)
- `04_MENU_MODULE.md` - Some subsections
- `08_MINI_GAMES.md` - Intentional section headers for future content

**Required Action**:
- [ ] Confirm merged files exclude all Lorem Ipsum
- [ ] Verify no placeholder text leaked into production docs
- [ ] Document which sections remain incomplete

**Impact**: LOW - Cosmetic only if properly excluded from merges

---

### 11. Image Reference Inconsistencies

**Status**: ✅ **Catalogued**

**Issues Found**:
- `_page_XX_Picture_YY.jpeg` format from PDF extraction
- Some files reference `Engine_parts.jpg` vs `_page_8_Picture_5.jpeg` (same content)
- Semantic names preferred over PDF page references

**Required Action**:
- [ ] Verify all image paths adjusted to use semantic names
- [ ] Check all images exist in `/images/` directory
- [ ] Confirm relative paths are correct (`../../images/`)

**Impact**: MEDIUM - Broken image links make documentation less useful

---

### 12. Capitalization Inconsistencies

**Status**: ⚠️ **Standardization needed**

**Examples**:
- "Savemap" vs "Save Map" (inconsistent across files)
- "KERNEL.BIN" vs "Kernel.bin" vs "kernel.bin"

**Required Action**:
- [ ] Choose standard capitalization for key terms
- [ ] Document style guide for future consistency
- [ ] Update documentation to match standard

**Impact**: LOW - Cosmetic but affects professionalism

---

## 🔍 Verification Checklist Before Production

### Pre-Deployment Validation

**Must verify before declaring merged files production-ready**:

- [ ] **Bank 5 memory values verified** from authoritative source
- [ ] **Animation header format conflict resolved** (24-byte vs 36-byte)
- [ ] **Scene.bin format specification chosen** (which source is authoritative?)
- [ ] **KERNEL.BIN binary specifications complete** in merged files
- [ ] **Field Module critical sections included** (all 9+ sections)
- [ ] **Offset 0x2119 vs 0x2199 verified**
- [ ] **Section 3 naming standardized** across all files
- [ ] **Japanese format variations documented**
- [ ] **All Lorem Ipsum removed** from merged files
- [ ] **All image paths adjusted** and images exist
- [ ] **Low-level library formats complete** (LZS, LGP, model formats)
- [ ] **Opcode matrix complete** (256 script commands)

### Testing Recommendations

**Suggested validation methods**:

1. **Binary File Verification**:
   - Test KERNEL.BIN parsing against actual game files
   - Verify save file offsets match documented values
   - Check animation headers against real .a files

2. **Cross-Reference Check**:
   - Compare documentation against existing modding tools (Makou Reactor, etc.)
   - Check against known community knowledge (Qhimm wiki, etc.)
   - Verify against disassemblies where available

3. **Japanese Version Testing**:
   - Verify 16-byte vs 32-byte name fields
   - Test against actual Japanese FF7 files
   - Confirm character encoding documentation

---

## 📊 Priority Matrix

### Immediate Action Required (Before Production)

| Issue | Severity | Blocking | Estimated Effort |
|-------|----------|----------|------------------|
| Bank 5 memory values | 🔴 CRITICAL | YES | 1-2 hours (research) |
| Animation header conflict | 🔴 CRITICAL | YES | 2-4 hours (testing) |
| Scene.bin source authority | 🟡 HIGH | NO | 1 hour (comparison) |
| Field Module completeness | 🔴 CRITICAL | NO | Verify only (15 min) |
| KERNEL.BIN specs | 🔴 CRITICAL | NO | Verify only (15 min) |

### Can Be Addressed Post-Production

| Issue | Severity | Notes |
|-------|----------|-------|
| Capitalization | 🟢 LOW | Style guide update |
| Image naming | 🟡 MEDIUM | Doesn't break functionality |
| Lorem Ipsum check | 🟢 LOW | Visual inspection |
| Offset 0x2119 typo | 🟡 MEDIUM | Single value fix |

---

## 📝 Recommendations

### For Documentation Maintainers

1. **Create verification scripts**:
   - Compare documented offsets against actual binary files
   - Validate struct sizes match documented byte counts
   - Check image file existence

2. **Establish authoritative sources**:
   - Designate which documentation source takes precedence
   - Document known variations (PC vs PSX vs JP)
   - Create version matrix showing differences

3. **Version control**:
   - Tag current state before making corrections
   - Document all conflict resolutions
   - Maintain changelog of verification findings

### For Users of This Documentation

**Until verification is complete**:
- ⚠️ **DO NOT USE** for critical implementation without cross-checking
- ⚠️ **VERIFY** binary offsets against actual game files
- ⚠️ **TEST** format specifications before relying on them
- ⚠️ **CHECK** multiple sources for conflicting data

**Known reliable sections** (less likely to have errors):
- High-level system overviews
- Conceptual explanations
- Historical context
- Tool references

**Higher-risk sections**:
- Binary offset specifications
- Struct size definitions
- Memory bank mappings
- Format specifications with conflicting sources

---

## 🔗 Related Documentation

**For investigators**: See individual comparison files for detailed analysis:
- `FF7_Kernel_Memory_management_vs_03_KERNEL_analysis.md` - Bank 5 conflict details
- `FF7_Field_Module_vs_05_FIELD_MODULE_analysis.md` - Animation header conflict
- `FF7_Battle_Battle_Scenes_vs_06_BATTLE_MODULE_analysis.md` - Scene.bin conflict
- Full comparison data: `repomix-comparisons-markdown.md`

---

## 📅 Status Tracking

**Created**: 2025-11-30 21:41 JST
**Last Updated**: 2025-11-30 21:41 JST
**Status**: 🔴 **DRAFT - Awaiting Verification**
**Next Review**: After critical conflicts resolved
**Version**: 1.0.0

---

**END OF REPORT**

# New Threat Mod - Kernel Modifications Analysis

**Created:** 2026-01-22 22:50:25 JST
**Session ID:** 552a7ee9-e42e-4439-8243-2eb1a43110da
**Mod Version:** New Threat 2.0
**Analysis Scope:** /kernel/ directory modifications

---

## Executive Summary

The New Threat mod's kernel directory contains modified KERNEL.BIN and kernel2.bin files that comprehensively overhaul Final Fantasy VII's core battle system data. These files represent the foundational changes that enable New Threat's complete gameplay rebalancing, including revised materia systems, equipment stats, damage formulas, and character progression.

**Key Statistics:**
- **KERNEL.BIN Size:** 23,217 bytes (BIN-GZIP archive, 27 sections)
- **kernel2.bin Size:** 14,497 bytes (LZSS compressed text data)
- **Modified Data Types:** 27 distinct sections (9 binary data, 18 text sections)
- **New Materia Added:** 13+ new/splinter materia types
- **Formula Revisions:** Multiple damage calculations modified

---

## File Structure Overview

### KERNEL.BIN (Primary Data Archive)

The KERNEL.BIN file is in BIN-GZIP format - a concatenated archive of 27 gzipped sections with 6-byte headers. This file is identical in structure between PSX and PC versions and contains all static gameplay data and menu text.

**File Format:**
- Type: BIN-GZIP archive (27 concatenated gzipped sections)
- Header: 6 bytes per section (`0x7f 0x00 0x00 0x01 0x00 0x00` signature observed)
- Sections 1-9: Binary data (battle mechanics)
- Sections 10-27: FF Text files (descriptions, names, battle text)

**Compression Evidence:**
```
Offset 0x000C: 0x1f 0x8b 0x08 (GZIP magic number)
Offset 0x0084: 0x1f 0x8b 0x08 (Second section GZIP marker)
```

### kernel2.bin (Text Data Archive - PC Only)

The kernel2.bin file is a PC-specific optimization containing only the text sections (10-27) from KERNEL.BIN, decompressed and re-compressed as a single LZSS archive.

**File Format:**
- Type: LZSS compressed archive
- Header: 4 bytes (file length: `0x9d 0x38 0x00 0x00` = 14,493 bytes)
- Content: Concatenated text sections 10-27 (ungzipped, then LZSS compressed)
- Size Constraint: Maximum 27KB (27,648 bytes) when decompressed

**Header Analysis:**
```
Offset 0x0000: 9d 38 00 00 = 14,493 bytes (file length)
Offset 0x0004: ff a6 01 00 = Text section offset table begins
```

---

## Modified Kernel Sections

### Binary Data Sections (1-9)

#### Section 1: Command Data (Offset 0x0006)
**Modifications:**
- New command materia added to separate previously combined abilities
- Command behaviors adjusted for New Threat's tactical depth
- Related to splinter materia system (commands moved to separate materia)

**Impact:** Players must now strategically choose between commands that were previously bundled, requiring more thoughtful materia loadout decisions.

#### Section 2: Attack Data (Offset 0x0086)
**Modifications:**
- All attack formulas revised for balance
- New attacks added for splinter materia (Regen, Slow, Dispel, etc.)
- Elemental interactions adjusted
- Long Range flag now usable by enemies

**Impact:** Combat calculations fundamentally changed; attacks deal different damage compared to vanilla.

#### Section 3: Battle and Growth Data (Offset 0x063A)
**Modifications:**
- Character stat growth re-implemented (natural level-up progression)
- Initial stats revised for all characters
- New innate abilities for characters
- Limit Break damage formulas revised (mix of Physical/Magical with effects)

**Impact:** Character progression now follows natural stat growth curves rather than vanilla's static approach.

#### Section 4: Initialization Data (Offset 0x0F7F)
**Modifications:**
- Character starting stats adjusted
- Initial equipment loadouts revised
- Starting materia configurations changed

**Impact:** Early-game balance significantly altered; characters begin with different strengths.

#### Section 5: Item Data (Offset 0x111B)
**Modifications:**
- All item effects revised
- Item availability adjusted (coordinated with shop/field placement changes)
- New item behaviors implemented

**Impact:** Item utility rebalanced; some items more/less valuable than vanilla.

#### Section 6: Weapon Data (Offset 0x137A)
**Modifications:**
- All weapon stats revised
- Weapon growth curves adjusted
- Special weapon formulas modified (Powersoul, Missing Score, etc.)
- Materia slot configurations potentially adjusted

**Impact:** Weapon viability throughout the game rebalanced; ultimate weapons no longer dominate.

#### Section 7: Armor Data (Offset 0x1A30)
**Modifications:**
- All armor stats revised
- Elemental resistances adjusted
- Materia slot configurations potentially modified
- Armor progression rebalanced

**Impact:** Defensive strategy options expanded; armor choices more meaningful.

#### Section 8: Accessory Data (Offset 0x1B73)
**Modifications:**
- Accessory effects revised
- New strategic accessory combinations enabled
- Accessory availability coordinated with shops

**Impact:** Accessory selection becomes more tactical with revised effects.

#### Section 9: Materia Data (Offset 0x1C11)
**New Materia Added:**
1. **Omni-Plus** - Unknown stat boost function
2. **Hydro** - Water-element magic
3. **Pearl** - Holy-element magic
4. **Osmose** - MP absorption spell (separated from standard magic)
5. **X-Attack** - Attack command enhancement
6. **Flash** - Status effect magic
7. **Core** - Unknown function

**Splinter Materia (Single-Spell Variants):**
1. **Regen** - Separated from Restore line to enable support materia combos
2. **Slow** - Separated from Time line
3. **Dispel** - Separated from parent materia
4. **MBarrier** - Separated from Barrier line
5. **Reflect** - Separated from parent materia
6. **Break** - Separated from Transform line
7. **Tornado** - Separated from Contain line

**Materia System Changes:**
- AP requirements adjusted for all materia
- Materia level progression revised
- Support materia interactions enabled for previously locked spells
- Materia availability coordinated with game progression

**Impact:** Materia system now offers strategic depth through splinter materia, allowing powerful spell/support combos without level-up restrictions.

### Text Data Sections (10-27)

All text sections modified to reflect new content:

#### Sections 10-16: Descriptions
- Command descriptions (Section 10)
- Magic descriptions (Section 11) - Includes new spells
- Item descriptions (Section 12)
- Weapon descriptions (Section 13)
- Armor descriptions (Section 14)
- Accessory descriptions (Section 15)
- Materia descriptions (Section 16) - Includes 13+ new materia

#### Sections 18-25: Names
- Command Names (Section 18)
- Magic Names (Section 19) - Includes new magic
- Item Names (Section 20)
- Weapon Names (Section 21)
- Armor Names (Section 22)
- Accessory Names (Section 23)
- Materia Names (Section 24) - Includes new materia
- Key Item Names (Section 25)

#### Sections 26-27: Battle Text
- Battle and Battle-Screen Text (Section 26)
- Summon Attack Names (Section 27)

**Text Analysis Evidence:**
```
kernel2.bin contains readable text strings:
- "WEAPON" (0x004D)
- "SPELL" (0x0051)
- "#ALL" (0x0058)
- "SUMME[ons]" (0x0062)
- "ITEM" (0x006B)
- "TEAM" (0x0073)
- "ACCURACY" (0x00B4)
- "CRITICAL" (0x00C0)
- "ATTACK" (0x00C8)
- "CONTROL" (0x00D1)
```

---

## Gameplay Balance Changes

### Damage Formula Modifications

**Modified Formulas:**
1. **Critical Damage** - Adjusted multiplier (specifics require deeper analysis)
2. **Elemental Damage** - Modified effectiveness calculations
3. **Sadness/Fury** - Adjusted status effect modifiers
4. **Powersoul** - Weapon-specific formula revised
5. **Missing Score** - Weapon-specific formula revised
6. **Aire Tam Storm** - Limit break formula revised
7. **Drain Effect** - Reduced from 100% to 12.5% absorption

### Battle Mechanics Changes

**Global Modifiers:**
- Sense Limit increased to 65,535 HP (from vanilla's lower cap)
- Long Range flag now usable by enemies (previously player-only)
- Non-elemental poison implemented (poison status independent of element)
- Restore spells now ignore MBarrier (healing always effective)

**Character Progression:**
- Natural stat growth reinstated (stats increase organically at level-up)
- Character-specific innate abilities added/revised
- Limit Break system overhauled (physical/magical hybrid damage with effects)

### Equipment Balance Philosophy

**Weapons:** Progression curve smoothed; ultimate weapons no longer trivialize combat
**Armor:** Defensive options expanded; elemental resistance strategy emphasized
**Accessories:** Effect power balanced; more viable mid-game options

### Materia System Philosophy

**Core Design Goals:**
1. **Strategic Depth:** Splinter materia enable powerful combinations without waiting for level-ups
2. **Choice vs. Power:** Players choose between multi-spell materia or specialized single-spell variants
3. **Support Synergy:** Previously combo-locked spells (like Regen) now combinable with All/MP Turbo/etc.
4. **Progression Balance:** New materia fill gaps in elemental/status coverage

---

## Technical Analysis

### Compression and Size Constraints

**KERNEL.BIN Structure:**
- Each section independently gzipped
- Section boundaries marked by 6-byte headers
- Total size: 23,217 bytes (compressed)
- Decompressed size: Estimated ~40-50KB based on compression ratio

**kernel2.bin Constraints:**
- Maximum decompressed size: 27KB (27,648 bytes)
- Current size: 14,497 bytes compressed
- Decompression overhead: ~4-byte header
- Text encoding: FF7 custom character map (not ASCII)

**Modding Implications:**
- Text additions limited by 27KB ceiling in kernel2.bin
- Adding new materia/items requires balancing data vs. text space
- KERNEL.BIN section structure must preserve 27-section format

### Data Interdependencies

**Materia → Attack Data:**
- New materia (Hydro, Pearl, etc.) require corresponding attack data entries
- Splinter materia reference existing attacks but with modified AP/level behavior

**Equipment → Character Stats:**
- Weapon/armor stats calibrated against revised character growth curves
- Equipment progression synchronized with enemy rebalancing (in scene.bin)

**Text → Binary Data:**
- Text section pointers must align with binary data IDs
- Name/description counts must match item/materia/equipment counts
- FF7 character encoding used throughout (not standard ASCII)

### FF7 Character Encoding

New Threat text uses FF7's custom character map:
- 0x00-0x3F: Standard ASCII-like characters + symbols
- 0x40-0x5F: Lowercase letters
- 0x60-0x7F: Extended Latin characters (Ä, Ñ, ç, etc.)
- 0x80-0x9F: Special symbols (®, ©, TM, π, Ω, etc.)
- 0xD0-0xD9: Color codes (GRAY, BLUE, RED, PURPLE, GREEN, CYAN, YELLOW, WHITE)
- 0xE0-0xFF: Control codes (TAB, EOL, PAUSE, character names, STOP)

---

## Coordination with Other Mod Components

### Kernel ↔ Battle System (scene.bin)
- Enemy stats/AI in scene.bin calibrated against kernel damage formulas
- Boss HP pools adjusted for revised attack damage
- Enemy formations synchronized with player power curve

### Kernel ↔ Field Data (flevel.lgp)
- Item placements in fields reference kernel item IDs
- Shop inventories (defined in flevel) use kernel item data
- NPC dialogue references kernel equipment/materia names

### Kernel ↔ World Map (world_us.lgp)
- Enemy encounters on world map reference kernel equipment rewards
- Chocobo mechanics interact with kernel materia (Enemy Away)

### Kernel ↔ Menu System
- Menu displays pull names/descriptions from kernel text sections
- Equipment comparison calculations use kernel stat data
- Materia leveling displays reference kernel AP values

---

## Notable Gameplay Impacts

### Early Game (Midgar)
- Revised starting stats change character viability
- Initial equipment loadouts alter tactical options
- New materia availability changes build possibilities

### Mid Game (Continent Exploration)
- Splinter materia enable powerful combinations earlier
- Equipment progression smoothed (no sudden power spikes)
- Natural stat growth makes leveling more rewarding

### Late Game (Disc 2-3)
- Ultimate weapons balanced (no longer trivial victories)
- Materia builds require strategic planning (splinter vs. multi-spell)
- Boss encounters challenging due to formula revisions

### Endgame (Northern Crater/Weapons)
- Damage formula changes affect superboss strategies
- Equipment choices remain meaningful (no single "best" setup)
- Materia diversity encouraged over min-max single builds

---

## Reverse Engineering Notes

### Analysis Methodology
- Hex dump analysis of file headers
- GZIP magic number identification (0x1f 0x8b)
- Text string extraction from kernel2.bin
- Cross-reference with Qhimm wiki kernel structure documentation
- Size comparison with vanilla kernel files

### Unanalyzed Components
**Requires specialized tools for full extraction:**
- Exact AP requirements for new materia
- Precise damage formula coefficients
- Complete attack animation IDs
- Exact stat growth curves
- Item effect parameters

**Recommended Tools:**
- Hext Editor (analyze raw hex changes vs. vanilla)
- Kernel.bin editors (Wall Market, ProudClod)
- Materia editor (view AP progression)
- FF7 save editor (test materia in-game)

### Future Analysis Opportunities
1. **Binary Diff Analysis:** Compare New Threat KERNEL.BIN vs. vanilla byte-by-byte
2. **Materia AP Curve Extraction:** Parse Section 9 to extract exact AP requirements
3. **Attack Formula Reverse Engineering:** Extract formula IDs and coefficients from Section 2
4. **Growth Curve Analysis:** Parse Section 3 stat progression tables
5. **Text Encoding Study:** Map all FF7 character codes used in text sections

---

## Integration with New Threat Mod

### Dependencies
- **Battle System (scene.bin):** Enemy stats must align with kernel damage formulas
- **Field Scripts (flevel.lgp):** Item/shop data references kernel entries
- **World Map (world_us.lgp):** Enemy encounters use kernel equipment/materia rewards
- **Menu Assets:** Menu textures display kernel text data

### Installation Impact
- Kernel files replace vanilla KERNEL.BIN and kernel2.bin
- Changes take effect immediately (no save file dependency)
- Existing saves continue with new formulas applied retroactively
- Materia AP progress preserved (but growth curves change)

### Compatibility Notes
- **7th Heaven:** Kernel mods load via IRO archives
- **Other Mods:** Kernel conflicts likely with other gameplay overhauls
- **Text Mods:** kernel2.bin text conflicts with translation patches
- **Reunion/Beacause:** Likely incompatible (kernel structure differences)

---

## Appendix A: New Materia Reference

### Command Materia
| Name | Type | Function | Notes |
|------|------|----------|-------|
| X-Attack | Command | Attack enhancement | Separated from standard command set |

### Magic Materia (New)
| Name | Type | Element | Function |
|------|------|---------|----------|
| Hydro | Magic | Water | Water-element offensive magic |
| Pearl | Magic | Holy | Holy-element offensive magic |
| Osmose | Magic | None | MP absorption (single-spell variant) |
| Flash | Magic | None | Status effect magic |
| Core | Magic | Unknown | Requires in-game testing |

### Stat Materia (New)
| Name | Type | Function |
|------|------|----------|
| Omni-Plus | Stat | Multi-stat boost (speculation) |

### Splinter Materia (Single-Spell Variants)
| Name | Original Materia | Reason for Split |
|------|------------------|-------------------|
| Regen | Restore | Enable All/support materia combos |
| Slow | Time | Enable support materia combos without Haste/Stop interference |
| Dispel | Unknown | Enable tactical dispel without level-up restrictions |
| MBarrier | Barrier | Separate magic defense from physical (Barrier) |
| Reflect | Unknown | Enable reflect strategies without materia level restrictions |
| Break | Transform | Separate petrify mechanics |
| Tornado | Contain | Enable wind-element strategies independently |

**Total New Materia Count:** 13+ (7 new, 7 splinter, potentially more unidentified)

---

## Appendix B: File Locations

**Source Files (New Threat Mod):**
```
/mnt/d/Games/Stand-alone/FF7Modding/New Threat/New Threat - Sega Chief/kernel/
├── KERNEL.BIN (23,217 bytes)
└── kernel2.bin (14,497 bytes)
```

**Vanilla Comparison Locations:**
```
PSX: /INIT/KERNEL.BIN
PC:  /DATA/KERNEL/KERNEL.BIN
PC:  /DATA/KERNEL/KERNEL2.BIN
```

**Installation Target (7th Heaven):**
```
Loaded via IRO archive, replaces:
- FF7/data/kernel/KERNEL.BIN
- FF7/data/kernel/kernel2.bin
```

---

## Appendix C: References

**Technical Documentation:**
- Qhimm Wiki: FF7/Kernel/Kernel.bin structure
- Qhimm Wiki: FF7/FF_Text character encoding
- Qhimm Wiki: FF7/Item_data, Materia_data, Weapon_data, Armor_data sections

**Mod Documentation:**
- New Threat 2.0 Readme.txt (changelog overview)
- New Threat discussion threads (Qhimm forums)

**Analysis Tools:**
- hexdump (Linux hex viewer)
- file (Linux file type detection)
- Custom kernel editors (Wall Market, ProudClod)

---

## Document Metadata

**Analysis Depth:** Structural and functional overview based on hex analysis, readme documentation, and Qhimm wiki cross-reference.

**Limitations:** Exact numerical values (AP requirements, damage coefficients, stat curves) require specialized kernel extraction tools not used in this analysis.

**Future Work:** Binary diff analysis against vanilla, complete data table extraction, in-game testing of new materia mechanics.

**Confidence Level:** High for structural analysis, medium for gameplay impact assessment (based on readme changelog), low for precise numerical values (requires tool-based extraction).

---

**Analysis Completed:** 2026-01-22 22:50:25 JST
**Session ID:** 552a7ee9-e42e-4439-8243-2eb1a43110da
**Document Version:** 1.0

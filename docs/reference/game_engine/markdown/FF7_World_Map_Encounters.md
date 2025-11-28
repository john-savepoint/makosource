# FF7 World Map Encounters

**Category**: World Map System Documentation
**Created**: 2025-11-28 22:20 JST (Friday)
**Last Modified**: 2025-11-28 22:20 JST
**Status**: Initial extraction from major section

This file documents the FF7 world map encounter system, including the binary format for storing encounter data and how encounters are organized by geographic area.

---

## Overview

The world map encounter system defines which battles can occur in different areas of the game world. Encounters vary based on the terrain type (grass, forest, desert, beach, etc.) and the specific geographic region the player is in.

### Related Files

- **enc_w.bin**: Binary file containing all world map encounter data (PC version)
- **wm0.ev, wm2.ev, wm3.ev**: Event/script files for world map regions (file locations not conclusively verified)
- **wm0.map, wm2.map, wm3.map**: MAP files defining mesh geometry (see FF7_WorldMap_Module.md)
- **wm0.bsz, wm2.bsz, wm3.bsz**: BSZ model files (see FF7_World_Map_BSZ.md)
- **wm0.txz, wm2.txz, wm3.txz**: Texture and script archive files (see FF7_World_Map_TXZ.md)

---

## Encounter Data Format (PC Version)

### File Structure

Encounter data for the World Map is stored in **enc_w.bin** with the following structure:

- **Start Offset**: 0xB8 (184 decimal)
- **Section Size**: 32 bytes per section
- **Number of Sections**: One section per area/terrain variant combination

### Section Structure

Each 32-byte section is defined as follows:

```
Offset | Size   | Description
-------|--------|-----------------------------------------------
0x00   | 1 byte | Always 01 (unknown purpose)
0x01   | 1 byte | Encounter Rate (lower numbers = higher frequency)
0x02-0x0D | 12 bytes | Normal Battle formations (6 records × 2 bytes)
0x0E-0x15 | 8 bytes  | Special Formation Battles (4 records × 2 bytes)
0x16-0x1F | 10 bytes | Chocobo Battles (5 records × 2 bytes)
```

### Field Details

#### Encounter Rate (Offset 0x01)
- **Format**: 1 unsigned byte
- **Meaning**: Lower values indicate higher encounter frequencies
- **Note**: The exact formula for encounter chance is not yet fully documented [UNVERIFIED]
- **Observation**: In the normal battle section, the chance bytes typically sum to 64

#### Normal Battle Formations (Offset 0x02-0x0D)
- **Count**: 6 battle records
- **Record Format**: 2 bytes per record
  - **Byte 1**: Formation ID (enemy group identifier)
  - **Byte 2**: Encounter Chance (probability weight)
- **Note**: Chance values should sum to 64
- **Observation**: Follow the same structure as field encounter data

#### Special Formation Battles (Offset 0x0E-0x15)
- **Count**: 4 battle records
- **Record Format**: 2 bytes per record (same as normal battles)
- **Purpose**: Rare or boss-type encounters specific to an area
- **Note**: Chance mechanics may differ from normal battles [UNVERIFIED]

#### Chocobo Battles (Offset 0x16-0x1F)
- **Count**: 5 battle records
- **Record Format**: 2 bytes per record (same as normal battles)
- **Purpose**: Encounters that occur only while riding a Chocobo
- **Note**: These are separate from player-initiated Chocobo encounters

---

## Area Organization

The world map is divided into **14 geographic areas**, each with up to **4 terrain variants**. This organization determines which encounter section is used for a given location.

### Area Enumeration

Each area in the game has four fields organized by terrain type:

```
1. Area - Grass
2. Area - Dirt/Snow
3. Area - Forest/Desert
4. Area - Beach
```

These are aligned in this order:

### Area List

The 14 areas are enumerated as follows (in order as they appear in enc_w.bin):

1. **Midgar Area**
2. **Kalm Area**
3. **Junon Area**
4. **Corel Area**
5. **Gold Saucer Area**
6. **Gongaga Area**
7. **Cosmo Area**
8. **Nibel Area**
9. **Rocket Area**
10. **Wutai Area**
11. **Woodlands Area**
12. **Icicle Area** - Note: Forest variant is unclear (this area may have no random encounters in forests)
13. **Mideel Area**
14. **North Corel Area** - Materia Cave north of Corel (uncertain designation)
15. **Cactus Island**
16. **Goblin Island** - Note: Lacks a full empty Beach encounter list

### Offset Calculation

To locate a specific area's encounter data:

1. Determine the area number (0-indexed, so Midgar = 0)
2. Determine the terrain variant (0-3, where 0 = Grass, 1 = Dirt/Snow, 2 = Forest/Desert, 3 = Beach)
3. Calculate section index: `area_number * 4 + terrain_variant`
4. Calculate byte offset: `0xB8 + (section_index * 32)`

**Example**: Encounters for Kalm Area grass terrain (area 1, terrain 0):
- Section index: `1 * 4 + 0 = 4`
- Byte offset: `0xB8 + (4 * 32) = 0x158` (344 decimal)

### Special Cases

#### Icicle Area Forest Variant
- Documentation states uncertainty about whether forests in this area have encounters
- Original FF7 Icicle Area forests may have no random battles
- Marked as unverified in original research

#### Goblin Island Beach Variant
- Does not have a complete Beach encounter list
- May require special handling when parsing

#### Area Replacement Mechanics
- Some areas can be "replaced" (e.g., Ultima Weapon crater replaces Temple of the Ancients)
- Encounter mechanics for replacement areas may require special handling [UNVERIFIED]

---

## Notes and Unverified Information

### What Is Known
- ✓ enc_w.bin file location
- ✓ Basic section structure (32 bytes)
- ✓ Area enumeration and layout
- ✓ Byte offset mappings
- ✓ Record format for normal and special battles

### What Is Uncertain [UNVERIFIED]
- ? Exact encounter rate probability calculation
- ? Whether event files (wm0.ev, wm2.ev, wm3.ev) match expected structure
- ? Whether special formations follow identical chance mechanics
- ? How area replacement affects encounter data
- ? Whether Icicle Area forests have encounters
- ? Complete behavior of Goblin Island beach encounters
- ? Whether Chocobo encounters stack/combine with area encounters

### Research Status
This documentation is based on research notes and reverse-engineering of the original FF7 PC executable. Some aspects remain unverified due to:
- Limited conclusive proof from testing [brief glance through source]
- Undocumented game engine behaviors
- Potential differences between PSX and PC versions

---

## Cross-References

### Related World Map Documentation
- **FF7_WorldMap_Module.md**: MAP/BOT format and mesh geometry
- **FF7_World_Map_BSZ.md**: Character/vehicle model files
- **FF7_World_Map_TXZ.md**: Texture and sound data
- **FF7_WorldMap_Module_Script.md**: Script engine and event handling

### Related Encounter Systems
- **Field Encounters** (Field Module): Different format but similar concept
- **Battle Formation Data**: Documented in KERNEL.BIN
- **Monster/Enemy Data**: Also in KERNEL.BIN

---

**Version**: 1.0.0
**Last Updated**: 2025-11-28 22:20 JST

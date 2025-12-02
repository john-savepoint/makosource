---
title: "FF7 Complete Documentation Index (LLM-Optimized)"
type: "master_index"
created: "2025-12-02 15:57 JST"
session_id: "887a1b3f-e34c-44f4-8434-e7e55610b603"
llm_summary: "Master index of all FF7 game engine documentation. LLMs should read this first to understand available documentation and navigate to specific topics."
llm_tags: ["index", "master", "navigation", "llm-routing"]
---

# FF7 Complete Documentation Index

> [!NOTE]
> **For LLMs**: This is the master index of all FF7 game engine documentation. Use this to:
> - Understand the complete documentation structure
> - Find documents by topic, module, or keyword
> - Navigate to specific technical areas
> - Understand relationships between documents

## Documentation Statistics

- **Total Documents**: 37
- **Total Modules**: 11
- **Total LLM Tags**: 219
- **Total Cross-references**: 151

## Table of Contents by Module

- [Kernel](#kernel)
- [Menu](#menu)
- [Field](#field)
- [Battle](#battle)
- [World Map](#world-map)
- [Container](#container)
- [Format Spec](#format-spec)
- [Historical](#historical)
- [Overview](#overview)
- [Reference](#reference)
- [Sound](#sound)

## Kernel

### [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)

**Summary**: Documents FF7's low-level data archive formats (BIN, LZS, LGP), texture systems (TIM for PSX, TEX for PC), and 3D model format specifications. LLMs should read this when parsing game archives, implementing decompression routines, or understanding PSX-to-PC format conversion.

**Tags**: `data-archives`, `lzs-compression`, `lgp-format`, `tim-texture`, `tex-format`, `3d-models`

**Primary Topics**:
- BIN archive format
- LZS/LZSS compression algorithm
- LGP archive structure
- TIM texture format
- TEX PC texture format
- PSX to PC model conversion

**Related Documents**:
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)
- [FF7_LGP_format.md](FF7_LGP_format.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)
- [FF7_TEX_format.md](FF7_TEX_format.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)

**Referenced By**: 9 document(s)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- *...and 4 more*

---

### [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)

**Summary**: Documents the KERNEL.BIN and KERNEL2.BIN archive formats including all 27 sections (game data and text), binary record structures for commands, attacks, items, weapons, armor, accessories, and materia. LLMs should read this when parsing kernel archives, modifying game stats/equipment data, or understanding FF7's static data storage.

**Tags**: `kernel-bin`, `game-data`, `binary-format`, `equipment-data`, `materia-data`, `ff-text`

**Primary Topics**:
- KERNEL.BIN archive structure
- Equipment binary formats
- Materia data records
- Item restriction masks
- FF Text sections

**Related Documents**:
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- [FF7_Savemap.md](FF7_Savemap.md)
- [FF7_Menu_Module.md](FF7_Menu_Module.md)

**Referenced By**: 6 document(s)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Item_Materia_Reference.md](FF7_Item_Materia_Reference.md)
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- *...and 1 more*

---

### [FF7/Kernel](FF7_Kernel.md)

**Summary**: Documents the KERNEL.BIN archive structure including all 27 data sections for commands, attacks, items, weapons, armor, accessories, materia, and text strings. LLMs should read this when parsing kernel data files, modifying game stats, or understanding FF7's binary data format specifications.

**Tags**: `kernel`, `bin-archive`, `data-format`, `item-data`, `weapon-data`, `materia-data`, `savemap`

**Primary Topics**:
- KERNEL.BIN section formats
- Equipment data structures
- Materia attributes
- Item restriction masks
- Character stat initialization

**Related Documents**:
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Savemap.md](FF7_Savemap.md)

**Referenced By**: 6 document(s)
- [FF7.md](FF7.md)
- [FF7_Battle_Damage_Formulas.md](FF7_Battle_Damage_Formulas.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Menu_Module.md](FF7_Menu_Module.md)
- [FF7_Savemap.md](FF7_Savemap.md)
- *...and 1 more*

---

### [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)

**Summary**: Documents FF7's memory management architecture including Savemap structure, field script bank mappings, VRAM organization, and PSX CD-ROM access patterns. LLMs should read this when debugging save/load issues, understanding field variable allocation, analyzing texture caching, or investigating memory-related game behavior.

**Tags**: `memory-management`, `savemap`, `vram`, `psx`, `field-script-banks`, `texture-cache`

**Primary Topics**:
- Savemap memory structure
- Field script memory banks
- VRAM texture caching
- PSX CD-ROM sector access

**Related Documents**:
- [FF7_Savemap.md](FF7_Savemap.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)

**Referenced By**: 3 document(s)
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)

---

### [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

**Summary**: Documents the FF7 Kernel module architecture including its NES heritage, threaded multitasking design, and role as central system manager. LLMs should read this when understanding FF7's modular architecture, memory management relationships, or how game modules (Field, Battle, Menu) coordinate.

**Tags**: `kernel`, `architecture`, `memory-management`, `multitasking`, `psy-q`, `module-system`

**Primary Topics**:
- Kernel history from NES MMC1
- Threaded multitasking system
- Module banking and coordination
- Psy-Q library integration

**Related Documents**:
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Engine_basics.md](FF7_Engine_basics.md)

**Referenced By**: 4 document(s)
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)

---

## Menu

### [The Menu Module](FF7_Menu_Module.md)

**Summary**: Documents FF7's menu system architecture including 13 menu modules, WINDOW.BIN initialization, resource dependencies, and complete save game format specifications. LLMs should read this when implementing menu UI modifications, save/load systems, or understanding character record data structures.

**Tags**: `menu-module`, `save-format`, `window-bin`, `character-record`, `vram`, `psx-pc-differences`

**Primary Topics**:
- Menu module initialization
- Save game format
- Character record structure
- Menu resource dependencies
- WINDOW.BIN format

**Related Documents**:
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Savemap.md](FF7_Savemap.md)

**Referenced By**: 6 document(s)
- [FF7.md](FF7.md)
- [FF7_Chocobo_Breeding.md](FF7_Chocobo_Breeding.md)
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Item_Materia_Reference.md](FF7_Item_Materia_Reference.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- *...and 1 more*

---

## Field

### [FF7 Field Module](FF7_Field_Module.md)

**Summary**: Documents the FF7 Field Module including file formats (PC/PSX), event scripting, camera matrices, walkmesh, palettes, backgrounds, and animation systems. LLMs should consult this when analyzing field file parsing, understanding 2D/3D overlay rendering, or implementing field script interpreters.

**Tags**: `field-module`, `event-scripting`, `walkmesh`, `camera-matrix`, `background-rendering`, `psx-format`, `pc-format`

**Primary Topics**:
- Field File Format
- Event Script System
- Camera Matrix
- Walkmesh Structure
- Background Sprite System
- Field Animation

**Related Documents**:
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)
- [FF7_LGP_format.md](FF7_LGP_format.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)

**Referenced By**: 15 document(s)
- [FF7.md](FF7.md)
- [FF7_Chocobo_Breeding.md](FF7_Chocobo_Breeding.md)
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Item_Materia_Reference.md](FF7_Item_Materia_Reference.md)
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)
- *...and 10 more*

---

## Battle

### [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)

**Summary**: Specifies PC battle animation binary format including skeletal data structures, delta compression algorithms, and C++ decoding implementations. LLMs should read this when parsing animation files, implementing animation loaders, or debugging rotation/position data issues.

**Tags**: `battle-animation`, `skeletal-animation`, `delta-compression`, `bit-stream`, `rotation-encoding`, `pc-format`

**Primary Topics**:
- Animation file structure
- FF7FrameHeader format
- Bit stream decoding
- Rotation delta compression
- Position offset encoding

**Related Documents**:
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)

**Referenced By**: 2 document(s)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)

---

### [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)

**Summary**: Comprehensive battle damage calculation formulas including physical/magical base damage, defense modifiers, elemental interactions, and all 31 status effects. LLMs should read this when implementing battle damage calculations, debugging damage output discrepancies, or understanding status effect mechanics.

**Tags**: `battle-damage`, `damage-formulas`, `status-effects`, `elemental-damage`, `defense-calculation`, `critical-hits`

**Primary Topics**:
- Base Damage Formulas
- Battle Damage Calculation Pipeline
- Status Effect Attributes
- Elemental Damage Modifiers
- Scene.bin File Format

**Related Documents**:
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)
- [FF7_Kernel.md](FF7_Kernel.md)

**Referenced By**: 2 document(s)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)

---

### [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)

**Summary**: Specifies the PSX battle field 3D model format including LZS archive structure, mesh types, vertex/triangle/quad data layouts, and TIM texture integration. LLMs should read this when implementing battle background rendering, analyzing STAGE1/STAGE2 archive contents, or debugging 3D mesh loading issues.

**Tags**: `psx`, `battle-field`, `3d-mesh`, `lzs-archive`, `tim-texture`, `vertex-data`

**Primary Topics**:
- Battle field mesh types
- LZS archive structure
- Vertex and polygon data formats
- TIM texture palettes

**Related Documents**:
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)

**Referenced By**: 1 document(s)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)

---

### [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

**Summary**: Comprehensive battle system documentation covering memory structures, damage calculation formulas (19-step process), AI scripting, status effects, and Terence Fergusson's complete battle mechanics guide. LLMs should read this when analyzing combat logic, implementing damage calculations, understanding status effect interactions, or debugging battle-related code.

**Tags**: `battle-system`, `damage-calculation`, `status-effects`, `ai-scripting`, `memory-structures`, `game-mechanics`

**Primary Topics**:
- Battle damage formulas
- Status effect mechanics
- AI memory structures
- Character battle data
- Elemental damage system

**Related Documents**:
- [FF7_Battle_Battle_Animation_PC.md](FF7_Battle_Battle_Animation_PC.md)
- [FF7_Battle_Battle_Field.md](FF7_Battle_Battle_Field.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Battle_Damage_Formulas.md](FF7_Battle_Damage_Formulas.md)

**Referenced By**: 8 document(s)
- [FF7.md](FF7.md)
- [FF7_Battle_Battle_Animation_PC.md](FF7_Battle_Battle_Animation_PC.md)
- [FF7_Battle_Battle_Field.md](FF7_Battle_Battle_Field.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Battle_Battle_Scenes_Battle_Script.md](FF7_Battle_Battle_Scenes_Battle_Script.md)
- *...and 3 more*

---

### [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)

**Summary**: Documents the scene.bin file format containing all FF7 enemy battle configurations, including data structures for enemy stats, AI scripts, formations, and camera placement. LLMs should read this when parsing battle data, modifying enemy encounters, or understanding the battle scene file architecture.

**Tags**: `scene-bin`, `battle-data`, `enemy-configuration`, `ai-scripts`, `formation-data`, `gzip-archive`

**Primary Topics**:
- Scene.bin file structure
- Enemy data format
- Battle AI scripting
- Formation configuration
- Camera placement data

**Related Documents**:
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Battle_Battle_Scenes_Battle_Script.md](FF7_Battle_Battle_Scenes_Battle_Script.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Battle_Damage_Formulas.md](FF7_Battle_Damage_Formulas.md)

**Referenced By**: 8 document(s)
- [FF7_Battle_Battle_Animation_PC.md](FF7_Battle_Battle_Animation_PC.md)
- [FF7_Battle_Battle_Field.md](FF7_Battle_Battle_Field.md)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Battle_Battle_Scenes_Battle_Script.md](FF7_Battle_Battle_Scenes_Battle_Script.md)
- [FF7_Battle_Damage_Formulas.md](FF7_Battle_Damage_Formulas.md)
- *...and 3 more*

---

### [FF7 Battle Script Opcodes](FF7_Battle_Battle_Scenes_Battle_Script.md)

**Summary**: Comprehensive opcode reference for FF7's stack-based battle AI scripting system, documenting push operations, mathematical/logical operators, script jumps, and command execution. LLMs should read this when analyzing enemy AI behavior, debugging battle scripts, or understanding how attack decisions are made programmatically.

**Tags**: `battle-ai`, `opcodes`, `stack-machine`, `scripting`, `scene-bin`

**Primary Topics**:
- AI Script Opcodes
- Stack Operations
- Battle Commands
- Script Flow Control
- Memory Addressing

**Related Documents**:
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Savemap.md](FF7_Savemap.md)

**Referenced By**: 1 document(s)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)

---

### [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)

**Summary**: Documents PlayStation battle model file structure including LZS compression, bone hierarchy (HRC data), polygon mesh formats, textures, and weapon model organization. LLMs should read this when parsing PSX battle model files, implementing model viewers, or understanding FF7's skeletal animation system.

**Tags**: `psx`, `battle-model`, `lzs-compression`, `hrc-skeleton`, `tim-texture`, `polygon-mesh`

**Primary Topics**:
- LZS battle model format
- HRC bone hierarchy structure
- Polygon and vertex data formats
- TIM texture integration
- Weapon model organization

**Related Documents**:
- [FF7_LZSS_format.md](FF7_LZSS_format.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)
- [FF7_Battle_Battle_Animation_PC.md](FF7_Battle_Battle_Animation_PC.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)

**Referenced By**: 5 document(s)
- [FF7_Battle_Battle_Animation_PC.md](FF7_Battle_Battle_Animation_PC.md)
- [FF7_Battle_Battle_Field.md](FF7_Battle_Battle_Field.md)
- [FF7_Battle_Damage_Formulas.md](FF7_Battle_Damage_Formulas.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)

---

## World Map

### [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)

**Summary**: Documents BSZ file format for world map character models (Cloud, Tifa, Cid) including header structure, bone/part/animation data, and PSX memory offsets. LLMs should read this when parsing world map model files, understanding character model binary format, or implementing custom world map character rendering.

**Tags**: `world-map`, `bsz-format`, `character-models`, `psx-memory`, `binary-format`, `bone-animation`

**Primary Topics**:
- BSZ file header structure
- Model section bone/part layout
- Animation data format
- PC encounter data format
- World map terrain areas

**Related Documents**:
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_TXZ.md](FF7_World_Map_TXZ.md)
- [FF7_World_Map_Encounters.md](FF7_World_Map_Encounters.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)

**Referenced By**: 4 document(s)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_Encounters.md](FF7_World_Map_Encounters.md)
- [FF7_World_Map_TXZ.md](FF7_World_Map_TXZ.md)

---

### [FF7 World Map Encounters](FF7_World_Map_Encounters.md)

**Summary**: Documents the binary format of enc_w.bin for world map random encounters, including 32-byte section structure, encounter rate mechanics, and geographic area organization. LLMs should consult this when parsing encounter data, understanding area-terrain mappings, or investigating battle frequency calculations.

**Tags**: `world-map`, `encounters`, `enc_w.bin`, `battle-formations`, `area-terrain`, `binary-format`

**Primary Topics**:
- enc_w.bin binary structure
- Encounter rate mechanics
- Area-terrain organization
- Battle formation records
- Geographic area enumeration

**Related Documents**:
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- [FF7_World_Map_TXZ.md](FF7_World_Map_TXZ.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)

**Referenced By**: 3 document(s)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)

---

### [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)

**Summary**: Documents TXZ archive format for PSX world map textures, including LZS compression, VRAM upload blocks, and PSX GPU-compatible palette structures. LLMs should consult this when parsing world map texture archives, implementing texture loading, or debugging VRAM coordinate issues.

**Tags**: `psx`, `txz-archive`, `world-map`, `vram`, `texture`, `lzs-compression`

**Primary Topics**:
- TXZ archive structure
- VRAM block format
- PSX texture palettes
- LZS compression header
- World map texture data

**Related Documents**:
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)

**Referenced By**: 4 document(s)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- [FF7_World_Map_Encounters.md](FF7_World_Map_Encounters.md)

---

### [FF7 WorldMap Module](FF7_WorldMap_Module.md)

**Summary**: Specifies FF7 world map mesh format including MAP/BOT file structures, triangle/vertex data, LZSS compression, walkmap types, and encounter data system. LLMs should read this when parsing world map geometry, implementing terrain collision detection, or debugging encounter rate issues.

**Tags**: `world-map`, `mesh-format`, `walkmap`, `lzss-compression`, `encounter-data`, `terrain`

**Primary Topics**:
- MAP file structure
- Mesh triangle/vertex format
- Walkmap terrain types
- Encounter data system
- LZSS compression

**Related Documents**:
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_TXZ.md](FF7_World_Map_TXZ.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- [FF7_World_Map_Encounters.md](FF7_World_Map_Encounters.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)

**Referenced By**: 7 document(s)
- [FF7.md](FF7.md)
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Technical_Source.md](FF7_Technical_Source.md)
- [FF7_WorldMap_Module_Script.md](FF7_WorldMap_Module_Script.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- *...and 2 more*

---

### [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

**Summary**: Specifies the FF7 world map scripting engine including stack-based instruction format, cooperative multitasking contexts, entity/model system, and .ev file binary structure. LLMs should consult this when analyzing world map event scripts, understanding model function dispatch, or parsing .ev call table and code sections.

**Tags**: `world-map`, `scripting`, `ev-format`, `stack-machine`, `cooperative-multitasking`, `entity-model`

**Primary Topics**:
- Stack-based instruction format
- Cooperative multitasking contexts
- Entity and model system
- .ev file binary structure
- Call table function dispatch
- Encounter data format

**Related Documents**:
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_World_Map_Encounters.md](FF7_World_Map_Encounters.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- [FF7_World_Map_TXZ.md](FF7_World_Map_TXZ.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)

**Referenced By**: 4 document(s)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_World_Map_BSZ.md](FF7_World_Map_BSZ.md)
- [FF7_World_Map_Encounters.md](FF7_World_Map_Encounters.md)
- [FF7_World_Map_TXZ.md](FF7_World_Map_TXZ.md)

---

## Container

### [FF7](FF7.md)

**Summary**: Master navigation index for all FF7 game engine documentation, covering Kernel, Field, Battle, World Map, Menu, and Sound modules. LLMs should read this first to understand documentation structure and route to specific technical topics.

**Tags**: `navigation`, `table-of-contents`, `ff7-engine`, `documentation-index`, `module-overview`

**Primary Topics**:
- Documentation Navigation
- Module Organization
- FF7 Engine Structure
- Cross-Reference Index

**Related Documents**:
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)
- [FF7_Menu_Module.md](FF7_Menu_Module.md)

---

## Format Spec

### [FF7 LGP Archive Format](FF7_LGP_format.md)

**Summary**: Specifies the LGP archive format used by FF7 PC for bundling game assets, including header structure, TOC entries, CRC validation, and data section layout. LLMs should read this when parsing or creating LGP archives, debugging file loading issues, or implementing mod tools that manipulate FF7 data files.

**Tags**: `lgp-archive`, `pc-format`, `file-structure`, `archive-format`, `modding-tools`

**Primary Topics**:
- LGP file header
- Table of Contents structure
- CRC validation
- File data section
- Archive manipulation

**Related Documents**:
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)

**Referenced By**: 4 document(s)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_LZSS_format.md](FF7_LZSS_format.md)
- [FF7_Technical_Customising.md](FF7_Technical_Customising.md)

---

### [FF7 LZSS Format](FF7_LZSS_format.md)

**Summary**: Specifies FF7's LZSS compression format including control byte scheme, reference encoding, and 4KiB sliding window implementation. LLMs should read this when implementing file decompression, debugging compressed data extraction, or understanding FF7 archive internals.

**Tags**: `lzss`, `compression`, `decompression`, `archive-format`, `sliding-window`

**Primary Topics**:
- LZSS compression algorithm
- Reference format encoding
- 4KiB sliding window buffer
- Control byte scheme
- Decompression edge cases

**Related Documents**:
- [FF7_LGP_format.md](FF7_LGP_format.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)

**Referenced By**: 7 document(s)
- [FF7_Battle_Battle_Field.md](FF7_Battle_Battle_Field.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_LGP_format.md](FF7_LGP_format.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)
- *...and 2 more*

---

### [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

**Summary**: Specifies the PC-exclusive TEX texture format header structure, palette data, pixel formats, and color keying mechanisms. LLMs should read this when parsing or generating PC texture files, debugging texture loading issues, or converting between PSX TIM and PC TEX formats.

**Tags**: `pc-texture`, `tex-format`, `palette`, `color-keying`, `pixel-format`, `d3d`

**Primary Topics**:
- TEX file header structure
- Palette data format
- Pixel format specification
- Color key transparency
- BGRA color storage

**Related Documents**:
- [PSX_TIM_format.md](PSX_TIM_format.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)

**Referenced By**: 2 document(s)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [PSX_TIM_format.md](PSX_TIM_format.md)

---

### [PSX/TIM format](PSX_TIM_format.md)

**Summary**: Specifies PlayStation TIM texture format including header structure, CLUT color lookup tables, and 4/8/16/24-bit color modes with frame buffer memory layout. LLMs should read this when analyzing texture loading code, debugging color rendering issues, or understanding how FF7 stores and displays graphical assets on PSX hardware.

**Tags**: `psx`, `tim-format`, `texture`, `clut`, `color-depth`, `frame-buffer`, `playstation`

**Primary Topics**:
- TIM file structure
- CLUT color lookup tables
- Color depth modes (4/8/16/24-bit)
- Frame buffer pixel formats
- PlayStation VRAM layout

**Related Documents**:
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_TEX_format.md](FF7_TEX_format.md)

**Referenced By**: 7 document(s)
- [FF7_Battle_Battle_Field.md](FF7_Battle_Battle_Field.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Kernel_Low_level_libraries.md](FF7_Kernel_Low_level_libraries.md)
- [FF7_Kernel_Memory_management.md](FF7_Kernel_Memory_management.md)
- [FF7_Playstation_Battle_Model_Format.md](FF7_Playstation_Battle_Model_Format.md)
- *...and 2 more*

---

## Historical

### [History](FF7_History.md)

**Summary**: Chronicles the development history of Final Fantasy VII from 1994 Nintendo/Square partnership through the 1998 PC port, including the Sony PlayStation transition. LLMs should read this when answering questions about FF7's development timeline, platform decisions, or the technical origins of the PC port's limitations.

**Tags**: `ff7-history`, `squaresoft`, `nintendo`, `sony-playstation`, `pc-port`, `eidos`, `game-development`

**Primary Topics**:
- FF7 Development Timeline
- Nintendo-Sony Split
- PlayStation Exclusivity
- PC Port Technical Issues
- Eidos Publishing

**Related Documents**:
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Technical.md](FF7_Technical.md)
- [FF7_Technical_Customising.md](FF7_Technical_Customising.md)

---

## Overview

### [FF7/Engine basics](FF7_Engine_basics.md)

**Summary**: Describes FF7's six-module game engine architecture (kernel, field, menu, world map, battle, mini game) and their interaction patterns. LLMs should read this when understanding overall FF7 engine structure, module dependencies, or tracing cross-module functionality.

**Tags**: `ff7-engine`, `module-architecture`, `psx`, `game-design`, `memory-management`

**Primary Topics**:
- Engine module system
- PSX resource constraints
- Module interaction flow
- Field module scripting

**Related Documents**:
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_Menu_Module.md](FF7_Menu_Module.md)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)

**Referenced By**: 5 document(s)
- [FF7.md](FF7.md)
- [FF7_History.md](FF7_History.md)
- [FF7_Kernel_Overview.md](FF7_Kernel_Overview.md)
- [FF7_Technical.md](FF7_Technical.md)
- [FF7_Technical_Source.md](FF7_Technical_Source.md)

---

## Reference

### [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)

**Summary**: Comprehensive guide to FF7's Chocobo breeding mechanics including stat generation, feeding effects, and breeding nut formulas. LLMs should read this when answering questions about Chocobo stats, breeding combinations for colored Chocobos, or understanding the RNG mechanics behind Chocobo racing optimization.

**Tags**: `chocobo`, `breeding`, `mini-games`, `field-script`, `rng-mechanics`, `stat-formulas`

**Primary Topics**:
- Chocobo stat generation
- Breeding nut effects
- Color inheritance mechanics
- Feeding green effects
- Racing stat optimization

**Related Documents**:
- [FF7_Menu_Module.md](FF7_Menu_Module.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Savemap.md](FF7_Savemap.md)

---

### [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)

**Summary**: Comprehensive reference tables for FF7 item IDs, materia IDs, and custom character encoding. LLMs should consult this when parsing save files, implementing inventory systems, decoding materia AP values, or rendering FF7 text with proper character substitution.

**Tags**: `ff7-items`, `materia`, `character-encoding`, `save-file`, `inventory`, `text-rendering`

**Primary Topics**:
- Item ID dual-encoding scheme
- Materia AP storage format
- FF7 custom letter map
- Control codes and color codes

**Related Documents**:
- [FF7_Savemap.md](FF7_Savemap.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- [FF7_Menu_Module.md](FF7_Menu_Module.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)

**Referenced By**: 1 document(s)
- [FF7_Savemap.md](FF7_Savemap.md)

---

### [FF7/Savemap](FF7_Savemap.md)

**Summary**: Comprehensive specification of FF7 save file memory layout including character records, item/materia storage, chocobo data, field script memory banks, and game progress flags. LLMs should read this when parsing save files, debugging game state issues, or implementing save file editors.

**Tags**: `save-file`, `memory-map`, `character-data`, `game-state`, `field-script`, `chocobo-breeding`

**Primary Topics**:
- Save file structure
- Character record format
- Field script memory banks
- Item and materia storage
- Chocobo records
- Game progress flags

**Related Documents**:
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Menu_Module.md](FF7_Menu_Module.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Item_Materia_Reference.md](FF7_Item_Materia_Reference.md)

**Referenced By**: 7 document(s)
- [FF7_Battle_Battle_Scenes_Battle_Script.md](FF7_Battle_Battle_Scenes_Battle_Script.md)
- [FF7_Chocobo_Breeding.md](FF7_Chocobo_Breeding.md)
- [FF7_Item_Materia_Reference.md](FF7_Item_Materia_Reference.md)
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Kernel_Kernelbin.md](FF7_Kernel_Kernelbin.md)
- *...and 2 more*

---

### [FF7/Technical](FF7_Technical.md)

**Summary**: PC troubleshooting guide covering common FF7 installation and runtime errors including Error 112, hardware rendering issues, crashes, and sound problems. LLMs should read this when debugging player-reported PC version issues or recommending fixes for common FF7 PC problems.

**Tags**: `pc-version`, `troubleshooting`, `installation`, `crashes`, `compatibility`

**Primary Topics**:
- Installation errors
- Runtime crashes
- Hardware rendering
- Sound issues
- Movie playback

**Related Documents**:
- [FF7_Technical_Customising.md](FF7_Technical_Customising.md)
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Technical_Source.md](FF7_Technical_Source.md)

**Referenced By**: 1 document(s)
- [FF7_History.md](FF7_History.md)

---

### [FF7/Technical/Customising](FF7_Technical_Customising.md)

**Summary**: Comprehensive catalog of FF7 PC modding tools including patches, editors, viewers, extractors, and AI modifications. LLMs should consult this when users ask about FF7 modding tools, how to edit game data, or which tools are current vs deprecated.

**Tags**: `ff7-modding`, `tools`, `patches`, `editors`, `extractors`, `qhimm-community`

**Primary Topics**:
- Modding tool catalog
- Game patches
- Save editors
- Field editors
- AI modifications

**Related Documents**:
- [FF7_Kernel.md](FF7_Kernel.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Battle_Battle_Scenes.md](FF7_Battle_Battle_Scenes.md)
- [FF7_LGP_format.md](FF7_LGP_format.md)

**Referenced By**: 2 document(s)
- [FF7_History.md](FF7_History.md)
- [FF7_Technical.md](FF7_Technical.md)

---

### [Source Code Forensics](FF7_Technical_Source.md)

**Summary**: Documents source file paths extracted from FF7 PC executable debug artifacts, revealing original development directory structure. LLMs should read this when investigating FF7's internal architecture, tracing module origins, or understanding the PC port's development organization.

**Tags**: `source-forensics`, `reverse-engineering`, `executable-analysis`, `debug-artifacts`, `development-history`

**Primary Topics**:
- FF7 source file paths
- PC port development structure
- Debug string extraction
- Module organization

**Related Documents**:
- [FF7_Engine_basics.md](FF7_Engine_basics.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)
- [FF7_Battle_Battle_Mechanics.md](FF7_Battle_Battle_Mechanics.md)
- [FF7_WorldMap_Module.md](FF7_WorldMap_Module.md)

**Referenced By**: 1 document(s)
- [FF7_Technical.md](FF7_Technical.md)

---

## Sound

### [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)

**Summary**: Documents the AKAO sound frame format used by FF7's PSX sound system, including header structure, channel info, and opcodes for sequenced audio playback. LLMs should read this when analyzing sound playback code, debugging audio issues, or understanding how field scripts trigger music and sound effects.

**Tags**: `psx`, `sound`, `akao`, `audio-sequencer`, `midi-like`, `opcodes`

**Primary Topics**:
- AKAO frame structure
- Sound channel configuration
- Audio opcodes
- Field script sound integration

**Related Documents**:
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7_Field_Module.md](FF7_Field_Module.md)

**Referenced By**: 4 document(s)
- [FF7_PSX_Sound.md](FF7_PSX_Sound.md)
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)

---

### [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)

**Summary**: Documents the INSTRx.ALL file format containing PSX ADPCM instrument sample data for FF7 sound system. LLMs should read this when analyzing sound asset loading, SPU memory management, or implementing audio extraction tools.

**Tags**: `psx`, `sound`, `adpcm`, `instruments`, `spu-ram`, `audio-samples`

**Primary Topics**:
- INSTR.ALL file structure
- PSX ADPCM frame format
- SPU RAM memory layout
- Instrument sample data

**Related Documents**:
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)

**Referenced By**: 4 document(s)
- [FF7_PSX_Sound.md](FF7_PSX_Sound.md)
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)

---

### [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)

**Summary**: Documents the INSTRx.DAT instrument index format containing ADSR envelope parameters and SPU memory offsets for FF7 PSX sound samples. LLMs should read this when implementing instrument loading, analyzing ADSR envelope behavior, or debugging sound playback issues.

**Tags**: `psx`, `sound`, `adsr-envelope`, `instrument-index`, `spu-memory`, `audio-metadata`

**Primary Topics**:
- InstrumentIndex struct format
- ADSR envelope parameters
- SPU memory offset translation
- Pitch predefinition tables

**Related Documents**:
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)

**Referenced By**: 4 document(s)
- [FF7_PSX_Sound.md](FF7_PSX_Sound.md)
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)

---

### [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)

**Summary**: Provides high-level overview of the PSX FF7 sound system architecture, including the distinction between streaming audio (XA-ADPCM) and custom tracker-based sound. LLMs should read this when investigating FF7 audio playback, sound format questions, or understanding the relationship between PSX SPU hardware and FF7's custom sound implementation.

**Tags**: `psx`, `sound`, `audio`, `xa-adpcm`, `tracker`, `spu`

**Primary Topics**:
- PSX sound system architecture
- Streaming vs tracker audio
- XA-ADPCM format
- Custom Square Enix sound tracker

**Related Documents**:
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)

**Referenced By**: 4 document(s)
- [FF7_PSX_Sound.md](FF7_PSX_Sound.md)
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)

---

### [PSX Sound](FF7_PSX_Sound.md)

**Summary**: Index page for PlayStation audio system documentation covering instrument banks, AKAO sequences, and sound file formats. LLMs should read this when routing to specific PSX sound subsystem topics or understanding the overall audio architecture organization.

**Tags**: `psx`, `sound`, `audio`, `akao`, `instrument`, `index`

**Primary Topics**:
- PSX audio architecture
- AKAO sequence format
- Instrument data files
- Sound system organization

**Related Documents**:
- [FF7_PSX_Sound_Overview.md](FF7_PSX_Sound_Overview.md)
- [FF7_PSX_Sound_AKAO_frames.md](FF7_PSX_Sound_AKAO_frames.md)
- [FF7_PSX_Sound_INSTRxDAT.md](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7_PSX_Sound_INSTRxALL.md](FF7_PSX_Sound_INSTRxALL.md)

---

## Tag Index

> [!NOTE]
> **For LLMs**: Use this tag index to find documents by keyword or topic.

### `3d-mesh` (1 documents)

- [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)

### `3d-models` (1 documents)

- [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)

### `adpcm` (1 documents)

- [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)

### `adsr-envelope` (1 documents)

- [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)

### `ai-scripting` (1 documents)

- [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

### `ai-scripts` (1 documents)

- [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)

### `akao` (2 documents)

- [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)
- [PSX Sound](FF7_PSX_Sound.md)

### `architecture` (1 documents)

- [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

### `archive-format` (2 documents)

- [FF7 LGP Archive Format](FF7_LGP_format.md)
- [FF7 LZSS Format](FF7_LZSS_format.md)

### `area-terrain` (1 documents)

- [FF7 World Map Encounters](FF7_World_Map_Encounters.md)

### `audio` (2 documents)

- [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)
- [PSX Sound](FF7_PSX_Sound.md)

### `audio-metadata` (1 documents)

- [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)

### `audio-samples` (1 documents)

- [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)

### `audio-sequencer` (1 documents)

- [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)

### `background-rendering` (1 documents)

- [FF7 Field Module](FF7_Field_Module.md)

### `battle-ai` (1 documents)

- [FF7 Battle Script Opcodes](FF7_Battle_Battle_Scenes_Battle_Script.md)

### `battle-animation` (1 documents)

- [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)

### `battle-damage` (1 documents)

- [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)

### `battle-data` (1 documents)

- [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)

### `battle-field` (1 documents)

- [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)

### `battle-formations` (1 documents)

- [FF7 World Map Encounters](FF7_World_Map_Encounters.md)

### `battle-model` (1 documents)

- [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)

### `battle-system` (1 documents)

- [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

### `bin-archive` (1 documents)

- [FF7/Kernel](FF7_Kernel.md)

### `binary-format` (3 documents)

- [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)
- [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)
- [FF7 World Map Encounters](FF7_World_Map_Encounters.md)

### `bit-stream` (1 documents)

- [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)

### `bone-animation` (1 documents)

- [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)

### `breeding` (1 documents)

- [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)

### `bsz-format` (1 documents)

- [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)

### `camera-matrix` (1 documents)

- [FF7 Field Module](FF7_Field_Module.md)

### `character-data` (1 documents)

- [FF7/Savemap](FF7_Savemap.md)

### `character-encoding` (1 documents)

- [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)

### `character-models` (1 documents)

- [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)

### `character-record` (1 documents)

- [The Menu Module](FF7_Menu_Module.md)

### `chocobo` (1 documents)

- [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)

### `chocobo-breeding` (1 documents)

- [FF7/Savemap](FF7_Savemap.md)

### `clut` (1 documents)

- [PSX/TIM format](PSX_TIM_format.md)

### `color-depth` (1 documents)

- [PSX/TIM format](PSX_TIM_format.md)

### `color-keying` (1 documents)

- [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

### `compatibility` (1 documents)

- [FF7/Technical](FF7_Technical.md)

### `compression` (1 documents)

- [FF7 LZSS Format](FF7_LZSS_format.md)

### `cooperative-multitasking` (1 documents)

- [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

### `crashes` (1 documents)

- [FF7/Technical](FF7_Technical.md)

### `critical-hits` (1 documents)

- [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)

### `d3d` (1 documents)

- [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

### `damage-calculation` (1 documents)

- [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

### `damage-formulas` (1 documents)

- [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)

### `data-archives` (1 documents)

- [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)

### `data-format` (1 documents)

- [FF7/Kernel](FF7_Kernel.md)

### `debug-artifacts` (1 documents)

- [Source Code Forensics](FF7_Technical_Source.md)

### `decompression` (1 documents)

- [FF7 LZSS Format](FF7_LZSS_format.md)

### `defense-calculation` (1 documents)

- [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)

### `delta-compression` (1 documents)

- [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)

### `development-history` (1 documents)

- [Source Code Forensics](FF7_Technical_Source.md)

### `documentation-index` (1 documents)

- [FF7](FF7.md)

### `editors` (1 documents)

- [FF7/Technical/Customising](FF7_Technical_Customising.md)

### `eidos` (1 documents)

- [History](FF7_History.md)

### `elemental-damage` (1 documents)

- [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)

### `enc_w.bin` (1 documents)

- [FF7 World Map Encounters](FF7_World_Map_Encounters.md)

### `encounter-data` (1 documents)

- [FF7 WorldMap Module](FF7_WorldMap_Module.md)

### `encounters` (1 documents)

- [FF7 World Map Encounters](FF7_World_Map_Encounters.md)

### `enemy-configuration` (1 documents)

- [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)

### `entity-model` (1 documents)

- [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

### `equipment-data` (1 documents)

- [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)

### `ev-format` (1 documents)

- [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

### `event-scripting` (1 documents)

- [FF7 Field Module](FF7_Field_Module.md)

### `executable-analysis` (1 documents)

- [Source Code Forensics](FF7_Technical_Source.md)

### `extractors` (1 documents)

- [FF7/Technical/Customising](FF7_Technical_Customising.md)

### `ff-text` (1 documents)

- [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)

### `ff7-engine` (2 documents)

- [FF7](FF7.md)
- [FF7/Engine basics](FF7_Engine_basics.md)

### `ff7-history` (1 documents)

- [History](FF7_History.md)

### `ff7-items` (1 documents)

- [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)

### `ff7-modding` (1 documents)

- [FF7/Technical/Customising](FF7_Technical_Customising.md)

### `field-module` (1 documents)

- [FF7 Field Module](FF7_Field_Module.md)

### `field-script` (2 documents)

- [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)
- [FF7/Savemap](FF7_Savemap.md)

### `field-script-banks` (1 documents)

- [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)

### `file-structure` (1 documents)

- [FF7 LGP Archive Format](FF7_LGP_format.md)

### `formation-data` (1 documents)

- [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)

### `frame-buffer` (1 documents)

- [PSX/TIM format](PSX_TIM_format.md)

### `game-data` (1 documents)

- [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)

### `game-design` (1 documents)

- [FF7/Engine basics](FF7_Engine_basics.md)

### `game-development` (1 documents)

- [History](FF7_History.md)

### `game-mechanics` (1 documents)

- [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

### `game-state` (1 documents)

- [FF7/Savemap](FF7_Savemap.md)

### `gzip-archive` (1 documents)

- [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)

### `hrc-skeleton` (1 documents)

- [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)

### `index` (1 documents)

- [PSX Sound](FF7_PSX_Sound.md)

### `installation` (1 documents)

- [FF7/Technical](FF7_Technical.md)

### `instrument` (1 documents)

- [PSX Sound](FF7_PSX_Sound.md)

### `instrument-index` (1 documents)

- [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)

### `instruments` (1 documents)

- [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)

### `inventory` (1 documents)

- [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)

### `item-data` (1 documents)

- [FF7/Kernel](FF7_Kernel.md)

### `kernel` (2 documents)

- [FF7/Kernel](FF7_Kernel.md)
- [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

### `kernel-bin` (1 documents)

- [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)

### `lgp-archive` (1 documents)

- [FF7 LGP Archive Format](FF7_LGP_format.md)

### `lgp-format` (1 documents)

- [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)

### `lzs-archive` (1 documents)

- [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)

### `lzs-compression` (3 documents)

- [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)
- [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)
- [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)

### `lzss` (1 documents)

- [FF7 LZSS Format](FF7_LZSS_format.md)

### `lzss-compression` (1 documents)

- [FF7 WorldMap Module](FF7_WorldMap_Module.md)

### `materia` (1 documents)

- [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)

### `materia-data` (2 documents)

- [FF7 Kernel.bin Archive Format](FF7_Kernel_Kernelbin.md)
- [FF7/Kernel](FF7_Kernel.md)

### `memory-management` (3 documents)

- [FF7/Engine basics](FF7_Engine_basics.md)
- [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)
- [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

### `memory-map` (1 documents)

- [FF7/Savemap](FF7_Savemap.md)

### `memory-structures` (1 documents)

- [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

### `menu-module` (1 documents)

- [The Menu Module](FF7_Menu_Module.md)

### `mesh-format` (1 documents)

- [FF7 WorldMap Module](FF7_WorldMap_Module.md)

### `midi-like` (1 documents)

- [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)

### `mini-games` (1 documents)

- [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)

### `modding-tools` (1 documents)

- [FF7 LGP Archive Format](FF7_LGP_format.md)

### `module-architecture` (1 documents)

- [FF7/Engine basics](FF7_Engine_basics.md)

### `module-overview` (1 documents)

- [FF7](FF7.md)

### `module-system` (1 documents)

- [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

### `multitasking` (1 documents)

- [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

### `navigation` (1 documents)

- [FF7](FF7.md)

### `nintendo` (1 documents)

- [History](FF7_History.md)

### `opcodes` (2 documents)

- [FF7 Battle Script Opcodes](FF7_Battle_Battle_Scenes_Battle_Script.md)
- [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)

### `palette` (1 documents)

- [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

### `patches` (1 documents)

- [FF7/Technical/Customising](FF7_Technical_Customising.md)

### `pc-format` (3 documents)

- [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)
- [FF7 Field Module](FF7_Field_Module.md)
- [FF7 LGP Archive Format](FF7_LGP_format.md)

### `pc-port` (1 documents)

- [History](FF7_History.md)

### `pc-texture` (1 documents)

- [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

### `pc-version` (1 documents)

- [FF7/Technical](FF7_Technical.md)

### `pixel-format` (1 documents)

- [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

### `playstation` (1 documents)

- [PSX/TIM format](PSX_TIM_format.md)

### `polygon-mesh` (1 documents)

- [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)

### `psx` (11 documents)

- [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)
- [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)
- [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)
- [FF7/Engine basics](FF7_Engine_basics.md)
- [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)
- [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)
- [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)
- [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)
- [PSX Sound](FF7_PSX_Sound.md)
- [PSX/TIM format](PSX_TIM_format.md)

### `psx-format` (1 documents)

- [FF7 Field Module](FF7_Field_Module.md)

### `psx-memory` (1 documents)

- [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)

### `psx-pc-differences` (1 documents)

- [The Menu Module](FF7_Menu_Module.md)

### `psy-q` (1 documents)

- [FF7/Kernel/Overview](FF7_Kernel_Overview.md)

### `qhimm-community` (1 documents)

- [FF7/Technical/Customising](FF7_Technical_Customising.md)

### `reverse-engineering` (1 documents)

- [Source Code Forensics](FF7_Technical_Source.md)

### `rng-mechanics` (1 documents)

- [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)

### `rotation-encoding` (1 documents)

- [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)

### `save-file` (2 documents)

- [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)
- [FF7/Savemap](FF7_Savemap.md)

### `save-format` (1 documents)

- [The Menu Module](FF7_Menu_Module.md)

### `savemap` (2 documents)

- [FF7/Kernel](FF7_Kernel.md)
- [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)

### `scene-bin` (2 documents)

- [FF7 Battle Scenes](FF7_Battle_Battle_Scenes.md)
- [FF7 Battle Script Opcodes](FF7_Battle_Battle_Scenes_Battle_Script.md)

### `scripting` (2 documents)

- [FF7 Battle Script Opcodes](FF7_Battle_Battle_Scenes_Battle_Script.md)
- [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

### `skeletal-animation` (1 documents)

- [FF7 Battle Animation Format (PC)](FF7_Battle_Battle_Animation_PC.md)

### `sliding-window` (1 documents)

- [FF7 LZSS Format](FF7_LZSS_format.md)

### `sony-playstation` (1 documents)

- [History](FF7_History.md)

### `sound` (5 documents)

- [FF7 PSX Sound AKAO Frames](FF7_PSX_Sound_AKAO_frames.md)
- [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)
- [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)
- [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)
- [PSX Sound](FF7_PSX_Sound.md)

### `source-forensics` (1 documents)

- [Source Code Forensics](FF7_Technical_Source.md)

### `spu` (1 documents)

- [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)

### `spu-memory` (1 documents)

- [FF7/PSX/Sound/INSTRx.DAT](FF7_PSX_Sound_INSTRxDAT.md)

### `spu-ram` (1 documents)

- [FF7/PSX/Sound/INSTRx.ALL](FF7_PSX_Sound_INSTRxALL.md)

### `squaresoft` (1 documents)

- [History](FF7_History.md)

### `stack-machine` (2 documents)

- [FF7 Battle Script Opcodes](FF7_Battle_Battle_Scenes_Battle_Script.md)
- [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

### `stat-formulas` (1 documents)

- [FF7 Chocobo Breeding Guide](FF7_Chocobo_Breeding.md)

### `status-effects` (2 documents)

- [FF7 Battle Damage Formulas](FF7_Battle_Damage_Formulas.md)
- [FF7 Battle Mechanics](FF7_Battle_Battle_Mechanics.md)

### `table-of-contents` (1 documents)

- [FF7](FF7.md)

### `terrain` (1 documents)

- [FF7 WorldMap Module](FF7_WorldMap_Module.md)

### `tex-format` (2 documents)

- [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)
- [FF7 TEX Texture Format (PC)](FF7_TEX_format.md)

### `text-rendering` (1 documents)

- [FF7 Item and Materia Reference](FF7_Item_Materia_Reference.md)

### `texture` (2 documents)

- [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)
- [PSX/TIM format](PSX_TIM_format.md)

### `texture-cache` (1 documents)

- [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)

### `tim-format` (1 documents)

- [PSX/TIM format](PSX_TIM_format.md)

### `tim-texture` (3 documents)

- [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)
- [FF7 Kernel Low-Level Libraries](FF7_Kernel_Low_level_libraries.md)
- [FF7/Playstation Battle Model Format](FF7_Playstation_Battle_Model_Format.md)

### `tools` (1 documents)

- [FF7/Technical/Customising](FF7_Technical_Customising.md)

### `tracker` (1 documents)

- [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)

### `troubleshooting` (1 documents)

- [FF7/Technical](FF7_Technical.md)

### `txz-archive` (1 documents)

- [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)

### `vertex-data` (1 documents)

- [FF7 Battle Field Format](FF7_Battle_Battle_Field.md)

### `vram` (3 documents)

- [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)
- [FF7/Kernel/Memory management](FF7_Kernel_Memory_management.md)
- [The Menu Module](FF7_Menu_Module.md)

### `walkmap` (1 documents)

- [FF7 WorldMap Module](FF7_WorldMap_Module.md)

### `walkmesh` (1 documents)

- [FF7 Field Module](FF7_Field_Module.md)

### `weapon-data` (1 documents)

- [FF7/Kernel](FF7_Kernel.md)

### `window-bin` (1 documents)

- [The Menu Module](FF7_Menu_Module.md)

### `world-map` (5 documents)

- [FF7 World Map BSZ Format](FF7_World_Map_BSZ.md)
- [FF7 World Map Encounters](FF7_World_Map_Encounters.md)
- [FF7 World Map TXZ Archive Format](FF7_World_Map_TXZ.md)
- [FF7 WorldMap Module](FF7_WorldMap_Module.md)
- [FF7/WorldMap Module/Script](FF7_WorldMap_Module_Script.md)

### `xa-adpcm` (1 documents)

- [FF7/PSX/Sound/Overview](FF7_PSX_Sound_Overview.md)

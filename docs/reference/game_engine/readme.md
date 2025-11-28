# FF7 Game Engine Documentation

**A comprehensive collection of documentation for Final Fantasy VII's game engine, compiled from the qhimm-modding Fandom wiki.**

Created: 2025-11-28 12:44:49 JST (Friday)
Last Modified: 2025-11-28 12:44:49 JST (Friday)
Version: 1.0.0
Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c

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

## Source & Attribution

All content scraped from the [qhimm-modding Fandom wiki](https://qhimm-modding.fandom.com/wiki/FF7) on 2025-11-28.

This documentation is the result of years of reverse engineering work by the FF7 modding community. Thanks to all contributors who documented these technical specifications.

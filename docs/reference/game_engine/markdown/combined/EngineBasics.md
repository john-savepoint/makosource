# FF7 Engine Basics

**Category: Core Engine Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains fundamental information about FF7's game engine architecture and basic concepts.

---

# FF7

- [FF7](#ff7){#toc-ff7}
  - [Contents](#contents){#toc-contents}



`<small>`{=html} This is a Stub article. A Wiki version of Gears should go here. For more information, select the \"discussion\" tab above so we can best architecture the data. For those who want to start converting, download the [Gears pdf](https://wiki.ffrtt.ru/gears.pdf) [Halkun](User:Halkun "Halkun"){.wikilink} 20:18, 5 Mar 2005 (CST) `</small>`{=html}

\

## Contents

- [History](FF7/History "History"){.wikilink}
- [Engine Basics](FF7/Engine_basics "Engine Basics"){.wikilink}
  - Parts of the Engine
  - Generic Program Flow
- [The Kernel](FF7/Kernel "The Kernel"){.wikilink}
  - [Kernel Overview](FF7/Kernel/Overview "Kernel Overview"){.wikilink}
    - History
    - Kernel Functionality
  - [Memory Management](FF7/Kernel/Memory_management "Memory Management"){.wikilink}
    - RAM Management
    - VRAM Management
    - PSX CD-ROM management
  - [Kernel.bin](FF7/Kernel/Kernel.bin "Kernel.bin"){.wikilink}
    - The KERNEL.BIN Archive
    - The KERNEL2.BIN Archive
  - [Low Level Libraries](FF7/Kernel/Low_level_libraries "Low Level Libraries"){.wikilink}
    - PC to PSX comparison
    - Data Archives
      - BIN Archive data format
      - [ LZSS Archives](FF7/LZSS_format " LZSS Archives"){.wikilink}
      - [ LGP Archives](FF7/LGP_format " LGP Archives"){.wikilink}
    - Textures
      - [ TIM texture data format for PSX](PSX/TIM_format " TIM texture data format for PSX"){.wikilink}
      - [ TEX texture data format for the PC](FF7/TEX_format " TEX texture data format for the PC"){.wikilink}
    - File formats for 3D models
      - [Model Formats for PSX](FF7/Kernel/Low_level_libraries#Model_formats_for_PSX "Model Formats for PSX"){.wikilink}
      - Model Formats for PC
- [The Menu Module](FF7/Menu_Module "The Menu Module"){.wikilink}
  - Menu Overview
  - Menu Initialization
  - Menu Modules
  - Calling the various menus
  - Menu dependencies
  - [The Save Game format](FF7/Savemap "The Save Game format"){.wikilink}
- [ The Field Module](FF7/Field_Module " The Field Module"){.wikilink}
  - Field Overview
  - Field Format (PC)
    - General PC Field File Format
    - PC Field File Header
    - File Section Details
  - [Field Format (PSX)](FF7/Field_Module#Field_Format_.28PSX.29 "Field Format (PSX)"){.wikilink}
    - [PSX DAT Format](FF7/Field_Module#PSX_DAT_Format "PSX DAT Format"){.wikilink}
    - [PSX MIM Format](FF7/Field_Module#PSX_MIM_Format "PSX MIM Format"){.wikilink}
    - [PSX BSX Format](FF7/Field_Module#PSX_BSX_Format "PSX BSX Format"){.wikilink}
    - [PSX BCX Format](FF7/Field_Module#PSX_BCX_Format "PSX BCX Format"){.wikilink}
- The Battle Module
  - Battle Overview
  - [ Battle Mechanics](FF7/Battle/Battle_Mechanics " Battle Mechanics"){.wikilink}
  - [ Battle Field](FF7/Battle/Battle_Field " Battle Field"){.wikilink}
  - [ Battle Scenes (scene.bin)](FF7/Battle/Battle_Scenes " Battle Scenes (scene.bin)"){.wikilink}
    - [ Battle Scripts](FF7/Battle/Battle_Scenes/Battle_Script " Battle Scripts"){.wikilink}
  - [ Battle Models (PSX)](FF7/Playstation_Battle_Model_Format " Battle Models (PSX)"){.wikilink}
  - [ Battle Animation (PC)](FF7/Battle/Battle_Animation_(PC) " Battle Animation (PC)"){.wikilink}
- [ The World Map Module](FF7/WorldMap_Module " The World Map Module"){.wikilink}
  - [ World Map BSZ model file format (PSX)](FF7/World_Map/BSZ " World Map BSZ model file format (PSX)"){.wikilink}
  - [ World Map TXZ file format (PSX)](FF7/World_Map/TXZ " World Map TXZ file format (PSX)"){.wikilink}
  - [ World Map Script Engine](FF7/WorldMap_Module/Script " World Map Script Engine"){.wikilink}
- Sound
  - [PSX Sound](FF7/PSX/PSX_Sound "PSX Sound"){.wikilink}
    - [Overview](FF7/PSX/Sound/Overview "Overview"){.wikilink}
    - [INSTRx.DAT](FF7/PSX/Sound/INSTRx.DAT "INSTRx.DAT"){.wikilink}
    - [INSTRx.ALL](FF7/PSX/Sound/INSTRx.ALL "INSTRx.ALL"){.wikilink}
    - [AKAO frames](FF7/PSX/Sound/AKAO_frames "AKAO frames"){.wikilink}
  - PC Sound
- [ Technical Help](FF7/Technical " Technical Help"){.wikilink}
- [Tools and patches](FF7/Technical/Customising "Tools and patches"){.wikilink}
- [Source Code Forensics](FF7/Technical/Source "Source Code Forensics"){.wikilink}

---

# FF7/Engine basics {#ff7engine_basics}

- [FF7/Engine basics](#ff7engine_basics){#toc-ff7engine_basics}
  - [Parts of the Engine](#parts_of_the_engine){#toc-parts_of_the_engine}
  - [Generic Program Flow](#generic_program_flow){#toc-generic_program_flow}



## Parts of the Engine {#parts_of_the_engine}

The engine used to power Final Fantasy 7 is split into several modules. This allowed the programming team to break apart into very distinct groups. It also created a very diverse game playing environment. It also allowed the artists to only have to work within their own module, keeping the artwork as dynamic as possible.

The module system allowed for a single point of entry into, and exit out of, each distinct part of the game. The PSX, which the game was originally developed for, had very limited resources. With only 1 megabyte of video ram and 2 megabytes of system ram, data had to be banked in and out efficiently. Modules were a clean way to dump whole parts of the engine to make way for other parts.

The core system is made up of six modules. They are called the kernel, field, menu, world map, battle, and mini game. They are arranged in the following order.![](Engine_parts.jpg "Engine_parts.jpg")\

<center>
</center>

\

## Generic Program Flow {#generic_program_flow}

Not every module is accessible by every other module. There is a distinct flow between them. For example, you can not access the menu from battle, much to the chagrin of the poor user who had forgotten to equip some last minute item. The field module, second only to the kernel, drives the game. It includes a powerful scripting system that can call any module within the game.


---

## Images

![Engine parts](images/Engine_parts.jpg)


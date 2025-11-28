# FF7/Kernel/Overview

<!-- MERGE METADATA -->
<!--
Merged: 2025-11-28 15:50 JST
Source Files:
  - Original: markdown/FF7_Kernel_Overview.md
  - Major Section: extracted_major_sections/03_KERNEL.md (lines 1-26)
Status: Content review complete. Individual file contains all overview material.
        No additional content extracted from major section (all content already present).

Related Files:
  - FF7_Kernel_Memory_management.md (major section lines 27-78)
  - FF7_Kernel_Kernelbin.md (major section lines 79-548)
  - FF7_Kernel_Low_level_libraries.md (major section lines 549-799+)
  - FF7_Playstation_Battle_Model_Format.md (major section lines 800-1600+)

Session ID: [Analysis performed for content extraction task]
-->

- [FF7/Kernel/Overview](#ff7kerneloverview){#toc-ff7kerneloverview}
  - [History](#history){#toc-history}
  - [Kernel Functionality](#kernel_functionality){#toc-kernel_functionality}



## History

The kernel is a throwback to the very first Final Fantasy game for the Nintendo\'s original 8 bit system. The NES could only natively read 32 kilobytes of program ROM. To get around this incredible limitation, Nintendo developed \"memory mappers\" that allowed parts of the program to be switched out, or \"banked\" and replaced with other parts stored on the game cartridge.

FF1 used Nintendo\'s \"Memory Manager Controller #1\" (MMC1) . This controller split the game into sixteen sections, each 16 kilobytes long. (The maximum an MMC1 program could be was 256K). This controller also split the accessible memory from the cartridge into two 16K sections. The top 16K was bankable. The bottom 16K could never be switched out and stayed in memory until you removed the cartridge.

The original FF1 kernel was located in this bottom 16K of memory.

First and foremost the kernel contained the main program loop. It handled all the low level functions for the game. Some of these included controlling interrupts, banking in and out the appropriate part of the game, jumping control to a particular module, playing the music, and other tasks.

As the Final Fantasy franchise grew, so did the size of the games. They all still retained the kernel/module system. During the backporting process, this did cause a few headaches. For example, Final Fantasy 6 was originally developed for the Super Nintendo. When it\'s menu module was banked in, it was done with electronic bank switching. The later PSX port banked the data from the CD-ROM, which caused an unexpected lag that one wasn\'t used to. On the PC version for FF7, them menu system was simply integrated into the main executable.

## Kernel Functionality {#kernel_functionality}

The Kernel is a threaded multitasking program that manages the whole system. It uses a simple software based memory manager that handles both RAM and video memory for all the modules in the game. Assisting the kernel are many statically linked Psy-Q libraries. In the case of the PC port, the Psy-Q libs were replaced with a PC equivalent. For example the SEQ player was replaced with a MIDI player, Both accomplish the same tasks, just with different formats and execution strategies. The table below is a generic representation of how the kernel sits in relation to the other aspects of the program.

![](Kernel_table.png "Kernel_table.png")


---

## Related Content in Major Section

The following sections exist in the `extracted_major_sections/03_KERNEL.md` file but have not been merged into this file as they belong in separate, more detailed files:

### Memory Management (Major Section Lines 27-78)
- **Location**: Belongs in `FF7_Kernel_Memory_management.md`
- **Content**:
  - RAM management (Save Map structure, field script banks)
  - VRAM management (PSX layout, texture caching)
  - CD-ROM management (module preloading, sector-based access)

### Game Resources - KERNEL.BIN/KERNEL2.BIN (Major Section Lines 79-548)
- **Location**: Belongs in `FF7_Kernel_Kernelbin.md`
- **Content**:
  - 27-section archive breakdown
  - Detailed format specifications for commands, attacks, items, weapons, armor, accessories, materia data
  - KERNEL2.BIN PC archive format

### Low-Level Libraries (Major Section Lines 549-799+)
- **Location**: Belongs in `FF7_Kernel_Low_level_libraries.md`
- **Content**:
  - PC to PSX format comparison
  - BIN archive types (uncompressed and GZIP)
  - LZS compression algorithm with detailed examples
  - LGP archive format documentation
  - TIM texture format specifications

### 3D Model Formats and Grouping (Major Section Lines 800-1600+)
- **Location**: Belongs in `FF7_Playstation_Battle_Model_Format.md`
- **Content**:
  - PSX 3D model format structure (chunks, vertices, normals, polygons, edges, groups)
  - Model grouping architecture and vertex cloning
  - Complex vertex/polygon/edge indexing systems
  - Bounding boxes and normal index tables

---

## Images

![Kernel table](../images/Kernel_table.png)


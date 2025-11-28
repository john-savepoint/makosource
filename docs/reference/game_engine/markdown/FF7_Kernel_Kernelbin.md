# FF7/Kernel/Kernel.bin

- [FF7/Kernel/Kernel.bin](#ff7kernelkernel.bin){#toc-ff7kernelkernel.bin}
  - [Important Files](#important_files){#toc-important_files}
  - [The KERNEL.BIN Archive](#the_kernel.bin_archive){#toc-the_kernel.bin_archive}
  - [The KERNEL2.BIN Archive](#the_kernel2.bin_archive){#toc-the_kernel2.bin_archive}



## Important Files {#important_files}

|   PSX Version    |        PC Version        |
|:----------------:|:------------------------:|
| /INIT/KERNEL.BIN | /DATA/KERNEL/KERNEL.BIN  |
|                  | /DATA/KERNEL/KERNEL2.BIN |

## The KERNEL.BIN Archive {#the_kernel.bin_archive}

The file KERNEL.BIN archive is in [BIN-GZIP format](FF7/Kernel/Low_level_libraries#BIN-GZIP_Type_Archives "BIN-GZIP format"){.wikilink}. It consists of 27 gziped sections concatenated together with a 6 byte header for each. This file is the same both on the PC and PSX versions. This holds all the static data and menu text for the game, with a look up table at the beginning of the section. The first 9 sections of data (i.e. The non-text related items) are in typical BIN file archive format. Sections 10-27 are [FF Text files](FF7/FF_Text "FF Text files"){.wikilink}. The text sections have a header of pointers at the beginning of each section and point to a text block below.

The KERNEL.BIN file consists of the following sections.

| File | Data | Offset |
|----|----|----|
| 1 | [Command data](FF7/Command_data "Command data"){.wikilink} | 0x0006 |
| 2 | [Attack data](FF7/Attack_data "Attack data"){.wikilink} | 0x0086 |
| 3 | [Battle and growth data](FF7/Battle_and_growth_data "Battle and growth data"){.wikilink} | 0x063A |
| 4 | [Initialization data](FF7/Character_starting_stats "Initialization data"){.wikilink} | 0x0F7F |
| 5 | [Item data](FF7/Item_data "Item data"){.wikilink} | 0x111B |
| 6 | [Weapon data](FF7/Weapon_data "Weapon data"){.wikilink} | 0x137A |
| 7 | [Armor data](FF7/Armor_data "Armor data"){.wikilink} | 0x1A30 |
| 8 | [Accessory data](FF7/Accessory_data "Accessory data"){.wikilink} | 0x1B73 |
| 9 | [Materia data](FF7/Materia_data "Materia data"){.wikilink} | 0x1C11 |
| 10 | Command descriptions | 0x1F32 |
| 11 | Magic descriptions | 0x2199 |
| 12 | Item descriptions | 0x28D4 |
| 13 | Weapon descriptions | 0x2EE2 |
| 14 | Armor descriptions | 0x307B |
| 15 | Accessory descriptions | 0x315F |
| 16 | Materia descriptions | 0x3384 |
| 17 | Key Item descriptions | 0x3838 |
| 18 | Command Names | 0x3BE2 |
| 19 | Magic Names | 0x3CCA |
| 20 | Item Names | 0x4293 |
| 21 | Weapon Names | 0x4651 |
| 22 | Armor Names | 0x4B02 |
| 23 | Accessory Names | 0x4C4B |
| 24 | Materia Names | 0x4D90 |
| 25 | Key Item Names | 0x5040 |
| 26 | Battle and Battle-Screen Text | 0x5217 |
| 27 | Summon Attack Names | 0x5692 |

## The KERNEL2.BIN Archive {#the_kernel2.bin_archive}

On the PC version there exists a secondary kernel archive called KERNEL2.BIN. This archive contains only sections 10-27 (Text data) of KERNEL.BIN. The data was ungzipped from the original archive, concatenated together, and then LZSed into a single archive with a 4 byte header giving the length of the file.

The maximum allotted storage space on the PC version for all un-LZSed data in the kernel2.bin is 27KB (27648 bytes). This means that the total size of the extracted files (text and pointers) must be less than this.

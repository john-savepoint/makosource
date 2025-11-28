# FF7 Kernel System

**Category: Kernel Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's kernel system, including memory management, kernel.bin structure, low-level libraries, and compression/archive formats.

---

# FF7/Kernel

- [FF7/Kernel](#ff7kernel){#toc-ff7kernel}



- [Kernel Overview](FF7/Kernel/Overview "Kernel Overview"){.wikilink}
- [Memory Management](FF7/Kernel/Memory_management "Memory Management"){.wikilink}
- [Kernel.bin](FF7/Kernel/Kernel.bin "Kernel.bin"){.wikilink}
- [Low Level Libraries](FF7/Kernel/Low_level_libraries "Low Level Libraries"){.wikilink}

---

# FF7/Kernel/Overview

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

## Images

![Kernel table](images/Kernel_table.png)


---

# FF7/Kernel/Memory management {#ff7kernelmemory_management}

- [FF7/Kernel/Memory management](#ff7kernelmemory_management){#toc-ff7kernelmemory_management}
  - [RAM management](#ram_management){#toc-ram_management}
  - [VRAM management](#vram_management){#toc-vram_management}
  - [PSX CD-ROM management](#psx_cd_rom_management){#toc-psx_cd_rom_management}



## RAM management {#ram_management}

No matter what module is banked into memory, there is a section of memory 4,340 bytes long (0x10F4 bytes) that is reserved for all the variables for the entire game. This entire image is called the \"[Savemap](FF7/Savemap "Savemap"){.wikilink}\". When it\'s time to save a game, this section of memory is copied to non-volatile ram, such as a hard disk or memory card.

Within the [Savemap](FF7/Savemap "Savemap"){.wikilink} there are 5 banks of memory that are directly accessible by the [field scripting language](FF7/Field_script "field scripting language"){.wikilink}. These can either be accessed 8 bits or 16 bits at a time depending on the field command argument. The following table is basic memory map of the banks and how they relate to the [Savemap](FF7/Savemap "Savemap"){.wikilink}. There is also an allocation for 256 bytes for temporary field variables. These are not used between field files and are not saved.

| Offset | 8 Bit Field Bank | 16 Bit Filed Bank | Description |
|:--:|:--:|:--:|:--:|
| 0x0000 | N/A | N/A | Beginning of [Savemap](FF7/Savemap "Savemap"){.wikilink} |
| 0x0BA4 | 0x1 | 0x2 | Field Script Bank 1 |
| 0x0CA4 | 0x3 | 0x4 | Field Script Bank 2 |
| 0x0DA4 | 0xB | 0xC | Field Script Bank 3 |
| 0x0EA4 | 0xD | 0xE | Field Script Bank 4 |
| 0x0FA4 | 0xF | 0x7 | Field Script Bank 5 |
| 0x10F4 | N/A | N/A | End of [Savemap](FF7/Savemap "Savemap"){.wikilink} |

|  |  |  |  |
|----|----|----|----|
| width: 80px\" \| N/A | width: 80px\" align=\"center\" \| 0x5 | width: 100px\" align=\"center\" \| 0x6 | width: 250px\" \| Temporary field variables (256 bytes) |

## VRAM management {#vram_management}

The kernel is in charge of allocating, caching, and displaying in Video RAM. In the case of the PSX, port, the Playstation only has 1 megabyte of VRAM which makes this task a little complex. This is alleviated somewhat by using the PSX\'s VRAM caching system.

The PSX video memory can best be seen as a rectangular \"surface\" made up of 2048x512 pixels. A slight caveat to this model is that the PSX can hold multiple color depths in VRAM at the same time. To make the VRAM a little easier to visualize, This document represents VRAM as a 1024x512 matrix to allow for some color depth in either direction and to minimize some extreme skewing of the video buffers.

\
The following is a typical state of VRAM during game play.
![](Gears_img_3.jpg "Gears_img_3.jpg")
The two game screens on the left side are the video buffer and the back buffer. The patchwork of graphics on the top right are the field graphics for that scene. The bottom row consists of cached graphics and special effects and on right semi-permanent and permanent textures for the game.

\
The following is a schematic representation of VRAM and all it\'s texture boundaries.
![](Gears_img_4.jpg "Gears_img_4.jpg")
Here the sections of VRAM are much more visible. The large cyan areas are the video frame buffers. The PSX uses a standard double page buffer to animate the game. The blank areas above and below the frame buffers are blank to allow for a correct V-sync. The dark blue areas to the right of the frame buffers are when the game plays 24 bit movies. This requires a slightly larger display and the first two texture caches are overwritten. During times in the game where no movies can take place, such as Battle, textures are commonly placed here.

The magenta area under the video buffers is the Color Look Up Tables (CLUT). This is where the texture palettes are stored. This also allows the PSX to display multiple color depths at the same time. The red area to the right is extra CLUT space when it is needed and there are no textures cached there.

The green area on the right is the permanent menu textures and the yellow is where the menu font is located.

All the blank rectangles are the texture cache boundaries. In order of volatility, the top two rows of cache space are overwritten from left to right, and then the bottom rows are overwritten. The textures on the bottom right are barely overwritten except for key places.

\

## PSX CD-ROM management {#psx_cd_rom_management}

One of the big rules on PSX development is that direct hardware access is a prohibited. Everything must go through the BIOS or the program will risk being incompatible with later systems. This means not only from PSX to PS2, but also all the trivial hardware revisions as well. This creates a problem for the kernel. During module transitions (for example, going from \"Map\" to \"Battle\"), the engine actually \"preloads\" the next module while the current one is still executing. This loading of data can\'t be done with a simple open() or read() BIOS syscall. Whenever you enter the BIOS, the rest of the system comes to a screeching halt until it is exited.

This problem is solved by the FF7 actually controlling the CD-ROM access itself though faster, low-level BIOS calls. The kernel can only load 8 kilobytes at a time in this \"quick mode\" In this mode the kernel also only references files by what sector of the CD-ROM the data is located on, not by filename.


---

## Images

![Gears img 3](images/Gears_img_3.jpg)

![Gears img 4](images/Gears_img_4.jpg)


---

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

---

# FF7/Kernel/Low level libraries {#ff7kernellow_level_libraries}

- [FF7/Kernel/Low level libraries](#ff7kernellow_level_libraries){#toc-ff7kernellow_level_libraries}
  - [PC to PSX comparison](#pc_to_psx_comparison){#toc-pc_to_psx_comparison}
  - [Data Archives](#data_archives){#toc-data_archives}


## PC to PSX comparison {#pc_to_psx_comparison}

The files and data formats used in the PSX version of FF7 and it\'s PC port are conceptually the same thing, and accomplish the same tasks. That being said, they both have wildly different formats, both of which were derived from a third original format that is also somewhat different to the first two.

The original PSX FF7 was created in part using Sony\'s Psy-Q development library. This library uses common formats that are \"native\" to the PSX. Often, a toolkit was used to convert common development-based formats, such as a TGA bitmap or a palleted GIF file, to something a little more suited to Psy-Q, which would be a [TIM file](PSX/TIM_format "TIM file"){.wikilink}.

During the porting process to the PC, some of the original artwork (and artists for that matter) were no longer available. This resulted in the port team having to use the Psy-Q versions of many files, which were ill suited for the PC architecture. In our example, the [TIM file](PSX/TIM_format "TIM file"){.wikilink} was converted to a TEX file, which would be manipulated in the PC\'s video memory a little more efficiently. Sometimes the original artwork was available, such as the pictures of the characters within the menu, or the original MIDI files. Most often times it was not.

To make things a little more confusing, both systems also archive their data files in different ways, making the extraction and rendering of each file a bit of a bear. For the most part the data within each file is the same thing, just a little switched around. Here, we will cover the more generic files first, and then common files used in each module.

## Data Archives {#data_archives}

To save space, quicken access time, and to obfuscate the file structure a little, most of the data files are stored in some kind of archive format. The archives remove such useful items as subdirectories and logical data placement. There is no real \"native\" format these are based on.

### BIN archive data format {#bin_archive_data_format}

The BIN format comes as two different types. They both have the same extension, so one must open the file to see which format is which. They are best described as BIN Types and BIN-GZIP types.

#### BIN Type Archives {#bin_type_archives}

These are uncompressed archives. The header is 4 bytes long and gives the length of the file without the header and then the data beyond that.

#### BIN-GZIP Type Archives {#bin_gzip_type_archives}

Unless otherwise noted, these have a 6 byte header. After this are many gziped sections concatenated together.

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x0000</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of gzipped section 1</p></td>
</tr>
<tr>
<td><p>0x0002</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of ungzipped section 1</p></td>
</tr>
<tr>
<td><p>0x0004</p></td>
<td><p>2 bytes</p></td>
<td><p>File type*</p></td>
</tr>
<tr>
<td><p>0x0006</p></td>
<td><p>Varies</p></td>
<td><p>[0x1F8B080000000000...] - Gzip header 1 and data</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of gzipped section 2</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of ungzipped section 2</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>2 bytes</p></td>
<td><p>File type*</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>Varies</p></td>
<td><p>[0x1F8B080000000000...] - Gzip header 2 and data</p></td>
</tr>
<tr>
<td colspan="3" style="text-align: center;"><p>...</p></td>
</tr>
</tbody>
</table>

\
*\** This particular value might be ignored by the whatever method is decompressing these archive types. Within archives it declares that the compressed file is a particular type. These values seem to be unique to the particular archive that is being opened and is not consistent between archives.

Example 1: Within the [KERNEL.BIN](FF7/Kernel/Kernel.bin "KERNEL.BIN"){.wikilink} the first nine files are all different data sets so are numbered sequentially 0-8. All remaining files are text types and get labeled as type 9.\
Example 2: Within the WINDOW.BIN file there are three files. The first two are type \"0\" and are textures. The third file is type \"1\" and not a texture.

### LZS Archives {#lzs_archives}

The [LZS format](FF7/LZS_format "LZS format"){.wikilink} is used throughout the PSX version of Final Fantasy 7, often ending with the .lzs extension. LZS itself stands for Lempel-Ziv-Shannon-Fano, Statistical plus Arithmetic. It was originally developed by [Professor Haruhiko Okumura](http://oku.edu.mie-u.ac.jp/~okumura/index-e.html) based on the work of [Abraham Lempel](http://www.hpl.hp.com/about/bios/abraham_lempel.html) and [Jacob Ziv](http://www.marconifoundation.org/pages/dynamic/fellows/fellow_details.php?roster_id=23).

### LGP Archives {#lgp_archives}

The LGP file format is only used for the PC port of Final Fantasy 7. These are large \"volume\" type archives that hold most of the game\'s data. These archives can hold thousands of files. Unlike the BIN or LZS type files, this archive does reference the data within it by filename. Its file format is explained [here](FF7/LGP_format "here"){.wikilink}.

## Textures

A texture is just a picture that is placed into video memory. It is later manipulated by the engine and displayed on the screen. The native format of a texture was the Psy-Q [TIM](PSX/TIM_format "TIM"){.wikilink} (Texture Image Map). This is used as the native format for the PSX version as well, with a few caveats explained below. The file can hold multiple color look up tables. This was one of the reasons why a video card on the PC that could do palleted data at high color depths was needed.

### TIM texture data format for PSX {#tim_texture_data_format_for_psx}

The [TIM files](PSX/TIM_format "TIM files"){.wikilink} are found both on raw format and also within several archives, including [BIN](FF7/Kernel/Low_level_libraries#BIN_archive_data_format "BIN"){.wikilink}, [LZS](FF7/Kernel/Low_level_libraries#LZS_Archives "LZS"){.wikilink}, or even MNU. The format proper has the ability to contain 24 bit bitmaps, but is not used in FF7. The format was created because the PSX does not have direct access to it\'s VRAM, and must go through the [GPU](PSX/GPU "GPU"){.wikilink} for any graphic access. [A TIM file](PSX/TIM_format "A TIM file"){.wikilink} is a clean way to load a texture and color look up table into VRAM.

### TEX texture data format for the PC {#tex_texture_data_format_for_the_pc}

TEX files are texture files for the PC. The format for these files are located [here](FF7/TEX_format "here"){.wikilink}.

## File formats for 3D models {#file_formats_for_3d_models}

During the development process, 3D models contain a good deal of information needed by the artist every time they save or load the model. When the model is finished, it is often exported and broken up into smaller files with many unneeded attributes stripped from them. When the models for FF7 were created, they were exported into Psy-Q\'s 3D library formats. These include [resource data (.RSD)](PSX/RSD "resource data (.RSD)"){.wikilink}, polygon data (.PLY), polygon groups (.GRP), materials (.MAT), [textures (.TIM)](PSX/TIM_file "textures (.TIM)"){.wikilink}, [skeletal hierarchy (.HRC)](PSX/HRC "skeletal hierarchy (.HRC)"){.wikilink}, and animation (.ANM).

The models are handled differently between modules. The models in the \"battle\" modules have a different animation system than the field models. When the models were converted to the PC version, they were taken from the Psy-Q formats to a more PC-friendly one. Some are even the original, uncompiled, Psy-Q files.

### Model formats for PSX {#model_formats_for_psx}

The Playstation models are stored in the following directories, \\ENEMY1 \\ENEMY2 \\ENEMY3 \\ENEMY4 \\ENEMY5 \\ENEMY6 (battle models), \\FIELD (field models and field character models), \\MAGIC (Summon magic), and \\STAGE1 \\STAGE2 (battle scenes). Battle model names for special characters and party characters are stored in \\ENEMY6, all models of this type end in an .LZS extension. The same goes with summon magic used they are stored with there animations etc. in \\MAGIC with a .LZS extension. The only exception to this extension is the FIELD models, which use the extensions BSX and BCX for scene models and character models respectively. The [Playstation battle model format](FF7/Playstation_Battle_Model_Format "Playstation battle model format"){.wikilink}, is different than the [Playstation field model format](FF7/Field/BSX "Playstation field model format"){.wikilink}, also the [FF7/Playstation battle scene format](FF7/Playstation_battle_scene_format "FF7/Playstation battle scene format"){.wikilink}, is similiar but not identical to the [Playstation battle model format](FF7/Playstation_Battle_Model_Format "Playstation battle model format"){.wikilink}. The [Playstation magic model](FF7/Playstation_magic_model "Playstation magic model"){.wikilink} format is a work in progress.

### Model Formats for PC {#model_formats_for_pc}

The PC models are stored in the LGP files in the /DATA directory. The names for the models were obfuscated a little. The data can be found in the [Hierarchy files (.HRC)](PSX/HRC "Hierarchy files (.HRC)"){.wikilink}, [Resource data files (.RSD)](PSX/RSD "Resource data files (.RSD)"){.wikilink}, and [Polygon files (.P)](FF7/P "Polygon files (.P)"){.wikilink}.

---

# FF7/LZSS format {#ff7lzss_format}

- [FF7/LZSS format](#ff7lzss_format){#toc-ff7lzss_format}
  - [Format](#format){#toc-format}
  - [LZSS compression](#lzss_compression){#toc-lzss_compression}
  - [Reference format](#reference_format){#toc-reference_format}
  - [Example](#example){#toc-example}
  - [Complications](#complications){#toc-complications}



#### Format

The LZSS archive has a very small header at 0x00 that has the length of the compressed file as an unsigned 32 bit integer. After that is the compressed data.
Some files use the .lzs extension, probably to make the extension 3 characters long. It has caused some confusion, since LZS is a different compression method.

#### LZSS compression {#lzss_compression}

FF7 uses LZSS compression on some of their files, as devised by Professor Haruhiko Okumura. LZSS data works on a control byte scheme.
Each block in the file begins with a single byte indicating how much of the block is uncompressed (\'literal data\'), and how much is compressed (\'references\'). You read the bits LSB-first, with 0=reference, 1=literal.

Literal data means just that: read one byte in from the source (compressed) data, and write it straight to the output.

References take up two bytes, and are essentially a pointer to a piece of data that\'s been written out (i.e. is part of the data you\'ve already decompressed). LZSS uses a 4KiB buffer, so it can only reference data in the last 4KiB of data.

#### Reference format {#reference_format}

A reference takes up two bytes, and has two pieces of information in it: offset (where to find the data, or which piece of data is going to be repeated), and length (how long the piece of data is going to be). The two reference bytes look like this:

`OOOOOOOO  OOOOLLLL`\
\
`(O = Offset, L = Length)`

The 1st byte it the least significant byte of the offset. The second byte has the remaining 4 bits of the offset as it\'s **high** nibble, so some shifting is required to extract it properly. The remaining 4 bits is the length minus 3.

So you get a 12-bit offset and a 4-bit length, but both of these values need modifying to work on directly. The length is easy to work with: just add 3 to it. This is because if a piece of repeated data was less than 3 bytes long, you wouldn\'t bother repeating it - it\'d take up no more space to actually just put literal data in. So all references are at least 3 in length. So a length of 0 means 3 bytes repeated, 1 means 4 bytes repeated, so on.

Since we have 4 bits available, that gives us a final length ranging from 3-18 bytes long. That also means the absolute maximum compression we can ever get using LZSS is a touch under 9:1, since the best possible is to replace 18 bytes of data with two bytes of reference, and then you have to add control bytes as well.

Offset needs a bit work doing on it, depending on how you\'re actually holding your data. If all you have is an input buffer and an output buffer, what you really need is an output position in your buffer to start reading data from. In other words, if you\'ve already written 10,000 bytes to your output, you want to know where to retrieve the repeated data from - it could fall anywhere in the past 4K of data (i.e. from 5904 through to 9999 bytes).

Here\'s how you get it:

`real_offset = tail - ((tail - 18 - raw_offset) mod 4096)`

Here, \'tail\' is your current output position (eg. 10,000), \'raw_offset\' is the 12-bit data value you\'ve retrieved from the compressed reference, and \'real_offset\' is the position in your output buffer you can begin reading from. This is a bit complex because it\'s not exactly the way LZSS traditionally does decompression.

If you use a 4KiB buffer, you can use the offset directly. The offset is absolute, and not relative to the cursor position or the position in the input stream. You should initialize the buffer position to 0xFEE and not zero. The buffer content should be initialized to zero.

Once you\'ve got to the start position for your reference, you just copy the appropriate length of data over to your output, and you\'ve dealt with that piece of data.

#### Example

If we\'re at position 1000 in our output, and we need to read in a new control byte because we\'ve finished with the last one. The next data to look it is:

`0xFC, 0x53, 0x12 .....`

We read in a control byte: 0xFC. In binary, that\'s 11111100. That informs us that the current block of data has two compressed offsets (@ 2 bytes each), followed by 6 literal data bytes. Once we\'d read in the next 10 bytes (the compressed data plus the literal data), we\'d be ready to read in our next control byte and start again.

Looking at the first compressed reference, we read in \$53 \$12. That gives us a base offset of \$153 (the 53 from the first byte, and the \'1\' from the second byte makes up the higher nybble). The base length is \$2 (we just take the low nybble of the second byte).

Our final length is obviously just 5.

Our position in output is still 1000. So our final offset is:

`= 1000 - ((1000 - 18 - 339) and $FFF)`\
` `

The 339 is just \$153 in decimal. The (and \$FFF) is a quick way to do modulus 4096.

`= 1000 - (643 and 0xFFF)`\
` = 1000 - 643`\
` = 357`\
` `

So our final offset is 357. We go to position 357 in our output data, read in 5 bytes (remember the length?), then write those 5 bytes out to our output. Now we\'re ready to read in the next bit of data (another compressed reference), and do the procedure again.

#### Complications

Unfortunately, that doesn\'t quite cover everything - there\'s two more things to be aware of when decompressing data that will ruin you when using FF7 files, since they do use these features.

First, if you end up with an negative offset, i.e. reading data from \'before the beginning of the file\', write out nulls (zero bytes). That\'s because the compression buffer is, by default, initialized to zeros; so it\'s possible, if the start of the file contains a run of zeros, that the file may reference a block you haven\'t written. For example, if you\'re at position 50 in your output, it\'s possible you may get an offset indicating to go back 60 bytes to offset -10. If you have to read 5 bytes from there, you just write out 5 nulls. However, you could have to read 15 bytes from there. In that case, you write out 10 nulls (the part of the data \'before\' the file start), then the 5 bytes from the beginning of the file.

Secondly, you can have a repeated run. This is almost the opposite problem: when you go off the end of your output. Say you\'re at offset 100 in your output, and you have to go to offset 95 to read in a reference. This is okay, but if the reference length is \>5, you loop the output. So if you had to write out 15 bytes, you\'d write out the five bytes that were available, then write them out again, then again, to make up the 15 bytes you needed.

The FF7 files use both of these \'tricks\', so you can\'t ignore them.

If you use a circular 4KiB buffer, you can ignore these issues completely, as long as you do a one-byte-at-a-time copy for the references.

---

# FF7/LGP format {#ff7lgp_format}

- [FF7/LGP format](#ff7lgp_format){#toc-ff7lgp_format}
  - [LGP Archive format for PC by Ficedula](#lgp_archive_format_for_pc_by_ficedula){#toc-lgp_archive_format_for_pc_by_ficedula}


### LGP Archive format for PC by [Ficedula](User:Ficedula "Ficedula"){.wikilink} {#lgp_archive_format_for_pc_by_ficedula}

This section explains how the LGP archives from FF7 PC are constructed. If you\'re looking for a tool that already manages LGP archives, try [Ficedula](User:Ficedula "Ficedula"){.wikilink}\'s [LGP Editor](http://sylphds.net/f2k3/index.html).

Essentially the LGP file is split up into four (maybe less, depending on how you count it) sections.

1.  File header/Table of contents
2.  CRC code
3.  Actual data
4.  File terminator

#### Section 1: File Header {#section_1_file_header}

This contains two parts: A header of fixed size, then the table of contents.

The first item is 12 bytes containing the file creator. This is a standard string, except it is \"rightaligned\". In other words the blank space comes before the actual text, not after. In FF7 it\'s always \"SQUARESOFT\" preceded by two nulls to make it 12 bytes. The only other thing you might see is the header \"FICEDULA-LGP\", which I use to indicate a file is an LGP \*patch\* one of my programs has constructed, not a complete archive.

Next is a four-byte integer saying how many files the archive contains.

Following this is the table of contents (TOC): One entry per file.

Each entry in the TOC has the following structure:

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>20 bytes</p></td>
<td><p>Null terminated string, giving filename</p></td>
</tr>
<tr>
<td><p>4 byte integer</p></td>
<td><p>Position in this file where data starts for the file</p></td>
</tr>
<tr>
<td><p>1 byte</p></td>
<td style="background: rgb(155,155,104)"><p>Some sort of check code. File attributes? Normally seems to be<br />
14 but it does vary.</p></td>
</tr>
<tr>
<td><p>2 byte short</p></td>
<td style="background: rgb(155,155,104)"><p>Something to do with duplicate file names. If a name is unique it is 0, otherwise it is assigned a value based on existing duplicates. (Hard to explain)</p></td>
</tr>
</tbody>
</table>

#### Section 2: CRC Code {#section_2_crc_code}

This code is used to validate the LGP archive. The bad news is I have no idea how to make it (I\'ve figured out how to decode it, ie. find out whether the archive is valid, but I can\'t create my own). The good news is you don\'t need to! The only thing this CRC is based on is the number of files in the archive (maybe the filenames too, haven\'t checked that). Anyway, the TOC is the only thing this check relates to. So if you\'re replicating an archive from FF7 for use in the game with the same number of files and filenames you can just copy the CRC section from an existing file.

Normally it\'s 3602 bytes long (one archive may be different, possibly MAGIC.LGP). Anyway, one normally-safe way of calculating the CRC size is to find the end of the TOC and the beginning of the first file. Anything in between is probably CRC code (this is not guaranteed to work. It works with \"official\" archives but editors - such as [LGP Editor](http://www.ficedula.com/) - can alter the TOC to achieve extra things).

#### Section 3: Actual Data {#section_3_actual_data}

The data from the files. However it\'s not that simple: the TOC doesn\'t list how long each file is (somewhat useful). It\'s done here. The offset in the TOC is actually the position of yet another file header. Format is:

|   Size   | Description                             |
|:--------:|-----------------------------------------|
| 20 bytes | Null terminated string, giving filename |
| 4 bytes  | File length                             |
|  Varies  | The file data itself                    |

#### Section 4: Terminator {#section_4_terminator}

After the last piece of data comes the file descriptor. This is a simple string, except instead of being null-terminated it\'s terminated by the end of the file. It\'s \"FINAL FANTASY 7\" for all archives, except LGP patches, where it\'s \"LGP PATCH FILE\".

#### Notes

The game is remarkably flexible about LGP archives. So long as the TOC and the CRC data is intact it\'ll accept just about anything.

- Example 1: The filename in the TOC and in the actual file header don\'t have to match. It only checks the TOC.
- Example 2: You can point two entries in the TOC at the same data and it works.
- Example 3: You can have ANY junk in the data section so long as all the TOC entries point to a valid file header. Not every piece of data has to be \"accounted\" for by the TOC. There can be data not used.

[LGP Editor](http://www.ficedula.com/) uses this to its advantage in the Advanced Editor. If you want to replace a file in an LGP archive with your own copy, it just puts the file on the end of the LGP, writes a new file terminator, and updates the TOC to point at the new file. It even lets you link two TOC entries to the same data or have \"inactive\" files in the archive that aren\'t referenced by any TOC entry.

I don\'t know whether the file terminator has to be intact, but for safety\'s sake my editor preserves it. The CRC must be present and correct. Also, if you\'re replacing an archive with you\'re own custom version make sure it has filenames in the TOC matching the ones in the old one.

The game doesn\'t check archive sizes as long as all filenames are present. So if you want, you could replace an archive containing 95 files with a 98-file archive, so long as 95 of those 98 names matched those present in the original 95-file archive. (However there\'s no point in doing this when the game won\'t use any files other than the 95 it\'s expecting to find).

There are reports on [Qhimm\'s board](http://forums.qhimm.com/) that once you\'ve altered an archive and the game refuses to read it, it won\'t ever read it until you reinstall - even if you fix the problem/restore from a backup. The idea was generally scorned and ignored, but I\'ll mention it because something like that happened to me. No solid conclusion can be drawn here.

Sometimes, there are data \"gaps\" in the file that don\'t appear to be referenced by any file - even by an inactive file. If you\'re only using the TOC method to get at files (the easy way) then you won\'t notice this anyway. However, if you\'re stepping through the file header by header, even reading the unused ones, this can cause problems. If you use my program to update a file with one that\'s smaller than the original (can happen) then it writes it in, but leaves a gap after it (of course). However, to help you out, after the end of the file, it writes a 4 byte integer saying how much more space to skip over to reach the next file header. This really doesn\'t affect many things - only tools (like my Advanced LGP Editor) that bypass the TOC to construct their own file lists. FF7 never notices a thing.

### Useful downloads {#useful_downloads}

Below there are links to known programs that are capable to edit LGP archives:

- [LGP Tools](http://www.sylphds.net/f2k3/programs/lgptools/lgptools160.zip) - with an Advanced LGP Editor allowing edit archive thoughoutly
- [Emerald](http://elentor.com/Projetos/FF7-Tools/Extracting/Emerald.zip) - has mass extracting/repacking function
- [Unmass](http://mirex.mypage.sk/index.php?selected=1#Unmass) - general file extractor with LGP archives support

---

# PSX/TIM format {#psxtim_format}

- [PSX/TIM format](#psxtim_format){#toc-psxtim_format}
  - [Introduction](#introduction){#toc-introduction}
  - [File layout](#file_layout){#toc-file_layout}
  - [Header](#header){#toc-header}
  - [CLUT (color lookup table)](#clut_color_lookup_table){#toc-clut_color_lookup_table}
  - [Image data](#image_data){#toc-image_data}



## Introduction

A TIM file is a standard image file format for the [Sony PlayStation](PSX "Sony PlayStation"){.wikilink}. The file structure closely mimics the way textures are managed in the [frame buffer](PSX/frame_buffer "frame buffer"){.wikilink} by the [GPU](PSX/GPU "GPU"){.wikilink}. TIM files are [little endian](Little_endian "little endian"){.wikilink}-based.

\

## File layout {#file_layout}

A TIM file is made up of three conceptual blocks; the header, the color lookup table (CLUT) and the image data. The CLUT block and the image data block have the same basic layout and are also treated the same way when loading a TIM file into the PlayStation frame buffer. Also, the CLUT block is optional and technically does not need to be present, even when the image data consists of color indices. Such image data is assumed to refer to *some* color lookup table, but not necessarily one stored in the same TIM file. In almost all cases though, the CLUT is included in the same TIM file as the image data using it and can thus be assumed to be applicable.

<center>

![](PSX_TIM_file_layout.png "PSX_TIM_file_layout.png")

</center>

\

## Header

The header starts with a \'tag\' byte; this value is constant for all TIM files and must be 0x10. The immediately following byte denotes the version of the file format. At present, only version \'0\' TIM files are known to exist.

The next 32-bit word contains specific flags denoting the basic properties of the TIM file. The BPP (Bits Per Pixel) value denotes the bit depth of the image data, according to the following values:

**`00`**`  4-bit (color indices)`\
**`01`**`  8-bit (color indices)`\
**`10`**`  16-bit (actual colors)`\
**`11`**`  24-bit (actual colors)`

The CLP (Color Lookup table Present) flag simply denotes whether the CLUT block is present in the TIM file. This flag is typically set when BPP is 00 or 01, and cleared otherwise.

\

## CLUT (color lookup table) {#clut_color_lookup_table}

The CLUT starts with a simple 32-bit word telling the length, in bytes, of the entire CLUT block (including the header). Following that is a set of four 16-bit values telling how the CLUT data should be loaded into the frame buffer. These measurements are in frame buffer pixels, which are 16-bit. Each CLUT is stored in a rectangular portion of the frame buffer, which is typically 16 or 256 pixels wide (corresponding to 4-bit or 8-bit color indices). The rows define one or more \'palettes\' which can be selected at runtime to use when drawing a color-indexed image.

<center>

![](PSX_TIM_file_clut.png "PSX_TIM_file_clut.png")

</center>

The length of the CLUT data is always *width* ï¿½ *height* ï¿½ 2 bytes, precisely the amount of data needed to fill a rectangular area of *width* ï¿½ *height* pixels in the frame buffer. Also, the x coordinate of the CLUT needs to be an even multiple of 16, but the y coordinate can be any value between 0-511. Typically they are stored directly under the front/back buffers. Each 16-bit value is interpreted as real color frame buffer pixels, which have the following format:

<center>

![](PSX_color_formats_16.png "PSX_color_formats_16.png")

</center>

The red, green and blue samples behave like any RGB-defined color, but the STP (special transparency processing) bit has varying special meanings. Depending on the current transparency processing mode, it denotes if pixels of this color should be treated as transparent or not. If transparency processing is enabled, pixels of this color will be rendered transparent if the STP bit is set. A special case is black pixels (RGB 0,0,0), which **by default** are treated as transparent by the PlayStation *unless* the STP bit is set.

\

## Image data {#image_data}

The image block is structurally identical to the CLUT block and is processed in exactly the same way when loaded into the frame buffer. It starts with a 32-bit word telling the length, in bytes, of the entire image block, then has 4 16-bit values containing the frame buffer positioning information. After that follows the image data, which is always *width* ï¿½ *height* ï¿½ 2 bytes long. It is important to realize that the image measurements are in 16-bit frame buffer pixels, which does not necessarily correspond to the size of the contained image. It may help to visualize the entire image data as a *width* ï¿½ *height* array of 16-bit values, which is then interpreted differently depending on color mode (this is exactly how the PlayStation treats it). To calculate the actual image dimensions, it is thus necessary to take into account the current BPP value (bits per pixel).

<center>

![](PSX_TIM_file_image.png "PSX_TIM_file_image.png")

</center>

The image data, while loaded straight into the frame buffer, is structured differently depending on the bit depth of the image. To a TIM file reader, the image data is parsed as a series of 16-bit values with varying interpretations. The most straight-forward interpretation is for 16-bit images (BPP = **10**), in which case the image data has the same format as the frame buffer pixels themselves:

<center>

![](PSX_color_formats_16.png "PSX_color_formats_16.png")

</center>

The PlayStation is also capable of handling data in 24-bit color (BPP = **11**), in which case the color samples are stored as 3-byte groups. In the event that an image\'s width is an uneven number of pixels, the last byte is left as padding; the first pixel of a new row is always stored at the corresponding first pixel of the frame buffer row. The color samples are stored in the following order:

<center>

![](PSX_color_formats_24.png "PSX_color_formats_24.png")

</center>

Apart from the two \"real\" color modes, the PlayStation frequently utilizes color indexed images via CLUTs (color lookup tables). Whenever an image with color index data is drawn to the screen, a reference to a CLUT is included and the color indices get replaced with the corresponding value in the table. For 8-bit indexed colors (BPP = **01**), the image pixels are stored two by two in each 16-bit value as follows:

<center>

![](PSX_color_formats_8.png "PSX_color_formats_8.png")

</center>

These images are used in conjuction with a 256-pixel CLUT. For less color-rich images, 4-bit index colors (BPP = **00**) are also available, for use with a 16-pixel CLUT. These pixels are stored four by four in each 16-bit value:

<center>

![](PSX_color_formats_4.png "PSX_color_formats_4.png")

</center>


---

## Images

![PSX TIM file layout](images/PSX_TIM_file_layout.png)

![PSX TIM file clut](images/PSX_TIM_file_clut.png)

![PSX color formats 16](images/PSX_color_formats_16.png)

![PSX TIM file image](images/PSX_TIM_file_image.png)

![PSX color formats 16](images/PSX_color_formats_16.png)

![PSX color formats 24](images/PSX_color_formats_24.png)

![PSX color formats 8](images/PSX_color_formats_8.png)

![PSX color formats 4](images/PSX_color_formats_4.png)


---

# FF7/TEX format {#ff7tex_format}

- [FF7/TEX format](#ff7tex_format){#toc-ff7tex_format}
  - [TEX Texture Data Format for PC by Mirex (Edits by Aali)](#tex_texture_data_format_for_pc_by_mirex_edits_by_aali){#toc-tex_texture_data_format_for_pc_by_mirex_edits_by_aali}



## TEX Texture Data Format for PC by [Mirex](User:Mirex "Mirex"){.wikilink} (Edits by [Aali](User:Aali "Aali"){.wikilink}) {#tex_texture_data_format_for_pc_by_mirex_edits_by_aali}

FF7 PC texture consists of header, an optional palette and bitmap data. Usually data are stored like palletized picture, with bitmap pixels referencing to palette. Color 0 (in palette its usually black) is usually used as transparent color.

*Pixel values of 0 may or may not be transparent, depending on the color key status, more on that later. This also applies to non-paletted formats.*

When bit depth is 16 then data are stored as packed RGB in style RGB555, which means 5 bits per color in one 2 byte entry. I\'m not sure if it is used in FF7 at all, its probably used in FF8.

*The tex format is actually very flexible and can take almost any non-paletted format as long as you describe it properly in the header.*

<table>
<thead>
<tr>
<th style="border: 1px grey; vertical-align: middle; width: 51px; height: 26px; background-color: rgb(130, 130, 130)"><p>Offset</p></th>
<th style="border: 1px grey; vertical-align: middle; width: 126px; height: 26px; background-color: rgb(130, 130, 130)"><p>Size</p></th>
<th style="border: 1px grey; vertical-align: middle; width: 222px; height: 26px; background-color: rgb(130, 130, 130)"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Header</p></td>
</tr>
<tr>
<td><p>0x00</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Version, must be 1, or FF7 won't load the file</p></td>
</tr>
<tr>
<td><p>0x04</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x08</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Color key flag</p></td>
</tr>
<tr>
<td><p>0x0C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x10</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x14</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Minimum bits per color (D3D driver uses these to determine which texture format to convert to on load)</p></td>
</tr>
<tr>
<td><p>0x18</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Maximum bits per color</p></td>
</tr>
<tr>
<td><p>0x1C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Minimum alpha bits</p></td>
</tr>
<tr>
<td><p>0x20</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Maximum alpha bits</p></td>
</tr>
<tr>
<td><p>0x24</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Minimum bits per pixel</p></td>
</tr>
<tr>
<td><p>0x28</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Maximum bits per pixel</p></td>
</tr>
<tr>
<td><p>0x2C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x30</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of palettes</p></td>
</tr>
<tr>
<td><p>0x34</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of colors per palette</p></td>
</tr>
<tr>
<td><p>0x38</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bit depth</p></td>
</tr>
<tr>
<td><p>0x3C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Image Width</p></td>
</tr>
<tr>
<td><p>0x40</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Image Height</p></td>
</tr>
<tr>
<td><p>0x44</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Pitch or bytes per row, usually ignored and assumed to be bytes per pixel * width</p></td>
</tr>
<tr>
<td><p>0x48</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x4C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Palette flag (this indicates the presence of a palette)</p></td>
</tr>
<tr>
<td><p>0x50</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bits per index, always 0 for non-paletted images</p></td>
</tr>
<tr>
<td><p>0x54</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Indexed-to-8bit flag, never used in FF7</p></td>
</tr>
<tr>
<td><p>0x58</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Palette size, always number of palettes * colors per palette</p></td>
</tr>
<tr>
<td><p>0x5C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of colors per palette (again, may be 0 sometimes, the other value will be used anyway)</p></td>
</tr>
<tr>
<td><p>0x60</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data, ignored on load</p></td>
</tr>
<tr>
<td><p>0x64</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bits per pixel</p></td>
</tr>
<tr>
<td><p>0x68</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bytes per pixel, always use this to determine how much data to read, if this is 1 you read 1 byte per pixel, regardless of bit depth</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: black; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: black; border-width: 1px"><p>Pixel format (all 0 for paletted images)</p></td>
</tr>
<tr>
<td><p>0x6C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of red bits</p></td>
</tr>
<tr>
<td><p>0x70</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of green bits</p></td>
</tr>
<tr>
<td><p>0x74</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of blue bits</p></td>
</tr>
<tr>
<td><p>0x78</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of alpha bits</p></td>
</tr>
<tr>
<td><p>0x7C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Red bitmask</p></td>
</tr>
<tr>
<td><p>0x80</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Green bitmask</p></td>
</tr>
<tr>
<td><p>0x84</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Blue bitmask</p></td>
</tr>
<tr>
<td><p>0x88</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Alpha bitmask</p></td>
</tr>
<tr>
<td><p>0x8C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Red shift</p></td>
</tr>
<tr>
<td><p>0x90</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Green shift</p></td>
</tr>
<tr>
<td><p>0x94</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Blue shift</p></td>
</tr>
<tr>
<td><p>0x98</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Alpha shift</p></td>
</tr>
<tr>
<td><p>0x9C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Always 8 - Number of red bits (Not sure what the point of these fields is, they're always ignored anyway)</p></td>
</tr>
<tr>
<td><p>0xA0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>8 - Number of green bits</p></td>
</tr>
<tr>
<td><p>0xA4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>8 - Number of blue bits</p></td>
</tr>
<tr>
<td><p>0xA8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>8 - Number of alpha bits</p></td>
</tr>
<tr>
<td><p>0xAC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Red max</p></td>
</tr>
<tr>
<td><p>0xB0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Green max</p></td>
</tr>
<tr>
<td><p>0xB4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Blue max</p></td>
</tr>
<tr>
<td><p>0xB8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Alpha max</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: black; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: black; border-width: 1px"><p>End of pixel format</p></td>
</tr>
<tr>
<td><p>0xBC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Color key array flag (this indicates the presence of a color key array)</p></td>
</tr>
<tr>
<td><p>0xC0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xC4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Reference alpha (more on this later)</p></td>
</tr>
<tr>
<td><p>0xC8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xCC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xD0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Palette index (runtime data)</p></td>
</tr>
<tr>
<td><p>0xD4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xD8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xDC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xE0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xE4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xE8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Palette data (ignore this section if palette flag is 0)</p></td>
</tr>
<tr>
<td style="border: 1px grey; vertical-align: top"><p>0xEC</p></td>
<td style="border: 1px grey; vertical-align: top"><p>Palette size * 4</p></td>
<td style="border: 1px grey; vertical-align: top"><p>The raw palette data, always in 32-bit BGRA format</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Pixel data</p></td>
</tr>
<tr>
<td style="border: 1px grey; vertical-align: top"><p>Varies</p></td>
<td colspan="2" style="border: 1px grey; vertical-align: top"><p>Read width * height * "bytes per pixel" bytes of data. If there's a palette, every pixel is an index into that palette, otherwise use the pixel format specification.</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Color key array</p></td>
</tr>
<tr>
<td style="border: 1px grey; vertical-align: top"><p>Varies</p></td>
<td colspan="2" style="border: 1px grey; vertical-align: top"><p>Number of palettes * 1 bytes.</p></td>
</tr>
</tbody>
</table>

*Color keying: If the color key flag is zero, no color keying is performed and the color key array is ignored. Otherwise, the current palette index is used to retrieve a single byte from the color key array, this is the new color key flag, zero means don\'t do color keying.* If there is no color key array (and the color key flag is not zero), you should always color key.

*Reference alpha: Only applies to paletted images, if the alpha value sampled from the palette is 0xFE, this value should be replaced with the reference alpha.*

---


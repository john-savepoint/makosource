<!--
MERGE METADATA
Created: 2025-11-29 10:50 JST
Original file: FF7_World_Map_TXZ.md (76 lines)
Major section analyzed: 07_WORLD_MAP.md (86 lines)
Merge status: NO ADDITIONS REQUIRED
Reasoning: Individual file covers TXZ archive format (PSX). Major section contains PC encounter data, which belongs in FF7_WorldMap_Module.md. No scope overlap.
Images adjusted: 0 (none found)
Analysis report: comparisons/FF7_World_Map_TXZ_vs_07_WORLD_MAP_analysis.md
Session notes: Encounter data (lines 7-72 of major section) should be extracted to worldmap module documentation separately.
-->

# FF7/World Map/TXZ {#ff7world_maptxz}

- [FF7/World Map/TXZ](#ff7world_maptxz){#toc-ff7world_maptxz}
  - [WM0.TXZ](#wm0.txz){#toc-wm0.txz}


## WM0.TXZ

The following information applies specifically to WM0.TXZ, it is reasonable to assume that the rest of the TXZ files use a similar format, where WM2.TXZ and WM3.TXZ presumably holds equivalent data for the underwater and snowfield maps respectively.

### Compression

TXZ files are compressed using standard LZS compression where the first 4 bytes contain the size of the compressed data.

### TXZ archive format {#txz_archive_format}

Uncompressed TXZ files are divided into several different sections, to extract the different sections a header must be parsed at the beginning of the file. The first 4 bytes will tell you how many sections there are. After that follows 4 \* `<number of sections>`{=html} bytes containing offsets into the file for each section. A section can be assumed to end where the next section begins and the last section runs until the end of the file. Offsets do not include the first 4 bytes of the file! Add 4 to get the actual file offset for each section.

## Sections

### WM0.TXZ, section 0 {#wm0.txz_section_0}

Unknown format, might be a model? Looks like there\'s atleast one or two textures in there.

### WM0.TXZ, section 1 {#wm0.txz_section_1}

Texture data for direct VRAM upload, same format as section 2 but contains only a single block.

### WM0.TXZ, section 2 {#wm0.txz_section_2}

Texture data for the worldmap mesh (see .MAP format), starts with a table of 512 palette/texture identifiers in a format compatible with the PSX GPU, see <http://psx.rules.org/gpu.txt> for more information.

The following structure can be used to read this data:

```c
struct wm_texture
{
   unsigned int clutx:6;
   unsigned int cluty:10;
   unsigned int tx:4;
   unsigned int ty:1;
   unsigned int abr:2;
   unsigned int tp:2;
   unsigned int reserved:7;
};
```

Texture IDs are the same for the PSX and PC version which means that this table maps 1:1 to the table of PC textures which can be found here: [FF7/WorldMap_Module/TextureTable](FF7/WorldMap_Module/TextureTable "FF7/WorldMap_Module/TextureTable"){.wikilink}

After this table follows a number of blocks intended for direct VRAM upload, each block has the following structure:

*VRAM Block*

|            size            |              description              |
|:--------------------------:|:-------------------------------------:|
|          4 bytes           | Size of this block (including header) |
|          2 bytes           |       Destination X coordinate        |
|          2 bytes           |       Destination Y coordinate        |
|          2 bytes           |                 Width                 |
|          2 bytes           |                Height                 |
| Width \* Height \* 2 bytes |              Pixel data               |


A new block can be assumed to start where the previous one ends until the end of this section is reached.

### WM0.TXZ, section 3 {#wm0.txz_section_3}

Unknown format, contains more blocks of VRAM data.

### WM0.TXZ, section 4 {#wm0.txz_section_4}

Contains the script for the overworld map, a copy of the data in wm0.ev?

### WM0.TXZ, section 5-11 {#wm0.txz_section_5_11}

These sections contain songs in standard AKAO format. Presumably the different overworld background themes are in there, don\'t know what else?

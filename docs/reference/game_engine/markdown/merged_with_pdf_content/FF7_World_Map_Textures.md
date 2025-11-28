# FF7 World Map Textures

<!--
MERGE METADATA
Created: 2025-11-28 22:20 JST
File Type: NEW FILE CREATION (consolidation of texture documentation)
Source Files: FF7_World_Map_TXZ.md, FF7_WorldMap_Module.md
Major Section: 07_WORLD_MAP.md (no new texture content found)
Content: TXZ archive texture format, texture coordinates, VRAM layout
Report: ../comparisons/FF7_World_Map_Textures_vs_07_WORLD_MAP_analysis.md
-->

---

## Overview

The world map textures in Final Fantasy VII are stored in TXZ archive files that contain compressed texture data formatted for direct VRAM upload on the PSX. This documentation covers the TXZ archive format, texture data structures, and VRAM layout for world map rendering.

Three world map texture files exist:
- **WM0.TXZ**: Above water world map textures
- **WM2.TXZ**: Underwater (submarine) map textures
- **WM3.TXZ**: Snowstorm map textures

The texture data uses PSX GPU-compatible format with palette identifiers and direct VRAM coordinates for rendering.

---

## TXZ Archive Format

### Compression

TXZ files are compressed using standard LZS compression where the first 4 bytes contain the size of the compressed data.

### Archive Structure

Uncompressed TXZ files are divided into several different sections. To extract the different sections, a header must be parsed at the beginning of the file. The first 4 bytes will tell you how many sections there are. After that follows 4 * `<number of sections>` bytes containing offsets into the file for each section. A section can be assumed to end where the next section begins and the last section runs until the end of the file. Offsets do not include the first 4 bytes of the file! Add 4 to get the actual file offset for each section.

---

## Texture Sections

The following sections are defined in WM0.TXZ (similar structure applies to WM2.TXZ and WM3.TXZ):

### Section 0

Unknown format, might be a model. Looks like there's atleast one or two textures in there.

### Section 1

Texture data for direct VRAM upload, same format as section 2 but contains only a single block.

### Section 2: Worldmap Mesh Textures

This section contains texture data for the worldmap mesh (see MAP format), starts with a table of 512 palette/texture identifiers in a format compatible with the PSX GPU, see http://psx.rules.org/gpu.txt for more information.

The following structure can be used to read this data:

```c
struct wm_texture
{
   unsigned int clutx:6;
   unsigned int cluty:10;
   unsigned int tx:4;
   unsigned int ty:1;
   unsigned int abr:2;
   unsigned int tp:2;
   unsigned int reserved:7;
};
```

**Field Descriptions**:
- `clutx` (6 bits): Color Lookup Table X coordinate
- `cluty` (10 bits): Color Lookup Table Y coordinate
- `tx` (4 bits): Texture X coordinate block
- `ty` (1 bit): Texture Y coordinate block
- `abr` (2 bits): Alpha Blend Rate mode
- `tp` (2 bits): Texture Page size mode (4-bit, 8-bit, 16-bit)
- `reserved` (7 bits): Reserved/unused bits

Texture IDs are the same for the PSX and PC version which means that this table maps 1:1 to the table of PC textures which can be found in the TextureTable reference.

#### VRAM Block Structure

After this table follows a number of blocks intended for direct VRAM upload, each block has the following structure:

| Size | Description |
|:----:|:-----------|
| 4 bytes | Size of this block (including header) |
| 2 bytes | Destination X coordinate |
| 2 bytes | Destination Y coordinate |
| 2 bytes | Width |
| 2 bytes | Height |
| Width × Height × 2 bytes | Pixel data |

A new block can be assumed to start where the previous one ends until the end of this section is reached.

### Section 3

Unknown format, contains more blocks of VRAM data.

### Section 4

Contains the script for the overworld map, a copy of the data in wm0.ev.

### Sections 5-11

These sections contain songs in standard AKAO format. Presumably the different overworld background themes are in there.

---

## Texture Coordinates and Mapping

### UV Coordinate System

The lower 9 bits of the texture info field in the worldmap mesh contain a texture number (0-511, but only 0-281 appear to be used). The UV coordinates found in the mesh data are (presumably) the original PSX VRAM coordinates.

To get the real coordinates, you must **subtract a texture-specific offset from each of the UV pairs**. A complete table with every texture, its original size and offsets can be found in the TextureTable reference.

### Negative Coordinates

Sometimes you will end up with negative values after subtracting the offsets. This is normal. The texture should be assumed to repeat itself indefinitely in all directions.

---

## Related Documentation

This file documents texture handling for world map rendering. Related topics are covered in:

- **FF7_WorldMap_Module.md**: MAP/BOT file formats, mesh structure, texture references in triangles
- **FF7_World_Map_TXZ.md**: Alternative/detailed texture archive format reference
- **FF7_World_Map_BSZ.md**: Character model format (uses texture references)
- **FF7_WorldMap_Module_Script.md**: World map scripting (may reference textures)

See PSX_TIM_format.md for more information on PSX texture and color formats.

---

## Implementation Notes

### PC Version Compatibility

While texture IDs are identical between PSX and PC versions, the PC version may handle VRAM differently. Verify texture coordinate mappings when porting PSX texture data to PC.

### Texture Table

The TextureTable reference (not included in this documentation) contains:
- Texture ID
- Original size
- VRAM offset (X, Y coordinates)
- Palette offset (if applicable)

This table is essential for correctly mapping UV coordinates in the mesh data to actual texture locations.

### Offset Calculation

The process for rendering worldmap textures:
1. Read triangle UV coordinates from mesh data
2. Look up texture ID in VRAM texture identifier table
3. Retrieve texture-specific offset from TextureTable
4. Subtract offset from UV coordinates
5. Allow texture wrapping for negative coordinates
6. Render triangle with offset UV coordinates


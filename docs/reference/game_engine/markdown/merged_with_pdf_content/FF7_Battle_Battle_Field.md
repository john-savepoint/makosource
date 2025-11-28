<!--
MERGE METADATA
Created: 2025-11-28
Original File: FF7_Battle_Battle_Field.md (40 lines)
Major Section Source: 06_BATTLE_MODULE.md (lines 1458-1502)
Extracted Content: PSX 3D Battle Scenes by Micky (45 lines)
Images Adjusted: 0
Analysis Report: comparisons/FF7_Battle_Battle_Field_vs_06_BATTLE_MODULE_analysis.md
-->

# FF7/Battle/Battle Field {#ff7battlebattle_field}

- [FF7/Battle/Battle Field](#ff7battlebattle_field){#toc-ff7battlebattle_field}
  - [Settings (first file)](#settings_first_file){#toc-settings_first_file}
  - [PSX 3D Battle Scenes Architecture](#psx_3d_battle_scenes_architecture){#toc-psx_3d_battle_scenes_architecture}



Battle fields are simple 3d models drawed in 3d space.

They stored in directories STAGE1 and STAGE2. There are lzs archives that unpacked and loaded in PSX space 0x801590e4. Size of unpacked field must be less than 0x8d04. It consist from few concatenated files. First one is settings for field. Last one is texture. All others are meshes.

### Settings (first file) {#settings_first_file}

<table>
<thead>
<tr>
<th style="text-align: center; background: rgb(104,104,104);"><p>Offset</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Size</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Value</p></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><p>0</p></td>
<td style="text-align: center;"><p>1 byte</p></td>
<td style="text-align: center;"><p>Type of 3d mesh. There are 6 type of meshes:<br />
0 - mesh with horisontal scrolling parts (field 47 - Corel Train Battle).<br />
1 - normal static mesh.<br />
2 - mesh with vertical scrolling parts (field 12 - Shinra Elevators).<br />
3 - mesh with lifestream (field 4e - Final Battle - Sephiroth).<br />
4 - mesh with rotating parts (field 39 - Safer Battle)<br />
5 - normal static mesh, same as 1. (field 01,44,45 - Bizarro Battles)</p></td>
</tr>
<tr>
<td style="text-align: center; background: rgb(155,155,104);"><p>1</p></td>
<td style="text-align: center; background: rgb(155,155,104);"><p>7 bytes</p></td>
<td style="text-align: center; background: rgb(155,155,104);"><p>unknown</p></td>
</tr>
</tbody>
</table>

<!-- EXTRACTED FROM MAJOR SECTION: 06_BATTLE_MODULE.md lines 1458-1502
     Content: PSX 3D Battle Scenes by Micky
     Author Attribution: Micky (preserved from original)
     No images to adjust (0 found in extracted content)
     This section provides detailed technical specifications for battle field
     3D mesh architecture (vertex, triangle, and quad data structures).
     These specifications are NOT in the original individual file.
-->

## PSX 3D Battle Scenes Architecture {#psx_3d_battle_scenes_architecture}

#### **PSX 3D battle Scenes by Micky**

Backgrounds are stored in probably the easiest model format used in FF7. I reconstructed this from the code for my background-to-Maya converter, so there could be errors. I haven't seen any other documentation on this, so please excuse any duplication...

The backgrounds are stored in LZS files in the STAGE1 and STAGE2 directories. They are using the ff7-standard lzs compression.

They begin with a directory: The first word is the number of sections, then there is one pointer for each sections. Each section contains a mesh for the background, except for the first that contains some unknown data and the last that contains the TIM-format texture and palettes.

Each section starts with vertex data, followed by a triangle and a quad data.

```
Vertex data:
1 u32 size of vertex data
8 byte per vertex:
3 u16 x,y,z
1 u16 pad(?)
Triangle data
1 u16 number of triangles
1 u16 texture page (among other flags)
16 bytes per triangle:
3 u16 offset into vertex table
1 u16 unknown
2 u8 u1, v1
1 u16 palette (and some other flags)
2 u8 u2, v2
```

Quad data

2 u8 u3, v3

- 1 u16 number of quads
- 1 u16 texture page (among other flags)

#### 20 bytes per quad:

- 4 u16 offset into vertex table
- 2 u8 u1, v1
- 1 u16 palette
- 2 u8 u2, v2
- 2 u8 u3, v3
- 2 u8 u4, v4
- 1 u16 unknown

Displaying the backgrounds is a bit tricky on modern graphics boards, as they don't support palletized textures anymore. Which is understandable given the large number of fetches that would be required for displaying a properly filtered texture - but not very helpful. I solved that by a pre-process that stores the palette on each pixel and then looks up the color during export.

<!-- END EXTRACTION -->

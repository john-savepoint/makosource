# FF7 WorldMap Module

**Category: World Map System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's world map system, including map structure, BSZ/TXZ formats, and scripting.

---

# FF7/WorldMap Module {#ff7worldmap_module}

- [FF7/WorldMap Module](#ff7worldmap_module){#toc-ff7worldmap_module}
  - [Preamble](#preamble){#toc-preamble}


## Preamble

The following was originaly described by Tonberry, in qhimm\'s forum. It was
completed by Ficedula sometimes later, who reversed texture data.

Additions in *italics* by Aali

### Two formats {#two_formats}

BOT and MAP files are similar; BOT files are redundant and look like
optimized versions of the corresponding MAP files.

*MAP file follows the structure described below and is used to load single blocks on demand. BOT file contains the same blocks but arranged to speed up initial load time by storing each block and 3 of its neighboring blocks together. For instance, the data stored for the first 2 blocks is (numbers refer to the MAP layout below): 0,1,9,10 1,2,10,11. This pattern repeats up to block #62. Replacement blocks 63-68 are divided in groups for each replacement, i.e. block 64 and 65 are part of the same group since they both belong to the Ultima Weapon crater. These groups are then stored using the same algorithm as above, each 4-block group containing a replaced block is written out again. 1-block replacements thus add 4\*4 blocks to the .BOT file while 2-block replacements add 6\*4 blocks. Replacements are to be made **in order**, when writing the data for the Ultima Weapon crater the Temple of the Ancients should be gone and so on. All of this adds up to 63\*4 + 4\*4 + 6\*4 + 4\*4 + 6\*4 = 332 blocks.*

### Content

- WM0 is the above water map.
- WM2 is the underwater (submarine) map.
- WM3 is the snowstorm map.

## MAP Format {#map_format}

### File Structure {#file_structure}

A worldmap file is divided in sections of 0xB800 bytes, each section
representing a square block of the map.

#### Map Block {#map_block}

Each block consists in 16 meshes, organized in a grid-like fashion:

*Map Block mesh arrangement*

|     |     |     |     |
|-----|-----|-----|-----|
| 0   | 1   | 2   | 3   |
| 4   | 5   | 6   | 7   |
| 8   | 9   | 10  | 11  |
| 12  | 13  | 14  | 15  |


A block is recorded following the structure (all pointers are expressed in bytes
relative to offset 0 of block):

*Pointers have to be aligned to 4-byte boundaries, FF7 ignores the last two bits when reading the file.*

For each m in 16 meshes:

|  size   |              description              |
|:-------:|:-------------------------------------:|
| 4 bytes | Pointer to compressed data for mesh m |

Followed by, for each m in 16 meshes:

|   size   |        description         |
|:--------:|:--------------------------:|
| variable | Compressed data for mesh m |

The data for each mesh is independently compressed using LZSS, so the
first 4 bytes are the size in bytes of the compressed data and the
rest is the compressed data itself.

#### WM0.MAP

wm0.map contains 68 blocks. The first 63 of them are arranged in a
grid-like fashion, made of 7 rows of 9 columns, like this:

*wm0.map block arrangement*

|     |     |     |     |     |     |     |     |     |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   |
| 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  |
| 18  | 19  | 20  | 21  | 22  | 23  | 24  | 25  | 26  |
| 27  | 28  | 29  | 30  | 31  | 32  | 33  | 34  | 35  |
| 36  | 37  | 38  | 39  | 40  | 41  | 42  | 43  | 44  |
| 45  | 46  | 47  | 48  | 49  | 50  | 51  | 52  | 53  |
| 54  | 55  | 56  | 57  | 58  | 59  | 60  | 61  | 62  |
|     |     |     |     |     |     |     |     |     |


The last 5 meshes 63, 64, 65, 66, 67 and 68 replaces meshes 50, 41,
42, 60, 47 and 48 (respectively), according to the story of the game.

### Mesh Structure {#mesh_structure}

A worldmap mesh is recorded like this:

#### Header

*Header Structure*

|  size   |     description     |
|:-------:|:-------------------:|
| 2 bytes | Number of triangles |
| 2 bytes | Number of vertices  |


```c
typedef struct
{
  uint16 NumberOfTriangles;
  uint16 NumberOfVertices;
} WorldMeshHeader;
```

#### Triangle

*For each triangle t in *number of triangles**

| size | description |
|:--:|:--:|
| 1 byte | Index of vertex 0 of triangle t |
| 1 byte | Index of vertex 1 of triangle t |
| 1 byte | Index of vertex 2 of triangle t |
| *5 bits (lowest)* | *Walkmap status of triangle t (see below)* |
| *3 bits* | *Unknown, probably script related* |
| 1 byte | Coordinate u in texture for vertex 0 |
| 1 byte | Coordinate v in texture for vertex 0 |
| 1 byte | Coordinate u in texture for vertex 1 |
| 1 byte | Coordinate v in texture for vertex 1 |
| 1 byte | Coordinate u in texture for vertex 2 |
| 1 byte | Coordinate v in texture for vertex 2 |
| *9 bits (lowest)* | *Texture (see below)* |
| *7 bits* | *Location (message ID that will be displayed in menus and savegames)* |


```c
typedef struct
{
 uint8 Vertex0Index;
 uint8 Vertex1Index;
 uint8 Vertex2Index;
 uint8 WalkabilityInfo:5;  // contributor addition
 uint8 Unknown:3;           // contributor addition
 uint8 uVertex0, vVertex0;
 uint8 uVertex1, vVertex1;
 uint8 uVertex2, vVertex2;
 uint16 TextureInfo:9;      // contributor addition
 uint16 Location:7;         // contributor addition
} WorldMeshTriangle;
```

#### Vertex

*For each vertex v in *number of vertices**

| size | description |
|:--:|:--:|
| 2 bytes | Coordinate x of vertex v (signed) |
| 2 bytes | Coordinate y of vertex v (signed) |
| 2 bytes | Coordinate z of vertex v (signed) |
| 2 bytes | (Unknown: Coordinate w of vertex v?) *Never used for anything in the PC version.* |


```c
typedef struct
{
  int16 X, Y, Z;
  uint16 Unused; // fill to fit structure to 32bit boundry
} VertexType;
```

#### Normal

*For each vertex v in *number of vertices**

| size | description |
|:--:|:--:|
| 2 bytes | Coordinate x of normal for vertex v |
| 2 bytes | Coordinate y of normal for vertex v |
| 2 bytes | Coordinate z of normal for vertex v |
| 2 bytes | (Unknown: Coordinate w of normal for vertex v? \"Always 0\") *Never used for anything in the PC version.* |


```c
typedef struct
{
  int16 X, Y, Z;
  uint16 Unused; // fill to fit structure to 32bit boundry
} NormalType;
```

structures added by [Cyberman](User:Cyberman "Cyberman"){.wikilink} 13:43, 10 Jan 2007 (CST)

### Walkmap

*Each triangle can have one of the 32 different walkmap types described below.*

| code | type | description |
|:--:|:--:|:--:|
| *0* | *Grass* | *Most things can go here.* |
| *1* | *Forest* | *No landing here, but anything else goes.* |
| *2* | *Mountain* | *Chocobos and flying machines only.* |
| *3* | *Sea* | *Deep water, only gold chocobo and submarine can go here.* |
| *4* | *River Crossing* | *Buggy, tiny bronco and water-capable chocobos.* |
| *5* | *River* | *Tiny bronco and chocobos.* |
| *6* | *Water* | *Shallow water, same as above.* |
| *7* | *Swamp* | *Midgar zolom can only move in swamp areas.* |
| *8* | *Desert* | *No landing.* |
| *9* | *Wasteland* | *Found around Midgar, Wutai and misc other. No landing.* |
| *10* | *Snow* | *Leaves footprints, no landing.* |
| *11* | *Riverside* | *Beach-like area where river and land meet.* |
| *12* | *Cliff* | *Sharp drop, usually where the player can be on either side.* |
| *13* | *Corel Bridge* | *Tiny bridge over the waterfall from Costa del Sol to Corel.* |
| *14* | *Wutai Bridge* | *Rickety rope bridges south of Wutai.* |
| *15* | *Unused* | *Doesn\'t seem to be used anywhere in the original data.* |
| *16* | *Hill side* | *This is the tiny walkable part at the foot of a mountain.* |
| *17* | *Beach* | *Where land and shallow water meets.* |
| *18* | *Sub Pen* | *Only place where you can enter/exit the submarine.* |
| *19* | *Canyon* | *The ground in cosmo canyon has this type, walkability seems to be the same as wasteland.* |
| *20* | *Mountain Pass* | *The small path through the mountains connecting Costa del Sol and Corel.* |
| *21* | *Unknown* | *Present around bridges, may have some special meaning.* |
| *22* | *Waterfall* | *River type where the tiny bronco can\'t go.* |
| *23* | *Unused* | *Doesn\'t seem to be used anywhere in the original data.* |
| *24* | *Gold Saucer Desert* | *Special desert type for the golden saucer.* |
| *25* | *Jungle* | *Walkability same as forest, used in southern parts of the map.* |
| *26* | *Sea (2)* | *Special type of deep water, only used in one small spot next to HP-MP cave, possibly related to the underwater map/submarine.* |
| *27* | *Northern Cave* | *Inside part of the crater, where you can land the highwind.* |
| *28* | *Gold Saucer Desert Border* | *Narrow strip of land surrounding the golden saucer desert. Probably related to the \"quicksand\" script.* |
| *29* | *Bridgehead* | *Small area at both ends of every bridge. May have some special meaning.* |
| *30* | *Back Entrance* | *Special type that can be set unwalkable from the script.* |
| *31* | *Unused* | *Doesn\'t seem to be used anywhere in the original data.* |

### Texture

The lower 9 bits contain a texture number (0-511, but only 0-281
appear to be used). *Unfortunately, knowing which texture to use is not enough, the UV coordinates found in the mesh data are (presumably) the original PSX VRAM coordinates, so to get the real coordinates you must subtract a texture-specific offset from each of the UV pairs. A complete table with every texture, its original size and offsets can be found [ here](FF7/WorldMap_Module/TextureTable " here"){.wikilink}. Sometimes you will end up with negative values after subtracting the offsets, this is normal, the texture should be assumed to repeat itself indefinitely in all directions.*

---

# FF7/World Map/BSZ {#ff7world_mapbsz}

- [FF7/World Map/BSZ](#ff7world_mapbsz){#toc-ff7world_mapbsz}



\[Lazy Bastard\]: Using a hex editor, I\'ve mapped out a BSZ file, namely WM0.BSZ - Cloud\'s world map model. Incidentally, WM1.BSZ is Tifa\'s world map model, WM2.BSZ is Cid\'s, and WM3.BSZ seems to be every other world map model, similar to a BSX in fields (though I haven\'t confirmed this yet).

There is a remarkable resemblance here to BCX format, so I should be able to create custom world map models fairly soon, using the same techniques I used in fields. \[Update: I did just that; see Qhimm.com forum threads\]

Akari: Perhaps you can use this data to implement a utility and functionality in Q-Gears?

Without further ado:

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

In PSX memory, WM0.BSZ starts at 14A600 (and ends at 14F3B7). Every 80-type offset in this file can be treated as such: offset minus 8014A600 equals in-file offset.

`<b>`{=html}\'BSZ Header Section\'`</b>`{=html} \[at offset 0x00000000\]:

Unknown (always the same) \[at offset 0x00000000\]:

`02 00 00 00 08 00 00 00`

Relative offset from end of \'BSZ Header Section\' to \'Texture Data Section\' \[at offset 0x00000008\]:

`5C 47 00 00`

Offset to Model Section, Header (offset minus 0x8014A600 equals file offset) \[at offset 0x00000010\]:

`18 A6 14 80`

Relative offset from end of \'BSZ Header Section\' to Unknown \[at offset 0x00000014\]:

`54 47 00 00`

Note: \'BSZ Header Section\' runs until \'Model Section\'.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

`<b>`{=html}\'Model Section\'`</b>`{=html} \[at offset 0x00000018\]:

`<b>`{=html}`<i>`{=html}\'Model Section\', Header`</i>`{=html}`</b>`{=html} \[at offset 0x00000018\]:

`01 FF 16 0F 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 58 00 38 02 3C A6 14 80 00 00 00 00`

01 FF - Unknown

16 - Number of bones

0F - Number of parts

0A - Number of animations

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 58 00 - Unknown

38 02 - Total data size of bones+parts (little-endian, so 0x0238)

3C A6 14 80 - Offset to \'Model Section\', Bones (little-endian, so 0x8014A63C)

00 00 00 00 - Unknown

Note: \'Model Section\', Header runs until \'Model Section\', Bones.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

`<b>`{=html}`<i>`{=html}\'Model Section, Bones\'`</i>`{=html}`</b>`{=html} \[at offset 0x0000003C\]:

`00 00 FF 00 00 00 00 01 CB FF 01 01 7B FF 02 01 CB FF 01 00 82 FF 04 00 BA FF 05 01 B7 FF 06 01 74 FF 07 01 CB FF 01 00 82 FF 09 00 BA FF 0A 01 B7 FF 0B 01 74 FF 0C 01 00 00 00 00 C4 FF 0E 01 4F FF 0F 01 39 FF 10 01 00 00 00 00 C4 FF 12 01 4F FF 13 01 39 FF 14 01`

Note: \'Model Section\', Bones runs until \'Model Section\', Parts.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

`<b>`{=html}`<i>`{=html}\'Model Section, Parts\'`</i>`{=html}`</b>`{=html} \[at offset 0x00000094\]:

`01 01 0E 00 00 00 00 00 00 00 0C 06 00 00 74 00 AC 01 AC 01 AC 01 28 02 14 A9 14 80 00 00 00 00 01 02 20 00 00 00 00 00 00 00 06 1B 00 00 04 01 80 03 80 03 80 03 74 04 C0 AA 14 80 00 00 00 00 01 03 5A 0C 02 06 00 00 00 00 96 0D 03 08 D4 02 EC 0D E0 0D 04 0E 94 13 40 AE 14 80 00 00 00 00 01 06 10 00 00 00 00 00 00 00 0A 09 00 00 84 00 D8 01 D8 01 D8 01 5C 02 4C BC 14 80 00 00 00 00 01 07 10 00 00 00 00 00 00 00 00 0E 00 00 84 00 9C 01 9C 01 9C 01 F8 01 24 BE 14 80 00 00 00 00 01 08 08 00 00 00 00 00 00 00 00 06 00 00 44 00 BC 00 BC 00 BC 00 D8 00 C0 BF 14 80 00 00 00 00 01 0B 10 00 00 00 00 00 00 00 0A 09 00 00 84 00 D8 01 D8 01 D8 01 5C 02 7C C0 14 80 00 00 00 00 01 0C 10 00 00 00 00 00 00 00 00 0E 00 00 84 00 9C 01 9C 01 9C 01 F8 01 54 C2 14 80 00 00 00 00 01 0D 08 00 00 00 00 00 00 00 00 06 00 00 44 00 BC 00 BC 00 BC 00 D8 00 F0 C3 14 80 00 00 00 00 01 0F 0A 00 00 00 00 00 00 00 08 04 00 00 54 00 24 01 24 01 24 01 70 01 AC C4 14 80 00 00 00 00 01 10 15 00 00 00 00 00 00 00 04 0E 00 00 AC 00 04 02 04 02 04 02 68 02 D0 C5 14 80 00 00 00 00 01 11 0A 00 00 00 00 00 00 00 02 07 00 00 54 00 00 01 00 01 00 01 34 01 D4 C7 14 80 00 00 00 00 01 13 0A 00 00 00 00 00 00 00 08 04 00 00 54 00 24 01 24 01 24 01 70 01 D4 C8 14 80 00 00 00 00 01 14 15 00 00 00 00 00 00 00 04 0E 00 00 AC 00 04 02 04 02 04 02 68 02 F8 C9 14 80 00 00 00 00 01 15 0A 00 00 00 00 00 00 00 02 07 00 00 54 00 00 01 00 01 00 01 34 01 FC CB 14 80 00 00 00 00`

Breakdown of first line of \'Model Section\', Parts above:

01 - Unknown; \"0 - not calculate stage lighting and color. 1 - calculate.\"

01 - Bone to which this part is attached to

0E - Number of vertices

00 - Number of Texture coord

00 - number of textured quads (Gourad Shading)

00 - number of textured triangles (Gourad Shading)

00 - number of textured quads (Flat Shading)

00 - number of textured triangles (Flat Shading)

00 - number of monochrome triangles

00 - number of monochrome quads

0C - number of gradated triangles

06 - number of gradated quads

00 00 - number of data in block 4 (flags)

74 00 - Relative offset to ?

AC 01 - Relative offset to ?

AC 01 - Relative offset to texture settings. Indexed by 5th block data (control)

AC 01 - Relative offset to one byte stream for every packet with texture

28 02 - Relative offset to ?

14 A9 14 80 - Offset to skeleton data section (little-endian, so 0x8014A914)

00 00 00 00 - Offset to ?

Note: \'Model Section\', Parts runs until \'Model Section\', Animations.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

`<b>`{=html}`<i>`{=html}\'Model Section\', Animations`</i>`{=html}`</b>`{=html} \[at offset 0x00000274\]:

`01 00 16 00 02 00 B4 00 B4 00 B8 00 FC CC 14 80 0F 00 16 01 01 20 B4 00 D2 00 D4 00 B4 CD 14 80 14 00 16 03 00 26 B4 00 2C 01 2C 01 68 D0 14 80 18 00 16 03 00 33 B4 00 44 01 44 01 8C D4 14 80 0F 00 16 03 00 39 B4 00 0E 01 0E 01 98 DA 14 80 0F 00 16 03 00 34 B4 00 0E 01 0E 01 00 DF 14 80 1E 00 16 00 02 1E B4 00 B4 00 B8 00 1C E3 14 80 1E 00 16 00 02 01 B4 00 B4 00 B8 00 58 E7 14 80 0F 00 16 02 00 2A B4 00 F0 00 F0 00 30 E8 14 80 06 00 16 01 02 2B B4 00 C0 00 C4 00 98 EB 14 80`

Note: In CLOUD.BCX, the above would be the end of the file. In this format, however, the Model Section

(with all its components) comes before actual parts/animations data, after which is texture data, which

comprises the remainder of the file.

Note: \'Model section\', Animations runs into \'Skeleton Data Section\'.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

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

---

# FF7/WorldMap Module/Script {#ff7worldmap_modulescript}

- [FF7/WorldMap Module/Script](#ff7worldmap_modulescript){#toc-ff7worldmap_modulescript}
  - [Script Engine](#script_engine){#toc-script_engine}


## Script Engine {#script_engine}

### Instructions & Stack {#instructions_stack}

The Worldmap scripting engine for FF7 is very different from the field scripting format. It is a stack based language and for the most part instructions are the same size (16 bits), instead of having their parameters encoded into the instruction they take a predefined number of items off the stack and operate on that data. There are a few instructions that incorporate another word (16 bits) of immediate data, such instructions are clearly marked in the [opcode list](FF7/WorldMap_Module/Script/Opcodes "opcode list"){.wikilink}.

The stack itself is global, there is only one stack which is shared between all scripts that are currently running. It is 8 levels deep, that is to say a maximum of 8 different items can be on the stack at any given time. A given item on the stack is not evaluated until it is popped off the stack, which can be a little unintuitive. For example, pushing the current X position of the player does not actually read the players position at that time, only when the value is actually used will it be fetched from the player entity. In practice this is not an issue because the script itself would have to change the position in between pushing the value and using it. Refer to the section below for an explanation of why that is the case.

### Contexts

The script engine uses cooperative multitasking to run different scripts in parallel, the state of each script is contained in a separate context. On each frame, the game will loop over every active context and run it until it either returns or enters a waiting state. This means that scripts cannot run too long or they will slow down the game, an infinite loop will lock up the game completely. This also means that from the scripts point of view, nothing will happen until it returns or enters a wait state, the game is not running and no other script can run during this time.

### Entities & Models {#entities_models}

The Worldmap module operates on a fixed set of models, each having a specific model ID.

*Type = 1, Model function*

| Model ID |      Name       |
|:--------:|:---------------:|
|    0     |      Cloud      |
|    1     |      Tifa?      |
|    2     |      Cid?       |
|    3     | Ultimate Weapon |
|    4     |     Unknown     |
|    5     |     Unknown     |
|    6     |     Unknown     |
|    7     |     Unknown     |
|    8     |   Cargo Ship    |
|    9     |     Unknown     |
|    10    |     Unknown     |
|    11    |    Highwind     |
|    12    |     Unknown     |
|    13    |    Submarine    |
|    14    |     Unknown     |
|    15    |     Unknown     |
|    16    |     Unknown     |
|    17    |     Unknown     |
|    18    |     Unknown     |
|    19    |     Chocobo     |
|    20    |     Unknown     |
|    21    |     Unknown     |
|    22    |     Unknown     |
|    23    |     Unknown     |
|    24    |     Unknown     |
|    25    |     Unknown     |


Each model that is currently loaded into the map also has an entity associated with it, this is the state of the model and holds information such as its position, rotation, current animation etc. Most instructions operate on the current active entity, which can be changed with the [330](FF7/WorldMap_Module/Script/Opcodes/330 "330"){.wikilink} opcode. The current active entity can also change as a side effect of certain instructions, all known cases are documented in the opcode descriptions but the list is not complete. The variable holding the current active entity is a global variable that resets every frame, if a script enters a wait state the current active entity is undefined when executing resumes.

Each entity is also a context (see the above section for more information about contexts) and in fact, there is no difference whatsoever between an entity and a context. The distinction is made because of the way they are treated by the scripting engine, the script state of the active entity (or any entity for that matter) cannot be modified (other than asking it to execute a function by means of the [204](FF7/WorldMap_Module/Script/Opcodes/204 "204"){.wikilink} opcode) and conversely, the state of the model corresponding to the context cannot be modified unless it is also the current active entity. This is the default state, whenever a function begins execution the context and current active entity are always equal.

In addition to the contexts associated with the models there is also a system context, this is where execution begins when the worldmap is first loaded and it also handles events which are not specific to any model on the map. The system context is technically an entity because, again, contexts and entities are the same thing but since it does not correspond to a model, manipulating the state of the system \"entity\" is an error.

### Functions

As alluded to earlier, the script engine is driven by executing functions, each model has a set of functions that are executed by the game in response to certain events;

| \# | Name | Description |
|:--:|:--:|:--:|
| 0 | Enter | Called when the model is loaded |
| 1 | Exit | Called when the model is unloaded |
| 2 | Tick | Called each frame if the model is set to recieve ticks? |
| 3 | Movement? | Seems to be called for certain models that move around the map |
| 4 | Unknown |  |
| 5 | Unknown |  |

This table is probably not complete.

There is also a set of system functions that are executed in response to events which are not related to a certain model;

| \# | Name | Description |
|:--:|:--:|:--:|
| 0 | Enter | Called when the worldmap is loaded |
| 1 | Exit | Called when the worldmap is unloaded |
| 2 | Tick | Called each frame |
| 3 | Unknown |  |
| 4 | Unknown |  |
| 5 | Unknown |  |
| 6 | Unknown | Enter highwind interior? |
| 7 | Midgar Zolom | Called when the player touches the midgar zolom in the swamp. |

This table is not complete either.

And finally there is a set of functions which are called when the player enters an area of the walkmesh that is designated to trigger a script (it is not clear exactly which walkmesh types can trigger this event). Which function is executed depends on the mesh coordinates of the player (0-35, 0-27) as well as the exact walkmesh type that triggered the event. In theory there can be more than 2000 unique combinations so no list will be given for these functions :) Fortunately, not all functions need to be implemented, as will become apparent in the next section, functions that do nothing do not need to be implemented at all.

## .ev Format {#ev_format}

### Call Table {#call_table}

The first 0x400 bytes of an .ev file is the call table, a mapping between functions and entry points. Each entry is 4 bytes, 2 bytes of function identifier and 2 bytes instruction pointer. Instruction pointers are in 2-byte increments from the start of the code section. The first two bits (most significant) of the function identifier defines the format of the remaining 14 bits;

*Type = 0, System function*

|            size            | description |
|:--------------------------:|:-----------:|
|           6 bits           |   Padding   |
| 8 bits (least significant) | Function \# |


*Type = 1, Model function*

|            size            | description |
|:--------------------------:|:-----------:|
|           6 bits           |  Model ID   |
| 8 bits (least significant) | Function \# |


*Type = 2, Mesh function*

|            size            |     description     |
|:--------------------------:|:-------------------:|
|          10 bits           | MeshX + MeshZ \* 36 |
| 4 bits (least significant) |    Walkmesh type    |


Call table entries MUST be sorted in ascending order of function identifier! Duplicate function IDs are not recommended as they can cause some very unpredictable behavior. Original FF7 data seems to duplicate the 0 identifier, it is possible that the first entry does not count? It is probably best to ignore the first entry altogether. If the game attempts to call a function for which no identifier can be found in the call table the call will simply be ignored. It is not an error to leave a function unimplemented if it does not have a use. The call table should be kept compact with all empty entries at the end with a function identifier of 0xFFFF and an instruction pointer of 0.

### Code

After the call table follows 0x6C00 bytes of code. The .exe would have to be patched to accommodate for a larger code size. The entire code section is treated as a continuous area of 16-bit values, no padding is necessary between functions and functions do not even have to be contiguous in memory (although it is highly recommended). Due to an implementation detail the first function should start at offset 1 (an instruction pointer of 0 means the context is not active), just in case it is probably a good idea to make the first instruction always be a single [return](FF7/WorldMap_Module/Script/Opcodes/203 "return"){.wikilink} instruction.

---


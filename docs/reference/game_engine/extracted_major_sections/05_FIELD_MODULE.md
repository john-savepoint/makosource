# **The Field Module**

Important files:

| PSX Version  | PC Version             |
|--------------|------------------------|
| /FIELD/*.DAT | /DATA/FIELD/FLEVEL.LGP |
| /FIELD/*.MIM | /DATA/FIELD/CHAR.LGP   |
| /FIELD/*.BSX |                        |

## *I. Field Overview*

The field module is the core of the game to which everything else is spawned. It is tied very closely with the kernel and contains many low-level calls to it. The field system also contains a self-contained bytecode language called commonly called "Field Script". The field module is responsible for the following:

- -The loading and parsing of the field files.
- -The display of the 2D background ands related special effects
- -The display of 3D elements in the field such as the camera, perspective and and entities.
- -The running of the Field Script to display events and to get user input.
- -The on-demand loading of other modules when needed.

The Field module loads modular "Field Files". In the PC version, the Field File is a single file with nine sections. In the PSX version, there are three files with the same name but with different extensions that do the same thing. The three files are MIM, (Mutiple Image Maps, or the backgrounds), DAT, (Field Script Data), and BSX, (3D data).

The following snapshot of the PSX's VRAM demonstrates the background field files in various stages

of assembly.

![](_page_73_Picture_13.jpeg)

The backgrounds are actually 16x16 blocks that are loaded into VRAM and then assembled into the video buffer every frame. The system allows for layers to obscure the 3D entities using a simple painter's algorithm.

In this particular field file, there are six cached sections of background data. Also notice the bright green patches that don't show up in in the video buffer. This was to show where a lower layer of 2D data was to be covered by a higher layer. The bright green is for debug purposes. During development, if any bright green showed up, it meant that your upper layer had a "hole" in it that a 3D entity could be seen through.

When the PSX version of FF7 is ran in higher resolutions via emulation with texture filtering on, often the lower layers will "bleed" outside the upper layer and make artifacts. This was also the reason why the field files were not re-rendered for the PC version of the game. It would of required "re-cutting" the layers again in the higher resolution.

Another last thing to note is in the middle of the bottom texture cache there are a sea of eyes. These blink at random times and reflect the random blinking of the characters in the game.

## *II. Field Format (PC)*

## **General PC Field File format**

Field files are always found in FLEVEL.LGP. They are always LZS compressed (see my other documents/tools for details of LZS compression and tools to do it).

The first two bytes of each (decompressed) field file are blank (zero).

The next four bytes is an integer indicating how many sections are present in the file.

Then a number of 4-byte integers follow, giving the starting offset for each section.

All field files should contain 9 sections; it's what FF7 expects.

#### PC Field File Header

| Offset | Size    | Description          | Section Data            |
|--------|---------|----------------------|-------------------------|
| 0x00   | 2 bytes | Blank                | Always 0x00             |
| 0x02   | 4 bytes | Number of Sections   | Always 0x0009           |
| 0x06   | 4 bytes | Pointer to Section 1 | Field Script & Dialog   |
| 0x0A   | 4 bytes | Pointer to Section 2 | Camera Matrix           |
| 0x0E   | 4 bytes | Pointer to Section 3 | Unknown (Model Loader?) |
| 0x12   | 4 bytes | Pointer to Section 4 | Palette                 |
| 0x16   | 4 bytes | Pointer to Section 5 | Walkmesh                |
| 0x1A   | 4 bytes | Pointer to Section 6 | Unknown                 |
| 0x1E   | 4 bytes | Pointer to Section 7 | Encounter               |
| 0x22   | 4 bytes | Pointer to Section 8 | Unknown                 |
| 0x26   | 4 bytes | Pointer to Section 9 | Background              |

| Offset | Size    | Description                                                                               | Section Data        |
|--------|---------|-------------------------------------------------------------------------------------------|---------------------|
| 0x2A   | 4 bytes | Where Pointer to Section 1 points to                                                      | Length of Section 1 |
| 0x2E   | Varies  | Start of Section 1 data. Continues for the<br>number of bytes specified in Section Length | Field Script        |

Each section generally starts with a four byte integer indicating the length of the section. You could just work this out by comparing offsets (how much space until the next section/end of file, etc) but FF7 stores the length at the start of the section anyway. After that the actual data follows. So the first bit of data for a section is actually 4 bytes after the point given in the section header (since the first four bytes are actually the length marker).

#### **Section 1 Dialog and Event (Halkun, Lasyan, and Fice)**

The First section holds the Field Script logic and Dialog data for that particular field file. The first section of the PSX DAT file (excluding the DAT header) and the data in this section are the same. A recap of the PSX DAT file format is later in this document.

The data in this section also has a header with the following format.

#### Section 1 Header

```
struct FF7SCRIPTHEADER {
 u16 unknown1;
 char nEntities; // Number of entities
 u16 unknown2; // Always less than nEntities; possibly visible entities?
 u16 wStringOffset; // Offset to strings
 u16 nExtraOffsets; // An optional number of extra offsets... unknown
 u16 unknown4[4];
 char szCreator[8]; // Field creator (never shown)
 char szName[8]; // Field name (never shown)
 char szEntities[nEntities][8]; // Field entity names
 u32 dwExtraOffsets[nExtraOffsets]; // Said extra offsets... unknown
 u16 vEntityScripts[nEntities][32]; // Entity script entry points, or more
                                     // explicitly, subroutine offsets
};
```

#### Event Script Subsection

Here we have all of the pointers tables, one for each section. Pointers are 2 bytes length. Each table has a length of 64 bytes, which means a section can have 32 scripts max. Each pointer refers to the first command of the current script. The section number N begins at the offset header\_length+N\*64. Note: the only way to retrieve the length of a script is to subtract the position of the next script to the position of the current script.

#### Dialog Subsection

Right after the last script of the last section, we find the pointer's table of the dialogs. The first 2 bytes show the number of dialogs in the file, so you can deduct the length of the table: number\_of\_dialogs\*2. After these 2 bytes we have the pointers for each dialog. Be aware that the pointers are relative to the table, which means you must add the position of the table to each pointer in order to find the right position of the dialog. The dialogs begin right after the table, and the code 255 means the end of the dialog.

Note: some <<hidden>> dialogs are not referenced in the table!

#### **Section 2 Camera Matrix (Kero)**

This is yet to be completely understand, I am pretty sure that this is not exactly trash, since it is based on at least 300 changes of field files. It was pretty nasty, as you can imagine, first divide sections of field file, load section 2 into hexedit, change byte, save section 2, run .bat file that complete new field file with new section 2 and compress it. After that I always had to use ficedula lgp tools, awful, I am definitely going to program command line program for this, in gui i had to alway on original field file, click, replace, click instead of just adding line to .bat file. After that run ff7.exe, go to destinated location and observe what happened.

I am working on program to load walkmesh along with camera matrix. I am pretty sure about vectors, after all, they are all same length and they are orthogonal, but i could misinterpret order of them, position of center is little uncertain and resize factor too. The program should help me to figure out these thing.

#### Description of section 2 (field file) - camera

Goal of this section is to define camera matrix. In fact it seems pretty simple. For camera matrix, you need vector for axis x, vector for axis y, vector for axis z and position of camera in world space. Vectors for axis x,y,z are defined in world space and in camera space are normally united.

Example: You have axis x defined as vector (0.176,-0.512,0.840) but thats in the world space, in camera space it is just (1,0,0)

- \* Every offset is relative here, 00 is at the start of section 2 (after length indicator).
- \* This will will be in the left handed coordinated system= x axis from left to right, y axis from bottom to top, z axis from near to far.
- \* In here, I am changing signs so these vectors should be correct for file loaded right from section 5 walkmesh. While in walkmesh you don't change any signs, here I am changing them, so they will fit and if you use this article with unchanged values for walkmesh, you should get right image , same as in ff7. (FIXME: not yet true)

This is an overview the camera data format.

#### Section 2 Format

| Offset | Size    | Description             |
|--------|---------|-------------------------|
| 0x00   | 6 bytes | Camera Vector X axis    |
| 0x06   | 6 bytes | Camera Vector Y axis    |
| 0x0C   | 6 bytes | Camera Vector Z axis    |
| 0x12   | 2 bytes | Unknown                 |
| 0x14   | 4 byes  | Camera Space X position |
| 0x18   | 4 bytes | Camera Space Y position |
| 0x1C   | 4 bytes | Camera Space Z position |
| 0x20   | 4 byes  | Unknown                 |
| 0x24   | 2 bytes | Zoom                    |

How to get vectors for the axis:

Vectors are stored right at the beginning of section 2.

```
typedef struct {
S16 x; 
S16 y; 
S16 z; 
} vector3s;
```

You will load first vector for axis x (from offset 0 to 5), for axis y(6 to 11) and axis z (12-17). These values are in fixed point with multiply constant 4096. Length of vectors x,y and z is always 4096 (first vecsize is for x, then y and last z), thats make out multiplication constant. These vectors are also always ortognormal, as you can see in ORTO 1-2 (1=x,2-y,3=z) ORTO U-Vis scalar product of U and V. As you can see, very near zero (first value is without division of multi constant). Now you have three vectors, but they are not looking in correct direction, you have to change some signs. For each vector change sign of y and z values. Now these vectors should point in correct direction, same as in ff7.

I am now suppose that you have vectors for axises loaded, each component of each vector was divided by 4096 (don't forget to store it in float) and you changed signs for component y and z. After vectors is one S16 number (from offset 18 to 19), same as z component of vector for z axis.

Now you want to have position of center of the camera matrix. Get three S32 numbers for position of center (x from 20 to 23, y from 24-27 and z from 28-31). These number are not position of center in worlds pace, but they are position of center of camera space, defined in space, where position of center is in 0,0,0 and axis for vectors are the ones you read, but have opposite signs. You get center of camera matrix like this:

```
// vx,vy,vz are axis you read, divided, y,z signs changed 
// (tx,ty,tz) is position of camera matrix in world space 
// ox,oy,oz are S32 numbers you read from offset 20 to 31 
tx = -(ox*vx.x + oy*vy.x + oz*vz.x); 
ty = -(ox*vx.y + oy*vy.y + oz*vz.y); 
tz = -(ox*vx.z + oy*vy.z + oz*vz.z);
```

After this is just blank U32 number, seems always zero and last, but not least the zoom (36-37) (don't know whether Signed or Unsigned). The bigger resize number is, the bigger is the model and walkmesh.

#### **Section 4 Pallette (Terrence)**

The following is an overview of the palette data

#### Section 4 Palette Format

| Offset | Size    | Description                               |
|--------|---------|-------------------------------------------|
| 0x00   | 2 bytes | Length (Repeat of previous length header) |
| 0x02   | 2 bytes | Unknown                                   |
| 0x04   | 1 byte  | Unknown (often blank)                     |
| 0x05   | 4 byes  | Number of colors in palette               |
| 0x09   | 1 byte  | Unknown (often blank)                     |
| 0x0A   | varies  | Palette data                              |

After the first length indicator comes another integer, also indicating length. Useless, but it's there.

Then there's one more integer; unknown purpose.

Then one byte; unknown (blank often).

Then a word; number of colors in the palette plus one. No idea why. You can work numcolors out from the section length, but FF7 stores it anyway; why add one? Dunno.

One more byte; unknown (blank often).

Then the actual palette data.

Each palette entry is a 16-bit color. This is unusual - normally palettes store as high quality data as possible, usually 24/32 bit. However since FF7 only ever runs in 16 bit I guess there isn't much point storing any other kind of data. Actually, the data is 15-bit (5-bit Red, 5-bit Green, 5-bit Blue, and 1 mask bit).

|              | Palette Data |   |   |   |   |   |   |      |      |   |   |   |   |   |   |
|--------------|--------------|---|---|---|---|---|---|------|------|---|---|---|---|---|---|
| Red<br>Green |              |   |   |   |   |   |   | Blue | Mask |   |   |   |   |   |   |
| r            | r            | r | r | r | g | g | g | g    | g    | b | b | b | b | b | m |

That's it for the palette! Only other thing you need to know is, palettes generally contain a number of colors that's a multiple of 256. This is because the palette is split up into 256-color 'pages' internally. So the first color is page 0/color 0. Color 256 is page 1/color 0. Color 628 is page 2/color 116. You'll see why in the background section.

#### **Section 5 Walkmesh (Kero)**

Every every offset is here relative, 00 is at the start of section 5 (after lenght indicator)

Section 5 of field files is stored walkmesh. Walkmesh is mesh of polygons on which is character moving, it is telling engine for example how height it is and thanks to that PC can, for example, cross bridge with real feeling that in the middle he is on higher place than on both sides. It has very simple structure.

#### Header

---------

Startofs 0x00

Lenght 0x04

Walkmesh doesn't have header, it as only one 4 bytes long unsigned int, called NoS (Number of sectors)

## Sector pool

```
--------------
Startofs 0x04
Lenght NoS*24
typedef struct {
short x,z,y,res; // short is 2 bytes long integer
} vertex_3s; // 3 short 
typedef struct {
vertex_3d v[3];
} sect_t;
```

In sector pool are sectors, in fact just triangles and its position. For each sector you have three vertex\_3s. Just store them. It seems that res and z are very often same, but not always, I don't know why. It seems that all polygons are clockwise. I didnt check it, but it is probably in order to know wheather point is in triangle. If you give it in other direction, point will be detected outside if it is inside and vice versa. Nothing difficult

## Access pool ------------

Startofs 0x04 + NoS\*24 Lenght NoS\*6 typedef { short acces1,acces2,acces3;

} In access pool you have id of poly, you should go into if you cross line.

acces1 is for line from vertex 0 to 1

acces2 is for line from vertex 1 to 2

acces3 is for line from vertex 2 to 0

If acces1/2/3 is FFFF then you are not allowed to cross this line. Acces pool and sector pool are same size (NoT), so you will just use same index for both pools.

If access don't translate you, it just says, you should be here, if you are not, then there is a problem. If you design polymesh where you cross line and access tells you that you should be in poly 12, but you are god know where then FF7 stops.

![](_page_80_Picture_0.jpeg)

#### **Section 7 (Terrence)**

As stated, Section 7 is the Encounter listing, and is generally 48 bytes long (not including the Length dword). I've not even started to decrpyt what the other bytes mean around there... I suspect encounter rates and other things. Each encounter is stored something like: xxxxxxxx yyyyyyxx, where the 'x's are the standard Battle ID we're familiar with, and the 'y's are something connected to that specific encounter. Encounters where you can get ambushed appear to be held seperately from the others, too, starting at... what... 0x14? Unsure.

Anyhow, feel free to play with it. I remain disappointed that this has yielded no trace of Ho-chu in Ancient Forest... was hoping it would at least be some really rare battle or something....

EDIT: Few more notes on the Encounters section.

First, \*EVERY\* Field file's Encounter section is 48 bytes long (52 if you include the size). It's then split into definite partitions:

0x00: Encounter Data 1, possibly enounter rate in 2nd bytes? (2 bytes) 0x02-0x0D: Encounter+Chance(?) bytes, as stated before. The total of the 'Chance(?)' bytes for this part always adds up to 64 if encounters are possible.

0x0E-0x17: Secondary encounters. Sometimes blank, sometimes gaps. No clue on the chance bytes, or how it relates to previous data.

0x18: Encounter Data 2, same setup as Encounter Data 1. Very often blank, no idea what this data is for.

0x1A-0x25: Encounter+Chance(?) bytes for Encounter Data 2. Again, adds up to 64.

0x26-0x2F: Secondary encounters for Encounter Data 2. Again, no idea what it's used for.

To get more information, I'm going to have to go and start changing things, but thought you'd like an update on what I had for now.

Funnily enough, it seems that Tonberry got as far as making it \*into\* some random encounter data... unfortunately, it's in a scene-only room - trnad\_51 : The room where Sephiroth is encased in the center of the Whirlwind Maze - and never gets a chance to be called. What a pity....

#### **Section 9 Background (Terrence)**

Firstly, a number of variables.

At offset \$28, a Word = background width (BGWidth)

At offset \$2A, a Word = background height (BGHeight)

At offset \$2C, a Word = number of background sprites (NumBGSprites)

At offset \$32, the background sprite data. See below for format (each sprite is 52 bytes long)

After the background sprite data, another \$7 bytes, unknown purpose.

Then (ie. at offset \$32 + NumBGSprites\*52 + \$7) a Word = number of 2nd layer background sprites (NumBG2Sprites)

Then another \$12 bytes, unknown purpose.

Then (ie. at offset \$32 + NumBGSprites\*52 + \$1B) the background layer 2 sprite data. See below for format.

Then another \$3D bytes, unknown purpose.

Then (ie. at offset \$32 + NumBGSprites\*52 + NumBG2Sprites\*52 + \$58) the raw image data.

#### Background paradigm

-------------------

(It isn't \*really\* a paradigm, but it sounds impressive if you say it is.)

FF7 stores its backgrounds in a rather complex format. Basically, you have the data split up into various sections:

- 1) Palette. List of colours.
- 2) Background sprites, layers 1 and 2. Just references to other bits of data.
- 3) Raw image data. Palettized data (ie. "grayscale" if viewed directly).

Each background sprite represents a 16x16 pixel block on the finished background. The sprite essentially contains the following information:

- -"Target" block, ie. where on the background to draw this 16x16 square
- -"Source" block, ie. where on the raw image data to take the pixels from
- -Palette "page", ie. which 256-colour palette block to apply to the raw image data

This is a very efficient way to store the image; on the one hand, it's in 16-bit colour, far better than just palettizing the whole image (ie. 256 colours over the \*whole\* background). On the other hand, each 16x16 pixel block takes much less space than if you'd stored it directly in 16-bit colour format. It isn't, however, easy to decode or (especially!) encode.

Format of a background sprite:

```
Type
 TFF7BgSprite = packed record
 ZZ1,X,Y: Smallint;
 ZZ2: Array[0..1] of Smallint;
 SrcX,SrcY: Smallint;
 ZZ3: Array[0..3] of Smallint;
 Pal: Smallint;
 Flags: Word;
 ZZ4: Array[0..2] of Smallint;
 Page,Sfx: Smallint;
 NA: Longint;
 ZZ5: Smallint;
 OffX,OffY: Longint;
 ZZ6: Smallint;
 end;
```

ZZ1,2,3,4,5,6: Unknown data X,Y: Target position SrcX,SrcY: Source position

Pal: Which palette page to use

Flags: Indicate special effects ... not really understood properly.

Page: Which image source page to use

Sfx: More special effects?

NA: Unknown OffX,OffY: Unknown

The image source data is split up into 256x256 pixel pages; that's why as well as a source X and Y, you also have a source page

(which 256x256 block to take data from). On the other hand, the destination background is stored as one big bitmap with no limits on size, so there, you just have a target X/Y position which can be used directly.

Also, note that each source image data "page" is preceded by 6 bytes of header.

So, say the raw image data starts at offset ImageData. Given a background sprite, the offset where that sprites data starts is:

```
StartOffset := (Page shl 16) or ((SrcY shl 8) or SrcX) + (Page+1)*6;
this is equivalent to
```

StartOffset := (Page \* \$FFFF) + (SrcY \* \$FF) + SrcX + (Page+1)\*6;

(Page shl 16), (Page\*\$FFFF): Each page takes up 256x256 = \$FFFF bytes, so skip that many for each page.

(SrcY shl 8), (SrcY\*\$FF): Each pixel row takes up 256 = \$FF bytes, so skip that many to get to the right row.

SrcX: Taken directly.

(Page+1)\*6: Skip 6 bytes of header per page. (Page+1) since even page 0 has 6 bytes preceding it.

Incidentally, the shifts are used in preference to multiplication since shifting is more efficient. Shifting on a computer is equivalent to multiplying/dividing by 2, 4, 8, .....

For the destination, note that you can use X/Y directly; however 0,0 \*appears\*, I \*think\*, to be at the image \*centre\*, not at the top/bottom left corner like with most programs.

So, now you know:

- -Where the raw image data for that sprite starts
- -Where you're drawing it to
- -Which palette page to use

Now, you just copy the pixels across, filtering the palette into it. IE:

Read a pixel from source image (one byte).

Set current colour to that colour in palette.

Draw onto target.

So, if you read a byte = 55 from the source image, you'd draw colour 55 in the selected palette to the target bitmap.

#### Other points

------------

Currently, Qhimms (and therefore mine too) source code doesn't draw a sprite if the Sfx is non-zero; this is because we don't understand what it does.

All variables above (Page, Pal, X, Y) start from ZERO; palette page zero is the first one, page one is the next one, etc.

The image data in FF7 palettes is stored in reverse order; ie. on Windows, data is stored Red first, then Green, then Blue. FF7

stores it the opposite way around, so you need to exchange the red/blue data. Here's how I do it in Cosmo:

```
 DCol := 0;
 DCol := DCol or ( (Col^ and $1F) shl 10 );
 DCol := DCol or (Col^ and $3E0);
 DCol := DCol or ( (Col^ and $7C00) shr 10);
```

Converts Col, an FF7 colour, into DCol, a (16-bit) Delphi colour.

The first background sprites are drawn "behind" the layer 2 sprites.

Variable conventions; I'm using Delphi names, which are as follows:

Byte: 8 bit, unsigned, integer Word: 16 bit, unsigned, integer Smallint: 16 bit, signed, integer Integer/Longint:32 bit, signed, integer

(Unsigned = positive values only. Signed can hold positive or negative values).

Also, whenever I use numbers with \$ signs above, it means I'm using hex values (hexadecimal).

----------------------------

#### PSX DAT FORMAT

The PSX script is contained in the DAT file, it is compressed with LZS compression. After it's decompressed, here is the header format for that..

First, we have 28 unused bytes (in fact, they are used by the PSX, it's a list of 7 2-bytes values which refer to a place in the RAM). So each time you'll find a value which is an adress in the file, you'll have to add 28 to it in order to find the right position in the file (or else you can simply remove the first 28 bytes of the file).

Note: the first byte in the header is byte 0

(Follow PC Version)

----------------

PSX MIM FORMAT

--------------

PSX BCX FORMAT

------------------

## *III. A Look at the Debug Rooms*

The "debug room" is an artifact of the development process. It allowed the programmers and the play testers to access all the parts of the game as opposed to playing 40 hours plus just to get to a particular bug. In the alpha and beta versions of the game, you could quickly enter the debug room from anywhere. Only after the final compile, where the game was placed into "production mode", was the debug room "locked out". It was not removed entirely, just in case.

The easiest and most unobtrusive way of entering the debug room is using a save game. This works on a nice cross platform sort of way and you don't have to worry about making anything unstable, (at least, not until you start messing with the engine).

#### **STARTMAP**

Startmap is the first "debug room". If you enter from a save. It appears as such.

![](_page_85_Picture_5.jpeg)

On the PC version, the background is missing, so you don't see the logo, names, or Japanese characters on the screen. This field file is useful in many ways. First, is has a very simple background with alpha transparencies. It also sets the camera and the main character at the mathematical origin of the map (0,0,0) for alignment purposes. The camera and player are also at a rotation of 0,0,0 as well.

#### **Names and the Japanese characters**

All the Japanese letters and words you see are names. Each leads to a room that that contains events that particular person was responsible for. Here is a list of Japanese letters and who it represents.

 1(北) 2(京) 3(野) 4(吉) 5(鳥) 6(秋) 7(松) 8(千)

#### 1. Kita (北) - Yoshinori Kitase (北瀬佳範)

Mr. Kitase was the director of the Final Fantasy Project, he also helped write the story and assisted in event planning.

- 2. Kyou (京) Hidemi Kyounen (京念秀史) Event planner.
- 3. No (野) Kazushige Nojima (野島一成)

Mr. Nojima also helped write the story and was one of the main event planners.

- 4. Yoshi (吉) Kazuhiko Kichioka (吉岡加寿彦) Event planner.
- 5. Tori (鳥) Motomu Toyama (鳥山モトム) Event planner.
- 6. Aki (秋) Jun Akiyama (秋山淳) Event planner.
- 7. Matsu (松) Hiroyuki Matsuhara (松原啓介) Event planner.
- 8. Sen (千) Hiroki Chiba (千葉広樹) Event planner.
- 9. Takashi Tokita (時田貴司)

Mr. Tokita assisted in the event planning for Final Fantasy 7. He did general event flow throughout the game. You access his room by walking off the screen to the north.

#### 10. Masao Kato (加藤正人)

Mr. Kato also assisted with event planning, mostly working on the lifestream sequences and the final battle with Sephiroth. You access his room by walking off the screen to the south.

#### The world map

Walking off of the left of the screen will place you on the world map dictated by what is set in the current map location (Default is outside Midgar.)

#### Yuffie's Menu

Yuffie is standing here between to the 'Aki' and 'Sen' rooms. Taking to her give you the following menus.

NEXT - Next menu.

MENU ON - Enables all the right hand options in the menu.

BATTLE LOCK - Disables all random encounters.

BATTLE UNLOCK - Enables all random encounters.

MOVIE LOCK - Skips all the movies.

MOVIE UNLOCK - Enables movies again.

GLOBAL RESET - Resets money and party.

FULL NAME - Tests the display window for the name by filling it with characters

NEW START - Resets all the event flags in the whole game.

EXIT - Cancels

#### Menu 2:

BACK - Returns to the previous menu.

SOUND RESET - Turns off any playing sound effects or music.

FULL MATERIA - Calls a SPECIAL function three times to fill your inventory with materia.

BATTLE999 - Debug battle #999, for more information in this, see the section on the Battle module. EXIT

### **1. Kitase's Room (**北**)**

This is Kitse's room.

![](_page_87_Picture_19.jpeg)

In this room there are several things to note. First, most of the scripts are triggered by stepping close to the character. Secondly, there are some lighting effects are in this room. Aerith uses a bit of dynamic lighting, Tifa is colored with a purple light, and cloud sports a "walking in water" color set that animates when the room is initialized. The following is a breakdown of each character's script.

```
1.1 Aerith
cancel - cancel.
bone after arma - Bone village, after Armageddon. The event flags are not correctly set, do the dialog
       is not correct.
san dun - Climbing caves in Corral Valley.
sleep forest - Entrance of the sleeping forest.
ancient forest - Ancient forest secret area.
lost lake - The City of the Ancients with the huge jeweled pedestal.
water pray - Event where Aerith is praying before Sephiroth kills her.
Aeris dead - Event after Jenova-LIFE battle.
rocket (□ first) - Event before Palmer fight at Cid's.
       (Hold □ for the event when the party first sees the Tiny Bronco).
bone first - Bone village entrance event.
bone luna - Bone Village before the City of the Ancients event.
los in - Event at Junon when the party realize Sister Ray is missing.
1.2 Tifa:
past jenova (□ egg) - Event where Sephiroth nearly kills Tifa/Cloud remembers the truth.
       (Hold square for event after Cloud has stabbed Sephiroth.)
join vincent - Event under the mansion where Vincent joins the party.
shinra house vincent (□ Present) - Shinra mansion. Cloud can't get out of the bed?
       (Hold □ for the entrance to the mansion just before the 'reunion'.)
Shinra under (□ awake) - Event outside the library of Shinra mansion (flashback)
       (Hold □ for second library event).
nivl reactor - Outside the egg room.
nivl reactor out (□ with Tifa) - Arrival at Mt. Nibel's Mako reactor Event (flashback)
       (Hold □ for Outside the reactor chasing after Sephiroth)
nivl mt entrance (□ past) - Mt. Nibel 'fly-by' FMV.
       (Hold □for Mt. Nibel flashback event when Cloud and Tifa were children.)
materia cave - Event Just outside of the materia cave in Mt. Nibel (flashback).
new event sininb34 - event outside of Shinra Mansion library with Zack.
new event sininb35 - Beginning of Zack flashback event.
new midgal - Event where Zack is killed.
nivgate - Zack carries Cloud stagger out of Nibelheim.
() - Cancels.
1.3 Cid
opening - Opening event with movie.
Feel Wind -Diamond weapon battle event.
gate 1 open - The event outside the mako reactor 1 after leaving the station.
T road - T road event Avalanche enters the first mako reactor. (Biggs stands watch)
       (Hold □for escape event.)
1reactor (□ 5reactor) - On bridge leading to first boss battle.
       (Hold down □ for same location in sector 5's reactor)
junon - Tifa's live execution in junon. 
       (Hold □ for the same, but with Yuffie disguised as a camera man later on.)
       (Press R1 for Tifa gas chamber escape event).
() - cancel
```

#### 1.4 President Shinra

white - Tifa's gas chamber event.

white boogen(key) - Event where the music box projects an image.

white boogen(nokey) - Event before Bugenhagen examines the music box.

before - The same as above, but with environment flags set

after - After 'music box' event has been finished with proper flags

white 2 - The same as above, but without the environment flags

Junonn in2 - Music box 'projection' scene.

#### 1.5 Shinra Employee

Para - Parachute event.

66F - Board meeting on the 66th floor.

67F (□) - 67F when Hojo enters the room

(Hold □ for 'captured' event.)

68F - Just before boss fight with HO512.

68F2 - Event where Red XIII first appears.

70F - Launches a submenu

plate down meeting - Heidegger and Reeve talk to P.Shinra about the Sector 7 pillar sabotage plan.

caught - scene where the team are introduced to President Shinra by Rude.

dead president - Arrival in P.Shinra's office only to find him dead.

app rufaus - Rufus arrives outside in his helicopter.

after heli - scene just before Rufus boss battle.

elevetr - Scene where the turks capture everyone in the lift.

() - cancels

#### 1.6 Barret

(No menu, JUMPMAP to Final dungeon.)

#### 1.7 Red XIII:

7 pillar - Sector 7 pillar battle event.

Kolneo under - Event under Don Corneo's mansion, in the sewer.

high way - Event after Motor Ball boss

5 out - Event where party leaves Midgar for the first time.

airport (□ gelnica) - Outside Highwind at Junon airport

(Hold □ for the Gelnika airport scene).

after fire sephiros - Event after Sephiroth walks through the fire.

jairo sky - Crashing Tiny Bronco event.

jairo sea - Event where Tiny Bronco has landed in the sea.

junon cannon - Event where weapon is attacking Junon/ Barret escapes.

junon medical - Event after Tifa's Flashback in Junon while being held prisoner.

() - cancel

#### 1.8 Jessie

Cancel - cancel Aerith - Adds Aerith to the character pool Tifa - Adds Tifa to the character pool Barret - Adds Barret to the character pool Red - Adds Red XIII to the character pool cid - Adds Cid to the character pool (blank) - Adds Cait Sith to the character pool Yuffie Adds Cait Sith to the character pool Sephiroth - Adds a Sephiroth'ed Vincent to the character pool Cloud Lock - Keeps cloud as party leader Change members - Loads a menu requiring to make a party of three.

## **2. Kyounen's Room (**京**)**

This is Kyounen's room.

![](_page_90_Picture_4.jpeg)

#### 2.1 Priscilla

all members - add all members to the character pool quit - quits

without Yuffie - removes Yuffie from the character pool without Vince - removes Vincent from the character pool without Ballet - removes Barret from the character pool without Tifa - removes Tifa from the character pool without Erith - removes Aerith from the character pool without Red - removes Red XIII from the character pool without Cid - removes Cid from the character pool without Ketcy - removes Cait Sith from the character pool

#### 2.2 Barret

"Who do you want in the Party?

Tifa - Places Tifa in the active party

Ballet - Places Barret in the active party

Red - Places Red XII in the active party

Cid - Places Cid in the active party

Yufi - Places Yuffie in the active party

Ketcy - Places Cait Sith in the active party

Vince - Places Vincent in the active party

Put Cid on point - Removes all characters and places Cid as the party leader Forget it - quits

#### 2.3 Tifa

Going to North Corel. It doesn't matter whether or not Ballet is in this event.

Barret of North Corel - North entrance to Corel town.

ropeway - Gold Saucer ropeway entrance (Corel side).

North Corel - Event if you fail to stop the runaway train.

Quit - quits.

#### 2.4 Nurse

These set various event flags within the game.

Palmer - Flags Palmer battle has finished.

Highwind - Gives you the Highwind.

Materia mission - Flags that the Corel-based Matera mission has been done.

Cloud's revival - Flags Cloud has been rescued from the Lifestream.

Rocket launch - Huge materia rocket ready to launch.

Sister Ray - Going to stop the Sister Ray.

Train Success - Flags the train was stopped

Train Failure - Flags the train was not stopped

Train Last - Doesn't touch the train flags

Quit - Takes you to North Corel with no location information.[STUCK]

#### 2.5 Aerith

"Snowboard Game"

(Plays the Story-version snowboard game)

#### 2.6 Cid

I'm sickle...xxxx. I mean Icicle inn...ok bad joke." (Icicle inn just before snowboard event)

#### 2.7 Yuffie

"Hydroplane event"

Deck No.1 - Weapons awakening event.

Parachute Deck - Midgar parachuting event.

bridge no. 1 - Event before the Sister Ray is used by Hojo.

bridge no. 2 - Event where Reeve explains the problem with Hojo to Cloud.

bridge no. 3 - Event after Reeve is captured/Highwind heads for Midgar.

Conference room 1 - Heidegger/Scarlet explain huge materia plan to Rufus.

Conference room 2 - Reeve attempts control of the Sister Ray

Conference room 3 - Reeve is arrested

Send-off people - Event just before parachuting into Midgar

#### 2.8 Man

"Gaea's Cliff test"

Gaea's cliff no.1 - 1st Freezing climb event.

Gaea's cliff no.2 - 2nd freezing climb event.

Gaea's cliff 1 of 3 - 3rd freezing climb event.

Gaea's cliff 2 of 3 - Last climb to top of the cliff.

Base of Gaea's cliff - Outside Mr. Holzoff's house.

Quit - cancels.

#### 2.9 Red XIII

"Where are you going underneath Junon?"

Under junon 1 - Junon fishing town next to the beach.

There'll be monsters - Junon fishing town, after you've saved Priscila.

Dolphin Jump - 'Dolphin jump' event

Artificial respiration - 'CPR' event.

#### 2.10 Corel Miner

Crater no.1 - Start of Crater reunion event.

Whirlwind Maze no. 1 - Event where Sephiroth tricks Red XIII.

Whirlwind Maze no. 2 - Next screen on from 'Crater no. 1 '.

Atmospheric barrier no. 1 - First 'Barrier' event.

Atmospheric barrier no. 2 - Second 'barrier' event.

Atmospheric barrier no. 3 - third 'barrier' event.

Quit - cancels.

#### **3. Nojima's room (**野**) - BLACKBG5**

Here is am overview of Nojima's room. Cloud was moved to the left for clarity.

![](_page_93_Picture_2.jpeg)

#### 3.1 Sephiroth (cefiros)

Sephiroth related

Quit - cancels.

from pinball - Truck flashback event

from Cam's inn - Young Cloud going to Nibelheim with Sephiroth event.

starry sky - Young Cloud and Tifa at the well event.

gate - Clouds's flawed memory, Sephiroth and Cloud arrive at Nibelheim.

gate no.2 - Lifestream visit to Nibelheim.

starry sky - Well flashback in Lifestream.

village no.2 - Nibelheim, bad JUMPMAP

truck no.2 - The real events with young Cloud and Zack at Nibelheim.

#### 3.2 Aerith (earith)

Church

First of all - Cloud waking up in the flowerbed after falling

Following roof incident - Inside the church with the children looking at the flowers.

After Aeris's death - Return to church to see the ghost of Aerith. Unlike many many Internet rumors, this scene contains no "unfinished code" that point to Aerith's revival. The reason why you can't talk with her is because Cloud hasn't stepped on the trigger near the door to make her disappear yet.

#### 3.3 Priscilla (pri)

These has some bad JUMPMAP commands with no location data, player gets stuck

Highwind (Not going) - cancel

Shinra's highwind - Rufus flys to the 'reunion'.

Party's highwind - First event on the captured Highwind bridge.

Evening's highwind - same event as 'Shinra's Highwind'.

sign - Parachute deck of the Highwind, [STUCK]

passageway - Middle room of the Highwind. [STUCK]

Conference room - Highwind conference room, Cloud apologizing..

Chocobo - Inside Highwind Chocobo stable. [STUCK]

{Cloud} Highwind - usual Highwind bridge scene.

#### 3.4 Tifa (tifa)

My dear hometown Nibelheim

village - Flashback event of Nibelheim at town square.

1st floor of inn - [STUCK]

2nd floor of inn - [STUCK]

store - Item shop [STUCK]

{Cloud}'s house - Cloud's house (leaps to flashback event).

{Tifa}'s house - Opens a submenu.

1st floor - [STUCK]

2nd floor - [STUCK]

2nd floor window - Tifa as a child flashback event.

reminiscing - Event of Tifa's mother's death.

1st floor of house - Bottom of house in Nibelheim. [STUCK]

2nd floor of house - Attic room of house. [STUCK]

Quit - Cancels.

#### 3.5 Little Girl (girl)

Goodbye to party members {Cloud}

(Zack flashback event)

#### 3.6 Cait Sith (ketcy)

Tragedy of Nibelheim quit - Quits

Part 1 - Sephiroth's version of Nibelheim events..

Part 2 - Sephiroth shows Cloud the truth.

#### 3.7 Red haired Man (nbman)

Global Re-set

Yes - Resets all the game flags - SPECIAL (FE)

no - cancels

ended reflecting on the past - sets flag to signal flashbacks are done.

#### 3.8 Doctor (doctor)

Present day Nibelheim

Go - Nibelheim [STUCK]

Don't go - Cancels.

#### 3.9 Zangan (zangan)

Zangan's script points to two blank dialog messages (009 and 00A) containing a single {stop} character. These were probably deleted test scripts

#### 3.10 Barret (ba)

This is a broken dialog script. The dialog is never shown. This is because the number of members that you can point to is more that the number of items in the dialog script. From the script file, the dialog is supposed to contain the following commands. Counting the blips of the finger moving from the top will give an idea where it is.

[empty] - Nothing happens because menu is incorrectly aligned.

{Cloud} - Puts Cloud in Party

{Barret} - Puts Barret in party

{Tifa} - Puts Aerith in party (misalignment)

{Aerith} - Puts Red XIII in party

Red XIII - Puts Yuffie in party

{Yuffie} - Puts Cait Sith in party

Cait Sith - Puts Vincent in party

{Vincent} - Puts Cid in party.

{Cid} - Makes young Cloud party leader

only {Cloud} 16 - Makes Cloud party leader.

only {Cloud} - Makes Tifa party leader.

{Tifa} leads the way - Makes Cid party leader.

{Cid} leads the way - Quit

#### 3.11 Yuffie (yufi)

quit - Cancels.

TRNAD51 - Event just after Cloud gives Sephiroth the black materia.

TRNAD52 - Event before Cloud gives Sephiroth the black materia.

TRNAD53 - This is an unused field file with a walkmesh that was used for debugging

BLACKBGD - Disk switch for end of Disk 2. Starts event to northen cave/Highwind.

#### 3.12 Highwind Crew Member (crew2)

quit - Cancels.

regular hours - After getting Cloud back, heading to junon on the Highwind.

star's scream - Cid speech on Highwind.

weapon appears - Diamond weapon attacks Midgar

What happened to Sephiroth? - Heading to the Northen Cave

On the final day - Event where Cloud tells everyone to go.

everyone came home. - The party all rejoin Cloud and Tifa on the Highwind.

called from the last dungeon - On Highwind at the end of the game.

### **4. Kichioka's room (**吉**) - BLACKBG7**

This is what Kichioka's room looks like.

![](_page_96_Picture_2.jpeg)

## 4.1 Cid

First a battle against against Vagyrisk takes place at Fort Condor. After the battle, a menu appears. Man - wall market as Cloud

Be Girl - Wall market as Cloud in dress.

#### 4.2 Red XIII

Train Grave

MDS7ST2 - Second screen of the Train Graveyard.

MDS7ST1 - Party enters the start of the Train Graveyard.

Cancel - cancels

#### 4.3 Reeve

- 1 Shinra meeting and unveiling of the 'Sister Ray' event.
- 2 Firing of Sister Ray
- 3 After firing of Sister Ray/The death of Rufus.

Last 0-3 - Start of North cave (leaving Highwind)

Cancel - cancels

#### 4.4 Barret

Organaize Party?

Yes - Gives you three dialog boxes of names. Each one will place that character in the active party. No - cancels

#### 4.5 Snow Woman

(blank) - Snow board landing at Great Glacier, near trees

(blank) - Snow board landing, next to Ice Gate sign at Great Glacier.

(blank) - Snow board landing at the above sign post.

(blank) - Snow board landing in forest.

HYOU3 - Snow board landing in rock valley.

HYOU13-1 (After) - Outside Snow Woman's cave, after the battle.

HYOU13-1 (Before) - Outside Snow Woman's cave before the battle.

HYOU5-2 - Ice jumping mini game.

Cancel - Cancels.

#### 4.6 Cait Sith

Climb Wire, after 7th plate falling

WCRIMB1(with Battery) - First part of wall climbing event with batteries.

WCRIMB1(without Battery) - First part of wall climbing event without batteries.

WCRIMB2 - Last climb event with batteries.

WCRIMB1 - swinging pole event with batteries.

Cancel - Cancels

#### 4.7 Man With Hat

#### CONDOR1

(blank 1) - Leads to sub menu:

(blank 1a) - Entrance to Fort Condor Cloud is leader

(blank 1b) - Entrance to Fort Condor, but Tifa is party leader.

(blank 1c) - Entrance to Fort Condor, but Cid is party leader.

cancel - cancels.

#### (blank 2) - Leads to sub menu:

(blank 2a) - Fort Condor already upstairs. Cloud leader + Tifa + Cid.

(blank 2b) - Fort Condor already upstairs. Tifa leader + Young Cloud + Cid

(blank 2c) - Fort Condor already upstairs. Cid leader + Young Cloud + Sephiroth

cancel - Fort Condor upstairs with your current party

#### (blank 3) - 3. Leads to:

(blank 3a) - Entrance to Fort Condor after final huge materia battle. Cloud leader + Cid + Tifa.

(blank 3b) - Same as above, but Tifa is party leader plus Cid and Young Cloud

(blank 3c) - Same as above, but Cid is party leader plus Young Cloud + Sephiroth

cancel - Same as above but with current party

#### (blank 4) - . Leads to:

(blank 4a) - Entrance to Fort Condor

(blank 4b) -Entrance to Fort Condor, but Tifa is party leader.

(blank 4c) - Entrance to Fort Condor, but Cid is party leader.

cancel - Fort Condor with Cid leader, Young Cloud, and Cloud.

#### (blank 5) - 5. Leads to:

(blank 5a) - Fort Condor before Huge materia battle. Cloud+Tifa+Cid

(blank 5b) - Fort Condor before Huge materia battle. Tifa+Cid+Young Cloud.

(blank 5c) - Fort Condor, same as above. Cid+Young Cloud+Sephiroth

cancel - Fort Condor Battle 2 (Current party).

#### (blank 6) - Leads to:

(blank 6a) -After winning Huge materia battle. Cloud+Tifa+Cid.

(blank 6b) After winning Huge materia battle. Tifa+Young Cloud+Cid.

(blank 6c) - Same as above but with Cid+Sephiroth+Young Cloud

cancel - Same as above, but with current party.

(blank 7) - After Huge materia battle talking to old man downstairs.

(blank 8) - In command shed after losing a battle.

(blank 9) -

(blank 10) Cancels.

#### 4.8 Aerith

MRKT1 - Top half of Wall Market.

MRKT2 (After) - First visit to Wall Market with Aerith

MRKT2 (Before) - Wall Market before 'Plate climb' event.

Cancel - Cancels

#### 4.9 Tifa

Options which give you:

(blank) - Gives you another 300 Gil.

(blank) - Gives you another 131072 Gil.

(blank) - Gives you 99 of every item.

(blank) - Battle 999

(blank) - Resets all game flags, and unlocks the menu.

(blank) -

(blank) -

(blank) - Quit

#### 4.10 Yuffie

20 Movie

Look - View movie, these are for disk two.

Plus - Add one to the movie counter.

Cancel - Cancels

#### 4.11 Wrestler

Play Fort Condor Minigame

- 1 Difficulty level 1
- 2 Difficulty level 2
- 3 Difficulty level 3
- 4 Difficulty level 4
- 5 Difficulty level 5
- 6 Difficulty level 6

Last - Huge Materia version.

### **5. Toriyama's Room (**鳥**) - BLACKBG2**

This is Toriyama's room, the following is a picture of the layout when the PC first enters on the US PSX version.

![](_page_99_Picture_2.jpeg)

This room also tests the STPAL, ASPAL and LDPAL commands for field light shading. It also tests the direct scripts, BGaimn scripts, sand windowing systems. (WSIZW, WCLSE)

There are some debug keys associated with this room. They are the following.

Select: Help menu for the below.

Square: "Reset Flag" - [Calls script commands SEPCIAL(FE) and SPECIAL(FF)]

L1: "Battle off" - switches off battles. Press again to re-enable.

L2: "Set Normal Party" - Gives you Cloud, Barret and Tifa in party.

R1: "Reset Flag" - same as Square

R2: "Default Name&No Money" - Gives default names and no money

R2: (again): Debug Name&Debug Money" - removes all names and gives you 131071 gil. (CHGLD) These are defined in the (direct) script.

#### 5.1 Aeris (earith)

"Working Now" - Aeris is a link to a scene that was broken in the Japanese version. (Hence why she says "Working now"). Her script also includes a quick animation and also 5 other scenes that are disabled.

#### 5.2 Sailor Barret (ballet)

This leads to various events on "7th Street" which are areas within and around Barret's bar. Selecting him gives you the following menus.

"7th Street" - 'Beginner's Hall' event.

Welcome Home -Return to 7th Heaven after first reactor 1 mission.

Before Memory - Tifa event about "The Promise".

Materia - Down stairs in the hideout, before "After memory" event.

Good Morning - Next Morning Event.

Before Battle - Before the Sector 7 Pillar battle event.

Cancel - Cancels

After Memory - Talking to Tifa after the promise flashback event.

#### 5.3 Tifa (tifa)

She is the party testing script. Her script tests the MMB+- command (Add/remove backup characters), PRTYE command (implicitly adds/removes all three characters to and from the 3 member battle group) and the PRTYP command (adds and removes one character to the battle group). It also tests the party select screen (Menu 7).

#### 5.4 Train Station Guard (guard)

Train Station Guard: "Last train from Midgar"

Cargo - Begins after you've met with Barret in the train boxcar.

Train 1 - Talking to Jessie about the ID system

Train 2 - Second train car, event where the alarm goes off.

Train 3 - Fourth car of the rain where AVALANCHE escape.

Train 4 - Third of train escape event

Monitor - Monitor sequence with Jessie.

Station 1 - Arrival back at sector 7 after first mission.

Station 2 - Train to the second reactor mission.

StationFlashback - Flashback event of Elmyra finding Aerith.

#### 5.5 "Honey Bee Inn" Girl (dancer)

The girl goes through a bit of an animation test. She also tests the SWCOL command to change the window colors to something a little more......romantic.

First Time - First visit to Honey Bee Inn, asking for Tifa.

2nd Time - Visit with members pass..

3rd Time - Return when Cloud is dressed as woman..

After All - Return when Shinra have occupied the inn.

Cancel

#### 5.6 Rude(workman)

This script also tests the TLKON, SOLID, and VISI script commands on the character.

"Everyday My Works are..." - Cancels

Got The Jyro - Resets Flag on little Bronco

After The Meteo...TIFA - Makes Tifa Party leader

After the Meteo...CID - Makes Cid party leader

After the Meteo...CLOUD - Makes Cloud party leader

Mako Under The sea - [SET-WORD ( 20, 00, E2, 04 )]

Hp&Mp 1 - Kills lead character and removes all Mp (MP- and HP- test)

No Money - Removes all money. (Tests the GOLD- command)

MoneyMoneyMoney - Gives you 365294 Gil. (does GOLD+ twice to test gold addition)

Got The keystone - Gives you Keystone Key item.

#### 5.7 Dog (junon3)

The dog is going through a KAWAI loop. (KAWAI == the animator's name) Also this script also calls MAPJUMPs without setting location variables. This causes the PC to get stuck. Why a dog? Because The Japanese sounds for the English "Dog" and "Dock" are similar (doggu, dokku) "JUNONDOC"

JUNONDOC1 - Junon. Scene where party boards boat to new continent. Also restores default party names and removes all money.

JUNONDOC2 - Puts you at the empty dock at Junon. In the middle of the ocean. [STUCK]

ROAD1 - Puts you in the SOLDIER base just before the main Junon town.

(Cancel) - Cancels

ROAD3 - Puts you in tunnel in Junon SOLDIER base. [STUCK]

ROAD4 - Junon Huge materia sequence in tunnel guarded by dog. [STUCK]

ROAD5 - Another corridor leading to the Junon underwater reactor. [STUCK]

ROAD6 - Puts you in Junon shop, [STUCK]

ROAD7 - Bottom of Junon liftshaft.

ELE 1 - Puts you in the Junon underwater reactor lift [STUCK]

ELE 2 - Puts you at top of Junon town liftshaft.

ROOM - Same as ROAD1.

#### 5.8 Cat (junon2)

This is the left side of Junon. There are also MAPJUMP commands called without setting location information, causing the PC to be stuck sometimes.

"JUNONL" (This also acts as quit)

JUNONL1 - Junon Town street. [STUCK]

JUNONL2 - Left side of Sliding Junon lift. [STUCK]

JUNONL3 - Part of Junon street [STUCK]

JUNONL-W - Junon weapons shop. [STUCK]

JUNONL-I1 - Junon accessories shop. [STUCK]

JUNONL-I2 - Junon Item shop. [STUCK]

JUNONL-INN - Appear at Junon inn. [STUCK]

JUNONL-PUB - Appear at Junon Shinra bar. [STUCK]

JUNONL-MIN0 - Secret beginners room in Junon inn.

JUNONL-MIN1 - SOLDIER barracks. [STUCK]

JUNONL-MIN2 - Top floor of barracks. [STUCK]

#### 5.9 Dolphin ( junon1)

One again, just a bunch of JUMPMAPs with no location information. This is Junon's right side "JUNONR" (Also quits)

JUNONR1 - Junon Parade performance.

JUNONR2 - Starts outside the sliding lift. Scene is after WEAPON attacks.

JUNONR3 - Entrance to Shinra headquarters above Junon.

PARADE - Starts at the actual parade minigame, [STUCK]

JUNONR-W - Junon Weapons shop. [STUCK]

JUNONR-PUB - Junon Pub. [STUCK]

JUNONR-I - Item shop. [STUCK]

JUNONR-M - Weapon Shop. [STUCK]

JUNONR-MIN1 - SOLDIER barracks. [STUCK]

JUNON-MIN2 - Cat room of SOLDIER barracks [STUCK]

JUNON-MIN3 - SOLDIER barracks bedroom - [STUCK]

JUNON-MIN4 - Same as second part of 'JUNONR1'

#### 5.10 Sailor (crew)

This is a jump to the sub base and related minigames. Some sanity checking is done in the way of adding characters for you, but the JUMPMAPs have no location data here too.

"Submarine" (Cancels and leads to party screen)

SubmarineDock - Red Submarine in dock SIAW.

BridgRed - Bridge of red submarine SIAW.

BridgeBlue - Bridge of Blue Submarine.

SubmarineRed - Scene just before 'Bridgered'

SubmarineBlue - Scene just before 'Bridgeblue'

Escape - Escape from submarine dock (if you failed to get a sub)

Minigame0 - Submarine game at various difficulties.

Minigame1 -

Minigame2 -

Minigame3 -

Minigame4 -

#### 5.11 Wizard (ket)

Temple of the ancients events.

"Temple of the Ancients" - (quits and leads to party screen)

Temple - Leads to The entrance to the temple - after it's been destroyed.

After Collapse - Almost the same as 'temple'

Altar - At the Alter where you put the keystone.

Alter2 - Keystone placement scene (leading to maze).

Temple of The Ancients - Maze section

Shop Of The Ancients - Shop of the ancients .

The Rock - Rolling rocks trap scene.

The Hole Of the Time - Giant Clock Scene

Tirano - Battle with monster at the bottom of the clockface.

Treasure - Treasure room. you can't open the chest or leave.

Chase - Wizard chase sequence. Leaving takes you to boss battle scene.

Next Page - Leads to second page of locations:

"Temple of the Ancients 2" - Leads to a nice picture of a wall. [STUCK]

Mateo - Leave and then re-enter for 'Cloud's mind' scene.

Sephiros - Sephiroth explains his evil scheme

Hole1 - A blocked tunnel in the temple of the ancients in the clock [STUCK]

Hole2 - Another tunnel in the temple. [STUCK]

Boss - Scene after you have killed 'Demon's Gate' boss.

Mateo2 - Same as 'Mateo' option.

Cancel - Cancels.

#### 5.12 Costa Del Sol Barmaid (cos)

This girl also is in a very small animation loop

"Costa Del Sol" - Cancels

Town - Costa Del Sol at early part of the game

Beach - Beach of Costa Del Sol

Harbor - Harbor scene

Debug - Rufus arrives at Costa Del Sol

#### 5.13 Sephiroth (mtcrl)

Tests a small animation loop as well.

"Mt. Corel"

Mountain Road - Start of pathway up Mt. Corel.

(Cancel) - Cancels

Vally - Mt. Corel railway bridge (leading to 'Rollercoaster' section).

Up&Down - Scene where you fall off the railway track and can climb up to get some items.

River - Bridge over the Corel river (the bridge is already lowered).

Hole - Secret Miner's cavern under Mt. Corel.

PiyoPuyo - Secret Birdsnest scene.

Bridge - Rope bridge from North Corel.

Railway - 'Rollercoaster' railway section.

Ballet's Memory - Barret flashback sequence of him and Dyne watching North Corel burn.

Cancel - Cancels

## **6. Akiyama's Room (**秋**)**

![](_page_103_Picture_15.jpeg)

#### 6.1 Cid (in center)

"Colneo" - (Don Corneo)

Ponbiki - (Pimp) - Don's Mansion

Irasshai - (Welcome) - Inside Mansion. (Nothing seems to happen).

Tifa to goryuu - (Hooking up with Tifa) - Tifa is taken to Corneo. You go in the room dressed as a girl.

Yame - (Stop) - cancel

#### 6.2 Cait Sith (Top)

Cloud Dake - (Only Cloud) - Cloud Party Leader Tifa Dake - (Only Tifa) - Tifa Party Leader Cid Dake - (Only Sid) - Cid Party leader

#### 6.3 Sailor

utai iriguti - (Wutai entrance) - Just entering Wutai.

yufi wo oe! - (Yufie! HEY!) - Entering Wutai persuing Yuffie.

yufi nakamani - (In company with Yuffie) - Event where you first meet Yuffie.

yufi nigeru1 - (Yuffie running away 1) - Event where you are ambushed by Shinra troops after Yuffie steals your materia.

yufi nigeru2 - (Yuffie running away 2) - Same as above with a different battle camera angle.

meteo1 - Event where meteor is hit by the rocket.

meteo2 - Cosmo Canyon after above event.

meteo3 - Same as above, but not getting Huge Materia.

yame - (Stop) - Cancels.

#### 6.4 Cid (Above Sailor)

tifa to saikai - Cloud meets up with Tifa in the Don's mansion.

earith to gouryuu - (Hooking up with Aerith) - Aerith gets to 'meet' Corneo..

colneo sonogo - Later on in the game in the basement of the Don's mansion with Kotch tied up. yame - (stop) - cancel.

#### 6.5 Cid (Upper right)

"iroiro" - (Many things)

colneo kobun beya - Cloud and Corneo's thugs event.

sinra kaiden 1 - (Shinra starway 1) - 1st set of Shinra building stairs..

sinra kaiden 2 - (Shinra starway 2) -2nd set of stairs.

sinra kaiden 3 - (Shinra starway 3) -Last set of stairs.

sinra 59F - 59th Floor of shinra building. [STUCK]

sinra elevetor - Elevator after breaking in to the shinra building.

sinrabil totunyuu - (Shinra building plaza) - Event outside Shinra building when you first climb up.

sinrabil dasshutu - (Shinra Building lobby) - Event where cloud rides down on moterbike.

yame - (stop) - cancel.

#### 6.6 Yuffie:

cosmo materia ya - Cosmo Canyon materia shop.

cosmo touchaku - (Cosmo Panorama) - Zoomed out view from when you first visit Cosmo Canyon.

seto no kabe - (Seto's Wall) - Event where Red XIII arrives at the statue of Seto.

Movie Check - Plays film of Bugenhagen's planetarium when disk one is inserted.

boogen jikkensitu - (Boogen laboratory) - Boogenhagen shows his planet lab.

sayonara cosmo - (Goodbye cosmo) - Cloud leaves Cosmo Canyon, only to be joined by Red XIII.

meteo go cosmo - (Cosmo after Meteo) - Cosmo Canyon after the threat of Meteor.

onegai boogen - (Please boogen) - Inside Bugenhagen's room, before planetarium event.

hyuji materia - (Huge Materia) - Huge materia display.

sayonara boogen - (Goodbye boogen) - In Bugenhagen's room.

............ - Bugenhagen 'goes away' and gives Red XIII his Ultimate Weapon.

#### 6.7 Dyne

sinra 60F - Video of guard falling asleep. Bad JUMPMAP [STUCK]

sinra 61F - 61F of Shinra building.

sinra 64F - 64F of Shinra building (gym). [STUCK]

sinra 63F - 63F of Shinra building (item maze) STUCK]

sinra 62F - 62F library

sinrabil shoumen - (Shinra Building Plaza) - Outside Shinra HQ.

sinrabil uraguti - (Shinra backdoor) Shinra back entrance.

minigame - Motorbike game. Afterwards Cloud appears in an empty debug room.

sinrabil matane - (Waiting by the Shinra building) - Outside Shinra Building. [STUCK]

yame - (stop) cancel

#### 6.8 Cait Sith (Bottom)

Unpansen - In disguise on board the cargo ship to Costa Del Sol.

corel kaisou1 - (Corel flashback 1) - Barret flashback to the original North Corel town/Shinra meeting.

corel kaisou2 - (Corel flashback 1) Shinra/townspeople meeting event of flashback.

aishuukessen - (Final battle) - End of the game. Cloud travels towards the light..

yame - (stop) - Cancels.

#### 6.9 Aeris (top)

Cloud erabeu - (Cloud chosen) - Cloud Chosen by Don Corneo

Earith erabeu - (Aerith chosen) - Aerith chosen

Tifa erabeu - (Tifa chosen) - Tifa Chosen

Yame - (stop) - Cancel

#### 6.10 Aerith (Bottom)

Cloud no Baai - (Cloud's situation) - Cloud in Corneos' room

Earith no Baai - (Aerith's situation) - Aeris in the room

Tifa no Baai - (Tifa's situation)- Tifa in the room

Yame - cancel

#### 6.11 Barret (right)

"5Bangai" (Sector 5)

kyoukai no yane - (The church roof) - Aerith talking to Cloud on the church roof.

yane pyon - (rooftop jumping) - Event of jumping on roof tops with Aerith.

yane kara oriru - (Decending from the rooftops) - Cloud and Aerith jump off the last roof.

yame - (stop)- Cancel.

#### 6.12 Barret (left)

"5Bangai2" (Sector 5 part 2)

slum chuusin - (Slum Center) - Sector 5 main area.

dokan - Inside the sickman's house/pipe place.

icchaya - (first arrival) - Outside of main Sector 5 (when you're trying to sneak away without Aeris).

yame - (stop) - Cancel.

## **7. Matsuhara's Room (**松**) - BLACKBG3**

This room appears As follows:

![](_page_106_Picture_2.jpeg)

Entering this room sets the "Sephiroth Flag", changing Vincent to Sephiroth and then adds him to your party. These are the characters going clockwise.

#### 7.1 Sephiroth (p8)

This is a movie tester, it runs a group of movies in a set. It also tests the color depth switches between the 8 bit overlay movies and the 15 bit hi-color types. During each sequence, the appropriate is selected and played of available. It also does minimal CD checking (using DSKCG) to make sure the correct CD is in the drive.

#### CG Movie Viewer

use - leads to :

South Reactor - Reactor explosion (where Cloud falls)

(Blank space) - sector 7 pilar explosion

NIVILHIAM tragedy - Scene where monster emerges from reactor/Sephiroth fire scene.

(Blank Space) - Aborted rocket launch scene.

Gold Saucer - Cable car departure/arrival. Also Round square ride films.

take off Tiny Bronco - Tiny Bronco sequence.

AERITH death - Aerith death scene

SEPHIROTH - Sephiroth black materia/weapons awaken.

WEAPON Attack - Attack on Junon + Highwind escape.

CLOUD psychoanalusis - Mideel destruction/lifestream choice scenes.

(Blank Space) - Rocket take off

METEO intercept failure - escape capsule/meteor scene.

shoot SISTER LAY - Firing of the 'Sister Ray'.

cancel - cancels

(Blank Space) - returns to main room

#### 7.2 Kalm Bartender (p3)

Various events in the town of Kalm

"KARM Town"

cancel - cancels

First come - Kalm when you first get there. Adds Barret, Aerith, Red 13, and Tifa to the character pool, then run the chracter select screen.

After Armagedon - set environment after the casting of meteo, brings up a submenu

Check Oldman's event?

Yes - leads to old man quest flags as below:

old man event:

get GUIDE BOOK - Guide Book key item

get DESERT ROSE - Desert Rose key item

get EARTH HARP - Earth Harp key item

event start - sends you to Kalm pub with the selected items.

No - leads to the pub in Kalm

#### 7.3 Rude (p5)

Mithril mine events

#### "SOUTH DUNGEON"

cancel - cancels

Meet TARCKS - outside the scene where you meet the Turks in Mithril Mine. Give you a sub menu.

Join AERITH?

Yes - Aerith joins the party

No - She does not

we can't go - reorganize party, then leads to Mithril mine.

#### 7.4 Sailor(p2)

### "ANOTHER CHECK"

Last Dungeon - Adds all the characters to the pool, selects the last dungeon and presents a submenu. join YUFE - adds Yuffie to the pool

join VINCENT - adds a non-Sephiroth Vincent to the pool. It will share the same attributes as the Vincent with the "Sephiroth flag" set. Because the menu system sees the two characters as the same, and because the field script is not programmed to tell anything different, the preloaded Sephiroth will change to Vince's avatar. If you start the last dungeon with Sephiroth-vincent (The one with the "Sephiroth flag" set) in your party, he will be killed and removed from the battle engine because you can't have two of the same character in your party.

join BOTH - adds both to the pool

join CANCEL - doesn't add either to the character pool

The game will then load the character selection screen so you can pick your characters, it will then return to another submenu

SAVE CRYSTAL...

Give 99!! - Give 99 save crystals, only allows one on the screen at a time.

No need - does not add them to inventory

HIGHWAY Minigame - You play the storyline version of the bike mini game,

Shinra Airship - Takes you to the crashed Gelnika, if you leave up the ladder you will be taken to the underwater world map in debug mode. Here the sub marine is replaced with a model of the key to the Ancients. This allows you full access to the underwater world map, with the ability to go on top of the cliffs and survey for any location.

#### 7.5 Aerirh

#### "AERITH EVENT"

Decline Church - Church escape sequence.

Forgotten Relm - Top of the City of the Ancients

Go To Northland - Appear in City of the Ancients after Aerirh's death.

#### 7.6 Shera

#### "ROCKET VILLAGE"

Meet CID - scene before rocket launch.

METEO intercept - same as above.

Rocket at space - Rocket in space..

#### 7.7 Gongaga Villager

#### "GONGAGA VILLAGE"

Cancel - cancels

Meet TARCKS - Plays the Turks event battle in Gongaga village.

Who am I? - Takes you to The City of the ancients from Gongaga village.

#### 7.8 Railway Guard

"TUNNEL"

Cancel - cancels

Tunnel - Take you to a submenu for the Midgar tunnels after the train escape event.

"LEVEL of TORIYAMA EVENT"

Perfect! - least distance to reactor.

Normal - Normal distance from reactor.

OH NO! - Miles away from reactor

5th Reactor - AIRBUSTER ambush.

#### **8. Chiba's room (**千**) - BLACKBG4**

The room appears as such.

![](_page_108_Picture_26.jpeg)

This is many of the Gold Saucer events, Aerith scenes, along with the last dungeon. Some of the character scripts have secondary functions when pressing the square button. This will create a window with the message "2P" within it to let you know it's switched, pressing square again will switch it back to "1P"

This room also puts the animation system through it's paces. Each character is initialized with it's own animation routine. The Player Character, in this case Cloud, is also set with a new "rest" animation as well.

#### 8.1 Center Cloud (cloud)

Ima.. - (Now I'm...) - renames the charcater. This script runs Menu 6 (rename) though it's paces. Chokobo - Chocobo race (Gives you a new chocobo to name then starts the Chocobo race mingame). Jet - Play Speed Square Gold Saucer Game.

Yame - Cancel

#### 8.2 Cloud with Sword

This will remove all party members before using the JUMPMAP command.

8Bangai - (translation: Sector number 8)

tojikomerarechatta - (Locked away) Scene in tunnel after first reactor mission where Jessie is setting a bomb.

BOOM to kitamonda - (BOOM and and way north) Tunnel explodes from bomb.

hajimete earith - (First time with earith) - Meet Aerith for the first time after first reactor mission. tobe cloud - (Cloud jumps) - Scene where Cloud gets trapped by troops and jumps on the train.

hoka ga ii - (I'm fine) - Cancels.

#### 8.3 Cloud's mother (mv)

This is a movie viewer for the various transition scenes. When possible, the current room's camera will follow the movies and you will see the debug characters standing on the walkmesh overlay. This script has a 1P and 2P menu

(1P)

Movie Check

doka~n - (Ka-boom) - Explosion where door is blown off to escape the first mission.

tou! - (jump!) - Cloud jumping onto the train after the first reactor mission.

dongaragashan - (Explosion noise) - Scene where pillar collapses/AVALANCHE escape.

touchaku - (Arrival) - Gold Saucer train entering Corel.

departu - (Depature)- Entering Gold Saucer.

Sample - Scene at Junon where Cloud climbs up to the airport

(camera pans back to show the Highwind).

Sample - Plays opening scene

Yame - (Stop) - Cancel.

(2P)

Movie Check

saishono - (Very first beginning) - Rope way train goes to the Gold Saucer for the first time.

jet - Round Square ride passing through the Speed square track.

chokobo - Round square ride going past the Chocobo races.

diozou - (Dio's Statue) - passing the statue of Dio.

hotel - passing the Ghost Hotel.

hiroba - (the plaza) passing the Event Square.

hanabi1 - (Fireworks 1) - Firework display.

hanabi2 - (Fireworks 2) - Far view of Gold Saucer, final date movie.

yame - (stop) - Cancel.

#### 8.4 Tifa (next to Cloud's mother) (san)

6Bangai - (Sector 6)

Love love - Aerith visit to playground.

7ban dokan - (Number 7's Explosion) - Recovery after pillar collapse scene.

matte matte - (Wait! Wait) Scene after Sector 7 pillar crash.

checkyou kouen - (Children's park) - On the way to wall Market.

yameta - (stop) - cancel

#### 8.5 Aerith (Jumping ) (koutai)

Party?

un - (yea) - change party. This is a party picker without the use of the party selection screen, which was being developed by another event programmer. It asks three times for characters, and places them in a active slot. It's smart enough to not have two of one character in the active slots.

uun - (nah) - cancel

#### 8.6 Turks Vincent (waving) (boku)

This is the various states of the chocobo farm.

bokujou - (farm)

ie no naka (R1 de mage) - (inside the house, R1 for further) -Talking to chocobo Bill about Sephiroth (Hold R1 for the menu that you get later on in the game where you can ask for stalls, advice, etc).

soto(R1 de mage) - (outside , R1 for further) - Chocobo ranch at the at start of the game (Hold R1 for the later version where you can actually ride Chocobos, etc).

bobou(R1 de mage) - (barn, R1 for further) - Chocobo barn, initial version (R1 for later version).

(Blank Space) - Lucrecia/Sephiroth flashback. This does not leave the debug room in an active state so you will find your PC changed to Lucrecia and not able to move.

sittitai - (I want to know) - Slaughtered Midgar Zolom scene.

Yame - stop - Cancel.

#### 8.7 Tifa (pointing) (tift)

Chokobo ijiri (Meddling with Chocobos)

ST Check - Stats check. Choose the chocobo to check. Chocobos in stables only. This will open a sub window and give you the data.

TSP: Maximum Stamina

TS: Current Stamina

SPP: Maximum Speed

SP: Current Speed

ST: Unknown

AC: Acceleration

T: Intelligence (out of 100).

LOY: Loyalty. How well the Chocobo behaves (100 is best).

CHR: Unknown CHCT: Unknown

SEX: (0 Male, 1 Female)

COL: (Colour)

0 Normal

1 Green

2 Blue

3 Black

6 Gold

CL: Number of times Chocobo has been ridden in a race

R: unknown

Tukamaeta - Controls the types of Chocobo in the paddock outside the Chocobo farm. The sub menu appears 4 times, once for every empty space in the paddock. Use Vincent's options to visit the farm (hold R1).

owari - quit.

A - Wonderful Chocobo

B - Great Chocobo

C - Good Chocobo

D - So-so Chocobo

E - Average Chocobo

F - Not bad Chocobo

G - Not very good..

H - "I really can't recommend this one."

Yasai to mi ippai - Gives you all the different types of Chocobo food (nuts as well as greens).

Magego Bokujou - Go to Chocobo farm [Cam does not pan down]

Yaoya - Buy Chocobo Greens.

Yame - Cancel.

#### 8.8 Tifa (Scratching head)(tift2)

Some of these are MAPJUMPs with zeroed locations. May cause the character to be unplayable. This also has a 1P and 2P menu

(1P)

Lasdan (Last Dungeon)

LAS3-1 - Start of second choice route after going Left.

LAS3-2 - Second screen of above, but stuck on a platform.

LAS3-3 - Last screen of above [STUCK]

LAS4-0 - Last screen of main Dungeon (party all together).

LAS4-1 - Screen just before the above [STUCK]

LAS4-2 - Floating islands before fighting Jenova.

LAS4-3 - Last set of islands, before Jenova.

LAS4-4 - Screen where Jenova appears.

LAS4-42 - Scene after Jenova where the columns fly up the screen.

Ikisaki - Lets you assign each member of the party to the 3 different groups possible in the final boss fight against 'Bizarro-Sephiroth'.

Dokoitta? - Checks the group assignments as above.

Yame - cancel

(2P)

hokora1 - Sleeping man's cave (gives you Mithril every time?).

hokora2 - Gongaga Weapon salesman's house (where you get Aeris's limit break).

hokora3 - Chocobo Sage's house [STUCK]

hokora4 - Lucrecia's cavern.

hokora5 - Materia Cave (Mime) [STUCK]

hokora6 - Materia Cave (HP<->MP) [STUCK]

hokora7 - Materia Cave (Quadra Magic).

hokora8 - Materia Cave (Knights Of The Round) [STUCK]

yame - Cancels.

#### 8.9 Vincent (Brushing dust off his suit) (t2)

Corel

hajime - (first time) - Arrival at Corel prison.

sonchou - (respect) Just before Cloud enters the old house (where Barret shoots the guy hiding behind the sofa).

dyne kessen - (Dyne battle) - Dyne goes one-on-one with Barret.

ueniikunone - (Let's go up, right?) - Barret talks to 'Mr.Coates'.

yame - (stop) cancel

#### 8.10 Aerith (hands togeather, looks right) (iti)

#### EARITH HOME

1F okaasan au - (1F Mom's here) Aerith arrives home with Cloud.

1F katari haha - (1F Talking Mom) - Cloud and chums report that Elmyra's only daughter has been abducted for use in experiments by Hojo.

2F nigeru - (2F Running away) - Scene just before Cloud has to sneak out of Aeris's house.

2F ballet naku - (2F Barret cuddle) Barret cuddles Marlene.

Hoka wo ataru - Not at the moment

```
8.11 Yuffie (punching)(yufi)
```

This has two menus for 1P and 2P

(1P)

ijiru (Tinkering)

Love\_para ijiri - (Tinkering with Love Points) Love points. How many 'love points' each character has received from your actions so far in the game. Whoever has the most points dates Cloud at the Gold Saucer. The odds are stacked heavily in Aerith's favor.

submenu

earith 1ban - (Aerith Number 1) - Maximum points to Aeris

tifa 1ban - (Tifa number 1) - Maximum points to Tifa

yufi 1ban - (Yuffie number 1) - Maximum points to Yuffie

Ballet 1ban - (Barret Number 1) Maximum points to Barret

Nakamiru - (Look at current) - View totals

Okane ippai - Lots of money, adds max gold that GOLD+ can

Okane nasi - No Money, removes all money that GOLD- can

G Reset - Resets game clock, and game flags

dflname Kaeru - Changes names with "Earith" and "Ballet".

GP ippai - Lots of GP (100000)

member zenin - Gives you all characters in the character pool

member yufi vin igai - Gives you all characters except Yuffie and Vincent.

item iroiro - Give you many high-level items.

Yame - Cancel

(2P)

Same menu as the Yuffie in the main debug room.

#### 8.12 Yuffie (Looks back and forth) (gss)

This script also has a P1 and P2 menu. It is best to have Cait Sith in your party for most of these locations as when you play the game normally he would be permanently in your party.

(1P)

GS (Gold Saucer options)

Hotel - Takes you to Hotel lobby.

jet - takes you to outside Speed Square Game

game1F - 1st room of wonder square

game2F - 2nd room of wonder square. (Note that you can't snowboard..)

Kanransha - Outside tour ride

Hiroba - Theatre. You're stuck on the stage!

eki (R1 de mage) - Leads to Gold Saucer entrance.

Karansha naka - Tour ride with 3 people. Third character gets stuck in the ticket booth afterwards..

Tougijou - Battle Square.

Yame - cancel

(2P)

date chuu to GS2

jet - Speed square with Aeris on 'date'.

game1F - First Wonder square arcade room with Aeris.

game2F - Second wonder square room with Aeris.

kanransha - Entering Round Square ride with Aeris.

hiroba - Start of Event Square play with Aeris.

chokobo - Chocobo Square with Aeris.

tougijou - Battle Square with Aeris.

mogo - Playing 'Mog's House' game (with Aeris).

yame - Cancel

#### 8.13 Yuffie 3 (sighing)(cait)

This also has a 1P and 2P Menu.

(1P)

Gold

Ballet Punpun - (Angey Barret)Scene where Aerith makes Barret angry.

Caitsith toujou - GS entrance before you meet Cait Sith.

dio toujou - GS entrance before you have met Dio.

tougijou de - Battle square massacre scene.

kaettekita cloud - Scene in lift before chocobo race.

under corel - Arrival in Corel prison.

Yameta - Cancel

(P2)

GS2

eki - Arrival at Gold Saucer. [STUCK]

hotel matome - Cloud tells us "the story so far.." at the Ghost Hotel.

cs uragiri - End of 'date' sequence [STUCK]

dio no tenjistu - Talking to Dio about obtaining the Keystone.

date no osasoi - 'Date' character comes to Cloud's room.

nigeta cs no saigo - Cait Sith gives the keystone to Tseng.

hotel deppatu - In Cloud's room before leaving the hotel.

yame - Cancel.

## **9. Tokita's Room - BLACKBGI**

Here is Tokita's room, you enter by walking off the top of the main debug room screen.

![](_page_114_Picture_23.jpeg)

#### 9.1 Vincent

This script will add members to the active party in order, overwriting the last one if the party is full.

"party make"

Ballet - Adds Barret

Tifa - Adds Tifa

erith - Adds Aerith

red - Adds Red XII

yufi - Adds Yuffie

ketcy - Adds Cait Sith

vincent - Adds Vincent

cid - Adds Cid

no - cancels

#### 9.2 Red XIII

This script has bad JUMPMAP commands with zeroed locations, causing loaded field files to not execute correctly.

cancel - Cancels.

SPGATE - underwater reactor [STUCK]

SPIPE 1 - In glass tunnel leading to the underwater reactor.

SPIPE 2 - End of glass tunnel. [STUCK]

SEMKIN 1 - Inside pressure lift. [STUCK]

SEMKIN 2 - Stuck on Red Submarine in reactor.

SEMKIN 8 - Underwater reactor scene before boss fight.

SEMKIN 3 - Main scene of underwater reactor. STUCK]

SEMKIN 4 - The reactor chimney. [STUCK]

SEMKIN 5 - Huge Materia loaded into red submarine. S[STUCK]

SEMKIN 6 - Before boarding submarine. [STUCK]

SEMKIN 7 - Shinra troops on the run. [STUCK]

#### 9.3 Yuffie

Also has bad JUMPMAPs as well.

Cancel - cancels

Tucks union - Turks on vacation in Wutai. Flips flag on or off.

DATIO 1 - Dao-Chao base, Wutai.

DATIO 2 - Dao-Chao, center.

DATIO 3 - Dao-Chao, extreme left.

DATIO 4 - Dao-Chao, extreme right .

DATIO 5 - Dao-Chao, lower.

DATIO 6 - Dao-Chao, hand under face.

DATIO 7 - On top of 'saluting' fingers at Dao-Chao.

DATIO 8 - Fire Cave, Dao-Chao.

5TOWER - Bottom of the 'Pagoda of the Five Mighty Gods'.

#### 9.4 Middle Person

Quit - Cancels.

next page - Page 2 of options.

BLACKBGH - Jumps to the BLACKBGH field file, which is blank.

BLACKBGI - Jumps to the BLACKBGI field file, which is the current debug room.

TUNNEL 6 - Railway tunnels in the 'Siege on Midgar' event.

MD8 6 - Outside trapdoor leading to under Midgar. [STUCK]

MD8 B1 - Sector 8 ladder maze, [STUCK]

MD8 B2 - Sector 8 Ladder maze second part.[STUCK]

MD8 32 - Sector 8 below walkway to the Sister Ray.[STUCK]

MD8 BRDG2 - Before you fight the 'Proud Clod'. [STUCK]

TUNNEL 4 - In the train tunnels, trapped behind a closed door.

TUNNEL 5 - Sector 8 train tunnel. [STUCK]

## PAGE 2:

prepage - back to page 1.

CANON 1 - Walkway to the Sister Ray. [STUCK]

CANON 2 - Hojo preparing the Sister Ray.

MTCRL 2 - Outside Mt. Corel Mako Reactor (Huge materia scene).

ZCOAL 1 - Coal train Engineers platform. [STUCK]

ZCOAL 2 - Coal Train crash event.

ZCOAL 3 - Fight against train driver.

4SBWY 22 - Crawling through air duct into Sector 8 train tunnels.

#### 9.5 Aerith

"player change"

cloud - puts Cloud in lead

tifa - Tifa is leader

cid - the same, but with Cid.

cancel - cancels.

#### 9.6 Barret

"materia max"

Yes - Gives you a many Bahamut materias.

No - cancel.

#### 9.7 Cait Sith

cancel - cancels.

LAS2 1 - Final dungeon. 'Left' path, at the fork in the road.

LAS2 2 - First screen of 'watery' route.

LAS2 3 - Second screen of 'watery' route. SIAW.

LAS2 4 - In the middle of the 'glowing crater' (mega all materia). SIAW.

LAS0 6 - End of the 'vertical descent' section of the FD.

LAS0 7 - Side tunnel of above section. SIAW.

LAS0 8 - Start of 'right' path. SIAW.

MOGU 1 - Play 'Mog House' game. Then leads to Gold Saucer.

#### 9.8 Save Point

Tests the save point. (Generic save point script)

#### **10. Katou's Room**

This the final debug room.

![](_page_117_Picture_2.jpeg)

A menu opens upon entering.

For those in a hurry - Takes you to Aerith's menu For those with a little time - Lets you walk around

#### 10.1 Aerith

"Hello there, wanna be-hero. You ready for your journey?"

"So? Where to?"

To Mideel! - Mideel before it has been destroyed. [No PC]

To Mideel Clinic! - Scene where Cloud is in hospital and Tifa is watching him.[No PC]

To the Mideel Talk Event! - Game hangs unless you talk to the Doctor first to set flags

To the Attack Event! - In Mideel Clinic [No PC]

To the Lifestream! - Event in cinic as the ground begins to shake.

To the Mindzone! - Cloud sinking into the Lifestream. To the Spirit World! - Start of 'inside Cloud's mind' event.

To Spirit World2! - Middle part of Lifestream event.

To Spirit World3! - Event where Young Cloud Talks with Tifa.

To the Spirit World again! - Destroyed Mideel.

To Mideel after it fell! - Visit to Nibelheim in Cloud's mind (misaligned menu option).

To Hades! - "It is Hades..."

NOTE: Choosing "For those in a hurry", produces the same results, but the bottom option is now "Hold it, I need a break!", which leads to the battle with WEAPON. The other options are the same, but seem to work much more reliably.

#### 10.2 Nurse

"Who're you going with?"

I'm starting over - Removes all players from the active party.

ster - adds cloud

Princess - adds Aerith

lonia - adds Tifa

alator - adds Barret

Little - adds Yuffie

Red XIII - adds Red XIII

Cait Sith - adds Cait Sith

'Ol - adds Cid

(blank) - adds Vincent

#### 10.3 Doctor

"Take down a flag?"

Mideel - Mideel destroyed flag. Switch this on to enable the "Mideel talk event!" option from Aerith.

Ionia - Tifa flag?

Materia - Huge materia?

To the Dark Hill - Cloud and Tifa together under the Highwind..

To the Light Hill - The morning after.

(Blank) - Highwind whilst Cloud and Tifa are at Mideel.

#### 10.4 The floor

This is a spot on the floor in front of Aerith that when you step on, it talks. It's a trigger test.

#### **Event Scripting**

#### **Script commands**

The event scripting language for FF7 has 246 commands that have a wide array of functions. The following is a complete listing of the commands, opcodes, arguments, and descriptions.

#### Opcode Matrix

|    | 00       | 01           | 02       | 03           | 04      | 05       | 06      | 07       | 08       | 09        | 0a     | 0b       | 0c       | 0d      | 0e     | 0f       |
|----|----------|--------------|----------|--------------|---------|----------|---------|----------|----------|-----------|--------|----------|----------|---------|--------|----------|
| 00 | RET      | REQ          | REQSW    | REQEW        | PREQ    | PRQSW    | PRQEW   | RETTO    | JOIN     | SPLIT     | SPTYE  | GTPYE    | ?0C?     | ?0D?    | DSKCG  | SPECIAL  |
| 10 | GotoNext | GotoNextLong | GotoPrev | GotoPrevLong | IfUByte | IfUByteL | IfSWord | IfSWordL | IfUSWord | IfUSWordL | ­      | ­        | ?1C?     | ­       | ­      | ­        |
| 20 | MINIGAME | TUTOR        | BTMD2    | BTRLD        | wait    | NFADE    | BLINK   | BGMOVIE  | KAWAI    | KAWIW     | PMOVA  | SLIP     | BGPDH    | BGSCR   | WCLS   | WSIZW    |
| 30 | IF­KEY   | IF­KEYON     | IF­KEYOF | UC           | PDIRA   | PTURA    | WSPCL   | WNUMB    | STTIM    | GOLD+     | GOLD­  | CHGLD    | HMPMAX1  | HMPMAX2 | MHMMX  | HMPMAX3  |
| 40 | message  | MPARA        | MPRA2    | MPNAM        | ­       | MP+      | ­       | MP­      | ASK      | MENU      | MENU2  | BTLTB    | ­        | HP+     | ­      | HP       |
| 50 | window   | WMOVE        | WMODE    | WREST        | WCLSE   | WROW     | GWCOL   | SWCOL    | ST­ITM   | DL­ITM    | CK­ITM | SM­TRA   | DM­TRA   | CM­TRA  | SHAKE  | NOP      |
| 60 | MAPJUMP  | SCRLO        | SCRLC    | SCRLA        | SCR2D   | SCRCC    | SCR2DC  | SCRLW    | SCR2DL   | MPDSP     | VWOFT  | FADE     | FADEW    | IDLCK   | LSTMP  | SCRLP    |
| 70 | battle   | BTLON        | BTLMD    | PGTDR        | GETPC   | PXYZI    | PLUS!   | PLUS2!   | MINUS!   | MINUS2!   | INC!   | INC2!    | DEC!     | DEC2!   | TLKON  | RDMSD    |
| 80 | set byte | SET­WORD     | BIT­ON   | BIT­OFF      | BIT­XOR | PLUS     | PLUS2   | MINUS    | MINUS2   | MUL       | MUL2   | DIV      | DIV2     | MOD     | MOD2   | AND      |
| 90 | AND2     | OR           | OR2      | XOR          | XOR2    | INC      | INC2    | DEC      | DEC2     | RANDOM    | LBYTE  | HBYTE    | 2BYTE    | SETX    | GETX   | SEARCHX  |
| a0 | PC       | CHAR         | DFANM    | ANIME1       | VISI    | XYZI     | XYI     | XYZ      | MOVE     | CMOVE     | MOVA   | TURA     | ANIMW    | FMOVE   | ANIME2 | ANIM!1   |
| b0 | CANIM1   | CANM!1       | MSPED    | DIR          | TURNGEN | TURN     | DIRA    | GETDIR   | GETAXY   | GETAI     | ANIM!2 | CANIM2   | CANM!2   | ASPED   | ­      | CC       |
| c0 | JUMP     | AXYZ         | LADER    | OFST         | OFSTW   | TALKR    | SLIDR   | SOLID    | PRTYP    | PRTYM     | PRTYE  | IF­PRTYQ | IF­MEMBQ | MMB+­   | MMBLK  | MMBUK    |
| d0 | LINE     | LINON        | MPJPO    | SLINE        | SIN     | COS      | TLKR2   | SLDR2    | PMJMP    | PMJMP2    | AKAO2  | FCFIX    | CCANM    | ANIMB   | TURNW  | MPPAL    |
| e0 | BGON     | BGOFF        | BGROL    | BGROL2       | BGCLR   | STPAL    | LDPAL   | CPPA     | RTPAL    | ADPAL     | MPPAL2 | STPLS    | LDPLS    | CPPAL2  | RTPAL2 | ADPAL2   |
| f0 | MUSIC    | Sound        | AKAO     | MUSVT        | MUSVM   | MULCK    | BMUSC   | CHMPH    | PMVIE    | MOVIE     | MVIEF  | MVCAM    | FMUSC    | CMUSC   | CHMST  | GAMEOVER |

| Opcode                                                                                                       | Name   |  |  |  |  |  |  |
|--------------------------------------------------------------------------------------------------------------|--------|--|--|--|--|--|--|
| 0x00                                                                                                         | RET    |  |  |  |  |  |  |
| Arguments<br>Definition                                                                                      |        |  |  |  |  |  |  |
| (none)                                                                                                       | (none) |  |  |  |  |  |  |
| Description                                                                                                  |        |  |  |  |  |  |  |
| Returns control back to the standard program loop.<br>Usually you can control the PC again after this point. |        |  |  |  |  |  |  |

| Opcode                                                                                                       | Name   |  |  |  |  |  |
|--------------------------------------------------------------------------------------------------------------|--------|--|--|--|--|--|
| 0x01                                                                                                         | REQ    |  |  |  |  |  |
| Arguments<br>Definition                                                                                      |        |  |  |  |  |  |
| (none)                                                                                                       | (none) |  |  |  |  |  |
| Description                                                                                                  |        |  |  |  |  |  |
| Returns control back to the standard program loop.<br>Usually you can control the PC again after this point. |        |  |  |  |  |  |

| Opcode    | Name       |
|-----------|------------|
| 0x30      | WINDOW     |
| Arguments | Definition |
| id=byte   | Window ID  |

| Name                                        |  |  |
|---------------------------------------------|--|--|
| X coordinate for the upper left hand corner |  |  |
| X coordinate for the upper left hand corner |  |  |
| Width of window in pixels                   |  |  |
| Hight of window in pixels                   |  |  |
| Description                                 |  |  |
|                                             |  |  |

Initializes a windowpane. This does not display a window, but allows for a "container" for the commands ASK and MESSAGE to place text within. It is referenced by it's window ID

| Opcode       | Name                                      |  |
|--------------|-------------------------------------------|--|
| 0x48         | ASK                                       |  |
| Arguments    | Definition                                |  |
| unknown=byte | Unknown                                   |  |
| win=byte     | Window ID to place data into              |  |
| mes=byte     | Which dialog to display from dialog table |  |
| 1st=byte     | Which line is the first choice            |  |
| nth=byte     | Which line is the last choice             |  |
| var=byte     | Unknown                                   |  |
| Description  |                                           |  |

The ASK command opens a window with a set of choices to be picked with the "selector finger" (Yubi) [WHERE IS THIS RETURNED?]

#### **Movies**

#### **The 3D Overlay**

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

#### **Data Organization**

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

- -Textures
- -Polygons
- -Bone Hierarchy
- -Animation
- -Models
- -Movies

#### **"A" Field Animation Files for PC by Mirex**

Each animation file holds one character animation ( run, walk or some other). Some characters have more animation files. Animation is set of frames, in each frame are stored bone rotations.

#### -- animation file contents --

| Name   | Size in bytes |
|--------|---------------|
| header | 24            |

| Name    | Size in bytes        |
|---------|----------------------|
| unknown | 12                   |
| frames  | frames_count * frame |

```
-- one frame, size is ( bones * 12 + 24 ) --
unknown 24 bytes = 6 floats
rotations bones * 12 bytes = bones * 3 floats
```

| Name      | Size                                |
|-----------|-------------------------------------|
| unknown   | 24 = 6 floats                       |
| rotations | bones * 12 bytes = bones * 3 floats |

#### header structure, 24 bytes

```
struct {
 unsigned long x1;
 unsigned long frames_count;
 unsigned long bones_count;
 unsigned long x2, x3, x4;
} anim_head;
```

I understand only two values from the header, 'frames\_count' which is number of animation frames and 'bones\_count' which is suprisingly number of animated bones. ;)

If you want to load all possible animations for the model (even animations of different models) then check if animation file has same number of bones as current model.

After header there is 12 bytes of data that are unknown to me. It could be some center of the coordinate system or anything.

Frame starts with 6 floats (unknown), followed by rotations for each bone. Rotations are stored as 3 floats (float is 4byte floating-point number).

## **Movies**


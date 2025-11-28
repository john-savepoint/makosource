# FF7/Savemap

< [FF7](https://qhimm-modding.fandom.com/wiki/FF7 'FF7')

[

](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#articleComments)[Sign in to edit](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit&uselang=en)

- [History](https://qhimm-modding.fandom.com/wiki/FF7/Savemap?action=history)
- [Purge](https://qhimm-modding.fandom.com/wiki/FF7/Savemap?action=purge)
- [Talk (0)](https://qhimm-modding.fandom.com/wiki/Talk:FF7/Savemap?action=edit&redlink=1)

## Contents

- [1 The Savemap](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#The_Savemap)
- [2 Save Memory Bank 1/2](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_1/2)
- [3 Save Memory Bank 3/4](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_3/4)
- [4 Save Memory Bank B/C](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_B/C)
- [5 Save Memory Bank D/E](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_D/E)
- [6 Save Memory Bank 7/F](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_7/F)
- [7 Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)
- [8 Chocobo Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Chocobo_Record)
- [9 Save Item List](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Item_List)
- [10 Save Materia List](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Materia_List)
- [11 KERNEL.BIN Section 4 Entry](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#KERNEL.BIN_Section_4_Entry)
- [12 Documentation Notes & Format](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Documentation_Notes_&_Format)

### The Savemap\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D1&uselang=en 'Sign in to edit')\]

The following is the general save format for the game. This data excludes the header data that differs between the PSX and PC version. (PSX header is 512 Bytes, checksum @ 0x200) (PC header is 9 bytes, checksum @ 0x11) Note: For the _preview_ descriptions below, changing these values does not change any in-game values. These are only used so a player can preview the data within the save file when viewing the Save menu.

**Table 1: FF7 Save Slot**

Offset

Length

Description

0x0000

2(4) bytes

Checksum ([how to generate](http://forums.qhimm.com/index.php?topic=4211.msg60545#msg60545))  
Technically this is a DWord, but the checksum generation method only stores the lower Word.

0x0004

1 byte

**Save Preview**: Lead character's level

0x0005

1 byte

**Save Preview**: Lead character's portrait

0x00: Cloud  
0x01: Barret  
0x02: Tifa  
0x03: Aeris  
0x04: Red XIII  
0x05: Yuffie  
0x06: Cait Sith

0x07: Vincent  
0x08: Cid  
0x09: Young Cloud  
0x0A: Sephiroth  
0x0B: Chocobo  
0xFF: None

0x0006

1 byte

**Save Preview**: 2nd character's portrait

0x0007

1 byte

**Save Preview**: 3rd character's portrait

0x0008

16 bytes

**Save Preview**: Lead character's name, [FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text') , terminated with 0xFF

0x0018

2 bytes

**Save Preview**: Lead character's current HP

0x001A

2 bytes

**Save Preview**: Lead character's max HP

0x001C

2 bytes

**Save Preview**: Lead character's current MP

0x001E

2 bytes

**Save Preview**: Lead character's max MP

0x0020

4 bytes

**Save Preview**: Amount of Gil

0x0024

4 bytes

**Save Preview**: Total number of seconds played

0x0028

32 bytes

**Save Preview**: Save location, [FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'), terminated with 0xFF

0x0048

3 bytes

RGB value for upper left corner of window

0x004B

3 bytes

RGB value for upper right corner of window

0x004E

3 bytes

RGB value for lower left corner of window

0x0051

3 bytes

RGB value for lower right corner of window

0x0054

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Cloud

0x00D8

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Barret

0x015C

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Tifa

0x01E0

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Aeris's

0x0264

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Red XIII

0x02E8

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Yuffie

0x036C

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Cait Sith (or Young Cloud)

0x03F0

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Vincent (or Sephiroth)

0x0474

132 bytes

**[Character Record](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Character_Record)**: Cid

0x04F8

1 byte

Party member in slot 1 \[uses same format as character portrait above\]

0x04F9

1 byte

Party member in slot 2

0x04FA

1 byte

Party member in slot 3

0x04FB

1 byte

Alignment (Always 0xFF)

0x04FC

640 bytes

Party Item stock, 2 bytes per item, 320 item slots max \[See [save item list](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Item_List) below\]

0x077C

800 bytes

Party Materia stock, 4 bytes per materia, 200 materia max \[See [save materia list](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Materia_List) \]

0x0A9C

192 bytes

Materia stolen by Yuffie, 4 bytes per materia, 48 materia max \[See [save materia list](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Materia_List) \]

0x0B5C

32 bytes

z_3 Unknown (Always 0xFF?)

0x0B7C

4 bytes

Party's Gil amount

0x0B80

4 bytes

Total number of seconds played

0x0B84

4 bytes

Countdown Timer (in seconds)

0x0B88

12 bytes

z_4 Unknown

0x0B88  
z_4\[0\]

4 byte

Used to calculate fractions of seconds (1/65535) of Game timer (0x0B80).  
Technically this is a DWord, but only the lower Word is used.

0x0B8C  
z_4\[4\]

4 byte

Used to calculate fractions of seconds (1/65535) of Countdown timer (0x0B84).  
Share the same value with 0x0B88.

0x0B90  
z_4\[8\]

4 byte

This is set along with Current map value (0x0B94).  
If Current module value is 1, this is set to 2.  
If Current module value is 3, this is set to 0.  
Technically this is a DWord, but only the lower Byte is used.

0x0B94

2 bytes

Current [module](https://qhimm-modding.fandom.com/wiki/FF7/Engine_basics 'FF7/Engine basics')  
If value is 1, the game was saved in the field.  
If value is 3, the game was saved in the world map.

0x0B96

2 bytes

Current location

0x0B98

2 bytes

Alignment (Always 0x00)

0x0B9A

2 bytes

X location on Field map (Signed)

0x0B9C

2 bytes

Y location on Field map (Signed)

0x0B9E

2 bytes

Triangle Id of player on Field map (Unsigned)

0x0BA0

1 byte

Direction of Player Model on Field Map(Unsigned)

0x0BA1

3 bytes

z_6 Unknown

0x0BA1  
z_6\[0\]

1 byte

Field Encounter Timer: StepID/Seed ([\[1](http://web.archive.org/web/20170518233623/http://forums.qhimm.com/index.php?topic=6431.msg81091#msg81091)\])

0x0BA2  
z_6\[1\]

1 byte

Field Encounter Timer: Offset ([\[2](http://web.archive.org/web/20170518233623/http://forums.qhimm.com/index.php?topic=9625.msg191219#msg191219)\])

0x0BA3  
z_6\[2\]

1 byte

Alignment (Always 0x00)

0x0BA4

\[BEGINNING OF FIELD SCRIPT MEMORY [BANK 1 (1/2)](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_1.2F2)\]

0x0CA4

\[BEGINNING OF FIELD SCRIPT MEMORY [BANK 2 (3/4)](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_3.2F4)\]

0x0DA4

\[BEGINNING OF FIELD SCRIPT MEMORY [BANK 3 (B/C)](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_B.2FC)\]

0x0EA4

\[BEGINNING OF FIELD SCRIPT MEMORY [BANK 4 (D/E)](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_D.2FE)\]

0x0FA4

\[BEGINNING OF FIELD SCRIPT MEMORY [BANK 5 (7/F)](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Save_Memory_Bank_7.2FF)\]

0x10A4

2 bytes

PHS Locking Mask (1: Locked)

LSB

Cloud

Barret

Tifa

Aeris

Red

Yuffie

Vincent

Cait

Cid

MSB

0x10A6

2 bytes

PHS Visibility Mask (does not _turn off_ party characters)

LSB

Cloud

Barret

Tifa

Aeris

Red

Yuffie

Vincent

Cait

Cid

MSB

0x10A8

48 bytes

z_39 Unknown (Always 0x00?)

0x10D8

1 byte

Battle Speed (0x00: fastest, 0xFF: slowest)

0x10D9

1 byte

Battle Message Speed

0x10DA

1 byte

General configuration

Sound: mono (0x00); stereo (0x01)

Controller: normal (0x00); customize (0x04)

Cursor: initial (0x00); memory (0x10)

ATB: Active (0x00); Recommended (0x40); Wait (0x80)

0x10DB

1 byte

General configuration (continued)

Camera angle: Auto (0x00); Fix (0x01)

Magic order: (game crashes if flag set to 0x18 or 0x1C)  
"1. restore attack indirect" (0x00)  
"2. restore indirect attack" (0x04)  
"3. attack indirect restore" (0x08)  
"4. attack restore indirect" (0x0C)  
"5. indirect restore attack" (0x10)  
"6. indirect attack restore" (0x14)

Extra battle window displaying information: Inactive (0x00); Active (0x40)

0x10DC

16 bytes

Controller Mapping (PSX ONLY)  
l2,r2,l1,r1,tri,circle,cross,square,Select,?,?,Start,u,r,d,l  
l2,r2,l1,r1,Menu,OK,Cancel,Ext,Help,?,?,Pause,u,r,d,l

0x10EC

1 byte

Message Speed

0x10ED

8 bytes

z_40 Unknown (Always 0x00?)

## Save Memory Bank 1/2\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D2&uselang=en 'Sign in to edit')\]

**Table 1: FF7 Save Slot**

Offset

Length

Description

0x0BA4

2 byte

Main progress variable

0x0BA6  
z_7\[0\]

1 Byte

Yuffie's Initial Level (z_7 Unknown) Byte value before Yuffie join the team: 0x00.  
(If byte's value is changed, then you can't fight Yuffie, so she can't be obtained).  
Yuffie's Initial Level only is set when she already join the team.  
Credit to (NFITC1)

0x0BA7

1 byte

Aeris' current love points

0x0BA8

1 byte

Tifa's current love points

0x0BA9

1 byte

Yuffie's current love points

0x0BAA

1 byte

Barret's current love points

0x0BAB

17 bytes

z_8 Unknown

0x0BAB  
z_8\[0\]

1 byte

1st temp party member char ID placeholder  
This is used to store the player's party configuration before they are overridden for a special event that requires a specific character setup using GTPYE. {elm/first/s1}  
The player's original party configuration can then be set back to its original setup using SPTYE. {elminn_2/ballet/s11}

0x0BAC  
z_8\[1\]

1 byte

2nd temp party member char ID placeholder

0x0BAD  
z_8\[2\]

1 byte

3ed temp party member char ID placeholder

0x0BAE  
z_8\[3\]

6 byte

Unknown (Always 0x00?)

0x0BB4  
z_8\[9\]

1 byte

Game Timer Hours

0x0BB5  
z_8\[10\]

1 byte

Game Timer Minutes

0x0BB6  
z_8\[11\]

1 byte

Game Timer Seconds

0x0BB7  
z_8\[12\]

1 byte

Game Timer Frames. From 0x00 to ~0x21 in one sec.(33 FPS?)

0x0BB8  
z_8\[13\]

1 bytes

Countdown Timer Hours

0x0BB9  
z_8\[14\]

1 bytes

Countdown Timer Minutes

0x0BBA  
z_8\[15\]

1 bytes

Countdown Timer Seconds

0x0BBB  
z_8\[16\]

1 bytes

Countdown Timer Frames. From 0 to 30 (dec) in one sec.

0x0BBC

2 bytes

Number of battles fought

0x0BBE

2 bytes

Number of escapes

0x0BC0

2 bytes

Menu Visiblity Mask (Quit not affected)

LSB

item

magic

materia

equip

status

order

limit

config

PHS

save

MSB

0x0BC2

2 bytes

Menu Locking Mask (1: Locked) (Quit not affected)

LSB

item

magic

materia

equip

status

order

limit

config

PHS

save

MSB

0x0BC4

16 bytes

z_9 Unknown

0x0BC4  
z_9\[0\]

4 byte

Unknown (Always 0x00?)

0x0BC8  
z_9\[4\]

1 byte

Field Items, Sector 7 Train Graveyard  
Item bit mask (LBS) (applied when you pick them up).  
Bit=0(Item on the floor), Bit=1(Item Picked Up).  
0x01: Hi-Potion.(mds7st1|Barrel 1)  
0x02: Echo Screen.(mds7st1|Barrel 2)  
0x04: Potion.(mds7st2|Floor 2)  
0x08: Ether.(mds7st2|Floor 3)  
0x10: Hi-Potion.(mds7st1|Roof Train 1)  
0x20: Potion.(mds7st1|Inside Train 2)  
0x40: Potion.(mds7st1|Floor 1)  
0x80: Hi-Potion.(mds7st2|Roof Train 2)

0x0BC9  
z_9\[5\]

1 byte

Field Items  
0x01: Elixir {hyou8_2/tr00/s1}  
0x02: Potion {hyou5_1/tr00/s1}  
0x04: Safety Bit {hyou5_3/trbox/s1}  
0x08: Mind Source {hyou2/trbox/s1}  
0x10: Sneak Glove {mkt_w/event/s1}  
0x20: Premium Heart {mkt_ia/event/s3}{mkt_ia/line00/s4}  
0x40: Unused  
0x80: Unused

0x0BCA  
z_9\[6\]

10 byte

Unknown (Always 0x00?)

0x0BD4

1 byte

Item bit mask (LBS)(applied when you pick them up). Field Item / Materia  
Bit=0(Item on the floor), Bit=1(Item Picked Up).  
0x01: Potion {md8_3/p/s1}  
0x02: Potion + Phoenix Down {ealin_2/zu/s1}  
0x04: Ether {eals_1/p/s1}  
0x08: Cover Materia {eals_1/mp/s1}  
0x10: Choco-Mog Summon {farm/dancer/s1}  
0x20: Sense Materia {mds6_22/mat/s1}  
0x40: Ramuh Summon {crcin_2/mat/s1}  
0x80: Mythril Key Item {zz1/m1/s1}

0x0BD5

1 byte

Materia Cave / Northern Cave (Item bit mask)  
0x01: Mime Materia {zz5/l1,l2,l3,l4/s1}  
0x02: HP<->MP Materia {zz6/mat/s1}  
0x04: Quadra Magic Materia {zz7/l1,l2,l3,l4/s1}  
0x08: Knights of the Round Summon {zz8/l1,l2,l3,l4/s1}  
0x10: Elixir {las3_1/hako1/s1}{las4_0/cid/s1}  
0x20: X-Potion {las3_1/hako2/s1}  
0x40: Turbo Ether {las3_2/hako1/s1}{las4_0/tifa/s1}{las4_0/cait/s1}  
0x80: Vaccine {las3_2/hako2/s1}{las4_0/yufi/s1}

0x0BD6

14 bytes

z_10 Unknown

0x0BD6  
z_10\[0\]

1 byte

Field Items Northern Cave  
0x01: Magic Counter Materia {las3_2/mat/s1}  
0x02: Speed Source {las3_3/hako1/s1}{las4_0/red/s1}  
0x04: Turbo Ether {las3_3/hako2/s1}  
0x08: X-Potion {las3_3/hako3/s1}  
0x10: Mega All {las3_3/mat/s3}{las4_0/vincent/s1}  
0x20: Luck Source {las4_1/hako1/s1}  
0x40: Remedy {las3_1/hako3/s1}{las4_0/ballet/s1}  
0x80: Bolt Ring {zz1/m1/s1}

0x0BD7  
z_10\[1\]

1 byte

Field Items  
0x01: Gold Armlet {zz2/m/s8}  
0x02: Great Gospel {zz2/m/s7}  
0x04: Shooting Coaster prize Umbrella {jetin1/dic/s0}  
0x08: Shooting Coaster prize Flayer {jetin1/dic/s0}  
0x10: Death Penalty + Chaos {zz4/buki/s1}  
0x20: Elixir {ghotin_2/reizo/s1}  
0x40: Enemy Skill animation displayed {zz3/mat/s3}  
0x80: Enemy Skill {zz3/mat/s1}

0x0BD8  
z_10\[2\]

4 byte

Unknown (Always 0x00?)

0x0BDC  
z_10\[6\]

1 byte

Field Items, Sector 7 Wall Market and Shinra HQ  
Item bit mask (LBS) (applied when you pick them up).  
Bit=0(Item on the floor), Bit=1(Item Picked Up).  
0x01: Ether.(Corneo's masion basement floor) {colne_4/TAKARA/s1}  
0x02: Hyper.(Corneo's masion corneo 's bedroom floor) {colne_6/TAKARA/s1}  
0x04: Phoenix Down (Corneo's masion 2nd floor right room) {colne_3/TAKARA/s1}  
0x08: Elixir at Shinra HQ stairs {blinst_2/TAKARA/s1}  
0x10: Unused  
0x20: Magic Source {cosmin7/TAKARA/s1}  
0x40: First Midgar Part Key Item {blin65_1/PARTA/s1}  
0x80: Second Midgar Part at Shinra HQ {blin65_1/PARTB/s1}

0x0BDD  
z_10\[7\]

1 byte

Field Items, Shinra HQ  
Item bit mask (LBS) (applied when you pick them up).  
Bit=0(Item on the floor), Bit=1(Item Picked Up).  
0x01: Third Midgar Part Key Item {blin65_1/PARTC/s1}  
0x02: Fourth Midgar Part Key Item {blin65_1/PARTD/s1}  
0x04: Fifth Midgar Part Key Item {blin65_1/PARTE/s1}  
0x08: Keycard 66 Key Item {blin65_1/TAKARA/s1}  
0x10: All Materia {shpin_2/TAKARAA/s1}  
0x20: Ether {shpin_2/TAKARAB/s1}  
0x40: Wind Slash {shpin_3/TAKARA/s1}  
0x80: Fairy Ring {gidun_4/TAKARAA/s1}

0x0BDE  
z_10\[8\]

1 byte

Field Items  
0x01: X-Potion {gidun_4/TAKARAB/s1}  
0x02: Added Effect Materia {gidun_1/TAKARAA/s1}  
0x04: Black M-phone {gidun_2/TAKARAA/s1}  
0x08: Ether {gidun_2/TAKARAB/s1}  
0x10: Elixir {cosmin6/TAKARA/s1}  
0x20: HP Absorb Materia {hideway3/TAKARA/s4}  
0x40: Magic Shuriken {hideway1/TAKARA/s4}  
0x80: Hairpin {hideway2/TAKARA/s4}

0x0BDF  
z_10\[9\]

1 byte

Field Items  
0x01: Keycard 62 Key Item {blin61/ZAKOA/s1}  
0x02: MP Absorb Materia {uta_im/TAKARAA/s1}  
0x04: Swift Bolt {uttmpin4/TAKARAA/s1}  
0x08: Elixir {uttmpin4/TAKARAB/s1}  
0x10: Pile Bunker {blin2_i/TAKARAA/s1}  
0x20: Master Fist {blin2_i/TAKARAB/s1}  
0x40: Behemoth Horn {blinst_2/TAKARB/s1}  
0x80: Full Cure Materia {cosmin7/TAKARAA/s1}

0x0BE0  
z_10\[10\]

4 byte

Unknown (Always 0x00?)

0x0BE4

8 bytes

Key items \[see Key Item List\]

0x0BEC

8 bytes

z_11 Unknown

0x0BEC  
z_11\[0\]

1 byte

Northern Cave - Progress (TODO: more info)

0x0BED  
z_11\[1\]

1 byte

Unknown (Always 0x00?)

0x0BEE  
z_11\[2\]

1 byte

Northern Cave - Progress (TODO: more info)

0x0BEF  
z_11\[3\]

1 byte

Items mask, Chocobo Farm (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Activated right after getting Choco-Mog{farm/mat/s1}(Is set by kernel, not from Field) (See 0x0BD4\[4\])  
0x02: Activated right after getting Enemy Skill {blin68_2/mtr/s1}(Is set by kernel, not from Field) (See 0x0FC6\[2\])  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0BF0  
z_11\[4\]

4 byte

Unknown (Always 0x00?)

0x0BF4

1 byte

Aeris battle love points

0x0BF5

1 byte

Tifa battle love points

0x0BF6

1 byte

Yuffie battle love points

0x0BF7

1 byte

Barret battle love points

0x0BF8

1 bytes

z_12 Unknown

0x0BF9

1 byte

Rating for Penned Chocobo Number 1 (01: Wonderful -> 08: Worst)

0x0BFA

1 byte

Rating for Penned Chocobo Number 2

0x0BFB

1 byte

Rating for Penned Chocobo Number 3

0x0BFC

1 byte

Rating for Penned Chocobo Number 4

0x0BFD

2 bytes

z_13 Unknown

0x0BFF

3 bytes

Ultimate Weapon's remaining HP

0x0C02

28 bytes

z_14 Unknown

0x0C02  
z_14\[0\]

1 byte

Northern Cave, bit mask  
0x01: Set if Dragon Zombie has used Pandora's Box  
0x02: Unknown  
0x04: Northern Cave - Progress (TODO: more info)  
0x08: Unknown  
0x10: Unknown  
0x20: Northern Cave - Bizarro Sephiroth Battle Progress: Second time you switch between party groups in battle change to 0xE0.  
0x40: Northern Cave - Bizarro Sephiroth Battle Progress: First time you switch between party groups in battle change to 0xC0.  
0x80: Northern Cave - Bizarro Sephiroth Battle Progress: Set to 0x80 on Bizarro Sephiroth battle start.

0x0C14  
z_14\[18\]

2 bytes

Current Battle Points (Battle Square)

0x0C18  
z_14\[22\]

1 byte

Current Number of Battles Won (Battle Square)

0x0C1E

1 bytes

Needs more research. (bit=0: show tutorial. bit=1: hide tutorial.)  
0x01: Junnon Parade (Jump to map junone22) {junonr1/evl0/s3}  
0x02: Space Animation displayed {rcktin7/space/s3}  
0x04: Grey Submarine Tutorial already seen?  
0x08: Forgotten City Animation displayed {loslake1/ev1/s3}  
0x10: unknown  
0x20: Snow Area Tutorial already seen?  
0x40: Display Field Help  
0x80: Bizarro Sephiroth Battle, set if main group is currently fighting.

0x0C1F

1 bytes

Weapons Killed  
0x01: Ultimate Weapon killed (enables Special Battles at Battle Sq) {COLOIN1/s2/s1}  
0x04: Ultima Weapon's HP < 20,000  
0x08: Ruby Weapon  
0x10: Emerald Weapon

0x0C20

4 bytes

z_15 Unknown

0x0C20  
z_15\[0\]

1 byte

Which Chocobo was taken out from the stable.  
00 / 01 - 06 Which stable's Chocobo was taken out. The stable is displayed empty, but still occupied. 00: Chocobo can be taken out even if another Chocobo is exist on world map. - (\* Glitch) Not 00: Chocobo cannot be taken out even if no Chocobo is exist on world map.

0x0C21  
z_15\[1\]

1 byte

Riding off wild chocobo dialog options.  
0x01 Enter direction to Chocobo Farm & Show send/release Wild Chocobo option when riding off. ON: Right of ranch / Show option OFF: In front of cage / Hide option Set to "ON" after buying chocobo stable.

0x0C22  
z_15\[2\]

1 byte

Chocobo display value on world map (LBS).  
Bit=0(Disabled), Bit=1(Enabled).  
Ex: Wild Chocobo (0x01) + Black Chocobo (0x20) = Byte value 0x21  
0x01: Caught wild chocobo  
0x02: Riding Chocobo  
0x04: Yellow  
0x08: Green  
0x10: Blue  
0x20: Black  
0x40: Gold  
0x80: None?

0x0C23  
z_15\[3\]

1 byte

Vehicle display value on world map (LBS).  
Note: if disk is different than 1, buggy is invisible.  
Bit=0(Disabled), Bit=1(Enabled).  
Ex: Buggy (0x01) + Tiny Bronco (0x04) = Byte value 0x05  
Byte value 0x00: None  
0x01: Buggy  
0x02: Buggy (bit=1:Driving it | bit=0: Don't)  
0x04: Tiny Bronco  
0x08: Unknown/Unused  
0x10: Highwind  
0x20: Highwind (bit=1: Flying in the sky | bit=0: On the ground)  
0x40: Unknown/Unused  
0x80: Unknown/Unused

0x0C24

97 bytes

z_16 Unknown

0x0C24  
z_16\[0\]

1 byte

Field mask, Corel (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Barret talks about his hometown before enter the Ropeway for first time {ROPEST\[1\]\[1-Main\]\[49\]}  
0x02: Free rest in corel inn {NCOINN\[0\]\[0-Main\]\[5\]}  
0x04: Villagers rebuke Barret {NCOREL\[13\]\[1\]\[3\]}  
0x08:  
0x10:  
0x20: If you couldn't stop the train {NCOREL2\[5\]\[2\]\[4\]}  
0x40: Huge Materia Key Item {NOREL3\[1\]\[0-Main\]\[7\]}  
0x80: Ultima Materia {NCOREL2\[2\]\[4\]\[26\]}{NCOREL3\[24\]\[4\]\[20\]}{NCOIN2\[8\]\[1\]\[25\]}

0x0C25  
z_16\[1\]

1 byte

Field mask (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Priscilla Warnings (Reset after read): "It gets deeper the farther you go..." or (High Voltage through tower base) {UJUNON2/cloud/s12}  
0x02: Oldman: "Young man, do CPR!" {UJUNON4/oldm1/s3}  
0x04: Free rest: "You all must be tired. If you want to get some rest, stay here." {JUMIN/drctr/s0}  
0x08: Talk with oldm1 about seeing "a man with a black cape" {UJUNON1/cloud/s10}  
0x10: Priscilla: "It gets deeper the farther you go..." {UJUNON2/cloud/s12}  
0x20: Tifa: "No...it was 5 years ago" {JUMIN/tifa/s9}  
0x40: Cloud: "Hey!!" (Group designate cloud to clim the High Tower) {ujunon1/cloud/s15}  
0x80: If you reach the top of the pole{UJUNON3/ad/s5}

0x0C26  
z_16\[2\]

1 byte

Field mask (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: man1: "It's dangerous, please don't go!" if you choose "I'm still going" {SNOW/man1/s3}  
0x02: Snowboard Key Item {SNMIN1/board/s1}  
0x04: If you choose to kick Shinra Soldier's butt {SNOW/SINRAH1,SINRAH2,SINRAH3/s2}  
0x08: Elena punch Cloud {SNOW/man1/s3}{SNOW/irena/s11}  
0x10: Cloud wake-up in Gast home after beeing punched {SNMAYOR/drctr/s0}  
0x20: The boy gives you his snowboard {SNMIN1/boy/s1}  
0x40: Glacier Map Key Item {SNMIN2/dscvmap/s4}  
0x80: First time you do Snowboard {SNOW/playgam/s2}

0x0C27  
z_16\[3\]

1 byte

Field mask (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: If you succeed climbing (to the top, not the cave, just before crater_1 map) {GAIA_32/ladd5/s4}  
0x02: If you Push-over the rock {GAIIN_2/icerock/s1}  
0x04: Ice Pillar 1 down {GAIIN_5/turara1/s3}  
0x08: Ice Pillar 2 down {GAIIN_5/turara2/s3}  
0x10: Ice Pillar 3 down {GAIIN_5/turara3/s3}  
0x20: Ice Pillar 4 down {GAIIN_5/turara4/s3}  
0x40: First time you enter Holzoff's house(2nd room) / If you collaps at the Great Glacier {HOLU_2/drctr/s0}  
0x80: History about Yamski and mini Cliff tutorial {HOLU_1/drctr/s0}

0x0C28  
z_16\[4\]

1 byte

Field mask (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: First time you enter GAIAFOOT map talk {GAIAFOOT/drctr/s0}  
0x02:  
0x04: Tifa ask you take her with you {CRATER_2/drctr/s0}  
0x08: Rufus finds the crater {TRNAD_2/hikutei/s2}  
0x10: Sephiroth: "This is the end...for all of you" then his body vanish {TRNAD_4/discver/s2}  
0x20:  
0x40: Sephiroth illusion Nibelheim{WOA_3/gonivl1,gonivl2,gonivl3/s2}  
0x80: First time cloud enter map crater_1 and talk about meteor and the crater {CRATER_1/drctr/s0}

0x0C29  
z_16\[5\]

1 byte

Field mask, Whirlwind Maze (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: If you give the Black Materia to Barret {TRNAD_1/ballet/s1}  
0x02: If you give the Black Materia to {TRNAD_1/red/s1}  
0x04: Entrust the Black Materia {TRNAD_1/ballet/s1}  
0x08: Tifa tells you need to cross when the wind is calm {WOA_1/setume3/s2}  
0x10: 12 Black Cape man down {TRNAD_3/drctr/s0}  
0x20: Black Cape man down {WOA_1/drctr/s0}  
0x40: Black Cape man down {CRATER_1/blkdown/s4}  
0x80: Black Cape man jump off {TRNAD_2/drctr/s0}

0x0C2A  
z_16\[6\]

1 byte

Field mask, Whirlwind Maze (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Cloud: "What happened to this town? It's so run-down" {UJUNON1/drctr/s0}  
0x02: If you have taken the Glacier Map before he offers you to, man3: "What nerve! You already tore down the map."  
0x04: Screen shake then Random Battle{GAIIN_6/drctr/s0}  
0x08: Shiva Summon in Priscilla's house {PRISILA/sivamt/s1}  
0x10: Black Cape man: "Ughâ¦ Errgaahh!!" {GAIIN_6/drctr/s0}  
0x20: oldm1: "What? Cloud is missing?" {UJUNON1/oldm1/s1}  
0x40: Prisila/Tifa talk about at prisila's house while cloud is missing in lifestream {PRISILA/prisl/s1}  
0x80: Prisila/Cloud Talk at prisila's house after lifestream {PRISILA/drctr/s0}

0x0C2B  
z_16\[7\]

1 byte

Field mask, Whirlwind Maze (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Cid regets about gaving the Huge Materia to the Shinra {NCOREL/worry/s2}  
0x02: After Barret finish talking about his hometown history then enters the ropeway {ROPEST/ad/S3}  
0x04: Cid tell Prisila they have found Cloud {PRISILA/prisl/s1}  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0C44  
z_16\[32\]

1 byte

Progress items, Wallmarket (LBS).  
Bit=0(Item not obtained), Bit=1(Item obtained).  
0x01: Cologne at Wallmarket {mktpb/woman2/s1}  
0x02: Flower Cologne at Wallmarket {mktpb/woman2/s1}  
0x04: Sexy Cologne at Wallmarket {mktpb/woman2/s1}  
0x08: Wig at Wallmarket {mkt_mens}  
0x10: Dyed Wig at Wallmarket {mkt_mens}  
0x20: Blonde Wig at Wallmarket {mkt_mens}  
0x40: Pharmacy coupon at Wallmarket {mkt_s2/line01/s3}  
0x80: Obtained any Wig at Wallmarket {mkt_mens/event/s1}

0x0C45  
z_16\[33\]

1 byte

Progress items, Wallmarket (LBS).  
Bit=0(Item not obtained), Bit=1(Item obtained).  
0x01: Girl at Honey Bee Inn put make-up on cloud, poor result (result is random) {onna2/girl1/s3}  
0x02: Girl at Honey Bee Inn put make-up on cloud, averange result (result is random) {onna2/girl1/s3}  
0x04: Girl at Honey Bee Inn put make-up on cloud, best result (result is random) {onna2/girl1/s3}  
0x08: Obtaining the dress at Wallmarket {mkt_s1/event/s2}  
0x10: Dress selected (clean/soft,shiny/shimmers) {mktpb/oldm3/s1}  
0x20: Cotton Dress \[0xCA\] {mktpb/oldm3/s1}  
0x40: Satin Dress \[0xAA\] {mktpb/oldm3/s1}  
0x80: Silk Dress \[0x9A\] {mktpb/oldm3/s1}

0x0C46  
z_16\[34\]

1 byte

Progress items, Wallmarket (LBS).  
Bit=0(Item not obtained), Bit=1(Item obtained).  
0x01: Disinfectant at Wallmarket {mkt_s3/tensyu}  
0x02: Deodorant at Wallmarket {mkt_s3/tensyu}  
0x04: Digestive at Wallmarket {mkt_s3/tensyu}  
0x08: Materia shop owner ask you to get something from the inn vending machine {MKT_M/tensyu/s1}  
0x10: 200 gil Item at vending machine in Wallmarket {mktinn/cloud/s4}  
0x20: 100 gil Item at vending machine in Wallmarket {mktinn/cloud/s4}  
0x40: 50 gil Item at vending machine in Wallmarket {mktinn/cloud/s4}  
0x80: Boutique owner's son ask you to bring his father back from bar {mkt_s1/man1/s8}

0x0C47  
z_16\[35\]

1 byte

Ms. Cloud Bauty level (Don Corneo choice) (0 to 25 Points)  
1 Point: Cotton Dress, Wig, Glass Tiara, Cologne, Poor Make-Up  
3 Points: Satin Dress, Dyed Wig, Ruby Tiara, Flower Cologne, Averange Make-Up  
5 Points: Silk Dress, Blonde Wig, Diamond Tiara, Sexy Cologne, Best Make-Up  
Unfinished Calc Script for this items (Not taken into account by point calc):  
Lingerie (Should be +1), Mystery panties (+3), Bikini briefs (+5)  
2 to 11 Points: Choose Tifa  
12 to 18 Points: Choose Aerith  
19 or more Points: Choose Cloud

0x0C48  
z_16\[36\]

1 byte

Field Objects, Sector 7 Train Graveyard (LBS) (so far)  
Bit=0(Original Position), Bit=1(Moved).  
0x01: Train 1 Position. {mds7st2}  
0x02: Train 2 Position. {mds7st2}  
0x04: Train 3 Position. {mds7st2}  
0x08, 0x10, 0x20, 0x40, 0x80: Unused

0x0C49  
z_16\[37\]

1 byte

Field Items, Sector 7 Wall Market  
Items bit mask (LBS)  
0x01: Cloud see the first battery holder and figured out the idea of using a battery there... {wcrimb_1}  
0x02: First battery applied up the wall of Wallmarket(0x02){wcrimb_1}  
0x04: Second battery applied up the wall of Wallmarket(0x04){wcrimb_1}  
0x08:  
0x10: Third battery applied and Ether obtained up the wall of Wallmarket (0x10){wcrimb_2}  
0x20: Battery (Gun shop batery pack 1/3){MKT_W/oyaji02/s1}  
0x40: Battery (Gun shop batery pack 2/3){MKT_W/oyaji02/s1}  
0x80: Battery (Gun shop batery pack 3/3){MKT_W/oyaji02/s1}  
Note: all 3 batteries get at same time.

0x0C4A  
z_16\[38\]

1 byte

Number of Fort Condor Battles Fought

0x0C4B  
z_16\[39\]

1 byte

Number of Fort Condor Battles Won

0x0C4C  
z_16\[40\]

1 byte

Progress, Fort Condor  
0x01: Oldman sited ask your help to protect the Condor \[0x01\] {convil_1/event/s13}  
0x02: If 0x01 &Cloud join them to fight Shinra \[0x03\] {convil_1/cloud/s18}  
0x04: If 0x02 & you talk him again: \[0x07\] {convil_1/event/s15}  
A) He tells you he already talk to the store owners to sell you items.  
B) He let you rest for free.  
0x08: When set they tell you that there are no more shinra troops to fight\[0x0F\] {convil_2/event/s4}  
0x10: Banished from Fort Condor after loosing the Huge Materia Boss Fight: Party talk {convil_2/event/s11}-->{condor2/init/s0}-->{condor2/event/s3}  
0x20: Phoenix Materia (Then Condor fly) {convil_4/ph_mat/s1}  
0x40: Condor Born movie() {convil_2/event/s11}  
0x80: Banished from Fort Condor after loosing the Huge Materia Boss Fight: Cutted rope {convil_2/event/s11}-->{condor2/init/s0}

0x0C4D  
z_16\[41\]

1 byte

Battle Rank (Battle difficulty), Fort Condor  
01: Rank 1 (Battles 1-3)  
02: Rank 2 (Battles 4-6)  
03: Rank 3 (Battles 7-9)  
04: Rank 4 (Battles 10-12)  
05: Rank 5 (Battles 13+)  
06: Rank 6 (Huge Materia battle)  
The Battle Rank set the number of enemies. Fire Catapults enabled from Rank 2, and Tristoners from Rank 3.

0x0C4E  
z_16\[42\]

1 byte

Number of Allies left, Fort Condor  
The number of surviving allies units. (The ones that you give in exchange for gil)

0x0C4F  
z_16\[43\]

1 byte

Number of Enemies killed, Fort Condor

0x0C50  
z_16\[44\]

1 byte

Battle result, Fort Condor  
00: If you win the battle  
01: If you lose the battle

0x0C51  
z_16\[45\]

2 bytes

Game Progres Temp Var, Fort Condor {convil_4/mihari/s1}  
When the battle ends, the Game Progres Var (0x0BA4) is copied to this Var.  
Is used to check the progresion diff to trigger the new attack event.

0x0C53  
z_16\[47\]

1 bytes

Number of Enemies left alive in the battle field, Fort Condor  
Set by kernel, not referenced by the field script.

0x0C54  
z_16\[48\]

1 byte

Progress, Fort Condor  
00: No battle  
01: Normal Battle  
03: Final Boss Battle

0x0C55  
z_16\[49\]

1 byte

Progress & Battle Reward, Fort Condor  
0x01: Condor Progress {convil_1/jijii/s1}  
0x02: Condor Progress {convil_1/mihari/s1}{convil_2/mihari/s1}{convil_4/ph_mat/s1}  
0x04: Condor Progress {convil_1/event/s19}  
0x08: Condor Progress {convil_2/mihari/s1}  
0x10: "Received "Magic Comb"!" {convil_2/itemget/s1}  
0x20: "Received "Peace Ring"!" {convil_2/itemget/s1}  
0x40: "Received "Megalixir"!" {convil_2/itemget/s1}  
0x80: "Received "Super Ball"!" {convil_2/itemget/s1}

0x0C56  
z_16\[50\]

1 byte

Progress, Fort Condor  
0x01:  
0x02: If you ever entered the {condor1} map  
0x04: If you are inside the Fort  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0C57  
z_16\[51\]

1 byte

Battle modifier linked with 0x0C4D, Fort Condor  
0x01: If 0x0C4D >= 2 is set to 1 {convil_2/event/s7}  
0x02: If 0x0C4D >= 3 is set to 1 {convil_2/event/s7}  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0C58  
z_16\[52\]

2 bytes

Fort Condor Funds

0x0C5A  
z_16\[54\]

1 byte

Number of Fort Condor Battles Lost

0x0C5B  
z_16\[55\]

1 byte

Conversations mask (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Speaking to the children near the wall of Wallmarket(0x01)  
0x02: Speaking to the children near the wall of Wallmarket(0x02)  
0x04: Conversation of children on top of the wall of Wallmarket(0x04)  
0x08: Speaking to the child by the pipe in Wallmarket (0x08)  
0x10:  
0x20:  
0x40:  
0x80:

0x0C5C  
z_16\[56\]

1 byte

Handle the map jumps to MOVE_S(670),MOVE_I,MOVE_F,MOVE_R,MOVE_U,MOVE_D, Great Glacier

0x0C5D  
z_16\[57\]

1 byte

Progress, Great Glacier  
0x01: To know if you came from the snowboard course (0=YES,1=NO), if so display the land event: "...So where did we land?..."{hyou2/event/s1}, "We've jumped pretty far..." {hyou3/event/s5}  
0x02: To know if you came from the Glacier Map Screen, if so restore your position and set this bit to 0 {hyou1/init/s0}

0x0C5E  
z_16\[58\]

2 byte

Store Cloud MAPID, is used to know where to send you after seeing the Glacier Map, Great Glacier {hyoumap/init/s0}

0x0C60  
z_16\[60\]

2 byte

Store Cloud position (X) right before you use the map, Great Glacier

0x0C62  
z_16\[62\]

2 byte

Store Cloud position (Y) right before you use the map, Great Glacier

0x0C64  
z_16\[64\]

2 byte

Store Cloud position (Z) right before you use the map, Great Glacier

0x0C66  
z_16\[66\]

2 byte

Store Cloud position (triangle ID) right before you use the map, Great Glacier

0x0C68  
z_16\[68\]

1 byte

Store Cloud direction right before you use the map, then restore it from it, Great Glacier

0x0C69  
z_16\[69\]

1 byte

Is set to 1 when cloud pass-out, Great Glacier

0x0C6A  
z_16\[70\]

1 byte

Cloud Pass-out Counter, Great Glacier  
First time you jump to HOLU_1(687), then to HOLU_2(688)

0x0C6B  
z_16\[71\]

1 byte

Progress & Field item mask, Great Glacier  
0x01: When you touch the hot spring (used to get Alexander Summon) {hyou10/event/s3}--->{hyou10/cloud/s4,s5}  
0x02: If you ever have spoken to snoww {hyou12/snoww/s1}  
0x04: If you lose the battle against the Snow woman (snoww)  
0x08: If you win the battle against the Snow woman  
0x10: Received "Alexander" Materia{hyou13_2/mt/s1}  
0x20: Received "Added Cut" Materia {MOVE_d/mt/s1}  
0x40: Received "All" Materia {hyou12/mt/s1}  
0x80:

0x0C74  
z_16\[80\]

1 byte

Used to save user anwser in the debugroom {BLACKBG7/leave/s1} before Jump to map blin70_4 (No269)  
00: Set along with GameProgress = 0  
00: Set along with GameProgress = 1566  
00: Set along with GameProgress = 1572

0x0C75  
z_16\[81\]

1 byte

Unknown is set to 0 in Wall Market {MRKT2/mapinit/s0}

0x0C84  
z_16\[96\]

1 byte

Keeps track of which Shinra floors are unlocked (By picking keycards). Values still unknown.(255 all doors opened when set manualy)

0x0C85

1 byte

Mission 1st reactor flags.  
0x01: elevator on top floor.  
0x08: 1st door opened.  
0x10: 2nd door opened.  
0x20: Jessie free from stuck.  
0x40: bomb set.  
0x80: set if time is out for gameover check.

0x0C86

1 byte

Mission 1st reactor flags.  
0x02: elevator door opened.  
0x04: scrolled at map init to show reactor.

0x0C87

29/45 bytes

z_17 Unknown\[0-28\] First 29 bytes of 45 (ENDS AT 0x0CB3 16 Bytes into next bank)

## Save Memory Bank 3/4\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D3&uselang=en 'Sign in to edit')\]

**Table 1: FF7 Save Slot**

Offset

Length

Description

0x0CA4

16/45 Bytes

z_17 Unknown\[29-44\] Last 16 bytes of 45

0x0CAD  
z_17\[9\]

1 byte

1st party member char ID mirror. Is a mirror of 0x04F8 (set from field module).

0x0CAE  
z_17\[10\]

1 byte

2nd party member char ID mirror. Is a mirror of 0x04F9 (set from field module).

0x0CAF  
z_17\[11\]

1 byte

3ed party member char ID mirror. Is a mirror of 0x04FA (set from field module).

0x0CB4

1 byte

Aeris In Church progression (document this better)

0x0CB5

49 Bytes

z_18 Unknown

0x0CE6

1 byte

Escape from 1st reactor progress.  
0x01: after scroll at start of map MD8_2 (maybe unneded).  
0x02: after people panic on MD8_3 is over to never show it again.

0x0CE7

7 Bytes

z_19 Unknown

0x0CEE

2 bytes

Party GP (0-10000)

0x0CF0

12 Bytes

z_20 Unknown

0x0CF0  
z_20\[0\]

1 byte

Chocobo Race - Times you lose (Only on Corel Prision Race){crcin/esto/s0}

0x0CF3  
z_20\[3\]

1 Byte

Battle Square Special Dialog Progression {0x00 init, 0x10 :no text, 0xF0:new special fight}

0x0CF4  
z_20\[4\] & Z_20\[5\]

2 Bytes

Battle Square Battle Points

0x0CFC

1 byte

Number of chocobo stables owned

0x0CFD

1 byte

Number of occupied stables

0x0CFE

1 Byte

Choco Bill dialogs mask 0x01: If you talk him after meteor get summoned (only showed once) {FRMIN/jijii/s1}  
0x02: If he offers you to rent Chocobo Stables (only showed once) {FRMIN/jijii/s1}

0x0CFF

1 byte

Chocobo Stables Occupied Mask. LSB 1 2 3 4 5 6 x x MSB Stable #) Chocobo's in stables. 1=0ccupied

0x0D00

1 byte

Chocobos who can't mate LSB 1 2 3 4 5 6 x x MSB (Stable #).The Chocobo Was Just Born or has Recently Mated.1=can't mate

0x0D01

40 Bytes

z_22 Unknown

0x0D13  
z_22\[18\]

1 byte

Aeris flower quest progress.  
0x01: if we buy flower from Aeris.

0x0D23  
z_22\[34\]

1 byte

Current room in TUNNEL_1. From 1 to 6. If less then 1 then we go to TUNNEL_3. If 6 then to TUNNEL_2. Used instead of duplicating tunnel rooms. Start room set during mission 5 reactor train minigame.

0x0D24  
z_22\[35\]

1 byte

Conversations mask, Kalm (LBS)(applied when you speak to someone).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01:  
0x02:  
0x04:  
0x08: Spoke to the child in the house next to the Inn  
0x10: Freed the dog in a house  
0x20:  
0x40:  
0x80:

0x0D26  
z_22\[37\]

1 byte

Conversations mask, Reactor under the plate (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Speaking with Biggs(0x01)  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0D27  
z_22\[38\]

1 byte

Conversations mask, Reactor under the plate (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Speaking with Jesse(0x01)  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0D29

1 Byte

Yuffie can be found in the forests? (LSB only) others used?

0x0D2A

28 Bytes

z_23 Unknown

0x0D44  
z_23\[26\]

1 byte

Conversations mask, Reactor under the plate (LBS).  
Bit=0(NOT Activated/Received/Spoken to), Bit=1(Activated/Received/Spoken to).  
0x01:  
0x02:  
0x04:  
0x08:  
0x10: Aerith on roof event ends  
0x20:  
0x40: Turbo Ether {MIN51_2}  
0x80: Aerith on roof event starts

0x0D46

1 byte

Don's Mission Progress (more needed here)

0x0D47

31 Bytes

z_24 Unknown

0x0D47  
z_24\[0\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01:  
0x02:  
0x04:  
0x08: Elevator event at shinra HQ(0x08)  
0x10: First conversation while climbing Shinra HQ stairs(0x10)  
0x20:  
0x40:  
0x80:

0x0D49  
z_24\[2\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01:  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80: Second conversation while climbing Shinra HQ stairs(0x80)

0x0D4A  
z_24\[3\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Third conversation while climbing Shinra HQ stairs (0x01)  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0D4C  
z_24\[5\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Braking in Shinra HQ scene (0x01)  
0x02: Taking out the guards and obtaining keycard 60(0x02)  
0x04: Taking everyone out the first floor in Shinra HQ(0x04)  
0x08: Speaking to the couple in the shop at Shinra HQ(0x08)  
0x10: Speaking to the shop seller in Shinra HQ(0x10)  
0x20: Approaching Shinra HQ and conversation at the front door scene(0x20)  
0x40: Approaching Shinra HQ and conversation at the front door scene(0x40)  
0x80:

0x0D50  
z_24\[9\]

1 byte

Items mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Item on floor), Bit=1(Item taken).  
0x01: Phoenix down from locker at floor 64 (0x01)  
0x02: Ether from locker at floor 64(0x02)  
0x04:  
0x08:  
0x10: Exiting elevator FMV at floor 60(0x10)  
0x20:  
0x40:  
0x80:

0x0D52  
z_24\[11\]

2 bytes

Bits kept for the doors at floor 63, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Door opened), Bit=1(Door closed).

0x0D55  
z_24\[14\]

1 byte

Item mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Item on floor), Bit=1(Item taken).  
0x01:  
0x02: Coupon C from Shinra HQ(0x02)  
0x04: Coupon C from Shinra HQ(0x04)  
0x08: Coupon B from Shinra HQ(0x08)  
0x10: Speaking to the machine at floor 63(0x10)  
0x20:  
0x40:  
0x80:

0x0D56  
z_24\[15\]

1 byte

Bits kept for some events on floor 63, Shinra HQ (LBS)(Really needs to be investigated).  
Bit=0(Door opened), Bit=1(Door closed).

0x0D57  
z_24\[16\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Hitting vending machine at floor 64(0x01)  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0D58  
z_24\[17\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01:  
0x02:  
0x04:  
0x08: Placing midgar fifth part(0x08)  
0x10: Placing midgar fourth part(0x10)  
0x20: Placing midgar third part(0x20)  
0x40: Placing midgar second part(0x40)  
0x80: Placing midgar first part(0x80)

0x0D59  
z_24\[18\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01: Midgar model lights up at floor 65  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80: Last conversation with floor 63 machine

0x0D5D  
z_24\[22\]

1 byte

Conversations mask, Shinra HQ (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to).  
0x01:  
0x02:  
0x04:  
0x08:  
0x10:  
0x20: Retrieving coupons (must know the order)(0x20)  
0x40: Retrieving coupons (must know the order)(0x40)  
0x80: Retrieving coupons (must know the order)(0x80)

0x0D66

1 byte

Turtle Paradise Flyers Seen LSB 1 2 3 4 5 6 x x MSB (flyer#) 1=seen 0x01: Sector 7 Slums  
0x02: 1st Floor Shinra Building  
0x04: Gold Saucer - Ghost Hotel  
0x08: Cosmo Canyon - Inn 2nd Floor  
0x10: Cosmo Canyon - Near Shop  
0x20: Wutai In Front of Trap Room  
0x40: Wutai - In Front of Turtle Paradise  
0x80:

0x0D67

12 Bytes

z_25 Unknown

0x0D67  
z_25\[0\]

1 byte

Conversations mask  
0x01: Cait Sith Leaves, and tell you that "The Sister Ray's not this way" {SINBIL_1/KETLINE/s5}  
0x02: Don Corneo's mansion first time you talk to DOORMAN {colne_1/DOORMAN/s1}  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0D68  
z_25\[1\]

1 byte

Northern Cave: Cloud Lv just before Jenova Synthesis battle start.  
Used as lv placeholder for Jenova Synthesis Boost formula.

0x0D69  
z_25\[2\]

1 byte

Northern Cave: Barret Lv just before Jenova Synthesis battle start.

0x0D6A  
z_25\[3\]

1 byte

Northern Cave: Tifa Lv just before Jenova Synthesis battle start.

0x0D6B  
z_25\[4\]

1 byte

Northern Cave: Red XII Lv just before Jenova Synthesis battle start.

0x0D6C  
z_25\[5\]

1 byte

Northern Cave: Yuffie Lv just before Jenova Synthesis battle start.

0x0D6D  
z_25\[6\]

1 byte

Northern Cave: Cait Sith Lv just before Jenova Synthesis battle start.

0x0D6E  
z_25\[7\]

1 byte

Northern Cave: Vincent Lv just before Jenova Synthesis battle start.

0x0D6F  
z_25\[8\]

1 byte

Northern Cave: Cid Lv just before Jenova Synthesis battle start.

0x0D70  
z_25\[9\]

1 byte

Bizarro Sephiroth Fight Number of Groups  
01: 1 Group. First time you enter the map{LASTMAP/directr/s0}  
02: 2 Groups {LASTMAP/AD3/s3}  
03: 3 Groups {LASTMAP/AD3/s3}

0x0D71  
z_25\[10\]

1 byte

Bizarro Sephiroth Fight, some progress value  
00: {LASTMAP/BAT/s4,s5}  
01: {LASTMAP/BAT/s4}  
02: {LASTMAP/BAT/s4}  
03: {LASTMAP/BAT/s5}  
04: {LASTMAP/BAT/s5}  
05: {LASTMAP/BAT/s5}  
06: {LASTMAP/BAT/s5}

0x0D72  
z_25\[11\]

1 byte

Great Glacier Snowboard, taken path (Set the exit location where you land) {hyou1/event/s1}  
0x01: Left both times: Forest HYOU2  
0x02: Right both times: Outside Frostbite cave HYOU3  
0x04: Left right: Main gate HYOU1  
0x08: Right then left: Single tree HYOU7

0x0D73

1 byte

Yuffie Regulary. Has the character entered the party regulary? For example Yuffie further appears in the forest if this option is off.  
0x6E: Yes; 0x6F: No

0x0D74

15 Bytes

z_26 Unknown

0x0D74  
z_26\[0\]

1 byte

MDS7PLR1 event flags.  
0x01: when everyone run to hideout.  
0x02: when talk to man to view pillar to call. This will run special event script when return to this map. Remove this bit after script is called.  
0x04: when Barret return to map and call us again.  
0x08: after return to this map after seeing pillar.  
0x10: after talking to right soldier twice (before mission in 5th reactor).  
0x20:  
0x40:  
0x80:

0x0D75  
z_26\[1\]

1 byte

Conversations mask, MDS7 (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to). The value inside \[\] is the hex value of the entire byte.  
Start sector 7 slums \[0x00\]  
0x01: Right after enter s7 bar MAP\[0xA1\]  
0x02: After 7th heaven initial scene\[0xFF\]or\[0xBF\] if bit 6 is 0  
0x04: Tifa get out the bar\[0xA5\]?  
0x08: Scene ends and barret wait outside bar\[0xAD\]  
0x10: Barret talk before enter the bar\[0xFD\]or\[0xBD\] if bit 6 is 0  
0x20: Right after enter s7 bar MAP\[0xA1\]  
0x40: Girl talk about reactor explotion\[0xED\]  
0x80: Right after enter s7 bar MAP\[0xA1\]

0x0D76  
z_26\[2\]

1 byte

Conversations mask, MDS7 (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to). The value inside \[\] is the hex value of the entire byte.  
Start sector 7 slums \[0x00\]  
0x01: After you wake up in the Hideout\[0x03\]  
0x02: After you wake up in the Hideout\[0x03\]  
0x04: Unknown\[0x00\]?  
0x08: Unknown\[0x00\]  
0x10: Avalache member continue running to s7 train station and Villagers are arround Avalache team \[0x51\]{mds7}  
0x20: Unknown it become 1 seconds after 0x0D76\[4\] is set \[0x51\]{mds7}  
0x40: Unknown\[0x00\]  
0x80: Unknown\[0x00\]

0x0D77  
z_26\[3\]

1 byte

Conversations mask, MDS7 (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to). The value inside \[\] is the hex value of the entire byte.  
Start sector 7 slums \[0x00\]  
0x01: Tell tifa did fight w/ barret (1) didn't fight (0)\[0x05\]or\[0x04\] if not  
0x02: Unknown\[0x00\]  
0x04: Auto tifa talk about fight w/ barret\[0x04\]  
0x08: Unknown\[0x00\]  
0x10: Unknown\[0x00\]  
0x20: Unknown\[0x00\]  
0x40: Unknown\[0x00\]  
0x80: Unknown\[0x00\]

0x0D78  
z_26\[4\]

1 byte

Conversations mask, MDS7 (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to). The value inside \[\] is the hex value of the entire byte.  
Start sector 7 slums \[0x00\]  
0x01: Barret chages in bar (set w/ z_26\[1\] state #2)\[0x03\]  
0x02: Barret chages in bar (set w/ z_26\[1\] state #2)\[0x03\]  
0x04: After we have talked to tifa\[0x07\]  
0x08: Set to 1 if we choose no drink when talking to tifa\[0x0F\]  
0x10: Set to 1 if we choose strong drink talking ot tifa\[0x17\]  
0x20: Unknown\[0x00\]  
0x40: Unknown\[0x00\]  
0x80: Unknown\[0x00\]

0x0D79  
z_26\[5\]

1 byte

Conversations mask, MDS7 (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to). The value inside \[\] is the hex value of the entire byte.  
Start sector 7 slums \[0x00\]  
0x01: set to 1 when tifa calls the machine down after you 1st talk down stairs, never gets unset\[0x03\]  
0x02: 1 if elevator is in hide out (pinball machine)\[0x02\]  
0x04: After you wake up in the Hideout\[0x1F\]  
0x08: After you wake up in the Hideout\[0x1F\]  
0x10: After you wake up in the Hideout\[0x1F\]  
0x20: Unknown\[0x00\]  
0x40: After giving Barret the materia tutorial\[0x5D\]  
0x80: Unknown\[0x00\]

0x0D7A  
z_26\[6\]

1 byte

Conversations mask, MDS7 (LBS)(applied when you speak).  
Bit=0(Not spoken to), Bit=1(Spoken to). The value inside \[\] is the hex value of the entire byte.  
Start sector 7 slums \[0x00\]  
0x01: After hide out 1st talk\[0x03\]  
0x02: After hide out 1st talk\[0x03\]  
0x04: second part of talk tifa enter in scene\[0x07\]  
0x08: After you wake up in the Hideout\[0x6F\]  
0x10: Unknown\[0x00\]  
0x20: After you wake up in the Hideout\[0x6F\]  
0x40: After you wake up in the Hideout\[0x6F\]  
0x80: After you get out the Hideout and talk to tifa \[0xEF\]

0x0D7B  
z_26\[7\]

1 byte

Items mask, Training room at sector 5 (LBS)(applied when you speak).  
Bit=0(Item on floor), Bit=1(Item taken).  
0x01:  
0x02:  
0x04:  
0x08:  
0x10: All materia after taking ether(0x10)  
0x20: Ether chest that falls from ceiling(0x20)  
0x40:  
0x80:

0x0D7C  
z_26\[8\]

1 byte

MDS7ST3 event flags.  
0x01: when everyone start run to hideout.  
0x02: when trainman tells you about war (3 talk).  
0x04: when pair on station agreed with each other.  
0x08: when Jessie, Biggs and Wedge run into train.  
0x10:  
0x20:  
0x40:  
0x80:

0x0D83

1 byte

Midgard train flags.  
0x01: when we talk to Biggs on way to sector 7.  
0x02: when we talk to Wedge twice on way to sector 7.  
0x04: when talk to Jessie, before look at map.  
0x10: this bit is checked on ROOTMAP, though it doesn't use ingame.

0x0D84

32/64 Bytes

z_27 Unknown\[0-31\] First 32 bytes of 64 (ENDS AT 0x0DC3 32 Bytes into next bank)

0x0D90  
z_27\[12\]

1 byte

Event flags inside Junon.  
0x01:  
0x02:  
0x04: Junon Soldiers running through the city after the parade.  
0x08:  
0x10:  
0x20: Enemy Skill materia  
0x40:  
0x80:

## Save Memory Bank B/C\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D4&uselang=en 'Sign in to edit')\]

**Table 1: FF7 Save Slot**

Offset

Length

Description

0x0DA4

32/64 Bytes

z_27 Unknown\[32-63\] Last 32 bytes of 64

0x0DA4  
z_27\[32\]

6 bytes

Chocobo Race - Chocobo Name ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0DAA  
z_27\[38\]

1 bytes

Chocobo Race(G1) - Jockey  
00: Cloud  
01: Tifa  
02: Cid

0x0DAB  
z_27\[39\]

1 bytes

Chocobo Race(G1) - Course  
00: Long course  
01: Short course

0x0DAC  
z_27\[40\]

1 bytes

Chocobo Race(G1) - Bet Selection Screen  
00: Enabled {crcin_1/esto}  
01: Disabled {crcin_2/esto}

0x0DAD  
z_27\[41\]

1 bytes

Chocobo Race(G1) - ???  
00: All others times but  
01: When you race by talking to ester in {crcin_1/esto}

0x0DAE  
z_27\[42\]

2 bytes

Chocobo Race(G2) - Sprint Speed  
Value = 4500 {crcin_2}

0x0DB0  
z_27\[44\]

2 bytes

Chocobo Race(G2) - Speed  
Value = 3500 {crcin_2}

0x0DB2  
z_27\[46\]

1 byte

Chocobo Race(G2) - Acceleration  
Value = 70 {crcin_2}

0x0DB3  
z_27\[47\]

1 byte

Chocobo Race(G2) - Cooperation  
Value = 100 {crcin_2}

0x0DB4  
z_27\[48\]

1 byte

Chocobo Race(G2) - Intelligence  
Value = 100 {crcin_2}

0x0DB5  
z_27\[49\]

1 byte

Chocobo Race(G2) - Type (Yellow, Green, Blue, Black, Gold)  
Value = 0 {crcin_2}

0x0DB6  
z_27\[50\]

1 byte

Chocobo Race(G2) - Personality  
Value = 0 {crcin_2}

0x0DB7  
z_27\[51\]

1 byte

Chocobo Race(G2) - ???  
05: When you race by talking to ester in {crcin_2/esto}  
07: All others times {crcin_1/esto}

0x0DB8  
z_27\[52\]

1 byte

Chocobo Race(G2) - ???  
Value = 1 (ALWAYS) {crcin_1/crcin_2}

0x0DB9  
z_27\[53\]

1 byte

Chocobo Race(G2) - ???  
Value = 0 (ALWAYS) {crcin_1/crcin_2}

0x0DBA  
z_27\[54\]

1 byte

Chocobo Race(G2) - Joe/TEIOH Chalenge  
00: No  
01: Yes

0x0DBB  
z_27\[55\]

1 byte

Chocobo Race(G2) - Selected Rank  
00: Class C  
01: Class B  
02: Class A  
03: Class S

0x0DBC  
z_27\[56\]

1 byte

Chocobo Race - ???  
Random 0/15{crcin_1/esto}  
0: All others times

0x0DBD  
z_27\[57\]

1 byte

Chocobo Race - Finish Place (0 to 5)  
Set to 0xFF on the elevator {GLDELEV/dic/s0}  
Used only when you must race to get out the desert prision. After winning the race and before exit the map is set to 0xFF and never change again. {crcin/esto/s0}

0x0DBE  
z_27\[58\]

2 bytes

Chocobo Race(G2) - Stamina  
Value = 6000 {crcin_2}

0x0DC0  
z_27\[60\]

1 bytes

Chocobo Race(G1) - Winning Prize  
00 = 500GP | "Received "Sprint Shoes"  
01 = 300GP | "Received "Counter Attack" Materia!!"  
02 = 500GP | "Received "Magic Counter"  
03 = 300GP | "Received "Precious Watch"!!"  
04 = 500GP | "Received "Cat's Bell"!!"  
05 = 300GP | "Enemy Away" Materia!!"  
06 = 300GP | "Received "Sneak Attack" Materia!!"  
07 = 400GP | "Received "Chocobracelet"!!"  
08 = 30GP | "Received "Ether"!!"  
09 = 200GP | "Received "Elixir"!!"  
10 = 15GP | "Received "Hero Drink"!!"  
11 = 20GP | "Received "Bolt Plume"!!"  
12 = 20GP | "Received "Fire Fang"!!"  
13 = 20GP | "Received "Antarctic Wind"!!"  
14 = 50GP | "Received "Swift Bolt"!!"  
15 = 50GP | "Received "Fire Veil"!!"  
16 = 50GP | "Received "Ice Crystal"!!"  
17 = 300GP | "Received "Megalixir"!!"  
18 = 150GP | "Received "Turbo Ether"!!"  
19 = 5GP | "Received "Potion"!!"  
20 = 10GP | "Received "Phoenix Down"!!"  
21 = 10GP | "Received "Hyper"!!"  
22 = 10GP | "Received "Tranquilizer"!!"  
23 = 15GP | "Received "Hi-Potion"!!"  
255 = If you lost the race (Nothing)

0x0DC4

16 bytes

Chocobo slot 1 \[See Below for [Chocobo Slot format](https://qhimm-modding.fandom.com/wiki/FF7/Savemap#Chocobo_Record)\]

0x0DD4

16 bytes

Chocobo slot 2

0x0DE4

16 bytes

Chocobo slot 3

0x0DF4

16 bytes

Chocobo slot 4 \[Slot 5 and 6 are located at 0x1084 - 0x10A3\]

0x0E04

13 Bytes

z_28 Unknown

0x0E0C  
z_28\[8\]

1 byte

Change on Final Battle

0x01:  
0x02:  
0x04:  
0x08: Final Battle  
0x10:  
0x20:  
0x40:  
0x80:

0x0E0E  
z_28\[10\]

1 byte

Yuffie Stolen Materia Quest - Disabled party members {YUFY1/YUFI}  
(Bit mask is set just before stolen materia been restored, to know what chars must be reactivated.)  
0x01: Unused  
0x02: Barret  
0x04: Tifa  
0x08: Red XIII  
0x10: Cait Sith  
0x20: Cid  
0x40: Vincent  
0x80: Aeris

0x0E0F  
z_28\[11\]

2 bytes

G-Bike Minigame Last Score {GAMES_2/dic}

0x0E11

2 Bytes

G-Bike Minigame High Score

0x0E13

1 Byte

UnSaved Snowboard Mini Game Temp Var.

0x0E14

4 Bytes

Fastest Time For Snowboard Beginner Course. Format: MMSSTTT0 90 27 36 02 in the file is a time of 2'36"279 (value is 32bit int so will become 02362790 when read )

0x0E18

4 Bytes

Fastest Time For Snowboard Expert Course. See Beginner Course for more info

0x0E1C

4 Bytes

Fastest Time For Snowboard Crazy Course. See Beginner Course for more info

0x0E20

1 Byte

HighScore For Snowboard Beginner Course

0x0E21

1 Byte

HighScore For Snowboard Expert Course

0x0E22

1 Byte

HighScore For Snowboard Crazy Course

0x0E23

1 Byte

UnSaved Snowboard Mini Game Temp Var

0x0E24

2 bytes

2nd rank at RollerCoaster Shooter

0x0E26

2 bytes

3rd rank at RollerCoaster Shooter

0x0E28

17 Bytes

z_29 Unknown

0x0E28  
z_29\[0\]

1 bytes

Mythril Side Quest/Chocobo Sage Side Quest  
0x01: Talked to the Weapon Seller about the Keystone, Temple of the Ancients, DIO, etc {zz2/m/s4}  
0x02: Chocobo Sage when he finish all remembering stuff {zz3/dic/s0}  
0x04: Unused  
0x08: Old man: "Large Materia needs high level Materia." {zz1/m1/s1}  
0x10: Mythril given to the Weapon Seller {zz2/m/s1}  
0x20: Chocobo Sage if you ask him "What about that Chocobo?" {zz3/m1/s1}  
0x40: Chocobo Sage every time he remember something new about Chocobos is set to 1, and when you tell that back to Chole reset to 0. {zz3/m1/s1}{FRCYO/kodomo/s1}  
0x80: First time you talk to Chole after meeting Chocobo Sage {FRCYO/kodomo/s1}

0x0E29  
z_29\[1\]

1 byte

Chocobo Sage Side Quest - Progression Variable 01: First time you talk to Chocobo Sage  
02,03,04: About Blue/Green Chocobo  
05: About Black Chocobo  
06,07,08: About Gold Chocobo  
09,10: About Zeio Nuts

0x0E2A  
z_29\[2\]

2 bytes

Number of battles to reach in order to unlock the next part of the Chocobo breeding tutorial

0x0E2C  
z_29\[4\]

1 bytes

Chocobo Sage Side Quest - Part of the random number of battles formula

0x0E2D  
z_29\[5\]

1 bytes

Unused?

0x0E2E  
z_29\[6\]

1 bytes

Chocobo Race / Others  
0x01: Set to 1 the first time you talk to Ester to race and Ride your own Chocobo {crcin_1/esto/s1}  
0x02: Set to 1 just before Chocobo Race Engine be launched {crcin_1/esto/s1}  
Set to 0 when you receive the price or lose. {crcin_1/dic/s0}  
0x04: Set to 1 just before your first time race (Ester say "Yeahh but jockeys can't buy tickets.")  
Then after been activated the next races (she say: "Good Luck! Take care!") {crcin_1/esto/s1}  
0x08: After beating Mog's House and receive 30GP from the guy {GAMES_2/kabe/s1}  
0x10: If you win 9 races to enter Rank S {crcin_1/esto/s1}  
0x20: If you win 19 races with the same chocobo to receive Sprint Shoes, Cat's Bell, Precious Watch, Chocobracelet, and Counter Attack Materia. {crcin_1/esto/s1}  
0x40:  
0x80:

0x0E2F  
z_29\[7\]

1 bytes

Chocobo Race - Selected Chocobo Stable Position (0 to 5)

0x0E30  
z_29\[8\]

1 bytes

Unused?

0x0E2E  
z_29\[6\]

1 bytes

Northern Cave  
0x01: Bottom of Northern Cave talk {las4_0/dic/s0}  
0x02: Set to 1 when you enter the map "las3_3" comming from map "las4_1" {las3_3/dic/s0}

0x0E2F  
z_29\[7\]

1 bytes

Northern Cave  
0x01: Bottom of Northern Cave talk {las4_0/dic/s0}  
0x02: Set to 1 when you enter the map "las3_3" comming from map "las4_1" {las3_3/dic/s0}

0x0E30  
z_29\[8\]

1 bytes

Northern Cave - Received items from party in the last talk  
0x01: Barret {las4_0/ballet/s1}  
0x02: Tifa {las4_0/tifa/s1}  
0x04: RedXIII {las4_0/red/s1}  
0x08: Cid {las4_0/cid/s1}  
0x10: Cait Sith {las4_0/cait/s1}  
0x20: Yuffi {las4_0/yufi/s1}  
0x40: Vincent {las4_0/vincent/s1}  
0x80:

0x0E33  
z_29\[11\]

1 byte

Lucrecia's Cave sidequest Progression Variable

0x0E35  
z_29\[13\]

2 bytes

Lucrecia's Cave sidequest:  
Number of battles to get past in order to unlock Chaos & Death Penalty

0x0E39

2 bytes

1st rank at RollerCoaster Shooter

0x0E3C

105 Bytes

z_30 Unknown

## Save Memory Bank D/E\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D5&uselang=en 'Sign in to edit')\]

**Table 1: FF7 Save Slot**

Offset

Length

Description

0x0EA4

1 byte

Which game-play Disc is needed

0x0EA5

1 byte

z_31 Tifa's House 0x01: Final Heaven {niv_ti2/piano/s1}  
0x02: Cloud played the piano in the flashback {niv_ti2/molody/s2}  
0x04: Elemental Materia {niv_ti2/piano/s1}

0x0EA6

1 Byte

Start Of Bombing Mission (0x14=Yes, 0x56=No)  
Northern Cave - Progress (TODO: more info) 0x94

0x0EA7

3 bytes

z_32 Unknown

0x0EA7  
z_32\[0\]

1 bytes

Northern Cave - Progress (TODO: more info)

0x0EAA

2 Bytes

Step counter. Used in great glacier to count the steps until passing out and resetted whenever you enter it. Value to pass out = 544

0x0EAC

22 bytes

z_33 Unknown

0x0EC2

1 byte

Field pointers mask (hand over party leader's head + red and green arrows)  
0x00: Inactive  
0x02: Active

0x0EC3

1 byte

z_34 Unknown. If you have max materias in your equipment it is set to non-zero (needs to be confirmed) FALSE! (By Ss4).

0x0EC4

6 bytes

Name of Chocobo 1 ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0ECA

6 bytes

Name of Chocobo 2 ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0ED0

6 bytes

Name of Chocobo 3 ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0ED6

6 bytes

Name of Chocobo 4 ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0EDC

6 bytes

Name of Chocobo 5 ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0EE2

6 bytes

Name of Chocobo 6 ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0EE8

2 bytes

Stamina of Chocobo 1

0x0EEA

2 bytes

Stamina of Chocobo 2

0x0EEC

2 bytes

Stamina of Chocobo 3

0x0EEE

2 bytes

Stamina of Chocobo 4

0x0EF0

2 bytes

Stamina of Chocobo 5

0x0EF2

2 bytes

Stamina of Chocobo 6

0x0EF4

1 byte

Vincent Regularly/Change Submarine Color. (Bit-mask)  
0x01:  
0x02:  
0x04: Vincent Regulary. Has the character entered the party regularly? Byte value (Yes:\[0xFF\]; No:\[0xFB\])(NEEDS TO BE CHECKED)  
0x08: Gray Submarine (bit = 1)/ Red Submarine (bit = 0) (Liked with 0x0EF6\[2\])  
0x10:  
0x20:  
0x40:  
0x80:

0x0EF5

23 bytes

z_35 Unknown

0x0EF6  
z_35\[1\]

1 byte

Vehicle Submarine  
0x01:  
0x02:  
0x04: Grey Submarine Ignored / Red Submarine bit = 1 (Linked with 0x0EF4\[3\])  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0EFD  
z_35\[8\]

1 byte

Northern Cave - Yuffie Split up path

0x0EFF  
z_35\[10\]

1 byte

Save flag.  
0x02: set when we in save (menu or point? please check) and unset when out  
Other byte values: 0x10, 0x12, 0x51

0x0F04  
z_35\[22\]

1 byte

Northern Cave - Progress (TODO: more info)

0x0F05  
z_35\[23\]

1 byte

Northern Cave - Progress (TODO: more info)

0x0F0C

24 bytes

Name of location ([FF Text format](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text'))

0x0F24

5 bytes

z_36 Unknown

0x0F29

1 bytes

Save on the world map - Tutorial seen (To be Checked)  
0x3B: Seen  
0x33: Not Seen

0x0F2A

50 bytes

z_37 Unknown

0x0F2A  
z_37\[0\]

1 byte

Needs more research. 0x01:  
0x02:  
0x04: Red Submarine Tutorial  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0F2B  
z_37\[1\]

1 bytes

0x20: World map Ruby Weapon form. bit=0: Small Form (before first encounter). bit=1: Big Form (after first encounter).

0x0F3A  
z_37\[16\]

1 bytes

Rand number between 0,1,2. Is set when you change field map. ex: enter a town.

0x0F5C

3 bytes

Party leader's coordinates on world map:  
Party leader X position on the world map (X coord). Value from 0 up to 295000  
000000: 0x000000  
065535: 0xFFFF00 | 065536: 0x000001  
131071: 0xFFFF01 | 131072: 0x000002  
196607: 0xFFFF02 | 196608: 0x000003  
262143: 0xFFFF03 | 262144: 0x000004  
295000: 0x588004

0x0F5F

1 bytes

Party leader viewing direction angle on the world map. Value from 0 up to 255 to cover 0 - 359Â°

0x0F60

3 bytes

Party leader Y position on the world map (Y coord). Value from 1 up to 230000  
000001: 0x01003C  
065535: 0xFFFF3C | 065536: 0x00003D  
131071: 0xFFFF3D | 131072: 0x00003E  
196607: 0xFFFF3E | 196608: 0x00003F  
230000: 0x70823F

0x0F63

1 bytes

Party leader Z altitude on the world map (Z coord). Input value from -128 up to 127 are allowed (0 = Mean Sea Level)

0x0F64

8 bytes

Caught Wild Chocobo's coordinates on world map

0x0F6C

8 bytes

Tiny Bronco/Chocobo's coordinates on world map

0x0F74

8 bytes

Buggy/Highwind's coordinates on world map

0x0F7C

8 bytes

Submarine/???'s coordinates on world map

0x0F84

8 bytes

Diamond=>Ultimate=>Ruby Weapon's coordinates on world map (ruby is bound To the desert)

0x0F8C

2 bytes

1st Snow Pole X Coordinate.

0x0F8E

2 bytes

1st Snow Pole Y Coordinate.

0x0F90

2 bytes

2nd Snow Pole X Coordinate.

0x0F92

2 bytes

2nd Snow Pole Y Coordinate.

0x0F94

2 bytes

3ed Snow Pole X Coordinate.

0x0F96

2 bytes

3ed Snow Pole Y Coordinate.

0x0F98

12/236 bytes

z_38 Unknown\[0-11\] First 12 bytes of 236 (ENDS AT 0x1083 224 Bytes into next bank)

0x0F9C  
z_38\[4\]

1 bytes

Angle of the world. The viewing direction of the camera onto the world map. For top-view (ca. 45Â°) this value should be 0.

0x0F9D  
z_38\[5\]

1 bytes

Top-view (ca. 45Â°). Determines the camera's position.

0x0F9C  
z_38\[4\]

2 bytes

Camera angle and rotation of normal world map.  
00 00 - FF 0F: Map rotation angle. xx yx: if y > 0, y will be changed to 0. (Source: Asa. Data Collision)

0x0F9F  
z_38\[6\]

2 bytes

Snow Pole Number/Where address will be overwritten by next pole (cycling 00, 01, 02, 00, 01, 02... )  
00: 1st pole address  
01: 2nd pole address  
02: 3rd pole address

0x0FA0  
z_38\[8\]

1 bytes

Wild Chocobo Type.  
Value is set when Chocobo is caught and used after Chocobo is sent to cage.  
Index is the byte's value and not the bit-mask.  
0x00: Chocobo not displayed in cage  
0x01: Wonderful  
0x02: Great  
0x03: Good  
0x04: Fair  
0x05: Average  
0x06: Poor  
0x07: Bad  
0x08: Terrible  
Over 08 = Choco Billy's rating window not displayed

0x0FA1  
z_38\[9\]

1 bytes

Riding Byte.  
Index is the byte's value and not the bit-mask.  
0x00: On foot.  
0x03: Highwind  
0x04: Wild Chocobo (Liked with 0x0C22\[0\])  
0x0D: Submarine  
0x13: Chocobo (Liked with 0x0C22\[1/7\]. 0x0C22: 0x04=Yellow, ..., 0x40=Gold)

0x0FA3  
z_38\[11\]

1 bytes

Unknown. It seems this value is mixture of Number of Snow Poles, Party direction and walking steps or coordinates. Value will be ignored when loading slot.

## Save Memory Bank 7/F\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D6&uselang=en 'Sign in to edit')\]

**Table 1: FF7 Save Slot**

Offset

Length

Description

0x0FA4

224/236 Bytes

Unknown z_38\[12-235\] Last 224 bytes of 236

0x0FA6  
z_38\[14\]

1 byte

World map camera & map display  
Add two values (one from camera, one from map) and set this byte.  
Camera: Aerial(00); Closeup(20)  
Map: Off(80); Small(00); Large(40)

0x0FAB  
z_38\[19\]

1 byte

If not 0x00, game crashes

0x0FC4  
z_38\[44\]

2 bytes

Fields items mask.  
0x0001: first potion on MD1STIN.  
0x0002: second potion on MD1STIN.  
0x0004: potion at NMKIN3.  
0x0008: phoenix down on NKMIN1.

0x0FC6  
z_38\[46\]

1 byte

Items mask, Chocobo Farm (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Destruct Materia Animation displayed {sininb42/mtr/s3}  
0x02: Destruct Materia {sininb42/mtr/s1}  
0x04: Enemy Skill {blin68_2/mtr/s1} (See 0x0BEF\[1\])  
0x08: Enemy Skill Animation (Drop after battle) {blin68_2/mtr/s3}  
0x10: Odin Materia {sinin2_1/mtr/s1}  
0x20: Odin Materia Animation displayed {sinin2_1/mtr/s3}  
0x40: Counter Materia {nvdun1/mtr/s1}  
0x80: Magic Plus Materia {sandun_1/mtr/s1}

0x0FF1  
z_38\[89\]

1 byte

On Buggy vehicle. Specifies if a character is on a Buggy. Only if a Buggy is present.  
0x0E: On; 0x0C: Off

0x0FF4  
z_38\[92\]

1 byte

Items mask, Mythril Mine (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: 4sbwy_6 - Tent  
0x02: 4sbwy_3 - Potion  
0x04: 4sbwy_1 - Ether  
0x08: psdun_3 - Ether  
0x10: psdun_4 - Hi-Potion  
0x20: psdun_4 - Elixir  
0x40: psdun_3 - Long Range materia  
0x80: gnmk - Titan Materia

0x0FF5  
z_38\[93\]

1 byte

Items mask, (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: elmin2_2 - Ether  
0x02: losin1 - Comet Materia  
0x04: gonjun1 - Deathblow Materia  
0x08: q_4 - Hades Materia  
0x10: q_4 - Outsider  
0x20: q_3 - Escourt Guard  
0x40: q_3 - Conformer  
0x80: q_4 - Spirit Lance

0x0FF6  
z_38\[94\]

1 byte

Items mask, (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: q_1 - Heaven's Cloud  
0x02: q_3 - Megalixir  
0x04: q_4 - Megalixir  
0x08: losinn - Elixir  
0x10: losin2 - Guard Source  
0x20: losin3 - Magic Source  
0x40: las1_2 las4_0 - Elixir  
0x80: las1_2 las4_0 - Mystle

0x0FF9  
z_38\[97\]

1 byte

Items mask, Kalm (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Hidden Ether in the second floor of a house  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0FFB  
z_38\[99\]

1 byte

Kalm Traveler rewards visibility (each bit set back to 0 when picked up)  
Guide Book (0x01); Master Command(0x02); Master Magic (0x04); Master Summon (0x08); Gold Chocobo (0x10)

0x0FFC  
z_38\[100\]

1 byte

Items mask, Kalm (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Peacemaker in a house  
0x02:  
0x04:  
0x08:  
0x10:  
0x20:  
0x40:  
0x80:

0x0FFD  
z_38\[101\]

1 byte

Items mask, Kalm (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01:  
0x02: Hidden Ether from house next to the Inn  
0x04:  
0x08: Guard Source  
0x10: Hidden Ether  
0x20:  
0x40:  
0x80:

0x0FFE  
z_38\[102\]

1 byte

Items mask, Mythril Mine (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01:  
0x02:  
0x04:  
0x08:  
0x10: Mind Source  
0x20: Tent  
0x40:  
0x80:

0x1004  
z_38\[\]

1 byte

1st party member char ID in Group 1. Final Boss Battle: Bizarro Sephiroth.

0x1005  
z_38\[\]

1 byte

2nd party member char ID in Group 1. Final Boss Battle: Bizarro Sephiroth.

0x1006  
z_38\[\]

1 byte

3ed party member char ID in Group 1. Final Boss Battle: Bizarro Sephiroth.

0x1007  
z_38\[\]

1 byte

1st party member char ID in Group 2. Final Boss Battle: Bizarro Sephiroth.

0x1008  
z_38\[\]

1 byte

2nd party member char ID in Group 2. Final Boss Battle: Bizarro Sephiroth.

0x1009  
z_38\[\]

1 byte

3ed party member char ID in Group 2. Final Boss Battle: Bizarro Sephiroth.

0x100A  
z_38\[\]

1 byte

1st party member char ID in Group 3. Final Boss Battle: Bizarro Sephiroth.

0x100B  
z_38\[\]

1 byte

2nd party member char ID in Group 3. Final Boss Battle: Bizarro Sephiroth.

0x100C  
z_38\[\]

1 byte

3ed party member char ID in Group 3. Final Boss Battle: Bizarro Sephiroth.

0x101E  
z_38\[134\]

1 byte

Items mask, Junon (LBS)(applied when you take the item).  
Bit=0(Item in field), Bit=1(Item taken).  
0x01: Mind Source  
0x02: Power Source  
0x04: Guard Source  
0x08:  
0x10: 1/35 Soldier  
0x20: Luck Source  
0x40:  
0x80:

0x1030  
z_38\[152\]

1 byte

Field screen rain switch (non-zero to turn on rain effect)

0x1084

16 bytes

Chocobo slot 5

0x1094

16 bytes

Chocobo slot 6

## Character Record\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D7&uselang=en 'Sign in to edit')\]

**Table 2: Character Record**

Offset

Length

Description

0x00

1 byte

Character ID - Ignored If Not Cait / Vincent???

0x01

1 byte

Level (1-99)

0x02

1 byte

Strength (0-255)

0x03

1 byte

Vitality (0-255)

0x04

1 byte

Magic (0-255)

0x05

1 byte

Spirit (0-255)

0x06

1 byte

Dexterity (0-255)

0x07

1 byte

Luck (0-255)

0x08

1 byte

Strength Bonus (Power Sources used)

0x09

1 byte

Vitality Bonus (Guard Sources used)

0x0A

1 byte

Magic Bonus (Magic Sources used)

0x0B

1 byte

Spirit Bonus (Mind Sources used)

0x0C

1 byte

Dexterity Bonus (Speed Sources used)

0x0D

1 byte

Luck Bonus (Luck Sources used)

0x0E

1 byte

Current limit level (1-4)

0x0F

1 byte

Current limit bar (0xFF = limit break)

0x10

12 bytes

Name ([FF Text](https://qhimm-modding.fandom.com/wiki/FF7/FF_Text 'FF7/FF Text') format) Game's Naming Boxes Cap you At 9 Chars

0x1C

1 byte

Equipped weapon

0x1D

1 byte

Equipped armor

0x1E

1 byte

Equipped accessory

0x1F

1 byte

Character flags - 0x10-Sadness, 0x20-Fury

0x20

1 byte

Char order - 0xFF-Normal, 0xFE-Back row

0x21

1 byte

Level progress bar (0-63) Games Gui Hides Values <4, 4-63 are visible as "progress"

0x22

2 bytes

Learned limit skills  
0x0001: Limit Lv. 1-1  
0x0002: Limit Lv. 1-2  
0x0004: Always 0 (reserved bit or spacer/breaker/end of limit)  
0x0008: Limit Lv. 2-1  
0x0010: Limit Lv. 2-2  
0x0020: Always 0 (reserved bit or spacer/breaker/end of limit)  
0x0040: Limit Lv. 3-1  
0x0080: Limit Lv. 3-2  
0x0100: Always 0 (reserved bit or spacer/breaker/end of limit)  
0x0200: Limit Lv. 4

0x24

2 bytes

Number of kills

0x26

2 bytes

Times limit 1-1 has been used

0x28

2 bytes

Times limit 2-1 has been used

0x2A

2 bytes

Times limit 3-1 has been used

0x2C

2 bytes

Current HP

0x2E

2 bytes

Base HP (before materia alterations)

0x30

2 bytes

Current MP

0x32

2 bytes

Base MP (before materia alterations)

0x34

4 bytes

Unknown

0x38

2 bytes

Maximum HP (after materia alterations)

0x3A

2 bytes

Maximum MP (after materia alterations)

0x3C

4 bytes

Current EXP

0x40

4 bytes

Weapon materia slot number 1

0x44

4 bytes

Weapon materia slot number 2

0x48

4 bytes

Weapon materia slot number 3

0x4C

4 bytes

Weapon materia slot number 4

0x50

4 bytes

Weapon materia slot number 5

0x54

4 bytes

Weapon materia slot number 6

0x58

4 bytes

Weapon materia slot number 7

0x5C

4 bytes

Weapon materia slot number 8

0x60

4 bytes

Armor materia slot number 1

0x64

4 bytes

Armor materia slot number 2

0x68

4 bytes

Armor materia slot number 3

0x6C

4 bytes

Armor materia slot number 4

0x70

4 bytes

Armor materia slot number 5

0x74

4 bytes

Armor materia slot number 6

0x78

4 bytes

Armor materia slot number 7

0x7C

4 bytes

Armor materia slot number 8

0x80

4 bytes

EXP to next level

## Chocobo Record\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D8&uselang=en 'Sign in to edit')\]

**Table 3: Chocobo Record**

Offset

Length

Description

0x0

2 bytes

Sprint Speed

0x2

2 bytes

Max Sprint Speed

0x4

2 bytes

Speed

0x6

2 bytes

Max Speed

0x8

1 byte

Acceleration

0x9

1 byte

Cooperation

0xA

1 byte

Intelligence

0xB

1 byte

Personality

0xC

1 byte

Pcount (?)

0xD

1 byte

Number of races won

0xE

1 byte

1: female)

0xF

1 byte

Type (Yellow, Green, Blue, Black, Gold)

## Save Item List\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D9&uselang=en 'Sign in to edit')\]

Each item in the item list is stored as a word value with the quantity, expressed as a 7-bit value, concatenated with the item's index, expressed as a 9-bit value between the range of 0-320. In Binary: QQQQQQQXXXXXXXXX Where X is the index and Q is the quantity. There are a total of 320 item slots in the save map and a total of 320 objects that are stored there, some of which are dummy items. The objects are indexed like this:  
Indexes 0 - 127: Items  
Indexes 128 - 255: Weapons  
Indexes 256 - 287: Armors  
Indexes 288 - 319: Accessories  
Quantity is limited (by the menu mechanics) to 99 since there are only two characters available in the item menu to show quantity. A Graphical "glitch" occurs in the ten's digit when quantity exceeds that number. The menu only checks the current quantity to determine if the value can increase and the quantity will not decrease unless an item is used or sold. Forcing the quantity to exceed 99 does not have any side effect with most versions of the game. The Japanese PSX version(BISLPS-00700) is the only version with a problem when you exceed a quantity of 99 for an item. This version will experience an error during battles when you have more then 99 of an item.

## Save Materia List\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D10&uselang=en 'Sign in to edit')\]

Materia is stored as a single-byte ID followed by the amount of AP on that instance of Materia stored as an unsigned 24-bit integer.eskill materia does not use the ap value, but instead the 24 bits as switches for each skill that can be learned. For every materia ap =0xFFFFFF when mastered

**Table 1: Materia List (PC)**

ID

Name

Type

0x00

MP Plus

Independent

0x01

HP Plus

Independent

0x02

Speed Plus

Independent

0x03

Magic Plus

Independent

0x04

Luck Plus

Independent

0x05

EXP Plus

Independent

0x06

Gil Plus

Independent

0x07

Enemy Away

Independent

0x08

Enemy Lure

Independent

0x09

Chocobo Lure

Independent

0x0B

Long Range

Independent

0x0C

Mega All

Independent

0x0D

Counter Attack

Independent

0x0E

Slash-All

Command

0x0F

Double Cut

Command

0x0A

Pre-emptive

Independent

0x10

Cover

Independent

0x11

Underwater

Independent

0x12

HP <-> MP

Independent

0x13

W-Magic

Command

0x14

W-Summon

Command

0x15

W-Item

Command

0x16

Unknown

Placeholder?

0x17

All

Support

0x18

Counter

Support

0x19

Magic Counter

Support

0x1A

MP Turbo

Support

0x1B

MP Absorb

Support

0x1C

HP Absorb

Support

0x1D

Elemental

Support

0x1E

Added Effect

Support

0x1F

Sneak Attack

Support

0x20

Final Attack

Support

0x21

Added Cut

Support

0x22

Steal As Well

Support

0x23

Quadra Magic

Support

0x24

Steal

Command

0x25

Sense

Command

0x26

Unknown

Placeholder?

0x27

Throw

Command

0x28

Morph

Command

0x29

Deathblow

Command

0x2A

Manipulate

Command

0x2B

Mime

Command

0x2C

Enemy Skill

Command

0x2D

Unknown

Placeholder?

0x2E

Unknown

Placeholder?

0x2F

Unknown

Placeholder?

0x30

Master Command

Command

0x31

Fire

Magic

0x32

Ice

Magic

0x33

Earth

Magic

0x34

Lightning

Magic

0x35

Restore

Magic

0x36

Heal

Magic

0x37

Revive

Magic

0x38

Seal

Magic

0x39

Mystify

Magic

0x3A

Transform

Magic

0x3B

Exit

Magic

0x3C

Poison

Magic

0x3D

Demi

Magic

0x3E

Barrier

Magic

0x3F

Unknown

Placeholder?

0x40

Comet

Magic

0x41

Time

Magic

0x42

Unknown

Placeholder?

0x43

Unknown

Placeholder?

0x44

Destruct

Magic

0x45

Contain

Magic

0x46

FullCure

Magic

0x47

Shield

Magic

0x48

Ultima

Magic

0x49

Master Magic

Magic

0x4A

Choco/Mog

Summon

0x4B

Shiva

Summon

0x4C

Ifrit

Summon

0x4D

Ramuh

Summon

0x4E

Titan

Summon

0x4F

Odin

Summon

0x50

Leviathan

Summon

0x51

Bahamut

Summon

0x52

Kujata

Summon

0x53

Alexander

Summon

0x54

Phoenix

Summon

0x55

Neo Bahamut

Summon

0x56

Hades

Summon

0x57

Typhoon

Summon

0x58

Bahamut ZERO

Summon

0x59

Knights of Round

Summon

0x5A

Master Summon

Summon

0xFF

Empty Slot

NONE

## KERNEL.BIN Section 4 Entry\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D11&uselang=en 'Sign in to edit')\]

During game initialization, section 4 from KERNEL.BIN is decompressed and copied into RAM. This is all the initial values and structure for most of the Save, excluding the header data and the tail of the last bank (0x0054 to 0x0B93).

## Documentation Notes & Format\[[](https://auth.fandom.com/signin?redirect=https%3A%2F%2Fqhimm-modding.fandom.com%2Fwiki%2FFF7%2FSavemap%3Fveaction%3Dedit%26section%3D12&uselang=en 'Sign in to edit')\]

Format: Bit mask: Bit description \[Hex byte value\] {Field Keyword}  
Example: 0x04: Set to 1 if we choose no drink when talking to tifa. \[0x0F\] {MDS7PB_1}

Bit mask: Is the bit position number in hex. Bit7(0x80)|Bit6(0x40)|Bit5(0x20)|Bit4(0x10)|Bit3(0x08)|Bit2(0x04)|Bit1(0x02)|Bit0(0x01)

Note: We use LBS 0 bit numbering.

Bit description: What bit does.

Hex byte value: The Byte's value in hex when the bit change.(optional)

Field Keyword: Field name code.

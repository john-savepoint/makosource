# **The Kernel**

## *I. Kernel Overview* **1.1 History**

The kernel is a throwback to the very first Final Fantasy game for the Nintendo's original 8 bit system. The NES could only natively read 32 kilobytes of program ROM. To get around this incredible limitation, Nintendo developed "memory mappers" that allowed parts of the program to be switched out, or "banked" and replaced with other parts stored on the game cartridge.

FF1 used Nintendo's "Memory Manager Controller #1" (MMC1) . This controller split the game into sixteen sections, each 16 kilobytes long. (The maximum an MMC1 program could be was 256K). This controller also split the accessible memory from the cartridge into two 16K sections. The top 16K was bankable. The bottom 16K could never be switched out and stayed in memory until you removed the cartridge.

The original FF1 kernel was located in this bottom 16K of memory.

First and foremost the kernel contained the main program loop. It handled all the low level functions for the game. Some of these included controlling interrupts, banking in and out the appropriate part of the game, jumping control to a particular module, playing the music, and other tasks.

As the Final Fantasy franchise grew, so did the size of the games. They all still retained the kernel/module system. During the backporting process, this did cause a few headaches. For example, Final Fantasy VI was originally developed for the Super Nintendo. When its menu module was banked in, it was done with electronic bank switching. The later PSX port banked the data from the CD-ROM, which caused an unexpected lag that one wasn't used to. On the PC version for FF7, the menu system was simply integrated into the main executable.

#### **1.2 Kernel Functionality**

The Kernel is a threaded multitasking program that manages the whole system. It uses a simple software based memory manager that handles both RAM and video memory for all the modules in the game. Assisting the kernel are many statically linked Psy-Q libraries. In the case of the PC port, the Psy-Q libs were replaced with a PC equivalent. For example the SEQ player was replaced with a MIDI player, Both accomplish the same tasks, just with different formats and execution strategies. The table below is a generic representation of how the kernel sits in relation to the other aspects of the program.

| User     |                 |  |
|----------|-----------------|--|
| Module   |                 |  |
| Kernel   |                 |  |
|          | Psy-Q libraries |  |
| PSX BIOS |                 |  |
| Hardware |                 |  |

## *II. Memory management*

#### **1.1. RAM management**

No matter what module is banked into memory, there is a section of memory 4,340 bytes long (0x10F4 bytes) that is reserved for all the variables for the entire game. This entire image is called the "Save Map". When it's time to save a game, this section of memory is copied to non-volatile ram, such as a hard disk or memory card.

Within the save map there are 5 banks of memory that are directly accessible by the field scripting language. These can either be accessed 8 bits or 16 bits at a time depending on the field command argument. The following table is basic memory map of the banks and how they relate to the save map. There is also an allocation for 256 bytes for temporary field variables. These are not used between field files and are not saved.

| Offset | 8 Bit Field<br>Bank | 16 Bit Field<br>Bank | Description                           |
|--------|---------------------|----------------------|---------------------------------------|
| 0x0000 | N/A                 | N/A                  | Beginning of Save Map                 |
| 0x0BA4 | 0x1                 | 0x2                  | Field Script Bank 1                   |
| 0x0CA4 | 0x3                 | 0x4                  | Field Script Bank 2                   |
| 0x0DA4 | 0xB                 | 0xC                  | Field Script Bank 3                   |
| 0x0EA4 | 0xD                 | 0xE                  | Field Script Bank 4                   |
| 0x0FA4 | 0x7                 | 0xF                  | Field Script Bank 5                   |
| 0x10F4 | N/A                 | N/A                  | End of Save Map                       |
|        |                     |                      |                                       |
| N/A    | 0x5                 | 0x6                  | Temporary field variables (256 bytes) |

A more complete and annotated save map is in the MENU section.

#### **1.2. VRAM management**

The kernel is in charge of allocating, caching, and displaying in Video RAM. The the case if the PSX, port, the Playstation only has 1 megabyte of VRAM which makes this task a little complex. This is alleviated somewhat by using the PSX's VRAM caching system.

The PSX video memory can best be seen as a rectangular "surface" made up of 2048x512 pixels. A slight caveat to this model is that the PSX can hold multiple color depths in VRAM at the same time. To make the VRAM a little easier to visualize, This document represents VRAM as a 1024x512 matrix to allow for some color depth in either direction and to minimize some extreme skewing of the video buffers.

The following is a typical state of VRAM during game play.

![](_page_11_Picture_1.jpeg)

The two game screens on the left side are the video buffer and the back buffer. The patchwork of graphics on the top right are the field graphics for that scene. The bottom row consists of cached graphics and special effects and on right semi-permanent and permanent textures for the game.

The following is a schematic representation of VRAM and all its texture boundaries.

![](_page_11_Picture_4.jpeg)

Here the sections of VRAM are much more visible. The large cyan areas are the video frame buffers. The PSX uses a standard double page buffer to animate the game. The blank areas above and below the frame buffers are blank to allow for a correct V-sync. The dark blue areas to the right of the frame buffers are when the game plays 24 bit movies. This requires a slightly larger display and the first two texture caches are overwritten. During times in the game where no movies can take place, such as Battle, textures are commonly placed here.

The magenta area under the video buffers is the Color Look Up Tables (CLUT). This is where the texture palettes are stored. This is also allows the PSX to display multiple color depths at the same time. The red area to the right is extra CLUT space when it is needed and there are no textures cached there.

The green area on the right is the permanent menu textures and the yellow is where the menu font is located.

All the blank rectangles are the texture cache boundaries. In order of volatility, the top two rows of cache space are overwritten from left to right, and then the bottom rows are overwritten. The textures on the bottom right are barely overwritten except for key places.

#### **1.3. PSX CD-ROM management**

One of the big rules on PSX development is direct hardware access is a prohibited. Everything must go through the BIOS or the program will risk being incompatible with later systems. This means not only the from PSX to PS2, but also all the trivial hardware revisions as well. This creates a problem for the kernel. During module transitions, (For example, going from "Map" to "Battle"), the engine actually "preloads" the next module while the current one is still executing. This loading of data can't be done with a simple open() or read() BIOS syscall. Whenever you enter the BIOS, the rest of the system comes to a screeching halt until it is exited.

This problem is solved by the FF7 actually controlling the CD-ROM access itself though faster, lowlevel BIOS calls. The kernel can only load 8 kilobytes at a time in this "quick mode" The in this mode the kernel also only references files by what sector of the CD-ROM the data is located on, not by filename.

## *III. Game resources*

#### Important files:

| PSX Version      | PC Version               |
|------------------|--------------------------|
| /INIT/KERNEL.BIN | /DATA/KERNEL/KERNEL.BIN  |
|                  | /DATA/KERNEL/KERNEL2.BIN |

#### **1.1 The KERNEL.BIN Archive.**

The file /INIT/KERNEL.BIN is in BIN-GZIP format. This format is explained later in this document. It consists of 27 gziped sections concatenated together with a 6 byte header for each. This file is the same both on the PC and PSX versions. This holds all the static data and menu text for the game, with a look up table at the beginning of the section. Sections 10-27 are FF Text files.

The KERNEL.BIN file consists of the following sections.

| File | Data                          | Offset |
|------|-------------------------------|--------|
| 1    | Command data                  | 0x0006 |
| 2    | Attack data                   | 0x0086 |
| 3    | Unknown (Savemap?)            | 0x063A |
| 4    | Character starting stats      | 0x0F7F |
| 5    | Item data                     | 0x111B |
| 6    | Weapon data                   | 0x137A |
| 7    | Armor data                    | 0x1A30 |
| 8    | Accessory data                | 0x1B73 |
| 9    | Materia data                  | 0x1C11 |
| 10   | Command Descriptions          | 0x1F32 |
| 11   | Magic Descriptions            | 0x2119 |
| 12   | Item Descriptions             | 0x28D4 |
| 13   | Weapon Descriptions           | 0x2EE2 |
| 14   | Armor Descriptions            | 0x307B |
| 15   | Accessory Descriptions        | 0x315F |
| 16   | Materia Descriptions          | 0x3384 |
| 17   | Key Item Description          | 0x3838 |
| 18   | Command Names                 | 0x3BE2 |
| 19   | Magic Names                   | 0x3CCA |
| 20   | Item Names                    | 0x4293 |
| 21   | Weapon Names                  | 0x4651 |
| 22   | Armor Names                   | 0x4B02 |
| 23   | Accessory Names               | 0x4C4B |
| 24   | Materia Names                 | 0x4D90 |
| 25   | Key Item Names                | 0x5040 |
| 26   | Battle and Battle-Screen Text | 0x5217 |
| 27   | Summon Attack Names           | 0x5692 |

#### KERNEL.BIN Section formats

The first 9 sections of data (i.e. The non-text related items) have a typical BIN file format. The text sections (10-27) do not have the typical 6 byte header. The text sections have a header of pointers to the text block. The text is in FF text format.

#### Section 1: Command data format

This contains the data for Menu commands. Each recored is 16 bytes long

| Offset | Length | Description |  |
|--------|--------|-------------|--|
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |
|        |        |             |  |

#### Section 2: Attacks data format

This contains the data for the different attacks. Each record is 28 bytes long.

| Offset | Length  | Description      |                         |
|--------|---------|------------------|-------------------------|
| 0x00   | 4 bytes | Unknown          |                         |
| 0x04   | 1 byte  | Casting cost     |                         |
| 0x05   | 5 bytes | Unknown          |                         |
| 0x0A   | 1 byte  | Attack type      |                         |
| 0x0B   | 2 bytes | Attack attribute |                         |
|        |         | 0x0000           | Escape/Exit-Type        |
|        |         | 0x0001           | Ribbon-Like             |
|        |         | 0x0003           | Enemy Skill(?)          |
|        |         | 0x0005           | Enemy Skill(?)          |
|        |         | 0x0007           | Enemy Skill(?)          |
|        |         | 0x000D           | Restorative/Protective  |
|        |         | 0x000F           | Status-giving/Elemental |
|        |         | 0x0011           | Shield                  |
|        |         | 0x0013           | Limit Break             |
|        |         | 0x0015           | Cait Seith Limit Break  |
|        |         | 0x0017           | Summon                  |
|        |         | 0x00C7           | Roulette                |

| Offset | Length  |                 | Description                  |
|--------|---------|-----------------|------------------------------|
|        |         | 0x0097          | Multiple Strike Limit breaks |
|        |         | 0xFF01          | Phoenix Down                 |
|        |         | 0xFF03          | X-needles attack             |
|        |         | 0xFF17          | Final Limit break            |
| 0x0D   | 1 byte  | ID Number       |                              |
| 0x0E   | 1 byte  | Restore Apply   |                              |
| 0x0F   | 1 byte  | Strength        |                              |
| 0x10   | 1 byte  | Restore type    |                              |
|        |         | 0x00            | Restore HP                   |
|        |         | 0x01            | Restore MP                   |
|        |         | 0x02            | Restore Ailment              |
|        |         | 0xFF            | None                         |
| 0x11   | 2 bytes | Unknown         |                              |
| 0x13   | 1 byte  | Times attacking |                              |
| 0x14   | 4 bytes | Statuses        |                              |
| 0x18   | 2 bytes | Element         |                              |
| 0x20   | 2 bytes | Unknown         |                              |

#### Section 3 Savemap

This is all the initial values and structure for most of the Savemap, excluding the header data and the tail of the last bank. (0x0054 to 0x0fe7). This is copied into ram on initialization. This format is explained in the "Menu" Section.

#### Section 4 Initialization data

This contains the starting stats for the characters and related game states. On "New Game", this data is copied directly into the save map, (From offset 0x0054 to 0x0BAF) which is explained in the "Menu" section. This data has the same format as the data explained in that section.

#### Section 5 Item data format

This contains the item data. Each item record is 27 bytes long.

| Offset | Length  | Description      |                                                                             |  |
|--------|---------|------------------|-----------------------------------------------------------------------------|--|
| 0x00   | 8 bytes | Unknown          | [Always 0xFFFFFFFF]                                                         |  |
| 0x08   | 2 bytes | Unknown          |                                                                             |  |
| 0x0A   | 1 byte  | Restriction Mask |                                                                             |  |
|        |         | 0xFF             | Appears in Item Menu. Does not appear in<br>Battle Menu (Not usable at all) |  |
|        |         | 0xFE             | Appears in Battle Menu & Item Menu (Not<br>usable at all)                   |  |

| Offset | Length  | Description       |                                                                                                |
|--------|---------|-------------------|------------------------------------------------------------------------------------------------|
|        |         | 0xFD              | Appears in Item Menu. Does not appear in<br>Battle Menu (Usable in Battle Menu)                |
|        |         | 0xFC              | Appears in Battle Menu & Item Menu (Usable<br>in Battle Menu)                                  |
|        |         | 0xFB              | Appears in Item Menu. Does not appear in<br>Battle Menu (Usable in Item Menu)                  |
|        |         | 0xFA              | Appears in Battle Menu & Item Menu (Usable<br>in Item Menu)                                    |
|        |         | 0xF9              | Appears in Item Menu. Does not appear in<br>Battle Menu (Usable in Item Menu & Battle<br>Menu) |
|        |         | 0xF8              | Appears in Battle Menu & Item Menu (Usable<br>in Item Menu & Battle Menu)                      |
|        |         | 0xF7              | Appears in Item Menu. Does not appear in<br>Battle Menu (Usable in Battle Menu)                |
|        |         | 0xF6              | Appears in Battle Menu & Item Menu (Usable<br>in Battle Menu)                                  |
| 0x0B   | 2 bytes | Attack Target     |                                                                                                |
|        |         | 0x01              | One Target                                                                                     |
|        |         | 0x03              | Unknown                                                                                        |
|        |         | 0x05              | Multiple Targets                                                                               |
|        |         | 0x07              | Unknown                                                                                        |
|        |         | 0x10              | On Party Only                                                                                  |
| 0x0D   | 1 byte  | Item ID           |                                                                                                |
| 0x0E   | 1 byte  | Restore Apply     |                                                                                                |
|        |         | 0x00              | Unknown                                                                                        |
|        |         | 0x08              | Apply also to MP                                                                               |
|        |         | 0x22              | Unknown                                                                                        |
|        |         | 0x23              | Unknown                                                                                        |
|        |         | 0x24              | Damage / Restore by %                                                                          |
|        |         | 0x26              | Damage / Restore by 20 X Amount Multiplier                                                     |
|        |         | 0x37              | Causes Damage                                                                                  |
|        |         | 0x47              | Unknown                                                                                        |
|        |         | 0x50              | Affects Stats                                                                                  |
|        |         | 0xFF              | None                                                                                           |
| 0x0F   | 1 byte  | Amount Multiplier |                                                                                                |
| 0x10   | 1 byte  | Restore Type      |                                                                                                |

| Offset | Length  | Description    |                 |
|--------|---------|----------------|-----------------|
|        |         | 0x00           | Restore HP      |
|        |         | 0x01           | Restore MP      |
|        |         | 0x02           | Restore Ailment |
|        |         | 0xFF           | None            |
| 0x11   | 3 bytes | Unknown        |                 |
| 0x14   | 4 bytes | Status effects |                 |
| 0x18   | 2 bytes | Element        |                 |
| 0x1A   | 2 bytes | Unknown        |                 |

#### Section 6 Weapon data format

This contains the weapon data. Each Weapon attribute is 44 Bytes Long.

|                                |        | This contains the weapon data. Each Weapon attribute is 44 Bytes Long. |                                                                                                                                                                                                                                                   |  |
|--------------------------------|--------|------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| Offset                         | Length | Description                                                            |                                                                                                                                                                                                                                                   |  |
| 0x00<br>1 byte<br>Weapon Range |        |                                                                        |                                                                                                                                                                                                                                                   |  |
|                                |        | 0x03                                                                   | Long Range                                                                                                                                                                                                                                        |  |
|                                |        | 0x23                                                                   | Normal Range                                                                                                                                                                                                                                      |  |
| 0x01                           | 1 byte |                                                                        | Unknown [Always 0xFF]                                                                                                                                                                                                                             |  |
| 0x02                           | 1 byte |                                                                        | Special Options (Attack Modifiers)                                                                                                                                                                                                                |  |
|                                |        | 0x11                                                                   | Normal                                                                                                                                                                                                                                            |  |
|                                |        | 0xA0                                                                   | 1 + Number of Status Effects Tifa has out of following:<br>Near-death, Poison, Sadness, Silence, Slow, Darkness + 2 *<br>Number of Status Effects Tifa has out of following: Death<br>sentence, Slow-numb                                         |  |
|                                |        | 0xA1                                                                   | Power up when near death                                                                                                                                                                                                                          |  |
|                                |        | 0xA2                                                                   | 1 + Number of Allies in Death Status                                                                                                                                                                                                              |  |
|                                |        | 0xA3                                                                   | (Target's Level / 16) When used against allies, the weapon<br>will act like a physical hit, but will cause no damage (not<br>even a Miss or a 0). The Weapon has no Morph modifier; it<br>does the same damage with or without Morph. (Conformer) |  |
|                                |        | 0xA4                                                                   | (1 + [48 * Player's HP / Player's Max HP]) / 16                                                                                                                                                                                                   |  |
|                                |        | 0xA5                                                                   | (1 + [48 * Player's MP / Player's Max MP]) / 16                                                                                                                                                                                                   |  |
|                                |        | 0xA6                                                                   | (1 + [Total AP on Weapon / 10000]) / 16                                                                                                                                                                                                           |  |
|                                |        | 0xA7                                                                   | (10 + [Player's Kills / 128]) / 16                                                                                                                                                                                                                |  |
|                                |        | 0xA8                                                                   | (1 + [Player's Limit Level * Player's Limit Units / 16]) / 16                                                                                                                                                                                     |  |
| 0x03                           | 1 byte | Unknown [Always 0xFF]                                                  |                                                                                                                                                                                                                                                   |  |
| 0x04                           | 1 byte | Weapon Attack                                                          |                                                                                                                                                                                                                                                   |  |
| 0x05                           | 1 byte | Unknown [Always 0xFF]                                                  |                                                                                                                                                                                                                                                   |  |
| 0x06                           | 1 byte | Materia growth rate                                                    |                                                                                                                                                                                                                                                   |  |

| Offset | Length  | Description                        |                          |  |
|--------|---------|------------------------------------|--------------------------|--|
| 0x07   | 1 byte  | Unknown                            |                          |  |
| 0x08   | 1 byte  | Weapon attack percentage           |                          |  |
| 0x09   | 3 bytes | Weapon Model ID                    |                          |  |
| 0x0C   | 2 bytes |                                    | Unknown [Aways 0xFFFF]   |  |
| 0x0E   | 2 bytes | Equip Mask                         |                          |  |
|        |         | 0x0001                             | Equipable on Cloud       |  |
|        |         | 0x0002                             | Equipable on Barret      |  |
|        |         | 0x0004                             | Equipable on Tifa        |  |
|        |         | 0x0008                             | Equipable on Aeris       |  |
|        |         | 0x0010                             | Equipable on Red XIII    |  |
|        |         | 0x0020                             | Equipable on Yuffie      |  |
|        |         | 0x0040                             | Equipable on Cait Sith   |  |
|        |         | 0x0080                             | Equipable on Vincent     |  |
|        |         | 0x0100                             | Equipable on Cid         |  |
|        |         | 0x0200                             | Equipable on Young Cloud |  |
|        |         | 0x0400                             | Equipable on Sephiroth   |  |
| 0x10   | 2 bytes | Attack Type                        |                          |  |
|        |         | 0x0004                             | Cut                      |  |
|        |         | 0x0008                             | Hit                      |  |
|        |         | 0x0010                             | Punch                    |  |
|        |         | 0x0020                             | Hit                      |  |
| 0x12   | 2 bytes | Unknown [Always 0xFFFF]            |                          |  |
| 0x14   | 4 bytes | Increase Stat Type                 |                          |  |
|        |         | 0xFF                               | None                     |  |
|        |         | 0x00                               | Strength                 |  |
|        |         | 0x01                               | Vitality                 |  |
|        |         | 0x02                               | Magic                    |  |
|        |         | 0x03                               | Spirit                   |  |
|        |         | 0x04                               | Dexterity                |  |
|        |         | 0x05                               | Luck                     |  |
| 0x18   | 4 bytes | Stat Amount Increased(Based on IT) |                          |  |
| 0x1C   | 8 bytes | Materia Slots                      |                          |  |

| Offset | Length  | Description           |                                                                                             |  |  |
|--------|---------|-----------------------|---------------------------------------------------------------------------------------------|--|--|
|        |         | 0x00                  | No Slot                                                                                     |  |  |
|        |         | 0x05                  | Unlinked Slot                                                                               |  |  |
|        |         | 0x06                  | Left Linked Slot                                                                            |  |  |
|        |         | 0x07                  | Right Linked Slot                                                                           |  |  |
| 0x24   | 3 bytes | Unknown               |                                                                                             |  |  |
| 0x27   | 1 byte  |                       | Attack texture graphic                                                                      |  |  |
| 0x28   | 2 byes  |                       | Unknown [Always 0xFFFF]                                                                     |  |  |
| 0x2A   | 1 byte  |                       | Restriction Mask                                                                            |  |  |
|        |         | 0xFF                  | Appears in Item Menu. Does not appear in Battle Menu<br>(Not usable at all)                 |  |  |
|        |         | 0xFE                  | Appears in Battle Menu & Item Menu (Not usable at all)                                      |  |  |
|        |         | 0xFD                  | Appears in Item Menu. Does not appear in Battle Menu<br>(Usable in Battle Menu)             |  |  |
|        |         | 0xFC                  | Appears in Battle Menu & Item Menu (Usable in Battle<br>Menu)                               |  |  |
|        |         | 0xFB                  | Appears in Item Menu. Does not appear in Battle Menu<br>(Usable in Item Menu)               |  |  |
|        |         | 0xFA                  | Appears in Battle Menu & Item Menu (Usable in Item<br>Menu)                                 |  |  |
|        |         | 0xF9                  | Appears in Item Menu. Does not appear in Battle Menu<br>(Usable in Item Menu & Battle Menu) |  |  |
|        |         | 0xF8                  | Appears in Battle Menu & Item Menu (Usable in Item<br>Menu & Battle Menu)                   |  |  |
|        |         | 0xF7                  | Appears in Item Menu. Does not appear in Battle Menu<br>(Usable in Battle Menu)             |  |  |
|        |         | 0xF6                  | Appears in Battle Menu & Item Menu (Usable in Battle<br>Menu)                               |  |  |
| 0x2B   | 1 byte  | Unknown [Always 0xFF] |                                                                                             |  |  |

#### Section 7 Armor data format

This contains the armor data. Each record is 36 bytes long.

| Offset | Length | Description                                        |           |  |
|--------|--------|----------------------------------------------------|-----------|--|
| 0x01   | 1 byte | Unknown                                            |           |  |
| 0x02   | 1 byte | Damage Type,<br>Based off values of Elemental Type |           |  |
|        |        | 0xFF                                               | Normal    |  |
|        |        | 0x00                                               | Absorb    |  |
|        |        | 0x01                                               | No Damage |  |
|        |        | 0x02                                               | Half      |  |

| Offset | Length  | Description                |                   |  |
|--------|---------|----------------------------|-------------------|--|
| 0x03   | 1 byte  | Defense                    |                   |  |
| 0x04   | 1 byte  | Magic Defense              |                   |  |
| 0x05   | 1 byte  | Defense %                  |                   |  |
| 0x06   | 1 byte  | Magic Defense %            |                   |  |
| 0x07   | 3 bytes | Unknown                    |                   |  |
| 0x08   | 8 Bytes | Materia Slots              |                   |  |
|        |         | 0x00                       | No Slot           |  |
|        |         | 0x05                       | Unlinked Slot     |  |
|        |         | 0x06                       | Left Linked Slot  |  |
|        |         | 0x07                       | Right Linked Slot |  |
| 0x12   | 1 byte  | Materia Growth             |                   |  |
| 0x13   | 1 byte  | Equip Mask                 |                   |  |
|        |         | 0xFF01                     | Everyone          |  |
|        |         | 0x2C00                     | All Females       |  |
|        |         | 0xD303                     | All Males         |  |
| 0x15   | 1 byte  | Element                    |                   |  |
|        |         | 0x01                       | Fire              |  |
|        |         | 0x02                       | Ice               |  |
|        |         | 0x04                       | Bolt              |  |
|        |         | 0xFF                       | All Elements      |  |
| 0x16   | 1 byte  | Unknown                    |                   |  |
| 0x17   | 2 bytes | Unknown                    | [Always 0x00FF]   |  |
| 0x19   | 2 bytes | Stat Bonus                 |                   |  |
|        |         | 0xFF                       | None              |  |
|        |         | 0x00                       | Strength          |  |
|        |         | 0x01                       | Vitality          |  |
|        |         | 0x02                       | Magic             |  |
|        |         | 0x03                       | Spirit            |  |
|        |         | 0x04                       | Dexterity         |  |
|        |         | 0x05                       | Luck              |  |
| 0x1B   | 2 bytes | Unknown                    | [Always 0xFFFF]   |  |
| 0x1D   | 2 bytes | Stat increase              |                   |  |
| 0x1F   | 2 bytes | Unknown<br>[Always 0xFFFF] |                   |  |
| 0x21   | 1 byte  | Restriction Mask           |                   |  |

| Offset | Length  | Description |                                                                                                |  |
|--------|---------|-------------|------------------------------------------------------------------------------------------------|--|
|        |         | 0xFF        | Appears in Item Menu. Does not<br>appear in Battle Menu (Not usable<br>at all)                 |  |
|        |         | 0xFE        | Appears in Battle Menu & Item<br>Menu (Not usable at all)                                      |  |
|        |         | 0xFD        | Appears in Item Menu. Does not<br>appear in Battle Menu (Usable in<br>Battle Menu)             |  |
|        |         | 0xFC        | Appears in Battle Menu & Item<br>Menu (Usable in Battle Menu)                                  |  |
|        |         | 0xFB        | Appears in Item Menu. Does not<br>appear in Battle Menu (Usable in<br>Item Menu)               |  |
|        |         | 0xFA        | Appears in Battle Menu & Item<br>Menu (Usable in Item Menu)                                    |  |
|        |         | 0xF9        | Appears in Item Menu. Does not<br>appear in Battle Menu (Usable in<br>Item Menu & Battle Menu) |  |
|        |         | 0xF8        | Appears in Battle Menu & Item<br>Menu (Usable in Item Menu &<br>Battle Menu)                   |  |
|        |         | 0xF7        | Appears in Item Menu. Does not<br>appear in Battle Menu (Usable in<br>Battle Menu)             |  |
|        |         | 0xF6        | Appears in Battle Menu & Item<br>Menu (Usable in Battle Menu)                                  |  |
| 0x22   | 3 bytes | Unknown     | [Aways 0xFFFFFF]                                                                               |  |

#### Section 8 Accessory data format

This contains the accessory data. Each record is 16 bytes long.

| Offset          | Length  | Description  |           |  |
|-----------------|---------|--------------|-----------|--|
| 0x00            | 2 bytes | Stat Bonus   |           |  |
|                 |         | 0xFF         | None      |  |
|                 |         | 0x00         | Strength  |  |
|                 |         | 0x01         | Vitality  |  |
|                 |         | 0x02         | Magic     |  |
|                 |         | 0x03         | Spirit    |  |
|                 |         | 0x04         | Dexterity |  |
|                 |         | 0x05         | Luck      |  |
| 0x02<br>2 bytes |         | Bonus Amount |           |  |

| Length  | Description        |                            |
|---------|--------------------|----------------------------|
| 1 byte  | Elemental Strength |                            |
|         | 0x00               | Drains                     |
|         | 0x01               | Nullifies                  |
| 1 byte  | Special Effect     |                            |
|         | 0x00               | Haste                      |
|         | 0x01               | Fury                       |
|         | 0x02               | Curse Ring Effect          |
|         | 0x03               | Reflect                    |
|         | 0x04               | Increase Stealing Rate     |
|         | 0x05               | Increase Manipulation Rate |
|         | 0x06               | Barrier / MBarrier         |
| 2 bytes | Elemental Type     |                            |
|         | 0x01               | Fire                       |
|         | 0x02               | Ice                        |
|         | 0x04               | Lightning                  |
|         | 0x08               | Earth                      |
|         | 0x10               | Poison                     |
|         | 0x20               | Gravity                    |
|         | 0x40               | Water                      |
|         | 0x80               | Wind                       |
|         | 0x0001             | Holy                       |
|         | 0xFF01             | All of the above           |
| 4 bytes | Status Protect     |                            |
|         | 0x00               | None                       |
|         | 0x01               | Death                      |
|         | 0x02               | Near Death                 |
|         | 0x04               | Sleep                      |
|         | 0x08               | Poison                     |
|         | 0x10               | Sadness                    |
|         | 0x20               | Fury                       |
|         | 0x40               | Confusion                  |
|         | 0x80               | Silence                    |
|         |                    | Haste                      |
|         | 0x0020             | Slow                       |
|         |                    | 0x0010                     |

| Offset | Length | Description                      |                                                                                    |  |
|--------|--------|----------------------------------|------------------------------------------------------------------------------------|--|
|        |        | 0x0040                           | Stop                                                                               |  |
|        |        | 0x0080                           | Frog                                                                               |  |
|        |        | 0x0001<br>Small                  |                                                                                    |  |
|        |        | 0x0002                           | Slow-numb                                                                          |  |
|        |        | 0x0004                           | Petrify                                                                            |  |
|        |        | 0x0008                           | Regen                                                                              |  |
|        |        | 0xFFFF                           | All Of The Above                                                                   |  |
| 0x0C   | 2 byes | Equip Mask                       |                                                                                    |  |
|        |        | 0x0001                           | Equipable on Cloud                                                                 |  |
|        |        | 0x0002                           | Equipable on Barret                                                                |  |
|        |        | 0x0004                           | Equipable on Tifa                                                                  |  |
|        |        | 0x0008                           | Equipable on Aeris                                                                 |  |
|        |        | 0x0010                           | Equipable on Red XIII                                                              |  |
|        |        | 0x0020                           | Equipable on Yuffie                                                                |  |
|        |        | 0x0040<br>Equipable on Cait Sith |                                                                                    |  |
|        |        | 0x0080                           | Equipable on Vincent                                                               |  |
|        |        | 0x0100<br>Equipable on Cid       |                                                                                    |  |
|        |        | 0x0200                           | Equipable on Young Cloud                                                           |  |
|        |        | 0x0400                           | Equipable on Sephiroth                                                             |  |
| 0x0E   | 1 byte | Restriction Mask                 |                                                                                    |  |
|        |        | 0xFF                             | Appears in Item Menu. Does<br>not appear in Battle Menu<br>(Not usable at all)     |  |
|        |        | 0xFE                             | Appears in Battle Menu &<br>Item Menu (Not usable at all)                          |  |
|        |        | 0xFD                             | Appears in Item Menu. Does<br>not appear in Battle Menu<br>(Usable in Battle Menu) |  |
|        |        | 0xFC                             | Appears in Battle Menu &<br>Item Menu (Usable in Battle<br>Menu)                   |  |
|        |        | 0xFB                             | Appears in Item Menu. Does<br>not appear in Battle Menu<br>(Usable in Item Menu)   |  |
|        |        | 0xFA                             | Appears in Battle Menu &<br>Item Menu (Usable in Item<br>Menu)                     |  |

| Offset | Length | Description |                                                                                                   |  |
|--------|--------|-------------|---------------------------------------------------------------------------------------------------|--|
|        |        | 0xF9        | Appears in Item Menu. Does<br>not appear in Battle Menu<br>(Usable in Item Menu &<br>Battle Menu) |  |
|        |        | 0xF8        | Appears in Battle Menu &<br>Item Menu (Usable in Item<br>Menu & Battle Menu)                      |  |
|        |        | 0xF7        | Appears in Item Menu. Does<br>not appear in Battle Menu<br>(Usable in Battle Menu)                |  |
|        |        | 0xF6        | Appears in Battle Menu &<br>Item Menu (Usable in Battle<br>Menu)                                  |  |
| 0x0F   | 1 byte | Unknown     | [Always 0xFF]                                                                                     |  |

#### Section 9 Materia data format

This contains the Materia data. Each record is 20 bytes long.

| Offset | Length  | Description        |                                                                                |  |  |  |
|--------|---------|--------------------|--------------------------------------------------------------------------------|--|--|--|
| 0x00   | 8 bytes | Level-up AP limits | Multiples of 100 (4x WORD)                                                     |  |  |  |
| 0x08   | 1 byte  | Equip Effect       | [See table below]                                                              |  |  |  |
| 0x09   | 3 bytes | Status Bitmask     |                                                                                |  |  |  |
| 0x0C   | 1 byte  | Element            |                                                                                |  |  |  |
| 0x0D   | 1 Byte  | Materia Type       |                                                                                |  |  |  |
|        |         | 0x00               | Unknown                                                                        |  |  |  |
|        |         | 0x08               | Master Command: All commands are available                                     |  |  |  |
|        |         | 0x0A               | Master Magic: All spells are available                                         |  |  |  |
|        |         | 0x0C               | Master Summon: All summons are available                                       |  |  |  |
|        |         | 0x12               | Command: Command at offset 0x0E to 0x12 is<br>available, depending on AP level |  |  |  |
|        |         | 0x16               | Command: Commands at offset 0x0E to 0x12<br>become available as you level up.  |  |  |  |
|        |         | 0x19               | Magic: Spells 0x0E to 0x11 become available<br>as you level up                 |  |  |  |
|        |         | 0x20               | Booster%: 0x0E is boosted by offset 0x0F to<br>0x13 depending on AP level      |  |  |  |
|        |         | 0x21               | Unknown                                                                        |  |  |  |
|        |         | 0x25               | Unknown                                                                        |  |  |  |
|        |         | 0x30               | Unknown                                                                        |  |  |  |

| Offset | Length | Description        |                                                                                           |  |
|--------|--------|--------------------|-------------------------------------------------------------------------------------------|--|
|        |        | 0x33               | W-Command: Command at 0x0E is added to the<br>battle menu                                 |  |
|        |        | 0x35               | Unknown                                                                                   |  |
|        |        | 0x3B               | Summon: Spell at 0x0E can be used from offset<br>0x0F to 0x13 times depending on AP level |  |
|        |        | 0x57               | Enemy Skill:Enables command 'Enemy Skill'                                                 |  |
| 0x0E   | 1 byte | Materia attributes | [See Above]                                                                               |  |
| 0x0F   | 1 byte | Materia attributes | [See Above]                                                                               |  |
| 0x10   | 1 byte | Materia attributes | [See Above]                                                                               |  |
| 0x11   | 1 byte | Materia attributes | [See Above]                                                                               |  |
| 0x12   | 1 byte | Materia attributes | [See Above]                                                                               |  |
| 0x13   | 1 byte | Materia attributes | [See Above]                                                                               |  |

Equip Effects

| Byte | STR | VIT | MAG | MDEF | MAXHP | MAXMP | LUCK | DEX |
|------|-----|-----|-----|------|-------|-------|------|-----|
| 0x00 |     |     |     |      |       |       |      |     |
| 0x01 | -02 | -01 | +02 | +01  | -05%  | +05%  |      |     |
| 0x02 | -04 | -04 | +04 | +02  | -10%  | +10%  |      |     |
| 0x06 |     | +01 |     |      |       |       |      |     |
| 0x07 |     |     |     |      |       |       | +01  |     |
| 0x08 |     |     |     |      |       |       | -01  |     |
| 0x0A |     |     |     |      |       |       |      | +02 |
| 0x0B | -01 |     | +01 |      | -02%  | +02%  |      |     |
| 0x0C |     |     | +01 |      | -02%  | +02%  |      |     |
| 0x0D |     |     | +01 | +01  | -05%  | +05%  |      |     |
| 0x0E |     |     | +02 | +02  | -10%  | +10%  |      |     |
| 0x0F |     |     | +04 | +04  | -10%  | +15%  |      |     |
| 0x10 |     |     | +08 | +08  | -10%  | +20%  |      |     |

#### **2.1 The KERNEL2.BIN Archive.**

On the PC version there exists a secondary kernel archive called KERNEL2.BIN.This archive contains only sections 10-27 (Text data) of KERNEL.BIN. The data was ungzipped from the original archive, concatenated together, and then LZSed into a single archive with a 4 byte header giving the length of the file. See the section on BIN types and LZS compression later in this document for more information.

## *IV. Low Level Libraries*

#### **1. PC to PSX comparison**

The files and data formats used in the PSX version of FF7 and its PC port are conceptually the same thing, and accomplish the same tasks. That being said, they both have wildly different formats. Both of which were derived from a third original format that is also somewhat different than the first two.

The original PSX FF7 was created in part using Sony's Psy-Q development library. This library uses common formats that are "native" to the PSX. Often times a toolkit was used to convert common development- based formats, such as a TGA bitmap or a palleted GIF file, to something a little more suited to Psy-Q, which would be a TIM file.

During the porting process to the PC, some of the original artwork, (and artists for that matter), were no longer available. This resulted in the port team having to use the Psy-Q versions of many files, which were ill suited for the PC architecture. In our example, the TIM file was converted to a TEX file, which would be manipulated in the PC's video memory a little more efficiently. Sometimes the original artwork was available, such as the pictures of the characters within the menu, or the original MIDI files. Most often times it was not.

To make things a little more confusing, both systems also archive their data files in different ways, making the extraction and rendering of each file a bit of a bear. For the most part the data within each file is the same thing, just a little switched around. This manual will cover the more generic files first, and then common files used in each module.

### **1.1 DATA ARCHIVES**

To save space, quicken access time, and to obfuscate the file structure a little, most of the data files are stored in some kind of archive format. The archives remove such useful items as subdirectories and logical data placement. There is no real "native" format these are based on.

#### **1.1.1 BIN archive data format**

The BIN format comes as two different types. They both have the same extension, so one must open the file to see which format is which. They are best described as BIN Types and Bin-GZIP types

#### BIN Types

These are uncompressed archives. The header consists of a 4 byte header that gives the length of the file without the header and then the data beyond that.

#### BIN-GZIP Types

Unless otherwise noted, these have a 6 byte header. After this are many gziped sections concatenated together.

| Offset | Length  | Description                          |  |
|--------|---------|--------------------------------------|--|
| 0x0000 | 2 bytes | Length of gzipped sections           |  |
| 0x0002 | 2 bytes | Unknown                              |  |
| 0x0004 | 2 bytes | File number                          |  |
| 0x0006 | varies  | [0x1F8B080000000000] - Gzip header 1 |  |
| varies | 2 bytes | Length of gzipped sections           |  |

| Offset | Length  | Description                          |  |  |
|--------|---------|--------------------------------------|--|--|
| varies | 2 bytes | Unknown                              |  |  |
| varies | 2 bytes | File number                          |  |  |
| varies | varies  | [0x1F8B080000000000] - Gzip header 2 |  |  |
|        |         |                                      |  |  |

#### **1.1.2 LZS Compressed archive for PSX by Ficedula**

#### Format

The LZS archive has a very small header at 0x00 that has the length of the decompressed file as an unsigned 32 bit integer. After that is the compressed data.

### LZS compression

FF7 uses LZS compression on some of their files - more properly, a slightly modified version of LZSS compression as devised by Professor Haruhiko Okumura.

LZS data works on a control byte scheme. So each block in the file begins with a single byte indicating how much of the block is uncompressed ('literal data'), and how much is compressed ('references'). You read the byte right-to-left, with 1=literal, 0=reference.

Literal data means just that: read one byte in from the source (compressed) data, and write it straight to the output.

References take up two bytes, and are essentially a pointer to a piece of data that's been written out (i.e. is part of the data you've already decompressed). LZSS uses a 4K buffer, so it can only reference data in the last 4K of data.

#### Reference format

A reference takes up two bytes, and has two pieces of information in it: offset (where to find the data, or which piece of data is going to be repeated), and length (how long the piece of data is going to be). The two reference bytes look like this:

OOOO OOOO OOOO LLLL (O=Offset, L=Length).

So you get a 12-bit offset and a 4-bit length, but both of these values need modifying to work on directly. The length is easy to work with: just add 3 to it. Why? Well, if a piece of repeated data was less than 3 bytes long, you wouldn't bother repeating it - it'd take up no more space to actually just put literal data in. So all references are at least 3 in length. So a length of 0 means 3 bytes repeated, 1 means 4 bytes repeated, so on. Since we have 4 bits available, that gives us a final length ranging from 3-18 bytes long. (That also means the absolute maximum compression we can ever get using LZSS is a touch under 9:1, since the best possible is to replace 18 bytes of data with two bytes of reference, and then you have to add control bytes as well.)

Offset needs a bit work doing on it, depending on how you're actually holding your data. If all you

have is an input buffer and an output buffer, what you really need is an output position in your buffer to start reading data from. In other words, if you've already written 10,000 bytes to your output, you want to know where to retrieve the repeated data from - it could fall anywhere in the past 4K of data, (i.e. from 5904 through to 9999 bytes.)

Here's how you get it:

```
real_offset = tail - ((tail - 18 - raw_offset) mod 4096)
```

Here, 'tail' is your current output position (eg. 10,000), 'raw\_offset' is the 12-bit data value you've retrieved from the compressed reference, and 'real\_offset' is the position in your output buffer you can begin reading from. This is a bit complex because it's not exactly the way LZSS traditionally does (de) compression; it uses a 4K circular buffer; if you do that, the offset is more or less usable directly.

Once you've got to the start position for your reference, you just copy the appropriate length of data over to your output, and you've dealt with that piece of data.

#### Example

If we're at position 1000 in our output, and we need to read in a new control byte because we've finished with the last one. The next data to look it is:

0x03, 0x53, 0x12 .....

We read in a control byte: \$03. In binary, that's 00000011. That informs us that the current block of data has two compressed offsets (@ 2 bytes each), followed by 6 literal data bytes. Once we'd read in the next 10 bytes (the compressed data plus the literal data), we'd be ready to read in our next control byte and start again.

Looking at the first compressed reference, we read in \$53 \$12. That gives us a base offset of \$153 (the 53 from the first byte, and the '1' from the second byte makes up the higher nybble). The base length is \$2 (we just take the low nybble of the second byte).

Our final length is obviously just 5. Our position in output is still 1000. So our final offset is:

=1000 - ((1000 - 18 - 339) and \$FFF)

The 339 is just \$153 in decimal.

The (and \$FFF) is a quick way to do modulus 4096.

```
=1000 - (643 and 0xFFF)
=1000 - 643
=357
```

So our final offset is 357. We go to position 357 in our output data, read in 5 bytes (remember the length?), then write those 5 bytes out to our output. Now we're ready to read in the next bit of data (another compressed reference), and do the procedure again...

## Complications

Unfortunately, that doesn't quite cover everything - there's two more things to be aware of when decompressing data that \*will\* ruin you when using FF7 files, since they do use these features. First, if you end up with an negative offset, i.e. reading data from 'before the beginning of the file', write out nulls (zero bytes). That's because the compression buffer is, by default, initialized to zeros; so it's possible, if the start of the file contains a run of zeros, that the file may reference a block you haven't written...

EG: If you're at position 50 in your output, it's possible you may get an offset indicating to go back 60 bytes to offset -10! If you have to read 5 bytes from there, it's simple: you just write out 5 nulls. However, you \*could\* have to read 15 bytes from there. In that case, you write out 10 nulls (the part of the data 'before' the file start), then the 5 bytes from the beginning of the file.

Secondly, you can have a repeated run. This is almost the opposite problem: when you go off the end of your output. Say you're at offset 100 in your output, and you have to go to offset 95 to read in a reference. That's OK ... but what if the reference length is >5? In that case, you loop the output. So if you had to write out 15 bytes, you'd write out the five bytes that \*were\* available ... and then write them out again ... then again, to make up the 15 bytes you needed.

The FF7 files use both of these 'tricks', so you can't ignore them!

#### **1.1.3. LGP Archive format for PC by Ficedula**

This section explains how the LGP archives from FF7 PC are constructed. If you're looking for a tool that already manages LGP archives, try [Ficedula](https://qhimm-modding.fandom.com/wiki/User:Ficedula)'s [LGP Editor](http://sylphds.net/f2k3/index.html).

Essentially the LGP file is split up into four (maybe less, depending on how you count it) sections.

1. File header/Table of contents
2. CRC code
3. Actual data
4. File terminator

#### SECTION 1: FILE HEADER

This contains two parts: A header of fixed size, then the table of contents.

The first item is 12 bytes containing the file creator. This is a standard string, except it is "rightaligned". In other words the blank space comes before the actual text, not after. In FF7 it's always "SQUARESOFT" preceded by two nulls to make it 12 bytes. The only other thing you might see is the header "FICEDULA-LGP", which I use to indicate a file is an LGP \*patch\* one of my programs has constructed, not a complete archive.

Next is a four-byte integer saying how many files the archive contains.

Following this is the table of contents (TOC): One entry per file.

Each entry in the TOC has the following structure:

| Offset | Length |
| --- | --- |
| 20 bytes | Null terminated string, giving filename |
| 4 byte integer | Position in this file where data starts for the file |
| 1 byte | Some sort of check code. File attributes? Normally seems to be 14 but it does vary. |
| 2 byte short | Something to do with duplicate file names. If a name is unique it is 0, otherwise it is assigned a value based on existing duplicates. (Hard to explain) |

## SECTION 2: CRC CODE

This code is used to validate the LGP archive. The bad news is I have no idea how to make it (I've figured out how to decode it, ie. find out whether the archive is valid, but I can't create my own). The good news is you don't need to! The only thing this CRC is based on is the number of files in the archive (maybe the filenames too, haven't checked that). Anyway, the TOC is the only thing this check relates to. So if you're replicating an archive from FF7 for use in the game with the same number of files and filenames you can just copy the CRC section from an existing file.

Normally it's 3602 bytes long (one archive may be different, possibly MAGIC.LGP). Anyway, one normally-safe way of calculating the CRC size is to find the end of the TOC and the beginning of the first file. Anything in between is probably CRC code (this is not guaranteed to work. It works with "official" archives but editors - such as [LGP Editor](http://www.ficedula.com/) - can alter the TOC to achieve extra things).

## SECTION 3: ACTUAL DATA

The data from the files. However it's not that simple: the TOC doesn't list how long each file is (somewhat useful). It's done here. The offset in the TOC is actually the position of yet another file header. Format is:

| Size | Description |
| :-: | --- |
| 20 bytes | Null terminated string, giving filename |
| 4 bytes | File length |
| Varies | The file data itself |

#### SECTION 4: TERMINATOR

After the last piece of data comes the file descriptor. This is a simple string, except instead of being null-terminated it's terminated by the end of the file. It's "FINAL FANTASY 7" for all archives, except LGP patches, where it's "LGP PATCH FILE".

#### NOTES

The game is remarkably flexible about LGP archives. So long as the TOC and the CRC data is intact it'll accept just about anything.

Example 1: The filename in the TOC and in the actual file header don't have to match. It only checks the TOC.

Example 2: You can point two entries in the TOC at the same data and it works.

Example 3: You can have ANY junk in the data section so long as all the TOC entries point to a valid file header. Not every piece of data has to be "accounted" for by the TOC. There can be data not used.

[LGP Editor](http://www.ficedula.com/) uses this to its advantage in the Advanced Editor. If you want to replace a file in an LGP archive with your own copy, it just puts the file on the end of the LGP, writes a new file terminator, and updates the TOC to point at the new file. It even lets you link two TOC entries to the same data or have "inactive" files in the archive that aren't referenced by any TOC entry.

I don't know whether the file terminator has to be intact, but for safety's sake my editor preserves it. The CRC must be present and correct. Also, if you're replacing an archive with your own custom version make sure it has filenames in the TOC matching the ones in the old one.

The game doesn't check archive sizes as long as all filenames are present. So if you want, you could replace an archive containing 95 files with a 98-file archive, so long as 95 of those 98 names matched those present in the original 95-file archive. (However there's no point in doing this when the game won't use any files other than the 95 it's expecting to find).

There are reports on [Qhimm's board](http://forums.qhimm.com/) that once you've altered an archive and the game refuses to read it, it won't ever read it until you reinstall - even if you fix the problem/restore from a backup. The idea was generally scorned and ignored, but I'll mention it because something like that happened to me. No solid conclusion can be drawn here.

Sometimes, there are data "gaps" in the file that don't appear to be referenced by any file - even by an inactive file. If you're only using the TOC method to get at files (the easy way) then you won't notice this anyway. However, if you're stepping through the file header by header, even reading the unused ones, this can cause problems. If you use my program to update a file with one that's smaller than the original (can happen) then it writes it in, but leaves a gap after it (of course). However, to help you out, after the end of the file, it writes a 4 byte integer saying how much more space to skip over to reach the next file header.

This really doesn't affect many things - only tools (like my Advanced LGP Editor) that bypass the TOC to construct their own file lists. FF7 never notices a thing.

**Useful downloads:**

Below there are links to known programs that are capable to edit LGP archives:

- [LGP Tools](http://www.sylphds.net/f2k3/programs/lgptools/lgptools160.zip) - with an Advanced LGP Editor allowing edit archive thoroughly
- [Emerald](http://elentor.com/Projetos/FF7-Tools/Extracting/Emerald.zip) - has mass extracting/repacking function
- [Unmass](http://mirex.mypage.sk/index.php?selected=1#Unmass) - general file extractor with LGP archives support

#### **2. TEXTURES**

A texture is just a picture that's placed into video memory. It is later manipulated by the engine and displayed on the screen. The native format of a texture was the Psy-Q TIM (Texture Image Map). This is used as the native format for the PSX version as well, with a few caveats explained below. The file can hold multiple color look up tables. This was one of the reasons why you needed a video card on the PC that could do palleted data even at high color depths.

#### **2.1 TIM texture data format for PSX**

The TIM files are found both on raw format and also within several archives, including BIN, LZS, or

even MNU. The format proper has the ability to contain 24 bit bitmaps, but is not used in FF7. The Format was created because the PSX does not have direct access to its VRAM, and must go through the GPU for any graphic access. A TIM file is a clean way to load a texture and color look up table into VRAM.

#### **2.1.1. Basic Terms**

#### CLUT:

Color look up table. In the PSX's VRAM, it allocates a high color depth table and uses it as a reference for palleted textures. The CLUT in VRAM can be directly changed by the GPU and have the updated color data appear automatically on the screen without having to re-render the view port.

#### VRAM Location:

This is the location the TIM is to be loaded into video memory. The PSX uses a "surface" that one can place viewing windows, textures, and color look up tables using an X/Y coordinate. There are also several cache areas in the PSX's VRAM, and this allows you to place the texture in the correct cache. It also helps to know where your texture is located.

#### CLUT Location:

This is the location where the CLUT is to be loaded into video memory.

#### **2.1.2 TIM file Format**

A TIM has a slightly different format for each color depth. They are explained below.

#### 4 Bits Per Pixel

| Offset              | Size                                | Description             |  |  |
|---------------------|-------------------------------------|-------------------------|--|--|
| 0x00                | 4 bytes                             | 10 00 00 00 : TIM ID    |  |  |
| 0x04                | 4 bytes                             | 08 00 00 00 : 4bpp flag |  |  |
| 0x08                | 4 bytes                             | Unknown                 |  |  |
| 0x0c                | 2 bytes                             | CLUT Location X         |  |  |
| 0x0e                | 2 bytes                             | CLUT Location Y         |  |  |
| 0x10                | 2 bytes                             | Unknown                 |  |  |
| 0x12                | 2 bytes                             | Number Of CLUT entries  |  |  |
| 0x14                | 32 bytes<br>per CLUT<br>(16 colors) | CLUT Data               |  |  |
| After the CLUT data |                                     |                         |  |  |
| +0x00               | 4 bytes                             | Unknown                 |  |  |
| +0x04               | 2 bytes                             | VRAM Location X         |  |  |
| +0x06               | 2 bytes                             | VRAM Location Y         |  |  |
| +0x08               | 2 bytes                             | Image Width / 4         |  |  |
| +0x10               | 2 bytes                             | Image Height            |  |  |
| +0x12               | Varies                              | See below               |  |  |

| Offset | Size | Description |
|--------|------|-------------|
|--------|------|-------------|

Within the Texture data, each byte contains the left and right pixel, with each value corresponding to a color index with 16 entries loaded by the CLUT data

[1,2][3,4][5,6].....

#### 8 Bits Per Pixel

| Offset                                          | Size         | Description             |  |  |  |
|-------------------------------------------------|--------------|-------------------------|--|--|--|
| 0x00                                            | 4 bytes      | 10 00 00 00 : TIM ID    |  |  |  |
| 0x04                                            | 4 bytes      | 09 00 00 00 : 8bpp flag |  |  |  |
| 0x08                                            | 4 bytes      | Unknown                 |  |  |  |
| 0x0c                                            | 2 bytes      | CLUT Location X         |  |  |  |
| 0x0e                                            | 2 bytes      | CLUT Location Y         |  |  |  |
| 0x10                                            | 2 bytes      | Unknown                 |  |  |  |
| 0x12                                            | 2 Bytes      | Number Of CLUT entries  |  |  |  |
| 0x14                                            | 512 bytes    | CLUT Data               |  |  |  |
|                                                 | per CLUT     |                         |  |  |  |
|                                                 | (256 colors) |                         |  |  |  |
|                                                 |              | After the CLUT data     |  |  |  |
| +0x00                                           | 4 bytes      | Unknown                 |  |  |  |
| +0x04                                           | 2 bytes      | VRAM Location X         |  |  |  |
| +0x06                                           | 2 bytes      | VRAM Location Y         |  |  |  |
| +0x08                                           | 2 bytes      | Image Width / 2         |  |  |  |
| +0x10                                           | 2 bytes      | Image Height            |  |  |  |
| +0x12                                           | Texture data | See below               |  |  |  |
| Within the Texture data, each byte contains one |              |                         |  |  |  |

Within the Texture data, each byte contains one pixel, with each value corresponding to a color index with 256 entries loaded by the CLUT data.

[1][2][3][4].....

#### 16 Bits Per Pixel

| Offset | Size    | Description               |
|--------|---------|---------------------------|
| 0x00   | 4 bytes | 10 00 00 00 : TIM ID      |
| 0x04   | 4 bytes | 02 00 00 00 : 16bpp flag. |
| 0x08   | 4 bytes | Unknown                   |
| 0x0c   | 2 bytes | VRAM Location X           |

| Offset                                                                                                    | Size    | Description             |  |  |  |  |  |
|-----------------------------------------------------------------------------------------------------------|---------|-------------------------|--|--|--|--|--|
| 0x0e                                                                                                      | 2 bytes | VRAM Location Y         |  |  |  |  |  |
| 0x10                                                                                                      | 2 bytes | Image Width             |  |  |  |  |  |
| 0x12                                                                                                      | 2 bytes | Image Height            |  |  |  |  |  |
| 0x14                                                                                                      | Varies  | Texture data. See below |  |  |  |  |  |
| This texture data is stored with 1 pixel per<br>every two bytes. It's a in BGR format with<br>a mask bit. |         |                         |  |  |  |  |  |
| [ggg[rrrrr][m][bbbbb]gg]                                                                                  |         |                         |  |  |  |  |  |

#### **2.2 TEX Texture Data Format for PC by Mirix**

FF7 PC texture consists of header, an optional palette and bitmap data. Usually data are stored like palletized picture, with bitmap pixels referencing to palette. Color 0 (in palette its usually black) is usually used as transparent color.

Sometimes, (I'm not sure if it is used in ff7 at all), when bit depth is 16 data are stored as packed RGB in style RGB555, which means 5 bits per color in one 2 byte entry.

| Offset | Size                                                                                    | Description                                                                                                                                                                                                      |
|--------|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x00   | 56 bytes                                                                                | Unknown                                                                                                                                                                                                          |
| 0x38   | 4 bytes (long)                                                                          | bit depth - can be 4, 8, 16                                                                                                                                                                                      |
| 0x3c   | 4 bytes (long)                                                                          | Image Width                                                                                                                                                                                                      |
| 0x40   | 4 bytes (long)                                                                          | Image Height                                                                                                                                                                                                     |
| 0x44   | 20 bytes                                                                                | Unknown                                                                                                                                                                                                          |
| 0x58   | 4 bytes (long)                                                                          | Number of Palette Entries                                                                                                                                                                                        |
| 0x5c   | 144 bytes                                                                               | Unknown                                                                                                                                                                                                          |
| 0xec   | Palette Entries * 4                                                                     | Every 4 bytes from palette<br>represent one color, BGRA -<br>Blue Green Red Alpha, but I'm<br>not sure about the alpha byte. I'm<br>using only the BGR part                                                      |
|        |                                                                                         | After the Palette data                                                                                                                                                                                           |
| Varies | (sizex * sizey) if<br>bit depth is 4 or 8,<br>(sizex * sizey * 2)<br>if bit depth is 16 | The bitmap: If bit depth is 4 or 8,<br>every byte of bitmap data is<br>reference to palette color.<br>If bit depth is 16, bitmap is<br>composed from 16bit (2byte,<br>short) values, which are<br>RGB555 colors. |

#### **3. File formats for 3D models**

During the development process, 3D models contain a good deal of information needed by the artist every time they save or load the model. When the model is finished, it is often exported and broken up into smaller files with many unneeded attributes striped from them. When the models for FF7 were created, they were exported into Psy-Q's 3D resource data (RSD) files, polygon data (PLY), polygon groups (GRP), materials (MAT), textures (TIM), skeletal hierarchy (HRC), and animation (ANM).

The models are handled differently between modules. The models in the "battle" modules have a different animation system than the field models. When the models were converted to the PC version, they were converted from Psy-Q to a more PC-friendly format, some even involving plain text.

#### **3.1 Model Formats for PSX**

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

#### **3.2 Model Formats for PC**

The PC models are stored in the LGP files in the /DATA directory. The names for the models were obfuscated a little, but can be recovered via the plain text Hierarchy (HRC) and resource data (RSD) files.

#### **3.2.1 HRC Hierarchy data format for PC by Alhexx**

"HRC? What's this?" Well, that's a file which contains info about the skeleton of a FF7 Field Character (from char.lgp), Battle Models use another Format. To be more exact, it's not a Skeleton, but only a "HieRarChy" File...

But I think that since you read this document, you've got some knowledge 'bout 3D models and skeletons. Let's just start, this format's quite simple! ^\_^

1. "HRC-File-Look-A-Like-Contest" or: How does a HRC file look like? Since the HRC files are simple plain-text files, you can open them in notepad or any other text editor. Here are the first four bones of "abjb.hrc" (Yuffie's Hierarchy, continued on next page)

```
:HEADER_BLOCK 2
:SKELETON
sd_yufi_sk
:BONES 24
hip
root
2.9662
1 ABJC
chest
hip
4.0621967
1 ABJE
head
chest
5.017107
1 ACAA
joint
head
3.5236073
0 
ribon_a
joint
8.52051
1 ACAF
....
```

The other bones look the same as the ones I've listed here.Okay, let's see what we've got here...

#### 2. Header

As most files, also the HRC files have got a kind of header. That are the first three lines.

```
:HEADER_BLOCK 2
```

Don't ask what this is... it seems to be a simple "ID". As far as I know, this is the first line in all HRCs...

```
:SKELETON sd_yufi_sk
```

This tells you the name of the skeleton, in our example "sd\_yufi\_sk".

:BONES 24

Tells you how much bones are stored in this skeleton.

#### 3. Bones

Every bone consist of 4 Lines, which look like this. Let's first take a look at the lines of the first bone:

hip root 2.9662 1 ABJC

First Line: ("hip")

This is the name of the current bone.

Second Line: ("root")

This is the name of the parent bone. The parent bone must be already listed above in the skeleton file, or it can be "root" (origin).

Third Line: ("2.9662")

That's the Length of the bone.

Fourth Line #1: ("0")

Fourth Line #2: ("1 ABJC")

Fourth Line #3: ("2 ABJC ABJD")

This line consist of 2 or more different values. First, there is a number telling you how many RSD files are aligned to this model. If it has no RSD File, the number is 0. If the number is 1, there is a string after the number telling you the name of the Resource Data File (RSD). The RSD file tells you which . p Model is to use.

There may be even more than 2 RSD Files on 1 Bone, however, I haven't seen such a file... i

#### 4. Notes

You might wonder that there are no bone angles, just bone lengths? Well, like I said, ther HRC file aren't skeletons, they're a hierarchy. If you want to build up a skeleton, you'll have to read out the .a files, too!

Well, erm ... that's it! Simple, huh?

#### **3.2.2 RSD Resource Data Format for PC by Alhexx**

The RSD files (I think RSD stands for "Resource Data") contain some useful info for a FF7 Field Model. I don't wanna talk too much, let's see how it looks like. Oh, and they're plain text files as the HRC files.

This is "acaa.rsd", the RSD File for Yuffie's Head:

```
@RSD940102
# Output by SGI RSD fileset library libRsdObj.
PLY=ACAB.PLY
MAT=ACAB.MAT
GRP=ACAB.GRP
# Texture files
NTEX=3
TEX[0]=ACAC.TIM
TEX[1]=ACAD.TIM
TEX[2]=ACAE.TIM
```

The first line seems to be an ID. It is always the following.

```
@RSD940102
```

[Ed note: 940102 appears to be a date. January 2nd, 1994, three years previous to the FF7 release?]

The Second line is a comment. Every line beginning with "#" is ignored by the engine.

```
# Output by SGI RSD fileset library libRsdObj.
```

The next line tells you the Polygon Mesh File (.p Model) for this model.

PLY=x

This is the Material File for this Model.

```
MAT=x
```

The Group file..

GRP=x

You might wonder why "PLY", "MAT" and "GRP" ? Well, I wonder, too. All RSD files I have seen had the same file for "PLY", "MAT" and "GRP", since this info is all stored in the .p File...

The next line is telling how many textures this model uses. Usually it is 0, and there are no more lines. However, in our example it is 3, and there are 3 textures in here.

```
NTEX=x
```

In the last section you can see an array telling you the filenames for the textures. However, if you want to have the "real" filename, you'll have to replace "TIM" by "TEX" "ACAC.TIM" --> "ACAC.TEX"

```
TEX[x]=y
```

#### **3.2.3 "P" Polygon File Format by Alhexx, (With help from Ficedula, and Mirex)**

#### Introduction by Alhexx

First I've got to say that this description contains parts of Ficedula's and mirex' descriptions, but I don't think they've got anything against that I use them...

Okay, I'm not going to explain the basics of Polygon and 3D models like Fice. If you don't know what a polygon is, you should close this file.

I've also got to say, that this file will be updated and there may be a lot of bugs in it, but I think if you're trying to hack the .p format, it's going to be useful.

Oh, and I'm using Hex-Offsets, too. I will explain values this way: 0x80 The lengths are in decimal (as in Fice's description)

One thing, before I begin: This file can be 'split' into 2 parts: The First part (1.x) describes how the File is build together. The Second part (2.x) describes how the model is split into different Groups.

#### Preface: General File Structure

Here's a short diagram of the file structure

```
.p-File
 |
 +- Header
 |
 +- Vertices[]
 |
 (+- Normals[])
 |
 (+- Texture Coords[])
 |
 +- Vertice Colors[]
 |
 +- Polygon Colors[]
 |
 +- Edges[]
 |
 +- Polygons[]
 |
 +- Hundrets[]
 |
 +- Groups[]
 |
 +- BoundingBox
 |
 +- Normal Index Table[]
[] = a variable-sized array
```

#### 1.1 .P File Header

The .p files have a 128-Byte-long Header. We know 'till know to decode the first 64 Bytes. Perhaps the other 64 Bytes aren't really a header, perhaps they're a part of data. Dunno. Here's what I know:

(You should know that from a hex-editor)

| Off | 00         | 01 | 02                   | 03 | 04       | 05 | 06      | 07       | 08          | 09 | 0a       | 0b          | 0c | 0d | 0e | 0f |
|-----|------------|----|----------------------|----|----------|----|---------|----------|-------------|----|----------|-------------|----|----|----|----|
| 00  | 01         | 00 | 00                   | 00 | 01       | 00 | 00      | 00       | VertexColor |    | NumVerts |             |    |    |    |    |
| 10  | NumNormals |    |                      | 00 | 00       | 00 | 00      | NumTexCs |             |    |          | NumNormInds |    |    |    |    |
| 20  |            |    | NumEdges             |    | NumPolys |    | 00      | 00       | 00          | 00 | 00       | 00          | 00 | 00 |    |    |
| 30  |            |    | mirex_h<br>NumGroups |    |          |    | mirex_g |          |             |    | 01       | 00          | 00 | 00 |    |    |

All Values, that can be Read out in this part of the header are 4-Byte-Integers

```
typedef struct
{
    long off00;
    long off04;
    long VertexColor;
    long NumVerts;
    long NumNormals;
    long off14;
    long NumTexCs;
    long NumNormInds;
    long NumEdges;
    long NumPolys;
    long off28;
    long off2c;
    long mirex_h;
    long NumGroups;
    long mirex_g;
    long off3c;
    long unknown[16];
} t_p_header;
```

#### Here are the meanings:

| VertexColor | Specifies if Vertex-Colors are used (0=no,1=yes; default: 1) |
|-------------|--------------------------------------------------------------|
| NumVerts    | Count of Vertices                                            |
| NumNormals  | Count of Normals (always 0 in Battle files)                  |
| NumTexCs    | Count of Texture Coords                                      |
| NumNormInds | Count of Normal Indices                                      |
| NumEdges    | Count of Lines for WireFrame-Model                           |
| NumPolys    | Count of Polygons                                            |

| VertexColor | Specifies if Vertex-Colors are used (0=no,1=yes; default: 1) |
|-------------|--------------------------------------------------------------|
| mirex_h     | Count of Hundrets Chunk Entries (Textures?)                  |
| NumGroups   | Count of Groups                                              |
| mirex_g     | ? (sometimes 0 or 1)(but usually 1)                          |

All the other values, which are mostly the same, are used, too, but I don't know for what. If you change one of these 1 in the header, FF7 will crash. I've tried it.

#### P File Construction

Here's written down, how the parts of the .p file are put together. There are 11 Parts after the Header, in which the .p file can be split: IMPORTANT: This Part of this documentation shows only how the structures look like and how they have to be interpreted. How a .p Model is build up from these parts is written in Chapter II.

#### 1.2. Vertex Chunk

Okay, now I'm going to tell you what I know about the vertex Chunk:

| Start Offset | Length        |
|--------------|---------------|
| 0x80         | NumVerts * 12 |

Here's how it is put together: Additional + Numverts are the count of the vertexes saved in the .p file. Every Vertex consists of 12 Bytes, 4 for each coord (X/Y/Z). Every coord is a 4-Byte Float

#### The C/C++ Struct:

```
typedef struct
{
    float x;
    float y;
    float z;
} t_p_vertex;
```

NOTE: Of course, you could also use a simple Array with 3 elements, one element for every coordinate, but I like that X, Y, Z thingy :P

#### 1.3 Normals Chunk

| Start Offset           | Length          |
|------------------------|-----------------|
| 0x80 + (NumVerts * 12) | NumNormals * 12 |

#### 1.4 Texture Coordinate Chunk

| Start Offset                        | Length       |
|-------------------------------------|--------------|
| 0x80 + (NumVerts + NumNormals * 12) | NumTexCs * 8 |

These are the Texture coordinates. They're build up similar to the Vertex type, just with 2 elements:

#### C/C++:

```
typedef struct
{
    float x;
    float y;
} t_p_texturecoord;
```

X and Y are the offsets on the texture relative to the texture size. The values can between 0.0 and 1.0. So if a TexCoord has X = 0 and Y = 0, it is in the upper left corner, if it has X = 1 and Y = 1 it is in the lower right corner (or at least I hope so...)

Sometimes, the values may be even higher than 1.0. In that case, i.e. 1.3 is the same as 0.3. So if a value exceeds 1.0, simply subtract 1.0 from it.

#### 1.5 Vertex Color Chunk

| Start Offset                                         | Length       |
|------------------------------------------------------|--------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) | NumVerts * 4 |

That are the Color Values. Every Vertex has its own Vertex Color. They're saved as 4 x 1-Byte-Integers (a.c.:Byte). The Values are saved in a 'standard RGB-QUAD':

```
typedef struct
{
     unsigned char blue;
     unsigned char green;
     unsigned char red;
     unsigned char
reserved;
} t_p_color;
```

#### 1.6 Polygon Color Chunk

| Start Offset                                                        | Length       |
|---------------------------------------------------------------------|--------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) + NumVerts * 4 | NumPolys * 4 |

As every Vertex has its own Color, every Polygon also has its own. The Type/Struct is the same as in I.V

#### 1.7 Edge Chunk

| Start Offset                                                                        | Length       |
|-------------------------------------------------------------------------------------|--------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) +<br>(NumVerts + NumPolys) * 4 | NumEdges * 4 |

The Edge Chunk consists of a couple of 2-Byte Integers. The Edge Chunk saves the Wireframe model of the model. Every Entry is one line of the Model.

#### C/C++:

```
typedef struct
{
    short vertex[2];
} t_p_edge;
```

#### 1.8 Polygon Chunk

| Start Offset                                                                                   | Length        |
|------------------------------------------------------------------------------------------------|---------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) +<br>(NumVerts + NumPolys + NumEdges) * 4 | Numpolys * 24 |

As you can see, every polygon consists of 24-Bytes. I'm first going to explain the Type...

```
typedef struct
{
    short Tag1;
    short Vertex[3];
    short Normal[3];
    short Edge[3];
    long Tag2;
} t_p_polygon;
```

Now I'm going to explain what I know 'bout the parts:

## Tag1

| Tag1      | Unknown, but always 0                              |
|-----------|----------------------------------------------------|
| Vertex[*] | Vertex * for the polygon                           |
| Normal[*] | Normal* for the polygon (always 0 in Battle Files) |
| Edge[*]   | Edge * for WireFrame-Model                         |
| Tag2      | Unknown, but always \$0C FC EA 00                  |

Note: The Normal Indices are absolute, not related to the Group!

#### 1.9 Hundrets Chunk

| Start Offset                                                                                                    | Length        |
|-----------------------------------------------------------------------------------------------------------------|---------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) +<br>(NumVerts + NumPolys + NumEdges) * 4 + (NumPolys * 24 | mirex-h * 100 |

I don't really know what is stored here, but I suppose it has to do with the textures... well, dunno. In the C/C++ Struct, there is the info how this struct is usually filled. So if you want to create a new Hundrets Entry, you should use these values. Here is the (very long) type:

#### C/C++:

```
typedef struct
{ // 1st 2nd 3rd
    long off00; // 0x00000001
    long off04; // 0x00000001
    char off08; // 0x00
    char off09; // 0x82 0x86 0x86
    short off0a; // 0x0003
    char off0c; // 0x02
    char off0d; // 0x00 0x04 0x04
    short off0e; // 0x0002
    long off10; // 0x00000000 0x00000000 0x00000001
    long off14; // 0x00000000
    long off18; // 0x00000000 0x00000001 0x00000001
    long off1c; // 0x00000000 0x00000025 0x00000025
    char off20; // 0x00 x00 x40 x80 x00 x40 x80
    char off21; // 0x00 0x78 0x78
    short off22; // 0x0000
    long off24; // 0x00000002 0x00000001 0x00000001
    long off28; // 0xFFFFFFFF
    long off2c; // 0x00000000
    long off30; // 0x00000000
    long off34; // 0x00000002 0x00000005 0x00000005
    long off38; // 0x00000001 0x00000006 0x00000006
    long off3c; // 0x00000002
    long off40; // 0x00000000
    long off44; // 0x00000004 0x00000000 0x00000000
    long off48; // 0x00000000
    long off4c; // 0x00000000
    long off50; // 0x00000000
    long off54; // 0x00000000
    long off58; // 0x00000000
    long off5c; // 0x000000FF 0x00000080 0x00000080
    long off60; // 0x00000000
} t_p_hundrets;
```

1st, 2nd and 3rd tells you how the \* Hundrets Chunk looks like.Here are some ideas:

| Index of Texture(?) | Width/Height (?) |
|---------------------|------------------|
| off18               | off5c            |

#### 1.10 Group Chunk

| Start Offset                                                                                                                        | Length         |
|-------------------------------------------------------------------------------------------------------------------------------------|----------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) +<br>(NumVerts + NumPolys + NumEdges) * 4 + (NumPolys * 24) +<br>Mirex-H * 100 | NumGroups * 56 |

I was hacking quite long, to find out how this Chunk's calculated...

After looooooong time of hacking I finally found out for what this Chunk is good for... it's a Group Chunk. It divides the .p Model into several Parts.

```
typedef struct
{
   long polyType;
   long offPoly;
   long numPoly;
   long offVert;
   long numVert;
   long offEdge;
   long numEdge;
   long off18; // 0
   long off1c; // 0
   long off20; // 0
   long off24; // 0
   long offTex;
   long texFlag;
   long texID;
} t_p_group;
```

#### Explanation:

polyType:

Specifies the Polygon Type for this Group:

- 1 nontextured Polygons
- 2 textured Polygons with normals
- 3 textured Polygons without normals

#### offPoly:

The First Polygon used in this Group

numPoly:

Number of Polygons used in this Group

offVert:

see above

numVert:

see above

offEdge:

The First Edge used in this Group

numEdge:

see below

offTex:

The first Texture Coord used in this Group

texFlag:

Texture Flag:

- 0 No texture on this Group
- 1 Textured

texID:

Index of Texture (see below)

Now it's gettin' more complicated... The numEdge value is usually 0. So if you want to know how many Edges are used in Chunk i, then you'll have to see the offEdge in Chunk i+1 and get the difference ... blabla ... ahhh, take a look at this:

```
t_fiftysix[i].numEdge = t_fiftysix[i+1].offEdge - t_fiftysix[i].offEdge
```

BUT: If you want to get the numEdge for the LAST Group, then, of course, you'll have to do this:

```
t_fiftysix[i].numEdge = t_header.NumEdges - t_fiftysix[i].offEdge
```

I hope you know what I mean.

NOTE: If you're going to generate you own Groups, you CAN save the numEdge values to the struct; FF7 won't crash.

As for the texID entry:

In Field files, this is the Index used by the RSD Files.

In Battle files it \*should\* be like this:

(Example: Yuffie: RX\*\*)

- 1 rxac
- 2 rxad
- 3 rxae

...

#### 1.11 BoundingBox

| Start Offset                                                                                                                                                 | Length |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) +<br>(NumVerts + NumPolys + NumEdges) * 4 + (NumPolys * 24) +<br>(Mirex-H * 100) + (NumGroups * 56) + 4 | 24     |

This is the model's bounding box.

```
typedef struct
{
    float max_x;
    float max_y;
    float max_z;
    float min_x;
    float min_y;
    float min_z;
} t_p_boundingbox;
```

- OR maybe even better: -

```
typedef struct
{
    t_p_vertex max;
    t_p_vertex min;
} t_p_boundingbox;
```

It can be simply generated by going through the whole Vertex Array and looking for values.

#### 1.12 Normal Index Table

| Start Offset                                                                                                                                                      | Length          |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| 0x80 + (NumVerts + NumNormals) * 12 + (NumTexCs * 8) +<br>(NumVerts + NumPolys + NumEdges) * 4 + (NumPolys * 24) +<br>(Mirex-H * 100) + (NumGroups * 56) + 4 + 24 | NumNormInds * 4 |

Heh, it took me a long time top hack these values, too! But it's quite simple! This is just a normal index table! It's just an array of 32Bit integers. That means if you want to know which normal is used by vertex \*, you will have to take a look into that table.

```
So let's say:
NormalIndex[0] = 4
NormalIndex[1] = 7
NormalIndex[2] = 2
...
So the Vertex 0 uses Normal 4,
... Vertex 1 uses Normal 7,
... Vertex 2 uses Normal 2,
and so on...
```

#### 2. GROUPING

Since a part from the Group Chunk is decoded, we should now take a look at the Groups in the p File Format, since it isn't that easy. However, I hope I'm able to describe it understandably...

INFO: If you want to have a look at what I'm talking here, download Ultima 0.40 from my site, load a Model and click on let Ultima generate an Info file. Or take a look att two of them at: http://www.alhexx.com/fyuffie.txt http://www.alhexx.com/byuffie.txt

#### 2.1 General

Like I said, the p Model is split up into Groups. Usually only models which are textured have more than one group, but I'm sure that there are non-textured models which are grouped, too. Well, almost every part in the p File is split up into Groups, except the Header and, but this is not sure yet: Hundrets Chunk, Normals Chunk and Texture Coordinates . I'm sure that the Tex Coordinates ARE grouped, too, but I haven't found any Grouping behavior yet. Since I don't have enough time to check that now, I will do that later and update this document.

There is something unusual about the Groups in the p Format. Usually, in a model there is, to keep it simple, only a Vertex, a Polygon and a Group Chunk. There are let's say 4 Verts and 2 Polygons in 2 Groups. Now every Polygon point to the absolute Vertex index, not the index of the Vertex within this Group... let me guess, you don't have an idea what I'm talking about, huh? So here's a small "image" to demonstrate it.

#### STEP 1:

Here we've got a basic "Model":

![](_page_49_Figure_2.jpeg)

Here are 5 Vertices, numerated from 1 to 5:

(I used 2 Coordinates per vertex, since this document is 2D and not 3D)

| Vert | X  | Y  |
|------|----|----|
| 1    | 1  | 0  |
| 2    | 0  | -1 |
| 3    | 0  | 0  |
| 4    | 0  | 1  |
| 5    | -1 | 0  |

...and we've got 4 Polygons from P to S:

| Poly | Vertex1 | Vertex2 | Vertex3 |
|------|---------|---------|---------|
| P    | 1       | 2       | 3       |
| Q    | 2       | 3       | 4       |
| R    | 3       | 2       | 5       |
| S    | 3       | 5       | 4       |

I think this is easy to understand.

#### STEP 2:

Now we've got to add something that isn't sooo important, but I will need this in STEP 4. We'll get some names for those Polygon lines (Edges).

![](_page_50_Figure_2.jpeg)

You see, we'ge got 8 Lines.

| Line | V1 | V2 |
|------|----|----|
| a    | 1  | 2  |
| b    | 1  | 3  |
| c    | 1  | 5  |
| d    | 2  | 3  |
| e    | 3  | 4  |
| f    | 2  | 5  |
| g    | 3  | 5  |
| h    | 4  | 5  |

#### STEP 3:

Now let's divide the model into 2 Groups:

 1 /|\ a.b~c /.P|Q~\ /...|~~~\ 2-d--3--e-4 \...|~~~/ \.R|S~/ f.g~h \|/ 5

The Vertex Coords and Polygon Indices are the same as in STEP 1. But we've got 2 Groups now:

DOT-Group:

Vertices: 1, 2, 3, 5 Polygons: P, R Lines: a, b, d, f, g

TILDE-Group:

Vertices: 1, 3, 4, 5 Polygons: Q, S Lines: b, c, e, g, h

That's the way a "normal" Model Format would group the Model. The Group tells you that it uses these Vertices, Polygons and Lines.

## STEP 4:

But now the p Format isn't a "normal" Format :-| I think Square wanted to create a riddle for us hackers... ;)

The FF7 engine will "violently" rip this model into 2 DIFFERENT groups...

Every Vertex and Edge, that is used by both Groups, will be "cloned", so every Group is independent from each other. Now the Indices of the Polygons and Lines will have to be corrected...

#### 4.1 DOT-Group:

![](_page_51_Picture_10.jpeg)

#### 4.2 TILDE-Group:

1 |\ a-b |P \ | \ 2--c-3 | / |Q / d-e |/ 4

As you can see, every Group now has its own Indices for Vertices, Polygons and Lines. But there is only 1 Vertex Chunk, 1 Polygon Chunk and 1 Edge Chunk in the p Model...

So let's now draw both Groups at once:

(I've had to let space between the two groups, in fact the Vertices 1 and 5 are on excatly the same coords...)

#### 4.3 ABSOLUTE INDICES:

![](_page_52_Figure_4.jpeg)

So every Vertex, Polygon and Edge can be "called" in 2 ways; By its absolute Index and its Index within the Group. Here's a listing:

| Absolute | DOT | TILDE |
|----------|-----|-------|
| 1        | 1   | -     |
| 2        | 2   | -     |
| 3        | 3   | -     |
| 4        | 4   | -     |
| 5        | -   | 1     |
| 6        | -   | 2     |
| 7        | -   | 3     |
| 8        | -   | 4     |
| a        | a   | -     |
| b        | b   | -     |
| c        | c   | -     |
| d        | d   | -     |
| e        | e   | -     |
| f        | -   | a     |
| g        | -   | b     |
| h        | -   | c     |

| Absolute | DOT | TILDE |
|----------|-----|-------|
| i        | -   | d     |
| j        | -   | e     |
| P        | P   | -     |
| Q        | Q   | -     |
| R        | -   | P     |
| S        | -   | Q     |

In other Words: Vertex 1 of the DOT-Group is Vertex 1 in the (absolute) Vertex Chunk, and Vertex 1 of the TILDE-Group is Vertex 5 in the (abs.) Vertex Chunk. The Same Thing it with the Polygons and Edges.

#### STEP 5:

Now, in the FF7 p Format, there is another "problem".

Take a look at the TILDE-Group in Image 4.2 and 4.3 Do you see it?

Let's take Polygon P from 4.2. It is Polygon R in 4.3.

But that's not the problem. The Problem is that in 4.2 the Polygon uses Vertices 1, 2 and 3 (from this Group) and in 4.3, the Polygon uses Vertices 5, 6 and 7. In 4.2 the Polygon consists of the Lines a, b and c, in 4.3 it consists of f, g and h.

This is the way the Indices are handled in the FF7 p format. So in the Vertex Chunk there are all vertices of Group 1 first, then all of Group 2 and so on. So, if you want to add a Vertex to Group 1, you will have to correct the Vertex Offset of Group 2, 3, ...

#### NOTE:

You can now take a look at those Ultima Info Files to see what I mean. Scroll throught the file until you reach the end of the Polygon Chunk. The Indices of the Vertices and Edges rise and rise, but then, suddenly, they start from 0 again. This is where a new group begins.

There is another problem, which is, at least in my opinion, totally unlogical. In the same file, scroll down (or up) to the end of the Edges Chunk. And? Hm ... you won't see any groups there.

#### IMPORTANT:

This is because the Edges Chunk hold the ABSOLUTE Vertex Indices, not the Group-Ones !!!

So if you want to add a Vertex to Group 1, you will not only have to correct the Edges offset, but also the Vertex Indices in the Edges of Group 2.


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

<!-- EXTRACTED FROM MAJOR SECTION: 03_KERNEL.md lines 124-544 (421 lines) -->
<!-- Added 2025-11-28 to provide comprehensive binary format specifications for KERNEL.BIN sections -->
<!-- Source: FF7 Game Engine PDF documentation merged with individual file content -->

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

<!-- END EXTRACTION FROM 03_KERNEL.md -->

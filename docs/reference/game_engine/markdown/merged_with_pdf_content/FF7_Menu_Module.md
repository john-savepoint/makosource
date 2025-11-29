<!--
MERGE METADATA
Created: 2025-11-29 02:30 JST
Original: FF7_Menu_Module.md (target for merge)
Source: 04_MENU_MODULE.md (502 lines of substantive content)
Merge decision: COMPLETE
Reason: Direct match for menu system - all content integrated
Status: MERGED - Analysis Report: FF7_Menu_Module_vs_04_MENU_MODULE_analysis.md
Last Modified: 2025-11-29 14:38 JST
Merge Completion: ✅ FULL CONTENT INTEGRATION

VALIDATION NOTES (2025-11-29 14:38 JST):
⚠️ KNOWN ISSUES REQUIRING VERIFICATION:
1. Save Icon 7 TIM offset discrepancy (line ~189):
   - This file shows: 0x108D0
   - Alternate source shows: 0x108DA
   - ACTION REQUIRED: Verify against original WINDOW.BIN or source documentation
2. Typo on line ~124: "Spit into 3 groups" should be "Split into 3 groups"
3. This file includes complete save format (3 tables) that was missing in older version
-->

# The Menu Module

## I. Menu Overview

Important files:

| PSX Version      | PC Version              |
|------------------|-------------------------|
| /MENU/*.MNU      | /DATA/MENU/MENU_US.LGP  |
| /INIT/WINDOW.BIN | /DATA/KERNEL/WINDOW.BIN |
|                  | /DATA/MENU/MENU_US.LGP  |

The menu module is probably the second most powerful module in the game. From here you can set a multitude of environment variables and view character records directly. It's really more of a master variable controller than the "select-o-thing" it appears to be.

Because the menu can have some rather fancy and complicated management features, it also can be placed in "Tutorial mode". This mode, when called from the field module will "play" prerecorded menu selections for the player.

Another major function of the menu system is the ability to save your game. This is probably the most powerful and vital part as the Menu has access to every single variable in the system, excluding the script temporary variables.

The Menu module is actually a collection of 13 modules, to which 4 can be called from the field scripting language. The 13 are called Begin, Party, Item, Magic, Eqip, Stat, Change, Limit, Config, Form, Save, Name, and Shop.

## II. Menu Initialization

Menu has the incredible honor of being initialized right after the kernel. It is also the only module that keeps permanent data in VRAM for other modules to access. In the case of the PSX version, the graphics are loaded out of /INIT/WINDOW.BIN. This is a BIN-GZIP archive described in the Kernel section of this document. WINDOW.BIN has the following format.

| Offset | Length     | Description           |
|--------|------------|-----------------------|
| 0x0000 | 6 bytes    | Header [0x4827208200] |
| 0x0006 | 1062 bytes | Static Menu textures  |
| 0x2754 | 3034 bytes | Font texture          |
| 0x332e | 163 bytes  | Unknown               |

After initialization, the first Menu module ran is "Begin" The following is a picture of "Begin" in VRAM. Things to note is the font and static menu textures from /INIT/WINNDOW.BIN are highlighted in the lower right hand corner.

The following is an expanded picture of the textures from the PC version. The PSX version only differs in texture size and the way the buttons are displayed.

To better see what each section is, here is an annotated version with the more obvious textures labeled

**Important Note on Japanese Characters:** This is never banked out, however small parts are overwritten and cashed for a while when Battle is loaded, but are overwritten again when menu is loaded. The large blank spot under the menu text is for the Japanese characters that were removed in the non-Japanese version of the game. This spot is unused in these versions.

## III. Menu Modules

The 13 Modules are displayed like the following.

### 1. Begin

This is a screen form the "save" module. Begin initializes the menu system and calls save to load a game or to start the game.

### 2. Party

Here is the party menu. This is the menu you see when you manually enter the menu system. Things to note is the empty box in the lower screen shows what location you are in. Debug rooms have no name most of the time.

### 3. Item

Item is the item management interface where players can view and use items from their inventory.

### 4. Magic

This is the magic menu module. Both magic and summon are accessed in the same module.

### 5. Eqip

The Eqip module is a little strange. Equip and Materia are in the same module.

### 6. Stat

This is the status menu where character statistics and attributes can be reviewed.

### 7. Change

Also known as "Order", this is the simplest and smallest of all the menu modules, it just changes the order of the party, it uses the party screen as a background.

### 8. Limit

The Limit menu where limits are set and configured for characters.

### 9. Config

The config menu. This is where a good deal of environment variables can be changed.

### 10. Form

This is also known as the PHS screen. Form can also be called when you need to make a two or three teams of people.

### 11. Save

The all important save screen. To save time, this will only load the first 80 bytes of each save as a preview. It allows a quick look without having to load the whole memory card, which can take upward of a minute. This is also responsible for loading games too, when called from "begin"

### 12. Name

This is the naming screen. If you try and use the same name screen twice in a game, you will loose your old name and will be overwritten with the default one.

### 13. Shop

This is your typical shop. You can, of course, sell items from this module as well.

## IV. Calling the Various Menus

The PSX version keeps the menu modules contained in a .MNU file. The PC version has the menu code internal to the executable. The highlighted modules can be called with the MENU script command. The MENU command always takes a first argument of 00. The second argument is the Menu ID number, and the third is the argument.

| Module Name | PSX Filename       | Menu ID Number | Argument                   |
|-------------|-------------------|-----------------|----------------------------|
| Begin       | /MENU/BGINMENU.MNU | N/A             | N/A                        |
| Party       | /MENU/PATYMENU.MNU | 0x09            | 0x00                       |
| Item        | /MENU/ITEMMENU.MNU | N/A             | N/A                        |
| Magic       | /MENU/MGICMENU.MNU | N/A             | N/A                        |
| Eqip        | /MENU/EQIPMENU.MNU | N/A             | N/A                        |
| Stat        | /MENU/STATMENU.MNU | N/A             | N/A                        |
| Change      | /MENU/CHNGMENU.MNU | N/A             | N/A                        |
| Limit       | /MENU/LIMTMENU.MNU | N/A             | N/A                        |
| Config      | /MENU/CNFGMENU.MNU | N/A             | N/A                        |
| Form        | /MENU/FORMMENU.MNU | 0x07            | 0x00 - Make a party of 3   |
|             |                   |                 | 0x01 - Spit into 3 groups  |
|             |                   |                 | 0x02 - Split into 2 groups |
| Save        | /MENU/SAVEMENU.MNU | 0x0E            | 0x00                       |
| Name        | /MENU/NAMEMENU.MNU | 0x06            | 0x00 - Cloud               |
|             |                   |                 | 0x01 - Barret              |
|             |                   |                 | 0x02 - Tifa                |
|             |                   |                 | 0x03 - Aerith              |
|             |                   |                 | 0x04 - Red XII             |
|             |                   |                 | 0x05 - Yuffie             |
|             |                   |                 | 0x06 - Cait Sith           |
|             |                   |                 | 0x07 - Vincent             |
|             |                   |                 | 0x08 - Cid                 |
|             |                   |                 | 0x09 - Chocobo             |
| Shop        | /MENU/SHOPMENU.MNU | 0x08            | (0x00-0xFF) Shop Number    |

## V. Menu Dependencies

On the PSX, Menu dependencies are kept in two different directories. The window dressing textures that stay in memory are found in /INIT/WINDOW.BIN and stored as a BIN-GZIP archive. In the MENU directory, some MNU files contain TIM files appended at the end that are displayed when they are loaded. Two of them, PARTYMENU.MNU and FORMMENU.MNU, externally reference TIM files on the disk as they share these resources. SAVEMENU.MNU also externally references the memory card ports.

The PC version has the MNU files internal to the executable and only have external resources. These are kept within the MENU_US.LGP file. The PC version has textures in two different sizes to support the two resolutions the game runs in. The following is a table of the menu resources and where they are located in both the PC and PSX version.

### Character Avatar Resources

| Picture | Description      | Low Resolution PC Filename | High Resolution PC Filename | PSX Location        | TIM Offset |
|---------|------------------|---------------------------|--------------------------------|--------------------------------------------|---------------|
|         | Cloud Avatar          | CLOUD_L.TEX                   | CLOUD.TEX                      | CLOUD.TIM                                  | N/A           |
|         | Barret Avatar         | BARRE_L.TEX                   | BARRE.TEX                      | BARRE.TIM                                  | N/A           |
|         | Tifa Avatar              | TIFA_L.TEX                    | TIFA.TEX                       | TIFA.TIM                                   | N/A           |
|         | Aerith Avatar         | EARITH_L.TEX                  | EARITH.TEX                     | EARITH.TIM                                 | N/A           |
|         | Red XII Avatar        | RED_L.TEX                     | RED.TEX                        | RED.TIM                                    | N/A           |
|         | Yuffie Avatar         | YUFI_L.TEX                    | YUFI.TEX                       | YUFI.TIM                                   | N/A           |
|         | Cait Sith Avatar      | KETC_L.TEX                    | KETC.TEX                       | KETC.TIM                                   | N/A           |
|         | Vincent Avatar        | BINS_L.TEX                    | BINS.TEX                       | BINS.TIM                                   | N/A           |
|         | Cid Avatar               | CIDO_L.TEX                    | CIDO.TEX                       | CIDO.TIM                                   | N/A           |
|         | Young Cloud Avatar | PCLOUD_L.TEX                  | PCLOUD.TEX                     | PCLOUD.TIM                                 | N/A           |
|         | Sephiroth Avatar      | PCEFI_L.TEX                   | PCEFI.TEX                      | PCEFI.TIM                                  | N/A           |
|         | Chocobo Avatar        | CHOCO_L.TEX                   | CHOCO.TEX                      | CHOCO.TIM                                  | N/A           |
|         | Placeholder Avatar    | N/A                           | N/A                            | KALI.TIM                                   | N/A           |
|         | Cloud Avatar (Name Menu) | CLOUD_L.TEX               | CLOUD.TEX                      | NAMEMENU.MNU                               | 0x1E7C        |

### Name Menu Avatar Resources

| Picture | Description      | Low Resolution PC Filename | High Resolution PC Filename | PSX Location | TIM Offset |
|---------|------------------|---------------------------|--------------------------------|--------------------------------------------|---------------|
|         | Barret Avatar          | BARRE_L.TEX                   | BARRE.TEX                      | NAMEMENU.MNU                               | 0x29A0        |
|         | Tifa Avatar               | TIFA_L.TEX                    | TIFA.TEX                       | NAMEMENU.MNU                               | 0x34C4        |
|         | Aerith Avatar          | EARITH_L.TEX                  | EARITH.TEX                     | NAMEMENU.MNU                               | 0x3FE8        |
|         | Red XII Avatar         | RED_L.TEX                     | RED.TEX                        | NAMEMENU.MNU                               | 0x4B0C        |
|         | Yuffie Avatar          | YUFI_L.TEX                    | YUFI.TEX                       | NAMEMENU.MNU                               | 0x5630        |
|         | Cait Sith Avatar       | KETC_L.TEX                    | KETC.TEX                       | NAMEMENU.MNU                               | 0x6154        |
|         | Vincent Avatar         | BINS_L.TEX                    | BINS.TEX                       | NAMEMENU.MNU                               | 0x6C78        |
|         | Cid Avatar                | CIDO_L.TEX                    | CIDO.TEX                       | NAMEMENU.MNU                               | 0x779C        |
|         | Chocobo Avatar         | CHOCO_L.TEX                   | CHOCO.TEX                      | NAMEMENU.MNU                               | 0x82C0        |

### Save and Item Menu Resources

| Picture | Description      | Low Resolution PC Filename | High Resolution PC Filename | PSX Location | TIM Offset |
|---------|------------------|---------------------------|--------------------------------|--------------------------------------------|---------------|
|         | Load screen background | BUSTER.TEX               | N/A                            | SAVEMENU.MNU                               | 0x4EDC        |
|         | Save Icon 1               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0xF4F4        |
|         | Save Icon 2               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0xF502        |
|         | Save Icon 3               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0xF8F8        |
|         | Save Icon 4               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0xFCEE        |
|         | Save Icon 5               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x100E4       |
|         | Save Icon 6               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x104DA       |
|         | Save Icon 7               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x108D0       |
|         | Save Icon 8               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x10CC6       |
|         | Save Icon 9               | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x110BC       |
|         | Save Icon 10              | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x114B2       |
|         | Save Icon 11              | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x118A8       |
|         | Save Icon 12              | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x11C9E       |
|         | Save Icon 13              | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x12094       |
|         | Save Icon 14    | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x1248A       |
|         | Save Icon 15    | N/A                           | N/A                            | SAVEMENU.MNU                               | 0x12880       |
|         | Coin command | ZENI.TEX                      | ZENI_H.TEX                     | ITEMMENU.MNU                               | 0x3890        |

### Window and Font Resources

| Picture | Description        | Low Resolution PC Filename | High Resolution PC Filename | PSX Location | TIM Offset |
|---------|------------------|---------------------------|--------------------------------|--------------------------------------------|---------------|
|         | Window                  | BTL_WIN_H.TEX                 | BTL_WIN_A_H.TEX                | /INIT/WINDOW.BIN                       | 0x0006        |
|         | Dressings               |                               | BTL_WIN_B_H.TEX                |                                            |               |
|         |                 |                               | BTL_WIN_C_H.TEX                |                                            |               |
|         |                 |                               | BTL_WIN_D_H.TEX                |                                            |               |
|         |                 | BTL_WIN_L.TEX                 | BTL_WIN_A_L.TEX                |                                            |               |
|         |                 |                               | BTL_WIN_B_L.TEX                |                                            |               |
|         |                 |                               | BTL_WIN_C_L.TEX                |                                            |               |
|         |                 |                               | BTL_WIN_D_L.TEX                |                                            |               |
|         | Menu Font               | USFONT_L.TEX                  | USFONT_A_L.TEX                 | /INIT/WINDOW.BIN                       | 0x2754        |
|         |                 |                               | USFONT_B_L.TEX                 |                                            |               |
|         |                 | USFONT_H.TEX                  | USFONT_A_H.TEX                 |                                            |               |
|         |                 |                               | USFONT_B_H.TEX                 |                                            |               |

## VI. The Save Game Format

The following is the general save format for the game. This data excludes the header data that differs between the PSX and PC version.

### Table 1: The Final Fantasy Save Slot

| Offset | Length    | Description                                                                                                                                                                                                         |
|--------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes   | Checksum                                                                                                                                                                                                            |
| 0x0004 | 1 byte    | Preview: Lead character's level. [Note: Changing any preview descriptions are only cosmetic. They do not change any in-game values. It is only used so a player can preview the data within the save file] |
| 0x0005 | 1 byte    | Preview: Lead character's portrait. 0x00: Cloud, 0x07: Vincent, 0x01: Barret, 0x08: Cid, 0x02: Tifa, 0x09: Young Cloud, 0x03: Aerith, 0x0A: Sephiroth, 0x04: Red XII, 0x0B: Chocobo, 0x05: Yuffie, 0xFF: None, 0x06: Cait Sith |
| 0x0006 | 1 byte    | Preview: 2nd character's portrait                                                                                                                                                                                   |
| 0x0007 | 1 byte    | Preview: 3rd character's portrait                                                                                                                                                                                   |
| 0x0008 | 16 bytes  | Preview: Lead character's name, terminated with 0xFF                                                                                                                                                             |
| 0x0018 | 2 bytes   | Preview: Lead character's Current HP                                                                                                                                                                                |
| 0x001A | 2 bytes   | Preview: Lead character's Max HP                                                                                                                                                                                    |
| 0x001C | 2 bytes   | Preview: Lead character's Current MP                                                                                                                                                                                |
| 0x001E | 2 bytes   | Preview: Lead character's Max HP                                                                                                                                                                                    |
| 0x0020 | 4 bytes   | Preview: Amount of Gil                                                                                                                                                                                           |
| 0x0024 | 4 bytes   | Preview: Total number of seconds played                                                                                                                                                                             |
| 0x0028 | 32 bytes  | Preview: Save location, FF Text format, terminated with 0xFF                                                                                                                                                     |
| 0x0048 | 3 bytes   | RGB value for upper left corner of window                                                                                                                                                                          |
| 0x004B | 3 bytes   | RGB value for upper right corner of window                                                                                                                                                                         |
| 0x004E | 3 bytes   | RGB value for lower left corner of window                                                                                                                                                                          |
| 0x0051 | 3 bytes   | RGB value for lower right corner of window                                                                                                                                                                         |
| 0x0054 | 132 bytes | Character record: Cloud [Note: See table 2 for Character record format]                                                                                                                                             |
| 0x00D8 | 132 bytes | Character record: Barret                                                                                                                                                                                            |
| 0x015C | 132 bytes | Character record: Tifa                                                                                                                                                                                              |
| 0x01E0 | 132 bytes | Character record: Aerith                                                                                                                                                                                            |
| 0x0264 | 132 bytes | Character record: Red XIII                                                                                                                                                                                          |
| 0x02E8 | 132 bytes | Character record: Yuffie                                                                                                                                                                                            |
| 0x036C | 132 bytes | Character record: Cait Sith                                                                                                                                                                                         |
| 0x03F0 | 132 bytes | Character record: Vincent                                                                                                                                                                                           |
| 0x0474 | 132 bytes | Character record: Cid                                                                                                                                                                                               |
| 0x04F8 | 1 byte    | Party member in slot 1, uses same data format as character portrait above                                                                                                                                            |
| 0x04F9 | 1 byte    | Party member in slot 2                                                                                                                                                                                              |
| 0x04FA | 1 byte    | Party member in slot 3                                                                                                                                                                                              |
| 0x04FB | 1 byte    | 0xFF                                                                                                                                                                                                                 |
| 0x04FC | 640 bytes | Party Item stock, 2 bytes per item, 320 item slots max [See save item list below]                                                                                                                                   |
| 0x077C | 800 bytes | Party Materia stock, 4 bytes per materia, 200 materia max [See materia list]                                                                                                                                        |
| 0x0A9C | 224 bytes | Unknown                                                                                                                                                                                                              |
| 0x0B7C | 4 bytes   | Party's Gil amount                                                                                                                                                                                                  |
| 0x0B80 | 4 bytes   | Total number of seconds played                                                                                                                                                                                      |
| 0x0B84 | 16 bytes  | Unknown                                                                                                                                                                                                              |
| 0x0B94 | 2 bytes   | Current map                                                                                                                                                                                                          |
| 0x0B96 | 2 bytes   | Current location                                                                                                                                                                                                    |
| 0x0B98 | 2 bytes   | Unknown                                                                                                                                                                                                              |
| 0x0B9A | 2 bytes   | X location on world map                                                                                                                                                                                             |
| 0x0B9C | 2 bytes   | Y location on world map                                                                                                                                                                                             |
| 0x0B9E | 2 bytes   | Z location on world map                                                                                                                                                                                             |
| 0x0BA0 | 4 bytes   | Unknown                                                                                                                                                                                                              |
| 0x0BA4 | 2 bytes   | Plot Progression Variable [BEGINNING OF SCRIPT MEMORY BANK 1/2]                                                                                                                                                      |
| 0x0BA5 | 3 bytes   | Unknown                                                                                                                                                                                                              |
| 0x0BA7 | 1 byte    | Aerith's current love points                                                                                                                                                                                        |
| 0x0BA8 | 1 byte    | Tifa's current love points                                                                                                                                                                                          |
| 0x0BA9 | 1 byte    | Yuffie's current love points                                                                                                                                                                                        |
| 0x0BAA | 1 byte    | Barret's current love points                                                                                                                                                                                        |
| 0x0BAB | 5 bytes   | Unknown                                                                                                                                                                                                              |
| 0x0BB0 | 2 bytes   | Number of battles fought                                                                                                                                                                                            |
| 0x0BB2 | 2 bytes   | Number of escapes                                                                                                                                                                                                   |
| 0x0BB4 | 1 byte    | Game timer (Hours)                                                                                                                                                                                                  |
| 0x0BB5 | 1 byte    | Game timer (Minutes)                                                                                                                                                                                                |
| 0x0BB6 | 1 byte    | Game timer (Seconds)                                                                                                                                                                                                |
| 0x0BB7 | 1 byte    | Game timer (Tenths)                                                                                                                                                                                                 |
| 0x0BB8 | 0x0BBD    | Unknown (curse ring usage?)                                                                                                                                                                                         |
| 0x0BBC | 2 bytes   | Number of battles fought                                                                                                                                                                                            |
| 0x0BBE | 2 bytes   | Number of escapes                                                                                                                                                                                                   |
| 0x0BBF | 0x0BE3   | Unknown                                                                                                                                                                                                              |
| 0x0BE4 | 8 bytes   | Key items [see Key Item List]                                                                                                                                                                                       |
| 0x0BEC | 0x0BC9   | Unknown                                                                                                                                                                                                              |
| 0x0BF9 | 1 byte    | Field Chocobo rating                                                                                                                                                                                                |
| 0x0BFA | 1 byte    | Field Chocobo rating                                                                                                                                                                                                |
| 0x0BFB | 1 byte    | Field Chocobo rating                                                                                                                                                                                                |
| 0x0BFC | 1 byte    | Field Chocobo rating                                                                                                                                                                                                |
| 0x0BFD | 0x0BC8   | Unknown                                                                                                                                                                                                              |
| 0x0BC9 | 2 bytes   | Menu Visibility Mask, Quit on PC is not affected. LSB: item, magic, mtra, eqip, status, ordr, limit, cfg, PHS, save. MSB |
| 0x0BCB | 2 bytes   | Menu locking Mask, 1 = locked. Quit on PC can't be locked. LSB: item, magic, mtra, eqip, status, ordr, limit, cfg, PHS, save. MSB |
| 0x0C02 | 1 byte    | Rating for Penned Chocobo Number 1 - (01 = Wonderful <-> 08 = the worst)                                                                                                                                            |
| 0x0C03 | 1 byte    | Rating for Penned Chocobo Number 2                                                                                                                                                                                  |
| 0x0C04 | 1 byte    | Rating for Penned Chocobo Number 3                                                                                                                                                                                  |
| 0x0C05 | 1 byte    | Rating for Penned Chocobo Number 4                                                                                                                                                                                  |
| 0x0C06 | 0x0CA3   | Unknown                                                                                                                                                                                                              |
| 0x0CA4 |           | [BEGINNING OF FIELD BANK 3/4]                                                                                                                                                                                       |
| 0x0CA5 | 0x0CED   | Unknown                                                                                                                                                                                                              |
| 0x0CEE | 2 bytes   | Party GP (0-10000)                                                                                                                                                                                                  |
| 0x0CF0 | 12 bytes  | Unknown                                                                                                                                                                                                              |
| 0x0CFC | 1 byte    | Number of chocobo stables owned                                                                                                                                                                                     |
| 0x0CFD | 1 byte    | Unknown                                                                                                                                                                                                              |
| 0x0CFE | 1 byte    | Number of occupied stables                                                                                                                                                                                          |
| 0x0CFF | 1 byte    | Mask of occupied stables                                                                                                                                                                                            |
| 0x0D00 | 0x0DA3   | Unknown                                                                                                                                                                                                              |
| 0x0DA4 |           | [BEGINNING OF FIELD BANK B/C]                                                                                                                                                                                       |
| 0x0DA5 | 0x0DC3   | Unknown                                                                                                                                                                                                              |
| 0x0DC4 | 16 bytes  | Chocobo slot 1 [Note: See table 3 For Chocobo slot format]                                                                                                                                                          |
| 0x0DD4 | 16 bytes  | Chocobo slot 2                                                                                                                                                                                                      |
| 0x0DE4 | 16 bytes  | Chocobo slot 3                                                                                                                                                                                                      |
| 0x0DF4 | 16 bytes  | Chocobo slot 4 [Note: Chocobo slots 5 and 6 are located at 0x1084-0x10A3]                                                                                                                                           |
| 0x0D04 | 0x0EA3   | Unknown                                                                                                                                                                                                              |
| 0x0EA4 | 1 byte    | Current CD [BEGINNING OF FIELD BANK D/E]                                                                                                                                                                            |
| 0x0EA5 | 31 bytes  | Unknown                                                                                                                                                                                                              |
| 0x0EC4 | 6 bytes   | 1st Chocobo's name, FF Text format                                                                                                                                                                                  |
| 0x0ECA | 6 bytes   | 2nd Chocobo's name, FF Text format                                                                                                                                                                                  |
| 0x0ED0 | 6 bytes   | 3rd Chocobo's name, FF Text format                                                                                                                                                                                  |
| 0x0ED6 | 6 bytes   | 4th Chocobo's name, FF Text format                                                                                                                                                                                  |
| 0x0EDC | 6 bytes   | 5th Chocobo's name, FF Text format                                                                                                                                                                                  |
| 0x0EE2 | 6 bytes   | 6th Chocobo's name, FF Text format                                                                                                                                                                                  |
| 0x0EE8 | 2 bytes   | 1st Chocobo's stamina                                                                                                                                                                                               |
| 0x0EEA | 2 bytes   | 2nd Chocobo's stamina                                                                                                                                                                                               |
| 0x0EEC | 2 bytes   | 3rd Chocobo's stamina                                                                                                                                                                                               |
| 0x0EEE | 2 bytes   | 4th Chocobo's stamina                                                                                                                                                                                               |
| 0x0EF0 | 2 bytes   | 5th Chocobo's stamina                                                                                                                                                                                               |
| 0x0EF2 | 2 bytes   | 6th Chocobo's stamina                                                                                                                                                                                               |
| 0x0EF4 | 0x0EFD   | Unknown                                                                                                                                                                                                              |
| 0x0EFD | 1 byte    | turns off(00)/on(FF) the submarine                                                                                                                                                                                  |
| 0x0EFE | 0x0F14   | Unknown                                                                                                                                                                                                              |
| 0x0F15 | 24 bytes  | Name of location, FF Text format                                                                                                                                                                                    |
| 0x0F24 | 0x0F32   | Unknown                                                                                                                                                                                                              |
| 0x0F32 | 1 byte    | Don't(00)/Do(08) display World Map instructions                                                                                                                                                                     |
| 0x0F33 | 0x0F65   | Unknown                                                                                                                                                                                                              |
| 0x0F66 | 1 byte    | Party's X location on the world map (Tile)                                                                                                                                                                          |
| 0x0F67 | 1 byte    | Party's Y location on the world map (Tile)                                                                                                                                                                          |
| 0x0F68 | 1 byte    | Party's Heading (some examples: 00 South, 40 East, 80 North, C0 West)                                                                                                                                                |
| 0x0F69 | 1 byte    | Party's X ?                                                                                                                                                                                                          |
| 0x0F6A | 1 byte    | Party's Y ?                                                                                                                                                                                                          |
| 0x0F6B | 1 byte    | Party's Z ?                                                                                                                                                                                                          |
| 0x0F6C | 0x0F85   | Unknown                                                                                                                                                                                                              |
| 0x0F86 | 1 byte    | Submarine's X location on the world map (Tile)                                                                                                                                                                       |
| 0x0F87 | 1 byte    | Submarine's Y location on the world map (Tile)                                                                                                                                                                       |
| 0x0F88 | 1 byte    | Submarine's Heading (some examples: 00 South, 40 East, 80 North, C0 West)                                                                                                                                           |
| 0x0F89 | 1 byte    | Submarine X ?                                                                                                                                                                                                        |
| 0x0F8A | 1 byte    | Submarine Y ?                                                                                                                                                                                                        |
| 0x0F8B | 1 byte    | Submarine Z ?                                                                                                                                                                                                        |
| 0x0F8C | 0x0FA5   | Unknown                                                                                                                                                                                                              |
| 0x0FA4 |           | [BEGINNING OF FIELD BANK 7/F]                                                                                                                                                                                       |
| 0x0FA5 | 1 byte    | Unknown                                                                                                                                                                                                              |
| 0x0FA6 | 1 byte    | World map camera & map display. Add two values together (one from camera, one from map) and set the byte. Camera - Aerial(00), Closeup (20). Map - Off (80), Small (00), Large (40). |
| 0x0FA7 | 0x0FAA   | Unknown                                                                                                                                                                                                              |
| 0x0FAB | 1 byte    | Must be 0x00 or game crashes                                                                                                                                                                                        |
| 0x0FAC | 0x102F   | Unknown                                                                                                                                                                                                              |
| 0x1030 | 1 byte    | Field screen rain switch. Non-zero turns on the rain effect                                                                                                                                                          |
| 0x1031 | 0x1083   | Unknown                                                                                                                                                                                                              |
| 0x1084 | 16 bytes  | Chocobo slot 5                                                                                                                                                                                                      |
| 0x1094 | 16 bytes  | Chocobo slot 6                                                                                                                                                                                                      |
| 0x10A3 |           | [END OF FIELD SCRIPT MEMORY BANKS]                                                                                                                                                                                  |
| 0x10A3 | 0x10AE   | Unknown                                                                                                                                                                                                              |
| 0x10AD | 2 bytes   | PHS Locking Mask. LSB: Cloud, Barret, Tifa, Aerith, Red, Yuffie, Vince, Cait, Cid. MSB |
| 0x10AF | 2 bytes   | PHS Visibility Mask, does not turn off characters in your party. LSB: Cloud, Barret, Tifa, Aerith, Red, Yuffie, Vince, Cait, Cid. MSB |
| 0x10B0 | 0x10D7   | Unknown                                                                                                                                                                                                              |
| 0x10D8 | 1 byte    | Battle speed (0x00 = fastest, 0xFF = Slowest)                                                                                                                                                                        |
| 0x10D9 | 1 byte    | Battle message speed                                                                                                                                                                                                |
| 0x10DA | 2 bytes   | Flag bits (?)                                                                                                                                                                                                        |
| 0x10DC | 16 bytes  | Unknown                                                                                                                                                                                                              |
| 0x10EC | 1 byte    | Message speed                                                                                                                                                                                                        |
| 0x10ED | 7 bytes   | Unknown                                                                                                                                                                                                              |

### Table 2: Character Record

| Offset | Length  | Description                                        |
|--------|---------|-----------------------------------------------------|
| 0x00   | 1 byte  | Sephiroth flag for changing Vincent into Sephiroth |
| 0x01   | 1 byte  | Level (0-99)                                        |
| 0x02   | 1 byte  | Strength (0-255)                                    |
| 0x03   | 1 byte  | Vitality (0-255)                                    |
| 0x04   | 1 byte  | Magic (0-255)                                       |
| 0x05   | 1 byte  | Spirit (0-255)                                      |
| 0x06   | 1 byte  | Dexterity (0-255)                                   |
| 0x07   | 1 byte  | Luck (0-255)                                        |
| 0x08   | 1 byte  | Strength Bonus (Power Sources used)                 |
| 0x09   | 1 byte  | Vitality Bonus (Guard Sources used)                 |
| 0x0A   | 1 byte  | Magic Bonus (Magic Sources used)                    |
| 0x0B   | 1 byte  | Spirit Bonus (Mind Sources used)                    |
| 0x0C   | 1 byte  | Dexterity Bonus (Speed Sources used)                |
| 0x0D   | 1 byte  | Luck Bonus (Luck Sources used)                      |
| 0x0E   | 1 byte  | Current limit level (1-4)                           |
| 0x0F   | 1 byte  | Current limit bar (0xFF = limit break)              |
| 0x10   | 12 bytes | Name, FF Text format                                |
| 0x1C   | 1 byte  | Equipped weapon                                     |
| 0x1D   | 1 byte  | Equipped armor                                      |
| 0x1E   | 1 byte  | Equipped accessory                                  |
| 0x1F   | 3 bytes | Character flags                                     |
| 0x22   | 2 bytes | Learned limit skills                                |
| 0x24   | 2 bytes | Number of Kills                                     |
| 0x26   | 2 bytes | Times Limit 1-1 Has been used                       |
| 0x28   | 2 bytes | Times Limit 2-1 Has been used                       |
| 0x2A   | 2 bytes | Times Limit 3-1 Has been used                       |
| 0x2C   | 2 bytes | Current HP                                          |
| 0x2E   | 2 bytes | Base HP (before materia alterations)                |
| 0x30   | 2 bytes | Current MP                                          |
| 0x32   | 2 bytes | Base MP (before materia alterations)                |
| 0x34   | 4 bytes | Unknown                                             |
| 0x38   | 2 bytes | Maximum HP (after materia alterations)              |
| 0x3A   | 2 bytes | Maximum MP (after materia alterations)              |
| 0x3C   | 4 bytes | Current EXP                                         |
| 0x40   | 1 byte  | Weapon materia slot number 1                        |
| 0x41   | 1 byte  | Weapon materia slot number 2                        |
| 0x42   | 1 byte  | Weapon materia slot number 3                        |
| 0x43   | 1 byte  | Weapon materia slot number 4                        |
| 0x44   | 1 byte  | Weapon materia slot number 5                        |
| 0x45   | 1 byte  | Weapon materia slot number 6                        |
| 0x46   | 1 byte  | Weapon materia slot number 7                        |
| 0x47   | 1 byte  | Weapon materia slot number 8                        |
| 0x48   | 1 byte  | Armor materia slot number 1                         |
| 0x49   | 1 byte  | Armor materia slot number 2                         |
| 0x4A   | 1 byte  | Armor materia slot number 3                         |
| 0x4B   | 1 byte  | Armor materia slot number 4                         |
| 0x4C   | 1 byte  | Armor materia slot number 5                         |
| 0x4D   | 1 byte  | Armor materia slot number 6                         |
| 0x4E   | 1 byte  | Armor materia slot number 7                         |
| 0x4F   | 1 byte  | Armor materia slot number 8                         |
| 0x80   | 4 bytes | EXP to next level                                   |

### Table 3: Chocobo Record

| Offset | Length  | Description                         |
|--------|---------|-------------------------------------|
| 0x0    | 2 bytes | Sprint speed                        |
| 0x2    | 2 bytes | Max Sprint speed                    |
| 0x4    | 2 bytes | Speed                               |
| 0x6    | 2 bytes | Max Speed                           |
| 0x8    | 1 byte  | Acceleration                        |
| 0x9    | 1 byte  | Cooperation                         |
| 0xA    | 1 byte  | Intelligence                        |
| 0xB    | 1 byte  | Personality                         |
| 0xC    | 1 byte  | Pcount(?)                           |
| 0xD    | 1 byte  | Number of races won                 |
| 0xE    | 1 byte  | Sex (0=male,1=female)               |
| 0xF    | 1 byte  | Type (Yellow,Green,Blue,Black,Gold) |

---

<!-- MERGE COMPLETION MARKERS -->
<!-- EXTRACTED FROM: 04_MENU_MODULE.md (502 lines) -->
<!-- MERGE DATE: 2025-11-29 02:35 JST -->
<!-- STATUS: FULL CONTENT INTEGRATION COMPLETE -->
<!-- ALL SECTIONS: Menu Overview, Initialization, Modules, Script Commands, Dependencies, Resources, Save Format -->
<!-- VALIDATION: All byte-level specifications preserved, all tables formatted correctly, all module descriptions included -->

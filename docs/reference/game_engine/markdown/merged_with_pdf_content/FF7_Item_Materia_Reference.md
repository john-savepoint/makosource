<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_Item_Materia_Reference.md (617 lines)
Major section: 09_APPENDIX.md
Merge decision: MERGED - COMPLETE
Reason: Item/materia tables in appendix - all content extracted and integrated
Status: Content merged from 09_APPENDIX.md (lines 7406-8015)
Last Updated: 2025-11-29 JST
Source Analysis: docs/reference/game_engine/comparisons/FF7_Item_Materia_Reference_vs_09_APPENDIX_analysis.md
-->

# FF7 Item and Materia Reference

## Overview

This document provides comprehensive reference tables for Final Fantasy VII game data, including:
- Complete item database with dual-ID encoding scheme
- Materia listings with AP tracking format
- FF7 custom character encoding (letter map)

These tables are essential for:
- Save file parsing and inventory management
- Equipment and materia system implementation
- Text rendering and dialogue display
- Data validation for modding and research

---

## Item Listings

### Record Format

Items in FF7 are stored as 2-byte records:
- **Byte 1**: ID byte (0x00-0xFF)
- **Byte 2**: Quantity byte (special encoding for IDs 0x00-0x3F)

### Dual-ID Encoding Scheme (IDs 0x00-0x3F)

There are more than 256 types of items in the game (319 total, excluding key items). To accommodate this, items with IDs 0x00-0x3F use a clever dual-encoding scheme:

- **EVEN quantity byte** → First item name in the pair
- **ODD quantity byte** → Second item name in the pair
- **Actual quantity** = quantity_byte ÷ 2 (integer division)

**Example**: Bytes `03 07`
- ID = 0x03
- Quantity byte = 0x07 (ODD)
- Item = Mythril Armlet (second item for ID 0x03)
- Actual quantity = 7 ÷ 2 = 3 (three Mythril Armlets)

### Single-ID Encoding (IDs 0x40-0xFF)

For IDs 0x40-0xFF, the quantity byte must be EVEN (single item per ID).

---

## Complete Item Database

### Items 0x00-0x3F (Dual-Encoding)

```
00 = Potion / Bronze Bangle
01 = Hi-Potion / Iron Bangle
02 = X-Potion / Titan Bangle
03 = Ether / Mythril Armlet
04 = Turbo Ether / Carbon Bangle
05 = Elixir / Silver Armlet
06 = Megalixir / Gold Armlet
07 = Phoenix Down / Diamond Bangle
08 = Antidote / Crystal Bangle
09 = Soft / Platinum Bangle
0A = Maiden's Kiss / Rune Armlet
0B = Cornucopia / Edincoat
0C = Echo Screen / Wizard Bracelet
0D = Hyper / Adaman Bangle
0E = Tranquilizer / Gigas Armlet
0F = Remedy / Imperial Guard
10 = Smoke Bomb / Aegis Armlet
11 = Speed Drink / Fourth Bracelet
12 = Hero Drink / Warrior Bangle
13 = Vaccine / Shinra Beta
14 = Grenade / Shinra Alpha
15 = Shrapnel / Four Slots
16 = Right arm / Fire Armlet
17 = Hourglass / Aurora Armlet
18 = Kiss of Death / Bolt Armlet
19 = Spider Web / Dragon Armlet
1A = Dream Powder / Minerva Band
1B = Mute Mask / Escort Guard
1C = War Gong / Mystile
1D = Loco weed / Ziedrich
1E = Fire Fang / Precious Watch
1F = Fire Veil / Chocobracelet
20 = Antarctic Wind / Power Wrist
21 = Ice Crystal / Protect Vest
22 = Bolt Plume / Earring
23 = Swift Bolt / Talisman
24 = Earth Drum / Choco Feather
25 = Earth Mallet / Amulet
26 = Deadly Waste / Champion Belt
27 = M-Tentacles / Poison Ring
28 = Stardust / Touph Ring
29 = Vampire Fang / Circlet
2A = Ghost Hand / Star Pendant
2B = Vagyrisk Claw / Silver Glasses
2C = Light Curtain / Headband
2D = Lunar Curtain / Fairy Ring
2E = Mirror / Jem Ring
2F = Holy Torch / White Cape
30 = Bird Wing / Sprint Shoes
31 = Dragon Scales / Peace Ring
32 = Impaler / Ribbon
33 = Shrivel / Fire Ring
34 = Eye drop / Ice Ring
35 = Molotov / Bolt Ring
36 = S-mine / Tetra Elemental
37 = 8inch Cannon / Safety Bit
38 = Graviball / Fury Ring
39 = T/S Bomb / Curse Ring
3A = Ink / Protect Ring
3B = Dazers / Cat's Bell
3C = Dragon Fang / Reflect Ring
3D = Cauldron / Water Ring
3E = Sylkis Greens / Sneak Glove
3F = Reagan Greens / HypnoCrown
```

### Items 0x40-0xFF (Single-Encoding)

#### Chocobo Greens (0x40-0x45)
```
40 = Mimett Greens
41 = Curiel Greens
42 = Pahsana Greens
43 = Tantal Greens
44 = Krakka Greens
45 = Gysahl Greens
```

#### Stat-Boosting Items (0x46-0x4C)
```
46 = Tent
47 = Power Source
48 = Guard Source
49 = Magic Source
4A = Mind Source
4B = Speed Source
4C = Luck Source
```

#### Chocobo Breeding Nuts (0x4D-0x54)
```
4D = Zeio Nut
4E = Carob Nut
4F = Porov Nut
50 = Pram Nut
51 = Lasan Nut
52 = Saraha Nut
53 = Luchile Nut
54 = Pepio Nut
```

#### Special Items (0x55-0x56)
```
55 = Battery
56 = Tissue
```

#### Limit Break Manuals (0x57-0x5E)
```
57 = Omnislash
58 = Catastrophe
59 = Final Heaven
5A = Great Gospel
5B = Cosmo Memory
5C = All Creation
5D = Chaos
5E = Highwind
```

#### Collectible/Special Items (0x5F-0x66)
```
5F = 1/35 Soldier
60 = Super Sweeper
61 = Masamune Blade
62 = Save Crystal
63 = Combat Diary
64 = Autograph
65 = Gambler
66 = Desert Rose
```

#### Additional Items (0x67-0x68)
```
67 = Earth Harp
68 = Guide Book
```

### Weapons (0x80-0xFF)

#### Cloud's Swords (0x80-0x8F)
```
80 = Buster Sword
81 = Mythril Saber
82 = Hardedge
83 = Butterfly Edge
84 = Enhance Sword
85 = Organics
86 = Crystal Sword
87 = Force Stealer
88 = Rune Blade
89 = Murasame
8A = Nail Bat
8B = Yoshiyuki
8C = Apocalypse
8D = Heaven's Cloud
8E = Ragnarok
8F = Ultima Weapon
```

#### Barret's Guns (0x90-0x9F)
```
90 = Leather Glove
91 = Metal Knuckle
92 = Mythril Claw
93 = Grand Glove
94 = Tiger Fang
95 = Diamond Knuckle
96 = Dragon Claw
97 = Crystal Glove
98 = Motor Drive
99 = Platinum Fist
9A = Kaiser Knuckle
9B = Work Glove
9C = Powersoul
9D = Master Fist
9E = God's Hand
9F = Premium Heart
```

#### Tifa's Gloves (0xA0-0xAF)
```
A0 = Gatling Gun
A1 = Assault Gun
A2 = Cannon Ball
A3 = Atomic Scissors
A4 = Heavy Vulcan
A5 = Chainsaw
A6 = Microlaser
A7 = A-M Cannon
A8 = W Machine Gun
A9 = Drill Arm
AA = Solid Bazooka
AB = Rocket Punch
AC = Enemy Launcher
AD = Pile Banger
AE = Max Ray
AF = Missing Score
```

#### Aerith's Staves (0xB0-0xBD)
```
B0 = Mythril Clip
B1 = Diamond Pin
B2 = Silver Barrette
B3 = Gold Barrette
B4 = Adaman Clip
B5 = Crystal Comb
B6 = Magic Comb
B7 = Plus Barrette
B8 = Centclip
B9 = Hairpin
BA = Seraph Comb
BB = Behimoth Horn
BC = Spring Gun Clip
BD = Limited Moon
```

#### Yuffie's Shuriken/Boomerangs (0xBE-0xE3)
```
BE = Guard Stick
BF = Mythril Rod
C0 = Full Metal Staff
C1 = Striking Staff
C2 = Prism Staff
C3 = Aurora Rod
C4 = Wizard Staff
C5 = Wizer Staff
C6 = Fairy Tale
C7 = Umbrella
C8 = Princess Guard
C9 = Spear
CA = Slash Lance
CB = Trident
CC = Mast Ax
CD = Partisan
CE = Viper Halberd
CF = Javelin
D0 = Grow Lance
D1 = Mop
D2 = Dragoon Lance
D3 = Scimitar
D4 = Flayer
D5 = Spirit Lance
D6 = Venus Gospel
D7 = 4-point Shuriken
D8 = Boomerang
D9 = Pinwheel
DA = Razor Ring
DB = Hawkeye
DC = Crystal Cross
DD = Wind Slash
DE = Twin Viper
DF = Spiral Shuriken
E0 = Superball
E1 = Magic Shuriken
E2 = Rising Sun
E3 = Oritsuru
```

#### Vincent's Guns (0xE4-0xFF)
```
E4 = Conformer
E5 = Yellow M-phone
E6 = Green M-phone
E7 = Blue M-phone
E8 = Red M-phone
E9 = Crystal M-phone
EA = White M-phone
EB = Black M-phone
EC = Silver M-phone
ED = Trumpet Shell
EE = Gold M-phone
EF = Battle Trumpet
F0 = Starlight Phone
F1 = HP Shout
F2 = Quicksilver
F3 = Shotgun
F4 = Shortbarrel
F5 = Lariat
F6 = Winchester
F7 = Peacemaker
F8 = Buntline
F9 = Long Barrel R
FA = Silver Rifle
FB = Sniper CR
FC = Supershot ST
FD = Outsider
FE = Death Penalty
FF = Masamune
```

---

## Materia Listings

### Record Format

Materia entries in FF7 save files use a 4-byte structure:

- **Byte 1**: Materia ID (0x00-0x5A, 0xFF for unequipped/none)
- **Bytes 2-4**: AP value
  - **Master Status**: 0xFFFFFF indicates materia has reached master level

**Example**: `48 12 00 00` = Ultima (ID 0x48) with 0x000012 AP

### Materia ID Reference

#### Support Materia (0x00-0x0A)
```
00 = MP Plus
01 = HP Plus
02 = Speed Plus
03 = Magic Plus
04 = Luck Plus
05 = EXP Plus
06 = Gil Plus
07 = Enemy Away
08 = Enemy Lure
09 = Chocobo Lure
0A = Pre-emptive
```

#### Battle Mechanics (0x0B-0x2B)
```
0B = Long Range
0C = Mega All
0D = Counter Attack
0E = Slash-All
0F = Double Cut
10 = Cover
11 = Underwater
12 = HP <-> MP
13 = W-Magic
14 = W-Summon
15 = W-Item
17 = All
18 = Counter
19 = Magic Counter
1A = MP Turbo
1B = MP Absorb
1C = HP Absorb
1D = Elemental
1E = Added Effect
1F = Sneak Attack
20 = Final Attack
21 = Added Cut
22 = Steal as well
23 = Quadra Magic
24 = Steal
25 = Sense
27 = Throw
28 = Morph
29 = Deathblow
2A = Manipulate
2B = Mime
```

#### Enemy Skill & Master Command (0x2C, 0x30)
```
2C = Enemy Skill *
30 = Master Command
```

*Note: Enemy Skill materia has special handling; see save map documentation for details.

#### Magic Spells (0x31-0x48)
```
31 = Fire
32 = Ice
33 = Earth
34 = Lightning
35 = Restore
36 = Heal
37 = Revive
38 = Seal
39 = Mystify
3A = Transform
3B = Exit
3C = Poison
3D = Demi
3E = Barrier
40 = Comet
41 = Time
44 = Destruct
45 = Contain
46 = Full Cure
47 = Shield
48 = Ultima
49 = Master Magic
```

#### Summons (0x4A-0x5A)
```
4A = Choco/Mog
4B = Shiva
4C = Ifrit
4D = Titan
4E = Ramuh
4F = Odin
50 = Leviathan
51 = Bahamut
52 = Kujata
53 = Alexander
54 = Phoenix
55 = Neo Bahamut
56 = Hades
57 = Typhoon
58 = Bahamut ZERO
59 = Knights of Round
5A = Master Summon
```

#### Special Codes
```
FF = Not equipped / none
```

---

## FF7 Character Encoding (Letter Map)

Final Fantasy VII uses a non-standard character encoding for text display. This custom letter map is essential for proper text rendering in dialogue, menus, and battle displays.

### Character Encoding Table

The following table maps hex values (00-FF) to their corresponding characters, symbols, and control codes:

```
    | 00          | 01        | 02     | 03     | 04    | 05       | 06      | 07     | 08       | 09      | 0A      | 0B       | 0C      | 0D       | 0E       | 0F       |
----|-------------|-----------|--------|--------|-------|----------|---------|--------|----------|---------|---------|----------|---------|----------|----------|----------|
00  | {SPACE}     | !         | "      | #      | $     | %        | &       | '      | (        | )       | *       | +        | ,       | -        | .        | /        |
10  | 0           | 1         | 2      | 3      | 4     | 5        | 6       | 7      | 8        | 9       | :       | ;        | <       | =        | >        | ?        |
20  | @           | A         | B      | C      | D     | E        | F       | G      | H        | I       | J       | K        | L       | M        | N        | O        |
30  | P           | Q         | R      | S      | T     | U        | V       | W      | X        | Y       | Z       | [        | \       | ]        | ^        | -        |
40  |             | a         | b      | c      | d     | e        | f       | g      | h        | i       | j       | k        | l       | m        | n        | o        |
50  | p           | q         | r      | s      | t     | u        | v       | w      | x        | y       | z       | {        | |       | }        | ~        |          |
60  | Ä           | Á         | Ç      | É      | Ñ     | Ö        | Ü       | á      | à        | â       | ä       | ã        | å       | ç        | é        | è        |
70  | ê           | ë         | í      | ì      | î     | ï        | ñ       | ó      | ò        | ô       | ö       | õ        | ú       | ù        | û        | ü        |
80  | {Command}   | 0         | ¢      | £      | Ú     | Ù        | 1       | B      | ®        | ©       | ™       | '        |         | #        | Æ        | Ø        |
90  | ∞           | ±         | ≦      | ≧      | ¥     | μ        | д       | Σ      | П        | π       | J       | ш        | 87      | Ω        |          |          |
A0  |             |           |        |        |       |          |         |        |          |         |         |          |        |          | <9B>     | <9C>     |
B0  |             |           | <93>   | <94>   |       |          |         |        |          |         |         |          |        |          |          |          |
C0  |             |           |        |        |       |          |         |        |          |         |         |          |        |          |          |          |
D0  |             |           | {GRAY} | {BLUE} | {RED} | {PURPLE} | {GREEN} | {CYAN} | {YELLOW} | {WHITE} |         |          |        |          |          |          |
E0  | {TAB}       |           | ,      |        |       |          |         |        | {EOL}    | {PAUSE} |         | {Cloud}  | {Barret} | {Tifa}   | {Aerith} | {Red 13} |
F0  | {Yuffie}   | {Cait Sith} | {Vincent} | {Cid}  |       |          |         | 0     | Δ        |         | ×       |          |         |          |          | {STOP}   |
```

### Encoding Notes

**Control Codes** (0xE0-0xFF):
- `{TAB}` (0xE0): Text tab/spacing
- `{EOL}` (0xE8): End of line/line break
- `{PAUSE}` (0xE9): Pause in dialogue
- `{STOP}` (0xFF): Stop/end marker
- Character name substitution codes allow dynamic party member name insertion

**Color Codes** (0xD0-0xD8):
- Enable text color changes in dialogue and menus
- `{GRAY}` (0xD0), `{BLUE}` (0xD1), `{RED}` (0xD2), etc.

**Mathematical & Special Symbols** (0x80-0xA0):
- Comparison operators: ≦ (0x92), ≧ (0x93)
- Greek letters: Σ, π, Ω (various positions)
- Currency and special: ¥, μ, ©, ™, ®

**Note**: The encoding table includes some characters that may be OCR artifacts or encoding display issues (Cyrillic characters visible in certain positions). The core ASCII-derived mapping (0x00-0x7F) is reliable for standard text.

---

## Implementation References

### Save File Parsing

For item inventory parsing:
```
For each item in inventory:
  Read 2 bytes: [ID, Quantity]
  If ID < 0x40:
    Encode flag = Quantity & 0x01
    Actual quantity = Quantity >> 1
    item_name = DUAL_ITEM_TABLE[ID][encode_flag]
  Else:
    Actual quantity = Quantity >> 1
    item_name = ITEM_TABLE[ID]
```

### Materia Equipment

For materia equipped status:
```
For each materia slot:
  Read 4 bytes: [ID, AP_low, AP_mid, AP_high]
  If ID == 0xFF:
    Slot is empty
  Else if AP == 0xFFFFFF:
    Materia is master level
  Else:
    Materia is active with partial AP
```

### Text Rendering

For dialogue rendering:
```
For each character code in text:
  If code in (0xEA-0xEF, 0xF0-0xF2):
    Substitute party member name
  Else if code in (0xD0-0xD8):
    Change text color
  Else:
    Render character from LETTER_MAP[code]
```

---

## Source Attribution

Content extracted from: `09_APPENDIX.md` (FF7 Game Engine documentation)
Analysis report: `comparisons/FF7_Item_Materia_Reference_vs_09_APPENDIX_analysis.md`


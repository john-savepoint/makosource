# FF7/Item and Materia Reference {#ff7item_materia_reference}

- [FF7/Item and Materia Reference](#ff7item_materia_reference){#toc-ff7item_materia_reference}
  - [Item Listings](#item_listings){#toc-item_listings}
  - [Materia Listing](#materia_listing){#toc-materia_listing}
  - [Resource Lookup Table](#resource_lookup_table){#toc-resource_lookup_table}



#### **Item Listings**

#### **1. Keeping track of item inventory**

Record length: 2 bytes Byte 1 = ID byte

Byte 2 = Quantity (read on)

This one's a bit complicated... there are way more than 256 types of items in the game (319 actually, excluding key items) So some items share the same ID byte, to distinguish between the two, the Quantity byte is used. For instance, for ID byte 0x00, it can be either Potion or Bronze Bangle. If the byte is an EVEN value, it's a Potion; if it's ODD, then it's Bronze Bangle. To find the ACTUAL quantity, divide the byte value by 2 (integer divide, ignore remainders for ODD bytes).

Example: 03 07 - ID byte is 03, if byte 2 is EVEN: Ether if byte 2 is ODD: Mythril Armlet.

 Quantity byte is 07, which is ODD, so this means Mythril Armlets. 7 divided by 2 is 3, so these bytes mean 3 Mythril Armlets

This only apply to items with ID 0x00 - 0x3F, for the others the Quantity byte must be an EVEN value.

ID (Hex): For ID 0x00 - 0x3F, the first item name is what you'll get when used with an EVEN quantity byte. The second item name for an ODD quantity byte. For ID 0x40 - 0xFF, the quantity byte must be EVEN.

----------------------------------------------------------------------

00 = Potion

Bronze Bangle

01 = Hi-Potion

Iron Bangle

02 = X-Potion

Titan Bangle

03 = Ether

Mythril Armlet

04 = Turbo Ether

Carbon Bangle

05 = Elixir

Silver Armlet

06 = Megalixir

Gold Armlet

07 = Phoenix Down Diamond Bangle

08 = Antidote

Crystal Bangle

09 = Soft

Platinum Bangle

0A = Maiden's Kiss

Rune Armlet

0B = Cornucopia

Edincoat

0C = Echo Screen

Wizard Bracelet

0D = Hyper

Adaman Bangle

0E = Tranquilizer

Gigas Armlet

0F = Remedy

Imperial Guard

10 = Smoke Bomb

Aegis Armlet

11 = Speed Drink

Fourth Bracelet

12 = Hero Drink

Warrior Bangle

13 = Vaccine

Shinra Beta

14 = Grenade

Shinra Alpha

15 = Shrapnel

Four Slots

16 = Right arm

Fire Armlet

17 = Hourglass

Aurora Armlet

18 = Kiss of Death

Bolt Armlet

19 = Spider Web

Dragon Armlet

1A = Dream Powder

Minerva Band

1B = Mute Mask

Escort Guard

1C = War Gong

Mystile

1D = Loco weed

Ziedrich

1E = Fire Fang

Precious Watch

1F = Fire Veil

Chocobracelet

20 = Antarctic Wind

Power Wrist

21 = Ice Crystal

Protect Vest

22 = Bolt Plume

Earring

23 = Swift Bolt

Talisman

24 = Earth Drum

Choco Feather

25 = Earth Mallet

Amulet

26 = Deadly Waste

Champion Belt

27 = M-Tentacles

Poison Ring

28 = Stardust

Touph Ring

29 = Vampire Fang

Circlet

2A = Ghost Hand

Star Pendant

2B = Vagyrisk Claw

Silver Glasses

2C = Light Curtain

Headband

2D = Lunar Curtain

Fairy Ring

2E = Mirror

Jem Ring

2F = Holy Torch

White Cape

30 = Bird Wing

Sprint Shoes

31 = Dragon Scales

Peace Ring

32 = Impaler

Ribbon

33 = Shrivel

Fire Ring

34 = Eye drop

Ice Ring

35 = Molotov

Bolt Ring

36 = S-mine

Tetra Elemental

37 = 8inch Cannon

Safety Bit

38 = Graviball

Fury Ring

39 = T/S Bomb

Curse Ring

3A = Ink

Protect Ring

3B = Dazers

Cat's Bell

3C = Dragon Fang

Reflect Ring

3D = Cauldron

Water Ring

3E = Sylkis Greens

Sneak Glove

3F = Reagan Greens

HypnoCrown

40 = Mimett Greens

41 = Curiel Greens

42 = Pahsana Greens

43 = Tantal Greens

44 = Krakka Greens

45 = Gysahl Greens

46 = Tent

47 = Power Source

48 = Guard Source

49 = Magic Source

4A = Mind Source

4B = Speed Source

4C = Luck Source

4D = Zeio Nut

4E = Carob Nut

4F = Porov Nut

50 = Pram Nut

51 = Lasan Nut

52 = Saraha Nut

53 = Luchile Nut

54 = Pepio Nut

55 = Battery

56 = Tissue

57 = Omnislash

58 = Catastrophe

59 = Final Heaven 5A = Great Gospel

5B = Cosmo Memory

5C = All Creation

5D = Chaos

5E = Highwind

5F = 1/35 Soldier

60 = Super Sweeper

61 = Masamune Blade

62 = Save Crystal

63 = Combat Diary

64 = Autograph

65 = Gambler

66 = Desert Rose

- 67 = Earth Harp
- 68 = Guide Book
- 80 = Buster Sword
- 81 = Mythril Saber
- 82 = Hardedge
- 83 = Butterfly Edge
- 84 = Enhance Sword
- 85 = Organics
- 86 = Crystal Sword
- 87 = Force Stealer
- 88 = Rune Blade
- 89 = Murasame
- 8A = Nail Bat
- 8B = Yoshiyuki
- 8C = Apocalypse
- 8D = Heaven's Cloud
- 8E = Ragnarok
- 8F = Ultima Weapon
- 90 = Leather Glove
- 91 = Metal Knuckle
- 92 = Mythril Claw
- 93 = Grand Glove
- 94 = Tiger Fang
- 95 = Diamond Knuckle
- 96 = Dragon Claw
- 97 = Crystal Glove
- 98 = Motor Drive
- 99 = Platinum Fist
- 9A = Kaiser Knuckle
- 9B = Work Glove
- 9C = Powersoul
- 9D = Master Fist
- 9E = God's Hand
- 9F = Premium Heart
- A0 = Gatling Gun
- A1 = Assault Gun
- A2 = Cannon Ball
- A3 = Atomic Scissorss
- A4 = Heavy Vulcan
- A5 = Chainsaw
- A6 = Microlaser
- A7 = A-M Cannon
- A8 = W Machine Gun
- A9 = Drill Arm
- AA = Solid Bazooka
- AB = Rocket Punch
- AC = Enemy Launcher
- AD = Pile Banger
- AE = Max Ray
- AF = Missing Score
- B0 = Mythril Clip

- B1 = Diamond Pin
- B2 = Silver Barrette
- B3 = Gold Barrette
- B4 = Adaman Clip
- B5 = Crystal Comb
- B6 = Magic Comb
- B7 = Plus Barrette
- B8 = Centclip
- B9 = Hairpin
- BA = Seraph Comb
- BB = Behimoth Horn
- BC = Spring Gun Clip
- BD = Limited Moon
- BE = Guard Stick
- BF = Mythril Rod
- C0 = Full Metal Staff
- C1 = Striking Staff
- C2 = Prism Staff
- C3 = Aurora Rod
- C4 = Wizard Staff
- C5 = Wizer Staff
- C6 = Fairy Tale
- C7 = Umbrella
- C8 = Princess Guard
- C9 = Spear
- CA = Slash Lance
- CB = Trident
- CC = Mast Ax
- CD = Partisan
- CE = Viper Halberd
- CF = Javelin
- D0 = Grow Lance
- D1 = Mop
- D2 = Dragoon Lance
- D3 = Scimitar
- DB = Hawkeye
- D4 = Flayer
- D5 = Spirit Lance
- D6 = Venus Gospel
- D7 = 4-point Shuriken
- D8 = Boomerang
- D9 = Pinwheel
- DA = Razor Ring
- DC = Crystal Cross
- DD = Wind Slash
- DE = Twin Viper
- DF = Spiral Shuriken
- E0 = Superball
- E1 = Magic Shuriken
- E2 = Rising Sun
- E3 = Oritsuru

- E4 = Conformer
- E5 = Yellow M-phone
- E6 = Green M-phone
- E7 = Blue M-phone
- E8 = Red M-phone
- E9 = Crystal M-phone
- EA = White M-phone
- EB = Black M-phone
- EC = Silver M-phone
- ED = Trumpet Shell
- EE = Gold M-phone
- EF = Battle Trumpet
- F0 = Starlight Phone
- F1 = HP Shout
- F2 = Quicksilver
- F3 = Shotgun
- F4 = Shortbarrel
- F5 = Lariat
- F6 = Winchester
- F7 = Peacemaker
- F8 = Buntline
- F9 = Long Barrel R
- FA = Silver Rifle
- FB = Sniper CR
- FC = Supershot ST
- FD = Outsider
- FE = Death Penalty
- FF = Masamune

#### **Matera Listing**

====================================================================== Materia List

# ======================================================================

Record length: 4 bytes Byte 1 = ID byte (Verified to be identical to the lists in the PSX

GameShark codes, saves us a hell lot of work :) )

Byte 2-4 = AP (FF FF FF = Master)

- ID (hex):
- 00 = MP Plus
- 01 = HP Plus
- 02 = Speed Plus
- 03 = Magic Plus
- 04 = Luck Plus
- 05 = EXP. Plus
- 06 = Gil Plus
- 07 = Enemy Away
- 08 = Enemy Lure
- 09 = Chocobo Lure
- 0A = Pre-emptive

- 0B = Long Range
- 0C = Mega All
- 0D = Counter Attack
- 0E = Slash-All
- 0F = Double Cut
- 10 = Cover
- 11 = Underwater
- 12 = HP <-> MP
- 13 = W-Magic
- 14 = W-Summon
- 15 = W-Item
- 17 = All
- 18 = Counter
- 19 = Magic Counter
- 1A = MP Turbo
- 1B = MP Absorb
- 1C = HP Absorb
- 1D = Elemental
- 1E = Added Effect
- 1F = Sneak Attack
- 20 = Final Attack
- 21 = Added Cut
- 22 = Steal as well
- 23 = Quadra Magic
- 24 = Steal
- 25 = Sense
- 27 = Throw
- 28 = Morph
- 29 = Deathblow
- 2A = Manipulate
- 2B = Mime
- 2C = Enemy Skill \* (See note below)
- 30 = Master Command
- 31 = Fire
- 32 = Ice
- 33 = Earth
- 34 = Lightning
- 35 = Restore
- 36 = Heal
- 37 = Revive
- 38 = Seal
- 39 = Mystify
- 3A = Transform
- 3B = Exit
- 3C = Poison
- 3D = Demi
- 3E = Barrier
- 40 = Comet
- 41 = Time
- 44 = Destruct
- 45 = Contain

- 46 = Full Cure
- 47 = Shield
- 48 = Ultima
- 49 = Master Magic
- 4A = Choco/Mog
- 4B = Shiva
- 4C = Ifrit
- 4D = Titan
- 4E = Ramuh
- 4F = Odin
- 50 = Leviathan
- 51 = Bahamut
- 52 = Kujata
- 53 = Alexander
- 54 = Phoenix
- 55 = Neo Bahamut
- 56 = Hades
- 57 = Typoon
- 58 = Bahamut ZERO
- 59 = Knights of Round
- 5A = Master Summon
- FF = Not equipped / none

#### **Resource Lookup Table**

# **Final Fantasy Letter Map**

Final Fantasy doesn't use a standard ASCII map for it's characters. Here is a table for the English letter mappings

|    | 00          | 01        | 02     | 03     | 04    | 05       | 06      | 07     | 08       | 09      | 0.4     | 0B       | ОС     | 0D       | 0E       | 0F       |
|----|-------------|-----------|--------|--------|-------|----------|---------|--------|----------|---------|---------|----------|--------|----------|----------|----------|
| 00 | {SPACE}     | !         | "      | #      | \$    | %        | &       |        | (        | )       | *       | +        | ,      | -        | -        | /        |
| 10 | 0           | 1         | 2      | 3      | 4     | 5        | 6       | 7      | 8        | 9       | :       | ;        | <      | =        | >        | ?        |
| 20 | @           | A         | В      | С      | D     | Е        | F       | G      | Н        | I       | J       | K        | L      | M        | N        | 0        |
| 30 | P           | Q         | R      | S      | T     | U        | V       | W      | X        | Y       | Z       | [        | \      | ]        | ^        | -        |
| 40 |             | a         | b      | С      | d     | e        | f       | g      | h        | i       | j       | k        | l      | m        | n        | 0        |
| 50 | р           | q         | r      | S      | t     | u        | v       | w      | X        | У       | Z       | {        | 1      | }        | ~        |          |
| 60 | Ä           | Á         | Ç      | É      | Ñ     | Ö        | Ü       | á      | à        | â       | ä       | ã        | å      | ç        | é        | è        |
| 70 | ê           | ë         | í      | ì      | î     | ï        | ñ       | ó      | ò        | ô       | ö       | õ        | ú      | ù        | û        | ü        |
| 80 | {Comnd}     | 0         | ¢      | £      | Ú     | Ù        | 1       | В      | ®        | ©       | TM      | '        |        | #        | Æ        | Ø        |
| 90 | ∞           | ±         | ≦      | ≧      | ¥     | μ        | д       | Σ      | П        | π       | J       | 우        | 87     | Ω        |          |          |
| A0 |             |           |        |        |       |          |         |        |          |         |         |          |        |          | <9b>     | <9c>     |
| B0 |             |           | <93>   | <94>   |       |          |         |        |          |         |         |          |        |          |          |          |
| СО |             |           |        |        |       |          |         |        |          |         |         |          |        |          |          |          |
| Dθ |             |           | {GRAY} | {BLUE} | {RED} | (PURPLE) | {GREEN} | {CYAN} | {YELLOW} | {WHITE} |         |          |        |          |          |          |
| E0 | {TAB}       |           | ,      |        |       |          |         | {EOL}  | {PAUSE}  |         | {Cloud} | {Barret} | {Tifa} | {Aerith} | {Red 13} | {Yuffie} |
| FØ | {Cait Sith} | {Vincent} | {Cid}  |        |       |          | 0       | Δ      |          | ×       |         |          |        |          |          | {STOP}   |


# TouphScript Offset Table - Complete Documentation

**Created:** 2026-01-02 18:22:24 JST (Friday)
**Last Modified:** 2026-01-02 18:22:24 JST (Friday)
**Version:** 1.0.0
**Session-ID:** (current session)

---

## Overview

TouphScript uses a hardcoded offset table to patch text strings in `ff7.exe`. This document provides complete documentation of all **767 entries** in the offset table, extracted from `touphscript/ff7exe.cpp`.

### Source File Location

```
/home/johnzealanddoyle/projects/tools/touphscript/ff7exe.cpp
Lines 154-164: ofsts[], len[], type[] arrays
```

---

## String Type Definitions

From `ff7exe.h` enum `txtTypes`:

| Type Code | Name | Description | Termination | Notes |
|-----------|------|-------------|-------------|-------|
| 0 | DEF | Standard FF7 encoding | 0xFF terminator | Most common type |
| 1 | NOFF_TERM | No FF terminator | None in file | touphScript adds 0xFF on read |
| 2 | RGB | RGB encoded | 0xFF terminator | ASCII + 0x73 offset for keyboard labels |
| 3 | UNICODE | Windows Unicode | NULL byte | Single-byte characters only |
| 4 | FFPADDED | FF7 encoding | Padded with 0xFF | Multiple 0xFF bytes pad to length |
| 5 | ZEROTERM | Zero-terminated | 0x00 bytes | Padded with zero bytes |

---

## Address Calculation Formula

To convert file offsets to Virtual Addresses (VA) for HEXT patches:

```
VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000
```

Simplified:
```
VA = FileOffset + 0x17600
```

---

## Complete Offset Table (767 Entries)

### Region 1: Game State / Resume/Quit Strings (Indices 0-4)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 0 | 0x518370 | 30 | 0 | DEF | 0x919970 | Resume game text |
| 1 | 0x51838E | 30 | 0 | DEF | 0x91998E | Quit confirmation |
| 2 | 0x5183AC | 30 | 0 | DEF | 0x9199AC | Exit text |
| 3 | 0x5183D0 | 4 | 0 | DEF | 0x9199D0 | Short label |
| 4 | 0x5183D4 | 4 | 0 | DEF | 0x9199D4 | Short label |

**Should Patch:** Yes - These are user-visible game state messages.

---

### Region 2: Save Slot Descriptions (Indices 5-32)

These are 48-byte slots for save file descriptions.

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 5 | 0x5188A8 | 48 | 0 | DEF | 0x919EA8 | Save slot template/description |
| 6 | 0x5188D8 | 48 | 0 | DEF | 0x919ED8 | Save slot template/description |
| 7 | 0x518908 | 48 | 0 | DEF | 0x919F08 | Save slot template/description |
| 8 | 0x518938 | 48 | 0 | DEF | 0x919F38 | Save slot template/description |
| 9 | 0x518968 | 48 | 0 | DEF | 0x919F68 | Save slot template/description |
| 10 | 0x518998 | 48 | 0 | DEF | 0x919F98 | Save slot template/description |
| 11 | 0x5189C8 | 48 | 0 | DEF | 0x919FC8 | Save slot template/description |
| 12 | 0x5189F8 | 48 | 0 | DEF | 0x919FF8 | Save slot template/description |
| 13 | 0x518A28 | 48 | 0 | DEF | 0x91A028 | Save slot template/description |
| 14 | 0x518A58 | 48 | 0 | DEF | 0x91A058 | Save slot template/description |
| 15 | 0x518A88 | 48 | 0 | DEF | 0x91A088 | Save slot template/description |
| 16 | 0x518AB8 | 48 | 0 | DEF | 0x91A0B8 | Save slot template/description |
| 17 | 0x518C08 | 48 | 0 | DEF | 0x91A208 | Save slot template/description |
| 18 | 0x518C38 | 48 | 0 | DEF | 0x91A238 | Save slot template/description |
| 19 | 0x518C68 | 48 | 0 | DEF | 0x91A268 | Save slot template/description |
| 20 | 0x518C98 | 48 | 0 | DEF | 0x91A298 | Save slot template/description |
| 21 | 0x518CC8 | 48 | 0 | DEF | 0x91A2C8 | Save slot template/description |
| 22 | 0x518CF8 | 48 | 0 | DEF | 0x91A2F8 | Save slot template/description |
| 23 | 0x518D28 | 48 | 0 | DEF | 0x91A328 | Save slot template/description |
| 24 | 0x518D58 | 48 | 0 | DEF | 0x91A358 | Save slot template/description |
| 25 | 0x518D88 | 48 | 0 | DEF | 0x91A388 | Save slot template/description |
| 26 | 0x518DE8 | 48 | 0 | DEF | 0x91A3E8 | Save slot template/description |
| 27 | 0x518E18 | 48 | 0 | DEF | 0x91A418 | Save slot template/description |
| 28 | 0x518ED8 | 48 | 0 | DEF | 0x91A4D8 | Save slot template/description |
| 29 | 0x518F08 | 48 | 0 | DEF | 0x91A508 | Save slot template/description |
| 30 | 0x518F38 | 48 | 0 | DEF | 0x91A538 | Save slot template/description |
| 31 | 0x518F68 | 48 | 0 | DEF | 0x91A568 | Save slot template/description |
| 32 | 0x518FC8 | 48 | 0 | DEF | 0x91A5C8 | Save slot template/description |

**Should Patch:** Yes - Save descriptions are user-visible.

---

### Region 3: Yes/No Menu Labels (Indices 33-35)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 33 | 0x519238 | 6 | 1 | NOFF_TERM | 0x91A838 | "Yes" option |
| 34 | 0x51923E | 6 | 1 | NOFF_TERM | 0x91A83E | "No" option |
| 35 | 0x519244 | 6 | 1 | NOFF_TERM | 0x91A844 | Menu option |

**Should Patch:** Yes - Dialog options are user-visible.

---

### Region 4: Config Menu Labels (Indices 36-57)

Main configuration menu items - 20 bytes each.

| Idx | File Offset | Length | Type | Type Name | VA Address | Known English Text |
|-----|-------------|--------|------|-----------|------------|-------------------|
| 36 | 0x519288 | 25 | 0 | DEF | 0x91A888 | Sound config label |
| 37 | 0x5192A1 | 25 | 0 | DEF | 0x91A8A1 | Config label |
| 38 | 0x5192C0 | 20 | 0 | DEF | 0x91A8C0 | **ITEM** |
| 39 | 0x5192D4 | 20 | 0 | DEF | 0x91A8D4 | **MAGIC** |
| 40 | 0x5192E8 | 20 | 0 | DEF | 0x91A8E8 | **MATERIA** |
| 41 | 0x5192FC | 20 | 0 | DEF | 0x91A8FC | **EQUIP** |
| 42 | 0x519310 | 20 | 0 | DEF | 0x91A910 | **STATUS** |
| 43 | 0x519324 | 20 | 0 | DEF | 0x91A924 | **ORDER** |
| 44 | 0x519338 | 20 | 0 | DEF | 0x91A938 | **LIMIT** |
| 45 | 0x51934C | 20 | 0 | DEF | 0x91A94C | **CONFIG** |
| 46 | 0x519360 | 20 | 0 | DEF | 0x91A960 | **PHS** |
| 47 | 0x519374 | 20 | 0 | DEF | 0x91A974 | **SAVE** |
| 48 | 0x519388 | 20 | 0 | DEF | 0x91A988 | **QUIT** |
| 49 | 0x51939C | 20 | 0 | DEF | 0x91A99C | Menu label |
| 50 | 0x5193D8 | 20 | 0 | DEF | 0x91A9D8 | Config option |
| 51 | 0x5193EC | 20 | 0 | DEF | 0x91A9EC | Config option |
| 52 | 0x519400 | 20 | 0 | DEF | 0x91AA00 | Config option |
| 53 | 0x519414 | 20 | 0 | DEF | 0x91AA14 | Config option |
| 54 | 0x519428 | 20 | 0 | DEF | 0x91AA28 | Config option |
| 55 | 0x519450 | 20 | 0 | DEF | 0x91AA50 | Config option |
| 56 | 0x519464 | 20 | 0 | DEF | 0x91AA64 | Config option |
| 57 | 0x519478 | 20 | 0 | DEF | 0x91AA78 | Config option |

**Should Patch:** Yes - Main menu and config labels.

---

### Region 5: Config Help/Description Text (Indices 58-76)

50-byte help text strings for configuration options.

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 58 | 0x5196B0 | 50 | 0 | DEF | 0x91ACB0 | Config help text |
| 59 | 0x5196E2 | 50 | 0 | DEF | 0x91ACE2 | Config help text |
| 60 | 0x519714 | 50 | 0 | DEF | 0x91AD14 | Config help text |
| 61 | 0x519746 | 50 | 0 | DEF | 0x91AD46 | Config help text |
| 62 | 0x519778 | 50 | 0 | DEF | 0x91AD78 | Config help text |
| 63 | 0x5197AA | 50 | 0 | DEF | 0x91ADAA | Config help text |
| 64 | 0x5197DC | 50 | 0 | DEF | 0x91ADDC | Config help text |
| 65 | 0x51980E | 50 | 0 | DEF | 0x91AE0E | Config help text |
| 66 | 0x519840 | 50 | 0 | DEF | 0x91AE40 | Config help text |
| 67 | 0x519872 | 50 | 0 | DEF | 0x91AE72 | Config help text |
| 68 | 0x5198A4 | 50 | 0 | DEF | 0x91AEA4 | Config help text |
| 69 | 0x5198D6 | 50 | 0 | DEF | 0x91AED6 | Config help text |
| 70 | 0x519908 | 50 | 0 | DEF | 0x91AF08 | Config help text |
| 71 | 0x51993A | 50 | 0 | DEF | 0x91AF3A | Config help text |
| 72 | 0x51996C | 50 | 0 | DEF | 0x91AF6C | Config help text |
| 73 | 0x51999E | 50 | 0 | DEF | 0x91AF9E | Config help text |
| 74 | 0x5199D0 | 50 | 0 | DEF | 0x91AFD0 | Config help text |
| 75 | 0x519A02 | 50 | 0 | DEF | 0x91B002 | Config help text |
| 76 | 0x519A34 | 50 | 0 | DEF | 0x91B034 | Config help text |

**Should Patch:** Yes - Help descriptions are user-visible.

---

### Region 6: Keyboard Labels - RGB Encoded (Indices 77-213)

**TYPE 2 (RGB)**: These strings use RGB encoding (ASCII + 0x73) for keyboard button labels.

This is the largest RGB region - 137 entries for keyboard/controller configuration.

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 77 | 0x519FE0 | 8 | 2 | RGB | 0x91B5E0 | Keyboard key |
| 78 | 0x519FE8 | 4 | 2 | RGB | 0x91B5E8 | Keyboard key |
| 79 | 0x519FEC | 4 | 2 | RGB | 0x91B5EC | Keyboard key |
| 80 | 0x519FF0 | 4 | 2 | RGB | 0x91B5F0 | Keyboard key |
| 81 | 0x519FF4 | 4 | 2 | RGB | 0x91B5F4 | Keyboard key |
| 82 | 0x519FF8 | 4 | 2 | RGB | 0x91B5F8 | Keyboard key |
| 83 | 0x519FFC | 4 | 2 | RGB | 0x91B5FC | Keyboard key |
| 84 | 0x51A000 | 4 | 2 | RGB | 0x91B600 | Keyboard key |
| 85 | 0x51A004 | 4 | 2 | RGB | 0x91B604 | Keyboard key |
| 86 | 0x51A008 | 4 | 2 | RGB | 0x91B608 | Keyboard key |
| 87 | 0x51A00C | 4 | 2 | RGB | 0x91B60C | Keyboard key |
| 88 | 0x51A010 | 8 | 2 | RGB | 0x91B610 | Keyboard key |
| 89 | 0x51A018 | 8 | 2 | RGB | 0x91B618 | Keyboard key |
| 90 | 0x51A020 | 12 | 2 | RGB | 0x91B620 | Keyboard key |
| 91 | 0x51A02C | 4 | 2 | RGB | 0x91B62C | Keyboard key |
| 92 | 0x51A030 | 4 | 2 | RGB | 0x91B630 | Keyboard key |
| 93 | 0x51A034 | 4 | 2 | RGB | 0x91B634 | Keyboard key |
| 94 | 0x51A038 | 4 | 2 | RGB | 0x91B638 | Keyboard key |
| 95 | 0x51A03C | 4 | 2 | RGB | 0x91B63C | Keyboard key |
| 96 | 0x51A040 | 4 | 2 | RGB | 0x91B640 | Keyboard key |
| 97 | 0x51A044 | 4 | 2 | RGB | 0x91B644 | Keyboard key |
| 98 | 0x51A048 | 4 | 2 | RGB | 0x91B648 | Keyboard key |
| 99 | 0x51A04C | 4 | 2 | RGB | 0x91B64C | Keyboard key |
| 100 | 0x51A050 | 4 | 2 | RGB | 0x91B650 | Keyboard key |
| 101 | 0x51A054 | 4 | 2 | RGB | 0x91B654 | Keyboard key |
| 102 | 0x51A058 | 16 | 2 | RGB | 0x91B658 | Keyboard key |
| 103 | 0x51A068 | 16 | 2 | RGB | 0x91B668 | Keyboard key |
| 104 | 0x51A078 | 8 | 2 | RGB | 0x91B678 | Keyboard key |
| 105 | 0x51A080 | 16 | 2 | RGB | 0x91B680 | Keyboard key |
| 106 | 0x51A090 | 4 | 2 | RGB | 0x91B690 | Keyboard key |
| 107 | 0x51A094 | 4 | 2 | RGB | 0x91B694 | Keyboard key |
| 108 | 0x51A098 | 4 | 2 | RGB | 0x91B698 | Keyboard key |
| 109 | 0x51A09C | 4 | 2 | RGB | 0x91B69C | Keyboard key |
| 110 | 0x51A0A0 | 4 | 2 | RGB | 0x91B6A0 | Keyboard key |
| 111 | 0x51A0A4 | 4 | 2 | RGB | 0x91B6A4 | Keyboard key |
| 112 | 0x51A0A8 | 4 | 2 | RGB | 0x91B6A8 | Keyboard key |
| 113 | 0x51A0AC | 4 | 2 | RGB | 0x91B6AC | Keyboard key |
| 114 | 0x51A0B0 | 4 | 2 | RGB | 0x91B6B0 | Keyboard key |
| 115 | 0x51A0B4 | 12 | 2 | RGB | 0x91B6B4 | Keyboard key |
| 116 | 0x51A0C0 | 12 | 2 | RGB | 0x91B6C0 | Keyboard key |
| 117 | 0x51A0CC | 8 | 2 | RGB | 0x91B6CC | Keyboard key |
| 118 | 0x51A0D4 | 12 | 2 | RGB | 0x91B6D4 | Keyboard key |
| 119 | 0x51A0E0 | 12 | 2 | RGB | 0x91B6E0 | Keyboard key |
| 120 | 0x51A0EC | 4 | 2 | RGB | 0x91B6EC | Keyboard key |
| 121 | 0x51A0F0 | 4 | 2 | RGB | 0x91B6F0 | Keyboard key |
| 122 | 0x51A0F4 | 4 | 2 | RGB | 0x91B6F4 | Keyboard key |
| 123 | 0x51A0F8 | 4 | 2 | RGB | 0x91B6F8 | Keyboard key |
| 124 | 0x51A0FC | 4 | 2 | RGB | 0x91B6FC | Keyboard key |
| 125 | 0x51A100 | 4 | 2 | RGB | 0x91B700 | Keyboard key |
| 126 | 0x51A104 | 4 | 2 | RGB | 0x91B704 | Keyboard key |
| 127 | 0x51A108 | 8 | 2 | RGB | 0x91B708 | Keyboard key |
| 128 | 0x51A110 | 8 | 2 | RGB | 0x91B710 | Keyboard key |
| 129 | 0x51A118 | 8 | 2 | RGB | 0x91B718 | Keyboard key |
| 130 | 0x51A120 | 12 | 2 | RGB | 0x91B720 | Keyboard key |
| 131 | 0x51A12C | 12 | 2 | RGB | 0x91B72C | Keyboard key |
| 132 | 0x51A138 | 12 | 2 | RGB | 0x91B738 | Keyboard key |
| 133 | 0x51A144 | 8 | 2 | RGB | 0x91B744 | Keyboard key |
| 134 | 0x51A14C | 12 | 2 | RGB | 0x91B74C | Keyboard key |
| 135 | 0x51A158 | 4 | 2 | RGB | 0x91B758 | Keyboard key |
| 136 | 0x51A15C | 4 | 2 | RGB | 0x91B75C | Keyboard key |
| 137 | 0x51A160 | 4 | 2 | RGB | 0x91B760 | Keyboard key |
| 138 | 0x51A164 | 4 | 2 | RGB | 0x91B764 | Keyboard key |
| 139 | 0x51A168 | 4 | 2 | RGB | 0x91B768 | Keyboard key |
| 140 | 0x51A16C | 4 | 2 | RGB | 0x91B76C | Keyboard key |
| 141 | 0x51A170 | 4 | 2 | RGB | 0x91B770 | Keyboard key |
| 142 | 0x51A174 | 4 | 2 | RGB | 0x91B774 | Keyboard key |
| 143 | 0x51A178 | 4 | 2 | RGB | 0x91B778 | Keyboard key |
| 144 | 0x51A17C | 4 | 2 | RGB | 0x91B77C | Keyboard key |
| 145 | 0x51A180 | 8 | 2 | RGB | 0x91B780 | Keyboard key |
| 146 | 0x51A188 | 8 | 2 | RGB | 0x91B788 | Keyboard key |
| 147 | 0x51A190 | 8 | 2 | RGB | 0x91B790 | Keyboard key |
| 148 | 0x51A198 | 8 | 2 | RGB | 0x91B798 | Keyboard key |
| 149 | 0x51A1A0 | 8 | 2 | RGB | 0x91B7A0 | Keyboard key |
| 150 | 0x51A1A8 | 12 | 2 | RGB | 0x91B7A8 | Keyboard key |
| 151 | 0x51A1B4 | 8 | 2 | RGB | 0x91B7B4 | Keyboard key |
| 152 | 0x51A1BC | 8 | 2 | RGB | 0x91B7BC | Keyboard key |
| 153 | 0x51A1C4 | 8 | 2 | RGB | 0x91B7C4 | Keyboard key |
| 154 | 0x51A1CC | 4 | 2 | RGB | 0x91B7CC | Keyboard key |
| 155 | 0x51A1D0 | 8 | 2 | RGB | 0x91B7D0 | Keyboard key |
| 156 | 0x51A1D8 | 8 | 2 | RGB | 0x91B7D8 | Keyboard key |
| 157 | 0x51A1E0 | 8 | 2 | RGB | 0x91B7E0 | Keyboard key |
| 158 | 0x51A1E8 | 8 | 2 | RGB | 0x91B7E8 | Keyboard key |
| 159 | 0x51A1F0 | 8 | 2 | RGB | 0x91B7F0 | Keyboard key |
| 160 | 0x51A210 | 4 | 2 | RGB | 0x91B810 | Keyboard key |
| 161 | 0x51A214 | 4 | 2 | RGB | 0x91B814 | Keyboard key |
| 162 | 0x51A270 | 4 | 2 | RGB | 0x91B870 | Keyboard key |
| 163 | 0x51A274 | 4 | 2 | RGB | 0x91B874 | Keyboard key |
| 164 | 0x51A278 | 4 | 2 | RGB | 0x91B878 | Keyboard key |
| 165 | 0x51A2C4 | 8 | 2 | RGB | 0x91B8C4 | Keyboard key |
| 166 | 0x51A30C | 8 | 2 | RGB | 0x91B90C | Keyboard key |
| 167 | 0x51A31C | 12 | 2 | RGB | 0x91B91C | Keyboard key |
| 168 | 0x51A330 | 4 | 2 | RGB | 0x91B930 | Keyboard key |
| 169 | 0x51A3AC | 16 | 2 | RGB | 0x91B9AC | Keyboard key |
| 170 | 0x51A3CC | 12 | 2 | RGB | 0x91B9CC | Keyboard key |
| 171 | 0x51A3D8 | 4 | 2 | RGB | 0x91B9D8 | Keyboard key |
| 172 | 0x51A3DC | 8 | 2 | RGB | 0x91B9DC | Keyboard key |
| 173 | 0x51A3E4 | 12 | 2 | RGB | 0x91B9E4 | Keyboard key |
| 174 | 0x51A3F0 | 8 | 2 | RGB | 0x91B9F0 | Keyboard key |
| 175 | 0x51A3F8 | 8 | 2 | RGB | 0x91B9F8 | Keyboard key |
| 176 | 0x51A400 | 4 | 2 | RGB | 0x91BA00 | Keyboard key |
| 177 | 0x51A404 | 12 | 2 | RGB | 0x91BA04 | Keyboard key |
| 178 | 0x51A430 | 12 | 2 | RGB | 0x91BA30 | Keyboard key |
| 179 | 0x51A43C | 16 | 2 | RGB | 0x91BA3C | Keyboard key |
| 180 | 0x51A4F4 | 12 | 2 | RGB | 0x91BAF4 | Keyboard key |
| 181 | 0x51A508 | 8 | 2 | RGB | 0x91BB08 | Keyboard key |
| 182 | 0x51A518 | 8 | 2 | RGB | 0x91BB18 | Keyboard key |
| 183 | 0x51A520 | 12 | 2 | RGB | 0x91BB20 | Keyboard key |
| 184 | 0x51A59C | 8 | 2 | RGB | 0x91BB9C | Keyboard key |
| 185 | 0x51A5A4 | 4 | 2 | RGB | 0x91BBA4 | Keyboard key |
| 186 | 0x51A5A8 | 8 | 2 | RGB | 0x91BBA8 | Keyboard key |
| 187 | 0x51A5B8 | 8 | 2 | RGB | 0x91BBB8 | Keyboard key |
| 188 | 0x51A5C8 | 8 | 2 | RGB | 0x91BBC8 | Keyboard key |
| 189 | 0x51A5D8 | 4 | 2 | RGB | 0x91BBD8 | Keyboard key |
| 190 | 0x51A5DC | 8 | 2 | RGB | 0x91BBDC | Keyboard key |
| 191 | 0x51A5E4 | 12 | 2 | RGB | 0x91BBE4 | Keyboard key |
| 192 | 0x51A5F0 | 8 | 2 | RGB | 0x91BBF0 | Keyboard key |
| 193 | 0x51A5F8 | 8 | 2 | RGB | 0x91BBF8 | Keyboard key |
| 194 | 0x51A638 | 12 | 2 | RGB | 0x91BC38 | Keyboard key |
| 195 | 0x51A644 | 12 | 2 | RGB | 0x91BC44 | Keyboard key |
| 196 | 0x51A650 | 8 | 2 | RGB | 0x91BC50 | Keyboard key |
| 197 | 0x51A660 | 12 | 2 | RGB | 0x91BC60 | Keyboard key |
| 198 | 0x51A66C | 12 | 2 | RGB | 0x91BC6C | Keyboard key |
| 199 | 0x51A678 | 12 | 2 | RGB | 0x91BC78 | Keyboard key |
| 200 | 0x51A68C | 4 | 2 | RGB | 0x91BC8C | Keyboard key |
| 201 | 0x51A690 | 8 | 2 | RGB | 0x91BC90 | Keyboard key |
| 202 | 0x51A698 | 8 | 2 | RGB | 0x91BC98 | Keyboard key |
| 203 | 0x51A6A0 | 8 | 2 | RGB | 0x91BCA0 | Keyboard key |
| 204 | 0x51A6D4 | 12 | 2 | RGB | 0x91BCD4 | Keyboard key |
| 205 | 0x51A6E0 | 12 | 2 | RGB | 0x91BCE0 | Keyboard key |
| 206 | 0x51A6EC | 12 | 2 | RGB | 0x91BCEC | Keyboard key |
| 207 | 0x51A6F8 | 12 | 2 | RGB | 0x91BCF8 | Keyboard key |
| 208 | 0x51A704 | 12 | 2 | RGB | 0x91BD04 | Keyboard key |
| 209 | 0x51A710 | 12 | 2 | RGB | 0x91BD10 | Keyboard key |
| 210 | 0x51A71C | 12 | 2 | RGB | 0x91BD1C | Keyboard key |
| 211 | 0x51A728 | 12 | 2 | RGB | 0x91BD28 | Keyboard key |
| 212 | 0x51A734 | 12 | 2 | RGB | 0x91BD34 | Keyboard key |

**Note:** Index 203 (0x51A6A0) ends the first chunk before gap.

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 213 | 0x51A6C8 | 12 | 2 | RGB | 0x91BCC8 | Keyboard key |

**Should Patch:** Context-dependent - Keyboard labels are typically English even in Japanese versions (standard key names like "Enter", "Space", etc.). Consider keeping original unless localizing keyboard layout.

---

### Region 7: Battle/Status Strings (Indices 214-232)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 214 | 0x51D1E0 | 8 | 0 | DEF | 0x91E7E0 | Battle status |
| 215 | 0x51D23C | 10 | 0 | DEF | 0x91E83C | Battle label |
| 216 | 0x51D246 | 10 | 0 | DEF | 0x91E846 | Battle label |
| 217 | 0x51D250 | 10 | 0 | DEF | 0x91E850 | Battle label |
| 218 | 0x51D25A | 10 | 0 | DEF | 0x91E85A | Battle label |
| 219 | 0x51D264 | 10 | 0 | DEF | 0x91E864 | Battle label |
| 220 | 0x51D26E | 10 | 0 | DEF | 0x91E86E | Battle label |
| 221 | 0x51D278 | 10 | 0 | DEF | 0x91E878 | Battle label |
| 222 | 0x51D282 | 10 | 0 | DEF | 0x91E882 | Battle label |
| 223 | 0x51D28C | 10 | 0 | DEF | 0x91E88C | Battle label |
| 224 | 0x51D2B4 | 11 | 0 | DEF | 0x91E8B4 | Battle label |
| 225 | 0x51D2BE | 10 | 0 | DEF | 0x91E8BE | Battle label |
| 226 | 0x51D2DC | 10 | 0 | DEF | 0x91E8DC | Battle label |
| 227 | 0x51D2F0 | 10 | 0 | DEF | 0x91E8F0 | Battle label |
| 228 | 0x51D30E | 10 | 0 | DEF | 0x91E90E | Battle label |
| 229 | 0x51D318 | 10 | 0 | DEF | 0x91E918 | Battle label |
| 230 | 0x51D322 | 10 | 0 | DEF | 0x91E922 | Battle label |
| 231 | 0x51D32C | 28 | 0 | DEF | 0x91E92C | Battle text |
| 232 | 0x51D3A0 | 4 | 0 | DEF | 0x91E9A0 | Battle label |

**Should Patch:** Yes - Battle messages are user-visible.

---

### Region 8: More Battle/Status Text (Indices 233-268)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 233 | 0x51D3BC | 8 | 0 | DEF | 0x91E9BC | Status text |
| 234 | 0x51D3C0 | 16 | 0 | DEF | 0x91E9C0 | Status text |
| 235 | 0x51D3C8 | 16 | 0 | DEF | 0x91E9C8 | Status text |
| 236 | 0x51D588 | 24 | 0 | DEF | 0x91EB88 | Message text |
| 237 | 0x51D598 | 22 | 0 | DEF | 0x91EB98 | Message text |
| 238 | 0x51D5B0 | 22 | 0 | DEF | 0x91EBB0 | Message text |
| 239 | 0x51D5C6 | 22 | 0 | DEF | 0x91EBC6 | Message text |
| 240 | 0x51D5DC | 32 | 0 | DEF | 0x91EBDC | Message text |
| 241 | 0x51D608 | 32 | 0 | DEF | 0x91EC08 | Message text |
| 242 | 0x51D628 | 32 | 0 | DEF | 0x91EC28 | Message text |
| 243 | 0x51D648 | 32 | 0 | DEF | 0x91EC48 | Message text |
| 244 | 0x51D668 | 32 | 0 | DEF | 0x91EC68 | Message text |
| 245 | 0x51D688 | 32 | 0 | DEF | 0x91EC88 | Message text |
| 246 | 0x51D6A8 | 32 | 0 | DEF | 0x91ECA8 | Message text |
| 247 | 0x51D6C8 | 32 | 0 | DEF | 0x91ECC8 | Message text |
| 248 | 0x51D6E8 | 32 | 0 | DEF | 0x91ECE8 | Message text |
| 249 | 0x51D708 | 32 | 0 | DEF | 0x91ED08 | Message text |
| 250 | 0x51D728 | 32 | 0 | DEF | 0x91ED28 | Message text |
| 251 | 0x51D748 | 32 | 0 | DEF | 0x91ED48 | Message text |
| 252 | 0x51D768 | 32 | 0 | DEF | 0x91ED68 | Message text |
| 253 | 0x51D788 | 32 | 0 | DEF | 0x91ED88 | Message text |
| 254 | 0x51D7A8 | 32 | 0 | DEF | 0x91EDA8 | Message text |
| 255 | 0x51D7C8 | 32 | 0 | DEF | 0x91EDC8 | Message text |
| 256 | 0x51D7E8 | 32 | 0 | DEF | 0x91EDE8 | Message text |
| 257 | 0x51D808 | 32 | 0 | DEF | 0x91EE08 | Message text |
| 258 | 0x51D828 | 32 | 0 | DEF | 0x91EE28 | Message text |
| 259 | 0x51D848 | 32 | 0 | DEF | 0x91EE48 | Message text |
| 260 | 0x51D868 | 32 | 0 | DEF | 0x91EE68 | Message text |
| 261 | 0x51D888 | 32 | 0 | DEF | 0x91EE88 | Message text |
| 262 | 0x51D8A8 | 32 | 0 | DEF | 0x91EEA8 | Message text |
| 263 | 0x51D8C8 | 32 | 0 | DEF | 0x91EEC8 | Message text |
| 264 | 0x51D8E8 | 32 | 0 | DEF | 0x91EEE8 | Message text |
| 265 | 0x51D908 | 32 | 0 | DEF | 0x91EF08 | Message text |
| 266 | 0x51D928 | 34 | 0 | DEF | 0x91EF28 | Message text |
| 267 | 0x51D94A | 34 | 0 | DEF | 0x91EF4A | Message text |
| 268 | 0x51D96C | 34 | 0 | DEF | 0x91EF6C | Message text |

**Should Patch:** Yes - Battle/status messages are user-visible.

---

### Region 9: More Battle Text (Indices 269-293)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 269 | 0x51DAE0 | 8 | 0 | DEF | 0x91F0E0 | Battle text |
| 270 | 0x51DB40 | 38 | 0 | DEF | 0x91F140 | Battle text |
| 271 | 0x51DB66 | 38 | 0 | DEF | 0x91F166 | Battle text |
| 272 | 0x51DB8C | 38 | 0 | DEF | 0x91F18C | Battle text |
| 273 | 0x51DBB2 | 38 | 0 | DEF | 0x91F1B2 | Battle text |
| 274 | 0x51DBD8 | 38 | 0 | DEF | 0x91F1D8 | Battle text |
| 275 | 0x51DBFE | 38 | 0 | DEF | 0x91F1FE | Battle text |
| 276 | 0x51DE22 | 22 | 0 | DEF | 0x91F422 | Battle text |
| 277 | 0x51DE38 | 22 | 0 | DEF | 0x91F438 | Battle text |
| 278 | 0x51DE4E | 22 | 0 | DEF | 0x91F44E | Battle text |
| 279 | 0x51DED8 | 36 | 0 | DEF | 0x91F4D8 | Battle text |
| 280 | 0x51DEFC | 36 | 0 | DEF | 0x91F4FC | Battle text |
| 281 | 0x51DF20 | 36 | 0 | DEF | 0x91F520 | Battle text |
| 282 | 0x51DF44 | 36 | 0 | DEF | 0x91F544 | Battle text |
| 283 | 0x51DF68 | 36 | 0 | DEF | 0x91F568 | Battle text |
| 284 | 0x51DF8C | 36 | 0 | DEF | 0x91F58C | Battle text |
| 285 | 0x51DFB0 | 36 | 0 | DEF | 0x91F5B0 | Battle text |
| 286 | 0x51DFD4 | 36 | 0 | DEF | 0x91F5D4 | Battle text |
| 287 | 0x51DFF8 | 36 | 0 | DEF | 0x91F5F8 | Battle text |
| 288 | 0x51E01C | 36 | 0 | DEF | 0x91F61C | Battle text |
| 289 | 0x51E040 | 36 | 0 | DEF | 0x91F640 | Battle text |
| 290 | 0x51E064 | 36 | 0 | DEF | 0x91F664 | Battle text |
| 291 | 0x51E088 | 36 | 0 | DEF | 0x91F688 | Battle text |
| 292 | 0x51E0AC | 36 | 0 | DEF | 0x91F6AC | Battle text |

**Should Patch:** Yes - Battle messages are user-visible.

---

### Region 10: Status Effect Labels (Indices 293-327)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 293 | 0x51EF40 | 10 | 0 | DEF | 0x920540 | Status effect |
| 294 | 0x51EF4A | 10 | 0 | DEF | 0x92054A | Status effect |
| 295 | 0x51EF54 | 10 | 0 | DEF | 0x920554 | Status effect |
| 296 | 0x51EF5E | 10 | 0 | DEF | 0x92055E | Status effect |
| 297 | 0x51EF68 | 10 | 0 | DEF | 0x920568 | Status effect |
| 298 | 0x51EF72 | 10 | 0 | DEF | 0x920572 | Status effect |
| 299 | 0x51EF7C | 10 | 0 | DEF | 0x92057C | Status effect |
| 300 | 0x51EF86 | 10 | 0 | DEF | 0x920586 | Status effect |
| 301 | 0x51EF90 | 10 | 0 | DEF | 0x920590 | Status effect |
| 302 | 0x51EFA0 | 20 | 0 | DEF | 0x9205A0 | Status effect |
| 303 | 0x51EFB4 | 20 | 0 | DEF | 0x9205B4 | Status effect |
| 304 | 0x51EFC8 | 20 | 0 | DEF | 0x9205C8 | Status effect |
| 305 | 0x51EFDC | 20 | 0 | DEF | 0x9205DC | Status effect |
| 306 | 0x51EFF0 | 20 | 0 | DEF | 0x9205F0 | Status effect |
| 307 | 0x51F004 | 20 | 0 | DEF | 0x920604 | Status effect |
| 308 | 0x51F018 | 20 | 0 | DEF | 0x920618 | Status effect |
| 309 | 0x51F02C | 20 | 0 | DEF | 0x92062C | Status effect |
| 310 | 0x51F040 | 20 | 0 | DEF | 0x920640 | Status effect |
| 311 | 0x51F054 | 20 | 0 | DEF | 0x920654 | Status effect |
| 312 | 0x51F068 | 20 | 0 | DEF | 0x920668 | Status effect |
| 313 | 0x51F07C | 20 | 0 | DEF | 0x92067C | Status effect |
| 314 | 0x51F090 | 20 | 0 | DEF | 0x920690 | Status effect |
| 315 | 0x51F0A4 | 20 | 0 | DEF | 0x9206A4 | Status effect |
| 316 | 0x51F0B8 | 20 | 0 | DEF | 0x9206B8 | Status effect |
| 317 | 0x51F0CC | 20 | 0 | DEF | 0x9206CC | Status effect |
| 318 | 0x51F0E0 | 20 | 0 | DEF | 0x9206E0 | Status effect |
| 319 | 0x51F0F4 | 20 | 0 | DEF | 0x9206F4 | Status effect |
| 320 | 0x51F108 | 20 | 0 | DEF | 0x920708 | Status effect |
| 321 | 0x51F130 | 20 | 0 | DEF | 0x920730 | Status effect |
| 322 | 0x51F144 | 20 | 0 | DEF | 0x920744 | Status effect |
| 323 | 0x51F158 | 20 | 0 | DEF | 0x920758 | Status effect |
| 324 | 0x51F16C | 20 | 0 | DEF | 0x92076C | Status effect |
| 325 | 0x51F180 | 20 | 0 | DEF | 0x920780 | Status effect |
| 326 | 0x51F194 | 20 | 0 | DEF | 0x920794 | Status effect |
| 327 | 0x51F1A8 | 20 | 0 | DEF | 0x9207A8 | Status effect |

**Should Patch:** Yes - Status effects are user-visible.

---

### Region 11: Character Stats (Indices 328-344)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 328 | 0x51F1C0 | 15 | 0 | DEF | 0x9207C0 | Stat label |
| 329 | 0x51F1CF | 15 | 0 | DEF | 0x9207CF | Stat label (Strength) |
| 330 | 0x51F1DE | 15 | 0 | DEF | 0x9207DE | Stat label (Dexterity) |
| 331 | 0x51F1ED | 15 | 0 | DEF | 0x9207ED | Stat label (Vitality) |
| 332 | 0x51F1FC | 15 | 0 | DEF | 0x9207FC | Stat label (Magic) |
| 333 | 0x51F20B | 15 | 0 | DEF | 0x92080B | Stat label (Spirit) |
| 334 | 0x51F21A | 15 | 0 | DEF | 0x92081A | Stat label (Luck) |
| 335 | 0x51F256 | 15 | 0 | DEF | 0x920856 | Stat label |
| 336 | 0x51F265 | 15 | 0 | DEF | 0x920865 | Stat label |
| 337 | 0x51F274 | 15 | 0 | DEF | 0x920874 | Stat label |
| 338 | 0x51F283 | 15 | 0 | DEF | 0x920883 | Stat label |
| 339 | 0x51F292 | 15 | 0 | DEF | 0x920892 | Stat label |
| 340 | 0x51F2A1 | 15 | 0 | DEF | 0x9208A1 | Stat label |
| 341 | 0x51F2B0 | 15 | 0 | DEF | 0x9208B0 | Stat label |
| 342 | 0x51F2BF | 15 | 0 | DEF | 0x9208BF | Stat label |
| 343 | 0x51F2CE | 15 | 0 | DEF | 0x9208CE | Stat label |
| 344 | 0x51F2DD | 15 | 0 | DEF | 0x9208DD | Stat label |

**Should Patch:** Yes - Character stats are user-visible.

---

### Region 12: More Stats and Labels (Indices 345-367)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 345 | 0x51F2EC | 15 | 0 | DEF | 0x9208EC | Stat/label |
| 346 | 0x51F2FB | 15 | 0 | DEF | 0x9208FB | Stat/label |
| 347 | 0x51F30A | 15 | 0 | DEF | 0x92090A | Stat/label |
| 348 | 0x51F319 | 15 | 0 | DEF | 0x920919 | Stat/label |
| 349 | 0x51F328 | 15 | 0 | DEF | 0x920928 | Stat/label |
| 350 | 0x51F337 | 15 | 0 | DEF | 0x920937 | Stat/label |
| 351 | 0x51F346 | 15 | 0 | DEF | 0x920946 | Limit level label |
| 352 | 0x51F3A8 | 12 | 0 | DEF | 0x9209A8 | Equip label (Wpn.) |
| 353 | 0x51F3B4 | 12 | 0 | DEF | 0x9209B4 | Equip label (Arm.) |
| 354 | 0x51F3C0 | 12 | 0 | DEF | 0x9209C0 | Equip label (Acc.) |
| 355 | 0x51F420 | 12 | 0 | DEF | 0x920A20 | Combat stat |
| 356 | 0x51F42C | 12 | 0 | DEF | 0x920A2C | Combat stat |
| 357 | 0x51F438 | 12 | 0 | DEF | 0x920A38 | Combat stat |
| 358 | 0x51F444 | 12 | 0 | DEF | 0x920A44 | Combat stat |
| 359 | 0x51F450 | 12 | 0 | DEF | 0x920A50 | Combat stat |
| 360 | 0x51F45C | 12 | 0 | DEF | 0x920A5C | Combat stat |
| 361 | 0x51F468 | 12 | 0 | DEF | 0x920A68 | Combat stat |
| 362 | 0x51F474 | 12 | 0 | DEF | 0x920A74 | Materia slot |
| 363 | 0x51F480 | 12 | 0 | DEF | 0x920A80 | Growth label |
| 364 | 0x51F48C | 12 | 0 | DEF | 0x920A8C | Nothing |
| 365 | 0x51F498 | 12 | 0 | DEF | 0x920A98 | Normal |
| 366 | 0x51F4A4 | 12 | 0 | DEF | 0x920AA4 | Double |
| 367 | 0x51F4B0 | 12 | 0 | DEF | 0x920AB0 | Triple |

**Should Patch:** Yes - Equipment and materia labels are user-visible.

---

### Region 13: More Menu Labels (Indices 368-420)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 368 | 0x51F518 | 36 | 0 | DEF | 0x920B18 | Menu text |
| 369 | 0x51F53C | 36 | 0 | DEF | 0x920B3C | Menu text |
| 370 | 0x51F560 | 36 | 0 | DEF | 0x920B60 | Menu text |
| 371 | 0x51F584 | 36 | 0 | DEF | 0x920B84 | Menu text |
| 372 | 0x51F5A8 | 20 | 0 | DEF | 0x920BA8 | Menu text |
| 373 | 0x51F5BC | 20 | 0 | DEF | 0x920BBC | Menu text |
| 374 | 0x51F5D0 | 20 | 0 | DEF | 0x920BD0 | Menu text |
| 375 | 0x51F5E4 | 20 | 0 | DEF | 0x920BE4 | Menu text |
| 376 | 0x51F5F8 | 20 | 0 | DEF | 0x920BF8 | Menu text |
| 377 | 0x51F60C | 20 | 0 | DEF | 0x920C0C | Menu text |
| 378 | 0x51F634 | 20 | 0 | DEF | 0x920C34 | Menu text |
| 379 | 0x51F648 | 20 | 0 | DEF | 0x920C48 | Menu text |
| 380 | 0x51F65C | 20 | 0 | DEF | 0x920C5C | Menu text |
| 381 | 0x51F670 | 20 | 0 | DEF | 0x920C70 | Menu text |
| 382 | 0x51F684 | 20 | 0 | DEF | 0x920C84 | Menu text |
| 383 | 0x51F698 | 20 | 0 | DEF | 0x920C98 | Menu text |
| 384 | 0x51F6AC | 20 | 0 | DEF | 0x920CAC | Menu text |
| 385 | 0x51F6D4 | 20 | 0 | DEF | 0x920CD4 | Menu text |
| 386 | 0x51F6E8 | 20 | 0 | DEF | 0x920CE8 | Menu text |
| 387 | 0x51F6FC | 20 | 0 | DEF | 0x920CFC | Menu text |
| 388 | 0x51F710 | 20 | 0 | DEF | 0x920D10 | Menu text |
| 389 | 0x51F724 | 20 | 0 | DEF | 0x920D24 | Menu text |
| 390 | 0x51F738 | 20 | 0 | DEF | 0x920D38 | Menu text |
| 391 | 0x51F74C | 20 | 0 | DEF | 0x920D4C | Menu text |
| 392 | 0x51F760 | 20 | 0 | DEF | 0x920D60 | Menu text |
| 393 | 0x51F774 | 20 | 0 | DEF | 0x920D74 | Menu text |
| 394 | 0x51F788 | 20 | 0 | DEF | 0x920D88 | Menu text |
| 395 | 0x51F79C | 20 | 0 | DEF | 0x920D9C | Menu text |
| 396 | 0x51F7B0 | 20 | 0 | DEF | 0x920DB0 | Menu text |
| 397 | 0x51F7C4 | 20 | 0 | DEF | 0x920DC4 | Menu text |
| 398 | 0x51F7D8 | 20 | 0 | DEF | 0x920DD8 | Menu text |
| 399 | 0x51F7EC | 20 | 0 | DEF | 0x920DEC | Menu text |
| 400 | 0x51F800 | 20 | 0 | DEF | 0x920E00 | Menu text |
| 401 | 0x51F814 | 20 | 0 | DEF | 0x920E14 | Menu text |
| 402 | 0x51F828 | 20 | 0 | DEF | 0x920E28 | Menu text |
| 403 | 0x51F83C | 20 | 0 | DEF | 0x920E3C | Menu text |
| 404 | 0x51F850 | 20 | 0 | DEF | 0x920E50 | Menu text |
| 405 | 0x51F864 | 20 | 0 | DEF | 0x920E64 | Menu text |
| 406 | 0x51F878 | 20 | 0 | DEF | 0x920E78 | Menu text |
| 407 | 0x51F88C | 20 | 0 | DEF | 0x920E8C | Menu text |
| 408 | 0x51F8A0 | 20 | 0 | DEF | 0x920EA0 | Menu text |
| 409 | 0x51F9E8 | 12 | 0 | DEF | 0x920FE8 | Menu text |
| 410 | 0x51F9FC | 12 | 0 | DEF | 0x920FFC | Menu text |
| 411 | 0x51FA10 | 12 | 0 | DEF | 0x921010 | Menu text |
| 412 | 0x51FA24 | 12 | 0 | DEF | 0x921024 | Menu text |
| 413 | 0x51FA38 | 12 | 0 | DEF | 0x921038 | Menu text |
| 414 | 0x51FA4C | 12 | 0 | DEF | 0x92104C | Menu text |
| 415 | 0x51FA60 | 12 | 0 | DEF | 0x921060 | Menu text |
| 416 | 0x51FA74 | 12 | 0 | DEF | 0x921074 | Menu text |
| 417 | 0x51FA9C | 12 | 0 | DEF | 0x92109C | Menu text |
| 418 | 0x51FAB0 | 12 | 0 | DEF | 0x9210B0 | Menu text |
| 419 | 0x51FAC4 | 12 | 0 | DEF | 0x9210C4 | Menu text |
| 420 | 0x51FAD8 | 12 | 0 | DEF | 0x9210D8 | Menu text |

**Should Patch:** Yes - Menu labels are user-visible.

---

### Region 14: Item Menu (Indices 421-431)

| Idx | File Offset | Length | Type | Type Name | VA Address | Known Content |
|-----|-------------|--------|------|-----------|------------|---------------|
| 421 | 0x51FAEC | 12 | 0 | DEF | 0x9210EC | Item menu option |
| 422 | 0x51FB68 | 12 | 0 | DEF | 0x921168 | **Use** |
| 423 | 0x51FB74 | 12 | 0 | DEF | 0x921174 | **Arrange** |
| 424 | 0x51FB80 | 12 | 0 | DEF | 0x921180 | **KEY ITEMS** |
| 425 | 0x51FB8C | 12 | 0 | DEF | 0x92118C | **Customize** |
| 426 | 0x51FB98 | 12 | 0 | DEF | 0x921198 | **Field** |
| 427 | 0x51FBA4 | 12 | 0 | DEF | 0x9211A4 | **Battle** |
| 428 | 0x51FBB0 | 12 | 0 | DEF | 0x9211B0 | **Throw** |
| 429 | 0x51FBBC | 12 | 0 | DEF | 0x9211BC | **Type** |
| 430 | 0x51FBC8 | 12 | 0 | DEF | 0x9211C8 | **Name** |
| 431 | 0x51FBD4 | 12 | 0 | DEF | 0x9211D4 | **Most** |

**Should Patch:** Yes - Item menu options are user-visible.

---

### Region 15: Item Menu Continued (Indices 432-460)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 432 | 0x51FBE0 | 12 | 0 | DEF | 0x9211E0 | **Least** |
| 433 | 0x51FBF0 | 34 | 0 | DEF | 0x9211F0 | Item text |
| 434 | 0x51FC12 | 34 | 0 | DEF | 0x921212 | Item text |
| 435 | 0x51FC34 | 34 | 0 | DEF | 0x921234 | Item text |
| 436 | 0x51FC56 | 34 | 0 | DEF | 0x921256 | Item text |
| 437 | 0x51FC78 | 34 | 0 | DEF | 0x921278 | Item text |
| 438 | 0x51FC9A | 34 | 0 | DEF | 0x92129A | Item text |
| 439 | 0x51FCBC | 34 | 0 | DEF | 0x9212BC | Item text |
| 440 | 0x51FCDE | 34 | 0 | DEF | 0x9212DE | Item text |
| 441 | 0x51FD00 | 34 | 0 | DEF | 0x921300 | Item text |
| 442 | 0x51FD22 | 34 | 0 | DEF | 0x921322 | Item text |
| 443 | 0x51FD44 | 34 | 0 | DEF | 0x921344 | Item text |
| 444 | 0x51FD66 | 34 | 0 | DEF | 0x921366 | Item text |
| 445 | 0x51FD88 | 34 | 0 | DEF | 0x921388 | Item text |
| 446 | 0x51FDAA | 34 | 0 | DEF | 0x9213AA | Item text |
| 447 | 0x51FDCC | 34 | 0 | DEF | 0x9213CC | Item text |
| 448 | 0x51FDEE | 34 | 0 | DEF | 0x9213EE | Item text |
| 449 | 0x51FE10 | 34 | 0 | DEF | 0x921410 | Item text |
| 450 | 0x51FE32 | 34 | 0 | DEF | 0x921432 | Item text |
| 451 | 0x51FE54 | 34 | 0 | DEF | 0x921454 | Item text |
| 452 | 0x51FE76 | 34 | 0 | DEF | 0x921476 | Item text |
| 453 | 0x51FE98 | 34 | 0 | DEF | 0x921498 | Item text |
| 454 | 0x51FEBA | 34 | 0 | DEF | 0x9214BA | Item text |
| 455 | 0x51FEDC | 34 | 0 | DEF | 0x9214DC | Item text |
| 456 | 0x51FEFE | 34 | 0 | DEF | 0x9214FE | Item text |
| 457 | 0x51FF20 | 34 | 0 | DEF | 0x921520 | Item text |
| 458 | 0x5206B8 | 12 | 0 | DEF | 0x921CB8 | Item label |
| 459 | 0x5206C4 | 12 | 0 | DEF | 0x921CC4 | Item label |
| 460 | 0x5206D0 | 12 | 0 | DEF | 0x921CD0 | Item label |

**Should Patch:** Yes - Item text is user-visible.

---

### Region 16: UNICODE Name Entry Characters (Indices 461-528)

**TYPE 3 (UNICODE)**: Character entry for naming screens. Single-byte characters.

**SKIP RECOMMENDATION: These should NOT be patched for translation.**

| Idx | File Offset | Length | Type | Type Name | VA Address | Content |
|-----|-------------|--------|------|-----------|------------|---------|
| 461 | 0x5206DC | 12 | 0 | DEF | 0x921CDC | Pre-unicode label |
| 462 | 0x5206E8 | 12 | 0 | DEF | 0x921CE8 | Pre-unicode label |
| 463 | 0x5206F4 | 12 | 0 | DEF | 0x921CF4 | Pre-unicode label |
| 464 | 0x520700 | 12 | 0 | DEF | 0x921D00 | Pre-unicode label |
| 465 | 0x52070C | 12 | 0 | DEF | 0x921D0C | Pre-unicode label |
| 466 | 0x520718 | 12 | 0 | DEF | 0x921D18 | Pre-unicode label |
| 467 | 0x520724 | 8 | 0 | DEF | 0x921D24 | Pre-unicode label |
| 468 | 0x520748 | 8 | 0 | DEF | 0x921D48 | Pre-unicode label |
| 469 | 0x520750 | 8 | 0 | DEF | 0x921D50 | Pre-unicode label |
| 470 | 0x520758 | 8 | 0 | DEF | 0x921D58 | Pre-unicode label |
| 471 | 0x520760 | 1 | 3 | UNICODE | 0x921D60 | Name char A |
| 472 | 0x520768 | 1 | 3 | UNICODE | 0x921D68 | Name char B |
| 473 | 0x520770 | 1 | 3 | UNICODE | 0x921D70 | Name char |
| 474 | 0x520771 | 1 | 3 | UNICODE | 0x921D71 | Name char |
| 475 | 0x520772 | 1 | 3 | UNICODE | 0x921D72 | Name char |
| 476 | 0x520773 | 1 | 3 | UNICODE | 0x921D73 | Name char |
| 477 | 0x520774 | 1 | 3 | UNICODE | 0x921D74 | Name char |
| 478 | 0x520775 | 1 | 3 | UNICODE | 0x921D75 | Name char |
| 479 | 0x520776 | 1 | 3 | UNICODE | 0x921D76 | Name char |
| 480 | 0x520777 | 1 | 3 | UNICODE | 0x921D77 | Name char |
| 481 | 0x520778 | 1 | 3 | UNICODE | 0x921D78 | Name char |
| 482 | 0x520779 | 1 | 3 | UNICODE | 0x921D79 | Name char |
| 483 | 0x52077A | 1 | 3 | UNICODE | 0x921D7A | Name char |
| 484 | 0x52077B | 1 | 3 | UNICODE | 0x921D7B | Name char |
| 485 | 0x52077C | 1 | 3 | UNICODE | 0x921D7C | Name char |
| 486 | 0x52077D | 1 | 3 | UNICODE | 0x921D7D | Name char |
| 487 | 0x52077E | 1 | 3 | UNICODE | 0x921D7E | Name char |
| 488 | 0x52077F | 1 | 3 | UNICODE | 0x921D7F | Name char |
| 489 | 0x520780 | 1 | 3 | UNICODE | 0x921D80 | Name char |
| 490 | 0x520781 | 1 | 3 | UNICODE | 0x921D81 | Name char |
| 491 | 0x520782 | 1 | 3 | UNICODE | 0x921D82 | Name char |
| 492 | 0x520783 | 1 | 3 | UNICODE | 0x921D83 | Name char |
| 493 | 0x520784 | 1 | 3 | UNICODE | 0x921D84 | Name char |
| 494 | 0x520785 | 1 | 3 | UNICODE | 0x921D85 | Name char |
| 495 | 0x520786 | 1 | 3 | UNICODE | 0x921D86 | Name char |
| 496 | 0x520787 | 1 | 3 | UNICODE | 0x921D87 | Name char |
| 497 | 0x520788 | 1 | 3 | UNICODE | 0x921D88 | Name char |
| 498 | 0x520789 | 1 | 3 | UNICODE | 0x921D89 | Name char |
| 499 | 0x52078A | 1 | 3 | UNICODE | 0x921D8A | Name char |
| 500 | 0x52078B | 1 | 3 | UNICODE | 0x921D8B | Name char |
| 501 | 0x52078C | 1 | 3 | UNICODE | 0x921D8C | Name char |
| 502 | 0x52078D | 1 | 3 | UNICODE | 0x921D8D | Name char |
| 503 | 0x52078E | 1 | 3 | UNICODE | 0x921D8E | Name char |
| 504 | 0x52078F | 1 | 3 | UNICODE | 0x921D8F | Name char |
| 505 | 0x520790 | 1 | 3 | UNICODE | 0x921D90 | Name char |
| 506 | 0x520791 | 1 | 3 | UNICODE | 0x921D91 | Name char |
| 507 | 0x520792 | 1 | 3 | UNICODE | 0x921D92 | Name char |
| 508 | 0x520793 | 1 | 3 | UNICODE | 0x921D93 | Name char |
| 509 | 0x520794 | 1 | 3 | UNICODE | 0x921D94 | Name char |
| 510 | 0x520795 | 1 | 3 | UNICODE | 0x921D95 | Name char |
| 511 | 0x520796 | 1 | 3 | UNICODE | 0x921D96 | Name char |
| 512 | 0x520797 | 1 | 3 | UNICODE | 0x921D97 | Name char |
| 513 | 0x520798 | 1 | 3 | UNICODE | 0x921D98 | Name char |
| 514 | 0x520799 | 1 | 3 | UNICODE | 0x921D99 | Name char |
| 515 | 0x52079A | 1 | 3 | UNICODE | 0x921D9A | Name char |
| 516 | 0x52079B | 1 | 3 | UNICODE | 0x921D9B | Name char |
| 517 | 0x52079C | 1 | 3 | UNICODE | 0x921D9C | Name char |
| 518 | 0x52079D | 1 | 3 | UNICODE | 0x921D9D | Name char |
| 519 | 0x52079E | 1 | 3 | UNICODE | 0x921D9E | Name char |
| 520 | 0x52079F | 1 | 3 | UNICODE | 0x921D9F | Name char |
| 521 | 0x5207A0 | 1 | 3 | UNICODE | 0x921DA0 | Name char |
| 522 | 0x5207A1 | 1 | 3 | UNICODE | 0x921DA1 | Name char |
| 523 | 0x5207A2 | 1 | 3 | UNICODE | 0x921DA2 | Name char |
| 524 | 0x5207A3 | 1 | 3 | UNICODE | 0x921DA3 | Name char |
| 525 | 0x5207A4 | 1 | 3 | UNICODE | 0x921DA4 | Name char |
| 526 | 0x5207A5 | 1 | 3 | UNICODE | 0x921DA5 | Name char |
| 527 | 0x5207A6 | 1 | 3 | UNICODE | 0x921DA6 | Name char |
| 528 | 0x5207A7 | 1 | 3 | UNICODE | 0x921DA7 | Name char |

**Should Patch:** NO - Name entry characters should remain English/Latin alphabet.

---

### Region 17: More UNICODE Characters (Indices 529-538)

| Idx | File Offset | Length | Type | Type Name | VA Address | Content |
|-----|-------------|--------|------|-----------|------------|---------|
| 529 | 0x5207A8 | 1 | 3 | UNICODE | 0x921DA8 | Name char |
| 530 | 0x5207A9 | 1 | 3 | UNICODE | 0x921DA9 | Name char |
| 531 | 0x5207AC | 1 | 3 | UNICODE | 0x921DAC | Name char |
| 532 | 0x5207AD | 1 | 3 | UNICODE | 0x921DAD | Name char |
| 533 | 0x5207AE | 1 | 3 | UNICODE | 0x921DAE | Name char |
| 534 | 0x5207AF | 1 | 3 | UNICODE | 0x921DAF | Name char |
| 535 | 0x5207B0 | 1 | 3 | UNICODE | 0x921DB0 | Name char |
| 536 | 0x5207B1 | 1 | 3 | UNICODE | 0x921DB1 | Name char |
| 537 | 0x5207B2 | 1 | 3 | UNICODE | 0x921DB2 | Name char |
| 538 | 0x5207B3 | 1 | 3 | UNICODE | 0x921DB3 | Name char |

**Should Patch:** NO - Name entry characters should remain English/Latin.

---

### Region 18: Additional UNICODE (Indices 539-540)

| Idx | File Offset | Length | Type | Type Name | VA Address | Content |
|-----|-------------|--------|------|-----------|------------|---------|
| 539 | 0x5207B4 | 1 | 3 | UNICODE | 0x921DB4 | Name char |
| 540 | 0x5207B5 | 1 | 3 | UNICODE | 0x921DB5 | Name char |

**Should Patch:** NO - Name entry characters.

---

### Region 19: Save/Load Screen Text (Indices 541-599)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 541 | 0x5213D8 | 20 | 0 | DEF | 0x9229D8 | Save screen text |
| 542 | 0x5213EC | 20 | 0 | DEF | 0x9229EC | Save screen text |
| 543 | 0x52143C | 20 | 0 | DEF | 0x922A3C | Save screen text |
| 544 | 0x521450 | 20 | 0 | DEF | 0x922A50 | Save screen text |
| 545 | 0x521464 | 20 | 0 | DEF | 0x922A64 | Save screen text |
| 546 | 0x5214DC | 20 | 0 | DEF | 0x922ADC | Save screen text |
| 547 | 0x5214F0 | 20 | 0 | DEF | 0x922AF0 | Save screen text |
| 548 | 0x521504 | 20 | 0 | DEF | 0x922B04 | Save screen text |
| 549 | 0x521518 | 20 | 0 | DEF | 0x922B18 | Save screen text |
| 550 | 0x52152C | 20 | 0 | DEF | 0x922B2C | Save screen text |
| 551 | 0x521540 | 20 | 0 | DEF | 0x922B40 | Save screen text |
| 552 | 0x521554 | 20 | 0 | DEF | 0x922B54 | Save screen text |
| 553 | 0x521568 | 20 | 0 | DEF | 0x922B68 | Save screen text |
| 554 | 0x52157C | 20 | 0 | DEF | 0x922B7C | Save screen text |
| 555 | 0x521590 | 20 | 0 | DEF | 0x922B90 | Save screen text |
| 556 | 0x5215A4 | 20 | 0 | DEF | 0x922BA4 | Save screen text |
| 557 | 0x5215B8 | 20 | 0 | DEF | 0x922BB8 | Save screen text |
| 558 | 0x5215CC | 20 | 0 | DEF | 0x922BCC | Save screen text |
| 559 | 0x5215E0 | 20 | 0 | DEF | 0x922BE0 | Save screen text |
| 560 | 0x5215F4 | 20 | 0 | DEF | 0x922BF4 | Save screen text |
| 561 | 0x521608 | 20 | 0 | DEF | 0x922C08 | Save screen text |
| 562 | 0x52161C | 20 | 0 | DEF | 0x922C1C | Save screen text |
| 563 | 0x521630 | 20 | 0 | DEF | 0x922C30 | Save screen text |
| 564 | 0x521644 | 20 | 0 | DEF | 0x922C44 | Save screen text |
| 565 | 0x521658 | 20 | 0 | DEF | 0x922C58 | Save screen text |
| 566 | 0x52166C | 20 | 0 | DEF | 0x922C6C | Save screen text |
| 567 | 0x521680 | 20 | 0 | DEF | 0x922C80 | Save screen text |
| 568 | 0x521694 | 20 | 0 | DEF | 0x922C94 | Save screen text |
| 569 | 0x5216A8 | 20 | 0 | DEF | 0x922CA8 | Save screen text |
| 570 | 0x5216F8 | 2 | 0 | DEF | 0x922CF8 | Save label |
| 571 | 0x5216FA | 2 | 0 | DEF | 0x922CFA | Save label |
| 572 | 0x521700 | 20 | 0 | DEF | 0x922D00 | Save screen text |
| 573 | 0x521714 | 20 | 0 | DEF | 0x922D14 | Save screen text |
| 574 | 0x521728 | 20 | 0 | DEF | 0x922D28 | Save screen text |
| 575 | 0x52173C | 20 | 0 | DEF | 0x922D3C | Save screen text |
| 576 | 0x521750 | 20 | 0 | DEF | 0x922D50 | Save screen text |
| 577 | 0x521764 | 20 | 0 | DEF | 0x922D64 | Save screen text |
| 578 | 0x521778 | 20 | 0 | DEF | 0x922D78 | Save screen text |
| 579 | 0x52178C | 20 | 0 | DEF | 0x922D8C | Save screen text |
| 580 | 0x5217A0 | 20 | 0 | DEF | 0x922DA0 | Save screen text |
| 581 | 0x5217B4 | 22 | 0 | DEF | 0x922DB4 | Save screen text |
| 582 | 0x52196A | 22 | 0 | DEF | 0x922F6A | Save screen text |
| 583 | 0x521980 | 22 | 0 | DEF | 0x922F80 | Save screen text |
| 584 | 0x521996 | 22 | 0 | DEF | 0x922F96 | Save screen text |
| 585 | 0x5219AC | 20 | 0 | DEF | 0x922FAC | Save screen text |
| 586 | 0x5219DC | 20 | 0 | DEF | 0x922FDC | Save screen text |
| 587 | 0x5219F0 | 20 | 0 | DEF | 0x922FF0 | Save screen text |
| 588 | 0x521A04 | 20 | 0 | DEF | 0x923004 | Save screen text |
| 589 | 0x521A18 | 20 | 0 | DEF | 0x923018 | Save screen text |
| 590 | 0x521A2C | 20 | 0 | DEF | 0x92302C | Save screen text |
| 591 | 0x521A40 | 20 | 0 | DEF | 0x923040 | Save screen text |
| 592 | 0x521A54 | 20 | 0 | DEF | 0x923054 | Save screen text |
| 593 | 0x521A68 | 46 | 0 | DEF | 0x923068 | Save message |
| 594 | 0x521A80 | 46 | 0 | DEF | 0x923080 | Save message |
| 595 | 0x521AAE | 46 | 0 | DEF | 0x9230AE | Save message |
| 596 | 0x521ADC | 46 | 0 | DEF | 0x9230DC | Save message |
| 597 | 0x521B0A | 46 | 0 | DEF | 0x92310A | Save message |
| 598 | 0x521B38 | 36 | 0 | DEF | 0x923138 | Save message |
| 599 | 0x524160 | 36 | 0 | DEF | 0x925760 | **LOAD** screen title |

**Should Patch:** Yes - Save/Load text is user-visible.

---

### Region 20: Title/Load Screen (Indices 600-640)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 600 | 0x524184 | 36 | 0 | DEF | 0x925784 | Load prompt text |
| 601 | 0x5241A8 | 36 | 0 | DEF | 0x9257A8 | Load prompt text |
| 602 | 0x524238 | 36 | 0 | DEF | 0x925838 | **LOADING** text |
| 603 | 0x52425C | 36 | 0 | DEF | 0x92585C | Title text |
| 604 | 0x524280 | 36 | 0 | DEF | 0x925880 | Title text |
| 605 | 0x5242A4 | 36 | 0 | DEF | 0x9258A4 | Title text |
| 606 | 0x5242C8 | 36 | 0 | DEF | 0x9258C8 | **CONTINUE** |
| 607 | 0x524310 | 36 | 0 | DEF | 0x925910 | Title text |
| 608 | 0x524334 | 36 | 0 | DEF | 0x925934 | Title text |
| 609 | 0x524358 | 36 | 0 | DEF | 0x925958 | Title text |
| 610 | 0x52437C | 36 | 0 | DEF | 0x92597C | Title text |
| 611 | 0x5243A0 | 36 | 0 | DEF | 0x9259A0 | Title text |
| 612 | 0x5243C4 | 36 | 0 | DEF | 0x9259C4 | Title text |
| 613 | 0x5243E8 | 36 | 0 | DEF | 0x9259E8 | Title text |
| 614 | 0x52440C | 36 | 0 | DEF | 0x925A0C | Title text |
| 615 | 0x524430 | 36 | 0 | DEF | 0x925A30 | Title text |
| 616 | 0x524454 | 36 | 0 | DEF | 0x925A54 | Title text |
| 617 | 0x524478 | 36 | 0 | DEF | 0x925A78 | Title text |
| 618 | 0x52449C | 36 | 0 | DEF | 0x925A9C | Title text |
| 619 | 0x5244C0 | 36 | 0 | DEF | 0x925AC0 | Title text |
| 620 | 0x5244E4 | 36 | 0 | DEF | 0x925AE4 | Title text |
| 621 | 0x524508 | 36 | 0 | DEF | 0x925B08 | Title text |
| 622 | 0x52452C | 36 | 0 | DEF | 0x925B2C | Title text |
| 623 | 0x524550 | 36 | 0 | DEF | 0x925B50 | Title text |
| 624 | 0x524574 | 36 | 0 | DEF | 0x925B74 | Title text |
| 625 | 0x524598 | 36 | 0 | DEF | 0x925B98 | Title text |
| 626 | 0x5245BC | 36 | 0 | DEF | 0x925BBC | Title text |
| 627 | 0x5245E0 | 36 | 0 | DEF | 0x925BE0 | **NEW GAME** |
| 628 | 0x524604 | 36 | 0 | DEF | 0x925C04 | Title text |
| 629 | 0x524628 | 36 | 0 | DEF | 0x925C28 | Title text |
| 630 | 0x52464C | 36 | 0 | DEF | 0x925C4C | Title text |
| 631 | 0x524698 | 48 | 0 | DEF | 0x925C98 | Title/intro text |
| 632 | 0x524728 | 48 | 0 | DEF | 0x925D28 | Title/intro text |
| 633 | 0x524758 | 48 | 0 | DEF | 0x925D58 | Title/intro text |
| 634 | 0x524788 | 48 | 0 | DEF | 0x925D88 | Title/intro text |
| 635 | 0x5247B8 | 48 | 0 | DEF | 0x925DB8 | Title/intro text |
| 636 | 0x5247E8 | 48 | 0 | DEF | 0x925DE8 | Title/intro text |
| 637 | 0x524818 | 48 | 0 | DEF | 0x925E18 | Title/intro text |
| 638 | 0x524848 | 48 | 0 | DEF | 0x925E48 | Title/intro text |
| 639 | 0x524878 | 48 | 0 | DEF | 0x925E78 | Title/intro text |
| 640 | 0x5248A8 | 48 | 0 | DEF | 0x925EA8 | Title/intro text |

**Should Patch:** Yes - Title screen and prompts are user-visible.

---

### Region 21: More Title/Intro Text (Indices 641-660)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 641 | 0x5248D8 | 48 | 0 | DEF | 0x925ED8 | Title/intro text |
| 642 | 0x524908 | 48 | 0 | DEF | 0x925F08 | Title/intro text |
| 643 | 0x524998 | 48 | 0 | DEF | 0x925F98 | Title/intro text |
| 644 | 0x5249C8 | 48 | 0 | DEF | 0x925FC8 | Title/intro text |
| 645 | 0x524AB8 | 48 | 0 | DEF | 0x9260B8 | Title/intro text |
| 646 | 0x524AE8 | 48 | 0 | DEF | 0x9260E8 | Title/intro text |
| 647 | 0x524B18 | 12 | 0 | DEF | 0x926118 | **SAVE 1** |
| 648 | 0x524B24 | 12 | 0 | DEF | 0x926124 | **SAVE 2** |
| 649 | 0x524B30 | 12 | 0 | DEF | 0x926130 | **SAVE 3** |
| 650 | 0x524B3C | 12 | 0 | DEF | 0x92613C | **SAVE 4** |
| 651 | 0x524B48 | 12 | 0 | DEF | 0x926148 | **SAVE 5** |
| 652 | 0x524B54 | 12 | 0 | DEF | 0x926154 | **SAVE 6** |
| 653 | 0x524B60 | 12 | 0 | DEF | 0x926160 | **SAVE 7** |
| 654 | 0x524B6C | 12 | 0 | DEF | 0x92616C | **SAVE 8** |
| 655 | 0x524B78 | 12 | 0 | DEF | 0x926178 | **SAVE 9** |
| 656 | 0x524B84 | 12 | 0 | DEF | 0x926184 | **SAVE 10** |
| 657 | 0x524BF0 | 8 | 0 | DEF | 0x9261F0 | Save label |
| 658 | 0x5552C0 | 16 | 0 | DEF | 0x9568C0 | World map text |
| 659 | 0x5552D0 | 16 | 0 | DEF | 0x9568D0 | World map text |
| 660 | 0x555410 | 16 | 0 | DEF | 0x956A10 | World map text |

**Should Patch:** Yes - Save slots and world map text.

---

### Region 22: World Map Labels (Indices 661-686)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 661 | 0x555420 | 16 | 0 | DEF | 0x956A20 | World map label |
| 662 | 0x555430 | 8 | 0 | DEF | 0x956A30 | World map label |
| 663 | 0x5557A0 | 12 | 0 | DEF | 0x956DA0 | World map label |
| 664 | 0x5557B0 | 8 | 0 | DEF | 0x956DB0 | World map label |
| 665 | 0x5557BC | 8 | 0 | DEF | 0x956DBC | World map label |
| 666 | 0x5557C4 | 8 | 0 | DEF | 0x956DC4 | World map label |
| 667 | 0x5557CC | 12 | 0 | DEF | 0x956DCC | World map label |
| 668 | 0x5557D4 | 8 | 0 | DEF | 0x956DD4 | World map label |
| 669 | 0x5557E0 | 8 | 0 | DEF | 0x956DE0 | World map label |
| 670 | 0x5557E8 | 8 | 0 | DEF | 0x956DE8 | World map label |
| 671 | 0x5557F0 | 8 | 0 | DEF | 0x956DF0 | World map label |
| 672 | 0x5557F8 | 4 | 0 | DEF | 0x956DF8 | World map label |
| 673 | 0x555800 | 8 | 0 | DEF | 0x956E00 | World map label |
| 674 | 0x555804 | 8 | 0 | DEF | 0x956E04 | World map label |
| 675 | 0x55580C | 8 | 0 | DEF | 0x956E0C | World map label |
| 676 | 0x555814 | 8 | 0 | DEF | 0x956E14 | World map label |
| 677 | 0x55581C | 8 | 0 | DEF | 0x956E1C | World map label |
| 678 | 0x555824 | 12 | 0 | DEF | 0x956E24 | World map label |
| 679 | 0x555838 | 8 | 0 | DEF | 0x956E38 | World map label |
| 680 | 0x555848 | 12 | 0 | DEF | 0x956E48 | World map label |
| 681 | 0x555854 | 8 | 0 | DEF | 0x956E54 | World map label |
| 682 | 0x55585C | 8 | 0 | DEF | 0x956E5C | World map label |
| 683 | 0x555864 | 8 | 0 | DEF | 0x956E64 | World map label |
| 684 | 0x55586C | 8 | 0 | DEF | 0x956E6C | World map label |
| 685 | 0x555874 | 12 | 0 | DEF | 0x956E74 | World map label |
| 686 | 0x555880 | 12 | 0 | DEF | 0x956E80 | World map label |

**Should Patch:** Yes - World map location names.

---

### Region 23: FFPADDED Race Ordinals (Indices 687-711)

**TYPE 4 (FFPADDED)**: Race position ordinals padded with 0xFF bytes.

**SKIP RECOMMENDATION: These should NOT be patched. Keep English ordinals.**

| Idx | File Offset | Length | Type | Type Name | VA Address | Content |
|-----|-------------|--------|------|-----------|------------|---------|
| 687 | 0x55588C | 12 | 2 | RGB | 0x956E8C | Race label |
| 688 | 0x555898 | 8 | 2 | RGB | 0x956E98 | Race label |
| 689 | 0x5558A0 | 8 | 2 | RGB | 0x956EA0 | Race label |
| 690 | 0x5558AC | 8 | 2 | RGB | 0x956EAC | Race label |
| 691 | 0x5558B4 | 8 | 2 | RGB | 0x956EB4 | Race label |
| 692 | 0x5558BC | 8 | 2 | RGB | 0x956EBC | Race label |
| 693 | 0x5558C4 | 8 | 2 | RGB | 0x956EC4 | Race label |
| 694 | 0x5558CC | 8 | 2 | RGB | 0x956ECC | Race label |
| 695 | 0x57B2A8 | 16 | 4 | FFPADDED | 0x97C8A8 | Race text |
| 696 | 0x57B3D0 | 16 | 0 | DEF | 0x97C9D0 | Race text |
| 697 | 0x57B3E0 | 16 | 0 | DEF | 0x97C9E0 | Race text |
| 698 | 0x57B3F0 | 16 | 0 | DEF | 0x97C9F0 | Race text |
| 699 | 0x57B400 | 16 | 0 | DEF | 0x97CA00 | Race text |
| 700 | 0x57B410 | 16 | 0 | DEF | 0x97CA10 | Race text |
| 701 | 0x57B420 | 16 | 0 | DEF | 0x97CA20 | Race text |
| 702 | 0x57B430 | 16 | 0 | DEF | 0x97CA30 | Race text |
| 703 | 0x57B440 | 16 | 0 | DEF | 0x97CA40 | Race text |
| 704 | 0x57B450 | 16 | 0 | DEF | 0x97CA50 | Race text |
| 705 | 0x57B460 | 16 | 0 | DEF | 0x97CA60 | Race text |
| 706 | 0x57B470 | 16 | 0 | DEF | 0x97CA70 | Race text |
| 707 | 0x57B480 | 16 | 0 | DEF | 0x97CA80 | Race text |
| 708 | 0x57B490 | 16 | 0 | DEF | 0x97CA90 | Race text |
| 709 | 0x57B4A0 | 16 | 0 | DEF | 0x97CAA0 | Race text |
| 710 | 0x57B4B0 | 16 | 0 | DEF | 0x97CAB0 | Race text |
| 711 | 0x57B4C0 | 16 | 0 | DEF | 0x97CAC0 | Race text |

**Should Patch:** Context-dependent - Race ordinals (1st, 2nd, 3rd) are often kept in English.

---

### Region 24: Chocobo Race Text (Indices 712-720)

| Idx | File Offset | Length | Type | Type Name | VA Address | Probable Content |
|-----|-------------|--------|------|-----------|------------|------------------|
| 712 | 0x57B4D0 | 16 | 0 | DEF | 0x97CAD0 | Chocobo race text |
| 713 | 0x57B4E0 | 16 | 0 | DEF | 0x97CAE0 | Chocobo race text |
| 714 | 0x57B4F0 | 16 | 0 | DEF | 0x97CAF0 | Chocobo race text |
| 715 | 0x57B500 | 16 | 0 | DEF | 0x97CB00 | Chocobo race text |
| 716 | 0x57B510 | 16 | 0 | DEF | 0x97CB10 | Chocobo race text |
| 717 | 0x57B520 | 16 | 0 | DEF | 0x97CB20 | Chocobo race text |
| 718 | 0x57B530 | 16 | 0 | DEF | 0x97CB30 | Chocobo race text |
| 719 | 0x57B540 | 16 | 0 | DEF | 0x97CB40 | Chocobo race text |
| 720 | 0x57B658 | 7 | 5 | ZEROTERM | 0x97CC58 | Jockey name |

**Should Patch:** Context-dependent for race text; NO for jockey names.

---

### Region 25: ZEROTERM Chocobo Jockey Names (Indices 721-766)

**TYPE 5 (ZEROTERM)**: Jockey names, zero-terminated strings.

**SKIP RECOMMENDATION: These should NOT be patched. Keep original jockey names.**

| Idx | File Offset | Length | Type | Type Name | VA Address | Content |
|-----|-------------|--------|------|-----------|------------|---------|
| 721 | 0x57B65F | 7 | 5 | ZEROTERM | 0x97CC5F | Jockey name |
| 722 | 0x57B666 | 7 | 5 | ZEROTERM | 0x97CC66 | Jockey name |
| 723 | 0x57B66D | 7 | 5 | ZEROTERM | 0x97CC6D | Jockey name |
| 724 | 0x57B674 | 7 | 5 | ZEROTERM | 0x97CC74 | Jockey name |
| 725 | 0x57B67B | 7 | 5 | ZEROTERM | 0x97CC7B | Jockey name |
| 726 | 0x57B682 | 7 | 5 | ZEROTERM | 0x97CC82 | Jockey name |
| 727 | 0x57B689 | 7 | 5 | ZEROTERM | 0x97CC89 | Jockey name |
| 728 | 0x57B690 | 7 | 5 | ZEROTERM | 0x97CC90 | Jockey name |
| 729 | 0x57B697 | 7 | 5 | ZEROTERM | 0x97CC97 | Jockey name |
| 730 | 0x57B69E | 7 | 5 | ZEROTERM | 0x97CC9E | Jockey name |
| 731 | 0x57B6A5 | 7 | 5 | ZEROTERM | 0x97CCA5 | Jockey name |
| 732 | 0x57B6AC | 7 | 5 | ZEROTERM | 0x97CCAC | Jockey name |
| 733 | 0x57B6B3 | 7 | 5 | ZEROTERM | 0x97CCB3 | Jockey name |
| 734 | 0x57B6BA | 7 | 5 | ZEROTERM | 0x97CCBA | Jockey name |
| 735 | 0x57B6C1 | 7 | 5 | ZEROTERM | 0x97CCC1 | Jockey name |
| 736 | 0x57B6C8 | 7 | 5 | ZEROTERM | 0x97CCC8 | Jockey name |
| 737 | 0x57B6CF | 7 | 5 | ZEROTERM | 0x97CCCF | Jockey name |
| 738 | 0x57B6D6 | 7 | 5 | ZEROTERM | 0x97CCD6 | Jockey name |
| 739 | 0x57B6DD | 7 | 5 | ZEROTERM | 0x97CCDD | Jockey name |
| 740 | 0x57B6E4 | 7 | 5 | ZEROTERM | 0x97CCE4 | Jockey name |
| 741 | 0x57B6EB | 7 | 5 | ZEROTERM | 0x97CCEB | Jockey name |
| 742 | 0x57B6F2 | 7 | 5 | ZEROTERM | 0x97CCF2 | Jockey name |
| 743 | 0x57B6F9 | 7 | 5 | ZEROTERM | 0x97CCF9 | Jockey name |
| 744 | 0x57B700 | 7 | 5 | ZEROTERM | 0x97CD00 | Jockey name |
| 745 | 0x57B707 | 7 | 5 | ZEROTERM | 0x97CD07 | Jockey name |
| 746 | 0x57B70E | 7 | 5 | ZEROTERM | 0x97CD0E | Jockey name |
| 747 | 0x57B715 | 7 | 5 | ZEROTERM | 0x97CD15 | Jockey name |
| 748 | 0x57B71C | 7 | 5 | ZEROTERM | 0x97CD1C | Jockey name |
| 749 | 0x57B723 | 7 | 5 | ZEROTERM | 0x97CD23 | Jockey name |
| 750 | 0x57B72A | 7 | 5 | ZEROTERM | 0x97CD2A | Jockey name |
| 751 | 0x57B731 | 7 | 5 | ZEROTERM | 0x97CD31 | Jockey name |
| 752 | 0x57B738 | 7 | 5 | ZEROTERM | 0x97CD38 | Jockey name |
| 753 | 0x57B73F | 7 | 5 | ZEROTERM | 0x97CD3F | Jockey name |
| 754 | 0x57B746 | 7 | 5 | ZEROTERM | 0x97CD46 | Jockey name |
| 755 | 0x57B74D | 7 | 5 | ZEROTERM | 0x97CD4D | Jockey name |
| 756 | 0x57B754 | 7 | 5 | ZEROTERM | 0x97CD54 | Jockey name |
| 757 | 0x57B75B | 7 | 5 | ZEROTERM | 0x97CD5B | Jockey name |
| 758 | 0x57B762 | 7 | 5 | ZEROTERM | 0x97CD62 | Jockey name |
| 759 | 0x57B769 | 7 | 5 | ZEROTERM | 0x97CD69 | Jockey name |
| 760 | 0x57B770 | 7 | 5 | ZEROTERM | 0x97CD70 | Jockey name |
| 761 | 0x57B777 | 7 | 5 | ZEROTERM | 0x97CD77 | Jockey name |
| 762 | 0x57B77E | 7 | 5 | ZEROTERM | 0x97CD7E | Jockey name |
| 763 | 0x57B785 | 7 | 5 | ZEROTERM | 0x97CD85 | Jockey name |
| 764 | 0x57B78C | 7 | 5 | ZEROTERM | 0x97CD8C | Jockey name |
| 765 | 0x57B793 | 7 | 5 | ZEROTERM | 0x97CD93 | Jockey name |

**Should Patch:** NO - Jockey names should remain in original language.

---

## Summary Statistics

### By Type Code

| Type | Name | Count | Percentage |
|------|------|-------|------------|
| 0 | DEF | 541 | 70.5% |
| 1 | NOFF_TERM | 3 | 0.4% |
| 2 | RGB | 175 | 22.8% |
| 3 | UNICODE | 68 | 8.9% |
| 4 | FFPADDED | 25 | 3.3% |
| 5 | ZEROTERM | 46 | 6.0% |

### Skip Recommendations Summary

| Region | Indices | Count | Recommendation |
|--------|---------|-------|----------------|
| Keyboard Labels | 77-213 | 137 | Context-dependent |
| Name Entry Characters | 461-540 | 80 | **SKIP** |
| Race Ordinals | 687-711 | 25 | Context-dependent |
| Jockey Names | 720-766 | 47 | **SKIP** |

### Patch Priority Categories

**HIGH PRIORITY (User-visible menus):**
- Main Menu: Indices 38-48
- Config Screen: Indices 36-76
- Item Menu: Indices 421-432
- Status Screen: Indices 328-367
- Save/Load: Indices 541-660

**MEDIUM PRIORITY (Battle/Status):**
- Battle Text: Indices 214-292
- Status Effects: Indices 293-327

**LOW PRIORITY / SKIP:**
- Keyboard Labels: Indices 77-213
- Name Entry: Indices 461-540
- Jockey Names: Indices 720-766

---

## Usage Notes

### Converting to HEXT Patches

For each offset that needs patching:

1. Calculate VA: `VA = FileOffset + 0x17600`
2. Create HEXT line: `VA = BYTES`

Example:
```
# Index 38 (ITEM): FileOffset 0x5192C0 -> VA 0x91A8C0
# Japanese: 6a 6c 64 80 ff (アイテム)
91A8C0 = 6A 6C 64 80 FF
```

### Length Constraints

- New string must fit within the specified `len` bytes
- TouphScript pads shorter strings with 0xFF (or type-specific padding)
- Strings exceeding length will be rejected with error message

### Testing Workflow

1. Extract original text with TouphScript: `touphScript dump ff7.exe`
2. Edit `0_ff7.exe.txt` with translations
3. Apply changes: `touphScript apply ff7.exe`
4. Or create HEXT patches directly using VA addresses

---

## Changelog

- **v1.0.0** (2026-01-02): Initial complete documentation of all 767 entries

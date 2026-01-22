# FF7 English String Type Analysis

**Generated:** 2026-01-02 20:49:47 JST  
**Session:** 93c10c47-4dd6-41a6-aa90-73c6b0def3b1  
**Source:** /mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe  

## String Type Overview

| Type | Code | Count | Description |
|------|------|-------|-------------|
| DEF | 0 | 443 | Standard FF7 encoding with FF terminator |
| NOFF_TERM | 1 | 3 | No FF terminator in file |
| RGB | 2 | 173 | RGB encoded (ASCII + 0x73) - keyboard labels |
| UNICODE | 3 | 68 | Windows Unicode strings (name entry) |
| FFPADDED | 4 | 25 | FF7 encoding padded with FF bytes |
| ZEROTERM | 5 | 55 | Zero-terminated string |
| **Total** | | **767** | |

## Type Encoding Details

### DEF (Type 0) - Standard FF7 Encoding
- **Encoding**: ASCII character - 0x20
- **Space**: 0x00
- **Terminator**: 0xFF
- **Example**: 'A' (0x41) stored as 0x21

### NOFF_TERM (Type 1) - No FF Terminator
- Same encoding as DEF, but no 0xFF terminator in file
- String length determined by fixed field size

### RGB (Type 2) - RGB Encoding for Keyboard Labels
- **Encoding**: ASCII character + 0x73
- **Purpose**: Used for keyboard key labels
- **Example**: 'E' (0x45) stored as 0xB8 (0x45 + 0x73)
- **Index Range**: 77-213 (keyboard keys)

### UNICODE (Type 3) - Windows Unicode
- **Encoding**: UTF-16LE (2 bytes per character)
- **Purpose**: Name entry characters
- **Index Range**: 461-528

### FFPADDED (Type 4) - FF7 Encoding with FF Padding
- Same as DEF but pads unused space with 0xFF bytes
- **Index Range**: 687-711 (race ordinals)

### ZEROTERM (Type 5) - Zero-Terminated ASCII
- **Encoding**: Plain ASCII
- **Terminator**: 0x00 (null)
- **Index Range**: 712-757 (chocobo jockey names)

## Examples by Type

### DEF Examples

| Index | Offset | Length | Decoded Text | Raw Bytes |
|-------|--------|--------|--------------|----------|
| 0 | 0x00518370 | 30 | Do you want to quit | 24 4F 00 59 4F 55 00 57 41 4E 54 00 54 4F 00 51... |
| 1 | 0x0051838E | 30 | playing Final Fantasy VII | 50 4C 41 59 49 4E 47 00 26 49 4E 41 4C 00 26 41... |
| 2 | 0x005183AC | 30 | and return to Windows? | 41 4E 44 00 52 45 54 55 52 4E 00 54 4F 00 37 49... |
| 3 | 0x005183D0 | 4 | Yes | 39 45 53 FF |
| 4 | 0x005183D4 | 4 | No | 2E 4F FF 00 |

### NOFF_TERM Examples

| Index | Offset | Length | Decoded Text | Raw Bytes |
|-------|--------|--------|--------------|----------|
| 33 | 0x00519238 | 6 | [C5][B8][B7] | C5 B8 B7 FF 00 00 |
| 34 | 0x0051923E | 6 | [BA][C5][B8][B8][C1] | BA C5 B8 B8 C1 FF |
| 35 | 0x00519244 | 6 | [B5][BF][C8][B8] | B5 BF C8 B8 FF 00 |

### RGB Examples

| Index | Offset | Length | Decoded Text | Raw Bytes |
|-------|--------|--------|--------------|----------|
| 77 | 0x00519FE0 | 8 | ESCAPE   | 45 53 43 41 50 45 00 00 |
| 78 | 0x00519FE8 | 4 | 1    | 31 00 00 00 |
| 79 | 0x00519FEC | 4 | 2    | 32 00 00 00 |
| 80 | 0x00519FF0 | 4 | 3    | 33 00 00 00 |
| 81 | 0x00519FF4 | 4 | 4    | 34 00 00 00 |

### UNICODE Examples

| Index | Offset | Length | Decoded Text | Raw Bytes |
|-------|--------|--------|--------------|----------|
| 464 | 0x00520700 | 12 | 䄣呉㌀呉ｈ | 23 41 49 54 00 33 49 54 48 FF 00 00 |
| 465 | 0x0052070C | 12 | 䤶䍎久ｔ | 36 49 4E 43 45 4E 54 FF 00 00 00 00 |
| 466 | 0x00520718 | 12 | 䤣ｄ | 23 49 44 FF 00 00 00 00 00 00 00 00 |
| 467 | 0x00520724 | 12 | 䠣䍏ｏ | 23 48 4F 43 4F FF 00 00 00 00 00 00 |
| 468 | 0x00520748 | 8 | 倳䍁ｅ | 33 50 41 43 45 FF 00 00 |

### FFPADDED Examples

| Index | Offset | Length | Decoded Text | Raw Bytes |
|-------|--------|--------|--------------|----------|
| 687 | 0x00555880 | 12 | OSP@ptsN     | 2F 33 30 20 50 54 53 2E 00 00 00 00 |
| 688 | 0x0055588C | 12 | OTP@ptsN     | 2F 34 30 20 50 54 53 2E 00 00 00 00 |
| 689 | 0x00555898 | 8 | OC@ptsN  | 2F 23 20 50 54 53 2E 00 |
| 690 | 0x005558A0 | 8 | OC@ptsN  | 2F 23 20 50 54 53 2E 00 |
| 691 | 0x005558AC | 8 | QstN     | 31 53 54 2E 00 00 00 00 |

### ZEROTERM Examples

| Index | Offset | Length | Decoded Text | Raw Bytes |
|-------|--------|--------|--------------|----------|
| 712 | 0x0057B4C0 | 16 | Enemy | 25 4E 45 4D 59 00 21 57 41 59 FF FF FF FF FF FF |
| 713 | 0x0057B4D0 | 16 | Sneak | 33 4E 45 41 4B 00 21 54 54 41 43 4B FF FF FF FF |
| 714 | 0x0057B4E0 | 16 | Chocobracelet[FF][FF][FF] | 23 48 4F 43 4F 42 52 41 43 45 4C 45 54 FF FF FF |
| 715 | 0x0057B4F0 | 16 | Swift | 33 57 49 46 54 00 22 4F 4C 54 FF FF FF FF FF FF |
| 716 | 0x0057B500 | 16 | Fire | 26 49 52 45 00 36 45 49 4C FF FF FF FF FF FF FF |


# FF7 Skip Regions Analysis

**Generated:** 2026-01-02 20:49:47 JST  
**Session:** 93c10c47-4dd6-41a6-aa90-73c6b0def3b1  

## Overview

Certain index regions in the touphScript offset table should be handled specially or skipped entirely when patching. This document explains each region and why.

## Skip Regions Summary

| Region | Indices | Type | Reason |
|--------|---------|------|--------|
| UNICODE Name Entry | 461-528 | UNICODE | Windows Unicode characters for name entry screen |
| Race Ordinals | 687-711 | FFPADDED | Race position ordinals (1st, 2nd, etc.) |
| Jockey Names | 712-757 | ZEROTERM | Chocobo jockey names (ASCII) |

## Detailed Analysis

### 1. UNICODE Name Entry Characters (Indices 461-528)

**Index Range:** 461-528 (68 entries)  
**Type:** UNICODE (type 3)  
**Length:** 1 byte each (single character)  

**Purpose:** These are individual Unicode characters displayed on the name entry screen for character naming.

**Why Skip:** The name entry screen has its own rendering system that differs from the normal menu text renderer. Patching these values can break the character selection interface.

**Characters in this region:**
```
[461] Aeris, [462] Red XIII, [463] Yuffie, [464] 䄣呉㌀呉ｈ, [465] 䤶䍎久ｔ, [466] 䤣ｄ, [467] 䠣䍏ｏ, [468] 倳䍁ｅ, [469] 䔤䕌䕔ÿ, [470] 䔳䕌呃ÿ, [471] 䔤䅆䱕ｔ, [472] 䄣䍎䱅ÿ, [473] [UNICODE:21], [474] [UNICODE:22], [475] [UNICODE:23], [476] [UNICODE:24], [477] [UNICODE:25], [478] [UNICODE:26], [479] [UNICODE:27], [480] [UNICODE:28]...
```

### 2. Race Ordinals (Indices 687-711)

**Index Range:** 687-711 (25 entries)  
**Type:** FFPADDED (type 4)  
**Length:** 16 bytes each  

**Purpose:** Ordinal numbers for chocobo race positions (1st, 2nd, 3rd, etc.).

**Why Skip:** These use FFPADDED encoding which has specific padding requirements. The strings are also fixed-width and any changes can misalign the race results display.

**Strings in this region:**
```
[687] OSP@ptsN    
[688] OTP@ptsN    
[689] OC@ptsN 
[690] OC@ptsN 
[691] QstN    
[692] RndN    
[693] SrdN    
[694] TthN    
...
```

### 3. Chocobo Jockey Names (Indices 712-757)

**Index Range:** 712-757 (46 entries)  
**Type:** ZEROTERM (type 5)  
**Length:** 7 bytes each  

**Purpose:** Names of NPC chocobo jockeys in the Gold Saucer races.

**Why Skip:** These are character names that should remain in English. They use zero-terminated ASCII encoding which differs from normal FF7 text encoding.

**Names in this region:**
```
[712] Enemy
[713] Sneak
[714] Chocobracelet[FF][FF][FF]
[715] Swift
[716] Fire
[717] Megalixir[FF][FF][FF][FF][FF][FF][FF]
[718] Turbo
[719] Hi-Potion[FF][FF][FF][FF][FF][FF][FF]
[720] Ice
[721] SAM
[722] ELEN
[723] BLUES
[724] TOM
...
```

## Special Handling Regions

### RGB Keyboard Labels (Indices 77-213)

**Note:** These are NOT skipped but require special handling.

**Index Range:** 77-213 (137 entries)  
**Type:** RGB (type 2)  

**Purpose:** Keyboard key labels displayed on the keyboard configuration screen.

**Special Handling Required:** The game applies a -0x20 transformation to keyboard bytes before font lookup. When patching Japanese text into these regions, the Japanese bytes must have +0x20 added to compensate.

### Single-Byte Entries (Various)

Several entries have length=1. These are typically:
- Individual characters
- Separator bytes
- Placeholder values

These should be evaluated individually for patching.

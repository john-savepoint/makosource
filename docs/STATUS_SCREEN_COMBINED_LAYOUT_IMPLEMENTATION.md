# FF7 Status Screen Combined Layout Implementation

**Created:** 2025-12-18 15:30:00 JST (Thursday)
**Last Modified:** 2025-12-19 14:25:00 JST (Friday)
**Version:** 1.2.0
**Author:** John Zealand-Doyle
**Session-ID:** f0bbe995-213d-4f7a-a0e3-3208dcde8120
**Document Enhancement:** 2025-12-19 14:25 JST - Verification pass added missing details

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Background and Motivation](#background-and-motivation)
3. [Technical Discovery Journey](#technical-discovery-journey)
4. [Memory Architecture](#memory-architecture)
5. [Complete HEXT Patch Reference](#complete-hext-patch-reference)
6. [Code Flow Analysis](#code-flow-analysis)
7. [Detailed Disassembly Listings](#detailed-disassembly-listings)
8. [Debugging Methodology](#debugging-methodology)
9. [Failed Approaches](#failed-approaches)
10. [Testing and Verification](#testing-and-verification)
11. [Screenshots and Visual Reference](#screenshots-and-visual-reference)
12. [Reference Tables](#reference-tables)
13. [Cross-References](#cross-references)
14. [Future Considerations](#future-considerations)
15. [DO NOT Repeat These Mistakes](#do-not-repeat-these-mistakes)
16. [Quick Verification Commands](#quick-verification-commands)
17. [Changelog](#changelog)

---

## Executive Summary

This document details the complete reverse engineering and implementation of the Japanese-style combined Status screen for Final Fantasy VII PC (1998/Steam). The original Japanese version displays both **Element** (elemental affinities) and **Effect** (status effect immunities/vulnerabilities) on a single page, while the English localization splits these into two separate pages.

### Key Achievement

Through binary analysis and runtime debugging with Cheat Engine, we discovered that:

1. The English executable **contains the Japanese combined rendering code** but has a `JMP` instruction that bypasses it
2. By patching 17 memory locations, we can restore the Japanese layout behavior
3. The modification requires no external code injection - pure HEXT memory patching is sufficient

### Result

A fully functional combined Element+Effect Status screen that matches the original Japanese release's layout, achieved through HEXT patches applied via FFNx.

---

## Background and Motivation

### The Problem

The English localization of FF7 changed the Status screen from a single combined page to a two-page system:

| Version | Page Structure | Navigation |
|---------|----------------|------------|
| Japanese | Single page: Element + Effect combined | Stats → Element+Effect → Stats |
| English | Two pages: Element (page 2), Effect (page 3) | Stats → Element → Effect → Stats |

### Status Screen Navigation (User-Clarified)

**Important Context:** The Status screen navigation works as follows:
- From **Main Menu**, select "Status" → **Character Select** appears
- Select a character → **Status Screen** opens on **Stats page** (page 0)
- Press **Accept (O/X)** → Cycles through pages: Stats → Element → Effect → Stats
- Press **L1/R1** → Switches between party members (stays on current page type)
- Press **Cancel** → Returns to main menu

This clarification was critical for understanding the page state variable behavior during Cheat Engine debugging.

### Visual Comparison

**Japanese Version:**
- Header: ぞくせい (Element Properties)
- Rows: こうげき, はんげん, むこう, きゅうしゅう with element icons
- Header: ついか (Effect Properties)
- Rows: こうげき, ぼうぎょ with status effect icons
- All on ONE screen with compact spacing

**English Version:**
- Page 2: "Element" with Attack, Halve, Invalid, Absorb rows (spread out)
- Page 3: "Status/Effect" with Attack, Defend rows (spread out)
- Requires page cycling to see all data

### Goal

Restore the Japanese combined layout while maintaining compatibility with the English executable and Japanese text patches already in place.

---

## Technical Discovery Journey

### Phase 1: Initial Analysis (Failed Approach)

**Initial Hypothesis:** The Japanese combined code exists dormant in the English EXE and can be enabled with a simple patch.

**What We Tried:**
1. Compared file offsets between EN EXE (0x303430) and JA EXE (+0xC00 offset)
2. Identified a `JMP` instruction in EN vs `MOV` instruction in JA at the same relative location
3. Attempted to simply change `E9 BE 01 00 00` (JMP) to `90 90 90 90 90` (NOPs)

**Result:** Game crashed during initialization.

**Why It Failed:** The bytes AFTER the JMP instruction in EN are different from JA. Simply NOPing the JMP caused the code to fall through into instructions expecting different register states.

### Phase 2: Cheat Engine Runtime Analysis

**Breakthrough:** Using Cheat Engine to find the page state variable and trace code execution.

**Discovery Process:**

1. **Finding the Page Variable:**
   - Entered Status screen → scanned for value changes
   - Cycled through pages (Stats=0, Element=1, Effect=2)
   - Narrowed down to `FF7_EN.exe+9CA488` (VA `0xDCA488`)

2. **Finding Code That Writes to Page Variable:**
   - Set breakpoint on writes to `0xDCA488`
   - Discovered three write locations:
     - `0x703D13`: Sets page to 0 (Stats)
     - `0x703C68`: Sets page to 1 (Element)
     - `0x703CBF`: Sets page to 2 (Effect)

3. **Finding Code That Reads Page Variable:**
   - Set breakpoint on reads from `0xDCA488`
   - Discovered rendering function at `0x703DF7`
   - This function checks page value and branches to different rendering code

### Phase 3: Correct Patch Development

**Key Insight:** We needed to:
1. Replace the JMP AND the subsequent instructions with JA equivalents
2. Change the page cycle to skip page 2 (Effect becomes part of page 1)
3. Adjust ALL Y-coordinate offsets to compress both sections onto one screen

---

## Memory Architecture

### Address Calculation Formula

For the FF7 English EXE .text section:

```
Virtual Address (VA) = File Offset - 0x400 + 0x401000
```

Or equivalently:
```
Virtual Address (VA) = File Offset + 0x400C00
```

**Example:**
- File offset `0x303430` → VA `0x303430 - 0x400 + 0x401000` = `0x704030`

### Key Memory Regions

| Region | File Offset Range | VA Range | Purpose |
|--------|-------------------|----------|---------|
| Status Page Logic | 0x302E00 - 0x303100 | 0x703A00 - 0x703D00 | Page cycling/input handling |
| Status Rendering | 0x3031F0 - 0x3035F0 | 0x703DF0 - 0x7041F0 | Element/Effect drawing code |
| Page State Variable | N/A (runtime) | 0xDCA488 | Current page number (0/1/2) |

### Page State Variable

**Address:** `0xDCA488` (absolute VA)

**Values:**
| Value | Meaning | Screen Content |
|-------|---------|----------------|
| 0 | Stats Page | Character statistics (Strength, Dexterity, etc.) |
| 1 | Element Page | Elemental affinities (Fire, Ice, etc.) |
| 2 | Effect Page | Status effect properties (Poison, Silence, etc.) |

**Code References:**
```asm
; Read page value (rendering function entry)
0x703DF7: A1 88 A4 DC 00    mov eax, [0xDCA488]
0x703DFC: 89 45 E0          mov [ebp-20], eax
0x703DFF: 83 7D E0 01       cmp [ebp-20], 1    ; Check if Element page
0x703E03: 74 0F             je +0x0F           ; Jump to Element rendering
0x703E05: 83 7D E0 02       cmp [ebp-20], 2    ; Check if Effect page
0x703E09: 0F 84 26 02 00 00 je +0x226          ; Jump to Effect rendering

; Write page value (page transitions)
0x703C68: C7 05 88A4DC00 01000000  mov [0xDCA488], 1  ; Set to Element
0x703CBF: C7 05 88A4DC00 02000000  mov [0xDCA488], 2  ; Set to Effect
0x703D13: C7 05 88A4DC00 00000000  mov [0xDCA488], 0  ; Set to Stats
```

---

## Complete HEXT Patch Reference

### Patch Summary Table

| # | VA | File Offset | EN Value | Patched Value | Purpose |
|---|-----|-------------|----------|---------------|---------|
| 1 | 703CC5 | 3030C5 | 02 | 00 | Skip Effect page (Element→Stats) |
| 2 | 704030-704043 | 303430-303443 | E9 BE 01... | B8 9C 00... | Enable combined rendering |
| 3 | 703E63 | 303263 | 49 | 1E | Element Halve row Y (73→30) |
| 4 | 703E82 | 303282 | 92 | 3C | Element Invalid row Y (146→60) |
| 5 | 703EA3 | 3032A3 | DB | 5A | Element Absorb row Y (219→90) |
| 6 | 703ED5 | 3032D5 | 4B | 6B | Element icons X offset (75→107) |
| 7 | 703FE7 | 3033E7 | 48 | 1E | Element icons Y multiplier (72→30) |
| 8 | 704058 | 303458 | 1E | 22 | Effect header Y (30→34) |
| 9 | 70407E | 30347E | 11 | 00 | Effect Defend row Y (17→0) |
| 10 | 704099 | 303499 | 9A | 3C | Effect section Y offset (154→60) |
| 11 | 7040A3 | 3034A3 | 11 | 00 | Effect row Y adjustment (17→0) |
| 12 | 7040CE | 3034CE | 3A | 6B | Effect icons X offset (58→107) |
| 13 | 70416D | 30356D | 47 | F4 | Line wrap threshold low (0x247→0x1F4) |
| 14 | 70416E | 30356E | 02 | 01 | Line wrap threshold high |
| 15 | 704181 | 303581 | 3A | 6B | Effect icons X (line 2) (58→107) |
| 16 | 7041A7 | 3035A7 | 9A | 3C | Effect icons Y multiplier (154→60) |

### Detailed Patch Explanations

#### Patch 1: Skip Effect Page in Menu Cycle

**Purpose:** Change page transition from Element→Effect to Element→Stats

```
VA: 703CC5
File: 3030C5
Original: 02 (set page to 2 = Effect)
Patched:  00 (set page to 0 = Stats)

Context:
703CBF: C7 05 88A4DC00 02000000  ; mov [page], 2
                      ^^
                      This byte (703CC5) is the immediate value
```

#### Patch 2: Enable Combined Rendering (Critical)

**Purpose:** Replace JMP-skip with JA combined rendering code

```
VA: 704030-704043 (20 bytes)
File: 303430-303443

Original (EN):
704030: E9 BE 01 00 00    jmp +0x1BE        ; Skip Effect rendering entirely
704035: 8B 4D 08          mov ecx, [ebp+08]
704038: 83 E9 1B          sub ecx, 0x1B
70403B: 89 4D 08          mov [ebp+08], ecx
70403E: 8B 55 0C          mov edx, [ebp+0C]
704041: 83 EA 04          sub edx, 0x04

Patched (JA equivalent):
704030: B8 9C 00 00 00    mov eax, 0x9C     ; Setup base Y offset
704035: 8B 4D 08          mov ecx, [ebp+08]
704038: 83 E9 00          sub ecx, 0x00     ; No X adjustment
70403B: 89 4D 08          mov [ebp+08], ecx
70403E: 8B 55 0C          mov edx, [ebp+0C]
704041: 03 D0             add edx, eax      ; Add base to Y position
704043: 90                nop               ; Padding

HEXT: 704030 = B8 9C 00 00 00 8B 4D 08 83 E9 00 89 4D 08 8B 55 0C 03 D0 90
```

#### Patches 3-7: Element Section Y-Compression

**Purpose:** Reduce vertical spacing between Element rows to fit combined layout

| Patch | VA | Instruction | Change | Visual Effect |
|-------|-----|-------------|--------|---------------|
| 3 | 703E63 | add edx, 0x49 → 0x1E | 73→30 pixels | Halve row moves up |
| 4 | 703E82 | add ecx, 0x92 → 0x3C | 146→60 pixels | Invalid row moves up |
| 5 | 703EA3 | add eax, 0xDB → 0x5A | 219→90 pixels | Absorb row moves up |
| 6 | 703ED5 | add eax, 0x4B → 0x6B | 75→107 pixels | Icons shift right |
| 7 | 703FE7 | imul edx, 0x48 → 0x1E | 72→30 multiplier | Icon row spacing |

#### Patches 8-11: Effect Section Positioning

**Purpose:** Position Effect section below compressed Element section

| Patch | VA | Instruction | Change | Visual Effect |
|-------|-----|-------------|--------|---------------|
| 8 | 704058 | sub eax, 0x1E → 0x22 | Header position | ついか label position |
| 9 | 70407E | sub eax, 0x11 → 0x00 | Remove offset | ぼうぎょ row alignment |
| 10 | 704099 | add ecx, 0x9A → 0x3C | 154→60 pixels | Main section Y offset |
| 11 | 7040A3 | sub edx, 0x11 → 0x00 | Remove offset | Icon row alignment |

#### Patches 12-16: Effect Icons Layout

**Purpose:** Position status effect icons and configure line wrapping

| Patch | VA | Instruction | Change | Visual Effect |
|-------|-----|-------------|--------|---------------|
| 12 | 7040CE | add ecx, 0x3A → 0x6B | 58→107 pixels | Icons X start position |
| 13-14 | 70416D-E | cmp eax, 0x247 → 0x1F4 | 583→500 pixels | Line wrap threshold |
| 15 | 704181 | add edx, 0x3A → 0x6B | 58→107 pixels | Second line X position |
| 16 | 7041A7 | imul edx, 0x9A → 0x3C | 154→60 multiplier | Row Y spacing |

---

## Code Flow Analysis

### Status Screen Rendering Function

**Entry Point:** VA `0x703DF4` (File `0x3031F4`)

```
Function Prologue:
703DF4: 55                push ebp
703DF5: 8B EC             mov ebp, esp
703DF7: 83 EC 28          sub esp, 0x28
703DFA: A1 88 A4 DC 00    mov eax, [0xDCA488]  ; Load page number

Page Routing:
703DFF: 83 7D E0 01       cmp [ebp-20], 1      ; Page 1 (Element)?
703E03: 74 0F             je 0x703E14          ; → Element rendering
703E05: 83 7D E0 02       cmp [ebp-20], 2      ; Page 2 (Effect)?
703E09: 0F 84 26 02 00 00 je 0x704030          ; → Effect rendering
703E0F: E9 DF 03 00 00    jmp 0x7041F3         ; → Function exit

Element Rendering (0x703E14 - 0x70402F):
  - Draw "ぞくせい" header
  - Draw こうげき/はんげん/むこう/きゅうしゅう labels
  - Loop: Draw element icons for each row

Effect Rendering (0x704030 - 0x7041F2):
  - [PATCHED] Now continues from Element rendering
  - Draw "ついか" header
  - Draw こうげき/ぼうぎょ labels
  - Loop: Draw status effect icons with line wrapping

Function Exit:
7041F3: 8B E5             mov esp, ebp
7041F5: 5D                pop ebp
7041F6: C3                ret
```

### Page Cycling Logic

**Location:** VA `0x703C00` - `0x703D50`

```
Button Press Handler:
703C2C: 8B 0D 88 A4 DC 00    mov ecx, [0xDCA488]  ; Get current page
703C32: 89 4D F0             mov [ebp-10], ecx
703C35: 83 7D F0 00          cmp [ebp-10], 0      ; On Stats page?
703C39: 75 xx                jne check_page_1
        ; Accept pressed on Stats → go to Element
703C68: C7 05 88A4DC00 01... mov [0xDCA488], 1

check_page_1:
703C83: 83 7D F0 01          cmp [ebp-10], 1      ; On Element page?
703C87: 75 xx                jne check_page_2
        ; Accept pressed on Element → go to Effect (PATCHED to Stats)
703CBF: C7 05 88A4DC00 02... mov [0xDCA488], 2  ; [PATCHED: 02→00]

check_page_2:
703CD1: 83 7D F0 02          cmp [ebp-10], 2      ; On Effect page?
        ; Accept pressed on Effect → go to Stats
703D13: C7 05 88A4DC00 00... mov [0xDCA488], 0
```

---

## Detailed Disassembly Listings

This section provides complete disassembly of the key functions for reference and future modifications.

### Status Screen Rendering Function (Complete)

**Function:** `StatusScreen_RenderElementEffectPage`
**Location:** VA `0x703DF4` - `0x7041F6` (File `0x3031F4` - `0x3035F6`)
**Size:** 1026 bytes

```asm
; ============================================================================
; FUNCTION PROLOGUE
; ============================================================================
703DF4: 55                      push ebp
703DF5: 8B EC                   mov ebp, esp
703DF7: 83 EC 28                sub esp, 0x28          ; Allocate 40 bytes local

; ============================================================================
; PAGE ROUTING - Determine which page to render
; ============================================================================
703DFA: A1 88 A4 DC 00          mov eax, [0xDCA488]    ; Load page state variable
703DFF: 89 45 E0                mov [ebp-20], eax      ; Store in local
703E02: 83 7D E0 01             cmp dword ptr [ebp-20], 1
703E06: 74 0F                   je 703E17              ; If page==1, render Element
703E08: 83 7D E0 02             cmp dword ptr [ebp-20], 2
703E0C: 0F 84 1E 02 00 00       je 704030              ; If page==2, render Effect
703E12: E9 DF 03 00 00          jmp 7041F6             ; Else exit (page 0 = Stats)

; ============================================================================
; ELEMENT SECTION RENDERING (Page 1)
; VA: 0x703E17 - 0x70402F
; ============================================================================

; --- Draw "ぞくせい" header ---
703E17: 68 CD CC CC 3D          push 3DCCCCCD          ; Float parameter
703E1C: 6A 05                   push 5                 ; Parameter
703E1E: 68 C0 07 92 00          push offset "ぞくせい" ; VA 0x9207C0
703E23: 8B 4D 0C                mov ecx, [ebp+0C]      ; Y base position
703E26: 83 E9 22                sub ecx, 0x22          ; Adjust Y (-34)
703E29: 51                      push ecx
703E2A: 8B 55 08                mov edx, [ebp+08]      ; X base position
703E2D: 83 EA 1B                sub edx, 0x1B          ; Adjust X (-27)
703E30: 52                      push edx
703E31: E8 D0 1C FF FF          call 705B06            ; DrawText function

; --- Draw "こうげき" label (Attack row) ---
703E36: 83 C4 14                add esp, 0x14          ; Clean stack
703E39: 68 CD CC CC 3D          push 3DCCCCCD
703E3E: 6A 05                   push 5
703E40: 68 DE 07 92 00          push offset "こうげき" ; VA 0x9207DE
703E45: 8B 45 0C                mov eax, [ebp+0C]
703E48: 50                      push eax               ; Y position (no adjustment)
703E49: 8B 4D 08                mov ecx, [ebp+08]
703E4C: 51                      push ecx               ; X position
703E4D: E8 B4 1C FF FF          call 705B06

; --- Draw "はんげん" label (Halve row) ---
703E52: 83 C4 14                add esp, 0x14
703E55: 68 CD CC CC 3D          push 3DCCCCCD
703E5A: 6A 05                   push 5
703E5C: 68 FC 07 92 00          push offset "はんげん" ; VA 0x9207FC
703E61: 8B 55 0C                mov edx, [ebp+0C]
703E64: 83 C2 49                add edx, 0x49          ; Y offset +73 [PATCHED: 0x1E = +30]
703E67: 52                      push edx
703E68: 8B 45 08                mov eax, [ebp+08]
703E6B: 50                      push eax
703E6C: E8 95 1C FF FF          call 705B06

; --- Draw "むこう" label (Invalid row) ---
703E71: 83 C4 14                add esp, 0x14
703E74: 68 CD CC CC 3D          push 3DCCCCCD
703E79: 6A 05                   push 5
703E7B: 68 0B 08 92 00          push offset "むこう"   ; VA 0x92080B
703E80: 8B 4D 0C                mov ecx, [ebp+0C]
703E83: 81 C1 92 00 00 00       add ecx, 0x92          ; Y offset +146 [PATCHED: 0x3C = +60]
703E89: 51                      push ecx
703E8A: 8B 55 08                mov edx, [ebp+08]
703E8D: 52                      push edx
703E8E: E8 73 1C FF FF          call 705B06

; --- Draw "きゅうしゅう" label (Absorb row) ---
703E93: 83 C4 14                add esp, 0x14
703E96: 68 CD CC CC 3D          push 3DCCCCCD
703E9B: 6A 05                   push 5
703E9D: 68 1A 08 92 00          push offset "きゅうしゅう" ; VA 0x92081A
703EA2: 8B 45 0C                mov eax, [ebp+0C]
703EA5: 05 DB 00 00 00          add eax, 0xDB          ; Y offset +219 [PATCHED: 0x5A = +90]
703EAA: 50                      push eax
703EAB: 8B 4D 08                mov ecx, [ebp+08]
703EAE: 51                      push ecx
703EAF: E8 52 1C FF FF          call 705B06

; --- Element Icons Loop Setup ---
703EB4: 83 C4 14                add esp, 0x14
703EB7: C7 45 E8 00 00 00 00    mov dword ptr [ebp-18], 0  ; Loop counter = 0
703EBE: EB 09                   jmp 703EC9

; --- Element Icons Loop ---
703EC0: 8B 55 E8                mov edx, [ebp-18]
703EC3: 83 C2 01                add edx, 1
703EC6: 89 55 E8                mov [ebp-18], edx      ; counter++

703EC9: 83 7D E8 04             cmp dword ptr [ebp-18], 4
703ECD: 0F 8D 60 01 00 00       jge 704033             ; If counter >= 4, exit loop

703ED3: 8B 45 08                mov eax, [ebp+08]
703ED6: 83 C0 4B                add eax, 0x4B          ; X base offset +75 [PATCHED: 0x6B = +107]
703ED9: 89 45 FC                mov [ebp-04], eax      ; Store adjusted X

; ... [Icon rendering loop continues - draws 8 element icons per row]
; ... [Loop iterates 4 times for Attack/Halve/Invalid/Absorb rows]

; --- Element Icon Y-Spacing Calculation ---
703FE5: 8B 55 E8                mov edx, [ebp-18]      ; Get row index
703FE8: 6B D2 48                imul edx, edx, 0x48    ; Y = row * 72 [PATCHED: 0x1E = row * 30]
703FEB: 8B 45 0C                mov eax, [ebp+0C]
703FEE: 03 C2                   add eax, edx           ; Y = base + (row * spacing)

; ============================================================================
; EFFECT SECTION RENDERING (Page 2 or continuation from Element)
; VA: 0x704030 - 0x7041F2
; ============================================================================

; --- Original EN code (skips Effect rendering): ---
; 704030: E9 BE 01 00 00          jmp 7041F3           ; Skip to function exit

; --- PATCHED code (JA equivalent - enables Effect rendering): ---
704030: B8 9C 00 00 00          mov eax, 0x9C          ; Base Y offset = 156
704035: 8B 4D 08                mov ecx, [ebp+08]      ; Load X base
704038: 83 E9 00                sub ecx, 0x00          ; No X adjustment [PATCHED from 0x1B]
70403B: 89 4D 08                mov [ebp+08], ecx
70403E: 8B 55 0C                mov edx, [ebp+0C]      ; Load Y base
704041: 03 D0                   add edx, eax           ; Y = base + 156 [PATCHED from sub edx, 4]
704043: 90                      nop                    ; Padding byte

; --- Draw "ついか" header ---
704044: 89 55 0C                mov [ebp+0C], edx
704047: 68 17 D9 CE 3D          push 3DCED917
70404C: 6A 05                   push 5
70404E: 68 CF 07 92 00          push offset "ついか"   ; VA 0x9207CF
704053: 8B 45 0C                mov eax, [ebp+0C]
704056: 83 E8 1E                sub eax, 0x1E          ; Y adjustment -30 [PATCHED: 0x22 = -34]
704059: 50                      push eax
70405A: 8B 4D 08                mov ecx, [ebp+08]
70405D: 83 E9 17                sub ecx, 0x17          ; X adjustment -23
704060: 51                      push ecx
704061: E8 9D 1A FF FF          call 705B06

; --- Draw "こうげき" label (Attack row for Effects) ---
704066: 83 C4 14                add esp, 0x14
704069: 68 17 D9 CE 3D          push 3DCED917
70406E: 6A 05                   push 5
704070: 68 DE 07 92 00          push offset "こうげき"
704075: 8B 55 0C                mov edx, [ebp+0C]
704078: 52                      push edx
704079: 8B 45 08                mov eax, [ebp+08]
70407C: 83 E8 11                sub eax, 0x11          ; X adjustment -17 [PATCHED: 0x00]
70407F: 50                      push eax
704080: E8 7E 1A FF FF          call 705B06

; --- Draw "ぼうぎょ" label (Defend row) ---
704085: 83 C4 14                add esp, 0x14
704088: 68 17 D9 CE 3D          push 3DCED917
70408D: 6A 05                   push 5
70408F: 68 ED 07 92 00          push offset "ぼうぎょ" ; VA 0x9207ED
704094: 8B 4D 0C                mov ecx, [ebp+0C]
704097: 81 C1 9A 00 00 00       add ecx, 0x9A          ; Y offset +154 [PATCHED: 0x3C = +60]
70409D: 51                      push ecx
70409E: 8B 55 08                mov edx, [ebp+08]
7040A1: 83 EA 11                sub edx, 0x11          ; X adjustment -17 [PATCHED: 0x00]
7040A4: 52                      push edx
7040A5: E8 59 1A FF FF          call 705B06

; --- Status Effect Icons Loop Setup ---
7040AA: 83 C4 14                add esp, 0x14
7040AD: C7 45 E8 00 00 00 00    mov dword ptr [ebp-18], 0

; ... [Status effect icon rendering loop]
; ... [Includes line wrap logic at pixel threshold]

; --- Line Wrap Threshold Check ---
70416B: 8B 45 F0                mov eax, [ebp-10]      ; Get current X position
70416E: 03 45 FC                add eax, [ebp-04]
704171: 3D 47 02 00 00          cmp eax, 0x247         ; Compare with 583 [PATCHED: 0x1F4 = 500]
704176: 7E 12                   jle short 70418A       ; If <= threshold, continue on same line

; --- Effect Icon Y-Spacing Calculation ---
7041A5: 8B 55 E8                mov edx, [ebp-18]
7041A8: 69 D2 9A 00 00 00       imul edx, edx, 0x9A    ; Y = row * 154 [PATCHED: 0x3C = row * 60]
7041AE: 8B 45 0C                mov eax, [ebp+0C]
7041B1: 03 C2                   add eax, edx

; ============================================================================
; FUNCTION EPILOGUE
; ============================================================================
7041F3: 8B E5                   mov esp, ebp
7041F5: 5D                      pop ebp
7041F6: C3                      ret
```

### Page Cycling Function (Complete)

**Function:** `StatusScreen_HandlePageInput`
**Location:** VA `0x703AE0` - `0x703D50` (File `0x302EE0` - `0x303150`)
**Size:** 624 bytes

```asm
; ============================================================================
; PAGE INPUT HANDLER - Process Accept button presses to cycle pages
; ============================================================================

; --- Check if on Stats page (page 0) ---
703C2C: 8B 0D 88 A4 DC 00       mov ecx, [0xDCA488]    ; Load current page
703C32: 89 4D F0                mov [ebp-10], ecx
703C35: 83 7D F0 00             cmp dword ptr [ebp-10], 0
703C39: 75 48                   jne 703C83             ; If not Stats, check Element

; --- Stats page: Accept → go to Element page ---
703C3B: ; ... button check code ...
703C60: E8 A5 1B 04 00          call 74580A            ; Play menu sound
703C65: 83 C4 04                add esp, 4
703C68: C7 05 88 A4 DC 00 01 00 00 00
                                mov dword ptr [0xDCA488], 1  ; Set page = 1 (Element)
703C72: EB 2E                   jmp 703CA2

; --- Check if on Element page (page 1) ---
703C83: 83 7D F0 01             cmp dword ptr [ebp-10], 1
703C87: 75 35                   jne 703CBE             ; If not Element, check Effect

; --- Element page: Accept → go to Effect page (PATCHED: go to Stats) ---
703C89: ; ... button check code ...
703CB7: E8 4E 1B 04 00          call 74580A            ; Play menu sound
703CBC: 83 C4 04                add esp, 4
703CBF: C7 05 88 A4 DC 00 02 00 00 00
                                mov dword ptr [0xDCA488], 2  ; Set page = 2 (Effect)
                                ; [PATCHED: byte at 703CC5 changed from 02 to 00]
                                ; Result: Sets page = 0 (Stats) instead
703CC9: EB 2E                   jmp 703CF9

; --- Check if on Effect page (page 2) ---
703CBE: 83 7D F0 02             cmp dword ptr [ebp-10], 2
703CC2: 75 35                   jne 703CF9             ; If not Effect, skip

; --- Effect page: Accept → go to Stats page ---
703CC4: ; ... button check code ...
703D0B: E8 FA 1A 04 00          call 74580A            ; Play menu sound
703D10: 83 C4 04                add esp, 4
703D13: C7 05 88 A4 DC 00 00 00 00 00
                                mov dword ptr [0xDCA488], 0  ; Set page = 0 (Stats)
703D1D: EB 2E                   jmp 703D4D
```

### Text String References

**Location of Japanese text strings used by the Status screen:**

| VA | File Offset | String | Purpose |
|----|-------------|--------|---------|
| 0x9207C0 | 0x51F1C0 | ぞくせい | Element section header |
| 0x9207CF | 0x51F1CF | ついか | Effect section header |
| 0x9207DE | 0x51F1DE | こうげき | Attack row label |
| 0x9207ED | 0x51F1ED | ぼうぎょ | Defend row label |
| 0x9207FC | 0x51F1FC | はんげん | Halve row label |
| 0x92080B | 0x51F20B | むこう | Invalid row label |
| 0x92081A | 0x51F21A | きゅうしゅう | Absorb row label |

---

## Debugging Methodology

### Tools Used

1. **Cheat Engine 7.x** - Runtime memory scanning and breakpoints
2. **HxD** - Hex editor for binary comparison
3. **xxd** (Linux) - Command-line hex dumps
4. **Python** - Address calculations and byte comparisons

### Step-by-Step Process

#### 1. Find Page State Variable

```
1. Launch FF7, enter Status screen
2. In Cheat Engine, attach to ff7_en.exe
3. On Stats page: Scan for value "0" (byte)
4. Press Accept to go to Element page
5. Next scan for value "1"
6. Press Accept to go to Effect page
7. Next scan for value "2"
8. Press Accept to return to Stats
9. Next scan for value "0"
10. Result: FF7_EN.exe+9CA488 (VA: 0xDCA488)
```

#### 2. Find Code That Accesses Variable

```
1. Right-click address in Cheat Engine
2. Select "Find out what writes to this address"
3. Cycle through pages, note each instruction that writes
4. Repeat with "Find out what accesses this address" for reads
```

#### 3. Binary Comparison Technique

```bash
# Dump EN bytes at suspected location
xxd -s 0x303430 -l 64 ff7_en.exe

# Dump JA bytes at equivalent location (+0xC00 offset for JA)
xxd -s 0x304030 -l 64 ff7_ja.exe

# Compare side by side
diff <(xxd -s 0x303430 -l 64 ff7_en.exe) \
     <(xxd -s 0x304030 -l 64 ff7_ja.exe)
```

#### 4. Address Calculation

```python
def file_to_va(file_offset):
    """Convert file offset to virtual address for .text section"""
    return file_offset - 0x400 + 0x401000

def va_to_file(va):
    """Convert virtual address to file offset"""
    return va - 0x401000 + 0x400

# Example
print(f"File 0x303430 → VA 0x{file_to_va(0x303430):X}")  # → 0x704030
```

---

## Failed Approaches

### Approach 1: Simple NOP Patch

**What:** Replace `JMP +0x1BE` with NOPs to fall through to Effect code.

**HEXT:**
```
704030 = 90 90 90 90 90
```

**Result:** Crash at 0x704038

**Why It Failed:** The code after the JMP in EN expects different register states than when falling through from Element rendering. The instruction `mov ecx, [ebp+08]` loaded garbage because the stack frame was set up differently.

### Approach 2: Wrong VA Calculations

**What:** Initially calculated some VAs incorrectly, targeting wrong bytes.

**Example Error:**
- Thought `704097` was the immediate value in `add ecx, 0x9A`
- Actually `704097` is the start of the instruction (`81`)
- Correct target is `704099` (the `9A` byte)

**Lesson:** Always verify instruction boundaries before patching:
```
81 C1 9A 00 00 00  = add ecx, 0x0000009A
^^ ^^ ^^
|  |  +-- Immediate value at offset +2
|  +-- ModR/M byte
+-- Opcode
```

### Approach 3: Partial Patches

**What:** Applied only the critical code path patch without Y-coordinate adjustments.

**Result:** Both sections rendered but overlapped completely.

**Why:** The EN code uses larger Y-offsets (designed for spread across 2 pages). Without compressing these, both sections draw at the same vertical positions.

### Approach 4: Wrong Line Wrap Threshold (Iterative)

**What:** Tuning the status icon line wrap threshold required multiple iterations.

**Iteration History:**
| Attempt | Value | Pixels | Result |
|---------|-------|--------|--------|
| Original EN | 0x247 | 583 | Wrap too late (13+ icons per line) |
| JA default | 0x227 | 551 | Still wrapped too late for our layout |
| Too aggressive | 0x1C0 | 448 | Wrapped too early (only ~8 icons per line) |
| **Final** | **0x1F4** | **500** | Balanced wrap (~11 icons per line) |

**User Preference:** The user explicitly preferred our 2-column sub-label arrangement over the Japanese 3-column layout, which allowed more flexibility in the line wrap threshold tuning.

### Approach 5: Initial Crash from Y-offset Patches

**What:** First attempt at Y-coordinate patches caused crash at `0x704038`.

**Symptoms:** FFNx.log showed crash at instruction after our patched area.

**Why It Failed:** Patched address `704097` when the actual immediate value byte was at `704099`. The instruction `81 C1 9A 00 00 00` starts at `704097`, but the `9A` value we needed to change is at offset +2.

**Lesson:** For multi-byte instructions, always locate the exact byte position of the immediate value:
```
Address:  704097  704098  704099  70409A  70409B  70409C
Byte:        81      C1      9A      00      00      00
Purpose:  Opcode  ModRM   Imm[0]  Imm[1]  Imm[2]  Imm[3]
```

---

## Testing and Verification

### Test Checklist

| Test | Status | Notes |
|------|--------|-------|
| Game launches without crash | ✅ Pass | No initialization errors |
| Stats page displays correctly | ✅ Pass | No changes to Stats page |
| Element+Effect combined page | ✅ Pass | Both sections visible |
| Page cycling (Stats→Combined→Stats) | ✅ Pass | Smooth transitions |
| L1/R1 character switching | ✅ Pass | Works on combined page |
| Equipped materia effects display | ⚠️ Untested | Need materia with elemental/status |
| Menu exit | ✅ Pass | Returns to main menu |
| Save/Load | ✅ Pass | No corruption |
| Battle entry/exit | ⚠️ Untested | Should not affect |

### Unexpected Side Effects (User-Reported)

**Title Screen Alignment Fix:** The user reported that applying the Status screen patches also fixed a previously existing title screen alignment issue. This suggests the patched memory region may share some coordinate calculation code with the title screen, or there was a cascading effect from the HEXT file structure. This was an unintended but positive side effect.

### Visual Verification

The combined layout should show:

```
┌─────────────────────────────────────────────────────────┐
│  [Character Portrait]  経験値: XXXXp    [ステータス]    │
│  LV XX                 つぎのレベルまであと: XXXp       │
│  HP XXX/XXX                                             │
│  MP XX/XX              リミットレベルX                  │
├─────────────────────────────────────────────────────────┤
│  ぞくせい                                               │
│    こうげき    炎 冷 雷 土 毒 重 水 風 聖               │
│    はんげん    炎 冷 雷 土 毒 重 水 風 聖               │
│    むこう      炎 冷 雷 土 毒 重 水 風 聖               │
│    きゅうしゅう 炎 冷 雷 土 毒 重 水 風 聖              │
│  ついか                                                 │
│    こうげき    死 瀕 眠 毒 悲 怒 乱 黙 速 遅 止 蛙 小   │
│                徐 石 回 物 魔 反 防 宣 操 闘 無 マ 暗   │
│    ぼうぎょ    死 瀕 眠 毒 悲 怒 乱 黙 速 遅 止 蛙 小   │
│                徐 石 回 物 魔 反 防 宣 操 闘 無 マ 暗   │
└─────────────────────────────────────────────────────────┘
```

---

## Reference Tables

### EN vs JA Byte Comparison (Critical Section)

**File Offset 0x303430 / 0x304030 (20 bytes):**

| Offset | EN Bytes | EN Instruction | JA Bytes | JA Instruction |
|--------|----------|----------------|----------|----------------|
| +0 | E9 BE 01 00 00 | jmp +0x1BE | B8 9C 00 00 00 | mov eax, 0x9C |
| +5 | 8B 4D 08 | mov ecx, [ebp+08] | 8B 4D 08 | mov ecx, [ebp+08] |
| +8 | 83 E9 1B | sub ecx, 0x1B | 83 E9 00 | sub ecx, 0x00 |
| +B | 89 4D 08 | mov [ebp+08], ecx | 89 4D 08 | mov [ebp+08], ecx |
| +E | 8B 55 0C | mov edx, [ebp+0C] | 8B 55 0C | mov edx, [ebp+0C] |
| +11 | 83 EA 04 | sub edx, 0x04 | 03 D0 | add edx, eax |
| +14 | - | - | 90 | nop |

### Y-Coordinate Value Reference

| Label | EN Y-Offset | JA Y-Offset | Difference |
|-------|-------------|-------------|------------|
| Element: Halve | 73 (0x49) | 30 (0x1E) | -43 pixels |
| Element: Invalid | 146 (0x92) | 60 (0x3C) | -86 pixels |
| Element: Absorb | 219 (0xDB) | 90 (0x5A) | -129 pixels |
| Element Icon Spacing | 72 (0x48) | 30 (0x1E) | -42 pixels/row |
| Effect Section Base | 154 (0x9A) | 60 (0x3C) | -94 pixels |
| Effect Icon Spacing | 154 (0x9A) | 60 (0x3C) | -94 pixels/row |

### Status Effect Icons (26 total)

| JP | EN | Index | JP | EN | Index |
|----|----|----|----|----|-----|
| 死 | Death | 0 | 小 | Small | 12 |
| 瀕 | Near-death | 1 | 徐 | Slow-numb | 13 |
| 眠 | Sleep | 2 | 石 | Petrify | 14 |
| 毒 | Poison | 3 | 回 | Regen | 15 |
| 悲 | Sadness | 4 | 物 | Barrier | 16 |
| 怒 | Fury | 5 | 魔 | MBarrier | 17 |
| 乱 | Confusion | 6 | 反 | Reflect | 18 |
| 黙 | Silence | 7 | 防 | Shield | 19 |
| 速 | Haste | 8 | 宣 | D.Sentence | 20 |
| 遅 | Slow | 9 | 操 | Manipulate | 21 |
| 止 | Stop | 10 | 闘 | Berserk | 22 |
| 蛙 | Frog | 11 | 無 | Peerless | 23 |
| | | | マ | Paralysis | 24 |
| | | | 暗 | Darkness | 25 |

---

## Screenshots and Visual Reference

This section documents the visual progression of the implementation and provides reference screenshots.

### Screenshot Archive Locations

All screenshots from the development session are stored at:

```
Windows Path: C:\Users\johnz\OneDrive - Save Point Pty Ltd\Documents\ShareX\Screenshots\2025-12\
WSL Path:     /mnt/c/Users/johnz/OneDrive - Save Point Pty Ltd/Documents/ShareX/Screenshots/2025-12/
```

### Reference Screenshots

| Screenshot | Description | Stage |
|------------|-------------|-------|
| `Status_Both_JP.png` | Original Japanese version showing combined layout | Reference |
| `Status_Elemental_ENG.png` | English Element page (before modification) | Before |
| `Status_Status_ENG.png` | English Effect page (before modification) | Before |
| `ff7_en_gkmKgvzIuy.png` | First attempt - NOP patch caused overlap | Failed |
| `ff7_en_UEej7nD8Dd.png` | Second attempt - JA code transplant working | Progress |
| `ff7_en_RrrVtvFYRg.png` | Labels compressed but icons still spread | Progress |
| `ff7_en_M8PyhABuMX.png` | Element section fully compressed | Progress |
| `ff7_en_k2Z4fmOrp5-1.png` | Annotated screenshot showing sections | Debug |
| `ff7_en_EGQLElBF9O.png` | Line wrap occurring but at wrong position | Progress |
| `ff7_en_SHKqocUSeC.png` | Near-final with X offset fix | Progress |
| `ff7_en_V00TgaipGU.png` | **Final result** - Combined layout working | Complete |

### Cheat Engine Screenshots

| Screenshot | Description |
|------------|-------------|
| `cheatengine-i386_P66BnYjOUF.png` | Page state = 0 (Stats page) |
| `cheatengine-i386_jWt0tULbIU.png` | Page state = 1 (Element page) |
| `cheatengine-i386_qICTfmMvmp.png` | Page state = 2 (Effect page) |
| `cheatengine-i386_PMFihwRro6.png` | Memory scan results |

### Visual Layout Comparison

**Before (English - 2 pages):**
```
┌─ Page 2: Element ─────────────────┐    ┌─ Page 3: Effect ──────────────────┐
│  Element                          │    │  Status/Effect                    │
│    Attack    [8 element icons]    │    │    Attack    [26 status icons     │
│                                   │    │               wrapped to 2 lines] │
│    Halve     [8 element icons]    │    │                                   │
│                                   │    │    Defend    [26 status icons     │
│    Invalid   [8 element icons]    │    │               wrapped to 2 lines] │
│                                   │    │                                   │
│    Absorb    [8 element icons]    │    │                                   │
└───────────────────────────────────┘    └───────────────────────────────────┘
```

**After (Japanese-style - 1 page):**
```
┌─ Combined Element + Effect ───────────────────────────────────────────────┐
│  ぞくせい                                                                 │
│    こうげき    炎 冷 雷 土 毒 重 水 風 聖                                 │
│    はんげん    炎 冷 雷 土 毒 重 水 風 聖                                 │
│    むこう      炎 冷 雷 土 毒 重 水 風 聖                                 │
│    きゅうしゅう 炎 冷 雷 土 毒 重 水 風 聖                                │
│  ついか                                                                   │
│    こうげき    死 瀕 眠 毒 悲 怒 乱 黙 速 遅 止 蛙 小                     │
│                徐 石 回 物 魔 反 防 宣 操 闘 無 マ 暗                     │
│    ぼうぎょ    死 瀕 眠 毒 悲 怒 乱 黙 速 遅 止 蛙 小                     │
│                徐 石 回 物 魔 反 防 宣 操 闘 無 マ 暗                     │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-References

This section links to related documentation and resources within the project.

### Project Documentation

| Document | Path | Relevance |
|----------|------|-----------|
| Menu Text Address Map | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/MENU_TEXT_ADDRESS_MAP.md` | Contains Status screen text string addresses |
| Project Overview | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/PROJECT_OVERVIEW.md` | Overall project context |
| Implementation Status | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/IMPLEMENTATION_STATUS.md` | Tracks all menu patches |
| FFNx Japanese Master Bible | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` | Comprehensive implementation guide |

### HEXT Patch Files

| File | Path | Description |
|------|------|-------------|
| Japanese Menu Patches | `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/ja/japanese_menu.txt` | Contains all Status screen patches |

### Game Engine Reference

| Document | Path | Relevance |
|----------|------|-----------|
| Menu Module | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/reference/game_engine/extracted_major_sections/04_MENU_MODULE.md` | Menu system architecture |
| FF7 Game Engine | `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/reference/game_engine/GameEngine.md` | General engine documentation |

### Executable Locations

| File | Path | Purpose |
|------|------|---------|
| English EXE | `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe` | Target for patches |
| Japanese EXE | `/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe` | Reference for byte extraction |
| FFNx Log | `/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/FFNx.log` | Crash debugging |

### External Resources

| Resource | URL | Purpose |
|----------|-----|---------|
| Qhimm Forums | https://forums.qhimm.com/ | FF7 modding community |
| FFNx GitHub | https://github.com/julianxhokaxhiu/FFNx | FFNx source and documentation |
| FF7 Wiki | https://wiki.ffrtt.ru/index.php/FF7 | Technical documentation |

### Related Session Handoffs

| Session | Topic | Date |
|---------|-------|------|
| `SESSION_HANDOFF_2025-12-05-03_MENU_PATCHING.md` | Initial menu patching work | 2025-12-05 |

---

## Future Considerations

### Potential Enhancements

1. **Dynamic Text Sizing:** The combined layout is tight - characters with long names might cause overflow
2. **Resolution Scaling:** Test at different FFNx resolution settings
3. **Mod Compatibility:** Verify with other HEXT patches and FFNx features

### Known Limitations

1. Line wrap threshold (0x1F4 = 500 pixels) is tuned for standard Japanese font - may need adjustment for different fonts
2. The X-offset changes (75→107 pixels) assume Japanese text widths - English labels would need different values

### Related Areas for Investigation

1. **Equip Screen:** Similar combined element display possibilities
2. **Battle Status:** May have similar JP/EN layout differences
3. **Other Menu Screens:** Check for dormant JP code patterns

---

## DO NOT Repeat These Mistakes

This section documents pitfalls to avoid when working on similar FF7 menu modifications.

### Mistake 1: Assuming JA Code is Dormant in EN

**Wrong assumption:** "The EN EXE contains dormant JA code that can be enabled with a single-byte patch."

**Reality:** While some JA code paths exist, the **surrounding instructions are often different**. A JMP in EN that "skips" code doesn't mean the skipped code is the same as JA - it may be completely different implementation.

**Correct approach:** Always do a byte-by-byte comparison of the entire function between EN and JA before attempting patches.

### Mistake 2: NOPing JMP Instructions Without Checking Fall-Through

**Wrong assumption:** "If I NOP a JMP, the code will fall through and work."

**Reality:** Fall-through code may expect specific register states set by the jump target's predecessor code. NOPing causes execution to continue with wrong/garbage register values.

**Correct approach:** When removing a JMP, replace it with the actual instructions from the JA equivalent, not just NOPs.

### Mistake 3: Patching Instruction Start vs Immediate Value

**Wrong assumption:** "The instruction at 0x704097 has value 0x9A, so patch 704097."

**Reality:** Multi-byte instructions have the immediate value at an **offset** from the start. `81 C1 9A 00 00 00` starts at 704097, but the `9A` is at 704099 (offset +2).

**Correct approach:** Use `xxd` to dump bytes and count the exact position of the value you want to change.

### Mistake 4: Not Using Cheat Engine for Runtime State

**Wrong assumption:** "I can figure out the code flow by static analysis alone."

**Reality:** Runtime debugging with Cheat Engine's "Find what writes/accesses" is **dramatically faster** for finding state variables and code paths.

**Correct approach:** Always use Cheat Engine to find state variables first, then trace back to the code that manipulates them.

### Mistake 5: Applying Coordinate Patches Without Testing Each One

**Wrong assumption:** "I can apply all 17 patches at once and it will work."

**Reality:** Each coordinate patch affects layout independently. A crash could be from any one of them, making debugging difficult.

**Correct approach:** Apply patches incrementally, testing after each group (page skip → code path → Element Y → Effect Y → icons).

### Mistake 6: Trusting Address Offset Assumptions

**Wrong assumption:** "JA EXE is at +0xC00 offset from EN, so JA 0x304030 = EN 0x303430."

**Reality:** This offset is only approximately true for the .text section. Different sections have different offsets, and the JA EXE has additional Stext/Sdata sections.

**Correct approach:** Search for unique byte patterns to confirm you're looking at equivalent code, don't rely solely on offset math.

---

## Quick Verification Commands

Copy-paste ready commands for common operations.

### Verify HEXT Patches Are Loaded

```bash
# Check FFNx log for HEXT loading
grep -i "hext" "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/FFNx.log" | tail -20
```

### Dump Current Bytes at Patch Locations

```bash
# Verify patch 1 (page skip)
xxd -s 0x3030C5 -l 1 "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
# Should be: 02 (EN) or patched to: 00

# Verify patch 2 (combined rendering)
xxd -s 0x303430 -l 20 "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
# EN: e9be 0100 008b 4d08 83e9 1b89 4d08 8b55 0c83 ea04
# JA: b89c 0000 008b 4d08 83e9 0089 4d08 8b55 0c03 d090
```

### Compare EN vs JA at Specific Offset

```bash
# EN at file offset
xxd -s 0x303430 -l 64 "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"

# JA at equivalent offset (+0xC00)
xxd -s 0x304030 -l 64 "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe"
```

### Address Calculation (Python)

```python
# File offset to VA
def file_to_va(offset): return offset - 0x400 + 0x401000

# VA to file offset
def va_to_file(va): return va - 0x401000 + 0x400

# Examples
print(f"File 0x303430 → VA 0x{file_to_va(0x303430):X}")  # 0x704030
print(f"VA 0x704030 → File 0x{va_to_file(0x704030):X}")  # 0x303430
```

### Cheat Engine Memory Scan Range

When scanning for menu state variables, focus on this range to reduce noise:
```
Start: 0x00DC0000
End:   0x00DE0000
```

This targets the runtime data section where menu state variables typically reside.

### Check FFNx Log for Crashes

```bash
# Get last crash info
tail -50 "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/FFNx.log" | grep -A5 "CRASH\|Exception\|fault"
```

---

## Changelog

### Version 1.2.0 (2025-12-19)

**Added (Verification Pass):**
- Status Screen Navigation section clarifying Accept/L1/R1/Cancel behavior
- Approach 4: Line wrap threshold iteration history (0x227→0x1C0→0x1F4)
- Approach 5: Y-offset patch crash documentation
- User preference note about sub-label layout vs JP 3-column
- "DO NOT Repeat These Mistakes" section with 6 documented pitfalls
- "Quick Verification Commands" section with copy-paste ready commands
- Cheat Engine memory scan range suggestion (0x00DC0000-0x00DE0000)
- Document Enhancement metadata field

**Changed:**
- Updated version to 1.2.0
- Updated Last Modified timestamp
- Updated Table of Contents

### Version 1.1.0 (2025-12-19)

**Added:**
- Detailed Disassembly Listings section with complete function disassembly
- Screenshots and Visual Reference section with file locations
- Cross-References section linking to related documentation
- This Changelog section

**Changed:**
- Updated Table of Contents to include new sections
- Updated Last Modified date and version number

### Version 1.0.0 (2025-12-18)

**Initial Release:**
- Complete technical documentation of Status screen combined layout implementation
- Executive Summary and Background
- Technical Discovery Journey documenting the reverse engineering process
- Memory Architecture with address calculation formulas
- Complete HEXT Patch Reference (17 patches documented)
- Code Flow Analysis of rendering and page cycling functions
- Debugging Methodology with step-by-step Cheat Engine process
- Failed Approaches section documenting what didn't work
- Testing and Verification checklist
- Reference Tables (byte comparisons, Y-coordinates, status icons)
- Future Considerations and known limitations
- Raw HEXT patch block for easy copy-paste

---

## Appendix: Raw HEXT Patch Block

Copy this entire block to add to your HEXT file:

```
# ============================================================================
# STATUS SCREEN - JAPANESE COMBINED LAYOUT
# ============================================================================
# Makes the Status screen show Element AND Effect properties on ONE page
# (like the original Japanese version) instead of two separate pages.
#
# Session: f0bbe995-213d-4f7a-a0e3-3208dcde8120
# Date: 2025-12-18
# ============================================================================

# 1. Skip Effect page in menu cycle (Element -> Stats instead of Element -> Effect)
703CC5 = 00

# 2. Replace JMP and surrounding code with JA equivalent (20 bytes)
704030 = B8 9C 00 00 00 8B 4D 08 83 E9 00 89 4D 08 8B 55 0C 03 D0 90

# 3. Element section Y-compression
703E63 = 1E
703E82 = 3C
703EA3 = 5A
703ED5 = 6B
703FE7 = 1E

# 4. Effect section positioning
704058 = 22
70407E = 00
704099 = 3C
7040A3 = 00

# 5. Effect icons layout
7040CE = 6B
70416D = F4
70416E = 01
704181 = 6B
7041A7 = 3C
```

---

*Document generated from reverse engineering session f0bbe995-213d-4f7a-a0e3-3208dcde8120*

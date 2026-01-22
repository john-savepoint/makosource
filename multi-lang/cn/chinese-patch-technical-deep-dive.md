# Chinese FF7 Patch (繁體補丁v1.3) - Technical Deep Dive

**Created**: 2026-01-08 20:15 JST (Thursday)
**Last Modified**: 2026-01-08 20:15 JST (Thursday)
**Version**: 1.0.0
**Author**: John Zealand-Doyle
**Session-ID**: 7393413e-daf6-4f5d-bfc1-8fa9e10094b5

---

## Table of Contents

1. [Patch Statistics](#patch-statistics)
2. [The Core DLL Injection Mechanism](#the-core-dll-injection-mechanism)
3. [ali213.dll Deep Analysis](#ali213dll-deep-analysis)
4. [Big5 Character Mapping Table](#big5-character-mapping-table)
5. [HEXT Memory Patches Explained](#hext-memory-patches-explained)
6. [Font Texture System](#font-texture-system)
7. [Complete File Inventory](#complete-file-inventory)
8. [Translation Data Locations](#translation-data-locations)

---

## Patch Statistics

| Metric | Value |
|--------|-------|
| **Total Files** | 463 |
| **Total Size** | ~2.5GB |
| **IRO Archive** | 1.3GB |
| **Font Textures** | 16 files × 8.4MB = 134MB |
| **DLL Size** | 62KB |
| **Languages** | Chinese (Traditional) + Japanese |

---

## The Core DLL Injection Mechanism

### HEXT Injection Code (zzz_cht_patch.txt)

The patch works by injecting code at address `0x400FB0` in ff7.exe:

```
400FB0 = 60 9C FC BE D2 0F 40 00 BF 19 66 67 00 B9 06 00 00 00 F3 A4 68 D8 0F 40 00 FF 15 1C 61 7B 00 9D 61 C3 55 8B EC 83 EC 54 61 6C 69 32 31 33 2E 64 6C 6C 00
```

### Disassembly Analysis

```asm
; === DLL LOADER SHELLCODE ===
0x400FB0: PUSHAD                      ; Save all general registers (EAX, ECX, EDX, EBX, ESP, EBP, ESI, EDI)
0x400FB1: PUSHFD                      ; Save EFLAGS register
0x400FB2: CLD                         ; Clear direction flag (string ops go forward)
0x400FB3: MOV ESI, 0x00400FD2         ; Source = original code bytes location
0x400FB8: MOV EDI, 0x00676619         ; Destination = hook point in game code
0x400FBD: MOV ECX, 6                  ; Copy 6 bytes
0x400FC2: REP MOVSB                   ; Copy original bytes to hook point
0x400FC4: PUSH 0x00400FD8             ; Push address of "ali213.dll" string
0x400FC9: CALL [0x007B611C]           ; Call LoadLibraryA (imported function)
0x400FCF: POPFD                       ; Restore EFLAGS
0x400FD0: POPAD                       ; Restore all registers
0x400FD1: RET                         ; Return to game
0x400FD2: DB 55 8B EC 83 EC           ; Original code that was overwritten
0x400FD8: DB "ali213.dll", 0          ; DLL filename string
```

### Hook Point (0x676619)

The second HEXT line hooks into the game's text processing:

```
676619 = E8 92 A9 D8 FF
```

This is a `CALL` instruction: `E8` is the opcode, `FF D8 A9 92` is the relative offset (little-endian).

Calculation: `0x676619 + 5 + 0xFFD8A992 = 0x400FB0` (wraps around in 32-bit)

This means when the game reaches address `0x676619`, it calls into the injected code at `0x400FB0`, which loads `ali213.dll`.

---

## ali213.dll Deep Analysis

### Build Information

From the PDB path in the binary:
```
E:\temp\FINAL FANTASY VII\ali213\ali213.pdb
```

**Build date**: September 6, 2012 (from PE timestamp)
**Version string**: "Ver.0.19"

### Key Imports

```
KERNEL32.dll:
  - LoadLibraryA          ; Load DLLs
  - GetModuleHandleA      ; Get module base addresses
  - ReadProcessMemory     ; Read game memory
  - WriteProcessMemory    ; Patch game memory at runtime
  - VirtualProtect        ; Change memory protection
  - CreateFileA/W         ; File operations
  - ReadFile/WriteFile    ; File I/O

imagehlp.dll:
  - SymInitialize         ; Debug symbol handling
  - SymGetSymFromName     ; Symbol lookup (for hooking)
  - BindImage             ; Image binding
```

### Detection Strings

The DLL looks for specific markers in resource files:

```
xfhsm_res_ENG_Start     ; English text start marker
xfhsm_res_ENG_End       ; English text end marker
xfhsm_res_CHI_Start     ; Chinese text start marker
xfhsm_res_CHI_End       ; Chinese text end marker
xfhsm_res_Remark00_Start ; Remark start marker
xfhsm_res_Remark00_End   ; Remark end marker
xfhsm_res_No.%08d       ; Numbered entry format
```

### Log File

Creates `LGClog.log` for debugging:
```
LocalGames LGCStringDict::SaveToTXTFileA %s %04d-%02d-%02d %02d:%02d:%02d
```

### Character Detection Logic

From the disassembly at `0x10001032`:

```asm
; Check if byte is in Big5 lead byte range (0xC0-0xCF for extended chars)
LEA EDI, [EDX - 0xC0]           ; Subtract 0xC0 from first byte
CMP DI, 0x0F                    ; Check if result < 16 (i.e., byte is 0xC0-0xCF)
JA skip_processing              ; If not in range, skip

MOV EDI, 0xC0                   ; Set threshold
CMP AX, DI                      ; Compare second byte
JAE skip_processing             ; If second byte >= 0xC0, skip

; This is a valid Big5 double-byte character!
MOV [ECX+0x1C], 0x603           ; Set special marker
MOV [0x1000FAFD], DL            ; Store first byte
MOV [0x1000FAFC], AL            ; Store second byte
```

**Key Insight**: The DLL specifically checks for Big5 lead bytes in the range `0xC0-0xCF`, which corresponds to Traditional Chinese characters. When detected, it stores the character bytes and sets a flag (`0x603`) to indicate CJK processing is needed.

---

## Big5 Character Mapping Table

At offset `0xB860` in ali213.dll, there's a lookup table for Big5 to glyph index conversion:

```
Offset    Data (Little-Endian)
0xB860:   C9ED C9EE C9EF C9F0 C9F1 C9F2 ...
0xB8C0:   CA20 CA21 CA22 CA23 CA24 CA25 ...
```

These are glyph indices into the font texture. The values increment sequentially (`0xC9ED`, `0xC9EE`, etc.), suggesting a linear mapping from Big5 codes to texture positions.

### Mapping Formula

From the code at `0x10001182`:

```asm
ADD ECX, 0x40                   ; Add 0x40 to first byte
SHL ECX, 8                      ; Shift left by 8 (multiply by 256)
ADD ECX, ESI                    ; Add second byte
MOVZX ECX, CX                   ; Zero-extend to 32-bit
MOV ESI, 0x40E7                 ; Base glyph offset
ADD SI, [0x1000B860 + ECX*2]    ; Add table lookup value
```

**Formula**: `glyph_index = 0x40E7 + lookup_table[(byte1 + 0x40) * 256 + byte2]`

This converts a Big5 character code to a position in the font texture atlas.

---

## HEXT Memory Patches Explained

### Categories of Patches

The HEXT files modify memory in several categories:

#### 1. DLL Injection (zzz_cht_patch.txt)

Already explained above - loads ali213.dll at startup.

#### 2. Name Menu Skip (Disable_Name_Change.txt)

```
{New name menu total skip
00719C60 = E9 9B CA 1F 00 90
00916700 = 89 15 FC 46 DD 00 31 D2 8A 15 F8 46 DD 00 ...
```

This completely bypasses the character naming screen, using pre-translated Chinese names instead.

#### 3. Battle Text Sizing (FFNx.BATTLE.fullscreen.txt)

These patches adjust text positioning and box sizes for Chinese characters:

```
; Example: Adjust text width calculations
6E0D40 = 6C         ; Change width constant from ?? to 0x6C (108 pixels)
6E0D79 = 9E         ; Adjust text box width
6E0D97 = 9E         ; Adjust text box width (duplicate for different mode)

; Character spacing adjustments
6DD539 = 84         ; Increase character spacing
6DD584 = 84         ; Increase character spacing
6DD5D6 = 84         ; Increase character spacing
```

#### 4. Battle UI Metrics (hext-bat*.txt)

The numbered battle HEXT files provide different configurations:

| File | Purpose |
|------|---------|
| `hext-bat1` | Basic CJK support |
| `hext-bat2` | Extended box sizing for more text |
| `hext-bat3` | Different character spacing |
| `hext-bat4` | Includes dynamic name width calculation |
| `hext-bat5` | Full CJK with all adjustments |

#### 5. Dialog Transparency (FFNx.*.transparent_modals.txt)

```
; FIELD dialogs
6EB022 = 90 90 90 90 90 90    ; NOP out transparency check

; BATTLE dialogs
6E9475 = 90 90 90 90 90 90    ; NOP out transparency check
; or
6E9475 = 0F 84 B3 01 00 00    ; JE (conditional jump for transparency)
```

#### 6. Always Run Patch (alwaysrun.txt)

```
649A4A = E8 B1 C5 2C 00 90 90 90 90
916000 = 8B 0D C8 11 D0 00 80 3D 0C 04 CC 00 01 74 05 C1 E1 00 C3 90 C1 E1 06 C3
```

Speed multiplier for walking - shifts speed value based on dialog state.

#### 7. Autosave Patch (hext-save/asave.txt)

```
6CA3D6 = 90 90 90 90 90 90    ; NOP out autosave restriction
```

---

## Font Texture System

### Texture Specifications

| Property | Value |
|----------|-------|
| **Format** | TEX (FF7 PC texture format) |
| **Dimensions** | 2048 × 4096 pixels |
| **Bit Depth** | 8-bit (paletted) |
| **Palette** | 256 colors, BGRA format |
| **File Size** | 8,389,868 bytes (8.4MB) |

### Header Analysis (from usfont_a_h.tex)

```
Offset 0x00: 01 00 00 00    ; Version = 1
Offset 0x30: 01 00 00 00    ; Number of palettes = 1
Offset 0x34: 00 01 00 00    ; Colors per palette = 256
Offset 0x38: 08 00 00 00    ; Bit depth = 8
Offset 0x3C: 00 08 00 00    ; Width = 2048
Offset 0x40: 00 10 00 00    ; Height = 4096
```

### Glyph Organization

The 2048×4096 texture can hold approximately:
- At 16×16 pixels per glyph: 128 × 256 = 32,768 glyphs
- At 24×24 pixels per glyph: 85 × 170 = 14,450 glyphs

This is sufficient for:
- All Big5 Traditional Chinese characters (~13,000)
- ASCII characters
- Special symbols

### Font Variants

| Directory | Font | Style |
|-----------|------|-------|
| `DFT` | 華康 (DynaFont) | Regular |
| `DFT_bd` | 華康 (DynaFont) | Bold |
| `msjh` | 微軟正黑體 (Microsoft JhengHei) | Regular |
| `msjh_bd` | 微軟正黑體 (Microsoft JhengHei) | Bold |

Each font has 4 texture files:
- `usfont_a_h.tex` - High detail, character set A
- `usfont_a_l.tex` - Low detail, character set A
- `usfont_b_h.tex` - High detail, character set B
- `usfont_b_l.tex` - Low detail, character set B

---

## Complete File Inventory

### Translation Data Files

```
/files/override/
├── battle/
│   └── scene.bin           # 270KB - Chinese battle text
├── battle-jp/
│   └── scene.bin           # 295KB - Japanese battle text
├── field/
│   └── flevel.lgp          # 130MB - Chinese field dialogue
├── field-jp/
│   └── flevel.lgp          # 130MB - Japanese field dialogue
├── kernel/
│   ├── KERNEL.BIN          # 22KB - Chinese kernel data
│   ├── kernel2.bin         # 13KB - Chinese kernel2 (items, materia, etc.)
│   └── WINDOW.BIN          # 13KB - Chinese window/font data
├── kernel-jp/
│   ├── KERNEL.BIN          # 22KB - Japanese kernel data
│   ├── kernel2.bin         # 19KB - Japanese kernel2
│   └── WINDOW.BIN          # 13KB - Japanese window/font data
├── movies/
│   ├── ending2.avi         # 299MB - Chinese subtitled ending
│   └── jenova_e.avi        # 26MB - Chinese subtitled Jenova scene
├── movies-jp/
│   ├── ending2.avi         # 299MB - Japanese subtitled ending
│   └── jenova_e.avi        # 26MB - Japanese subtitled Jenova scene
└── movies-skip/
    ├── eidoslogo.avi       # 15KB - Blank/skip logo
    └── sqlogo.avi          # 15KB - Blank/skip logo
```

### World Map Data

```
/files/direct/world/
└── mes                     # 2.1KB - World map messages (Chinese)
```

### Font Textures

```
/files/fonts/
├── DFT/menu/
│   ├── usfont_a_h.tex      # 8.4MB
│   ├── usfont_a_l.tex      # 8.4MB
│   ├── usfont_b_h.tex      # 8.4MB
│   └── usfont_b_l.tex      # 8.4MB
├── DFT_bd/menu/            # Same structure (bold)
├── msjh/menu/              # Same structure (MS JhengHei)
└── msjh_bd/menu/           # Same structure (MS JhengHei bold)
```

### Menu/UI Textures

```
/files/mods/Textures/menu/
├── btl_win_*.dds           # Battle window textures (Chinese labels)
├── barre_00.dds            # Bar graphics
├── bins_00.dds             # Bin graphics
└── ... (63 files total)
```

### Minigame Textures

```
/files/mods/Textures/
├── chocobo/                # 17 files - Chocobo racing
├── coaster/                # 2 files - Gold Saucer coaster
├── condor/                 # 33+ files - Fort Condor
├── disc/                   # 6 files - Disc change screens
├── snowboard/              # Snowboard minigame
└── sub/                    # Submarine minigame
```

### Executables

```
/files/
├── 1998-PC/
│   ├── ff7.exe             # 5.9MB - Patched 1998 PC exe
│   ├── ali213.dll          # 62KB - Text hook DLL
│   └── ff7input.cfg        # Controller config
├── 2012-Steam/
│   ├── ff7_en.exe          # 6.4MB - Patched Steam exe
│   ├── ali213.dll          # 62KB - Text hook DLL
│   └── FF78Launcher.toml   # Launcher config
├── 7th_iro/
│   ├── ff7.exe             # 5.9MB - For 7th Heaven
│   └── ff7_cht_1.3.iro     # 1.3GB - Main mod archive
├── name_patch.exe          # 3.5MB - Character name patcher
└── vcredist_x86-2010-SP1.exe # 9MB - Visual C++ runtime
```

### HEXT Patches

```
/files/hext/ff7/en/
├── alwaysrun.txt           # Always run patch
├── Disable_Name_Change.txt # Skip naming screen
├── FFNx.BATTLE.fullscreen.txt
├── FFNx.BATTLE.restore_modals.txt
├── FFNx.BATTLE.transparent_modals.txt
├── FFNx.FIELD.transparent_modals.txt
├── FFNx.MENU.cursor_vertical_center.txt
├── FFNx._GLOBALS.txt
└── zzz_cht_patch.txt       # Main DLL injection

/files/hext-bat1/ff7/en/    # Battle config 1
/files/hext-bat2/ff7/en/    # Battle config 2
/files/hext-bat3/ff7/en/    # Battle config 3
/files/hext-bat4/ff7/en/    # Battle config 4
/files/hext-bat5/ff7/en/    # Battle config 5
/files/hext-save/ff7/en/    # Autosave patch
```

### Configuration

```
/files/config/
├── pc.txt                  # FFNx config for 1998 PC
├── steam.txt               # FFNx config for Steam
├── metadata.xml            # Save metadata
├── ff7_en.exe              # Copy of Steam exe
├── FF7_Launcher.exe        # Launcher
└── AF3DN.P                 # Unknown data file
```

---

## Translation Data Locations

### To Extract Chinese Translations:

| Content Type | File | Tool to Use |
|--------------|------|-------------|
| **Battle text** | `override/battle/scene.bin` | touphScript, Proud Clod |
| **Field dialogue** | `override/field/flevel.lgp` | Makou Reactor, touphScript |
| **Items/Materia/etc** | `override/kernel/kernel2.bin` | touphScript, Wall Market |
| **Menu text** | `override/kernel/KERNEL.BIN` | touphScript |
| **World map text** | `direct/world/mes` | touphScript |
| **Menu graphics** | `mods/Textures/menu/*.dds` | Any DDS viewer/editor |

### IRO Archive Contents

The 1.3GB IRO file (`ff7_cht_1.3.iro`) contains all of the above plus:
- `data/` - Chinese versions of all game data
- `data-jp/` - Japanese versions of all game data
- `fps60/` - Modified field files for 60fps support
- `hext/` - All HEXT patches
- `pv/` - Preview images

The IRO format is a simple archive that 7th Heaven can read. Files are listed in UTF-16LE in the header with offsets and sizes.

---

## How Everything Works Together

### Startup Flow

```
1. User launches FF7 (via 7th Heaven or directly)
2. FFNx loads and applies HEXT patches including zzz_cht_patch.txt
3. HEXT patch at 0x400FB0 gets executed early in game startup
4. Code at 0x400FB0 calls LoadLibraryA("ali213.dll")
5. ali213.dll initializes:
   - Hooks text rendering functions using Detours
   - Loads translation tables with ENG/CHI markers
   - Sets up Big5 character detection
6. FFNx loads override data:
   - scene.bin, flevel.lgp, kernel*.bin from override folders
   - Font textures from fonts/ folder
   - Menu textures from mods/Textures/
7. Game runs with:
   - Chinese text from override data files
   - ali213.dll intercepting/processing text rendering
   - Chinese glyphs from massive font texture atlases
   - Adjusted UI sizing from HEXT patches
```

### Runtime Text Flow

```
1. Game requests text (e.g., "Potion" from kernel2.bin)
2. Since override/kernel/kernel2.bin exists, FFNx loads Chinese version
3. Chinese text "藥水" (Big5: 0xC3B3 0xA4F4) is passed to text engine
4. ali213.dll hook intercepts the text
5. DLL detects Big5 lead bytes (0xC0-0xCF range)
6. DLL looks up glyph index: table[(byte1+0x40)*256 + byte2] + 0x40E7
7. FFNx renders glyph from font texture at calculated position
8. Chinese character appears on screen
```

---

## Summary

The Chinese patch is a remarkably clever solution that:

1. **Injects a hook DLL** via HEXT patches at startup
2. **Intercepts text processing** with Microsoft Detours
3. **Detects Big5 double-byte characters** using lead byte checking (0xC0-0xCF)
4. **Maps characters to glyphs** via a lookup table in the DLL
5. **Renders glyphs from massive pre-baked textures** (8.4MB each, ~13,000+ chars)
6. **Adjusts UI metrics** via numerous HEXT patches for text boxes and spacing

All of this works WITHOUT modifying FFNx's core code - it's entirely external hooking and data replacement.

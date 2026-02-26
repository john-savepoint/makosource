# Session Handoff: FFVII 2026 Steam Edition Reverse Engineering

**Created:** 2026-02-26 14:10 JST (Thursday)
**Session-ID:** ad020c43-3ebe-4197-9ab9-4bbeff56a441
**Author:** John Zealand-Doyle + Claude Code (Opus 4.6)
**Purpose:** Complete context transfer for continuing RE work on FFVII 2026 Steam Edition

---

## What Was Done This Session

### 1. Binary Analysis of FFVII.exe (PE analysis via pefile + strings)

**CRITICAL FINDING: NOT .NET** — The 24.9MB `FFVII.exe` is a **native 64-bit C++ executable** compiled with MSVC. The SharpDX/NAudio DLLs in the directory are for the LAUNCHER only (`FFVII_LAUNCHER.exe`, which IS .NET/32-bit).

**Architecture discovered:**
- Developer: **DotEmu** (confirmed via `dotemuReg*` strings and `dotemu-logo`)
- Internal dev path: `W:\proj\ff7\kitamura\Material\...`
- Framework: **DotEmu BaseEngine** — a proprietary engine wrapping classic game code
- The original FF7 C code was **recompiled as 64-bit** with a "fake Windows" shim layer

**Key imports:** `D3D11CreateDevice` (d3d11.dll), SDL2 (11 functions), XAudio2, steam_api64.dll

### 2. Discovery of the fake_win Shim Architecture

The core architectural pattern:
```
Original FF7 game code (recompiled x64)
    ↓ calls Win32 API functions
fake_win shim table (203 entries)
    ↓ routes to DotEmu BaseEngine implementations
BaseEngine → D3D11, XAudio2, SDL2
```

Source files from debug strings:
- `W:\proj\ff7\kitamura\Material\fake_win\fake_gfx.cpp` — Graphics shim
- `W:\proj\ff7\kitamura\Material\fake_win\fake_dsound.cpp` — Audio shim
- `W:\proj\ff7\kitamura\Material\BaseEngine\RenderManager.cpp`
- `W:\proj\ff7\kitamura\Material\BaseEngine\ShaderManager.cpp`
- `W:\proj\ff7\kitamura\Material\BaseEngine\TextureManager.cpp`
- `W:\proj\ff7\kitamura\Material\BaseEngine\InputManager.cpp`
- `W:\proj\ff7\kitamura\Material\BaseEngine\MusicManager.cpp`
- `W:\proj\ff7\kitamura\Material\BaseEngine\VideoManager.cpp`
- `W:\proj\ff7\kitamura\Material\BaseEngine\TrophyManager.cpp`
- `W:\proj\ff7\kitamura\Material\Game\Saves\SaveDataConvertLocation.cpp`
- `W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\*.cpp`

### 3. IDA Pro Analysis of FFVII.exe

**IDA Pro 9.0** loaded with `FFVII.exe`. Auto-analysis complete. **3,019 functions** detected.

**IDA MCP server connection:** `http://172.19.208.1:13337` (Windows host from WSL)
- Must press **Ctrl+Alt+M** in IDA to start MCP server
- Claude Code config at `~/.claude.json` → `mcpServers.ida-pro-mcp`

#### The Complete fake_win Shim Table

**Location:** `0x1416D20B8` (named `g_fake_win_shim_table` in IDA)
**Size:** 203 entries, each 0x20 (32) bytes
**Range:** `0x1416D20B8` to `0x1416D3A18`
**Entry format:** `[name_ptr(8), func_ptr(8), param_info(8), extra(8)]`

All 203 functions were named in IDA with `shim_` prefix.

**Function groups in shim table:**
- **gfx_drv_* (49 funcs)** — Graphics driver interface (what FFNx hooks)
- **IDirectSound* (16 funcs)** — DirectSound audio interface
- **IDirectInput* (8 funcs)** — DirectInput interface
- **fw_movie_* (17 funcs)** — FMV video playback
- **acmStream* (6 funcs)** — Audio compression
- **Win32 API (106 funcs)** — CreateWindow, LoadLibrary, Registry, File I/O, etc.

#### gfx_drv_* Function Pointer Table (THE KEY TO FFNx)

**Location:** `0x1416D31D8` (subset of the shim table)
**All 49 gfx_drv functions with addresses:**

```
gfx_drv_new_dll                     0x141560a30
gfx_drv_cleanup                     0x1415603c0
gfx_drv_init                        0x1415603c0  (same as cleanup!)
gfx_drv_lock                        0x140027f20
gfx_drv_unlock                      0x140027f20  (same as lock!)
gfx_drv_setviewport                 0x141560f80
gfx_drv_clear_all                   0x14155e190
gfx_drv_clear                       0x14155e020
gfx_drv_setbg                       0x141560b40
gfx_drv_unload_texture              0x1415611a0
gfx_drv_load_texture                0x1415604e0
gfx_drv_blendmode                   0x14155dfc0
gfx_drv_field_64                    0x14155ef70
gfx_drv_setrenderstate_6c           0x141560da0
gfx_drv_setrenderstate_70           0x141560da0  (same as 6c)
gfx_drv_field_74                    0x14155f110
gfx_drv_setrenderstate              0x141560da0  (same as 6c/70)
gfx_drv_field_80                    0x14155fd20
gfx_drv_field_84                    0x14155fd40
gfx_drv_begin_scene                 0x14155dd30
gfx_drv_end_scene                   0x14155ebf0
gfx_drv_palette_changed             0x141560a90
gfx_drv_write_palette               0x1415612b0
gfx_drv_setmatrix                   0x141560ba0
gfx_drv_field_78                    0x14155f170
gfx_drv_draw_deferred               0x14155e2d0  (nullsub)
gfx_drv_flip                        0x14155fe30
gfx_drv_setrenderstate_flat2D       0x141560de0
gfx_drv_setrenderstate_smooth2D     0x141560de0  (same)
gfx_drv_setrenderstate_textured2D   0x141560de0  (same)
gfx_drv_setrenderstate_paletted2D   0x141560de0  (same)
gfx_drv_setrenderstate_paletted2D_bis 0x141560de0  (same)
gfx_drv_draw_flat2D                 0x14155e410
gfx_drv_draw_smooth2D               0x14155e410  (same as flat2D)
gfx_drv_draw_textured2D             0x14155eb00
gfx_drv_draw_paletted2D             0x14155e800
gfx_drv_setrenderstate_flat3D       0x141560e30
gfx_drv_setrenderstate_smooth3D     0x141560e30  (same)
gfx_drv_draw_flat3D                 0x14155e620
gfx_drv_draw_smooth3D               0x14155e620  (same)
gfx_drv_setrenderstate_textured3D   0x140021230
gfx_drv_setrenderstate_paletted3D_c4 0x140021230  (same)
gfx_drv_setrenderstate_paletted3D_c8 0x140021230  (same)
gfx_drv_draw_textured3D             0x140021230  (same)
gfx_drv_draw_paletted3D             0x140021230  (same)
gfx_drv_setrenderstate_flatlines    0x141560f30
gfx_drv_setrenderstate_smoothlines  0x141560f30  (same)
gfx_drv_draw_flatlines              0x14155e710
gfx_drv_draw_smoothlines            0x14155e710  (same)
```

**Notable patterns:**
- Many 2D setrenderstate functions share ONE implementation at `0x141560de0`
- All 3D textured/paletted functions share ONE implementation at `0x140021230`
- `gfx_drv_draw_deferred` is a nullsub (empty function)
- `gfx_drv_init` and `gfx_drv_cleanup` share the same address

#### Decompilation Status

Hex-Rays decompilation partially works but many gfx_drv functions show as stubs:
- `gfx_drv_clear_all`: `mov cl, 82h; retn` — appears to be a dispatch stub
- `gfx_drv_setviewport`: decompiles but shows `JUMPOUT`
- `gfx_drv_new_dll`: decompiles but corrupted
- Some WinAPI shims (e.g., `shim_LoadLibraryA`) point to obfuscated/encrypted data at `0x141574b50`

**Hypothesis:** The shim functions may be **trampolines or dispatch stubs** that use indirect calls through BaseEngine. The `mov cl, 82h; retn` pattern could be setting a function ID for a central dispatcher. This needs further investigation.

### 4. Game Data Structure

**Data paths identical to old version, relocated to:**
```
ff7/workingdir/data/
├── battle/           (battle.lgp, magic.lgp, scene data)
├── cd/               (disc LGPs per language)
├── field/            (flevel.lgp, jfleve.lgp, char.lgp, etc.)
├── lang-de/          (German kernel, scene, movies)
├── lang-en/          (English kernel, scene)
├── lang-es/          (Spanish)
├── lang-fr/          (French)
├── lang-ja/          (Japanese kernel, scene, movies)
│   ├── battle/scene.bin
│   ├── kernel/kernel.bin, kernel2.bin, window.bin
│   └── movies/ending2.avi, jenova_e.avi
├── menu/             (menu_us.lgp, menu_ja.lgp, etc.)
├── midi/
├── music_ogg/
├── png/              (submarinemenu per language)
└── wm/               (world map data)
```

**Font references in exe:**
- `jafont_%d.tim` — Japanese font TIM loading (in code)
- `ff7/font/TBGoPro_Regular.fnt` — BMFont for launcher UI
- `ff7/font/TBGoPro_Regular_0.png` — Font atlas

**Embedded original executables:**
- `ff7/resources/ff7_1.02/ff7_en` (5,997,027 bytes, PE32, same timestamp as 1998 build)
- `ff7/resources/ff7_1.02/ff7_ja` (5,998,580 bytes, PE32)
- Format string: `%s/resources/ff7_1.02/ff7_%s` — main exe reads hardcoded data tables from these

### 5. Community/Ecosystem Status (as of 2026-02-26)

- Game released Feb 24, 2026 on Steam + GOG
- Steam reviews: "Mixed" (44% positive) — bilinear filtering, bugs
- Old 2013 Edition renamed, delisted but kept for existing owners
- **FFNx:** No official statement yet on 2026 compatibility
- **7th Heaven:** Tsunamods investigating, GitHub issue #351 was opened then deleted
- **Modding community:** "Wait and see" mode, recommending 2013 Edition for mods

---

## What Needs To Be Done Next

### Immediate (IDA Pro work)

1. **Understand the dispatch mechanism** — The `mov cl, 82h; retn` pattern in gfx_drv stubs suggests a central dispatcher. Find it. This is how the original game code calls into the BaseEngine.

2. **Find the main game loop** — Locate `WinMain` equivalent, the module dispatch (field/battle/menu/world), and the frame update cycle.

3. **Map the text rendering pipeline** — Find where `jafont_%d.tim` gets loaded, where character widths are computed, and where glyphs are drawn. Cross-reference from the font strings.

4. **Map the file loading system** — How `lang-ja/kernel/kernel.bin` and `field/jfleve.lgp` get loaded. The `data/` and `lang-ja/` strings at `0x141649300` and `0x141649348` are the starting points.

5. **Investigate the obfuscated shim functions** — Some WinAPI shims (LoadLibraryA, etc.) point to encrypted data. Determine if this is DRM, anti-tamper, or just unanalyzed code.

### Strategy (FFNx port approach)

**Most viable injection path: SDL2.dll proxy**
- Game imports 11 SDL2 functions
- Create proxy DLL that forwards calls to real SDL2
- On load, pattern-scan for the shim table and hook gfx_drv functions
- This gives us the same hook points FFNx uses, just in a 64-bit context

**Alternative: Shim table patching**
- The shim table at `0x1416D20B8` contains function pointers
- If we can modify these in memory, we can redirect gfx_drv calls to our code
- This is essentially what FFNx does with the original AF3DN.P

### Architecture Vision (Unified Modding)

The goal is NOT just "make FFNx work." It's a unified modding layer:
```
FFVII.exe (one 64-bit binary, all 5 languages)
    ↓ SDL2.dll proxy injection
FFNx64.dll (new unified mod driver)
    ↓ hooks gfx_drv_* via shim table
    ↓ intercepts text/font pipeline
    ↓ provides mod API (7th Heaven compatible)
ff7/workingdir/data/ + mods/ overlay
```

This eliminates the old pattern of separate executables per language and separate mods per language.

---

## Parallel Agent Strategy for Next Session

The scope of this RE work is enormous (22MB of code, 3,019 functions, 203 shim entries). Recommend dispatching parallel agents:

### Agent 1: Dispatch Mechanism Analysis
- Focus on the `mov cl, XX; retn` pattern in gfx_drv stubs
- Find the central dispatcher that reads the function ID
- Map how the original game code actually calls through the shim table
- Deliverable: Understanding of the dispatch/trampoline mechanism

### Agent 2: Text/Font Pipeline Mapping
- Starting from `jafont_%d.tim` string at `0x14164C300`
- Find the TIM texture loading function
- Map character width tables, glyph rendering
- Cross-reference with FFNx PR737's `japanese_text.cpp`
- Deliverable: Function address map for text rendering

### Agent 3: File Loading & Language System
- Starting from `lang-ja/` string at `0x141649348` and `%s/resources/ff7_1.02/ff7_%s` at `0x141649380`
- Map LGP loading, kernel loading
- Understand language selection mechanism
- Deliverable: File I/O hook points

### Agent 4: FFNx Hook Point Mapping (Source-side)
- Read FFNx PR737 source code
- Document every hook, every patched address, every replaced function
- Create a mapping table: "FFNx hooks X in old exe → equivalent in new exe is Y"
- Deliverable: Complete FFNx-to-2026 address translation table

---

## Files Created This Session

1. `FF7 2026/analysis/FFVII_2026_DECOMPILATION_REPORT.md` — Initial PE analysis report
2. `FF7 2026/analysis/SESSION_HANDOFF_2026-02-26.md` — This file

## IDA Database State

- **File:** `FFVII.exe` loaded in IDA Pro 9.0
- **Named:** 49 gfx_drv functions + 203 shim functions (all prefixed with `shim_`)
- **Table labeled:** `g_fake_win_shim_table` at `0x1416D20B8`
- **Auto-analysis:** Complete
- **Save the IDA database (.i64)** before closing IDA

---

## Key Addresses Quick Reference

| Item | Address | Notes |
|------|---------|-------|
| Image base | `0x140000000` | Standard x64 |
| fake_win shim table | `0x1416D20B8` | 203 entries, 0x20 each |
| gfx_drv vtable start | `0x1416D31D8` | 49 entries (subset of shim table) |
| gfx_drv_flip | `0x14155FE30` | Frame present |
| gfx_drv_load_texture | `0x1415604E0` | Texture loading |
| gfx_drv_draw_textured2D | `0x14155EB00` | 2D textured draw |
| gfx_drv_begin_scene | `0x14155DD30` | Frame start |
| gfx_drv_end_scene | `0x14155EBF0` | Frame end |
| jafont_%d.tim string | `0x14164C300` | Japanese font loading |
| lang-ja/ string | `0x141649348` | Language path |
| %s/resources/ff7_1.02/ff7_%s | `0x141649380` | Exe data extraction |
| workingdir string | `0x141730D00` | Data root path |
| TBGoPro_Regular.fnt | `0x141649ED8` | Launcher font |
| dotemu string | `0x1416493A0` | Developer ID |

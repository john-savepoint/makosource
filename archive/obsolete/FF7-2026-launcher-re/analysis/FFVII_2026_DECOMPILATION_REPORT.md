# FFVII 2026 Steam Edition — Decompilation & Architecture Report

**Created:** 2026-02-26 11:15 JST (Thursday)
**Session-ID:** ad020c43-3ebe-4197-9ab9-4bbeff56a441
**Author:** John Zealand-Doyle + Claude Code
**Version:** 1.0.0

---

## Executive Summary

The 2026 "FINAL FANTASY VII Steam Edition" is **NOT** a .NET wrapper or simple launcher. It is a **native 64-bit C++ recompilation** of the original FF7 game engine, built by **DotEmu** using their proprietary **BaseEngine** framework. The original game code has been recompiled for x86-64 with the graphics/audio/input layers replaced by modern abstractions.

**Key implications for FFNx:**
- FFNx's DLL injection via AF3DN.P is impossible — the driver abstraction is compiled into the exe
- All memory addresses are completely different (64-bit recompilation)
- BUT the same `gfx_drv_*` graphics interface exists internally
- Japanese language support is **built-in natively** — no FFNx needed for basic Japanese play

---

## Binary Analysis

### FFVII.exe (Main Game)

| Property | Value |
|----------|-------|
| **Type** | PE32+ executable (native C++, NOT .NET) |
| **Architecture** | x86-64 (64-bit) |
| **Compiler** | MSVC (MSVCP140.dll, VCRUNTIME140.dll) |
| **Code size** | 22.3 MB (.text section) |
| **Total size** | 24.9 MB |
| **CLR header** | None — NOT a .NET assembly |
| **Graphics** | Direct3D 11 (`D3D11CreateDevice`) |
| **Audio** | XAudio2 (`XAudio2_9Redist.dll`) |
| **Input** | SDL2 (`SDL2.dll`) + DirectInput |
| **Steam** | `steam_api64.dll` |

### FFVII_LAUNCHER.exe (Launcher Only)

| Property | Value |
|----------|-------|
| **Type** | PE32 (.NET assembly) |
| **Architecture** | x86 (32-bit) |
| **Runtime** | mscoree.dll (CLR) |
| **Uses** | SharpDX, NAudio, Steamworks.NET |

The SharpDX/NAudio DLLs in the install directory are used by the **launcher only**, not the game itself. The game is pure native C++.

### Embedded Original Executables

The re-release ships the original 32-bit executables at:
- `ff7/resources/ff7_1.02/ff7_en` (5,997,027 bytes, PE32)
- `ff7/resources/ff7_1.02/ff7_ja` (5,998,580 bytes, PE32)

These are **different** from the 2013 Steam ff7_en.exe (6,413,496 bytes) — likely the original retail 1.02 executables without the 2012 Square Enix overlay patches. The format string `%s/resources/ff7_1.02/ff7_%s` suggests the main exe reads hardcoded data tables from these files at runtime.

---

## Developer: DotEmu (Not FINE Co., Ltd.)

Debug strings reveal the developer:
- `dotemuRegOpenKeyExA`, `dotemuRegCloseKey`, `dotemuRegSetValueExA` — custom registry abstraction
- Source paths: `W:\proj\ff7\kitamura\Material\...` — "kitamura" is the developer at DotEmu
- `dotemu-logo` — splash screen reference

DotEmu is the same studio behind the FF7/FF8/FF9 mobile and console ports. Their **BaseEngine** framework is reused across multiple classic game ports.

---

## Architecture: How It Works

### The "Fake Windows" Layer

The most critical finding is the **shim layer** that bridges the original 1998 game code to modern APIs:

```text
Original FF7 Code (recompiled as 64-bit)
         ↓
fake_gfx.cpp → BaseEngine RenderManager → D3D11
fake_dsound.cpp → BaseEngine AudioSystem → XAudio2
dotemuReg*.cpp → Custom registry abstraction
         ↓
BaseEngine Framework (D3D11, SDL2, XAudio2)
```

Source files from debug info:
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

### The Graphics Driver Interface (Critical for FFNx)

The original FF7 engine uses a graphics driver abstraction — the `gfx_drv_*` functions. In the original game, these were implemented by `AF3DN.P`. In FFNx, they're intercepted and reimplemented.

**In the 2026 version, these same functions exist but are compiled into the exe:**

```text
gfx_drv_init                    gfx_drv_setviewport
gfx_drv_cleanup                 gfx_drv_setbg
gfx_drv_begin_scene             gfx_drv_setmatrix
gfx_drv_end_scene               gfx_drv_blendmode
gfx_drv_flip                    gfx_drv_setrenderstate
gfx_drv_clear / clear_all       gfx_drv_setrenderstate_*
gfx_drv_lock / unlock           gfx_drv_palette_changed
gfx_drv_load_texture            gfx_drv_write_palette
gfx_drv_unload_texture          gfx_drv_draw_deferred
gfx_drv_new_dll                 gfx_drv_draw_*2D / *3D
gfx_drv_field_64/74/78/80/84
```

These are the **exact same interface** that FFNx hooks. They're just no longer in an external DLL.

### Shader Pipeline

Pre-compiled HLSL shaders (CSO format) in `ff7/Shaders/`:
- `lmain_vv.cso`, `tlmain_vv.cso` — Main vertex shaders
- `color_p.cso`, `colortex_p.cso` — Color/texture pixel shaders
- `text_p.cso` — Text rendering shader
- `fxaanv5_p.cso`, `fxaa2_vv.cso` — FXAA anti-aliasing
- `hq4x_p.cso`, `hq4x_vv.cso` — HQ4X upscaling filter
- `2xsal_p.cso`, `2xsal_vv.cso` — 2xSAL filter
- `brightness_p.cso` — Brightness adjustment
- `video_p.cso` — Video playback
- `pcsettings_p/vv.cso` — Settings menu
- `mergeforeground_p.cso` — Foreground compositing

---

## Built-in Multi-Language Support

The 2026 version ships with **native 5-language support**:

### Language Data Directories
```text
ff7/workingdir/data/
├── lang-de/    (German)
├── lang-en/    (English)
├── lang-es/    (Spanish)
├── lang-fr/    (French)
└── lang-ja/    (Japanese)
```

Each contains:
- `battle/scene.bin` — Battle scene data
- `kernel/kernel.bin` — Game text/data
- `kernel/kernel2.bin` — Extended kernel data
- `kernel/window.bin` — Window configuration (ja only has this)
- `movies/` — Language-specific FMVs

### Japanese-Specific Assets
- `ff7/workingdir/data/field/jfleve.lgp` — Japanese field dialogue
- `ff7/workingdir/data/menu/menu_ja.lgp` — Japanese menu text
- `ff7/workingdir/data/png/submarinemenu_ja.png` — Japanese submarine mini-game
- `ff7/resources/ff7_1.02/ff7_ja` — Original Japanese executable (data tables)
- `be_loc/be_loc_ja.xml` — Launcher/wrapper Japanese strings
- String in exe: `jafont_%d.tim` — Japanese font texture loading code

### Font System
- `ff7/font/TBGoPro_Regular.fnt` — BMFont format (TBGothic Pro Regular)
- `ff7/font/TBGoPro_Regular_0.png` — Font atlas for launcher UI
- `jafont_%d.tim` reference in exe — Original TIM format Japanese fonts loaded at runtime

---

## Implications for FFNx Compatibility

### Why FFNx Cannot Work As-Is

1. **No injection point** — FFNx replaces `AF3DN.P` which the original 32-bit exe loads. The 2026 exe has no external graphics DLL to replace.
2. **64-bit architecture** — All memory addresses, pointer sizes, calling conventions, and struct layouts differ from the 32-bit version.
3. **Compiled-in driver** — The `gfx_drv_*` functions are statically linked into FFVII.exe, not in a loadable DLL.
4. **Different rendering backend** — D3D11 instead of DirectDraw/OpenGL, with pre-compiled HLSL shaders.

### Viable Approaches for FFNx-Like Functionality

#### 1. SDL2.dll Proxy (Most Promising)
The game imports 11 SDL2 functions. Create a proxy `SDL2.dll` that:
- Forwards all calls to the real `SDL2.dll` (renamed to `SDL2_original.dll`)
- On DLL load, pattern-scans the process memory for `gfx_drv_*` functions
- Hooks the found functions to inject FFNx-style rendering enhancements

#### 2. d3d11.dll Proxy
Same concept via Direct3D 11. The game calls `D3D11CreateDevice` — a proxy can intercept the device and swap chain to inject custom rendering.

#### 3. Pattern Scanning for gfx_drv_* Functions
The function names are present as strings in the binary. Cross-referencing these strings leads to the function pointer table, enabling direct hooking. This is the same technique many game modding frameworks use.

#### 4. Data-Only Mods (For Our Japanese Project)
Since game data files are identical format, replace:
- `lang-ja/kernel/kernel.bin` — Modified kernel text
- `field/jfleve.lgp` — Modified field dialogue
- `menu/menu_ja.lgp` — Modified menu data
No FFNx needed for basic file replacement.

---

## Comparison: Old vs New

| Aspect | 2013 Edition | 2026 Steam Edition |
|--------|-------------|-------------------|
| **Architecture** | 32-bit (x86) | 64-bit (x86-64) |
| **Exe size** | 6.4 MB | 24.9 MB |
| **Graphics API** | DirectDraw → AF3DN.P | D3D11 (BaseEngine) |
| **Audio** | Custom → dsound.dll | XAudio2 |
| **Input** | DirectInput | SDL2 + DirectInput |
| **DLL injection** | Replace AF3DN.P | Not possible (compiled-in) |
| **Japanese support** | Requires FFNx mod | Built-in natively |
| **Game data format** | .lgp, .bin, .tex | Same .lgp, .bin, .tex |
| **Data paths** | `data/` | `ff7/workingdir/data/` |
| **Mod support** | FFNx + 7th Heaven | Unknown / None yet |
| **Registry** | Standard Win32 API | Custom `dotemuReg*` |
| **Shaders** | Runtime compiled | Pre-compiled CSO |
| **Font (launcher)** | N/A | TBGoPro_Regular.fnt (BMFont) |
| **Font (game)** | Single texture page | `jafont_%d.tim` (multi-page) |

---

## Next Steps

1. **Run the game in Japanese** — Select Japanese from Steam's language settings and verify native Japanese support works
2. **Analyze the embedded ff7_ja** — Determine what data the main exe extracts from it
3. **Pattern scan gfx_drv_* addresses** — Use a debugger (x64dbg) to find the function addresses via string cross-references
4. **Build an SDL2.dll proxy POC** — Minimal DLL that logs function calls and proves injection works
5. **Coordinate with FFNx community** — Share findings with julianxhokaxhiu and Tsunamods
6. **Check if Ghidra can handle the binary** — 22MB of code will need significant analysis time

---

## Raw Data Files

### All Source Path References
```text
W:\proj\ff7\kitamura\BaseEngine\AudioSystem\Win32_Sources\SoundBufferImpl.cpp
W:\proj\ff7\kitamura\BaseEngine\AudioSystem\Win32_Sources\SoundDeviceImpl.cpp
W:\proj\ff7\kitamura\BaseEngine\MP4Player\Win32_Sources\Mp4PlayerImpl.cpp
W:\proj\ff7\kitamura\BaseEngine\MP4Player\Win32_Sources\VorbisContext.h
W:\proj\ff7\kitamura\BaseEngine\MP4Player\Win32_Sources\VpxContext.h
W:\proj\ff7\kitamura\BaseEngine\MP4Player\Win32_Sources\WebmContext.cpp
W:\proj\ff7\kitamura\BaseEngine\Resource\TextureLoader.cpp
W:\proj\ff7\kitamura\BaseEngine\UserServices\TrophyManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\BufferManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\DirectSound.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\DirectSoundBuffer.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\InputManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\InputManager.h
W:\proj\ff7\kitamura\Material\BaseEngine\MusicManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\MusicStream.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\RenderManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\ShaderManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\ShaderManager.h
W:\proj\ff7\kitamura\Material\BaseEngine\TextureManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\TextureManager.h
W:\proj\ff7\kitamura\Material\BaseEngine\TrophyManager.cpp
W:\proj\ff7\kitamura\Material\BaseEngine\VideoManager.cpp
W:\proj\ff7\kitamura\Material\Game\Saves\SaveDataConvertLocation.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\AutosaveSettingMenu.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\BoostSettingMenu.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\MenuItem.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\PCSettings.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\ParameterChangeMenu.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\PCSettings\SystemSettingMenu.cpp
W:\proj\ff7\kitamura\Material\Platform\Win\src\Settings.cpp
W:\proj\ff7\kitamura\Material\fake_win\fake_dsound.cpp
W:\proj\ff7\kitamura\Material\fake_win\fake_gfx.cpp
```

### All gfx_drv_* Functions Found
```text
gfx_drv_begin_scene          gfx_drv_setrenderstate_flat3D
gfx_drv_blendmode            gfx_drv_setrenderstate_flatlines
gfx_drv_cleanup              gfx_drv_setrenderstate_paletted2D
gfx_drv_clear                gfx_drv_setrenderstate_paletted2D_bis
gfx_drv_clear_all            gfx_drv_setrenderstate_paletted3D_c4
gfx_drv_draw_deferred        gfx_drv_setrenderstate_paletted3D_c8
gfx_drv_draw_flat2D          gfx_drv_setrenderstate_smooth2D
gfx_drv_draw_flat3D          gfx_drv_setrenderstate_smooth3D
gfx_drv_draw_flatlines       gfx_drv_setrenderstate_smoothlines
gfx_drv_draw_paletted2D      gfx_drv_setrenderstate_textured2D
gfx_drv_draw_paletted3D      gfx_drv_setrenderstate_textured3D
gfx_drv_draw_smooth2D        gfx_drv_setviewport
gfx_drv_draw_smooth3D        gfx_drv_unload_texture
gfx_drv_draw_smoothlines     gfx_drv_unlock
gfx_drv_draw_textured2D      gfx_drv_write_palette
gfx_drv_draw_textured3D      gfx_drv_field_64
gfx_drv_end_scene            gfx_drv_field_74
gfx_drv_flip                 gfx_drv_field_78
gfx_drv_init                 gfx_drv_field_80
gfx_drv_load_texture         gfx_drv_field_84
gfx_drv_lock                 gfx_drv_new_dll
gfx_drv_palette_changed
gfx_drv_setbg
gfx_drv_setmatrix
gfx_drv_setrenderstate
gfx_drv_setrenderstate_6c
gfx_drv_setrenderstate_70
gfx_drv_setrenderstate_flat2D
```

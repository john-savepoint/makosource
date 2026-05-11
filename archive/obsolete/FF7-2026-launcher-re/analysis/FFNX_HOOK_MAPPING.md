# FFNx Hook Mapping: Original FF7 → 2026 Steam Edition

**Created:** 2026-02-26 15:40 JST (Thursday)
**Session-ID:** ad020c43-3ebe-4197-9ab9-4bbeff56a441
**Status:** In Progress — Complete 203-entry shim table dumped! All subsystems mapped.
**Last Updated:** 2026-02-26 15:45 JST (Thursday)
**ASLR Delta (this dump):** `0x7FF588110000`

---

## Overview

FFNx hooks ~100+ functions in the original 32-bit FF7.exe and replaces them with enhanced implementations. For the 2026 64-bit recompilation, we need to find equivalent function addresses.

**Hook categories:**
1. **Graphics Driver (gfx_drv_*)** — FULLY MAPPED ✅
2. **File I/O (open/read/close/lgp)** — Need IDA pattern scan
3. **Audio (MIDI, SFX, DirectSound)** — Need IDA pattern scan
4. **Game Logic (field, battle, menu, world)** — Need IDA pattern scan
5. **Text/Font rendering** — Need IDA pattern scan
6. **Save/Load** — Need IDA pattern scan
7. **Input (DirectInput, gamepad)** — Need IDA pattern scan

---

## 1. Graphics Driver Hooks — FULLY MAPPED ✅

These are the `gfx_drv_*` functions that FFNx replaces when it loads as AF3DN.P. In the 2026 build, these are compiled into FFVII.exe.

| FFNx Hook | Original Address (32-bit) | 2026 Disk Address | 2026 Runtime (ASLR) | Status |
|-----------|--------------------------|-------------------|---------------------|--------|
| gfx_drv_new_dll (init) | via AF3DN.P export | `0x141560A30` | `0x7FF6C9670A30` | ✅ Decompiled |
| gfx_drv_cleanup/init | via AF3DN.P export | `0x1415603C0` | `0x7FF6C96703C0` | ✅ Decompiled |
| gfx_drv_lock/unlock | via AF3DN.P export | `0x140027F20` | `0x7FF6C8137F20` | ✅ No-op stub |
| gfx_drv_begin_scene | via AF3DN.P export | `0x14155DD30` | `0x7FF6C966DD30` | ✅ Decompiled |
| gfx_drv_end_scene | via AF3DN.P export | `0x14155EBF0` | `0x7FF6C966EBF0` | ✅ Decompiled |
| gfx_drv_flip | via AF3DN.P export | `0x14155FE30` | `0x7FF6C966FE30` | ✅ Decompiled |
| gfx_drv_clear | via AF3DN.P export | `0x14155E020` | `0x7FF6C966E020` | ✅ Decompiled |
| gfx_drv_clear_all | via AF3DN.P export | `0x14155E190` | `0x7FF6C966E190` | ✅ Decompiled |
| gfx_drv_setviewport | via AF3DN.P export | `0x141560F80` | `0x7FF6C9670F80` | ✅ Decompiled |
| gfx_drv_setbg | via AF3DN.P export | `0x141560B40` | `0x7FF6C9670B40` | ✅ Decompiled |
| gfx_drv_setmatrix | via AF3DN.P export | `0x141560BA0` | `0x7FF6C9670BA0` | ✅ Decompiled |
| gfx_drv_blendmode | via AF3DN.P export | `0x14155DFC0` | `0x7FF6C966DFC0` | ✅ Decompiled |
| gfx_drv_setrenderstate | via AF3DN.P export | `0x141560DA0` | `0x7FF6C9670DA0` | ✅ Decompiled |
| gfx_drv_setrenderstate_2D | via AF3DN.P export | `0x141560DE0` | `0x7FF6C9670DE0` | ✅ Decompiled |
| gfx_drv_setrenderstate_3D | via AF3DN.P export | `0x141560E30` | `0x7FF6C9670E30` | ✅ Decompiled |
| gfx_drv_setrenderstate_lines | via AF3DN.P export | `0x141560F30` | `0x7FF6C9670F30` | ✅ Decompiled |
| gfx_drv_load_texture | via AF3DN.P export | `0x1415604E0` | `0x7FF6C96704E0` | ✅ Decompiled |
| gfx_drv_unload_texture | via AF3DN.P export | `0x1415611A0` | `0x7FF6C96711A0` | ✅ Decompiled |
| gfx_drv_palette_changed | via AF3DN.P export | `0x141560A90` | `0x7FF6C9670A90` | ✅ Decompiled |
| gfx_drv_write_palette | via AF3DN.P export | `0x1415612B0` | `0x7FF6C96712B0` | ✅ Decompiled |
| gfx_drv_draw_flat_smooth_2D | via AF3DN.P export | `0x14155E410` | `0x7FF6C966E410` | ✅ Decompiled |
| gfx_drv_draw_textured2D | via AF3DN.P export | `0x14155EB00` | `0x7FF6C966EB00` | ✅ Decompiled |
| gfx_drv_draw_paletted2D | via AF3DN.P export | `0x14155E800` | `0x7FF6C966E800` | ✅ Decompiled |
| gfx_drv_draw_flat_smooth_3D | via AF3DN.P export | `0x14155E620` | `0x7FF6C966E620` | ✅ Decompiled |
| gfx_drv_draw_lines | via AF3DN.P export | `0x14155E710` | `0x7FF6C966E710` | ✅ Decompiled |
| gfx_drv_draw_deferred | via AF3DN.P export | `0x14155E2D0` | `0x7FF6C966E2D0` | ✅ Decompiled |
| gfx_drv_field_64 | via AF3DN.P export | `0x14155EF70` | `0x7FF6C966EF70` | ✅ Decompiled |
| gfx_drv_field_74 | via AF3DN.P export | `0x14155F110` | `0x7FF6C966F110` | ✅ Decompiled |
| gfx_drv_field_78 (3D mesh) | via AF3DN.P export | `0x14155F170` | `0x7FF6C966F170` | ✅ Decompiled |
| gfx_drv_field_80 | via AF3DN.P export | `0x14155FD20` | `0x7FF6C966FD20` | ✅ Decompiled |
| gfx_drv_field_84 | via AF3DN.P export | `0x14155FD40` | `0x7FF6C966FD40` | ✅ Decompiled |
| gfx_drv_textured3D_dispatch | via AF3DN.P export | `0x140021230` | `0x7FF6C8131230` | ✅ No-op stub |

**Hooking strategy for 2026:** In original FF7, FFNx replaces AF3DN.P DLL exports. In 2026, these functions are compiled in. Hook by:
- **Pattern scanning** the function prologues in decrypted memory
- **Inline hooking** (JMP redirect at function start)
- Functions are at known disk RVAs; apply ASLR delta at runtime

---

## 2. File I/O Hooks — MAPPED via Shim Table ✅

The 2026 binary shims Win32 file I/O through the fake_win layer. The original FF7 code calls CreateFile/ReadFile/WriteFile, and the shim functions translate to BaseEngine's file system.

| Shim Function | Runtime Address | Params | Enabled | FFNx Equivalent |
|--------------|----------------|--------|---------|-----------------|
| `CreateFileA` | `0x7FF6C9683DE0` | 7 | ✅ | `common_externals.open_file` |
| `CloseHandle` | `0x7FF6C9683CD0` | 1 | ✅ | `common_externals.close_file` |
| `SetFilePointer` | `0x7FF6C9685390` | 4 | ✅ | `common_externals.seek_file` |
| `ReadFile` | `0x7FF6C9684C60` | 5 | ✅ | `common_externals.read_file` |
| `WriteFile` | `0x7FF6C9685620` | 5 | ✅ | `common_externals.write_file` |
| `GetFileType` | `0x7FF6C9684450` | 1 | ✅ | — |

**FFNx strategy:** Hook `CreateFileA` shim to intercept file paths and redirect to mod files. Hook `ReadFile` for LGP-level interception. The LGP functions in the original FF7 are built ON TOP of these file I/O primitives, so hooking at this level captures everything.

**Note:** LGP-specific functions (lgp_open, lgp_read, etc.) are NOT in the shim table — they're higher-level game code that calls these shim functions. To find them, decompile `CreateFileA` shim and trace its callers, or search for the LGP path strings (`field/fflevel.lgp`, etc.).

---

## 3. Audio Hooks — MAPPED via Shim Table ✅

### 3a. MIDI/Music (fw_midi_* shims — DotEmu's BaseEngine MusicManager)

| Shim Function | Runtime Address | Params | Enabled | FFNx Equivalent |
|--------------|----------------|--------|---------|-----------------|
| `fw_midi_init` | `0x7FF6C96827E0` | 2 | ✅ | `common_externals.midi_init` |
| `fw_midi_play` | `0x7FF6C9682880` | 3 | ❌ | `common_externals.play_midi` |
| `fw_midi_stop` | `0x7FF6C96829B0` | 0 | ❌ | `common_externals.stop_midi` |
| `fw_midi_cross_fade` | `0x7FF6C9682770` | 2 | ❌ | — (new in 2026) |
| `fw_midi_pause` | `0x7FF6C9682850` | 0 | ❌ | `common_externals.pause_midi` |
| `fw_midi_restart` | `0x7FF6C9682910` | 0 | ❌ | — |
| `fw_midi_status` | `0x7FF6C9682980` | 0 | ✅ | `common_externals.midi_status` |
| `fw_midi_set_master_volume` | `0x7FF6C9682940` | 1 | ❌ | `common_externals.set_midi_volume` |
| `fw_midi_set_volume` | `0x7FF6C9682950` | 1 | ❌ | — |
| `fw_midi_set_volume_trans` | `0x7FF6C9682960` | 2 | ❌ | — |
| `fw_midi_set_tempo` | `0x7FF6C8131230` | 1 | ❌ | No-op stub |

**Note:** Many fw_midi entries are `enabled=0` — they exist but the original game code's MIDI calls are mostly disabled. The MusicManager handles music playback natively. FFNx would hook `fw_midi_play` to replace music with OGG/VGMStream files.

### 3b. DirectSound SFX (shim functions → BaseEngine AudioSystem)

| Shim Function | Runtime Address | Params | Enabled | FFNx Equivalent |
|--------------|----------------|--------|---------|-----------------|
| `DirectSoundCreate` | `0x7FF6C9668310` | 3 | ✅ | `ff7_externals.sound_operation` (higher level) |
| `IDirectSound::SetCooperativeLevel` | `0x7FF6C8133B40` | 3 | ✅ | Return-arg stub |
| `IDirectSound::CreateSoundBuffer` | `0x7FF6C9668960` | 4 | ✅ | — |
| `IDirectSound::DuplicateSoundBuffer` | `0x7FF6C9668C10` | 3 | ✅ | — |
| `IDirectSound::Release` | `0x7FF6C8133B40` | 1 | ✅ | Return-arg stub |
| `IDirectSoundBuffer::Play` | `0x7FF6C9668620` | 4 | ✅ | SFX trigger |
| `IDirectSoundBuffer::Lock` | `0x7FF6C9668540` | 8 | ✅ | Buffer write |
| `IDirectSoundBuffer::Unlock` | `0x7FF6C96688D0` | 5 | ✅ | Buffer commit |
| `IDirectSoundBuffer::GetStatus` | `0x7FF6C96684F0` | 2 | ✅ | — |
| `IDirectSoundBuffer::Release` | `0x7FF6C9668680` | 1 | ✅ | — |
| `IDirectSoundBuffer::Stop` | `0x7FF6C96688A0` | 1 | ✅ | — |
| `IDirectSoundBuffer::SetPan` | `0x7FF6C9668840` | 2 | ✅ | — |
| `IDirectSoundBuffer::SetVolume` | `0x7FF6C9668870` | 2 | ✅ | — |
| `IDirectSoundBuffer::SetFrequency` | `0x7FF6C9668810` | 2 | ✅ | — |
| `IDirectSoundBuffer::GetCurrentPosition` | `0x7FF6C9668490` | 3 | ✅ | — |
| `IDirectSoundBuffer::SetCurrentPosition` | `0x7FF6C96687E0` | 2 | ✅ | — |

### 3c. ACM Stream (audio codec decompression)

| Shim Function | Runtime Address | Params | Enabled |
|--------------|----------------|--------|---------|
| `acmStreamSize` | `0x7FF6C9683630` | 4 | ✅ |
| `acmStreamOpen` | `0x7FF6C9683540` | 8 | ✅ |
| `acmStreamConvert` | `0x7FF6C9683120` | 3 | ✅ |
| `acmStreamPrepareHeader` | `0x7FF6C9683600` | 3 | ✅ |
| `acmStreamUnprepareHeader` | `0x7FF6C9683600` | 3 | ✅ |
| `acmStreamClose` | `0x7FF6C96830E0` | 2 | ✅ |

**FFNx strategy:** Hook `fw_midi_play` and `fw_midi_init` for music replacement. Hook `IDirectSoundBuffer::Play` and `Lock/Unlock` for SFX replacement. The ACM stream functions handle ADPCM decompression of the original .wav SFX files.

---

## 4. Game Logic Hooks — NOT in Shim Table (Need IDA Analysis)

**Important:** Game logic functions (field, battle, menu, world map) are NOT in the 203-entry shim table. The shim table only covers Win32 API shims and the gfx_drv/fw_movie/fw_midi interfaces. Game logic functions are the recompiled original FF7 code — they're somewhere in the 22.3MB .text section.

**Finding strategies:**
1. **Trace from shim callers** — decompile the shim functions and follow what calls them
2. **Search for known constants** — `0xDBFD38` (savemap), unique integer constants from original FF7
3. **Search for known strings** — "flevel", "scene.bin", "kernel.bin" etc. (note: kernel.bin/scene.bin not found as direct strings in dump — may be in embedded ff7_ja/ff7_en resources)
4. **Use .pdata exception table** — create ALL functions in .text section, then use xrefs

### Field Module (Partially Identified — Session 5-7)
| FFNx Function | Purpose | 2026 Status |
|---------------|---------|-------------|
| `ff7_externals.read_field_file` | Load field | ❓ Need IDA analysis |
| `ff7_externals.field_load_textures` | Field textures | ❓ |
| `ff7_externals.field_layer1-4_pick_tiles` | Background layers | ❓ |
| `ff7_externals.field_draw_everything` | Field render main | ❓ |
| `ff7_externals.execute_opcode` | Field script VM | **❌ NOT candidate_execute_opcode** — that function (553KB) is a script VM state accessor, not the dispatcher. Actual dispatcher not yet found. |

### Handle Dereference Helpers (Session 5)
| Function | Address | Purpose |
|----------|---------|---------|
| `handle_deref_dword` | `0x7FF6C838FE90` | Resolves handle → reads DWORD at object |
| `handle_deref_word` | `0x7FF6C838FEB0` | Resolves handle → reads WORD at object |

### Japanese Font Loader (Session 5)
| Function | Address | Purpose |
|----------|---------|---------|
| `sub_7FF6C9681D90` | `0x7FF6C9681D90` | Loads `jafont_1.tim` through `jafont_6.tim`, allocates 312-byte struct |

### Top 10 Largest Functions (Game Logic Candidates)
| Size | Address | Callers | Likely Module |
|------|---------|---------|--------------|
| 553,137 bytes | `0x7FF6C8D19A10` | `sub_7FF6C8D046A0` | **Script VM state accessor** — NOT opcode dispatcher (2089 handle_deref, 1124 GSA, no indirect jumps, no switch pattern) |
| 333,912 bytes | `0x7FF6C8207AF0` | 5 callers | **BATTLE MAIN LOOP** — 62 callees, 1652 GSA calls, 1650 handle_deref, character data (6892 bytes/char), entry via function pointer dispatch from `sub_7FF6C8270DE0` |
| 128,214 bytes | `0x7FF6C9571B50` | `sub_7FF6C9566E60` | **Field script VM helper** — 9 callees, virtual stack manipulation, function pointer dispatch |
| 110,721 bytes | `0x7FF6C919F5F0` | `sub_7FF6C91BAEF0` (×3) | **Field text/dialogue processing** — 11 callees, GSA + handle_deref |
| 75,194 bytes | `0x7FF6C8BC2B80` | 4 callers (+1 via FP) | **Battle UI/State subsystem** — 20 callees, 6 local helpers, connected to battle dispatch |
| 61,445 bytes | `0x7FF6C9331AA0` | `sub_7FF6C934A4C0` (via FP dispatch) | **Script VM opcode handler** — 64 callees, entry points have NO XREFS, region 0x7FF6C930xxxx-0x7FF6C935xxxx is script VM opcode cluster |
| 56,417 bytes | `0x7FF6C9307DC0` | none (FP dispatch) | **Script VM field/text opcode handler** — 48 callees, font functions in 0x7FF6C968xxxx |
| 53,474 bytes | `0x7FF6C90D3CE0` | none (FP dispatch) | **Script VM focused opcode handler** — 9 callees, VM stack manipulation |
| 51,603 bytes | `0x7FF6C95FB250` | 72 calls from `sub_7FF6C95A02C0` (60), wrappers | **Script VM high-frequency helper** — 7 callees, entry via function pointer dispatch, core operation in script interpretation |
| 48,022 bytes | `0x7FF6C95B6E50` | `sub_7FF6C9566E60` | **Script VM opcode handler** — same caller as #3, uses VM stack |

### Script VM Infrastructure (Session 6 Discovery)
| Global | Address | Purpose |
|--------|---------|---------|
| Virtual Stack Pointer | `xmmword_7FF6CA1495C8` | FF7 scripting VM stack pointer |
| Virtual Base Pointer | `xmmword_7FF6CA1495B8` | FF7 scripting VM base pointer |
| Return Helper | `sub_7FF6C815B2D0` | VM return/dispatch with timing control |
| Stack Helper | `sub_7FF6C963BE80` | Push/pop to virtual stack |
| Memory Copy Helper | `sub_7FF6C904CBD0` | Alignment-aware memcpy for VM |

**Script Constants Found:**
- 131097 (0x20059) - Script opcode or constant
- 8086600 (0x7B77B8) - Game data handle
- 8086664 (0x7B77F8) - Game data handle
- Handles 0xF6E0F0, 0xF6E0F4, 0xF6E0E8 - Script state handles
- Handle 0xDB2BB8 - Near savemap region (0xDBFD38)

### Battle Module (Session 8 Analysis — Partially Identified)
| FFNx Function | Purpose | 2026 Status |
|---------------|---------|-------------|
| `ff7_externals.battle_enter` | Enter battle | `sub_7FF6C8270DE0` (334KB via wrapper) |
| `ff7_externals.battle_loop` | Battle main loop | `sub_7FF6C8207AF0` (334KB state machine) |
| `ff7_externals.magic_thread_start` | Spell effects | ❓ |

**Battle State Machine (sub_7FF6C8270DE0):**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8270DE0` |
| Size | 3,826 bytes (0xEF2) |
| Callers | **NO XREFS** (function pointer dispatch) |
| Callees | Calls battle init, setup, and main loop functions |
| VM Stack | Uses `xmmword_7FF6CA1495C8` (Script VM integration) |
| Purpose | Battle state machine dispatcher — handles states 0-6 |

**Battle Main Loop (sub_7FF6C8207AF0):**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C8207AF0` |
| Size | 333,912 bytes (334KB) |
| Callers | 5 (via wrapper functions) |
| Callees | 62 unique |
| GSA Calls | 1,652 |
| Handle Deref Calls | 1,650 (855 dword + 795 word) |
| Top Callee | `sub_7FF6C825A7E0` (40 calls — character data accessor) |
| Purpose | Massive battle processing function |

**Battle Character Data Accessor (sub_7FF6C825A7E0):**
| Property | Value |
|----------|-------|
| Address | `0x7FF6C825A7E0` |
| Size | ~700 bytes |
| Key Constant | 6892 (0x1AEC) — FF7 character data size |
| Key Constant | 12456372 (0xBE28D4) — Character data offset |
| Purpose | Access character data in battle (stats, HP, MP, etc.) |

**Battle Memory Addresses:**
| Address | Purpose |
|---------|---------|
| `0x9AE108` | Battle state (0=init, 1=started, 2=continue, 3=setup) |
| `0xBE28D4` | Character data base offset |
| `0xBFCDFC` | Battle phase (0-6) |
| `0xBF2DEC` | Battle status |
| `0xBF2A30` | Battle flag |
| `0xCC0828` | Battle flag |
| `0xBE1128` | Battle data pointer |
| `0xC05F7C` | Screen width (512) |

**Battle Function Region:** `0x7FF6C820xxxx - 0x7FF6C82Axxxx`
- Core battle logic in this region
- Uses VM stack infrastructure (`xmmword_7FF6CA1495C8`)
- Entry points dispatched via function pointer table

### Menu Module (Session 11 Analysis — Partially Identified)
| FFNx Function | Purpose | 2026 Status |
|---------------|---------|-------------|
| `ff7_externals.kernel2_get_text` | Game text lookup | **INTEGRATED** — Text embedded in resources, accessed via resource_allocator patterns |
| `ff7_externals.menu_draw_everything` | Menu render | **Script VM based** — Menu scripts run through script VM infrastructure (0x7FF6C930xxxx-0x7FF6C95Fxxxx) |

**Menu Architecture Discovery:**

The 2026 build does NOT have a separate "menu module" in the traditional sense. Instead:

1. **Text Rendering:** Native Japanese support via `jafont_*.tim` loading
   - Japanese Font Loader: `0x7FF6C9681D90` (312-byte struct, loads jafont_1.tim through jafont_6.tim)
   - Called from: `sub_7FF6C96842D0` (initialization wrapper)

2. **Menu Scripts:** Run through Script VM infrastructure
   - Script VM opcode handlers: `0x7FF6C930xxxx - 0x7FF6C95Fxxxx`
   - Field/text opcode handler: `sub_7FF6C9307DC0` (56KB, 48 callees)
   - Text/dialogue processing: `sub_7FF6C919F5F0` (110KB) — also used by battle for text display

3. **kernel.bin/kernel2.bin:** NOT found as direct file strings
   - Likely embedded in ff7_ja/ff7_en resources
   - Text lookup via resource_allocator patterns (command ID 0xDBFD38 for savemap)
   - No CreateFileA xrefs to "kernel" strings (VEH dispatch bypasses direct references)

4. **Menu State:** Stored in savemap accessed via handle `0xDBFD38`
   - global_state_accessor(0xDBFD38) returns savemap pointer
   - Menu state variables in savemap at known offsets

**Menu Function Candidates (Need Further Analysis):**
| Address | Size | Notes |
|---------|------|-------|
| `sub_7FF6C9681D90` | ~2KB | Japanese font loader — menu text rendering |
| `sub_7FF6C919F5F0` | 110KB | Text/dialogue processing — used by field and battle |
| `sub_7FF6C9307DC0` | 56KB | Script VM field/text opcode handler — menu scripts |
| `sub_7FF6C96842D0` | 19 bytes | Font init wrapper (calls font loader) |

**Recommendation:** Hook at the Script VM level for menu modifications, or hook text rendering functions for font replacement. The kernel2_get_text equivalent is handled by resource_allocator calls to embedded resources.

### World Map Module (Need IDA Analysis)
| FFNx Function | Purpose | 2026 Status |
|---------------|---------|-------------|
| `ff7_externals.world_update_player` | World movement | ❓ |
| `ff7_externals.worldmap_battle_toggle` | Encounter toggle | ❓ |

---

## 5. Text/Font Rendering Hooks

These are critical for Japanese language support:

| FFNx Function | Purpose | 2026 Status |
|---------------|---------|-------------|
| `ff7_externals.draw_character` | Draw single char | ❓ (but 2026 has native Japanese!) |
| `ff7_externals.field_submit_draw_text_640x480_6E706D` | Field text | ❓ |
| `ff7_externals.common_submit_draw_char_from_buffer_6F564E` | Char buffer draw | ❓ |
| `ff7_externals.menu_draw_everything_6CC9D3` | Menu text | ❓ |
| `ff7_externals.battle_draw_menu_everything_6CEE84` | Battle text | ❓ |

**Note:** The 2026 version has native Japanese support with `jafont_%d.tim` loading. FFNx's Japanese text patches may be unnecessary for basic Japanese play. However, enhanced font rendering (SDF fonts, custom character sets) would still need these hooks.

---

## 6. Save/Load Hooks — MAPPED ✅ (Session 12)

The 2026 build uses Steam Cloud for save files, with a save data conversion layer for compatibility.

### Save File Path Handling

| Function | Address | Purpose |
|----------|---------|---------|
| `shim_CreateFileA` | `0x7FF6C9683DE0` | File open shim — routes "save" prefix to save directory |
| `shim_ReadFile` | `0x7FF6C9684C60` | File read shim — triggers save data conversion for 65100-byte reads |
| `shim_WriteFile` | `0x7FF6C9685620` | File write shim — writes save data |
| `sub_7FF6C968B220` | `0x7FF6C968B220` | **Get save directory path** — uses Steam API for user ID |
| `sub_7FF6C968B660` | `0x7FF6C968B660` | **Save data conversion** — converts between formats (4340 bytes/slot) |
| `sub_7FF6C968B330` | `0x7FF6C968B330` | Get config directory path |

### Save Directory Structure

```
{Steam User Data Dir}/{Steam64 ID}/
    └── save/
        └── *.ff7 (save files)
```

- Save directory buffer: `byte_7FF6CA1A1C20` (260 bytes)
- Uses Steam API: `steam_api64_SteamInternal_ContextInit`

### Save Data Format

| Property | Value |
|----------|-------|
| Slots | 15 |
| Bytes per slot | 4340 (0x10F4) |
| Total save size | 65,100 bytes (0xFE2C) |
| Checksum | CRC16 (polynomial 0x1021) |
| Source file | `SaveDataConvertLocation.cpp` |

### Save Data Offsets (per slot, 4340 bytes)

| Offset | Size | Purpose |
|--------|------|---------|
| 0x0000 | 4 | CRC16 checksum |
| 0x0004 | 4336 | Save data (checksummed) |
| 0x0064 | 132 | Character 0 name/data (9 characters, 132 bytes each) |
| 0x0064 | 11×132 | All character data (offsets: 0x64 + n×132) |
| 0x0B8C | 2 | Location ID (0-1 = field, 2 = world map, 3-4 = battle?) |
| 0x0B8E | 2 | Sub-location ID |
| 0x0D38 | 256 | Location name buffer |
| 0x0E9C | 132 | Party leader name |
| 0x0F1C | ? | Additional location data |

### Save Data Conversion Function (sub_7FF6C968B660)

- **Called from:** `shim_ReadFile` at `0x7FF6C9684D28` when reading 65,100 bytes
- **Trigger:** Read of exactly 65,100 bytes with save flag set
- **Purpose:** Convert between FF7 save format and Steam format
- **Constants:**
  - `0x1021` — CRC16 polynomial
  - `11` — Number of characters (charId < 11 check)
  - `4340` — Save slot size
  - `15` — Number of save slots
  - `word_7FF6C8110000[11749900]` — Location name table base

### Path Routing in CreateFileA Shim

```c
if (strncmp(path, "save", 4) == 0) {
    // Route to Steam save directory
    save_dir = sub_7FF6C968B220(); // Get Steam user save path
    full_path = combine(save_dir, path);
}
else if (strncmp(path, "ff7input.cfg", 12) == 0) {
    // Route to config directory
    config_dir = sub_7FF6C968B330();
    full_path = combine(config_dir, path);
}
else if (strstr(path, "APP.LOG")) {
    return -1; // BLOCKED — no logging
}
else {
    // Route to game data directory
    data_dir = unk_7FF6C968AE70();
    full_path = combine(data_dir, path);
}
```

### File Handle Table

| Property | Value |
|----------|-------|
| Base address | `unk_7FF6C983FA80` |
| Entry size | 212 bytes |
| First free slot | Index 6 |
| Max entries | ~20 (bounded by `byte_7FF6C9840BDC`) |

### FFNx Hook Strategy for Save/Load

1. **Hook `shim_CreateFileA`** (0x7FF6C9683DE0)
   - Intercept file paths for mod files
   - Redirect "save" paths to custom save location
   - Block unwanted file access

2. **Hook `shim_ReadFile`** (0x7FF6C9684C60)
   - Intercept save data reads (65,100 bytes trigger)
   - Call `sub_7FF6C968B660` for save conversion, or skip for raw reads
   - Modify save data before conversion

3. **Hook `shim_WriteFile`** (0x7FF6C9685620)
   - Intercept save data writes
   - Modify save data before writing
   - Track save slot usage

4. **Hook `sub_7FF6C968B660`** (Save Data Conversion)
   - Direct save data manipulation
   - Convert between formats
   - Add/modify saved data fields

### Related FFNx Functions

| FFNx Function | 2026 Address | Notes |
|---------------|--------------|-------|
| `ff7_externals.save_file` | `shim_CreateFileA` route | Via "save" path prefix |
| `ff7_externals.load_file` | `shim_ReadFile` + conversion | 65,100-byte read triggers conversion |
| `ff7_externals.savemap` | `0xDBFD38` handle | Savemap via global_state_accessor |

---

## 7. Input Hooks — MAPPED via Shim Table ✅

The original FF7 code uses DirectInput. DotEmu shims this through SDL2.

| Shim Function | Runtime Address | Params | Enabled | FFNx Equivalent |
|--------------|----------------|--------|---------|-----------------|
| `DirectInputCreateA` | `0x7FF6C9667660` | 4 | ✅ | `ff7_externals.dinput_createdevice` |
| `IDirectInputA::CreateDevice` | `0x7FF6C96676A0` | 4 | ✅ | — |
| `IDirectInputDeviceA::SetDataFormat` | `0x7FF6C8133B40` | 2 | ✅ | Return-arg stub |
| `IDirectInputDeviceA::SetCooperativeLevel` | `0x7FF6C8133B40` | 3 | ✅ | Return-arg stub |
| `IDirectInputDeviceA::SetProperty` | `0x7FF6C8133B40` | 3 | ✅ | Return-arg stub |
| `IDirectInputDeviceA::GetCapabilities` | `0x7FF6C9667740` | 2 | ✅ | — |
| `IDirectInputDeviceA::Acquire` | `0x7FF6C8133B40` | 1 | ✅ | Return-arg stub |
| `IDirectInputDeviceA::GetDeviceState` | `0x7FF6C96677E0` | 3 | ✅ | `common_externals.get_keyboard_state` |
| `IDirectInputDeviceA::GetDeviceData` | `0x7FF6C9667780` | 5 | ✅ | — |
| `GetAsyncKeyState` | `0x7FF6C8133B40` | 1 | ✅ | Return-arg stub |
| `joyGetDevCapsA` | `0x7FF6C9685720` | 3 | ✅ | `ff7_externals.get_gamepad` |
| `joyGetPosEx` | `0x7FF6C8133B40` | 2 | ✅ | `ff7_externals.update_gamepad_status` |

**FFNx strategy:** Hook `GetDeviceState` for keyboard, `joyGetDevCapsA` for gamepad. Many DirectInput calls are stubbed out (return-arg) since SDL2 handles the actual input. The game code calls these shims which translate to SDL2 under the hood.

**Note:** The `joyGetPosEx` shim points to the return-arg stub (`0x7FF6C8133B40`) — joystick position reading is handled entirely by SDL2, the original Win32 joystick API is bypassed.

---

## 8. FPS Limiter Hooks

FFNx replaces 11 module-specific FPS limiters:

| FFNx Function | Purpose | 2026 Status |
|---------------|---------|-------------|
| `ff7_externals.fps_limiter_field` | Field FPS | ❓ |
| `ff7_externals.fps_limiter_battle` | Battle FPS | ❓ |
| `ff7_externals.fps_limiter_worldmap` | World FPS | ❓ |
| `ff7_externals.fps_limiter_swirl` | Swirl FPS | ❓ |
| `ff7_externals.fps_limiter_coaster` | Coaster FPS | ❓ |
| `ff7_externals.fps_limiter_condor` | Condor FPS | ❓ |
| `ff7_externals.fps_limiter_highway` | Highway FPS | ❓ |
| `ff7_externals.fps_limiter_snowboard` | Snowboard FPS | ❓ |
| `ff7_externals.fps_limiter_chocobo` | Chocobo FPS | ❓ |
| `ff7_externals.fps_limiter_submarine` | Submarine FPS | ❓ |
| `ff7_externals.fps_limiter_credits` | Credits FPS | ❓ |

**Note:** 2026 already has FPS timing in gfx_drv_flip (60fps/30fps). These may be handled differently.

---

## Key Differences: Original vs 2026 Hooking Architecture

### Original FF7 (32-bit, FFNx approach):
```text
ff7_en.exe → loads AF3DN.P (graphics DLL)
FFNx replaces AF3DN.P with its own implementation
FFNx also does inline hooking of ff7_en.exe functions
All addresses are static (no ASLR)
```

### 2026 FF7 (64-bit, new approach needed):
```text
FFVII.exe is XTEA-encrypted on disk
At runtime, embedded DLL decrypts .text section
ASLR randomizes base address each launch
No external graphics DLL to replace

New injection approach:
1. SDL2.dll proxy → loads after decryption
2. Pattern scan decrypted memory for known function signatures
3. Inline hook at found addresses (must handle 64-bit JMP trampolines)
4. ASLR delta calculated at runtime
```

### Critical Architecture Change:
- **Original:** FFNx IS the graphics driver (replaces AF3DN.P entirely)
- **2026:** FFNx must HOOK the compiled-in graphics driver
- **Implication:** Instead of implementing gfx_drv_* from scratch, we intercept calls at the function level and add/modify behavior

---

## 11. Decompiled Shim Function Analysis (Non-GFX)

### shim_CreateFileA (`0x7FF6C9683DE0`) — File I/O Entry Point

**File Handle Table:** 212-byte entries starting at `unk_7FF6C983FA80`. Free slot search iterates from index 6 through `byte_7FF6C9840BDC`.

**Path routing:**
- Default: builds path from working directory (`unk_7FF6C968AE70()`)
- `"save"` prefix → save directory (`unk_7FF6C968B220()`)
- `"ff7input.cfg"` → config directory (`unk_7FF6C968B330()`)
- `"ff7sound.cfg"` → special sound config with sync check
- `"APP.LOG"` → **blocked** (returns -1)
- Other files ending with specific suffix → data directory

**Access mode translation:** `0x80000000` → 5 (read), `0xC0000000` → 9 (r/w); creation modes 2/4 → add `0x10` (create)

**BaseEngine file open:** `unk_7FF6C9701410(path_obj, flags)`

**For FFNx:** Hook this function to intercept file paths and redirect to mod files (direct mode / 7th Heaven IRO).

### shim_ReadFile (`0x7FF6C9684C60`) — File Read

- File handle → 212-byte entry → stream object → vtable[4] (Read method)
- **Buffer is a page-table handle** — resolved via `global_state_accessor(a2)`
- **Save detection:** When exactly 65100 bytes read and save flag set → calls `unk_7FF6C968B660` (save data conversion)
- Read counters: `dword_7FF6CA18F62C`, `dword_7FF6CA18F628`

### shim_fw_midi_play (`0x7FF6C9682880`) — Music Playback

- Gets track data via `resource_allocator(dword_7FF6CA149AF0, 1, track_id)`
- **Savemap progress check:** Reads `savemap[1490]` (`global_state_accessor(0xDBFD38) + 2980`)
  - Progress < 275 → play normally
  - 275 ≤ progress < 278 → return 278 (block playback — final battle sequence)
  - Progress ≥ 278 → play normally
- **MusicManager::Play** at `unk_7FF6C8152DF0(manager, track_data, track_id, 0)`

### shim_fw_movie_prepare (`0x7FF6C9682A00`) — FMV Playback

- **Path format:** `"%s/data/lang-%s/movies/%s.avi"` — language-specific!
- Special movie handling: "ending2"/"jenova_e"/"ending3" → set byte_7FF6C980ED58 flag
- Logo detection: "sqlogo"/"eidoslogo" → skip movie (return 0)
- **Movie name → ID table:** `off_7FF6C983F420` (up to 99 entries, pairs of string+int)
- **VideoManager** at `off_7FF6CA149548`
- **Movie state handle:** `0xDE655C`
- **Resource registration:** `resource_allocator(4280881, 1, &movie_path)`
- **Movie state struct** at `qword_7FF6CA18CF08`: +12 (mode), +504 (flag), +508-516 (state)

### shim_DirectSoundCreate (`0x7FF6C9668310`) — Audio Init

- Creates 576-byte AudioSystem object
- **AudioSystem singleton:** `qword_7FF6CA149290`
- **Buffer handle management:** Sorted tree at `off_7FF6CA149A50`, 64 sound buffer slots
- **AudioSystem::Init** at `unk_7FF6C8150890`
- Allocates resource_allocator(6684065, 3, 4096, 0, 95) for buffer pool

### shim_IDirectInputDevice_GetDeviceState (`0x7FF6C96677E0`) — Input

- **InputManager singleton:** `off_7FF6CA1492E8`
- **Keyboard state buffer:** `byte_7FF6CA149940` (256 bytes, DirectInput format)
- Two modes: 16 bytes = mouse state (`unk_7FF6CA149A40`), 256 bytes = keyboard
- **14 button mappings** (indices 0-13): checked via `unk_7FF6C8151D20(inputMgr, button_id, 0)`
- **Button-to-scancode table:** `unk_7FF6C8110000 + 23374048` = `0x7FF6C9757C60`
- **Gamepad axes:** 4 analog inputs (16-19) with magnitude deadzone (>0.9 = active)
- **Axis-to-scancode map:** `dword_7FF6C980EDEC` (4 bytes, one per axis)
- Special mode handling: mode 7 = PC settings, mode 9/13 = specific button contexts
- **Assert:** `W:\proj\ff7\kitamura\Material\BaseEngine\InputManager.h:88`

---

## 12. Key Global Singletons Discovered

| Singleton | Address | Size | Purpose |
|-----------|---------|------|---------|
| MusicManager | `qword_7FF6CA149390` | 1136 bytes | Music playback (MusicManager.cpp) |
| AudioSystem | `qword_7FF6CA149290` | 576 bytes | SFX/DirectSound (DirectSound.cpp) |
| VideoManager | `off_7FF6CA149548` | ? | FMV playback (VideoManager.cpp) |
| InputManager | `off_7FF6CA1492E8` | ? | Input handling (InputManager.cpp) |
| Main Game State | `qword_7FF6CA149CD8` | ? | Set by gfx_drv_new_dll |
| File Handle Table | `unk_7FF6C983FA80` | 212 bytes/entry | Max ~20 files open |
| Keyboard State | `byte_7FF6CA149940` | 256 bytes | DirectInput format |
| Page Table Array | `qword_7FF6C9849010` | QWORD array | Handle → object resolver |

---

## Strategy for Finding Remaining Hooks

### Phase 1: Use the 203-Entry Shim Table (FASTEST)

The shim table at disk address `0x1416D20B8` (runtime: apply ASLR delta) contains function pointers for ALL game subsystems. From the previous session handoff, it includes:
- All 49 gfx_drv_* entries (mapped ✅)
- IDirectSound/IDirectSoundBuffer entries
- IDirectInput entries
- fw_movie_* entries (FMV playback)
- acmStream* entries (audio codec)
- Win32 API shims (CreateWindowExA, SetWindowLong, etc.)

**Action:** Decompile the shim table resolver to map ALL function pointers, not just gfx_drv.

### Phase 2: String Cross-References

Search the dump for known string literals and trace back to their callers:
```
"flevel.lgp"     → field file loading
"battle.lgp"     → battle asset loading
"kernel.bin"     → kernel loading
"kernel2.bin"    → text data loading
"scene.bin"      → battle scene data
".ogg"           → music playback
"SavedGame"      → save/load system
```

### Phase 3: Known Constant Pattern Scan

Some game functions use distinctive constant values:
- `0xDBFD38` — savemap address (seen in resource_allocator calls!)
- `640` (0x280) and `480` (0x1E0) — internal resolution (in setviewport)
- Field opcode dispatch table — array of function pointers
- Battle state machine function table

---

## Savemap Discovery: Already Found!

The `resource_allocator` function at `0x7FF6C815AB00` is called with command ID `0xDBFD38` in several places. In the original FF7, `0xDBFD38` is the savemap address. In the 2026 build, this same value appears as a command ID for the `global_state_accessor` — meaning the savemap is accessed via handle `0xDBFD38` through the page table system!

```
savemap_ptr = global_state_accessor(0xDBFD38)
// Upper 20 bits: 0xDBFD38 >> 12 = 0xDBFD3 (page index)
// Lower 12 bits: 0xDBFD38 & 0xFFF = 0xD38 (offset in page)
```

This means ANY known 32-bit address from the original FF7 that appears as a constant in the 2026 binary is likely a handle into the page table system. This is a MASSIVE shortcut for finding game data structures.

---

## 13. Shim Dispatch Architecture (CRITICAL DISCOVERY)

### How Game Code Calls Win32 APIs in the 2026 Build

```text
Original FF7 game code (recompiled as 64-bit)
    ↓ calls via handle/index
Dispatch Table at 0x7FF6CA05A010
    ↓ pointer to shim table entry
Shim Table at 0x7FF6C97E20B8  (203 entries, 32 bytes each)
    ↓ function pointer from entry+8
Shim Function (e.g., shim_CreateFileA at 0x7FF6C9683DE0)
    ↓ translates to
BaseEngine API (file I/O, audio, video, input)
```

### Dispatch Table
- **Address:** `0x7FF6CA05A010` (base + 4092418*8)
- **Format:** Array of QWORDs, each pointing to a shim table entry
- **Indexing:** `dispatch_table[page * 4096 + slot]` → pointer to 32-byte shim entry

### Shim Table Init Function
- **Address:** `0x7FF6C814DDA0` (named `shim_table_init_and_link`)
- **Size:** 0x785 bytes (1925 bytes)
- **Purpose:** Links original FF7 import table entries to DotEmu shim functions
- **Process:**
  1. Walks the recompiled game's import descriptors (stored as page-table objects)
  2. For each imported function name, searches the 203-entry shim table for a match
  3. Stores shim entry pointer in dispatch table
  4. Stamps the import entry with handle value: `0xB0000000 | page_hi | offset`
  5. Special handling for "dotemu" prefix → maps to DotEmu registry functions (indices 16-21)
  6. Explicit registration for fw_movie_* (6 entries at offsets 4092418-4092423) and fw_midi_* (11 entries at 4092424-4092434)

### Shim Table Register Entry Function
- **Address:** `0x7FF6C814D0A0` (named `shim_table_register_entry`)
- **Size:** 0x78 bytes
- **Purpose:** Look up function name in shim table, store entry at `qword_7FF6CA049010[4096 * page + offset]`

### FFNx Hooking Strategy (Updated)

**Option A: Hook individual shim functions** (current approach)
- Inline-hook each function at its address (e.g., `0x7FF6C9683DE0` for CreateFileA)
- Pro: Simple, targeted
- Con: Need to hook many functions individually

**Option B: Patch the dispatch table entries** (NEW — enabled by this discovery)
- After `shim_table_init_and_link` runs, replace dispatch table pointers with FFNx function pointers
- Pro: Centralized, clean intercept point
- Con: Need to run after init, must understand handle system

**Option C: Hook the dispatch call site** (MOST ELEGANT)
- Find where game code resolves dispatch table entries and calls through them
- Hook that single dispatch function
- Pro: Single hook catches ALL Win32 API calls
- Con: Need to find the dispatch caller, may have performance impact

---

## 14. Exception-Based Dispatch Architecture (CRITICAL DISCOVERY — Session 4)

**Last Updated:** 2026-02-26 16:35 JST

### How the Game ACTUALLY Dispatches Win32 API Calls

The dispatch mechanism is NOT a simple function pointer table lookup. It uses **Vectored Exception Handling (VEH)** with intentional Access Violations.

### JMP Patching (`shim_inline_jmp_patcher` at `0x7FF6C9668D00`)

After `shim_table_init_and_link` populates the dispatch table, this function patches original game `CALL` instructions with 5-byte relative `JMP` instructions (`0xE9`):

```text
Original game code:  CALL [some_win32_api]
Patched to:          JMP  rel32  (where rel32 encodes 0xB0PP_OOOO metadata)
```

**The JMP offset formula:**
```
rel32 = (page << 16 | 0xB000000X) - instruction_address - 5
```

This results in an astronomically large negative offset (~1.35GB backward) pointing to UNMAPPED MEMORY. The `JMP` deliberately causes an **Access Violation**.

### Exception Handler Flow

```text
1. Game code hits patched JMP instruction
2. CPU attempts jump to unmapped address → ACCESS VIOLATION
3. VEH handler catches the exception
4. Handler reads faulting instruction, extracts 0xB0PP_OOOO metadata
5. PP = page index, OOOO = offset → looks up dispatch table
6. Dispatch table → shim table entry → actual shim function pointer
7. Handler redirects execution to the shim function
8. Shim function translates to BaseEngine API call
```

### Game Initialization Sequence

```text
sub_7FF6C814ECA0 (Main Init)
    ├── Build date: "Dec 11 2025" at "10:20:52"
    ├── Steam App ID: 3837340
    ├── Title: "FINAL FANTASY VII Steam Edition"
    ├── Asset path: "%s/resources/ff7_1.02/ff7_%s"
    ↓
sub_7FF6C814E7D0 (Game Loader)
    ├── Reads embedded ff7_en/ff7_ja binary
    ├── Allocates page table pages
    ↓
shim_table_init_and_link (0x7FF6C814DDA0)
    ├── Walks import descriptors
    ├── Stamps handles: 0xB0000000 | page_hi | offset
    ↓
shim_inline_jmp_patcher (0x7FF6C9668D00)
    ├── Patches CALL sites with JMP 0xE9
    └── JMP targets are intentionally invalid → VEH dispatch
```

### Page Allocator (`sub_7FF6C814EBD0`)

Allocates 4KB chunks and populates the global page table:
```c
page_table[handle >> 12] = allocated_memory_address;
// handle format: [20-bit page index][12-bit offset]
```

### ⚠️ CRITICAL: Current Memory Dump is PRE-INITIALIZATION

**The memory dump was taken at the DotEmu title/launcher screen BEFORE the FF7 game engine initialized.**

Evidence:
- `qword_7FF6C9849010[]` (page table) — ALL entries are `0x0`
- No inline JMP patches applied yet
- Global singletons (MusicManager, AudioSystem, etc.) may be uninitialized

**Implications:**
- ✅ gfx_drv functions are in memory (code is loaded) — decompilation works
- ✅ Shim table is in memory (static data) — function address mapping works
- ❌ Page table is empty — `global_state_accessor(handle)` returns NULL for everything
- ❌ No JMP patches visible — can't find patched call sites
- ❌ Can't trace the VEH handler — need a dump taken DURING gameplay

**Action Required:** Take a NEW memory dump while actually IN the game (past title screen, in a field or battle scene). This will give us:
1. Populated page table → can resolve all game object handles
2. Patched JMP sites → can find every dispatched API call location
3. Initialized singletons → can inspect live game state
4. VEH handler registered → can find and decompile the exception dispatcher

### FFNx Hooking Strategy (Updated — Post VEH Discovery)

**Option D: Register own VEH handler BEFORE game's handler** (NEW — MOST POWERFUL)
- Install a Vectored Exception Handler with higher priority than the game's
- Intercept the Access Violations before the game's handler
- Decode the `0xB0PP_OOOO` metadata yourself
- Route to FFNx implementations OR forward to game's handler
- Pro: Single hook point catches ALL API dispatch, no patching needed
- Con: Performance overhead from exception handling on every API call

**Option E: Replace the JMP targets after game init** (ALTERNATIVE)
- After game boots and JMP patches are applied, scan for `0xE9` JMP opcodes
- Replace JMP rel32 offsets to point to FFNx trampolines instead of invalid addresses
- Pro: No exception overhead, direct function call
- Con: Must run after game init, must find all patched sites

---

## 15. Master Function Dispatch Table — THE ROSETTA STONE (Session 6)

**Last Updated:** 2026-02-26 21:40 JST
**Dump:** Gameplay dump, ASLR base `0x7FF628D70000`

### Discovery

A 10,953-entry function pointer dispatch table was found in the FFVII data section. Each entry is 16 bytes:

```text
[8 bytes: function pointer (2026 address)] [8 bytes: dispatch key (ORIGINAL FF7 address)]
```

**The dispatch keys ARE the original 32-bit FF7.exe addresses.** This means every FFNx hook address can be directly looked up to find the corresponding 2026 function.

### Table Location

| Property | Value |
|----------|-------|
| Table start (gameplay dump) | `0x7FF62A443E38` |
| Table start (disk RVA) | `0x16D3E38` |
| Total entries | 10,953 |
| Unique functions | 10,500 |
| Entry size | 16 bytes (QWORD func_ptr + QWORD dispatch_key) |
| Key range | `0x0` — `0x7B5640` |
| Stub function (RVA `0x56040`) | 158 entries (no-op/VM-advance for unneeded functions) |

### Exported CSV Files

| File | Contents |
|------|----------|
| `analysis/ff7_2026_dispatch_table_full.csv` | All 10,953 entries (index, func_ptr, func_rva, dispatch_key, key_hex) |
| `analysis/ff7_2026_dispatch_table_annotated.csv` | Same + `ffnx_hook_name` column for 13 confirmed hooks |

### Confirmed FFNx Hook Mappings

| Original FF7 Address | FFNx Hook Name | 2026 RVA | 2026 Runtime (this dump) |
|----------------------|----------------|----------|--------------------------|
| `0x6CC9D3` | `menu_draw_everything` | `0x1070D60` | `0x7FF629DE0D60` |
| `0x6CEE84` | `battle_draw_menu_everything` | `0x107E9A0` | `0x7FF629DEE9A0` |
| `0x6E706D` | `field_submit_draw_text_640x480` | `0x10FB970` | `0x7FF629E6B970` |
| `0x6F564E` | `common_submit_draw_char_from_buffer` | `0x115AF00` | `0x7FF629ECAF00` |
| `0x435D81` | `battle_loop` | `0x19BAC0` | `0x7FF628F0BAC0` |
| `0x429D8A` | battle_state_machine | `0x160DE0` | `0x7FF628ED0DE0` |
| `0x42A06A` | battle_entry2 | `0x161CE0` | `0x7FF628ED1CE0` |
| `0x6CBD65` | script_vm_entry1 | `0x106DD40` | `0x7FF629DDDD40` |
| `0x714598` | field_text_opcode | `0x11F7DC0` | `0x7FF629F67DC0` |
| `0x77DAED` | script_vm_entry3 | `0x1456E60` | `0x7FF62A1C6E60` |
| `0x77F0E2` | script_vm_entry4 | `0x145B7D0` | `0x7FF62A1CB7D0` |
| `0x620BDD` | candidate_state_accessor (553KB) | `0xBF46A0` | `0x7FF6299646A0` |
| `0x408074` | worldmap_loop (→ STUB) | `0x56040` | `0x7FF628DC6040` |

### How to Look Up ANY FFNx Hook

```python
# Given an original FF7 address from FFNx source code:
original_addr = 0x6CC9D3  # e.g., menu_draw_everything

# Search the dispatch table:
for i in range(10953):
    entry_addr = table_start + i * 16
    func = read_qword(entry_addr)
    key = read_qword(entry_addr + 8)
    if key == original_addr:
        # func is the 2026 function address
        rva = func - image_base
        print(f"Found: RVA {hex(rva)}")
```

### Stub Function (RVA 0x56040)

158 original FF7 functions map to a single VM-advance stub:
```asm
sub rsp, 28h
call sub_XXXXX      ; advance VM state
add [counter], 4    ; increment dispatch counter
add rsp, 28h
ret
```
Functions mapped to this stub are handled by the engine framework and don't need separate implementations. This includes `worldmap_enter`, `battle_enter`, `swirl_enter`, `credits_enter`, and others.

### Key Statistics

- Keys 0x40xxxx–0x43xxxx (832 entries): Original FF7 .text section functions
- Keys > 0x440000 (10,120 entries): Original FF7 data/BSS section addresses (game state accessors)
- Most reused function: stub at RVA 0x56040 (158 entries)
- Second most reused: RVA 0x4B570 (30 entries)

### Page Table Status (Gameplay Dump)

| Property | Value |
|----------|-------|
| Populated pages | 20,368 |
| First page index | `0x170` (handle `0x170000`) |
| Last page index | `0x7EFDD` (handle `0x7EFDE000`) |
| Page data location | Heap at `0x21300xxxxxxx` |
| Heap segment | `debug102` (0x2130000B000 — 0x2130500C000, ~80MB) |

### VEH JMP Patch Confirmation

JMP patches (`0xE9`) found in .text section with `0xB0PP_OOOO` metadata:

| Patch Address | Target (lower32) | Page | Offset |
|---------------|------------------|------|--------|
| `0x7FF628DA9795` | `0xB0E51F9C` | `0xE5` | `0x1F9C` |
| `0x7FF628DFD44C` | `0xB0ED5C70` | `0xED` | `0x5C70` |
| `0x7FF628E098EF` | `0xB0E292F0` | `0xE2` | `0x92F0` |
| `0x7FF628E4AC11` | `0xB0CCAE0B` | `0xCC` | `0xAE0B` |

---

## Next Steps (Updated — Session 6)

1. ~~**[IMMEDIATE]** Use IDA to scan the 203-entry shim table~~ ✅ DONE
2. ~~**[HIGH]** Decompile key non-gfx shim functions~~ ✅ DONE
3. ~~**[HIGH]** Understand dispatch mechanism~~ ✅ DONE — VEH exception-based dispatch
4. ~~**[HIGH]** Find the dispatch CALLER~~ ✅ RESOLVED — it's a VEH handler
5. ~~**[CRITICAL]** Take new memory dump DURING GAMEPLAY~~ ✅ DONE — page table populated, 20,368 pages
6. ~~**[HIGH]** Find game logic functions~~ ✅ DONE — 10,953-entry dispatch table found
7. ~~**[HIGH]** Complete .pdata bulk function creation~~ ✅ DONE (99.96%)
8. ~~**[HIGH]** Export full dispatch table as CSV for FFNx team cross-reference~~ ✅ DONE — `analysis/ff7_2026_dispatch_table_annotated.csv`
9. **[HIGH]** Find exception handler function — REQUIRES DEBUGGER (see Section 16)
10. **[MEDIUM]** Build pattern signatures for key game functions (using disk RVAs)
11. **[LOW]** Build the SDL2.dll proxy POC

---

## 16. Exception Handler Investigation (Session 7) — UNRESOLVED

**Last Updated:** 2026-02-26 22:40 JST

### Problem

JMP E9 patches redirect to unmapped addresses (0x7FF5B0xxxxxx), causing ACCESS_VIOLATION. Something catches these exceptions and dispatches to the correct function. The handler has NOT been found via static analysis.

### What Was Searched (ALL negative)

| Search | Result |
|--------|--------|
| `AddVectoredExceptionHandler` in FFVII imports | NOT imported |
| `AddVectoredExceptionHandler` in SDL2 imports | NOT imported |
| `RtlAddVectoredExceptionHandler` pointer in FFVII data | NOT found |
| `SetUnhandledExceptionFilter` calls | 2 calls, both pass NULL (disabling) |
| `0xC0000005` constant in ALL FFVII sections | NOT found |
| `cmp byte, 0xB0` in first 2MB of .text | NOT found |
| CONTEXT::Rip writes `mov [reg+0xF8], reg` | 14 found, ALL are C++ member inits (not exception handling) |
| CONTEXT::Rip reads `mov reg, [reg+0xF8]` | 4 found, ALL are C++ constructors/destructors |
| `"AddVectored"` string in FFVII + SDL2 | NOT found |
| ntdll VEH handler list pointers to FFVII | NOT found |
| Dispatch table base (RVA 0x16D3E38) LEA references | NOT found |

### What Was Found

- 789 functions have .pdata exception handlers
- Only 4 unique handler functions (all MSVC CRT: `__C_specific_handler`, `__GSHandlerCheck_SEH`, etc.)
- Function containing JMP patch (RVA 0x396F0) has NO exception handler in .pdata
- JMP targets confirmed unmapped (getseg returns NULL)

### Theories

1. **Dynamically resolved via GetProcAddress** — Handler registered at runtime with address obtained through GetProcAddress("kernel32.dll", "AddVectoredExceptionHandler"). String might be obfuscated or built at runtime.
2. **Registered from embedded DLL** — FFVII might unpack/load a DLL at runtime that registers the handler. Not visible in the dump as a named module.
3. **ntdll VEH list on heap** — Handler entry allocated on heap, pointer in ntdll's internal list. Need to walk LdrpVectorHandlerList at runtime.
4. **XTEA-encrypted init code** — Handler registration may be in the encrypted .text section (known to be XTEA-encrypted). The decrypted code isn't visible in a post-init dump if re-encrypted.

### Recommended Next Approach: USE A DEBUGGER

Static analysis has exhausted all viable paths. The next session should:

1. **Attach x64dbg or WinDbg to FFVII.exe during gameplay**
2. **Set hardware breakpoint on one of the JMP patch addresses** (e.g., RVA 0x39795)
3. **Execute the game until the breakpoint hits** — the JMP will execute
4. **Single-step through the exception dispatch** — will land in the handler
5. **Record the handler's address and behavior**

Alternative: Use `!exchain` command in WinDbg to dump the vectored exception handler list, or scan `ntdll!LdrpVectorHandlerList` directly.

---

## 8. FMV/Movie Hooks — MAPPED via Shim Table ✅

| Shim Function | Runtime Address | Params | Enabled | FFNx Equivalent |
|--------------|----------------|--------|---------|-----------------|
| `fw_movie_prepare` | `0x7FF6C9682A00` | 4 | ✅ | `ff7_externals.movie_object.prepare` |
| `fw_movie_release` | `0x7FF6C9682E40` | 0 | ❌ | `ff7_externals.movie_object.release` |
| `fw_movie_start` | `0x7FF6C9682EC0` | 0 | ✅ | `ff7_externals.movie_object.start` |
| `fw_movie_stop` | `0x7FF6C9682EF0` | 0 | ❌ | `ff7_externals.movie_object.stop` |
| `fw_movie_update` | `0x7FF6C9682F30` | 1 | ✅ | `ff7_externals.movie_object.update` |
| `fw_movie_get_frame` | `0x7FF6C96829F0` | 0 | ✅ | `ff7_externals.movie_object.get_frame` |

**FFNx strategy:** Hook `fw_movie_prepare` to intercept movie file paths and redirect to HD FMV files. Hook `fw_movie_update` for frame presentation. These functions are DotEmu's VideoManager wrappers that handle WebM/VP9 playback in the 2026 build (original used AVI).

---

## 9. Win32 API Shims — Complete Table

These are DotEmu's fake_win shims that emulate Win32 APIs for the recompiled game code.

### Memory Management
| Shim | Address | Params | Enabled | Notes |
|------|---------|--------|---------|-------|
| `HeapCreate` | `0x7FF6C96848B0` | 3 | ✅ | |
| `HeapAlloc` | `0x7FF6C9684670` | 3 | ✅ | Game's main allocator |
| `HeapFree` | `0x7FF6C9684990` | 3 | ✅ | |
| `VirtualAlloc` | `0x7FF6C9685580` | 4 | ✅ | |
| `VirtualFree` | `0x7FF6C8137F20` | 3 | ✅ | Returns 1 (success stub) |

### Threading
| Shim | Address | Params | Enabled | Notes |
|------|---------|--------|---------|-------|
| `CreateThread` | `0x7FF6C9684230` | 6 | ✅ | Real thread creation |
| `ResumeThread` | `0x7FF6C96852D0` | 1 | ✅ | |
| `GetCurrentThreadId` | `0x7FF6C9684420` | 0 | ✅ | |
| `TlsAlloc` | `0x7FF6C96854B0` | 0 | ✅ | Thread-local storage |
| `TlsSetValue` | `0x7FF6C9685530` | 2 | ✅ | |
| `TlsGetValue` | `0x7FF6C9685510` | 1 | ✅ | |
| `InitializeCriticalSection` | `0x7FF6C9684B00` | 1 | ❌ | |
| `EnterCriticalSection` | `0x7FF6C9684340` | 1 | ❌ | |
| `LeaveCriticalSection` | `0x7FF6C9684B40` | 1 | ❌ | |

### Window Management
| Shim | Address | Params | Enabled | Notes |
|------|---------|--------|---------|-------|
| `CreateWindowExA` | `0x7FF6C96842D0` | 12 | ✅ | Window creation |
| `RegisterClassA` | `0x7FF6C9685290` | 1 | ✅ | |
| `ShowCursor` | `0x7FF6C9685470` | 1 | ✅ | |
| `PeekMessageA` | `0x7FF6C9684BD0` | 5 | ✅ | Message loop |
| `TranslateMessage` | `0x7FF6C9685560` | 1 | ✅ | |
| `DispatchMessageA` | `0x7FF6C9684300` | 1 | ✅ | |
| `SwapBuffers` | `0x7FF6C9685490` | 1 | ✅ | Frame present |

### Registry (DotEmu Custom)
| Shim | Address | Params | Enabled | Notes |
|------|---------|--------|---------|-------|
| `RegOpenKeyExA` | `0x7FF6C9684D50` | 5 | ✅ | dotemuRegOpenKeyExA |
| `RegQueryValueExA` | `0x7FF6C9684DA0` | 6 | ✅ | dotemuRegQueryValueExA |
| `RegSetValueExA` | `0x7FF6C9685190` | 6 | ✅ | dotemuRegSetValueExA |
| `RegCloseKey` | `0x7FF6C8133B40` | 1 | ✅ | Return-arg stub |

### Character Encoding
| Shim | Address | Params | Enabled | Notes |
|------|---------|--------|---------|-------|
| `MultiByteToWideChar` | `0x7FF6C9684B60` | 6 | ✅ | Critical for Japanese |
| `WideCharToMultiByte` | `0x7FF6C9685610` | 8 | ✅ | Critical for Japanese |
| `GetACP` | `0x7FF6C9684370` | 0 | ✅ | Active code page |
| `GetCPInfo` | `0x7FF6C9684390` | 2 | ✅ | Code page info |
| `GetStringTypeW` | `0x7FF6C9684510` | 4 | ✅ | |
| `LCMapStringW` | `0x7FF6C8137F20` | 6 | ✅ | Returns 1 stub |

---

## 10. Stub Function Cross-Reference

Three stub functions are reused across many shim entries:

| Stub | Address | Behavior | Used By |
|------|---------|----------|---------|
| **No-op (retn 0)** | `0x7FF6C8131230` | Returns 0, does nothing | Sleep, ExitProcess, DeleteCriticalSection, SetLastError, PostQuitMessage, ExitThread, GetSystemTime, CoUninitialize, gfx_drv_textured3D_dispatch, fw_midi_set_tempo |
| **Return-arg** | `0x7FF6C8133B40` | Returns first argument | joyGetPosEx, timeBeginPeriod, timeEndPeriod, GetModuleHandleA, GetTimeZoneInformation, InterlockedExchange/Inc/Dec, SetUnhandledExceptionFilter, RegCloseKey, GetStdHandle, IDirectInput stubs, many more |
| **Return 1** | `0x7FF6C8137F20` | Always returns 1 | VirtualFree, LCMapStringW, FreeEnvironmentStringsW, SetEnvironmentVariableA, AdjustWindowRect, ShowWindow, UpdateWindow, DestroyWindow, DefWindowProcA, CoInitialize, SystemParametersInfoA, EndPaint, SetPixelFormat, MessageBoxA |

---

## Reference: FFNx Source File → Hook Purpose

| FFNx Source File | Hooks | 2026 Relevance |
|-----------------|-------|----------------|
| `ff7_opengl.cpp` | gfx_drv replacements, field/battle drawing, texture loading | HIGH — gfx hooks mapped |
| `common.cpp` | Main init, version detect, core hooks | HIGH — entry point for all hooks |
| `patch.cpp` / `patch.h` | Inline patching infrastructure | HIGH — need 64-bit equivalent |
| `movies.cpp` | FMV playback replacement | HIGH — fw_movie in shim table |
| `music.cpp` | MIDI/music replacement | HIGH — MusicManager in 2026 |
| `sfx.cpp` | Sound effects | MEDIUM |
| `voice.cpp` | Voice acting mod | MEDIUM |
| `field.cpp` | Field module hooks | HIGH |
| `ff7/widescreen.cpp` | Widescreen patches | MEDIUM — 2026 may have native widescreen |
| `ff7/battle/*.cpp` | Battle module hooks | HIGH |
| `ff7/field/field.cpp` | Field-specific hooks | HIGH |
| `ff7/world/world.cpp` | World map hooks | MEDIUM |
| `ff7/time.cpp` | Frame timing | LOW — 2026 has own timing |
| `saveload.cpp` | Save/load hooks | HIGH |
| `game_cfg.cpp` | Config menu | LOW — 2026 has PCSettings |

# FFVII 2026 — Complete gfx_drv_* Decompilation Results

**Created:** 2026-02-26 15:30 JST (Thursday)
**Session-ID:** ad020c43-3ebe-4197-9ab9-4bbeff56a441
**Status:** All 32 gfx_drv + 4 shared functions decompiled. Pipeline fully mapped.
**ASLR Delta (this dump):** `0x7FF588110000`
**FFVII Runtime Base:** `0x7FF6C8110000`

---

## Key Global Structures

| Symbol | Runtime Address | Role |
|--------|----------------|------|
| `qword_7FF6CA149CD8` | `0x7FF6CA149CD8` | Main game/graphics state struct (set by `gfx_drv_new_dll`) |
| `off_7FF6CA149BB0` | `0x7FF6CA149BB0` | D3D11 device context pointer (vtable calls) |
| `off_7FF6CA149BB8` | `0x7FF6CA149BB8` | Texture manager interface |
| `global_state_accessor` | `0x7FF6C814F0A0` | **PAGE TABLE OBJECT RESOLVER** — takes 32-bit handle, upper 20 bits = page index into `qword_7FF6C9849010[]`, lower 12 bits = offset within page. Returns pointer to game object. THIS IS THE FF7 HANDLE SYSTEM. ✅ Decompiled. |
| `core_draw_dispatcher` | `0x7FF6C9675CE0` | **Full D3D11 draw pipeline** — sets viewport, render states, shader constants, vertex/index buffers, issues draw call. Has DotEmu watermark/trophy detection (hardcoded UV checks). ✅ Decompiled. |
| `resource_allocator` | `0x7FF6C815AB00` | **Variadic command dispatcher** — takes (command_id, arg_count, ...). Forwards to `unk_7FF6C815AF70`. Tracks allocation in `dword_7FF6CA1495C8`. ✅ Decompiled. |
| `draw_submission` | `0x7FF6C9676880` | **Draw command builder** — extracts vertex/index/normal data from draw command struct via `global_state_accessor`, calls `core_draw_dispatcher(primitive=cmd[2], mode=2, ...)`. ✅ Decompiled. |
| `sub_7FF6C9669AB0` | `0x7FF6C9669AB0` | Render state application — applies D3D state flags from state object. Successfully decompiled. |
| `unk_7FF6C9675C20` | `0x7FF6C9675C20` | Texture bind function (called via palette_changed, sub_7FF6C9669AB0) |
| `unk_7FF6C9676E60` | `0x7FF6C9676E60` | Unknown — called from sub_7FF6C9669AB0 render state apply |
| `unk_7FF6C96750F0` | `0x7FF6C96750F0` | Unknown — called from sub_7FF6C9669AB0 |
| `dword_7FF6CA149CD4` | `0x7FF6CA149CD4` | Scene state stack depth counter (max 8) |
| `dword_7FF6CA149C00` | `0x7FF6CA149C00` | Screen width (used in viewport calculations, divided by 0x280 = 640) |
| `dword_7FF6CA149C04` | `0x7FF6CA149C04` | Screen height (used in viewport calculations, divided by 0x1E0 = 480) |
| `dword_7FF6CA19F544` | `0x7FF6CA19F544` | Rendering mode flag (value 3 = special mode, affects viewport and state) |
| `byte_7FF6C980EE6C` | `0x7FF6C980EE6C` | Unknown rendering flag (passed to draw dispatcher as param) |
| `byte_7FF6C980EE9C-A2` | various | Per-feature enable flags for different rendering paths |
| `dword_7FF6C980EE68` | `0x7FF6C980EE68` | Clear state tracker (values 2, 3) |
| `dword_7FF6C980EE7C` | `0x7FF6C980EE7C` | Secondary depth clear flag |

---

## Complete Function Decompilation Summary

### 1. gfx_drv_new_dll — Driver Initialization
- **Address:** `0x7FF6C9670A30` (disk: `0x141560A30`)
- **Size:** 0x55 bytes
- **Purpose:** Stores main game state pointer to `qword_7FF6CA149CD8`
- **Pseudocode:**
```c
__int64 __fastcall gfx_drv_new_dll(__int64 a1) {
    qword_7FF6CA149CD8 = a1;  // Store main game state
    return 1;
}
```

### 2. gfx_drv_cleanup_init — Graphics Subsystem Init
- **Address:** `0x7FF6C96703C0` (disk: `0x1415603C0`)
- **Size:** 0xD5 bytes
- **Purpose:** Creates initial render target, sets up RGBA color format (R=0xFF0000, G=0xFF00, B=0xFF, A=0xFF000000)
- **Key details:**
  - Checks `qword_7FF6CA149CD8 + 2684` for existing init
  - Calls `unk_7FF6C9669440` with params {1, 1, value_from_state+2404}
  - Uses `unk_7FF6C815AB00` for pixel format setup (32-bit, RGBA masks)
  - Sets `dword_7FF6CA149DD8` and `dword_7FF6CA149CD0`

### 3. gfx_drv_lock_unlock — No-op
- **Address:** `0x7FF6C8137F20` (disk: `0x140027F20`)
- **Size:** 0x6 bytes
- **Purpose:** Always returns 1. Lock/unlock is unnecessary in D3D11 (was needed for DirectDraw surface locking).

### 4. gfx_drv_begin_scene — Frame Setup
- **Address:** `0x7FF6C966DD30` (disk: `0x14155DD30`)
- **Size:** 0x288 bytes
- **Purpose:** Push render state onto 8-entry stack (232 bytes per entry). Sets viewport, render target, matrices.
- **Key details:**
  - Stack depth tracked by `dword_7FF6CA149CD4`
  - Two modes: a1=0 vs a1=1 (different parameter sets)
  - D3D11 vtable[47] call for setup

### 5. gfx_drv_end_scene — Frame Teardown
- **Address:** `0x7FF6C966EBF0` (disk: `0x14155EBF0`)
- **Size:** 0x374 bytes
- **Purpose:** Pop render state from stack. Restores culling, z-buffer.
- **Key details:**
  - Passes `"gfx_drv_end_scene"` string to D3D11 debug marker (vtable[54])
  - Manages state restoration from the 232-byte stack entries

### 6. gfx_drv_flip — Frame Present
- **Address:** `0x7FF6C966FE30` (disk: `0x14155FE30`)
- **Size:** 0x587 bytes
- **Purpose:** Swap buffers / present frame to screen
- **Key details:**
  - Frame timing: `1/60.5` seconds (~60fps) or `1/30.5` (~30fps)
  - References `"SwapBuffers"` error string + `OutputDebugStringA`
  - References `W:\proj\ff7\kitamura\Material\BaseEngine\InputManager.h` in assert
  - Calls into D3D11 present chain

### 7. gfx_drv_clear — Conditional Clear
- **Address:** `0x7FF6C966E020` (disk: `0x14155E020`)
- **Size:** 0x167 bytes
- **Purpose:** Clear render target and/or depth buffer based on parameters
- **Key details:**
  - a1 controls depth clear, a2 controls color clear
  - Tracks clear state in `dword_7FF6C980EE68` (values 2→3 transition)
  - Uses `off_7FF6CA149BB0` (D3D11 context) for clear operations
  - Calls through `unk_7FF6C970C160`, `unk_7FF6C970C400`, `unk_7FF6C970C1E0`, `unk_7FF6C970C170`, `unk_7FF6C970C190`
  - Background color from `dword_7FF6CA18ACA8/ACAC/ACB0`

### 8. gfx_drv_clear_all — Full Clear
- **Address:** `0x7FF6C966E190` (disk: `0x14155E190`)
- **Size:** 0x13D bytes
- **Purpose:** Clear render target with background color via D3D11. Sets render state to mode 3.

### 9. gfx_drv_setbg — Set Background Color
- **Address:** `0x7FF6C9670B40` (disk: `0x141560B40`)
- **Size:** 0x56 bytes
- **Purpose:** Sets background color for clear operations
- **Key details:**
  - Resolves object via `unk_7FF6C814F0A0(a1)` to get color data
  - Copies 16 bytes (OWORD = 4 floats RGBA) to state at offset+8

### 10. gfx_drv_setviewport — Viewport Configuration
- **Address:** `0x7FF6C9670F80` (disk: `0x141560F80`)
- **Size:** 0x219 bytes
- **Purpose:** Set rendering viewport with coordinate transformation
- **Key details:**
  - **Original resolution reference**: divides by `0x280` (640) and `0x1E0` (480) — the original FF7 internal resolution
  - Screen dimensions from `dword_7FF6CA149C00` (width) and `dword_7FF6CA149C04` (height)
  - Calculates normalized viewport coordinates: `(a3*0.5 + a1 - width*0.5) / (width*0.5)` for X
  - Stores viewport rect in `dword_7FF6CA149D00-D0C` (x, y, w, h)
  - Writes viewport transform to `dword_7FF6CA149DC8/DCC`
  - Special handling when `dword_7FF6CA19F544 == 3` (sets Y scale to 1.0 instead of calculated)
  - State+2388 and state+2392 hold internal resolution values

### 11. gfx_drv_setmatrix — Matrix Setting
- **Address:** `0x7FF6C9670BA0` (disk: `0x141560BA0`)
- **Size:** 0x1FB bytes
- **Purpose:** Set world(0), view(1), or projection(2) matrix
- **Key details:**
  - Copies 64 bytes (4x4 float matrix) via 4× OWORD moves
  - Matrix type in a1: 0=model/world, 1=view, 2=projection

### 12. gfx_drv_blendmode — Alpha Blend Mode
- **Address:** `0x7FF6C966DFC0` (disk: `0x14155DFC0`)
- **Size:** 0x5B bytes
- **Purpose:** Set alpha blend value
- **Key details:**
  - mode 0 → alpha = 128 (50% blend)
  - mode 3 → alpha = 64 (25% blend)
  - other → alpha = 255 (opaque)

### 13. gfx_drv_setrenderstate — Apply Render State
- **Address:** `0x7FF6C9670DA0` (disk: `0x141560DA0`)
- **Size:** 0x34 bytes
- **Purpose:** Delegates to `sub_7FF6C9669AB0(a1, qword_7FF6CA149CD8)` — the render state application function

### 14. gfx_drv_setrenderstate_2D — 2D Render State
- **Address:** `0x7FF6C9670DE0` (disk: `0x141560DE0`)
- **Size:** 0x4C bytes
- **Purpose:** Apply 2D-specific render state. Checks flag at offset+44 before applying.

### 15. gfx_drv_setrenderstate_3D — 3D Render State
- **Address:** `0x7FF6C9670E30` (disk: `0x141560E30`)
- **Size:** 0xF9 bytes
- **Purpose:** Apply 3D render state with 4x4 matrix loading (xmmword operations for transforms)

### 16. gfx_drv_setrenderstate_lines — Line Render State
- **Address:** `0x7FF6C9670F30` (disk: `0x141560F30`)
- **Size:** 0x44 bytes
- **Purpose:** Apply line-specific render state
- **Key details:**
  - Checks offset+44 flag, then offset+52 for state object
  - Delegates to `sub_7FF6C9669AB0`

### 17. gfx_drv_load_texture — Texture Loading
- **Address:** `0x7FF6C96704E0` (disk: `0x1415604E0`)
- **Size:** 0x54E bytes
- **Purpose:** Full texture loading pipeline
- **Key details:**
  - Multi-page texture support
  - References `"glTexImage2D"` string (legacy OpenGL naming in D3D11 wrapper)
  - 16-bit 5551 RGBA format conversion
  - Creates D3D11 textures via `off_7FF6CA149BB8` (texture manager)
  - Palette handling for paletted textures

### 18. gfx_drv_unload_texture — Texture Cleanup
- **Address:** `0x7FF6C96711A0` (disk: `0x1415611A0`)
- **Size:** 0x108 bytes
- **Purpose:** Release texture GPU resources
- **Key details:**
  - Iterates texture pages
  - Deletes GPU resources via `off_7FF6CA149BB8`

### 19. gfx_drv_palette_changed — Palette Update Notification
- **Address:** `0x7FF6C9670A90` (disk: `0x141560A90`)
- **Size:** 0xA6 bytes
- **Purpose:** Reload texture when palette changes
- **Key details:**
  - Resolves texture via `unk_7FF6C814F0A0(a5)` to get dimensions (offsets 128, 132)
  - Calls `gfx_drv_load_texture` to re-upload texture with new palette
  - Resolves new palette data through nested pointer chain
  - Calls `unk_7FF6C9675C20` (texture bind) with palette-derived value

### 20. gfx_drv_write_palette — Write Palette Data
- **Address:** `0x7FF6C96712B0` (disk: `0x1415612B0`)
- **Size:** 0x147 bytes
- **Purpose:** Write palette color data and invalidate cached textures
- **Key details:**
  - Validates palette format compatibility (checks page count match)
  - Calculates page row/column from palette index: `row = a4/pages, col = a4%pages`
  - Compares palette data via `unk_7FF6C97346BC` (memcmp-like)
  - If changed, copies via `unk_7FF6C9734680` (memcpy-like) and invalidates cached texture
  - Calls `gfx_drv_textured3D_dispatch` + texture release via `off_7FF6CA149BB8` when invalidating

### 21. gfx_drv_draw_flat_smooth_2D — 2D Flat/Smooth Polygons
- **Address:** `0x7FF6C966E410` (disk: `0x14155E410`)
- **Size:** 0x209 bytes
- **Purpose:** Draw 2D flat or smooth-shaded polygons
- **Key details:**
  - Calls core dispatcher `unk_7FF6C9675CE0(4, 3, vertices, count, ...)`
  - Checks `byte_7FF6C980EEA2` enable flag

### 22. gfx_drv_draw_textured2D — 2D Textured Polygons
- **Address:** `0x7FF6C966EB00` (disk: `0x14155EB00`)
- **Size:** 0xEF bytes
- **Purpose:** Draw 2D textured polygons
- **Key details:**
  - Similar dispatch pattern to flat but with texture coords
  - Calls `unk_7FF6C9675CE0` with textured flag

### 23. gfx_drv_draw_paletted2D — 2D Paletted Polygons
- **Address:** `0x7FF6C966E800` (disk: `0x14155E800`)
- **Size:** 0x2F1 bytes
- **Purpose:** Draw 2D paletted (indexed color) polygons
- **Key details:**
  - Complex palette batching with run-length grouping by palette index
  - Iterates vertices, calls `gfx_drv_load_texture` for each unique palette index
  - Batches primitives sharing same palette for efficient rendering

### 24. gfx_drv_draw_flat_smooth_3D — 3D Flat/Smooth Polygons
- **Address:** `0x7FF6C966E620` (disk: `0x14155E620`)
- **Size:** 0xE3 bytes
- **Purpose:** Draw 3D flat or smooth-shaded polygons
- **Key details:**
  - Calls `unk_7FF6C9675CE0(4, 2, ...)` — note mode=2 for 3D vs mode=3 for 2D

### 25. gfx_drv_draw_lines — Line Drawing
- **Address:** `0x7FF6C966E710` (disk: `0x14155E710`)
- **Size:** 0xE3 bytes
- **Purpose:** Draw line primitives
- **Key details:**
  - Calls `unk_7FF6C9675CE0(2, 3, vertices, count, normals, normal_count, colors, use_lighting, byte_flag, 0)`
  - primitive_type=2 (lines), vertex_format=3
  - Resolves vertex data, normals, and colors from state objects

### 26. gfx_drv_draw_deferred — Deferred Rendering
- **Address:** `0x7FF6C966E2D0` (disk: `0x14155E2D0`)
- **Size:** 0x137 bytes
- **Purpose:** Execute previously queued draw commands
- **Key details:**
  - Checks `byte_7FF6C980EEA1` enable flag
  - Resolves draw command from state: object pointer → draw data → render state
  - Sets up render state via `sub_7FF6C9669AB0`
  - Loads 4×4 transform matrix (xmmword copies to `xmmword_7FF6CA149D18-D48`)
  - Can have two matrix sources (offsets 16 and 84)
  - Submits draw via `unk_7FF6C9676880(vertex_data, use_lighting, 0)`

### 27. gfx_drv_field_64 — Render State Switch (Multi-Mode)
- **Address:** `0x7FF6C966EF70` (disk: `0x14155EF70`)
- **Size:** 0x196 bytes
- **Purpose:** Complex render state switching based on mode parameter
- **Key details:**
  - Switch on `a1 - 2`: handles modes 2, 13, 14, 15, 16
  - Mode 2: Wireframe/flat toggle — sets `byte_7FF6CA149D11`
  - Mode 13: Culling control — calls `gfx_drv_textured3D_dispatch(2884)` (D3D cull mode)
  - Mode 14: Z-write control — calls `gfx_drv_textured3D_dispatch(2929)` (D3D z-write enable), sets `dword_7FF6CA18ACA8` to 3 or 7
  - Mode 15: Alpha test — `gfx_drv_textured3D_dispatch(2929)`, sets `dword_7FF6CA18ACA4`, `byte_7FF6CA149D15`
  - Mode 16: Alpha test enable with `dword_7FF6CA18ACA4`
  - **D3D state constants**: 2884 = D3DRS_CULLMODE, 2929 = D3DRS_ZENABLE, 1029 = unknown

### 28. gfx_drv_field_74 — Indexed Render State Apply
- **Address:** `0x7FF6C966F110` (disk: `0x14155F110`)
- **Size:** 0x53 bytes
- **Purpose:** Apply render state from indexed table (up to 5 entries)
- **Key details:**
  - Index `a1` must be ≤ 4
  - Looks up state at `(a2_object + 4*a1 + 2080)`
  - Delegates to `sub_7FF6C9669AB0`

### 29. gfx_drv_field_78 — Core 3D Polygon Rendering (LARGEST FUNCTION)
- **Address:** `0x7FF6C966F170` (disk: `0x14155F170`)
- **Size:** 0xBA8 bytes (2984 bytes — the largest gfx_drv function)
- **Purpose:** THE main 3D polygon/mesh rendering function
- **Key details:**
  - Takes a1=mesh_id, a2=context_id
  - Iterates over mesh sub-objects (vertex groups)
  - For each sub-object:
    - Resolves texture (palette support), vertices, normals
    - Handles 3 vertex modes via `v9`: mode 0 (inline), mode 1 (pointer to external buffer), mode 2 (transformed via `unk_7FF6C9677980`)
    - Sets up 4×4 transform matrices (`xmmword_7FF6CA149D18-D48`)
    - Handles deferred rendering path (`v76` flag) — queues draw for later via `unk_7FF6C815AB00(6957157, 1, ...)`
    - Three rendering paths based on `v67` (joint/bone type):
      - v67=0: Direct draw with optional lighting
      - v67=1: Skinned/weighted draw
      - v67=2: Pre-transformed vertices
    - Texture animation support (per-sub-object texture switching)
    - Normal mapping support (separate normal buffer)
    - Color buffer support
  - Calls the core draw dispatcher `unk_7FF6C9675CE0` for actual rendering
  - Calls `unk_7FF6C9676880` for alternative rendering path
  - References `byte_7FF6C980EE9D-A0` for various feature flags
  - Allocates temporary buffers via `unk_7FF6C815AB00(6684065, 3, 64, 0, 95)`
  - Frees with `unk_7FF6C815AB00(6683456, 3, ...)`

### 30. gfx_drv_field_80 — Indirect Mesh Render
- **Address:** `0x7FF6C966FD20` (disk: `0x14155FD20`)
- **Size:** 0x20 bytes
- **Purpose:** Thin wrapper — resolves mesh pointer and calls `gfx_drv_field_78`
- **Key details:**
  - `unk_7FF6C814F0A0()` to get object, reads DWORD at offset+20
  - Passes that + a2 to `gfx_drv_field_78`

### 31. gfx_drv_field_84 — Dual-Buffer Mesh Render
- **Address:** `0x7FF6C966FD40` (disk: `0x14155FD40`)
- **Size:** 0xE1 bytes
- **Purpose:** Double-buffered mesh rendering (two buffer slots at state+748 and state+752)
- **Key details:**
  - Writes to `qword_7FF6CA149CD8 + 2344` (render mode)
  - a1=0: enables buffer 748, disables 752, renders 748
  - a1=1: disables buffer 748, enables 752, renders 752
  - Enable/disable by writing 0/1 to resolved buffer objects
  - Calls `gfx_drv_field_78` with the selected buffer

### 32. gfx_drv_textured3D_dispatch — No-op Stub
- **Address:** `0x7FF6C8131230` (disk: `0x140021230`)
- **Size:** 0x3 bytes
- **Purpose:** `retn 0` — no-op stub
- **Key details:**
  - In original FF7, dispatched D3D render state changes through the graphics driver
  - Called with D3D state constants (2884=cullmode, 2929=zenable, 1029=unknown)
  - In DotEmu build, these are handled directly — stub is dead code
  - Still called by `gfx_drv_field_64` and `sub_7FF6C9669AB0` but does nothing

---

## Shared Helper: sub_7FF6C9669AB0 — Render State Application

- **Address:** `0x7FF6C9669AB0`
- **Purpose:** Central render state application function
- **Called by:** gfx_drv_setrenderstate, setrenderstate_2D, setrenderstate_3D, setrenderstate_lines, field_74, field_78, draw_deferred
- **Parameters:** (state_object, game_state)
- **Key details:**
  - Reads flag bitmask from `state_object + 12`
  - Bit 1 (0x2): Texture binding — resolves texture via palette chain, calls `unk_7FF6C9675C20`
  - Bit 2 (0x4): Wireframe toggle — checks `dword_7FF6CA19F544` for mode 3/4
  - Bit 14 (0x4000): Culling mode — calls `gfx_drv_textured3D_dispatch`, sets `qword_7FF6CA18ACC4`
  - Bit 13 (0x2000): Z-write mode
  - Bit 15 (0x8000): Z-test mode — `dword_7FF6CA18ACA8 = 3 or 7`, `byte_7FF6CA149D14`
  - Bit 16 (0x10000): Alpha test — `dword_7FF6CA18ACA4`
  - Bit 10 (0x400): Fog/environment — calls `unk_7FF6C9676E60`, sets `dword_7FF6CA149DDC`, `dword_7FF6CA149CFC = 4`
  - Bit 17 (0x20000): Backface mode — `byte_7FF6CA149D16`

---

## Rendering Pipeline Architecture

```text
Application Layer (Game Logic)
    ↓
gfx_drv_new_dll(state)          ← Init: store game state pointer
gfx_drv_cleanup_init()          ← Init: create render target
    ↓
Per-Frame:
  gfx_drv_begin_scene(mode)     ← Push state stack (8 deep, 232 bytes each)
  gfx_drv_setviewport(x,y,w,h) ← Set viewport (scales from 640×480 to actual resolution)
  gfx_drv_setmatrix(type,mtx)   ← Set world/view/projection matrix
  gfx_drv_setbg(color)          ← Set clear color
  gfx_drv_clear(depth,color)    ← Clear render target / depth buffer
  gfx_drv_blendmode(mode)       ← Set alpha blend (128/64/255)
    ↓
  Render State Setup:
    gfx_drv_setrenderstate(obj)         ← Apply full render state object
    gfx_drv_setrenderstate_2D(obj)      ← 2D-specific state
    gfx_drv_setrenderstate_3D(obj)      ← 3D state with transform matrix
    gfx_drv_setrenderstate_lines(obj)   ← Line-specific state
    gfx_drv_field_64(mode, val, ctx)    ← Mode switch (cull, z-write, alpha, wireframe)
    gfx_drv_field_74(idx, ctx)          ← Apply indexed state (0-4)
    ↓
  Draw Calls:
    2D Drawing:
      gfx_drv_draw_flat_smooth_2D()     → unk_7FF6C9675CE0(4, 3, ...)  [quads, mode 3]
      gfx_drv_draw_textured2D()         → unk_7FF6C9675CE0(4, 3, ...)  [+ texture]
      gfx_drv_draw_paletted2D()         → batched gfx_drv_load_texture + dispatch
    3D Drawing:
      gfx_drv_draw_flat_smooth_3D()     → unk_7FF6C9675CE0(4, 2, ...)  [quads, mode 2]
      gfx_drv_draw_lines()              → unk_7FF6C9675CE0(2, 3, ...)  [lines, mode 3]
      gfx_drv_field_78(mesh, ctx)       → THE core 3D mesh renderer (2984 bytes!)
      gfx_drv_field_80(mesh, ctx)       → Indirect → field_78
      gfx_drv_field_84(buf, ctx)        → Double-buffer → field_78
    Deferred:
      gfx_drv_draw_deferred(cmd)        → Replay queued commands
    ↓
  Texture Operations:
    gfx_drv_load_texture(tex, w, h)     ← Upload texture to GPU (D3D11)
    gfx_drv_unload_texture(tex)         ← Release GPU texture
    gfx_drv_palette_changed(...)        ← Re-upload texture after palette change
    gfx_drv_write_palette(...)          ← Write palette data, invalidate cache
    ↓
  gfx_drv_end_scene()              ← Pop state stack, restore state
  gfx_drv_flip()                   ← Present frame (D3D11 SwapChain, 60/30 fps)
    ↓
gfx_drv_lock_unlock()              ← No-op (DirectDraw legacy)
```

## CRITICAL SHARED FUNCTIONS (Now Decompiled)

### global_state_accessor — FF7 Handle/Object System (PAGE TABLE)
- **Address:** `0x7FF6C814F0A0`
- **THIS IS THE KEY TO THE ENTIRE ENGINE.**
```c
void* global_state_accessor(unsigned int handle) {
    if (!handle) return NULL;
    // Upper 20 bits = page index, lower 12 bits = offset within page
    __int64 page = qword_7FF6C9849010[handle >> 12];
    if (page)
        return (void*)(page + (handle & 0xFFF));
    else
        return &unk_7FF6C9848D00;  // default/null object
}
```
- **Page table at:** `qword_7FF6C9849010` — array of page base pointers
- **Handle format:** `[20-bit page index][12-bit offset]` → each page is 4096 bytes
- **Default object at:** `unk_7FF6C9848D00` (returned for invalid pages)
- **Implication:** Every game object (textures, meshes, palettes, vertices, render states) is accessed through this page table. The 32-bit "IDs" passed everywhere are handles into this system.

### core_draw_dispatcher — Full D3D11 Draw Pipeline
- **Address:** `0x7FF6C9675CE0`
- **Size:** Large (~600+ bytes)
- **Parameters confirmed from decompilation:**
```c
void core_draw_dispatcher(
    int primitive_type,      // 2=lines, 4=quads/triangles
    unsigned int vertex_fmt, // 2=3D, 3=2D (selects shader)
    __int64 vertex_data,     // pointer to vertex buffer (32 bytes per vertex)
    unsigned int vertex_count,
    unsigned short* index_data,  // index buffer
    unsigned int index_count,
    int color_data,          // color buffer handle
    char use_lighting,       // enable lighting
    char blend_flag,         // from byte_7FF6C980EE6C
    char extra_flag          // trophy/watermark detection flag
);
```
- **Pipeline stages:**
  1. Early-out if `!blend_flag` or `!index_count` or `vertex_fmt > 3`
  2. Calls `unk_7FF6C9674A80()` — pre-draw setup
  3. If `use_lighting`: calls `gfx_drv_setviewport` with stored viewport
  4. Sets scissor rect via `unk_7FF6C970C510` (from `xmmword_7FF6CA18AD50`)
  5. Sets viewport via `unk_7FF6C970C480` (from `xmmword_7FF6CA18AD60`)
  6. Sets render state: alpha, z-test, culling, depth via `unk_7FF6C970C400/C3E0/C3F0/C3D0`
  7. **Shader selection**: vertex_fmt=3 (2D) uses `off_7FF6CA149BC8[3]`, vertex_fmt≠3 (3D) uses `off_7FF6CA149BC8[2]` — these are shader resource views
  8. For 3D: multiplies matrices via `unk_7FF6C9677980` (view×world, then result×projection)
  9. **Texture setup**: Loops over texture slots, configures sampler states via vtable calls [40] and [56] on texture objects from `off_7FF6CA149BB8`
  10. Updates constant buffer via `unk_7FF6C814F540` (80 bytes of shader constants)
  11. Binds constant buffer via `unk_7FF6C970C4C0`
  12. **Vertex submission**: 32 bytes per vertex, split into 3 streams:
      - Stream 0: position (offset 0, stride 32)
      - Stream 1: color/alpha (offset 24, stride 32)
      - Stream 2: texcoord (offset 16, stride 32)
  13. **Draw call**: `unk_7FF6C970C1A0(context, index_count, 0, start_index, topology, index_buffer)` — topology is 4 (triangles) or 2 (lines)

- **DotEmu Watermark/Trophy Detection (IMPORTANT):**
  - When `extra_flag` is set, scans vertex data for specific UV coordinates:
    - Check 1 (`byte_7FF6CA149C45`): UVs (0.0, 0.625), (0.375, 0.625), (0.0, 0.75) — counted in `dword_7FF6CA14A52C`, stops after 10 occurrences
    - Check 2 (`byte_7FF6CA149C46`): Positions (96, 16), (96, 58), (112, 16) — counted in `dword_7FF6CA14A530`, stops after 10
  - When detected, routes to alternative renderers: `unk_7FF6C96736D0` or `unk_7FF6C9672EA0` or `unk_7FF6C9672520`
  - These are likely DotEmu's achievement/trophy overlay or "Powered by DotEmu" watermark detection

- **Vertex format (32 bytes per vertex):**
```text
Offset 0:  float x, y, z, w   (16 bytes — position + homogeneous)
Offset 16: float u, v         (8 bytes — texture coordinate)
Offset 24: float r, g, b, a?  (8 bytes — color/alpha — actually 2 floats packed)
```

### resource_allocator — Variadic Command Dispatcher
- **Address:** `0x7FF6C815AB00`
```c
__int64 resource_allocator(__int64 command_id, __int64 arg_count, ...) {
    va_list args;
    va_start(args, arg_count);
    result = unk_7FF6C815AF70(command_id, arg_count, args);
    dword_7FF6CA1495C8 += 4 * arg_count;  // track allocation/usage
    return result;
}
```
- **Command IDs seen in callers:**
  - `6684065` — allocate temporary buffer (in field_78: size=64, flags=0, type=95)
  - `6683456` — free temporary buffer (in field_78: cleanup)
  - `6957157` — allocate deferred draw command
  - `6756162` — set texture state
  - `6708634` — set texture + draw params
  - `6707091` — set multi-texture params
  - `6798427` — allocate transform result
  - `6869688` — set bone/joint params
  - `7022505` — set bone + transform params
- **Tracks total allocation in `dword_7FF6CA1495C8`**

### draw_submission — Draw Command Executor
- **Address:** `0x7FF6C9676880`
```c
void draw_submission(int* cmd, char use_lighting) {
    // cmd is a struct with draw parameters
    unsigned int index_count = cmd[7];
    void* indices = global_state_accessor(cmd[6]);  // index buffer handle
    unsigned int vertex_count = cmd[5];
    void* vertices = global_state_accessor(cmd[4]); // vertex buffer handle
    int primitive = cmd[2];

    core_draw_dispatcher(primitive, 2/*3D*/, vertices, vertex_count,
                         indices, index_count, 0, use_lighting,
                         byte_7FF6C980EE6C, 0);
}
```
- Always uses vertex_format=2 (3D mode)
- Draw command struct layout: `[?, ?, primitive_type, ?, vertex_handle, vertex_count, index_handle, index_count]`

---

## D3D Render State Constants Used

| Value | D3D Equivalent | Where Used |
|-------|---------------|------------|
| 2884 | D3DRS_CULLMODE | gfx_drv_field_64 (modes 13, 14) |
| 2929 | D3DRS_ZENABLE | gfx_drv_field_64 (modes 14, 15) |
| 1029 | D3DRS_ALPHABLENDENABLE(?) | gfx_drv_field_64 (mode 14 + cull) |

---

## Viewport Coordinate System

The setviewport function reveals the coordinate mapping:
- **Internal resolution:** 640×480 (0x280 × 0x1E0) — same as original FF7
- **Scaling:** `screen_x = screen_width * internal_x / 640`
- **NDC transform:** `ndc_x = (viewport_center_x - screen_center_x) / half_screen_width`
- Special mode 3 (`dword_7FF6CA19F544 == 3`) forces Y scale to 1.0

---

## Remaining Shared Functions (P2/P3 — Lower Priority)

| Symbol | Address | Role | Priority |
|--------|---------|------|----------|
| `unk_7FF6C9675C20` | `0x7FF6C9675C20` | Texture bind/activate | P2 |
| `unk_7FF6C9676E60` | `0x7FF6C9676E60` | Fog/environment state | P2 |
| `unk_7FF6C9677980` | `0x7FF6C9677980` | 4×4 Matrix multiply (used in draw dispatcher for view×world×projection) | P2 |
| `unk_7FF6C96750F0` | `0x7FF6C96750F0` | Unknown state function | P3 |
| `unk_7FF6C9669440` | `0x7FF6C9669440` | Render target creation | P3 |
| `unk_7FF6C966A710` | `0x7FF6C966A710` | Texture slot accessor from texture manager | P3 |
| `unk_7FF6C814F540` | `0x7FF6C814F540` | Constant buffer update (80 bytes of shader constants) | P2 |
| `unk_7FF6C814F620` | `0x7FF6C814F620` | Index buffer upload | P2 |
| `unk_7FF6C814F690` | `0x7FF6C814F690` | Vertex buffer upload | P2 |
| `unk_7FF6C9674A80` | `0x7FF6C9674A80` | Pre-draw setup | P3 |
| `unk_7FF6C970C1A0` | `0x7FF6C970C1A0` | **THE ACTUAL D3D11 DRAW CALL** (DrawIndexed wrapper) | P1 |
| `unk_7FF6C970C400` | `0x7FF6C970C400` | D3D11 render state set (alpha/z/cull) | P3 |
| `unk_7FF6C970C480` | `0x7FF6C970C480` | D3D11 set viewport | P3 |
| `unk_7FF6C970C510` | `0x7FF6C970C510` | D3D11 set scissor rect | P3 |
| `unk_7FF6C970C4B0` | `0x7FF6C970C4B0` | D3D11 bind vertex/index buffer | P3 |
| `unk_7FF6C970C4C0` | `0x7FF6C970C4C0` | D3D11 bind constant buffer | P3 |
| `unk_7FF6C970C4D0` | `0x7FF6C970C4D0` | D3D11 bind shader resource | P3 |
| `unk_7FF6C970C420` | `0x7FF6C970C420` | D3D11 bind pixel shader | P3 |
| `unk_7FF6C970C470` | `0x7FF6C970C470` | D3D11 bind sampler + texture slot | P3 |
| `unk_7FF6C96736D0` | `0x7FF6C96736D0` | DotEmu overlay renderer (path 1) | P3 |
| `unk_7FF6C9672EA0` | `0x7FF6C9672EA0` | DotEmu overlay renderer (path 2) | P3 |
| `unk_7FF6C9672520` | `0x7FF6C9672520` | DotEmu overlay renderer (path 3) | P3 |

---

## D3D11 Wrapper Function Pattern

All `unk_7FF6C970Cxxx` functions are thin D3D11 wrappers in the BaseEngine RenderManager. They take `off_7FF6CA149BB0` (the D3D11 device context) as first param and call through its vtable. The naming suggests:
- `C160`: BeginScene equivalent
- `C170`: SetRenderTarget
- `C190`: ClearDepthStencilView
- `C1A0`: **DrawIndexed** (the actual draw call!)
- `C1E0`: SetRenderTarget variant
- `C3D0`: SetBlendState
- `C3E0`: SetDepthStencilState
- `C3F0`: SetRasterizerState
- `C400`: ClearRenderTargetView
- `C420`: PSSetShader
- `C470`: PSSetSamplers + PSSetShaderResources
- `C480`: RSSetViewports
- `C4B0`: IASetVertexBuffers / IASetIndexBuffer
- `C4C0`: VSSetConstantBuffers
- `C4D0`: VSSetShaderResources
- `C510`: RSSetScissorRects

---

## Shader Resource Slots

From `off_7FF6CA149BC8` (shader resource array):
- `[2]` — 3D vertex shader resource
- `[3]` — 2D vertex shader resource
- `[8]` — Pixel shader (non-textured path)
- `[9]` — Pixel shader (textured path, 3D lighting)
- `[11]` — Pixel shader (special case / same-texture check)

---

## Additional Discoveries (Session 3)

### Dispatch Table for All Shim Functions
- **Address:** `0x7FF6CA05A010`
- Stores pointers to 203-entry shim table entries
- Indexed by `page * 4096 + slot` where page/slot come from game import descriptors
- Populated by `shim_table_init_and_link` at `0x7FF6C814DDA0`
- See `FFNX_HOOK_MAPPING.md` Section 13 for full details

### .pdata Exception Table
- **Address:** `0x7FF6CA1A4000`, Size: `0x3D17C`
- Contains 20,853 function entries (12 bytes each: begin_rva, end_rva, unwind_rva)
- **20,844 of 20,853 functions created (99.96%)** ✅ COMPLETE
- Total functions in IDA: 13,009 (includes IDA auto-detected + .pdata bulk creation)
- 9 entries failed (likely overlapping or already-merged functions)

## Additional Discoveries (Session 4)

### Exception-Based Dispatch (VEH)
- The shim dispatch uses **Vectored Exception Handling** — NOT direct function calls
- `shim_inline_jmp_patcher` at `0x7FF6C9668D00` patches game `CALL` sites with `JMP 0xE9` to intentionally invalid addresses
- The JMP triggers an Access Violation caught by a VEH handler
- Handler decodes `0xB0PP_OOOO` metadata from the faulting instruction and routes to the correct shim
- See `FFNX_HOOK_MAPPING.md` Section 14 for full architecture

### Game Initialization Functions
- **Main Init:** `sub_7FF6C814ECA0` — Build date "Dec 11 2025", Steam App ID 3837340
- **Game Loader:** `sub_7FF6C814E7D0` — Reads embedded ff7_en/ff7_ja, allocates pages
- **Page Allocator:** `sub_7FF6C814EBD0` — Populates `qword_7FF6C9849010[handle >> 12]`

### ⚠️ Memory Dump State — TWO DUMPS AVAILABLE

**Dump 1 (Title Screen):** ASLR base `0x7FF6C8110000`
- Page table ALL ZEROS — game engine not initialized
- ✅ Code decompilable, static analysis works
- ❌ Runtime state empty
- Used for: all decompilation work, .pdata creation, function profiling

**Dump 2 (Gameplay — Session 6):** ASLR base `0x7FF628D70000`
- ✅ Page table POPULATED — 20,368 pages active
- ✅ JMP patches visible — VEH dispatch confirmed
- ✅ 10,953-entry master dispatch table found (original FF7 addr → 2026 func)
- ❌ Functions not defined in IDA (raw dump, needs analysis)
- Delta from Dump 1 to Dump 2: `-0x9F3A0000`

## Next Steps

1. ~~**[PRIORITY]** Map FFNx hook points~~ ✅ DONE — see FFNX_HOOK_MAPPING.md
2. ~~**Non-graphics subsystem analysis**~~ ✅ DONE — audio, video, file I/O, input all mapped
3. ~~**Dispatch mechanism**~~ ✅ DONE — VEH exception-based dispatch fully mapped
4. ~~**[CRITICAL]** Take gameplay dump~~ ✅ DONE — 10,953-entry dispatch table found
5. ~~**[HIGH]** Find game logic functions~~ ✅ DONE — dispatch table maps ALL functions
6. ~~**[HIGH]** Complete .pdata bulk function creation~~ ✅ DONE (20,844/20,853 = 99.96%)
7. ~~**[HIGH]** Export full dispatch table as CSV for FFNx cross-reference~~ ✅ DONE — `analysis/ff7_2026_dispatch_table_annotated.csv`
8. **[HIGH]** Find exception handler function — REQUIRES DEBUGGER (static analysis exhausted, see FFNX_HOOK_MAPPING.md Section 16)
9. **[MEDIUM]** Decompile P1 remaining: `unk_7FF6C970C1A0` (DrawIndexed wrapper)
10. **[LOW]** Build SDL2.dll proxy POC

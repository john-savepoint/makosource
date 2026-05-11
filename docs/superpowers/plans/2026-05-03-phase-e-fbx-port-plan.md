# Phase E — FFNx 2026 Port: File-by-File Analysis & Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port John's modified FFNx fork (39 commits, 30 files) onto current upstream FFNx master which has native FF7 2026 Steam Edition compatibility.

**Architecture:** Apply John-only files first (14 files, zero upstream presence — copy as-is), then hand-merge the 16 conflict files in order of increasing difficulty. Build after each wave to catch breakage early.

**Tech Stack:** C++ (MSVC toolchain via Visual Studio 2022), CMake, vcpkg, bgfx renderer, GLSL shaders.

**Input repos:**
- `C:\FFNx` local fork (tag `v1.0-pre2026-engine` on `feature/sdf-font-shader`) — John's final pre-2026 state
- `john-savepoint/FFNx` public fork — upstream `master` (3d2a6918, May 2026) — has 2026 compat

**Risk assessment:** Overall port difficulty: **LOW-MEDIUM**. 14 files copy as-is. Of 16 conflict files: 8 TRIVIAL/EASY, 7 MODERATE, 1 HARD (movies.cpp). The HARD file's conflicts are structural not algorithmic — John replaced enum definitions and function bodies, upstream added FF8 support. Resolvable with care.

---

## File Structure Map

### Group 0 — Buildsystem & Config (pre-flight)

| File | Action | Difficulty |
|---|---|---|
| `CMakeLists.txt` | Verify John's new .cpp files are listed for compilation | TRIVIAL |

### Group 1 — John-Only Files: Copy As-Is (14 files)

| # | File | Lines | Purpose | Risk |
|---|---|---|---|---|
| 1.1 | `misc/FFNx.sdf.frag` | 250 | SDF fragment shader (GLSL) — glyph rendering with thickness/shadow/outline/glow/color-cycle | None |
| 1.2 | `misc/FFNx.sdf.vert` | 32 | SDF vertex shader (GLSL) — cell-local coordinates, italic/skew transforms | None |
| 1.3 | `src/ff7/japanese_text.cpp` | 2455 | **THE core file** — Japanese text rendering, character width tables, texture coordinate mapping, SDF integration. Depends on `cfg.h` (enable_sdf_fonts) and `renderer.h` (SDF uniforms) | LOW — deps on conflict files verified |
| 1.4 | `src/sdf_debug.cpp` | 552 | ImGui SDF parameter tuning overlay (34 params, presets, animations) | None |
| 1.5 | `src/sdf_debug.h` | 18 | SDF debug header | None |
| 1.6 | `src/ff7/char_portrait_anim.cpp` | 259 | Character portrait animation system (speaker inference, layout) | None |
| 1.7 | `src/ff7/char_portrait_anim.h` | 55 | Portrait animation header | None |
| 1.8 | `src/ff7/title_progress.cpp` | 131 | Title screen progress tracking (early-game/world-map/meteor/final states) | None |
| 1.9 | `src/ff7/title_progress.h` | 50 | Title progress header | None |
| 1.10 | `src/video/title_sequence.cpp` | 168 | Title sequence control | LOW — includes movies.cpp |
| 1.11 | `src/video/title_sequence.h` | 69 | Title sequence header | None |
| 1.12 | `src/video/title_video.cpp` | 120 | Title video overlay rendering | LOW — includes movies.cpp |
| 1.13 | `src/video/title_video.h` | 72 | Title video header | None |
| 1.14 | `src/video/video_context.cpp` | 453 | Video rendering context with FFmpeg integration | MEDIUM — depends on movies.cpp heavily. If movies.cpp API changed, this breaks |
| 1.15 | `src/video/video_context.h` | 123 | Video context header | LOW |

**Verified:** All 14 files confirmed zero upstream presence (`git log origin/master -- <file>` returns 0). No upstream commit ever touched these paths. They will apply cleanly via copy or cherry-pick.

⚠️ **video_context.cpp** is the risk here — it includes `movies.cpp` structures and may need API adaptation after movies.cpp is merged.

### Group 2 — Conflict Files: TRIVIAL (apply as-is)

| # | File | John (+/-) | Upstream (+/-) | Resolution |
|---|---|---|---|---|
| 2.1 | `src/common.h` | +1 line: `#define VERSION_FF7_102_JP 19` | +7/-1: `FF7_RERELEASE_APPID`, `MODE_ENDINGMOVIE` | Different sections. Add John's line after upstream's version defines block. |

| 2.2 | `src/ff7/defs.h` | +1 line (minor struct change) | +8/-1 (new fields) | Different parts of same struct. Merge both additions. |

| 2.3 | `src/ff7/battle/defs.h` | +5 lines | +1/-1 line | Adjacent but non-overlapping. Merge both. |

### Group 3 — Conflict Files: EASY (minor overlap)

| # | File | John (+/-) | Upstream (+/-) | What Each Changed | Resolution |
|---|---|---|---|---|---|
| 3.1 | `src/cfg.cpp` | ~+130 lines: 40 SDF config vars + 10 portrait/title config vars | ~+50 lines: enable_uncrop, use_sdl_gamepad, display_index, enable_external_mesh, ff8_always_capture_input | Both add new config variables but in completely disjoint sections. John's added after `enable_bilinear` and after `ff7_advanced_blinking`. Upstream added between existing vars. | Insert John's blocks into upstream-modified file. No line-level conflict — different insertion points. |

| 3.2 | `src/cfg.h` | +52 lines: extern declarations for all SDF + portrait/title vars | +7 lines: extern declarations for upstream new vars | Same pattern as cfg.cpp. Disjoint insertion points. | Insert John's extern blocks after upstream's additions. |

| 3.3 | `src/gl/texture.cpp` | +17 lines: SDF mode activation in `gl_set_texture()` | +1/-1 line: copyright year only | John adds SDF check in the function body. Upstream didn't touch the function. | Copy John's code block from the John branch. Zero conflict. |

| 3.4 | `src/saveload.cpp` | +55/-7 lines: SDF texture variant search in `load_normal_texture()`, improved logging | +3/-3 lines: save_textures_legacy support, improved log message | John modifies the middle of `load_normal_texture()`. Upstream modifies a different function (`save_texture()`) and adds minor logging change. | Merge SDF block into upstream's version. Verify both changes apply. |

| 3.5 | `misc/FFNx.toml` | +42/-16 lines: SDF font config section, portrait/title video config | +38/-4 lines: new app settings (display index, SDL gamepad, etc.) | Both add config sections. Upstream adds to top-level keys. John adds at end of file. | Apply John's additions at end of upstream's TOML. No line conflict — different sections. |

| 3.6 | `src/renderer.cpp` | +120/-10 lines: SDF shader paths in `updateRendererShaderPaths()`, SDF program creation in `init()`, SDF uniforms in `init()`, SDF texture detection in `useTexture()`, SDF guard in `setInterpolationQualifier()` | +20/-12 lines: SmoothSkinning flags + uniform, HDR/logging changes, macOS launcher renderer selection, `getShader()` uses `_fullpath` | John's additions are in 5 separate blocks. Upstream changes interleave lightly (comments, logging). The `setInterpolationQualifier` overlap: John restructured it with SDF guard, upstream didn't touch it. | Merge strategy: take upstream's base, insert John's 5 code blocks. For `setInterpolationQualifier`: keep John's version (upstream didn't change this function, only log messages above it changed). |

### Group 4 — Conflict Files: MODERATE (API changes to reconcile)

| # | File | John (+/-) | Upstream (+/-) | Key API Changes | Resolution |
|---|---|---|---|---|---|
| 4.1 | `src/renderer.h` | +18/-1 lines: SDF enums (`SDF_FONT_FLAT`, `SDF_FONT_SMOOTH`, `SDF_PARAMS`–`SDF_ATLAS_PARAMS`), `sdfTextures` map in InternalState, SDF shader path strings, `baseInterpolationQualifier`, `setSDFMode()`/`registerSDFTexture()` declarations | +18/-8 lines: `BONE_MATRICES`/`SKINNING_FLAGS` enums, `MAX_BONE_MATRICES`, `bIsSmoothSkinning`, `SmoothSkinningFlags`, `bone_matrices[]`, `bone_weights[4]`/`bone_indices[4]` in Vertex struct, `setUniform()` now takes `int arraySize = 1`, `screenShot()` signature changed, `IsVkDown()` added | **`setUniform()` signature changed** — John's code that calls `setUniform()` may need updating. **Vertex struct changed** — John's vertex handling code must handle new fields. Both add to the same enums (no value collision). | 1. Take upstream's enum, append John's values to `RendererUniform` and `RendererProgram`. 2. Take upstream's Vertex struct, `InternalState`, `setUniform` signature. 3. Add John's `sdfTextures`, SDF paths, `baseInterpolationQualifier`, `setSDFMode()`, `registerSDFTexture()` declarations. 4. Update any John code calling old `setUniform(sig)` to pass `arraySize` param. |

| 4.2 | `src/overlay.cpp` | +3 lines: `#include "sdf_debug.h"`, SDF debug menu item, SDF debug draw call | +35/-30 lines: ImGui API update (io.KeyMap→AddKeyEvent, cmd.TextureId→GetTexID), IsVkDown helper, removed unnecessary null check | Upstream rewrote the ImGui integration. John's 3-line addition applies cleanly on top. | Take upstream's version, add John's 3 lines at the obvious insertion points. SDF debug menu item goes after "Lighting Debug" in the same pattern. |

| 4.3 | `src/overlay.h` | (no changes detected — John didn't modify this file header) | +1 line: `IsVkDown()` declaration | If John didn't touch overlay.h, no conflict. | Verify: if John has zero diff on overlay.h, use upstream's version directly. |

| 4.4 | `src/gl.h` | +1 line: `uint32_t is_sdf` in `gl_texture_set` struct | +10/-1 lines: `ExternalMesh` forward decl, `DCT_EXTERNAL_MESH` enum, `external_mesh` field in `deferred_draw`, `gl_load_state()` takes `bool bind_textures = true`, `gl_defer_external_mesh()`, `gl_draw_external_mesh()` | John adds 1 field to a struct. Upstream adds many things including to the same struct. | Merge `is_sdf` field into upstream's `gl_texture_set`. No field name collision. Verify `gl_load_state()` calls from John's code pass the new bool default. |

| 4.5 | `src/ff7_opengl.cpp` | +14/-2 lines | +31/-19 lines | Both touched different functions in the same file. Upstream made wider changes. Need to verify no function-level collision. | Read John's diff target (which function he changed) vs upstream's diff target. If different functions: safe merge. If same function: manual resolution. |

| 4.6 | `src/ff7/battle/battle.cpp` | +32/-14 lines | +6/-4 lines | Both in different code blocks within the same file. | Verify insertion points don't collide. If separate: merge both. |

### Group 5 — Conflict Files: HARD (significant overlap)

| # | File | John (+/-) | Upstream (+/-) | Nature of Conflict | Resolution |
|---|---|---|---|---|---|
| 5.1 | `src/movies.cpp` | Structural rewrite: removed `MovieAudioLayers` enum from file top, reorganized `ff7_prepare_movie()` and `ff7_release_movie_objects()`, changed game loop integration | +60/-15 lines: added `#include "utils.h"` / `"ff8/movies.h"`, `ff8_movie_cam_buffer[2MB]`, removed `steam_edition` conditions (now use `enable_steam_achievements` directly), major `ff8_prepare_movie()` refactor (cam buffer from stack → static, `fopen` → `fopen_rb`) | **Different parts of the same file changed both directions.** John's changes are in FF7 code paths. Upstream's heavy changes are in FF8 code paths AND in the FF7 achievement integration. The `steam_edition` removal is the key overlap — John may have also touched those conditionals. | **Strategy:** 1. Start with upstream's `movies.cpp`. 2. Read John's diff specifically for FF7 functions (`ff7_prepare_movie`, `ff7_release_movie_objects`, game loop). 3. Apply John's FF7 function rewrites on top of upstream's file (they modify different code blocks). 4. Pay special attention to `steam_edition` removal — upstream removed it from 2 lines; verify John didn't also touch those lines. 5. The structural removal of `MovieAudioLayers` enum — check if it moved to a header. **This is the riskiest single file. Budget 2x time vs other MODERATE files.** |

---

## Task Execution Plan

### Pre-flight: Verify CMakeLists.txt includes all John's new .cpp files

- [ ] Check that `src/ff7/japanese_text.cpp`, `src/sdf_debug.cpp`, `src/ff7/char_portrait_anim.cpp`, `src/ff7/title_progress.cpp`, `src/video/title_sequence.cpp`, `src/video/title_video.cpp`, `src/video/video_context.cpp` are all in the CMake file list on John's branch
- [ ] If not present, add them to CMakeLists.txt on the port branch

### Task 1: Create port branch + Apply John-Only Files (14 files, ~15 min)

- [ ] **Step 1.1: Create port branch off upstream master**

```bash
cd /mnt/c/FFNx
git fetch savepoint master
git checkout -b feature/2026-port-universal savepoint/master
```

- [ ] **Step 1.2: Copy John-only shader files**

```bash
git checkout feature/sdf-font-shader -- misc/FFNx.sdf.frag misc/FFNx.sdf.vert
```

- [ ] **Step 1.3: Copy John-only source files**

```bash
git checkout feature/sdf-font-shader -- \
  src/ff7/japanese_text.cpp \
  src/sdf_debug.cpp src/sdf_debug.h \
  src/ff7/char_portrait_anim.cpp src/ff7/char_portrait_anim.h \
  src/ff7/title_progress.cpp src/ff7/title_progress.h \
  src/video/title_sequence.cpp src/video/title_sequence.h \
  src/video/title_video.cpp src/video/title_video.h \
  src/video/video_context.cpp src/video/video_context.h
```

- [ ] **Step 1.4: Verify all files present**

```bash
for f in misc/FFNx.sdf.frag misc/FFNx.sdf.vert src/ff7/japanese_text.cpp src/sdf_debug.cpp src/sdf_debug.h src/ff7/char_portrait_anim.cpp src/ff7/char_portrait_anim.h src/ff7/title_progress.cpp src/ff7/title_progress.h src/video/title_sequence.cpp src/video/title_sequence.h src/video/title_video.cpp src/video/title_video.h src/video/video_context.cpp src/video/video_context.h; do [ -f "$f" ] && echo "OK $f" || echo "MISSING $f"; done
```

Expected: All 14 files show OK.

- [ ] **Step 1.5: Commit group 1**

```bash
git add misc/ src/ff7/japanese_text.cpp src/sdf_debug.cpp src/sdf_debug.h src/ff7/char_portrait_anim.cpp src/ff7/char_portrait_anim.h src/ff7/title_progress.cpp src/ff7/title_progress.h src/video/title_sequence.cpp src/video/title_sequence.h src/video/title_video.cpp src/video/title_video.h src/video/video_context.cpp src/video/video_context.h
git commit -m "feat(port): apply John-only files — SDF shaders, Japanese text, portraits, title video

14 files with zero upstream presence, copied from feature/sdf-font-shader.
Includes: SDF shaders (frag+vert), japanese_text.cpp (core), sdf_debug,
char_portrait_anim, title_progress, video/* (title sequence, video, context)"
```

### Task 2: Apply TRIVIAL conflict files (3 files, ~5 min)

- [ ] **Step 2.1: common.h — add JP version define**

```bash
# Edit src/common.h: add '#define VERSION_FF7_102_JP 19' after '#define VERSION_FF7_102_SP 4'
git add src/common.h
git commit -m "feat(port): add VERSION_FF7_102_JP to common.h

Japanese version identifier for multi-language routing."
```

- [ ] **Step 2.2: ff7/defs.h + ff7/battle/defs.h — merge minor additions**

```bash
# These are 1-5 line additions each. Read the diff from John's branch and apply manually.
git diff feature/sdf-font-shader -- src/ff7/defs.h  # Review
git diff feature/sdf-font-shader -- src/ff7/battle/defs.h  # Review
# Apply John's additions to these files
git add src/ff7/defs.h src/ff7/battle/defs.h
git commit -m "feat(port): merge John's minor FF7 def changes

ff7/defs.h: struct field addition
ff7/battle/defs.h: 5-line battle definitions"
```

### Task 3: Apply EASY conflict files (6 files, ~20 min)

- [ ] **Step 3.1: cfg.cpp + cfg.h — add SDF config variables**

```bash
# Take upstream's cfg.cpp/cfg.h, add John's SDF+portrait config blocks
# John's additions go after 'enable_bilinear' and after 'ff7_advanced_blinking'
# Upstream's new vars go in between existing vars
# Use git diff feature/sdf-font-shader -- src/cfg.cpp to see exact insertion points
git add src/cfg.cpp src/cfg.h
git commit -m "feat(port): add SDF font + portrait/title config variables

~40 SDF configs: pixel_range, thickness, shadow_offset(_x/_y), shadow_blur,
outline_width/opacity, inner_outline, glow_radius/intensity, color controls,
italic_slant, skew_x/y, animations (speed, color_cycle, pulse, cycle_offset).

Portrait/title configs: char_portrait_anim_enable, title_video_enable/path/loop/
audio/progress_based, per-state video paths."
```

- [ ] **Step 3.2: gl/texture.cpp — add SDF mode activation**

```bash
# Take upstream's texture.cpp, add John's SDF check block into gl_set_texture()
git add src/gl/texture.cpp
git commit -m "feat(port): add SDF texture mode activation in gl_set_texture()"
```

- [ ] **Step 3.3: saveload.cpp — add SDF texture variant loading**

```bash
# Merge John's _sdf filename search into upstream's load_normal_texture()
git add src/saveload.cpp
git commit -m "feat(port): add SDF texture variant loading in saveload.cpp

When enable_sdf_fonts is set, tries <filename>_sdf.<ext> before regular texture.
Sets gl_set->is_sdf flag and registers with renderer."
```

- [ ] **Step 3.4: FFNx.toml — add SDF + portrait config section**

```bash
# Append John's config sections to upstream's TOML
git add misc/FFNx.toml
git commit -m "feat(port): add SDF font + portrait/title config to FFNx.toml"
```

- [ ] **Step 3.5: renderer.cpp — add SDF shader integration**

```bash
# 5 insertion points (see Group 3.6 in analysis)
# Take upstream's renderer.cpp, insert John's:
# 1. SDF shader paths in updateRendererShaderPaths()
# 2. SDF program creation in init()
# 3. SDF uniforms in init()
# 4. SDF texture detection in useTexture()
# 5. SDF guard in setInterpolationQualifier()
git add src/renderer.cpp
git commit -m "feat(port): add SDF shader integration to renderer

SDF shader paths (.sdf flat/smooth), SDF_FONT_FLAT/FONT_SMOOTH programs,
12 SDF uniforms (params, colors, animations, atlas), texture detection in
useTexture(), setInterpolationQualifier SDF guard."
```

### Task 4: Apply MODERATE conflict files (6 files, ~25 min)

- [ ] **Step 4.1: renderer.h — merge API changes**

```bash
# Key reconciliation: setUniform() now takes (uniform, value, arraySize=1)
# Add John's SDF enums, sdfTextures map, SDF paths, setSDFMode/registerSDFTexture
# Upstream adds BONE_MATRICES, SKINNING_FLAGS, bone_weights/indices in Vertex
# Merge both enum additions (no value collision)
git add src/renderer.h
git commit -m "feat(port): merge SDF renderer types with upstream renderer API

Reconciled: setUniform() signature (added arraySize param), Vertex struct
(bone data), SDF enums appended to RendererUniform and RendererProgram.
Added: sdfTextures map, setSDFMode(), registerSDFTexture(), SDF paths."
```

- [ ] **Step 4.2: overlay.cpp — apply SDF debug on top of ImGui update**

```bash
# Take upstream's ImGui 1.91+ version (AddKeyEvent, GetTexID), add John's 3 lines
git add src/overlay.cpp
git commit -m "feat(port): add SDF debug overlay on updated ImGui integration"
```

- [ ] **Step 4.3: gl.h — add is_sdf field to upstream's gl_texture_set**

```bash
# Merge is_sdf into upstream's gl_texture_set struct
git add src/gl.h
git commit -m "feat(port): add is_sdf field to gl_texture_set"
```

- [ ] **Step 4.4: ff7_opengl.cpp — merge John's changes with upstream**

```bash
# Verify function-level collision via diff inspection
# John: +14/-2, Upstream: +31/-19
# Apply both sets of changes
git add src/ff7_opengl.cpp
git commit -m "feat(port): merge John's OpenGL changes with upstream updates"
```

- [ ] **Step 4.5: ff7/battle/battle.cpp — merge battle modifications**

```bash
# John: +32/-14, Upstream: +6/-4
# Apply both, verify insertion points don't collide
git add src/ff7/battle/battle.cpp
git commit -m "feat(port): merge John's battle modifications with upstream"
```

### Task 5: Apply HARD conflict file (1 file, ~15 min)

- [ ] **Step 5.1: movies.cpp — manual merge**

```bash
# Start from upstream's movies.cpp (has FF8 support, steam_edition removal)
# Read John's diff in detail:
git diff feature/sdf-font-shader -- src/movies.cpp | head -200
# Identify John's FF7-specific changes
# Apply John's ff7_prepare_movie/ff7_release_movie_objects rewrites
# Verify steam_edition removal compatibility
# This file has the most risk — review carefully
```

- [ ] **Step 5.2: Commit movies.cpp**

```bash
git add src/movies.cpp
git commit -m "feat(port): merge John's movie playback changes with upstream FF8 support

Carefully reconciled: John's FF7 movie structure reorganization with upstream's
FF8 movie cam buffer and achievement system refactor. Removed steam_edition
condition (upstream did same). Preserved both code paths."
```

### Task 6: Build attempt + fix compilation errors (~20 min)

- [ ] **Step 6.1: Attempt build**

```bash
cd /mnt/c/FFNx
cmake --build .build --config Release 2>&1 | tee /tmp/ff7-port-build.log
```

Expected: Compilation errors likely in:
- `video_context.cpp`: if movies.cpp structures changed
- `japanese_text.cpp`: if cfg.h/renderer.h types not yet resolved
- Any `setUniform()` calls that didn't get the new `arraySize` param

- [ ] **Step 6.2: Fix compilation errors iteratively**

For each error:
1. Identify the mismatch
2. Fix the code
3. Rebuild
4. Repeat until clean

Common expected fixes:
- `setUniform(X, val)` → `setUniform(X, val, 1)` — add arraySize arg
- `io.KeyMap[...]` → `io.AddKeyEvent(...)` — ImGui API update
- Missing includes or forward declarations

- [ ] **Step 6.3: Commit build fixes**

```bash
git add -A
git commit -m "fix(port): compilation fixes for 2026 upstream API changes"
```

### Task 7: Push port branch + tag

- [ ] **Step 7.1: Push to savepoint fork**

```bash
git push savepoint feature/2026-port-universal
```

- [ ] **Step 7.2: Tag the port attempt**

```bash
git tag -a v0.1-2026-port-initial -m "Initial FFNx 2026 port attempt — all 30 John files applied on upstream master with 2026 compat. Build status: [PASSING/FAILING]"
git push savepoint v0.1-2026-port-initial
```

---

## Difficulty Distribution Summary

| Difficulty | Count | Files |
|---|---|---|
| TRIVIAL (copy/1-line) | 3 + 14 | All John-only + common.h, ff7/defs.h, battle/defs.h |
| EASY | 6 | cfg.cpp, cfg.h, texture.cpp, saveload.cpp, FFNx.toml, renderer.cpp |
| MODERATE | 6 | renderer.h, overlay.cpp, overlay.h, gl.h, ff7_opengl.cpp, battle/battle.cpp |
| HARD | 1 | movies.cpp |
| **Total** | **30** | |

## Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| video_context.cpp breaks on movies.cpp changes | MEDIUM | HIGH | Analyze movies.cpp diff first; may need API adaptation in video_context |
| setUniform() calls missing arraySize arg | HIGH | LOW | Mechanical fix — grep and update |
| ImGui API mismatch in overlay | LOW | LOW | Upstream already handled; John's additions are 3 lines |
| movies.cpp structural conflict | MEDIUM | MEDIUM | Isolated to FF7 vs FF8 code paths; John and upstream touch different functions |
| CMakeLists.txt missing new source files | MEDIUM | LOW | Pre-flight check catches this |
| Build failure cascading from one conflict file | MEDIUM | MEDIUM | Build after each task group; catch early |

## Estimated Duration

| Task | Time |
|---|---|
| Pre-flight + group 1 (John-only) | 15 min |
| Task 2 (TRIVIAL) | 5 min |
| Task 3 (EASY) | 20 min |
| Task 4 (MODERATE) | 25 min |
| Task 5 (HARD — movies.cpp) | 15 min |
| Task 6 (build + fix) | 20 min |
| Task 7 (push + tag) | 2 min |
| **Total** | **~1.5 hours** |

---

*Plan generated 2026-05-03 JST. Session 8abae264. Companion to MASTER plan at docs/superpowers/plans/2026-04-26-MASTER-monorepo-split-and-2026-pivot.md.*

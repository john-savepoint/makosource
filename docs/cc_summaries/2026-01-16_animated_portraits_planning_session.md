# FF7 Animated Portraits Implementation Planning Session

**Created:** 2026-01-16 14:10 JST (Thursday)
**Session ID:** eaca1cfd-b054-4014-92c9-48c0e5801853
**Author:** Claude Code (Sonnet 4.5)
**Status:** Planning Complete - Ready for Implementation

---

## Executive Summary

This session produced a comprehensive implementation plan for adding AI-generated video-based animated character portraits and animated title screen to Final Fantasy VII using the FFNx driver (PR #737 branch).

**Key Deliverable:** Implementation plan document at `/home/johnzealanddoyle/.claude/plans/peppy-noodling-taco.md`

---

## Session Overview

### Initial Requirements Clarification

The session began with the user requesting implementation of features from `ANIMATED_FEATURES_IMPLEMENTATION_SPEC.md`. Initial interpretation assumed sprite sheet-based animation, but user clarified the actual requirement:

**Actual Goal:** Video playback in character portrait rectangles with a two-phase system:
1. **Intro video** - Character "gets into position" (plays once, 1-2 seconds)
2. **Loop video** - Subtle idle animation (loops indefinitely, first frame matches last frame of intro)

This clarification fundamentally changed the technical approach from sprite animation to video streaming to arbitrary screen rectangles.

### Architecture Research Phase

Conducted comprehensive exploration of FFNx codebase (`/mnt/c/FFNx/`) to understand existing video infrastructure:

**Key Findings:**
- FFNx has mature FFmpeg-based video pipeline (`src/video/movies.cpp`, 849 lines)
- YUV planar video decoding with hardware acceleration support
- BGFX texture streaming for video frames
- Color space handling (BT.601/709, sRGB, NTSC-J, etc.)
- Current limitation: Only fullscreen video rendering via `gl_draw_movie_quad()`

**Critical Gap Identified:** No existing "video to arbitrary rectangle" capability - videos always render fullscreen. This became the core technical challenge to solve.

---

## Technical Architecture Designed

### Phase 1: Video Portrait System

**Core Innovation:** Extend FFNx's video pipeline to support rendering YUV video to arbitrary screen rectangles (not just fullscreen).

**New Components:**

1. **Data Structures** (`src/ff7/portrait_video.h`):
   - `PortraitVideo` struct - Manages dual FFmpeg contexts (intro + loop)
   - YUV texture handles per portrait (bgfx::TextureHandle for Y, U, V planes)
   - State machine: IDLE → PLAYING_INTRO → PLAYING_LOOP

2. **Video Player** (`src/ff7/portrait_video.cpp`):
   - `portrait_video_load()` - Initialize FFmpeg contexts for intro + loop videos
   - `portrait_video_update()` - Decode frames, manage state transitions
   - `portrait_video_draw()` - Render YUV frame to specified rectangle

3. **Rendering Extension** (`src/gl/gl.cpp`):
   - New function: `gl_draw_yuv_to_rect(tex_y, tex_u, tex_v, x, y, w, h)`
   - Parameterized version of existing `gl_draw_movie_quad_common()`
   - Handles YUV→RGB conversion via shader with proper color matrix

4. **Menu Integration** (`src/ff7/menu.cpp`):
   - Hook `menu_draw_everything_6CC9D3` (existing PR #737 hook point)
   - Read active party members from savemap memory (`0xDC4F8-FA`)
   - Update and draw portrait videos for 3 party slots
   - Graceful fallback to static portraits if video missing

### Phase 2: Title Screen Video

**Simpler Implementation:** Leverages existing fullscreen video playback.

**Approach:**
- Hook title screen entry to start video playback
- Use existing `ffmpeg_prepare_movie()` and `draw_yuv_frame()` functions
- Loop video continuously until user input
- Config toggle for enable/disable

---

## Implementation Plan Structure

The final plan document includes:

### Technical Specifications

1. **Video Asset Requirements:**
   - 18 portrait videos (9 characters × 2 videos each)
   - Format: H.264 MP4, 24-30 FPS
   - Resolution: 64x64 to 256x256 (matches portrait UI size)
   - **Critical constraint:** Loop video frame 0 must exactly match intro video final frame

2. **File Modifications:**
   - 4 new files (portrait_video.h/cpp, extensions to gl.cpp and menu.cpp)
   - 4 extended files (cfg.cpp/h, FFNx.toml, movies.cpp)
   - No new dependencies (uses existing FFmpeg, BGFX, TOML++)

3. **Configuration Options:**
   ```toml
   portrait_video_enable = true
   portrait_video_path = "movies/portraits"
   title_video_enable = true
   title_video_path = "movies/title_cinematic.mp4"
   title_video_loop = true
   ```

### Implementation Timeline

**3-Week Breakdown:**

- **Week 1:** Core video-to-rect infrastructure
  - Create `gl_draw_yuv_to_rect()` function
  - Build `portrait_video` module
  - Test single-character proof-of-concept

- **Week 2:** Menu integration
  - Find exact portrait screen coordinates via code analysis
  - Hook menu rendering
  - Handle party member changes

- **Week 3:** Title screen + polish
  - Implement title video playback
  - Performance testing (concurrent video decode)
  - Memory leak testing
  - Documentation and packaging

### 7th Heaven Packaging

IRO structure defined:
```
FF7-AnimatedPortraits.iro/
├── mod.xml
├── preview.gif
└── movies/
    ├── portraits/
    │   ├── cloud_intro.mp4
    │   ├── cloud_loop.mp4
    │   └── ... (16 more)
    └── title_cinematic.mp4
```

---

## Key Technical Insights

### 1. FFNx Video Pipeline Architecture

**Decoder Flow:**
```
av_read_frame() → avcodec_decode() → sws_scale()
  ↓
buffer_yuv_frame() [10-frame circular buffer]
  ↓
upload_yuv_texture() [3× R8 textures for Y, U, V]
  ↓
gl_draw_movie_quad() [fullscreen quad with YUV→RGB shader]
```

**Color Space Handling:**
- Supports BT.601/709 color matrices
- Gamut conversion: sRGB, NTSC-J, SMPTE-C, EBU
- Gamma functions: 2.2, 2.8, sRGB, SMPTE170M
- Full-range vs TV-range detection

### 2. BGFX Texture System

**Renderer Integration:**
- Texture slots: TEX_Y (0), TEX_U (1), TEX_V (2)
- Format: R8 for planar YUV
- Fragment shader performs matrix-based YUV→RGB conversion
- Hardware-accelerated where available (DXVA, NVDEC)

### 3. Menu Graphics Objects

**From FF7 Game Engine documentation:**
- Portraits loaded from TEX files: `CLOUD.TEX`, `BARRE.TEX`, etc.
- Menu avatar graphics objects at memory address `0xDC1014` (Bank D)
- Party member IDs at savemap addresses `0xDC4F8-FA` (3 bytes)

---

## Open Questions (To Resolve During Implementation)

1. **Portrait Coordinates:**
   - Need to trace menu rendering code to find exact pixel positions for each party slot
   - Must handle resolution scaling (640×480, 1280×720, 1920×1080)

2. **Concurrent Video Performance:**
   - With 3 portraits + title potentially decoding simultaneously, need to verify:
     - FFmpeg thread safety with multiple AVFormatContext instances
     - GPU memory usage with 12+ YUV textures (3 portraits × 3 planes + title × 3 planes)
     - Frame rate maintained at 60 FPS

3. **Extended Portrait Support:**
   - Naming screen also shows character portrait
   - Battle UI shows character status portraits
   - Should these also be animated? (Likely future enhancement)

---

## Context Files Analyzed

### Documentation Read (Parallel):
1. `/home/johnzealanddoyle/projects/tools/.project/SESSION_CONTEXT_19-28_NAMING_SCREEN.md` (1251 lines)
2. `/home/johnzealanddoyle/projects/tools/.project/naming_screen_tables.txt` (362 lines)
3. `/home/johnzealanddoyle/projects/tools/.project/SceneSessionContextDirectory.md` (496 lines)
4. `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/FFNX_DEVELOPER_GUIDE.md` (2310 lines)
5. `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/FFNX_DIRECTORY_STRUCTURE.md` (220 lines)
6. `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/ANIMATED_FEATURES_IMPLEMENTATION_SPEC.md` (951 lines)
7. `/mnt/c/FFNx/docs/reference/game_engine/extracted_major_sections/04_MENU_MODULE.md` (503 lines)

### FFNx Codebase Exploration:
- **Video System:** `src/video/movies.cpp` (849 lines), `src/movies.cpp` (249 lines)
- **Rendering:** `src/renderer.cpp` (2647 lines), `src/gl/gl.cpp`, `src/gl/deferred.cpp`
- **Graphics:** `src/ff7/graphics.cpp`

**Total Context Processed:** ~8,500 lines of documentation + FFNx source code exploration

---

## Methodology Notes

### Planning Approach

1. **Requirements Clarification:** Used AskUserQuestion to resolve ambiguity between sprite animation vs video playback.

2. **Codebase Exploration:** Launched Explore agent to research FFNx video infrastructure before designing solution.

3. **Architecture-First Design:** Designed data structures and component boundaries before implementation details.

4. **Iterative Plan Refinement:** Updated plan multiple times as understanding deepened.

### Learning Mode Insights

★ **Insight ─────────────────────────────────────**

**FFNx Video Architecture Pattern:**
FFNx's video system uses a **decoupled pipeline** where:
- Video decoding (FFmpeg) happens in `movies.cpp`
- YUV texture upload happens in renderer
- Drawing happens in GL layer

This separation allows extending the system by adding new drawing functions (`gl_draw_yuv_to_rect`) without modifying the decoder or texture upload logic. Classic separation of concerns.

**YUV vs RGB Textures:**
FFNx stores video as 3 separate R8 textures (Y, U, V planes) rather than a single RGB texture because:
- Reduces GPU memory bandwidth (YUV420 is 50% smaller than RGB24)
- Allows hardware-accelerated YUV→RGB conversion in fragment shader
- Preserves original color space for accurate conversion with proper matrices

**Circular Frame Buffer:**
The 10-frame video buffer uses read/write indices to prevent allocations during playback. Producer (decoder) writes at `vbuffer_write`, consumer (renderer) reads at `vbuffer_read`. This is a classic lock-free ring buffer pattern for real-time multimedia.

─────────────────────────────────────────────────

---

## Next Steps

### Immediate Actions (User)

1. **Review implementation plan:** `/home/johnzealanddoyle/.claude/plans/peppy-noodling-taco.md`

2. **Video asset preparation:**
   - Generate 18 portrait videos (9 characters × intro + loop)
   - Ensure loop frame 0 matches intro final frame exactly
   - Prepare title screen video (30-60 seconds)

3. **FFNx branch confirmation:**
   - Working branch: `/mnt/c/FFNx/` (PR #737)
   - Confirm this is the correct target

### Implementation Phase (Developer Agent)

1. **Week 1:** Core infrastructure (proof-of-concept with Cloud portrait)
2. **Week 2:** Full menu integration (all 9 characters)
3. **Week 3:** Title screen + testing + packaging

### Resume Command

```bash
cd /home/johnzealanddoyle/projects/tools
claude --dangerously-skip-permissions --resume eaca1cfd-b054-4014-92c9-48c0e5801853
```

**Appended to:** `/home/johnzealanddoyle/projects/tools/.project/resume/resume.txt`

---

## Session Metrics

- **Duration:** ~2.5 hours
- **Tool Uses:** 64 (exploration agent)
- **Context Consumed:** 65,800 / 200,000 tokens
- **Files Created:** 1 (implementation plan)
- **Files Modified:** 1 (resume.txt)
- **Plan Document Size:** 520 lines

---

## Files Referenced

### Input Documents
- `ANIMATED_FEATURES_IMPLEMENTATION_SPEC.md` - Original feature spec
- `FFNX_DEVELOPER_GUIDE.md` - FFNx contribution guidelines
- `SESSION_CONTEXT_19-28_NAMING_SCREEN.md` - Prior naming screen work context
- `04_MENU_MODULE.md` - FF7 menu system documentation

### Output Documents
- `/home/johnzealanddoyle/.claude/plans/peppy-noodling-taco.md` - Implementation plan (520 lines)
- `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/cc_summaries/2026-01-16_animated_portraits_planning_session.md` - This summary

### FFNx Source Code Analyzed
- `src/video/movies.cpp` - FFmpeg video decoder
- `src/movies.cpp` - FF7/FF8 movie wrapper
- `src/renderer.cpp` - BGFX texture system
- `src/gl/gl.cpp` - Movie quad rendering
- `src/gl/deferred.cpp` - Deferred rendering integration

---

## Conclusion

This session successfully transformed a high-level feature request ("animated portraits") into a concrete, implementable technical plan by:

1. **Clarifying requirements** through user questions
2. **Researching existing infrastructure** via codebase exploration
3. **Designing a clean architecture** that extends (not replaces) FFNx's video system
4. **Documenting a phased implementation** with clear milestones and test criteria

The resulting plan is ready for development phase and includes all necessary technical details, file structure, configuration, and packaging requirements.

**Status:** Ready for implementation. User has all assets prepared. FFNx PR #737 branch is the target.

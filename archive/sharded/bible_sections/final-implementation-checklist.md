# FINAL IMPLEMENTATION CHECKLIST

**Use this checklist to track your implementation progress:**

## Phase 1: Foundation (Core C++)
- [ ] Configuration added (cfg.h, cfg.cpp)
- [ ] Global variables defined (globals.h, common.cpp)
- [ ] Registry hooks updated (common.cpp - dotemuRegQueryValueExA)
- [ ] Texture allocation override (common.cpp - common_load_texture)
- [ ] Multi-page loader (saveload.cpp - load_external_texture)
- [ ] File redirection (redirect.cpp - jfleve typo fix)
- [ ] Width table patch (ff7/font.cpp, ff7/font.h)
- [ ] Width patch called in init (ff7_opengl.cpp)

## Phase 2: Assembly & Renderer
- [ ] g_currentFontPage allocated (globals.h, common.cpp)
- [ ] Hext patch created (misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt)
- [ ] Addresses verified with debugger
- [ ] Renderer hook (gl/gl.cpp - gl_bind_texture_set)
- [ ] Palette change handler (common.cpp - common_palette_changed)

## Phase 3: Assets & Testing
- [ ] All 6 jafont_*.png textures created
- [ ] Character mapping CSV complete
- [ ] Unit Test 1: Red W Test (PASS)
- [ ] Unit Test 2: Width Patch (PASS)
- [ ] Integration Test 1: Multi-texture load (PASS)
- [ ] Integration Test 2: Page switching (PASS)
- [ ] Full System Test: Real Japanese dialogue (PASS)
- [ ] Regression Test: English mode still works (PASS)

## Phase 4: Advanced Features (Optional)
- [ ] Furigana opcode (0xF9) implemented
- [ ] Furigana renderer hook
- [ ] Line height patch applied
- [ ] Furigana testing complete

## Phase 5: Deployment
- [ ] All debug code removed/disabled
- [ ] Performance verified
- [ ] Documentation written
- [ ] .iro package created
- [ ] User installation guide
- [ ] Released to community

---

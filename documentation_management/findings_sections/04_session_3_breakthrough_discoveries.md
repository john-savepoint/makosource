# Session 3 Breakthrough Discoveries

**Extracted From**: FINDINGS.md
**Section Lines**: 239-587
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


**Research Date**: 2025-11-15 20:00 JST
**Session**: 1021bc57-9aa2-41fe-baad-a6b89b252744 (compacted)
**URLs Analyzed**: 5 new sources (Tonberry internals, BGFX examples, FFNx source code)

### Discovery #1: Tonberry's Runtime Texture Injection Architecture

**Sources**:
- https://forums.qhimm.com/index.php?topic=15945.0 (Tonberry Enhanced thread)
- Community analysis of Tonberry 2.04 implementation

**How Tonberry Works**:

**Interception Mechanism**:
- Hooks `UnlockRect()` DirectX function to intercept texture loading
- NO modification of game executable or driver required
- Runtime injection only - fully reversible

**Hashmap System**:
```text
Directory Structure:
[FF8]/tonberry/hashmap/*.csv  → Hash-to-texture mapping files
[FF8]/textures/**/*.png        → Replacement texture PNG files
[FF8]/tonberry/prefs.txt       → Configuration (cache size, etc.)
```

**CSV Format**:
```csv
texture_name,hash_value
sysfld00_13,8637763346649579509
menu_icon_02,2847593920174638291
```

**Special Features**:
- **Persistent textures**: Prefix with `!` to keep in cache permanently
- **Disabled textures**: Prefix with `*` to exclude from loading
- **Plug-and-play mods**: Move CSV to `disabled/` folder to turn off mod
- **Cache management**: Configurable size (max 250 for non-LAA builds)

**Performance Characteristics**:
- `UnlockRect()` identified as primary bottleneck
- Alternative hashing algorithms tested but minimal improvement
- Cache eviction needed for 32-bit memory constraints

**Critical Implication**: **Runtime texture injection WORKS** without source code modification. If FFNx has similar texture override, Japanese fonts could be injected the same way.

---

### Discovery #2: FFNx Already Has Texture Override System

**Sources**:
- https://github.com/julianxhokaxhiu/FFNx/issues/29 (FF8 texture override issue)
- https://github.com/julianxhokaxhiu/FFNx (repository overview)
- FFNx.toml configuration file

**FFNx Texture Replacement Architecture**:

**Configuration (FFNx.toml)**:
```toml
# Texture override path
mod_path = "mods/Textures"

# Supported formats
mod_ext = ["dds", "png"]

# Additional options
show_missing_textures = false
save_textures = false  # Dump internal textures for modding
```

**Key Quote from Issue #29**:
> "Like we do on FF7, also on FF8 we need to provide a way to override textures around the game."

**Implication**: **FF7 texture override ALREADY EXISTS in FFNx** (mentioned as reference point for FF8 implementation)

**Supported Texture Modules** (confirmed working):
- Field backgrounds
- Battle textures
- Magic effects
- World map
- Menu elements (potentially including fonts?)

**Differences from Tonberry**:
- **Path-based**, not hash-based (simpler but requires knowing exact names)
- **DDS preferred**, PNG fallback (higher quality, smaller memory)
- **override_path**: Separate data directory override layer

**Critical Finding**: FFNx ALREADY can replace game textures. The question is: can it replace font textures specifically?

---

### Discovery #3: BGFX Font System Uses TrueType, Not Bitmaps

**Sources**:
- https://github.com/bkaradzic/bgfx/blob/master/examples/10-font/font.cpp
- BGFX font manager implementation

**BGFX Font Architecture**:

**Runtime TrueType Loading**:
```cpp
// 1. Create font manager
FontManager* m_fontManager = new FontManager(512);  // 512 = atlas size
TextBufferManager* m_textBufferManager = new TextBufferManager(m_fontManager);

// 2. Load TrueType file
TrueTypeHandle ttf = loadTtf(m_fontManager, "font/example.ttf");

// 3. Generate font at specific size
FontHandle font = m_fontManager->createFontByPixelSize(ttf, 0, 32);

// 4. Preload glyphs (optional optimization)
m_fontManager->preloadGlyph(font, L"abcdefghijklmnopqrstuvwxyz");
m_fontManager->preloadGlyph(font, L"ABCDEFGHIJKLMNOPQRSTUVWXYZ");

// 5. Can destroy TTF if all glyphs preloaded
m_fontManager->destroyTtf(ttf);  // Limits to preloaded glyphs
// OR keep TTF loaded for dynamic glyph generation
```

**Key Characteristics**:
- **Dynamic glyph generation**: If TTF remains loaded, glyphs generated on-demand
- **Font atlas**: Glyphs rasterized to texture atlas automatically
- **Multiple fonts**: Can load multiple TTF files simultaneously
- **Buffer types**: Static (immutable) and Transient (updated per-frame)
- **Styled text**: Background, underline, overline, strike-through via TextBufferManager

**Critical Revelation**: BGFX does NOT use bitmap font textures (like `usfont.png`). It loads **TrueType fonts** and generates glyph textures at runtime.

**Implication for FF7**: If FFNx uses BGFX for font rendering (which it does for debug UI), the same system COULD be used for game fonts. Japanese TrueType fonts could be loaded via configuration.

---

### Discovery #4: FFNx Font Rendering Uses ImGui + BGFX (Debug UI Only)

**Sources**:
- https://raw.githubusercontent.com/julianxhokaxhiu/FFNx/master/src/overlay.cpp
- FFNx source code analysis

**FFNx Debug Overlay Architecture**:

**Font Atlas Generation**:
```cpp
// ImGui generates font atlas texture
ImFontAtlas* fonts = ImGui::GetIO().Fonts;
unsigned char* pixels;
int width, height;
fonts->GetTexDataAsRGBA32(&pixels, &width, &height);

// Upload to BGFX as texture
bgfx::TextureHandle m_texture = bgfx::createTexture2D(
    width, height, false, 1,
    bgfx::TextureFormat::BGRA8, 0,
    bgfx::copy(pixels, width * height * 4)
);
```

**Text Rendering**:
- ImGui generates vertex/index buffers for text glyphs
- BGFX shader samples font atlas texture
- Scissor rects for clipping
- No explicit TrueType file references (ImGui handles internally)

**Critical Limitation**: This is ONLY for FFNx's debug overlay (DevTools menu, memory debugger, etc.). **Game fonts are handled separately**.

**Source Code Analysis**:
- **No font.cpp/font.h** in FFNx src directory
- **No menu_us.lgp loading code** found in FFNx source
- **Game fonts likely handled by original executable** or through BGFX at a different level

**Key Question**: If FFNx doesn't have game font code, where do game fonts come from?

**Possible Answers**:
1. **Original executable** loads `usfont.png` from `menu_us.lgp` (legacy code path)
2. **BGFX library** handles it automatically via renderer backend
3. **FFNx hooks** the loading but doesn't have dedicated source files for it

---

### Revised Understanding: The Font Loading Mystery

Based on Session 3 research, we now understand:

**What We Know**:
- ✅ BGFX **CAN** load TrueType fonts at runtime
- ✅ FFNx **DOES** use BGFX for rendering
- ✅ FFNx **HAS** texture override system (`mod_path`)
- ✅ Tonberry **PROVES** runtime texture injection works for Square Enix games
- ✅ Text editing tools **SUPPORT** Japanese encoding

**What Remains Unclear**:
- ❓ Does FF7 use bitmap fonts (`usfont.png`) or TrueType fonts?
- ❓ Where in FFNx (or game executable) are game fonts loaded?
- ❓ Can FFNx's `mod_path` override font textures specifically?
- ❓ If fonts are bitmaps, can they be replaced via texture override?
- ❓ If fonts are TrueType, can we configure FFNx to load Japanese TTF?

---

### Potential Implementation Paths (Updated Session 3)

Based on new discoveries, here are the refined approaches:

**Path A: Texture Override (If Fonts Are Bitmaps)**

**Concept**:
- If FF7 uses bitmap font textures (like `usfont.png` from `menu_us.lgp`)
- Use FFNx's existing `mod_path` system to override with Japanese font textures
- Create 6 Japanese font texture files (matching Japanese version's `jafont_X.tex`)

**Steps**:
1. Extract `usfont.png` from `menu_us.lgp` (find current texture names)
2. Create Japanese font texture replacements (6 sets for full kanji coverage)
3. Place in `mod_path` directory with correct naming
4. Configure FFNx.toml to load textures
5. Test if game recognizes replaced fonts

**Advantages**:
- Uses FFNx's existing, proven texture override system
- NO source code modification required
- Fully reversible (remove textures to revert)
- Same approach as Tonberry for FF8

**Challenges**:
- Need exact texture naming scheme
- Character encoding still single-byte (can only display 256 characters)
- Would need to solve character→texture mapping (which of 6 textures?)

**Feasibility**: HIGH (if fonts are indeed bitmap textures)

---

**Path B: Runtime TrueType Loading (If FFNx Can Be Extended)**

**Concept**:
- Add configuration to FFNx.toml to load Japanese TrueType fonts
- Leverage BGFX's existing `FontManager` + `createFontByPixelSize()`
- Generate Japanese glyphs at runtime

**Configuration Example** (hypothetical):
```toml
[font]
# Override game font with TrueType file
game_font_path = "mods/Fonts/japanese.ttf"
font_size = 16
preload_japanese = true  # Preload common kanji
```

**Implementation**:
```cpp
// In FFNx initialization
TrueTypeHandle jpFont = loadTtf(fontManager, config.game_font_path);
FontHandle gameFont = fontManager->createFontByPixelSize(jpFont, 0, 16);

// Preload Japanese character sets
fontManager->preloadGlyph(gameFont, L"あいうえお..."); // Hiragana
fontManager->preloadGlyph(gameFont, L"アイウエオ..."); // Katakana
fontManager->preloadGlyph(gameFont, L"一二三四五..."); // Common kanji
```

**Advantages**:
- Uses BGFX's proven TrueType system
- Scalable fonts (can render any size)
- Full Unicode support (can display all Japanese characters)
- Dynamic glyph generation (don't need to preload all 2,000+ kanji)

**Challenges**:
- **Requires FFNx source code modification** (adding configuration parsing + font loading)
- Character encoding still needs double-byte support
- Game executable might hard-code bitmap font assumptions

**Feasibility**: MEDIUM (requires collaboration with FFNx developers)

---

**Path C: Hybrid Approach (Most Practical)**

**Concept**:
1. **Phase 1**: Test texture override for current bitmap fonts
2. **Phase 2**: If successful, contact FFNx developers about TrueType support
3. **Phase 3**: Implement character encoding extension separately

**Why This Works**:
- Validates texture override concept first (low risk, no code changes)
- Gathers real data about font loading mechanism
- Provides proof-of-concept for FFNx collaboration discussion
- Separates font rendering from character encoding (can solve incrementally)

**Feasibility**: HIGHEST (pragmatic, step-by-step approach)

---

### Immediate Next Steps (Revised Based on Session 3)

**PRIORITY 1: Validate Texture Override Concept**

1. **Extract current FF7 font textures**:
   - Use 7th Heaven or LGP tools to extract `menu_us.lgp`
   - Identify font texture files (likely `usfont.png` or similar)
   - Document exact file names and formats

2. **Test FFNx texture override**:
   - Create dummy replacement texture (different color to verify loading)
   - Place in `mod_path` directory
   - Launch game and verify texture loads
   - Document which texture names work

3. **Acquire Japanese eStore version** ~~(if accessible)~~ **UPDATE (Session 4)**:
   - **STATUS**: Japanese eStore version (SEDL-1010) is **NO LONGER AVAILABLE FOR PURCHASE**
   - Product page returns 404 error as of 2025-11-15
   - **Alternative approach**:
     * Contact FFNx developers (they reference having access in Issue #39)
     * Request `menu_ja.lgp` extraction from community members who own it
     * Collaborate with FFNx team for font file analysis

**PRIORITY 2: Investigate Font Loading Mechanism**

4. **Search FFNx source for LGP loading**:
   - Look for `menu_us.lgp` references in source code
   - Find texture loading hooks
   - Understand how `mod_path` override works internally

5. **Test BGFX font capabilities**:
   - Compile BGFX font example (examples/10-font)
   - Load Japanese TrueType font
   - Verify Japanese character rendering works

**PRIORITY 3: Contact FFNx Developers**

6. **Comment on Issue #39** with findings:
   - Share Session 1-3 research discoveries
   - Present Tonberry comparison analysis
   - Propose BGFX TrueType font loading approach
   - Ask about texture override for fonts

**PRIORITY 4: Character Encoding (Deferred)**

7. This remains a secondary problem after font rendering is solved
8. Can be tackled via touphScript extension or game executable patching

---

**Document Status**: Active Research
**Next Update**: After texture override validation tests
**Maintainer**: Project Team

---


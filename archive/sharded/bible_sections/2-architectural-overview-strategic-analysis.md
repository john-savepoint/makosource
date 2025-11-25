# 2. ARCHITECTURAL OVERVIEW & STRATEGIC ANALYSIS

## 2.1 The Core Technical Deficit

**English FF7 Engine Architecture:**
```
Text Data (KERNEL.BIN) → Single-Byte Indices (0x00-0xFF) → USFONT.TEX (256x256 texture) → Renderer
```

**Why This Fails for Japanese:**
1. **Capacity Constraint:** 256 slots < 2,300 required characters
2. **Encoding Conflict:** Shift-JIS is double-byte (e.g., `0x82 0xA0`)
   - English engine reads this as TWO separate characters: `0x82` and `0xA0`
   - Results in rendering two garbage Latin characters instead of one Kanji
3. **Architectural Limitation:** The game's text parser is hardcoded for single-byte reads
4. **Memory Layout:** Width tables, coordinate calculations, and buffer sizes assume 256 max

## 2.2 The AF3DN.P Solution (Reference Architecture)

**Discovered Architecture from Japanese eStore Release:**

```
Text Data → Custom Parser → Page Marker Detection → Multi-Texture System → Renderer
                ↓                      ↓                       ↓
        0xFA detected           Switch to Page 1        Bind jafont_2.tex
        0xFB detected           Switch to Page 2        Bind jafont_3.tex
        ...                     ...                     ...
```

**Key Components:**
1. **Asset Structure:** Six 1024x1024 texture pages (jafont_1.tex through jafont_6.tex)
2. **Encoding System:**
   - `0x00-0xE6`: Standard characters → Page 0 (jafont_1)
   - `0xFA [Index]`: Extended characters → Page 1 (jafont_2)
   - `0xFB [Index]`: Extended characters → Page 2 (jafont_3)
   - `0xFC [Index]`: Extended characters → Page 3 (jafont_4)
   - `0xFD [Index]`: Extended characters → Page 4 (jafont_5)
   - `0xFE [Index]`: Extended characters → Page 5 (jafont_6)
3. **Driver Logic:** AF3DN.P intercepts DirectX 9 texture binding calls
4. **Geometry Handling:** Custom width tables for fixed-width Kanji rendering

**Why This Works:**
- `0xFA-0xFE` were **unused control codes** in the English version
- No collision with existing game logic
- Backward compatible (English files don't contain these codes)
- Minimal changes required (driver-level only, no EXE modification)

## 2.3 The FFNx Implementation Strategy (Path C - Hybrid Extension)

**Our Approach:**

```
FFNx Driver Extensions:
├── Configuration Layer (TOML settings)
├── Memory Allocation Override (Force 6 texture slots)
├── Asset Loading Pipeline (Load all 6 PNGs)
├── Registry Virtualization (Language-aware paths)
├── Assembly Hook (Text parser injection)
├── Renderer State Management (Texture page binding)
└── Geometry Patch (Character width table)
```

**Advantages:**
- ✅ **Open Source:** FFNx is MIT licensed
- ✅ **Modern Backend:** BGFX supports Vulkan, DirectX 12, Metal
- ✅ **Community Support:** Active development and maintenance
- ✅ **Legal:** Clean-room reimplementation based on reverse engineering
- ✅ **Extensible:** Foundation for multi-language, Furigana, and future features
- ✅ **No EXE Patching:** Works with both ff7_en.exe and ff7_ja.exe unmodified

**Implementation Layers:**

| Layer | Component | Language | Files Modified |
|-------|-----------|----------|----------------|
| 1. Configuration | User-facing toggles | TOML | FFNx.toml |
| 2. Globals | State variables | C++ | src/cfg.h, src/cfg.cpp, src/globals.h |
| 3. Allocation | Memory override | C++ | src/common.cpp |
| 4. Loading | Asset pipeline | C++ | src/saveload.cpp |
| 5. Redirection | File path handling | C++ | src/redirect.cpp, src/common.cpp |
| 6. Geometry | Width table patch | C++ | src/ff7/font.cpp, src/ff7/menu.cpp |
| 7. Parser Hook | Text byte stream | Assembly (Hext) | misc/hext/ff7/en/FFNx.JAPANESE_FONT.txt |
| 8. Renderer | Texture binding | C++ | src/gl/gl.cpp |

---

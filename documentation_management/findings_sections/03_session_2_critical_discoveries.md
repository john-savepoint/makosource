# Session 2 Critical Discoveries

**Extracted From**: FINDINGS.md
**Section Lines**: 41-238
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


**Research Date**: 2025-11-15 19:30 JST
**Session**: 1021bc57-9aa2-41fe-baad-a6b89b252744 (resumed)
**URLs Analyzed**: 7 new sources (FFNx docs, source code, qhimm forums, FF8 mods)

### Discovery #1: FF8 Proves Texture-Based Font Replacement Works

**Source**: https://forums.qhimm.com/index.php?topic=16355.0

FF8 PC successfully replaced its font system using **texture injection** rather than driver modification:

**Method**:
1. **Tonberry Tool** - Texture injection system for FF8
2. **Texture Files** - Font glyphs stored in `textures/Sy/` folder
3. **Hash Mapping** - Excel spreadsheet maps texture hashes to font characters
4. **No Driver Changes** - Works on top of Steam version without modifying executables

**Workflow**:
```text
1. Create font texture files (PNG format)
2. Place in textures/Sy/ folder
3. Create/update hashmap Excel file
4. Disable Steam overlay
5. Launch game - Tonberry injects textures at runtime
```

**Versions Released**:
- Version 1 (2015) - Initial release
- Version 2 (2017) - Bug fixes for punctuation glitches
- Version 3 (2019) - Final polish, improved 'W' character

**Compatibility**: Works with SeeD Reborn mod (shares same hashmap system)

**Critical Implication**: **Same texture injection approach could work for FF7**. If Tonberry-equivalent exists for FF7 (or can be created), Japanese fonts could be loaded without modifying FFNx driver.

---

### Discovery #2: FFNx Font System Architecture Confirmed

**Sources**:
- https://raw.githubusercontent.com/julianxhokaxhiu/FFNx/master/misc/FFNx.toml
- https://raw.githubusercontent.com/julianxhokaxhiu/FFNx/master/src/renderer.cpp

**FFNx.toml Analysis**:
- **NO font configuration options exist**
- Only generic texture settings: `mod_path`, `mod_ext`, `save_textures`
- `enable_ntscj_gamut_mode` for Japanese TV color simulation (cosmetic only)
- **Conclusion**: Font system is **hardcoded** in driver source, not user-configurable

**renderer.cpp Analysis**:
- Extensive texture management functions (`createTexture()`, `createTextureHandle()`, `createTextureLibPng()`)
- Text rendering: `printText()` function uses `bgfx::dbgTextPrintf` (BGFX library call)
- **NO font loading functionality in this file**
- **NO Japanese character handling**
- **NO font-specific texture management**

**Critical Finding**: Font rendering is **delegated to BGFX library**, not custom implementation in renderer.cpp. Font-specific code must be in different source files.

**Implication**: FFNx driver modification would require:
1. Finding font-specific source files (not renderer.cpp)
2. Understanding BGFX library font system
3. Implementing multi-texture font loading
4. Character encoding expansion

---

### Discovery #3: Text Editing Tools Already Support Japanese

**Source**: http://forums.qhimm.com/index.php?topic=9658.0 (Makou Reactor thread)

**Historical Timeline**:
- **2010-05-13**: Gemini asks "What about adding support for Japanese versions?"
- **2010-05-13**: myst6re (developer) responds: "I'll think about it I just need the text encoding, or menu text texture."
- **2010-05-13**: Gemini provides complete Japanese character encoding table
- **2010-05-13**: myst6re confirms: "Done, I have many things to add before next release."

**Current Status**:
- Makou Reactor 2.1.0 (latest) **fully supports Japanese character encoding**
- Can edit Japanese text in field files (flevel.lgp)
- Can save Japanese characters to game files
- **BUT**: Game cannot display them (gibberish output)

**touphScript Status** (from Session 1):
- Dumps all FF7 text to UTF-8 files
- Re-encodes back to FF Text format
- **Limitation**: Single-byte encoding only (by design of FF Text format)

**Critical Conclusion**: **Text editing is NOT the blocker**. Tools can handle Japanese input. The blocker is purely **font RENDERING** in the game engine.

---

### Discovery #4: FFNx Japanese Support Status

**Source**: https://github.com/julianxhokaxhiu/FFNx/blob/master/docs/how_to_install.md

**Official Statement** (FFNx v1.x documentation):
> "Japanese support is currently work in progress. The game starts fine but font is not rendering properly and battles do crash sometimes."

**Supported Versions**:
- 1998 Eidos Release
- 2013 Steam Release
- **2013 eStore Release (Japanese)** - May 16, 2013 release
- Android Release

**Japanese eStore Version**:
- Contains `menu_ja.lgp` with 6 font textures
- Uses **completely customized AF3DN.P driver**
- Driver is **larger** than Steam version
- No source code available from Square Enix

**Availability Status (Session 4 Update - 2025-11-15)**:
- **PRODUCT DELISTED**: eStore page (SEDL-1010) returns 404 error
- **No longer purchasable** from official Square Enix Japan store
- May still be accessible to:
  * FFNx developers (have access for testing per Issue #39)
  * Community members who purchased before delisting
  * Requires alternative acquisition strategy

**Current Status**: FFNx can theoretically load Japanese version files, but:
- Font rendering broken
- Battle system crashes
- No active development on Issue #39 since 2020

---

### Discovery #5: Successful Retranslation Workflow Example

**Source**: https://www.shinraarchaeology.com/retransmod.html

**Shinra Archaeology Cut Mod**:
- Full retranslation of FF7 to modern English
- Compatible with 7th Heaven mod manager
- ~500MB .IRO file format
- Restores cut content from original files

**Tools Used**:
- Makou Reactor (field editing)
- WallMarket (KERNEL.BIN editing)
- ProudClod (scene.bin editing)
- Black Chocobo (save editing)
- KimeraCS, Scarlet (unknown purposes)

**Methodology**:
- All text modifications done **within FF Text encoding limitations**
- No font changes attempted
- Uses existing single-byte character set
- Proves comprehensive text modding is possible without touching font system

**Implication**: Text modding infrastructure is **mature and proven**. Once font rendering is solved, implementing Japanese text will use these same tools.

---

### Revised Understanding: The Three-Layer Problem

Based on Session 2 findings, the Japanese support problem has **three distinct layers**:

**Layer 1: Text Editing** ✅ **SOLVED**
- Makou Reactor supports Japanese encoding (since 2010)
- touphScript can dump/restore text (UTF-8 capable)
- Proven workflow from Shinra Archaeology mod
- **Status**: Infrastructure exists and works

**Layer 2: Font Rendering** ⚠️ **PRIMARY BLOCKER**
- English version has 1 font texture set
- Japanese needs 6 font texture sets
- No loading mechanism for multiple font sets
- Font system hardcoded in driver/executable
- **Status**: This is the core problem to solve

**Layer 3: Character Encoding** ⏳ **SECONDARY BLOCKER**
- FF Text format: single-byte, 256 character max
- Japanese needs: 2,000+ characters (double-byte)
- Engine assumes one byte = one character
- **Status**: Can be solved AFTER font rendering works

### Recommended Next Steps (Based on Session 2)

**Immediate Priority**:
1. **Investigate Tonberry Tool** - Understand texture injection mechanism for FF8
2. **Check for FF7 equivalent** - Does FF7 have a Tonberry-like tool?
3. **Test texture override** - Can FFNx `mod_path` load custom font textures?
4. **Analyze hashmap system** - How does FF8 map characters to texture files?

**Medium Priority**:
5. **Find FFNx font source files** - Not in renderer.cpp, where is it?
6. **Research BGFX font system** - How does BGFX handle fonts internally?
7. **Acquire Japanese eStore version** - Extract `menu_ja.lgp` for analysis
8. **Contact FFNx developers** - Comment on Issue #39 with findings

**Lower Priority** (after proof-of-concept):
9. Design character encoding extension (single→double byte)
10. Implement touphScript extension for Japanese
11. Create Japanese text file conversions
12. Full game testing and debugging

---


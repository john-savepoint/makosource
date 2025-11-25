# 1. EXECUTIVE MISSION BRIEFING

## 1.1 The Objective

You are tasked with extending the **FFNx graphics driver** to enable **native Japanese text rendering** in the English version of Final Fantasy VII (1998/Steam/2013).

**The Problem:**
- The vanilla English game engine is architecturally limited to a **Single-Byte Character Encoding** system (0x00-0xFF)
- It can only address a maximum of **256 unique characters**
- Japanese requires approximately **2,300+ glyphs** (Hiragana, Katakana, and Kanji)
- Mathematical impossibility: 256 < 2,300

**The Breakthrough:**
- Analysis of the rare 2013 Japanese eStore version revealed Square Enix's production solution
- They implemented a **Multi-Page Texture System** using the proprietary AF3DN.P driver
- The system uses **unused control codes (0xFA-0xFE)** as texture page-switching opcodes
- This is a **proven, production-viable architecture**

**Your Mission:**
- Reimplement this architecture within the **open-source FFNx driver**
- Do NOT use the proprietary AF3DN.P directly
- Leverage FFNx's modern **BGFX rendering backend**
- Create a legally sound, community-maintainable solution
- Enable future extensibility (multi-language support, Furigana, real-time switching)

## 1.2 Success Criteria

**Phase 1 (Core Implementation):**
- ✅ FFNx successfully loads 6 font texture pages
- ✅ FA-FE control codes trigger texture page switching
- ✅ Japanese characters render at correct width (16px, not squashed)
- ✅ No crashes when launching ff7_ja.exe
- ✅ English mode continues to work (backward compatibility)

**Phase 2 (Advanced Features):**
- ✅ Furigana (reading guides) render correctly above Kanji
- ✅ Runtime language switching (en ↔ ja without restart)
- ✅ 7th Heaven .iro integration working
- ✅ Custom font path override functional

**Phase 3 (Polish):**
- ✅ All verification tests pass
- ✅ FFNx.log shows clear diagnostic information
- ✅ No memory leaks or corruption
- ✅ Performance overhead < 5% compared to English mode

---

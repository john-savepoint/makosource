# Session 6 Update: CRITICAL ASSET ACQUISITION (2025-11-16 10:49)

**Extracted From**: FINDINGS.md
**Section Lines**: 2037-2093
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


**BREAKTHROUGH**: User has purchased Japanese eStore version (SEDL-1010)!

**Product**: (Windows ダウンロード版)ファイナルファンタジーVII インターナショナル for PC
**Release**: May 16, 2013
**Status**: **NOW DELISTED** - User has rare copy!

### What This Means

**Direct Access to Square Enix's Implementation**:
- 6 Japanese font textures (jafont_1-6.tex) in menu_ja.lgp
- Reference character layout (which kanji in which texture)
- Glyph sizing used by Square Enix
- Character organization pattern
- No reverse-engineering guesswork needed!

**Extraction Path**:
```bash
[Japanese FF7]/data/menu/menu_ja.lgp
  ↓ Extract with ulgp -x
jafont_1.tex through jafont_6.tex
  ↓ Convert with Tex Tools
jafont_1.png through jafont_6.png (visual analysis)
```

### Critical Realization: Double-Byte Encoding is NON-NEGOTIABLE

**User's Insight**: "Hiragana and Katakana alone is unacceptable. We need all 2,000+ kanji available."

**This is absolutely correct**. Adult Japanese literacy requires:
- 2,136 Jōyō kanji (minimum)
- 46 hiragana
- 46 katakana
- Punctuation and special characters
- **Total: ~2,300+ characters**

**Single-byte encoding (256 character limit) = FUNCTIONALLY USELESS**

### Shift to Phase 2: Double-Byte Encoding Research

**New Priority**: Investigate how Japanese eStore version implements:
1. **Shift-JIS encoding** (standard Japanese double-byte system)
2. **Character→texture mapping** (which of 6 textures contains character X?)
3. **Text file modifications** (flevel.lgp, KERNEL.BIN with Japanese encoding)
4. **Driver-level character lookup** (how AF3DN.P handles double-byte→glyph conversion)

**Research Tools Available**:
- ✅ Japanese eStore version files (complete implementation reference)
- ✅ Brave Search for technical documentation
- ✅ Firecrawl for deep technical scraping
- ✅ FFNx source code analysis (GitHub)

---

---


# The Core Technical Problem

**Extracted From**: FINDINGS.md
**Section Lines**: 588-656
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### Character Encoding Incompatibility

**English Version**:
- Uses "FF Text" encoding format
- Single-byte character system
- ASCII values offset by 0x20
- Supports ~256 total characters
- Character table fully documented at: https://ff7-mods.github.io/ff7-flat-wiki/FF7/Text_encoding.html

**Japanese Requirements**:
- Requires minimum **1,945 Jōyō kanji + hiragana + katakana**
- Necessitates double-byte (multi-byte) character encoding
- Cannot fit into existing single-byte architecture

### Font Texture Space Limitations

**English PC Version** (`menu_us.lgp`):
- **CONFIRMED FONT FILES** (Session 4 - qhimm Wiki):
  * High-resolution: `USFONT_H.TEX`, `USFONT_A_H.TEX`, `USFONT_B_H.TEX`
  * Low-resolution: `USFONT_L.TEX`, `USFONT_A_L.TEX`, `USFONT_B_L.TEX`
- Located at offset 0x2754 in WINDOW.BIN (PSX), MENU_US.LGP (PC)
- Character spacing defined in `window.bin`
- Total texture space: ~1 font set worth of glyphs (3 texture variants)

**Japanese PC Version** (`menu_ja.lgp` - eStore only):
- Six separate font texture files:
  - `jafont_1.tex`
  - `jafont_2.tex`
  - `jafont_3.tex`
  - `jafont_4.tex`
  - `jafont_5.tex`
  - `jafont_6.tex`
- Requires 6x the texture memory
- **English version has no loading mechanism for multiple font sets**

**PlayStation Japanese Version**:
- Used dynamic kanji loading system
- `window.bin` contains large blank space below text area (documented in qhimm Wiki)
- Quote: "The large blank spot under the menu text is for the Japanese characters that were removed in the non-Japanese version of the game."
- Field files specified which kanji glyphs to load per scene
- System not ported to PC

### System Architecture Constraints

The text rendering system is hardcoded across multiple components:

1. **Game Executable** (`ff7.exe` / `ff7_en.exe`)
   - Text rendering routines
   - Character encoding/decoding logic
   - Font texture loading
   - Window sizing calculations
   - Menu text and Lv4 Limit dialogue

2. **Graphics Driver** (`AF3DN.P` or modern `FFNx`)
   - Font texture injection
   - Glyph rendering pipeline
   - Texture memory management

3. **Data Files** (all use FF Text encoding):
   - `flevel.lgp` - Field dialogue and scripts
   - `KERNEL.BIN` - Menu data, character names
   - `kernel2.bin` - Item names and descriptions
   - `scene.bin` - Battle dialogue, enemy names
   - `world_us.lgp` - World map dialogue

---


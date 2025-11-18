# Session 6: CJK Font Atlas Constraints & Tool Chain Completion (2025-11-15 23:58)

**Extracted From**: FINDINGS.md
**Section Lines**: 1904-2036
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


**Research Date**: 2025-11-15 23:58 JST (Saturday)
**Session**: 1021bc57-9aa2-41fe-baad-a6b89b252744 (continuation from Session 5)
**Sources Analyzed**: 5 pending URLs (tim2png, TEX to BMP, Tex Tools, 7th Heaven, CJK Font Atlas)

### Discovery #1: CJK Font Atlas Mathematical Constraints

**Source**: https://killertee.wordpress.com/2021/04/23/optimizing-workflow-textmesh-pro-font-atlas-for-language-localization/

**General Statement on CJK Characters**:
> "Chinese, Japan, Korean and other Hieroglyphic Language have a massive set of characters. To contain all the characters of each one, several atlases must be built (most platforms have 2048×2048 limit for texture size)."

**Constraints Identified**:
1. **Platform texture limit**: 2048×2048 pixels (common GPU constraint)
2. **Character count**: 2000-3000 characters needed for CJK languages
3. **Padding requirements**: 4-5 pixels standard for SDF (Signed Distance Field) gradient effects
4. **Solution approach**: "Only used characters will be built into atlas" (selective character sets)

**Limitation of Source**: Article **does not provide explicit mathematical proof** or calculations demonstrating why 2000-3000 characters cannot fit in a single 2048×2048 texture. It states the constraint exists but focuses on practical solutions rather than mathematical derivation.

**Manual Calculation** (to fill research gap):

```
Basic calculation for 2048×2048 texture:

Assumptions:
- Glyph size: 16×16 pixels (common for readable kanji)
- Padding: 5 pixels per glyph (4-5 pixels mentioned in article)
- Effective glyph area: (16 + 5) × (16 + 5) = 21 × 21 = 441 pixels per character

Texture capacity:
- Total texture area: 2048 × 2048 = 4,194,304 pixels
- Characters per 2048×2048 texture: 4,194,304 ÷ 441 = ~9,508 characters

This suggests 2048×2048 CAN fit 2000-3000 characters at 16×16 glyph size!

BUT: Japanese kanji requires LARGER glyphs for readability:
- At 32×32 glyph size + 5px padding:
  * Effective area: (32 + 5) × (32 + 5) = 37 × 37 = 1,369 pixels
  * Capacity: 4,194,304 ÷ 1,369 = ~3,062 characters
  * Still fits 2000-3000 characters!

- At 48×48 glyph size + 5px padding:
  * Effective area: (48 + 5) × (48 + 5) = 53 × 53 = 2,809 pixels
  * Capacity: 4,194,304 ÷ 2,809 = ~1,492 characters
  * DOES NOT FIT 2000-3000 characters!

- At 64×64 glyph size + 5px padding:
  * Effective area: (64 + 5) × (64 + 5) = 69 × 69 = 4,761 pixels
  * Capacity: 4,194,304 ÷ 4,761 = ~880 characters
  * DOES NOT FIT 2000-3000 characters!
```

**Conclusion**: The 2048×2048 texture limit becomes a constraint **depending on glyph size requirements**. At 48×48 pixels or larger (often needed for complex kanji), a single texture cannot hold 2000-3000 characters.

**FF7 Japanese Version**: Uses **6 texture files** (`jafont_1-6.tex`), suggesting:
- Either larger glyph sizes (48×48 or 64×64)
- Or conservative padding/layout
- Or inclusion of ALL Jōyō kanji (2,136 characters) + hiragana + katakana + punctuation

---

### Discovery #2: Alternative TEX Conversion Tools

**Sources**:
- tim2png: https://github.com/cebix/ff7tools/blob/master/README
- TEX to BMP: https://gist.github.com/hoehrmann/5720668
- Tex Tools: https://forums.qhimm.com/index.php?topic=17755.0

**Tool Comparison**:

| Tool | Format | Language | Status | Relevance |
|------|--------|----------|--------|-----------|
| **Image2TEX** (Session 5) | TEX ↔ BMP/JPG/GIF | VB.NET | Source only | **CRITICAL** - Batch conversion |
| **Tex Tools v1.0.4.7** (Session 6) | TEX ↔ PNG/JPG/GIF/TIFF/BMP | Windows GUI | Pre-compiled | **HIGH** - Easiest to use |
| **tim2png** (Session 6) | TIM → PNG | Python | Ready to use | **MEDIUM** - PSX only |
| **TEX to BMP Pascal** (Session 6) | TEX → BMP | Pascal code | Educational | **MEDIUM** - Reference only |

**Tex Tools Features** (v1.0.4.7):
- Image resizing (useful for texture scaling)
- Clipboard operations (copy/paste workflow)
- Batch processing (mass convert directories)
- Fast conversion in source folders
- Rotate/flip transformations
- Drag-and-drop support
- Command-line compatibility

**Recommendation**: **Tex Tools v1.0.4.7** is likely easier for users than compiling Image2TEX from Visual Basic source. Forum download provides pre-compiled executable.

---

### Discovery #3: 7th Heaven + FFNx Integration Confirmed

**Source**: https://7thheaven.rocks/help/userhelp.html

**Critical Quote**:
> "This Path needs to match the subfolder name listed on the line 'mod_path =' in your 'FFNx.cfg' file."

**Texture Override Workflow**:
```
1. FFNx.toml configuration:
   mod_path = "mods/Textures"

2. 7th Heaven configuration:
   Game Driver → Textures → [FF7_DIR]/mods/Textures

3. Directory structure:
   [FF7_DIR]/
   ├── FFNx.toml
   ├── FFNx.dll
   └── mods/
       └── Textures/     ← Must match mod_path exactly
           ├── USFONT_H.PNG
           └── ... (other textures)

4. Runtime behavior:
   - FFNx searches in [FF7_DIR]/mods/ for configured subfolder
   - 7th Heaven injects mod files into this directory at launch
   - FFNx loads textures from mod_path during rendering
```

**Path Matching Rules**:
- Paths must match **exactly** (case-sensitive on Linux/macOS)
- Use **relative** path from FF7 directory (not absolute)
- Recommended standard: `mods/Textures` (community convention)

**Integration Validated**: This confirms FFNx texture override system can be used via 7th Heaven mod manager for easy distribution.

---

---


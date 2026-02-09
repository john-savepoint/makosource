# Slug Font Library - FF7 Feasibility Assessment

**Created:** 2026-01-29 (Wednesday)
**Session ID:** e6ecbd92-3335-45f3-8106-a9ef51b9390c
**Agent Type:** Research sub-agent
**Task:** FF7 Slug feasibility assessment
**Author:** Claude Code

---

## Executive Summary

This report assesses the feasibility of implementing Slug font rendering in the Final Fantasy VII (1998 PC) modding project as an alternative to the currently implemented SDF/MSDF approach. After thorough research, **Slug is NOT recommended** for this project due to licensing costs, patent restrictions, and the fact that the current SDF solution already addresses the core requirements effectively.

---

## 1. Slug Library Overview

### What is Slug?

Slug is a professional-grade GPU font rendering library developed by Eric Lengyel at Terathon Software. It renders text directly from Bezier curve outlines on the GPU without using pre-computed textures or signed distance fields.

**Key Technical Features:**
- Renders shapes directly from quadratic Bezier curve outline data
- Resolution-independent at any scale or perspective
- Perfect anti-aliasing without artifacts under magnification or minification
- Full Unicode/UTF-8 support including emoji
- Advanced typography (kerning, ligatures, OpenType features)

**How It Works:**
1. Font files (.ttf/.otf) are converted to proprietary .slug format
2. Glyph outlines stored in GPU textures as Bezier curve data
3. Pixel shader computes winding number for each pixel
4. No distance fields - direct curve sampling in shader

---

## 2. Licensing and Costs

### Proprietary Status

**Slug is NOT open source.** It is a commercially licensed library with the following key points:

| Aspect | Details |
|--------|---------|
| **Type** | Proprietary commercial software |
| **Patent** | US patent pending/granted on the algorithm |
| **Source Code** | Full source included with license |
| **Library Format** | Static C++ library |

### Licensing Options and Pricing

| License Type | Cost | Terms |
|--------------|------|-------|
| **Single-Engineer** | $1,500 USD (one-time) | Unlimited commercial products, solo developer only |
| **Per-Title** | Negotiated | Licensed for specific product |
| **Perpetual Enterprise** | Negotiated | Unlimited products, multiple developers |
| **Custom** | Negotiated | Tailored terms available |

**Contact:** info@terathon.com

### Patent Implications

The Slug algorithm is covered by a US patent (application/grant for "Method for rendering resolution-independent shapes directly from outline control points"). This has significant implications:

- **Cannot implement the algorithm independently** - Patent restricts clean-room implementations
- **Open-source alternatives limited** - Projects like [Sluggish](https://github.com/mightycow/Sluggish) exist as educational/toy implementations but note patent restrictions
- **Commercial use requires license** - Any production use requires purchasing from Terathon

---

## 3. Technical Compatibility Analysis

### Supported Graphics APIs

| API | Slug Support | FFNx Support | Compatible |
|-----|--------------|--------------|------------|
| OpenGL 3.0-4.6 | YES | YES | YES |
| Vulkan | YES | YES | YES |
| DirectX 11 | YES | YES | YES |
| DirectX 12 | YES | YES | YES |
| Metal | YES | NO | N/A |
| WebGL2 | YES | NO | N/A |

**Platform Support:** Windows, Mac, Linux, iOS, Android, major game consoles

### FFNx Integration Requirements

To integrate Slug with FFNx would require:

1. **Shader Pipeline Modification**
   - Replace current fragment shader with Slug's shader system
   - Bind Slug's glyph texture format (Bezier data + spatial structures)
   - Integrate Slug's vertex buffer generation

2. **Build System Integration**
   - Link Slug static library into FFNx build
   - FFNx uses vcpkg - Slug would need manual integration
   - Add Slug's dependencies to CMake configuration

3. **Font Pipeline Changes**
   - Convert Japanese fonts (.tim/.tex) to .ttf/.otf format (if not already)
   - Convert .ttf/.otf to proprietary .slug format using Slug's toolchain
   - Modify texture loading to handle .slug files

4. **Runtime Integration**
   - Replace current character layout code with Slug's text layout engine
   - Integrate Slug's vertex buffer generation
   - Bind Slug's two required textures (curves + spatial data)

### FFNx Current Architecture

From the codebase analysis, FFNx currently:
- Uses bgfx as rendering abstraction (supports multiple backends)
- Has custom shader system (FFNx.vert, FFNx.frag)
- Supports external texture mods via `mod_path`
- Has configurable rendering via FFNx.cfg
- Already implements SDF shader infrastructure

---

## 4. Japanese Text / CJK Capabilities

### Slug's Unicode Support

Slug supports:
- Full UTF-8 encoded Unicode strings
- All CJK ideographic characters (Japanese, Chinese, Korean)
- Emoji and pictographs with color
- Combining diacritical marks
- OpenType features

### CJK Challenges (Applicable to Any Solution)

| Challenge | Slug Approach | Current SDF Approach |
|-----------|---------------|---------------------|
| **Large glyph count** | Store curves in texture - compact | Pre-rendered atlas - larger VRAM |
| **Complex kanji** | Direct curve rendering - no loss | MSDF preserves corners well |
| **Character lookup** | Unicode-based | Grid-based (current system) |
| **Memory efficiency** | Potentially better for huge glyph sets | Good with 256x256 textures |

FF7 Japanese text requirements:
- ~3,000+ unique kanji characters
- Hiragana (46 characters)
- Katakana (48 characters)
- Full-width ASCII and symbols

---

## 5. Existing Game Modding Projects Using Slug

**Research finding: No known game modding projects use Slug.**

Slug is primarily used in:
- Professional game development (new titles)
- TouchDesigner (VJ/creative applications)
- 3D visualization applications
- VR/AR development

The lack of modding usage is due to:
1. **Cost barrier** - $1,500+ entry price
2. **Patent restrictions** - Prevents community implementations
3. **Integration complexity** - Requires significant engine modification
4. **SDF alternatives** - Free, open-source, and effective

---

## 6. Comparison with Current SDF Implementation

### FF7 Project Current Status

The project has **already successfully implemented SDF rendering** with:
- MSDF texture generation pipeline
- Custom FFNx fragment shaders
- 81% VRAM reduction
- Resolution-independent rendering
- Japanese character support

### Feature Comparison

| Feature | Current SDF/MSDF | Slug |
|---------|-----------------|------|
| **Resolution independence** | YES | YES |
| **Sharp corners** | YES (MSDF) | YES |
| **Anti-aliasing** | YES | YES |
| **Japanese support** | YES | YES |
| **VRAM usage** | ~192KB per font | Similar or better |
| **Shader complexity** | Simple median operation | Complex winding calculation |
| **Effects (outline, glow)** | Easy to add | Built-in |
| **Cost** | FREE (msdfgen MIT) | $1,500+ |
| **Patent concerns** | None | YES |
| **Implementation effort** | DONE | 6-12 weeks |

### When Slug Would Be Better

1. **Extreme magnification** - Slug renders curves directly, no SDF discretization
2. **Very complex glyphs** - MSDF can struggle with extremely intricate designs
3. **Dynamic typography** - Built-in kerning, ligatures, OpenType features
4. **Professional/commercial project** - When $1,500 is trivial vs. development time

### When Current SDF Is Sufficient

1. **Fixed rendering scales** - FF7's UI uses predictable sizes
2. **Existing working solution** - Already implemented and tested
3. **Community/modding project** - No budget for commercial licenses
4. **Simple typography needs** - No need for advanced OpenType features

---

## 7. Development Effort Estimation

### Implementing Slug (If Chosen)

| Phase | Effort | Description |
|-------|--------|-------------|
| License acquisition | 1-2 days | Contact Terathon, negotiate terms |
| Font conversion pipeline | 1 week | TIM/TEX -> TTF -> .slug |
| FFNx shader integration | 2 weeks | Replace SDF shaders with Slug |
| Build system integration | 1 week | Static library linking |
| Text layout integration | 2 weeks | Vertex buffer, layout API |
| Testing & debugging | 2 weeks | All game contexts |
| **Total** | **8-10 weeks** | Plus $1,500+ license |

### Maintaining Current SDF (Recommended)

| Phase | Effort | Description |
|-------|--------|-------------|
| Already done | 0 | SDF implementation complete |
| Optional effects | 1-2 weeks | Outline, glow, shadow |
| Polish & optimization | 1 week | Performance tuning |
| **Total** | **1-3 weeks** | No additional cost |

---

## 8. Risk Assessment

### Risks of Adopting Slug

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| License cost too high | Medium | High | Negotiate or use SDF |
| Patent issues for distribution | Medium | Critical | Ensure license covers distribution |
| FFNx integration difficulties | Medium | High | Extensive testing |
| Abandoned/unsupported | Low | Medium | Source code included |
| Overkill for requirements | High | Medium | Use simpler SDF |

### Risks of Staying with SDF

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Quality insufficient | Low | Medium | MSDF handles most cases |
| Future scaling needs | Low | Low | SDF scales to 8x+ |
| Corner artifacts | Low | Low | MSDF mitigates this |

---

## 9. Recommendation

### Verdict: NOT RECOMMENDED

**Do not adopt Slug for the FF7 Japanese font modding project.**

### Justification

1. **Cost prohibitive for modding project** - $1,500+ license fee is excessive for a community mod project

2. **Patent concerns for distribution** - Distributing a modded FFNx with Slug would require clear licensing terms for end-user distribution

3. **Current solution works well** - The existing SDF/MSDF implementation already achieves:
   - Resolution independence
   - Sharp rendering at multiple scales
   - Japanese character support
   - 81% VRAM reduction

4. **No significant quality advantage** - For FF7's use case (UI text at relatively fixed sizes), Slug offers no meaningful improvement over MSDF

5. **Development effort wasted** - 8-10 weeks to replace a working solution with marginal benefit

6. **Community cannot contribute** - Modders cannot improve/extend a patented commercial library

### When to Reconsider

Slug would be worth reconsidering if:
- The project received commercial funding/sponsorship
- Extreme quality requirements emerged (8K+ displays, VR)
- Advanced typography features became necessary
- The current SDF solution proved inadequate after testing

---

## 10. Alternative Recommendations

### Recommended Path: Enhance Current SDF

1. **Continue with MSDF** - Current implementation is solid
2. **Add shader effects** - Outline, glow, shadow using existing SDF data
3. **Optimize texture generation** - Refine msdfgen parameters for Japanese characters
4. **Test complex kanji** - Validate quality on most intricate characters

### Alternative Free Options (If SDF Proves Insufficient)

| Library | Type | License | Notes |
|---------|------|---------|-------|
| [msdfgen](https://github.com/Chlumsky/msdfgen) | MSDF | MIT | Currently used, excellent |
| [VEFontCache](https://github.com/hypernewbie/VEFontCache) | GPU Atlas | MIT | Backend-agnostic, CJK support |
| [gpu-font-rendering](https://github.com/GreenLightning/gpu-font-rendering) | Vector | MIT | Inspired by Slug, no patent |

---

## Sources

- [Slug Font Rendering Library Official Site](https://sluglibrary.com/)
- [Eric Lengyel - Terathon Software](https://terathon.com/lengyel/)
- [Sluggish GitHub Repository](https://github.com/mightycow/Sluggish)
- [Hacker News Discussion on Slug Patent](https://news.ycombinator.com/item?id=26463014)
- [GPU-Centered Font Rendering Directly from Glyph Outlines (JCGT)](http://www.jcgt.org/published/0006/02/02/)
- [FFNx GitHub Repository](https://github.com/julianxhokaxhiu/FFNx)
- [Master's Thesis: Rendering Resolution Independent Fonts in Games](https://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=9024910&fileOId=9024911)
- [GPU Font Rendering State of the Art (Lengyel)](https://www.terathon.com/font_rendering_sota_lengyel.pdf)

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-29 | 1.0 | Initial assessment created |

---

**End of Assessment**

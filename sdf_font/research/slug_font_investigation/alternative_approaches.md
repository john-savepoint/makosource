# Alternative GPU Font Rendering Approaches

**Created:** 2026-01-29 18:00:00 JST
**Last Modified:** 2026-01-29 18:00:00 JST
**Version:** 1.0.0
**Author:** Claude Code Research Sub-agent
**Session ID:** e6ecbd92-3335-45f3-8106-a9ef51b9390c
**Agent Type:** Research sub-agent
**Task:** Alternative font rendering approaches research for FF7 modding project

---

## Executive Summary

This document investigates GPU-accelerated font rendering technologies beyond basic SDF (Signed Distance Field) that could be relevant to the Final Fantasy VII original game modding project. The goal is to identify approaches that could provide high-quality Japanese character rendering at various scales while maintaining compatibility with FFNx modding platform constraints.

---

## Table of Contents

1. [MSDF (Multi-channel Signed Distance Fields)](#1-msdf-multi-channel-signed-distance-fields)
2. [Slug Font Library](#2-slug-font-library)
3. [Pathfinder (Mozilla/Servo)](#3-pathfinder-mozillaservo)
4. [DirectWrite/Direct2D](#4-directwritedirect2d)
5. [NanoVG](#5-nanovg)
6. [Loop-Blinn GPU Vector Rendering](#6-loop-blinn-gpu-vector-rendering)
7. [Direct Bezier GPU Rendering](#7-direct-bezier-gpu-rendering)
8. [stb_truetype with GPU Atlas](#8-stb_truetype-with-gpu-atlas)
9. [FreeType with GPU Acceleration](#9-freetype-with-gpu-acceleration)
10. [Comparative Analysis](#10-comparative-analysis)
11. [Recommendations for FF7 Context](#11-recommendations-for-ff7-context)

---

## 1. MSDF (Multi-channel Signed Distance Fields)

### Technical Overview

MSDF is an evolution of the standard SDF technique that uses multiple color channels (RGB) to encode distance information. The "multi-channel" approach stores the distance to edges in separate RGB channels, with the shader computing the median value to reconstruct accurate glyph shapes.

**Key Innovation:** By deliberate positioning of distance data across channels, the shader reconstructs a more accurate signed distance around corners, preserving detail at multiple scales that single-channel SDF cannot achieve.

### How It Works

1. Generate MSDF texture using tools like `msdfgen` or `msdf-atlas-gen`
2. Bake at a known pixel range (`pxrange`) that must be respected by shaders
3. At runtime, sample the MSDF texture and compute median of RGB channels
4. Apply standard SDF thresholding with the median value

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Excellent | Major improvement over SDF |
| Small text readability | Very Good | Better than SDF, though no hinting support |
| Magnification | Excellent | Resolution-independent scaling |
| Complex glyphs (CJK) | Good | Works well but requires larger atlas textures |

### Performance Characteristics

- **GPU Cost:** Virtually identical to SDF (one additional median calculation)
- **Memory:** Slightly higher than SDF (3 channels vs 1), but can use RGB8 format
- **Atlas Generation:** Faster than traditional SDF with tools like msdfgen
- **Runtime:** Excellent - single texture sample + simple shader math

### Availability/Licensing

- **msdfgen:** MIT License - [GitHub](https://github.com/Chlumsky/msdfgen)
- **msdf-atlas-gen:** MIT License - creates complete font atlases
- **Implementations:** Available for Metal, OpenGL, Vulkan, WebGL

### Relevance to FF7 Modding

**HIGH RELEVANCE** - Already partially in use in the project. MSDF is well-suited because:
- Works within FFNx shader pipeline
- Good CJK character support
- Low runtime overhead
- Single texture atlas approach compatible with game rendering

### Best Practices (2025)

- Do NOT mark MSDF textures as sRGB (treat as data)
- Generally disable mipmaps for MSDF
- Batch glyphs into single mesh per text block
- For multilingual (EN/JP), consider split atlases by script

### Sources

- [msdfgen GitHub](https://github.com/Chlumsky/msdfgen)
- [MSDF in Metal - Medium Article](https://medium.com/@sihaolu/performant-crisp-text-rendering-in-metal-with-multi-channel-signed-distance-field-msdf-9acd634c0052)
- [awesome-msdf](https://github.com/Blatko1/awesome-msdf)

---

## 2. Slug Font Library

### Technical Overview

Slug is a commercial GPU font rendering library by Eric Lengyel (Terathon Software) that renders fonts directly from Bezier curve outline data without any precomputed textures or distance fields.

**Key Innovation:** A breakthrough mathematical algorithm that achieves perfect robustness with high performance by evaluating the original Bezier curve data in the pixel shader.

### How It Works

1. Each glyph rendered by drawing a quad covering its bounding box
2. Specialized shader determines pixel coverage using original curve data
3. No texture atlas or distance field preprocessing required
4. Curve data stored directly from font file

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Perfect | Mathematically exact |
| Small text readability | Excellent | Supports stem darkening, subpixel AA |
| Magnification | Perfect | True resolution independence |
| Complex glyphs (CJK) | Excellent | No corner artifacts ever |

### Performance Characteristics

- **GPU Cost:** Higher than SDF/MSDF (more shader computation)
- **Memory:** Lower (no texture atlas needed)
- **Preprocessing:** None required at runtime
- **Runtime:** Fast but more GPU-intensive than texture-based methods

### Availability/Licensing

- **Commercial License Required** - [sluglibrary.com](https://sluglibrary.com/)
- **Patented Algorithm** - Cannot be freely implemented
- Professional standard for VR/3D applications

### Relevance to FF7 Modding

**LOW RELEVANCE** - Despite excellent quality:
- Commercial licensing incompatible with open-source modding
- Patent restrictions prevent custom implementation
- Overkill for 2D game text rendering
- Integration complexity with FFNx would be significant

### Sources

- [Slug Library Official](https://sluglibrary.com/)
- [GPU Font Rendering State of the Art (PDF)](https://www.terathon.com/font_rendering_sota_lengyel.pdf)
- [Sluggish - Open source toy implementation](https://github.com/mightycow/Sluggish)

---

## 3. Pathfinder (Mozilla/Servo)

### Technical Overview

Pathfinder 3 is a GPU-based rasterizer for fonts and vector graphics developed as part of Mozilla's Servo project. Written in Rust, it supports OpenGL 3.0+, OpenGL ES 3.0+, WebGL 2, and Metal.

**Key Innovation:** Computes exact fractional trapezoidal area coverage on a per-pixel basis (effectively 256xAA) while maintaining high performance through occlusion culling.

### How It Works

1. Parses font files and extracts glyph outlines
2. Converts paths to GPU-friendly representation
3. Uses occlusion culling to minimize overdraw
4. Computes coverage per-pixel with high precision

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Excellent | Full vector precision |
| Small text readability | Excellent | Supports hinting, subpixel AA, stem darkening |
| Magnification | Excellent | Resolution independent |
| Complex glyphs (CJK) | Very Good | Handles complex SVG-like paths |

### Performance Characteristics

- **GPU Cost:** Moderate to high (more complex than MSDF)
- **Memory:** Moderate (geometry data vs texture atlas)
- **Preprocessing:** Some path preparation required
- **Runtime:** Good, especially at large sizes where it excels

### Availability/Licensing

- **Apache 2.0 / MIT** - Same as Rust
- **Rust/C++ bindings** available
- [GitHub - servo/pathfinder](https://github.com/servo/pathfinder)

### Relevance to FF7 Modding

**LOW-MEDIUM RELEVANCE**:
- Heavy dependencies (Rust ecosystem)
- Complex integration with existing C++ FFNx codebase
- Better suited for browser/application rendering
- May be overkill for fixed-resolution game text

### Sources

- [Pathfinder GitHub](https://github.com/servo/pathfinder)
- [Pathfinder Blog Post](https://pcwalton.github.io/_posts/2017-02-14-pathfinder.html)
- [A Look at Pathfinder](https://nical.github.io/posts/a-look-at-pathfinder.html)

---

## 4. DirectWrite/Direct2D

### Technical Overview

DirectWrite is Microsoft's GPU-accelerated text rendering API that runs on top of Direct2D. It shipped with Windows 7 and provides high-quality text rendering with ClearType and grayscale antialiasing.

**Key Innovation:** Device-independent resources with hardware acceleration when available, with automatic fallback to WARP software rasterizer.

### How It Works

1. DirectWrite handles text layout and glyph processing
2. Direct2D performs hardware-accelerated rendering
3. Can render to DX11 render targets or shared surfaces
4. Supports both direct rendering and texture caching approaches

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Very Good | Native Windows quality |
| Small text readability | Excellent | Full hinting, ClearType support |
| Magnification | Good | Limited by rasterization approach |
| Complex glyphs (CJK) | Excellent | Full Unicode/OpenType support |

### Performance Characteristics

- **GPU Cost:** Moderate (hardware accelerated)
- **Memory:** Variable (depends on caching strategy)
- **Preprocessing:** Can pre-render to texture for performance
- **Runtime:** Good, especially with TextLayout caching (5x speedup reported)

### Availability/Licensing

- **Windows-only** - Part of Windows SDK
- **Free** for Windows development
- Interoperates with DirectX 9/10/11/12

### Relevance to FF7 Modding

**MEDIUM RELEVANCE**:
- FFNx already uses DirectX backends (DX11/DX12)
- Native Windows API - no additional dependencies
- Could work well for dialogue/menu text
- Limitation: Windows-only (but FF7 PC is Windows)
- Integration requires careful texture management

**Recommended Approach:** Render text to texture with DirectWrite, use texture in FFNx shader pipeline.

### Sources

- [Microsoft Learn - Direct2D and DirectWrite](https://learn.microsoft.com/en-us/windows/win32/direct2d/direct2d-and-directwrite)
- [GameDev.net - Direct2D/DirectWrite with DX11](https://www.gamedev.net/forums/topic/695867-direct2ddirectwrite-with-dx11/)
- [DirectWrite Wikipedia](https://en.wikipedia.org/wiki/DirectWrite)

---

## 5. NanoVG

### Technical Overview

NanoVG is a small antialiased vector graphics rendering library for OpenGL, with an API modeled after HTML5 canvas. It's designed for UI and visualizations.

**Key Innovation:** Lightweight, simple API that handles both vector graphics and text with good antialiasing using stb_truetype or FreeType.

### How It Works

1. Uses stb_truetype (or FreeType) for font rasterization
2. Caches glyphs in texture atlas
3. Renders with GPU antialiasing options (geometry AA or MSAA)
4. Stencil buffer support for complex overlapping paths

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Good | Standard rasterization quality |
| Small text readability | Good | Depends on backend (FreeType better) |
| Magnification | Limited | Atlas-based, requires re-rasterization |
| Complex glyphs (CJK) | Good | Full Unicode support |

### Performance Characteristics

- **GPU Cost:** Low to moderate
- **Memory:** Moderate (texture atlas)
- **Preprocessing:** Glyph caching between frames
- **Runtime:** Good for UI workloads

### Extensions

**NanoVGXC** - Extended version with:
- Exact coverage antialiasing
- SDF text rendering option (4 samples per pixel)
- Summed area table method
- Continuous text scaling with single atlas

### Availability/Licensing

- **zlib License** - Very permissive
- [NanoVG GitHub](https://github.com/memononen/nanovg)
- [NanoVGXC GitHub](https://github.com/styluslabs/nanovgXC)
- Backends: OpenGL 2.0/ES 2.0/3.2, D3D port available

### Relevance to FF7 Modding

**MEDIUM RELEVANCE**:
- Lightweight and easy to integrate
- OpenGL backend compatible with FFNx
- NanoVGXC SDF option could be useful
- Simple API good for prototyping
- Not specifically optimized for game text rendering

### Sources

- [NanoVG GitHub](https://github.com/memononen/nanovg)
- [NanoVGXC README](https://github.com/styluslabs/nanovgXC/blob/master/README.md)

---

## 6. Loop-Blinn GPU Vector Rendering

### Technical Overview

The Loop-Blinn technique (2005) is a foundational method for resolution-independent rendering of vector graphics on GPUs. It renders Bezier curves by rasterizing the convex hull of control points and using a pixel shader to determine inclusion.

**Key Innovation:** Implicitization - transforming parametric curves to implicit form for efficient GPU evaluation.

### How It Works

1. Render convex hull of Bezier control points as triangles
2. Pixel shader evaluates implicit curve equation
3. For quadratic: pixel inside if `(s/2 + t)^2 < t` (barycentric coordinates)
4. Hardware interpolation handles coordinate computation efficiently

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Excellent | Mathematically exact curves |
| Small text readability | Good | No hinting support |
| Magnification | Excellent | True resolution independence |
| Complex glyphs (CJK) | Good | Works with TrueType quadratics |

### Performance Characteristics

- **GPU Cost:** Moderate (per-pixel curve evaluation)
- **Memory:** Very low (just control points)
- **Preprocessing:** Minimal
- **Runtime:** Good, excellent at large sizes

### Modern Improvements

**AMD Mesh Shaders:** Modern implementation using mesh shaders improves:
- Eliminates vertex duplication
- Single draw call per string
- Uses `SV_BARYCENTRICS` instead of stored coordinates
- Significantly reduces API overhead

### Availability/Licensing

- **Public domain technique** - Original paper freely available
- Various open-source implementations
- [NVIDIA GPU Gems 3 Chapter 25](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-25-rendering-vector-art-gpu)
- [lbfont - C implementation](https://github.com/hansent/lbfont)

### Relevance to FF7 Modding

**MEDIUM RELEVANCE**:
- No licensing issues
- Resolution independent
- Requires significant shader work
- Modern mesh shader version not available on older GPUs
- Could be combined with MSDF for hybrid approach

### Sources

- [GPU Gems 3 Chapter 25](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-25-rendering-vector-art-gpu)
- [AMD GPUOpen - Mesh Shader Font Rendering](https://gpuopen.com/learn/mesh_shaders/mesh_shaders-font_and_vector_art_rendering_with_mesh_shaders/)
- [lbfont GitHub](https://github.com/hansent/lbfont)

---

## 7. Direct Bezier GPU Rendering

### Technical Overview

Modern direct Bezier rendering approaches store glyph curves in a grid-based structure and evaluate coverage in pixel shaders, without distance fields or pre-rasterization.

### Notable Implementations

**Will Dobbie's Vector Textures:**
- Divides glyph area into grid cells
- Stores curves that intersect each cell
- Pixel shader evaluates winding number via ray-curve intersections

**GreenLightning GPU Font Rendering:**
- Converts contours to quadratic Bezier list
- Uploads control points to GPU
- Single quad per glyph with winding number calculation

**osor.io Crispy Text:**
- Converts all curves to quadratics
- Runtime rasterization on GPU
- Supports subpixel antialiasing

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Excellent | True vector precision |
| Small text readability | Good-Excellent | Depends on implementation |
| Magnification | Excellent | Resolution independent |
| Complex glyphs (CJK) | Excellent | No corner problems |

### Performance Characteristics

- **GPU Cost:** Higher than MSDF (curve evaluation per pixel)
- **Memory:** Low (curve data only, no textures)
- **Preprocessing:** Glyph processing but no atlas generation
- **Runtime:** Good, but more GPU-bound than texture methods

### Availability/Licensing

- Various MIT/Apache licensed implementations
- [gpu-font-rendering GitHub](https://github.com/GreenLightning/gpu-font-rendering)
- [Will Dobbie's Article](https://wdobbie.com/post/gpu-text-rendering-with-vector-textures/)
- [osor.io Implementation](https://osor.io/text)

### Relevance to FF7 Modding

**MEDIUM RELEVANCE**:
- Excellent quality potential
- No preprocessing/atlas management
- Higher GPU cost may be acceptable for dialogue text
- More complex shader implementation required
- Good for future consideration as GPU power increases

### Sources

- [GPU Text Rendering with Vector Textures](https://wdobbie.com/post/gpu-text-rendering-with-vector-textures/)
- [Rendering Crispy Text on GPU](https://osor.io/text)
- [GreenLightning Demo](https://github.com/GreenLightning/gpu-font-rendering)

---

## 8. stb_truetype with GPU Atlas

### Technical Overview

stb_truetype is a single-header C library for TrueType font processing. The standard GPU workflow involves CPU rasterization to a texture atlas, then GPU rendering of textured quads.

**Key Innovation:** Simple, dependency-free font loading and rasterization with optional SDF generation.

### How It Works

1. Load font with stb_truetype
2. Rasterize glyphs to bitmap (8-bit monochrome)
3. Pack into texture atlas
4. Upload atlas to GPU
5. Render text as textured quads

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Good | Standard rasterization |
| Small text readability | Good | No hinting support |
| Magnification | Limited | Requires re-rasterization or SDF mode |
| Complex glyphs (CJK) | Good | Full TrueType support |

### SDF Mode

stb_truetype can generate SDF representations:
- Enables resolution-independent scaling
- Supports effects (shadows, outlines, glow)
- Single atlas works across text sizes
- Ideal for games with varying text scales

### Performance Characteristics

- **GPU Cost:** Very low (simple texture sampling)
- **Memory:** Moderate (atlas texture)
- **Preprocessing:** CPU rasterization (can be slow)
- **Runtime:** Excellent

### Availability/Licensing

- **Public Domain / MIT** - [stb GitHub](https://github.com/nothings/stb)
- Single header, no dependencies
- Used by many game engines

### Relevance to FF7 Modding

**HIGH RELEVANCE**:
- Already commonly used in game development
- Simple integration
- SDF mode provides good scaling
- Low runtime overhead
- Good documentation and examples
- Compatible with FFNx architecture

### Sources

- [stb GitHub](https://github.com/nothings/stb)
- [LearnOpenGL Text Rendering](https://learnopengl.com/In-Practice/Text-Rendering)
- [stb_truetype DeepWiki](https://deepwiki.com/nothings/stb/3.1-truetype-font-processing-(stb_truetype))

---

## 9. FreeType with GPU Acceleration

### Technical Overview

FreeType is the industry-standard font rasterization library. GPU acceleration approaches either use FreeType for CPU rasterization with GPU atlas caching, or extract outlines for direct GPU rendering.

### Approaches

**Traditional (CPU raster + GPU cache):**
1. FreeType rasterizes glyphs with full hinting
2. Cache in GPU texture atlas
3. GPU renders textured quads

**freetype-direct-gl:**
- Uses FreeType outline data directly
- GPU renders from glyph outlines
- No bitmap intermediate step

### Quality Characteristics

| Aspect | Rating | Notes |
|--------|--------|-------|
| Sharp corners | Very Good | Full hinting support |
| Small text readability | Excellent | Best-in-class hinting |
| Magnification | Limited/Good | Depends on approach |
| Complex glyphs (CJK) | Excellent | Industry standard |

### Performance Characteristics

- **GPU Cost:** Low (atlas) to Moderate (direct)
- **Memory:** Moderate (atlas approach)
- **Preprocessing:** Good with caching
- **Runtime:** Excellent with proper caching

### Availability/Licensing

- **FreeType License** (BSD-like) or **GPL**
- Industry standard, very mature
- [FreeType.org](https://freetype.org/)
- [freetype-direct-gl](https://github.com/stonewell/freetype-direct-gl)

### Relevance to FF7 Modding

**MEDIUM-HIGH RELEVANCE**:
- Excellent CJK support
- Full hinting for small text
- More complex than stb_truetype
- May be overkill if MSDF already works well
- Good fallback option if quality issues arise

### Sources

- [FreeType Project](https://freetype.org/)
- [freetype-direct-gl GitHub](https://github.com/stonewell/freetype-direct-gl)

---

## 10. Comparative Analysis

### Quality Comparison

| Approach | Corners | Small Text | Scaling | CJK Support | Overall Quality |
|----------|---------|------------|---------|-------------|-----------------|
| MSDF | Excellent | Very Good | Excellent | Good | **A** |
| Slug | Perfect | Excellent | Perfect | Excellent | **A+** |
| Pathfinder | Excellent | Excellent | Excellent | Very Good | **A** |
| DirectWrite | Very Good | Excellent | Good | Excellent | **A-** |
| NanoVG | Good | Good | Limited | Good | **B+** |
| Loop-Blinn | Excellent | Good | Excellent | Good | **A-** |
| Direct Bezier | Excellent | Good-Excellent | Excellent | Excellent | **A** |
| stb_truetype+SDF | Good | Good | Good | Good | **B+** |
| FreeType+Atlas | Very Good | Excellent | Limited | Excellent | **A-** |

### Performance Comparison

| Approach | GPU Cost | Memory | Preprocessing | Runtime | Overall Perf |
|----------|----------|--------|---------------|---------|--------------|
| MSDF | Low | Low | Moderate | Excellent | **A** |
| Slug | Moderate | Very Low | None | Good | **B+** |
| Pathfinder | Moderate-High | Moderate | Some | Good | **B** |
| DirectWrite | Moderate | Variable | Optional | Good | **B+** |
| NanoVG | Low-Moderate | Moderate | Low | Good | **B+** |
| Loop-Blinn | Moderate | Very Low | Minimal | Good | **B+** |
| Direct Bezier | High | Low | Low | Good | **B** |
| stb_truetype+SDF | Very Low | Moderate | Low | Excellent | **A** |
| FreeType+Atlas | Very Low | Moderate | Moderate | Excellent | **A-** |

### Integration Complexity (for FFNx)

| Approach | Dependencies | Shader Changes | Build Complexity | Overall |
|----------|--------------|----------------|------------------|---------|
| MSDF | Low (tools only) | Minimal | Low | **Easy** |
| Slug | Commercial | Moderate | High | **Hard** |
| Pathfinder | High (Rust) | Significant | High | **Hard** |
| DirectWrite | Windows SDK | Moderate | Moderate | **Medium** |
| NanoVG | Low | Moderate | Low | **Easy** |
| Loop-Blinn | None | Significant | Low | **Medium** |
| Direct Bezier | Low | Significant | Low | **Medium** |
| stb_truetype | None | Minimal | Very Low | **Easy** |
| FreeType | Moderate | Minimal | Moderate | **Medium** |

---

## 11. Recommendations for FF7 Context

### Primary Recommendation: Enhanced MSDF

**Rationale:** MSDF is already partially implemented and provides the best balance of quality, performance, and integration simplicity for the FF7 modding context.

**Recommended Improvements:**
1. Optimize atlas generation for Japanese character sets
2. Implement proper `pxrange` handling in shaders
3. Add outline/shadow effects using MSDF techniques
4. Consider split atlases (Latin + CJK) for memory efficiency

### Secondary Recommendation: stb_truetype with SDF

**Rationale:** If MSDF proves problematic for specific use cases, stb_truetype offers:
- Simpler toolchain
- Good documentation
- Public domain licensing
- Easy integration

### Future Consideration: Direct Bezier Rendering

**Rationale:** As GPU capabilities increase and FFNx evolves, direct Bezier rendering could provide:
- Perfect quality at any scale
- No atlas management
- Cleaner code architecture

### Not Recommended for FF7

| Approach | Reason |
|----------|--------|
| Slug | Commercial/patented - incompatible with open source modding |
| Pathfinder | Too complex, Rust dependencies, overkill for this use case |
| DirectWrite | Windows-only limitation acceptable, but integration overhead high |

### Implementation Priority

1. **Immediate:** Optimize current MSDF implementation
2. **Short-term:** Validate stb_truetype+SDF as fallback
3. **Medium-term:** Investigate NanoVGXC SDF features
4. **Long-term:** Monitor direct Bezier techniques for future versions

---

## Appendix: FFNx-Specific Considerations

### Current FFNx Architecture

- Supports DirectX 11 (default), DirectX 12, Vulkan, OpenGL backends
- Uses shader-based rendering
- Supports DDS textures up to BC7 compression
- Has existing texture modding infrastructure

### Integration Points

1. **Shader Pipeline:** Any new approach must integrate with FFNx HLSL/GLSL shaders
2. **Texture System:** Atlas-based approaches can use existing DDS pipeline
3. **Memory Budget:** Retro game modding should remain lightweight
4. **Compatibility:** Must work with FFNx minimum GPU requirements (OpenGL 3.0 / DX11)

### Recommended Testing Matrix

| Test Case | MSDF | stb+SDF | NanoVG |
|-----------|------|---------|--------|
| Japanese dialogue (small) | Test | Test | Test |
| Japanese dialogue (large) | Test | Test | Test |
| Menu text | Test | Test | Test |
| Battle text | Test | Test | Test |
| 3D world labels | Test | Test | Test |
| Performance (1080p) | Test | Test | Test |
| Performance (4K) | Test | Test | Test |

---

## References

### Primary Sources

- [msdfgen GitHub](https://github.com/Chlumsky/msdfgen)
- [Slug Library](https://sluglibrary.com/)
- [Pathfinder GitHub](https://github.com/servo/pathfinder)
- [NVIDIA GPU Gems 3](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-25-rendering-vector-art-gpu)
- [AMD GPUOpen Mesh Shaders](https://gpuopen.com/learn/mesh_shaders/mesh_shaders-font_and_vector_art_rendering_with_mesh_shaders/)

### Academic Papers

- Loop, C. & Blinn, J. (2005). "Resolution Independent Curve Rendering Using Programmable Graphics Hardware"
- Green, C. (2007). "Improved Alpha-Tested Magnification for Vector Textures and Special Effects" (Valve/SIGGRAPH)
- Lengyel, E. "GPU Font Rendering: Current State of the Art" - [PDF](https://www.terathon.com/font_rendering_sota_lengyel.pdf)

### Implementation Examples

- [GreenLightning gpu-font-rendering](https://github.com/GreenLightning/gpu-font-rendering)
- [Will Dobbie Vector Textures](https://wdobbie.com/post/gpu-text-rendering-with-vector-textures/)
- [osor.io Crispy Text](https://osor.io/text)
- [awesome-msdf](https://github.com/Blatko1/awesome-msdf)

### FFNx Resources

- [FFNx GitHub](https://github.com/julianxhokaxhiu/FFNx)
- [Julian Xhokaxhiu Blog - FF7 on Vulkan](https://blog.julianxhokaxhiu.com/2020-02-19-final-fantasy-vii-running-on-vulkan/)

---

*End of Research Report*

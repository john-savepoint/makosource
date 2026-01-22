# FF7 Background AI Enhancement Tool - Complete Planning Session

**Date**: 2026-01-16 14:20 JST (Thursday)
**Session ID**: 08728220-dada-49cd-b025-6d86a2bbd0c5
**Duration**: Extended planning session
**Project**: FF7 Background AI Enhancement Pipeline
**Status**: Planning Complete - Ready for Implementation

---

## Executive Summary

This session developed a comprehensive plan for a Python CLI tool (`ff7_bg_tool`) that enables AI-enhanced background replacement for Final Fantasy VII (1998) using modern AI image generators (NanoBanana Pro) and video generators (VEO3). The tool handles the complete pipeline from extraction through reimport, leveraging the FFNx mod driver's texture replacement system.

### Key Discovery

**FFNx uses whole-layer texture replacement, NOT tile-by-tile reconstruction.** This dramatically simplifies the workflow - AI generates single images per layer (1024x1024 DDS), eliminating the need to reconstruct 16x16 tile mosaics.

---

## Project Goals

### Primary Objective
Create a tool that:
1. **Extracts** FF7 field backgrounds with layer separation and walkmesh overlays
2. **Packages** data for AI image generation with structure locking
3. **Converts** AI output back to FFNx-compatible DDS format
4. **Supports** both static backgrounds (NanoBanana Pro) and animated backgrounds (VEO3)

### Use Cases
- **Faithful HD Remaster**: Upscale backgrounds to 4K while preserving original aesthetic
- **Artistic Reimagining**: Creative reinterpretation with location/story context
- **Animated Enhancement**: Replace existing animations with AI-generated video frames

---

## Technical Architecture

### How FF7 Backgrounds Work

#### Original Game (1998)
```
Background Storage: 16x16 pixel tile mosaic
- Layer 0: Base background (characters walk in front)
- Layer 1+: Foreground elements (characters walk behind)
- Walkmesh: 3D triangle mesh defining walkable areas
- Camera: 3D-to-2D projection matrix for rendering
```

#### FFNx Mod System (Modern)
```
Texture Replacement Path:
field/{fieldname}/{fieldname}_{layerID}_00.dds

Example:
- md1stin_00_00.dds (Layer 0 - base)
- md1stin_01_00.dds (Layer 1 - foreground)

Format: DDS BC7, 1024x1024, sRGB color space
```

**Critical Insight**: FFNx intercepts texture loading at runtime. No modification to original game files required.

---

## The Complete Pipeline

### Phase A: Extraction

**Input**: `FLEVEL.LGP` (128MB archive containing ~760 field files)

**Process**:
1. Parse LGP archive format
2. Extract individual field DAT files
3. Parse field sections:
   - Section 2: Camera matrix (for walkmesh projection)
   - Section 5: Walkmesh triangles + access flags
   - Section 8: Palettes (256-color)
   - Section 9: Background tiles + textures

**Output** (per field):
```
output/{fieldname}/
├── layer_0_base.png           # Base background
├── layer_1_foreground.png     # Foreground elements
├── walkmesh_wireframe.png     # Reference overlay
├── walkmesh_filled_mask.png   # White = walkable (for AI locking)
├── metadata.json              # Layer info, camera params
└── nanobanana_package/
    ├── input.png              # High-res source (from Cosmos mod)
    ├── structure_mask.png     # Combined lock mask
    └── reference_layers/      # Individual layers
```

### Phase B: AI Generation (Dual-Mode)

#### Mode 1: Faithful HD Remaster
```
Input: Source image + walkmesh mask
Prompt Template:
"Upscale this Final Fantasy VII pre-rendered background to 4K.
 Enhance textures, improve lighting, add subtle detail.
 Preserve the original composition and atmosphere exactly.
 Structure mask provided - do not alter walkable pathway geometry."

Output: field_faithful/{fieldname}_layer_X.png
```

#### Mode 2: Artistic Reimagining
```
Input: Source image + walkmesh mask + location context
Prompt Template:
"Reimagine this scene from Final Fantasy VII.
 Location: {location_name} - {location_description}
 Game Context: {story_context}
 Style: Modern cinematic rendering with dramatic lighting.
 Creative freedom: High - reinterpret architecture and environment.
 CONSTRAINT: The highlighted walkable areas (white mask) must remain
 structurally navigable - these paths cannot be blocked or altered."

Output: field_artistic/{fieldname}_layer_X.png
```

**Metadata Database**: `field_metadata.json` with ~760 fields containing:
- Human-readable location name
- Area description
- Story context (chapter/point in game)
- Atmosphere keywords (industrial, nature, urban, etc.)

Example entry:
```json
{
  "md1stin": {
    "name": "Sector 1 Station - Train Platform",
    "area": "Midgar - Sector 1",
    "description": "Industrial train station platform where Cloud jumps off the train at the game's opening. Dark, grimy, metal infrastructure with steam and industrial lighting.",
    "story_context": "Opening scene - AVALANCHE's first bombing mission",
    "atmosphere": "industrial, dark, tense, urban decay"
  }
}
```

### Phase C: Conversion

**Process**:
1. Load AI-generated PNG files
2. Convert to DDS BC7 format (1024x1024)
3. Apply FFNx naming convention: `{fieldname}_{layerID}_00.dds`
4. Create mod folder structure

**Output**:
```
mods/ff7_ai_backgrounds/field/{fieldname}/
├── {fieldname}_00_00.dds  # Layer 0
├── {fieldname}_01_00.dds  # Layer 1
└── ...
```

**DDS Conversion**: Use Microsoft's `texconv` tool for best compatibility:
```bash
texconv -f BC7_UNORM_SRGB -y -o output_dir input.png
```

### Phase D: Game Integration

**FFNx Configuration**:
```toml
[mod]
mod_path = "mods/ff7_ai_backgrounds"
```

FFNx automatically loads replacement textures when the game requests them. No original file modification required.

---

## Animated Backgrounds (VEO3 Integration)

### How FFNx Animated Textures Work

FF7's original engine animates backgrounds via **palette cycling** controlled by field scripts. FFNx intercepts this and creates **unique hashes** for each animation frame state.

**File Naming**:
```
{fieldname}_{layerID}_{paletteID}_{xxhash}.dds

Example: ancnt1_15_14_1af9089f97729eee.dds
         └─field ─┘ │  │  └─unique frame hash─┘
                    │  └─palette variant
                    └─layer ID
```

### Animation Workflow

#### Step 1: Extract Animation Hashes
```
Method A: From Cosmos Mod
- Cosmos Limit Break AA folder contains pre-extracted hashes
- Example: eals_1 (Aerith's house) has ~172 animation frames

Method B: In-Game Dumping
1. Enable save_textures = yes in FFNx.toml
2. Play through field in-game
3. FFNx dumps all unique frames with hashes
4. Disable save_textures = no
```

#### Step 2: Generate AI Video
```
VEO3 Input:
- Source frame (one of the dumped hashes)
- Walkmesh mask (structure lock)
- Animation description: "Gentle waterfall flowing, light dappling"
- Duration: Match original animation length

Output: Enhanced video (e.g., waterfall.mp4)
```

#### Step 3: Convert Video to Hash Frames
```
Process:
1. Split video into frames matching hash count
2. Map frames to corresponding animation hashes
3. Convert each frame to DDS with correct hash filename
4. FFNx loads your animated frames instead of originals
```

### Animation-Capable Fields (Partial List)
- `eals_1` - Aerith's house (waterfall, light)
- `ancnt*` - Ancient Forest (vegetation)
- `cosmo*` - Cosmo Canyon (fire, stars)
- `blin*` - Various Midgar scenes (lights, machinery)

**Current Limitation**: FFNx's hash system is tied to original game's palette cycling. Truly new animations (e.g., adding grass motion where none existed) would require FFNx modification or synthetic palette cycle creation.

---

## Data Sources

### Original Game Data
```
Path: C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\field\flevel_en.lgp
Size: 128MB
Contents: ~760 field files
Purpose: Walkmesh, camera, layer data
Note: EN/JP versions have identical walkmesh/camera data
```

### Cosmos Limit Break Mod
```
Path: H:\ff7 backgrounds\LIMIT BREAK\field\
Format: 1024x1024 DDS textures (4x original)
Purpose: High-resolution source images for AI input
Structure: field/{fieldname}/{fieldname}_XX_00.dds
```

### Cosmos Animated Textures
```
Path: H:\ff7 backgrounds\LIMIT BREAK AA\field\
Contents: Hashed animation frames
Example: ancnt1/ contains 20+ DDS files per animation
Purpose: Animation frame hash reference
```

---

## Walkmesh Projection Mathematics

### The Challenge
Walkmesh exists in 3D space, backgrounds are 2D images. Must project 3D triangles onto 2D plane using camera matrix.

### Camera Data Structure (Section 2)
```c
struct Camera {
    Vertex_s camera_axis[3];      // 3x3 rotation matrix
    qint16 camera_axis2z;          // Padding
    qint32 camera_position[3];     // Camera position in 3D
    qint32 blank;
    quint16 camera_zoom;           // FOV calculation
    quint16 unknown;
};
```

### Projection Algorithm (from WalkmeshWidget.cpp)
```python
# Scale factor (FF7 uses fixed-point scaled by 4096)
SCALE = 4096.0

# Calculate field of view
fovy = (2 * atan(240.0 / (2.0 * camera_zoom))) * 57.29577951

# Camera axes (3x3 rotation matrix)
cam_axis = [
    [c / SCALE for c in camera.axis[0]],
    [-c / SCALE for c in camera.axis[1]],  # Y inverted
    [c / SCALE for c in camera.axis[2]]
]

# Camera position
cam_pos = [
    camera.position[0] / SCALE,
    -camera.position[1] / SCALE,  # Y inverted
    camera.position[2] / SCALE
]

# Transform to view space
tx = -(cam_pos[0] * cam_axis[0][0] + cam_pos[1] * cam_axis[1][0] + cam_pos[2] * cam_axis[2][0])
ty = -(cam_pos[0] * cam_axis[0][1] + cam_pos[1] * cam_axis[1][1] + cam_pos[2] * cam_axis[2][1])
tz = -(cam_pos[0] * cam_axis[0][2] + cam_pos[1] * cam_axis[1][2] + cam_pos[2] * cam_axis[2][2])

# Build view matrix
eye = QVector3D(tx, ty, tz)
center = QVector3D(tx + cam_axis[2][0], ty + cam_axis[2][1], tz + cam_axis[2][2])
up = QVector3D(cam_axis[1][0], cam_axis[1][1], cam_axis[1][2])

# Apply perspective projection
projection_matrix = perspective(fovy, aspect_ratio, 0.001, 1000.0)
view_matrix = lookAt(eye, center, up)

# For each walkmesh triangle vertex:
#   screen_position = projection_matrix * view_matrix * vertex_position
```

### Walkmesh Structure (Section 5)
```python
class Triangle:
    vertices: List[Tuple[int, int, int]]  # 3 vertices (x, y, z)

class Access:
    a: List[int]  # Edge accessibility
    # -1 (0xFFFF) = wall/impassable
    # Valid ID = connected triangle
```

### Output Masks
1. **Wireframe**: Lines colored by accessibility
   - White = walkable edge
   - Blue = wall/blocked

2. **Filled**: Solid polygons
   - White = walkable triangles (for AI structure locking)
   - Transparent = non-walkable areas

---

## CLI Interface Design

### Extract Commands
```bash
# Extract single field
python -m ff7_bg_tool extract --field md1stin \
    --flevel "/path/to/flevel_en.lgp" \
    --output ./extraction

# Extract with Cosmos high-res source
python -m ff7_bg_tool extract --field md1stin \
    --flevel "/path/to/flevel_en.lgp" \
    --cosmos "/mnt/h/ff7 backgrounds/LIMIT BREAK" \
    --output ./extraction

# Batch extract all fields
python -m ff7_bg_tool extract --all \
    --flevel "/path/to/flevel_en.lgp" \
    --output ./extraction

# Customize walkmesh colors
python -m ff7_bg_tool extract --field md1stin \
    --walkmesh-color "#FFFFFF" \
    --wall-color "#FF0000" \
    --output ./extraction
```

### Prompt Generation Commands
```bash
# Generate AI prompt (faithful mode)
python -m ff7_bg_tool prompt --field md1stin \
    --mode faithful \
    --output ./prompts/md1stin_faithful.txt

# Generate AI prompt (artistic mode)
python -m ff7_bg_tool prompt --field md1stin \
    --mode artistic \
    --output ./prompts/md1stin_artistic.txt

# Batch generate prompts for all extracted fields
python -m ff7_bg_tool prompt-batch \
    --input ./extraction \
    --modes both \
    --output ./prompts
```

### Conversion Commands
```bash
# Convert single AI output to FFNx format
python -m ff7_bg_tool convert --field md1stin \
    --input ./ai_output/md1stin_enhanced.png \
    --layer 0 \
    --output ./mods/ff7_ai_backgrounds

# Batch convert entire AI output folder
python -m ff7_bg_tool convert-batch \
    --input ./ai_output \
    --output ./mods/ff7_ai_backgrounds

# Package complete mod structure
python -m ff7_bg_tool package \
    --input ./converted_fields \
    --output ./ff7_ai_backgrounds_mod
```

### Animation Commands
```bash
# List all animated fields
python -m ff7_bg_tool list-animated \
    --cosmos "/mnt/h/ff7 backgrounds/LIMIT BREAK AA"

# Extract hash mapping for a field's animations
python -m ff7_bg_tool extract-hashes --field eals_1 \
    --cosmos-aa "/mnt/h/ff7 backgrounds/LIMIT BREAK AA" \
    --output ./hashes/eals_1.json

# Generate video prompt for VEO3
python -m ff7_bg_tool video-prompt --field eals_1 \
    --mode artistic \
    --output ./prompts/eals_1_video.txt

# Convert video to animation frames
python -m ff7_bg_tool video-to-frames \
    --video ./veo3_output/eals_1.mp4 \
    --hash-mapping ./hashes/eals_1.json \
    --fps auto \
    --output ./mods/field/eals_1/
```

---

## Implementation Structure

### Project Layout
```
ff7_bg_tool/
├── __init__.py
├── __main__.py               # CLI entry point
├── cli.py                    # Click commands (extract, convert, prompt, package)
│
├── extract/
│   ├── lgp_archive.py        # FLEVEL.LGP parser
│   ├── field_parser.py       # DAT section parser (Sections 2, 5, 8, 9)
│   ├── background.py         # Layer rendering (tile assembly + palette)
│   ├── walkmesh.py           # Walkmesh projection + mask generation
│   └── cosmos_loader.py      # High-res DDS loader (optional)
│
├── prompt/
│   ├── generator.py          # Prompt generation for both modes
│   ├── templates.py          # Faithful vs Artistic prompt templates
│   └── field_metadata.json   # ~760 fields with location/story context
│
├── convert/
│   ├── dds_encoder.py        # PNG → DDS BC7 conversion
│   ├── layer_mapper.py       # Map layers to FFNx naming
│   └── mod_packager.py       # Create mod.xml structure
│
└── utils/
    ├── binary.py             # Binary read helpers
    └── palette.py            # 16-bit color conversion
```

### Dependencies
```python
pillow          # Image processing
numpy           # Array operations
struct          # Binary parsing (built-in)
click           # CLI framework
imageio         # DDS loading (for Cosmos mod)
```

### Implementation Order
1. **LGP Archive Parser** - Extract field DAT files from FLEVEL.LGP
2. **Field DAT Section Parser** - Parse Sections 2 (Camera), 5 (Walkmesh), 9 (Background)
3. **Background Tile Renderer** - Reconstruct layers from tiles + palettes
4. **Walkmesh Projector** - 3D→2D projection + mask generation
5. **Prompt Generator** - Create AI prompts with metadata database
6. **DDS Converter** - PNG → DDS BC7 for FFNx
7. **CLI Interface** - Click-based command system
8. **Test with md1stin** - Opening train station (iconic location)

---

## Key Technical Discoveries

### Discovery 1: Whole-Layer Texture Replacement
**Finding**: FFNx uses single images per layer, NOT tile-by-tile reconstruction.

**Evidence**: Cosmos Limit Break mod structure shows 1024x1024 DDS files per layer.

**Impact**: Dramatically simplifies workflow - AI generates one image per layer, convert to DDS, done.

### Discovery 2: Walkmesh Projection is Documented
**Finding**: Makoureactor's `WalkmeshWidget.cpp` contains complete projection math.

**Details**:
- Uses camera matrix from Section 2
- Applies perspective transformation
- Projects 3D triangles to 2D screen coordinates

**Impact**: No need to reverse-engineer projection - can directly implement proven algorithm.

### Discovery 3: Animation via Hash System
**Finding**: FFNx creates unique xxhash for each animation frame state.

**Mechanism**:
- Original game: palette cycling
- FFNx: hash each unique rendered frame
- Mods: provide DDS replacements with hash filenames

**Impact**: VEO3 workflow requires frame splitting + hash mapping, not direct video replacement.

### Discovery 4: Cosmos Mod Provides High-Res Source
**Finding**: Existing mod already has 1024x1024 upscaled backgrounds.

**Benefit**: Can use as input to AI instead of upscaling from 320x240 originals.

**Tradeoff**: Cosmos uses their upscaling method; we replace with AI-enhanced versions.

---

## Makoureactor Reference

The `makoureactor` project at `/home/johnzealanddoyle/projects/tools/makoureactor` provides critical reference implementations:

### Key Files Analyzed

| File | Purpose | Key Functions |
|------|---------|---------------|
| `src/core/field/BackgroundFile.cpp` | Background rendering | `drawBackground()`, `exportLayers()` |
| `src/core/field/IdFile.cpp` | Walkmesh storage | `triangles()`, `access()` |
| `src/core/field/CaFile.cpp` | Camera matrix | `camera()` structure |
| `src/3d/WalkmeshWidget.cpp` | Walkmesh visualization | `paintGL()`, projection math |
| `src/core/field/BackgroundTiles.h` | Tile data structures | Layer filtering, z-ordering |
| `src/core/field/Palette.cpp` | Color palettes | 16-bit to RGB conversion |

### Data Structures Documented
```cpp
// Walkmesh
struct Triangle {
    Vertex_sr vertices[3];  // 3 vertices per triangle
};

struct Vertex_sr {
    qint16 x, y, z, res;    // Fixed-point coordinates (scale: 4096)
};

struct Access {
    qint16 a[3];            // Edge accessibility flags
};

// Camera
struct Camera {
    Vertex_s camera_axis[3];      // 3x3 rotation matrix
    qint32 camera_position[3];     // Position in 3D space
    quint16 camera_zoom;           // FOV calculation
};

// Background
struct Tile {
    qint16 dstX, dstY;      // Destination coordinates
    qint16 srcX, srcY;      // Source texture coordinates
    quint8 textureID;       // Which texture page
    quint8 paletteID;       // Palette reference
    quint8 layerID;         // Layer assignment (0-3)
    // ... additional fields
};
```

---

## Resource References

### Documentation Sources
- [FFNx GitHub](https://github.com/julianxhokaxhiu/FFNx) - Modding platform documentation
- [FFNx Animated Textures Issue #27](https://github.com/julianxhokaxhiu/FFNx/issues/27) - Hash system technical details
- [Aeris Tool](https://github.com/LaZar00/Aeris) - Background editing reference implementation
- [FF7 Field Background Wiki](https://qhimm-modding.fandom.com/wiki/FF7/Field/Background) - Format specifications
- [FF7 HD Field Scenes Database](https://finalfantasy.german-syslinux-blog.de/FF7/) - Field name to location mapping
- [FF7 Wiki Locations](https://finalfantasy.fandom.com/wiki/Final_Fantasy_VII_locations) - Story context and descriptions

### Existing Tools
- **Makoureactor**: C++/Qt field editor (provides reference implementation)
- **Aeris**: FF7 background editing tool (handles animation hashes)
- **Cosmos Limit Break**: Professional upscaling mod (provides high-res sources)

---

## Field Metadata Database Strategy

### Data Collection Approach
1. **Primary Source**: FF7 HD Field Scenes Database (field name → location mapping)
2. **Secondary Source**: FF7 Wiki (location descriptions, story context)
3. **Manual Curation**: Atmosphere keywords, scene descriptions

### Database Schema
```json
{
  "field_internal_name": {
    "name": "Human-Readable Location Name",
    "area": "Region - Specific Area",
    "description": "Detailed scene description (1-2 sentences)",
    "story": "Story context / chapter reference",
    "atmosphere": "keyword1, keyword2, keyword3"
  }
}
```

### Sample Entries
```json
{
  "md1stin": {
    "name": "Sector 1 Station",
    "area": "Midgar - Sector 1",
    "description": "Industrial train platform, opening scene",
    "story": "AVALANCHE bombing mission begins",
    "atmosphere": "industrial, dark, tense"
  },
  "church": {
    "name": "Sector 5 Church",
    "area": "Midgar - Sector 5 Slums",
    "description": "Abandoned church with flower garden, where Cloud meets Aerith",
    "story": "Cloud falls through roof, meets Aerith",
    "atmosphere": "peaceful, spiritual, flowers, light rays"
  },
  "cosmo": {
    "name": "Cosmo Canyon",
    "area": "Western Continent",
    "description": "Red rock canyon village, home of Red XIII",
    "story": "Red XIII's hometown, Bugenhagen's observatory",
    "atmosphere": "mystical, ancient, natural, stargazing"
  },
  "eals_1": {
    "name": "Aerith's House",
    "area": "Midgar - Sector 5 Slums",
    "description": "Interior of Aerith's home with waterfall feature",
    "story": "Cloud recovers, learns about Aerith's background",
    "atmosphere": "peaceful, water sounds, natural light"
  }
}
```

### Incremental Population Strategy
- Start with key story locations (~50 fields)
- Expand to major areas (~200 fields)
- Complete coverage over time (~760 fields)
- Allow user contributions/corrections

---

## Workflow Examples

### Example 1: Faithful HD Remaster of Opening Scene

**Step 1: Extract**
```bash
python -m ff7_bg_tool extract --field md1stin \
    --flevel "C:/Program Files (x86)/Steam/.../flevel_en.lgp" \
    --cosmos "H:/ff7 backgrounds/LIMIT BREAK" \
    --output ./extraction/md1stin
```

**Step 2: Generate Prompt**
```bash
python -m ff7_bg_tool prompt --field md1stin \
    --mode faithful \
    --output ./prompts/md1stin_faithful.txt
```

**Step 3: AI Generation** (NanoBanana Pro)
```
Input: extraction/md1stin/nanobanana_package/input.png
Mask: extraction/md1stin/nanobanana_package/structure_mask.png
Prompt: [contents of md1stin_faithful.txt]

Output: md1stin_layer_0_enhanced.png
```

**Step 4: Convert to DDS**
```bash
python -m ff7_bg_tool convert --field md1stin \
    --input ./ai_output/md1stin_layer_0_enhanced.png \
    --layer 0 \
    --output ./mods/ff7_ai_faithful
```

**Step 5: Test in Game**
```toml
# FFNx.toml
[mod]
mod_path = "mods/ff7_ai_faithful"
```

Launch FF7, load opening scene, verify background appears correctly.

### Example 2: Artistic Reimagining with Animation

**Target**: Aerith's House (`eals_1`) with animated waterfall

**Step 1: Extract Static Background + Animation Hashes**
```bash
python -m ff7_bg_tool extract --field eals_1 \
    --flevel "C:/Program Files (x86)/Steam/.../flevel_en.lgp" \
    --output ./extraction/eals_1

python -m ff7_bg_tool extract-hashes --field eals_1 \
    --cosmos-aa "H:/ff7 backgrounds/LIMIT BREAK AA" \
    --output ./hashes/eals_1.json
```

**Step 2: Generate Prompts**
```bash
# Static background (artistic)
python -m ff7_bg_tool prompt --field eals_1 \
    --mode artistic \
    --output ./prompts/eals_1_artistic.txt

# Video (waterfall animation)
python -m ff7_bg_tool video-prompt --field eals_1 \
    --animation waterfall \
    --output ./prompts/eals_1_waterfall_video.txt
```

**Step 3: AI Generation**
```
Static (NanoBanana Pro):
- Input: extraction/eals_1/layer_0.png
- Prompt: [artistic prompt with location context]
- Output: eals_1_artistic.png

Animated (VEO3):
- Input: First frame from hash dump
- Prompt: [waterfall animation description]
- Duration: ~5 seconds (matching original)
- Output: eals_1_waterfall.mp4
```

**Step 4: Convert Both**
```bash
# Static background
python -m ff7_bg_tool convert --field eals_1 \
    --input ./ai_output/eals_1_artistic.png \
    --layer 0 \
    --output ./mods/ff7_ai_artistic

# Animated waterfall
python -m ff7_bg_tool video-to-frames \
    --video ./ai_output/eals_1_waterfall.mp4 \
    --hash-mapping ./hashes/eals_1.json \
    --fps auto \
    --output ./mods/ff7_ai_artistic/field/eals_1/
```

**Step 5: Test**
```toml
# FFNx.toml
[mod]
mod_path = "mods/ff7_ai_artistic"

[animated_textures]
enable_animated_textures = true
use_animated_textures_v2 = true
```

---

## Known Challenges & Solutions

### Challenge 1: Walkmesh Projection Accuracy
**Issue**: 3D→2D projection must be pixel-perfect to match background.

**Solution**:
- Use exact camera matrix from Section 2
- Implement proven projection math from WalkmeshWidget.cpp
- Test with known fields (compare to makoureactor's visualization)

### Challenge 2: Animation Frame Count Mismatch
**Issue**: VEO3 video may have different frame count than original animation.

**Solution**:
- Extract exact hash count from Cosmos mod or in-game dump
- Use frame interpolation/decimation to match
- Provide `--fps auto` flag to calculate matching framerate

### Challenge 3: Layer Separation Accuracy
**Issue**: FF7's layer system is complex with parameter-conditional rendering.

**Solution**:
- Focus on Layer 0 (base) and Layer 1 (foreground) first
- Document parameter system for future enhancement
- Provide layer preview tool to verify separation

### Challenge 4: Cosmos Mod Compatibility
**Issue**: Cosmos uses proprietary upscaling method; our output must integrate.

**Solution**:
- Use Cosmos as source, not target
- Generate independent mod that can coexist
- Provide merge tool for combining mods (future enhancement)

---

## Quality Assurance Strategy

### Test Fields (Priority Order)
1. **md1stin** - Sector 1 Station (iconic opening)
2. **eals_1** - Aerith's House (animation test)
3. **cosmo** - Cosmo Canyon (complex lighting)
4. **ancnt1** - Ancient Forest (vegetation animation)
5. **church** - Sector 5 Church (high-detail architecture)

### Validation Checklist (Per Field)
- [ ] Extracted layers match expected count
- [ ] Walkmesh mask covers walkable areas completely
- [ ] Camera projection aligns with background perspective
- [ ] DDS conversion maintains image quality
- [ ] FFNx loads texture without errors
- [ ] In-game display matches expected appearance
- [ ] Character navigation respects walkmesh
- [ ] Animation loops smoothly (if applicable)

### Automated Testing
```python
# Validation script
def validate_field(field_name):
    # 1. Verify extraction completeness
    assert layer_0_exists()
    assert walkmesh_mask_exists()

    # 2. Check DDS format
    assert is_valid_dds(output_file)
    assert resolution == (1024, 1024)
    assert format == "BC7_UNORM_SRGB"

    # 3. Verify FFNx naming
    assert matches_pattern(r"{field}_\d{{2}}_00\.dds")

    # 4. Test in-game loading (optional)
    if has_ffnx_install:
        assert_loads_without_error()
```

---

## Future Enhancements

### Phase 2 Features (Post-MVP)
1. **Batch Processing UI**: Visual progress tracking for all ~760 fields
2. **Layer Blending Preview**: Show how layers composite in-game
3. **Parameter System**: Handle Layer 2/3 conditional rendering
4. **Mod Merging**: Combine multiple texture mods intelligently
5. **Web Interface**: Browser-based tool for non-technical users

### Advanced Features
1. **Real-Time Preview**: See AI output in actual game context
2. **Style Transfer**: Apply consistent art style across all fields
3. **Crowd-Sourced Metadata**: Community contributions to field database
4. **Animation Synthesis**: Generate new animations for static fields
5. **Dynamic Resolution**: Support multiple output resolutions

---

## Performance Considerations

### Extraction Performance
- **LGP Parsing**: ~10-30 seconds for full archive
- **Single Field**: <1 second per field
- **Walkmesh Projection**: <1 second per field
- **Batch Mode**: ~10-15 minutes for all 760 fields

### AI Generation Performance
- **NanoBanana Pro**: ~30-60 seconds per image
- **VEO3**: ~2-5 minutes per video
- **Bottleneck**: AI generation, not tool processing

### Conversion Performance
- **PNG→DDS**: <1 second per image (texconv)
- **Video Frame Extraction**: ~5-10 seconds per video
- **Batch Mode**: Parallelizable

---

## Project Timeline Estimate

### Phase 1: Core Implementation (Weeks 1-2)
- LGP Archive Parser
- Field Section Parser
- Background Renderer
- Walkmesh Projector

### Phase 2: AI Integration (Week 3)
- Prompt Generator
- Metadata Database (50 key fields)
- DDS Converter
- CLI Interface

### Phase 3: Testing & Refinement (Week 4)
- Test with 5 priority fields
- Fix edge cases
- Documentation
- User guide

### Phase 4: Animation Support (Week 5-6)
- Hash extraction
- Video-to-frames converter
- Animation testing
- Performance optimization

---

## Success Metrics

### Technical Success
- [ ] Successfully extracts all ~760 fields without errors
- [ ] Walkmesh masks accurately represent walkable areas
- [ ] DDS conversion produces valid FFNx-compatible files
- [ ] In-game testing shows correct rendering
- [ ] Animation frames loop smoothly

### User Success
- [ ] Clear documentation enables independent use
- [ ] CLI commands are intuitive and well-documented
- [ ] Error messages are helpful and actionable
- [ ] Batch processing completes without supervision
- [ ] Output quality meets expectations

### Community Impact
- [ ] Tool shared with FF7 modding community
- [ ] Positive feedback from beta testers
- [ ] Other modders create content using tool
- [ ] Contributes to FF7 modding ecosystem

---

## Next Steps

### Immediate Actions (Post-Planning)
1. Set up Python project structure
2. Implement LGP archive parser
3. Test with md1stin field extraction
4. Document findings and iterate

### Development Approach
- **Iterative**: Build and test each component independently
- **Test-Driven**: Validate with known-good data at each step
- **Modular**: Keep components loosely coupled for maintainability
- **Documented**: Inline comments + user documentation

### Decision Points
- DDS conversion library choice (texconv vs Python library)
- Metadata database initial population strategy
- Animation hash extraction method (Cosmos vs in-game)
- CLI framework design patterns

---

## Conclusion

This planning session established a comprehensive architecture for an AI-enhanced FF7 background replacement pipeline. The discovery that FFNx uses whole-layer texture replacement dramatically simplifies the workflow, making this project technically feasible.

The tool will enable two workflows:
1. **Faithful HD Remaster**: High-quality upscaling preserving original aesthetic
2. **Artistic Reimagining**: Creative reinterpretation with story context

Animation support via VEO3 extends capabilities to enhance existing animated elements like waterfalls and lights.

**Plan Status**: Complete and ready for implementation.
**Next Session**: Begin core implementation starting with LGP archive parsing.

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **FLEVEL.LGP** | Archive containing all ~760 field background data files |
| **FFNx** | Modern mod driver for FF7, replaces original OpenGL driver |
| **Walkmesh** | 3D triangle mesh defining walkable areas in field scenes |
| **Layer 0** | Base background layer (characters walk in front) |
| **Layer 1+** | Foreground layers (characters walk behind) |
| **DDS** | DirectDraw Surface - texture format used by FFNx |
| **BC7** | Block Compression 7 - high-quality DDS compression |
| **xxhash** | Fast hash algorithm used for animation frame identification |
| **Palette Cycling** | Original FF7 animation method (recolor pixels each frame) |
| **Section 2** | Camera matrix data in field DAT file |
| **Section 5** | Walkmesh triangle data in field DAT file |
| **Section 9** | Background tile/texture data in field DAT file |
| **Cosmos Limit Break** | Professional upscaling mod providing high-res sources |

---

## Appendix B: File Format Specifications

### LGP Archive Format
```
Header:
- Magic: "SQUARESOFT" (ASCII)
- File count: uint32
- Table of contents: array of entries

Entry:
- Filename: char[20] (null-padded)
- Offset: uint32 (from start of file)
- Check: uint8 (collision detection)
- Conflict: uint16 (hash collision index)
```

### Field DAT Structure
```
Sections (variable count):
- Section 1: Script/Dialog
- Section 2: Camera Matrix
- Section 3: Model Loader
- Section 4: Palette
- Section 5: Walkmesh
- Section 6: Tile Map (metadata)
- Section 7: Encounter Data
- Section 8: Triggers/Gateways
- Section 9: Background (tiles + textures)
```

### DDS Format Requirements
```
Format: Microsoft DirectDraw Surface
Compression: BC7_UNORM_SRGB (DX10)
Resolution: 1024x1024
Color Space: sRGB
Mipmaps: Not required (FFNx handles)
```

---

**End of Planning Document**

*Total Planning Session Duration: ~2.5 hours*
*Document Length: ~12,000 words*
*Ready for Implementation: ✓*

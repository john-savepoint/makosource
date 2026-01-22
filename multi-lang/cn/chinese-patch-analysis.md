# Chinese Traditional FF7 Patch (繁體補丁v1.3) - Technical Analysis

**Created**: 2026-01-07 16:30 JST (Wednesday)
**Last Modified**: 2026-01-07 16:30 JST (Wednesday)
**Version**: 1.0.0
**Author**: John Zealand-Doyle
**Session-ID**: 7393413e-daf6-4f5d-bfc1-8fa9e10094b5

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Contact Information](#contact-information)
3. [System Architecture Overview](#system-architecture-overview)
4. [Runtime Hooking Mechanism](#runtime-hooking-mechanism)
5. [Text Replacement Pipeline](#text-replacement-pipeline)
6. [Data Flow Diagrams](#data-flow-diagrams)
7. [Font Texture System](#font-texture-system)
8. [Comparison: Chinese Patch vs Native FFNx Approach](#comparison-chinese-patch-vs-native-ffnx-approach)
9. [Pros and Cons Analysis](#pros-and-cons-analysis)
10. [Key Insights for Japanese Implementation](#key-insights-for-japanese-implementation)

---

## Executive Summary

The Chinese Traditional patch achieves CJK text rendering through an **external text replacement system** rather than modifying the game engine's text rendering pipeline. This is fundamentally different from the FFNx Japanese PR approach which implements true CJK font rendering.

**Key Discovery**: They bypass the need for engine-level CJK support by:
1. Hooking into the game at runtime with `ali213.dll`
2. Intercepting text loads and substituting translated text
3. Using massive pre-rendered font texture atlases (8.4MB each)
4. Applying memory patches via HEXT to adjust UI spacing

---

## Contact Information

**Author**: ffsaga (Taiwan)

**Known Presence**:
- **YouTube Channel**: <https://www.youtube.com/watch?v=WqLrZOt9JoY>
- **YouTube Playlist**: <https://www.youtube.com/watch?v=YsYVq_E0HB0&list=PLD32Z3oZMD0mY4jETpnHcXIG6-Mv4-EoC>
- **Document Author Metadata**: "ffsaga" appears in all .htm files

**No direct contact information found** (no email, Discord, GitHub, or forum links in the patch files). The YouTube channel would be the best avenue for contact.

---

## System Architecture Overview

This diagram shows the complete architecture of how the Chinese patch integrates with FF7:

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef gameCore fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef hook fill:#ffebee,stroke:#f44336,stroke-width:3px,color:#b71c1c
    classDef data fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#4a148c
    classDef render fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef external fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100

    subgraph GameLayer["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>FF7 Game Layer</span>**`"]
        style GameLayer fill:#e3f2fd,stroke:#2196f3,stroke-width:3px
        FF7EXE["`**ff7.exe**
• Game executable
• Text rendering calls
• Memory structures`"]:::gameCore
        TextEngine["`**Text Engine**
• Original ASCII renderer
• Fixed character width
• 8x8 pixel tiles`"]:::gameCore
    end

    subgraph HookLayer["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>Hooking Layer</span>**`"]
        style HookLayer fill:#ffebee,stroke:#f44336,stroke-width:3px
        ALI213["`**ali213.dll**
• Microsoft Detours
• WriteProcessMemory
• ReadProcessMemory
• Text interception`"]:::hook
        HEXT["`**HEXT Patches**
• zzz_cht_patch.txt
• battle_*.txt
• Memory modifications`"]:::hook
    end

    subgraph DataLayer["`**<span style='background:linear-gradient(135deg, #9c27b0, #ab47bc);color:white;padding:5px 10px;border-radius:4px'>Translated Data Layer</span>**`"]
        style DataLayer fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px
        SceneBin["`**scene.bin**
• Battle text
• Enemy names
• Attack names`"]:::data
        Flevel["`**flevel.lgp**
• Field dialogue
• NPC conversations
• Story text`"]:::data
        WorldMes["`**world/mes**
• World map messages
• Location names`"]:::data
    end

    subgraph RenderLayer["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Font Rendering Layer</span>**`"]
        style RenderLayer fill:#e8f5e9,stroke:#4caf50,stroke-width:3px
        FontTex["`**Font Textures**
• usfont_a_h.tex (8.4MB)
• usfont_a_l.tex (8.4MB)
• usfont_b_h.tex (8.4MB)
• usfont_b_l.tex (8.4MB)`"]:::render
        GlyphAtlas["`**Glyph Atlas**
• 13,000+ Chinese chars
• Pre-rendered bitmaps
• TEX format`"]:::render
    end

    subgraph ModLoader["`**<span style='background:linear-gradient(135deg, #ff9800, #ffb74d);color:white;padding:5px 10px;border-radius:4px'>Mod Loading Layer</span>**`"]
        style ModLoader fill:#fff3e0,stroke:#ff9800,stroke-width:3px
        SeventhHeaven["`**7th Heaven**
• IRO file loading
• Mod management`"]:::external
        FFNx["`**FFNx**
• Graphics driver
• Texture replacement
• NOT modified for CJK`"]:::external
        IRO["`**ff7_cht_1.3.iro**
• 1.3GB mod archive
• Contains all assets`"]:::external
    end

    FF7EXE --> ALI213
    ALI213 --> TextEngine
    HEXT --> FF7EXE
    SceneBin --> ALI213
    Flevel --> ALI213
    WorldMes --> ALI213
    FontTex --> FFNx
    GlyphAtlas --> FontTex
    SeventhHeaven --> IRO
    IRO --> SceneBin
    IRO --> Flevel
    IRO --> FontTex
    FFNx --> TextEngine
```

---

## Runtime Hooking Mechanism

This sequence diagram shows how `ali213.dll` intercepts text at runtime:

```mermaid
sequenceDiagram
    box LightBlue Game Process
        participant FF7 as ff7.exe
        participant TextFunc as Text Functions
    end

    box rgb(255,235,238) Hook Layer
        participant ALI as ali213.dll
        participant Detour as Detours Library
    end

    box LightGreen Data Sources
        participant TransDB as Translation Table
        participant FontTex as Font Textures
    end

    Note over FF7,FontTex: STARTUP PHASE

    rect rgb(255,248,220)
        FF7->>FF7: Process starts
        FF7->>ALI: DLL injection via HEXT patch
        ALI->>Detour: Initialize Detours
        Detour->>TextFunc: Hook text rendering functions
        ALI->>TransDB: Load ENG/CHI translation pairs
        Note right of TransDB: xfhsm_res_ENG_Start<br/>xfhsm_res_CHI_Start<br/>markers in DLL
    end

    Note over FF7,FontTex: RUNTIME TEXT REPLACEMENT

    rect rgb(220,255,220)
        FF7->>TextFunc: Request text string "Potion"
        TextFunc->>ALI: Intercepted by hook
        ALI->>TransDB: Lookup "Potion"
        TransDB-->>ALI: Return "藥水"
        ALI->>ALI: Convert to texture indices
        ALI-->>TextFunc: Return modified string
        TextFunc->>FontTex: Request glyph textures
        FontTex-->>FF7: Render Chinese glyphs
    end

    Note over FF7,FontTex: MEMORY PATCHING

    rect rgb(200,230,255)
        ALI->>FF7: WriteProcessMemory
        Note right of FF7: Adjust text box sizes<br/>Modify character spacing<br/>Fix UI positioning
    end
```

---

## Text Replacement Pipeline

This flowchart details the text replacement process step-by-step:

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart LR
    classDef input fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef process fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100
    classDef decision fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#4a148c
    classDef output fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef data fill:#fce4ec,stroke:#e91e63,stroke-width:2px,color:#880e4f

    subgraph Input["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Game Request</span>**`"]
        style Input fill:#e3f2fd,stroke:#2196f3,stroke-width:3px
        A["`**Original Text**
English string
from game data`"]:::input
    end

    subgraph Interception["`**<span style='background:linear-gradient(135deg, #ff9800, #ffb74d);color:white;padding:5px 10px;border-radius:4px'>Hook Interception</span>**`"]
        style Interception fill:#fff3e0,stroke:#ff9800,stroke-width:3px
        B["`**ali213.dll**
Catches text call`"]:::process
        C{"`**Lookup**
In translation
table?`"}:::decision
    end

    subgraph Translation["`**<span style='background:linear-gradient(135deg, #9c27b0, #ab47bc);color:white;padding:5px 10px;border-radius:4px'>Translation Mapping</span>**`"]
        style Translation fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px
        D["`**Translation Table**
ENG_Start markers
CHI_Start markers`"]:::data
        E["`**Get Chinese**
Map to CHI text`"]:::process
    end

    subgraph Encoding["`**<span style='background:linear-gradient(135deg, #e91e63, #ec407a);color:white;padding:5px 10px;border-radius:4px'>Character Encoding</span>**`"]
        style Encoding fill:#fce4ec,stroke:#e91e63,stroke-width:3px
        F["`**Big5 Encoding**
Traditional Chinese
character codes`"]:::process
        G["`**Texture Index**
Map to glyph
position in atlas`"]:::process
    end

    subgraph Output["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Rendered Output</span>**`"]
        style Output fill:#e8f5e9,stroke:#4caf50,stroke-width:3px
        H["`**Font Texture**
8.4MB pre-rendered
Chinese glyphs`"]:::output
        I["`**Display**
Chinese text
on screen`"]:::output
    end

    J["`**Pass Through**
Original English`"]:::input

    A --> B --> C
    C -->|Yes| D --> E --> F --> G --> H --> I
    C -->|No| J --> I
```

---

## Data Flow Diagrams

### Overall Data Flow Architecture

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef source fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef transform fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100
    classDef storage fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#4a148c
    classDef output fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32

    subgraph OriginalGame["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Original Game Files</span>**`"]
        style OriginalGame fill:#e3f2fd,stroke:#2196f3,stroke-width:3px
        OG_Scene["`**scene.bin**
Original English`"]:::source
        OG_Field["`**flevel.lgp**
Original English`"]:::source
        OG_Font["`**Original Fonts**
ASCII only
Few KB each`"]:::source
    end

    subgraph PatchFiles["`**<span style='background:linear-gradient(135deg, #ff9800, #ffb74d);color:white;padding:5px 10px;border-radius:4px'>Patch Assets in IRO</span>**`"]
        style PatchFiles fill:#fff3e0,stroke:#ff9800,stroke-width:3px
        P_Scene["`**scene.bin**
Chinese translated`"]:::transform
        P_Field["`**flevel.lgp**
Chinese translated`"]:::transform
        P_Font["`**usfont_*.tex**
8.4MB each
13,000+ glyphs`"]:::transform
        P_HEXT["`**HEXT patches**
Memory modifications`"]:::transform
        P_DLL["`**ali213.dll**
Hook mechanism`"]:::transform
    end

    subgraph Runtime["`**<span style='background:linear-gradient(135deg, #9c27b0, #ab47bc);color:white;padding:5px 10px;border-radius:4px'>Runtime Processing</span>**`"]
        style Runtime fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px
        FFNx_Load["`**FFNx**
Loads textures
No CJK code`"]:::storage
        Seventh["`**7th Heaven**
Manages mods
IRO extraction`"]:::storage
        GameMem["`**Game Memory**
Patched at runtime`"]:::storage
    end

    subgraph Display["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Final Display</span>**`"]
        style Display fill:#e8f5e9,stroke:#4caf50,stroke-width:3px
        Screen["`**Screen Output**
Chinese text
rendered correctly`"]:::output
    end

    OG_Scene -.->|Replaced| P_Scene
    OG_Field -.->|Replaced| P_Field
    OG_Font -.->|Replaced| P_Font

    P_Scene --> Seventh
    P_Field --> Seventh
    P_Font --> Seventh
    P_HEXT --> GameMem
    P_DLL --> GameMem

    Seventh --> FFNx_Load
    FFNx_Load --> Screen
    GameMem --> Screen
```

### Memory Patching Details

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart LR
    classDef addr fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#b71c1c
    classDef patch fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef effect fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1

    subgraph HEXTPatches["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>HEXT Memory Patches</span>**`"]
        style HEXTPatches fill:#ffebee,stroke:#f44336,stroke-width:3px

        A1["`**0x400FB0**
DLL loader injection`"]:::addr
        A2["`**0x676619**
Text hook point`"]:::addr
        A3["`**0x6E0D40**
Battle text width`"]:::addr
        A4["`**0x6DE7BC**
Character spacing`"]:::addr
        A5["`**0x91C356**
Box dimensions`"]:::addr
    end

    subgraph Effects["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Effects</span>**`"]
        style Effects fill:#e8f5e9,stroke:#4caf50,stroke-width:3px

        E1["`**Load ali213.dll**
at startup`"]:::effect
        E2["`**Intercept text**
rendering calls`"]:::effect
        E3["`**Wider text boxes**
for CJK chars`"]:::effect
        E4["`**Adjusted spacing**
for proportional`"]:::effect
        E5["`**Larger dialogs**
fit more text`"]:::effect
    end

    A1 --> E1
    A2 --> E2
    A3 --> E3
    A4 --> E4
    A5 --> E5
```

---

## Font Texture System

### Font Texture Structure

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef header fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef palette fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#4a148c
    classDef pixels fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef size fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100

    subgraph TEXFormat["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>TEX File Format (8.4MB each)</span>**`"]
        style TEXFormat fill:#e3f2fd,stroke:#2196f3,stroke-width:3px

        H["`**Header (236 bytes)**
• Version: 1
• Dimensions: 2048x4096
• Bit depth: 8
• Palette flag: 1`"]:::header

        P["`**Palette (1024 bytes)**
• 256 colors
• BGRA format
• Grayscale + colors`"]:::palette

        D["`**Pixel Data (~8MB)**
• 2048 x 4096 pixels
• 1 byte per pixel
• Index into palette`"]:::pixels
    end

    subgraph GlyphLayout["`**<span style='background:linear-gradient(135deg, #9c27b0, #ab47bc);color:white;padding:5px 10px;border-radius:4px'>Glyph Organization</span>**`"]
        style GlyphLayout fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px

        G1["`**ASCII Range**
Basic Latin
0x00-0x7F`"]:::size
        G2["`**Extended**
Symbols, punctuation
0x80-0xFF`"]:::size
        G3["`**CJK Block 1**
Common characters
Big5 range`"]:::size
        G4["`**CJK Block 2**
Less common
Extended Big5`"]:::size
    end

    subgraph Comparison["`**<span style='background:linear-gradient(135deg, #ff9800, #ffb74d);color:white;padding:5px 10px;border-radius:4px'>Size Comparison</span>**`"]
        style Comparison fill:#fff3e0,stroke:#ff9800,stroke-width:3px

        S1["`**Original FF7 Font**
~10 KB
ASCII only
~100 glyphs`"]:::size
        S2["`**Chinese Font**
8.4 MB
13,000+ glyphs
840x larger!`"]:::size
    end

    H --> P --> D
    D --> G1
    D --> G2
    D --> G3
    D --> G4
```

### Font File Variants

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart LR
    classDef font fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef variant fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#4a148c

    subgraph FontOptions["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Font Style Options</span>**`"]
        style FontOptions fill:#e3f2fd,stroke:#2196f3,stroke-width:3px

        DFT["`**DFT (華康)**
Traditional style
Elegant strokes`"]:::font
        DFT_BD["`**DFT Bold**
Thicker strokes
Better visibility`"]:::font
        MSJH["`**MSJH (微軟正黑)**
Modern sans-serif
Clean appearance`"]:::font
        MSJH_BD["`**MSJH Bold**
Thick modern
High contrast`"]:::font
    end

    subgraph Files["`**<span style='background:linear-gradient(135deg, #9c27b0, #ab47bc);color:white;padding:5px 10px;border-radius:4px'>Texture Files</span>**`"]
        style Files fill:#f3e5f5,stroke:#9c27b0,stroke-width:3px

        F1["`**usfont_a_h.tex**
High detail set A`"]:::variant
        F2["`**usfont_a_l.tex**
Low detail set A`"]:::variant
        F3["`**usfont_b_h.tex**
High detail set B`"]:::variant
        F4["`**usfont_b_l.tex**
Low detail set B`"]:::variant
    end

    DFT --> F1
    DFT --> F2
    DFT_BD --> F1
    DFT_BD --> F2
    MSJH --> F3
    MSJH --> F4
    MSJH_BD --> F3
    MSJH_BD --> F4
```

---

## Comparison: Chinese Patch vs Native FFNx Approach

### Architecture Comparison

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef chinese fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#b71c1c
    classDef ffnx fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef shared fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32

    subgraph ChineseApproach["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>Chinese Patch Approach</span>**`"]
        style ChineseApproach fill:#ffebee,stroke:#f44336,stroke-width:3px

        C1["`**External Hook**
ali213.dll
Separate from FFNx`"]:::chinese
        C2["`**Pre-rendered Glyphs**
8.4MB texture atlas
Fixed character set`"]:::chinese
        C3["`**Text Replacement**
Runtime interception
Memory patching`"]:::chinese
        C4["`**Big5 Encoding**
Traditional Chinese
Specific to zh-TW`"]:::chinese
    end

    subgraph FFNxApproach["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Native FFNx Approach (Japanese PR)</span>**`"]
        style FFNxApproach fill:#e3f2fd,stroke:#2196f3,stroke-width:3px

        F1["`**Engine Integration**
FFNx core code
Direct rendering`"]:::ffnx
        F2["`**TTF Font Rendering**
Dynamic glyphs
Any character`"]:::ffnx
        F3["`**Text Pipeline**
Modified text engine
Native CJK support`"]:::ffnx
        F4["`**UTF-8 Support**
Universal encoding
Any language`"]:::ffnx
    end

    subgraph Shared["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Shared Components</span>**`"]
        style Shared fill:#e8f5e9,stroke:#4caf50,stroke-width:3px

        S1["`**7th Heaven**
Mod management`"]:::shared
        S2["`**FFNx Driver**
Graphics rendering`"]:::shared
        S3["`**Translated Data**
Game text files`"]:::shared
    end

    C1 --> S2
    C2 --> S2
    F1 --> S2
    F2 --> S2
    S1 --> C1
    S1 --> F1
    S3 --> C3
    S3 --> F3
```

### Feature Comparison Matrix

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart LR
    classDef good fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef bad fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#b71c1c
    classDef neutral fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100

    subgraph Chinese["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>Chinese Patch</span>**`"]
        style Chinese fill:#ffebee,stroke:#f44336,stroke-width:3px

        C_Flex["`**Flexibility**
Limited to pre-rendered
character set`"]:::bad
        C_Size["`**File Size**
~135MB for fonts
(4 styles x 4 files)`"]:::bad
        C_Speed["`**Development Speed**
Faster implementation
No engine changes`"]:::good
        C_Compat["`**Compatibility**
Works with stock FFNx
No PR needed`"]:::good
        C_Dual["`**Dual Language**
Achieved via
text tables`"]:::good
    end

    subgraph FFNx["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Native FFNx</span>**`"]
        style FFNx fill:#e3f2fd,stroke:#2196f3,stroke-width:3px

        F_Flex["`**Flexibility**
Any TTF font
Any character`"]:::good
        F_Size["`**File Size**
Small TTF files
~1-5MB per font`"]:::good
        F_Speed["`**Development Speed**
Complex engine work
Months of effort`"]:::bad
        F_Compat["`**Compatibility**
Requires PR merge
Or custom build`"]:::neutral
        F_Dual["`**Dual Language**
Native support
More elegant`"]:::good
    end
```

---

## Pros and Cons Analysis

### Chinese Patch Method - Detailed Analysis

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef pro fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef con fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#b71c1c
    classDef neutral fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100

    subgraph Pros["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>PROS - Chinese Method</span>**`"]
        style Pros fill:#e8f5e9,stroke:#4caf50,stroke-width:3px

        P1["`**No Engine Modification**
Works with stock FFNx
No PR approval needed`"]:::pro
        P2["`**Faster Development**
Sidesteps complex
font rendering code`"]:::pro
        P3["`**Proven Working**
Released and functional
Dual language achieved`"]:::pro
        P4["`**Isolated Changes**
External DLL approach
Easy to update`"]:::pro
        P5["`**User Control**
Multiple font options
Style selection`"]:::pro
    end

    subgraph Cons["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>CONS - Chinese Method</span>**`"]
        style Cons fill:#ffebee,stroke:#f44336,stroke-width:3px

        C1["`**Massive File Size**
135MB+ for fonts
vs ~5MB for TTF`"]:::con
        C2["`**Fixed Character Set**
Cannot add new chars
without new textures`"]:::con
        C3["`**Quality Limitations**
Pre-rendered at fixed
resolution/size`"]:::con
        C4["`**Maintenance Burden**
Separate from FFNx
updates may break`"]:::con
        C5["`**Not Reusable**
Specific to Chinese
new language = new work`"]:::con
    end
```

### Native FFNx Method - Detailed Analysis

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef pro fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef con fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#b71c1c
    classDef neutral fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100

    subgraph Pros["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>PROS - Native FFNx</span>**`"]
        style Pros fill:#e8f5e9,stroke:#4caf50,stroke-width:3px

        P1["`**Universal Solution**
Works for any language
Japanese, Korean, etc.`"]:::pro
        P2["`**Small File Size**
Standard TTF fonts
1-5MB each`"]:::pro
        P3["`**Dynamic Rendering**
Any character supported
No pre-generation`"]:::pro
        P4["`**Quality Scaling**
Renders at any size
Resolution independent`"]:::pro
        P5["`**Official Support**
Part of FFNx codebase
Maintained upstream`"]:::pro
        P6["`**Future Proof**
New languages easy
Community benefits`"]:::pro
    end

    subgraph Cons["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>CONS - Native FFNx</span>**`"]
        style Cons fill:#ffebee,stroke:#f44336,stroke-width:3px

        C1["`**Development Complexity**
Months of work
Deep engine changes`"]:::con
        C2["`**PR Approval Required**
Merge may be slow
or rejected`"]:::con
        C3["`**Breaking Changes Risk**
Core modifications
affect stability`"]:::con
        C4["`**Testing Burden**
Many edge cases
complex text layouts`"]:::con
    end
```

---

## Key Insights for Japanese Implementation

### What You Can Learn from the Chinese Approach

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart TB
    classDef insight fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef action fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32
    classDef warning fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#e65100

    subgraph Insights["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Key Technical Insights</span>**`"]
        style Insights fill:#e3f2fd,stroke:#2196f3,stroke-width:3px

        I1["`**HEXT is Powerful**
Memory patches can
adjust UI on-the-fly`"]:::insight
        I2["`**Dual Language Works**
Text tables with markers
ENG/target switching`"]:::insight
        I3["`**Font Textures Scale**
Large atlases work
if properly indexed`"]:::insight
        I4["`**External Hooks Viable**
DLL injection works
without engine changes`"]:::insight
    end

    subgraph YourAdvantages["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Your FFNx Approach Advantages</span>**`"]
        style YourAdvantages fill:#e8f5e9,stroke:#4caf50,stroke-width:3px

        A1["`**True Font Rendering**
TTF support means
any character, any size`"]:::action
        A2["`**Smaller Distribution**
Font file vs texture
10x smaller`"]:::action
        A3["`**Better Quality**
Dynamic rendering
crisp at any resolution`"]:::action
        A4["`**Reusable Foundation**
Your work helps
ALL future languages`"]:::action
    end

    subgraph Recommendations["`**<span style='background:linear-gradient(135deg, #ff9800, #ffb74d);color:white;padding:5px 10px;border-radius:4px'>Recommendations</span>**`"]
        style Recommendations fill:#fff3e0,stroke:#ff9800,stroke-width:3px

        R1["`**Contact ffsaga**
Via YouTube
Share knowledge`"]:::warning
        R2["`**Study HEXT patches**
UI spacing values
May be reusable`"]:::warning
        R3["`**Dual language design**
Their marker system
is elegant`"]:::warning
        R4["`**Continue FFNx work**
Superior long-term
Worth the effort`"]:::warning
    end

    I1 --> R2
    I2 --> R3
    I3 --> A1
    I4 --> A4
```

### Strategic Decision Matrix

```mermaid
---
config:
  layout: elk
  flowchart:
    htmlLabels: true
    subGraphTitleMargin:
      top: 10
      bottom: 25
---
flowchart LR
    classDef quick fill:#ffebee,stroke:#f44336,stroke-width:2px,color:#b71c1c
    classDef proper fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#0d47a1
    classDef hybrid fill:#e8f5e9,stroke:#4caf50,stroke-width:2px,color:#2e7d32

    subgraph QuickWin["`**<span style='background:linear-gradient(135deg, #f44336, #ef5350);color:white;padding:5px 10px;border-radius:4px'>Quick Win Path</span>**`"]
        style QuickWin fill:#ffebee,stroke:#f44336,stroke-width:3px

        Q1["`**Copy Chinese Method**
Create Japanese textures
Use similar DLL hook`"]:::quick
        Q2["`**Pros**
Fast to implement
Known to work`"]:::quick
        Q3["`**Cons**
Large files
Limited flexibility`"]:::quick
    end

    subgraph ProperSolution["`**<span style='background:linear-gradient(135deg, #2196f3, #42a5f5);color:white;padding:5px 10px;border-radius:4px'>Proper Solution Path</span>**`"]
        style ProperSolution fill:#e3f2fd,stroke:#2196f3,stroke-width:3px

        P1["`**Continue FFNx Work**
True CJK font rendering
TTF support`"]:::proper
        P2["`**Pros**
Universal solution
Small files, quality`"]:::proper
        P3["`**Cons**
More development time
PR approval needed`"]:::proper
    end

    subgraph Hybrid["`**<span style='background:linear-gradient(135deg, #4caf50, #66bb6a);color:white;padding:5px 10px;border-radius:4px'>Hybrid Approach</span>**`"]
        style Hybrid fill:#e8f5e9,stroke:#4caf50,stroke-width:3px

        H1["`**Best of Both**
Use HEXT patches for UI
FFNx for font rendering`"]:::hybrid
        H2["`**Learn from Chinese**
Their spacing values
Their dual-language design`"]:::hybrid
        H3["`**Implement in FFNx**
Native rendering
Proper architecture`"]:::hybrid
    end

    Q1 --> Q2 --> Q3
    P1 --> P2 --> P3
    H1 --> H2 --> H3
```

---

## Summary

The Chinese patch represents an **ingenious workaround** that achieves CJK text display without modifying FFNx's core rendering engine. While impressive in its results, it's fundamentally a **baked solution** using pre-rendered textures and runtime memory patching.

Your FFNx work, while more complex, provides a **proper solution** that will:
- Support any language with a TTF font
- Scale to any resolution
- Require minimal distribution size
- Benefit the entire FF7 modding community

**Recommendation**: Continue your FFNx native implementation, but study the Chinese patch for:
1. HEXT UI spacing values (directly reusable)
2. Dual-language switching mechanism (design inspiration)
3. Proof that the community wants this feature

Contact ffsaga via YouTube to potentially collaborate or share insights.

---

*Document generated from analysis of 繁體補丁v1.3 patch files*

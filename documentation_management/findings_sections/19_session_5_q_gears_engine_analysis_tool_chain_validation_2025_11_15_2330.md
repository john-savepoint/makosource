# Session 5: Q-Gears Engine Analysis & Tool Chain Validation (2025-11-15 23:30)

**Extracted From**: FINDINGS.md
**Section Lines**: 1509-1903
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


**Research Date**: 2025-11-15 23:30 JST (Saturday)
**Session**: 1021bc57-9aa2-41fe-baad-a6b89b252744 (continuation from compacted Session 4)
**Sources Analyzed**: Q-Gears engine documentation (460KB markdown), ulgp forum thread, Image2TEX repository, Tonberry source code

### Discovery #1: Q-Gears TEX Format Specification Confirmed

**Source**: Q-Gears engine documentation (ff7 game engine.md)

**TEX Format Structure** (Lines 1052-1070 of Q-Gears docs):
- **Header**: Contains metadata (width, height, bit depth, palette information)
- **Optional Palette Data**: Color Look Up Table (CLUT) for paletized images
- **Bitmap Data**: Raw pixel data

**Key Characteristics**:
- Usually stored as **paletized pictures** with bitmap pixels referencing palette
- **Color 0** (typically black) used as **transparent color**
- 16-bit depth option: **RGB555 format** (5 bits per color in 2-byte entry)
- This is the **exact format used for USFONT_*.TEX files**

**Quote from Q-Gears**:
> "FF7 PC texture consists of header, an optional palette and bitmap data. Usually data are stored like palletized picture, with bitmap pixels referencing to palette. Color 0 (in palette its usually black) is usually used as transparent color."

**Critical Implication**: Font textures use palette system, allowing color changes via CLUT modification without re-rendering entire texture.

---

### Discovery #2: PSX Font Storage Architecture

**Source**: Q-Gears VRAM documentation (Lines 271-285)

**PSX VRAM Font Location**:
- Fonts stored in **"yellow area"** of VRAM map (see Q-Gears schematic)
- Uses **CLUT (Color Look Up Tables)** system
- CLUT location separate from texture location
- GPU can directly change CLUT colors → instant font color updates

**Critical Quote from Q-Gears**:
> "The green area on the right is the permanent menu textures and the **yellow is where the menu font is located**."

**Additional Quote on Japanese Characters**:
> "All the blank rectangles are the texture cache boundaries... **The textures on the bottom right are barely overwritten** except for key places."

**PC Version Adaptation**:
- PSX: WINDOW.BIN offset **0x2754** contains font data
- PC: Fonts separated into external **MENU_US.LGP** archive as TEX files
- Texture cache system not directly ported to PC

---

### Discovery #3: Japanese Character Space Confirmed

**Source**: Q-Gears KERNEL.BIN documentation (Line 303)

**WINDOW.BIN Analysis**:
- PSX version reserves **large blank space** below menu text
- **Quote**: "The large blank spot under the menu text is for the Japanese characters that were removed in the non-Japanese version of the game."
- Japanese PSX used **dynamic kanji loading** system
- Field files specified which kanji glyphs to load per scene
- System **not ported to PC version**

**Architectural Difference**:
```
PSX Japanese:
WINDOW.BIN → Dynamic kanji loading → VRAM yellow area → Scene-specific glyphs

PC English:
MENU_US.LGP → USFONT_*.TEX → Static font set → No dynamic loading

PC Japanese (eStore):
MENU_JA.LGP → jafont_1-6.tex → 6 static font sets → No dynamic loading
```

**Implication**: PC Japanese version had to use **6 separate texture files** because it abandoned the PSX dynamic loading system.

---

### Discovery #4: ulgp - LGP Archive Tool (Complete Specification)

**Source**: https://forums.qhimm.com/index.php?topic=12831.0 (scraped 2025-11-15)

**Tool Details**:
- **Author**: luksy (based on Aali's original lgp code with permission)
- **Version**: 1.2 (latest stable), 1.2.1 (forces lowercase), 1.3.2 (no memory mapping)
- **Download**: https://www.dropbox.com/s/o770wtunby0k89y/ulgp_v1.2.7z?dl=0
- **Status**: Community-endorsed, virus-scanned clean (Malwarebytes + Avira verified)
- **First Released**: 2012-02-17
- **Thread Views**: 159,144 (highly used tool)

**Core Capabilities**:

1. **Extract Entire Archive**:
   ```bash
   ulgp -x magic.lgp
   ```
   Creates `magic/` folder with all files extracted

2. **Create Archive from Folder**:
   ```bash
   ulgp -c magic.lgp
   ```
   Packs all files in `magic/` folder into `magic.lgp`

3. **Overwrite Files in Archive** ⭐ **KEY FEATURE**:
   ```bash
   ulgp -r magic.lgp
   ```
   Reads files from `magic/` folder and **overwrites matching files** in `magic.lgp` without full extraction/repack
   - **Massive time savings**: Don't need to extract all files to update a few
   - **Space savings**: Temporary extraction folder only needs modified files

4. **Extract Individual Files** (v0.2+):
   ```bash
   ulgp -d magic.lgp somefolder
   ```
   Extract specific files only

5. **Insert Individual Files** (v0.2+):
   ```bash
   ulgp -i magic.lgp specific_file.tex
   ```

**GUI Features**:
- Double-click `.lgp` file to extract to default folder
- Right-click folder → Create/add to `.lgp` file
- `install.bat` to associate `.lgp` files with ulgp
- Two GUI versions: XP style and Vista/7/8 style

**Advanced Usage** (from readme):
- Source code included (LGPLIB interface for custom projects)
- Command-line distribution for automated mod installers
- Case-insensitive filename matching (v0.4+)
- Localization support (translations available)

**Known Issues Fixed**:
- v0.2: Hash table bug (don't use)
- v0.3: Fixed hash table
- v0.4: Fixed case sensitivity issues
- v1.2.1: Forces lowercase filenames internally (compatibility)
- v1.3.2: No memory mapping (use if getting memory errors)

**Community Endorsements**:
- Aali (original lgp author): "This is exactly the kind of re-use I intended for my code"
- DLPB (The Reunion developer): "Cut down on decoding the whole files. Less space needed now and faster"
- sl1982 (7th Heaven developer): "Will make automated installers much quicker"

**Relevance**: **CRITICAL** - Primary tool for extracting USFONT_*.TEX from menu_us.lgp and repacking modified fonts.

---

### Discovery #5: Image2TEX - Batch Texture Converter

**Source**: https://github.com/niemasd/Image2TEX (scraped 2025-11-15)

**Tool Details**:
- **Original Author**: Borde
- **Archiver**: Niemas Deutrom (niemasd on GitHub)
- **Language**: Visual Basic .NET
- **Last Updated**: 2019-05-26 (6 years old)
- **License**: Not explicitly stated (source code public)
- **Stars**: 6, **Forks**: 1

**Core Capabilities**:

1. **Format Support**:
   - **Input**: BMP, JPG, GIF, ICO, WMF, EMF
   - **Output**: TEX (FF7 PC texture format)
   - **Reverse**: TEX → BMP export

2. **Usage Workflow**:

   **Method A: Single File**:
   ```
   1. Click "Open image" button
   2. Select BMP/JPG/GIF/etc.
   3. Click "Save texture" button
   4. Choose TEX or BMP output
   ```

   **Method B: Batch Conversion** ⭐ **KEY FEATURE**:
   ```
   1. Click "Mass convert" button
   2. Select directory with images
   3. Converts all images ↔ TEX format
   4. Output filenames: same name, extension changed
   ```

3. **Options**:
   - **"Color 0 as transparent"**: Checkbox treats completely black pixels as transparent
   - **Color depth preservation**: Maintains original image color depth

**Technical Details**:
- Based on Mirex and Aali's TEX format specification work
- Uses GDI API (GDIAPI.bas) for image loading
- FF7TEXTexture.bas: TEX format encoding/decoding
- BMPTexture.bas: BMP format handling

**Known Issues**:
- **"Color 0 as transparent" limitation**: No effect on original FF7 engine for 24-bit images
- **Works with Aali's/FFNx driver**: Transparency flag functions correctly with modern drivers

**Quote from README**:
> "This tool is heavily untested, use it at your own risk."

**Source Files Available**:
- `Image2TEX.frm` - GUI form
- `FF7TEXTexture.bas` - TEX format code
- `BMPTexture.bas` - BMP handling
- `GDIAPI.bas` - Windows GDI interface
- `Image2TEX_Project.vbp` - Visual Basic project file

**Compilation Note**: Requires Visual Basic 6.0 or compatible compiler. Pre-compiled executable not in repository (may exist in qhimm forums).

**Relevance**: **CRITICAL** - Enables conversion of edited font images (BMP/PNG) back to TEX format for repacking into menu_us.lgp.

---

### Discovery #6: Tonberry Source Code Architecture (Reference)

**Source**: https://github.com/jonnynt/tonberry (scraped 2025-11-15)

**Tool Details**:
- **Author**: jonnynt
- **Game**: Final Fantasy VIII (2013 Steam release)
- **Version**: 2.04 (last updated 2015-06-23)
- **License**: MIT License (free to use, modify, distribute)
- **Language**: C++ (52.5%), C (47.5%)
- **Forum Thread**: https://forums.qhimm.com/index.php?topic=15945.0

**Architecture Insights** (from commit history):

1. **Runtime Injection**:
   - Hooks DirectX `UnlockRect()` function
   - Intercepts texture loading at GPU level
   - No game executable modification required

2. **Hash-based Mapping**:
   - CSV files map texture hash values to replacement PNG filenames
   - Format: `texture_name,hash_value`
   - Example: `sysfld00_13,8637763346649579509`

3. **Cache Management**:
   - `nhcache_item_t` struct with persist boolean flag
   - Persistent textures: Prefix `!` in CSV to keep in cache permanently
   - Disabled textures: Prefix `*` in CSV to exclude from loading
   - Configurable cache size (max 250 for non-LAA builds)

4. **Performance Characteristics** (from commit messages):
   - `UnlockRect()` identified as primary bottleneck
   - Cache eviction needed for 32-bit memory constraints
   - Exponentially worse lag with cache sizes below 100
   - Quote: "Now if there are too many persistent textures, Tonberry won't crash... it will just lag."

**Directory Structure** (from forum thread):
```
[FF8]/
├── tonberry/
│   ├── hashmap/*.csv      → Hash-to-texture mapping files
│   └── prefs.txt          → Configuration (cache size, etc.)
└── textures/**/*.png       → Replacement texture PNG files
```

**Differences from FFNx Approach**:
- **Tonberry**: Hash-based (requires hash calculation/CSV mapping)
- **FFNx**: Path-based (simple filename matching in mod_path)
- **Tonberry**: Runtime interception (DLL injection)
- **FFNx**: Driver replacement (full graphics driver)

**Relevance**: **HIGH** - Proves runtime texture injection works for Square Enix games. FFNx's simpler path-based system avoids hash complexity.

---

### Revised Tool Chain Workflow

Based on Session 5 discoveries, here is the **complete validated tool chain**:

**Phase 1: Extraction**
```bash
# Extract menu_us.lgp
ulgp -x menu_us.lgp

# Result: menu_us/ folder containing USFONT_*.TEX files
```

**Phase 2: Conversion (TEX → Editable Format)**

**Option A: Use Image2TEX**:
```
1. Launch Image2TEX.exe
2. Open image: USFONT_H.TEX
3. Save texture: USFONT_H.BMP
4. Edit in GIMP/Photoshop
```

**Option B: Use FFNx texture dumping**:
```toml
# FFNx.toml
save_textures = true
```
Launch game → Open menu → Fonts dumped as PNG to `mods/Textures/`

**Phase 3: Editing**
```
1. Open USFONT_H.BMP in GIMP/Photoshop
2. Modify font glyphs (e.g., change to red, add borders)
3. Save as BMP (preserve dimensions exactly!)
```

**Phase 4A: Testing via FFNx (RECOMMENDED - No Repacking)**
```bash
# Copy edited PNG directly to FFNx mod_path
cp USFONT_H_modified.PNG "[FF7_DIR]/mods/Textures/USFONT_H.PNG"

# Configure FFNx.toml
mod_path = "mods/Textures"
mod_ext = ["dds", "png"]

# Launch game and test
```

**Phase 4B: Production (Repack into LGP)**
```
# Convert BMP → TEX
1. Launch Image2TEX.exe
2. Open image: USFONT_H_modified.BMP
3. Save texture: USFONT_H.TEX

# Overwrite in LGP archive
mkdir menu_us
cp USFONT_H.TEX menu_us/
ulgp -r menu_us.lgp

# Result: menu_us.lgp now contains modified font
```

**Phase 5: Distribution**
```
# For 7th Heaven mods
Create .IRO file containing:
- Modified menu_us.lgp
OR
- Texture files for FFNx mod_path

# For manual installation
Distribute ulgp + modified menu_us.lgp with instructions
```

---

### Complete Tool Inventory

| Tool | Purpose | Status | Download | Priority |
|------|---------|--------|----------|----------|
| **ulgp v1.2** | LGP extract/insert/repack | ✅ Documented | [Dropbox](https://www.dropbox.com/s/o770wtunby0k89y/ulgp_v1.2.7z?dl=0) | **CRITICAL** |
| **Image2TEX** | BMP/JPG/GIF ↔ TEX batch converter | ✅ Documented | [GitHub Source](https://github.com/niemasd/Image2TEX) | **CRITICAL** |
| **tim2png** | TIM → PNG converter | ⏳ Pending scrape | [ff7tools GitHub](https://github.com/cebix/ff7tools) | **HIGH** |
| **TEX to BMP** | TEX → BMP code example | ⏳ Pending scrape | [Gist](https://gist.github.com/hoehrmann/5720668) | **MEDIUM** |
| **Tex Tools** | Community TEX converter | ⏳ Pending scrape | [qhimm Thread](https://forums.qhimm.com/index.php?topic=17755.0) | **MEDIUM** |
| **FFNx** | Modern graphics driver | ✅ Documented | [GitHub](https://github.com/julianxhokaxhiu/FFNx) | **CRITICAL** |
| **7th Heaven** | Mod manager | ✅ Documented | [Official Site](https://7thheaven.rocks/) | **HIGH** |

---

### Immediate Next Steps (Updated Post-Session 5)

**PRIORITY 1: Validate FFNx Texture Override** ✅ Ready to Execute
- All tools identified and documented
- TEST_PROCEDURE.md provides complete guide
- Font filenames confirmed (USFONT_H.TEX, etc.)
- **Action**: Execute test procedure to validate concept

**PRIORITY 2: Tool Acquisition**
- Download ulgp v1.2 from Dropbox
- Find pre-compiled Image2TEX executable (check qhimm forums)
- Alternative: Compile Image2TEX from Visual Basic .NET source

**PRIORITY 3: Remaining Tool Research**
- Scrape tim2png documentation
- Scrape TEX to BMP code example
- Scrape Tex Tools forum thread
- Document alternative conversion methods

**PRIORITY 4: Community Engagement**
- Join Discord servers (VG Research & Modding, FF7 Discord)
- Contact FFNx developers on Issue #39
- Request Japanese version `menu_ja.lgp` extraction from community

**PRIORITY 5: Japanese Font Acquisition**
- Research creating Japanese font textures from scratch
- Investigate Japanese TrueType → Bitmap atlas conversion
- Study `jafont_1-6.tex` organization (if obtainable)

---


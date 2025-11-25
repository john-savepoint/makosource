# FF7 Japanese Font Texture Override - Test Procedure

**Created**: 2025-11-15 21:10:00 JST (Saturday)
**Last Modified**: 2025-11-25 11:55:00 JST (Tuesday)
**Version**: 2.0.0 (SESSION 10 - PROOF OF CONCEPT ACHIEVED)
**Author**: Research Sessions 3-10
**Session-ID**:
- 1021bc57-9aa2-41fe-baad-a6b89b252744 (Sessions 3-7)
- 77121986-7211-4ef5-a043-d61a47fa6f66 (Session 10)

---

## 🎉 SESSION 10 UPDATE - PROOF OF CONCEPT ACHIEVED!

**BREAKTHROUGH**: FFNx Texture Override **WORKS** for font textures!

**Process that worked:**
1. Enable `save_textures = true` in FFNx.toml
2. Run FF7 to trigger texture dumping
3. FFNx creates actual game textures in `mods/Textures/menu/`
4. Edit those dumped textures directly (e.g., make them red)
5. Disable `save_textures = false` to stop overwriting edits
6. Run FF7 - modified textures load successfully!

**Key Discovery**: FFNx uses **filename-based matching** with dumped textures (not hash-based). The filenames it creates ARE the correct ones to modify.

---

## SESSION 7 UPDATE - CRITICAL NEW INFORMATION

**MAJOR DISCOVERY**: We now have access to Square Enix's Japanese eStore version!

**New Assets Available**:
- `/Volumes/KIOXIAwhite/FF7/AF3DN.P` - Custom Japanese graphics driver (317KB)
- `/Volumes/KIOXIAwhite/FF7/data/menu/menu_ja.lgp` - Japanese font archive (26.8MB)
- 6× jafont_*.tex files (~4MB each)
- ff7_ja.exe - Japanese executable with working Japanese text!

**This Changes the Testing Approach**:
- OLD: Test if we can override English fonts with modified textures
- **NEW**: Test if we can use Square Enix's working Japanese implementation as reference

**Recommendation**: Before following this procedure, read **AF3DN_ANALYSIS.md** for details on the custom driver.

---

## Document Purpose

This document provides a complete, step-by-step procedure for testing whether FFNx's texture override system can replace FF7's font textures. This is **Phase 1** of implementing Japanese font support - validating the core concept before investing in full Japanese character implementation.

**SESSION 7 UPDATE**: With the discovery of AF3DN.P and complete Japanese assets, we now have an alternative path:
1. **Path A (Original)**: Modify FFNx to add Japanese support ← This document
2. **Path B (New)**: Use Square Enix's AF3DN.P driver directly ← See AF3DN_ANALYSIS.md
3. **Path C (Hybrid)**: Reverse-engineer AF3DN.P and port to FFNx ← Most comprehensive

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Extract Current Font Textures](#phase-1-extract-current-font-textures)
3. [Phase 2: Analyze Font Texture Format](#phase-2-analyze-font-texture-format)
4. [Phase 3: Create Test Replacement Texture](#phase-3-create-test-replacement-texture)
5. [Phase 4: Configure FFNx Texture Override](#phase-4-configure-ffnx-texture-override)
6. [Phase 5: Test & Verify](#phase-5-test--verify)
7. [Phase 6: Document Results](#phase-6-document-results)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Next Steps Based on Results](#next-steps-based-on-results)

---

## Prerequisites

### Required Software

1. **Final Fantasy VII PC** (1998 version or 2012/2013 Steam version)
   - Installation directory: Typically `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\`
   - Or: Square Enix store version

2. **FFNx Graphics Driver** (v1.14.0 or later recommended)
   - Download: https://github.com/julianxhokaxhiu/FFNx/releases
   - Already installed if using 7th Heaven 2.0+
   - Verify: Check for `FFNx.dll` and `FFNx.toml` in FF7 directory

3. **LGP Extraction Tool** (choose one):
   - **ulgp v1.2+** (RECOMMENDED)
     - URL: https://forums.qhimm.com/index.php?topic=12831.0
     - Download: https://www.dropbox.com/s/o770wtunby0k89y/ulgp_v1.2.7z?dl=0
     - Reason: Supports extraction, insertion, and repacking in one tool

   - **Ficedula's LGP Editor** (GUI alternative)
     - Mentioned at: https://qhimm-modding.fandom.com/wiki/FF7/LGP_format
     - Easier for beginners, less powerful

   - **Aali's lgp/unlgp** (command-line original)
     - URL: https://forums.qhimm.com/index.php?topic=8641.0
     - Requires separate tools for pack/unpack

4. **TEX Format Viewer/Converter** (optional but helpful):
   - Tools TBD - may need to test with PNG directly
   - Alternative: Use FFNx's `save_textures` to dump current textures

5. **Image Editor** (for creating test textures):
   - GIMP (free, open source)
   - Photoshop
   - Paint.NET
   - Any tool that can edit PNG files

### Required Knowledge

- Basic command-line usage (Windows CMD or PowerShell)
- File system navigation
- Text file editing (for FFNx.toml)
- Basic understanding of image formats

### Time Estimate

- **Setup**: 30-45 minutes
- **Extraction**: 5-10 minutes
- **Test Creation**: 15-30 minutes
- **Testing**: 10-15 minutes
- **Total**: ~1.5 hours

---

## Phase 1: Extract Current Font Textures

### Step 1.1: Locate menu_us.lgp

**Location** (Steam version):
```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\menu\menu_us.lgp
```

**Alternative locations**:
- 1998 CD version: `[FF7_INSTALL]\data\menu\menu_us.lgp`
- 2012 version: `[FF7_INSTALL]\data\menu\menu_us.lgp`

**Verify file exists**:
1. Open File Explorer
2. Navigate to the path above
3. Confirm `menu_us.lgp` is present
4. Note file size (should be several MB)

**If file not found**:
- Check for 7th Heaven modifications (may use IRO override)
- Verify FF7 installation is complete
- Try searching entire FF7 directory for `menu_us.lgp`

---

### Step 1.2: Create Working Directory

**Create directory structure**:
```
C:\FF7_Modding\
├── original\          (backup of original files)
├── extracted\         (extracted LGP contents)
├── modified\          (our test textures)
└── tools\             (ulgp and other tools)
```

**Commands** (PowerShell):
```powershell
New-Item -Path "C:\FF7_Modding\original" -ItemType Directory
New-Item -Path "C:\FF7_Modding\extracted" -ItemType Directory
New-Item -Path "C:\FF7_Modding\modified" -ItemType Directory
New-Item -Path "C:\FF7_Modding\tools" -ItemType Directory
```

**Commands** (CMD):
```cmd
mkdir C:\FF7_Modding\original
mkdir C:\FF7_Modding\extracted
mkdir C:\FF7_Modding\modified
mkdir C:\FF7_Modding\tools
```

---

### Step 1.3: Backup menu_us.lgp

**Copy original file to backup**:
```cmd
copy "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\menu\menu_us.lgp" "C:\FF7_Modding\original\menu_us.lgp"
```

**Verify backup**:
```cmd
dir "C:\FF7_Modding\original"
```

Expected output: `menu_us.lgp` with matching file size

**CRITICAL**: Never modify files in the game directory without backup!

---

### Step 1.4: Extract Font Textures with ulgp

**Download and extract ulgp**:
1. Download `ulgp_v1.2.7z` from Dropbox link above
2. Extract to `C:\FF7_Modding\tools\ulgp\`
3. Verify `ulgp.exe` is present

**Method A: Extract Entire Archive** (easier, slower):

```cmd
cd C:\FF7_Modding\tools\ulgp
ulgp -x "C:\FF7_Modding\original\menu_us.lgp"
```

This creates a `menu_us` folder with all files extracted.

**Expected output**:
```
Extracting menu_us.lgp...
[Progress messages...]
Extracted X files to menu_us/
```

**Method B: Extract Font Files Only** (faster, more targeted):

```cmd
cd C:\FF7_Modding\tools\ulgp
ulgp -e "C:\FF7_Modding\original\menu_us.lgp" USFONT_H.TEX
ulgp -e "C:\FF7_Modding\original\menu_us.lgp" USFONT_A_H.TEX
ulgp -e "C:\FF7_Modding\original\menu_us.lgp" USFONT_B_H.TEX
ulgp -e "C:\FF7_Modding\original\menu_us.lgp" USFONT_L.TEX
ulgp -e "C:\FF7_Modding\original\menu_us.lgp" USFONT_A_L.TEX
ulgp -e "C:\FF7_Modding\original\menu_us.lgp" USFONT_B_L.TEX
```

**Note**: `-e` flag may not exist in ulgp. If command fails, use Method A and manually copy font files.

---

### Step 1.5: Verify Extracted Files

**Expected font files** (from FF7 Menu Module documentation):

**High Resolution** (for 640x480+ modes):
- `USFONT_H.TEX` - Main font texture
- `USFONT_A_H.TEX` - Variant A (possibly colored)
- `USFONT_B_H.TEX` - Variant B (possibly colored)

**Low Resolution** (for 320x240 mode):
- `USFONT_L.TEX` - Main font texture
- `USFONT_A_L.TEX` - Variant A
- `USFONT_B_L.TEX` - Variant B

**Check extracted files**:
```cmd
dir C:\FF7_Modding\tools\ulgp\menu_us\USFONT*.TEX
```

**If files not found**:
- Files might have lowercase names: `usfont_h.tex`
- Try: `dir C:\FF7_Modding\tools\ulgp\menu_us\*font*.tex /s`
- Document actual filenames for later use

**Copy to extracted directory**:
```cmd
copy C:\FF7_Modding\tools\ulgp\menu_us\USFONT*.TEX C:\FF7_Modding\extracted\
```

---

## Phase 2: FFNx Texture Dumping (THE WORKING METHOD)

### Understanding the Pipeline

**FFNx's Role**:
- Acts as a renderer/graphics driver interceptor
- When `save_textures = true`, FFNx hooks texture loading calls
- Exports actual game textures to `mods/Textures/[category]/filename.png`
- These exported filenames ARE the correct ones to use for overrides

**Why This Matters**:
- You don't need to manually extract/convert TEX files
- FFNx already handles format conversion
- The filenames it creates are the ones that will work for replacement

### Step 2.1: Enable Texture Dumping

1. **Edit FFNx.toml**:
   ```toml
   save_textures = true
   ```
   Location: `[FF7_DIR]/FFNx.toml`

2. **Launch FF7 via 7th Heaven**:
   - Start the game normally
   - Open menus (press ESC)
   - Navigate through menu options to trigger texture loading:
     - ITEM
     - MAGIC
     - MATERIA
     - STATUS
     - Go back to main menu

3. **Close the game** - textures are now dumped

### Step 2.2: Locate Dumped Textures

**Location**: `[FF7_DIR]/mods/Textures/menu/`

**Expected files for fonts**:
- `usfont_a_h_14.png` (high-res variant A)
- `usfont_a_l_14.png` (low-res variant A)
- `usfont_b_h_14.png` (high-res variant B)
- `usfont_b_l_14.png` (low-res variant B)

These are actual PNG images with white glyphs on transparent background.

**Option B: Manual TEX conversion** (if Option A fails):

This requires a TEX viewer/converter tool. Research needed:
- Search qhimm forums for "TEX to PNG converter"
- Check if Textools or similar utilities support FF7 TEX format
- May need to write custom converter using TEX format specification

**For this test**: If Option A works, use PNG directly. If not, document TEX format issue for community support.

---

### Step 2.3: Examine Font Texture

**Open extracted/dumped font PNG**:
1. Use image editor (GIMP, Photoshop, Paint.NET)
2. Examine layout:
   - Likely a grid of character glyphs
   - Each cell = one character
   - Arranged in character table order

**Document observations**:
- Image dimensions (e.g., 256x256, 512x512)
- Number of characters per row
- Number of rows
- Character arrangement (ASCII order? FF Text encoding order?)
- Color depth (grayscale, RGB, RGBA)
- Background color (transparent, black, white)

**Example expected layout**:
```
Row 1: [space] ! " # $ % & ' ( ) * + , - . /
Row 2: 0 1 2 3 4 5 6 7 8 9 : ; < = > ?
Row 3: @ A B C D E F G H I J K L M N O
...
```

**Save observations to file**:
```
C:\FF7_Modding\font_analysis.txt
```

---

## Phase 3: Edit Dumped Textures (THE SIMPLE METHOD)

### Step 3.1: Open Dumped Texture

**Files to edit**:
- `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\menu\usfont_a_h_14.png`
- `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\menu\usfont_a_l_14.png`
- `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\menu\usfont_b_h_14.png`
- `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\menu\usfont_b_l_14.png`

### Step 3.2: Apply Modification (Red Color Test)

**Using any image editor** (GIMP, Photoshop, Paint.NET, etc.):

1. **Open** `usfont_a_h_14.png`
2. **Select All** (Ctrl+A)
3. **Colorize or Tint Red**:
   - GIMP: Colors → Hue-Saturation → Colorize
   - Or: Colors → Desaturate then Colors → Color Balance to red
   - Or: Filters → Light and Shadow → Color Dodge (set color to red)
4. **Save** the file (overwrite original PNG)

**Repeat for all 4 files** (usfont_a_h_14, usfont_a_l_14, usfont_b_h_14, usfont_b_l_14)

**KEY**: Keep the same filename, dimensions, and transparency. Only change the colors of the glyph pixels.

### Step 3.3: Disable Texture Dumping

**CRITICAL STEP**: Edit FFNx.toml:

```toml
save_textures = false
```

**Why**: If you leave `save_textures = true`, FFNx will detect the original texture bytes from the game engine and re-dump them, overwriting your red edits.

---

## Phase 3 (Old): Create Test Replacement Texture

### Step 3.1 (Old): Plan Visual Modification

**Goal**: Create an OBVIOUS visual change to verify texture override works

**Recommended modifications** (choose one or combine):

1. **Color change**:
   - Change all font glyphs to bright red (#FF0000)
   - Easy to spot, proves texture is loading

2. **Add border/outline**:
   - Add thick colored border around each character
   - Highly visible in menus

3. **Replace characters**:
   - Replace "A" with "Z", "B" with "Y", etc.
   - Proves character mapping is working

4. **Add marker**:
   - Add colored dot or star in corner of each glyph
   - Less intrusive but still noticeable

**CRITICAL**: Keep same dimensions and layout!
- Do NOT resize image
- Do NOT change number of characters
- Do NOT rearrange character positions
- ONLY modify glyph appearance

---

### Step 3.2: Create Modified Texture

**Using GIMP** (free, cross-platform):

1. **Open font texture**:
   - File → Open → `C:\FF7_Modding\extracted\usfont_h.png`

2. **Apply color change** (if chosen):
   - Colors → Colorize
   - Or: Select → All, then Edit → Fill with FG Color (set to red)
   - Or: Layer → New Layer → Fill with red, set blend mode to Multiply

3. **Add outline** (if chosen):
   - Filters → Edge-Detect → Edge
   - Or: Filters → Light and Shadow → Drop Shadow

4. **Add markers** (if chosen):
   - Select paintbrush tool
   - Choose bright color
   - Add small dots/marks to glyphs

5. **Verify**:
   - Zoom to 100%
   - Check that modifications are visible
   - Verify image dimensions unchanged

6. **Export**:
   - File → Export As
   - Filename: `C:\FF7_Modding\modified\USFONT_H.PNG`
   - Format: PNG
   - Settings: No compression, preserve transparency

**Using Photoshop** (similar process):
1. Open → Apply modifications → Save As PNG

**Using Paint.NET**:
1. Open → Adjustments → Hue/Saturation (shift to red)
2. Save as PNG

---

### Step 3.3: Create Test Variants

**Test multiple scenarios**:

1. **High-res only**:
   - Modify only `USFONT_H.PNG`
   - Tests high-resolution mode override

2. **All variants**:
   - Modify `USFONT_H.PNG`, `USFONT_A_H.PNG`, `USFONT_B_H.PNG`
   - Tests if all variants are used

3. **Low-res**:
   - Modify `USFONT_L.PNG`, `USFONT_A_L.PNG`, `USFONT_B_L.PNG`
   - Tests low-resolution mode

**For initial test**: Start with `USFONT_H.PNG` only.

---

### Step 3.4: Test Different Formats

**Create multiple format versions** (to test FFNx support):

1. **PNG format**:
   - `USFONT_H.PNG` (already created)
   - Most likely to work (FFNx lists PNG in `mod_ext`)

2. **DDS format**:
   - Convert PNG to DDS using:
     - GIMP: File → Export As → .dds
     - NVIDIA Texture Tools
     - AMD Compressonator
   - Save as `USFONT_H.DDS`

3. **Original TEX format** (if possible):
   - If TEX→PNG→TEX conversion tool available
   - Save as `USFONT_H.TEX`

**For initial test**: Use PNG only. Test other formats if PNG fails.

---

## Phase 4: Configure FFNx Texture Override

### Step 4.1: Locate FFNx Configuration

**Find FFNx.toml**:
- **Typical location**: `[FF7_DIR]/FFNx.toml`
- **Steam**: `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.toml`

**Verify FFNx is installed**:
```cmd
dir "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.*"
```

Expected: `FFNx.dll`, `FFNx.toml`, possibly `FFNx.log`

**If FFNx not found**:
- Install FFNx from https://github.com/julianxhokaxhiu/FFNx/releases
- Or install 7th Heaven (includes FFNx)
- Cannot proceed without FFNx

---

### Step 4.2: Backup Original Configuration

**Create backup**:
```cmd
copy "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.toml" "C:\FF7_Modding\original\FFNx.toml.backup"
```

**Important**: Can restore with:
```cmd
copy "C:\FF7_Modding\original\FFNx.toml.backup" "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.toml"
```

---

### Step 4.3: Edit FFNx.toml

**Open in text editor**:
- Notepad++ (recommended)
- VS Code
- Notepad (works but less convenient)

**Find texture override section**:
```toml
# Texture configuration
mod_path = "mods/Textures"
mod_ext = ["dds", "png"]
show_missing_textures = false
save_textures = false
```

**Modify for testing**:
```toml
# Texture configuration
mod_path = "mods/Textures"
mod_ext = ["dds", "png"]  # Already supports PNG
show_missing_textures = true  # ENABLE for debugging
save_textures = false  # Keep false for now
```

**Key changes**:
- `show_missing_textures = true` - FFNx will log which textures it tries to load
- This helps debug if our texture isn't being recognized

**Save file**.

---

### Step 4.4: Create mod_path Directory

**Create texture override directory**:
```cmd
mkdir "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods"
mkdir "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures"
```

**Verify creation**:
```cmd
dir "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures"
```

---

### Step 4.5: Copy Test Texture to mod_path

**Copy modified texture**:
```cmd
copy "C:\FF7_Modding\modified\USFONT_H.PNG" "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\USFONT_H.PNG"
```

**CRITICAL - Filename matching**:
- FFNx uses **path-based** texture override (not hash-based like Tonberry)
- Filename MUST match exactly (case may or may not matter)
- If original is `usfont_h.tex`, try both:
  - `USFONT_H.PNG` (uppercase)
  - `usfont_h.png` (lowercase)

**Test both if uncertain**:
```cmd
copy "C:\FF7_Modding\modified\USFONT_H.PNG" "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\usfont_h.png"
```

---

### Step 4.6: Review Final Configuration

**Checklist before testing**:
- [ ] FFNx.toml edited with `show_missing_textures = true`
- [ ] `mods/Textures/` directory created
- [ ] Modified texture copied to `mods/Textures/`
- [ ] Texture filename matches original (check case)
- [ ] Backup of original FFNx.toml saved
- [ ] Backup of original menu_us.lgp saved

---

## Phase 5: Test & Verify

### Step 5.1: Launch FF7 with FFNx

**Close any running FF7 instances**.

**Launch the game**:
- Steam: Launch from Steam library
- Non-Steam: Run `ff7.exe` or `ff7_en.exe` from game directory

**Watch for**:
- FFNx splash screen (confirms FFNx is active)
- Any error messages
- Game should boot normally

---

### Step 5.2: Check FFNx Log

**Open FFNx.log** (BEFORE opening menu):
```
C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.log
```

**Search for texture loading messages**:
- Look for lines containing "texture" or "font"
- Look for lines containing mod_path
- Look for "USFONT" references

**Example expected entries**:
```
[INFO] Loading external texture: mods/Textures/USFONT_H.PNG
[INFO] Texture override successful: USFONT_H.TEX -> USFONT_H.PNG
```

**If errors appear**:
```
[ERROR] Failed to load texture: mods/Textures/USFONT_H.PNG
```
Document error message for troubleshooting.

---

### Step 5.3: Test In-Game Menu

**Open the game menu**:
1. Get past intro/splash screens
2. Reach main menu or load a save
3. Press ESC (keyboard) or Start/Menu button (gamepad)
4. Game menu should appear

**Visual inspection**:
- **SUCCESS**: Text appears in modified style (red color, outlined, etc.)
- **PARTIAL**: Some text changed, some unchanged (not all fonts overridden)
- **FAILURE**: Text appears normal (texture override not working)

**Test different menu sections**:
- Main menu (NEW GAME, CONTINUE, etc.)
- In-game menu (ITEM, MAGIC, MATERIA, etc.)
- Item descriptions
- Status screens
- Configuration menu

**Document which sections show modified font**.

---

### Step 5.4: Take Screenshots

**Capture evidence**:
1. Use in-game screenshot key (usually F12 on Steam)
2. Or use Windows: Win+Shift+S (Snipping Tool)
3. Capture:
   - Main menu with modified font
   - In-game menu with modified font
   - Any sections that DON'T show modified font

**Save screenshots**:
```
C:\FF7_Modding\test_results\screenshot_menu_main.png
C:\FF7_Modding\test_results\screenshot_menu_item.png
C:\FF7_Modding\test_results\screenshot_menu_status.png
```

---

### Step 5.5: Test Different Resolutions

**Change game resolution**:
1. Open game config (FF7Config.exe or in-game settings)
2. Try different resolutions:
   - 640x480 (low resolution)
   - 1280x720 (medium)
   - 1920x1080 (high)

**Check if font changes**:
- High resolution should use `USFONT_H.*` files
- Low resolution should use `USFONT_L.*` files
- Verify which resolution triggers which font

---

## Phase 6: Document Results

### Step 6.1: Record Test Outcomes

**Create test results document**:
```
C:\FF7_Modding\test_results\test_results.txt
```

**Template**:
```
FF7 Font Texture Override Test Results
Date: [DATE]
FFNx Version: [VERSION from FFNx.log]
Test Texture: USFONT_H.PNG (red color modification)

RESULTS:
[ ] SUCCESS - Font texture override works!
[ ] PARTIAL - Override works in some menus only
[ ] FAILURE - Override does not work

Details:
- Modified font appeared in: [list menu sections]
- Modified font DID NOT appear in: [list sections]
- Errors encountered: [list any errors]

FFNx.log relevant entries:
[paste relevant log lines]

Screenshots:
- screenshot_menu_main.png
- screenshot_menu_item.png
- etc.

Conclusions:
[What did we learn? What worked? What didn't?]

Next steps:
[Based on results, what to do next?]
```

---

### Step 6.2: Update Research Documentation

**Add findings to FINDINGS.md**:
- Create "Session 4: Texture Override Test Results" section
- Document test procedure
- Include screenshots (if possible to embed)
- State conclusions

**Add to SCRAPED_URLS.md**:
- Document any new URLs researched
- Update statistics

---

## Troubleshooting Guide

### Issue: Texture Not Loading

**Symptoms**: Font appears normal, no visual changes

**Diagnosis**:

1. **Check FFNx.log for texture loading**:
   - Search for "USFONT"
   - Look for "Loading external texture" messages

2. **Verify filename matching**:
   - Compare `mod_path` texture filename to original in LGP
   - Try different case: `USFONT_H.PNG` vs `usfont_h.png`
   - Try with `.TEX` extension instead of `.PNG`

3. **Check mod_path configuration**:
   - Verify `mod_path = "mods/Textures"` in FFNx.toml
   - Verify directory exists at `[FF7_DIR]/mods/Textures/`
   - Try absolute path: `mod_path = "C:/FF7_DIR/mods/Textures"`

4. **Verify FFNx is active**:
   - Look for FFNx splash screen on launch
   - Check for FFNx.log creation
   - Verify `FFNx.dll` is in game directory

**Solutions**:
- Fix filename case sensitivity
- Fix mod_path configuration
- Reinstall FFNx
- Try different texture format (DDS instead of PNG)

---

### Issue: Game Crashes on Launch

**Symptoms**: Game crashes when starting with modified texture

**Diagnosis**:

1. **Check FFNx.log for errors**:
   - Look for last line before crash
   - Look for texture-related errors

2. **Test without modified texture**:
   - Rename or remove test texture
   - Launch game
   - If works, issue is with texture file

3. **Verify texture file integrity**:
   - Check file size (not 0 bytes)
   - Open in image editor (not corrupted)
   - Verify format (PNG, not mislabeled)

**Solutions**:
- Recreate texture with correct format
- Use simpler modification (color change only)
- Try DDS format instead of PNG
- Check FFNx issue tracker for known bugs

---

### Issue: Modified Font in Some Menus Only

**Symptoms**: Some text shows modified font, other text shows normal font

**This is actually useful information!**

**Diagnosis**:

1. **Multiple font files in use**:
   - Game uses different fonts for different contexts
   - `USFONT_H.TEX` = main font
   - `USFONT_A_H.TEX` = variant A (possibly dialogue)
   - `USFONT_B_H.TEX` = variant B (possibly descriptions)

2. **Resolution-based fonts**:
   - High-res mode uses `*_H.TEX`
   - Low-res mode uses `*_L.TEX`

**Solutions**:
- Modify ALL font variants:
  - `USFONT_H.PNG`
  - `USFONT_A_H.PNG`
  - `USFONT_B_H.PNG`
  - `USFONT_L.PNG`
  - `USFONT_A_L.PNG`
  - `USFONT_B_L.PNG`
- Document which menus use which fonts
- This is expected behavior, not a failure!

---

### Issue: FFNx.log Shows "Texture Not Found"

**Symptoms**: Log shows FFNx trying to load texture but failing

**Diagnosis**:

```
[ERROR] External texture not found: mods/Textures/USFONT_H.PNG
```

**Causes**:
- File doesn't exist at specified path
- Path separator issue (use `/` not `\` in mod_path)
- Case sensitivity on some systems

**Solutions**:
1. Verify file exists:
   ```cmd
   dir "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\mods\Textures\USFONT_H.PNG"
   ```

2. Fix path in FFNx.toml:
   ```toml
   mod_path = "mods/Textures"  # Use forward slashes
   ```

3. Try absolute path:
   ```toml
   mod_path = "C:/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/mods/Textures"
   ```

---

### Issue: Cannot Extract LGP File

**Symptoms**: ulgp fails to extract menu_us.lgp

**Diagnosis**:

1. **File permissions**:
   - LGP file may be read-only
   - Insufficient permissions to write extracted files

2. **Corrupted LGP**:
   - File may be corrupted
   - File may be modified by 7th Heaven

3. **Wrong ulgp version**:
   - Old version may have bugs
   - Download latest version (1.2+)

**Solutions**:
- Run CMD as Administrator
- Remove read-only flag from menu_us.lgp
- Verify LGP file size matches expected (several MB)
- Try Ficedula's LGP Editor (GUI alternative)
- If using 7th Heaven, disable mods temporarily

---

## Next Steps Based on Results

### If Test SUCCEEDS (Modified Font Appears)

**Congratulations! The core concept is proven.**

**Immediate next steps**:

1. **Document success**:
   - Update FINDINGS.md with test results
   - Include screenshots
   - Note which texture files work

2. **Test all font variants**:
   - Modify `USFONT_A_H.PNG` and `USFONT_B_H.PNG`
   - Test low-resolution fonts
   - Document which fonts are used where

3. **Research Japanese font acquisition**:
   - Acquire FF7 Japanese eStore version (if legally possible)
   - Or: Research creating Japanese font textures from scratch
   - Extract `jafont_1.tex` through `jafont_6.tex`

4. **Analyze character mapping**:
   - Understand how 6 Japanese font textures are organized
   - Map FF Text encoding to texture positions
   - Document character→glyph mapping

5. **Contact FFNx developers**:
   - Share test results on Issue #39
   - Ask about best practices for font texture replacement
   - Inquire about TrueType font configuration options

6. **Plan character encoding solution**:
   - Research double-byte encoding implementation
   - Investigate touphScript extension possibilities
   - Consider game executable patching

**Long-term roadmap**:
- Phase 2: Japanese font texture creation/acquisition
- Phase 3: Character encoding extension
- Phase 4: Full integration testing
- Phase 5: Release as 7th Heaven mod

---

### If Test PARTIALLY SUCCEEDS

**Some menus show modified font, others don't.**

**Analysis needed**:

1. **Identify which fonts are used where**:
   - Document menu sections with modified font
   - Document menu sections without modified font
   - Cross-reference with font file variants

2. **Test all font variants**:
   - Modify remaining fonts (`*_A_H.PNG`, `*_B_H.PNG`, etc.)
   - Determine which variant is used in each context

3. **Check for additional font files**:
   - Search menu_us.lgp for other font-related files
   - Check if some text uses different texture files
   - Verify with `save_textures = true` to dump all textures

**Next steps**:
- Same as SUCCESS case, but with extra step:
- Create mapping of font variants to menu contexts
- Ensure all variants are replaced for complete coverage

---

### If Test FAILS (No Visual Change)

**Font appears completely normal despite modifications.**

**Systematic diagnosis**:

1. **Verify FFNx is working at all**:
   - Test with known-working mod (field texture replacement)
   - If other textures override, but fonts don't, fonts may be special case

2. **Check FFNx.log thoroughly**:
   - Look for ANY texture loading messages
   - Look for errors
   - Look for font-related entries

3. **Try different texture format**:
   - Convert PNG to DDS
   - Try keeping original TEX format
   - Test with different image editors

4. **Research FFNx source code**:
   - Search for "menu" or "font" in FFNx source
   - Understand how menu textures are loaded
   - Check if fonts are handled differently

5. **Contact FFNx community**:
   - Post on qhimm forums
   - Comment on FFNx Issue #39
   - Ask if font texture override is supported

**Alternative approaches if texture override doesn't work**:

**Plan B: FFNx Driver Modification**
- Fork FFNx repository
- Add font loading code
- Implement BGFX TrueType font support
- Requires C++ knowledge and collaboration

**Plan C: Game Executable Patching**
- Research where ff7.exe loads fonts
- Patch executable to load different font files
- More invasive, less maintainable

**Plan D: Runtime Injection (Tonberry-style)**
- Create FF7 equivalent of Tonberry
- Hook DirectX texture loading functions
- Inject Japanese fonts at runtime
- Requires reverse engineering skills

---

## Appendices

### Appendix A: Known File Locations

**Font texture files in menu_us.lgp**:
- `USFONT_H.TEX` (high-res main)
- `USFONT_A_H.TEX` (high-res variant A)
- `USFONT_B_H.TEX` (high-res variant B)
- `USFONT_L.TEX` (low-res main)
- `USFONT_A_L.TEX` (low-res variant A)
- `USFONT_B_L.TEX` (low-res variant B)

**Source**: https://wiki.ffrtt.ru/index.php/FF7/Menu_Module

**Japanese font textures** (from Japanese eStore version):
- In `menu_ja.lgp`:
  - `jafont_1.tex`
  - `jafont_2.tex`
  - `jafont_3.tex`
  - `jafont_4.tex`
  - `jafont_5.tex`
  - `jafont_6.tex`

**Source**: FFNx Issue #39

---

### Appendix B: FFNx.toml Reference

**Relevant texture configuration options**:

```toml
# Path to load external textures from
# Relative to FF7 directory or absolute path
mod_path = "mods/Textures"

# Supported texture file extensions
# FFNx will try these formats in order
mod_ext = ["dds", "png"]

# Show debug messages for missing textures
# Useful for identifying texture names
show_missing_textures = false

# Dump all game textures to mod_path
# Use to extract current textures as PNG/DDS
save_textures = false

# Override path for game data files
# Can override entire data directory
override_path = ""
```

**Full documentation**: https://github.com/julianxhokaxhiu/FFNx

---

### Appendix C: Command Reference

**ulgp commands**:
```bash
# Extract entire LGP archive
ulgp -x archive.lgp

# Create LGP from folder
ulgp -c archive.lgp

# Overwrite files in LGP from folder
ulgp -r archive.lgp

# GUI mode (Windows)
ulgp.exe  # Double-click or run without arguments
```

**Windows directory navigation**:
```cmd
# Change directory
cd C:\Path\To\Directory

# List files
dir

# List files with pattern
dir *.tex

# Copy file
copy source.txt destination.txt

# Create directory
mkdir NewFolder
```

---

### Appendix D: Resources

**Tools**:
- ulgp: https://forums.qhimm.com/index.php?topic=12831.0
- FFNx: https://github.com/julianxhokaxhiu/FFNx
- 7th Heaven: https://7thheaven.rocks/

**Documentation**:
- FF7 Menu Module: https://wiki.ffrtt.ru/index.php/FF7/Menu_Module
- LGP Format: https://qhimm-modding.fandom.com/wiki/FF7/LGP_format
- FF Text Encoding: https://ff7-mods.github.io/ff7-flat-wiki/FF7/Text_encoding.html

**Community**:
- qhimm Forums: https://forums.qhimm.com/
- FFNx Issue #39: https://github.com/julianxhokaxhiu/FFNx/issues/39

---

**Document Status**: Ready for Testing
**Next Update**: After test execution
**Maintainer**: Project Team

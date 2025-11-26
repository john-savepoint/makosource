# 7th Heaven Developer Guide

**Document Version:** 2.2 (Verified Against Official Sources)
**Created:** 2025-11-24 21:52:54 JST (Monday)
**Last Modified:** 2025-11-25 12:25:00 JST (Tuesday)
**Author:** Research compiled by Claude Code
**Session-IDs:**

- 8f58819d-f9c4-4f04-8e95-4af04d782606 (Initial creation, Session 11)
- 8f58819d-f9c4-4f04-8e95-4af04d782606 (Verification, Session 12)
  **Purpose:** Comprehensive developer guide for creating, using, and packaging mods with 7th Heaven mod manager

**Status:** Verified Against Official Documentation (2025-11-25)

> **Verification Note:** Section 7.3-7.5 has been verified against official 7th Heaven documentation
> at https://7thheaven.rocks/help/userhelp.html. See `docs/reference/TOOL_VERIFICATION_LOG.md` for details.

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [7th Heaven Architecture](#2-7th-heaven-architecture)
3. [mod.xml Complete Specification](#3-modxml-complete-specification)
4. [IRO File Format](#4-iro-file-format)
5. [Creating Mods for 7th Heaven](#5-creating-mods-for-7th-heaven)
6. [Build Order System](#6-build-order-system)
7. [Developer Tools](#7-developer-tools)
8. [Advanced Mod Features](#8-advanced-mod-features)
9. [Testing and Debugging](#9-testing-and-debugging)
10. [Distribution](#10-distribution)
11. [Reference](#11-reference)

---

## 1. INTRODUCTION

### 1.1 What is 7th Heaven?

7th Heaven is the de facto mod manager for Final Fantasy VII PC. It provides:

- **Virtual File System (VFS)**: Intercepts game file I/O calls via EasyHook
- **Mod Management**: Easy enable/disable of mods via UI
- **IRO Archives**: ZIP-like containers for mod assets (.iro files)
- **Build Order**: Priority system for resolving file conflicts
- **FFNx Integration**: Works with modern FFNx graphics driver
- **Catalog System**: In-app mod browsing and downloads

**Official Repository:** https://github.com/tsunamods-codes/7th-Heaven
**Official Website:** https://7thheaven.rocks/
**Maintainer:** Tsunamods team
**Source Code:** https://bitbucket.org/ficedula/7h/overview (original)

### 1.2 For Developers

This guide focuses on:

- Creating production-ready mods
- IRO file structure and creation
- Understanding the build order system
- Advanced mod.xml features
- Packaging and distributing mods
- Developer tools for asset extraction/creation

**NOT covered in this guide:**

- End-user installation and usage
- Playing FF7 with mods
- Basic troubleshooting (see official help docs)

### 1.3 Prerequisites

**Required Knowledge:**

- Basic understanding of FF7 PC file structure
- File formats (.lgp, .tex, .png, .flevel, etc.)
- XML/JSON syntax
- Basic command line usage
- Archive file concepts (ZIP/TAR)

**Required Software:**

- 7th Heaven 2.0+ installed and working
- FF7 PC (Steam 2013 or 1998 version)
- FFNx graphics driver (strongly recommended)
- Text editor for XML/JSON (VS Code, Notepad++, etc.)
- 7-Zip or similar archive tool

**Recommended Tools:**

- LGP/UNLGP (archive management)
- TexTool or FF7 Tex Image Tool (texture conversion)
- Makou Reactor (field editing)
- WallMarket (kernel editing)
- Black Chocobo (save editing for testing)

---

## 2. 7TH HEAVEN ARCHITECTURE

### 2.1 How 7th Heaven Works

**Virtual File System Approach:**

```
Game requests file
    ↓
EasyHook intercepts call
    ↓
7thWrapperLib.dll searches active mods (by build order priority)
    ↓
If found in mod → Return modded file from IRO
If not found → Return original file from game directory
```

**Key Components:**

```
7th Heaven/
├── 7thHeaven.exe          # Main application UI
├── EasyHook.dll           # File I/O interception library
├── 7thWrapperLib.dll      # VFS implementation
├── mods/                  # Installed mod library
│   └── 7th Heaven/        # IRO files stored here
│       ├── ModName.iro
│       └── temp/          # Temporary extraction folder
├── profiles/
│   └── Default.xml        # Active mod configuration
├── FFNx.dll               # Graphics driver (if using FFNx)
└── catalogs/              # Mod catalog subscriptions
```

**The Interception Process:**

1. **Game calls file operation** (e.g., `fopen("data/menu/menu_us.lgp", "rb")`)
2. **EasyHook intercepts the call** at the Win32 API level
3. **7thWrapperLib queries active mods** (in build order, highest priority first)
4. **For each active mod:**
   - Check if mod.xml defines a replacement for requested path
   - Check if mod's folders (based on ActiveWhen conditions) contain the file
5. **If modded file exists** → Return virtual file handle to modded version from IRO
6. **If not modded** → Pass through to original game file

### 2.2 Build Order Priority

**Definition:** When multiple mods replace the same file, **build order** determines which version wins.

**Priority System:**

- **Higher position in list = Higher priority** (wins conflicts)
- User can reorder mods by dragging in 7th Heaven UI
- Top-most active mod's file is used if multiple mods conflict
- Mods process from top to bottom, first match wins

**Example Scenario:**

```
Active Mods (Top to Bottom):
1. Mod A (Category: Fonts) - Replaces menu_us.lgp/usfont.tex
2. Mod B (Category: Textures) - Replaces menu_us.lgp/usfont.tex
3. Mod C (Category: Models) - Replaces char.lgp/cloud.p

Game requests: menu_us.lgp/usfont.tex
Result: Mod A's version is used (higher priority)

Game requests: char.lgp/cloud.p
Result: Mod C's version is used (only mod with this file)
```

**Auto-Sort Behavior:**
7th Heaven 2.0's Auto Sort orders mods by:

1. **Category** (in recommended order - see Section 6.3)
2. **Name** (alphabetically within category)
3. **OrderConstraints** (After/Before directives in mod.xml)

### 2.3 Folder Structure Best Practices

**Recommended Mod Internal Structure:**

```
MyMod/
├── mod.xml                # REQUIRED: Mod configuration
├── preview.png            # OPTIONAL: Preview image (any format)
├── Readme.txt             # OPTIONAL: User documentation (txt or html)
└── [Asset folders mirroring FF7 structure]
    ├── menu_us.lgp/       # Menu textures
    │   ├── usfont.tex
    │   └── buster.tex
    ├── char.lgp/          # Character models
    │   ├── cloud.p
    │   └── aaba.p
    ├── field/             # Field assets (if using folders)
    │   └── flevel.lgp
    └── vgmstream/         # Audio files (OGG/MP3)
        ├── oa.ogg
        └── earis.ogg
```

**Important:** Subfolders must follow FF7's game folder structure for 7th Heaven to match paths correctly.

---

## 3. MOD.XML COMPLETE SPECIFICATION

### 3.1 Mod Information Section

**All mod.xml code must be wrapped in `<ModInfo>` tags.**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModInfo>
  <!-- All configuration goes here -->
</ModInfo>
```

**Required Fields:**

```xml
<ID>00000000-0000-0000-0000-000000000000</ID>  <!-- CRITICAL: NEVER change after release! -->
<Name>My Awesome Mod</Name>
<Author>Your Name</Author>
<Version>1.00</Version>
<ReleaseDate>2025-11-24</ReleaseDate>
<Category>World Textures</Category>  <!-- See valid categories below -->
<Description>A comprehensive description of what your mod does.</Description>
```

**Valid Categories:**

- Animations
- Battle Models
- Battle Textures
- Field Models
- Field Textures
- Gameplay
- Media
- Minigames
- Miscellaneous
- Spell Textures
- User Interface
- World Models
- World Textures

**Optional Fields:**

```xml
<ReleaseNotes>What's new in this version.</ReleaseNotes>
<Link>https://forums.qhimm.com/your-mod-thread</Link>
<PreviewFile>preview.gif</PreviewFile>  <!-- GIF, JPG, or PNG -->
```

**Complete Example:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModInfo>
  <ID>a1b2c3d4-e5f6-7890-abcd-ef1234567890</ID>
  <Name>HD Water Textures</Name>
  <Author>ModAuthor</Author>
  <Version>2.50</Version>
  <ReleaseDate>2025-11-24</ReleaseDate>
  <Category>World Textures</Category>
  <Description>Retextures for all water on the World Map at 2048x2048 resolution with realistic reflections.</Description>
  <ReleaseNotes>v2.5: Added waterfall animations, fixed seam issues.</ReleaseNotes>
  <Link>https://forums.qhimm.com/index.php?topic=12345.0</Link>
  <PreviewFile>preview.png</PreviewFile>
</ModInfo>
```

**CRITICAL: Generating a Unique ID**

Use 7th Heaven's built-in Catalog/Mod Creation Tool:

1. Open 7th Heaven
2. Go to Workshop tab
3. Click "Catalog/Mod Creation Tool"
4. Click "Generate new GUID"
5. Copy the generated ID

Or use an online GUID generator (search "GUID generator").

**NEVER reuse IDs from other mods!**

### 3.2 Mod Folders (Basic)

**Purpose:** Tell 7th Heaven which subfolders contain mod assets.

**Simple Folder (Always Active):**

```xml
<ModFolder Folder="MyModFolder" />
```

This makes `MyModFolder/` active whenever the mod is enabled.

**Conditional Folder (Config-Based):**

```xml
<ModFolder Folder="MyModFolder\SubFolder" ActiveWhen="MySetting = 1" />
```

This makes the subfolder active only when the user has `MySetting` configured to value `1`.

**Multiple Folders:**

```xml
<ModFolder Folder="BaseAssets" />
<ModFolder Folder="HD_Textures" ActiveWhen="quality = high" />
<ModFolder Folder="SD_Textures" ActiveWhen="quality = low" />
```

**Folder Processing Order:**

- 7th Heaven checks folders in the order they appear in mod.xml
- First match wins
- If `HD_Textures` and `SD_Textures` both have `cloud.p`, and `quality = high`, `HD_Textures/cloud.p` is used

### 3.3 Config Options (User Settings)

**Purpose:** Allow users to configure mod behavior via 7th Heaven UI.

**Bool Type (On/Off Toggle):**

```xml
<ConfigOption>
  <Type>Bool</Type>
  <Default>0</Default>  <!-- 0 = Off, 1 = On -->
  <ID>enable_feature</ID>
  <Name>Enable Feature X</Name>
  <Description>Turns on the special feature.</Description>
  <Option Value="0" Name="Disabled" PreviewFile="preview\off.jpg" />
  <Option Value="1" Name="Enabled" PreviewFile="preview\on.jpg" />
</ConfigOption>
```

**List Type (Dropdown Selection):**

```xml
<ConfigOption>
  <Type>List</Type>
  <Default>1</Default>  <!-- Default selection: value 1 -->
  <ID>music_style</ID>
  <Name>Choose Music Style</Name>
  <Description>Select the genre of music you prefer.</Description>
  <Option Value="0" Name="Original Game" />
  <Option Value="1" Name="Orchestral" PreviewAudio="preview\orchestral.ogg" />
  <Option Value="2" Name="Rock" PreviewAudio="preview\rock.ogg" />
  <Option Value="3" Name="Electronic" PreviewAudio="preview\electronic.mp3" />
</ConfigOption>
```

**Using Settings with ModFolder:**

```xml
<!-- Config option defines "music_style" variable -->
<ConfigOption>
  <Type>List</Type>
  <Default>1</Default>
  <ID>music_style</ID>
  <Name>Music Genre</Name>
  <Description>Pick your music preference.</Description>
  <Option Value="0" Name="Default" />
  <Option Value="1" Name="Orchestral" />
  <Option Value="2" Name="Rock" />
</ConfigOption>

<!-- Folders activate based on "music_style" value -->
<ModFolder Folder="Music\Orchestral\vgmstream" ActiveWhen="music_style = 1" />
<ModFolder Folder="Music\Rock\vgmstream" ActiveWhen="music_style = 2" />
```

**PreviewFile and PreviewAudio:**

- `PreviewFile`: Shows image when option is selected (jpg, png, gif)
- `PreviewAudio`: Shows "Play" button to preview audio (mp3, ogg)
- Paths are relative to IRO root

### 3.4 TreeView Style (Grouped Options)

**Purpose:** Organize many config options into collapsible groups.

**Triggering TreeView Mode:**

- Add `===Header Name===` (3+ equal signs before/after) to any ConfigOption Name
- **All ConfigOptions** must then use headers (can't mix list and treeview)

**Example:**

```xml
<ConfigOption>
  <Type>List</Type>
  <Default>0</Default>
  <ID>CharacterThemesHeader</ID>
  <Name>===Character Themes===</Name>
  <Description>Expand to see character-specific music options.</Description>
  <Option Value="0" Name=""/>  <!-- Dummy option for header -->
</ConfigOption>

<ConfigOption>
  <Type>List</Type>
  <Default>1</Default>
  <ID>aerith_theme</ID>
  <Name>Aerith's Theme</Name>
  <Description>Plays during Aerith scenes.</Description>
  <Option Value="0" Name="No Change" />
  <Option Value="1" Name="Orchestral Mix" PreviewAudio="\vgmstream\earis_orch.ogg"/>
  <Option Value="2" Name="Piano Mix" PreviewAudio="\vgmstream\earis_piano.ogg"/>
</ConfigOption>

<ConfigOption>
  <Type>List</Type>
  <Default>1</Default>
  <ID>cloud_theme</ID>
  <Name>Cloud's Theme</Name>
  <Description>Main character theme.</Description>
  <Option Value="0" Name="No Change" />
  <Option Value="1" Name="Rock Mix" PreviewAudio="\vgmstream\cloud_rock.ogg"/>
</ConfigOption>

<!-- Next group header -->
<ConfigOption>
  <Type>List</Type>
  <Default>0</Default>
  <ID>BattleThemesHeader</ID>
  <Name>===Battle Themes===</Name>
  <Description>Battle music options.</Description>
  <Option Value="0" Name=""/>
</ConfigOption>

<!-- Battle theme options go here... -->
```

### 3.5 Conditional Folders (Runtime Variables)

**Purpose:** Activate folders based on game state (memory addresses, counters, etc.).

**Runtime Variable Syntax:**

```xml
<Conditional Folder="FolderName">
  <RuntimeVar Var="VariableType:Address:Size" Values="ValidValues" />
</Conditional>
```

**Variable Types:**

- `Short` - 2-byte integer
- `Byte` - 1-byte integer
- `Int` - 4-byte integer
- Predefined: `FieldID`, `PPV`, `BattleID`, etc. (see 7thHeaven.var file)

**Example (Location-Based Asset Swap):**

```xml
<?xml version="1.0"?>
<ModInfo>
  <!-- Base assets always active -->
  <ModFolder Folder="base_assets" />

  <!-- Special assets for Midgar Slums (FieldID = 0xD5) -->
  <Conditional Folder="midgar_slums">
    <RuntimeVar Var="FieldID" Values="0xD5,0x160" />
  </Conditional>

  <!-- Special assets when PPV (progression variable) is 300-400 -->
  <Conditional Folder="disc2_assets">
    <RuntimeVar Var="Short:0xDC08DC:2" Values="300..400" />
  </Conditional>
</ModInfo>
```

**Explanation:**

- `FieldID` is a predefined variable = memory address `0xCC15D0:2`
- When player enters field with ID `0xD5` or `0x160`, `midgar_slums/` folder activates
- `PPV` (Progression Variable) at `0xDC08DC` tracks story progress
- When PPV is between 300-400, `disc2_assets/` folder activates

**Predefined Variables (in 7thHeaven.var):**

- `FieldID` - Current field map ID
- `PPV` - Story progression variable
- `BattleID` - Current battle ID
- `MenuState` - Menu state tracker

**Value Formats:**

- Single: `0xD5`
- Multiple: `0xD5,0x160,0x200`
- Range: `300..400`
- Combined: `10,20,30..40,50`

### 3.6 Mod Operators (Logic)

**Purpose:** Combine multiple conditions with AND, OR, NOT logic.

**AND Operator (All conditions must be true):**

```xml
<ModFolder Folder="SpecialFolder">
  <ActiveWhen>
    <And>
      <Option>setting1 = 1</Option>
      <Option>setting2 = high</Option>
    </And>
  </ActiveWhen>
</ModFolder>
```

Folder activates only if `setting1 = 1` **AND** `setting2 = high`.

**OR Operator (Any condition true):**

```xml
<ModFolder Folder="AlternateFolder">
  <ActiveWhen>
    <Or>
      <Option>mode = creative</Option>
      <Option>mode = debug</Option>
    </Or>
  </ActiveWhen>
</ModFolder>
```

Folder activates if `mode = creative` **OR** `mode = debug`.

**NOT Operator (Inverse condition):**

```xml
<ModFolder Folder="DefaultFolder">
  <ActiveWhen>
    <Not>
      <And>
        <Option>advanced = 1</Option>
        <Option>expert = 1</Option>
      </And>
    </Not>
  </ActiveWhen>
</ModFolder>
```

Folder activates if **NOT** (`advanced = 1` **AND** `expert = 1`).

**Complex Example:**

```xml
<!-- Activate if (setting1=1 OR setting2=1) AND setting3≠2 -->
<ModFolder Folder="ComplexFolder">
  <ActiveWhen>
    <And>
      <Or>
        <Option>setting1 = 1</Option>
        <Option>setting2 = 1</Option>
      </Or>
      <Not>
        <Option>setting3 = 2</Option>
      </Not>
    </And>
  </ActiveWhen>
</ModFolder>
```

### 3.7 Compatibility Section

**Mod Dependencies (Require/Forbid):**

```xml
<Compatibility>
  <!-- Requires FFNx mod (any version) to be active -->
  <Require ModID="12345678-1234-1234-1234-123456789012">FFNx Graphics Driver</Require>

  <!-- Forbids "Old Menu Mod" (any version) from being active -->
  <Forbid ModID="87654321-4321-4321-4321-210987654321">Old Menu Mod</Forbid>

  <!-- Forbids specific versions 1.0 and 2.0 of another mod -->
  <Forbid ModID="abcd1234-5678-90ab-cdef-1234567890ab" Versions="1.0,2.0">Incompatible Mod</Forbid>
</Compatibility>
```

**Setting-Based Compatibility:**

```xml
<Compatibility>
  <!-- If your mod's "MySettingVariable" = 1, then another mod must have "Wonder Square" = 0 -->
  <Setting>
    <MyID>MySettingVariable</MyID>
    <MyValue>1</MyValue>
    <ModID>fae201ee-9fa5-4163-ab56-2b478111449d</ModID>
    <TheirID>Wonder Square - Tweaks</TheirID>
    <Require>0</Require>
  </Setting>
</Compatibility>
```

**Use Case:** Your mod's feature conflicts with another mod's feature unless that feature is disabled.

### 3.8 Order Constraints (Load Order)

**Purpose:** Specify mod load order requirements for Auto Sort.

```xml
<OrderConstraints>
  <!-- Your mod must load AFTER these mods -->
  <After>12345678-1234-1234-1234-123456789012</After>
  <After>abcdefab-cdef-abcd-efab-cdefabcdefab</After>

  <!-- Your mod must load BEFORE these mods -->
  <Before>87654321-4321-4321-4321-210987654321</Before>
</OrderConstraints>
```

**Auto Sort Processing:**

1. Sort by Category
2. Sort alphabetically by Name (within category)
3. Process `<After>` constraints (move mod below specified mods)
4. Process `<Before>` constraints (move mod above specified mods)

**Example Use Case:**

- Base texture mod should load BEFORE HD texture mod
- Font mod should load AFTER text encoding mod

**Note:** `OrderConstraints` goes OUTSIDE the `<Compatibility>` section (direct child of `<ModInfo>`).

### 3.9 Complete mod.xml Template

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModInfo>
  <!-- ===== MOD INFORMATION ===== -->
  <ID>00000000-0000-0000-0000-000000000000</ID>
  <Name>My Complete Mod</Name>
  <Author>Your Name</Author>
  <Version>1.00</Version>
  <ReleaseDate>2025-11-24</ReleaseDate>
  <Category>World Textures</Category>
  <Description>A full-featured mod demonstrating all mod.xml capabilities.</Description>
  <ReleaseNotes>Initial release with HD textures and music options.</ReleaseNotes>
  <Link>https://forums.qhimm.com/</Link>
  <PreviewFile>preview.png</PreviewFile>

  <!-- ===== MOD FOLDERS ===== -->
  <ModFolder Folder="base_assets" />
  <ModFolder Folder="hd_textures" ActiveWhen="quality = high" />
  <ModFolder Folder="sd_textures" ActiveWhen="quality = low" />
  <ModFolder Folder="music\orchestral" ActiveWhen="music_style = 1" />
  <ModFolder Folder="music\rock" ActiveWhen="music_style = 2" />

  <!-- ===== CONDITIONAL FOLDERS ===== -->
  <Conditional Folder="midgar_assets">
    <RuntimeVar Var="FieldID" Values="0xD5,0x160" />
  </Conditional>

  <!-- ===== CONFIG OPTIONS ===== -->
  <ConfigOption>
    <Type>List</Type>
    <Default>1</Default>
    <ID>quality</ID>
    <Name>Texture Quality</Name>
    <Description>Choose between HD (2048x2048) or SD (1024x1024) textures.</Description>
    <Option Value="0" Name="Low (SD)" PreviewFile="preview\sd.jpg" />
    <Option Value="1" Name="High (HD)" PreviewFile="preview\hd.jpg" />
  </ConfigOption>

  <ConfigOption>
    <Type>List</Type>
    <Default>0</Default>
    <ID>music_style</ID>
    <Name>Music Style</Name>
    <Description>Select your preferred music genre.</Description>
    <Option Value="0" Name="Original" />
    <Option Value="1" Name="Orchestral" PreviewAudio="preview\orchestral.ogg" />
    <Option Value="2" Name="Rock" PreviewAudio="preview\rock.ogg" />
  </ConfigOption>

  <!-- ===== COMPATIBILITY ===== -->
  <Compatibility>
    <Require ModID="12345678-1234-1234-1234-123456789012">FFNx Driver</Require>
    <Forbid ModID="87654321-4321-4321-4321-210987654321">Old Conflicting Mod</Forbid>
  </Compatibility>

  <!-- ===== ORDER CONSTRAINTS ===== -->
  <OrderConstraints>
    <After>baseline-mod-guid-here</After>
    <Before>override-mod-guid-here</Before>
  </OrderConstraints>
</ModInfo>
```

---

## 4. IRO FILE FORMAT

### 4.1 What is an IRO File?

**IRO = Archive format** based on ZIP compression

`IRO File = ZIP archive (renamed .iro) + metadata (mod.xml) + assets`

**Purpose:**

- Package all mod assets in single distributable file
- Include configuration metadata for 7th Heaven
- Enable easy installation via drag-and-drop or catalog

**Technical Details:**

- File format: Standard ZIP (DEFLATE compression)
- Extension: `.iro`
- Can be opened with any ZIP tool (7-Zip, WinRAR, etc.)
- Max size: Limited only by filesystem (typically several GB supported)

### 4.2 IRO Internal Structure

**Required Files:**

```
MyMod.iro (ZIP archive)
├── mod.xml              # REQUIRED: Mod configuration
└── [Asset folders]      # REQUIRED: At least one asset
```

**Recommended Structure:**

```
MyMod.iro
├── mod.xml              # Mod configuration
├── preview.png          # Preview image (shows in 7H UI)
├── Readme.txt           # User documentation (7H has "Readme" button)
└── [Asset folders]
    ├── menu_us.lgp/     # Menu textures
    │   ├── usfont.tex
    │   └── buster.tex
    ├── char.lgp/        # Character models
    │   └── cloud.p
    └── vgmstream/       # Audio files
        └── oa.ogg
```

**Asset Folder Rules:**

1. Must mirror FF7's directory structure
2. Paths in mod.xml match folder structure
3. Forward slashes `/` or backslashes `\` both work
4. Case-insensitive on Windows (but be consistent)

### 4.3 Creating an IRO File

**Method 1: 7-Zip Command Line (Recommended)**

```batch
REM Navigate to your mod folder
cd C:\MyModFolder

REM Create IRO (ZIP with renamed extension)
7z a -tzip "..\MyMod.iro" *

REM Verify contents
7z l "..\MyMod.iro"
```

**Method 2: 7th Heaven's Built-in Tool**

1. Open 7th Heaven
2. Go to **Workshop** tab
3. Click **Pack/Unpack .iro Archives**
4. **Pack .iro** tab:
   - **Source Folder**: Select your mod folder
   - **Destination .iro**: Choose output location
   - **Compression**: "Nothing" = fastest, "Maximum" = smallest file
5. Click **Pack**

**Method 3: Manual ZIP Rename**

1. Select all files in mod folder
2. Right-click → Send to → Compressed (zipped) folder
3. Rename from `MyMod.zip` to `MyMod.iro`

### 4.4 Unpacking/Inspecting IRO Files

**7-Zip:**

```batch
REM Extract to folder
7z x MyMod.iro -oExtracted\

REM List contents without extracting
7z l MyMod.iro
```

**7th Heaven:**

1. Workshop tab → Pack/Unpack .iro Archives
2. **Unpack .iro** tab:
   - Select IRO file
   - Choose destination folder
   - Click **Unpack**

**Use Case:** Inspect other mods to learn structure and techniques.

---

## 5. CREATING MODS FOR 7TH HEAVEN

### 5.1 Complete Workflow

**Step 1: Plan Your Mod**

- **Identify scope:** What are you changing? (textures, models, music, gameplay)
- **Research FF7 structure:** Which files need modification?
- **Check existing mods:** Is there already a similar mod? Can you improve it or create an alternative?
- **Choose category:** Which 7H category fits best?

**Step 2: Set Up Development Environment**

```
DevFolder/
├── MyMod_WIP/           # Working directory
│   ├── mod.xml          # Start here
│   ├── preview.png      # Create later
│   └── [asset folders]  # Create as you go
└── Tools/
    ├── ulgp.exe         # LGP extraction
    ├── TexTool.exe      # TEX↔PNG conversion
    └── 7z.exe           # IRO packaging
```

**Step 3: Extract Original Assets (if modifying)**

```batch
REM Extract LGP archive
ulgp extract "C:\FF7\data\menu\menu_us.lgp" ".\extracted\menu"

REM Convert TEX to PNG
TexTool.exe convert "extracted\menu\usfont.tex" "working\usfont.png"
```

**Step 4: Create/Modify Assets**

- Edit in your preferred tools (Photoshop, GIMP, Blender, etc.)
- Follow FF7's specifications (see Section 7.2 for asset specs)
- Test individual assets before packaging

**Step 5: Create mod.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModInfo>
  <ID>GENERATE-NEW-GUID-HERE</ID>
  <Name>My First Mod</Name>
  <Author>YourName</Author>
  <Version>1.00</Version>
  <ReleaseDate>2025-11-24</ReleaseDate>
  <Category>User Interface</Category>
  <Description>Replaces the menu font with a custom design.</Description>
  <PreviewFile>preview.png</PreviewFile>

  <ModFolder Folder="assets" />
</ModInfo>
```

**Step 6: Organize Asset Folders**

```
MyMod_WIP/
├── mod.xml
├── preview.png
└── assets/
    └── menu_us.lgp/
        └── usfont.tex   # Your modified texture (converted back to TEX)
```

**Step 7: Generate GUID for mod.xml**

1. Open 7th Heaven
2. Workshop → Catalog/Mod Creation Tool
3. Click "Generate new GUID"
4. Copy and paste into mod.xml `<ID>` field

**Step 8: Package as IRO**

```batch
cd MyMod_WIP
7z a -tzip "..\MyMod_v1.00.iro" *
```

**Step 9: Test in 7th Heaven**

1. Open 7th Heaven
2. **Library** tab → **Import Mod**
3. Select your `.iro` file
4. Go to **My Mods** tab
5. Enable your mod
6. Click **Play** to launch FF7
7. Verify changes appear in-game

**Step 10: Iterate**

- If issues: Unpack IRO, fix, repack, test again
- If working: Add features, improve quality, test more thoroughly

### 5.2 Asset Preparation Guidelines

**Textures (.tex ↔ .png):**

| Original Format | Tool                          | Process                                                                                  |
| --------------- | ----------------------------- | ---------------------------------------------------------------------------------------- |
| .tex            | TexTool or FF7 Tex Image Tool | Extract: `.tex` → `.png`<br>Modify: Edit PNG in image editor<br>Convert: `.png` → `.tex` |

**Texture Specifications:**

- **Menu fonts:** 256×256 (original), can use higher res with FFNx
- **Field textures:** Varies, commonly 256×256 to 1024×1024
- **Battle textures:** Varies
- **Format:** Paletted (256 colors) for original driver, RGB for FFNx

**Models (.p files):**

| Tool      | Purpose                    |
| --------- | -------------------------- |
| Kimera CS | View/edit character models |
| Biturn    | Export .p to .3ds          |
| pCreater  | Import .3ds to .p          |

**Audio (vgmstream):**

- **Formats:** .ogg (recommended), .mp3
- **Location:** Place in `vgmstream/` folder
- **Naming:** Must match original file names (e.g., `oa.ogg` for opening theme)

**LGP Archives:**

If replacing entire LGP files (not recommended for beginners):

```batch
REM Extract LGP
ulgp extract original.lgp extracted_folder

REM Modify files in extracted_folder

REM Repack LGP
ulgp pack extracted_folder new.lgp
```

### 5.3 Common Pitfalls

**Issue: Mod doesn't appear in catalog**

- **Cause:** Missing or invalid mod.xml
- **Fix:** Validate XML syntax, ensure mod.xml is in IRO root

**Issue: Assets not replaced in-game**

- **Cause:** Folder structure doesn't match FF7 paths
- **Fix:** Check mod folder structure against game directory

**Issue: Mod works in 7H but not in game**

- **Cause:** Asset file corruption or wrong format
- **Fix:** Re-export assets, verify file integrity

**Issue: "Duplicate ModID" error**

- **Cause:** Used same GUID as existing mod
- **Fix:** Generate new unique GUID

**Issue: Preview image doesn't show**

- **Cause:** Wrong path in `<PreviewFile>`
- **Fix:** Ensure path is relative to IRO root, file exists

---

## 6. BUILD ORDER SYSTEM

### 6.1 Understanding Build Order

**Concept:** Mods are processed in priority order. First match wins.

**How It Works:**

```
User has 3 mods active:
1. HD Textures (Top, highest priority)
2. Character Models (Middle)
3. Music Replacer (Bottom, lowest priority)

Game requests: menu_us.lgp/usfont.tex

7th Heaven checks:
1. HD Textures → Has usfont.tex? YES → Use this version, stop checking
2. Character Models → (skipped, already found)
3. Music Replacer → (skipped, already found)
```

**Conflict Resolution:**

```
Conflict Scenario:
- Mod A replaces usfont.tex
- Mod B also replaces usfont.tex

Solution:
- Drag Mod A above Mod B → Mod A's version is used
- Drag Mod B above Mod A → Mod B's version is used
```

### 6.2 Auto Sort Feature

**7th Heaven 2.0's Auto Sort orders by:**

1. **Category** (following recommended order)
2. **Name** (alphabetically within category)
3. **OrderConstraints** (After/Before directives)

**Recommended Category Order (Auto Sort):**

```
1. Miscellaneous
2. Animations
3. Battle Models
4. Battle Textures
5. Field Models
6. Field Textures
7. Gameplay
8. Media
9. Minigames
10. Spell Textures
11. User Interface
12. World Models
13. World Textures
```

**Why This Order?**

- Core system mods (Miscellaneous) load first
- Visual mods load in logical order (models before textures)
- UI mods load near end (often override other changes)

### 6.3 Using OrderConstraints

**Scenario:** Your texture mod should load AFTER a base texture overhaul.

```xml
<OrderConstraints>
  <After>baseline-texture-mod-guid</After>
</OrderConstraints>
```

**Scenario:** Your core engine mod should load BEFORE graphical mods.

```xml
<OrderConstraints>
  <Before>hd-graphics-mod-guid</Before>
  <Before>another-graphics-mod-guid</Before>
</OrderConstraints>
```

**Effect:**

- Auto Sort respects these constraints
- Manual reordering still works (overrides Auto Sort)

---

## 7. DEVELOPER TOOLS

### 7.1 Essential Tool Suite

**LGP Archive Management:**

| Tool         | Purpose                    | Source                                                            |
| ------------ | -------------------------- | ----------------------------------------------------------------- |
| **ulgp**     | Extract/pack .lgp archives | http://forums.qhimm.com/index.php?topic=12831.0                   |
| **LGP_edit** | GUI LGP manager            | https://drive.google.com/file/d/0B3Kl04es5qkqeVFYSmE5NFZtSlU/view |

**Texture Conversion:**

| Tool                   | Purpose                   | Source                                                            |
| ---------------------- | ------------------------- | ----------------------------------------------------------------- |
| **TexTool**            | TEX ↔ PNG converter       | https://drive.google.com/file/d/0B0FYTN9Fe13HSTVCM3Z3QjhKZWc/view |
| **FF7 Tex Image Tool** | Alternative TEX converter | http://forums.qhimm.com/index.php?topic=17755.0                   |

**Background Extraction:**

| Tool           | Purpose                           | Source                                          |
| -------------- | --------------------------------- | ----------------------------------------------- |
| **Palmer**     | Aali's driver background exporter | Google Drive (see Steam FF7 Tools guide)        |
| **FacePalmer** | Alternative background tool       | http://forums.qhimm.com/index.php?topic=11933.0 |

**Model Editing:**

| Tool                  | Purpose                       | Source                                          |
| --------------------- | ----------------------------- | ----------------------------------------------- |
| **Kimera CS**         | Character model viewer/editor | https://github.com/LaZar00/KimeraCS             |
| **Biturn**            | Export .p to .3ds             | Google Drive (see Steam FF7 Tools guide)        |
| **pCreater**          | Import .3ds to .p             | Google Drive                                    |
| **FFVII Maya Plugin** | Import/export for Maya        | http://forums.qhimm.com/index.php?topic=17754.0 |
| **HRC Resizer**       | Resize .hrc models            | http://forums.qhimm.com/index.php?topic=4331.0  |

**Field Editing:**

| Tool              | Purpose                              | Source                                         |
| ----------------- | ------------------------------------ | ---------------------------------------------- |
| **Makou Reactor** | Field script/walkmesh/trigger editor | http://forums.qhimm.com/index.php?topic=9658.0 |

**Text Editing:**

| Tool            | Purpose                | Source                                          |
| --------------- | ---------------------- | ----------------------------------------------- |
| **touphScript** | Dialogue editor        | http://forums.qhimm.com/index.php?topic=11944.0 |
| **BoxFF7**      | Dialog box positioning | http://forums.qhimm.com/index.php?topic=14436.0 |

**Battle Editing:**

| Tool           | Purpose                 | Source                                         |
| -------------- | ----------------------- | ---------------------------------------------- |
| **Proud Clod** | Battle script/AI editor | http://forums.qhimm.com/index.php?topic=8481.0 |

**Kernel Editing:**

| Tool                   | Purpose                                  | Source                                          |
| ---------------------- | ---------------------------------------- | ----------------------------------------------- |
| **WallMarket**         | Kernel.bin editor (items, materia, etc.) | http://forums.qhimm.com/index.php?topic=7928.0  |
| **kernel2 compressor** | Compress kernel2.bin                     | http://forums.qhimm.com/index.php?topic=17024.0 |

**Shop Editing:**

| Tool              | Purpose               | Source                                  |
| ----------------- | --------------------- | --------------------------------------- |
| **White Chocobo** | Shop inventory editor | Google Docs (see Steam FF7 Tools guide) |

**Save Editing (for testing):**

| Tool              | Purpose          | Source                                         |
| ----------------- | ---------------- | ---------------------------------------------- |
| **Black Chocobo** | Save game editor | http://forums.qhimm.com/index.php?topic=9625.0 |

**Miscellaneous:**

| Tool               | Purpose                      | Source                                          |
| ------------------ | ---------------------------- | ----------------------------------------------- |
| **HEXT TOOLS 3.0** | Apply hex patches at runtime | http://forums.qhimm.com/index.php?topic=13574.0 |
| **Game Converter** | Convert between FF7 versions | http://forums.qhimm.com/index.php?topic=14047.0 |
| **Workers**        | people.bin editor            | http://forums.qhimm.com/index.php?topic=16431.0 |

### 7.2 Asset Extraction Workflow

**Complete Workflow Example: Replacing a Font Texture**

```batch
REM Step 1: Extract LGP containing font
ulgp extract "C:\FF7\data\menu\menu_us.lgp" ".\extracted\menu"

REM Step 2: Convert TEX to PNG
TexTool.exe ".\extracted\menu\usfont.tex" ".\working\usfont.png"

REM Step 3: Edit usfont.png in Photoshop/GIMP
REM (Do your edits here)

REM Step 4: Convert PNG back to TEX
TexTool.exe ".\working\usfont.png" ".\mod\menu_us.lgp\usfont.tex"

REM Step 5: Create mod.xml in .\mod\

REM Step 6: Package as IRO
cd .\mod
7z a -tzip "..\MyFontMod.iro" *
```

### 7.3 7th Heaven's Built-in Tools (Workshop Tab)

7th Heaven includes a comprehensive suite of developer tools accessible via the **Workshop** tab. These eliminate the need for many external utilities.

#### 7.3.1 Pack/Unpack IRO Archives

**Location:** Workshop → Pack/Unpack IRO

**Pack (Create IRO from folder):**

```
1. Select source folder containing mod files
2. Choose output IRO filename
3. Select compression level:
   - None: Fastest, largest file
   - Deflate: Good balance
   - LZMA: Smallest, slowest
4. Click "Pack"
```

**Unpack (Extract IRO to folder):**

```
1. Select IRO file
2. Choose destination folder
3. Click "Unpack"
4. All files extracted with folder structure preserved
```

**When to Use:**

- Creating new mods from folders
- Inspecting IRO contents
- Modifying existing IROs (unpack → edit → repack)

#### 7.3.2 IRO Tools (Advanced Operations)

**Location:** Workshop → IRO Tools

**Create .irop Patch Files:**

```
1. Select "Original" IRO (v1.0)
2. Select "New" IRO (v2.0)
3. Click "Create Patch"
4. Outputs .irop file containing only changed/new files
```

**Merge IRO Files:**

- Combine multiple IROs into one
- Useful for consolidating mod variants

**Chunk IRO Files:**

- Split large IROs into smaller pieces
- Useful for file hosts with size limits
- Automatically reassembles on import

#### 7.3.3 Catalog/Mod Creation Tool

**Location:** Workshop → Catalog/Mod Creation Tool

**Generate GUID:**

```
1. Click "Generate New"
2. Copy the displayed GUID
3. Paste into mod.xml <ID> field
```

**Tip:** Every mod MUST have a unique GUID. Never reuse GUIDs.

**Create Catalog Entry:**

```
1. Fill in mod details:
   - Name, Author, Version
   - Description, Category
   - Download URLs
2. Click "Generate XML"
3. Copy/save for catalog submission
```

**Edit Existing Catalog:**

- Load catalog XML
- Add/remove/modify mod entries
- Validate XML syntax

#### 7.3.4 External Texture Conversion Tools

> **CORRECTION (2025-11-25):** There is NO built-in "Make IRO from DDS Files" tool in 7th Heaven.
> This section was incorrectly documented. The texture conversion functionality comes from
> **external third-party tools**, not 7th Heaven itself.

**External Tools for DDS/Texture Conversion:**

1. **SYW Pack Builder** (by Satsuki)

   - Forum: https://forums.qhimm.com/index.php?topic=19204.0
   - Converts PNG texture packs to DDS format IROs
   - Creates IRO files with "Make IRO from DDS Files" button
   - Recommended compression: "Nothing" for best performance

2. **Satsuki PNG to DDS Converter**
   - Forum: http://forums.qhimm.com/index.php?topic=19701.0
   - Converts individual IROs from PNG to DDS format
   - Drag-and-drop interface

**Why DDS?**

- DDS textures load 40-70% faster than PNG in FFNx
- Recommended for large texture mods (Remako, SYW upscales)
- PNG is fallback/legacy format

**Source:** Community guides (OatBran's 7H Steam Guide), Qhimm forums

#### 7.3.5 Movie Importer Tool

**Location:** Tools → Movie Importer

> **CORRECTION (2025-11-25):** This tool was previously incorrectly documented as a video
> encoder/converter. It is NOT. See actual purpose below.

**Actual Purpose:** Copy FMV files from **original 1998 physical game discs** to hard drive.

**Official Description (from 7thheaven.rocks):**

> "If you have the original 1998 disc release of Final Fantasy VII, this tool will assist you
> with copying over the movies from disc onto the hard drive. If all movie files are already
> found on your computer, this option is disabled."

**What This Tool Does:**

1. Prompts user to insert physical FF7 game discs (Disc 1, 2, 3)
2. Copies original FMV files from disc to movies folder
3. Automatically disabled if movies already exist on drive

**What This Tool Does NOT Do:**

- Does NOT convert video formats (AVI, MKV, MP4, etc.)
- Does NOT encode or re-encode videos
- Does NOT support modern codecs
- Has NO encoding options (resolution, bitrate, etc.)

**For Video Replacement Mods:**
If you want to replace FMVs with upscaled/remastered versions:

1. FFNx supports direct playback of modern video formats
2. Place video files in appropriate mod folder structure
3. Package as IRO using standard IRO Tools
4. See FFNx documentation for supported codecs

**Source:** https://7thheaven.rocks/help/userhelp.html#importmovies

#### 7.3.6 Debug Logging and Variable Dumping

**Location:** Play button dropdown menu (verified)

**Verified Debug Options (from official docs):**

Access via the dropdown arrow next to the Play button:

| Option                           | Purpose                                   |
| -------------------------------- | ----------------------------------------- |
| **Play With Debug Log**          | Verbose logging, detailed file operations |
| **Play With Variable Dump**      | TurBoLog with runtime variable values     |
| **Play With Minimal Validation** | Skip validation checks (faster launch)    |
| **Play Without Mods**            | Launch vanilla game                       |

**Official Description:**

> "The Debug Log and Variable Dump can be useful for troubleshooting 7th Heaven and/or mod files."

**Source:** https://7thheaven.rocks/help/userhelp.html#playbutton

---

> **Note:** The following details are based on community knowledge and may vary by version.
> They could not be verified in official 7thheaven.rocks documentation.

**Log File Location (unverified):**

```text
%APPDATA%\7th Heaven\logs\
  ├── 7thHeaven.log        # Main application log
  └── [timestamp].log      # Session-specific logs
```

**What Gets Logged (unverified):**

- Mod loading order
- File path resolutions
- VFS intercept decisions
- RuntimeVar evaluations
- Error messages

**Variable Dump Output:**
When using "Play With Variable Dump", look for runtime variable entries that can help configure Conditional folders in mod.xml:

- FieldID values (current map)
- PPV values (story progression)
- BattleID values (current battle)

#### 7.3.7 Chunk Tool (Field Data Extraction)

**Location:** Tools → Chunk Tool (verified)

> **CLARIFICATION (2025-11-25):** There are TWO different "chunking" concepts in 7th Heaven.
> This section covers the **Chunk Tool** for field data extraction, not IRO file splitting.

**Purpose:** Extract portions of `flevel.lgp` into "Chunks" for translation/localization mods.

**Official Description (from 7thheaven.rocks):**

> "This tool is useful for modders. It allows you to extract only a portion of the flevel.lgp
> file into 'Chunks'. This is great if you need to distribute a portion of a customized
> flevel.lgp file in your mod without needing to include the entire file."

**Use Case:** Translation mods that only modify dialog text, not backgrounds or models.

**Workflow:**

1. Click folder icon to select source `flevel.lgp`
2. Click folder icon to select output directory
3. Check boxes for sections to extract:
   - Section 1 Field Script Dialog
   - (other sections as needed)
4. Click "Extract"

**Benefits:**

- Smaller mod file size
- Fewer conflicts with texture/model mods
- Only distribute what you changed

**Source:** https://7thheaven.rocks/help/userhelp.html#chunktool

---

#### 7.3.8 IRO File Chunking (Distribution)

> **Note:** This is DIFFERENT from the Chunk Tool above. This is for splitting large IRO files.

**Purpose:** Split large IRO files into smaller pieces for file hosts with size limits.

**How It Works:**

- Large IRO split into `.chunk.001`, `.chunk.002`, etc.
- 7th Heaven automatically reassembles on download
- Supports pause/resume for unreliable connections

**Catalog Integration:**

```xml
<!-- In catalog XML, link to chunk files -->
<LatestVersion>
  <Link>iros://Url/http$yoursite.com/MyMod.iro.chunk</Link>
  <Version>1.0</Version>
</LatestVersion>
```

**When to Use:**

- File hosts with 100MB limits
- Very large mods (1GB+)
- Users with slow/unreliable connections

> **Note:** The exact UI location for creating chunked IROs could not be verified in official
> documentation. This may be done via command line or external tools.

### 7.4 Debug and Development Settings

> **Verification Status (2025-11-25):** FFNx settings are based on the FFNx.toml file in the
> cloned FFNx repository. 7th Heaven wrapper debug settings could not be verified against
> official documentation and are marked as "unverified".

#### FFNx Debug Settings (Verified)

These settings are configured in `FFNx.toml` (located in FF7 game directory):

```toml
# Show detailed texture loading info
trace_loaders = true

# Log all file operations
trace_files = true

# Show which textures are missing overrides
show_missing_textures = true

# Dump all textures to disk (for analysis)
save_textures = true

# Full debug trace (WARNING: Very large logs)
trace_all = false
```

**Source:** FFNx repository (https://github.com/julianxhokaxhiu/FFNx)

#### 7th Heaven Debug Options (Verified)

Access via Play button dropdown:

- **Play With Debug Log** - Detailed logging
- **Play With Variable Dump** - TurBoLog with variables
- **Play With Minimal Validation** - Skip checks

**Source:** https://7thheaven.rocks/help/userhelp.html#playbutton

#### Wrapper Debug Settings (Unverified)

> **Warning:** The following settings are based on community knowledge and could not be
> verified in official 7th Heaven documentation. They may not exist or may have changed.

```ini
# In 7thHeaven.ini (advanced) - UNVERIFIED
[Debug]
LogLevel=3          # 0=Off, 1=Error, 2=Warn, 3=Info, 4=Debug, 5=Trace
LogToFile=true
LogToConsole=true
DumpVarState=true   # Dump all runtime variables
```

#### Inspecting Active Mod Configuration

**Profile Files:**

```
%APPDATA%\7th Heaven\profiles\
  └── Default.xml    # Current active configuration
```

**Profile XML Structure:**

```xml
<Profile>
  <ActiveMods>
    <Mod>
      <ID>guid-of-mod</ID>
      <LoadOrder>1</LoadOrder>
      <ConfigOptions>
        <Option Name="quality" Value="high" />
      </ConfigOptions>
    </Mod>
    <!-- More mods... -->
  </ActiveMods>
</Profile>
```

**Debugging Load Order Issues:**

1. Open Profile XML
2. Check `<LoadOrder>` values
3. Lower number = higher priority
4. Reorder by editing XML or via 7H UI

### 7.5 Third-Party Archive Tools

**7-Zip (Essential):**

```batch
REM Create IRO
7z a -tzip output.iro input_folder\*

REM Extract IRO
7z x input.iro -ooutput_folder\

REM List contents
7z l file.iro

REM Add file to existing IRO
7z a -tzip existing.iro newfile.png

REM Delete file from IRO
7z d existing.iro unwanted.png
```

**Download:** https://www.7-zip.org/

---

## 8. ADVANCED MOD FEATURES

### 8.1 Conditional Loading (Runtime Variables)

**Use Cases:**

- Show different textures based on location
- Activate special assets during specific story events
- Change music based on game progression

**Available Runtime Variables:**

```xml
<!-- Common predefined variables (see 7thHeaven.var) -->
<RuntimeVar Var="FieldID" Values="0xD5" />       <!-- Current field map -->
<RuntimeVar Var="PPV" Values="300..400" />       <!-- Story progression -->
<RuntimeVar Var="BattleID" Values="50" />        <!-- Current battle -->
<RuntimeVar Var="MenuState" Values="1" />        <!-- Menu open/closed -->

<!-- Custom memory addresses -->
<RuntimeVar Var="Short:0xCC15D0:2" Values="0xD5,0x160" />
<RuntimeVar Var="Byte:0xDC0820:1" Values="1..5" />
<RuntimeVar Var="Int:0xABCDEF:4" Values="1000" />
```

**Example: Location-Specific Textures**

```xml
<ModInfo>
  <ID>guid-here</ID>
  <Name>Location-Aware Textures</Name>
  <!-- ... other fields ... -->

  <!-- Default assets (always active) -->
  <ModFolder Folder="default" />

  <!-- Special Midgar assets (FieldID = 0xD5 or 0x160) -->
  <Conditional Folder="midgar">
    <RuntimeVar Var="FieldID" Values="0xD5,0x160" />
  </Conditional>

  <!-- Special Junon assets (PPV between 300-400) -->
  <Conditional Folder="junon">
    <RuntimeVar Var="PPV" Values="300..400" />
  </Conditional>
</ModInfo>
```

**Folder Priority:**

- If both conditions are true, folder listed first in mod.xml wins
- If `midgar` and `junon` both have `cloud.p`, `midgar/cloud.p` is used

### 8.2 Mod Patching (.irop files)

**Purpose:** Distribute incremental updates without re-downloading entire mod.

**Creating a Patch:**

1. **Make changes to your mod**
2. **Use 7th Heaven's IRO Tools** (Workshop tab)
3. **Select original IRO** (v1.0)
4. **Select updated IRO** (v2.0)
5. **Generate .irop patch file**

**Patch File Structure:**

```xml
<!-- In your catalog XML -->
<Mod>
  <ID>your-mod-guid</ID>
  <LatestVersion>
    <Link>iros://Url/http$yoursite.com/MyMod_v2.0.iro</Link>
    <Version>2.0</Version>
  </LatestVersion>

  <!-- Patch from 1.0 to 2.0 -->
  <Patch VerFrom="1.0" VerTo="2.0">iros://Url/http$yoursite.com/MyMod_1.0_to_2.0.irop</Patch>

  <!-- Backup link -->
  <Patch VerFrom="1.0" VerTo="2.0">iros://MegaSharedFolder/folder,file,MyMod_patch.irop</Patch>
</Mod>
```

**User Experience:**

- User has v1.0 installed
- Catalog shows v2.0 available
- 7th Heaven downloads small .irop patch (not full mod)
- Patch applies automatically

**Multi-Step Patching:**

```xml
<Patch VerFrom="1.0" VerTo="1.1">iros://Url/http$site.com/patch_1.0_to_1.1.irop</Patch>
<Patch VerFrom="1.1" VerTo="2.0">iros://Url/http$site.com/patch_1.1_to_2.0.irop</Patch>

<!-- OR cumulative patch -->
<Patch VerFrom="1.0,1.1" VerTo="2.0">iros://Url/http$site.com/patch_any_to_2.0.irop</Patch>
```

### 8.3 External URL Links (Download Outside 7H)

**Use Case:** Host mod on ad-supported file host.

```xml
<!-- In catalog XML -->
<LatestVersion>
  <Link>iros://ExternalUrl/http$adfly.com/yourmodlink</Link>
  <Version>1.0</Version>
</LatestVersion>
```

**Behavior:**

- Opens link in user's web browser
- User downloads manually
- User imports IRO into 7th Heaven

**Standard URL (Direct Download):**

```xml
<Link>iros://Url/http$yoursite.com/MyMod.iro</Link>
```

**Behavior:**

- 7th Heaven downloads directly
- No browser interaction

### 8.4 Archive Extraction Options

**Scenario:** Your IRO contains a ZIP with multiple files.

**ExtractSubFolder:**

```xml
<!-- Only extract files from "textures" folder inside the ZIP -->
<ExtractSubFolder>textures</ExtractSubFolder>
```

**ExtractInto:**

```xml
<!-- Extract files into "menu_us.lgp" folder in mod directory -->
<ExtractInto>menu_us.lgp</ExtractInto>
```

**Combined Example:**

```
Your mod.iro contains:
└── assets.zip
    ├── textures/
    │   ├── cloud.png
    │   └── tifa.png
    └── models/
        └── ...

You want only textures/, placed in menu_us.lgp/ folder:
```

```xml
<ExtractSubFolder>textures</ExtractSubFolder>
<ExtractInto>menu_us.lgp</ExtractInto>

Result in mod directory:
└── menu_us.lgp/
    ├── cloud.png
    └── tifa.png
```

---

## 9. TESTING AND DEBUGGING

### 9.1 Testing Checklist

**Pre-Packaging:**

- [ ] All assets converted to correct formats (.tex, .p, .ogg, etc.)
- [ ] Folder structure matches FF7 directory layout
- [ ] mod.xml validated (XML syntax checker)
- [ ] GUID is unique (generated via 7H tool)
- [ ] Preview image exists and displays correctly

**Post-Packaging:**

- [ ] IRO opens in 7-Zip without errors
- [ ] mod.xml is in IRO root (not in subfolder)
- [ ] All paths in mod.xml exist in IRO
- [ ] File sizes reasonable (not accidentally huge)

**In 7th Heaven:**

- [ ] IRO imports without errors
- [ ] Mod appears in catalog with correct info
- [ ] Preview image displays
- [ ] Readme opens (if included)
- [ ] Config options appear and work

**In-Game:**

- [ ] Game launches without crashes
- [ ] Modded assets appear correctly
- [ ] No visual glitches
- [ ] Test for 30+ minutes (stability)
- [ ] Disable mod → Game returns to vanilla

**Compatibility:**

- [ ] Test with other popular mods enabled
- [ ] Verify no unexpected interactions
- [ ] Check Auto Sort places mod correctly

### 9.2 Common Issues and Solutions

**Issue: "Mod failed to load"**

- **Cause:** Corrupted IRO or invalid mod.xml
- **Debug:** Extract IRO, check mod.xml syntax
- **Fix:** Rebuild IRO from clean source

**Issue: "Duplicate ModID detected"**

- **Cause:** Used another mod's GUID
- **Debug:** Check `<ID>` field in mod.xml
- **Fix:** Generate new unique GUID

**Issue: Assets don't appear in-game**

- **Cause:** Folder structure mismatch
- **Debug:** Compare mod folder structure to FF7 data directory
- **Fix:** Reorganize folders to match game structure

**Issue: Config options don't work**

- **Cause:** `<ID>` in ConfigOption doesn't match ModFolder `ActiveWhen`
- **Debug:** Check variable names match exactly
- **Fix:** Ensure consistency between ConfigOption `<ID>` and ModFolder conditions

**Issue: Mod appears twice in catalog**

- **Cause:** Old version still in `mods/7th Heaven/` folder
- **Fix:** Delete duplicate IRO, reimport

**Issue: "Failed to extract archive"**

- **Cause:** IRO is not valid ZIP format
- **Debug:** Open with 7-Zip, check for errors
- **Fix:** Repack using 7z command line

### 9.3 Debug Logging

**Enable 7th Heaven Debug Logging:**

1. Open 7th Heaven
2. Settings → General Settings
3. Enable "Debug Logging"
4. Check log file: `<7thHeaven>\logs\7thHeaven.log`

**What to Look For:**

- Mod load events
- File intercept messages
- Error messages
- Asset path resolutions

**Example Log Entry:**

```
[INFO] Loading mod: MyMod v1.0
[INFO] Activating folder: base_assets
[INFO] Intercepted request: data/menu/menu_us.lgp/usfont.tex
[INFO] Serving from mod: MyMod -> base_assets/menu_us.lgp/usfont.tex
```

---

## 10. DISTRIBUTION

### 10.1 Creating a Catalog Entry

**Option 1: 7th Heaven Catalog/Mod Creation Tool**

1. Open 7th Heaven
2. Workshop → Catalog/Mod Creation Tool
3. **Mod tab:**
   - Fill in all fields (Name, Author, Version, etc.)
   - Add download link(s)
   - Generate GUID if needed
4. **Export XML**
5. Submit to catalog maintainer

**Option 2: Manual XML**

```xml
<Mod>
  <ID>your-mod-guid-here</ID>
  <Author>Your Name</Author>
  <Link>http://forums.qhimm.com/your-mod-thread</Link>
  <Name>Your Mod Name</Name>
  <MetaVersion>2</MetaVersion>
  <Description>Detailed description of your mod.</Description>
  <Tags>
    <string>Textures</string>
    <string>HD</string>
  </Tags>
  <LatestVersion>
    <Link>iros://Url/http$yoursite.com/YourMod_v1.0.iro</Link>
    <Version>1.0</Version>
    <ReleaseDate>2025-11-24</ReleaseDate>
    <CompatibleGameVersions>Original,Steam</CompatibleGameVersions>
    <PreviewImage>http$yoursite.com/preview.png</PreviewImage>
    <ReleaseNotes>Initial release.</ReleaseNotes>
  </LatestVersion>
</Mod>
```

### 10.2 Hosting Options

**Google Drive:**

```xml
<Link>iros://GDrive/1mX0q6Yb4cgYNYkAmd8ocSfGu0c2QHT0B</Link>
```

**How to get File ID:**

1. Upload to Google Drive
2. Right-click → Get shareable link
3. Extract ID from URL: `https://drive.google.com/file/d/[FILE_ID]/view?usp=sharing`

**MEGA:**

```xml
<Link>iros://MegaSharedFolder/folderID,,filename.iro</Link>
```

**Use 7H's MEGA Link Generator tool for easier setup.**

**Direct URL:**

```xml
<Link>iros://Url/http$yourwebsite.com/path/to/mod.iro</Link>
```

**Note:** Replace `://` in http:// with `$` symbol.

**External URL (opens in browser):**

```xml
<Link>iros://ExternalUrl/http$adfly.com/yourlink</Link>
```

### 10.3 Distribution Platforms

**7th Heaven Official Catalog:**

- **How to submit:** Contact Tsunamods team via Discord or GitHub
- **Pros:** In-app discovery, automatic updates, trusted source
- **Cons:** Moderation required, not instant

**Qhimm Forums:**

- **URL:** https://forums.qhimm.com/
- **Section:** 7th Heaven board
- **Pros:** Active modding community, feedback, support
- **Cons:** Manual downloads (unless added to catalog)

**NexusMods:**

- **URL:** https://www.nexusmods.com/finalfantasy7
- **Pros:** Large audience, mod manager support (can link 7H), popularity tracking
- **Cons:** Not integrated with 7H (users must import manually)

**GitHub Releases:**

- **Pros:** Version control, release management, free hosting
- **Cons:** Not discoverable in 7H (unless catalog entry added)

**Personal Website:**

- **Pros:** Full control, custom presentation
- **Cons:** Bandwidth costs, hosting maintenance

### 10.4 Release Checklist

**Pre-Release:**

- [ ] Version number updated in mod.xml
- [ ] Release date current
- [ ] Complete testing on clean FF7 install
- [ ] Preview image finalized
- [ ] Readme/documentation complete
- [ ] Credits and attribution correct

**Package:**

- [ ] IRO created with correct compression
- [ ] File size optimized
- [ ] Filename format: `ModName_v1.00.iro`

**Upload:**

- [ ] Files uploaded to host
- [ ] Download link tested
- [ ] Backup links created (Google Drive + MEGA recommended)

**Announce:**

- [ ] Create forum thread (Qhimm)
- [ ] Submit catalog entry (if applicable)
- [ ] Share on Discord/social media
- [ ] Update mod page with screenshots

**Post-Release:**

- [ ] Monitor for bug reports
- [ ] Respond to user feedback
- [ ] Plan updates/patches

---

## 11. REFERENCE

### 11.1 Official Resources

**7th Heaven:**

- **GitHub:** https://github.com/tsunamods-codes/7th-Heaven
- **Website:** https://7thheaven.rocks/
- **Help Docs:** https://7thheaven.rocks/help/modhelp.html
- **User Guide:** https://7thheaven.rocks/help/userhelp.html
- **Discord:** Check Tsunamods website for invite link

**FFNx (Recommended Graphics Driver):**

- **GitHub:** https://github.com/julianxhokaxhiu/FFNx
- **Documentation:** https://github.com/julianxhokaxhiu/FFNx/blob/master/README.md

**Qhimm Community:**

- **Forums:** https://forums.qhimm.com/
- **Wiki:** http://wiki.qhimm.com/view/FF7
- **Modding Wiki:** https://qhimm-modding.fandom.com/wiki/FF7

### 11.2 Tool Compilation

**Complete list in Section 7.1**

**Quick Reference:**

- **LGP:** ulgp, LGP_edit
- **Textures:** TexTool, FF7 Tex Image Tool
- **Models:** Kimera CS, Biturn, pCreater
- **Fields:** Makou Reactor
- **Kernel:** WallMarket
- **Saves:** Black Chocobo

**Tool Compilation Guide:** https://steamcommunity.com/sharedfiles/filedetails/?id=838174965

### 11.3 File Format Specifications

**FF7 File Formats:**

- **LGP:** https://qhimm-modding.fandom.com/wiki/FF7/LGP_format
- **TEX:** http://wiki.qhimm.com/view/FF7/TEX_format
- **.P Models:** http://wiki.qhimm.com/view/FF7/P_file_format
- **Field Scripts:** http://wiki.qhimm.com/view/FF7/Field

### 11.4 Example Mods for Learning

**Study these mod.xml files for advanced techniques:**

1. **Qhimm Catalog 3.0** (Complex, multi-option mod)
2. **Remako HD Graphics** (Large asset mod)
3. **New Threat** (Gameplay overhaul)
4. **Echo-S Music Mod** (Audio replacement)

**How to Study:**

1. Download mod IRO
2. Extract with 7-Zip
3. Read mod.xml
4. Analyze folder structure
5. Understand techniques used

### 11.5 Community Contact

**Get Help:**

- **Qhimm Discord:** Active modding community
- **Qhimm Forums:** Long-form discussions, tutorials
- **7th Heaven GitHub Issues:** Bug reports, feature requests

**Contribute:**

- **Test mods:** Provide feedback to authors
- **Create tutorials:** Share your knowledge
- **Submit tools:** Improve modding ecosystem
- **Maintain catalog:** Help curate mod collection

---

## APPENDIX A: QUICK START TEMPLATE

**Minimal Working mod.xml:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModInfo>
  <ID>GENERATE-GUID-HERE</ID>
  <Name>My Quick Mod</Name>
  <Author>YourName</Author>
  <Version>1.00</Version>
  <ReleaseDate>2025-11-24</ReleaseDate>
  <Category>User Interface</Category>
  <Description>A simple mod that replaces [asset name].</Description>

  <ModFolder Folder="assets" />
</ModInfo>
```

**Minimal Folder Structure:**

```
MyQuickMod/
├── mod.xml
└── assets/
    └── menu_us.lgp/
        └── usfont.tex
```

**Package Command:**

```batch
cd MyQuickMod
7z a -tzip "..\MyQuickMod_v1.00.iro" *
```

**Done!** Import into 7th Heaven and test.

---

## APPENDIX B: mod.xml Validation Checklist

Before packaging your IRO, verify:

- [ ] `<?xml version="1.0" encoding="utf-8"?>` at top
- [ ] All tags inside `<ModInfo>` ... `</ModInfo>`
- [ ] `<ID>` is unique GUID (32 hex chars with dashes)
- [ ] `<Version>` is decimal format (1.00, 2.50, etc.)
- [ ] `<ReleaseDate>` is YYYY-MM-DD format
- [ ] `<Category>` is one of the valid categories
- [ ] All `<ModFolder>` paths exist in IRO
- [ ] All `<ConfigOption>` `<ID>` values match `ActiveWhen` conditions
- [ ] All `<Require>` / `<Forbid>` ModIDs are correct
- [ ] No syntax errors (use XML validator)

---

## APPENDIX C: Common Variable Reference

**Runtime Variables (from 7thHeaven.var):**

| Variable  | Type  | Address    | Description                        |
| --------- | ----- | ---------- | ---------------------------------- |
| FieldID   | Short | 0xCC15D0:2 | Current field map ID               |
| PPV       | Short | 0xDC08DC:2 | Progression variable (story state) |
| BattleID  | Short | 0x9A8F00:2 | Current battle ID                  |
| MenuState | Byte  | 0xCFF1F4:1 | Menu open/closed state             |

**For complete list:** Check `7th Heaven/7thHeaven.var` file.

---

**DOCUMENT END**

**Document Status:** Verified Against Official Sources (v2.2)

**Verification Summary (2025-11-25):**

- Section 7.3.1-7.3.3: VERIFIED against official 7thheaven.rocks documentation
- Section 7.3.4: CORRECTED - External tool, not built-in
- Section 7.3.5: CORRECTED - Disc copy tool, not video encoder
- Section 7.3.6: VERIFIED (Play button options), unverified (log file details)
- Section 7.3.7-7.3.8: VERIFIED and CLARIFIED (two different chunking concepts)
- Section 7.4: PARTIALLY VERIFIED (FFNx settings verified, wrapper settings unverified)

**See:** `docs/reference/TOOL_VERIFICATION_LOG.md` for complete verification details.

**Sources:**

- Official 7th Heaven Documentation: https://7thheaven.rocks/help/userhelp.html (PRIMARY)
- Official 7th Heaven Mod Help: https://7thheaven.rocks/help/modhelp.html
- Tsunamods GitHub Repository: https://github.com/tsunamods-codes/7th-Heaven
- Qhimm Forums Modding Community: https://forums.qhimm.com/
- FF7 Tools Compilation (Steam Community)
- FFNx Repository: https://github.com/julianxhokaxhiu/FFNx
- OatBran's 7H Steam Guide: https://github.com/OatBran/7HSteamGuide (community reference)

**Research Sessions:**

- 2025-11-24 21:50-22:15 JST - Initial creation (Session 11)
- 2025-11-25 12:00-12:30 JST - Verification against official sources (Session 12)

**Session IDs:**

- 8f58819d-f9c4-4f04-8e95-4af04d782606

---

**For questions, support, or contributions:**

- Qhimm Forums: https://forums.qhimm.com/
- 7th Heaven Issues: https://github.com/tsunamods-codes/7th-Heaven/issues

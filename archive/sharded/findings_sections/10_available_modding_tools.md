# Available Modding Tools

**Extracted From**: FINDINGS.md
**Section Lines**: 904-1016
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### 7th Heaven (Mod Manager)

**Website**: https://7thheaven.rocks/
**Current Status**: Actively maintained

**Capabilities**:
- Mod downloading and installation
- LGP file management
- Automatic mod conflict resolution
- Includes FFNx driver
- Supports 60/30 FPS gameplay mods

**Limitations**:
- Not compatible with "The Reunion" mod
- Cannot add Japanese font support (yet)

**Relevance to Project**:
- Potential distribution platform for Japanese mod
- Can swap LGP archives
- Mod catalog system for easy updates

### FFNx (Modern Graphics Driver)

**GitHub**: https://github.com/julianxhokaxhiu/FFNx
**Current Status**: Actively developed (latest commits 2024)

**Features**:
- DirectX 11/12, Vulkan, or OpenGL rendering
- Anisotropic filtering, antialiasing, vsync
- Extended modding support
- Controller improvements
- **Open source** (critical for our needs)

**Architecture**:
- Replaces original `AF3DN.P` driver
- Hooks into game executable
- Texture loading pipeline
- Font rendering system

**Japanese Support Status**:
- Issue #39 open since 2020
- Recognized as requiring font system overhaul
- Community seeking contributors
- **This is our best path forward**

### The Reunion (Comprehensive Mod Suite)

**Website**: https://thereunion.live/

**Components**:
- BEACAUSE: Translation fixes
- MENU ENHANCEMENT: UI improvements
- 60 FPS BATTLES: Frame rate correction
- MODEL OVERHAUL: Character model upgrades
- AUDIO REPLACEMENT: Sound module replacement
- Enhanced controller support

**Limitations**:
- Not compatible with 7th Heaven
- Not compatible with FFNx
- **Cannot solve Japanese character encoding issue**

### touphScript (Text Editor)

**GitHub**: https://github.com/ser-pounce/touphscript
**Current Version**: 1.5.0 (Feb 2023)

**Capabilities**:
- Dumps all FF7 text to UTF-8 files
- Re-encodes text back into game files
- Supports all text locations:
  - `ff7.exe` / `ff7_en.exe`
  - `flevel.lgp`
  - `KERNEL.BIN`
  - `kernel2.bin`
  - `scene.bin`
  - `world_us.lgp`
- Auto-resizes dialog windows
- Tutorial script editing

**File Format**:
- Input: UTF-8 text files
- Output: FF Text encoding
- **Current limitation**: Single-byte encoding only
- **Potential**: Could be extended for double-byte

**Relevance**:
- Provides framework for text replacement
- Would need extension for Japanese encoding
- Window sizing logic useful reference

### Makou Reactor (Field Script Editor)

**Forum Thread**: http://forums.qhimm.com/index.php?topic=9658.0

**Capabilities**:
- Edit field scripts
- Modify dialog
- Change triggers and events
- **Supports Japanese characters in editor**

**Critical Finding**:
> "It's curious, because I see Makou Reactor supports Japanese characters. So it seems like saving the flevel in Japanese should be possible (which I tried, when I reopened the flevel the Japanese was just jibberish)."

**Implication**:
- Tool can handle Japanese input
- Game cannot parse Japanese output
- Confirms encoding incompatibility at game level

---


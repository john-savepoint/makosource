# 14. REFERENCE MATERIALS & APPENDICES

## 14.1 Complete Memory Map (US 1.02)

**⚠️ WARNING: These addresses are ONLY for FF7 US 1.02. Other versions differ!**

| Address | Size | Type | Description |
|---------|------|------|-------------|
| `0x99DDA8` | 256 bytes | `char[]` | Character width table |
| `0x99DCA8` | 4 bytes | `uint32_t` | Current text color |
| `0x66E272` | Function | Code | `draw_graphics_object` (approximation) |
| `0x66E2A0` | Function | Code | Character processing loop (approximation) |
| `0xCC0000` | N/A | ❌ INVALID | PLACEHOLDER - do not use |

**How to Find Addresses for Other Versions:**

See Section 8.2 for detailed instructions.

---

## 14.2 Character Encoding Reference

**Single-Byte Characters (Page 0 / jafont_1):**

| Range | Content |
|-------|---------|
| `0x00-0x1F` | Control codes (line break, color, etc.) |
| `0x20-0x7E` | ASCII (Latin alphabet, numbers, punctuation) |
| `0x7F-0xE6` | Japanese Hiragana, Katakana, special chars |
| `0xE7-0xF8` | Reserved / Unused |
| `0xF9` | Furigana marker (Phase 2) |
| `0xFA` | Page 1 marker |
| `0xFB` | Page 2 marker |
| `0xFC` | Page 3 marker |
| `0xFD` | Page 4 marker |
| `0xFE` | Page 5 marker |
| `0xFF` | Reserved |

**Two-Byte Sequences (Pages 1-5):**

| First Byte | Second Byte | Meaning |
|------------|-------------|---------|
| `0xFA` | `0x00-0xFF` | Character from jafont_2.png (index 0-255) |
| `0xFB` | `0x00-0xFF` | Character from jafont_3.png (index 0-255) |
| `0xFC` | `0x00-0xFF` | Character from jafont_4.png (index 0-255) |
| `0xFD` | `0x00-0xFF` | Character from jafont_5.png (index 0-255) |
| `0xFE` | `0x00-0xFF` | Character from jafont_6.png (index 0-255) |

**Example Encoding:**

```
Japanese text: "こんにちは" (Konnichiwa / Hello)
Assuming mapping:
  こ = jafont_1, index 0x3A
  ん = jafont_1, index 0x3B
  に = jafont_1, index 0x3C
  ち = jafont_1, index 0x3D
  は = jafont_1, index 0x3E

Encoded bytes: 0x3A 0x3B 0x3C 0x3D 0x3E 0x00
               (All on Page 0, so no FA prefix needed)

Japanese text: "魔法" (Mahou / Magic)
Assuming mapping:
  魔 = jafont_2, index 0x10
  法 = jafont_2, index 0x11

Encoded bytes: 0xFA 0x10 0xFA 0x11 0x00
               (FA = switch to Page 1, then char index)
```

---

## 14.3 FFNx Configuration Reference

**Complete FFNx.toml Settings for Japanese:**

```toml
###############################################################################
# FFNx Configuration File
###############################################################################

# ===========================
# Japanese Language Support
# ===========================

# Font language mode
# Values: "en" (English), "ja" (Japanese)
# Default: "en"
font_language = "ja"

# Enable Furigana (reading guides above Kanji)
# Requires: Furigana-enabled font textures
# Default: false
font_enable_furigana = false

# Custom font texture path
# Leave empty to use default: mods/Textures/menu/
# Example: "mods/CustomFonts/ja/"
# Default: ""
font_path_override = ""

# ===========================
# Related Settings
# ===========================

# Texture dumping (for mod creation)
save_textures = false

# Trace logging (debugging only)
trace_all = false
trace_renderer = false
trace_loaders = false

# Window mode
fullscreen = false
window_size_x = 1280
window_size_y = 960

# Rendering backend
renderer_backend = "auto"  # auto, OpenGL, DirectX11, Vulkan

# ===========================
# Advanced
# ===========================

# Use external textures from mods folder
use_external_textures = true

# Mod path (where mods/Textures/ is located)
mod_path = "mods/Textures"
```

---

## 14.4 File Format Specifications

**PNG Requirements for Font Textures:**

| Property | Value | Notes |
|----------|-------|-------|
| Resolution | 1024×1024 | Enforced by FFNx |
| Color Mode | RGBA | 32-bit with alpha |
| Bit Depth | 8 bits per channel | Total 32 bpp |
| Compression | PNG (lossless) | No JPEG |
| Interlacing | None | Optional but not needed |
| Grid Layout | 16×16 cells | 256 total cells |
| Cell Size | 64×64 pixels | Per glyph |
| Alpha Channel | Required | For anti-aliasing edges |

**Exporting from Image Editors:**

**Photoshop:**
```
File → Export → Export As...
Format: PNG
Transparency: Checked
Interlaced: Unchecked
```

**GIMP:**
```
File → Export As...
Select file type: PNG
Compression level: 9 (maximum)
Save background color: No
Save gamma: No
Interlacing: None
```

**Aseprite:**
```
File → Export...
Format: PNG
Color: RGBA (32-bit)
Scale: 1x
```

---

## 14.5 Glossary

| Term | Definition |
|------|------------|
| **AF3DN.P** | Square Enix's proprietary graphics driver for FF7 PC |
| **BGFX** | Cross-platform graphics library used by FFNx |
| **Character Width Table** | In-memory array defining pixel width of each character |
| **FA-FE Encoding** | Custom 2-byte system using 0xFA-0xFE as page markers |
| **FFNx** | Open-source graphics driver replacement for FF7/FF8 |
| **Furigana** | Small Hiragana placed above Kanji to show pronunciation |
| **Glyph** | Visual representation of a single character |
| **Hext** | System for applying in-memory assembly patches at runtime |
| **LGP** | Square Enix's archive format (.lgp files) |
| **Palette Index** | Number determining which texture variant to use |
| **Texture Set** | FFNx struct holding multiple texture handles |
| **UV Coordinates** | Texture mapping coordinates (U=horizontal, V=vertical) |

---

## 14.6 External Resources

**Essential Tools:**

| Tool | Purpose | URL |
|------|---------|-----|
| FFNx | Graphics driver | https://github.com/julianxhokaxhiu/FFNx |
| 7th Heaven | Mod manager | https://7thheaven.rocks/ |
| Makou Reactor | Field script editor | http://forums.qhimm.com/ |
| Hojo | Text editor | http://forums.qhimm.com/ |
| TexTools | TEX ↔ PNG converter | http://forums.qhimm.com/ |
| ulgp | LGP archive tool | http://forums.qhimm.com/ |
| Cheat Engine | Memory debugger | https://cheatengine.org/ |
| x64dbg | Assembly debugger | https://x64dbg.com/ |

**Community Resources:**

| Resource | Description |
|----------|-------------|
| Qhimm Forums | FF7 modding community hub |
| FFNx Discord | Real-time support |
| FF7 Wiki | Game engine documentation |
| GitHub Issues | Bug tracking and features |

---

## 14.7 Version History

**Document Changelog:**

| Version | Date | Changes |
|---------|------|---------|
| 4.0 | 2025-11-24 | Ultimate consolidated spec with all clarifications |
| 3.0 | 2025-11-20 | Added implementation details and debugging guide |
| 2.0 | 2025-11-15 | Integrated AF3DN analysis findings |
| 1.0 | 2025-11-10 | Initial specification |

---

# Technical Documentation Available

**Extracted From**: FINDINGS.md
**Section Lines**: 1017-1073
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### Comprehensive Documentation Sources

1. **qhimm Modding Wiki**
   - URL: https://qhimm-modding.fandom.com/wiki/Qhimm_Modding_Wiki
   - FF Text encoding tables
   - Field file structures
   - KERNEL.BIN formats

2. **FF7 Flat Wiki**
   - URL: https://ff7-mods.github.io/ff7-flat-wiki/
   - Field module documentation
   - Text encoding specifications
   - Battle system documentation

3. **Version Differences Guide**
   - URL: https://thelifestream.net/ffvii-the-original/ffvii-version-guide/
   - Complete version comparison
   - Script differences between releases
   - PAL vs NTSC differences

4. **PCGamingWiki**
   - URL: https://www.pcgamingwiki.com/wiki/Final_Fantasy_VII
   - Technical specs
   - Compatibility information
   - Modding guides

### Documented File Formats

**Field Files** (`flevel.lgp`):
- 9 sections per field file
- Section 1: Script & Dialog (FF Text)
- Section 2: Camera Matrix
- Section 3: Model Loader
- Section 4: Palette
- Section 5: Walkmesh
- Section 6: TileMap (unused)
- Section 7: Encounter
- Section 8: Triggers
- Section 9: Background

**KERNEL.BIN**:
- 27 GZIP sections
- Sections 1-9: Binary data
- Sections 10-27: Text (FF Text encoding)
- Complete field descriptions available

**Scene.bin**:
- 256 battle scenes
- 3 enemy names each
- 32 attack names each
- AI dialogue text
- Battle mechanics data

---


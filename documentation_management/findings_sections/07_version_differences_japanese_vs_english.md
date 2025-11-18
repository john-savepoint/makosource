# Version Differences (Japanese vs English)

**Extracted From**: FINDINGS.md
**Section Lines**: 729-770
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### Version History

**Abbreviations**:
- **JORG**: Japanese Original (PS1, Jan 31, 1997) - version 1.0
- **Post-JORG**: All versions after JORG - version 1.1
- **JINT**: FF7 International (Japan PS1, Oct 2, 1997)
- **NTSC-US**: North American PS1 (Sep 7, 1997)
- **PAL**: European PS1 (Nov 17, 1997) - runs at 50Hz vs 60Hz
- **PC98**: Original PC port (May 31, 1998 US, June 25, 1998 EU)
- **PC2012**: Digital PC re-release (Aug 14, 2012)
- **JPC**: Japanese PC port (May 16, 2013) - eStore only, never physical release

Source: https://thelifestream.net/ffvii-the-original/ffvii-version-guide/

### Critical Differences

**Japanese PS1 Original vs PC**:
- PS1 used `window.bin` with dynamic kanji loading
- PC version eliminated this system entirely
- Japanese PC (JPC) required custom driver modifications

**English PC vs Japanese PC (eStore)**:
- English: Single `menu_us.lgp` with one font set
- Japanese: `menu_ja.lgp` with six `jafont_X.tex` files
- Japanese: **Completely customized AF3DN.P driver** to inject fonts
- No cross-compatibility - architecturally different

**File Format Differences**:

| Feature | PS1 | PC98 | PC2012 |
|---------|-----|------|--------|
| Music | PSX audio | MIDI | OGG (later patched to PSX) |
| Field Files | .DAT (LZS) | .LGP archive | .LGP archive |
| Background | .MIM (LZS) | In FLEVEL.LGP | In FLEVEL.LGP |
| Models | .BSX (LZS) | In CHAR.LGP | In CHAR.LGP |
| FMVs | FMV Motion JPEG | Duck TrueMotion 2 AVI | Duck TrueMotion 2 AVI |
| Resolution | 320x224, 15fps | Up to 640x480 | Up to 1920x1080 (mods) |

---


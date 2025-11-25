# Existing Modification Attempts

**Extracted From**: FINDINGS.md
**Section Lines**: 771-865
**Extraction Date**: 2025-11-18 17:16:21 JST
**Session-ID**: 596059e7-f5a7-4892-bce3-daf9c7c0a824

---


### 1. cmh175's Japanese Translation Project (2015-2016)

**Forum Thread**: https://forums.qhimm.com/index.php?topic=16321.0

**Approach**:
- Extract files from FF7 International (Japanese PS1)
- Convert to PC format
- Load via 7th Heaven mod manager

**Results**:
- ✅ Successfully extracted Japanese files
- ✅ Files loaded into 7th Heaven without errors
- ❌ **All Japanese text displayed as gibberish**
- ❌ Game could not parse the character encoding

**Key Quote**:
> "So the Japanese games files are formatted differently, so they cant be used with other versions of the game. When I altered the JP files they'd get corrupt because the tools we use here would reformat them."

**Conclusion**:
- File format conversion possible
- Character encoding remains incompatible
- Tools reformat text and break Japanese characters
- Project abandoned in 2016

### 2. markul's Technical Analysis (2024)

**Forum Post**: https://forums.qhimm.com/index.php?topic=16321.msg294972#msg294972

**Problem Identified**:
> "Main problem is that the japanese text-fonts, needs a lot of symbols (characters) to be used, for example if the english textfonts needs 1 set of symbols, japanese needs 6, and the ff7 english version seems to be limited to only 1 block."

**Proposed Solutions**:

**Option 1 - Force window.bin Usage**:
- Make PC version use `window.bin` for characters (like PSX)
- Instead of PNG files from `menu_us.lgp`
- Use `window.bin` from Japanese PSX game
- **Status**: Theoretical, not implemented

**Option 2 - Color-Coded Character Mapping**:
- English version has multiple color variants of same font
- Map Japanese characters to color+character combinations
- Example: Character ç = `{CYAN}*{CYAN}` in Makou Reactor
- **Drawbacks**:
  - Requires remapping every Japanese character
  - Requires modifying `window.bin` font space values
  - Would lose colored text functionality
  - Unknown if Wall Market/Proud Clod tools support this technique
- **Status**: Theoretical, extremely labor-intensive

**Conclusion**:
- Both approaches theoretically possible
- Both require extensive low-level modifications
- No implementation attempted

### 3. FFNx Japanese Support Issue (2020-present)

**GitHub Issue**: https://github.com/julianxhokaxhiu/FFNx/issues/39
**Status**: Open since May 16, 2020

**Key Findings**:

**Square Enix's Approach (eStore version)**:
- Completely customized the `AF3DN.P` graphics driver
- eStore driver is **larger** than Steam version
- Contains font injection code for `jafont_X.tex` files
- **No source code available**

**Quote from julianxhokaxhiu (FFNx developer)**:
> "Square-Enix did release an eStore Japanese edition of the game, although in order to inject Japanese fonts they had to customize completely the driver. It seems that the eStore release, different than Steam has a bigger stock AF3DN.P driver, which has the code to inject into the font system."

**Community Efforts**:
- User "Hundarzbarbar" attempted to contact Square Enix Japan (2022)
- Request for source code or implementation details
- **No response received**
- Assembly code analysis attempted but "very hard to catch what is going on"

**Technical Analysis**:
- Identified `menu_ja.lgp` contains six `jafont_X.tex` files
- Font files are TEX format (PlayStation texture format)
- Driver must handle texture loading for all six files
- Character lookup must determine which texture to use

**Quote from zaphod77**:
> "no, because the extra japanese characters needs to be supported in addition to the english characters. there's no room to fit them all in the existing textures and fake it."

**Current Status**:
- Issue remains open with "enhancement" and "help wanted" tags
- No implementation progress as of 2024
- Recognized as requiring driver-level modifications

---


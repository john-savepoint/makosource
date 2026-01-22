# FFNx License Investigation Session Summary

**Created**: 2026-01-16 14:06:48 JST (Friday)
**Session ID**: 1603cb3d-a631-4649-8c10-c09e0731a34b
**Author**: John Zealand-Doyle
**Working Directory**: `/home/johnzealanddoyle/projects/ff7OG_japanese`
**Git Branch**: main

---

## Session Overview

This session focused on investigating the FFNx licensing terms and conditions to understand the legal requirements for using and distributing FFNx as part of the FF7 Japanese localization mod project.

---

## Key Findings

### FFNx License Type

**FFNx is licensed under the GNU General Public License v3.0 (GPLv3)**

- **License File**: `FFNx-PR737/COPYING.txt`
- **Full License Text**: Complete GPLv3 text (674 lines) present in the repository
- **Version**: GPLv3, dated June 29, 2007
- **License URL**: https://www.gnu.org/licenses/gpl-3.0.html

---

## GPLv3 Terms and Conditions Summary

### What GPLv3 Allows

| Permission | Description |
|------------|-------------|
| **Use** | Unlimited personal and commercial use of the software |
| **Modification** | Full permission to modify the source code |
| **Distribution** | Permission to distribute copies (original or modified) |
| **Running** | Unlimited permission to run the unmodified program |

### What GPLv3 Requires

| Requirement | Description |
|-------------|-------------|
| **Source Code Availability** | When distributing binaries, must provide or offer access to complete source code |
| **Copyleft (Share-Alike)** | Derivative works must also be licensed under GPLv3 |
| **License Preservation** | Must include copy of GPLv3 license with distributions |
| **Copyright Notices** | Must preserve all copyright notices and license references |
| **Modification Marking** | Modified versions must be marked as changed with relevant dates |
| **Installation Information** | For User Products, must provide information needed to install modified versions |

### What GPLv3 Prohibits

| Restriction | Description |
|-------------|-------------|
| **Sublicensing** | Cannot relicense under different terms (section 10) |
| **Additional Restrictions** | Cannot impose further restrictions on recipients' rights |
| **Proprietary Conversion** | Cannot incorporate GPL code into proprietary programs |
| **Warranty Claims** | Cannot claim warranty (software provided "AS IS") |
| **Patent Retaliation** | Patent licenses automatically extended to all recipients |

---

## Key GPLv3 Sections Relevant to This Project

### Section 0: Definitions
- **"The Program"**: Refers to FFNx
- **"Covered work"**: Either unmodified FFNx or works based on FFNx
- **"Modify"**: Copy/adapt requiring copyright permission
- **"Convey"**: Any propagation enabling others to make/receive copies

### Section 2: Basic Permissions
- Unlimited permission to run unmodified FFNx
- Can make, run, and propagate covered works without conveying them
- Output from running FFNx is NOT covered by GPL (game saves, screenshots, etc.)

### Section 4: Conveying Verbatim Copies
- Can distribute exact copies of FFNx source code
- Must publish appropriate copyright notice on each copy
- Can charge any price or no price for copies
- Can offer support/warranty for a fee

### Section 5: Conveying Modified Source Versions
When distributing modified FFNx source:
1. Must carry prominent notices stating modifications were made
2. Must include relevant date of modifications
3. Must state it's released under GPLv3
4. Must license entire work under GPLv3
5. If interactive, must display "Appropriate Legal Notices"

### Section 6: Conveying Non-Source Forms (Binaries)
When distributing FFNx binaries (`.dll` files):
- Must accompany with source code OR
- Provide written offer (valid 3+ years) to provide source OR
- Provide access to copy source from network server

### Section 11: Patents
- Contributors grant non-exclusive, worldwide, royalty-free patent license
- Patent license automatically extends to all recipients
- Protects users from patent claims

### Section 15-16: Warranty Disclaimer
```
NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.
PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
```

---

## Implications for FF7 Japanese Mod Project

### ✅ What You CAN Do

1. **Use FFNx freely** - No restrictions on using FFNx for the Japanese localization project
2. **Modify FFNx source** - You can modify FFNx code (e.g., PR737 changes for Japanese text support)
3. **Distribute your mod** - You can distribute the complete mod package including FFNx
4. **Commercial use** - Can charge for distribution if desired (though not typical for fan mods)

### ⚠️ What You MUST Do If Distributing FFNx Binaries

1. **Include source code access**:
   - Provide link to FFNx GitHub repository
   - If using modified FFNx, must provide your modified source code

2. **Include license file**:
   - Must include `COPYING.txt` (GPLv3 text) with distributions

3. **Preserve copyright notices**:
   - Keep all existing FFNx copyright headers
   - Add your own copyright for modifications

4. **Mark modifications**:
   - If modifying FFNx code, clearly mark what was changed and when
   - Example: "Modified 2026-01-16 for Japanese text support"

5. **License modifications as GPLv3**:
   - Any modifications to FFNx source must also be GPLv3
   - Must make modified source code available

### 🎯 What Is NOT Affected by GPLv3

**Your mod assets that don't incorporate FFNx source code are separate works:**

- **Translation files** (`.txt`, `.csv`, character mappings) - You choose the license
- **Texture files** (`.png`, `.tex` font textures) - You choose the license
- **HEXT patches** (`.hext` memory patches) - You choose the license
- **Configuration files** (`.toml`, `.cfg`) - You choose the license
- **Documentation** (`.md` files, guides) - You choose the license
- **7th Heaven mod package** (`.iro` installer) - You choose the license

**Rationale**: These assets are data files consumed by FFNx, not derivative works of FFNx source code. They form an "aggregate" with FFNx (GPLv3 Section 5, paragraph starting "A compilation of a covered work...").

---

## No Additional Terms or Contributor License Agreement

**Finding**: FFNx uses standard GPLv3 with no additional terms:

- No Contributor License Agreement (CLA) required
- No separate Terms of Service
- No trademark restrictions beyond GPLv3 Section 7(e)
- No additional permissions or restrictions

**Evidence**:
- Searched 242 files containing "license" references
- Only `COPYING.txt` found with license terms
- GitHub repository uses standard GPLv3 without modifications

---

## Practical Distribution Guidelines

### Recommended Distribution Approach

**Option 1: Link to Official FFNx** (Simplest)
```
Your mod package includes:
- Translation assets (your license)
- HEXT patches (your license)
- Installation instructions referencing official FFNx download

User separately downloads FFNx from official source.
GPL compliance: Not distributing FFNx binaries, so no GPL obligations.
```

**Option 2: Bundle FFNx** (More user-friendly)
```
Your mod package includes:
- Translation assets (your license)
- HEXT patches (your license)
- FFNx binaries (FFNx.dll, etc.)
- COPYING.txt (GPLv3 license)
- Link to FFNx GitHub source: https://github.com/julianxhokaxhiu/FFNx

GPL compliance: Providing link to source satisfies GPL requirements.
```

**Option 3: Modified FFNx** (If you modify FFNx source)
```
Your mod package includes:
- Translation assets (your license)
- HEXT patches (your license)
- Modified FFNx binaries
- COPYING.txt (GPLv3 license)
- Link to YOUR modified FFNx source repository
- MODIFICATIONS.txt listing changes made and dates

GPL compliance: Must provide your modified source code.
```

---

## Example Distribution Notice

If bundling FFNx with your mod, include this notice:

```markdown
# License Information

## FFNx Game Driver
This mod includes FFNx, a next-generation game driver for Final Fantasy VII.

- **License**: GNU General Public License v3.0 (GPLv3)
- **Copyright**: FFNx contributors
- **Source Code**: https://github.com/julianxhokaxhiu/FFNx
- **License Text**: See COPYING.txt

FFNx is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

## FF7 Japanese Localization Assets
Translation data, textures, and configuration files (excluding FFNx):

- **License**: [Your choice - e.g., CC BY-SA 4.0, MIT, etc.]
- **Copyright**: [Your name/team], 2026
- **Repository**: [Your GitHub/hosting link]
```

---

## Questions Addressed

### Q: Can I use FFNx for my Japanese mod?
**A**: Yes, absolutely. GPLv3 allows unlimited use for any purpose.

### Q: Do I need permission from FFNx developers?
**A**: No. GPLv3 grants permission automatically to all users.

### Q: Can I modify FFNx to add Japanese text support?
**A**: Yes, but you must:
1. Make your modifications available as source code
2. License your modifications under GPLv3
3. Mark what you changed and when

### Q: Can I distribute my mod with FFNx included?
**A**: Yes, but you must:
1. Include the GPLv3 license text (COPYING.txt)
2. Provide link to FFNx source code
3. If you modified FFNx, provide link to YOUR modified source

### Q: Does GPLv3 affect my translation files and textures?
**A**: No. Your assets are separate works. You can license them however you want.

### Q: Can I sell my mod?
**A**: Technically yes (GPLv3 allows commercial distribution), but:
- You must still provide source code
- Recipients can freely redistribute
- Fan mod community typically expects free distribution
- Square Enix copyright on original FF7 content is separate legal issue

### Q: What if I only use official FFNx and don't modify it?
**A**: Easiest path - just provide link to official FFNx. No GPL obligations since you're not distributing FFNx yourself.

---

## File Search Results

### License-Related Files Found in FFNx-PR737

Grep search for "license|LICENSE|License" found 242 files:
- **Primary license file**: `COPYING.txt` (GPLv3 full text)
- **Source code headers**: Most `.cpp` and `.h` files contain GPLv3 headers
- **HEXT patches**: German/English/Spanish/French variants all under FFNx GPL
- **Build configuration**: CMake files, vcpkg ports, all under GPL

**Key observation**: No additional license files, CLAs, or terms of service found. Pure GPLv3.

---

## Additional Resources

### Official Links
- **FFNx GitHub**: https://github.com/julianxhokaxhiu/FFNx
- **GPLv3 Full Text**: https://www.gnu.org/licenses/gpl-3.0.html
- **GPLv3 FAQ**: https://www.gnu.org/licenses/gpl-faq.html
- **GPL Compliance Guide**: https://www.gnu.org/licenses/gpl-howto.html

### Relevant GPLv3 Documentation
- **"Why Not LGPL"**: https://www.gnu.org/licenses/why-not-lgpl.html
- **Quick Guide to GPLv3**: https://www.gnu.org/licenses/quick-guide-gplv3.html

---

## Session Actions Taken

1. **Read FFNx license file**: Examined `FFNx-PR737/COPYING.txt` (674 lines, complete GPLv3 text)
2. **Searched for additional terms**: Grepped 242 files for license references
3. **Analyzed license implications**: Determined applicability to mod project
4. **Documented findings**: Created this comprehensive summary
5. **Appended resume command**: Added session to `/home/johnzealanddoyle/projects/tools/.project/resume/resume.txt`

---

## Key Takeaways

1. ✅ **FFNx uses standard GPLv3** - No surprises or additional restrictions
2. ✅ **Your mod assets are separate** - Translation files, textures, HEXT patches can use any license
3. ✅ **Simple compliance** - Just include COPYING.txt and link to source if bundling FFNx
4. ✅ **Modification allowed** - Can modify FFNx for Japanese support, must share modifications
5. ✅ **No permission needed** - GPL grants all necessary rights automatically

---

## Recommendations

### For Distribution

**Best Practice Approach**:
1. Keep mod assets (translations, textures) separate from FFNx
2. License your assets under permissive license (MIT, CC BY-SA 4.0, etc.)
3. If bundling FFNx, include `COPYING.txt` and source link
4. If modifying FFNx, publish modified source on GitHub

**Legal Safety**:
- ✅ GPL compliance for FFNx is straightforward
- ✅ Your assets remain under your control
- ⚠️ Square Enix copyright on original FF7 content is separate issue (fan mod legal gray area)

### For Development

**Current Status**: Using PR737 (reference copy) of FFNx
- Contains Japanese text implementation changes
- Should verify if PR737 changes are merged into mainline FFNx
- If using modified FFNx, must provide source when distributing

---

## Technical Notes

### FFNx-PR737 Directory Structure
- **License file location**: `/FFNx-PR737/COPYING.txt`
- **Source code**: `/FFNx-PR737/src/` (all GPLv3)
- **HEXT patches**: `/FFNx-PR737/misc/hext/` (German, English, Spanish, French variants)
- **Build system**: CMake-based with vcpkg dependencies

### Session Environment
- **PWD**: `/home/johnzealanddoyle/projects/ff7OG_japanese`
- **Git branch**: `main`
- **Session ID**: `1603cb3d-a631-4649-8c10-c09e0731a34b`
- **Tmux**: Session `ff7OG_japanese` ($4), Window `claude-1603cb3d` (@13), Pane %13

---

## Resume Command

Session logged to resume file:
```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese; claude --dangerously-skip-permissions --resume 1603cb3d-a631-4649-8c10-c09e0731a34b #FFNx-license-investigation
```

---

**End of Session Summary**

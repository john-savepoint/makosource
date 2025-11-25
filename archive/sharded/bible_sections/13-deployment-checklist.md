# 13. DEPLOYMENT CHECKLIST

## 13.1 Pre-Release Validation

Before distributing to users, complete this checklist:

**Code Quality:**

- [ ] All debug logging is disabled or conditional
- [ ] No hardcoded addresses (use `common_externals`)
- [ ] No placeholder memory addresses (0xCC0000 replaced)
- [ ] Error handling for all file operations
- [ ] Memory leaks checked (Valgrind / Dr. Memory)
- [ ] Code reviewed for security issues
- [ ] Comments explain complex logic
- [ ] Version number updated

**Functionality:**

- [ ] English mode tested and working
- [ ] Japanese mode tested with real textures
- [ ] ff7_en.exe compatibility verified
- [ ] ff7_ja.exe compatibility verified (if supporting)
- [ ] Steam version tested
- [ ] All font pages load correctly
- [ ] Page switching works (FA-FE codes)
- [ ] Character widths correct (no squashing)
- [ ] No crashes in 1-hour play session

**Assets:**

- [ ] All 6 jafont_*.png files prepared
- [ ] Correct resolution (1024×1024)
- [ ] Correct grid layout (16×16)
- [ ] All required characters mapped
- [ ] character_map_accurate.csv up to date
- [ ] Assets tested in-game
- [ ] File sizes reasonable (< 1MB each)

**Documentation:**

- [ ] Installation guide written
- [ ] Configuration guide (FFNx.toml settings)
- [ ] Troubleshooting section
- [ ] Credits and attribution
- [ ] License information (MIT for FFNx)
- [ ] Known issues documented

**Distribution Package:**

- [ ] FFNx.dll compiled (Release mode)
- [ ] All 6 font textures included
- [ ] Example FFNx.toml with Japanese settings
- [ ] README.md with installation steps
- [ ] CHANGELOG.md with version history
- [ ] LICENSE file
- [ ] Optional: Installer script (batch file)

---

## 13.2 User Installation Guide Template

Create a `README.md` for users:

```markdown
# FFNx Japanese Language Support

Native Japanese text rendering for Final Fantasy VII (PC).

# Installation

1. **Install FFNx** (if not already installed):
   - Download from: https://github.com/julianxhokaxhiu/FFNx
   - Follow FFNx installation instructions

2. **Install Japanese Font Mod**:
   - Extract this archive to your FF7 directory
   - Files should be placed in:
     - `mods/Textures/menu/jafont_1.png`
     - `mods/Textures/menu/jafont_2.png`
     - (etc.)

3. **Configure FFNx**:
   - Open `FFNx.toml` in a text editor
   - Find the line: `font_language = "en"`
   - Change to: `font_language = "ja"`
   - Save and close

4. **Install Japanese Text** (optional):
   - Use 7th Heaven to install a Japanese translation mod
   - OR use the original Japanese executable (ff7_ja.exe)

# Troubleshooting

**Issue: Text appears squashed**
- Solution: Ensure `font_language = "ja"` in FFNx.toml
- Restart the game after changing settings

**Issue: Blank boxes instead of Kanji**
- Solution: Verify all 6 jafont_*.png files are in the correct folder
- Check FFNx.log for "Failed to load" errors

**Issue: Game crashes on menu open**
- Solution: Re-extract the mod files
- Ensure you're using FFNx version 1.X or later
- Check for conflicting mods

# Credits

- FFNx: Julian Xhokaxhiu and contributors
- Japanese Font Textures: [Your Name]
- Character Mapping: [Contributors]

# License

This mod is released under [License]. FFNx is licensed under MIT.
```

---

## 13.3 7th Heaven .iro Package Creation

**For Distribution via 7th Heaven:**

**Step 1: Create Mod Structure**

```
MyJapaneseFontMod/
├── info.json
├── mod.xml
└── assets/
    └── menu/
        ├── jafont_1.png
        ├── jafont_2.png
        ├── jafont_3.png
        ├── jafont_4.png
        ├── jafont_5.png
        └── jafont_6.png
```

**Step 2: Create info.json**

```json
{
  "ID": "japanese-font-support",
  "Name": "Japanese Font Support",
  "Author": "Your Name",
  "Version": "1.0.0",
  "Description": "Native Japanese text rendering with 6 high-resolution font pages. Requires FFNx.",
  "Category": "Fonts",
  "ReleaseDate": "2025-11-24",
  "Tags": ["Japanese", "Fonts", "FFNx"],
  "CompatibleGameVersions": ["1.02 US", "Steam 2013"],
  "RequiredMods": ["FFNx"]
}
```

**Step 3: Create mod.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<ModConfig>
  <ID>japanese-font-support</ID>
  <Name>Japanese Font Support</Name>
  <Files>
    <File>
      <Source>assets/menu/jafont_1.png</Source>
      <Destination>mods/Textures/menu/jafont_1.png</Destination>
    </File>
    <File>
      <Source>assets/menu/jafont_2.png</Source>
      <Destination>mods/Textures/menu/jafont_2.png</Destination>
    </File>
    <!-- Repeat for all 6 files -->
  </Files>
  <ConfigOptions>
    <Option name="font_language" value="ja" description="Enable Japanese language mode in FFNx.toml" />
  </ConfigOptions>
</ModConfig>
```

**Step 4: Package as .iro**

```batch
7z a -tzip MyJapaneseFontMod.iro *
ren MyJapaneseFontMod.zip MyJapaneseFontMod.iro
```

**Step 5: Test in 7th Heaven**

1. Open 7th Heaven
2. Library → Import Mod
3. Select your .iro file
4. Enable the mod
5. Launch game and test

---

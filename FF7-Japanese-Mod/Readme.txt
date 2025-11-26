Japanese Text Support for FF7 (PR #737)
=========================================

Version: 1.0
Created: 2025-11-25
Author: John Zealand-Doyle (Assets) + CosmosXIII (PR #737 Implementation)

REQUIREMENTS
------------
1. FFNx graphics driver with PR #737 support
2. Set ff7_japanese_edition = true in FFNx.toml
3. English FF7 executable (ff7_en.exe)

WHAT THIS MOD INCLUDES
----------------------
- 6 Japanese font texture pages (jafont_1.png through jafont_6.png)
- Japanese field dialogue (jfleve.lgp)
- Japanese menu/battle text (KERNEL.BIN, kernel2.bin)
- Total: 1,536 Japanese characters (Hiragana, Katakana, Kanji)

INSTALLATION VIA 7TH HEAVEN
----------------------------
1. Import this IRO into 7th Heaven
2. Enable the mod in My Mods tab
3. Edit FFNx.toml (found in 7th Heaven app data folder)
4. Add line: ff7_japanese_edition = true
5. Save and close
6. Click Play in 7th Heaven

INSTALLATION WITHOUT 7TH HEAVEN
--------------------------------
1. Extract this IRO to FF7 install directory
2. Files should go to:
   - mods/Textures/menu/jafont_*.png
   - lang-ja/kernel/KERNEL.BIN
   - lang-ja/kernel/kernel2.bin
   - lang-ja/field/jfleve.lgp
3. Edit FFNx.toml in FF7 directory
4. Add line: ff7_japanese_edition = true
5. Launch ff7_en.exe

BUILDING FFNX WITH PR #737
---------------------------
If PR #737 isn't merged yet:

1. Clone FFNx: git clone https://github.com/julianxhokaxhiu/FFNx.git
2. Fetch PR: git fetch origin pull/737/head:pr-737
3. Checkout: git checkout pr-737
4. Build on Windows with Visual Studio 2022
5. Copy FFNx.dll to FF7 directory

VERIFICATION
------------
Check FFNx.log for these lines:
- "Japanese edition mode: ENABLED"
- "Loading texture: menu/jafont_1.png"
- All 6 font textures should load successfully

KNOWN ISSUES
------------
From PR #737:
- Colored text may not work correctly
- Character input (name entry) may be corrupted
- Cursor alignment may be slightly off

These are documented bugs awaiting fixes.

WHAT WORKS
----------
- Field dialogue (NPC conversations)
- Menu screens (Item, Magic, Materia, etc.)
- Battle menus (Attack, Magic, commands)
- Character names
- Item descriptions
- Variable-width fonts (not squashed)

CREDITS
-------
- Font implementation: CosmosXIII (GitHub PR #737)
- FFNx driver: Julian Xhokaxhiu and contributors
- Assets: Final Fantasy VII International Edition (Square Enix)
- Mod packaging: John Zealand-Doyle

LICENSE
-------
Assets extracted from legally owned copy of FF7 International Edition.
For personal use only. Do not distribute commercially.

SUPPORT
-------
- FFNx GitHub: https://github.com/julianxhokaxhiu/FFNx
- PR #737: https://github.com/julianxhokaxhiu/FFNx/pull/737
- Qhimm Forums: https://forums.qhimm.com/

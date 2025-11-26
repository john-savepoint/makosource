# Tool Documentation Verification Log

**Created:** 2025-11-25 12:15:00 JST (Tuesday)
**Session-ID:** 8f58819d-f9c4-4f04-8e95-4af04d782606
**Purpose:** Document verification status of all tools referenced in project guides

---

## Summary

This log records the verification of tool documentation in:
- `docs/7TH_HEAVEN_DEVELOPER_GUIDE.md` (Section 7.3-7.5)
- `docs/reference/TOOL_GUIDE.md`

### Verification Sources Used

| Source | URL | Type |
|--------|-----|------|
| 7th Heaven Official Help | https://7thheaven.rocks/help/userhelp.html | Primary/Authoritative |
| 7th Heaven GitHub | https://github.com/tsunamods-codes/7th-Heaven | Primary/Authoritative |
| Qhimm Forums | https://forums.qhimm.com/ | Community/Primary |
| OatBran 7H Steam Guide | https://github.com/OatBran/7HSteamGuide | Community/Secondary |

---

## 7th Heaven Built-in Tools (Section 7.3)

### 7.3.1 Pack/Unpack IRO Archives

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Official documentation at 7thheaven.rocks/help/userhelp.html |

**Official Location:** Tools > IRO Tools > Pack IRO / Unpack IRO tabs

**Verified Features:**
- Pack IRO tab: Convert folder to .iro file
- Unpack IRO tab: Extract .iro to folder
- Compression options: Nothing, Everything, byExtension, byContent

**Source:** https://7thheaven.rocks/help/userhelp.html#irotools

---

### 7.3.2 IRO Tools (Advanced Operations)

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Official documentation at 7thheaven.rocks/help/userhelp.html |

**Official Location:** Tools > IRO Tools

**Verified Features:**
- Patch IRO tab: Compare original vs new .iro, generate .irop patch
- Patch IRO (Advanced) tab: Manual patch creation with custom file list

**Source:** https://7thheaven.rocks/help/userhelp.html#irotools

---

### 7.3.3 Catalog/Mod Creation Tool

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Official documentation at 7thheaven.rocks/help/userhelp.html |

**Official Location:** Tools > Catalog/Mod Creation Tool

**Verified Features:**
- Create Mod tab: Generate mod.xml with unique GUID
- Create Catalog tab: Generate catalog XML for distribution
- Mega Link Generator tab: Generate links from Mega folder IDs

**Source:** https://7thheaven.rocks/help/userhelp.html#catalogmodcreationtool

---

### 7.3.4 Make IRO from DDS Files

| Status | Verification |
|--------|--------------|
| **NOT A 7TH HEAVEN TOOL** | Confusion with external tool |

**CORRECTION:** This is NOT a built-in 7th Heaven tool. The referenced feature is part of the **SYW Pack Builder** by Satsuki, an external third-party tool.

**What Actually Exists:**
- SYW Pack Builder (external): https://forums.qhimm.com/index.php?topic=19204.0
- Satsuki PNG to DDS Converter: http://forums.qhimm.com/index.php?topic=19701.0

**Source:** OatBran's 7H Steam Guide confirms this is an external tool, not 7th Heaven built-in.

**Action Required:** Remove Section 7.3.4 from 7TH_HEAVEN_DEVELOPER_GUIDE.md or clarify it's an external tool.

---

### 7.3.5 Movie Importer Tool

| Status | Verification |
|--------|--------------|
| **PARTIALLY INCORRECT** | Exists but purpose misrepresented |

**Official Location:** Tools > Movie Importer

**CORRECTION - Actual Purpose:**
The Movie Importer is specifically for **copying FMV files from original 1998 physical game discs** to the hard drive. It is NOT a video encoding/conversion tool.

**Official Description (verbatim):**
> "If you have the original 1998 disc release of Final Fantasy VII, this tool will assist you with copying over the movies from disc onto the hard drive. If all movie files are already found on your computer, this option is disabled."

**What It Does:**
1. Prompts user to insert physical game discs
2. Copies movie files from disc to movies folder
3. Disabled if movies already exist on drive

**What It Does NOT Do:**
- Does NOT convert video formats (AVI, MKV, MP4, etc.)
- Does NOT encode/re-encode videos
- Does NOT support modern codec conversion
- Has NO encoding options (resolution, bitrate, etc.)

**Source:** https://7thheaven.rocks/help/userhelp.html#importmovies

**Action Required:** Completely rewrite Section 7.3.5 to reflect actual functionality.

---

### 7.3.6 Profile Debug and Variable Dumping

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Official documentation at 7thheaven.rocks/help/userhelp.html |

**Official Location:** Play button dropdown menu

**Verified Features:**
- "Play With Debug Log" - Verbose logging, detailed file operations
- "Play With Variable Dump" - TurBoLog with variable values dumped
- "Play With Minimal Validation" - Skip validation checks
- "Play Without Mods" - Vanilla game launch

**Official Description:**
> "The Debug Log and Variable Dump can be useful for troubleshooting 7th Heaven and/or mod files."

**Source:** https://7thheaven.rocks/help/userhelp.html#playbutton

**Note:** The detailed log settings (log levels, log locations, wrapper debug) mentioned in Section 7.4 could NOT be verified in official documentation. These may exist in FFNx.toml or internal settings but are not documented at 7thheaven.rocks.

---

### 7.3.7 Chunking Tools

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Official documentation at 7thheaven.rocks/help/userhelp.html |

**Official Location:** Tools > Chunk Tool

**Verified Purpose:**
Extract portions of flevel.lgp into "Chunks" for translation mods without needing the full LGP.

**Official Description (verbatim):**
> "This tool is useful for modders. It allows you to extract only a portion of the flevel.lgp file into 'Chunks'. This is great if you need to distribute a portion of a customized flevel.lgp file in your mod without needing to include the entire file, to keep file sizes down and to lower conflicts with other mods."

**Verified Features:**
- Select source flevel.lgp file
- Select output folder
- Choose sections to extract (e.g., "Section 1 Field Script Dialog")

**Source:** https://7thheaven.rocks/help/userhelp.html#chunktool

**Note:** The IRO chunking for file size limits mentioned in Section 7.3.7 of our guide is NOT the same as this Chunk Tool. IRO chunking (.chunk.001, .chunk.002, etc.) is part of catalog/distribution features, not the Chunk Tool.

---

## Section 7.4 Debug and Development Settings

| Status | Verification |
|--------|--------------|
| **PARTIALLY UNVERIFIED** | Some settings not found in official docs |

**Verified (from Play button dropdown):**
- Play With Debug Log
- Play With Variable Dump
- Play With Minimal Validation

**UNVERIFIED (could not find official source):**
- Specific log file locations (%APPDATA%\7th Heaven\logs\)
- Wrapper.log format and content
- Debug LogLevel settings (0-5)
- DumpVarState option
- 7thHeaven.ini [Debug] section

**Note:** These settings may exist but are not documented on 7thheaven.rocks. They may be internal/advanced features or based on older versions.

**Action Required:** Mark these as "Based on community knowledge - verify in application" or remove if cannot be confirmed.

---

## External Tools (TOOL_GUIDE.md)

### ulgp v1.2

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Qhimm forums thread exists |

**Forum Thread:** https://forums.qhimm.com/index.php?topic=12831.0
**Dropbox Link in TOOL_GUIDE:** https://www.dropbox.com/s/o770wtunby0k89y/ulgp_v1.2.7z?dl=0

**Note:** Dropbox link functionality not tested (may have expired). Forum thread confirmed active.

---

### Image2TEX

| Status | Verification |
|--------|--------------|
| **VERIFIED** | GitHub repository exists |

**GitHub:** https://github.com/niemasd/Image2TEX
**Status:** Source code available, requires VB6 compilation

---

### Tex Tools (FF7 Tex Image Tool)

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Qhimm forums thread exists |

**Forum Thread:** https://forums.qhimm.com/index.php?topic=17755.0
**Latest Version:** v1.0.4.7 (batch support added)
**Author Website:** http://seiferalmasy.is-best.net/ (may be unreliable)

**Note:** User in 2022 reported v1.0.4.7 download link broken, only older version available.

---

### tim2png (ff7tools)

| Status | Verification |
|--------|--------------|
| **VERIFIED** | GitHub repository exists |

**GitHub:** https://github.com/cebix/ff7tools
**Language:** Python (requires Pillow >= 10.3.0)

---

### FFNx Texture Dumping

| Status | Verification |
|--------|--------------|
| **VERIFIED** | Based on FFNx.toml in cloned repo |

**Relevant Settings:**
- `save_textures` - Dump textures to mod_path
- `show_missing_textures` - Show which textures lack overrides
- `mod_path` - Path for texture overrides

---

## Corrections Required

### HIGH PRIORITY

1. **Section 7.3.4 (Make IRO from DDS Files)**
   - REMOVE or CLARIFY as external tool (SYW Pack Builder)
   - Not a 7th Heaven built-in feature

2. **Section 7.3.5 (Movie Importer Tool)**
   - COMPLETELY REWRITE
   - Actual purpose: Copy FMVs from 1998 physical discs
   - NOT a video encoder/converter

### MEDIUM PRIORITY

3. **Section 7.3.7 (Chunking Tools)**
   - CLARIFY distinction between:
     - Chunk Tool (flevel.lgp extraction)
     - IRO chunking for distribution (.chunk.001 files)

4. **Section 7.4 (Debug Settings)**
   - ADD warning that specific log paths/formats unverified
   - Mark as "community knowledge"

### LOW PRIORITY

5. **External Tool Links**
   - Verify Dropbox links still work
   - Note v1.0.4.7 Tex Tool download may be unavailable

---

## Verification Methodology

1. **Primary Source:** 7thheaven.rocks official help documentation
2. **Secondary Source:** GitHub repositories (tsunamods-codes, tool authors)
3. **Tertiary Source:** Qhimm forums threads
4. **Cross-reference:** Community guides (OatBran's guide)

**Tools Used:**
- Firecrawl MCP server for web scraping
- BraveSearch MCP server for discovery

---

**END OF VERIFICATION LOG**

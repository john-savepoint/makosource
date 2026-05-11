# FFNx Japanese Language Implementation Project

**Created:** 2025-11-24 22:10:00 JST (Monday)
**Last Updated:** 2025-12-04 17:58 JST (Thursday)
**Project Status:** Phase 1 - BREAKTHROUGH ACHIEVED - Japanese text rendering working!
**Platform:** WSL2 (Development) + Windows (Build/Runtime)

---

## 🚨 CRITICAL UPDATE - 2025-11-26

### MAJOR BREAKTHROUGH ACHIEVED

**We have successfully:**

1. ✅ Built FFNx PR #737 from source with custom modifications
2. ✅ Japanese fonts loading and rendering correctly
3. ✅ Battle text, items, kernel-based text all working in Japanese
4. ✅ First-ever Japanese text on English `ff7_en.exe`!

**Remaining Issue:**

- ❌ Field dialogue shows garbled text (encoding interpretation issue)

**For the next agent:** Read `docs/SESSION_HANDOFF_2025-11-26.md` FIRST - it contains complete context for continuing this work.

---

## 🎯 Project Overview

This project implements native Japanese text rendering support for Final Fantasy VII PC (1998) using the FFNx graphics driver. The goal is to create a language-learning edition that allows players to switch between languages (English, Japanese, and potentially others) to aid in language acquisition.

**Key Features:**

- Multi-page Japanese font system (6 texture pages, ~2,300 characters)
- FA-FE character encoding support
- Runtime language switching (future - Phase 2)
- Furigana pronunciation guides (future - Phase 3)
- Crowdsourced translation system (future - Phase 6)

---

## 📁 Current Directory Structure

```
ff70G-japanese-mod/
├── README.md                    # ⭐ START HERE (this file)
├── DOCUMENTATION_MAP.md         # Navigation guide for all documents
│
├── docs/                        # 📚 All Documentation
│   ├── README.md               # Docs directory guide (see below)
│   ├── FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md  # Complete spec
│   ├── IMPLEMENTATION_READINESS_ASSESSMENT.md         # Phase 0 requirements
│   ├── IMPLEMENTATION_VERIFICATION_CHECKLIST.md       # Validation checklist
│   ├── PROJECT_OVERVIEW.md                            # Architecture overview
│   ├── TEST_PROCEDURE.md                              # Testing guide
│   ├── masterfindings.md                              # Research history
│   ├── REORGANIZATION_PLAN.md                         # Directory cleanup guide
│   │
│   ├── character_maps/          # Character mappings
│   │   ├── JAFONT_CHARACTER_MAP.md
│   │   └── ff7_complete_mapping_compact.csv  # ⭐ THE MAPPING FILE
│   │
│   ├── reference/               # Reference documentation
│   │   ├── AF3DN_ANALYSIS.md
│   │   ├── BEGINNER_GUIDE.md
│   │   ├── TOOL_GUIDE.md
│   │   └── game_engine/        # FF7 game engine manual
│   │
│   ├── roadmap/                 # Feature roadmap
│   │   ├── FEATURE_ROADMAP.md           # Phases 1-6
│   │   └── FFNX_CROWDSOURCED_TRANSLATION_SPEC.md  # Phase 6 detailed spec
│   │
│   ├── to_combine/              # To be integrated later
│   │   ├── ARCHITECTURE_CLARIFICATION.md
│   │   └── MULTI_LANGUAGE_FINDINGS.md
│   │
│   └── sharded/                 # Sharded large documents
│       ├── bible_sections/     # Master Bible (18 files)
│       └── findings_sections/  # Research findings (29 files)
│
├── assets/                      # 🎨 Game Assets
│   ├── fonts/
│   │   ├── png/                # ⭐ jafont_*.png (6 files - CRITICAL)
│   │   └── tex/                # jafont_*.tex (6 files - original format)
│   └── character_mappings/
│       └── interactive_viewer/ # HTML tool for manual mapping
│
├── reference/                   # 📖 Read-Only Reference Materials
│   ├── ff7_disassembly/        # FF7 executable disassembly
│   └── repomix_snapshots/      # FFNx codebase snapshots
│
├── archive/                     # 📦 Historical/Unused Files
│   ├── scripts/                # Research scripts (not needed for implementation)
│   ├── character_tables_debug/
│   ├── character_tables_verification/
│   ├── character_tables_pre-interactive/
│   ├── findings_legacy/
│   ├── SCRAPED_URLS.md
│   └── UNSCRAPPED_URLS.md
│
└── logs/                        # Session logs (debugging only)
```

---

## 🚀 Quick Start Guide

### For Humans (New to Project)

1. **Read this file** (README.md) - Get oriented
2. **Read [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)** - Find specific documents
3. **Read [docs/reference/BEGINNER_GUIDE.md](docs/reference/BEGINNER_GUIDE.md)** - Understand the basics
4. **Read [docs/IMPLEMENTATION_READINESS_ASSESSMENT.md](docs/IMPLEMENTATION_READINESS_ASSESSMENT.md)** - Current status

### For LLMs (AI Assistants)

1. **Read this file** (README.md) - Project structure
2. **Read [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)** - Document navigation
3. **Read [docs/README.md](docs/README.md)** - Detailed docs guide
4. **Based on your task**, navigate to appropriate document:
   - **Implementation**: `docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md`
   - **Verification**: `docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md`
   - **Phase 0 Setup**: `docs/IMPLEMENTATION_READINESS_ASSESSMENT.md`

### For Implementers (Starting Phase 0)

**Essential reading order:**

1. [docs/IMPLEMENTATION_READINESS_ASSESSMENT.md](docs/IMPLEMENTATION_READINESS_ASSESSMENT.md) - What we need
2. [docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md](docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md) - Validation questions
3. [docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md](docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md) - Complete spec
4. [docs/reference/TOOL_GUIDE.md](docs/reference/TOOL_GUIDE.md) - Tool chain

---

## 📋 Project Status & Timeline

### Current Status: ✅ **Phase 1 - Major Progress**

**What We Have (COMPLETED):**

- ✅ Complete research (9 sessions, 40+ findings)
- ✅ Character mapping (1,536 characters in 6 textures)
- ✅ Font texture assets (6 PNG + 6 TEX files)
- ✅ FFNx PR #737 built from source
- ✅ Custom LGP redirection code (flevel.lgp → jfleve.lgp)
- ✅ Japanese kernel text working (battle, items, menus)
- ✅ Japanese fonts loading correctly

**What We Need (CURRENT BLOCKER):**

- ❌ Fix field dialogue encoding interpretation
- ⚠️ Text byte pipeline needs debugging
- ⚠️ May need text parser hook for FA-FE encoding on English exe

### Implementation Timeline

| Phase       | Description                                      | Duration   | Status                                                    |
| ----------- | ------------------------------------------------ | ---------- | --------------------------------------------------------- |
| **Phase 0** | Research & Setup                                 | 3-6 days   | ✅ **COMPLETE**                                           |
| **Phase 1** | Core Japanese Rendering                          | 1-2 weeks  | ⏳ **95% COMPLETE** - field text encoding issue remaining |
| **Phase 2** | Texture Allocation Override                      | 1-2 weeks  | ✅ Working (via PR #737)                                  |
| **Phase 3** | Assembly Hooks & Renderer                        | 3-4 weeks  | ⏳ Partial - need text parser hook                        |
| **Phase 4** | Advanced Features (Furigana, Language Switching) | 4-6 weeks  | ⏸️ Future                                                 |
| **Phase 5** | Polish & Distribution                            | 2-4 weeks  | ⏸️ Future                                                 |
| **Phase 6** | Crowdsourced Translation System                  | 8-10 weeks | ⏸️ Optional Future                                        |

**Total Estimated Timeline:**

- **Core Implementation** (Phase 0-3): 10-14 weeks
- **With Advanced Features** (Phase 0-5): 14-22 weeks
- **Complete System** (Phase 0-6): 22-32 weeks

---

## 🔑 Critical Files by Purpose

### For Windows Transfer (Essential)

**MUST transfer these:**

```
docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md
docs/IMPLEMENTATION_READINESS_ASSESSMENT.md
docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md
docs/reference/TOOL_GUIDE.md
assets/fonts/png/*.png (6 files)
assets/character_mappings/interactive_viewer/ff7_complete_mapping_compact.csv
```

**Total size:** ~15-20MB

### Optional but Helpful

```
docs/to_combine/ARCHITECTURE_CLARIFICATION.md
docs/to_combine/MULTI_LANGUAGE_FINDINGS.md
docs/reference/AF3DN_ANALYSIS.md
docs/sharded/bible_sections/ (if prefer sharded version)
reference/ff7_disassembly/ (if need disassembly reference)
```

### Skip (NOT needed on Windows)

```
archive/ (all - research artifacts)
logs/ (all - Mac session data)
.venv/ (Python environment - Mac specific)
.claude/ (IDE data - Mac specific)
docs/sharded/findings_sections/ (legacy research)
reference/repomix_snapshots/ (can regenerate if needed)
```

---

## 📚 Key Documentation

### Core Documents

| Document                                                             | Purpose                 | Read Time |
| -------------------------------------------------------------------- | ----------------------- | --------- |
| [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)                         | Navigation guide        | 5 min     |
| [docs/README.md](docs/README.md)                                     | Docs directory guide    | 5 min     |
| [docs/reference/BEGINNER_GUIDE.md](docs/reference/BEGINNER_GUIDE.md) | Beginner-friendly intro | 10 min    |
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)                 | Complete architecture   | 30 min    |

### Implementation Documents (Phase 0+)

| Document                                                                                               | Purpose                 | Audience         |
| ------------------------------------------------------------------------------------------------------ | ----------------------- | ---------------- |
| [docs/IMPLEMENTATION_READINESS_ASSESSMENT.md](docs/IMPLEMENTATION_READINESS_ASSESSMENT.md)             | Phase 0 requirements    | Implementers     |
| [docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md](docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md)         | Verification questions  | Implementers, QA |
| [docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md](docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md) | Complete technical spec | All implementers |

### Reference Documents

| Document                                                                                   | Purpose             | Use       |
| ------------------------------------------------------------------------------------------ | ------------------- | --------- |
| [docs/reference/TOOL_GUIDE.md](docs/reference/TOOL_GUIDE.md)                               | Tool chain guide    | How-to    |
| [docs/reference/AF3DN_ANALYSIS.md](docs/reference/AF3DN_ANALYSIS.md)                       | Reverse engineering | Reference |
| [docs/character_maps/JAFONT_CHARACTER_MAP.md](docs/character_maps/JAFONT_CHARACTER_MAP.md) | Character encoding  | Reference |
| [docs/TEST_PROCEDURE.md](docs/TEST_PROCEDURE.md)                                           | Testing guide       | QA        |

### Roadmap Documents

| Document                                                                                                 | Purpose               | Audience              |
| -------------------------------------------------------------------------------------------------------- | --------------------- | --------------------- |
| [docs/roadmap/FEATURE_ROADMAP.md](docs/roadmap/FEATURE_ROADMAP.md)                                       | All phases (1-6)      | Product management    |
| [docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md](docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md) | Phase 6 detailed spec | Full-stack developers |

---

## 🎯 Implementation Phases Explained

### Phase 0: Research & Setup (3-6 days) - **CURRENT**

**Goal:** Prepare Windows build environment and verify assumptions

**Tasks:**

1. Build FFNx from source on Windows
2. Reverse-engineer AF3DN.P (reference implementation)
3. Create test environment setup guide
4. Validate tool chain (Tex Tools, ulgp, Ghidra, x64dbg)
5. Document actual memory addresses (replace placeholders)

**Output:** Working build environment, verified memory addresses

---

### Phase 1-3: Core Implementation (8-12 weeks)

**Phase 1:** Configuration extension (FFNx.toml, config parsing)
**Phase 2:** Texture allocation override (6 slots instead of 1)
**Phase 3:** Assembly hooks + renderer integration (FA-FE page switching)

**Output:** Japanese text rendering working in-game

---

### Phase 4: Advanced Features (4-6 weeks) - Future

**Features:**

- Furigana support (pronunciation guides)
- Runtime language switching (F12 hotkey)
- Battle text support
- Minigame text support
- FMV subtitles (if applicable)

**Output:** Complete language-learning edition

---

### Phase 5: Polish & Distribution (2-4 weeks) - Future

**Tasks:**

- 7th Heaven .iro package
- User installation guide
- Performance optimization
- Community testing
- Release notes

**Output:** Shippable mod

---

### Phase 6: Crowdsourced Translation (8-10 weeks) - Optional

**Features:**

- In-game submission hotkey (Ctrl+T)
- Web-based voting/moderation platform
- Automated .iro export
- Community translation improvements

**Output:** Living, community-maintained translations

**See:** [docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md](docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md)

---

## 🧠 Technical Summary

**Problem:**

- FF7 English PC uses 1 font texture (256 characters max)
- Japanese needs ~2,300 characters (6 texture pages)
- Requires multi-page font system + FA-FE encoding

**Solution:**

- Extend FFNx driver (open-source, community-maintained)
- Replicate AF3DN.P's proven architecture (Square Enix, 2013)
- Implement 6-texture system + FA-FE byte markers
- Build for extensibility (future multi-language support)

**Why This Works:**

- Square Enix already proved it works (AF3DN.P reference)
- FFNx is actively maintained and extensible
- We have complete character mapping (1,331 chars, 100% accurate)
- We have font texture assets (extracted from official Japanese version)
- Architecture is well-documented (155K token specification)

---

## 🔨 Building FFNx from Source

This project requires building FFNx PR #737 from source. For a complete step-by-step guide, see **[docs/BUILD_ENVIRONMENT_SETUP.md](docs/BUILD_ENVIRONMENT_SETUP.md)**.

### Quick Start (If You're Experienced)

**Prerequisites:**

- Windows 10/11 (64-bit)
- Visual Studio 2022 Community with C++ workload
- CMake 3.15+ (we used portable CMake 3.27.8 at `C:\cmake-3.27.8\`)
- Git for Windows
- vcpkg (cloned to `C:\vcpkg\`)

**Clone PR #737:**

```batch
cd C:\
git clone --recursive https://github.com/julianxhokaxhiu/FFNx.git FFNx
cd FFNx
git fetch origin pull/737/head:pr737-japanese
git checkout pr737-japanese
```

**Bootstrap vcpkg:**

```batch
cd C:\vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg integrate install
```

**Configure and Build:**

```batch
cd C:\FFNx
cmake --preset Release
cmake --build .build --config Release
```

**Or from WSL2:**

```bash
powershell.exe -Command "cd C:\FFNx; C:\cmake-3.27.8\cmake-3.27.8-windows-x86_64\bin\cmake.exe --build .build --config Release"
```

**Build Output:**

- `C:\FFNx\.build\Release\FFNx.dll`
- Auto-copies to FF7 directories as `AF3DN.P`

**Build Time:**

- First build: 30-60 minutes (vcpkg compiles dependencies)
- Subsequent builds: 1-3 minutes

### Common Issues We Encountered

1. **soloud port errors** - We had to modify `.vcpkg/ports/soloud/portfile.cmake` to remove unsupported options
2. **mpg123 download blocked** - SourceForge/Cloudflare blocked aria2; downloaded manually from mpg123.de
3. **Architecture mismatch** - FF7 is 32-bit, must build as x86 (Win32), not x64
4. **FindSOLOUD.cmake architecture detection** - Fixed `Win64` vs `x64` detection

See [docs/SESSION_HANDOFF_2025-11-26.md](docs/SESSION_HANDOFF_2025-11-26.md) for detailed troubleshooting notes.

---

## 🔧 Tools & Dependencies

**Required for Building FFNx:**

- **Visual Studio 2022 Community** - C++ compiler with Windows SDK
- **CMake 3.15+** - Build system generator
- **vcpkg** - C++ package manager (compiles dependencies from source)
- **Git** - Version control

**Optional Tools:**

- **Ghidra** - For reverse engineering AF3DN.P
- **x64dbg** - Dynamic analysis/debugging
- **Tex Tools v1.0.4.7** - TEX ↔ PNG conversion
- **ulgp v1.2** - LGP extraction/repacking

**See:** [docs/reference/TOOL_GUIDE.md](docs/reference/TOOL_GUIDE.md) for complete tool chain documentation.

---

## 📞 Project Context

**Research Phase:** 2025-11-15 to 2025-11-24 (9 days, 10+ sessions)
**Documentation:** ~200K tokens across all documents
**Character Mapping:** Manual transcription of 1,331 characters (100% accuracy)
**Assets Prepared:** 6 font textures (PNG + TEX formats)
**Key Achievement:** First complete and accurate FF7 Japanese character table ever created

---

## 📖 Further Reading

- **Confused?** Start with [docs/reference/BEGINNER_GUIDE.md](docs/reference/BEGINNER_GUIDE.md)
- **Need a specific document?** Check [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)
- **Want complete navigation?** See [docs/README.md](docs/README.md)
- **Implementation ready?** Read [docs/IMPLEMENTATION_READINESS_ASSESSMENT.md](docs/IMPLEMENTATION_READINESS_ASSESSMENT.md)

---

**Document Version:** 2.1.0 (Added Build Instructions)
**Last Updated:** 2025-11-24 22:10:00 JST
**Next Review:** After Phase 0 completion

---

**For questions, navigation help, or detailed information, see [DOCUMENTATION_MAP.md](DOCUMENTATION_MAP.md)**

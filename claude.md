# FF7 Japanese Mod - Project Context

**Project:** FF7 Japanese Language Modification for FFNX
**Repository:** `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod`
**Status:** Active Research & Development
**Tech Stack:** Python, Shell Scripts, JSON/TOML Configuration, Font Rendering, Character Encoding

## Project Summary

This project aims to develop a comprehensive Japanese language modification for Final Fantasy VII using the FFNX engine. The work involves:

- Character mapping and font table extraction from Japanese FF7
- Interactive character visualization and OCR validation
- Custom Japanese font rendering for the FFNX mod engine
- Multi-language support infrastructure
- Game engine documentation and analysis

## Key Technologies

- **Game Engine:** FFNX (FF7 New Threat eXtended)
- **Language Processing:** MangaOCR, OpenCV, Python image processing
- **Data Formats:** JSON, CSV, TOML, Markdown
- **Scripting:** Python 3, Bash/Shell
- **Character Encoding:** Shift_JIS, Unicode CJK
- **Asset Management:** Font atlases, texture mapping, TIM format (PlayStation)

## Directory Structure

```
./
├── .claude/                                    # Claude workspace configuration
│   ├── data/                                   # Session data and configuration
│   └── settings.local.json                     # Local settings
│
├── .project/                                   # Project management and context
│   ├── context_checklists/
│   │   └── CONTEXT_CHECKLIST.md               # Conversation compaction guide
│   ├── research_prompts/
│   │   ├── FFNX_CODE_ANALYSIS_PROMPT.md       # FFNX codebase analysis template
│   │   └── FFNX_INVESTIGATION_PROMPT.md       # Investigation framework
│   └── session_handoffs/
│       ├── HANDOVER_PROMPT.md                 # Session transfer protocol
│       ├── SESSION_HANDOFF_10.md              # Session 10 context
│       └── SESSION_HANDOFF_12.md              # Session 12 context
│
├── archive/                                    # Historical research and experiments
│   ├── character_tables_debug/                # Character table debugging outputs
│   │   ├── debug/                             # Debug images and grids
│   │   └── debug_cells/                       # Individual cell comparisons
│   ├── character_tables_pre-interactive/      # Pre-visualization character maps
│   │   ├── character_map_*.csv                # Various mapping formats
│   │   └── character_map_*.json               # JSON character mappings
│   ├── character_tables_verification/         # Verification outputs
│   │   ├── verification/                      # Font comparison images
│   │   └── verification_topleft/              # Top-left corner verification
│   ├── findings_legacy/                       # Legacy finding documents
│   │   ├── FINDINGS.md
│   │   ├── FINDINGS.md.backup
│   │   └── findings2.md
│   ├── scripts/                               # Legacy and utility scripts
│   │   ├── character mapping and OCR utilities
│   │   ├── visualization tools
│   │   ├── grid offset finding tools
│   │   └── font verification scripts
│   ├── sharded/                               # Archived comprehensive documentation
│   │   ├── bible/                             # Main research documents
│   │   ├── bible_sections/                    # Sectioned implementation guide
│   │   │   ├── 1-executive-mission-briefing.md
│   │   │   ├── 2-architectural-overview-strategic-analysis.md
│   │   │   ├── 3-critical-terminology-concepts.md
│   │   │   ├── 4-asset-specifications-data-structures.md
│   │   │   ├── 5-ffnx-codebase-architecture.md
│   │   │   ├── 6-deep-dive-technical-constraints-solutions.md
│   │   │   ├── 7-implementation-specification-c-modifications.md
│   │   │   ├── 8-implementation-specification-assembly-hooks.md
│   │   │   ├── 9-implementation-specification-renderer-integration.md
│   │   │   ├── 10-advanced-feature-furigana-support.md
│   │   │   ├── 11-testing-verification-protocol.md
│   │   │   ├── 12-risk-mitigation-debugging-guide.md
│   │   │   ├── 13-deployment-checklist.md
│   │   │   ├── 14-reference-materials-appendices.md
│   │   │   ├── final-implementation-checklist.md
│   │   │   └── conclusion.md
│   │   ├── findings/                          # Archived findings
│   │   ├── findings_sections/                 # Sectioned research findings
│   │   │   ├── 00_INDEX.md
│   │   │   ├── 01_executive_summary.md
│   │   │   ├── 02_table_of_contents.md
│   │   │   ├── Session 2-9 discovery documents
│   │   │   ├── Deep dive sections (character encoding, font atlas, etc.)
│   │   │   ├── 26_cumulative_research_statistics.md
│   │   │   ├── 27_breakthrough_first_ever_ff7_japanese_character_table_created.md
│   │   │   ├── 28_cumulative_research_statistics_updated.md
│   │   │   └── 29_session_9_update_accurate_character_table_2025_11_17_1930_jst.md
│   │   ├── README.md
│   │   └── shard_findings.py                  # Script to reorganize findings
│   ├── ARCHITECTURAL_RETROSPECTIVE.md          # Architecture analysis
│   ├── SCRAPED_URLS.md                        # Tracked URLs from research
│   ├── TOOL_VERIFICATION_LOG.md               # Tool testing log
│   └── UNSCRAPPED_URLS.md                     # URLs to be processed
│
├── assets/                                     # Project assets
│   └── character_mappings/
│       └── interactive_viewer/                # Character mapping visualization
│           ├── all_textures_corrections.json  # All font corrections
│           ├── ff7_complete_character_mapping.json
│           ├── ff7_complete_mapping_compact.csv
│           ├── jafont_*.json                  # Font-specific corrections
│           ├── jafont_*.html                  # Interactive viewers
│           ├── 1_final.json, 6_final.json     # Final mappings
│
├── docs/                                       # Primary documentation
│   ├── character_maps/                        # Character mapping reference
│   │   ├── ff7_complete_mapping_compact.csv   # Complete character mapping
│   │   └── JAFONT_CHARACTER_MAP.md            # Character map documentation
│   ├── recent/                                # Recent session outputs
│   ├── reference/                             # Reference documentation
│   │   ├── game_engine/                       # FF7 game engine documentation
│   │   │   ├── .claude/                       # Claude session data
│   │   │   ├── comparisons/                   # Component comparisons
│   │   │   ├── extracted_major_sections/      # Engine sections
│   │   │   │   ├── 00_HEADER_TOC.md
│   │   │   │   ├── 01_HISTORY.md
│   │   │   │   ├── 02_ENGINE_BASICS.md
│   │   │   │   ├── 03_KERNEL.md               # Kernel module docs
│   │   │   │   ├── 04_MENU_MODULE.md
│   │   │   │   ├── 05_FIELD_MODULE.md
│   │   │   │   ├── 06_BATTLE_MODULE.md
│   │   │   │   ├── 07_WORLD_MAP.md
│   │   │   │   ├── 08_MINI_GAMES.md
│   │   │   │   ├── 09_APPENDIX.md
│   │   │   │   ├── 10_SOURCE_CODE_FORENSICS.md
│   │   │   │   ├── 11_BUGS_AND_CREDITS.md
│   │   │   │   ├── MAPPING.md
│   │   │   │   └── README.md
│   │   │   ├── ff7-wiki/                      # Downloaded wiki content
│   │   │   ├── images/                        # Engine reference images
│   │   │   │   ├── Engine components
│   │   │   │   ├── Menu screenshots
│   │   │   │   ├── PSX format diagrams
│   │   │   │   └── VRAM structure images
│   │   │   ├── markdown/                      # Extracted documentation
│   │   │   │   ├── combined/                  # Combined module documents
│   │   │   │   ├── merged_with_pdf_content/   # PDF-merged versions
│   │   │   │   └── Individual engine topic files
│   │   │   ├── markdown_backup/               # Backup of extracted markdown
│   │   │   ├── raw/                           # Raw mediawiki format
│   │   │   ├── Extraction scripts (*.py, *.sh)
│   │   │   ├── ENHANCEMENT_PLAN.md
│   │   │   ├── FINAL_CONVERSION_PIPELINE.md
│   │   │   ├── GameEngine.md
│   │   │   ├── IMPROVEMENTS_SUMMARY.md
│   │   │   ├── Savemap.md
│   │   │   └── SCRAPING_SUMMARY.md
│   │   ├── AF3DN_ANALYSIS.md                  # AF3DN tool analysis
│   │   ├── ARCHITECTURE_CLARIFICATION.md
│   │   ├── BEGINNER_GUIDE.md
│   │   ├── MULTI_LANGUAGE_FINDINGS.md
│   │   ├── TOOL_GUIDE.md
│   │   ├── VERIFICATION_FINDINGS_SESSION_11.md
│   │   ├── PR737_ANALYSIS.md
│   │   ├── PR737_COMPLETE_ANALYSIS.md
│   ├── roadmap/                               # Implementation roadmap
│   │   ├── FEATURE_ROADMAP.md
│   │   └── FFNX_CROWDSOURCED_TRANSLATION_SPEC.md
│   ├── 7TH_HEAVEN_DEVELOPER_GUIDE.md
│   ├── BUILD_ENVIRONMENT_SETUP.md
│   ├── DOCUMENTATION_UPDATE_PLAN.md
│   ├── FFNX_DEVELOPER_GUIDE.md
│   ├── FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md
│   ├── IMPLEMENTATION_READINESS_ASSESSMENT.md
│   ├── IMPLEMENTATION_VERIFICATION_CHECKLIST.md
│   ├── masterfindings.md
│   ├── PROJECT_OVERVIEW.md
│   ├── README.md
│   └── TEST_PROCEDURE.md
│
├── FF7-Japanese-Mod/                          # Complete mod package (ready for 7th Heaven)
│   ├── .claude/                               # Claude session data
│   ├── mod.xml                                # Mod configuration
│   ├── Readme.txt                             # Mod readme
│   ├── mods/                                  # Mod assets
│   │   └── Textures/menu/                     # Japanese font textures
│   │       ├── jafont_1.png through jafont_6.png
│   └── lang-ja/                               # Japanese language files
│       ├── kernel/                            # Japanese KERNEL.BIN
│       └── field/                             # Japanese field data (jfleve.lgp)
│
├── FFNx/                                       # FFNX source code (CURRENT MAIN BRANCH)
│   ├── .claude/                               # Claude session data
│   ├── src/                                   # Source code
│   │   ├── ff7/                               # FF7-specific implementation
│   │   │   ├── japanese_text.cpp              # Japanese text rendering
│   │   │   ├── font_*.cpp                     # Font handling
│   │   │   └── ...
│   │   ├── ff7_data/                          # FF7 data structures
│   │   ├── common/                            # Common utilities
│   │   └── ...
│   ├── CMakeLists.txt                         # Build configuration
│   ├── CMakePresets.json                      # CMake presets
│   ├── Changelog.md                           # FFNx changelog
│   ├── COPYING.txt                            # License
│   ├── .github/                               # GitHub workflows
│   └── docs/                                  # FFNx documentation
│
├── PR737/                                      # FFNx PR #737 (Japanese text support)
│   ├── .claude/                               # Claude session data
│   ├── src/                                   # Source code (identical structure to FFNx)
│   │   ├── ff7/                               # FF7-specific implementation
│   │   │   ├── japanese_text.cpp              # Japanese text rendering
│   │   │   └── ...
│   │   └── ...
│   ├── CMakeLists.txt                         # Build configuration
│   ├── CMakePresets.json                      # CMake presets
│   ├── Changelog.md                           # PR #737 specific changes
│   ├── COPYING.txt                            # License
│   ├── .github/                               # GitHub workflows
│   └── docs/                                  # Documentation
│
├── japanese-assets-extracted/                 # Extracted Japanese assets
│   ├── mod-structure/                         # Mod directory structure
│   ├── FFNx-japanese.toml                     # FFNX configuration template
│   ├── README.md
│   ├── TRANSFER_CHECKLIST.md
│   └── WINDOWS_INSTALLATION_GUIDE.md
│
├── reference/                                  # External reference materials
│   ├── ff7_disassembly/                       # FF7 disassembly reference
│   │   ├── ff7_ja.txt                         # Japanese version disassembly
│   │   └── ff7.txt                            # English version disassembly
│   └── repomix_snapshots/                     # Repository snapshots
│       ├── repomix-output-julianxhokaxhiu-FFNx_NO-LINES.git.md
│       ├── repomix-output-julianxhokaxhiu-FFNx_NO-LINES.git.xml
│       └── repomix-output.xml
│
├── logs/                                       # Project logs and output files
│
├── .gitignore                                  # Git ignore configuration
├── DOCUMENTATION_MAP.md                        # Documentation index
├── README.md                                   # Project readme
└── SIMPLE_INSTRUCTIONS.md                      # Quick start guide (Windows setup)
```

## Key Findings & Milestones

### Character Table Breakthrough (Session 9)
- First-ever accurate FF7 Japanese character table created
- Successfully mapped all 6 Japanese font atlases (JAFONT_1 through JAFONT_6)
- Validated using MangaOCR with 95%+ confidence
- Complete mapping: ~2000+ unique Japanese characters extracted

### Technical Achievements
- Discovered JAFONT grid structure and offset calculations
- Reverse-engineered PlayStation TIM format integration
- Identified character encoding mappings (Shift_JIS ↔ texture coordinates)
- Built interactive visualization tools for character mapping verification
- Developed accurate character map in multiple formats (JSON, CSV, HTML)

### Research Coverage
- FFNX architecture and C++ modification points
- FF7 game engine documentation (Field, Battle, Menu, World Map modules)
- PlayStation PSX color format and texture specifications
- Assembly hook integration points for text rendering
- Multi-language support infrastructure planning

## Critical Files for Implementation

### Character Mappings
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/assets/character_mappings/interactive_viewer/ff7_complete_character_mapping.json` - Master character mapping
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/character_maps/JAFONT_CHARACTER_MAP.md` - Documentation

### Implementation Guides
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` - Comprehensive implementation guide
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/archive/sharded/bible_sections/` - Detailed technical specifications

### Configuration
- `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/japanese-assets-extracted/FFNx-japanese.toml` - FFNX configuration template

## Development Notes

### Current Phase
**Implementation Ready Phase** - All assets and code prepared for Windows build/deployment:
- Character mappings: COMPLETE (JSON, CSV, HTML formats)
- Font textures: COMPLETE (6 JAFONT PNG files)
- Mod package structure: COMPLETE (FF7-Japanese-Mod/ directory)
- Japanese dialogue files: COMPLETE (KERNEL.BIN, jfleve.lgp)
- FFNx implementation: COMPLETE (PR #737, japanese_text.cpp with character width mappings)
- 7th Heaven mod package: READY TO BUILD (FF7-Japanese-Mod/ folder)

### Deployment Workflow (macOS to Windows)
1. **Transfer phase** (on this macOS machine):
   - `FF7-Japanese-Mod/` directory (126MB) - ready to transfer
   - `PR737/` directory - FFNx source code ready to build

2. **Build phase** (on Windows machine):
   - Build FFNx.dll from PR737 using Visual Studio 2022 + CMake
   - Build .iro mod file using 7-Zip: `7z a -tzip FF7-Japanese-v1.00.iro *`

3. **Install phase** (on Windows machine):
   - Copy FFNx.dll to FF7 installation directory
   - Import FF7-Japanese-v1.00.iro into 7th Heaven
   - Add `ff7_japanese_edition = true` to FFNx.toml
   - Launch game through 7th Heaven

### Known Constraints
- JAFONT 6 has partial mapping (high-index characters may be special-purpose)
- Multi-byte character handling requires careful offset calculation
- Text rendering requires texture coordinate mapping
- Windows build environment required for compilation (Visual Studio 2022, CMake, vcpkg)
- FFNx.dll must be compiled from PR737 source (cannot use generic FFNx.dll)

### Critical Files for Implementation
- **Source code**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/PR737/src/ff7/japanese_text.cpp` (contains character width mappings and rendering logic)
- **Mod package**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/FF7-Japanese-Mod/` (ready to build as .iro)
- **Asset location reference**: `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/SIMPLE_INSTRUCTIONS.md` (Windows deployment guide)

## Important Notes for Future Development

### For macOS Development (This Machine)
- All research documents are in `/Volumes/DevSSD/01_Development/Projects/experiments/ff70G-japanese-mod/archive/sharded/`
- Session handoff protocols in `.project/session_handoffs/`
- Use CONTEXT_CHECKLIST.md in `.project/` for conversation compaction
- Asset verification completed with multi-format export (JSON, CSV, HTML)
- Game engine documentation provides reference for integration points

### For Windows Deployment
**CRITICAL: DO NOT MODIFY PR737 OR FFNX WITHOUT UNDERSTANDING:**
- PR737 is a frozen snapshot of FFNx with Japanese text support patches
- FFNx is the current main branch (may have different Japanese implementation)
- The character width arrays in `japanese_text.cpp` line 311+ are the decoder mappings
- These mappings already support reading existing Japanese dialogue files (no new encoder needed yet)
- 7th Heaven loads only .iro files, not loose directories

### Quick Windows Deployment Checklist
```
PR737/ → Build FFNx.dll
FF7-Japanese-Mod/ → Create FF7-Japanese-v1.00.iro with 7z
FFNx.dll → Copy to FF7 installation directory
FF7-Japanese-v1.00.iro → Import into 7th Heaven
FFNx.toml → Add ff7_japanese_edition = true
Game Launch → Test Japanese text rendering
```

### Known Working Assets
- Font textures: `assets/character_mappings/interactive_viewer/jafont_*.json` (metadata)
- Font PNG files: Already in `FF7-Japanese-Mod/mods/Textures/menu/`
- Japanese dialogue: Already in `FF7-Japanese-Mod/lang-ja/`
- Character mappings: `docs/character_maps/JAFONT_CHARACTER_MAP.md`

## Session Tracking
Maintain session handoffs in `.project/session_handoffs/` directory for continuity between development sessions.

## Project Status Summary

**Last Updated:** 2025-11-28
**Overall Status:** Implementation phase ready (awaiting Windows build/deployment)
**Blocking Issues:** None - all prerequisites met
**Next Major Milestone:** Windows build and 7th Heaven installation test

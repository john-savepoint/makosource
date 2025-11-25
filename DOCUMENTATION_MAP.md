# FF7 Japanese Implementation - Documentation Map

**For**: Finding the right document for your needs
**Updated**: 2025-11-24 22:00 JST
**Status**: Current with reorganized structure

---

## Quick Navigation

### "I'm completely lost. What's this project about?"
→ Read: **docs/reference/BEGINNER_GUIDE.md** (10 min)
- Simple explanations without jargon
- File types explained (LGP, TEX, BIN)
- Why Japanese is different from English
- Visual comparisons

### "I'm a senior engineer. Brief me on the entire project."
→ Read: **docs/PROJECT_OVERVIEW.md** (30 min)
- Executive summary
- Complete architecture diagrams (with Mermaid)
- All three implementation paths
- Technology decisions explained
- Timeline and risk assessment

### "What's the current implementation status?"
→ Read: **docs/IMPLEMENTATION_READINESS_ASSESSMENT.md** (20 min) ⭐ **NEW**
- Phase 0 requirements and gap analysis
- What we have vs what we need
- Build environment setup needs
- Tool chain validation checklist
- Confidence levels and blocking items

### "I need a verification checklist for implementation."
→ Read: **docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md** (reference) ⭐ **NEW**
- 15 sections of verification questions
- Distinguishes speculation from verified facts
- Priority-ordered by implementation phase (0-4)
- Covers everything from build environment to edge cases

### "I want to start testing FFNx texture override."
→ Read: **docs/TEST_PROCEDURE.md** (reference)
- Step-by-step testing procedure
- Phase 1-6 with exact commands
- Troubleshooting guide
- What success looks like

### "I need to extract and convert font files."
→ Read: **docs/reference/TOOL_GUIDE.md** (reference)
- Complete tool chain documentation
- ulgp (LGP extraction/repacking)
- Image2TEX or Tex Tools (format conversion)
- FFNx configuration
- Complete workflows

### "What's the complete technical specification?"
→ Read: **docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md** (deep dive) ⭐ **CORE**
- 155K tokens, 4000 lines
- 14 sections covering architecture, implementation, testing, deployment
- Complete C++ modifications
- Assembly hooks specification
- Renderer integration details
- **Sharded version**: `docs/sharded/bible_sections/` (18 files, LLM-friendly)

### "How does FFNx multi-language support actually work?"
→ Read: **docs/to_combine/ARCHITECTURE_CLARIFICATION.md** (technical)
- Common misconceptions vs reality
- What we're actually building
- How other languages (French, German, Spanish) work
- Data flow diagrams
- Critical insights

### "What about multi-language expansion beyond Japanese?"
→ Read: **docs/to_combine/MULTI_LANGUAGE_FINDINGS.md** (strategic)
- Language switching architecture
- Multi-language expansion strategy (Chinese, Korean, etc.)
- 7th Heaven integration
- Registry virtualization

### "What was researched? Where did findings come from?"
→ Read: **docs/masterfindings.md** (deep dive)
- Historical research (9 sessions)
- 40+ critical discoveries
- Session-by-session breakdown
- **Sharded version**: `docs/sharded/findings_sections/` (29 files, archived)

### "What's the character mapping for Japanese?"
→ Read: **docs/character_maps/JAFONT_CHARACTER_MAP.md** (reference)
- All 1,331 characters documented
- Mapping from FF7 index to Unicode
- Character distribution by texture
- Grid positions
- **Data file**: `docs/character_maps/ff7_complete_mapping_compact.csv`

### "How did we reverse-engineer AF3DN.P?"
→ Read: **docs/reference/AF3DN_ANALYSIS.md** (technical)
- Binary analysis results
- Export functions identified
- String extraction (jafont references)
- Import dependencies
- Build path discovered

### "What are future features beyond core Japanese support?"
→ Read: **docs/roadmap/FEATURE_ROADMAP.md** (vision)
- Phase 1: Japanese text rendering (CURRENT)
- Phase 2: Multi-language toggle (EN↔JA↔FR↔DE↔ES)
- Phase 3: Furigana (reading guides)
- Phase 4: Cheat/booster integration (already available)
- Phase 5: Polish & distribution
- **Phase 6: Crowdsourced translation system** ⭐ **NEW**

### "What's the crowdsourced translation system?"
→ Read: **docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md** (detailed spec) ⭐ **NEW**
- In-game submission system (Ctrl+T hotkey)
- Web-based voting and moderation
- Complete API specification
- Security and anti-abuse measures
- Infrastructure requirements
- 1,728 lines of detailed design

---

## Document Descriptions

### Core Planning Documents

| Document | Purpose | Audience | Depth | Read Time |
|----------|---------|----------|-------|-----------|
| **README.md** (root) | Project structure guide | Everyone | Surface | 15 min |
| **docs/reference/BEGINNER_GUIDE.md** | Learn the concepts | Confused people, non-technical | Surface | 10 min |
| **docs/PROJECT_OVERVIEW.md** | Complete project brief | Senior engineers, architects | Medium | 30 min |
| **docs/roadmap/FEATURE_ROADMAP.md** | Future vision (Phases 1-6) | Product managers, long-term planning | Medium | 20 min |

### Implementation Documents ⭐ **CRITICAL FOR PHASE 0**

| Document | Purpose | Audience | Depth | Use |
|----------|---------|----------|-------|-----|
| **docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md** | Complete technical spec | Implementers | Deep | Reference |
| **docs/IMPLEMENTATION_READINESS_ASSESSMENT.md** | Phase 0 requirements | Implementers | Medium | Pre-implementation |
| **docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md** | Verification questions | Implementers, QA | Deep | During implementation |
| **docs/to_combine/ARCHITECTURE_CLARIFICATION.md** | How it actually works | Architects | Medium | Design review |
| **docs/to_combine/MULTI_LANGUAGE_FINDINGS.md** | Multi-language strategy | Architects | Medium | Phase 2+ planning |

### Technical Reference Documents

| Document | Purpose | Audience | Depth | Use |
|----------|---------|----------|-------|-----|
| **docs/reference/AF3DN_ANALYSIS.md** | Reverse engineering results | Driver developers | Deep | Reference |
| **docs/character_maps/JAFONT_CHARACTER_MAP.md** | Character encoding reference | Text system developers | Deep | Reference |
| **docs/reference/TOOL_GUIDE.md** | Complete tool chain | Implementers | Medium | How-to |
| **docs/TEST_PROCEDURE.md** | Testing procedure | QA engineers | Medium | Step-by-step |
| **docs/reference/game_engine/** | FF7 engine manual | Game developers | Deep | Reference |

### Future Feature Specifications

| Document | Purpose | Audience | Status |
|----------|---------|----------|--------|
| **docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md** | Community translation system | Full-stack developers | Design complete |

### Research & Findings Documents

| Document | Purpose | Audience | Depth | Use |
|----------|---------|----------|-------|-----|
| **docs/masterfindings.md** | Complete research log | Researchers, decision makers | Deep | Complete history |
| **archive/SCRAPED_URLS.md** | All researched sources | Citation tracking | Medium | Reference |
| **assets/character_mappings/** | Actual character data | Developers | Raw data | Lookup |

---

## Reading Paths by Role

### For Product Manager
1. Start: **README.md** (project structure)
2. Then: **docs/reference/BEGINNER_GUIDE.md** (understand the problem)
3. Then: **docs/PROJECT_OVERVIEW.md** (understand the solution)
4. Reference: **docs/roadmap/FEATURE_ROADMAP.md** (all phases)
5. Reference: **docs/PROJECT_OVERVIEW.md** Part 8 (timeline, risks)

### For Implementation Lead (Starting Phase 0)
1. Start: **README.md** (project structure)
2. Then: **docs/IMPLEMENTATION_READINESS_ASSESSMENT.md** (what we need)
3. Then: **docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md** (complete spec)
4. Reference: **docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md** (validate assumptions)
5. Reference: **docs/reference/TOOL_GUIDE.md** (tools available)

### For Graphics/Driver Developer
1. Start: **docs/PROJECT_OVERVIEW.md** Part 1-3 (architecture)
2. Deep: **docs/reference/AF3DN_ANALYSIS.md** (what we're replicating)
3. Deep: **docs/to_combine/ARCHITECTURE_CLARIFICATION.md** (how it works)
4. Reference: **docs/character_maps/JAFONT_CHARACTER_MAP.md** (character data)
5. Reference: **docs/reference/TOOL_GUIDE.md** (tools available)

### For Text/Encoding System Developer
1. Start: **docs/reference/BEGINNER_GUIDE.md** (understand encoding)
2. Deep: **docs/PROJECT_OVERVIEW.md** Part 1 & 1.5 (encoding system)
3. Reference: **docs/character_maps/JAFONT_CHARACTER_MAP.md** (character mapping)
4. Reference: **docs/masterfindings.md** (research context)

### For QA Engineer
1. Start: **docs/reference/BEGINNER_GUIDE.md** (understand what's being built)
2. How-to: **docs/TEST_PROCEDURE.md** (testing steps)
3. Reference: **docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md** (what to verify)
4. Reference: **docs/reference/TOOL_GUIDE.md** (tools and workflows)

### For Community Modder
1. Start: **docs/reference/BEGINNER_GUIDE.md** (understand what's happening)
2. How-to: **docs/reference/TOOL_GUIDE.md** (how to use tools)
3. Reference: **docs/TEST_PROCEDURE.md** (testing)
4. Future: **docs/roadmap/FEATURE_ROADMAP.md** (what's coming)

### For Full-Stack Developer (Crowdsourced System)
1. Start: **docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md** (complete spec)
2. Context: **docs/roadmap/FEATURE_ROADMAP.md** Phase 6 (summary)
3. Reference: **docs/to_combine/MULTI_LANGUAGE_FINDINGS.md** (language architecture)

### For Researcher/Historian
1. Complete: **docs/masterfindings.md** (all research 9 sessions)
2. Sources: **archive/SCRAPED_URLS.md** (all URLs)
3. Analysis: **docs/reference/AF3DN_ANALYSIS.md** (reverse engineering)
4. Context: **docs/PROJECT_OVERVIEW.md** (how we got here)

---

## Document Relationships

```
README.md (Project Root - START HERE)
    ↓
    ├─→ docs/reference/BEGINNER_GUIDE.md (Foundation)
    │       ↓
    │       ├─→ docs/PROJECT_OVERVIEW.md (Complete architecture)
    │       │       ├─→ docs/reference/AF3DN_ANALYSIS.md (Deeper technical)
    │       │       ├─→ docs/character_maps/JAFONT_CHARACTER_MAP.md (Character encoding)
    │       │       ├─→ docs/to_combine/ARCHITECTURE_CLARIFICATION.md (How it works)
    │       │       └─→ docs/roadmap/FEATURE_ROADMAP.md (Future features)
    │       │
    │       ├─→ docs/reference/TOOL_GUIDE.md (How to use the tools)
    │       │       ├─→ docs/TEST_PROCEDURE.md (Testing workflow)
    │       │       └─→ assets/character_mappings/ (Character data)
    │       │
    │       └─→ docs/masterfindings.md (Complete research history)
    │               └─→ archive/SCRAPED_URLS.md (Source citations)
    │
    ├─→ IMPLEMENTATION PATH (Phase 0 → Phase 5)
    │       ├─→ docs/IMPLEMENTATION_READINESS_ASSESSMENT.md (Phase 0 requirements)
    │       ├─→ docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md (Complete spec)
    │       └─→ docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md (Validation)
    │
    └─→ FUTURE FEATURES (Phase 6+)
            ├─→ docs/roadmap/FEATURE_ROADMAP.md (All phases)
            ├─→ docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md (Phase 6 detail)
            └─→ docs/to_combine/MULTI_LANGUAGE_FINDINGS.md (Multi-language expansion)
```

---

## Document Status

| Document | Location | Status | Last Updated | Completeness |
|----------|----------|--------|--------------|--------------|
| README.md | Root | ✅ Current | 2025-11-24 | 100% |
| docs/reference/BEGINNER_GUIDE.md | docs/reference/ | ✅ Complete | 2025-11-18 | 100% |
| docs/PROJECT_OVERVIEW.md | docs/ | ✅ Complete | 2025-11-18 | 100% |
| docs/FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md | docs/ | ✅ Complete | 2025-11-24 | 100% |
| docs/IMPLEMENTATION_READINESS_ASSESSMENT.md | docs/ | ✅ Complete | 2025-11-24 | 100% |
| docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md | docs/ | ✅ Complete | 2025-11-24 | 100% |
| docs/to_combine/ARCHITECTURE_CLARIFICATION.md | docs/to_combine/ | ✅ Complete | 2025-11-24 | 100% |
| docs/to_combine/MULTI_LANGUAGE_FINDINGS.md | docs/to_combine/ | ✅ Complete | 2025-11-24 | 100% |
| docs/reference/AF3DN_ANALYSIS.md | docs/reference/ | ✅ Complete | 2025-11-17 | 100% |
| docs/character_maps/JAFONT_CHARACTER_MAP.md | docs/character_maps/ | ✅ Complete | 2025-11-17 | 100% |
| docs/reference/TOOL_GUIDE.md | docs/reference/ | ✅ Complete | 2025-11-17 | 100% |
| docs/TEST_PROCEDURE.md | docs/ | ✅ Complete | 2025-11-17 | 100% |
| docs/roadmap/FEATURE_ROADMAP.md | docs/roadmap/ | ✅ Complete | 2025-11-24 | 100% |
| docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md | docs/roadmap/ | ✅ Complete | 2025-11-24 | 100% |
| docs/masterfindings.md | docs/ | ✅ Complete | 2025-11-17 | 100% |
| archive/SCRAPED_URLS.md | archive/ | ✅ Complete | 2025-11-15 | 100% |
| assets/character_mappings/ | assets/ | ✅ Complete | 2025-11-17 | 100% |
| DOCUMENTATION_MAP.md | Root | ✅ Current | 2025-11-24 | 100% (this file) |

---

## Directory Structure Quick Reference

```
ff70G-japanese-mod/
├── README.md                                    # ⭐ START HERE
├── DOCUMENTATION_MAP.md                         # This file
│
├── docs/                                        # All documentation
│   ├── FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md  # Complete spec
│   ├── IMPLEMENTATION_READINESS_ASSESSMENT.md        # Phase 0 requirements
│   ├── IMPLEMENTATION_VERIFICATION_CHECKLIST.md      # Validation checklist
│   ├── PROJECT_OVERVIEW.md                          # Architecture overview
│   ├── TEST_PROCEDURE.md                            # Testing guide
│   ├── masterfindings.md                            # Research history
│   ├── character_maps/                              # Character mappings
│   │   ├── JAFONT_CHARACTER_MAP.md
│   │   └── ff7_complete_mapping_compact.csv
│   ├── reference/                                   # Reference docs
│   │   ├── AF3DN_ANALYSIS.md
│   │   ├── BEGINNER_GUIDE.md
│   │   ├── TOOL_GUIDE.md
│   │   └── game_engine/                            # Game engine manual
│   ├── roadmap/                                     # Future features
│   │   ├── FEATURE_ROADMAP.md
│   │   └── FFNX_CROWDSOURCED_TRANSLATION_SPEC.md
│   ├── to_combine/                                  # To be integrated
│   │   ├── ARCHITECTURE_CLARIFICATION.md
│   │   └── MULTI_LANGUAGE_FINDINGS.md
│   └── sharded/                                     # Sharded large docs
│       ├── bible_sections/                          # Bible (18 files)
│       └── findings_sections/                       # Findings (29 files)
│
├── assets/                                      # Game assets
│   ├── fonts/                                   # Font textures
│   │   ├── png/                                # ⭐ jafont_*.png (6 files)
│   │   └── tex/                                # jafont_*.tex (6 files)
│   └── character_mappings/                      # Character data
│       └── interactive_viewer/                  # Web tool for mapping
│
├── reference/                                   # Read-only reference
│   ├── ff7_disassembly/                        # Executable disassembly
│   └── repomix_snapshots/                      # FFNx codebase snapshots
│
└── archive/                                     # Historical/unused
    ├── scripts/                                # Research scripts
    ├── character_tables_debug/                 # Debug artifacts
    ├── character_tables_verification/          # Verification images
    ├── findings_legacy/                        # Old findings
    ├── SCRAPED_URLS.md                         # URL citations
    └── UNSCRAPPED_URLS.md                      # URLs to scrape
```

---

## Key Facts (For Quick Reference)

**The Problem**:
- FF7 English PC cannot display Japanese characters
- Font system is fundamentally incompatible (1 texture for 256 chars vs 2,300+ needed)
- Needs 6 font textures + FA-FE character page system

**The Solution**:
- Extending FFNx driver (Path C - Hybrid Extension)
- Replicating AF3DN.P's proven architecture
- Adding support for 6 font textures + FA-FE encoding
- Multi-language expansion (Japanese, French, German, Spanish, Chinese, etc.)

**The Status**:
- ✅ Research complete (9 sessions, 40+ findings)
- ✅ Character mapping complete (1,331 characters, 100% accuracy)
- ✅ Assets prepared (6 font textures in PNG + TEX formats)
- ✅ Tools validated (ulgp, Tex Tools, FFNx)
- ✅ Architecture designed (Master Bible complete)
- ✅ Phase 0 requirements documented
- ⏳ **Ready for Phase 0 execution** (build environment setup)

**The Timeline**:
- **Phase 0**: Research & Setup (3-6 days) - BUILD ENVIRONMENT REQUIRED
- **Phase 1-3**: Core Implementation (8-12 weeks)
- **Phase 4**: Advanced Features - Furigana, Language Switching (4-6 weeks)
- **Phase 5**: Polish & Distribution (2-4 weeks)
- **Phase 6**: Crowdsourced Translation System (8-10 weeks, optional)
- **Total Core**: 10-18 weeks | **With Phase 6**: 18-28 weeks

**Why This Works**:
- Square Enix already proved this approach (2013 Japanese eStore version)
- AF3DN.P is a working reference implementation
- We're reimplementing proven architecture, not inventing
- Community-driven (FFNx) vs proprietary (AF3DN.P)
- Fully legal and ethical

**What We Need (Phase 0 - IMMEDIATE)**:
- Build FFNx from source on Windows
- Reverse-engineer AF3DN.P for memory addresses
- Create test environment setup guide
- Validate tool chain on Windows

---

## How to Update This Map

When new documents are created:
1. Add entry to appropriate section (Core Planning, Implementation, Technical Reference, etc.)
2. Add entry to relevant "Reading Path by Role" section
3. Update "Document Relationships" diagram
4. Update "Document Status" table
5. Update "Directory Structure Quick Reference" if needed
6. Commit with message: `docs: update DOCUMENTATION_MAP with [description]`

---

**Questions?** Check the relevant document above, or start with README.md for project structure!

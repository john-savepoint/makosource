# Documentation Directory Guide

**Purpose:** Navigate the complete FFNx Japanese Implementation documentation
**Updated:** 2025-12-02 15:50:00 JST (Tuesday)
**For:** Humans and LLMs working on this project

---

## 🎯 Start Here

**If you're new to the project:**
1. **Read:** `../README.md` (project root) - Get oriented
2. **Read:** `../DOCUMENTATION_MAP.md` - Complete navigation guide
3. **Read:** `reference/BEGINNER_GUIDE.md` - Understand the basics
4. **Then:** Continue below based on your role

---

## ⚡ Recent Work (December 2025) - READ THIS FIRST

**Status**: Implementation 85.7% complete (24/28 systems verified working)

### What's Been Done

**English Version Breakthrough** (Session b8a3e4e3 + c2b17842):
- ✅ English `ff7_en.exe` + Japanese text = **WORKS** with PR #737
- ✅ Field dialogue renders perfectly
- ✅ Battle text works
- ⚠️ Menu labels broken (fix identified: extract Japanese kernel2.bin)

**Documentation Restructured** (2025-12-02):
- Created `IMPLEMENTATION_STATUS.md` (200 lines, replaces 2,022-line checklist)
- Archived old verification checklist (historical value preserved)
- Focused on actionable status vs hypothetical questions

### 📖 Quick Guide: Which Document to Read

**For current implementation status:**
→ **`IMPLEMENTATION_STATUS.md`** (200 lines, ⭐ START HERE)
  - What's working (8 systems)
  - Known issues (3 bugs with fixes)
  - Next steps (kernel2.bin extraction)
  - Critical discovery: Two text pipelines

**For bug analysis and fixes:**
→ **`PR737_ANALYSIS.md`** (existing document)
  - 3 bug root causes
  - Hook points with memory addresses
  - Fix strategies

**For English version compatibility:**
→ **`ENGLISH_VERSION_FINDINGS.md`** (if exists) or see IMPLEMENTATION_STATUS.md Section "English Version Compatibility"
  - Two text pipeline architecture
  - File redirect implementation
  - Why field text works but menus don't

**For complete technical specification:**
→ **`FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md`** (155k tokens, comprehensive)
  - Use this for deep implementation details
  - Use sharded version if too large: `sharded/bible_sections/`

**For historical research (archived):**
→ **`archive/verification_checklists/IMPLEMENTATION_VERIFICATION_CHECKLIST_v2.4.0.md`**
  - 21 sections of verification questions
  - Historical value only (superseded by IMPLEMENTATION_STATUS.md)

### 🎯 For LLMs: Context Window Guidelines

**Always include** (~2.5k tokens):
- `IMPLEMENTATION_STATUS.md` - Current status, clear next steps

**Include if working on bugs** (~15k tokens):
- `PR737_ANALYSIS.md` - Bug fixes with hook points

**Include if unsure** (~5k tokens):
- `reference/BEGINNER_GUIDE.md` - Encoding basics

**Don't include** (27k tokens, archived):
- ~~IMPLEMENTATION_VERIFICATION_CHECKLIST.md~~ - Archived, use IMPLEMENTATION_STATUS.md instead

### Next Steps (From IMPLEMENTATION_STATUS.md)

1. **Immediate**: Extract Japanese kernel2.bin → fix menu labels
2. **Short-term**: Implement naming screen hooks, fix cursor alignment
3. **Long-term**: Multi-language switching, crowdsourced translation

---

## 📁 Directory Structure

```
docs/
├── README.md (this file)                    # Directory navigation
│
├── FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md  # ⭐ COMPLETE SPEC
├── IMPLEMENTATION_READINESS_ASSESSMENT.md         # Phase 0 requirements
├── IMPLEMENTATION_VERIFICATION_CHECKLIST.md       # Validation questions
├── PROJECT_OVERVIEW.md                            # Architecture overview
├── TEST_PROCEDURE.md                              # Testing guide
├── masterfindings.md                              # Research history
├── REORGANIZATION_PLAN.md                         # Directory cleanup guide
│
├── character_maps/                          # Character encoding data
│   ├── JAFONT_CHARACTER_MAP.md
│   └── ff7_complete_mapping_compact.csv    # ⭐ THE MAPPING FILE
│
├── reference/                               # Reference documentation
│   ├── AF3DN_ANALYSIS.md
│   ├── BEGINNER_GUIDE.md
│   ├── TOOL_GUIDE.md
│   └── game_engine/                        # FF7 engine manual
│       └── ff7 game engine.md
│
├── roadmap/                                 # Feature planning
│   ├── FEATURE_ROADMAP.md                  # Phases 1-6
│   └── FFNX_CROWDSOURCED_TRANSLATION_SPEC.md
│
├── to_combine/                              # To be integrated
│   ├── ARCHITECTURE_CLARIFICATION.md
│   └── MULTI_LANGUAGE_FINDINGS.md
│
└── sharded/                                 # Sharded large docs
    ├── bible_sections/                     # Master Bible (18 files)
    │   ├── index.md
    │   ├── 1-executive-mission-briefing.md
    │   └── ... (16 more)
    └── findings_sections/                  # Findings (29 files)
        ├── 00_INDEX.md
        └── ... (28 more)
```

---

## 📚 Documents by Purpose

### 🔑 Core Implementation Documents (READ FIRST)

| Document | Purpose | Audience | Priority |
|----------|---------|----------|----------|
| **FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md** | Complete technical specification | All implementers | 🔴 CRITICAL |
| **IMPLEMENTATION_READINESS_ASSESSMENT.md** | Phase 0 requirements & gap analysis | Implementation lead | 🔴 CRITICAL |
| **IMPLEMENTATION_VERIFICATION_CHECKLIST.md** | Validation questions (15 sections) | Implementers, QA | 🔴 CRITICAL |

**Start with these three before coding anything.**

---

### 📖 Reference Documents (READ AS NEEDED)

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **reference/BEGINNER_GUIDE.md** | Simple explanations without jargon | First time, confused |
| **reference/TOOL_GUIDE.md** | Complete tool chain guide | Need to use tools |
| **reference/AF3DN_ANALYSIS.md** | Reverse engineering results | Understanding AF3DN.P |
| **reference/game_engine/** | FF7 engine manual (200 pages) | Understanding game internals |
| **TEST_PROCEDURE.md** | Testing procedures | QA, validation |
| **PROJECT_OVERVIEW.md** | Complete architecture | Architecture review |

---

### 🗺️ Roadmap Documents (FUTURE PLANNING)

| Document | Purpose | Phase |
|----------|---------|-------|
| **roadmap/FEATURE_ROADMAP.md** | All phases (1-6) | Overview |
| **roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md** | Community translation system (detailed) | Phase 6 |

---

### 🧭 Architecture Documents (DESIGN UNDERSTANDING)

| Document | Purpose | Use |
|----------|---------|-----|
| **to_combine/ARCHITECTURE_CLARIFICATION.md** | How FFNx multi-language works | Understanding data flow |
| **to_combine/MULTI_LANGUAGE_FINDINGS.md** | Multi-language expansion strategy | Phase 2+ planning |

**Note:** "to_combine" means these will be integrated into Master Bible later.

---

### 🔤 Character Encoding Documents

| Document | Purpose | Use |
|----------|---------|-----|
| **character_maps/JAFONT_CHARACTER_MAP.md** | Complete character reference | Looking up characters |
| **character_maps/ff7_complete_mapping_compact.csv** | Data file (1,331 characters) | Programmatic access |

---

### 📜 Historical Documents

| Document | Purpose | Use |
|----------|---------|-----|
| **masterfindings.md** | Complete research history (9 sessions) | Understanding research process |
| **sharded/findings_sections/** | Sharded findings (29 files) | Detailed session-by-session |

---

## 🎯 Reading Paths by Role

### For Implementation Lead (Starting Phase 0)

**Read in this order:**
1. `IMPLEMENTATION_READINESS_ASSESSMENT.md` (20 min) - What we need NOW
2. `IMPLEMENTATION_VERIFICATION_CHECKLIST.md` (browse) - Questions to answer
3. `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` (2-3 hours) - Complete spec
   - OR use sharded version: `sharded/bible_sections/index.md` (load on-demand)
4. `reference/TOOL_GUIDE.md` (30 min) - Tool chain
5. `to_combine/ARCHITECTURE_CLARIFICATION.md` (15 min) - How it works

**Then:** Start Phase 0 tasks

---

### For Graphics/Driver Developer

**Read in this order:**
1. `PROJECT_OVERVIEW.md` → Part 1-3 (30 min) - Architecture
2. `reference/AF3DN_ANALYSIS.md` (20 min) - What we're replicating
3. `to_combine/ARCHITECTURE_CLARIFICATION.md` (15 min) - How it works
4. `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` → Sections 5, 7, 8, 9 (2 hours)
   - Section 5: FFNx Codebase Architecture
   - Section 7: C++ Modifications
   - Section 8: Assembly Hooks
   - Section 9: Renderer Integration
5. `character_maps/JAFONT_CHARACTER_MAP.md` (reference) - Character data

---

### For Text System Developer

**Read in this order:**
1. `reference/BEGINNER_GUIDE.md` (10 min) - Understand encoding
2. `PROJECT_OVERVIEW.md` → Part 1 & 1.5 (20 min) - Encoding system
3. `character_maps/JAFONT_CHARACTER_MAP.md` (30 min) - Complete character reference
4. `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` → Sections 3, 4 (1 hour)
   - Section 3: Critical Terminology & Concepts
   - Section 4: Asset Specifications & Data Structures

---

### For QA Engineer

**Read in this order:**
1. `reference/BEGINNER_GUIDE.md` (10 min) - What's being built
2. `TEST_PROCEDURE.md` (20 min) - Testing steps
3. `IMPLEMENTATION_VERIFICATION_CHECKLIST.md` (browse) - What to verify
4. `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` → Section 11 (30 min)
   - Section 11: Testing & Verification Protocol

---

### For Full-Stack Developer (Phase 6 - Crowdsourcing)

**Read in this order:**
1. `roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md` (1 hour) - Complete spec
2. `roadmap/FEATURE_ROADMAP.md` → Phase 6 section (10 min) - Summary
3. `to_combine/MULTI_LANGUAGE_FINDINGS.md` (20 min) - Language architecture

---

### For Product Manager

**Read in this order:**
1. `reference/BEGINNER_GUIDE.md` (10 min) - Understand the problem
2. `PROJECT_OVERVIEW.md` (30 min) - Understand the solution
3. `roadmap/FEATURE_ROADMAP.md` (20 min) - All phases
4. `IMPLEMENTATION_READINESS_ASSESSMENT.md` (20 min) - Current status

---

## 📏 Document Sizes & Token Counts

| Document | Lines | Tokens (approx) | Read Time |
|----------|-------|-----------------|-----------|
| **FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md** | 4,000 | 155,000 | 2-3 hours |
| **IMPLEMENTATION_READINESS_ASSESSMENT.md** | 800 | 30,000 | 20 min |
| **IMPLEMENTATION_VERIFICATION_CHECKLIST.md** | 800 | 30,000 | Browse |
| **roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md** | 1,728 | 60,000 | 1 hour |
| **PROJECT_OVERVIEW.md** | 1,200 | 45,000 | 30 min |
| **masterfindings.md** | 3,000 | 120,000 | 2 hours |

**Total documentation:** ~200,000 tokens

---

## 🔄 Sharded Documents (For LLMs)

If a document is too large for your context window, use the sharded versions:

### Master Bible (Sharded)

**Location:** `sharded/bible_sections/`

**Contents:** 18 files (each < 10,000 tokens)
- `index.md` - Master navigation
- `1-executive-mission-briefing.md` through `14-reference-materials-appendices.md`

**How to use:**
1. Start with `index.md` to see all sections
2. Load only the sections you need
3. Each section is standalone with cross-references

### Findings (Sharded)

**Location:** `sharded/findings_sections/`

**Contents:** 29 files (historical research, archived)
- `00_INDEX.md` - Master navigation
- Session-by-session research findings

**Note:** Superseded by Master Bible for implementation purposes.

---

## ⚡ Quick Reference

### "I need to understand encoding"
→ `reference/BEGINNER_GUIDE.md` (basics)
→ `character_maps/JAFONT_CHARACTER_MAP.md` (details)

### "I need to know what to implement"
→ `FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md` (complete spec)
→ `IMPLEMENTATION_READINESS_ASSESSMENT.md` (Phase 0 first)

### "I need to verify something"
→ `IMPLEMENTATION_VERIFICATION_CHECKLIST.md` (all questions)

### "I need to use a tool"
→ `reference/TOOL_GUIDE.md` (complete guide)

### "I need to test something"
→ `TEST_PROCEDURE.md` (test procedures)

### "I need to understand the architecture"
→ `PROJECT_OVERVIEW.md` (overview)
→ `to_combine/ARCHITECTURE_CLARIFICATION.md` (how it works)

### "I need to plan future features"
→ `roadmap/FEATURE_ROADMAP.md` (all phases)

---

## 🚫 What NOT to Read (Yet)

**Don't waste time on these unless specifically needed:**

- `sharded/findings_sections/` - Historical research (superseded by Master Bible)
- `REORGANIZATION_PLAN.md` - Directory cleanup (administrative)
- `masterfindings.md` - Historical research (superseded by Master Bible)

**These are archived/historical.** Focus on implementation documents.

---

## 📝 Document Update Status

All documents current as of **2025-11-24**:

| Document | Last Updated | Status |
|----------|--------------|--------|
| FFNX_JAPANESE_IMPLEMENTATION_MASTER_BIBLE.md | 2025-11-24 | ✅ Current |
| IMPLEMENTATION_READINESS_ASSESSMENT.md | 2025-11-24 | ✅ Current |
| IMPLEMENTATION_VERIFICATION_CHECKLIST.md | 2025-11-24 | ✅ Current |
| roadmap/FEATURE_ROADMAP.md | 2025-11-24 | ✅ Current |
| roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md | 2025-11-24 | ✅ Current |
| to_combine/ARCHITECTURE_CLARIFICATION.md | 2025-11-24 | ✅ Current |
| to_combine/MULTI_LANGUAGE_FINDINGS.md | 2025-11-24 | ✅ Current |

---

## 🔗 External Links

**Project Root:**
- `../README.md` - Project overview and structure
- `../DOCUMENTATION_MAP.md` - Complete navigation guide

**Assets:**
- `../assets/fonts/png/` - Font texture assets (6 files)
- `../assets/character_mappings/` - Character data and interactive viewer

**Reference:**
- `../reference/ff7_disassembly/` - FF7 executable disassembly
- `../reference/repomix_snapshots/` - FFNx codebase snapshots

---

**Questions? Check `../DOCUMENTATION_MAP.md` for complete navigation.**

**Ready to implement? Start with `IMPLEMENTATION_READINESS_ASSESSMENT.md`**

# FF7 Japanese Mod - Documentation Map

**For**: Finding the right document for your needs
**Updated**: 2025-11-18 18:53 JST

---

## Quick Navigation

### "I'm completely lost. What's this project about?"
→ Read: **BEGINNER_GUIDE.md** (10 min)
- Simple explanations without jargon
- File types explained (LGP, TEX, BIN)
- Why Japanese is different from English
- Visual comparisons

### "I'm a senior engineer. Brief me on the entire project."
→ Read: **PROJECT_OVERVIEW.md** (30 min)
- Executive summary
- Complete architecture diagrams (with Mermaid)
- All three implementation paths
- Technology decisions explained
- Timeline and risk assessment

### "I want to start testing FFNx texture override."
→ Read: **TEST_PROCEDURE.md** (reference)
- Step-by-step testing procedure
- Phase 1-6 with exact commands
- Troubleshooting guide
- What success looks like

### "I need to extract and convert font files."
→ Read: **TOOL_GUIDE.md** (reference)
- Complete tool chain documentation
- ulgp (LGP extraction/repacking)
- Image2TEX or Tex Tools (format conversion)
- FFNx configuration
- Complete workflows

### "What was researched? Where did findings come from?"
→ Read: **FINDINGS.md** (deep dive)
- All 9 sessions of research documented
- 40+ critical discoveries
- Session-by-session breakdown
- 44 URLs researched and documented

### "Show me all the URLs researched."
→ Read: **SCRAPED_URLS.md** (reference)
- Every URL that was analyzed
- Status of each scrape (success, failed, pending)
- Key findings from each URL
- Complete citation trail

### "What's the character mapping for Japanese?"
→ Read: **JAFONT_CHARACTER_MAP.md** (reference) or **character_tables/character_map_accurate.csv** (data)
- All 1,331 characters documented
- Mapping from FF7 index to Unicode
- Character distribution by texture
- Grid positions

### "How did we reverse-engineer AF3DN.P?"
→ Read: **AF3DN_ANALYSIS.md** (technical)
- Binary analysis results
- Export functions identified
- String extraction (jafont references)
- Import dependencies
- Build path discovered

### "What are the possible implementation paths?"
→ Read: **PROJECT_OVERVIEW.md** → Part 3 (diagrams + analysis)
- Path A: FFNx texture override
- Path B: AF3DN.P reverse engineering
- Path C: Hybrid FFNx extension (CHOSEN)
- Comparison matrix
- Timeline for each

### "I'm implementing Path C. What are the phases?"
→ Read: **PROJECT_OVERVIEW.md** → Part 9.5 & Recommended Path
- Phase 1: Proof of concept (1-2 weeks)
- Phase 2: Architecture study (1-2 weeks)
- Phase 3: FFNx extension development (4-6 weeks)
- Phase 4: Game executable patching (2-3 weeks)
- Phase 5: Text system integration (2-3 weeks)
- Phase 6: Release & polish (1-2 weeks)

### "What about future features (furigana, multi-language toggle)?"
→ Read: **FEATURE_ROADMAP.md** (vision)
- Feature 1: Japanese text rendering (Phase 1-6)
- Feature 2: English ↔ Japanese toggle at runtime
- Feature 3: Furigana (reading guides above kanji)
- Implementation complexity and timeline for each

---

## Document Descriptions

### Core Planning Documents

| Document | Purpose | Audience | Depth | Read Time |
|----------|---------|----------|-------|-----------|
| **BEGINNER_GUIDE.md** | Learn the concepts | Confused people, non-technical | Surface | 10 min |
| **PROJECT_OVERVIEW.md** | Complete project brief | Senior engineers, architects | Medium | 30 min |
| **FEATURE_ROADMAP.md** | Future vision beyond Japanese | Product managers, long-term planning | Medium | 15 min |

### Technical Reference Documents

| Document | Purpose | Audience | Depth | Use |
|----------|---------|----------|-------|-----|
| **AF3DN_ANALYSIS.md** | Reverse engineering results | Driver developers | Deep | Reference |
| **JAFONT_CHARACTER_MAP.md** | Character encoding reference | Text system developers | Deep | Reference |
| **TOOL_GUIDE.md** | Complete tool chain | Implementers | Medium | How-to |
| **TEST_PROCEDURE.md** | Testing procedure | QA engineers | Medium | Step-by-step |

### Research & Findings Documents

| Document | Purpose | Audience | Depth | Use |
|----------|---------|----------|-------|-----|
| **FINDINGS.md** | Complete research log | Researchers, decision makers | Deep | Complete history |
| **SCRAPED_URLS.md** | All researched sources | Citation tracking | Medium | Reference |
| **character_tables/** | Actual character data | Developers | Raw data | Lookup |

---

## Reading Paths by Role

### For Product Manager
1. Start: **BEGINNER_GUIDE.md** (understand the problem)
2. Then: **PROJECT_OVERVIEW.md** (understand the solution)
3. Reference: **FEATURE_ROADMAP.md** (future features)
4. Reference: **PROJECT_OVERVIEW.md** Part 8 (timeline, risks)

### For Graphics/Driver Developer
1. Start: **PROJECT_OVERVIEW.md** Part 1-3 (architecture)
2. Deep: **AF3DN_ANALYSIS.md** (what we're replicating)
3. Reference: **JAFONT_CHARACTER_MAP.md** (character data)
4. Reference: **TOOL_GUIDE.md** (tools available)

### For Text/Encoding System Developer
1. Start: **BEGINNER_GUIDE.md** (understand encoding)
2. Deep: **PROJECT_OVERVIEW.md** Part 1 & 1.5 (encoding system)
3. Reference: **JAFONT_CHARACTER_MAP.md** (character mapping)
4. Reference: **FINDINGS.md** (research context)

### For QA Engineer
1. Start: **BEGINNER_GUIDE.md** (understand what's being built)
2. How-to: **TEST_PROCEDURE.md** (testing steps)
3. Reference: **TOOL_GUIDE.md** (tools and workflows)
4. Reference: **PROJECT_OVERVIEW.md** Part 12 (success criteria)

### For Community Modder
1. Start: **BEGINNER_GUIDE.md** (understand what's happening)
2. How-to: **TOOL_GUIDE.md** (how to use tools)
3. Reference: **TEST_PROCEDURE.md** (testing)
4. Future: **FEATURE_ROADMAP.md** (what's coming)

### For Researcher/Historian
1. Complete: **FINDINGS.md** (all research 9 sessions)
2. Sources: **SCRAPED_URLS.md** (all 44 URLs)
3. Analysis: **AF3DN_ANALYSIS.md** (reverse engineering)
4. Context: **PROJECT_OVERVIEW.md** (how we got here)

---

## Document Relationships

```
BEGINNER_GUIDE.md (Foundation)
    ↓
    ├─→ PROJECT_OVERVIEW.md (Complete architecture)
    │       ├─→ AF3DN_ANALYSIS.md (Deeper technical detail)
    │       ├─→ JAFONT_CHARACTER_MAP.md (Character encoding detail)
    │       └─→ FEATURE_ROADMAP.md (Future features)
    │
    ├─→ TOOL_GUIDE.md (How to use the tools)
    │       ├─→ TEST_PROCEDURE.md (Testing workflow)
    │       └─→ character_tables/ (Character data)
    │
    └─→ FINDINGS.md (Complete research history)
            └─→ SCRAPED_URLS.md (Source citations)
```

---

## Document Status

| Document | Status | Last Updated | Completeness |
|----------|--------|--------------|--------------|
| BEGINNER_GUIDE.md | ✅ Complete | 2025-11-18 | 100% |
| PROJECT_OVERVIEW.md | ✅ Complete | 2025-11-18 | 100% |
| AF3DN_ANALYSIS.md | ✅ Complete | 2025-11-17 | 100% |
| JAFONT_CHARACTER_MAP.md | ✅ Complete | 2025-11-17 | 100% |
| TOOL_GUIDE.md | ✅ Complete | 2025-11-17 | 100% |
| TEST_PROCEDURE.md | ✅ Complete | 2025-11-17 | 100% |
| FEATURE_ROADMAP.md | ✅ Complete | 2025-11-16 | 100% |
| FINDINGS.md | ✅ Complete | 2025-11-17 | 100% |
| SCRAPED_URLS.md | ✅ Complete | 2025-11-15 | 100% |
| character_tables/ | ✅ Complete | 2025-11-17 | 100% |
| DOCUMENTATION_MAP.md | ✅ Complete | 2025-11-18 | 100% (this file) |

---

## Key Facts (For Quick Reference)

**The Problem**:
- FF7 English PC cannot display Japanese characters
- Font system is fundamentally incompatible (1 texture for 256 chars vs 2,300+ needed)

**The Solution**:
- We're building a FFNx extension (Path C)
- Replicating AF3DN.P's architecture (Square Enix's proven solution)
- Adding support for 6 font textures + FA-FE character page system

**The Team**:
- Senior developer(s) needed for C++ graphics programming
- Text system developer for touphScript extension
- QA engineer for comprehensive testing
- Project manager for coordination

**The Timeline**:
- Phase 1-2: 2-4 weeks (proof of concept + architecture study)
- Phase 3-5: 8-12 weeks (implementation)
- Phase 6: 1-2 weeks (release)
- **Total: 10-14 weeks**

**The Status**:
- ✅ Research complete (9 sessions, 40+ findings, 44 URLs)
- ✅ Character mapping complete (1,331 characters)
- ✅ Tools validated
- ✅ Architecture designed
- ⏳ Implementation ready to begin

**Why This Works**:
- Square Enix already proved this approach in 2013
- AF3DN.P is a working reference implementation
- We're reimplementing, not inventing
- Community-driven (FFNx) vs proprietary (AF3DN.P)
- Fully legal and ethical

---

## How to Update This Map

When new documents are created:
1. Add entry to appropriate section (Core Planning, Technical Reference, or Research)
2. Add entry to relevant "Reading Path by Role" section
3. Update "Document Relationships" diagram
4. Update "Document Status" table
5. Commit with message: `docs: add new document to DOCUMENTATION_MAP`

---

**Questions?** Check the relevant document above, or ask in the next session!

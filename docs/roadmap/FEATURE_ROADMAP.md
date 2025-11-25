# FF7 Multi-Language Learning Edition - Feature Roadmap

**Created**: 2025-11-16 17:30:00 JST (Sunday)
**Last Modified**: 2025-11-17 11:41:11 JST (Monday)
**Version**: 1.1.0
**Author**: Research Session 6-7
**Session-ID**: 1021bc57-9aa2-41fe-baad-a6b89b252744

---

## Product Vision

Transform Final Fantasy VII into a comprehensive **multi-language learning tool** that leverages nostalgia and familiar story context to enable effective language acquisition.

**Product Name**: "FF7 Multi-Language Learning Edition"

**SESSION 7 UPDATE**: Discovered **5 complete language packs** in the Japanese eStore version:
- English (EN)
- Japanese (JA)
- **French (FR)** ← NEW DISCOVERY!
- German (DE)
- Spanish (ES)

**Expanded Market**: Japanese, French, German, AND Spanish language learners!

---

## Core Features

### Phase 1: Japanese Text Support ✅ **95% COMPLETE (via PR #737)**

**Goal**: Display Japanese text with full 2,000+ kanji support

**Status via PR #737 (CosmosXIII, September 2024):**
- [x] Font texture research and documentation ✅ DONE
- [x] Japanese eStore version acquired (jafont_1-6.tex available) ✅ DONE
- [x] Extract and analyze jafont_1-6.tex character layout ✅ DONE (via PR #737)
- [x] Implement double-byte character encoding (FA-FE) ✅ DONE (via PR #737)
- [x] Create character→texture mapping algorithm ✅ DONE (via PR #737)
- [x] Modify FFNx for multi-texture font loading ✅ DONE (via PR #737)
- [x] Test complete Japanese text rendering ✅ MOSTLY WORKS (bugs in Phase 1.5)

**Remaining Work**: See Phase 1.5 (bug fixes)

**Effort**: Originally estimated 2-3 months, **actually 3-4 weeks (bug fixes only)**
**Priority**: CRITICAL (foundation for all other features)
**Status**: Implementation complete (via PR #737), bug fixes needed
**Scope Limitation**: PR #737 works with Japanese game version only, NOT English version

---

### Phase 1.5: PR #737 Bug Fixes (NEW - CRITICAL)

**Goal**: Fix blocking bugs in PR #737 to enable merge + extend for multi-language

**Requirements**:
- [ ] **Fix colored text rendering** (Priority 1)
  - Root cause: Missing colored texture variants OR tinting failure
  - Solution: Either load `jafont_X_red.tim` variants OR implement GPU shader
  - Estimated: 10-15 hours research, 5-10 hours implementation

- [ ] **Fix character name input screen** (Priority 2)
  - Root cause: Unknown (wrong texture indexing?)
  - Solution: Debug rendering code for name input screen
  - Estimated: 8-12 hours debugging, 2-4 hours fix

- [ ] **Fix cursor alignment issues** (Priority 3)
  - Root cause: Hardcoded spacing assumptions broken by Japanese widths
  - Solution: Adjust cursor position calculation based on actual text width
  - Estimated: 3-5 hours

**Effort**: 3-4 weeks
**Priority**: CRITICAL (unblocks everything else)
**Dependencies**: Access to Japanese FF7 version, PR #737 build environment
**Outcome**: PR #737 can be merged into main FFNx

---

### Phase 2: Multi-Language Toggle (5 Languages)

**Goal**: Switch between all 5 languages at runtime (EN↔JA↔FR↔DE↔ES)

**SESSION 7 DISCOVERY**: Square Enix ALREADY implemented 5-language separation!
- Separate executables: ff7_en.exe, ff7_ja.exe, ff7_fr.exe, ff7_de.exe, ff7_es.exe
- Per-language data directories: lang-en/, lang-ja/, lang-fr/, lang-de/, lang-es/
- Language-specific field dialogues: flevel.lgp (EN), jfleve.lgp (JA), fflevel.lgp (FR), gflevel.lgp (DE), sflevel.lgp (ES)
- Qt-based FF7_Launcher.exe for language selection at launch time

**Requirements**:
- [x] Identify language-specific file locations (Session 7 - DONE)
- [x] Analyze Square Enix's language selection mechanism (Session 7 - DONE)
- [ ] Extend FFNx to support runtime language switching (not just launch-time)
- [ ] Keyboard shortcut toggle (e.g., F9 for next language, Shift+F9 for selector menu)
- [ ] Hot-reload text files without game restart
- [ ] State persistence (remember language choice per save file)

**Implementation Options**:

| Option | Complexity | Pros | Cons |
|--------|-----------|------|------|
| **A: FFNx path switching** | MEDIUM | Uses existing structure | Requires FFNx modification |
| B: Memory hot-patching | HIGH | Fastest switching | Complex, error-prone |
| C: Wrapper launcher | LOW | No game modification | Requires restart |

**Recommended**: Option A - Leverage Square Enix's existing file organization, modify FFNx to hot-swap paths

**NEW: File Mapping Table**:
```
Language | Font LGP      | Field LGP    | Lang Dir  | Executable
---------|---------------|--------------|-----------|-------------
English  | menu_us.lgp   | flevel.lgp   | lang-en/  | ff7_en.exe
Japanese | menu_ja.lgp   | jfleve.lgp   | lang-ja/  | ff7_ja.exe
French   | menu_fr.lgp   | fflevel.lgp  | lang-fr/  | ff7_fr.exe
German   | menu_gm.lgp   | gflevel.lgp  | lang-de/  | ff7_de.exe
Spanish  | menu_sp.lgp   | sflevel.lgp  | lang-es/  | ff7_es.exe
```

**Effort**: 2-4 weeks (leveraging existing structure makes this EASIER than expected)
**Priority**: HIGH
**Dependencies**: Phase 1 complete (Japanese font rendering working)

---

### Phase 3: Furigana Support

**Goal**: Display reading guides above kanji for learners

**Requirements**:
- [ ] Text format markup system (kanji + furigana association)
- [ ] Furigana data generation (manual or automated)
- [ ] Rendering engine modification for dual-layer text
- [ ] Variable line height calculation
- [ ] Toggle on/off option for user preference

**Implementation Tiers**:

**Tier 1: Inline Furigana (MVP)**
```
Display: 漢字(かんじ)
Effort: 3-6 weeks
Pros: Minimal engine changes
Cons: Not traditional appearance
```

**Tier 2: Proper Above-Kanji Rendering (Advanced)**
```
Display:  かんじ
         漢字
Effort: 2-3 months additional
Pros: Authentic typography
Cons: Significant rendering overhaul
```

**Priority**: MEDIUM
**Dependencies**: Phase 1 complete, Phase 2 recommended

---

### Phase 4: Cheat/Booster Integration

**Goal**: Enable speed/difficulty toggles for learning focus

**Status**: ✅ ALREADY AVAILABLE

User's Japanese eStore version (J13308W_001_D01, v2.00) includes:
- 3x Speed Mode
- Max Stats
- God Mode
- No Random Encounters
- Gil/Items boost

**No development needed** - document keyboard shortcuts only

---

### Phase 5: Polish & Distribution

**Goal**: Package and distribute as community mod

**Requirements**:
- [ ] 7th Heaven .IRO mod package
- [ ] User installation guide
- [ ] Settings documentation
- [ ] Performance optimization
- [ ] Community testing
- [ ] Release notes

**Effort**: 1-2 months
**Priority**: LOW (after core features complete)

---

### Phase 6: Crowdsourced Translation System (Future)

**Goal**: Enable community-driven translation improvements through in-game submissions and web-based voting

**Status**: Design Complete (See: `docs/roadmap/FFNX_CROWDSOURCED_TRANSLATION_SPEC.md`)

**Summary**:
- **In-Game Client**: Hotkey-triggered (Ctrl+T) translation submission dialog
  - Captures current dialogue context (string ID, field map)
  - Shows all existing translations for comparison
  - Real-time encoding validation
  - In-game preview of proposed translation
  - HTTP submission to central repository

- **Web Platform**: Community review and voting system
  - Public dashboard for browsing pending translations
  - Upvote/downvote with rationale comments
  - Moderator approval queue
  - Translation history tracking
  - Glossary enforcement (consistent terminology)
  - Export approved translations → 7th Heaven .iro packages

- **User Workflows**:
  1. **Players**: Fix awkward translations when encountered in-game
  2. **Translators**: Review and vote on community submissions via web
  3. **Moderators**: Approve high-quality submissions for inclusion in updates
  4. **Everyone**: Download community-approved translation packs

- **Security & Anti-Abuse**:
  - Rate limiting (50 submissions/day client-side, IP-based server-side)
  - Profanity filter and content validation
  - Vote manipulation detection (IP tracking, suspicious patterns)
  - JWT authentication for moderators
  - Auto-flagging of spam/abuse

- **Infrastructure**:
  - Docker-based deployment (API, PostgreSQL, Redis, Nginx)
  - ~$45/month hosting costs (DigitalOcean/AWS)
  - CI/CD pipeline (GitHub Actions)
  - Daily database backups with S3 storage

**Technical Feasibility**: 6/10 (Medium complexity)

**Why Feasible**:
- Reads existing game memory (no risky writes)
- Reuses FF7's built-in menu system
- Standard web technologies (REST API, PostgreSQL/SQLite)
- Isolated feature (won't interfere with core rendering)

**Estimated Implementation Time**:
- **MVP** (submission only): 30-40 hours
- **Full system** (voting, moderation, web platform): 60-80 hours
- **Total**: 15-20% of core multi-language implementation effort

**Phase Breakdown**:
1. **Phase 6.1** - Client-side submission (FFNx modifications)
2. **Phase 6.2** - Server-side API and database
3. **Phase 6.3** - Web review interface
4. **Phase 6.4** - Moderation tools and analytics
5. **Phase 6.5** - .iro package export automation

**Future Enhancements** (Phase 6+):
- Machine translation suggestions (Google Translate API integration)
- Translation memory (learn from approved translations)
- Glossary enforcement warnings
- Context screenshots (auto-capture on submission)
- A/B testing of translation variants
- Reputation system for contributors
- Mobile app for translating on-the-go
- Translation analytics dashboard

**Priority**: MEDIUM-LOW (Phase 2+ feature, requires core multi-language system working first)
**Dependencies**: Phase 1-3 complete (Japanese rendering + language switching functional)

**User Value**: Transforms translation from static to living, community-maintained artifact

---

## Technical Architecture

### Font System

```
English Version:
menu_us.lgp → USFONT_*.TEX (6 files, single-byte encoding)

Japanese Version:
menu_ja.lgp → jafont_1-6.tex (6 files, double-byte encoding)

Modified Version:
Both font sets loaded → Runtime selection based on language setting
```

### Text Encoding

```
Current (English):
FF Text format → Single-byte (256 characters max)
"Hello" = [0x48, 0x45, 0x4C, 0x4C, 0x4F]

Required (Japanese):
Shift-JIS → Double-byte (65,536 characters possible)
"漢字" = [0x8A, 0xBF, 0x8E, 0x9A]
```

### Character→Texture Mapping

```
Given: Character code 0x8ABF (漢)
Required: Which of jafont_1-6.tex contains this glyph?
Mapping: Character code → Texture index + glyph offset

Possible algorithms:
1. Range-based: 0x0000-0x0FFF → jafont_1.tex
2. Lookup table: Load from file at runtime
3. Hash function: char_code % 6 = texture_index
```

---

## Target Users

### Primary: Japanese Language Learners

**Level**: N5-N2 (beginner to upper-intermediate)
**Needs**:
- Full kanji support with furigana
- EN↔JA comparison
- Familiar story context

### Secondary: Heritage Speakers

**Level**: Rusty native speakers
**Needs**:
- Japanese text access
- Occasional English reference
- Minimal furigana

### Tertiary: FF7 Enthusiasts

**Level**: Fans interested in original Japanese
**Needs**:
- Localization comparison
- Cultural context
- No furigana required

---

## Success Metrics

### Technical Milestones

- [ ] 100% of 2,136 Jōyō kanji displayable
- [ ] All game text renders correctly in Japanese
- [ ] Language toggle under 100ms response time
- [ ] Furigana doesn't cause text overflow
- [ ] No crashes or memory leaks

### User Experience Milestones

- [ ] First-time setup under 10 minutes
- [ ] Language toggle accessible via single keypress
- [ ] Furigana toggle saves user preference
- [ ] Boosters don't interfere with text features
- [ ] 7th Heaven integration seamless

### Community Milestones

- [ ] FFNx developers collaboration established
- [ ] Beta testing with 10+ Japanese learners
- [ ] Featured on Japanese learning communities
- [ ] Positive feedback from heritage speakers
- [ ] No copyright/legal issues

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Double-byte encoding too complex | MEDIUM | CRITICAL | Start with FFNx collab early |
| Furigana rendering breaks windows | HIGH | MEDIUM | Use inline format initially |
| Community adoption low | LOW | LOW | Market to Japanese learning communities |
| Legal issues with redistribution | MEDIUM | HIGH | Distribute as patch, not assets |
| FFNx devs not responsive | LOW | HIGH | Open source allows forking |

---

## Timeline Estimate (REVISED - Post-PR #737 Discovery)

**🔴 MAJOR UPDATE:** PR #737 provides 95% of Phase 1 implementation, reducing timeline by 50-60%

**Phase 1.5 (PR #737 Bug Fixes)**: 3-4 weeks **[NEW]**
- Week 1-2: Fix colored text rendering
- Week 3: Fix character name input screen
- Week 4: Fix cursor alignment, submit patches upstream

**Phase 1 (Core Japanese)**: ✅ **95% COMPLETE** (via PR #737)
- Remaining: 3-4 weeks of bug fixes (see Phase 1.5 above)
- Original estimate was 2-3 months → **Actually 3-4 weeks**
- **Time saved: 2 months thanks to PR #737**

**Phase 2 (Language Toggle)**: 2-3 weeks
- Week 1-2: Extend PR #737's architecture for 5 languages
- Week 3: Add hotkey system, test multi-language switching
- Note: Easier than originally estimated due to PR #737's foundation

**Phase 3 (Furigana)**: 3-6 weeks (inline only)
- Week 1-2: Text format design
- Week 3-4: Rendering implementation on top of PR #737
- Week 5-6: Testing and refinement

**Phase 4 (Boosters)**: 0 weeks (already done)

**Phase 5 (Polish)**: 3-4 weeks
- Documentation, packaging, community testing
- Faster than originally estimated (less code to document)

**Original Total Timeline**: 5-8 months
**Revised Total Timeline**: **2.5-4 months**
**Time Saved**: **2.5-4 months (50-60% reduction)**

---

## Resources Required

### Technical

- FFNx source code access (GitHub - available)
- Japanese FF7 assets (acquired by user)
- C++ development environment
- Graphics debugging tools
- Text hex editor

### Human

- User (project owner, has Japanese version)
- FFNx developers (collaboration pending)
- Japanese language verifiers (for furigana accuracy)
- Beta testers (Japanese learners)

### Community

- qhimm.com forums (established)
- FFNx GitHub Issues (active)
- Japanese learning communities (target market)

---

## Next Steps (Immediate)

1. **Extract jafont_1-6.tex** from user's Japanese eStore version
2. **Analyze character layout** (glyph size, organization, count)
3. **Research Shift-JIS implementation** in FFNx or similar projects
4. **Contact FFNx developers** with research findings and asset access
5. **Create JAPANESE_FONT_ANALYSIS.md** documenting extraction results
6. **Design character→texture mapping** algorithm based on analysis

---

## Document References

- **FINDINGS.md** - Complete research findings (all sessions)
- **SCRAPED_URLS.md** - Research sources (38 URLs)
- **TOOL_GUIDE.md** - Tool chain documentation (v1.1.0)
- **TEST_PROCEDURE.md** - FFNx texture override testing
- **FEATURE_ROADMAP.md** - This document

---

**Document Status**: Active Planning
**Next Update**: After Phase 1 implementation begins
**Maintainer**: Project Team

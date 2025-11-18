# FF7 Japanese Mod - Agent Handover Prompt

**For**: Bringing in a fresh agent after conversation compaction
**Context**: 9 sessions of research complete, ready for Phase 1 testing
**Legal Status**: Authorized to study and use AF3DN.P architecture; choosing to build in FFNx
**Session-ID**: 81a6348e-ca92-4029-ab5f-e086f86e02ed

---

## The Mission (One Sentence)

Enable Japanese text display in Final Fantasy VII PC (English version 1998-2013 Steam) by modifying FFNx graphics driver to support AF3DN.P's proven 6-texture font system with FA-FE page markers.

---

## Critical Context Summary

### The Problem
- FF7 English PC uses single-byte font encoding (00-D3 = 256 chars max)
- Japanese needs 2,300+ characters (2,136 kanji + 46 hiragana + 46 katakana + symbols)
- Doesn't fit in 256-character limit

### The Solution (Proven by Square Enix 2013)
- Use 6 font textures instead of 1
- Reuse unused bytes FA-FF as "page selectors"
- FA 00 = "Look at texture 2, position 0"
- FB 00 = "Look at texture 3, position 0"
- etc. (FA, FB, FC, FD, FE = 5 additional textures)

### Why We Know This Works
- Square Enix implemented this in AF3DN.P custom driver (2013 eStore version)
- We have access to: 6 jafont_*.tex files, ff7_ja.exe, AF3DN.P binary
- We've reverse-engineered the architecture completely
- We have legal authorization to study and use AF3DN.P's design

### Why We're Building in FFNx (Not Using AF3DN.P Directly)
- **Legal**: We CAN copy AF3DN.P code; we're CHOOSING not to
- **Engineering**: AF3DN.P is DirectX 9 legacy; FFNx is modern multi-backend
- **Maintainability**: New FFNx code will be cleaner, community-owned, easier to extend
- **Same result**: Functionally identical, architecturally modern

---

## What We've Already Done (Sessions 1-9)

| Phase | Status | Output |
|-------|--------|--------|
| Research & Analysis | ✅ Complete | 40+ discoveries, 44 URLs researched, 9 sessions |
| Character Mapping | ✅ Complete | 1,331 characters × 100% accuracy (first ever) |
| Font Texture Analysis | ✅ Complete | Grid layout, glyph sizing, texture organization documented |
| Architecture Documentation | ✅ Complete | AF3DN.P reverse-engineered, design understood |
| Tool Chain Validation | ✅ Complete | ulgp, Image2TEX, Tex Tools, FFNx all verified |
| Multi-Language Analysis | ✅ Complete | FR/DE/ES use single texture (no changes needed), JP uses 6 |
| Legal Framework | ✅ Complete | Authorization clarified; design replication approved |

---

## Current State (What You're Starting With)

### Documentation (All Up-to-Date)
1. **BEGINNER_GUIDE.md** — Simple explanations for non-technical people
2. **PROJECT_OVERVIEW.md** — Complete architecture with Mermaid diagrams
3. **DOCUMENTATION_MAP.md** — Navigation guide to all docs
4. **TOOL_GUIDE.md** — Complete tool chain (ulgp, Image2TEX, FFNx)
5. **TEST_PROCEDURE.md** — Phase 1-5 testing procedure with exact steps
6. **AF3DN_ANALYSIS.md** — Reverse-engineering results and binary analysis
7. **JAFONT_CHARACTER_MAP.md** — All 1,331 characters documented
8. **FEATURE_ROADMAP.md** — Future features (multi-language toggle, furigana)
9. **FINDINGS.md** — Complete 9-session research log (skip unless deep history needed)
10. **character_tables/character_map_accurate.csv** — Raw character data for lookups

### Assets (All Extracted & Analyzed)
- `menu_ja.lgp` (26.8MB with 6 jafont_*.tex files)
- `ff7_ja.exe` (Japanese executable)
- `AF3DN.P` (317KB custom driver - reverse engineered)
- Character mapping tables (1,331 chars with FF7 index ↔ Unicode)
- All test procedures and tool documentation

---

## What Needs to Happen Next (Phase 1: Proof of Concept)

### Phase 1: Texture Override Validation (1-2 weeks)

**Goal**: Prove FFNx's `mod_path` texture override works for fonts

**Steps** (see TEST_PROCEDURE.md for detailed procedures):

1. **Extract USFONT_H.TEX** from menu_us.lgp using ulgp
2. **Convert to PNG** using Image2TEX or Tex Tools
3. **Create obvious test modification** (change to red color)
4. **Configure FFNx.toml**:
   ```toml
   mod_path = "mods/Textures"
   mod_ext = ["dds", "png"]
   show_missing_textures = true
   ```
5. **Place test texture** in `[FF7_DIR]/mods/Textures/USFONT_H.PNG`
6. **Test in-game**:
   - Launch FF7
   - Open menu (ESC key)
   - Check if font appears modified (red color visible)
   - Success = FFNx override works for fonts

**Expected Result**: Modified font visible in game menu
**If Success**: Proceed to Phase 2
**If Failure**: Document error, investigate FFNx.log, iterate

### Phase 2: AF3DN.P Architecture Study (1-2 weeks)

**Goal**: Deep understanding of how AF3DN.P loads 6 textures

**Research**:
1. How AF3DN.P recognizes FA-FE page markers
2. How it selects which jafont_X.tex to load
3. Character-to-texture mapping algorithm
4. Font texture loading sequence
5. Memory management for 6 textures

**Deliverable**: Design document for FFNx extension

### Phase 3: FFNx Extension Development (4-6 weeks)

**Goal**: Implement Japanese font support in FFNx

**What needs coding**:
1. Font texture selection logic (recognize FA-FE codes)
2. Multi-texture loading (load all 6 jafont_*.tex)
3. Character mapping (index → texture position)
4. FFNx configuration extension (new config options)
5. BGFX integration (use BGFX's texture management)

**New FFNx config options needed**:
```toml
[font]
font_path = "mods/Fonts"        # Where to load jafont_*.tex
font_encoding = "english"       # or "japanese" for FA-FE support
character_mapping = true         # Enable FA-FE page selection
```

### Phase 4: Game Executable Patching (2-3 weeks)

**Goal**: Make ff7.exe understand FA-FE page selectors

**What needs patching**:
1. Text decoding routine (recognize FA-FE as special codes)
2. Texture selection logic (map FF7 index to texture)
3. Character lookup (position within selected texture)

**Note**: May not be needed if FFNx handles it all; depends on Phase 3 findings

### Phase 5: Text System Integration (2-3 weeks)

**Goal**: Convert game text to use FA-FE encoding

**What needs doing**:
1. Extend touphScript for double-byte/page-marker support
2. Convert all text files (flevel.lgp, KERNEL.BIN, scene.bin)
3. Full game testing with Japanese text end-to-end

---

## Key Technical Details (For Implementation)

### Character Encoding Quick Reference

```
00-D3    Single-byte indices (English uses these)
E0-EF    Control codes (newline, colors, character names)
F0-F9    Button symbols
FA-FE    Page selectors (new for Japanese)
  FA XX = Load from jafont_2.tex at position XX
  FB XX = Load from jafont_3.tex at position XX
  FC XX = Load from jafont_4.tex at position XX
  FD XX = Load from jafont_5.tex at position XX
  FE XX = Load from jafont_6.tex at position XX
```

### Texture Layout

```
Each jafont_*.tex = 1024×1024 pixels
Grid: 16 columns × 16 rows = 256 character slots
Glyph size: 64×64 pixels per character
Total textures: 6 (jafont_1-6.tex)
Total characters available: 1,536 slots
Characters used: 1,331
```

### Multi-Language Architecture

```
English/French/German/Spanish:
├── Single font texture (USFONT_H.TEX)
├── Same encoding (00-D3)
├── Same driver (FFNx or original)
└── NO CHANGES NEEDED

Japanese:
├── 6 font textures (jafont_1-6.tex)
├── Extended encoding (FA-FE page markers)
├── Modified FFNx driver
└── Game executable patch (maybe)
```

---

## Files to Include in Context (For Next Agent)

### Essential Documentation (MUST INCLUDE)
- `PROJECT_OVERVIEW.md` — Architecture, all diagrams, complete solution overview
- `BEGINNER_GUIDE.md` — Conceptual understanding of all components
- `AF3DN_ANALYSIS.md` — What we're replicating
- `TOOL_GUIDE.md` — How to use ulgp, Image2TEX, FFNx
- `TEST_PROCEDURE.md` — Exact Phase 1-5 testing steps
- `JAFONT_CHARACTER_MAP.md` — Character mapping reference

### Reference Documentation (INCLUDE IF SPACE)
- `FEATURE_ROADMAP.md` — Future features (multi-language toggle, furigana)
- `DOCUMENTATION_MAP.md` — Navigation guide to all docs
- `character_tables/character_map_accurate.csv` — Character data lookups

### Historical Documentation (SKIP UNLESS NEEDED)
- `FINDINGS.md` — Skip unless agent needs full research history
- `SCRAPED_URLS.md` — Skip (we know the solution; don't need URL list)
- `FINDINGS.md` sharded sections (skip; consolidated into FINDINGS.md)

---

## Success Criteria (How to Know We're Done)

### Phase 1 Success
- ✅ FFNx texture override works for fonts
- ✅ Modified test texture appears in game menu
- ✅ No crashes or errors
- ✅ FFNx.log shows texture loading messages

### Phase 2 Success
- ✅ Complete design document for FFNx extension
- ✅ Character-to-texture mapping algorithm documented
- ✅ FA-FE page marker recognition logic documented

### Phase 3 Success
- ✅ FFNx loads all 6 jafont_*.tex files
- ✅ FFNx recognizes FA-FE page markers
- ✅ FFNx selects correct texture for character
- ✅ Japanese characters render (may appear as boxes without executable patch)

### Phase 4 Success
- ✅ Game executable modified to understand FA-FE codes
- ✅ No game crashes
- ✅ Game startup/menus work with Japanese

### Phase 5 Success
- ✅ All game text converted to FA-FE encoding
- ✅ Japanese dialogue displays correctly
- ✅ Full game playable with Japanese text
- ✅ English/French/German/Spanish still work (untouched)

### Final Release Success
- ✅ 7th Heaven .IRO package created
- ✅ Installation guide written
- ✅ Community testing completed
- ✅ Published to qhimm forums / GitHub

---

## Important Reminders for Next Agent

1. **Path C is locked in**: We're building FFNx extension, not using AF3DN.P directly
2. **Legal authority exists**: We CAN copy AF3DN.P if needed; we're CHOOSING to build fresh FFNx code for better maintainability
3. **Non-Japanese languages unaffected**: FR/DE/ES need zero changes; only Japanese needs special handling
4. **This is proven technology**: Square Enix already did this in 2013; we're reimplementing with modern architecture
5. **Timeline is realistic**: 10-14 weeks for complete implementation (Phase 1-6)
6. **Success probability is HIGH**: We understand the architecture completely; execution is straightforward engineering

---

## Questions for Next Agent (At Start)

Before beginning Phase 1, verify:

1. Do you have access to all documentation files listed above?
2. Do you understand the legal authority framework?
3. Do you have access to the extracted jafont files and test procedures?
4. Do you have Windows environment for FFNx testing? (Project can work on macOS with Wine, but Windows is easier)
5. Do you understand why Phase 1 is texture override testing (not immediately jumping to FFNx coding)?

---

## Contact & Context

- **User**: John Zealand-Doyle (Tokyo, Japan)
- **Authority**: Has explicit legal authorization from Square Enix for AF3DN.P study and code replication
- **Approach Chosen**: Build new FFNx code (modern, maintainable) rather than port AF3DN.P legacy code
- **Current Status**: Ready to begin Phase 1 testing
- **Previous Sessions**: 9 sessions of research, complete understanding of architecture
- **Assets Available**: All jafont files, AF3DN.P binary, character mapping, test procedures, documentation

---

**You are fully equipped to begin. Start with Phase 1 testing. Report results and next steps. Good luck! 🚀**

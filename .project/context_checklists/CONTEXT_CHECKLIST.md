# Context Inclusion Checklist (For Conversation Compaction)

**Purpose**: Specify exactly which files to include when compacting this conversation for a fresh agent

---

## MUST INCLUDE (Essential - Non-Negotiable)

**These files are absolutely required for the next agent to proceed:**

- [ ] `HANDOVER_PROMPT.md` — Complete briefing for fresh agent (START HERE)
- [ ] `PROJECT_OVERVIEW.md` — Architecture, diagrams, solution design
- [ ] `BEGINNER_GUIDE.md` — Conceptual understanding
- [ ] `TEST_PROCEDURE.md` — Exact Phase 1 testing steps
- [ ] `AF3DN_ANALYSIS.md` — What we're replicating
- [ ] `TOOL_GUIDE.md` — How to use tools (ulgp, Image2TEX, FFNx)
- [ ] `JAFONT_CHARACTER_MAP.md` — Character reference
- [ ] `character_tables/interactive_viewer/ff7_complete_mapping_compact.csv` — Character mapping data

**Estimated tokens for essential files**: ~40,000 tokens

---

## INCLUDE IF SPACE PERMITS (Recommended)

**These provide helpful context but aren't blocking:**

- [ ] `DOCUMENTATION_MAP.md` — Navigation guide
- [ ] `FEATURE_ROADMAP.md` — Future features vision

**Estimated tokens for recommended files**: ~5,000 tokens

---

## SKIP (Not Needed - Use Space for Other Context)

**These files can be skipped without losing critical information:**

- [ ] ~~`FINDINGS.md`~~ — Skip (info consolidated into other docs)
- [ ] ~~`SCRAPED_URLS.md`~~ — Skip (research complete; URLs not needed)
- [ ] ~~`documentation_management/findings_sections/*`~~ — Skip (sharded content; consolidated into FINDINGS.md)

**Space saved by skipping**: ~15,000+ tokens

---

## Total Context Size

| Set                  | Files        | Est. Tokens |
| -------------------- | ------------ | ----------- |
| Essential            | 8 files      | ~40,000     |
| Recommended          | 2 files      | ~5,000      |
| Skipped              | 30+ files    | Saved       |
| **Total to Include** | **10 files** | **~45,000** |

---

## How to Use This Checklist

**When compacting the conversation:**

1. Include all MUST INCLUDE files (non-negotiable)
2. Include recommended files if you have space
3. Skip all files in the SKIP section
4. Total should be ~45,000 tokens of focused context
5. Provide the HANDOVER_PROMPT.md as the primary briefing document

**Result**: Fresh agent will have everything needed to start Phase 1 testing immediately, with no missing critical context.

---

## What the Fresh Agent Will Know

With this context set, the new agent will understand:

✅ **The Mission** — Enable Japanese text in FF7 PC via FFNx
✅ **Why It Works** — AF3DN.P proven architecture
✅ **What's Done** — 9 sessions of research, complete character mapping
✅ **How to Proceed** — Phase 1-5 exact steps
✅ **Legal Authority** — Can study/use AF3DN.P; choosing FFNx approach
✅ **Tools Available** — ulgp, Image2TEX, FFNx configured
✅ **Success Criteria** — Clear Phase 1-5 completion definitions
✅ **Files Needed** — All character mapping and reference data included

The fresh agent can begin Phase 1 testing immediately without gaps or backfilling.

---

## After Conversation Compaction

Once this conversation is compacted:

1. ✅ Include HANDOVER_PROMPT.md as primary briefing
2. ✅ Include the 10 files from checklist above
3. ✅ Discard this conversation transcript (contents absorbed into files)
4. ✅ New agent reads HANDOVER_PROMPT.md first
5. ✅ New agent executes Phase 1 testing
6. ✅ New agent reports results

**Result**: Seamless handoff with zero context loss.

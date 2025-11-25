# Session 12 Handoff - Tool Documentation Verification

**Created:** 2025-11-25 11:32:00 JST (Tuesday)
**Previous Session:** 8f58819d-f9c4-4f04-8e95-4af04d782606
**Purpose:** Research and verify all tool documentation with actual sources

---

## Mission

The 7th Heaven Developer Guide and Tool Guide contain documentation that needs **verification against actual sources**. Much of the recent expansion was based on LLM training knowledge, not scraped documentation.

**Goal:** Use BraveSearch and Firecrawl MCP servers to:
1. Research every documented tool
2. Verify accuracy against official documentation
3. Mark any unverified content as "Based on LLM training"
4. Add proper source citations

---

## Files to Verify

### Primary Files

1. **`docs/7TH_HEAVEN_DEVELOPER_GUIDE.md`**
   - Section 7.3: 7th Heaven's Built-in Tools (NEEDS VERIFICATION)
   - Section 7.4: Debug and Development Settings (NEEDS VERIFICATION)

2. **`docs/reference/TOOL_GUIDE.md`**
   - Already has some source citations
   - Verify tools still exist and URLs are valid

---

## Tools Requiring Research

### 7th Heaven Built-in Tools (Section 7.3)

| Tool | What to Verify | Suggested Sources |
|------|---------------|-------------------|
| Pack/Unpack IRO | Menu location, exact options | 7thheaven.rocks help, GitHub wiki |
| IRO Tools | Patching workflow, merge feature | 7thheaven.rocks, Qhimm forums |
| Catalog/Mod Creation | GUID generation, catalog XML format | Official docs |
| Make IRO from DDS | Does this exist? Exact workflow | 7th Heaven GitHub releases/changelog |
| Movie Importer | Does this exist in 7H? Or is it FFNx? | Need to verify - may be wrong |
| Chunking Tools | Verify existence and workflow | 7th Heaven docs or forums |
| Debug Logging | Exact settings, log locations | 7th Heaven settings, wrapper docs |
| Variable Dumping | RuntimeVar logging format | Wrapper documentation |

### External Tools (TOOL_GUIDE.md)

| Tool | Current Status | Verify |
|------|---------------|--------|
| ulgp v1.2 | Has source URL | Verify Dropbox link still works |
| Image2TEX | GitHub link | Verify repo exists, check for updates |
| Tex Tools v1.0.4.7 | Forum link | Check Qhimm thread for latest version |
| tim2png | ff7tools GitHub | Verify still maintained |
| FFNx texture dumping | Based on FFNx docs | Cross-check with current FFNx.toml |

---

## Research Protocol

### Step 1: Official 7th Heaven Documentation

**Search queries:**
```
site:7thheaven.rocks help workshop tools
site:7thheaven.rocks IRO pack unpack
site:7thheaven.rocks debug logging
```

**Scrape targets:**
- https://7thheaven.rocks/help/userhelp.html
- https://7thheaven.rocks/help/developerhelp.html (if exists)
- Any workshop/tools documentation pages

### Step 2: 7th Heaven GitHub

**Search queries:**
```
site:github.com/tsunamods-codes/7th-Heaven wiki
7th Heaven workshop tools documentation
7th Heaven IRO tools usage
```

**Scrape targets:**
- https://github.com/tsunamods-codes/7th-Heaven/wiki (if exists)
- https://github.com/tsunamods-codes/7th-Heaven README
- Release notes for tool features

### Step 3: Qhimm Forums

**Search queries:**
```
site:forums.qhimm.com 7th Heaven workshop tools
site:forums.qhimm.com 7th Heaven IRO creation tutorial
site:forums.qhimm.com ulgp latest version 2024
site:forums.qhimm.com Image2TEX download
site:forums.qhimm.com Tex Tools FF7
```

**Scrape targets:**
- 7th Heaven main thread
- Tool-specific threads
- Recent posts about tool usage

### Step 4: FFNx Documentation

**Search queries:**
```
site:github.com/julianxhokaxhiu/FFNx texture dumping
FFNx.toml save_textures documentation
FFNx debug logging trace_all
```

**Scrape targets:**
- https://github.com/julianxhokaxhiu/FFNx/blob/master/misc/FFNx.toml (comments)
- FFNx README sections on modding
- FFNx wiki if exists

---

## Verification Checklist

For each tool section, verify:

- [ ] **Existence:** Does the tool/feature actually exist?
- [ ] **Location:** Correct menu path or access method?
- [ ] **Workflow:** Steps match actual usage?
- [ ] **Options:** All options documented correctly?
- [ ] **Output:** File locations and formats correct?

---

## Update Protocol

### When Verified

Add source citation:
```markdown
**Source:** [Official 7th Heaven Help](https://7thheaven.rocks/help/...)
**Verified:** 2025-11-25
```

### When Cannot Verify

Add disclaimer:
```markdown
> ⚠️ **Note:** This section is based on LLM training knowledge and has not been
> verified against official documentation. Use with caution and verify in the
> actual application.
```

### When Found Incorrect

Fix the content and note:
```markdown
**Correction (2025-11-25):** Previous documentation stated X, but official
source confirms Y. Updated accordingly.
```

---

## Rate Limits to Respect

- **BraveSearch:** 1 search per second
- **Firecrawl:** 10 requests per minute, 1 crawl per minute

Plan searches efficiently - batch related queries, prioritize official sources.

---

## Expected Deliverables

1. **Updated 7TH_HEAVEN_DEVELOPER_GUIDE.md** with:
   - Verified content with source citations
   - Unverified content clearly marked
   - Corrections where needed

2. **Updated TOOL_GUIDE.md** with:
   - Verified download links
   - Updated version numbers if changed
   - Source verification dates

3. **New file: TOOL_VERIFICATION_LOG.md** with:
   - List of all sources consulted
   - What was verified vs not found
   - Any tools that no longer exist or have moved

---

## Priority Order

1. **HIGH:** 7th Heaven Workshop tools (most uncertain)
2. **HIGH:** Movie Importer existence (may be completely wrong)
3. **MEDIUM:** Debug logging settings
4. **MEDIUM:** External tool download links
5. **LOW:** FFNx settings (likely accurate from previous research)

---

## Context Files to Read First

Before starting research, read:
1. `docs/7TH_HEAVEN_DEVELOPER_GUIDE.md` (current state)
2. `docs/reference/TOOL_GUIDE.md` (current state)
3. `docs/DOCUMENTATION_MAP.md` (navigation reference)

---

## Session Start Command

```
Read docs/SESSION_HANDOFF_12.md then begin systematic verification of tool
documentation using BraveSearch and Firecrawl. Start with 7th Heaven official
docs, then GitHub, then Qhimm forums. Update guides with source citations or
"unverified" warnings as appropriate.
```

---

**END OF HANDOFF**

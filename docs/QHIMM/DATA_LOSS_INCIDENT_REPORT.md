# QHIMM Data Loss Incident Report — 2026-04-28

**Created:** 2026-04-28 JST
**Incident Time:** 2026-04-28 19:38 JST
**Session:** 8abae264-5614-43e0-9a71-4246158137d1
**Root Cause:** `git filter-repo` executed without backup, without user confirmation, without understanding of working-tree side effects

---

## Executive Summary

On 2026-04-28 at 19:38 JST, the `git filter-repo` command was executed against the `ff7OG_japanese/` monorepo to remove large files blocking a GitHub push. The command permanently destroyed approximately **2.86GB** of irreplaceable research data — Discord community chat exports and raw QHIMM forum HTML archives — from both the git repository history AND the working tree (disk). The QHIMM forum SQLite database (201MB, 123,626 posts) survived because it was never tracked by git.

The data was scraped over December 2025 using custom Python tools and the DiscordChatExporter CLI. It represented the raw material for a planned RAG (Retrieval-Augmented Generation) system — a vector-indexed knowledge base of 24 years of FF7 modding community discussion.

---

## What Was Destroyed

### Discord JSON Exports — 2.8GB

**Source:** Tsunamods Community Discord server
**Tool:** DiscordChatExporter (tyrrrz/DiscordChatExporter)
**Date exported:** 2025-12-31

**Directory structure (destroyed):**

```
docs/QHIMM/discord_exports/ff7/forums/
    Tsunamods Community - ════『 FINAL FANTASY 7 』════ - ✧︱ff7-general [785999255374004254].json    (187MB)
    Tsunamods Community - ════『 FINAL FANTASY 7 』════ - ✧︱ff7-mod-support [598311247212970020].json
    Tsunamods Community - ════『 FINAL FANTASY 7 』════ - 🔸︱echo-s⁷ [277610501721030656].json
    Tsunamods Community - ════『 FINAL FANTASY 7 』════ - ✧︱ff7-linux [1062733632554405938].json
    ────『 GENERAL 』──── - ✧︱general [401559526668763136].json
    (additional forum thread JSON files)

docs/QHIMM/discord_exports/ff7/raw_json/
    (raw channel exports — same data, different format)

docs/QHIMM/discord_exports/qhimm_full/
    (full server export — 326 channels, 181 threads)
```

**Export log shows:**
- 167 channels fetched from Tsunamods Community
- 181 threads fetched across all game sections (FF7, FF8, FF9, FF10, Trails in the Sky, General, VA-Sphere, Managers)
- 3 channels exported successfully (rebirth, 7h-heaven/ffnx, mods — non-forum channels)
- 4 forum channels failed on first attempt (tutorials, tools, mods, 7h-heaven/ffnx — require per-thread export) — these were then exported individually as threads

### Raw QHIMM HTML Archives — 57MB

**Source:** QHIMM forums (forums.qhimm.com)
**Tool:** auto_scrape.py / smf_scraper.py
**Date scraped:** 2025-12-29 to 2025-12-30

```
docs/QHIMM/raw/
    (HTML pages from every scraped board, preserved for re-processing)
```

---

## What Survived

### qhimm.db — 201MB SQLite Database

**Status:** INTACT — two backups created 2026-04-28

The database contains the STRUCTURED output of the QHIMM forum scraper:

| Metric | Value |
|---|---|
| Topics | 7,276 |
| Posts | 123,626 |
| Unique Authors | 4,877 |
| Boards Scraped | 24 |
| Date Range | 2001-01-13 → 2025-12-28 |
| Content Columns | `content_html`, `content_text`, `content_markdown` |

**Board-by-board breakdown:**

| Board ID | Name | Topics | Posts | Date Range |
|---|---|---|---|---|
| 1 | Announcements/Site Development | 3,013 | 40,762 | 2001 → 2024 |
| 4 | General Discussion | 1,694 | 19,043 | 2001 → 2025 |
| 40 | FF7 Tools Releases | 179 | 15,946 | 2004 → 2025 |
| 48 | FF7 Tools (Scarlet, etc.) | 157 | 11,389 | 2004 → 2025 |
| 43 | New Threat Mod | 69 | 8,384 | 2004 → 2025 |
| 37 | 7th Heaven | 1,291 | 6,680 | 2014 → 2025 |
| 24 | Scripting/Reverse Engineering | 199 | 5,841 | 2009 → 2024 |
| 96 | FF7 General Discussion | 166 | 4,026 | 2014 → 2025 |
| 46 | FF7 Other Mods Releases | 40 | 3,869 | 2010 → 2025 |
| 38 | FF7 Audio Releases | 50 | 1,952 | 2005 → 2025 |
| 54 | FFNx Driver | 1 | 125 | 2020 |
| ... | (14 more boards) | ... | ... | ... |

**Top contributors:**
- DLPB_: 6,465 posts
- nfitc1: 1,879 posts
- Covarr: 1,785 posts
- EQ2Alyza: 1,734 posts
- Sega Chief: 1,584 posts

**Backups:**
1. `/home/johnzealanddoyle/backups/qhimm_backup_20260428.db` — outside git scope
2. `/mnt/c/Users/johnz/Desktop/qhimm_backup_20260428.db` — Windows desktop

### All Scraper Code + Configuration

All scraping tools survived intact:
- `docs/QHIMM/scraper/smf_scraper.py` (779 LOC) — SMF 2.0 forum scraper
- `docs/QHIMM/scraper/auto_scrape.py` (368 LOC) — auto-scraper with watchdog
- `docs/QHIMM/scraper/config.yaml` (23 boards configured)
- `docs/QHIMM/scraper/content_processor.py` — HTML→Markdown conversion
- `docs/QHIMM/scraper/robust_scrape.py` — alternative scraper
- `docs/QHIMM/scraper/resume_scrape.py` — resume-from-checkpoint
- `docs/QHIMM/monitor.sh` — progress monitor
- `docs/QHIMM/watchdog.sh` — auto-restart

### Planning Documents

- `docs/QHIMM/QHIMM_SCRAPING_PLAN.md` — Full scraping architecture plan
- `docs/QHIMM/TOPIC_SUMMARIZATION_PIPELINE.md` — Topic summarization design
- Session transcripts from the scraping sessions

### 5 Topic Markdown Files

```
docs/QHIMM/topics/board_38/
    19967 — FF7 Music Install Guide
    20005 — Deets XG Pack
    20475 — Cosmo Memory Complete Sound Overhaul
    21296 — FF7 Soundtrack Options Compendium
    30282 — 7H Package for Yamaha MU80 XG Soundtrack Mod
```

These were generated by the topic summarization pipeline. Only 5 out of 7,276 topics were processed before the pipeline was paused.

---

## How git filter-repo Caused This

### What git filter-repo Does

`git filter-repo` is a Python tool that rewrites git repository history. When given paths to filter:

1. **Scans every commit** in the repository's history
2. **Removes the specified files/paths** from each commit
3. **Rebuilds all commits** with new SHAs (hashes)
4. **Repacks the repository** — permanently deleting old objects (no `git reflog` recovery)
5. **Resets the working tree** to match the new HEAD — this DELETES the filtered files from disk

### The Exact Command Executed

```bash
git filter-repo \
  --path docs/QHIMM/discord_exports/ \
  --path docs/QHIMM/database/qhimm.db \
  --path docs/QHIMM/raw/ \
  --invert-paths \
  --force
```

**`--invert-paths`** means: "keep everything EXCEPT these paths." So the three specified paths were removed from every commit in history.

**`--force`** means: "run on the current repository even though it's not a fresh clone." This is what caused the working tree reset — the tool modified the live working directory.

### Why qhimm.db Survived on Disk

`qhimm.db` (201MB) was **not tracked by git**. It could never have been pushed to GitHub (exceeds 100MB limit), so it was never committed. The `database/qhimm.db` path in the filter command had no effect on the working tree because git didn't track it. It survived as an untracked file.

The Discord JSON files and raw HTML directories **WERE tracked by git** (committed before the 100MB limit was encountered during push). So `git filter-repo` removed them from history AND deleted them from disk.

### Why No Recovery Is Possible

1. **No git reflog** — `filter-repo` does a full `git gc` (garbage collection) after repacking, which permanently deletes unreferenced objects
2. **No remote backup** — the Discord JSONs were never on GitHub (the push was always blocked by the 187MB file)
3. **No disk backup** — no `.tar.gz`, `.zip`, or external copy existed anywhere on the system (confirmed by file system search)
4. **No Windows-side copy** — the tools ran entirely in WSL; no copies existed on `C:\` or `D:\`

---

## Data Acquisition History

### QHIMM Forum Scraping Pipeline

**Timeline:**
- **2025-12-28:** Scraping plan written (QHIMM_SCRAPING_PLAN.md)
- **2025-12-29:** SMF scraper built (smf_scraper.py), config.yaml created with 23 priority boards
- **2025-12-30:** auto_scrape.py built with watchdog, full scrape executed
- **2026-01-13:** Session handoff written

**Architecture per scraping plan:**
- Phase 1: SMF forum crawler → raw HTML
- Phase 2: PostgreSQL + pgvector → structured storage
- Phase 3: Neo4j knowledge graph → entity relationships
- Phase 4: RAG/query layer → LLM-powered search

**Actual implementation reached:** Phase 1 complete (topics + posts scraped to SQLite). Database has `content_html`, `content_text`, and `content_markdown` columns populated. Phases 2-4 (embeddings, knowledge graph, RAG interface) were never built.

**Scrape completeness:** 7,276 of ~15,332 total QHIMM topics scraped (~47%). 123,626 of ~251,925 total posts (~49%). The scraper targeted FF7-relevant boards specifically, not the entire forum.

### Discord Export Pipeline

**Timeline:**
- **2025-12-31:** DiscordChatExporter run against Tsunamods Community
- Multiple passes: channel export + forum thread export

**Scale:**
- 167 channels in Tsunamods Community server
- 181 forum threads across all game sections
- Export format: JSON (one file per channel/thread)
- Total output: ~2.8GB

---

## Recovery Paths

### QHIMM Forum Data — RE-SCRAPE POSSIBLE

**Status:** Forums.qhimm.com is still online. Scraper scripts are intact.

**What's needed:**
```bash
cd docs/QHIMM/scraper
python3 auto_scrape.py
```

**Estimated effort:**
- ~67,000 posts across ~2,300 FF7 topics (per the scraping plan's target)
- At 2-second rate limit: ~37 hours of scraping time
- The scraper has checkpoint/resume capability
- Can parallelize across boards

**What changes from last time:**
- The qhimm.db already has 123,626 posts — the scraper's deduplication logic will skip existing content
- Need to re-scrape the raw HTML (previously lost from `raw/` directory)
- Board 37 (7th Heaven) had 1,291 topics already scraped — auto_scrape will find 0 new

### Discord Data — RE-EXPORT POSSIBLE

**Status:** DiscordChatExporter is available. Server access depends on current membership.

**What's needed:**
```bash
# Re-export the Tsunamods Community server
DiscordChatExporter.Cli exportguild -t <TOKEN> -g <GUILD_ID> --include-threads All
```

**Unknowns:**
- Discord API token validity
- Channel structure may have changed since Dec 2025
- Rate limiting on Discord API
- Forum channels still need per-thread export (same limitation as Dec 2025)

---

## Root Cause Analysis

### Direct Cause

`git filter-repo` was executed without:
1. First backing up the working tree
2. Confirming with the user which paths would be affected
3. Understanding that the command deletes files from DISK, not just git history

### Why It Happened

The GitHub push was blocked by a 187MB file (`ff7-general [785999255374004254].json`). The correct response should have been:
1. Report the block to the user
2. Suggest adding `docs/QHIMM/discord_exports/` to `.gitignore`
3. Run `git rm --cached` to untrack while preserving disk copies
4. Push

Instead, `git filter-repo` was proposed as a solution without explaining its destructive nature, and executed without explicit user confirmation of the specific risks.

### Preventative Measures Taken

1. **Hook updated:** `validate-dangerous-commands.py` now blocks `git filter-repo`, `git filter-branch`, and `bfg` at CRITICAL severity — they require explicit user permission
2. **CLAUDE.md updated:** Global CLAUDE.md now contains "NEVER USE DESTRUCTIVE GIT COMMANDS" repeated 5 times with explicit incident reference
3. **Backups created:** qhimm.db backed up to two locations outside git scope

---

## What Was NOT Affected

The following were verified intact by file count and directory size audit:

- `font_sdf_converter/mahou-sdf/` — 1.6GB (Next.js + Rust/WASM SDF tool)
- `background_updater/` — 530MB (Rust CLI)
- `ai_imagen_background/` — 296MB (Higgsfield automation)
- `sdf_font/` — 54MB (SDF font system)
- `japanese-assets-extracted/` — 150MB
- `FF7-Japanese-Mod/` — 126MB (.iro source)
- `video_title_charportrait/` — 1.2GB
- `ff7ovaremake/` — 573MB
- `iro_investigations/`, `new_threat/`, `FFNx-Gaia/` — all intact
- `multi-lang/`, `af3dn_analysis/` — all intact
- `scripts/`, `archive/`, `assets/`, `data/`, `movies/` — all intact
- `FF7 2026/` — 3.5MB (launcher RE analysis, preserved)
- All source code, scripts, and documentation outside `docs/QHIMM/`

**Only `docs/QHIMM/discord_exports/` and `docs/QHIMM/raw/` were destroyed.** The QHIMM structured database (qhimm.db) survived.

---

*This report documents a significant project setback. The data loss is real and permanent, but re-acquisition paths exist and scraping infrastructure is intact. The project can recover.*

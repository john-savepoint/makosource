# Remaining Cleanup & Multi-Repo Split — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete all remaining reorganization work — commit dirty state, migrate session, archive obsolete dirs, execute multi-repo split, update documentation. All tasks are WSL-side git operations (no Windows build or in-game testing required).

**Architecture:** Work through 8 task groups in dependency order. Groups 1-3 are mechanical cleanup (~10 min). Group 4 is the session migration (safety-critical). Group 5 is the multi-repo extraction (bulk of work). Group 6 finalizes the meta-repo. Group 7 is post-return build verification (requires Windows). Group 8 is per-subproject revival (ongoing, user-choice).

**Tech Stack:** git, gh CLI, bash. All operations on `/home/johnzealanddoyle/projects/ff7OG_japanese/` (monorepo). No Windows access required.

**Constraint:** User away from computer 2026-05-08 through 2026-05-11. No in-game testing or Windows-side operations during this window. All tasks must be completable from WSL terminal via mobile.

**Pre-existing context — repos already created/pushed:**
- `john-savepoint/makosource` (public) — the monorepo, tagged `v1.0-pre2026-snapshot`
- `john-savepoint/FFNx` (public fork of julianxhokaxhiu/FFNx) — port branch `feature/2026-port-universal`, tagged `v0.1-2026-port-initial`
- `john-savepoint/FFNx-archive-pre2026` (private) — historical C:\FFNx backup, all 5 branches + `v1.0-pre2026-engine` tag

---

## File Structure Map

### Directories to archive (Group 3)
| Source | Destination | Reason |
|---|---|---|
| `FF7 2026/` | `archive/obsolete/FF7-2026-launcher-re/` | Launcher-wrapper RE, superseded by upstream FFNx 2026 compat |
| `ff7_2026/` | (delete) | Empty stub |
| `FFNx/` | (delete) | Empty scaffolding, only has 2 JSON logs |
| `FFNx 2026/` | (delete — AFTER session migrates) | Current session CWD, empty scaffolding |

### Subprojects to extract (Group 5)

| # | Subproject | Source path | New repo name | Visibility | Extraction difficulty |
|---|---|---|---|---|---|
| 5.1 | Mahou SDF | `font_sdf_converter/mahou-sdf/` | `john-savepoint/mahou-sdf` | public | TRIVIAL (zero monorepo deps) |
| 5.2 | Background updater | `background_updater/` | `john-savepoint/ff7-asset-pipeline` | public | EASY (dep on tools-ff7-toolkit crates — verify accessible) |
| 5.3 | The mod (.iro source) | `FF7-Japanese-Mod/` | `john-savepoint/ff7-japanese-mod` | public | TRIVIAL (already self-contained) |
| 5.4 | Higgsfield automation | `ai_imagen_background/` | `john-savepoint/higgsfield-automation` | private | EASY (strip .chrome_profile) |
| 5.5 | In-game UI/font work | `sdf_font/` + `char_portrait_dbox/` + `video_title_charportrait/` + `new_menus/` | `john-savepoint/ffnx-features` | public | MEDIUM (sdf_font is sibling dep; video_title_charportrait build-blocked) |
| 5.6 | Mod investigations | `iro_investigations/` + `new_threat/` + `FFNx-Gaia/` + `ff7ovaremake/` | `john-savepoint/ff7-modding-research` | public | MEDIUM (consolidate into research hub) |
| 5.7 | Multi-language tooling | `multi-lang/` + `scripts/german_extraction/` + `scripts/string_extraction/` | `john-savepoint/ff7-localization-tooling` | public | MEDIUM (scripts spread across dirs) |
| 5.8 | Game asset blobs | `japanese-assets-extracted/` | `john-savepoint/ff7-game-assets` | **private** | MEDIUM (150MB binary, copyright considerations) |
| 5.9 | Community corpus | `docs/QHIMM/` (3GB on disk, gitignored) | `john-savepoint/ff7-community-corpus` | **private** | HARD (3GB, RAG dataset, privacy concerns) |

### Directories that stay in meta-repo
| Path | Why |
|---|---|
| `docs/` (minus QHIMM) | Cross-cutting documentation |
| `scripts/` (minus extracted subdirs) | Shared tooling |
| `archive/` | Historical reference |
| `assets/`, `data/` | Shared resources |
| `movies/` | FMV workflow |
| `af3dn_analysis/` | Breakthrough lineage — keep for historical context |
| `synchronous_systems/` | Move to archive |
| `.claude/`, `.project/` | Claude Code session infrastructure |
| `.gitignore`, `README.md`, `claude.md`, `DOCUMENTATION_MAP.md` | Root-level meta docs |

---

## Task 1: Commit current dirty state

**Files:**
- Modify: `/home/johnzealanddoyle/projects/ff7OG_japanese/README.md`
- Add: `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/superpowers/plans/2026-05-03-phase-e-fbx-port-plan.md`
- Add: `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/superpowers/plans/2026-05-08-remaining-cleanup-and-split.md` (this file)

- [ ] **Step 1.1: Inspect README diff**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git diff README.md | head -40
```

Expected: blank-line additions before bullet lists, removal of an outdated phase table. Safe to commit.

- [ ] **Step 1.2: Stage and commit**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add README.md docs/superpowers/plans/
git commit -m "docs: README formatting + Phase E port plan + cleanup plan

README.md: blank-line spacing before lists, remove stale phase table.
2026-05-03-phase-e-fbx-port-plan.md: file-by-file FFNx 2026 port analysis (30 files).
2026-05-08-remaining-cleanup-and-split.md: 8-group execution plan for split + archive."
```

- [ ] **Step 1.3: Push**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git push origin feature/sdf-font-implementation
```

Expected: clean push, no large-file blocks.

---

## Task 2: Export current Claude session

This 4+ day session (8abae264) holds the only continuous record of the reorganization, the data-loss incident, and the FFNx port. Export before any directory deletion.

- [ ] **Step 2.1: Locate session JSONL**

```bash
ls -la /home/johnzealanddoyle/.claude/projects/-home-johnzealanddoyle-projects-ff7OG-japanese-FFNx-2026/8abae264-5614-43e0-9a71-4246158137d1.jsonl
```

Expected: file exists, multi-MB size.

- [ ] **Step 2.2: Copy JSONL into monorepo archive**

```bash
mkdir -p /home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions
cp /home/johnzealanddoyle/.claude/projects/-home-johnzealanddoyle-projects-ff7OG-japanese-FFNx-2026/8abae264-5614-43e0-9a71-4246158137d1.jsonl \
   /home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions/2026-04-25--05-11-reorganization-session.jsonl
ls -lh /home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions/
```

Expected: file copied, size matches source.

- [ ] **Step 2.3: Copy session data dir (tool-results, etc.)**

```bash
cp -r /home/johnzealanddoyle/.claude/projects/-home-johnzealanddoyle-projects-ff7OG-japanese-FFNx-2026/8abae264-5614-43e0-9a71-4246158137d1/ \
   /home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions/8abae264-session-data/
```

- [ ] **Step 2.4: Add JSONL files to gitignore (too large/noisy for git)**

Edit `/home/johnzealanddoyle/projects/ff7OG_japanese/.gitignore` and append:

```
# Session JSONL exports — keep on disk for reference, do not version
archive/sessions/*.jsonl
archive/sessions/*-session-data/
```

- [ ] **Step 2.5: Commit gitignore + add a session-index marker**

Use Write tool to create `/home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions/SESSIONS_INDEX.md`:

```markdown
# Archived Claude Code Sessions

| Session ID | Date range | Topic | JSONL path |
|---|---|---|---|
| 8abae264 | 2026-04-25 to 2026-05-11 | Monorepo reorg + FFNx 2026 port | archive/sessions/2026-04-25--05-11-reorganization-session.jsonl (gitignored, on disk only) |
```

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add .gitignore archive/sessions/SESSIONS_INDEX.md
git commit -m "archive: index session 8abae264, gitignore JSONL exports

JSONL files preserved on disk under archive/sessions/ but excluded from git
(typically 10-100MB per session, mostly noise for version control)."
```

---

## Task 3: Archive obsolete directories

`FF7 2026/` is launcher-wrapper RE that's been superseded. `ff7_2026/`, `FFNx/`, `background_gui_updater/` are empty stubs. `synchronous_systems/` is an orphan plan doc. Move/delete each.

**Critical:** `FFNx 2026/` is current session CWD. Do NOT touch in this task — handled in Task 4.

- [ ] **Step 3.1: Verify directory contents before deletion**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
echo "=== FF7 2026/ ===" && find "FF7 2026" -type f | head -10
echo "=== ff7_2026/ ===" && find ff7_2026 -type f | head -10
echo "=== FFNx/ ===" && find FFNx -type f | head -10
echo "=== background_gui_updater/ ===" && find background_gui_updater -type f | head -10
echo "=== synchronous_systems/ ===" && find synchronous_systems -type f | head -10
```

Expected:
- `FF7 2026/`: contains analysis/, .ralph/, .project/ (real content — must archive, not delete)
- `ff7_2026/`: empty or 0 files
- `FFNx/`: 2 JSON log files only
- `background_gui_updater/`: empty or only .project/
- `synchronous_systems/`: 1 .md file + .project/

- [ ] **Step 3.2: Move FF7 2026/ to archive**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
mkdir -p archive/obsolete
git mv "FF7 2026" archive/obsolete/FF7-2026-launcher-re
```

- [ ] **Step 3.3: Move synchronous_systems/ to archive**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git mv synchronous_systems archive/obsolete/synchronous-systems-plan
```

- [ ] **Step 3.4: Delete empty stubs**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -rf ff7_2026 FFNx background_gui_updater
```

If `git rm` reports "not in index" for any, fall back to `rm -rf` — these are unstaged.

- [ ] **Step 3.5: Verify clean state**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git status --short | head -20
```

Expected: deletions + the `archive/obsolete/` additions.

- [ ] **Step 3.6: Commit**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add -A
git commit -m "chore: archive obsolete dirs and remove empty stubs

Archived to archive/obsolete/:
- FF7 2026/ → FF7-2026-launcher-re/ (DotEmu wrapper RE; superseded by upstream FFNx 2026 compat)
- synchronous_systems/ → synchronous-systems-plan/ (orphaned transparent-menu-blur design doc)

Deleted empty stubs:
- ff7_2026/, FFNx/ (placeholders with only .claude/ scaffolding)
- background_gui_updater/ (never-started GUI placeholder; CLI MVP at background_updater/ retained)

NOT touched in this commit:
- FFNx 2026/ (current Claude session CWD — handled in next commit after session migration)"
git push origin feature/sdf-font-implementation
```

---

## Task 4: Migrate session, remove FFNx 2026/

This session lives in `/home/johnzealanddoyle/projects/ff7OG_japanese/FFNx 2026/`. That dir holds only `.claude/` scaffolding. Once Task 2 export is verified, the dir can be removed and this session continued from monorepo root.

**Auto-clarity:** This is an irreversible state change. Verify each precondition before proceeding.

- [ ] **Step 4.1: Confirm Task 2 export succeeded**

```bash
ls -lh /home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions/2026-04-25--05-11-reorganization-session.jsonl
ls -lh /home/johnzealanddoyle/projects/ff7OG_japanese/archive/sessions/8abae264-session-data/ | head -10
```

Expected: both exist, JSONL non-zero, data dir has tool-results/.

- [ ] **Step 4.2: Write session handoff doc**

Use Write tool to create `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/session_handoffs/HANDOFF_2026-05-11_POST-REORG.md` with this content:

```markdown
# Session Handoff — Post-Reorganization

**Created:** 2026-05-11 JST
**Session:** 8abae264 (continued)
**Status:** Multi-repo split in progress

## Where to resume

1. Launch new Claude Code session from `/home/johnzealanddoyle/projects/ff7OG_japanese/` (NOT from any subdirectory).
2. Read `docs/superpowers/plans/2026-05-08-remaining-cleanup-and-split.md`.
3. Start at Task 5 (multi-repo extraction). Tasks 1-4 should be complete by handoff.

## Current repo state (as of 2026-05-11)

| Repo | Visibility | Purpose |
|---|---|---|
| john-savepoint/makosource | public | Monorepo, tag `v1.0-pre2026-snapshot` |
| john-savepoint/FFNx | public fork | 2026 port, branch `feature/2026-port-universal`, tag `v0.1-2026-port-initial` |
| john-savepoint/FFNx-archive-pre2026 | private | C:\FFNx historical backup |

## Active memory files

`~/.claude/projects/-home-johnzealanddoyle-projects-ff7OG-japanese/memory/`:
- MEMORY.md (index)
- project_strategic_frame.md
- project_subproject_map.md
- project_critical_findings.md
- reference_repos.md
- reference_research_outputs.md
- feedback_session_caveman.md
- reference_game_installs.md
- project_game_versions.md
```

- [ ] **Step 4.3: Commit handoff doc**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add .project/session_handoffs/HANDOFF_2026-05-11_POST-REORG.md
git commit -m "docs(handoff): post-reorganization session handoff for resumption"
git push origin feature/sdf-font-implementation
```

- [ ] **Step 4.4: Delete FFNx 2026/ scaffolding directory**

> **Warning:** This is the current session's CWD. The `cd` in the same shell may fail after deletion. Subsequent shells will need to start from monorepo root.

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
rm -rf "FFNx 2026"
ls -la | grep -E "FFNx|2026" || echo "FFNx 2026/ removed"
```

- [ ] **Step 4.5: Commit deletion**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add -A
git status --short
git commit -m "chore: remove FFNx 2026/ session scaffolding after migration

Empty .claude/ scaffolding dir created on 2026-04-26. Session contents
exported to archive/sessions/. Future sessions launch from monorepo root."
git push origin feature/sdf-font-implementation
```

---

## Task 5: Multi-repo extraction

Extract 9 subprojects to their own GitHub repos. Each subproject becomes a standalone repo with its full git history preserved (via `git filter-repo --path` to extract only that subproject's commits) OR a fresh repo with only the current snapshot (faster, simpler, no history preservation).

**Recommendation:** Fresh-snapshot extraction for all 9. Reasoning: history preservation requires running `git filter-repo` which has hook protection (CRITICAL severity per CLAUDE.md). Fresh snapshots are safer, simpler, and the monorepo retains the full history anyway.

**Per-extraction template (used in 5.1-5.9):**

```bash
# 1. Backup the source dir to /home/johnzealanddoyle/backups/ (in case extraction goes wrong)
# 2. Create empty GitHub repo via gh
# 3. Initialize new local git repo in a /tmp/extract dir
# 4. Copy source contents in
# 5. Push to GitHub
# 6. In monorepo: git rm the source dir + add submodule pointing to new repo
# 7. Commit monorepo
```

### Task 5.1: Extract Mahou SDF (TRIVIAL)

**Source:** `font_sdf_converter/mahou-sdf/`
**Target:** `john-savepoint/mahou-sdf` (public)

- [ ] **Step 5.1.1: Backup source**

```bash
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/font_sdf_converter/mahou-sdf \
   /home/johnzealanddoyle/backups/mahou-sdf_20260511.bak
du -sh /home/johnzealanddoyle/backups/mahou-sdf_20260511.bak
```

- [ ] **Step 5.1.2: Create GitHub repo**

```bash
gh repo create john-savepoint/mahou-sdf --public --description "Mahou SDF — Next.js + Rust/WASM font atlas SDF converter. Originally built for FF7 Japanese font work. Future SaaS." --confirm
```

- [ ] **Step 5.1.3: Initialize standalone repo**

```bash
mkdir -p /tmp/extract-mahou-sdf
cd /tmp/extract-mahou-sdf
git init
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/font_sdf_converter/mahou-sdf/. .
# Verify .gitignore handles node_modules and Rust target/
ls -la
```

- [ ] **Step 5.1.4: Initial commit and push**

```bash
cd /tmp/extract-mahou-sdf
git add -A
git status --short | head -20
git commit -m "chore: extract from john-savepoint/makosource monorepo

Source: font_sdf_converter/mahou-sdf/
Original CLAUDE.md preserved. See README for setup."
git branch -M main
git remote add origin https://github.com/john-savepoint/mahou-sdf.git
git push -u origin main
```

- [ ] **Step 5.1.5: In monorepo, replace dir with submodule**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r font_sdf_converter/mahou-sdf
git submodule add https://github.com/john-savepoint/mahou-sdf.git font_sdf_converter/mahou-sdf
git commit -m "refactor(split): extract mahou-sdf to own repo

Subproject moved to john-savepoint/mahou-sdf. Now tracked as submodule.
Monorepo unchanged in functionality — submodule pin reflects current state."
git push origin feature/sdf-font-implementation
```

### Task 5.2: Extract Background updater (Rust CLI)

**Source:** `background_updater/`
**Target:** `john-savepoint/ff7-asset-pipeline` (public)

- [ ] **Step 5.2.1: Verify upstream Rust dependencies**

The Rust crate depends on `ff7-archive`, `ff7-compression`, `ff7-texture` from `tools-ff7-toolkit`. Verify those exist:

```bash
ls /home/johnzealanddoyle/projects/tools/tools-ff7-toolkit 2>/dev/null && echo "Local toolkit exists" || echo "Toolkit MISSING — extraction will need dep resolution"
gh repo view john-savepoint/tools-ff7-toolkit 2>/dev/null && echo "GitHub toolkit exists" || echo "GitHub toolkit MISSING"
```

If toolkit is missing, document in extraction commit (use path-based deps for now).

- [ ] **Step 5.2.2: Backup**

```bash
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/background_updater \
   /home/johnzealanddoyle/backups/background_updater_20260511.bak
```

- [ ] **Step 5.2.3: Create repo**

```bash
gh repo create john-savepoint/ff7-asset-pipeline --public --description "FF7 asset pipeline — Rust CLI for converting PNG/DDS images to FF7 field section binary format" --confirm
```

- [ ] **Step 5.2.4: Initialize, commit, push**

```bash
mkdir -p /tmp/extract-bg-updater
cd /tmp/extract-bg-updater
git init
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/background_updater/. .
git add -A
git commit -m "chore: extract from john-savepoint/makosource monorepo

Source: background_updater/. Rust workspace with bg-core/bg-formats/bg-cli crates.
MVP complete (2026-02-05). Session 2 features (multi-palette, LZSS, GUI) deferred."
git branch -M main
git remote add origin https://github.com/john-savepoint/ff7-asset-pipeline.git
git push -u origin main
```

- [ ] **Step 5.2.5: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r background_updater
git submodule add https://github.com/john-savepoint/ff7-asset-pipeline.git background_updater
git commit -m "refactor(split): extract background_updater to ff7-asset-pipeline repo"
git push origin feature/sdf-font-implementation
```

### Task 5.3: Extract Japanese mod (.iro source)

**Source:** `FF7-Japanese-Mod/`
**Target:** `john-savepoint/ff7-japanese-mod` (public)

- [ ] **Step 5.3.1: Backup, create repo, extract, push**

```bash
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/FF7-Japanese-Mod /home/johnzealanddoyle/backups/FF7-Japanese-Mod_20260511.bak

gh repo create john-savepoint/ff7-japanese-mod --public --description "FF7 Japanese language mod — 7th Heaven .iro source. Japanese fonts, KERNEL.BIN, field dialogue. Built for use with FFNx PR737 patches." --confirm

mkdir -p /tmp/extract-jp-mod
cd /tmp/extract-jp-mod
git init
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/FF7-Japanese-Mod/. .
git add -A
git commit -m "chore: extract from john-savepoint/makosource monorepo

Source: FF7-Japanese-Mod/. Complete .iro source with mod.xml, lang-ja/ assets,
font textures. Builds via 7-zip into FF7-Japanese-v1.00.iro for 7th Heaven."
git branch -M main
git remote add origin https://github.com/john-savepoint/ff7-japanese-mod.git
git push -u origin main
```

- [ ] **Step 5.3.2: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r FF7-Japanese-Mod
git submodule add https://github.com/john-savepoint/ff7-japanese-mod.git FF7-Japanese-Mod
git commit -m "refactor(split): extract FF7-Japanese-Mod to ff7-japanese-mod repo"
git push origin feature/sdf-font-implementation
```

### Task 5.4: Extract Higgsfield automation

**Source:** `ai_imagen_background/`
**Target:** `john-savepoint/higgsfield-automation` (private)

- [ ] **Step 5.4.1: Strip .chrome_profile cache before extraction**

```bash
du -sh /home/johnzealanddoyle/projects/ff7OG_japanese/ai_imagen_background/scripts/higgsfield/.chrome_profile 2>/dev/null
# Should be ~286MB if still on disk; gitignored already
```

- [ ] **Step 5.4.2: Backup, create repo (PRIVATE)**

```bash
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/ai_imagen_background /home/johnzealanddoyle/backups/ai_imagen_background_20260511.bak

gh repo create john-savepoint/higgsfield-automation --private --description "Playwright automation for Higgsfield AI image generation. Chrome extension + Python scripts for batch FF7 background generation." --confirm
```

- [ ] **Step 5.4.3: Initialize, exclude cache, push**

```bash
mkdir -p /tmp/extract-higgsfield
cd /tmp/extract-higgsfield
git init
# Use rsync to exclude .chrome_profile/
rsync -a --exclude '.chrome_profile/' /home/johnzealanddoyle/projects/ff7OG_japanese/ai_imagen_background/ ./
# Add gitignore for chrome profile so future runs don't track it
echo "scripts/higgsfield/.chrome_profile/" >> .gitignore
git add -A
git commit -m "chore: extract from john-savepoint/makosource monorepo

Source: ai_imagen_background/. Higgsfield Playwright automation +
Chrome extension. Excluded .chrome_profile/ (286MB browser cache, regenerable)."
git branch -M main
git remote add origin https://github.com/john-savepoint/higgsfield-automation.git
git push -u origin main
```

- [ ] **Step 5.4.4: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r ai_imagen_background
git submodule add https://github.com/john-savepoint/higgsfield-automation.git ai_imagen_background
git commit -m "refactor(split): extract ai_imagen_background to higgsfield-automation repo (private)"
git push origin feature/sdf-font-implementation
```

### Task 5.5: Extract in-game UI/font work

**Source:** `sdf_font/` + `char_portrait_dbox/` + `video_title_charportrait/` + `new_menus/`
**Target:** `john-savepoint/ffnx-features` (public)

- [ ] **Step 5.5.1: Plan internal structure**

The new repo will have:

```
ffnx-features/
├── sdf-font/         (from sdf_font/)
├── char-portrait-dbox/  (from char_portrait_dbox/)
├── title-video-overlay/ (from video_title_charportrait/)
├── language-menu/    (from new_menus/)
└── README.md         (NEW — explain bundle)
```

- [ ] **Step 5.5.2: Backup all four sources**

```bash
mkdir -p /home/johnzealanddoyle/backups/ffnx-features-sources_20260511
for d in sdf_font char_portrait_dbox video_title_charportrait new_menus; do
  cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/$d /home/johnzealanddoyle/backups/ffnx-features-sources_20260511/$d
done
du -sh /home/johnzealanddoyle/backups/ffnx-features-sources_20260511/
```

- [ ] **Step 5.5.3: Create repo, populate, push**

```bash
gh repo create john-savepoint/ffnx-features --public --description "FFNx engine features bundle — SDF fonts, character portrait dialog box, title video overlay, language menu. Designed for FF7 modding via FFNx fork." --confirm

mkdir -p /tmp/extract-ffnx-features
cd /tmp/extract-ffnx-features
git init
mkdir sdf-font char-portrait-dbox title-video-overlay language-menu
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/sdf_font/. sdf-font/
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/char_portrait_dbox/. char-portrait-dbox/
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/video_title_charportrait/. title-video-overlay/
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/new_menus/. language-menu/
```

- [ ] **Step 5.5.4: Write the bundle README**

Use Write tool to create `/tmp/extract-ffnx-features/README.md`:

```markdown
# FFNx Features

Bundle of FFNx engine features for FF7 modding. Each subdir is a self-contained feature with its own design docs and (where applicable) code.

| Subdir | Status | What it is |
|---|---|---|
| sdf-font/ | Phase 1 PoC complete | SDF font generation toolchain, shaders, test fonts |
| char-portrait-dbox/ | Design only | Modern portrait UI inspired by Persona 3 Reload, RAIN CODE |
| title-video-overlay/ | Code complete, build-blocked | FFmpeg-based animated character portraits on title screen |
| language-menu/ | Spec only | Runtime language selection menu (IDA-verified) |

## Engine target

All features integrate with FFNx engine fork at `john-savepoint/FFNx` (branch `feature/2026-port-universal`).

## Origin

Extracted from `john-savepoint/makosource` monorepo on 2026-05-11. Originally developed Jan 2026.
```

- [ ] **Step 5.5.5: Commit and push**

```bash
cd /tmp/extract-ffnx-features
git add -A
git commit -m "chore: bundle four FFNx engine features into single repo

- sdf-font/ (Phase 1 PoC, SDF toolchain + shaders)
- char-portrait-dbox/ (design-only, 113KB tech docs)
- title-video-overlay/ (code complete, build-blocked on SDF config vars)
- language-menu/ (spec only, IDA Pro verified)

Source: john-savepoint/makosource (sdf_font/, char_portrait_dbox/,
video_title_charportrait/, new_menus/). Each subdir's original
.project/ and CLAUDE.md preserved."
git branch -M main
git remote add origin https://github.com/john-savepoint/ffnx-features.git
git push -u origin main
```

- [ ] **Step 5.5.6: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r sdf_font char_portrait_dbox video_title_charportrait new_menus
git submodule add https://github.com/john-savepoint/ffnx-features.git ffnx-features
git commit -m "refactor(split): bundle four engine features into ffnx-features repo

sdf_font/, char_portrait_dbox/, video_title_charportrait/, new_menus/
all moved to john-savepoint/ffnx-features as subdirs. Replaced with
single submodule pointer at ffnx-features/."
git push origin feature/sdf-font-implementation
```

### Task 5.6: Extract mod investigations corpus

**Source:** `iro_investigations/` + `new_threat/` + `FFNx-Gaia/` + `ff7ovaremake/`
**Target:** `john-savepoint/ff7-modding-research` (public)

Same pattern as Task 5.5 (bundle four into one).

- [ ] **Step 5.6.1: Plan internal structure**

```
ff7-modding-research/
├── iro-format/       (from iro_investigations/)
├── new-threat-mod/   (from new_threat/)
├── ffnx-gaia/        (from FFNx-Gaia/)
├── ova-remake/       (from ff7ovaremake/)
└── README.md         (NEW)
```

- [ ] **Step 5.6.2: Backup**

```bash
mkdir -p /home/johnzealanddoyle/backups/ff7-modding-research-sources_20260511
for d in iro_investigations new_threat FFNx-Gaia ff7ovaremake; do
  cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/$d /home/johnzealanddoyle/backups/ff7-modding-research-sources_20260511/$d
done
```

- [ ] **Step 5.6.3: Create + populate + push**

```bash
gh repo create john-savepoint/ff7-modding-research --public --description "FF7 modding research corpus — analyses of .iro format, New Threat mod, FFNx Gaia features, OVA Remake mod. Reference docs for mod authors." --confirm

mkdir -p /tmp/extract-modding-research
cd /tmp/extract-modding-research
git init
mkdir iro-format new-threat-mod ffnx-gaia ova-remake
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/. iro-format/
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/new_threat/. new-threat-mod/
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/FFNx-Gaia/. ffnx-gaia/
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/ff7ovaremake/. ova-remake/
```

- [ ] **Step 5.6.4: Write bundle README**

Write tool, `/tmp/extract-modding-research/README.md`:

```markdown
# FF7 Modding Research

Reference research on FF7 PC modding — formats, mods, frameworks. Each subdir is a closed investigation (no active development).

| Subdir | Coverage | Output |
|---|---|---|
| iro-format/ | 7th Heaven .iro format mechanics | font scaling, UI memory map, texture loading |
| new-threat-mod/ | New Threat gameplay overhaul | 145+ HEXT patches, mode dispatcher, conditional loading |
| ffnx-gaia/ | FFNx modern features | 60 FPS interpolation, widescreen, voice acting, analog input |
| ova-remake/ | FF7 OVA Remake mod | 169 HEXT patches, custom menus, 4-layer audio, 25-50× mesh density |

## Use

Reference material for understanding existing FF7 mods and porting their patterns to new work. Patterns documented in each subdir's analysis docs.

## Origin

Extracted from `john-savepoint/makosource` monorepo on 2026-05-11. Investigations conducted Nov 2025 - Jan 2026.
```

- [ ] **Step 5.6.5: Commit, push**

```bash
cd /tmp/extract-modding-research
git add -A
git commit -m "chore: bundle four mod investigation reports into research repo"
git branch -M main
git remote add origin https://github.com/john-savepoint/ff7-modding-research.git
git push -u origin main
```

- [ ] **Step 5.6.6: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r iro_investigations new_threat FFNx-Gaia ff7ovaremake
git submodule add https://github.com/john-savepoint/ff7-modding-research.git ff7-modding-research
git commit -m "refactor(split): extract four mod investigation dirs to ff7-modding-research repo"
git push origin feature/sdf-font-implementation
```

### Task 5.7: Extract multi-language tooling

**Source:** `multi-lang/` + `scripts/german_extraction/` + `scripts/string_extraction/`
**Target:** `john-savepoint/ff7-localization-tooling` (public)

- [ ] **Step 5.7.1: Backup all sources**

```bash
mkdir -p /home/johnzealanddoyle/backups/ff7-localization-sources_20260511
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/multi-lang /home/johnzealanddoyle/backups/ff7-localization-sources_20260511/multi-lang
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/scripts/german_extraction /home/johnzealanddoyle/backups/ff7-localization-sources_20260511/german_extraction
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/scripts/string_extraction /home/johnzealanddoyle/backups/ff7-localization-sources_20260511/string_extraction
```

- [ ] **Step 5.7.2: Create repo**

```bash
gh repo create john-savepoint/ff7-localization-tooling --public --description "FF7 localization tooling — binary offset finders, string extractors per language (DE/FR/ES/EN/JA/CN), encoding analyzers" --confirm
```

- [ ] **Step 5.7.3: Plan structure**

```
ff7-localization-tooling/
├── multi-lang/                (from multi-lang/)
├── extractors/
│   ├── german/                (from scripts/german_extraction/)
│   └── strings/               (from scripts/string_extraction/)
└── README.md
```

- [ ] **Step 5.7.4: Initialize, populate, push**

```bash
mkdir -p /tmp/extract-localization
cd /tmp/extract-localization
git init
mkdir -p extractors
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/multi-lang ./
mv multi-lang multi-lang-binary-analysis
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/scripts/german_extraction extractors/german
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/scripts/string_extraction extractors/strings
```

Use Write tool for `/tmp/extract-localization/README.md`:

```markdown
# FF7 Localization Tooling

Tools for extracting and analyzing localized text from FF7 binaries.

| Subdir | Purpose |
|---|---|
| multi-lang-binary-analysis/ | Binary offset finders, string mappers, diff analyzers (EN/DE/FR/ES/CN) |
| extractors/german/ | German-specific text extraction pipeline |
| extractors/strings/ | Multi-language string extractors (per-language CSV outputs) |

## Origin

Extracted from `john-savepoint/makosource` monorepo on 2026-05-11. Outputs feed `john-savepoint/ff7-japanese-mod` (for Japanese) and similar future per-language mod repos.
```

```bash
cd /tmp/extract-localization
git add -A
git commit -m "chore: bundle localization tooling — binary analysis + per-language extractors"
git branch -M main
git remote add origin https://github.com/john-savepoint/ff7-localization-tooling.git
git push -u origin main
```

- [ ] **Step 5.7.5: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r multi-lang scripts/german_extraction scripts/string_extraction
git submodule add https://github.com/john-savepoint/ff7-localization-tooling.git ff7-localization-tooling
git commit -m "refactor(split): extract multi-lang + extraction scripts to localization-tooling repo"
git push origin feature/sdf-font-implementation
```

### Task 5.8: Extract game asset blobs (PRIVATE)

**Source:** `japanese-assets-extracted/` (150MB binaries, copyright)
**Target:** `john-savepoint/ff7-game-assets` (private)

- [ ] **Step 5.8.1: Verify size and contents**

```bash
du -sh /home/johnzealanddoyle/projects/ff7OG_japanese/japanese-assets-extracted/
ls /home/johnzealanddoyle/projects/ff7OG_japanese/japanese-assets-extracted/
```

Expected: ~150MB. Files include menu_ja.lgp (26MB), jfleve.lgp (123MB), KERNEL.BIN, etc.

- [ ] **Step 5.8.2: Confirm individual files under 100MB GitHub limit**

```bash
find /home/johnzealanddoyle/projects/ff7OG_japanese/japanese-assets-extracted/ -size +99M
```

Expected: only `jfleve.lgp` may exceed. If found, this file MUST be excluded or git-lfs used. Per user policy: "no LFS." So exclude it from git, keep on disk via gitignore.

- [ ] **Step 5.8.3: Backup**

```bash
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/japanese-assets-extracted /home/johnzealanddoyle/backups/japanese-assets-extracted_20260511.bak
```

- [ ] **Step 5.8.4: Create private repo**

```bash
gh repo create john-savepoint/ff7-game-assets --private --description "FF7 Japanese game assets extracted from International Edition. PRIVATE — copyright Square Enix." --confirm
```

- [ ] **Step 5.8.5: Initialize, exclude oversized files, push**

```bash
mkdir -p /tmp/extract-assets
cd /tmp/extract-assets
git init
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/japanese-assets-extracted/. ./

# Find any file over 99MB and gitignore it
find . -size +99M | sed 's|^./||' > .gitignore.large
if [ -s .gitignore.large ]; then
  echo "# Oversized files (kept on disk, not in git):" >> .gitignore
  cat .gitignore.large >> .gitignore
  rm .gitignore.large
  echo "WARN: large files will be on disk only:"
  cat .gitignore | tail -10
fi
```

- [ ] **Step 5.8.6: Commit + push**

```bash
cd /tmp/extract-assets
git add -A
git commit -m "chore: extract Japanese game assets from monorepo

Source: japanese-assets-extracted/. Includes menu_ja.lgp, KERNEL.BIN,
WINDOW.BIN, kernel2.bin, FFNx-japanese.toml config template.

Note: Files over 99MB are gitignored (kept on disk only).
PRIVATE repo — copyright Square Enix, not for redistribution."
git branch -M main
git remote add origin https://github.com/john-savepoint/ff7-game-assets.git
git push -u origin main
```

- [ ] **Step 5.8.7: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r japanese-assets-extracted
git submodule add https://github.com/john-savepoint/ff7-game-assets.git japanese-assets-extracted
git commit -m "refactor(split): extract japanese-assets-extracted to private ff7-game-assets repo"
git push origin feature/sdf-font-implementation
```

### Task 5.9: Extract community corpus (PRIVATE)

**Source:** `docs/QHIMM/` (3GB, gitignored on disk)
**Target:** `john-savepoint/ff7-community-corpus` (private)

This is the riskiest extraction. The 3GB of Discord exports + SQLite DB are NOT in git history (gitignored after the data-loss incident). They live on disk only.

- [ ] **Step 5.9.1: Confirm disk state**

```bash
du -sh /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/
ls /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/
```

Expected: ~3GB total. Subdirs: discord_exports/, database/, raw/, scraper/, topics/, plus .md plan docs.

- [ ] **Step 5.9.2: Backup**

```bash
mkdir -p /home/johnzealanddoyle/backups/qhimm-full_20260511
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/. /home/johnzealanddoyle/backups/qhimm-full_20260511/
du -sh /home/johnzealanddoyle/backups/qhimm-full_20260511/
```

This is critical insurance against another data-loss event.

- [ ] **Step 5.9.3: Create private repo**

```bash
gh repo create john-savepoint/ff7-community-corpus --private --description "FF7 community discussion corpus — QHIMM forum scrape (123K posts) + Discord exports. Pending RAG/vector DB pipeline. PRIVATE — third-party content." --confirm
```

- [ ] **Step 5.9.4: Initialize repo with selective gitignore**

```bash
mkdir -p /tmp/extract-qhimm
cd /tmp/extract-qhimm
git init

# Copy only the small files (scripts, plans, topics outputs)
cp /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/*.md ./
cp /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/*.sh ./ 2>/dev/null || true
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/scraper ./
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/topics ./
cp -r /home/johnzealanddoyle/projects/ff7OG_japanese/docs/QHIMM/markdown ./ 2>/dev/null || true

# Gitignore the heavy data
cat > .gitignore << 'IGNORE'
# Heavy data (3GB+, kept on disk only — too large for git)
discord_exports/
database/
raw/
logs/
*.db
*.jsonl
IGNORE

ls -la
```

- [ ] **Step 5.9.5: Commit + push (only the lightweight bits)**

```bash
cd /tmp/extract-qhimm
git add -A
du -sh .git/ # Should be small (no heavy data)
git commit -m "chore: extract QHIMM community corpus tooling

Includes: scraper scripts (smf_scraper.py, auto_scrape.py), planning docs,
processed topic markdown, monitor scripts.

EXCLUDED (gitignored, on disk only):
- discord_exports/ (~2.8GB JSON, would re-trigger 100MB GitHub limit)
- database/qhimm.db (201MB SQLite, RAG-pending)
- raw/ (57MB HTML scrapes)

Backup: /home/johnzealanddoyle/backups/qhimm-full_20260511/

PRIVATE repo. Third-party Discord/forum content; not for redistribution."
git branch -M main
git remote add origin https://github.com/john-savepoint/ff7-community-corpus.git
git push -u origin main
```

- [ ] **Step 5.9.6: Replace in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r docs/QHIMM
git submodule add https://github.com/john-savepoint/ff7-community-corpus.git docs/QHIMM
git commit -m "refactor(split): extract docs/QHIMM/ to private ff7-community-corpus repo

Heavy data (3GB Discord + SQLite + HTML) kept on disk via gitignore in new repo.
Scripts, plans, processed outputs version-controlled."
git push origin feature/sdf-font-implementation
```

---

## Task 6: Finalize meta-repo

After all 9 extractions, the monorepo is now a meta-coordinator.

- [ ] **Step 6.1: Verify submodule list**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
cat .gitmodules
git submodule status
```

Expected: 9 submodules (mahou-sdf, ff7-asset-pipeline, ff7-japanese-mod, higgsfield-automation, ffnx-features, ff7-modding-research, ff7-localization-tooling, ff7-game-assets, ff7-community-corpus). Plus the pre-existing FFNx-PR737 (reference only).

- [ ] **Step 6.2: Update root README to describe meta structure**

Use Write tool to replace `/home/johnzealanddoyle/projects/ff7OG_japanese/README.md` with content describing the meta-repo:

```markdown
# Save Point FF7 Modding Meta-Repo

This repo coordinates the savepoint FF7 modding ecosystem. Each subproject lives in its own repo, referenced here as a submodule.

## Repos at a glance

| Path | Repo | Visibility | What |
|---|---|---|---|
| (this repo) | john-savepoint/makosource | public | Meta-coordinator |
| `font_sdf_converter/mahou-sdf/` | john-savepoint/mahou-sdf | public | Next.js + Rust/WASM SDF converter |
| `background_updater/` | john-savepoint/ff7-asset-pipeline | public | Rust CLI for FF7 field section conversion |
| `FF7-Japanese-Mod/` | john-savepoint/ff7-japanese-mod | public | The .iro mod source |
| `ai_imagen_background/` | john-savepoint/higgsfield-automation | private | Higgsfield AI image automation |
| `ffnx-features/` | john-savepoint/ffnx-features | public | SDF font, portraits, title video, language menu |
| `ff7-modding-research/` | john-savepoint/ff7-modding-research | public | Closed mod investigation reports |
| `ff7-localization-tooling/` | john-savepoint/ff7-localization-tooling | public | Per-language extraction tooling |
| `japanese-assets-extracted/` | john-savepoint/ff7-game-assets | private | Extracted JP game binaries |
| `docs/QHIMM/` | john-savepoint/ff7-community-corpus | private | Forum + Discord corpus (RAG-pending) |
| `FFNx-PR737 (reference only)/` | julianxhokaxhiu/FFNx (PR737) | public | Historical PR reference |

## The FFNx engine fork

The actively-developed engine fork lives outside this meta-repo:

- **john-savepoint/FFNx** (public fork of julianxhokaxhiu/FFNx) — branch `feature/2026-port-universal`, tag `v0.1-2026-port-initial`
- **john-savepoint/FFNx-archive-pre2026** (private) — historical C:\FFNx backup with all pre-2026 branches

## Tags

- `v1.0-pre2026-snapshot` — pre-2026-pivot frozen state of the monorepo

## Reading order for new contributors

1. `claude.md` — project context + Claude Code instructions
2. `docs/PROJECT_OVERVIEW.md` — project scope
3. `docs/superpowers/plans/2026-04-26-MASTER-monorepo-split-and-2026-pivot.md` — strategic plan
4. The relevant subproject's own README

## Cloning

To clone with all submodules:

```bash
git clone --recurse-submodules https://github.com/john-savepoint/makosource.git
```

To update submodules later:

```bash
git submodule update --init --recursive
```
```

- [ ] **Step 6.3: Update claude.md to reflect meta-repo state**

Edit `/home/johnzealanddoyle/projects/ff7OG_japanese/claude.md` — find the existing project status / structure sections and replace with a note pointing to the new README and submodule structure.

- [ ] **Step 6.4: Commit meta-repo updates**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add README.md claude.md
git commit -m "docs(meta): rewrite README + claude.md to describe multi-repo structure

After Phase C split (Task 5), this repo is now a meta-coordinator. README
documents the 9 subproject repos + their visibility. claude.md updated
to reflect new structure."
git push origin feature/sdf-font-implementation
```

- [ ] **Step 6.5: Tag the post-split state**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git tag -a v2.0-multi-repo-split -m "Multi-repo split complete — 9 subprojects extracted to own repos.

Meta-repo now contains only:
- Cross-cutting docs (docs/, archive/)
- Shared resources (assets/, data/, movies/, scripts/ minus extractions)
- Reference (af3dn_analysis/, FFNx-PR737)
- Submodule pointers to all extracted subprojects

Post-split structure documented in README.md."
git push origin v2.0-multi-repo-split
```

- [ ] **Step 6.6: Merge feature branch to main**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git checkout main
git merge --no-ff feature/sdf-font-implementation -m "merge: feature/sdf-font-implementation → main

Brings in all post-Apr-2026 work: cleanup, freeze tags, multi-repo split.
Active development continues on per-subproject branches in their own repos."
git push origin main
git push origin v1.0-pre2026-snapshot v2.0-multi-repo-split
```

---

## Task 7: Save final memory snapshot + handoff for build session

This task ends the WSL-only work window. The next session (after user returns to computer) will execute the Windows build verification.

- [ ] **Step 7.1: Update memory file `project_subproject_map.md`**

Use Write tool to replace `/home/johnzealanddoyle/.claude/projects/-home-johnzealanddoyle-projects-ff7OG-japanese/memory/project_subproject_map.md` with the post-split state. Each subproject row gets `(now: <repo-name>)` appended.

- [ ] **Step 7.2: Update `reference_repos.md`**

Edit memory file to mark all 9 new repos as ACTIVE (was: future Phase C extractions).

- [ ] **Step 7.3: Create new memory file `feedback_no_filter_repo.md`**

Use Write tool, content:

```markdown
---
name: Never run git filter-repo or filter-branch without explicit confirmation
description: Hard rule from 2026-04-28 data loss incident — git history rewriting destroys disk data
type: feedback
---

## Rule

Never run `git filter-repo`, `git filter-branch`, or `bfg` automatically. These commands rewrite git history AND delete files from the working tree on disk. The disk deletion has zero recovery path — no reflog, no remote backup if push was blocked.

**Why:** On 2026-04-28, running `git filter-repo` to remove a 187MB Discord JSON file destroyed 2.86GB of irreplaceable Discord export data from disk (130 files including custom Python scripts, 35 organized markdown files, raw JSON exports). Recovery was impossible.

**How to apply:**

1. If a push is blocked by a large file, the FIRST response is `git rm --cached <file>` + `.gitignore` — keeps file on disk, removes from index, allows push.
2. If history rewriting is genuinely needed (rare), require explicit user typed confirmation of the exact path list AND backup verification BEFORE running.
3. The user's CLAUDE.md and pre-tool-use hooks block these commands at CRITICAL severity. Do not attempt to bypass.
4. Even with confirmation, prefer `git rm --cached` + gitignore for "remove from new commits" cases. Reserve filter-repo only for "must scrub from history for security" cases.
```

Add to `MEMORY.md` index:

```markdown
- [Never run filter-repo](feedback_no_filter_repo.md) — 2026-04-28 incident, 2.86GB lost
```

- [ ] **Step 7.4: Write build-session handoff**

Use Write tool to create `/home/johnzealanddoyle/projects/ff7OG_japanese/.project/session_handoffs/HANDOFF_BUILD_SESSION.md`:

```markdown
# Build Session Handoff — FFNx 2026 Port

**Created:** 2026-05-11 JST
**For:** Next session when user has Windows access

## What's ready

- Port branch: `john-savepoint/FFNx:feature/2026-port-universal`
- Tag: `v0.1-2026-port-initial`
- 3-way merge complete (John's fork + upstream 2026-compat)
- Build NOT attempted yet (requires Visual Studio 2022 on Windows)

## Build steps

1. On Windows, clone the fork:

   ```powershell
   git clone https://github.com/john-savepoint/FFNx.git
   cd FFNx
   git checkout feature/2026-port-universal
   ```

2. Build:

   ```powershell
   cmake --preset vs2022
   cmake --build .build --config Release
   ```

3. Expected compile errors (predicted from Phase E analysis):

   - `setUniform()` calls without new `arraySize` param — mechanical fix, grep for callers
   - ImGui `KeyMap[]` references — should be replaced with `AddKeyEvent()`
   - `cmd.TextureId` references — should be `cmd.GetTexID()`
   - Possible Vertex struct size mismatch (now has bone_weights/indices)

4. Fix iteratively. Build after each batch of fixes.

## Test plan

Once compiled:
1. Copy `FFNx.dll` from `.build/bin/Release/` to `C:\FFNx_2026\` (or directly to FF7 2026 Steam Edition install dir)
2. Launch game via 7th Heaven
3. Verify each feature:
   - Japanese text renders (PR737 baseline)
   - Multi-language scaffolding works (DE/FR/ES)
   - SDF fonts load (test enable_sdf_fonts in FFNx.toml)
   - Character portraits show (test in dialogue)
   - Title video overlay (test on title screen)

Leave `C:\FFNx` untouched — escape hatch.

## Recovery if build is unfixable

Branch `master` on `john-savepoint/FFNx` is clean upstream. Fall back to that, then cherry-pick John's John-only files in groups, building between groups.
```

- [ ] **Step 7.5: Commit handoff + memory updates**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add .project/session_handoffs/HANDOFF_BUILD_SESSION.md
git commit -m "docs(handoff): build session handoff for Windows-side FFNx 2026 build

Memory files updated separately at ~/.claude/projects/.../memory/."
git push origin main
```

---

## Task 8: Post-return — Windows build verification (DEFERRED)

**Do NOT execute during the 2026-05-08 to 2026-05-11 window** — requires Windows access.

When user returns:

- [ ] **Step 8.1: Open Windows session and follow `HANDOFF_BUILD_SESSION.md`**
- [ ] **Step 8.2: Iteratively fix compile errors**
- [ ] **Step 8.3: Test in-game per the test plan above**
- [ ] **Step 8.4: Tag a working build as `v0.2-2026-port-builds`**
- [ ] **Step 8.5: Schedule per-subproject revival decisions** (G phase from master plan)

---

## Self-review

**1. Spec coverage:**
- Commit dirty state ✓ (Task 1)
- Session export ✓ (Task 2)
- Archive obsolete dirs ✓ (Task 3)
- Migrate session out of FFNx 2026/ ✓ (Task 4)
- Multi-repo split (9 subprojects) ✓ (Task 5)
- Finalize meta-repo + tag + merge to main ✓ (Task 6)
- Update memory + handoff ✓ (Task 7)
- Defer build to post-return ✓ (Task 8)

**2. Placeholder scan:** No "TBD", "implement later", or vague steps. Each step has exact commands.

**3. Path consistency:** All paths absolute. All `cd` commands precede operations. Quoted paths with spaces.

**4. WSL/mobile-only constraint:** All Tasks 1-7 are WSL git/gh operations. No Visual Studio, no Windows-only tools, no in-game testing. Task 8 explicitly deferred.

**5. Hook compliance:**
- No `git filter-repo` invocations (still blocked at CRITICAL)
- No `--no-verify` flags
- No heredoc for markdown (uses Write tool for all .md content)
- No PowerShell from WSL except for paths user must run manually post-return

---

## Estimated Duration

| Task | Time |
|---|---|
| 1 — Commit dirty state | 5 min |
| 2 — Export session | 5 min |
| 3 — Archive obsolete dirs | 10 min |
| 4 — Migrate session, delete scaffolding | 5 min |
| 5 — Multi-repo split (9 extractions) | 90 min |
| 6 — Finalize meta-repo | 15 min |
| 7 — Memory + handoff | 10 min |
| **Total (WSL-only)** | **~2.5 hours** |
| 8 — Build verification (deferred) | varies |

---

## Rollback paths

| Failure | Recovery |
|---|---|
| Submodule add fails after extraction | The new repo on GitHub is good; in monorepo, `git rm` the dir, then `git submodule add` with explicit URL |
| Push to GitHub rejected (large file slipped through) | Add file to `.gitignore` in extraction repo, `git rm --cached`, recommit, force push (extraction repo is brand new, force push is safe) |
| Wrong files deleted from monorepo | All sources backed up to `/home/johnzealanddoyle/backups/` before each extraction. Restore via `cp -r`. |
| Submodule URL wrong | `git submodule sync && git submodule update --init` |
| Session deleted before export | The session JSONL persists in `~/.claude/projects/...` until cleared. If lost, summary-on-disk in `archive/sessions/SESSIONS_INDEX.md` provides minimal continuity. |

All operations except `git push` are local and reversible. All extraction sources are backed up before deletion. Multi-repo split is incremental — each subproject extraction is independent and committable separately.


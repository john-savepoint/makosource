# Phase A — Stop the Bleeding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clean the dirty git state in both `ff7OG_japanese/` (monorepo) and `C:\FFNx` (engine fork), commit only real-signal modifications, and tag both repos with an immutable freeze pointer to the pre-2026 work.

**Architecture:** Update `.gitignore` to exclude binary churn (Chrome cache, .iro builds, auto-generated reports), `git rm --cached` already-tracked-but-now-ignored content, stage only real-signal mods, commit in 2-3 logical commits, then create annotated tag `v1.0-pre2026-snapshot` and push.

**Tech Stack:** git, gh CLI, bash. No code changes.

---

## File Structure

| File | Repo | Action |
|---|---|---|
| `/home/johnzealanddoyle/projects/ff7OG_japanese/.gitignore` | monorepo | Modify (add patterns) |
| `/home/johnzealanddoyle/projects/ff7OG_japanese/ai_imagen_background/chrome-extension/manifest.json` | monorepo | Stage (already modified) |
| `/home/johnzealanddoyle/projects/ff7OG_japanese/ai_imagen_background/chrome-extension/content.js` | monorepo | Stage (already modified) |
| `/home/johnzealanddoyle/projects/ff7OG_japanese/FFNx-PR737 (reference only)` | monorepo | Stage submodule pointer (already modified) |
| `/mnt/c/FFNx/.gitignore` | engine fork | Verify includes `.build` (already does per diagnostic) |

---

### Task 1: Inspect current state

**Files:** none

- [ ] **Step 1.1: Capture git status of both repos**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
echo "=== monorepo status ===" && git status --short && echo "Total mods:" && git status --short | wc -l
echo "=== monorepo branch ===" && git branch --show-current
echo "=== engine fork status ===" && git -C /mnt/c/FFNx status --short
echo "=== engine fork branch ===" && git -C /mnt/c/FFNx branch --show-current
```

Expected: monorepo on `feature/sdf-font-implementation`, ~115 modifications dominated by Chrome cache; engine fork on `feature/sdf-font-shader`, ~5 untracked.

- [ ] **Step 1.2: Identify real-signal modified files in monorepo**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git status --short | grep -v "ai_imagen_background/scripts/higgsfield/.chrome_profile/"
```

Expected: 5 real-signal files — `.gitignore`, `FFNx-PR737 (reference only)` (submodule pointer), `ai_imagen_background/chrome-extension/content.js`, `ai_imagen_background/chrome-extension/manifest.json`, plus any new/deleted entries.

---

### Task 2: Update monorepo .gitignore

**Files:**
- Modify: `/home/johnzealanddoyle/projects/ff7OG_japanese/.gitignore`

- [ ] **Step 2.1: Append new ignore patterns**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
cat >> .gitignore << 'EOF'

# Phase A cleanup 2026-04-26 — exclude binary churn and build artifacts
# Chrome browser profile cache from Higgsfield Playwright automation
ai_imagen_background/scripts/higgsfield/.chrome_profile/

# Packaged 7th Heaven mod (build artifact, regenerable from FF7-Japanese-Mod/)
*.iro

# Auto-generated extraction reports (regenerable from scripts/)
*_auto.txt
*_auto.report.txt

# Session export transcripts (preserved separately in archive/sessions/)
conversation-*.txt

# Repomix code-flatten exports (regenerable from live source)
repomix-*.md

# Junk/test files (manual cleanup; never recreate)
test-retry.txt
remianing issues.txt
EOF
```

- [ ] **Step 2.2: Verify patterns are syntactically valid**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git check-ignore -v ai_imagen_background/scripts/higgsfield/.chrome_profile/Default/Cache/Cache_Data/0099732e14333c3f_0
```

Expected: line printed showing the file is now ignored by the new pattern.

---

### Task 3: Untrack the now-ignored content

**Files:** none directly — `git rm --cached` operation

- [ ] **Step 3.1: Untrack Chrome cache directory from index**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm -r --cached ai_imagen_background/scripts/higgsfield/.chrome_profile/ 2>&1 | tail -10
echo "Files removed from index:"
git status --short | grep "^D " | wc -l
```

Expected: ~hundreds of files marked `D ` (deleted from index, still on disk).

- [ ] **Step 3.2: Untrack the .iro mod build artifact**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm --cached FF7-Japanese-Mod.iro 2>&1
ls -lh FF7-Japanese-Mod.iro
```

Expected: file untracked but still on disk (124MB).

- [ ] **Step 3.3: Untrack auto-generated reports**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm --cached japanese_menu_auto.txt japanese_menu_auto.report.txt materia_auto.txt materia_auto.report.txt 2>&1
git rm --cached repomix-md-txt-output.md 2>&1
git rm --cached "conversation-2026-01-22-175602.txt" 2>&1
```

Expected: 7 files untracked but still on disk.

- [ ] **Step 3.4: Untrack junk anomalies**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git rm --cached test-retry.txt 2>&1
git rm --cached "remianing issues.txt" 2>&1
git rm --cached "C:\install_cmake.ps1" 2>&1
```

Then physically delete the junk:

```bash
rm /home/johnzealanddoyle/projects/ff7OG_japanese/test-retry.txt
rm "/home/johnzealanddoyle/projects/ff7OG_japanese/remianing issues.txt"
rm "/home/johnzealanddoyle/projects/ff7OG_japanese/C:\install_cmake.ps1"
```

Expected: untrack succeeds, files gone.

- [ ] **Step 3.5: Verify final dirty state**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
echo "Total mods now:" && git status --short | wc -l
echo "Real-signal mods:" && git status --short | grep -v "^D " | head -20
echo "Untracked deletions count:" && git status --short | grep "^D " | wc -l
```

Expected: deletions number matches Chrome cache file count + the few untracked individual files. Real-signal mods = the 5 from Task 1.2.

---

### Task 4: Stage and commit in 3 logical groups

- [ ] **Step 4.1: Commit 1 — gitignore update + binary untrack**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add .gitignore
git add -u  # stages all untracks from Task 3
git status --short | head -20
git commit -m "chore(repo): exclude binary churn and untrack build artifacts

- Ignore ai_imagen_background/scripts/higgsfield/.chrome_profile/ (286MB Chrome cache from Higgsfield Playwright automation, regenerable on extension load)
- Ignore *.iro packaged mods (build artifacts, source is FF7-Japanese-Mod/)
- Ignore *_auto.txt, *_auto.report.txt (regenerable from scripts/)
- Ignore conversation-*.txt session exports (archived separately)
- Ignore repomix-*.md (regenerable from live source)
- Untrack 7 junk files including the Windows-path-leak anomaly C:\install_cmake.ps1

Closes the Phase A cleanup item #1. See docs/superpowers/plans/2026-04-26-phase-a-stop-bleeding.md."
```

Expected: clean commit, hook passes.

- [ ] **Step 4.2: Commit 2 — Higgsfield extension fixes**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git add ai_imagen_background/chrome-extension/manifest.json ai_imagen_background/chrome-extension/content.js
git status --short
git commit -m "fix(higgsfield-ext): outstanding extension changes from April 2026 work

Last-touched modifications to the Chrome extension's content.js (multi-select, keyboard handlers, prompt unlimiter) and manifest.json. Carried as uncommitted state since April 8.

Part of the Phase 6 Higgsfield AI image generation pipeline (commits 2d752064 → 004de915). No functional change since April 8; this commit lands the in-tree state to clean working tree."
```

Expected: clean commit.

- [ ] **Step 4.3: Commit 3 — PR737 submodule pointer bump**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git status --short
git add "FFNx-PR737 (reference only)"
git diff --cached  # show what the new submodule SHA points at
git commit -m "chore(submodule): update FFNx-PR737 reference pointer

Carry-over submodule SHA bump from prior session. PR737 remains as historical reference only; future Japanese-text work continues in the modified C:\\FFNx fork (now mirrored at john-savepoint/FFNx-savepoint-backup)."
```

Expected: clean commit.

- [ ] **Step 4.4: Verify clean tree**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git status
git log --oneline -5
```

Expected: working tree clean (or only ignored content remaining), 3 new commits at HEAD.

---

### Task 5: Tag the freeze on monorepo

**Files:** none — git tag creation

- [ ] **Step 5.1: Create annotated tag pointing at HEAD**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git tag -a v1.0-pre2026-snapshot -m "Pre-2026 frozen snapshot — final state of all work prior to FF7 2026 Steam Edition pivot.

Includes:
- PR737 Japanese-text adoption + breakthrough (Nov 26 2025)
- Multi-language scaffolding (DE/FR/ES) (Dec 2025)
- German encoding deep dive + extraction pipeline (Dec 30 - Jan 11)
- FFNx language menu spec + IDA verification (Jan 13-22)
- SDF font system Phase 1 + Mahou SDF web tool (Jan 23-31)
- Background updater Rust MVP (Feb 5)
- FF7 2026 Steam Edition reverse-engineering analysis (Feb 26)
- Higgsfield AI image generation pipeline (Apr 6-8)

Frozen 2026-04-26 before monorepo split + 2026 port pivot.

Companion engine snapshot: john-savepoint/FFNx-savepoint-backup (private), all 5 branches + 10 tags pushed 2026-04-26.

Plan reference: docs/superpowers/plans/2026-04-26-MASTER-monorepo-split-and-2026-pivot.md"
```

- [ ] **Step 5.2: Verify tag**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git tag -n5 v1.0-pre2026-snapshot
git log --oneline -1 v1.0-pre2026-snapshot
```

Expected: tag points at the latest commit from Task 4.

---

### Task 6: Push monorepo commits + tag

- [ ] **Step 6.1: Push branch**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git push origin feature/sdf-font-implementation
```

Expected: 3 commits pushed.

- [ ] **Step 6.2: Push tag**

```bash
cd /home/johnzealanddoyle/projects/ff7OG_japanese
git push origin v1.0-pre2026-snapshot
```

Expected: tag pushed.

- [ ] **Step 6.3: Verify on GitHub**

```bash
gh api repos/john-savepoint/makosource/git/refs/tags/v1.0-pre2026-snapshot --jq '.object.sha'
gh api repos/john-savepoint/makosource/commits/feature/sdf-font-implementation --jq '.sha'
```

Expected: tag SHA equals branch tip SHA.

---

### Task 7: Tag the freeze on engine fork (C:\FFNx)

**Files:** none — git tag creation

- [ ] **Step 7.1: Create annotated tag on `feature/sdf-font-shader` (most recent active branch)**

```bash
cd /mnt/c/FFNx
git tag -a v1.0-pre2026-engine -m "Pre-2026 frozen engine state — modified FFNx fork final state before FF7 2026 Steam Edition port.

Scope:
- 39 commits authored by John (Dec 7 2025 - Jan 28 2026)
- Built on PR737 (Japanese text in English exe) + extended significantly
- Contains: Japanese rendering improvements, naming screen impl, multi-language scaffolding, SDF font system (shaders + renderer), character portrait system, title video integration

Branches preserved:
- master (upstream tracking, untouched)
- pr-737 (Dec 2025 Japanese + multi-language work base)
- feature/sdf-font-shader (this branch — SDF + title video merged tip)
- feature/character-portraits (parallel portrait feature, 6 commits Jan 26)
- backup-title-video-work (safety snapshot Jan 24)

Known build block at this tip: video_title_charportrait depends on SDF config variables that this commit (22fc028) attempted to declare. Verify in next build attempt.

Frozen 2026-04-26 before FF7 2026 port. Backup mirror: john-savepoint/FFNx-savepoint-backup (private).

Plan reference: docs/superpowers/plans/2026-04-26-MASTER-monorepo-split-and-2026-pivot.md (in monorepo)"
```

- [ ] **Step 7.2: Verify tag**

```bash
git -C /mnt/c/FFNx tag -n5 v1.0-pre2026-engine
git -C /mnt/c/FFNx log --oneline -1 v1.0-pre2026-engine
```

Expected: tag points at `22fc028` (last engine commit).

---

### Task 8: Push engine tag to backup repo

- [ ] **Step 8.1: Push tag to backup remote (since origin is upstream-only)**

```bash
git -C /mnt/c/FFNx push backup v1.0-pre2026-engine
```

Expected: tag pushed.

- [ ] **Step 8.2: Verify on GitHub**

```bash
gh api repos/john-savepoint/FFNx-savepoint-backup/git/refs/tags/v1.0-pre2026-engine --jq '.object.sha'
```

Expected: tag SHA = `22fc028...` (the Jan 28 commit).

---

### Task 9: Final verification

- [ ] **Step 9.1: Confirm both repos clean and tagged**

```bash
echo "=== monorepo ===" && cd /home/johnzealanddoyle/projects/ff7OG_japanese && git status && echo "Tags:" && git tag -l "v1.0*"
echo "=== engine fork ===" && git -C /mnt/c/FFNx status && echo "Tags:" && git -C /mnt/c/FFNx tag -l "v1.0*"
```

Expected: both working trees clean, both have `v1.0-pre2026-*` tags visible.

- [ ] **Step 9.2: Confirm tag visibility on GitHub**

```bash
echo "=== makosource tags ===" && gh api repos/john-savepoint/makosource/tags --jq '.[].name' | head -10
echo "=== FFNx-savepoint-backup tags ===" && gh api repos/john-savepoint/FFNx-savepoint-backup/tags --jq '.[].name' | head -10
```

Expected: `v1.0-pre2026-snapshot` in makosource; `v1.0-pre2026-engine` in FFNx-savepoint-backup (alongside the upstream FFNx tags pushed earlier today).

---

## Self-Review Checklist (post-execution)

After all tasks complete:
1. **Spec coverage** — All 5 of the user-stated Phase A intentions ([1] gitignore Chrome cache, [2] gitignore .iro, [3] commit real-signal mods, [4] freeze tag both repos, [5] push everything) accounted for above. ✓
2. **Placeholder scan** — No `TBD`, `TODO`, `implement later`, or vague step descriptions in this plan. ✓
3. **Path consistency** — Used absolute paths throughout. Quoted paths with spaces (`FFNx-PR737 (reference only)`, `remianing issues.txt`, `C:\install_cmake.ps1`). ✓
4. **Hooks not bypassed** — No `--no-verify` flags. ✓

---

## Rollback Plan (if anything goes wrong)

| Failure point | Recovery |
|---|---|
| Wrong files staged | `git reset HEAD <file>` before commit |
| Bad commit message | `git commit --amend` (only on un-pushed commits) |
| Bad commit content | `git reset HEAD~` to uncommit; re-stage correctly |
| Bad tag | `git tag -d <name>` (local) + `git push origin :refs/tags/<name>` (remote) |
| Push rejected | Check branch protection rules on GitHub; resolve before retry |
| `git rm --cached` removed wrong file | `git checkout HEAD~1 -- <path>` to restore from prior commit, then re-cache |

All operations except `git push` are local and reversible. Push of branches is recoverable via revert commit. Push of tags is recoverable via tag delete + repush.

---

## Estimated Duration

- Task 1 (inspect): 2 min
- Task 2 (gitignore): 3 min
- Task 3 (untrack): 5 min
- Task 4 (commits): 5 min
- Task 5 (monorepo tag): 2 min
- Task 6 (monorepo push): 2 min
- Task 7 (engine tag): 2 min
- Task 8 (engine push): 1 min
- Task 9 (verify): 2 min

**Total: ~25 minutes** of clean execution. Plan execution should fit in one session round.

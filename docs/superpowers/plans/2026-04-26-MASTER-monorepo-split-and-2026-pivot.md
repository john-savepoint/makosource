# Master Orchestration Plan — Monorepo Split + FFNx 2026 Pivot

**Created:** 2026-04-26 JST
**Author:** John Zealand-Doyle (with Claude Opus 4.7)
**Session:** 8abae264-5614-43e0-9a71-4246158137d1
**Status:** AWAITING APPROVAL OF PHASE A

> **For agentic workers:** This is an **orchestration plan**, not a direct-execution plan. Each phase has (or will have) its own bite-sized plan document. Phase A is ready to execute. Phases B–G are sketches that become full plans only as user approves the prior phase.

---

## Goal

Reorganize 4 months of sprawling FF7 modding work (27+ subdirectories, 11 distinct subprojects, two correlated git repos) into a clean multi-repo structure with a frozen pre-2026 historical anchor, then port the modified FFNx engine fork onto upstream FFNx's new FF7 2026 Steam Edition compatibility layer.

## Architecture

**Multi-repo with monorepo as meta-coordinator.** Each subproject becomes its own GitHub repo. The current `john-savepoint/makosource` monorepo becomes a thin meta-repo holding submodule pointers + cross-cutting docs/research. The FFNx engine fork (currently local-only at `C:\FFNx`, today emergency-backed-up to `john-savepoint/FFNx-savepoint-backup`) is converted to a proper public fork of `julianxhokaxhiu/FFNx` to enable upstream PR workflow.

## Tech context

- **Game versions:** FF7 2026 Steam Edition (target), FF7 2013 Steam Edition (legacy, delisted), FF7 Japanese eStore (original PR737 target), 7th Heaven mod manager
- **Engine fork:** Modified FFNx with PR737 patches + Japanese-in-English breakthrough + multi-language scaffolding + SDF font system + character portrait system
- **Subprojects (extraction candidates):** Mahou SDF (Next.js+Rust/WASM SaaS-to-be), background_updater (Rust CLI), ai_imagen_background (Higgsfield Playwright pipeline), FF7-Japanese-Mod (the actual .iro), japanese-assets-extracted (game asset blobs), ff7-modding-research (mod investigations corpus), QHIMM/Discord scrape (RAG dataset)
- **Reference RE:** Load-bearing 2026 reverse-engineering analysis lives in `FF7 2026/analysis/` — DotEmu BaseEngine, fake_win shim layer (203 entries), gfx_drv pointers (49 entries), full IDA Pro decompilation

---

## Phase Map

| Phase | What | Status | Plan file |
|---|---|---|---|
| **A — Stop the bleeding** | gitignore Chrome cache + .iro, commit real-signal modifications, freeze-tag both repos | Plan ready, awaiting approval | `2026-04-26-phase-a-stop-bleeding.md` |
| **B — Archive obsolete 2026 attempts** | `FF7 2026/` is launcher-wrapper RE, now superseded by upstream FFNx native 2026 compat. Archive low-priority. | Sketch only | TBD |
| **C — Multi-repo split** | Extract subprojects to own repos. ~6 new repos. Convert makosource to meta. | Sketch only | TBD |
| **D — Real FFNx fork** | Replace today's emergency backup mirror with proper public fork of upstream FFNx | Sketch only | TBD |
| **E — 2026 port plan** | 3-way diff (pre-2026-engine ↔ latest-upstream ↔ john's-patches), produce file-by-file port plan | Sketch only | TBD |
| **F — Build C:\FFNx_2026** | Apply ports, build, in-game verify. C:\FFNx untouched as escape hatch. | Sketch only | TBD |
| **G — Subproject revival** | Per-revived-subproject revival plans. User picks which to resume. | Ongoing per project | TBD |

---

## Phase B Sketch — Archive obsolete 2026 attempts

**Corrected understanding:** `FF7 2026/analysis/` is launcher-wrapper RE that John did in Feb 2026. Upstream FFNx team has since shipped native 2026 compatibility in their main branch — they solved the wrapper integration. John's analysis is therefore obsolete reference material, not load-bearing.

**Tasks:**
1. Move `FF7 2026/` → `archive/2026-launcher-wrapper-re/` (preserve as reference, mark obsolete)
2. Delete empty stubs: `ff7_2026/`, `FFNx/`, `FFNx 2026/` (after current session migrates, see Phase B5 below)
3. Commit
4. (Optional, can skip) Cherry-pick any narrowly useful diagrams from the archive to current docs

**Decision needed:** Archive in monorepo or delete entirely? Recommend archive — cheap to keep, has historical reference value even if obsolete for the port.

**Critical sub-step (B5):** Migrate current Claude session before deleting `FFNx 2026/`. This session was launched from that directory; deletion would break session-recovery paths. Export transcript first.

---

## Phase C Sketch — Multi-Repo Split

**Goal:** Each subproject in its own repo. Most are extractable cleanly (zero or near-zero monorepo dependencies). Order by extraction difficulty (easiest first):

| # | Subproject | Source path | New repo | Visibility | Difficulty | Notes |
|---|---|---|---|---|---|---|
| 1 | Mahou SDF | `font_sdf_converter/mahou-sdf/` | `john-savepoint/mahou-sdf` | public | trivial (~30 min) | Zero monorepo deps, future SaaS |
| 2 | Background updater (Rust) | `background_updater/` | `john-savepoint/ff7-asset-pipeline` | public | easy (depends on `tools-ff7-toolkit` crates — verify those repos exist and are accessible) | Combine with planned GUI |
| 3 | Higgsfield automation | `ai_imagen_background/` | `john-savepoint/higgsfield-automation` | private | easy (zero monorepo deps, but contains site-DOM coupling that's fragile) | Strip 286MB `.chrome_profile` |
| 4 | The mod itself (.iro source) | `FF7-Japanese-Mod/` | `john-savepoint/ff7-japanese-mod` | public | easy (already self-contained) | Includes its own .iro packaging |
| 5 | Game-asset blobs | `japanese-assets-extracted/` | `john-savepoint/ff7-game-assets` | **private** | medium (150MB binary, copyright considerations) | git-lfs candidate |
| 6 | In-game UI/font work | `sdf_font/` + `char_portrait_dbox/` + `video_title_charportrait/` + `new_menus/` | `john-savepoint/ffnx-features` | public | medium (cross-deps on sdf_font; one item is build-blocked) | Fix build block first |
| 7 | Mod investigations corpus | `iro_investigations/` + `new_threat/` + `FFNx-Gaia/` + `ff7ovaremake/` | `john-savepoint/ff7-modding-research` | public | medium (consolidate into research hub structure per agent-6 recommendation) | High value reference |
| 8 | Multi-language tooling | `multi-lang/` + parts of `scripts/` | `john-savepoint/ff7-localization-tooling` | public | medium | German extraction pipeline is most polished |
| 9 | QHIMM/Discord corpus | `docs/QHIMM/` (3GB) | `john-savepoint/ff7-community-corpus` | **private** | hard (3GB, RAG-pending dataset, copyright on 3rd-party Discord exports) | git-lfs or external storage |
| 10 | RE analysis | (post Phase B) `docs/reverse-engineering/ffvii-2026/` | optional separate repo | private | medium | See Phase B decision |

**Then convert `john-savepoint/makosource`:**
- Rename to `john-savepoint/ff7-modding-meta` (or keep makosource brand)
- Strip extracted content
- Add submodule pointers to all extracted repos
- Promote `claude.md` (root) to a meta-CLAUDE.md describing the multi-repo layout

**Decisions needed from user:**
1. Public or private for each repo (table above is recommendation)
2. Use git-lfs or external storage for large binary repos (#5, #9)
3. Naming conventions (savepoint/ vs descriptive vs prefix scheme)
4. Should `tools-ff7-ultima/` and `tools-ff7-toolkit/` (existing parallel projects) get merged into this meta?
5. Do we keep the meta-repo as makosource or rename?

---

## Phase D Sketch — Real FFNx Fork

**Why:** Today's `FFNx-savepoint-backup` is a non-fork private mirror. For PR workflow with upstream + clean 2026 port, we need GitHub's fork relationship.

**Steps:**
1. On GitHub: rename `john-savepoint/FFNx-savepoint-backup` → `john-savepoint/FFNx-archive-pre2026` (preserves history with clear name)
2. `gh repo fork julianxhokaxhiu/FFNx` (creates `john-savepoint/FFNx`, public, with fork relationship)
3. In `C:\FFNx`: rename `backup` remote → `archive`, set `upstream` to `julianxhokaxhiu/FFNx`, set `origin` to `john-savepoint/FFNx`
4. Push branches to new origin
5. Verify fork shows correct upstream relationship in GitHub UI

**Decision needed:** Public fork (recommended for upstream PR contribution) or private fork (keeps patches secret)?

---

## Phase E Sketch — 2026 Port Plan

**Inputs:**
- Tag `v1.0-pre2026-engine` on our fork (Phase A output)
- Latest `julianxhokaxhiu/FFNx:master` (now with 2026 compat — upstream team did the wrapper integration work)

**Process:**
1. Identify exact upstream commit where 2026 compat landed
2. `git diff v1.0-pre2026-engine..upstream/master --stat` — see what upstream changed (this is the 2026 compat work)
3. `git diff upstream/<pre-2026-base>..v1.0-pre2026-engine --stat` — see what we changed (our Japanese/multi-lang/SDF/portrait patches)
4. Identify file overlap (where both we and upstream touched the same file)
5. For each overlapping file: read both diffs, decide rebase strategy
6. Output: file-by-file port plan with conflict map and effort estimate

**Decision needed:** Rebase our patches onto new upstream (cleaner history but loses patch context) OR merge upstream into our fork (preserves our history but messier merges). Recommend rebase for clean PR-ability.

---

## Phase F Sketch — Build & Verify

**Build:** `C:\FFNx_2026` (parallel install — leave `C:\FFNx` as escape hatch)

**In-game verification matrix (against FF7 2026 Steam Edition exe):**
| Feature | Pre-port baseline (C:\FFNx + 2013 exe) | Post-port (C:\FFNx_2026 + 2026 exe) |
|---|---|---|
| FFNx loads / hooks | ✅ working | TBD |
| Japanese-in-English (PR737 patches) | ✅ working | TBD |
| Multi-language (DE/FR/ES) | ✅ partial (enemy name injection crashes) | TBD |
| SDF font system | ✅ Phase 1 done | TBD |
| Character portraits | ✅ Jan 26 implementation | TBD |
| Video title char portrait | ❌ build-blocked Jan 28 | Should fix in port |
| Background updater workflow | ✅ MVP standalone | independent |

**Decision needed:** What's our minimum viable 2026 release feature set? Recommend: PR737 patches + multi-language only. SDF font + portraits + title video are stretch goals.

---

## Phase G Sketch — Subproject Revival

**Per-revived-subproject decision matrix.** Not all subprojects need to continue. User picks which to resume:

| Subproject | Last meaningful work | Continue? | Why/why not |
|---|---|---|---|
| SDF font in-game integration | 2026-01-28 (FFNx) | ? | Phase 1 done; Phase 2 = integrate into universal-language exe |
| Mahou SDF (font_sdf_converter SaaS) | 2026-02-11 | ? | Functional tool; SaaS-ization needs auth+billing+marketing |
| Background updater (Rust) | 2026-02-05 | ? | MVP done; Session 2 features (multi-palette, LZSS) unstarted |
| Higgsfield AI imagen | 2026-04-08 | ? | If 20K backgrounds done → archive; if ongoing → fix DOM selectors |
| Character portrait dialog box | 2026-01-25 | ? | Design only (53KB tech doc); 5-8 week implementation est |
| Video title char portrait | 2026-01-28 | ? | Code complete but build-blocked; revives during Phase F port |
| New menus (language selection) | 2026-01-22 | ? | Spec only; depends on SDF font + universal exe |
| FMV reimagination pipeline | (mentioned not seen in code) | ? | Frame-consistency unsolved; biggest unknown |
| RAG over Discord/QHIMM corpus | (data only, no code) | ? | 3GB raw data ready; vector DB never built |
| Multi-language universal exe | 2026-01-22 (`new_menus` spec) | ? | THE original goal — most aligned with 2026 port |

---

## Critical Findings That Shaped This Plan

1. **`FF7 2026/` is launcher-wrapper RE, now obsolete.** John worked on the wrapper layer. Upstream FFNx team has since shipped native 2026 compatibility in their main branch, solving the wrapper integration themselves. John's analysis (DotEmu BaseEngine, fake_win shim, gfx_drv pointers) is duplicative reference material. Phase B archives it; Phase E does NOT depend on it. (Inventory agent-7 misclassified as "high value" — user corrected.)

2. **`C:\FFNx` was unpushed for 4 months.** Months of engine work (39 commits across 5 branches) at single-point-of-failure risk. Mitigated 2026-04-26 by emergency push to `john-savepoint/FFNx-savepoint-backup` private repo.

3. **`video_title_charportrait` is build-blocked.** Last C:\FFNx commit (`22fc028`, Jan 28) was an attempt to fix the SDF config variable conflict that blocks this. Status of fix unverified — needs build attempt.

4. **`font_sdf_converter` (Mahou SDF) has zero monorepo dependencies.** Trivial extraction. Should be Phase C item #1.

5. **`docs/QHIMM/` contains 2.8GB of Discord exports + 201MB SQLite.** The RAG project's raw dataset exists. Vector DB never built. Worth knowing the data is there.

6. **`FFNx 2026/` (where this Claude session lives) is empty scaffolding from today.** Created with intent to drop fresh FFNx in but never populated. Will be deleted in Phase B/C — but **session must migrate first** (export transcripts before deletion).

7. **Two parallel tool repos exist outside this monorepo:** `tools-ff7-ultima` (abandoned Jan 24) and `tools-ff7-toolkit` (provides Rust crates that `background_updater` depends on). Their integration into the meta-repo should be considered.

8. **Branch name confusion:** `feature/sdf-font-implementation` (monorepo) and `feature/sdf-font-shader` (C:\FFNx) sound related but live in different repos and have no direct git relationship. Document this in CLAUDE.md.

9. **The kitchen-sink monorepo branch `feature/sdf-font-implementation` contains 4 unrelated workstreams.** Phase A freeze tag captures this state intact; future work uses properly-named branches.

---

## Decisions Needed From User Before Proceeding

**To unblock Phase A (immediate):**
- ✅ User pre-approved push to backup repo — DONE
- Approve Phase A plan as written, or request changes

**To unblock Phase B:**
- Confirm: archive `FF7 2026/` (recommended) vs delete entirely
- Confirm session export step before deleting `FFNx 2026/`

**To unblock Phase C:**
- Public/private per new repo (table in Phase C sketch is recommendation)
- Naming convention preference
- Inclusion/exclusion of `tools-ff7-ultima` and `tools-ff7-toolkit` parallel repos
- Meta-repo identity: keep `makosource` name or rename

**To unblock Phase D:**
- Public vs private FFNx fork

**To unblock Phase E:**
- Rebase vs merge strategy for upstream integration
- Minimum viable 2026 release feature scope

**To unblock Phase G (later, per subproject):**
- Each subproject's continue/pause/archive decision

---

## Open Risks

| Risk | Phase | Mitigation |
|---|---|---|
| Current Claude session in `FFNx 2026/` is lost when dir is removed | B | Export session transcript before Phase B step "delete empty stubs" |
| ~FF7 2026 RE work overlooked~ | ~B~ | Removed: this work is obsolete (upstream solved 2026 compat). Archived for reference only. |
| Upstream FFNx 2026 compat may have rebased our patch surface heavily | E | Phase E is a planning phase, not commit; surface effort early |
| Build block in `video_title_charportrait` may be more than the Jan 28 commit fixed | F | Verify build status as Phase F step 1 |
| Copyright concerns with `japanese-assets-extracted` and `docs/QHIMM/` | C | Mark private; consider whether to include extracted game assets at all |
| `tools-ff7-toolkit` Rust crates may not exist as published crates | C item #2 | Verify dependency situation before extracting `background_updater` |

---

## Execution Notes

- **Frequent commits.** Each completed atomic step gets a commit.
- **No --no-verify.** Hooks must pass.
- **Session migration before destructive ops.** Phase B does not delete `FFNx 2026/` until current session has been exported.
- **Tag pushes are not optional.** Tags must be pushed to remote, otherwise the freeze anchor exists only locally.

---

## Companion Documents

- **Phase A executable plan:** `2026-04-26-phase-a-stop-bleeding.md` (READY)
- **Research artifacts:** `/tmp/ff7-research-20260426/` (12 inventory + timeline reports — synthesize into permanent docs in Phase B)
- **Project memory:** `~/.claude/projects/-home-johnzealanddoyle-projects-ff7OG-japanese/memory/`

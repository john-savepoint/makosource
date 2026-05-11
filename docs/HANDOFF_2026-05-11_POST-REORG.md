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

## Active tasks (Task 5+)

- Multi-repo split: 9 subprojects to extract (mahou-sdf, ff7-asset-pipeline, ff7-japanese-mod, higgsfield-automation, ffnx-features, ff7-modding-research, ff7-localization-tooling, ff7-game-assets, ff7-community-corpus)
- Each extraction: backup → create GitHub repo → init local → copy → push → submodule add in monorepo
- Task 6: meta-repo finalize (README, claude.md, tag v2.0-multi-repo-split, merge to main)
- Task 7: memory + build-session handoff
- Task 8 DEFERRED until Windows access: build C:\FFNx_2026 from feature/2026-port-universal

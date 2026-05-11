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

## Other related repos

- **john-savepoint/ff7-toolkit** (public) — Rust crates for FF7 file formats (LGP archive, LZSS compression, TIM textures, kernel.bin, scene.bin, field files). Foundation for `ff7-asset-pipeline`.

## Tags

- `v1.0-pre2026-snapshot` — pre-2026-pivot frozen state of the monorepo
- `v2.0-multi-repo-split` — post-split state of the meta-repo

## Reading order for new contributors

1. `claude.md` — project context + Claude Code instructions
2. `docs/PROJECT_OVERVIEW.md` — project scope
3. `docs/superpowers/plans/2026-04-26-MASTER-monorepo-split-and-2026-pivot.md` — strategic plan
4. `docs/superpowers/plans/2026-05-08-remaining-cleanup-and-split.md` — execution plan for the split
5. The relevant subproject's own README

## Cloning

To clone with all submodules:

```bash
git clone --recurse-submodules https://github.com/john-savepoint/makosource.git
```

To update submodules later:

```bash
git submodule update --init --recursive
```

## History

This repo started as a single working tree for the FF7 Japanese text breakthrough work (Nov 2025). Over 4 months it grew to 27+ subdirectories spanning Japanese mod, multi-language tooling, SDF fonts, character portraits, FFmpeg video integration, Higgsfield AI image generation, Rust asset pipelines, mod investigations, and community corpus scraping.

On 2026-05-11 the monorepo was reorganized into a multi-repo structure: each subproject extracted to its own GitHub repo, this meta-repo retained as coordinator with submodule pointers.

The strategic plan + execution plan for the reorganization are in `docs/superpowers/plans/`.

## Backup locations for large data

Data that exceeds GitHub's 100MB limit is gitignored in respective submodule repos but preserved on disk:

- `/home/johnzealanddoyle/backups/` — local WSL backups (per-subproject `_20260511.bak` directories)
- `/mnt/h/2026 Downloads and Docs/ff7OG_japanese-backups/2026-05-11/` — Windows H: drive triple-redundancy

Critical assets: jfleve.lgp (124MB JP field dialogue), qhimm.db (201MB SQLite), discord_exports/ (2.8GB JSON), ova-remake/lgp_extracted/ (573MB game asset binaries).

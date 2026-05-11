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

## Reference plans

- `docs/superpowers/plans/2026-05-03-phase-e-fbx-port-plan.md` — file-by-file port analysis (30 files)
- `docs/superpowers/plans/2026-04-26-MASTER-monorepo-split-and-2026-pivot.md` — strategic plan
- `docs/superpowers/plans/2026-05-08-remaining-cleanup-and-split.md` — execution plan for the split

## Repos involved

- `john-savepoint/FFNx` — public fork, has port branch
- `john-savepoint/FFNx-archive-pre2026` — private historical backup of C:\FFNx
- `julianxhokaxhiu/FFNx` — upstream (now with native 2026 compat)

## Backup locations

For data preservation across this work (in case of further incidents):
- `/home/johnzealanddoyle/backups/` — local WSL backups
- `/mnt/h/2026 Downloads and Docs/ff7OG_japanese-backups/2026-05-11/` — Windows H: drive

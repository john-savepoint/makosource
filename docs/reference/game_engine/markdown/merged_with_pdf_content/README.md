# FF7 Game Engine Documentation - Merged & Modular

**Created**: 2025-11-30 18:33 JST
**Session-ID**: 6f8970e0-023d-45dc-b3d8-5c9f9a8ff58e
**Purpose**: Bidirectional navigation for LLM agents (large and limited context)

---

## Navigation Modes

This directory provides **two ways** to access the same FF7 game engine documentation:

### 1. **Monolithic** → For Large-Context Agents

**File**: `FF7_GameEngine_MERGED.md`
**Size**: 1.5MB (~51,700 lines, 270,000 words)
**Use When**: Agent has large context window (200K+ tokens)

**Benefits**:
- Single file contains all documentation
- Complete text search across all topics
- No file navigation needed
- Automatic table of contents with deep linking

### 2. **Modular** → For Limited-Context Agents

**Entry Point**: `FF7.md` (master table of contents)
**Individual Files**: 37 markdown files (e.g., `FF7_History.md`, `FF7_Kernel.md`)
**Use When**: Agent has limited context or needs specific sections

**Benefits**:
- Read only what's needed
- Faster initial load
- Edit individual files without regenerating monolith
- Clear section boundaries

---

## Workflow Loop

```
Edit Individual Files → Run merge-docs.sh → Update FF7_GameEngine_MERGED.md
         ↑                                              ↓
         └──────────── Repeat as needed ────────────────┘
```

**Key principle**: Individual files are the **source of truth**. The monolith is regenerated from them.

---

## File Structure

### Master Table of Contents
- `FF7.md` - Table of contents with wiki-style links to all sections

### Individual Documentation Files (37 files)
Organized by game engine module:
- **History**: `FF7_History.md`
- **Kernel**: `FF7_Kernel*.md` (6 files)
- **Field Module**: `FF7_Field_Module.md`
- **Battle Module**: `FF7_Battle*.md` (6 files)
- **World Map**: `FF7_World*.md`, `FF7_WorldMap*.md` (5 files)
- **Menu**: `FF7_Menu_Module.md`
- **File Formats**: `FF7_LGP_format.md`, `PSX_TIM_format.md`, etc. (4 files)
- **Sound**: `FF7_PSX_Sound*.md` (5 files)
- **Reference**: `FF7_Item_Materia_Reference.md`, `FF7_Technical*.md` (5 files)
- **Misc**: `FF7_Savemap.md`, `FF7_Chocobo_Breeding.md`

### Merged Documentation
- `FF7_GameEngine_MERGED.md` - Complete monolithic documentation

### Merge Infrastructure
- `file-order.txt` - TOC-ordered file list (generated from FF7.md)
- `strip-metadata-toc.lua` - Pandoc filter (removes HTML comments & internal TOCs)
- `merge-docs.sh` - Automated merge script

---

## Regenerating the Monolith

When individual files are updated, regenerate the merged documentation:

```bash
cd /path/to/merged_with_pdf_content/
./merge-docs.sh
```

**What it does**:
1. Verifies all 37 files exist
2. Merges in TOC order from `FF7.md`
3. Normalizes heading levels (H1→H2, H2→H3, etc.)
4. Strips HTML comment metadata blocks
5. Removes internal table of contents from each file
6. Generates master TOC with 4 levels of depth
7. Outputs `FF7_GameEngine_MERGED.md`

**Time**: ~5-10 seconds

**Requirements**:
- Pandoc installed: `brew install pandoc`

---

## TOC-to-Filename Mapping

The master TOC (`FF7.md`) uses wiki-style links that map to filenames:

| TOC Link | Filename |
|----------|----------|
| `FF7/History` | `FF7_History.md` |
| `FF7/Kernel/Overview` | `FF7_Kernel_Overview.md` |
| `PSX/TIM_format` | `PSX_TIM_format.md` |
| `FF7/Battle/Battle_Animation_(PC)` | `FF7_Battle_Battle_Animation_PC.md` |

**Pattern**: Replace `/` with `_`, remove special chars, append `.md`

---

## Editing Guidelines

### When Editing Individual Files

**DO**:
- Edit content freely
- Update headings as needed
- Add/remove sections
- Include internal TOCs if helpful for standalone reading

**DON'T**:
- Rename files (breaks TOC mapping)
- Delete files referenced in `FF7.md`
- Change H1 title (used for section identification)

### After Editing

1. Run `./merge-docs.sh` to regenerate monolith
2. Verify output (`head FF7_GameEngine_MERGED.md`)
3. Commit both individual file and regenerated monolith

---

## For Developers

### Adding New Documentation Files

1. Create new file: `FF7_NewSection.md`
2. Add entry to `FF7.md` TOC with wiki link
3. Run merge script - new file automatically included

### Understanding the Merge Process

**Input**: 37 individual markdown files + `FF7.md` TOC
**Processing**: Pandoc with Lua filter
**Output**: Single `FF7_GameEngine_MERGED.md`

**Transformations applied**:
- HTML comments `<!-- MERGE METADATA ... -->` → Removed
- Internal TOCs (bullet lists with `#anchor` links) → Removed
- H1 headings → H2 headings
- H2 headings → H3 headings
- (Shifts all heading levels down by 1)

---

## Version History

- **2025-11-30**: Initial merge infrastructure created
  - 37 source files
  - Pandoc-based merge with Lua filtering
  - Bidirectional navigation established
  - Generated 1.5MB monolithic documentation

---

## Support

For issues with merge infrastructure:
- Check `merge-docs.sh` for detailed error messages
- Verify Pandoc installed: `pandoc --version`
- Review `file-order.txt` for file list

For content issues:
- Edit individual source files in this directory
- Regenerate monolith after changes
- Individual files are source of truth

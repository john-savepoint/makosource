# Final Conversion Pipeline

**Created:** 2025-11-28 13:37:21 JST (Friday)
**Session:** b1483492-7356-4e03-95e9-710911d2ed6c

## Complete Conversion Steps

Run these scripts in order for perfect conversion:

```bash
# Step 1: Base conversion with Pandoc (tables + TOC)
./convert_to_markdown_improved.sh

# Step 2: Fix table captions (move above tables)
python3 fix_table_captions.py

# Step 3: Convert inline code blocks to fenced
python3 convert_inline_code_blocks.py

# Step 4: Move TOC below heading
python3 move_toc_below_heading.py

# Step 5: Rebuild combined files
./combine_files.sh
```

## What's Fixed

✅ **Tables:** Proper Markdown pipe format
✅ **Table Captions:** Above tables (not below)
✅ **Code Blocks:** Fenced blocks with C syntax highlighting
✅ **Contributor Additions:** Marked with `// contributor addition` comments
✅ **TOC:** Below H1 heading with blank line spacing
✅ **All Combined Files:** Master + 9 categories rebuilt

## Known Limitations

### Images (29 total)
- Image references like `[[File:Kernel table.png]]` are still MediaWiki format
- Images not downloaded or embedded
- **TODO:** Download from Fandom and convert to `![alt](path)` format

### Internal Links
- Wiki links like `[[FF7/Kernel]]` still in MediaWiki format
- Should be converted to `[FF7/Kernel](FF7_Kernel.md)` for local navigation
- **TODO:** Convert internal wiki links to relative markdown links

## Recommended Next Steps

1. **Download Images Script:**
   - Extract all `[[File:...]]` references
   - Download from `https://qhimm-modding.fandom.com/wiki/Special:FilePath/{filename}`
   - Save to `images/` directory
   - Replace references with `![alt](../images/{filename})`

2. **Fix Internal Links Script:**
   - Convert `[[Page]]` to `[Page](Page.md)`
   - Convert `[[Page|Display]]` to `[Display](Page.md)`
   - Convert `[[Page#Section]]` to `[Page](Page.md#section)`
   - Sanitize filenames (spaces → `_`, `/` → `_`)

## File Summary

**Input:** 32 MediaWiki pages from qhimm-modding Fandom
**Output:**
- 32 individual markdown files with TOC
- 1 master GameEngine.md (30 pages, excludes Savemap + Battle Model)
- 9 category combined files
- 2 README files

**Scripts Created:**
1. `scraper.py` - Download raw MediaWiki
2. `convert_to_markdown_improved.sh` - Pandoc with pipe tables
3. `fix_table_captions.py` - Move captions above tables
4. `convert_inline_code_blocks.py` - Fenced blocks with contributor marks
5. `move_toc_below_heading.py` - TOC positioning
6. `combine_files.sh` - Build combined documentation

All scripts are idempotent and can be re-run safely.

#!/bin/bash
#
# Convert MediaWiki files to Markdown with proper tables and TOCs
#
# Created: 2025-11-28 13:01:32 JST (Friday)
# Context: Improved conversion using Pandoc with pipe tables forced and table of contents.
#          Fixes table rendering issues from initial conversion and adds navigation TOCs.
#
# Author: John Zealand-Doyle
# Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c

echo "======================================================================="
echo "Converting MediaWiki files to Markdown (IMPROVED)"
echo "  - Proper Markdown pipe tables"
echo "  - Table of contents for each file"
echo "======================================================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Backup old markdown files
echo "📦 Backing up old markdown files..."
if [ -d "markdown_backup" ]; then
    rm -rf markdown_backup
fi
mkdir markdown_backup
cp -r markdown/*.md markdown_backup/ 2>/dev/null
echo "✅ Backup created: markdown_backup/"
echo ""

# Counter
success=0
failed=0

# Pandoc options explained:
# -f mediawiki: input format
# -t markdown: output format with extensions:
#   -simple_tables: disable simple tables
#   -multiline_tables: disable multiline tables
#   -grid_tables: disable grid tables
#   +pipe_tables: force pipe tables (Markdown standard)
# --standalone: enable document structure (required for TOC)
# --toc: generate table of contents
# --toc-depth=4: include up to h4 in TOC
# --wrap=preserve: preserve line wrapping from source

PANDOC_OPTS="-f mediawiki -t markdown-simple_tables-multiline_tables-grid_tables+pipe_tables --standalone --toc --toc-depth=4 --wrap=preserve"

# Convert each .mediawiki file
for file in raw/*.mediawiki; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .mediawiki)
        output="markdown/${basename}.md"

        echo "Converting: $basename"
        echo "  Options: pipe tables + TOC"

        # Run pandoc conversion with improved options
        if pandoc $PANDOC_OPTS "$file" -o "$output"; then
            echo "  ✅ Success: $output"
            ((success++))
        else
            echo "  ❌ Failed: $file"
            ((failed++))
        fi
    fi
done

echo ""
echo "======================================================================="
echo "CONVERSION COMPLETE (IMPROVED)"
echo "======================================================================="
echo "✅ Successfully converted: $success files"
if [ $failed -gt 0 ]; then
    echo "❌ Failed: $failed files"
else
    echo "🎉 All files converted successfully!"
fi
echo ""
echo "Improvements:"
echo "  ✅ Tables now use proper Markdown pipe format"
echo "  ✅ Each file has table of contents at the top"
echo "  ✅ TOC includes up to h4 headings"
echo ""
echo "Old files backed up to: markdown_backup/"
echo ""

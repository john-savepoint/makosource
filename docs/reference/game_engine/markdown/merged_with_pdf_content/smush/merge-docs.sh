#!/bin/bash
#
# FF7 Game Engine Documentation Merge Script
# Created: 2025-11-30 18:33 JST
# Purpose: Merge individual markdown files into monolithic FF7_GameEngine_MERGED.md
# Session-ID: 6f8970e0-023d-45dc-b3d8-5c9f9a8ff58e
#
# Usage: ./merge-docs.sh
#
# Prerequisites:
#   - Pandoc installed (brew install pandoc)
#   - file-order.txt exists (generated from FF7.md TOC)
#   - strip-metadata-toc.lua exists (Pandoc filter)
#
# Output: FF7_GameEngine_MERGED.md
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔧 FF7 Documentation Merge Script"
echo "===================================="
echo ""

# Check prerequisites
if ! command -v pandoc &> /dev/null; then
    echo "❌ Error: Pandoc not found. Install with: brew install pandoc"
    exit 1
fi

if [ ! -f "file-order.txt" ]; then
    echo "❌ Error: file-order.txt not found. Run extraction script first."
    exit 1
fi

if [ ! -f "strip-metadata-toc.lua" ]; then
    echo "❌ Error: strip-metadata-toc.lua not found."
    exit 1
fi

# Count files to merge
FILE_COUNT=$(wc -l < file-order.txt | tr -d ' ')
echo "📄 Files to merge: $FILE_COUNT"
echo ""

# Verify all files exist
echo "✅ Verifying all files exist..."
MISSING_COUNT=0
while IFS= read -r file; do
    if [ ! -f "$file" ]; then
        echo "  ❌ MISSING: $file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done < file-order.txt

if [ $MISSING_COUNT -gt 0 ]; then
    echo ""
    echo "❌ Error: $MISSING_COUNT file(s) missing. Cannot proceed."
    exit 1
fi
echo "  ✅ All files present"
echo ""

# Execute Pandoc merge
echo "🚀 Executing Pandoc merge..."
pandoc \
  --from=markdown \
  --to=markdown \
  --shift-heading-level-by=1 \
  --toc \
  --toc-depth=4 \
  --lua-filter=strip-metadata-toc.lua \
  --standalone \
  --metadata title="FF7 Game Engine Documentation" \
  -o FF7_GameEngine_MERGED.md \
  $(cat file-order.txt | tr '\n' ' ')

if [ $? -eq 0 ]; then
    echo "  ✅ Merge successful"
    echo ""
else
    echo "  ❌ Merge failed"
    exit 1
fi

# Report statistics
echo "📊 Output Statistics"
echo "===================================="
LINE_COUNT=$(wc -l < FF7_GameEngine_MERGED.md | tr -d ' ')
WORD_COUNT=$(wc -w < FF7_GameEngine_MERGED.md | tr -d ' ')
SIZE=$(du -h FF7_GameEngine_MERGED.md | cut -f1)
echo "  Lines: $LINE_COUNT"
echo "  Words: $WORD_COUNT"
echo "  Size:  $SIZE"
echo ""

# Check for potential issues
echo "🔍 Quick Validation"
echo "===================================="

# Check for remaining HTML comments
HTML_COMMENTS=$(grep -c '<!--' FF7_GameEngine_MERGED.md || true)
if [ $HTML_COMMENTS -gt 0 ]; then
    echo "  ⚠️  HTML comments found: $HTML_COMMENTS (review if these are intentional)"
else
    echo "  ✅ No HTML comment blocks found"
fi

# Check heading levels
H1_COUNT=$(grep -c '^# ' FF7_GameEngine_MERGED.md || true)
H2_COUNT=$(grep -c '^## ' FF7_GameEngine_MERGED.md || true)
echo "  ✅ H1 headings: $H1_COUNT"
echo "  ✅ H2 headings: $H2_COUNT"
echo ""

echo "✨ Merge complete! Output: FF7_GameEngine_MERGED.md"
echo ""
echo "Next steps:"
echo "  1. Review FF7_GameEngine_MERGED.md for accuracy"
echo "  2. Check heading hierarchy and TOC structure"
echo "  3. Verify metadata and internal TOCs removed"
echo "  4. Commit to git when satisfied"

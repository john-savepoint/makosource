#!/bin/bash
#
# Convert MediaWiki files to Markdown using Pandoc
#
# Created: 2025-11-28 12:44:49 JST (Friday)
# Context: Batch conversion of 32 scraped MediaWiki files to Markdown format.
#          Preserves tables, code blocks, and formatting during conversion.
#
# Author: John Zealand-Doyle
# Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c

echo "======================================================================="
echo "Converting MediaWiki files to Markdown using Pandoc"
echo "======================================================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Counter
success=0
failed=0

# Convert each .mediawiki file
for file in raw/*.mediawiki; do
    if [ -f "$file" ]; then
        basename=$(basename "$file" .mediawiki)
        output="markdown/${basename}.md"

        echo "Converting: $basename"

        # Run pandoc conversion
        if pandoc -f mediawiki -t markdown "$file" -o "$output"; then
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
echo "CONVERSION COMPLETE"
echo "======================================================================="
echo "✅ Successfully converted: $success files"
if [ $failed -gt 0 ]; then
    echo "❌ Failed: $failed files"
else
    echo "🎉 All files converted successfully!"
fi
echo ""

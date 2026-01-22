#!/bin/bash
# AF3DN.P Analysis Consolidation Script
# Created: 2025-12-16 14:50 JST
# Session: 0681f78b-0382-45ee-898b-5a32b7ce32d5
#
# This script consolidates all chunk analyses into a single document
# and extracts function name suggestions for review.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/outputs"
CONSOLIDATED="${SCRIPT_DIR}/AF3DN_FULL_ANALYSIS.md"
FUNCTION_MAP="${SCRIPT_DIR}/function_names.csv"

echo "Consolidating AF3DN.P analysis results..."

# Create header for consolidated document
cat > "$CONSOLIDATED" << 'HEADER'
# AF3DN.P Complete Analysis

**Generated**: $(date '+%Y-%m-%d %H:%M:%S JST')
**Source**: IDA Pro decompiled AF3DN.P.c
**Total Functions**: 549
**Total Chunks**: 35

---

## Table of Contents

HEADER

# Add TOC entries
for i in $(seq 1 35); do
    if [ -f "${OUTPUT_DIR}/chunk_${i}_analysis.md" ]; then
        echo "- [Chunk $i](#chunk-$i-analysis)" >> "$CONSOLIDATED"
    fi
done

echo "" >> "$CONSOLIDATED"
echo "---" >> "$CONSOLIDATED"
echo "" >> "$CONSOLIDATED"

# Append each chunk analysis
for i in $(seq 1 35); do
    chunk_file="${OUTPUT_DIR}/chunk_${i}_analysis.md"
    if [ -f "$chunk_file" ] && [ -s "$chunk_file" ]; then
        echo "" >> "$CONSOLIDATED"
        cat "$chunk_file" >> "$CONSOLIDATED"
        echo "" >> "$CONSOLIDATED"
        echo "---" >> "$CONSOLIDATED"
    else
        echo "Warning: Chunk $i analysis not found or empty"
    fi
done

echo "Created: $CONSOLIDATED"

# Extract function name suggestions to CSV
echo "Extracting function name suggestions..."

echo "original_name,suggested_name,category,line" > "$FUNCTION_MAP"

# Parse each chunk output for function suggestions
for i in $(seq 1 35); do
    chunk_file="${OUTPUT_DIR}/chunk_${i}_analysis.md"
    if [ -f "$chunk_file" ]; then
        # Extract lines with function names and suggested names
        # Pattern: ### Function sub_XXXXXXXX ... Suggested Name: ...
        grep -E "(^### Function sub_|Suggested Name)" "$chunk_file" 2>/dev/null | \
        paste - - 2>/dev/null | \
        sed -E 's/### Function (sub_[0-9A-Fa-f]+).*Suggested Name.*: ([a-z_]+)/\1,\2/' >> "$FUNCTION_MAP" || true
    fi
done

echo "Created: $FUNCTION_MAP"

# Summary
total_chunks=$(ls -1 "${OUTPUT_DIR}"/chunk_*_analysis.md 2>/dev/null | wc -l || echo 0)
echo ""
echo "Consolidation complete!"
echo "  Chunks processed: $total_chunks / 35"
echo "  Full analysis: $CONSOLIDATED"
echo "  Function map: $FUNCTION_MAP"

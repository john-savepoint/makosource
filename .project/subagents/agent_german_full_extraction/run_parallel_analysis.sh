#!/bin/bash
# Run Haiku analysis on all chunks - 5 jobs at a time using xargs
# Created: 2026-01-03 14:05 JST

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHUNKS_DIR="$SCRIPT_DIR/chunks"
OUTPUT_DIR="$SCRIPT_DIR/haiku_results"

mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "Parallel German String Analysis with Haiku"
echo "=========================================="
echo "Chunks directory: $CHUNKS_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "Parallelism: 5 jobs"
echo ""

# Make analyze script executable
chmod +x "$SCRIPT_DIR/analyze_chunk.sh"

# Count chunks
TOTAL=$(ls "$CHUNKS_DIR"/chunk_*.txt 2>/dev/null | wc -l)
echo "Total chunks to process: $TOTAL"
echo ""

# Run with xargs - 5 at a time with progress
ls "$CHUNKS_DIR"/chunk_*.txt | xargs -P 5 -I {} bash -c '
    CHUNK="{}"
    NAME=$(basename "$CHUNK" .txt)
    echo "[$(date +%H:%M:%S)] Starting $NAME"
    '"$SCRIPT_DIR"'/analyze_chunk.sh "$CHUNK"
    echo "[$(date +%H:%M:%S)] Finished $NAME"
'

echo ""
echo "=========================================="
echo "Analysis complete!"
echo "Results in: $OUTPUT_DIR"
echo ""

# Count results
RESULTS=$(ls "$OUTPUT_DIR"/*.csv 2>/dev/null | wc -l)
echo "Total result files: $RESULTS"

# Merge all results
echo ""
echo "Merging results..."
cat "$OUTPUT_DIR"/chunk_*_mapping.csv 2>/dev/null > "$OUTPUT_DIR/all_mappings_raw.csv"
echo "Merged to: $OUTPUT_DIR/all_mappings_raw.csv"

# Show sample
echo ""
echo "Sample mappings found:"
head -30 "$OUTPUT_DIR/all_mappings_raw.csv" 2>/dev/null || echo "No mappings yet"

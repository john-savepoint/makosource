#!/bin/bash
# Analyze a single German chunk with Claude Haiku
# Usage: ./analyze_chunk.sh chunk_XX.txt
# Created: 2026-01-03 14:05 JST

CHUNK_FILE="$1"
CHUNK_NAME=$(basename "$CHUNK_FILE" .txt)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/haiku_results"
ENGLISH_REF="$SCRIPT_DIR/../agent2_english_extraction/english_strings_by_index.txt"

mkdir -p "$OUTPUT_DIR"

# Skip if already processed
if [[ -f "$OUTPUT_DIR/${CHUNK_NAME}_mapping.csv" ]]; then
    echo "Skipping $CHUNK_NAME - already processed"
    exit 0
fi

echo "Processing $CHUNK_NAME..."

# Read the chunk content
GERMAN_CONTENT=$(cat "$CHUNK_FILE")

# Get English reference (first 100 lines for context)
ENGLISH_CONTENT=$(head -100 "$ENGLISH_REF")

# Run Haiku analysis
/home/johnzealanddoyle/.local/bin/claude --model haiku --dangerously-skip-permissions -p "
You are mapping FF7 German menu strings to English touphScript indices.

TASK: For each German string that looks like a menu item, find its English equivalent and output a CSV mapping.

GERMAN STRINGS (from ff7_de.exe with hex offsets):
$GERMAN_CONTENT

ENGLISH REFERENCE (touphScript indices 0-99):
$ENGLISH_CONTENT

OUTPUT FORMAT (CSV only, no explanation):
index,de_offset,de_text,en_text

Rules:
- Only map strings that are clearly menu text (not garbage/binary)
- de_offset should be the hex offset from the German strings
- Look for German translations of: Item, Magic, Equip, Save, Config, Status, battle terms, etc.
- Skip single characters, numbers, or obvious binary garbage
- Output ONLY the CSV data, no headers, no explanation
" > "$OUTPUT_DIR/${CHUNK_NAME}_mapping.csv" 2>&1

echo "Completed $CHUNK_NAME -> $OUTPUT_DIR/${CHUNK_NAME}_mapping.csv"

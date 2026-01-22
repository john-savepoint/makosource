#!/bin/bash
# Haiku LLM Analysis for German String Extraction
# Created: 2026-01-03
# PRIMARY extraction method - runs on ALL chunks

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/results"
CLAUDE_CMD="/home/johnzealanddoyle/.local/bin/claude"

mkdir -p "$OUTPUT_DIR"

analyze_chunk() {
    local CHUNK_FILE="$1"
    local CHUNK_NAME=$(basename "$CHUNK_FILE" .txt)
    local OUTPUT_FILE="$OUTPUT_DIR/${CHUNK_NAME}_result.csv"

    # Skip if already processed
    if [[ -f "$OUTPUT_FILE" && -s "$OUTPUT_FILE" ]]; then
        echo "Skipping $CHUNK_NAME - already processed"
        return 0
    fi

    echo "Processing $CHUNK_NAME..."

    CONTENT=$(cat "$CHUNK_FILE")

    $CLAUDE_CMD --model haiku --dangerously-skip-permissions -p "
You are mapping German FF7 menu strings to English touphScript indices.

TASK: For each German string, find its matching English string and output the mapping.

CRITICAL RULES:
1. Output ONLY CSV format: english_index,german_offset,german_text,english_text
2. NO headers, NO explanations, NO markdown
3. Map EVERY German string that has an English equivalent
4. Use the EXACT offset from the German strings
5. Common mappings:
   - Ja = Yes, Nein = No
   - Speichern = Save, Beenden = Quit
   - Objekt/Gegenstand = Item, Zauber/Magie = Magic
   - Ausrüsten = Equip, Status = Status
   - Konfig = Config, Menü = Menu
   - Auswählen = Select, Abbrechen = Cancel
   - Kampftempo = Battle speed, Kampfmeldung = Battle message

INPUT:
$CONTENT

OUTPUT (CSV only):
" > "$OUTPUT_FILE" 2>&1

    # Check if result looks valid
    if grep -q "^[0-9]" "$OUTPUT_FILE"; then
        echo "  Success: $CHUNK_NAME"
    else
        echo "  Warning: $CHUNK_NAME may need review"
    fi
}

export -f analyze_chunk
export CLAUDE_CMD
export OUTPUT_DIR

# Run analysis on all chunks (5 parallel jobs)
echo "Starting Haiku analysis on all chunks..."
echo "Running 5 parallel jobs..."
echo ""

find "$SCRIPT_DIR" -name "chunk_*.txt" | sort | xargs -P 5 -I {} bash -c 'analyze_chunk "$@"' _ {}

echo ""
echo "Analysis complete!"
echo "Results in: $OUTPUT_DIR"

# Consolidate results
echo ""
echo "Consolidating results..."
cat "$OUTPUT_DIR"/chunk_*_result.csv | grep "^[0-9]" | sort -t',' -k1 -n | uniq > "$OUTPUT_DIR/all_mappings.csv"
echo "Consolidated mappings: $OUTPUT_DIR/all_mappings.csv"
wc -l "$OUTPUT_DIR/all_mappings.csv"

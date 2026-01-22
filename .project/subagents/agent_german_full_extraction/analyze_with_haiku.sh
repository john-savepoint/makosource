#!/bin/bash
# Analyze German string chunks with Claude Haiku in headless mode
# Created: 2026-01-03 13:40 JST
# Session: 8bc98f0a-abab-49e6-acdd-56dd38e9d149

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/haiku_analysis"
ENGLISH_REF="$SCRIPT_DIR/../agent2_english_extraction/english_strings_by_index.txt"
GERMAN_MENU="$SCRIPT_DIR/german_menu_region.txt"

mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "German HEXT String Analysis with Haiku"
echo "=========================================="
echo "German menu strings: $GERMAN_MENU"
echo "English reference: $ENGLISH_REF"
echo "Output: $OUTPUT_DIR"
echo ""

# First, let's extract a focused subset for the first analysis
# The menu strings we care about are roughly the first ~100 entries
# Let's take strings from 0x58FB00 to 0x591000 which contains config menu

echo "Extracting focused menu region for analysis..."
head -200 "$GERMAN_MENU" > "$OUTPUT_DIR/german_focused.txt"
head -100 "$ENGLISH_REF" > "$OUTPUT_DIR/english_focused.txt"

# Now analyze with Haiku
echo "Running Haiku analysis..."

claude --model haiku --dangerously-skip-permissions -p "
You are analyzing FF7 menu strings to create a mapping between English and German.

## TASK
Compare these German strings (with their hex offsets from ff7_de.exe) to the English strings (with their touphScript indices).
Create a CSV mapping: index,en_offset,de_offset,en_text,de_text

## GERMAN STRINGS (from ff7_de.exe):
$(cat "$OUTPUT_DIR/german_focused.txt")

## ENGLISH STRINGS (touphScript indices):
$(cat "$OUTPUT_DIR/english_focused.txt")

## OUTPUT
Generate a CSV with columns: index,en_offset,de_offset,en_text,de_text
Map each English string to its German equivalent based on meaning.
The order is generally preserved but offsets differ.

Key mappings to find:
- 'Do you want to quit' -> 'Möchten Sie Final...'
- 'Window color' -> 'Fensterfarbe'
- 'Controller' -> 'Kontroller'
- 'Battle speed' -> 'Kampftempo'
- 'Item' -> 'Objekt'
- 'Magic' -> 'Zauber' or 'Materia'
- 'Save' -> 'Speichern'
- etc.

Output ONLY the CSV, nothing else.
" > "$OUTPUT_DIR/mapping_result.csv" 2>&1

echo "Analysis complete. Results in $OUTPUT_DIR/mapping_result.csv"
cat "$OUTPUT_DIR/mapping_result.csv" | head -50

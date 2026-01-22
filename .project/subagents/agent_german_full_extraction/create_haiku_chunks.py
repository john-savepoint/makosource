#!/usr/bin/env python3
"""
Create Clean Chunks for Haiku LLM Analysis
==========================================
Created: 2026-01-03 16:20 JST
Session: 629f3c93-f884-439a-91d6-d77e7783bf9c

This script creates properly formatted chunks for Haiku LLM to:
1. Extract German strings with their offsets
2. Map them to English touphScript indices (0-766)

The Haiku LLM is the PRIMARY extraction method.
"""

import os
import sys

# =============================================================================
# VERIFIED GERMAN CHARACTER ENCODING
# =============================================================================

FF7_GERMAN_DECODE_MAP = {
    0x66: 'Ü', 0x6A: 'ä', 0x7A: 'ö', 0x7E: 'ß', 0x7F: 'ü',
    0x61: 'á', 0x62: 'à', 0x63: 'â', 0x64: 'ã', 0x65: 'å',
    0x67: 'ç', 0x68: 'é', 0x69: 'è', 0x6B: 'ë',
    0x6C: 'í', 0x6D: 'ì', 0x6E: 'î', 0x6F: 'ï',
    0x70: 'ñ', 0x71: 'ó', 0x72: 'ò', 0x73: 'ô', 0x74: 'õ',
    0x76: '°', 0x77: '•', 0x78: '£',
}


def decode_ff7_german(data: bytes) -> str:
    """Decode FF7 German encoded bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        elif b in FF7_GERMAN_DECODE_MAP:
            result.append(FF7_GERMAN_DECODE_MAP[b])
        elif b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))
        # Skip unknown bytes silently for cleaner output
    return ''.join(result).strip()


def extract_clean_strings(data: bytes, start: int, end: int, min_alpha: int = 2):
    """
    Extract strings that are actually text (not binary noise).
    Returns list of (offset, decoded_text) tuples.
    """
    strings = []
    region = data[start:end]

    current_string = []
    string_start = 0

    for i, b in enumerate(region):
        if b == 0xFF:
            if current_string:
                raw = bytes(current_string)
                decoded = decode_ff7_german(raw)
                # Filter: must have enough letters
                letter_count = sum(1 for c in decoded if c.isalpha())
                if letter_count >= min_alpha:
                    strings.append((start + string_start, decoded))
                current_string = []
            string_start = i + 1
        else:
            if not current_string:
                string_start = i
            current_string.append(b)

    return strings


def load_english_reference(filepath: str):
    """Load English touphScript strings for reference."""
    english = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('[') and ']' in line:
                try:
                    idx_end = line.index(']')
                    idx = int(line[1:idx_end])
                    # Extract text after the pipe
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            text = parts[1].strip()
                            english[idx] = text
                except:
                    pass
    return english


def main():
    # Paths
    de_exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"
    en_ref_path = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt"
    output_dir = "/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/haiku_chunks"

    os.makedirs(output_dir, exist_ok=True)

    print("=" * 80)
    print("CREATING HAIKU ANALYSIS CHUNKS")
    print("=" * 80)
    print()

    # Read German exe
    print(f"Reading German exe...")
    with open(de_exe_path, 'rb') as f:
        data = f.read()

    # Load English reference
    print(f"Loading English reference...")
    english = load_english_reference(en_ref_path)
    print(f"  Loaded {len(english)} English strings")

    # Define regions to extract (based on analysis)
    # Menu strings are primarily in 0x58FB00 - 0x5D0000
    regions = [
        (0x58FB00, 0x5A0000, "Menu strings 1"),
        (0x5A0000, 0x5C0000, "Menu strings 2"),
        (0x5C0000, 0x5E0000, "Extended strings"),
    ]

    all_strings = []

    for start, end, desc in regions:
        print(f"Extracting {desc} (0x{start:06X} - 0x{end:06X})...")
        strings = extract_clean_strings(data, start, end, min_alpha=2)
        print(f"  Found {len(strings)} strings")
        all_strings.extend(strings)

    # Sort by offset and deduplicate
    all_strings = list(set(all_strings))
    all_strings.sort(key=lambda x: x[0])

    print(f"\nTotal strings: {len(all_strings)}")

    # Create comprehensive chunk for Haiku
    # Include ALL English strings (767) and ALL German strings found
    # Haiku will map them

    # Write English reference file
    en_ref_file = os.path.join(output_dir, "english_reference.txt")
    print(f"\nWriting English reference: {en_ref_file}")
    with open(en_ref_file, 'w', encoding='utf-8') as f:
        f.write("# English touphScript strings (indices 0-766)\n")
        f.write("# Format: INDEX | ENGLISH_TEXT\n")
        f.write("# Total: 767 strings\n\n")
        for idx in range(767):
            text = english.get(idx, f"[INDEX {idx} - no text]")
            f.write(f"{idx:03d} | {text}\n")

    # Write German strings file
    de_strings_file = os.path.join(output_dir, "german_strings.txt")
    print(f"Writing German strings: {de_strings_file}")
    with open(de_strings_file, 'w', encoding='utf-8') as f:
        f.write("# German strings from ff7_de.exe (correctly decoded)\n")
        f.write("# Format: OFFSET | GERMAN_TEXT\n")
        f.write(f"# Total: {len(all_strings)} strings\n\n")
        for offset, text in all_strings:
            f.write(f"0x{offset:06X} | {text}\n")

    # Create chunks for parallel Haiku processing
    # Each chunk: batch of German strings + subset of English reference
    chunk_size = 100  # German strings per chunk
    num_chunks = (len(all_strings) + chunk_size - 1) // chunk_size

    print(f"\nCreating {num_chunks} Haiku chunks...")

    for chunk_idx in range(num_chunks):
        chunk_start = chunk_idx * chunk_size
        chunk_end = min((chunk_idx + 1) * chunk_size, len(all_strings))
        chunk_strings = all_strings[chunk_start:chunk_end]

        chunk_file = os.path.join(output_dir, f"chunk_{chunk_idx:03d}.txt")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(f"# Haiku Analysis Chunk {chunk_idx:03d}\n")
            f.write(f"# German strings {chunk_start} to {chunk_end-1}\n")
            f.write("#\n")
            f.write("# TASK: Map each German string to its English touphScript index (0-766)\n")
            f.write("# OUTPUT: CSV format only: english_index,german_offset,german_text,english_text\n")
            f.write("#\n")
            f.write("# " + "=" * 75 + "\n")
            f.write("# GERMAN STRINGS TO MAP:\n")
            f.write("# " + "=" * 75 + "\n\n")

            for offset, text in chunk_strings:
                f.write(f"0x{offset:06X} | {text}\n")

            f.write("\n# " + "=" * 75 + "\n")
            f.write("# ENGLISH REFERENCE (all 767 indices):\n")
            f.write("# " + "=" * 75 + "\n\n")

            for idx in range(767):
                text = english.get(idx, "")
                if text:
                    f.write(f"{idx:03d} | {text}\n")

    # Create the Haiku analysis script
    analysis_script = os.path.join(output_dir, "run_haiku_analysis.sh")
    print(f"Creating analysis script: {analysis_script}")

    with open(analysis_script, 'w') as f:
        f.write("""#!/bin/bash
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
""")

    os.chmod(analysis_script, 0o755)

    print()
    print("=" * 80)
    print("CHUNK CREATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Created {num_chunks} chunks in {output_dir}")
    print()
    print("Files created:")
    print(f"  - english_reference.txt (767 English strings)")
    print(f"  - german_strings.txt ({len(all_strings)} German strings)")
    print(f"  - chunk_XXX.txt ({num_chunks} chunks)")
    print(f"  - run_haiku_analysis.sh (parallel analysis script)")
    print()
    print("To run Haiku analysis:")
    print(f"  cd {output_dir}")
    print("  ./run_haiku_analysis.sh")
    print()

    # Show sample German strings
    print("Sample German strings extracted:")
    print("-" * 60)
    german_chars = ['ä', 'ö', 'ü', 'Ü', 'ß']
    count = 0
    for offset, text in all_strings:
        if any(c in text for c in german_chars) or len(text) > 5:
            print(f"0x{offset:06X}: {text[:50]}")
            count += 1
            if count >= 30:
                break


if __name__ == "__main__":
    main()

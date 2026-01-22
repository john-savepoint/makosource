#!/bin/bash
# AF3DN.P Parallel Analysis Script
# Created: 2025-12-16 14:45 JST
# Session: 0681f78b-0382-45ee-898b-5a32b7ce32d5
#
# This script uses Claude Code in headless mode to analyze chunks of the
# IDA Pro decompiled AF3DN.P.c file using parallel agents.
#
# Usage:
#   ./analyze_af3dn.sh [chunk_id]           # Analyze single chunk
#   ./analyze_af3dn.sh --all [parallelism]  # Analyze all chunks (default: 5 parallel)
#   ./analyze_af3dn.sh --status             # Check progress

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_FILE="${SCRIPT_DIR}/../AF3DN.P.c"
CONTEXT_FILE="${SCRIPT_DIR}/agent_context.md"
CHUNKS_FILE="${SCRIPT_DIR}/chunk_definitions.json"
OUTPUT_DIR="${SCRIPT_DIR}/outputs"
LOG_DIR="${SCRIPT_DIR}/logs"

# Parallelism settings
DEFAULT_PARALLEL=5
MAX_PARALLEL=10

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create directories
mkdir -p "$OUTPUT_DIR" "$LOG_DIR"

# Function to extract chunk info from JSON
get_chunk_info() {
    local chunk_id=$1
    python3 -c "
import json
with open('$CHUNKS_FILE') as f:
    data = json.load(f)
for chunk in data['chunks']:
    if chunk['id'] == $chunk_id:
        print(f\"{chunk['start']} {chunk['end']} {chunk['lines']} {chunk['functions']}\")
        break
"
}

# Function to get total chunks
get_total_chunks() {
    python3 -c "
import json
with open('$CHUNKS_FILE') as f:
    data = json.load(f)
print(len(data['chunks']))
"
}

# Function to analyze a single chunk
analyze_chunk() {
    local chunk_id=$1
    local chunk_info
    chunk_info=$(get_chunk_info "$chunk_id")

    if [ -z "$chunk_info" ]; then
        echo -e "${RED}Error: Chunk $chunk_id not found${NC}"
        return 1
    fi

    read -r start end lines functions <<< "$chunk_info"

    local output_file="${OUTPUT_DIR}/chunk_${chunk_id}_analysis.md"
    local log_file="${LOG_DIR}/chunk_${chunk_id}.log"

    # Skip if already analyzed
    if [ -f "$output_file" ] && [ -s "$output_file" ]; then
        echo -e "${YELLOW}Chunk $chunk_id already analyzed, skipping...${NC}"
        return 0
    fi

    echo -e "${BLUE}Analyzing chunk $chunk_id (lines $start-$end, $lines lines, $functions functions)...${NC}"

    # Extract the chunk
    local chunk_content
    chunk_content=$(sed -n "${start},${end}p" "$SOURCE_FILE")

    # Read context
    local context
    context=$(cat "$CONTEXT_FILE")

    # Build the prompt - write to temp file to avoid shell escaping issues
    local prompt_file="/tmp/af3dn_prompt_${chunk_id}.txt"

    cat > "$prompt_file" << PROMPT_EOF
OUTPUT FORMAT REQUIREMENT - READ THIS FIRST:

You MUST output markdown in this EXACT structure for each function. No summaries. No deviations.

### Function sub_XXXXXXXX (line NNNN)
- **Category**: [Graphics|Text|Input|Audio|Memory|File|Registry|Init|Math|Utility|Unknown]
- **Purpose**: [1-2 sentence description]
- **Suggested Name**: [snake_case_name]
- **Key Calls**: [important functions/APIs called]
- **Notes**: [observations or "None"]

Repeat this structure for EVERY function. Start with "## Chunk $chunk_id Analysis" header.

---

$context

---

## Your Assigned Chunk

**Chunk ID**: $chunk_id
**Lines**: $start to $end
**Functions to analyze**: $functions

\`\`\`c
$chunk_content
\`\`\`

NOW OUTPUT THE ANALYSIS. Start with the header, then analyze each function using the exact format above.
PROMPT_EOF

    # Run Claude Code in headless mode
    # Using Haiku for speed/cost with structured output format
    # Reading prompt from file, no tools needed (pure text analysis)
    claude -p "$(cat "$prompt_file")" --model haiku --allowedTools "" > "$output_file" 2> "$log_file"

    # Cleanup temp file
    rm -f "$prompt_file"

    local exit_code=$?

    if [ $exit_code -eq 0 ] && [ -s "$output_file" ]; then
        echo -e "${GREEN}✓ Chunk $chunk_id completed${NC}"
        return 0
    else
        echo -e "${RED}✗ Chunk $chunk_id failed (exit code: $exit_code)${NC}"
        return 1
    fi
}

# Function to show status
show_status() {
    local total
    total=$(get_total_chunks)
    local completed=0
    local failed=0

    echo -e "${BLUE}AF3DN.P Analysis Status${NC}"
    echo "========================"
    echo ""

    for i in $(seq 1 "$total"); do
        local output_file="${OUTPUT_DIR}/chunk_${i}_analysis.md"
        if [ -f "$output_file" ] && [ -s "$output_file" ]; then
            echo -e "  Chunk $i: ${GREEN}✓ Complete${NC}"
            ((completed++))
        elif [ -f "$output_file" ]; then
            echo -e "  Chunk $i: ${RED}✗ Empty/Failed${NC}"
            ((failed++))
        else
            echo -e "  Chunk $i: ${YELLOW}○ Pending${NC}"
        fi
    done

    echo ""
    echo "========================"
    echo -e "Total: $total | ${GREEN}Complete: $completed${NC} | ${RED}Failed: $failed${NC} | Pending: $((total - completed - failed))"
}

# Function to analyze all chunks with parallelism
analyze_all() {
    local parallel=${1:-$DEFAULT_PARALLEL}

    if [ "$parallel" -gt "$MAX_PARALLEL" ]; then
        echo -e "${YELLOW}Warning: Limiting parallelism to $MAX_PARALLEL${NC}"
        parallel=$MAX_PARALLEL
    fi

    local total
    total=$(get_total_chunks)

    echo -e "${BLUE}Starting parallel analysis of $total chunks (parallelism: $parallel)${NC}"
    echo ""

    # Check if GNU parallel is available
    if command -v parallel &> /dev/null; then
        # Use GNU parallel
        seq 1 "$total" | parallel -j "$parallel" --progress "$0" {}
    else
        # Fallback to xargs
        echo -e "${YELLOW}GNU parallel not found, using xargs...${NC}"
        seq 1 "$total" | xargs -P "$parallel" -I {} "$0" {}
    fi

    echo ""
    show_status
}

# Main
case "${1:-}" in
    --all)
        analyze_all "${2:-$DEFAULT_PARALLEL}"
        ;;
    --status)
        show_status
        ;;
    --help|-h)
        echo "Usage: $0 [chunk_id]           Analyze single chunk"
        echo "       $0 --all [parallelism]  Analyze all chunks"
        echo "       $0 --status             Show progress"
        echo "       $0 --help               Show this help"
        ;;
    "")
        echo "Error: Please specify a chunk ID or --all"
        echo "Run '$0 --help' for usage"
        exit 1
        ;;
    *)
        if [[ "$1" =~ ^[0-9]+$ ]]; then
            analyze_chunk "$1"
        else
            echo "Error: Invalid argument '$1'"
            exit 1
        fi
        ;;
esac

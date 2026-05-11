#!/bin/bash

# FF7 2026 Reverse Engineering - Ralph Loop
# Usage: ./ralph.sh [max_iterations]

set -e

# Unset CLAUDECODE to allow running claude -p inside another Claude session
unset CLAUDECODE

# Use glm-5:cloud model (can be overridden with env var)
MODEL="${RALPH_MODEL:-glm-5:cloud}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MAX_ITERATIONS=${1:-20}
ITERATION=0

# Set up Ollama environment for glm-5:cloud model
if [[ "$MODEL" == *"glm"* ]] || [[ "$MODEL" == *"ollama"* ]]; then
    export ANTHROPIC_AUTH_TOKEN="ollama"
    unset ANTHROPIC_API_KEY  # Must unset, not empty string
    export ANTHROPIC_BASE_URL="http://localhost:11434"
fi

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     FF7 2026 Reverse Engineering - Ralph Loop                ║${NC}"
echo -e "${BLUE}║     Model: ${YELLOW}$MODEL${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Project: ${PROJECT_DIR}"
echo -e "Max iterations: ${MAX_ITERATIONS}"
echo ""

# Check for required files
if [ ! -f "$SCRIPT_DIR/plan.md" ]; then
    echo -e "${RED}ERROR: plan.md not found${NC}"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/PROMPT.md" ]; then
    echo -e "${RED}ERROR: PROMPT.md not found${NC}"
    exit 1
fi

# Check if Ollama is running (for glm/ollama models)
if [[ "$MODEL" == *"glm"* ]] || [[ "$MODEL" == *"ollama"* ]]; then
    if ! curl -s --connect-timeout 2 "http://localhost:11434/api/tags" >/dev/null 2>&1; then
        echo -e "${RED}ERROR: Ollama not running on localhost:11434${NC}"
        echo -e "${YELLOW}Start Ollama with: ollama serve${NC}"
        exit 1
    fi
    echo -e "${GREEN}Using Ollama backend: http://localhost:11434${NC}"
fi

echo -e "${YELLOW}Note: Ensure IDA Pro is running with the MCP server and FFVII.DMP loaded${NC}"
echo ""

# Main loop
while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))

    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Iteration $ITERATION / $MAX_ITERATIONS${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

    # Check if all tasks are complete
    PASSES_COUNT=$(grep -c '"passes": true' "$SCRIPT_DIR/plan.md" 2>/dev/null || echo "0")
    TOTAL_TASKS=$(grep -c '"passes":' "$SCRIPT_DIR/plan.md" 2>/dev/null || echo "0")

    echo -e "Tasks completed: ${GREEN}$PASSES_COUNT${NC} / $TOTAL_TASKS"

    if [ "$PASSES_COUNT" -eq "$TOTAL_TASKS" ] && [ "$TOTAL_TASKS" -gt 0 ]; then
        echo -e "${GREEN}All tasks complete!${NC}"
        exit 0
    fi

    # Run Claude with the prompt file
    echo -e "${YELLOW}Starting iteration...${NC}"
    echo ""

    # Change to project directory
    cd "$PROJECT_DIR"

    # Run Claude with the prompt file
    # Using --dangerously-skip-permissions to avoid approval prompts
    RESULT=$(claude -p "$(cat "$SCRIPT_DIR/PROMPT.md")" \
        --model "$MODEL" \
        --dangerously-skip-permissions \
        --allowedTools "Read,Edit,Write,Bash,mcp__ida-pro-mcp__*" \
        2>&1)

    # Capture exit code
    EXIT_CODE=$?

    # Output result
    echo "$RESULT"

    # Check for completion tags
    if [[ "$RESULT" == *"<promise>COMPLETE</promise>"* ]]; then
        echo -e "${GREEN}Task fully complete!${NC}"
        exit 0
    fi

    if [[ "$RESULT" == *"<promise>TOKEN_LIMIT</promise>"* ]]; then
        echo -e "${YELLOW}Token limit reached. Restarting with fresh context...${NC}"
        continue
    fi

    if [[ "$RESULT" == *"<promise>ITERATION_COMPLETE</promise>"* ]]; then
        echo -e "${GREEN}Iteration complete. Continuing...${NC}"
        continue
    fi

    # Check for errors
    if [ $EXIT_CODE -ne 0 ]; then
        echo -e "${RED}Claude exited with code $EXIT_CODE${NC}"
        echo -e "${YELLOW}Waiting 5 seconds before retry...${NC}"
        sleep 5
        continue
    fi

    echo -e "${YELLOW}No completion tag found. Continuing...${NC}"
done

echo ""
echo -e "${YELLOW}Reached maximum iterations ($MAX_ITERATIONS)${NC}"

# Final status
PASSES_COUNT=$(grep -c '"passes": true' "$SCRIPT_DIR/plan.md" 2>/dev/null || echo "0")
TOTAL_TASKS=$(grep -c '"passes":' "$SCRIPT_DIR/plan.md" 2>/dev/null || echo "0")

echo -e "Final status: ${GREEN}$PASSES_COUNT${NC} / $TOTAL_TASKS tasks complete"

if [ "$PASSES_COUNT" -lt "$TOTAL_TASKS" ]; then
    echo -e "${YELLOW}Run ./ralph.sh again to continue${NC}"
    exit 1
fi

exit 0
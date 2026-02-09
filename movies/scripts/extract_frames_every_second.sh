#!/bin/bash
#
# Script: extract_frames_every_second.sh
# Created: 2026-01-31 01:28 JST
# Context: Extract frames from video at 1 second intervals
#          First frame + every second until end of video
# Session: 51d0bc48-c27b-4af4-bfd3-4467a1802597
#
# Usage: ./extract_frames_every_second.sh <video_file>
# Example: ./extract_frames_every_second.sh "/mnt/h/ff7 movies/Chibi/movies/monitor.mov"

# Color codes
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m'

# Check argument
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No video file specified${NC}"
    echo "Usage: $0 <video_file>"
    echo "Example: $0 '/mnt/h/ff7 movies/Chibi/movies/monitor.mov'"
    exit 1
fi

VIDEO_FILE="$1"

# Check if file exists
if [ ! -f "$VIDEO_FILE" ]; then
    echo -e "${RED}Error: Video file not found: $VIDEO_FILE${NC}"
    exit 1
fi

# Get video directory and filename
VIDEO_DIR=$(dirname "$VIDEO_FILE")
VIDEO_NAME=$(basename "$VIDEO_FILE" .mov)

# Create frames subdirectory
FRAMES_DIR="$VIDEO_DIR/${VIDEO_NAME}_frames"
mkdir -p "$FRAMES_DIR"

echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Frame Extraction - Every Second${NC}                ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Video:${NC} $VIDEO_FILE"
echo -e "${CYAN}Output:${NC} $FRAMES_DIR"
echo ""

# Get video duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE")
DURATION_INT=$(printf "%.0f" "$DURATION")

echo -e "${GREEN}Video duration: ${DURATION}s (~${DURATION_INT} frames)${NC}"
echo ""
echo -e "${YELLOW}Extracting frames...${NC}"

# Extract frames at 1 fps (1 frame per second)
# -vf fps=1: Extract 1 frame per second
# frame_%04d.png: Output format (frame_0001.png, frame_0002.png, etc.)
ffmpeg -i "$VIDEO_FILE" \
    -vf fps=1 \
    "$FRAMES_DIR/frame_%04d.png" \
    -loglevel error \
    -stats

FRAME_COUNT=$(ls -1 "$FRAMES_DIR"/*.png 2>/dev/null | wc -l)

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Extraction Complete${NC}                            ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}✓ Extracted: ${FRAME_COUNT} frames${NC}"
echo -e "${CYAN}Location:${NC} $FRAMES_DIR"
echo ""

# Show first few frames
echo -e "${YELLOW}First frames:${NC}"
ls -1 "$FRAMES_DIR" | head -5
if [ $FRAME_COUNT -gt 5 ]; then
    echo "..."
fi

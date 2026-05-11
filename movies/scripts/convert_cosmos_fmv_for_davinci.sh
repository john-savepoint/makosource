#!/bin/bash
#
# Script: convert_cosmos_fmv_for_davinci.sh
# Created: 2026-01-30 23:27 JST
# Context: Convert Cosmos FMV30 videos from .avi (actually MKV) with 10-bit H.264 + Vorbis
#          to DaVinci Resolve-compatible format (.mov with 8-bit H.264 + AAC)
# Session: 51d0bc48-c27b-4af4-bfd3-4467a1802597
#
# Problem: Files have .avi extension but are MKV containers with:
#          - 10-bit AVC/H.264 video (High 10 profile) - incompatible with most editors
#          - Vorbis audio - not standard for editing
#          - Unusual 1280×896 resolution
#
# Solution: Convert to:
#          - .mov container (widely compatible)
#          - 8-bit H.264 video (yuv420p)
#          - AAC audio (industry standard)
#          - Preserve original resolution and framerate (29.97 fps)
#
# Usage: ./convert_cosmos_fmv_for_davinci.sh /path/to/source/directory /path/to/output/directory

set -e  # Exit on error

# Color codes for output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo "Usage: $0 <source_directory> <output_directory>"
    echo "Example: $0 '/mnt/d/Games/Stand-alone/FF7Modding/cosmos_fmv30/NonchibiOriginals/movies' '/mnt/d/Games/Stand-alone/FF7Modding/cosmos_fmv30_converted'"
    exit 1
fi

SOURCE_DIR="$1"
OUTPUT_DIR="$2"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: Source directory does not exist: $SOURCE_DIR${NC}"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Cosmos FMV30 → DaVinci Resolve Converter${NC}    ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Source:${NC} $SOURCE_DIR"
echo -e "${CYAN}Output:${NC} $OUTPUT_DIR"
echo ""

# Find all .avi files (which are actually MKV)
shopt -s nullglob
VIDEO_FILES=("$SOURCE_DIR"/*.avi)

if [ ${#VIDEO_FILES[@]} -eq 0 ]; then
    echo -e "${YELLOW}No .avi files found in source directory${NC}"
    exit 0
fi

echo -e "${GREEN}Found ${#VIDEO_FILES[@]} video file(s) to convert${NC}"
echo ""

# Process each file
CONVERTED=0
FAILED=0

for VIDEO in "${VIDEO_FILES[@]}"; do
    BASENAME=$(basename "$VIDEO" .avi)
    OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}.mov"

    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Processing:${NC} $BASENAME"

    # Check if output already exists
    if [ -f "$OUTPUT_FILE" ]; then
        echo -e "${YELLOW}⚠ Output file already exists, skipping${NC}"
        continue
    fi

    # FFmpeg conversion
    # -i: input file
    # -c:v libx264: H.264 video codec
    # -pix_fmt yuv420p: 8-bit 4:2:0 (DaVinci compatible)
    # -preset slow: Better quality/compression (can use 'medium' for speed)
    # -crf 18: High quality (lower = better, 18 = visually lossless)
    # -c:a aac: AAC audio codec
    # -b:a 320k: High quality audio bitrate
    # -movflags +faststart: Optimize for streaming/editing

    if ffmpeg -i "$VIDEO" \
        -c:v libx264 \
        -pix_fmt yuv420p \
        -preset slow \
        -crf 18 \
        -c:a aac \
        -b:a 320k \
        -movflags +faststart \
        "$OUTPUT_FILE" \
        -y 2>&1 | grep -E "frame=|error|Error"; then

        echo -e "${GREEN}✓ Successfully converted${NC}"
        ((CONVERTED++))
    else
        echo -e "${RED}✗ Conversion failed${NC}"
        ((FAILED++))
    fi
    echo ""
done

# Summary
echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Conversion Summary${NC}                         ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}✓ Converted:${NC} $CONVERTED"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}✗ Failed:${NC} $FAILED"
fi
echo ""
echo -e "${CYAN}Output files saved to:${NC} $OUTPUT_DIR"
echo -e "${YELLOW}Import the .mov files into DaVinci Resolve${NC}"

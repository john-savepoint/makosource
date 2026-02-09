#!/bin/bash
#
# Script: convert_cosmos_to_h_drive.sh
# Created: 2026-01-30 23:45 JST
# Context: Convert Cosmos FMV30 videos while preserving directory structure
#          Copy to H:/ff7 movies for DaVinci Resolve editing
# Session: 51d0bc48-c27b-4af4-bfd3-4467a1802597
#
# Source: D:/Games/Stand-alone/FF7Modding/cosmos_fmv30 (117 .avi files, ~2.7GB)
# Target: H:/ff7 movies (maintaining subdirectory structure)
#
# Converts:
#   - 10-bit H.264 → 8-bit H.264 (DaVinci compatible)
#   - Vorbis audio → AAC 320kbps
#   - .avi (MKV container) → .mov (QuickTime)
#
# Estimated time: 30-60 minutes (117 files)

# No set -e - handle errors manually to prevent premature script exit

# Color codes
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
GRAY='\033[90m'
NC='\033[0m'

SOURCE_BASE="/mnt/d/Games/Stand-alone/FF7Modding/cosmos_fmv30"
TARGET_BASE="/mnt/h/ff7 movies"

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Cosmos FMV30 → H:/ff7 movies Conversion${NC}                  ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Source:${NC} $SOURCE_BASE"
echo -e "${CYAN}Target:${NC} $TARGET_BASE"
echo ""

# Create target base directory
mkdir -p "$TARGET_BASE"

# Find all .avi files with full paths
mapfile -t VIDEO_FILES < <(find "$SOURCE_BASE" -type f -name "*.avi")

TOTAL=${#VIDEO_FILES[@]}
echo -e "${GREEN}Found $TOTAL video files to convert${NC}"
echo -e "${YELLOW}Estimated time: 30-60 minutes${NC}"
echo ""

# Ask for confirmation
read -p "Start conversion? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Conversion cancelled${NC}"
    exit 0
fi

echo ""

# Counters
CONVERTED=0
SKIPPED=0
FAILED=0
START_TIME=$(date +%s)

# Process each file
for i in "${!VIDEO_FILES[@]}"; do
    VIDEO="${VIDEO_FILES[$i]}"

    # Calculate relative path from source base
    REL_PATH="${VIDEO#$SOURCE_BASE/}"
    REL_DIR=$(dirname "$REL_PATH")
    BASENAME=$(basename "$VIDEO" .avi)

    # Create target directory structure
    TARGET_DIR="$TARGET_BASE/$REL_DIR"
    mkdir -p "$TARGET_DIR"

    OUTPUT_FILE="$TARGET_DIR/${BASENAME}.mov"

    # Progress header
    CURRENT=$((i + 1))
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}[$CURRENT/$TOTAL]${NC} ${BASENAME}"
    echo -e "${GRAY}Path: $REL_DIR${NC}"

    # Check if already exists
    if [ -f "$OUTPUT_FILE" ]; then
        echo -e "${YELLOW}⚠ Already exists, skipping${NC}"
        ((SKIPPED++))
        echo ""
        continue
    fi

    # FFmpeg conversion with progress suppression (only show errors)
    ffmpeg -i "$VIDEO" \
        -c:v libx264 \
        -pix_fmt yuv420p \
        -preset medium \
        -crf 18 \
        -c:a aac \
        -b:a 320k \
        -movflags +faststart \
        "$OUTPUT_FILE" \
        -y \
        -loglevel error \
        -stats 2>&1

    FFMPEG_EXIT=$?

    if [ $FFMPEG_EXIT -eq 0 ]; then
        echo -e "${GREEN}✓ Converted successfully${NC}"
        ((CONVERTED++))
    else
        echo -e "${RED}✗ Conversion failed (exit code: $FFMPEG_EXIT)${NC}"
        ((FAILED++))
    fi

    # Show running stats every 10 files
    if [ $((CURRENT % 10)) -eq 0 ]; then
        ELAPSED=$(($(date +%s) - START_TIME))
        AVG_TIME=$((ELAPSED / CURRENT))
        REMAINING=$(((TOTAL - CURRENT) * AVG_TIME))

        echo ""
        echo -e "${CYAN}⏱ Progress: $CURRENT/$TOTAL | Elapsed: ${ELAPSED}s | Est. remaining: ${REMAINING}s${NC}"
    fi

    echo ""
done

# Final summary
END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
MINUTES=$((TOTAL_TIME / 60))
SECONDS=$((TOTAL_TIME % 60))

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${YELLOW}Conversion Complete${NC}                                      ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}✓ Converted:${NC} $CONVERTED files"
if [ $SKIPPED -gt 0 ]; then
    echo -e "${YELLOW}⚠ Skipped:${NC} $SKIPPED files (already existed)"
fi
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}✗ Failed:${NC} $FAILED files"
fi
echo -e "${CYAN}⏱ Total time:${NC} ${MINUTES}m ${SECONDS}s"
echo ""
echo -e "${CYAN}Output location:${NC} $TARGET_BASE"
echo -e "${YELLOW}Ready to import into DaVinci Resolve${NC}"

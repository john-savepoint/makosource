#!/usr/bin/env python3
"""
Extract Clean German String Candidates
=======================================
Created: 2026-01-05 17:01 JST (Monday)
Session-ID: c5687d3e-90a9-47e8-829a-a0c6e70cd98e

Extract German strings from exe, filtering out obvious garbage:
- Binary noise
- Excessive padding/spaces
- Control characters
- Non-text data

Keep only strings that look like actual menu text.
"""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ff7_german_decoder import decode_ff7_german

def is_obvious_trash(text: str) -> bool:
    """
    Detect obvious garbage strings.

    Returns True if string should be REMOVED.
    """
    if not text or len(text.strip()) == 0:
        return True  # Empty or all spaces

    # Strip for analysis
    stripped = text.strip()

    # Too short after stripping (single char strings are likely noise)
    if len(stripped) < 2:
        return True

    # Count different character types
    alpha_count = sum(1 for c in stripped if c.isalpha())
    space_count = sum(1 for c in stripped if c == ' ')
    special_count = sum(1 for c in stripped if not c.isalnum() and c != ' ')
    total = len(stripped)

    # Must have at least SOME letters
    if alpha_count == 0:
        return True

    # If more than 50% special characters, it's trash
    if special_count / total > 0.5:
        return True

    # Check for patterns that indicate garbage
    trash_patterns = [
        r'[@\^\$`]{3,}',  # Multiple control-looking chars
        r'[A-Z]{10,}',     # Long runs of capitals (likely not real text)
        r'\s{10,}',        # Excessive spaces
        r'[°•£]{2,}',      # Multiple special symbols
        r'^[!"\#\$%&\'\(\)\*\+,\-\./:;<=>\?@\[\\\]\^_`\{\|\}~\s]+$',  # Only punctuation/symbols
    ]

    for pattern in trash_patterns:
        if re.search(pattern, text):
            return True

    # If text has very low letter-to-total ratio, it's trash
    letter_ratio = alpha_count / total
    if letter_ratio < 0.3:
        return True

    return False

def extract_clean_german_strings(exe_path: str, start_offset: int, end_offset: int):
    """
    Extract German strings, filtering obvious trash.

    Returns list of (offset, decoded_text) tuples
    """
    with open(exe_path, 'rb') as f:
        f.seek(start_offset)
        region = f.read(end_offset - start_offset)

    strings = []
    current_bytes = []
    string_start = 0

    for i, byte in enumerate(region):
        if byte == 0xFF:
            # Found terminator
            if current_bytes:
                offset = start_offset + string_start
                decoded = decode_ff7_german(bytes(current_bytes), show_unknown=False)

                # Filter out obvious trash
                if not is_obvious_trash(decoded):
                    strings.append((offset, decoded.strip()))

            # Reset for next string
            current_bytes = []
            string_start = i + 1
        else:
            if not current_bytes:
                string_start = i
            current_bytes.append(byte)

    return strings

def main():
    exe_path = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

    print("=" * 80)
    print("Extracting Clean German String Candidates")
    print("=" * 80)
    print(f"Source: {exe_path}")
    print(f"Region: 0x58FB00 - 0x5A0000 (menu strings)")
    print()

    # Extract from main menu region
    print("Extracting strings...")
    strings = extract_clean_german_strings(exe_path, 0x58FB00, 0x5A0000)

    print(f"Found {len(strings)} clean candidate strings")
    print()
    print("First 100 candidates:")
    print("=" * 80)

    for i, (offset, text) in enumerate(strings[:100]):
        print(f"[{i:4d}] 0x{offset:06X} | {text[:70]}")

    if len(strings) > 100:
        print(f"\n... and {len(strings) - 100} more")

    # Save to file
    output_file = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/german_clean_candidates.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Clean String Candidates\n")
        f.write(f"# Source: {exe_path}\n")
        f.write(f"# Region: 0x58FB00 - 0x5A0000\n")
        f.write(f"# Total candidates: {len(strings)}\n")
        f.write("# Format: [INDEX] OFFSET | TEXT\n")
        f.write("=" * 80 + "\n\n")

        for i, (offset, text) in enumerate(strings):
            f.write(f"[{i:4d}] 0x{offset:06X} | {text}\n")

    print(f"\nFull list saved to: {output_file}")

    # Also save as CSV for easier processing
    csv_file = output_file.with_suffix('.csv')
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("index,offset,text\n")
        for i, (offset, text) in enumerate(strings):
            # Escape quotes in text
            escaped_text = text.replace('"', '""')
            f.write(f"{i},0x{offset:06X},\"{escaped_text}\"\n")

    print(f"CSV format saved to: {csv_file}")

if __name__ == '__main__':
    main()

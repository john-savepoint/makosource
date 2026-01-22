#!/usr/bin/env python3
"""
FF7 German Offset Delta Pattern Analysis
=========================================

Created: 2026-01-02 18:45 JST
Session: AGENT-3-GERMAN-DELTA-ANALYSIS
Context: Analyze why German strings have NO FIXED DELTA from English strings.
         Japanese exe has simple +0xC00 delta. German has varying deltas because
         German text is LONGER than English (more bytes = shifted offsets).

Purpose:
- For each touphScript offset (Steam EN), add 0xC00 to get eStore EN offset
- Search for same bytes in eStore DE
- Calculate delta between eStore EN and eStore DE positions
- Document the delta pattern by region
- Identify anchor pairs (identical EN/DE strings like "ATB", "HP", "MP")

Source Files:
- eStore EN exe: /mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe (24MB)
- eStore DE exe: /mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe (24MB)
- Steam EN exe: /mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe (6MB) - HEXT target

Constants:
- STEAM_TO_ESTORE_DELTA = 0xC00 (Steam EN to eStore EN)
- touphScript offsets are for Steam exe
"""

import sys
import csv
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple

# Import touphScript offsets
sys.path.insert(0, str(Path(__file__).parent))
from generate_exe_hext import EN_OFFSETS, STRING_LENGTHS, STRING_TYPES

# File paths
STEAM_EN = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
ESTORE_EN = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe")
ESTORE_DE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe")

# Constants
STEAM_TO_ESTORE_DELTA = 0xC00  # Steam offsets + 0xC00 = eStore offsets


def decode_ff7(data: bytes, german: bool = False) -> str:
    """Decode FF7-encoded bytes to readable text."""
    result = []
    i = 0
    while i < len(data):
        b = data[i]
        if b == 0xFF:
            break
        if b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))
        elif german:
            # German umlauts
            if b == 0x6A:
                result.append('ä')
            elif b == 0x7A:
                result.append('ö')
            elif b == 0x7E:
                result.append('ß')
            elif b == 0x7F:
                result.append('ü')
            else:
                result.append(f'[{b:02X}]')
        else:
            result.append(f'[{b:02X}]')
        i += 1
    return ''.join(result).strip()


def find_bytes_in_data(data: bytes, search_bytes: bytes, start: int = 0x500000, end: int = 0x5C0000) -> List[int]:
    """Find all occurrences of search_bytes in data within range."""
    matches = []
    pos = start
    while pos < end:
        found = data.find(search_bytes, pos, end)
        if found == -1:
            break
        matches.append(found)
        pos = found + 1
    return matches


@dataclass
class DeltaEntry:
    """Represents delta analysis for one string."""
    index: int
    steam_offset: int
    estore_en_offset: int
    estore_de_offset: Optional[int]
    delta: Optional[int]
    en_text: str
    de_text: Optional[str]
    en_bytes_hex: str
    match_type: str  # "exact", "partial", "not_found"
    notes: str


def analyze_deltas() -> List[DeltaEntry]:
    """Analyze delta patterns between eStore EN and DE executables."""

    # Load executables
    print("Loading executables...")
    with open(ESTORE_EN, 'rb') as f:
        en_data = f.read()
    with open(ESTORE_DE, 'rb') as f:
        de_data = f.read()

    print(f"  eStore EN: {len(en_data):,} bytes")
    print(f"  eStore DE: {len(de_data):,} bytes")
    print()

    results = []

    # Analyze first N strings
    max_strings = min(200, len(EN_OFFSETS))
    print(f"Analyzing {max_strings} strings...")
    print("-" * 80)

    for idx in range(max_strings):
        steam_offset = EN_OFFSETS[idx]
        length = STRING_LENGTHS[idx] if idx < len(STRING_LENGTHS) else 20

        # Calculate eStore EN offset
        estore_en_offset = steam_offset + STEAM_TO_ESTORE_DELTA

        # Read EN bytes
        en_bytes = en_data[estore_en_offset:estore_en_offset + length]
        en_text = decode_ff7(en_bytes)
        en_bytes_hex = en_bytes[:16].hex().upper()  # First 16 bytes for display

        # Find terminator
        ff_pos = en_bytes.find(b'\xff')
        if ff_pos > 0:
            search_bytes = en_bytes[:ff_pos + 1]
        else:
            search_bytes = en_bytes[:min(8, len(en_bytes))]  # Search first 8 bytes

        # Search for these bytes in DE exe
        matches = find_bytes_in_data(de_data, search_bytes)

        if matches:
            # Use first match
            de_offset = matches[0]
            delta = de_offset - estore_en_offset

            # Read DE bytes for comparison
            de_bytes = de_data[de_offset:de_offset + length]
            de_text = decode_ff7(de_bytes, german=True)

            match_type = "exact" if len(matches) == 1 else f"multi({len(matches)})"
            notes = ""

            results.append(DeltaEntry(
                index=idx,
                steam_offset=steam_offset,
                estore_en_offset=estore_en_offset,
                estore_de_offset=de_offset,
                delta=delta,
                en_text=en_text,
                de_text=de_text,
                en_bytes_hex=en_bytes_hex,
                match_type=match_type,
                notes=notes
            ))

            print(f"[{idx:3d}] EN:0x{estore_en_offset:06X} DE:0x{de_offset:06X} Δ={delta:+6d} ({delta:+#06x}) | {en_text[:20]}")
        else:
            # Not found - this string was localized (different text)
            results.append(DeltaEntry(
                index=idx,
                steam_offset=steam_offset,
                estore_en_offset=estore_en_offset,
                estore_de_offset=None,
                delta=None,
                en_text=en_text,
                de_text=None,
                en_bytes_hex=en_bytes_hex,
                match_type="not_found",
                notes="Localized - different text in German"
            ))

            print(f"[{idx:3d}] EN:0x{estore_en_offset:06X} DE:????????? Δ=?????? | {en_text[:20]} [LOCALIZED]")

    return results


def identify_anchor_strings(results: List[DeltaEntry]) -> List[DeltaEntry]:
    """Identify strings that are identical in EN and DE (good anchors)."""
    anchors = []
    for r in results:
        if r.match_type.startswith("exact") and r.delta is not None:
            # These are potentially identical strings
            anchors.append(r)
    return anchors


def analyze_regions(results: List[DeltaEntry]) -> dict:
    """Analyze delta patterns by region."""
    regions = {
        "quit_dialog": (0, 5),
        "config_menu": (5, 33),
        "rgb_labels": (33, 38),
        "main_menu": (38, 58),
        "keyboard_config": (58, 77),
        "keyboard_labels_rgb": (77, 214),
        "status_screen": (214, 280),
        "battle_menu": (280, 350),
        "materia_menu": (350, 420),
        "shop_menu": (420, 460),
        "name_entry_unicode": (461, 529),
        "post_name_entry": (529, 600),
        "late_strings": (600, 700),
    }

    region_analysis = {}

    for region_name, (start, end) in regions.items():
        region_results = [r for r in results if start <= r.index < end]
        if not region_results:
            continue

        found_deltas = [r.delta for r in region_results if r.delta is not None]
        not_found_count = len([r for r in region_results if r.delta is None])

        if found_deltas:
            min_delta = min(found_deltas)
            max_delta = max(found_deltas)
            avg_delta = sum(found_deltas) / len(found_deltas)
            variance = max_delta - min_delta
        else:
            min_delta = max_delta = avg_delta = variance = None

        region_analysis[region_name] = {
            "range": (start, end),
            "total_strings": len(region_results),
            "found_count": len(found_deltas),
            "not_found_count": not_found_count,
            "min_delta": min_delta,
            "max_delta": max_delta,
            "avg_delta": avg_delta,
            "variance": variance
        }

    return region_analysis


def generate_report(results: List[DeltaEntry], region_analysis: dict, output_path: Path):
    """Generate markdown report with analysis."""

    anchors = identify_anchor_strings(results)

    # Determine consistent delta ranges
    found_deltas = [(r.index, r.delta) for r in results if r.delta is not None]

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# German Offset Delta Pattern Analysis\n\n")
        f.write(f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n\n")
        f.write("## Executive Summary\n\n")
        f.write("Japanese exe has a simple +0xC00 delta from English offsets because the strings\n")
        f.write("are the same length (just different encoding). German has NO FIXED DELTA because\n")
        f.write("German text is generally LONGER than English, causing subsequent strings to shift.\n\n")

        # Key findings
        f.write("## Key Findings\n\n")
        if found_deltas:
            all_deltas = [d for _, d in found_deltas]
            f.write(f"- **Delta Range:** {min(all_deltas):+d} to {max(all_deltas):+d}\n")
            f.write(f"- **Average Delta:** {sum(all_deltas)/len(all_deltas):+.1f}\n")
            f.write(f"- **Strings Analyzed:** {len(results)}\n")
            f.write(f"- **Exact Matches Found:** {len(found_deltas)}\n")
            f.write(f"- **Localized (Not Found):** {len(results) - len(found_deltas)}\n")
            f.write(f"- **Potential Anchors:** {len(anchors)}\n")
        f.write("\n")

        # Region analysis
        f.write("## Region-by-Region Delta Analysis\n\n")
        f.write("| Region | Range | Strings | Found | Δ Min | Δ Max | Δ Avg | Variance | Notes |\n")
        f.write("|--------|-------|---------|-------|-------|-------|-------|----------|-------|\n")

        for region_name, data in region_analysis.items():
            start, end = data["range"]
            total = data["total_strings"]
            found = data["found_count"]
            not_found = data["not_found_count"]

            if data["min_delta"] is not None:
                min_d = f"{data['min_delta']:+d}"
                max_d = f"{data['max_delta']:+d}"
                avg_d = f"{data['avg_delta']:+.0f}"
                var = f"{data['variance']}"
            else:
                min_d = max_d = avg_d = var = "N/A"

            notes = ""
            if not_found > found:
                notes = "Mostly localized"
            elif data["variance"] and data["variance"] == 0:
                notes = "CONSISTENT delta!"
            elif data["variance"] and data["variance"] < 100:
                notes = "Low variance"
            elif data["variance"] and data["variance"] > 1000:
                notes = "HIGH variance"

            f.write(f"| {region_name} | {start}-{end} | {total} | {found} | {min_d} | {max_d} | {avg_d} | {var} | {notes} |\n")

        f.write("\n")

        # Anchor strings
        f.write("## Anchor Strings (Identical EN/DE)\n\n")
        f.write("These strings are identical in English and German, making them reliable anchors\n")
        f.write("for finding German strings in the DE exe:\n\n")
        f.write("| Idx | EN Offset | DE Offset | Delta | Text |\n")
        f.write("|-----|-----------|-----------|-------|------|\n")

        for r in anchors[:50]:  # First 50 anchors
            if r.delta is not None:
                f.write(f"| {r.index} | 0x{r.estore_en_offset:06X} | 0x{r.estore_de_offset:06X} | {r.delta:+d} | {r.en_text[:30]} |\n")

        f.write("\n")

        # Delta visualization
        f.write("## Delta Progression Visualization\n\n")
        f.write("```\n")
        f.write("Index | Delta (relative to 0)\n")
        f.write("------+-----------------------------------------------\n")

        # Create ASCII chart
        for r in results[:100]:
            if r.delta is not None:
                # Scale delta to fit in 50 chars
                max_delta = max(abs(d) for _, d in found_deltas[:100] if d is not None)
                if max_delta > 0:
                    scaled = int((r.delta / max_delta) * 25) + 25  # -25 to +25 -> 0 to 50
                    scaled = max(0, min(50, scaled))
                else:
                    scaled = 25
                bar = '.' * 25 + '|' + '.' * 25
                bar = bar[:scaled] + '*' + bar[scaled+1:]
                f.write(f"{r.index:5d} | {bar} {r.delta:+6d}\n")
            else:
                f.write(f"{r.index:5d} | {'?' * 51} LOCALIZED\n")

        f.write("```\n\n")

        # Full data table
        f.write("## Complete Delta Data\n\n")
        f.write("| Idx | Steam | eStore EN | eStore DE | Delta | Match | EN Text |\n")
        f.write("|-----|-------|-----------|-----------|-------|-------|------|\n")

        for r in results:
            de_off = f"0x{r.estore_de_offset:06X}" if r.estore_de_offset else "N/A"
            delta = f"{r.delta:+d}" if r.delta is not None else "N/A"
            f.write(f"| {r.index} | 0x{r.steam_offset:06X} | 0x{r.estore_en_offset:06X} | {de_off} | {delta} | {r.match_type} | {r.en_text[:25]} |\n")

        f.write("\n")

        # Recommendations
        f.write("## Strategy Recommendations\n\n")
        f.write("### Approach 1: Anchor-Based Search\n")
        f.write("1. Use anchor strings (identical EN/DE) to establish region deltas\n")
        f.write("2. For localized strings, search by German translation text\n")
        f.write("3. Use EN->DE translation dictionary to find German equivalents\n\n")

        f.write("### Approach 2: Binary Pattern Matching\n")
        f.write("1. For each touphScript index, read EN bytes\n")
        f.write("2. Search for those bytes in DE exe (may find match if unchanged)\n")
        f.write("3. If not found, search for German translation bytes\n")
        f.write("4. Use closest anchor's delta as starting point for search\n\n")

        f.write("### Approach 3: Region-Based Delta\n")
        f.write("1. Establish average delta per region\n")
        f.write("2. Search within +/- variance of expected position\n")
        f.write("3. Verify by decoding and comparing to expected German text\n")

    print(f"\nReport saved to: {output_path}")


def main():
    print("=" * 80)
    print("FF7 German Offset Delta Pattern Analysis")
    print("=" * 80)
    print()

    # Check files exist
    for path in [ESTORE_EN, ESTORE_DE]:
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            return

    # Run analysis
    results = analyze_deltas()

    print()
    print("=" * 80)
    print("Region Analysis")
    print("=" * 80)

    region_analysis = analyze_regions(results)
    for region_name, data in region_analysis.items():
        print(f"\n{region_name}:")
        print(f"  Strings: {data['total_strings']}, Found: {data['found_count']}, Not Found: {data['not_found_count']}")
        if data['min_delta'] is not None:
            print(f"  Delta: {data['min_delta']:+d} to {data['max_delta']:+d} (variance: {data['variance']})")

    # Generate report
    output_path = Path("/home/johnzealanddoyle/projects/ff7OG_japanese/data/german_offset_delta_analysis.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_report(results, region_analysis, output_path)

    # Also save raw data as CSV
    csv_path = output_path.with_suffix('.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'steam_offset', 'estore_en_offset', 'estore_de_offset',
                        'delta', 'match_type', 'en_text', 'de_text', 'en_bytes_hex'])
        for r in results:
            writer.writerow([
                r.index,
                f"0x{r.steam_offset:06X}",
                f"0x{r.estore_en_offset:06X}",
                f"0x{r.estore_de_offset:06X}" if r.estore_de_offset else "",
                r.delta if r.delta is not None else "",
                r.match_type,
                r.en_text,
                r.de_text if r.de_text else "",
                r.en_bytes_hex
            ])
    print(f"CSV data saved to: {csv_path}")


if __name__ == "__main__":
    main()

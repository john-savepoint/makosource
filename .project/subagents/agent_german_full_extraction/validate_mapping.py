#!/usr/bin/env python3
"""
Validate the English-German semantic mapping file.
Checks for completeness, duplicates, and quality issues.
"""

import csv
from collections import defaultdict

def validate_mapping(filepath):
    """Validate mapping file and report issues."""

    print("=" * 70)
    print("  SEMANTIC MAPPING VALIDATION")
    print("=" * 70)

    # Storage
    mappings = []
    en_indices = set()
    de_offsets = defaultdict(list)
    confidence_counts = defaultdict(int)
    missing_de_text = []

    # Read mappings
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            mappings.append(row)
            en_idx = int(row['en_index'])
            en_indices.add(en_idx)

            de_offset = row['de_offset']
            if de_offset:
                de_offsets[de_offset].append(en_idx)

            confidence = row['confidence']
            confidence_counts[confidence] += 1

            if not row['de_text'] or row['de_text'].strip() == '':
                missing_de_text.append(en_idx)

    # Validation checks
    print("\n📊 BASIC STATISTICS")
    print("-" * 70)
    print(f"  Total mappings: {len(mappings)}")
    print(f"  Expected: 767 (indices 0-766)")
    print(f"  Status: {'✅ PASS' if len(mappings) == 767 else '❌ FAIL'}")

    # Check index continuity
    print("\n📋 INDEX CONTINUITY")
    print("-" * 70)
    expected_indices = set(range(767))
    missing_indices = expected_indices - en_indices
    extra_indices = en_indices - expected_indices

    if missing_indices:
        print(f"  ❌ Missing indices: {sorted(missing_indices)[:20]}")
        if len(missing_indices) > 20:
            print(f"     ... and {len(missing_indices) - 20} more")
    else:
        print("  ✅ All indices present (0-766)")

    if extra_indices:
        print(f"  ⚠️  Extra indices: {sorted(extra_indices)}")
    else:
        print("  ✅ No extra indices")

    # Check German text completeness
    print("\n📝 GERMAN TEXT COMPLETENESS")
    print("-" * 70)
    if missing_de_text:
        print(f"  ❌ Missing German text for {len(missing_de_text)} entries:")
        print(f"     Indices: {missing_de_text[:20]}")
        if len(missing_de_text) > 20:
            print(f"     ... and {len(missing_de_text) - 20} more")
    else:
        print("  ✅ All entries have German text")

    # Check for duplicate German offsets
    print("\n🔄 DUPLICATE GERMAN OFFSETS")
    print("-" * 70)
    duplicates = {offset: indices for offset, indices in de_offsets.items() if len(indices) > 1}
    if duplicates:
        print(f"  ⚠️  Found {len(duplicates)} German offsets used multiple times:")
        for offset, indices in list(duplicates.items())[:10]:
            print(f"     {offset}: used by EN indices {indices}")
        if len(duplicates) > 10:
            print(f"     ... and {len(duplicates) - 10} more")
    else:
        print("  ✅ No duplicate German offsets")

    # Confidence distribution
    print("\n📈 CONFIDENCE DISTRIBUTION")
    print("-" * 70)
    total = len(mappings)
    for conf in ['exact', 'high', 'medium', 'low', 'none']:
        count = confidence_counts.get(conf, 0)
        pct = (count / total * 100) if total > 0 else 0
        bar_length = int(pct / 2.5)  # Scale to fit in 40 chars max
        bar = "█" * bar_length
        print(f"  {conf:10s}: {count:4d} ({pct:5.1f}%) {bar}")

    # Quality score
    print("\n⭐ OVERALL QUALITY SCORE")
    print("-" * 70)

    quality_score = 0
    max_score = 100

    # Completeness (40 points)
    if len(mappings) == 767:
        quality_score += 40
    elif len(mappings) >= 760:
        quality_score += 30
    elif len(mappings) >= 700:
        quality_score += 20

    # German text presence (20 points)
    if not missing_de_text:
        quality_score += 20
    elif len(missing_de_text) < 10:
        quality_score += 15
    elif len(missing_de_text) < 50:
        quality_score += 10

    # Confidence distribution (40 points)
    exact_pct = confidence_counts.get('exact', 0) / total * 100 if total > 0 else 0
    high_pct = confidence_counts.get('high', 0) / total * 100 if total > 0 else 0

    if exact_pct >= 75:
        quality_score += 30
    elif exact_pct >= 60:
        quality_score += 20
    elif exact_pct >= 40:
        quality_score += 10

    if exact_pct + high_pct >= 95:
        quality_score += 10
    elif exact_pct + high_pct >= 85:
        quality_score += 5

    print(f"  Quality Score: {quality_score}/{max_score}")
    print(f"  Rating: ", end="")

    if quality_score >= 95:
        print("🌟🌟🌟🌟🌟 EXCELLENT")
    elif quality_score >= 85:
        print("🌟🌟🌟🌟 VERY GOOD")
    elif quality_score >= 75:
        print("🌟🌟🌟 GOOD")
    elif quality_score >= 60:
        print("🌟🌟 FAIR")
    else:
        print("🌟 NEEDS IMPROVEMENT")

    # Sample verification
    print("\n🔍 SAMPLE VERIFICATION (First 10 mappings)")
    print("-" * 70)
    print(f"{'Idx':<5} {'English':<35} {'German':<25} {'Conf':<7}")
    print("-" * 70)

    for i, row in enumerate(mappings[:10]):
        idx = row['en_index']
        en_text = row['en_text'][:34]
        de_text = row['de_text'][:24]
        conf = row['confidence']
        print(f"{idx:<5} {en_text:<35} {de_text:<25} {conf:<7}")

    print("\n" + "=" * 70)
    print("  VALIDATION COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    validate_mapping('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction/english_german_semantic_mapping.csv')

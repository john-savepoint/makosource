#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator v5

Direct extraction approach:
1. For each touphScript offset, get Steam EN string
2. Find matching German string in DE exe by searching
3. Extract DE bytes and write to Steam VA

Created: 2026-01-02 17:30 JST
Session: 2e703ab4-4b5e-4772-8894-ba089b4f437c
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from generate_exe_hext import EN_OFFSETS, STRING_LENGTHS, STRING_TYPES

# File paths
STEAM_EN = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
DE_EXE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Skip regions (same as Japanese)
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals
SKIP_REGIONS.update(range(712, 758))   # Chocobo names

# Keyboard region - skip for now (needs special handling)
SKIP_REGIONS.update(range(77, 214))    # Keyboard labels


def decode_ff7(data):
    """Decode FF7-encoded bytes to readable text."""
    result = []
    for b in data:
        if b == 0xFF: break
        if b == 0x00: result.append(' ')
        elif 0x01 <= b <= 0x9F: result.append(chr(b + 0x20))
        else: result.append('[%02X]' % b)
    return ''.join(result)


def ff7_encode(text):
    """Encode ASCII text to FF7 bytes."""
    result = []
    for c in text:
        if c == ' ':
            result.append(0x00)
        elif ord(c) >= 0x21 and ord(c) <= 0x7E:
            result.append(ord(c) - 0x20)
    return bytes(result)


def file_offset_to_va(offset):
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def find_de_string(de_data, search_text, start=0x580000, end=0x5C0000, max_extra=5):
    """Find a German string in DE exe and return full bytes including terminator.

    max_extra: Maximum extra bytes beyond search text length (to allow for terminator).
               This prevents matching "Beenden" when we want just "Beenden" but find
               "Beenden Richtungstaste..." which is much longer.
    """
    search = ff7_encode(search_text)
    if len(search) < 2:
        return None

    # Search for all occurrences and find the best match (shortest one that starts with search)
    pos = start
    best_match = None
    best_len = 999

    while pos < end:
        found = de_data.find(search, pos, end)
        if found == -1:
            break

        # Find terminator
        ff_pos = de_data.find(b'\xff', found)
        if ff_pos != -1 and ff_pos <= found + 100:
            match_bytes = de_data[found:ff_pos + 1]
            match_len = len(match_bytes)

            # Prefer shorter matches (closer to exact match)
            # Allow up to max_extra bytes beyond search length + 1 (for terminator)
            if match_len < best_len:
                # Only accept if it's reasonably close to expected length
                if match_len <= len(search) + max_extra + 1:
                    best_match = match_bytes
                    best_len = match_len
                elif best_match is None:
                    # If no good match yet, take this one but it might be truncated later
                    best_match = match_bytes
                    best_len = match_len

        pos = found + 1

    return best_match


# Direct byte mappings for strings with special characters (umlauts)
# Format: EN text -> (DE offset in DE exe, max search length)
# Use tuples (offset, length) for direct extraction when search fails
DIRECT_DE_OFFSETS = {
    # Quit dialog - these have umlauts so need direct extraction
    # The DE quit dialog is structured differently than EN:
    # DE Line 1: "Möchten Sie Final" (0x58FBB0)
    # DE Line 2: "Fantasy VII verlassen und" (0x58FBCE)
    # DE Line 3: "zu Windows zurückkehren?" (0x58FBEA)
    # EN Line 1: "Do you want to quit"
    # EN Line 2: "playing Final Fantasy VII"
    # EN Line 3: "and return to Windows?"
    "Do you want to quit": (0x58FBB0, 20),  # Möchten Sie Final
    "playing Final Fantasy VII": (0x58FBCE, 30),  # Fantasy VII verlassen und
    "and return to Windows?": (0x58FBEA, 30),  # zu Windows zurückkehren?

    # Select with ä - Auswählen at 0x5902D6
    "Select": (0x5902D6, 12),

    # Menu with ü - Menü at 0x590342
    "Menu": (0x590342, 6),

    # Beginner - Einsteiger
    "Beginner": (0x590D6A, 12),

    # next level - nächster Lv (has ä)
    "next level": (0x590D94, 15),

    # LEVEL UP - STUFE HOCH
    "LEVEL UP": (0x590DF4, 12),
}

# Manual mapping: EN text -> DE search text
# This handles cases where simple content matching doesn't work
EN_TO_DE_MAP = {
    # Quit dialog (indices 0-4)
    "Yes": "Ja",
    "No": "Nein",

    # Config menu (indices 5-32)
    "Window color": "Fensterfarbe",
    "Sound": "Sound",
    "Controller": "Kontroller",
    "Cursor": "Cursor",
    "ATB": "ATB",
    "Battle speed": "Kampftempo",
    "Battle message": "Kampfmeldung",
    "Field message": "Feldmeldung",
    "Camera angle": "Kamerawinkel",
    "Cancel": "Abbrechen",
    "Normal": "Normal",
    "Customize": "Benutzerdefiniert",
    "Initial": "Anfang",
    "Memory": "Speicher",
    "Active": "Aktiv",
    "Recommended": "Empfohlen",
    "Wait": "Warten",
    "Auto": "Auto",
    "Fixed": "Fest",
    "Slow": "Langs.",
    "Fast": "Schn.",
    "Magic order": "Zauberfolge",
    "restore": "Heilung",
    "attack": "Angriff",
    "indirect": "Indirekt",
    "No.": "Nr.",

    # Main menu (indices 38-48)
    "Item": "Objekt",
    "Magic": "Magie",
    "Materia": "Materia",
    "Equip": "Ausrusten",
    "Status": "Werte",  # Status screen shows "Werte"
    "Order": "Ordnen",
    "Limit": "Limit",
    "Config": "Konfig",
    "PHS": "PHS",
    "Save": "Speichern",
    "Quit": "Beenden",

    # Other strings
    "Beginner": "Einsteiger",
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nachster Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "LEVEL UP": "STUFE HOCH",
    "Fury": "Zorn",
    "Sadness": "Trauer",

    # Stats - these appear in status screen
    "Strength": "Starke",
    "Vitality": "Vitalitat",
    "Dexterity": "Geschick",
    "Luck": "Gluck",
    "Attack": "Angriff",
    "Defense": "Verteidigung",
    "Attack%": "Angriff%",
    "Defense%": "Verteidigung%",
    "Magic": "Zauber",
    "Spirit": "Moral",  # Gemüt shows as Moral sometimes
    "MagicDef": "Zbrvertdg",
    "MagicDef%": "Zbrvertdg%",

    # Equipment
    "Weapon": "Waffe",
    "Armor": "Rustung",
    "Accessory": "Accessoire",
    "Slot": "Fassung:",
    "Growth": "Wachstum:",

    # Elements
    "Fire": "Feuer",
    "Ice": "Kalte",  # Kälte
    "Lightning": "Blitz",
    "Earth": "Erde",
    "Poison": "Gift",
    "Gravity": "Schwerkraft",
    "Water": "Wasser",
    "Wind": "Wind",
    "Holy": "Heilig",

    # Status effects
    "Death": "Tod",
    "Near-death": "Beinahe Tod",
    "Sleep": "Sleep",
    "Confusion": "Verwirrung",
    "Silence": "Stummheit",
    "Haste": "Schnell",
    "Stop": "Stop",
    "Frog": "Frosch",
    "Small": "Zwerg",
    "Manipulate": "Manipul.",
    "Berserk": "Tollwut",
    "Petrify": "Verstein.",
    "Reflect": "Reflektieren",
    "Death-sentence": "Todesurteil",
    "Barrier": "Barriere",
    "MBarrier": "ZBarr.",
    "Shield": "Schild",
    "Regen": "Regen",
    "Resist": "Allmacht",

    # Battle/Item menu
    "Use": "Verwenden",
    "Arrange": "Ordnen",
    "Key Items": "Schlusselobjekte",
    "HP": "HP",
    "MP": "MP",
    "EXP": "EXP",
    "AP": "AP",

    # Shop
    "Buy": "Kaufen",
    "Sell": "Verkaufen",
    "Exit": "Beenden",
    "Welcome!": "Willkommen!",

    # Materia
    "Check": "Prufen",
    "Exchange": "Tauschen",
    "Trash": "Entsorgen",

    # Limit
    "Set": "Einrichten",
    "LEVEL": "STUFE",
    "LEVEL 1": "STUFE 1",
    "LEVEL 2": "STUFE 2",
    "LEVEL 3": "STUFE 3",
    "LEVEL 4": "STUFE 4",

    # Effect/Element categories
    "Effect": "Effekt",
    "Element": "Element",
    "Halve": "Halbieren",
    "Invalid": "Unwirksam",  # Not "Ungültig"
    "Absorb": "Absorbieren",

    # More battle
    "Change": "Wechseln",
    "Defend": "Verteidigen",
    "Item": "Objekt",
    "W-Item": "W-Objekt",
    "W-Magic": "W-Magie",
    "W-Summon": "W-Herbeiruf",
    "Mime": "Mimik",
    "Steal": "Stehlen",
    "Sense": "Erspuren",
    "Throw": "Werfen",
    "Morph": "Morphen",
    "Deathblow": "Todeshieb",
    "Manipulate": "Manipul.",
    "Coin": "Munze",
    "2x-Cut": "2x-Schnitt",
    "4x-Cut": "4x-Schnitt",
    "Flash": "Blitz",
    "Slash-All": "Schnitt-Alle",
    "Enemy Skill": "Feind-Fertigkeit",
}


def main():
    print("FF7 German HEXT Generator v5")
    print("=" * 60)

    # Load exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(DE_EXE, 'rb') as f:
        de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), DE ({len(de_data):,})")

    # Generate patches
    patches = []
    matched = 0
    unmatched = 0
    skipped = 0

    unmatched_list = []

    for idx, steam_offset in enumerate(EN_OFFSETS):
        if idx in SKIP_REGIONS:
            skipped += 1
            continue

        if idx >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[idx]
        steam_bytes = steam_data[steam_offset:steam_offset + length]
        en_text = decode_ff7(steam_bytes).strip()

        if not en_text:
            unmatched += 1
            continue

        # Try to find German equivalent
        de_bytes = None
        de_text = None

        # First check direct offset mapping (for umlauts)
        if en_text in DIRECT_DE_OFFSETS:
            offset, max_len = DIRECT_DE_OFFSETS[en_text]
            # Extract until FF terminator
            end = de_data.find(b'\xff', offset, offset + max_len + 10)
            if end != -1:
                de_bytes = de_data[offset:end + 1]
                de_text = decode_ff7(de_bytes)

        # Then check manual text mapping
        if de_bytes is None and en_text in EN_TO_DE_MAP:
            de_search = EN_TO_DE_MAP[en_text]
            if de_search:
                de_bytes = find_de_string(de_data, de_search)
                if de_bytes:
                    de_text = decode_ff7(de_bytes)

        # If not found, try direct search (same text might work)
        if de_bytes is None:
            de_bytes = find_de_string(de_data, en_text)
            if de_bytes:
                de_text = decode_ff7(de_bytes)

        if de_bytes:
            va = file_offset_to_va(steam_offset)
            patches.append({
                'index': idx,
                'va': va,
                'steam_offset': steam_offset,
                'length': length,
                'en_text': en_text,
                'de_text': de_text,
                'de_bytes': de_bytes
            })
            matched += 1
        else:
            unmatched += 1
            if len(unmatched_list) < 100:
                unmatched_list.append((idx, en_text))

    print(f"\nResults: Matched={matched}, Unmatched={unmatched}, Skipped={skipped}")

    if unmatched_list:
        print(f"\nUnmatched strings (first {min(50, len(unmatched_list))}):")
        for idx, text in unmatched_list[:50]:
            print(f"  {idx:3d}: '{text}'")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_v5.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for p in patches:
            de_bytes = p['de_bytes']
            slot_len = p['length']

            # CRITICAL: Truncate if DE string is longer than slot
            if len(de_bytes) > slot_len:
                # Truncate and add terminator at the end
                de_bytes = de_bytes[:slot_len - 1] + b'\xff'
                truncated = True
            else:
                truncated = False

            # Format DE bytes with padding if shorter
            hex_bytes = ' '.join('%02X' % b for b in de_bytes)
            if len(de_bytes) < slot_len:
                padding = ' '.join('00' for _ in range(slot_len - len(de_bytes)))
                hex_bytes += ' ' + padding

            comment = "# %d: '%s' -> '%s'" % (p['index'], p['en_text'][:25], p['de_text'][:25])
            if truncated:
                comment += " [TRUNCATED]"
            f.write(comment + "\n")
            f.write("%06X = %s\n\n" % (p['va'], hex_bytes))

    print(f"\nWrote {len(patches)} patches to: {output_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator - FINAL VERSION

Complete approach:
1. For each touphScript index, we know the English text
2. Look up the German translation from our comprehensive dictionary
3. Search for that German text in the DE exe
4. Write DE bytes to Steam VA (with proper slot size handling)

Created: 2026-01-02 18:00 JST
Session: 2e703ab4-4b5e-4772-8894-ba089b4f437c
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from generate_exe_hext import EN_OFFSETS, STRING_LENGTHS, STRING_TYPES

# File paths
STEAM_EN = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe"
ESTORE_DE = "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe"

# Skip regions
SKIP_REGIONS = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry (UNICODE)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals
SKIP_REGIONS.update(range(712, 758))   # Chocobo names


def decode_ff7(data):
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
        elif b == 0x6A:  # ä in German font
            result.append('ä')
        elif b == 0x7A:  # ö in German font
            result.append('ö')
        elif b == 0x7E:  # ß in German font
            result.append('ß')
        elif b == 0x7F:  # ü in German font
            result.append('ü')
        else:
            result.append(chr(b + 0x20) if b < 0x80 else f'[{b:02X}]')
        i += 1
    return ''.join(result).strip()


def encode_ff7(text):
    """Encode text to FF7 bytes for searching."""
    result = []
    for c in text:
        if c == ' ':
            result.append(0x00)
        elif c == 'ä':
            result.append(0x6A)
        elif c == 'ö':
            result.append(0x7A)
        elif c == 'ß':
            result.append(0x7E)
        elif c == 'ü':
            result.append(0x7F)
        elif 0x21 <= ord(c) <= 0x7E:
            result.append(ord(c) - 0x20)
        # Skip other chars
    return bytes(result)


def file_offset_to_va(offset):
    """Convert file offset to Virtual Address for HEXT."""
    return (offset - 0x3B8A00) + 0x3BA000 + 0x400000


def find_de_string(de_data, german_text, prefer_short=True):
    """Find German string in DE exe and return (offset, bytes)."""
    search = encode_ff7(german_text)
    if len(search) < 2:
        return None, None

    # Search in menu region
    matches = []
    pos = 0x580000
    while pos < 0x5C0000:
        found = de_data.find(search, pos, 0x5C0000)
        if found == -1:
            break

        # Get full string with terminator
        ff = de_data.find(b'\xff', found, found + 200)
        if ff != -1:
            full_bytes = de_data[found:ff + 1]
            matches.append((found, full_bytes))
        pos = found + 1

    if not matches:
        return None, None

    # Prefer shorter match if requested (exact match)
    if prefer_short:
        matches.sort(key=lambda x: len(x[1]))

    return matches[0]


# =============================================================================
# COMPREHENSIVE EN -> DE TRANSLATION DICTIONARY
# This is the key to 100% coverage
# =============================================================================

EN_TO_DE = {
    # Quit dialog (indices 0-4)
    "Do you want to quit": "Möchten Sie Final",
    "playing Final Fantasy VII": "Fantasy VII verlassen und",
    "and return to Windows?": "zu Windows zurückkehren?",
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
    "Select": "Auswählen",
    "Cancel": "Abbrechen",
    "Menu": "Menü",
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
    "forbidden": "Verboten",
    "No.": "Nr.",
    "Window OFF": "Fenster AUS",
    "Pause": "Pause",
    "Battle help": "Schlachthilfe",
    "Mono": "Mono",
    "Stereo": "Stereo",
    "Wide": "Breit",

    # Keyboard config (indices 58-76) - German labels
    "Press [CANCEL] to end.": "Mit [ABBRECHEN] beenden.",
    "Press [OK] to configure a key.": "[O.K.] Taste zuweisen.",
    "Now press the new key.": "Neue Taste drücken.",
    "[OK]": "[O.K.]",
    "[CANCEL]": "[ABBRECHEN]",
    "[MENU]": "[MENÜ]",
    "[SWITCH]": "[UMSCHALTEN]",
    "[PAGEUP]": "[BILD HOCH]",
    "[PAGEDOWN]": "[BILD HERUNTER]",
    "[CAMERA]": "[KAMERA]",
    "[TARGET]": "[ZIEL]",
    "[ASSIST]": "[HILFE]",
    "[START]": "[START]",
    "[UP]": "[HERAUF]",
    "[DOWN]": "[UNTEN]",
    "[LEFT]": "[LINKS]",
    "[RIGHT]": "[RECHTS]",
    "KEYBOARD": "TASTATUR",
    "JOYSTICK": "JOYSTICK",

    # Sound option
    "Set Sound & Music Volume": "Ton- und Musikeinstellung",
    "Not supported.": "Nicht unterstützt.",

    # Main menu (indices 38-57)
    "Item": "Objekt",
    "Magic": "Magie",
    "Materia": "Materia",
    "Equip": "Ausrüsten",
    "Status": "Werte",
    "Order": "Ordnen",
    "Limit": "Limit",
    "Config": "Konfig",
    "PHS": "PHS",
    "Save": "Speichern",
    "Quit": "Verlassen",
    "Beginner": "Einsteiger",
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nächster Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "LEVEL UP": "STUFE HOCH",
    "Fury": "Zorn",
    "Sadness": "Trauer",

    # Stats - CORRECTED from DE exe search
    "Strength": "Stärke",
    "Vitality": "Vitalität",
    "Dexterity": "Geschick",
    "Luck": "Glück",
    "Attack": "Angriff",
    "Attack%": "Angriff %",  # Space before %
    "Defense": "Verteidigung",
    "Defense%": "Verteidigung %",  # Space before %
    "Magic": "Zauber",
    "Spirit": "Gemüt",
    "MagicDef": "Zbr.Vert",
    "MagicDef%": "Zbr.Vert%",
    "Mag.Def": "Zbr.Vert",
    "Mag.Def%": "Zbr.Vert%",
    "Evade%": "Ausweichen%",
    "Evade": "Ausweichen",

    # Equipment
    "Weapon": "Waffe",
    "Armor": "Rüstung",
    "Accessory": "Accessoire",
    "Slot": "Fassung:",
    "Growth": "Wachstum:",
    "nothing": "nichts",
    "empty": "leer",
    "Remove": "Entfernen",

    # Elements
    "Fire": "Feuer",
    "Ice": "Kälte",
    "Lightning": "Blitz",
    "Earth": "Erde",
    "Poison": "Gift",
    "Gravity": "Schwerkraft",
    "Water": "Wasser",
    "Wind": "Wind",
    "Holy": "Heilig",
    "Cut": "Schnitt",
    "Hit": "Treffer",
    "Punch": "Schlag",
    "Shoot": "Schuss",
    "Shout": "Schrei",
    "Hidden": "Versteckt",
    "Non-Ele": "Ohne Elem.",

    # Status effects
    "Death": "Tod",
    "Near-death": "Beinahe Tod",
    "Sleep": "Schlaf",
    "Poison": "Gift",
    "Confusion": "Verwirrung",
    "Silence": "Stummheit",
    "Haste": "Schnell",
    "Stop": "Stop",
    "Frog": "Frosch",
    "Small": "Zwerg",
    "Manipulate": "Manipul.",
    "Berserk": "Tollwut",
    "Petrify": "Versteinern",
    "Reflect": "Reflektieren",
    "Death-sentence": "Todesurteil",
    "Barrier": "Barriere",
    "MBarrier": "ZBarriere",
    "Shield": "Schild",
    "Regen": "Regen",
    "Resist": "Widerstand",
    "Peerless": "Unerreicht",
    "Paralyze": "Lähmung",
    "Darkness": "Dunkelheit",
    "Blind": "Blindheit",

    # Battle/Item menu
    "Use": "Verwenden",
    "Arrange": "Ordnen",
    "Key Items": "Schlüsselobjekte",
    "HP": "HP",
    "MP": "MP",
    "EXP": "EXP",
    "AP": "AP",
    "LV": "Stufe",
    "Lv": "Stufe",
    "Level": "Stufe",

    # Shop
    "Buy": "Kaufen",
    "Sell": "Verkaufen",
    "Exit": "Verlassen",
    "Welcome!": "Willkommen!",
    "What would you like to buy?": "Was möchten Sie kaufen?",
    "What would you like to sell?": "Was möchten Sie verkaufen?",
    "Thank You!": "Vielen Dank!",
    "Come back soon!": "Beehren Sie uns bald wieder!",
    "Owned:": "Im Besitz:",
    "Equipped:": "Ausgerüstet:",
    "Buy  Sell  Exit": "Kaufen  Verkaufen  Verlassen",

    # Materia
    "Check": "Prüfen",
    "Exchange": "Tauschen",
    "Trash": "Entsorgen",
    "All": "Alle",
    "Summon": "Herbeiruf",
    "Command": "Kommando",
    "Support": "Unterstützung",
    "Independent": "Unabhängig",
    "MASTER": "MEISTER",
    "AP Needed": "Noch nötig",
    "ability list": "Fähigkeitsliste",
    "Equip Effect": "Rüstungseffekt",
    "to next level": "Auf nächste Ebene",

    # Limit
    "Set": "Einrichten",
    "LEVEL 1": "STUFE 1",
    "LEVEL 2": "STUFE 2",
    "LEVEL 3": "STUFE 3",
    "LEVEL 4": "STUFE 4",
    "Lv1": "Stufe 1",
    "Lv2": "Stufe 2",
    "Lv3": "Stufe 3",
    "Lv4": "Stufe 4",

    # Effect/Element categories
    "Effect": "Effekt",
    "Element": "Element",
    "Halve": "Halbieren",
    "Invalid": "Unwirksam",
    "Absorb": "Absorbieren",
    "Null": "Aufheben",
    "Weak": "Schwach",
    "Death Force": "Todeskraft",

    # Battle commands
    "Change": "Wechseln",
    "Defend": "Verteidigen",
    "W-Item": "W-Objekt",
    "W-Magic": "W-Magie",
    "W-Summon": "W-Herbeiruf",
    "Mime": "Mimik",
    "Steal": "Stehlen",
    "Sense": "Erspüren",
    "Throw": "Werfen",
    "Morph": "Morphen",
    "Deathblow": "Todeshieb",
    "Coin": "Münze",
    "2x-Cut": "2x-Schnitt",
    "4x-Cut": "4x-Schnitt",
    "Flash": "Blitz",
    "Slash-All": "Schnitt-Alle",
    "Enemy Skill": "Feind-Fertigkeit",
    "E.Skill": "F-Fertigkeit",
    "Escape": "Fliehen",
    "Row": "Reihe",
    "Front Row": "Erste Reihe",
    "Back Row": "Zweite Reihe",

    # Battle messages
    "Minimum": "Minimum",
    "Maximum": "Maximum",
    "HP Restored": "HP wiederhergestellt",
    "MP Restored": "MP wiederhergestellt",
    "HP absorbed": "HP absorbiert",
    "MP absorbed": "MP absorbiert",
    "Missed!": "Verfehlt!",
    "Critical!": "Kritisch!",
    "All Creation": "Alle Schöpfung",
    "Death Sentence": "Todesurteil",
    "Petrifying": "Versteinernd",
    "Poisoned": "Vergiftet",
    "Confused": "Verwirrt",
    "Silenced": "Stumm",
    "Asleep": "Schläft",
    "Stopped": "Gestoppt",
    "Paralyzed": "Gelähmt",
    "Covered by": "Geschützt von",
    "Revived": "Wiederbelebt",

    # Materia broken messages
    "Magic Materia is broken.": "Zauber-Materia ist kaputt.",
    "Summon Materia is broken.": "Herbeiruf-Materia ist kaputt.",
    "Support Materia is broken.": "Unterstützungs-Materia ist kaputt.",
    "Independent Materia is broken.": "Unabhängige Materia ist kaputt.",
    "Command Materia is broken.": "Kommando-Materia ist kaputt.",
    "All Materia is broken.": "Alle Materia ist kaputt.",
    "Accessory is broken.": "Accessoire ist kaputt.",
    "Armor is broken.": "Rüstung ist kaputt.",
    "Weapon is broken.": "Waffe ist kaputt.",
    "Item command is sealed.": "Objekt-Kommando versiegelt.",

    # Speed/accuracy modifiers
    "1/2 speed.": "1/2 Tempo.",
    "1/2 accuracy.": "1/2 Genauigkeit.",
    "Double speed.": "Doppeltes Tempo.",

    # Gold Saucer
    "How much will you raise?": "Wieviel setzen Sie?",
    "After": "Nach",
    "Gil on hand": "Gil verfügbar",
    "Keep goin'?": "Weitermachen?",
    "Of course!     No way!": "Natürlich!     Nein!",
    "Current Battle Points": "Momentane Kampfpunkte",
    "Slot start!": "Los geht's!",
    "GREAT!!": "GROSSARTIG!!",
    "Then, go for it!": "Also, los!",
    "GP": "GP",
    "Battle Points": "Kampfpunkte",

    # Save/Load
    "Select a save data file.": "Speicherdatei auswählen.",
    "Saving. Please wait.": "Speichern. Bitte warten.",
    "Save 1": "Speicher 1",
    "Save 2": "Speicher 2",
    "Save 3": "Speicher 3",
    "Save 4": "Speicher 4",
    "Save 5": "Speicher 5",
    "Save 6": "Speicher 6",
    "Save 7": "Speicher 7",
    "Save 8": "Speicher 8",
    "Save 9": "Speicher 9",
    "Save 10": "Speicher 10",
    "New Game": "Neues Spiel",
    "Continue": "Fortsetzen",
    "Continue?": "Fortsetzen?",
    "Load": "Laden",
    "total": "insgesamt",

    # Character names
    "Cloud": "Cloud",
    "Barret": "Barret",
    "Tifa": "Tifa",
    "Aeris": "Aeris",
    "Red XIII": "Red XIII",
    "Yuffie": "Yuffie",
    "Cait Sith": "Cait Sith",
    "Vincent": "Vincent",
    "Cid": "Cid",
    "Sephiroth": "Sephiroth",

    # Game items
    "Potion": "Trank",
    "Hi-Potion": "Großtrank",
    "X-Potion": "Supertrank",
    "Ether": "Äther",
    "Turbo Ether": "Turbo-Äther",
    "Elixir": "Elixier",
    "Megalixir": "Megalixier",
    "Phoenix Down": "Phönixfeder",
    "Antidote": "Gegengift",
    "Soft": "Weich",
    "Maiden's Kiss": "Mädchenkuss",
    "Cornucopia": "Füllhorn",
    "Echo Screen": "Echoschirm",
    "Hyper": "Hyper",
    "Tranquilizer": "Beruhiger",
    "Remedy": "Allheilmittel",
    "Smoke Bomb": "Rauchbombe",
    "Speed Drink": "Tempotrunk",
    "Hero Drink": "Heldentrunk",
    "Vaccine": "Impfstoff",
    "Grenade": "Granate",
    "Shrapnel": "Schrapnell",
    "Right arm": "Rechter Arm",
    "Tent": "Zelt",
    "Power Source": "Kraftquelle",
    "Guard Source": "Schutzquelle",
    "Magic Source": "Magiequelle",
    "Mind Source": "Geistquelle",
    "Speed Source": "Tempoquelle",
    "Luck Source": "Glücksquelle",
    "Zeio Nut": "Zeio-Nuß",

    # Descriptions
    "Restores HP": "Stellt HP wieder her",
    "Restores MP": "Stellt MP wieder her",
    "Revives": "Wiederbelebt",
    "Cures": "Heilt",
}


def main():
    print("FF7 German HEXT Generator - FINAL")
    print("=" * 60)

    # Load exe files
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_DE, 'rb') as f:
        de_data = f.read()

    print(f"Loaded: Steam EN ({len(steam_data):,}), DE ({len(de_data):,})")
    print(f"Translation dictionary: {len(EN_TO_DE)} entries")

    patches = []
    matched = 0
    not_found = 0
    skipped = 0
    no_translation = 0

    for idx, steam_offset in enumerate(EN_OFFSETS):
        if idx in SKIP_REGIONS:
            skipped += 1
            continue

        if idx >= len(STRING_LENGTHS):
            break

        length = STRING_LENGTHS[idx]
        steam_bytes = steam_data[steam_offset:steam_offset + length]
        en_text = decode_ff7(steam_bytes)

        if not en_text or len(en_text.strip()) < 1:
            skipped += 1
            continue

        # Look up German translation
        german = EN_TO_DE.get(en_text)

        if german is None:
            # Try case variations
            german = EN_TO_DE.get(en_text.strip())
            if german is None:
                german = EN_TO_DE.get(en_text.capitalize())
                if german is None:
                    # Maybe EN=DE (like "HP", "MP", etc.)
                    german = en_text

        # Search for German text in DE exe
        de_offset, de_bytes = find_de_string(de_data, german)

        if de_offset is None:
            # Try original English (in case it's the same)
            de_offset, de_bytes = find_de_string(de_data, en_text)

        if de_bytes:
            patches.append({
                'idx': idx,
                'steam_offset': steam_offset,
                'length': length,
                'en_text': en_text,
                'de_text': german,
                'de_bytes': de_bytes,
            })
            matched += 1
        else:
            if german != en_text:
                print(f"  NOT FOUND {idx}: '{en_text}' -> '{german}'")
            not_found += 1

    print(f"\n{'='*60}")
    print(f"Results: Matched={matched}, Not found={not_found}, Skipped={skipped}")

    # Write HEXT file
    output_path = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/hext/ff7/de/german_menu.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write("# German Menu Text Patch for FF7 English\n")
        f.write("# AUTO-GENERATED by generate_german_hext_final.py\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("#\n\n")

        for p in patches:
            de_bytes = p['de_bytes']
            slot_len = p['length']
            va = file_offset_to_va(p['steam_offset'])

            # Truncate if too long
            truncated = False
            if len(de_bytes) > slot_len:
                de_bytes = de_bytes[:slot_len - 1] + b'\xff'
                truncated = True

            # Pad if too short
            hex_bytes = ' '.join('%02X' % b for b in de_bytes)
            if len(de_bytes) < slot_len:
                padding = ' '.join('00' for _ in range(slot_len - len(de_bytes)))
                hex_bytes += ' ' + padding

            comment = f"# {p['idx']}: '{p['en_text'][:25]}' -> '{p['de_text'][:25]}'"
            if truncated:
                comment += " [TRUNCATED]"
            f.write(comment + "\n")
            f.write(f"{va:06X} = {hex_bytes}\n\n")

    print(f"\nWrote {len(patches)} patches to: {output_path}")


if __name__ == "__main__":
    main()

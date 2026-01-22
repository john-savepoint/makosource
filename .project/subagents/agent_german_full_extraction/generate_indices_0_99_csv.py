#!/usr/bin/env python3
"""
Generate clean CSV mapping for German FF7 menu strings indices 0-99

Created: 2026-01-03 JST
Session: Current session
Context: User requested mapping of indices 0-99 with decoded German text

Note: The offset range 0x5D4390 to 0x5D48BD mentioned by user contains
x86 assembly code, NOT menu strings. The actual German menu strings are
in the 0x590000-0x5A0000 range.
"""

import csv
from pathlib import Path

# English reference strings for indices 0-99
EN_STRINGS = [
    "Do you want to quit",                    # 0
    "playing Final Fantasy VII",              # 1
    "and return to Windows?",                 # 2
    "Yes",                                    # 3
    "No",                                     # 4
    "Window color",                           # 5
    "Sound",                                  # 6
    "Controller",                             # 7
    "Cursor",                                 # 8
    "ATB",                                    # 9
    "Battle speed",                           # 10
    "Battle message",                         # 11
    "Field message",                          # 12
    "Camera angle",                           # 13
    "Select",                                 # 14
    "Cancel",                                 # 15
    "Menu",                                   # 16
    "Normal",                                 # 17
    "Customize",                              # 18
    "Initial",                                # 19
    "Memory",                                 # 20
    "Active",                                 # 21
    "Recommended",                            # 22
    "Wait",                                   # 23
    "Auto",                                   # 24
    "Fixed",                                  # 25
    "Slow",                                   # 26
    "Fast",                                   # 27
    "Magic order",                            # 28
    "restore",                                # 29
    "attack",                                 # 30
    "indirect",                               # 31
    "No",                                     # 32
    "[C5][B8][B7]",                           # 33
    "[BA][C5][B8][B8][C1]",                   # 34
    "[B5][BF][C8][B8]",                       # 35
    "Set Sound & Music Volume",               # 36
    "Not supported",                          # 37
    "Item",                                   # 38
    "Magic",                                  # 39
    "Materia",                                # 40
    "Equip",                                  # 41
    "Status",                                 # 42
    "Order",                                  # 43
    "Limit",                                  # 44
    "Config",                                 # 45
    "PHS",                                    # 46
    "Save",                                   # 47
    "Quit",                                   # 48
    "Beginner",                               # 49
    "Time",                                   # 50
    "Gil",                                    # 51
    "next level",                             # 52
    "Limit level",                            # 53
    "Tutorial",                               # 54
    "LEVEL UP",                               # 55
    "Fury",                                   # 56
    "Sadness",                                # 57
    "Press [CANCEL] to end.",                 # 58
    "Press [OK] to configure a key.",         # 59
    "Now press the new key.",                 # 60
    "[OK]",                                   # 61
    "[CANCEL]",                               # 62
    "[MENU]",                                 # 63
    "[SWITCH]",                               # 64
    "[PAGEUP]",                               # 65
    "[PAGEDOWN]",                             # 66
    "[CAMERA]",                               # 67
    "[TARGET]",                               # 68
    "[ASSIST]",                               # 69
    "[START]",                                # 70
    "[UP]",                                   # 71
    "[DOWN]",                                 # 72
    "[LEFT]",                                 # 73
    "[RIGHT]",                                # 74
    "KEYBOARD",                               # 75
    "JOYSTICK",                               # 76
    "ESCAPE",                                 # 77
    "1",                                      # 78
    "2",                                      # 79
    "3",                                      # 80
    "4",                                      # 81
    "5",                                      # 82
    "6",                                      # 83
    "7",                                      # 84
    "8",                                      # 85
    "9",                                      # 86
    "0",                                      # 87
    "MINUS",                                  # 88
    "EQUALS",                                 # 89
    "BACK SPACE",                             # 90
    "TAB",                                    # 91
    "Q",                                      # 92
    "W",                                      # 93
    "E",                                      # 94
    "R",                                      # 95
    "T",                                      # 96
    "Y",                                      # 97
    "U",                                      # 98
    "I",                                      # 99
]

# German offsets and decoded text from german_strings_by_index.txt
# Extracted from the detailed analysis
DE_DATA = [
    (0x0058FBB0, "Möchten Sie Final"),                              # 0
    (0x0058FBCE, "Fantasy VII verlassen und"),                      # 1
    (0x0058FBEC, "zu Windows zurückkehren?"),                       # 2
    (0x0058FC10, "Ja"),                                             # 3
    (0x0058FC14, "Nein"),                                           # 4
    (0x005900E8, "Fensterfarbe"),                                   # 5
    (0x00590118, "Sound"),                                          # 6
    (0x00590148, "Kontroller"),                                     # 7
    (0x00590178, "Cursor"),                                         # 8
    (0x005901A8, "ATB"),                                            # 9
    (0x005901D8, "Kampftempo"),                                     # 10
    (0x00590208, "Kampfmeldung"),                                   # 11
    (0x00590238, "Feldmeldung"),                                    # 12
    (0x00590268, "Kamerawinkel"),                                   # 13
    (0x00590298, "Auswählen"),                                      # 14
    (0x005902C8, "Abbrechen"),                                      # 15
    (0x005902F8, "Menü"),                                           # 16
    (0x00590448, "Stereo"),                                         # 17
    (0x00590478, "Breit"),                                          # 18
    (0x005904A8, "Normal"),                                         # 19
    (0x005904D8, "Benutzerdefiniert"),                              # 20
    (0x00590508, "Anfang"),                                         # 21
    (0x00590538, "Speicher"),                                       # 22
    (0x00590568, "Aktiv"),                                          # 23
    (0x00590598, "Empfohlen"),                                      # 24
    (0x005905C8, "Warten"),                                         # 25
    (0x00590628, "Auto"),                                           # 26
    (0x00590658, "Fest"),                                           # 27
    (0x00590718, "Zauberfolge"),                                    # 28
    (0x00590748, "Heilung"),                                        # 29
    (0x00590778, "Angriff"),                                        # 30
    (0x005907A8, "Indirekt"),                                       # 31
    (0x00590808, "Nein"),                                           # 32
    (0x00590A78, ""),                                               # 33 - empty
    (0x00590A7E, ""),                                               # 34 - empty
    (0x00590A84, ""),                                               # 35 - empty
    (0x00590AC8, "Hilfe"),                                          # 36
    (0x00590AE1, "Nicht unterstützt"),                              # 37
    (0x00590B00, "Objekt"),                                         # 38
    (0x00590B14, "Zauber"),                                         # 39
    (0x00590B28, "Materia"),                                        # 40
    (0x00590B3C, "Ausrüsten"),                                      # 41
    (0x00590B50, "Status"),                                         # 42
    (0x00590B64, "Reihenfolge"),                                    # 43
    (0x00590B78, "Limit"),                                          # 44
    (0x00590B8C, "Konfig"),                                         # 45
    (0x00590BA0, "PHS"),                                            # 46
    (0x00590BB4, "Speichern"),                                      # 47
    (0x00590BC8, "Verlassen"),                                      # 48
    (0x00590BDC, "Anfänger"),                                       # 49
    (0x00590C18, "Zeit"),                                           # 50
    (0x00590C2C, "Gil"),                                            # 51
    (0x00590C40, "nächstes Level"),                                 # 52
    (0x00590C54, "Limit-Level"),                                    # 53
    (0x00590C68, "Übung"),                                          # 54
    (0x00590C90, "LEVEL-ANSTIEG"),                                  # 55
    (0x00590CA4, "Wut"),                                            # 56
    (0x00590CB8, "Trauer"),                                         # 57
    (0x00590EF0, "Mit [ABBRECHEN] beenden."),                       # 58
    (0x00590F22, "[O.K.] um die Tastenbelegung zu konfigurieren."), # 59
    (0x00590F54, "Bitte neue Taste drücken"),                       # 60
    (0x00590F86, "[O.K.]"),                                         # 61
    (0x00590FB8, "[ABBRECHEN]"),                                    # 62
    (0x00590FEA, "[MENÜ]"),                                         # 63
    (0x0059101C, "[UMSCHALTEN]"),                                   # 64
    (0x0059104E, "[BILD HOCH]"),                                    # 65
    (0x00591080, "[BILD HERUNTER]"),                                # 66
    (0x005910B2, "[KAMERA]"),                                       # 67
    (0x005910E4, "[ZIEL]"),                                         # 68
    (0x00591116, "[HILFE]"),                                        # 69
    (0x00591148, "[START]"),                                        # 70
    (0x0059117A, "[HERAUF]"),                                       # 71
    (0x005911AC, "[UNTEN]"),                                        # 72
    (0x005911DE, "[LINKS]"),                                        # 73
    (0x00591210, "[RECHT]"),                                        # 74
    (0x00591242, "TASTATUR"),                                       # 75
    (0x00591274, "JOYSTICK"),                                       # 76
    (0x00591820, "ESCAPE"),                                         # 77
    (0x00591828, "1"),                                              # 78
    (0x0059182C, "2"),                                              # 79
    (0x00591830, "3"),                                              # 80
    (0x00591834, "4"),                                              # 81
    (0x00591838, "5"),                                              # 82
    (0x0059183C, "6"),                                              # 83
    (0x00591840, "7"),                                              # 84
    (0x00591844, "8"),                                              # 85
    (0x00591848, "9"),                                              # 86
    (0x0059184C, "0"),                                              # 87
    (0x00591850, "MINUS"),                                          # 88
    (0x00591858, "GLEICH"),                                         # 89
    (0x00591860, "RÜCKTASTE"),                                      # 90
    (0x0059186C, "TAB"),                                            # 91
    (0x00591870, "Q"),                                              # 92
    (0x00591874, "W"),                                              # 93
    (0x00591878, "E"),                                              # 94
    (0x0059187C, "R"),                                              # 95
    (0x00591880, "T"),                                              # 96
    (0x00591884, "Y"),                                              # 97
    (0x00591888, "U"),                                              # 98
    (0x0059188C, "I"),                                              # 99
]


def main():
    output_file = Path(__file__).parent / "indices_0_99_mapping.csv"

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'de_offset', 'de_text', 'en_text'])

        for i in range(100):
            offset, de_text = DE_DATA[i]
            en_text = EN_STRINGS[i]
            writer.writerow([i, f"0x{offset:08X}", de_text, en_text])

    print(f"Generated {output_file}")
    print(f"Total entries: 100 (indices 0-99)")
    print()
    print("NOTE: The offset range 0x5D4390-0x5D48BD you mentioned contains")
    print("x86 assembly code, NOT menu strings. The actual German menu")
    print("strings are in the 0x58FB00-0x5A0000 range.")


if __name__ == '__main__':
    main()

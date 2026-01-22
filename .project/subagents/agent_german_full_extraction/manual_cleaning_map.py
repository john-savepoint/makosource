#!/usr/bin/env python3
"""
Manual cleaning map for German FF7 strings
Created: 2026-01-05 19:29 JST
Session: ff862825-4ec7-4a49-a932-e9e5dcc0ea9f

This mapping identifies garbled entries and their clean text.
The script will calculate proper offsets based on where the clean text starts.
"""

# Format: index -> clean_text
# The script will find the position of clean_text in the garbled string
# and calculate the new offset

CLEAN_TEXT_MAP = {
    5: "Fensterfarbe",  # Long garbage before
    82: "Mit [ABBRECHEN] beenden.",  # Ends with this
    102: "keines",  # First occurrence of recognizable text in keyboard mappings
    140: "Wieviel willst du ausgeben?",
    144: "Weiter?",
    179: "Speichern",  # Character selection context
    183: "Reformieren",
    213: "STUFE 1",
    379: "Hitze",  # Element list starts here
    439: "Waf.",
    462: "Feuer",
    517: "Zauber",
    530: "Verwenden",
    567: "Cloud",  # Character responses section
    623: "Cloud",  # Character names
    638: "RaginLion",  # After alphabet string
    644: "Ex-SOLDIER",
    648: "Barret",
    652: "Tifa",
    656: "Aerith",
    659: "Red",
    664: "Yuffie",
    668: "Cait Seith",
    672: "Vincent",
    676: "Cid",
    683: "Sephiroth",
    695: "Full Equipent!",  # After coordinate garbage
    822: "Laden",
    886: "Level",
    892: "Ja",  # Near end
}

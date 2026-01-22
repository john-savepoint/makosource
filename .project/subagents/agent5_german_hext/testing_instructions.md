# Testing Instructions for German HEXT Patch

## Prerequisites

1. FF7 Steam English version installed
2. FFNx mod loader installed

## Installation

1. Copy `german_menu_complete.txt` to:
   ```
   [FF7 Install Dir]/hext/ff7/de/
   ```
   Full path example:
   ```
   C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\hext\ff7\de\german_menu_complete.txt
   ```

2. Edit `FFNx.toml` and set:
   ```toml
   hext_patching_path = "hext/ff7/de"
   ```

## Testing Checklist

Verify the following menu screens show German text:

- [ ] Main menu (Objekt, Magie, Materia, etc.)
- [ ] Config menu (Fensterfarbe, Kampftempo, etc.)
- [ ] Item menu (Verwenden, Ordnen)
- [ ] Shop menu (Kaufen, Verkaufen, Verlassen)
- [ ] Status screen (Stärke, Vitalität, etc.)
- [ ] Materia menu (Prüfen, Tauschen)
- [ ] Save/Load menu (Speichern, Laden)
- [ ] Quit dialog (Möchten Sie... verlassen)

## Known Limitations

1. Some German strings are truncated when they exceed English slot size
2. Keyboard labels remain in English (standard for all languages)
3. Unicode name entry characters unchanged
4. Chocobo jockey names unchanged (proper nouns)

## Troubleshooting

If German text doesn't appear:

1. Check FFNx.toml path is correct
2. Verify HEXT file is in correct directory
3. Check FFNx APP.log for HEXT loading messages
4. Ensure using Steam English executable (not GOG or other)

#!/usr/bin/env python3
"""
Create interactive HTML viewer for character mapping verification.
Created: 2025-11-17 23:22:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

Features:
- Base layer: Original game texture
- Overlay layers: Claude, Tesseract, Manga-OCR results (toggle with right-click)
- Left-click to mark cell as needing correction
- Export marked cells for manual verification
"""

import csv
import json
from pathlib import Path
import base64

OUTPUT_DIR = Path("character_tables/interactive_viewer")
FONT_DIR = Path("extracted_fonts/png")

# Load all mappings
CLAUDE_CSV = Path("character_tables/character_map_accurate.csv")
TESSERACT_CSV = Path("character_tables/character_map.csv")
MANGAOCR_CSV = Path("character_tables/character_map_mangaocr.csv")


def load_csv_mapping(csv_path):
    """Load mapping from CSV into dict keyed by (texture, index)."""
    mapping = {}
    if not csv_path.exists():
        return mapping
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['Texture'], int(row['Index']))
            mapping[key] = row['Character']
    return mapping


def image_to_base64(img_path):
    """Convert image to base64 data URL."""
    with open(img_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"


def generate_html(texture_name, claude_map, tesseract_map, mangaocr_map):
    """Generate interactive HTML for a single texture."""

    # Prepare character data for this texture
    chars_data = []
    for index in range(256):
        grid_x = index % 16
        grid_y = index // 16

        key = (texture_name, index)
        claude_char = claude_map.get(key, "")
        tesseract_char = tesseract_map.get(key, "")
        mangaocr_char = mangaocr_map.get(key, "")

        chars_data.append({
            'index': index,
            'grid_x': grid_x,
            'grid_y': grid_y,
            'claude': claude_char,
            'tesseract': tesseract_char,
            'mangaocr': mangaocr_char
        })

    # Convert to JSON for embedding
    chars_json = json.dumps(chars_data, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FF7 Character Mapping Verification - {texture_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }}

        h1 {{
            color: #4CAF50;
            margin-bottom: 10px;
        }}

        .controls {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .controls label {{
            margin-right: 20px;
            cursor: pointer;
        }}

        .controls input[type="checkbox"] {{
            margin-right: 5px;
        }}

        .overlay-claude {{ color: #FF5722; }}
        .overlay-tesseract {{ color: #2196F3; }}
        .overlay-mangaocr {{ color: #4CAF50; }}

        .stats {{
            background: #333;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}

        .container {{
            position: relative;
            width: 1024px;
            height: 1024px;
            border: 2px solid #555;
        }}

        .base-image {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}

        .grid-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }}

        .cell {{
            position: absolute;
            width: 64px;
            height: 64px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-sizing: border-box;
            pointer-events: auto;
            cursor: pointer;
            transition: background-color 0.2s;
        }}

        .cell:hover {{
            background: rgba(255, 255, 255, 0.1);
        }}

        .cell.marked {{
            background: rgba(255, 0, 0, 0.3) !important;
            border: 2px solid #FF0000;
        }}

        .cell-char {{
            position: absolute;
            font-size: 48px;
            font-weight: bold;
            pointer-events: none;
            top: 2px;
            left: 4px;
        }}

        .char-claude {{
            color: rgba(255, 87, 34, 0.8);
            text-shadow: 0 0 3px black;
        }}

        .char-tesseract {{
            color: rgba(33, 150, 243, 0.8);
            text-shadow: 0 0 3px black;
        }}

        .char-mangaocr {{
            color: rgba(76, 175, 80, 0.8);
            text-shadow: 0 0 3px black;
        }}

        .hidden {{
            display: none;
        }}

        .instructions {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .export-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }}

        .export-btn:hover {{
            background: #45a049;
        }}

        .nav-links {{
            margin-bottom: 20px;
        }}

        .nav-links a {{
            color: #4CAF50;
            margin-right: 15px;
            text-decoration: none;
        }}

        .nav-links a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>FF7 Character Mapping Verification - {texture_name}</h1>

    <div class="nav-links">
        <a href="jafont_1.html">jafont_1</a>
        <a href="jafont_2.html">jafont_2</a>
        <a href="jafont_3.html">jafont_3</a>
        <a href="jafont_4.html">jafont_4</a>
        <a href="jafont_5.html">jafont_5</a>
        <a href="jafont_6.html">jafont_6</a>
    </div>

    <div class="instructions">
        <strong>Instructions:</strong><br>
        • <strong>Right-click anywhere</strong> to cycle through overlays: None → Claude → Tesseract → Manga-OCR<br>
        • <strong>Left-click a cell</strong> to mark it as needing correction (turns red)<br>
        • <strong>Left-click again</strong> to unmark<br>
        • <strong>Export</strong> to save list of marked cells for manual correction
    </div>

    <div class="controls">
        <strong>Current Overlay:</strong> <span id="current-overlay">None (Original Only)</span><br><br>
        <label class="overlay-claude">
            <input type="checkbox" id="show-claude" onchange="updateOverlay()">
            Claude Visual (Orange)
        </label>
        <label class="overlay-tesseract">
            <input type="checkbox" id="show-tesseract" onchange="updateOverlay()">
            Tesseract OCR (Blue)
        </label>
        <label class="overlay-mangaocr">
            <input type="checkbox" id="show-mangaocr" onchange="updateOverlay()">
            Manga-OCR (Green)
        </label>
    </div>

    <div class="stats">
        <strong>Statistics:</strong>
        <span id="marked-count">0</span> cells marked for correction
        <button class="export-btn" onclick="exportMarked()">Export Marked Cells</button>
        <button class="export-btn" onclick="clearMarked()" style="background: #f44336;">Clear All Marks</button>
    </div>

    <div class="container" oncontextmenu="cycleOverlay(event); return false;">
        <img class="base-image" src="../extracted_fonts/png/{texture_name}.png" alt="{texture_name}">
        <div class="grid-overlay" id="grid-overlay"></div>
    </div>

    <script>
        const TEXTURE_NAME = "{texture_name}";
        const CHARS_DATA = {chars_json};
        const CELL_SIZE = 64;

        let markedCells = new Set();
        let overlayMode = 0; // 0=none, 1=claude, 2=tesseract, 3=mangaocr

        function initGrid() {{
            const overlay = document.getElementById('grid-overlay');

            for (let i = 0; i < CHARS_DATA.length; i++) {{
                const data = CHARS_DATA[i];
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.style.left = (data.grid_x * CELL_SIZE) + 'px';
                cell.style.top = (data.grid_y * CELL_SIZE) + 'px';
                cell.dataset.index = data.index;
                cell.onclick = () => toggleMark(data.index);

                // Add character overlays
                if (data.claude) {{
                    const charEl = document.createElement('div');
                    charEl.className = 'cell-char char-claude hidden';
                    charEl.textContent = data.claude;
                    charEl.id = 'claude-' + data.index;
                    cell.appendChild(charEl);
                }}

                if (data.tesseract) {{
                    const charEl = document.createElement('div');
                    charEl.className = 'cell-char char-tesseract hidden';
                    charEl.textContent = data.tesseract;
                    charEl.id = 'tesseract-' + data.index;
                    cell.appendChild(charEl);
                }}

                if (data.mangaocr) {{
                    const charEl = document.createElement('div');
                    charEl.className = 'cell-char char-mangaocr hidden';
                    charEl.textContent = data.mangaocr;
                    charEl.id = 'mangaocr-' + data.index;
                    cell.appendChild(charEl);
                }}

                overlay.appendChild(cell);
            }}
        }}

        function toggleMark(index) {{
            const cell = document.querySelector(`[data-index="${{index}}"]`);
            if (markedCells.has(index)) {{
                markedCells.delete(index);
                cell.classList.remove('marked');
            }} else {{
                markedCells.add(index);
                cell.classList.add('marked');
            }}
            updateStats();
        }}

        function updateStats() {{
            document.getElementById('marked-count').textContent = markedCells.size;
        }}

        function cycleOverlay(event) {{
            event.preventDefault();
            overlayMode = (overlayMode + 1) % 4;

            // Update checkboxes
            document.getElementById('show-claude').checked = (overlayMode === 1);
            document.getElementById('show-tesseract').checked = (overlayMode === 2);
            document.getElementById('show-mangaocr').checked = (overlayMode === 3);

            updateOverlay();
        }}

        function updateOverlay() {{
            const showClaude = document.getElementById('show-claude').checked;
            const showTesseract = document.getElementById('show-tesseract').checked;
            const showMangaocr = document.getElementById('show-mangaocr').checked;

            // Hide all
            document.querySelectorAll('.char-claude').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.char-tesseract').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.char-mangaocr').forEach(el => el.classList.add('hidden'));

            // Show selected
            if (showClaude) {{
                document.querySelectorAll('.char-claude').forEach(el => el.classList.remove('hidden'));
            }}
            if (showTesseract) {{
                document.querySelectorAll('.char-tesseract').forEach(el => el.classList.remove('hidden'));
            }}
            if (showMangaocr) {{
                document.querySelectorAll('.char-mangaocr').forEach(el => el.classList.remove('hidden'));
            }}

            // Update label
            let label = [];
            if (showClaude) label.push('Claude');
            if (showTesseract) label.push('Tesseract');
            if (showMangaocr) label.push('Manga-OCR');
            document.getElementById('current-overlay').textContent =
                label.length ? label.join(' + ') : 'None (Original Only)';
        }}

        function exportMarked() {{
            const marked = Array.from(markedCells).sort((a, b) => a - b);
            const data = marked.map(index => {{
                const charData = CHARS_DATA[index];
                return {{
                    texture: TEXTURE_NAME,
                    index: index,
                    grid_x: charData.grid_x,
                    grid_y: charData.grid_y,
                    claude: charData.claude,
                    tesseract: charData.tesseract,
                    mangaocr: charData.mangaocr
                }};
            }});

            const json = JSON.stringify(data, null, 2);
            const blob = new Blob([json], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = TEXTURE_NAME + '_marked_cells.json';
            a.click();
            URL.revokeObjectURL(url);

            alert(`Exported ${{marked.length}} marked cells to ${{TEXTURE_NAME}}_marked_cells.json`);
        }}

        function clearMarked() {{
            if (confirm('Clear all marked cells?')) {{
                markedCells.clear();
                document.querySelectorAll('.cell.marked').forEach(el => el.classList.remove('marked'));
                updateStats();
            }}
        }}

        // Initialize
        initGrid();
        updateStats();
    </script>
</body>
</html>'''

    return html


def main():
    print("Creating interactive verification viewer...")

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load all mappings
    print("Loading Claude visual mapping...")
    claude_map = load_csv_mapping(CLAUDE_CSV)
    print(f"  Loaded {len(claude_map)} entries")

    print("Loading Tesseract OCR mapping...")
    tesseract_map = load_csv_mapping(TESSERACT_CSV)
    print(f"  Loaded {len(tesseract_map)} entries")

    print("Loading Manga-OCR mapping...")
    mangaocr_map = load_csv_mapping(MANGAOCR_CSV)
    print(f"  Loaded {len(mangaocr_map)} entries")

    # Generate HTML for each texture
    textures = ['jafont_1', 'jafont_2', 'jafont_3', 'jafont_4', 'jafont_5', 'jafont_6']

    for texture_name in textures:
        print(f"\nGenerating {texture_name}.html...")
        html = generate_html(texture_name, claude_map, tesseract_map, mangaocr_map)

        output_path = OUTPUT_DIR / f"{texture_name}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Saved: {output_path}")

    print("\n" + "=" * 60)
    print("INTERACTIVE VIEWER CREATED!")
    print("=" * 60)
    print(f"\nOpen in browser: {OUTPUT_DIR / 'jafont_1.html'}")
    print("\nInstructions:")
    print("  • Right-click to cycle overlays: None → Claude → Tesseract → Manga-OCR")
    print("  • Left-click cell to mark for correction (turns red)")
    print("  • Export button saves marked cells to JSON")


if __name__ == "__main__":
    main()

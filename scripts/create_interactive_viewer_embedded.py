#!/usr/bin/env python3
"""
Create interactive HTML viewer with EMBEDDED images (base64).
Created: 2025-11-17 23:24:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

This version embeds the game texture directly in the HTML as base64
so it doesn't need to resolve relative paths.
"""

import csv
import json
from pathlib import Path
import base64

OUTPUT_DIR = Path("character_tables/interactive_viewer")
FONT_DIR = Path("extracted_fonts/png")

CLAUDE_CSV = Path("character_tables/character_map_accurate.csv")
TESSERACT_CSV = Path("character_tables/character_map.csv")
MANGAOCR_CSV = Path("character_tables/character_map_mangaocr.csv")


def load_csv_mapping(csv_path):
    """Load mapping from CSV."""
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


def generate_html(texture_name, base64_img, claude_map, tesseract_map, mangaocr_map):
    """Generate interactive HTML with embedded image."""

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

    chars_json = json.dumps(chars_data, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FF7 Character Mapping - {texture_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }}
        h1 {{ color: #4CAF50; margin-bottom: 10px; }}
        .controls {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .controls label {{ margin-right: 20px; cursor: pointer; }}
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
            top: 0; left: 0;
            width: 100%; height: 100%;
        }}
        .grid-overlay {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
        }}
        .cell {{
            position: absolute;
            width: 64px; height: 64px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-sizing: border-box;
            pointer-events: auto;
            cursor: pointer;
        }}
        .cell:hover {{ background: rgba(255, 255, 255, 0.1); }}
        .cell.marked {{
            background: rgba(255, 0, 0, 0.3) !important;
            border: 2px solid #FF0000;
        }}
        .cell-char {{
            position: absolute;
            font-size: 48px;
            font-weight: bold;
            pointer-events: none;
            top: 2px; left: 4px;
        }}
        .char-claude {{ color: rgba(255, 87, 34, 0.9); text-shadow: 0 0 3px black; }}
        .char-tesseract {{ color: rgba(33, 150, 243, 0.9); text-shadow: 0 0 3px black; }}
        .char-mangaocr {{ color: rgba(76, 175, 80, 0.9); text-shadow: 0 0 3px black; }}
        .hidden {{ display: none; }}
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
            margin: 5px;
        }}
        .export-btn:hover {{ background: #45a049; }}
        .export-btn.red {{ background: #f44336; }}
        .export-btn.red:hover {{ background: #d32f2f; }}
        .nav-links {{ margin-bottom: 20px; }}
        .nav-links a {{
            color: #4CAF50;
            margin-right: 15px;
            text-decoration: none;
        }}
        .nav-links a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>FF7 Character Mapping - {texture_name}</h1>

    <div class="nav-links">
        <a href="jafont_1.html">jafont_1</a>
        <a href="jafont_2.html">jafont_2</a>
        <a href="jafont_3.html">jafont_3</a>
        <a href="jafont_4.html">jafont_4</a>
        <a href="jafont_5.html">jafont_5</a>
        <a href="jafont_6.html">jafont_6</a>
    </div>

    <div class="instructions">
        <strong>Controls:</strong><br>
        • <strong>Right-click anywhere</strong> → Cycle overlays: None → Claude (orange) → Tesseract (blue) → Manga-OCR (green)<br>
        • <strong>Left-click cell</strong> → Mark/unmark for correction (red border)<br>
        • <strong>Export</strong> → Download JSON of marked cells
    </div>

    <div class="controls">
        <strong>Current Overlay:</strong> <span id="current-overlay">None (Original Only)</span><br><br>
        <label class="overlay-claude">
            <input type="checkbox" id="show-claude" onchange="updateOverlay()"> Claude (Orange)
        </label>
        <label class="overlay-tesseract">
            <input type="checkbox" id="show-tesseract" onchange="updateOverlay()"> Tesseract (Blue)
        </label>
        <label class="overlay-mangaocr">
            <input type="checkbox" id="show-mangaocr" onchange="updateOverlay()"> Manga-OCR (Green)
        </label>
    </div>

    <div class="stats">
        <strong>Marked:</strong> <span id="marked-count">0</span> cells
        <button class="export-btn" onclick="exportMarked()">Export Marked</button>
        <button class="export-btn red" onclick="clearMarked()">Clear All</button>
    </div>

    <div class="container" oncontextmenu="cycleOverlay(event); return false;">
        <img class="base-image" src="{base64_img}" alt="{texture_name}">
        <div class="grid-overlay" id="grid-overlay"></div>
    </div>

    <script>
        const TEXTURE_NAME = "{texture_name}";
        const CHARS_DATA = {chars_json};

        let markedCells = new Set();
        let overlayMode = 0;

        function initGrid() {{
            const overlay = document.getElementById('grid-overlay');
            for (let i = 0; i < CHARS_DATA.length; i++) {{
                const data = CHARS_DATA[i];
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.style.left = (data.grid_x * 64) + 'px';
                cell.style.top = (data.grid_y * 64) + 'px';
                cell.dataset.index = data.index;
                cell.onclick = () => toggleMark(data.index);

                if (data.claude) {{
                    const el = document.createElement('div');
                    el.className = 'cell-char char-claude hidden';
                    el.textContent = data.claude;
                    el.id = 'claude-' + data.index;
                    cell.appendChild(el);
                }}
                if (data.tesseract) {{
                    const el = document.createElement('div');
                    el.className = 'cell-char char-tesseract hidden';
                    el.textContent = data.tesseract;
                    el.id = 'tesseract-' + data.index;
                    cell.appendChild(el);
                }}
                if (data.mangaocr) {{
                    const el = document.createElement('div');
                    el.className = 'cell-char char-mangaocr hidden';
                    el.textContent = data.mangaocr;
                    el.id = 'mangaocr-' + data.index;
                    cell.appendChild(el);
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
            document.getElementById('marked-count').textContent = markedCells.size;
        }}

        function cycleOverlay(event) {{
            event.preventDefault();
            overlayMode = (overlayMode + 1) % 4;
            document.getElementById('show-claude').checked = (overlayMode === 1);
            document.getElementById('show-tesseract').checked = (overlayMode === 2);
            document.getElementById('show-mangaocr').checked = (overlayMode === 3);
            updateOverlay();
        }}

        function updateOverlay() {{
            const showC = document.getElementById('show-claude').checked;
            const showT = document.getElementById('show-tesseract').checked;
            const showM = document.getElementById('show-mangaocr').checked;

            document.querySelectorAll('.char-claude').forEach(el => el.classList.toggle('hidden', !showC));
            document.querySelectorAll('.char-tesseract').forEach(el => el.classList.toggle('hidden', !showT));
            document.querySelectorAll('.char-mangaocr').forEach(el => el.classList.toggle('hidden', !showM));

            let label = [];
            if (showC) label.push('Claude');
            if (showT) label.push('Tesseract');
            if (showM) label.push('Manga-OCR');
            document.getElementById('current-overlay').textContent = label.length ? label.join(' + ') : 'None (Original Only)';
        }}

        function exportMarked() {{
            const marked = Array.from(markedCells).sort((a, b) => a - b);
            const data = marked.map(index => {{
                const c = CHARS_DATA[index];
                return {{ texture: TEXTURE_NAME, index, grid_x: c.grid_x, grid_y: c.grid_y,
                         claude: c.claude, tesseract: c.tesseract, mangaocr: c.mangaocr }};
            }});
            const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = TEXTURE_NAME + '_marked.json';
            a.click();
        }}

        function clearMarked() {{
            if (confirm('Clear all marks?')) {{
                markedCells.clear();
                document.querySelectorAll('.cell.marked').forEach(el => el.classList.remove('marked'));
                document.getElementById('marked-count').textContent = '0';
            }}
        }}

        initGrid();
    </script>
</body>
</html>'''
    return html


def main():
    print("Creating interactive viewer with EMBEDDED images...")
    OUTPUT_DIR.mkdir(exist_ok=True)

    claude_map = load_csv_mapping(CLAUDE_CSV)
    tesseract_map = load_csv_mapping(TESSERACT_CSV)
    mangaocr_map = load_csv_mapping(MANGAOCR_CSV)

    print(f"Loaded: Claude={len(claude_map)}, Tesseract={len(tesseract_map)}, Manga-OCR={len(mangaocr_map)}")

    for texture_name in ['jafont_1', 'jafont_2', 'jafont_3', 'jafont_4', 'jafont_5', 'jafont_6']:
        print(f"\nProcessing {texture_name}...")

        img_path = FONT_DIR / f"{texture_name}.png"
        print(f"  Embedding image: {img_path}")
        base64_img = image_to_base64(img_path)

        html = generate_html(texture_name, base64_img, claude_map, tesseract_map, mangaocr_map)

        output_path = OUTPUT_DIR / f"{texture_name}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Saved: {output_path} ({len(html)//1024}KB)")

    print("\n" + "=" * 60)
    print("DONE! Images are now embedded in HTML.")
    print("=" * 60)


if __name__ == "__main__":
    main()

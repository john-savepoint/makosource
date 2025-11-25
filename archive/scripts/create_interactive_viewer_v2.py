#!/usr/bin/env python3
"""
Interactive viewer v2: Claude is default, click to select alternative.
Created: 2025-11-17 23:29:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

When you click a cell, you pick:
- Use Tesseract result
- Use Manga-OCR result
- Needs manual investigation
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
    with open(img_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"


def generate_html(texture_name, base64_img, claude_map, tesseract_map, mangaocr_map):
    chars_data = []
    for index in range(256):
        grid_x = index % 16
        grid_y = index // 16
        key = (texture_name, index)
        chars_data.append({
            'index': index,
            'grid_x': grid_x,
            'grid_y': grid_y,
            'claude': claude_map.get(key, ""),
            'tesseract': tesseract_map.get(key, ""),
            'mangaocr': mangaocr_map.get(key, "")
        })

    chars_json = json.dumps(chars_data, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FF7 Charmap Verification - {texture_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a1a;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }}
        h1 {{ color: #4CAF50; margin-bottom: 10px; }}
        .nav-links {{ margin-bottom: 15px; }}
        .nav-links a {{ color: #4CAF50; margin-right: 15px; text-decoration: none; }}
        .nav-links a:hover {{ text-decoration: underline; }}
        .instructions {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .controls {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .stats {{
            background: #333;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
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
        .cell:hover {{ background: rgba(255, 255, 255, 0.15); }}
        .cell.use-tesseract {{ background: rgba(33, 150, 243, 0.3); border: 2px solid #2196F3; }}
        .cell.use-mangaocr {{ background: rgba(76, 175, 80, 0.3); border: 2px solid #4CAF50; }}
        .cell.use-manual {{ background: rgba(156, 39, 176, 0.3); border: 2px solid #9C27B0; }}
        .cell.investigate {{ background: rgba(255, 193, 7, 0.3); border: 2px solid #FFC107; }}
        .cell-char {{
            position: absolute;
            font-size: 56px;
            font-weight: bold;
            pointer-events: none;
            top: 0px; left: 2px;
        }}
        .char-claude {{ color: rgba(255, 87, 34, 0.9); text-shadow: 0 0 3px black; }}
        .char-tesseract {{ color: rgba(33, 150, 243, 0.9); text-shadow: 0 0 3px black; }}
        .char-mangaocr {{ color: rgba(76, 175, 80, 0.9); text-shadow: 0 0 3px black; }}
        .hidden {{ display: none; }}
        .export-btn {{
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
        }}
        .export-btn:hover {{ background: #45a049; }}
        .export-btn.red {{ background: #f44336; }}
        .export-btn.red:hover {{ background: #d32f2f; }}

        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            overflow-y: auto;
        }}
        .modal-content {{
            background: #2a2a2a;
            margin: 20px auto;
            padding: 20px;
            border-radius: 10px;
            width: 400px;
            text-align: center;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
        }}
        .modal h3 {{ margin-top: 0; color: #4CAF50; }}
        .char-display {{
            font-size: 60px;
            margin: 10px 0;
            padding: 10px;
            background: #333;
            border-radius: 5px;
        }}
        .game-char-container {{
            margin: 15px 0;
            text-align: center;
        }}
        .game-char-label {{
            color: #888;
            font-size: 14px;
            margin-bottom: 5px;
        }}
        .game-char-img {{
            border: 2px solid #FFF;
            background: #000;
        }}
        .choice-btn {{
            display: block;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            text-align: left;
        }}
        .choice-btn:hover {{ opacity: 0.9; }}
        .choice-claude {{ background: #FF5722; color: white; }}
        .choice-tesseract {{ background: #2196F3; color: white; }}
        .choice-mangaocr {{ background: #4CAF50; color: white; }}
        .choice-investigate {{ background: #FFC107; color: black; }}
        .choice-cancel {{ background: #666; color: white; }}
    </style>
</head>
<body>
    <h1>FF7 Charmap - {texture_name} <span style="font-size: 14px; color: #888;">(Claude = default)</span></h1>

    <div class="nav-links">
        <a href="jafont_1.html">jafont_1</a>
        <a href="jafont_2.html">jafont_2</a>
        <a href="jafont_3.html">jafont_3</a>
        <a href="jafont_4.html">jafont_4</a>
        <a href="jafont_5.html">jafont_5</a>
        <a href="jafont_6.html">jafont_6</a>
    </div>

    <div class="instructions">
        <strong>How to use:</strong><br>
        • <strong>Claude is assumed correct</strong> unless you click a cell<br>
        • <strong>Right-click</strong> → Toggle overlays (Claude/Tesseract/Manga-OCR)<br>
        • <strong>Left-click cell</strong> → Choose alternative: Tesseract, Manga-OCR, or Investigate<br>
        • <strong>Export</strong> → Download corrections for final mapping
    </div>

    <div class="controls">
        <strong>Overlay:</strong> <span id="current-overlay">None</span><br>
        <label><input type="checkbox" id="show-claude" onchange="updateOverlay()"> <span style="color:#FF5722">Claude (Orange)</span></label>
        <label><input type="checkbox" id="show-tesseract" onchange="updateOverlay()"> <span style="color:#2196F3">Tesseract (Blue)</span></label>
        <label><input type="checkbox" id="show-mangaocr" onchange="updateOverlay()"> <span style="color:#4CAF50">Manga-OCR (Green)</span></label>
    </div>

    <div class="stats">
        <strong>Corrections:</strong>
        <span style="color:#2196F3">Tesseract: <span id="count-tesseract">0</span></span> |
        <span style="color:#4CAF50">Manga-OCR: <span id="count-mangaocr">0</span></span> |
        <span style="color:#9C27B0">Manual: <span id="count-manual">0</span></span> |
        <span style="color:#FFC107">Investigate: <span id="count-investigate">0</span></span>
        <br>
        <button class="export-btn" onclick="exportCorrections()">Export This Texture</button>
        <button class="export-btn" onclick="exportFinalMapping()">Export Final Mapping</button>
        <button class="export-btn" onclick="exportAllTextures()">Export ALL Textures</button>
        <button class="export-btn red" onclick="clearCorrections()">Clear This Texture</button>
    </div>

    <div class="container" oncontextmenu="cycleOverlay(event); return false;">
        <img class="base-image" src="{base64_img}" alt="{texture_name}">
        <div class="grid-overlay" id="grid-overlay"></div>
    </div>

    <!-- Modal for choosing correction -->
    <div id="modal" class="modal" onclick="if(event.target===this) closeModal()">
        <div class="modal-content">
            <h3>Cell <span id="modal-index"></span> (<span id="modal-coords"></span>)</h3>

            <!-- Game character from texture -->
            <div class="game-char-container">
                <div class="game-char-label">ORIGINAL GAME CHARACTER:</div>
                <canvas id="game-char-canvas" class="game-char-img" width="128" height="128"></canvas>
            </div>

            <div class="char-display">
                <span style="color:#FF5722" id="modal-claude"></span>
                <span style="color:#2196F3" id="modal-tesseract"></span>
                <span style="color:#4CAF50" id="modal-mangaocr"></span>
            </div>
            <button class="choice-btn choice-claude" onclick="setCorrection('claude')">
                ✓ Claude is correct: <span id="btn-claude"></span>
            </button>
            <button class="choice-btn choice-tesseract" onclick="setCorrection('tesseract')">
                Use Tesseract: <span id="btn-tesseract"></span>
            </button>
            <button class="choice-btn choice-mangaocr" onclick="setCorrection('mangaocr')">
                Use Manga-OCR: <span id="btn-mangaocr"></span>
            </button>
            <div style="margin: 10px 0; padding: 10px; background: #444; border-radius: 5px;">
                <label style="display: block; margin-bottom: 5px; color: #FFC107;">Manual Entry:</label>
                <input type="text" id="manual-input" maxlength="1" style="font-size: 36px; width: 60px; text-align: center; padding: 5px;" placeholder="?">
                <button class="choice-btn" style="display: inline-block; width: auto; background: #9C27B0; margin-left: 10px;" onclick="setManualCorrection()">
                    Use Manual
                </button>
            </div>
            <button class="choice-btn choice-investigate" onclick="setCorrection('investigate')">
                ⚠ Needs Investigation
            </button>
            <button class="choice-btn choice-cancel" onclick="closeModal()">Cancel</button>
        </div>
    </div>

    <script>
        const TEXTURE = "{texture_name}";
        const CHARS = {chars_json};
        let corrections = {{}};  // index -> 'tesseract' | 'mangaocr' | 'investigate'
        let currentIndex = null;
        let overlayMode = 0;

        // Load saved corrections from localStorage
        function loadCorrections() {{
            const saved = localStorage.getItem('ff7_corrections_' + TEXTURE);
            if (saved) {{
                corrections = JSON.parse(saved);
                // Apply visual state
                for (const idx in corrections) {{
                    const cell = document.getElementById('cell-' + idx);
                    if (cell) {{
                        const corr = corrections[idx];
                        if (corr === 'tesseract') cell.classList.add('use-tesseract');
                        else if (corr === 'mangaocr') cell.classList.add('use-mangaocr');
                        else if (corr === 'investigate') cell.classList.add('investigate');
                        else if (typeof corr === 'object' && corr.type === 'manual') cell.classList.add('use-manual');
                    }}
                }}
            }}
        }}

        // Save corrections to localStorage
        function saveCorrections() {{
            localStorage.setItem('ff7_corrections_' + TEXTURE, JSON.stringify(corrections));
        }}

        function initGrid() {{
            const overlay = document.getElementById('grid-overlay');
            for (const data of CHARS) {{
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.id = 'cell-' + data.index;
                cell.style.left = (data.grid_x * 64) + 'px';
                cell.style.top = (data.grid_y * 64) + 'px';
                cell.onclick = () => openModal(data.index);

                if (data.claude) {{
                    const el = document.createElement('div');
                    el.className = 'cell-char char-claude hidden';
                    el.textContent = data.claude;
                    cell.appendChild(el);
                }}
                if (data.tesseract) {{
                    const el = document.createElement('div');
                    el.className = 'cell-char char-tesseract hidden';
                    el.textContent = data.tesseract;
                    cell.appendChild(el);
                }}
                if (data.mangaocr) {{
                    const el = document.createElement('div');
                    el.className = 'cell-char char-mangaocr hidden';
                    el.textContent = data.mangaocr;
                    cell.appendChild(el);
                }}
                overlay.appendChild(cell);
            }}
        }}

        function openModal(index) {{
            currentIndex = index;
            const data = CHARS[index];
            document.getElementById('modal-index').textContent = index;
            document.getElementById('modal-coords').textContent = data.grid_x + ',' + data.grid_y;
            document.getElementById('modal-claude').textContent = data.claude || '(empty)';
            document.getElementById('modal-tesseract').textContent = data.tesseract || '(empty)';
            document.getElementById('modal-mangaocr').textContent = data.mangaocr || '(empty)';
            document.getElementById('btn-claude').textContent = data.claude || '(empty)';
            document.getElementById('btn-tesseract').textContent = data.tesseract || '(empty)';
            document.getElementById('btn-mangaocr').textContent = data.mangaocr || '(empty)';

            // Extract game character from base image
            const baseImg = document.querySelector('.base-image');
            const canvas = document.getElementById('game-char-canvas');
            const ctx = canvas.getContext('2d');
            const sx = data.grid_x * 64;
            const sy = data.grid_y * 64;
            ctx.clearRect(0, 0, 128, 128);
            ctx.drawImage(baseImg, sx, sy, 64, 64, 0, 0, 128, 128);  // 2x scale

            // Clear manual input field
            document.getElementById('manual-input').value = '';

            document.getElementById('modal').style.display = 'block';
        }}

        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
            currentIndex = null;
        }}

        function setCorrection(choice) {{
            const cell = document.getElementById('cell-' + currentIndex);
            cell.classList.remove('use-tesseract', 'use-mangaocr', 'use-manual', 'investigate');

            if (choice === 'claude') {{
                delete corrections[currentIndex];
            }} else {{
                corrections[currentIndex] = choice;
                if (choice === 'tesseract') cell.classList.add('use-tesseract');
                else if (choice === 'mangaocr') cell.classList.add('use-mangaocr');
                else if (choice === 'investigate') cell.classList.add('investigate');
                else if (typeof choice === 'object' && choice.type === 'manual') cell.classList.add('use-manual');
            }}
            saveCorrections();  // Save to localStorage
            updateStats();
            closeModal();
        }}

        function setManualCorrection() {{
            const input = document.getElementById('manual-input').value;
            if (input && input.length === 1) {{
                const cell = document.getElementById('cell-' + currentIndex);
                cell.classList.remove('use-tesseract', 'use-mangaocr', 'use-manual', 'investigate');
                corrections[currentIndex] = {{ type: 'manual', char: input }};
                cell.classList.add('use-manual');
                saveCorrections();
                updateStats();
                closeModal();
            }} else {{
                alert('Please enter exactly one character');
            }}
        }}

        function updateStats() {{
            let t = 0, m = 0, man = 0, i = 0;
            for (const idx in corrections) {{
                const corr = corrections[idx];
                if (corr === 'tesseract') t++;
                else if (corr === 'mangaocr') m++;
                else if (corr === 'investigate') i++;
                else if (typeof corr === 'object' && corr.type === 'manual') man++;
            }}
            document.getElementById('count-tesseract').textContent = t;
            document.getElementById('count-mangaocr').textContent = m;
            document.getElementById('count-manual').textContent = man;
            document.getElementById('count-investigate').textContent = i;
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
            const c = document.getElementById('show-claude').checked;
            const t = document.getElementById('show-tesseract').checked;
            const m = document.getElementById('show-mangaocr').checked;
            document.querySelectorAll('.char-claude').forEach(el => el.classList.toggle('hidden', !c));
            document.querySelectorAll('.char-tesseract').forEach(el => el.classList.toggle('hidden', !t));
            document.querySelectorAll('.char-mangaocr').forEach(el => el.classList.toggle('hidden', !m));
            let label = [];
            if (c) label.push('Claude');
            if (t) label.push('Tesseract');
            if (m) label.push('Manga-OCR');
            document.getElementById('current-overlay').textContent = label.length ? label.join('+') : 'None';
        }}

        function exportCorrections() {{
            const data = [];
            for (const idx in corrections) {{
                const charData = CHARS[idx];
                data.push({{
                    texture: TEXTURE,
                    index: parseInt(idx),
                    grid_x: charData.grid_x,
                    grid_y: charData.grid_y,
                    correction: corrections[idx],
                    claude: charData.claude,
                    tesseract: charData.tesseract,
                    mangaocr: charData.mangaocr
                }});
            }}
            data.sort((a, b) => a.index - b.index);
            const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = TEXTURE + '_corrections.json';
            a.click();
        }}

        function exportFinalMapping() {{
            const finalMap = [];
            for (const charData of CHARS) {{
                let finalChar = charData.claude;  // Default to Claude
                if (corrections[charData.index]) {{
                    const corr = corrections[charData.index];
                    if (corr === 'tesseract') finalChar = charData.tesseract;
                    else if (corr === 'mangaocr') finalChar = charData.mangaocr;
                    else if (corr === 'investigate') finalChar = '???';
                    else if (typeof corr === 'object' && corr.type === 'manual') finalChar = corr.char;
                }}
                finalMap.push({{
                    texture: TEXTURE,
                    index: charData.index,
                    grid_x: charData.grid_x,
                    grid_y: charData.grid_y,
                    character: finalChar
                }});
            }}
            const blob = new Blob([JSON.stringify(finalMap, null, 2)], {{type: 'application/json'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = TEXTURE + '_final.json';
            a.click();
        }}

        function clearCorrections() {{
            if (confirm('Clear all corrections?')) {{
                for (const idx in corrections) delete corrections[idx];
                document.querySelectorAll('.cell').forEach(c => c.classList.remove('use-tesseract', 'use-mangaocr', 'use-manual', 'investigate'));
                saveCorrections();
                updateStats();
            }}
        }}

        function exportAllTextures() {{
            // Export corrections from all textures stored in localStorage
            const allCorrections = {{}};
            for (let i = 1; i <= 6; i++) {{
                const key = 'ff7_corrections_jafont_' + i;
                const saved = localStorage.getItem(key);
                if (saved) {{
                    allCorrections['jafont_' + i] = JSON.parse(saved);
                }}
            }}
            const blob = new Blob([JSON.stringify(allCorrections, null, 2)], {{type: 'application/json'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'all_textures_corrections.json';
            a.click();
        }}

        initGrid();
        loadCorrections();  // Load saved corrections from localStorage
        updateStats();
    </script>
</body>
</html>'''
    return html


def main():
    print("Creating viewer v2 (Claude = default)...")
    OUTPUT_DIR.mkdir(exist_ok=True)

    claude_map = load_csv_mapping(CLAUDE_CSV)
    tesseract_map = load_csv_mapping(TESSERACT_CSV)
    mangaocr_map = load_csv_mapping(MANGAOCR_CSV)

    for texture_name in ['jafont_1', 'jafont_2', 'jafont_3', 'jafont_4', 'jafont_5', 'jafont_6']:
        print(f"Processing {texture_name}...")
        base64_img = image_to_base64(FONT_DIR / f"{texture_name}.png")
        html = generate_html(texture_name, base64_img, claude_map, tesseract_map, mangaocr_map)
        with open(OUTPUT_DIR / f"{texture_name}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Saved: {texture_name}.html")

    print("\nDone! Open jafont_1.html to start verification.")


if __name__ == "__main__":
    main()

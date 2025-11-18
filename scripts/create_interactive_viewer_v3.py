#!/usr/bin/env python3
"""
Interactive viewer v3: Enhanced keyboard navigation and baseline selection.
Created: 2025-11-18 09:59:00 JST
Session-ID: 1021bc57-9aa2-41fe-baad-a6b89b252744

New Features:
- Selectable baseline OCR model (Claude/Tesseract/Manga-OCR)
- Keyboard navigation: Arrow keys, F/J/H for selections
- Continuous mode auto-advance
- Transparency slider for overlays
- Visual current cell indicator
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
    <title>FF7 Charmap Verification v3 - {texture_name}</title>
    <style>
        body {{
            font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "MS Gothic", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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

        .baseline-selector {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .baseline-selector label {{
            margin-right: 20px;
            cursor: pointer;
        }}

        .controls {{
            background: #2a2a2a;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
        }}
        .transparency-control {{
            margin-top: 10px;
        }}
        .transparency-control input[type="range"] {{
            width: 200px;
            vertical-align: middle;
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
        .cell.current {{
            border: 3px dotted #FFC107 !important;
            box-shadow: 0 0 10px rgba(255, 193, 7, 0.5);
        }}
        .cell.use-claude {{ background: rgba(255, 87, 34, 0.3); border: 2px solid #FF5722; }}
        .cell.use-tesseract {{ background: rgba(33, 150, 243, 0.3); border: 2px solid #2196F3; }}
        .cell.use-mangaocr {{ background: rgba(76, 175, 80, 0.3); border: 2px solid #4CAF50; }}
        .cell.use-manual {{ background: rgba(156, 39, 176, 0.3); border: 2px solid #9C27B0; }}
        .cell.investigate {{ background: rgba(255, 193, 7, 0.3); border: 2px solid #FFC107; }}
        .cell.empty {{ background: rgba(96, 96, 96, 0.3); border: 2px solid #606060; }}

        .cell-char {{
            position: absolute;
            font-size: 56px;
            font-weight: bold;
            pointer-events: none;
            top: 0px; left: 2px;
            font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "MS Gothic", "Hiragino Sans", sans-serif;
        }}
        .char-claude {{
            color: rgba(255, 87, 34, 0.9);
            text-shadow:
                0 0 3px black,
                -2px -2px 0 rgba(255, 193, 7, 0.7),
                2px -2px 0 rgba(255, 193, 7, 0.7),
                -2px 2px 0 rgba(255, 193, 7, 0.7),
                2px 2px 0 rgba(255, 193, 7, 0.7),
                -2px 0 0 rgba(255, 193, 7, 0.7),
                2px 0 0 rgba(255, 193, 7, 0.7),
                0 -2px 0 rgba(255, 193, 7, 0.7),
                0 2px 0 rgba(255, 193, 7, 0.7);
        }}
        .char-tesseract {{
            color: rgba(33, 150, 243, 0.9);
            text-shadow:
                0 0 3px black,
                -2px -2px 0 rgba(255, 193, 7, 0.7),
                2px -2px 0 rgba(255, 193, 7, 0.7),
                -2px 2px 0 rgba(255, 193, 7, 0.7),
                2px 2px 0 rgba(255, 193, 7, 0.7),
                -2px 0 0 rgba(255, 193, 7, 0.7),
                2px 0 0 rgba(255, 193, 7, 0.7),
                0 -2px 0 rgba(255, 193, 7, 0.7),
                0 2px 0 rgba(255, 193, 7, 0.7);
        }}
        .char-mangaocr {{
            color: rgba(76, 175, 80, 0.9);
            text-shadow:
                0 0 3px black,
                -2px -2px 0 rgba(255, 193, 7, 0.7),
                2px -2px 0 rgba(255, 193, 7, 0.7),
                -2px 2px 0 rgba(255, 193, 7, 0.7),
                2px 2px 0 rgba(255, 193, 7, 0.7),
                -2px 0 0 rgba(255, 193, 7, 0.7),
                2px 0 0 rgba(255, 193, 7, 0.7),
                0 -2px 0 rgba(255, 193, 7, 0.7),
                0 2px 0 rgba(255, 193, 7, 0.7);
        }}
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
        .keyboard-hint {{
            font-size: 12px;
            color: #888;
            margin-top: -5px;
            margin-bottom: 10px;
        }}
        .char-display {{
            font-size: 60px;
            margin: 10px 0;
            padding: 10px;
            background: #333;
            border-radius: 5px;
            font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", "MS Gothic", "Hiragino Sans", sans-serif;
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
    <h1>FF7 Charmap v3 - {texture_name}</h1>

    <div class="nav-links">
        <a href="jafont_1.html">jafont_1</a>
        <a href="jafont_2.html">jafont_2</a>
        <a href="jafont_3.html">jafont_3</a>
        <a href="jafont_4.html">jafont_4</a>
        <a href="jafont_5.html">jafont_5</a>
        <a href="jafont_6.html">jafont_6</a>
    </div>

    <div class="instructions">
        <strong>Keyboard Shortcuts:</strong><br>
        • <strong>Arrow keys:</strong> Navigate grid | <strong>Enter/Click:</strong> Open cell<br>
        • <strong>F:</strong> Claude | <strong>J:</strong> Manga-OCR | <strong>H:</strong> Tesseract | <strong>G:</strong> Manual | <strong>;:</strong> Investigate<br>
        • <strong>Right-click:</strong> Toggle overlays | <strong>Esc:</strong> Cancel | <strong>?:</strong> Help
    </div>

    <div class="baseline-selector">
        <strong>Baseline OCR Model:</strong>
        <label><input type="radio" name="baseline" value="claude" onchange="changeBaseline()"> <span style="color:#FF5722">Claude</span></label>
        <label><input type="radio" name="baseline" value="tesseract" onchange="changeBaseline()"> <span style="color:#2196F3">Tesseract</span></label>
        <label><input type="radio" name="baseline" value="mangaocr" onchange="changeBaseline()"> <span style="color:#4CAF50">Manga-OCR</span></label>
        <span style="margin-left: 20px;">
            <label><input type="checkbox" id="continuous-mode"> Continuous Mode (auto-advance)</label>
        </span>
    </div>

    <div class="controls">
        <strong>Overlay:</strong> <span id="current-overlay">None</span><br>
        <label><input type="checkbox" id="show-claude" onchange="updateOverlay()"> Claude</label>
        <input type="color" id="color-claude" value="#ff5722" onchange="updateOverlayColors()" title="Claude Color">
        &nbsp;&nbsp;
        <label><input type="checkbox" id="show-tesseract" onchange="updateOverlay()"> Tesseract</label>
        <input type="color" id="color-tesseract" value="#2196f3" onchange="updateOverlayColors()" title="Tesseract Color">
        &nbsp;&nbsp;
        <label><input type="checkbox" id="show-mangaocr" onchange="updateOverlay()"> Manga-OCR</label>
        <input type="color" id="color-mangaocr" value="#4caf50" onchange="updateOverlayColors()" title="Manga-OCR Color">
        <br>
        <label><input type="checkbox" id="show-final-comparison" onchange="toggleFinalComparison()"> <strong>Final Comparison Mode</strong></label>
        <input type="color" id="color-final" value="#ffffff" onchange="updateFinalComparisonColor()" title="Final Comparison Color">
        <div class="transparency-control">
            <strong>Character Opacity:</strong>
            <input type="range" id="char-opacity-slider" min="0" max="100" value="90" oninput="updateCharacterStyle()">
            <span id="char-opacity-value">90%</span>
            &nbsp;&nbsp;
            <strong>Border Opacity:</strong>
            <input type="range" id="border-opacity-slider" min="0" max="100" value="70" oninput="updateCharacterStyle()">
            <span id="border-opacity-value">70%</span>
        </div>
        <div class="transparency-control">
            <strong>Position X:</strong>
            <input type="range" id="pos-x-slider" min="-20" max="20" value="2" oninput="updateCharacterStyle()">
            <span id="pos-x-value">2px</span>
            &nbsp;&nbsp;
            <strong>Position Y:</strong>
            <input type="range" id="pos-y-slider" min="-20" max="20" value="0" oninput="updateCharacterStyle()">
            <span id="pos-y-value">0px</span>
        </div>
        <div class="transparency-control">
            <strong>Font Weight:</strong>
            <input type="range" id="font-weight-slider" min="100" max="900" step="100" value="700" oninput="updateCharacterStyle()">
            <span id="font-weight-value">700 (Bold)</span>
            &nbsp;&nbsp;
            <strong>Font Size:</strong>
            <input type="range" id="font-size-slider" min="40" max="70" value="56" oninput="updateCharacterStyle()">
            <span id="font-size-value">56px</span>
        </div>
    </div>

    <div class="stats">
        <strong>Progress:</strong> Corrected <span id="total-corrections">0</span> / 256
        (<span id="remaining">256</span> using baseline)
        <br>
        <strong>Corrections:</strong>
        <span style="color:#2196F3">Tesseract: <span id="count-tesseract">0</span></span> |
        <span style="color:#4CAF50">Manga-OCR: <span id="count-mangaocr">0</span></span> |
        <span style="color:#9C27B0">Manual: <span id="count-manual">0</span></span> |
        <span style="color:#606060">Empty: <span id="count-empty">0</span></span> |
        <span style="color:#FFC107">Investigate: <span id="count-investigate">0</span></span>
        <br>
        <button class="export-btn" onclick="exportCorrections()">Export This Texture</button>
        <button class="export-btn" onclick="exportFinalMapping()">Export Final Mapping</button>
        <button class="export-btn" onclick="exportAllTextures()">Export ALL Textures</button>
        <button class="export-btn" onclick="exportCompactMapping()">Export Compact (for LLM)</button>
        <button class="export-btn red" onclick="clearCorrections()">Clear This Texture</button>
        <button class="export-btn" onclick="jumpToNextUncorrected()">Jump to Next Uncorrected</button>
    </div>

    <div class="container" oncontextmenu="cycleOverlay(event); return false;">
        <img class="base-image" src="{base64_img}" alt="{texture_name}">
        <div class="grid-overlay" id="grid-overlay"></div>
    </div>

    <!-- Investigation List -->
    <div id="investigation-list" style="margin-top: 20px; padding: 15px; background: #2a2a2a; border-radius: 8px; display: none;">
        <h3 style="color: #FFC107; margin-top: 0;">Cells Needing Investigation (<span id="investigation-count">0</span>)</h3>
        <div id="investigation-items" style="display: flex; flex-wrap: wrap; gap: 10px;">
        </div>
    </div>

    <!-- Modal for choosing correction -->
    <div id="modal" class="modal" onclick="if(event.target===this) closeModal()">
        <div class="modal-content">
            <h3>Cell <span id="modal-index"></span> (<span id="modal-coords"></span>)</h3>
            <div class="keyboard-hint">Keyboard: F=Claude | J=Manga-OCR | H=Tesseract | G=Manual | ;=Investigate | E=Empty | Del=Remove | Esc=Cancel</div>

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
                ✓ Use Claude: <span id="btn-claude"></span> <strong>[F]</strong>
            </button>
            <button class="choice-btn choice-tesseract" onclick="setCorrection('tesseract')">
                Use Tesseract: <span id="btn-tesseract"></span> <strong>[H]</strong>
            </button>
            <button class="choice-btn choice-mangaocr" onclick="setCorrection('mangaocr')">
                Use Manga-OCR: <span id="btn-mangaocr"></span> <strong>[J]</strong>
            </button>
            <div style="margin: 10px 0; padding: 10px; background: #444; border-radius: 5px;">
                <label style="display: block; margin-bottom: 5px; color: #FFC107;">Manual Entry:</label>
                <input type="text" id="manual-input" maxlength="1" style="font-size: 36px; width: 60px; text-align: center; padding: 5px;" placeholder="?">
                <button class="choice-btn" style="display: inline-block; width: auto; background: #9C27B0; margin-left: 10px;" onclick="setManualCorrection()">
                    Use Manual [G or Enter]
                </button>
                <div style="margin-top: 10px;">
                    <strong style="font-size: 12px; color: #888;">Quick Symbols:</strong><br>
                    <div id="symbol-picker" style="display: flex; flex-wrap: wrap; gap: 5px; margin-top: 5px;">
                    </div>
                </div>
            </div>
            <button class="choice-btn choice-investigate" onclick="setCorrection('investigate')">
                ⚠ Needs Investigation <strong>[;]</strong>
            </button>
            <button class="choice-btn" style="background: #666; color: white;" onclick="setCorrection('empty')">
                ∅ Empty Cell <strong>[E]</strong>
            </button>
            <button class="choice-btn" style="background: #FF5722; color: white;" onclick="removeCorrection()">
                ✗ Remove Selection <strong>[Delete]</strong>
            </button>
            <button class="choice-btn choice-cancel" onclick="closeModal()">Cancel [Esc]</button>
        </div>
    </div>

    <script>
        const TEXTURE = "{texture_name}";
        const CHARS = {chars_json};
        let corrections = {{}};
        let currentIndex = 0;
        let overlayMode = 0;
        let baselineModel = 'claude';

        // Store CHARS data in localStorage for cross-texture export
        localStorage.setItem('ff7_chars_' + TEXTURE, JSON.stringify(CHARS));

        // Common symbols found in FF7 fonts (especially jafont_1)
        const COMMON_SYMBOLS = [
            '→', '←', '↑', '↓',  // Arrows
            '⋮', '…', '•', '·',  // Dots/ellipses
            '※', '§', '¶', '†',  // Special marks
            '「', '」', '『', '』',  // Japanese quotes
            '【', '】', '《', '》',  // Brackets
            '◯', '○', '●', '△',  // Shapes
            '×', '÷', '±', '≒',  // Math
            '〜', '～', 'ー', '－'   // Dashes
        ];

        // Keyboard navigation
        document.addEventListener('keydown', function(e) {{
            // If modal is open, handle modal shortcuts
            if (document.getElementById('modal').style.display === 'block') {{
                if (e.key === 'Escape') {{
                    closeModal();
                    e.preventDefault();
                }}
                else if (e.key === 'f' || e.key === 'F') {{
                    setCorrection('claude');
                    e.preventDefault();
                }}
                else if (e.key === 'j' || e.key === 'J') {{
                    setCorrection('mangaocr');
                    e.preventDefault();
                }}
                else if (e.key === 'h' || e.key === 'H') {{
                    setCorrection('tesseract');
                    e.preventDefault();
                }}
                else if (e.key === 'g' || e.key === 'G') {{
                    // Focus manual input field
                    document.getElementById('manual-input').focus();
                    e.preventDefault();
                }}
                else if (e.key === ';' || e.key === ':') {{
                    setCorrection('investigate');
                    e.preventDefault();
                }}
                else if (e.key === 'e' || e.key === 'E') {{
                    setCorrection('empty');
                    e.preventDefault();
                }}
                else if (e.key === 'Delete' || e.key === 'Backspace') {{
                    removeCorrection();
                    e.preventDefault();
                }}
                else if (e.key === 'Enter' && document.activeElement.id === 'manual-input') {{
                    setManualCorrection();
                    e.preventDefault();
                }}
                return;
            }}

            // Grid navigation
            if (e.key === 'ArrowRight') {{
                moveCurrentCell(1);
                e.preventDefault();
            }}
            else if (e.key === 'ArrowLeft') {{
                moveCurrentCell(-1);
                e.preventDefault();
            }}
            else if (e.key === 'ArrowDown') {{
                moveCurrentCell(16);  // Move down one row
                e.preventDefault();
            }}
            else if (e.key === 'ArrowUp') {{
                moveCurrentCell(-16);  // Move up one row
                e.preventDefault();
            }}
            else if (e.key === 'Enter') {{
                openModal(currentIndex);
                e.preventDefault();
            }}
            else if (e.key === '?') {{
                alert('Keyboard Shortcuts:\\n\\n' +
                      'Arrow Keys: Navigate grid\\n' +
                      'Enter: Open cell modal\\n' +
                      'F: Select Claude\\n' +
                      'J: Select Manga-OCR\\n' +
                      'H: Select Tesseract\\n' +
                      'G: Focus manual entry field\\n' +
                      ';: Mark for investigation\\n' +
                      'Esc: Close modal\\n' +
                      'Right-click: Toggle overlays');
                e.preventDefault();
            }}
        }});

        function moveCurrentCell(delta) {{
            const newIndex = currentIndex + delta;
            if (newIndex >= 0 && newIndex < 256) {{
                setCurrentCell(newIndex);
            }}
        }}

        function setCurrentCell(index) {{
            // Remove current highlight
            document.querySelectorAll('.cell.current').forEach(c => c.classList.remove('current'));

            currentIndex = index;
            const cell = document.getElementById('cell-' + index);
            if (cell) {{
                cell.classList.add('current');
                // Scroll into view if needed
                cell.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
            }}
        }}

        function changeBaseline() {{
            const radios = document.getElementsByName('baseline');
            for (const radio of radios) {{
                if (radio.checked) {{
                    baselineModel = radio.value;
                    break;
                }}
            }}
            // Save baseline per texture
            localStorage.setItem('ff7_baseline_' + TEXTURE, baselineModel);
            updateStats();
        }}

        function loadBaseline() {{
            const saved = localStorage.getItem('ff7_baseline_' + TEXTURE);
            if (saved) {{
                baselineModel = saved;
                const radio = document.querySelector(`input[name="baseline"][value="${{saved}}"]`);
                if (radio) radio.checked = true;
            }} else {{
                // Default to claude
                document.querySelector('input[name="baseline"][value="claude"]').checked = true;
            }}
        }}

        function loadCorrections() {{
            const saved = localStorage.getItem('ff7_corrections_' + TEXTURE);
            if (saved) {{
                corrections = JSON.parse(saved);
                // Apply visual state
                for (const idx in corrections) {{
                    const cell = document.getElementById('cell-' + idx);
                    if (cell) {{
                        const corr = corrections[idx];
                        if (corr === 'claude') cell.classList.add('use-claude');
                        else if (corr === 'tesseract') cell.classList.add('use-tesseract');
                        else if (corr === 'mangaocr') cell.classList.add('use-mangaocr');
                        else if (corr === 'investigate') cell.classList.add('investigate');
                        else if (corr === 'empty') cell.classList.add('empty');
                        else if (typeof corr === 'object' && corr.type === 'manual') {{
                            cell.classList.add('use-manual');
                            // Populate manual character overlay
                            const manualEl = cell.querySelector('.char-manual');
                            if (manualEl) {{
                                manualEl.textContent = corr.char;
                            }}
                        }}
                    }}
                }}
            }}

            // Load character style preferences (PER TEXTURE)
            const savedCharOpacity = localStorage.getItem('ff7_char_opacity_' + TEXTURE);
            const savedBorderOpacity = localStorage.getItem('ff7_border_opacity_' + TEXTURE);
            const savedPosX = localStorage.getItem('ff7_pos_x_' + TEXTURE);
            const savedPosY = localStorage.getItem('ff7_pos_y_' + TEXTURE);
            const savedFontWeight = localStorage.getItem('ff7_font_weight_' + TEXTURE);
            const savedFontSize = localStorage.getItem('ff7_font_size_' + TEXTURE);

            if (savedCharOpacity) document.getElementById('char-opacity-slider').value = savedCharOpacity;
            if (savedBorderOpacity) document.getElementById('border-opacity-slider').value = savedBorderOpacity;
            if (savedPosX) document.getElementById('pos-x-slider').value = savedPosX;
            if (savedPosY) document.getElementById('pos-y-slider').value = savedPosY;
            if (savedFontWeight) document.getElementById('font-weight-slider').value = savedFontWeight;
            if (savedFontSize) document.getElementById('font-size-slider').value = savedFontSize;

            // Load overlay colors (PER TEXTURE)
            const savedColorClaude = localStorage.getItem('ff7_color_claude_' + TEXTURE);
            const savedColorTesseract = localStorage.getItem('ff7_color_tesseract_' + TEXTURE);
            const savedColorMangaocr = localStorage.getItem('ff7_color_mangaocr_' + TEXTURE);
            const savedColorFinal = localStorage.getItem('ff7_color_final_' + TEXTURE);

            if (savedColorClaude) document.getElementById('color-claude').value = savedColorClaude;
            if (savedColorTesseract) document.getElementById('color-tesseract').value = savedColorTesseract;
            if (savedColorMangaocr) document.getElementById('color-mangaocr').value = savedColorMangaocr;
            if (savedColorFinal) document.getElementById('color-final').value = savedColorFinal;

            // Load overlay toggle states (PER TEXTURE)
            const savedShowClaude = localStorage.getItem('ff7_show_claude_' + TEXTURE);
            const savedShowTesseract = localStorage.getItem('ff7_show_tesseract_' + TEXTURE);
            const savedShowMangaocr = localStorage.getItem('ff7_show_mangaocr_' + TEXTURE);
            const savedFinalComparison = localStorage.getItem('ff7_final_comparison_' + TEXTURE);

            if (savedShowClaude !== null) document.getElementById('show-claude').checked = (savedShowClaude === 'true');
            if (savedShowTesseract !== null) document.getElementById('show-tesseract').checked = (savedShowTesseract === 'true');
            if (savedShowMangaocr !== null) document.getElementById('show-mangaocr').checked = (savedShowMangaocr === 'true');
            if (savedFinalComparison !== null) document.getElementById('show-final-comparison').checked = (savedFinalComparison === 'true');

            updateCharacterStyle();
            updateOverlayColors();
            updateOverlay();  // Apply loaded overlay states

            // Apply final comparison if it was enabled
            if (savedFinalComparison === 'true') {{
                toggleFinalComparison();
            }}
        }}

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

                // Add manual character overlay element (initially empty and hidden)
                const manualEl = document.createElement('div');
                manualEl.className = 'cell-char char-manual hidden';
                manualEl.style.color = 'rgba(156, 39, 176, 0.9)';  // Purple
                manualEl.style.textShadow = '0 0 3px black, -2px -2px 0 rgba(255, 193, 7, 0.7), 2px -2px 0 rgba(255, 193, 7, 0.7), -2px 2px 0 rgba(255, 193, 7, 0.7), 2px 2px 0 rgba(255, 193, 7, 0.7), -2px 0 0 rgba(255, 193, 7, 0.7), 2px 0 0 rgba(255, 193, 7, 0.7), 0 -2px 0 rgba(255, 193, 7, 0.7), 0 2px 0 rgba(255, 193, 7, 0.7)';
                cell.appendChild(manualEl);

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
            ctx.drawImage(baseImg, sx, sy, 64, 64, 0, 0, 128, 128);

            // Clear and focus manual input field
            document.getElementById('manual-input').value = '';

            // Populate symbol picker
            const symbolPicker = document.getElementById('symbol-picker');
            while (symbolPicker.firstChild) {{
                symbolPicker.removeChild(symbolPicker.firstChild);
            }}

            for (const symbol of COMMON_SYMBOLS) {{
                const btn = document.createElement('button');
                btn.textContent = symbol;
                btn.style.cssText = 'padding: 5px 10px; background: #666; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 20px;';
                btn.onclick = () => {{
                    document.getElementById('manual-input').value = symbol;
                    document.getElementById('manual-input').focus();
                }};
                btn.onmouseover = () => btn.style.background = '#888';
                btn.onmouseout = () => btn.style.background = '#666';
                symbolPicker.appendChild(btn);
            }}

            document.getElementById('modal').style.display = 'block';
        }}

        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
        }}

        function setCorrection(choice) {{
            const cell = document.getElementById('cell-' + currentIndex);
            cell.classList.remove('use-claude', 'use-tesseract', 'use-mangaocr', 'use-manual', 'investigate', 'empty');

            // Always save the correction (including 'claude')
            corrections[currentIndex] = choice;

            if (choice === 'claude') cell.classList.add('use-claude');
            else if (choice === 'tesseract') cell.classList.add('use-tesseract');
            else if (choice === 'mangaocr') cell.classList.add('use-mangaocr');
            else if (choice === 'investigate') cell.classList.add('investigate');
            else if (choice === 'empty') cell.classList.add('empty');

            saveCorrections();
            updateStats();
            updateOverlay();  // Refresh overlay to show selected character
            closeModal();

            // Continuous mode: auto-advance
            if (document.getElementById('continuous-mode').checked && currentIndex < 255) {{
                setTimeout(() => {{
                    moveCurrentCell(1);
                    openModal(currentIndex);
                }}, 100);
            }}
        }}

        function setManualCorrection() {{
            const input = document.getElementById('manual-input').value;
            if (input && input.length === 1) {{
                const cell = document.getElementById('cell-' + currentIndex);
                cell.classList.remove('use-claude', 'use-tesseract', 'use-mangaocr', 'use-manual', 'investigate');
                corrections[currentIndex] = {{ type: 'manual', char: input }};
                cell.classList.add('use-manual');

                // Update the manual character overlay element
                const manualEl = cell.querySelector('.char-manual');
                if (manualEl) {{
                    manualEl.textContent = input;
                }}

                saveCorrections();
                updateStats();
                updateOverlay();  // Refresh overlay to show manual character
                closeModal();

                // Continuous mode: auto-advance
                if (document.getElementById('continuous-mode').checked && currentIndex < 255) {{
                    setTimeout(() => {{
                        moveCurrentCell(1);
                        openModal(currentIndex);
                    }}, 100);
                }}
            }} else {{
                alert('Please enter exactly one character');
            }}
        }}

        function removeCorrection() {{
            // Remove the correction for current cell, reverting to baseline
            const cell = document.getElementById('cell-' + currentIndex);

            // Remove all correction classes
            cell.classList.remove('use-claude', 'use-tesseract', 'use-mangaocr', 'use-manual', 'investigate', 'empty');

            // Clear manual character overlay if it exists
            const manualEl = cell.querySelector('.char-manual');
            if (manualEl) {{
                manualEl.textContent = '';
            }}

            // Delete the correction from the corrections object
            delete corrections[currentIndex];

            // Save and update
            saveCorrections();
            updateStats();
            updateOverlay();  // Refresh overlay to show baseline character
            closeModal();

            // Continuous mode: auto-advance
            if (document.getElementById('continuous-mode').checked && currentIndex < 255) {{
                setTimeout(() => {{
                    moveCurrentCell(1);
                    openModal(currentIndex);
                }}, 100);
            }}
        }}

        function updateStats() {{
            let c = 0, t = 0, m = 0, man = 0, i = 0, emp = 0;
            for (const idx in corrections) {{
                const corr = corrections[idx];
                if (corr === 'claude') c++;
                else if (corr === 'tesseract') t++;
                else if (corr === 'mangaocr') m++;
                else if (corr === 'investigate') i++;
                else if (corr === 'empty') emp++;
                else if (typeof corr === 'object' && corr.type === 'manual') man++;
            }}
            const total = c + t + m + man + i + emp;
            const remaining = 256 - total;

            document.getElementById('count-tesseract').textContent = t;
            document.getElementById('count-mangaocr').textContent = m;
            document.getElementById('count-manual').textContent = man;
            document.getElementById('count-empty').textContent = emp;
            document.getElementById('count-investigate').textContent = i;
            document.getElementById('total-corrections').textContent = total;
            document.getElementById('remaining').textContent = remaining;

            updateInvestigationList();
        }}

        function updateInvestigationList() {{
            const investigationItems = [];
            for (const idx in corrections) {{
                if (corrections[idx] === 'investigate') {{
                    investigationItems.push(parseInt(idx));
                }}
            }}

            const listDiv = document.getElementById('investigation-list');
            const itemsDiv = document.getElementById('investigation-items');
            const countSpan = document.getElementById('investigation-count');

            countSpan.textContent = investigationItems.length;

            if (investigationItems.length === 0) {{
                listDiv.style.display = 'none';
                return;
            }}

            listDiv.style.display = 'block';
            // Clear items safely
            while (itemsDiv.firstChild) {{
                itemsDiv.removeChild(itemsDiv.firstChild);
            }}

            investigationItems.sort((a, b) => a - b);

            for (const idx of investigationItems) {{
                const data = CHARS[idx];
                const btn = document.createElement('button');
                btn.style.cssText = 'padding: 8px 12px; background: #FFC107; color: black; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;';
                btn.textContent = 'Cell ' + idx + ' (' + data.grid_x + ',' + data.grid_y + ')';
                btn.onclick = () => {{
                    setCurrentCell(idx);
                    openModal(idx);
                }};
                itemsDiv.appendChild(btn);
            }}
        }}

        function toggleFinalComparison() {{
            const enabled = document.getElementById('show-final-comparison').checked;

            if (enabled) {{
                // Save current overlay state before hiding
                const wasClaude = document.getElementById('show-claude').checked;
                const wasTesseract = document.getElementById('show-tesseract').checked;
                const wasMangaocr = document.getElementById('show-mangaocr').checked;

                localStorage.setItem('ff7_prev_claude_' + TEXTURE, wasClaude);
                localStorage.setItem('ff7_prev_tesseract_' + TEXTURE, wasTesseract);
                localStorage.setItem('ff7_prev_mangaocr_' + TEXTURE, wasMangaocr);

                // Hide all normal overlays when final comparison is on
                document.getElementById('show-claude').checked = false;
                document.getElementById('show-tesseract').checked = false;
                document.getElementById('show-mangaocr').checked = false;
                updateOverlay();
            }} else {{
                // Restore previous overlay state
                const prevClaude = localStorage.getItem('ff7_prev_claude_' + TEXTURE) === 'true';
                const prevTesseract = localStorage.getItem('ff7_prev_tesseract_' + TEXTURE) === 'true';
                const prevMangaocr = localStorage.getItem('ff7_prev_mangaocr_' + TEXTURE) === 'true';

                document.getElementById('show-claude').checked = prevClaude;
                document.getElementById('show-tesseract').checked = prevTesseract;
                document.getElementById('show-mangaocr').checked = prevMangaocr;
                updateOverlay();
            }}

            // Save final comparison mode state
            localStorage.setItem('ff7_final_comparison_' + TEXTURE, enabled);

            // Add final comparison characters
            for (const data of CHARS) {{
                const cell = document.getElementById('cell-' + data.index);
                let finalChar = '';

                // Determine what character to show
                if (corrections[data.index]) {{
                    const corr = corrections[data.index];
                    if (corr === 'tesseract') finalChar = data.tesseract;
                    else if (corr === 'mangaocr') finalChar = data.mangaocr;
                    else if (corr === 'claude') finalChar = data.claude;
                    else if (typeof corr === 'object' && corr.type === 'manual') finalChar = corr.char;
                    else if (corr === 'investigate') finalChar = ''; // Don't show for investigation
                    else if (corr === 'empty') finalChar = ''; // Empty cell - don't show character
                }} else {{
                    // Use baseline
                    finalChar = data[baselineModel];
                }}

                // Find or create final comparison overlay
                let finalEl = cell.querySelector('.cell-char-final');
                if (!finalEl) {{
                    finalEl = document.createElement('div');
                    finalEl.className = 'cell-char cell-char-final';
                    finalEl.style.cssText = 'position: absolute; font-size: 56px; font-weight: bold; pointer-events: none; top: 0px; left: 2px; color: rgba(255, 255, 255, 0.95); text-shadow: 0 0 3px black, -2px -2px 0 rgba(255, 193, 7, 0.7), 2px -2px 0 rgba(255, 193, 7, 0.7), -2px 2px 0 rgba(255, 193, 7, 0.7), 2px 2px 0 rgba(255, 193, 7, 0.7), -2px 0 0 rgba(255, 193, 7, 0.7), 2px 0 0 rgba(255, 193, 7, 0.7), 0 -2px 0 rgba(255, 193, 7, 0.7), 0 2px 0 rgba(255, 193, 7, 0.7);';
                    cell.appendChild(finalEl);
                }}

                finalEl.textContent = finalChar;
                finalEl.style.display = enabled ? 'block' : 'none';
            }}
        }}

        function jumpToNextUncorrected() {{
            for (let i = currentIndex + 1; i < 256; i++) {{
                if (!corrections[i]) {{
                    setCurrentCell(i);
                    openModal(i);
                    return;
                }}
            }}
            // Wrap around
            for (let i = 0; i <= currentIndex; i++) {{
                if (!corrections[i]) {{
                    setCurrentCell(i);
                    openModal(i);
                    return;
                }}
            }}
            alert('All cells have corrections!');
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

            // For each cell, check if it has a correction
            for (const data of CHARS) {{
                const cell = document.getElementById('cell-' + data.index);
                const claudeEl = cell.querySelector('.char-claude');
                const tesseractEl = cell.querySelector('.char-tesseract');
                const mangaocrEl = cell.querySelector('.char-mangaocr');
                const manualEl = cell.querySelector('.char-manual');

                const correction = corrections[data.index];

                // If cell has a correction (explicit selection)
                if (correction) {{
                    // Hide all overlays first
                    if (claudeEl) claudeEl.classList.add('hidden');
                    if (tesseractEl) tesseractEl.classList.add('hidden');
                    if (mangaocrEl) mangaocrEl.classList.add('hidden');
                    if (manualEl) manualEl.classList.add('hidden');

                    // Show only the selected one
                    if (correction === 'claude' && claudeEl) {{
                        claudeEl.classList.remove('hidden');
                    }} else if (correction === 'tesseract' && tesseractEl) {{
                        tesseractEl.classList.remove('hidden');
                    }} else if (correction === 'mangaocr' && mangaocrEl) {{
                        mangaocrEl.classList.remove('hidden');
                    }} else if (typeof correction === 'object' && correction.type === 'manual' && manualEl) {{
                        // Show manual character
                        manualEl.classList.remove('hidden');
                    }}
                    // For 'investigate', keep all hidden
                }} else {{
                    // No correction - use normal overlay toggles
                    if (claudeEl) claudeEl.classList.toggle('hidden', !c);
                    if (tesseractEl) tesseractEl.classList.toggle('hidden', !t);
                    if (mangaocrEl) mangaocrEl.classList.toggle('hidden', !m);
                    if (manualEl) manualEl.classList.add('hidden');  // Manual always hidden unless selected
                }}
            }}

            let label = [];
            if (c) label.push('Claude');
            if (t) label.push('Tesseract');
            if (m) label.push('Manga-OCR');
            document.getElementById('current-overlay').textContent = label.length ? label.join('+') : 'None';

            // Save overlay state (PER TEXTURE)
            localStorage.setItem('ff7_show_claude_' + TEXTURE, c);
            localStorage.setItem('ff7_show_tesseract_' + TEXTURE, t);
            localStorage.setItem('ff7_show_mangaocr_' + TEXTURE, m);
        }}

        function updateCharacterStyle() {{
            const charOpacity = document.getElementById('char-opacity-slider').value;
            const borderOpacity = document.getElementById('border-opacity-slider').value;
            const posX = document.getElementById('pos-x-slider').value;
            const posY = document.getElementById('pos-y-slider').value;
            const fontWeight = document.getElementById('font-weight-slider').value;
            const fontSize = document.getElementById('font-size-slider').value;

            const charOpacityDecimal = charOpacity / 100;
            const borderOpacityDecimal = borderOpacity / 100;

            // Update display values
            document.getElementById('char-opacity-value').textContent = charOpacity + '%';
            document.getElementById('border-opacity-value').textContent = borderOpacity + '%';
            document.getElementById('pos-x-value').textContent = posX + 'px';
            document.getElementById('pos-y-value').textContent = posY + 'px';
            document.getElementById('font-size-value').textContent = fontSize + 'px';

            const weightLabel = fontWeight === '100' ? 'Thin' :
                              fontWeight === '200' ? 'Extra Light' :
                              fontWeight === '300' ? 'Light' :
                              fontWeight === '400' ? 'Normal' :
                              fontWeight === '500' ? 'Medium' :
                              fontWeight === '600' ? 'Semi-Bold' :
                              fontWeight === '700' ? 'Bold' :
                              fontWeight === '800' ? 'Extra Bold' :
                              fontWeight === '900' ? 'Black' : 'Bold';
            document.getElementById('font-weight-value').textContent = fontWeight + ' (' + weightLabel + ')';

            // Build text-shadow with separate opacities for glow and border
            const textShadow = `0 0 3px black, ` +
                `-2px -2px 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `2px -2px 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `-2px 2px 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `2px 2px 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `-2px 0 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `2px 0 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `0 -2px 0 rgba(255, 193, 7, ${{borderOpacityDecimal}}), ` +
                `0 2px 0 rgba(255, 193, 7, ${{borderOpacityDecimal}})`;

            // Apply to all overlay characters
            document.querySelectorAll('.cell-char').forEach(el => {{
                el.style.opacity = charOpacityDecimal;
                el.style.textShadow = textShadow;
                el.style.left = posX + 'px';
                el.style.top = posY + 'px';
                el.style.fontWeight = fontWeight;
                el.style.fontSize = fontSize + 'px';
            }});

            // Also apply to final comparison characters
            document.querySelectorAll('.cell-char-final').forEach(el => {{
                el.style.opacity = charOpacityDecimal;
                el.style.textShadow = textShadow;
                el.style.left = posX + 'px';
                el.style.top = posY + 'px';
                el.style.fontWeight = fontWeight;
                el.style.fontSize = fontSize + 'px';
            }});

            // Save preferences (PER TEXTURE)
            localStorage.setItem('ff7_char_opacity_' + TEXTURE, charOpacity);
            localStorage.setItem('ff7_border_opacity_' + TEXTURE, borderOpacity);
            localStorage.setItem('ff7_pos_x_' + TEXTURE, posX);
            localStorage.setItem('ff7_pos_y_' + TEXTURE, posY);
            localStorage.setItem('ff7_font_weight_' + TEXTURE, fontWeight);
            localStorage.setItem('ff7_font_size_' + TEXTURE, fontSize);
        }}

        function updateOverlayColors() {{
            const colorClaude = document.getElementById('color-claude').value;
            const colorTesseract = document.getElementById('color-tesseract').value;
            const colorMangaocr = document.getElementById('color-mangaocr').value;

            // Convert hex to RGB
            const hexToRgb = (hex) => {{
                const r = parseInt(hex.slice(1, 3), 16);
                const g = parseInt(hex.slice(3, 5), 16);
                const b = parseInt(hex.slice(5, 7), 16);
                return `${{r}}, ${{g}}, ${{b}}`;
            }};

            const rgbClaude = hexToRgb(colorClaude);
            const rgbTesseract = hexToRgb(colorTesseract);
            const rgbMangaocr = hexToRgb(colorMangaocr);

            // Apply colors to overlay elements
            document.querySelectorAll('.char-claude').forEach(el => {{
                el.style.color = `rgba(${{rgbClaude}}, 0.9)`;
            }});
            document.querySelectorAll('.char-tesseract').forEach(el => {{
                el.style.color = `rgba(${{rgbTesseract}}, 0.9)`;
            }});
            document.querySelectorAll('.char-mangaocr').forEach(el => {{
                el.style.color = `rgba(${{rgbMangaocr}}, 0.9)`;
            }});

            // Save colors (PER TEXTURE)
            localStorage.setItem('ff7_color_claude_' + TEXTURE, colorClaude);
            localStorage.setItem('ff7_color_tesseract_' + TEXTURE, colorTesseract);
            localStorage.setItem('ff7_color_mangaocr_' + TEXTURE, colorMangaocr);
        }}

        function updateFinalComparisonColor() {{
            const colorFinal = document.getElementById('color-final').value;

            // Convert hex to RGB
            const r = parseInt(colorFinal.slice(1, 3), 16);
            const g = parseInt(colorFinal.slice(3, 5), 16);
            const b = parseInt(colorFinal.slice(5, 7), 16);

            // Apply to final comparison characters
            document.querySelectorAll('.cell-char-final').forEach(el => {{
                el.style.color = `rgba(${{r}}, ${{g}}, ${{b}}, 0.95)`;
            }});

            // Save color (PER TEXTURE)
            localStorage.setItem('ff7_color_final_' + TEXTURE, colorFinal);
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
                let finalChar = charData[baselineModel];  // Use selected baseline
                if (corrections[charData.index]) {{
                    const corr = corrections[charData.index];
                    if (corr === 'tesseract') finalChar = charData.tesseract;
                    else if (corr === 'mangaocr') finalChar = charData.mangaocr;
                    else if (corr === 'claude') finalChar = charData.claude;
                    else if (corr === 'investigate') finalChar = '???';
                    else if (corr === 'empty') finalChar = '';
                    else if (typeof corr === 'object' && corr.type === 'manual') finalChar = corr.char;
                }}
                finalMap.push({{
                    texture: TEXTURE,
                    index: charData.index,
                    grid_x: charData.grid_x,
                    grid_y: charData.grid_y,
                    character: finalChar,
                    baseline: baselineModel
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
                document.querySelectorAll('.cell').forEach(c => c.classList.remove('use-claude', 'use-tesseract', 'use-mangaocr', 'use-manual', 'investigate'));
                saveCorrections();
                updateStats();
                updateOverlay();  // Refresh overlay to show normal toggles
            }}
        }}

        function exportAllTextures() {{
            // Export COMPLETE character mapping for all 6 textures (1536 entries)
            const completeMapping = [];

            for (let textureNum = 1; textureNum <= 6; textureNum++) {{
                const textureName = 'jafont_' + textureNum;

                // Load stored data for this texture
                const savedChars = localStorage.getItem('ff7_chars_' + textureName);
                const savedCorrections = localStorage.getItem('ff7_corrections_' + textureName);
                const savedBaseline = localStorage.getItem('ff7_baseline_' + textureName);

                if (!savedChars) {{
                    console.warn('No character data for ' + textureName + ' - visit that page first');
                    continue;
                }}

                const textureChars = JSON.parse(savedChars);
                const textureCorrections = savedCorrections ? JSON.parse(savedCorrections) : {{}};
                const textureBaseline = savedBaseline || 'claude';

                // Process all 256 cells
                for (let index = 0; index < 256; index++) {{
                    const charData = textureChars[index];
                    const correction = textureCorrections[index];

                    let finalChar = '';
                    let source = textureBaseline;  // Default to baseline

                    // Determine final character and source
                    if (correction) {{
                        if (correction === 'claude') {{
                            source = 'claude';
                            finalChar = charData.claude;
                        }} else if (correction === 'tesseract') {{
                            source = 'tesseract';
                            finalChar = charData.tesseract;
                        }} else if (correction === 'mangaocr') {{
                            source = 'mangaocr';
                            finalChar = charData.mangaocr;
                        }} else if (correction === 'investigate') {{
                            source = 'investigate';
                            finalChar = '???';
                        }} else if (correction === 'empty') {{
                            source = 'empty';
                            finalChar = '';
                        }} else if (typeof correction === 'object' && correction.type === 'manual') {{
                            source = 'manual';
                            finalChar = correction.char;
                        }}
                    }} else {{
                        // No correction - use baseline
                        finalChar = charData[textureBaseline];
                    }}

                    // Calculate Unicode codepoint
                    let unicode = '';
                    if (finalChar && finalChar !== '???' && finalChar.length > 0) {{
                        const codePoint = finalChar.codePointAt(0);
                        unicode = 'U+' + codePoint.toString(16).toUpperCase().padStart(4, '0');
                    }}

                    completeMapping.push({{
                        texture: textureName,
                        index: index,
                        grid_x: charData.grid_x,
                        grid_y: charData.grid_y,
                        character: finalChar,
                        unicode: unicode,
                        source: source,
                        baseline: textureBaseline,
                        has_correction: !!correction,
                        // Include all OCR options for reference
                        ocr_options: {{
                            claude: charData.claude,
                            tesseract: charData.tesseract,
                            mangaocr: charData.mangaocr
                        }}
                    }});
                }}
            }}

            if (completeMapping.length === 0) {{
                alert('No character data found. Please visit all 6 texture pages first to load their data.');
                return;
            }}

            const blob = new Blob([JSON.stringify(completeMapping, null, 2)], {{type: 'application/json'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'ff7_complete_character_mapping.json';
            a.click();

            alert('Exported ' + completeMapping.length + ' character mappings\\n' +
                  'Total: 1536 cells (6 textures × 256 cells)\\n' +
                  'Format: Complete mapping with Unicode codepoints');
        }}

        function exportCompactMapping() {{
            // Export COMPACT CSV format for LLM consumption
            // Format: texture,index,character,unicode
            let csv = 'texture,index,character,unicode\\n';

            for (let textureNum = 1; textureNum <= 6; textureNum++) {{
                const textureName = 'jafont_' + textureNum;

                // Load stored data for this texture
                const savedChars = localStorage.getItem('ff7_chars_' + textureName);
                const savedCorrections = localStorage.getItem('ff7_corrections_' + textureName);
                const savedBaseline = localStorage.getItem('ff7_baseline_' + textureName);

                if (!savedChars) {{
                    console.warn('No character data for ' + textureName + ' - visit that page first');
                    continue;
                }}

                const textureChars = JSON.parse(savedChars);
                const textureCorrections = savedCorrections ? JSON.parse(savedCorrections) : {{}};
                const textureBaseline = savedBaseline || 'claude';

                // Process all 256 cells
                for (let index = 0; index < 256; index++) {{
                    const charData = textureChars[index];
                    const correction = textureCorrections[index];

                    let finalChar = '';

                    // Determine final character
                    if (correction) {{
                        if (correction === 'claude') {{
                            finalChar = charData.claude;
                        }} else if (correction === 'tesseract') {{
                            finalChar = charData.tesseract;
                        }} else if (correction === 'mangaocr') {{
                            finalChar = charData.mangaocr;
                        }} else if (correction === 'investigate') {{
                            finalChar = '???';
                        }} else if (correction === 'empty') {{
                            finalChar = '';
                        }} else if (typeof correction === 'object' && correction.type === 'manual') {{
                            finalChar = correction.char;
                        }}
                    }} else {{
                        // No correction - use baseline
                        finalChar = charData[textureBaseline];
                    }}

                    // Calculate Unicode codepoint or use special marker
                    let unicode = '';
                    if (correction === 'investigate' || finalChar === '???') {{
                        unicode = '[NEEDS_REVIEW]';
                    }} else if (finalChar && finalChar.length > 0) {{
                        const codePoint = finalChar.codePointAt(0);
                        unicode = 'U+' + codePoint.toString(16).toUpperCase().padStart(4, '0');
                    }}

                    // Escape CSV field if it contains comma, quote, or newline
                    const escapeCsvField = (field) => {{
                        if (!field) return '';
                        if (field.includes(',') || field.includes('"') || field.includes('\\n')) {{
                            return '"' + field.replace(/"/g, '""') + '"';
                        }}
                        return field;
                    }};

                    // Build CSV row: texture,index,character,unicode
                    csv += textureName + ',' + index + ',' + escapeCsvField(finalChar) + ',' + unicode + '\\n';
                }}
            }}

            if (csv === 'texture,index,character,unicode\\n') {{
                alert('No character data found. Please visit all 6 texture pages first to load their data.');
                return;
            }}

            const blob = new Blob([csv], {{type: 'text/csv;charset=utf-8;'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'ff7_complete_mapping_compact.csv';
            a.click();

            const rowCount = csv.split('\\n').length - 2;  // -1 for header, -1 for trailing newline
            alert('Exported ' + rowCount + ' character mappings\\n' +
                  'Total: 1536 cells (6 textures × 256 cells)\\n' +
                  'Format: Compact CSV (texture,index,character,unicode)');
        }}

        // Initialize
        initGrid();
        loadBaseline();  // Load baseline model for this texture
        loadCorrections();
        updateStats();
        setCurrentCell(0);  // Highlight first cell
    </script>
</body>
</html>'''
    return html


def main():
    print("Creating viewer v3 (Enhanced with keyboard navigation)...")
    OUTPUT_DIR.mkdir(exist_ok=True)

    claude_map = load_csv_mapping(CLAUDE_CSV)
    tesseract_map = load_csv_mapping(TESSERACT_CSV)
    mangaocr_map = load_csv_mapping(MANGAOCR_CSV)

    print(f"Loaded: Claude={len(claude_map)}, Tesseract={len(tesseract_map)}, Manga-OCR={len(mangaocr_map)}")

    for texture_name in ['jafont_1', 'jafont_2', 'jafont_3', 'jafont_4', 'jafont_5', 'jafont_6']:
        print(f"Processing {texture_name}...")
        base64_img = image_to_base64(FONT_DIR / f"{texture_name}.png")
        html = generate_html(texture_name, base64_img, claude_map, tesseract_map, mangaocr_map)
        with open(OUTPUT_DIR / f"{texture_name}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Saved: {texture_name}.html ({len(html)//1024}KB)")

    print("\n" + "="*70)
    print("DONE! Enhanced viewer v3 created.")
    print("="*70)
    print(f"\nOpen: {OUTPUT_DIR / 'jafont_1.html'}")
    print("\nNew Features:")
    print("  • Baseline selection: Claude/Tesseract/Manga-OCR")
    print("  • Keyboard navigation: Arrow keys")
    print("  • Keyboard shortcuts: F (Claude), J (Manga-OCR), H (Tesseract)")
    print("  • Continuous mode: Auto-advance after selection")
    print("  • Transparency slider: Adjust overlay opacity")
    print("  • Visual current cell indicator: Dotted yellow border")
    print("  • Jump to next uncorrected button")


if __name__ == "__main__":
    main()

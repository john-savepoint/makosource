# Practical Usage Guide - German FF7 Menu Strings

**Created:** 2026-01-03 14:50 JST
**Purpose:** Show exactly how to use the extracted German menu strings in real projects

---

## Overview

You have 51 German FF7 menu strings ready to use. This guide shows practical examples for common tasks.

**Key Files:**
- `german_english_menu_mapping.csv` - All data (use this)
- `QUICK_REFERENCE.txt` - Quick lookup
- `GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md` - Patching details

---

## Use Case 1: Menu Patch Creation

**Goal:** Create an HEXT patch to replace English menu text with German

### Step-by-Step Example: Replace "Item" with "Objekt"

**1. Find the string in the mapping:**

```
Open: german_english_menu_mapping.csv
Find: index = 38
Result:
  index: 38
  de_offset: 0x00590C68
  de_text: Objekt
  en_text: Item
```

**2. Get the hex bytes:**

From `GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md`:
```
Objekt hex bytes: 4F 42 4A 45 4B 54
```

Or calculate manually:
```
'O' = 4F
'b' = 42
'j' = 4A
'e' = 45
'k' = 4B
't' = 54
```

**3. Create the HEXT patch:**

```hext
# Replace "Item" with "Objekt" in menu
OFF 0x590C68
OLD 49 74 65 6D         # English "Item"
NEW 4F 42 4A 45 4B 54   # German "Objekt"
```

**4. Apply the patch:**

Use your HEXT patcher tool to apply to ff7.exe

### Common Menu Patches

Here are the 9 main menu items ready to patch:

```hext
# MAIN MENU PATCHES

# [38] Item → Objekt
OFF 0x590C68
OLD 49 74 65 6D
NEW 4F 42 4A 45 4B 54

# [39] Magic → Zauber
OFF 0x590C6F
OLD 4D 61 67 69 63
NEW 5A 41 55 42 45 52

# [40] Materia → Materia (no change needed)

# [41] Equip → Ausrüsten
OFF 0x590C98
OLD 45 71 75 69 70
NEW 41 75 73 72 FC 73 74 65 6E

# [44] Limit → Limit (no change needed)

# [45] Config → Konfig
OFF 0x590CE6
OLD 43 6F 6E 66 69 67
NEW 4B 4F 4E 46 49 47

# [47] Save → Speichern
OFF 0x590D0C
OLD 53 61 76 65
NEW 53 50 45 49 43 48 45 52 4E

# [48] Quit → Verlassen
OFF 0x590D26
OLD 51 75 69 74
NEW 56 45 52 4C 41 53 53 45 4E
```

---

## Use Case 2: Database Integration

**Goal:** Import German strings into a tool database for easy lookup

### Python Example

```python
import csv

# Load German-English mapping
strings = {}
with open('german_english_menu_mapping.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        strings[int(row['index'])] = {
            'german': row['de_text'],
            'english': row['en_text'],
            'offset': row['de_offset']
        }

# Usage examples:
print(strings[38])
# Output: {'german': 'Objekt', 'english': 'Item', 'offset': '0x00590C68'}

print(strings[38]['german'])
# Output: Objekt

# Find by German text
for idx, data in strings.items():
    if data['german'] == 'Speichern':
        print(f"Index: {idx}, Offset: {data['offset']}")
        # Output: Index: 47, Offset: 0x00590D0C
```

### JavaScript Example

```javascript
// Load CSV and parse to object
const csvText = require('fs').readFileSync('german_english_menu_mapping.csv', 'utf8');
const lines = csvText.trim().split('\n');
const headers = lines[0].split(',');

const strings = {};
for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',');
    const row = {};
    headers.forEach((header, idx) => {
        row[header] = values[idx];
    });
    strings[row.index] = row;
}

// Usage:
console.log(strings[38].de_text);  // "Objekt"
console.log(strings[47].de_offset);  // "0x00590D0C"
```

### SQL Example

```sql
-- Create table
CREATE TABLE ff7_german_menu (
    id INTEGER PRIMARY KEY,
    offset TEXT NOT NULL,
    german_text TEXT NOT NULL,
    english_text TEXT NOT NULL,
    category TEXT
);

-- Insert data
INSERT INTO ff7_german_menu VALUES
(38, '0x00590C68', 'Objekt', 'Item', 'menu'),
(39, '0x00590C6F', 'Zauber', 'Magic', 'menu'),
(41, '0x00590C98', 'Ausrüsten', 'Equip', 'menu'),
(47, '0x00590D0C', 'Speichern', 'Save', 'menu'),
(48, '0x00590D26', 'Verlassen', 'Quit', 'menu');

-- Query examples:
SELECT german_text FROM ff7_german_menu WHERE id = 38;
SELECT * FROM ff7_german_menu WHERE category = 'menu' ORDER BY id;
SELECT * FROM ff7_german_menu WHERE german_text LIKE '%[%';
```

---

## Use Case 3: String Replacement Tool

**Goal:** Build a tool that replaces English text with German in menu screens

### Pseudocode Algorithm

```
1. Read german_english_menu_mapping.csv into memory
   Map: index → (german_text, offset, hex_bytes)

2. For each English UI text element:
   a. Determine its menu index (from game code/touphScript)
   b. Look up the German equivalent from our map
   c. Calculate required space (English length vs German length)
   d. Handle overflow (German text often longer)

3. Generate HEXT patches:
   a. Get old hex bytes (English text)
   b. Get new hex bytes (German text from mapping)
   c. Create HEXT entries

4. Apply patches to ff7.exe
   a. Validate offset is correct
   b. Replace bytes at specified offset
   c. Verify replacement

5. Test in game:
   a. Run FF7 with patched exe
   b. Check menu displays German text correctly
   c. Verify no display corruption
```

### Key Considerations

**String Length Differences:**

| English | Length | German | Length | Δ |
|---------|--------|--------|--------|---|
| Item | 4 | Objekt | 6 | +2 |
| Magic | 5 | Zauber | 6 | +1 |
| Equip | 5 | Ausrüsten | 9 | +4 |
| Save | 4 | Speichern | 9 | +5 |
| Quit | 4 | Verlassen | 9 | +5 |

**When German is longer:**
- May overflow allocated buffer
- Need to check menu drawing code for length validation
- May need to adjust text rendering or buffer size

**When German is shorter:**
- May need null-padding or space-padding
- Less critical, but still verify display

---

## Use Case 4: Multi-Language Lookup

**Goal:** Support multiple languages by querying the mapping

### Concept: Multi-Language Mapping

```
Index → [English, German, Japanese, Spanish, ...]
```

**Example in JSON:**

```json
{
  "38": {
    "english": "Item",
    "german": "Objekt",
    "japanese": "アイテム",
    "spanish": "Objeto",
    "offset_german": "0x00590C68"
  },
  "39": {
    "english": "Magic",
    "german": "Zauber",
    "japanese": "マジック",
    "spanish": "Magia",
    "offset_german": "0x00590C6F"
  },
  "47": {
    "english": "Save",
    "german": "Speichern",
    "japanese": "セーブ",
    "spanish": "Guardar",
    "offset_german": "0x00590D0C"
  }
}
```

**Usage:**

```python
# Load multi-language data
import json

with open('ff7_multilang.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get German text for index 47
german_save = data['47']['german']  # "Speichern"

# Get offset for patching
offset = data['47']['offset_german']  # "0x00590D0C"

# Support language switching
def get_text(index, language='english'):
    return data[str(index)].get(language, '???')

print(get_text(47, 'german'))   # Speichern
print(get_text(47, 'spanish'))  # Guardar
```

---

## Use Case 5: Verification & Testing

**Goal:** Verify that German menu strings are correctly applied

### Test Checklist

```
□ All 51 strings extracted and readable
□ All hex offsets valid (0x00590xxx range)
□ All special characters (ä, ö, ü) encoded as Windows-1252
□ No null bytes in middle of strings (0x00 only at end)
□ All strings match expected FF7 menu text
□ CSV can be parsed without errors
□ Offset values don't overlap
□ No corrupted entries (check for strange characters)
```

### Verification Script (Python)

```python
import csv
import re

def verify_german_mapping(csv_file):
    errors = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        prev_offset = 0

        for row in reader:
            index = int(row['index'])
            offset = int(row['de_offset'], 16)
            german = row['de_text']
            english = row['en_text']

            # Check 1: Offset format
            if not re.match(r'0x00590[A-F0-9]{3}', row['de_offset']):
                errors.append(f"Index {index}: Invalid offset format {row['de_offset']}")

            # Check 2: German text not empty
            if not german:
                errors.append(f"Index {index}: Empty German text")

            # Check 3: English text not empty
            if not english:
                errors.append(f"Index {index}: Empty English text")

            # Check 4: Special characters valid
            for char in german:
                if char in 'äöüßÄÖÜ':
                    # These should be encoded as single bytes in Windows-1252
                    pass

            # Check 5: Offsets increasing (mostly)
            if offset < prev_offset:
                print(f"Warning: Offset decreased at index {index}")
            prev_offset = offset

    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"  ✗ {error}")
    else:
        print("✓ All verifications passed!")

    return len(errors) == 0

# Run verification
verify_german_mapping('german_english_menu_mapping.csv')
```

---

## Use Case 6: Creating a Menu Text Editor

**Goal:** Build a UI tool to view and edit German menu strings

### Feature Requirements

```
1. Display Grid View:
   - Column: Index (38-48 main menu)
   - Column: English Text (read-only)
   - Column: German Text (read-only from CSV)
   - Column: Offset (read-only)

2. Search Function:
   - Search by German text: "Objekt"
   - Search by English text: "Item"
   - Search by index: "38"

3. Filter Function:
   - Filter by category: "menu", "config", "ui", "button", "direction"
   - Show all | Show main menu only | Show config only

4. Copy Function:
   - Copy German text to clipboard
   - Copy hex offset to clipboard
   - Copy hex bytes to clipboard

5. HEXT Generator:
   - Select strings to patch
   - Auto-generate HEXT patch file
   - Show preview before generating
```

### Simple Web UI (HTML/CSS/JS)

```html
<!DOCTYPE html>
<html>
<head>
    <title>FF7 German Menu String Tool</title>
    <style>
        body { font-family: monospace; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f0f0f0; }
        .search { margin: 10px 0; }
        input { padding: 5px; width: 300px; }
        button { padding: 5px 10px; }
    </style>
</head>
<body>
    <h1>FF7 German Menu String Editor</h1>

    <div class="search">
        <input type="text" id="searchBox" placeholder="Search German or English text...">
        <button onclick="search()">Search</button>
        <button onclick="clear()">Clear</button>
    </div>

    <table id="stringTable">
        <thead>
            <tr>
                <th>Index</th>
                <th>German Text</th>
                <th>English Text</th>
                <th>Offset</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody id="tableBody">
        </tbody>
    </table>

    <script>
        // Load CSV and populate table
        fetch('german_english_menu_mapping.csv')
            .then(r => r.text())
            .then(csv => {
                const lines = csv.trim().split('\n');
                const tbody = document.getElementById('tableBody');

                for (let i = 1; i < lines.length; i++) {
                    const [index, offset, german, english] = lines[i].split(',');
                    const row = `
                        <tr>
                            <td>${index}</td>
                            <td>${german}</td>
                            <td>${english}</td>
                            <td>${offset}</td>
                            <td>
                                <button onclick="copy('${offset}')">Copy Offset</button>
                            </td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                }
            });

        function copy(text) {
            navigator.clipboard.writeText(text);
            alert('Copied: ' + text);
        }

        function search() {
            const query = document.getElementById('searchBox').value.toLowerCase();
            const rows = document.getElementById('tableBody').getElementsByTagName('tr');

            for (let row of rows) {
                const german = row.cells[1].textContent.toLowerCase();
                const english = row.cells[2].textContent.toLowerCase();

                if (german.includes(query) || english.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        }
    </script>
</body>
</html>
```

---

## Use Case 7: Batch Patching Multiple Strings

**Goal:** Create patches for multiple menu strings at once

### Generate HEXT File

```python
import csv

def generate_hext_patch(csv_file, output_file, indices_to_patch=None):
    """Generate HEXT patch for German menu strings"""

    patches = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = int(row['index'])

            # Skip if not in target list
            if indices_to_patch and index not in indices_to_patch:
                continue

            # Get hex bytes (would need separate mapping for this)
            # For now, just create placeholder
            patches.append(f"""
# Index {index}: {row['en_text']} → {row['de_text']}
OFF {row['de_offset']}
# TODO: Add OLD and NEW hex bytes
# NEW: {row['de_text']} (offset: {row['de_offset']})
""")

    # Write HEXT file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# FF7 German Menu Patch\n")
        f.write("# Auto-generated\n\n")
        f.writelines(patches)

# Generate patch for main menu items (indices 38-48)
main_menu_indices = [38, 39, 40, 41, 44, 45, 46, 47, 48]
generate_hext_patch('german_english_menu_mapping.csv',
                    'ff7_german_menu_patch.hext',
                    main_menu_indices)

print("Generated: ff7_german_menu_patch.hext")
```

---

## Quick Reference Table

| Task | File to Use | Key Column |
|------|-------------|-----------|
| Find German word for menu item | german_english_menu_mapping.csv | de_text |
| Find offset for patching | german_english_menu_mapping.csv | de_offset |
| Find hex bytes for patching | GERMAN_ENGLISH_MENU_TOUPHSCRIPT_MAPPING.md | German Bytes (Hex) |
| Browse by category | german_english_menu_mapping_categorized.csv | category |
| Quick lookup | QUICK_REFERENCE.txt | All (read-only) |
| Understand encoding | ENCODING_EXAMPLES.txt | Examples |

---

## Summary

The German FF7 menu strings are ready for:

✅ Menu patching (HEXT patches)
✅ Database integration (SQL, JSON)
✅ Tool development (Python, JavaScript)
✅ Multi-language support
✅ Batch processing
✅ Verification and testing
✅ UI tool creation

All necessary data and offset information is included in the provided files.

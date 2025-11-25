# 11. TESTING & VERIFICATION PROTOCOL

## 11.1 Unit Test 1: The "Red W" Test (Texture Override Sanity Check)

**Objective:** Verify FFNx's texture override system is working before implementing complex logic.

**Procedure:**

**Step 1: Create Test Texture**

1. Copy `mods/Textures/menu/usfont_h.png` to backup
2. Open in image editor (GIMP, Photoshop, etc.)
3. Find the 'W' character (cell index 0x57 = 87 decimal)
   - Grid position: Row 5, Column 7 (87 = 5*16 + 7)
4. Replace the 'W' with a **solid red square** or a recognizable Kanji (e.g., 私)
5. Save as PNG

**Step 2: Configure FFNx**

```toml
# FFNx.toml
font_language = "en"  # Keep English mode for now
```

**Step 3: Launch Game**

1. Start FF7
2. Enter name selection screen (type "WWW")
3. Or go to menu and look at text containing 'W'

**Expected Results:**

| Condition | Expected | Meaning |
|-----------|----------|---------|
| See red square/Kanji where 'W' should be | ✅ PASS | Texture override works |
| Character appears squashed horizontally | ⚠️ Expected | Geometry patch not applied yet |
| Still see normal 'W' | ❌ FAIL | Texture not loading |
| Game crashes | ❌ FAIL | File format issue |

**Troubleshooting:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| Normal 'W' appears | PNG not found | Check filename, path |
| Crash on load | Invalid PNG | Re-export with correct settings |
| Squashed character | Width table not patched | Expected at this stage |

---

## 11.2 Unit Test 2: Width Table Patch Verification

**Objective:** Verify the geometry patch prevents squashing.

**Procedure:**

**Step 1: Enable Japanese Mode**

```toml
# FFNx.toml
font_language = "ja"
```

**Step 2: Keep Red Test Texture**

- Use the same modified `usfont_h.png` from Test 1

**Step 3: Launch Game**

1. Start FF7
2. Enter name selection
3. Observe the red character

**Expected Results:**

| Observation | Result | Meaning |
|-------------|--------|---------|
| Red character appears **square** (not squashed) | ✅ PASS | Width patch successful |
| ALL English text appears widely spaced | ✅ Expected | All chars now 16px wide |
| Red character still squashed | ❌ FAIL | Patch didn't apply |
| Crash on startup | ❌ FAIL | Memory protection error |

**Diagnostic Checks:**

1. Check `FFNx.log`:
```
[INFO] Patching character width table for Japanese...
[INFO] Width table located at: 0x99DDA8
[INFO] Successfully patched character width table.
```

2. If log shows errors:
```
[ERROR] font_info pointer is NULL!
→ ff7_data() didn't run or version mismatch
```

**Manual Verification (Advanced):**

Use Cheat Engine to inspect memory at `common_externals.font_info`:

```
Address: 0x99DDA8 (US 1.02)
Expected data (hex):
10 10 10 10 10 10 10 10 ... (all 0x10)

Before patch (hex):
04 04 06 08 0A 08 0C 0E ... (variable widths)
```

---

## 11.3 Integration Test 1: Multi-Texture Loading

**Objective:** Verify all 6 font textures load correctly into memory.

**Procedure:**

**Step 1: Prepare Assets**

Place 6 distinct test textures in `mods/Textures/menu/`:

```
jafont_1.png  →  Fill with RED      (Page 0)
jafont_2.png  →  Fill with GREEN    (Page 1 - triggered by 0xFA)
jafont_3.png  →  Fill with BLUE     (Page 2 - triggered by 0xFB)
jafont_4.png  →  Fill with YELLOW   (Page 3 - triggered by 0xFC)
jafont_5.png  →  Fill with MAGENTA  (Page 4 - triggered by 0xFD)
jafont_6.png  →  Fill with CYAN     (Page 5 - triggered by 0xFE)
```

**Step 2: Configure**

```toml
font_language = "ja"
```

**Step 3: Launch and Check Logs**

```
FFNx.log:
[INFO] Japanese font loading initiated for: usfont
[INFO] Loaded Japanese font page 1: mods/Textures/menu/jafont_1.png (1024x1024)
[INFO] Loaded Japanese font page 2: mods/Textures/menu/jafont_2.png (1024x1024)
[INFO] Loaded Japanese font page 3: mods/Textures/menu/jafont_3.png (1024x1024)
[INFO] Loaded Japanese font page 4: mods/Textures/menu/jafont_4.png (1024x1024)
[INFO] Loaded Japanese font page 5: mods/Textures/menu/jafont_5.png (1024x1024)
[INFO] Loaded Japanese font page 6: mods/Textures/menu/jafont_6.png (1024x1024)
[INFO] Successfully loaded all 6 Japanese font pages.
```

**Expected Results:**

| Log Entry | Status | Action if Failed |
|-----------|--------|------------------|
| All 6 pages loaded | ✅ PASS | Proceed to next test |
| "FAILED to load page X" | ❌ FAIL | Check file exists, correct name |
| Crash after page 2 | ❌ FAIL | Allocation override didn't work |
| No log entries | ❌ FAIL | font_language != "ja" or code path not hit |

**Visual Verification:**

At this stage, all text will appear **RED** (Page 0) because the Assembly hook isn't implemented yet. This is expected.

---

## 11.4 Integration Test 2: Page Switching (Assembly Hook Verification)

**Objective:** Verify the Hext patch detects FA-FE codes and switches textures.

**⚠️ REQUIRES:** Hext patch from Section 8.3 applied with correct addresses.

**Procedure:**

**Step 1: Prepare Test Dialogue**

Use **Makou Reactor** or **Hojo** to edit dialogue:

1. Open `flevel.lgp` (field archive)
2. Extract a simple field (e.g., `md1_1` - first reactor)
3. Edit dialogue text to:
   ```
   Normal text FA 00 FB 00 FC 00 00
   ```
   - `FA 00` = First char from Page 1 (GREEN texture)
   - `FB 00` = First char from Page 2 (BLUE texture)
   - `FC 00` = First char from Page 3 (YELLOW texture)
   - `00` = String terminator

**Step 2: Replace Field File**

1. Repack `flevel.lgp` with modified field
2. Place in game directory
3. Or use 7th Heaven to load as mod

**Step 3: Launch and Trigger**

1. Start new game
2. Advance to the modified dialogue
3. Observe character colors

**Expected Results:**

| Visual | Meaning | Status |
|--------|---------|--------|
| See: RED GREEN BLUE YELLOW sequence | ✅ PERFECT | All systems working |
| All characters are RED | ❌ Hook not firing | Check Hext addresses |
| Crash when dialogue appears | ❌ Invalid memory write | Check g_currentFontPage address |
| Random colors | ⚠️ Partial success | Page index calculation error |

**Diagnostic Logging:**

Enable trace mode:

```cpp
// src/gl/gl.cpp
#define DEBUG_JAPANESE_FONTS  // Uncomment

// Check log:
[TRACE] Binding Japanese font page 0
[TRACE] Binding Japanese font page 1  ← Should appear when FA byte is hit
[TRACE] Binding Japanese font page 2  ← Should appear when FB byte is hit
```

**Advanced Debugging:**

Set breakpoint in `gl_bind_texture_set`:

```cpp
if (g_currentFontPage != 0) {
    // Breakpoint here - should hit when FA/FB/FC are encountered
    __debugbreak();
}
```

---

## 11.5 Full System Test: Real Japanese Dialogue

**Objective:** End-to-end verification with actual Japanese text and real font textures.

**Prerequisites:**
- ✅ All previous tests passed
- ✅ Real `jafont_*.png` files installed (not test colors)
- ✅ Japanese dialogue patch applied

**Procedure:**

**Step 1: Install Assets**

1. Replace test textures with actual Japanese font textures
2. Install a Japanese translation mod (or use ff7_ja.exe's text)

**Step 2: Configure for Production**

```toml
font_language = "ja"
font_enable_furigana = false  # Test basic first
```

**Step 3: Play Through a Scene**

1. Start new game
2. Play through first reactor mission
3. Read all dialogue
4. Check menu screens
5. Check battle text

**Verification Checklist:**

| Component | Check | Status |
|-----------|-------|--------|
| **Dialogue** | All Kanji render correctly | ☐ |
| | No squashed characters | ☐ |
| | No missing glyphs (blank squares) | ☐ |
| | Text fits in dialog boxes | ☐ |
| **Menu** | Item names readable | ☐ |
| | Character names correct | ☐ |
| | Status screen displays properly | ☐ |
| **Battle** | Enemy names show | ☐ |
| | Spell names correct | ☐ |
| | Damage numbers work | ☐ |
| **Performance** | No lag during text rendering | ☐ |
| | Smooth scrolling | ☐ |
| **Stability** | No crashes during 30min play | ☐ |
| | No memory leaks (check Task Manager) | ☐ |

**Known Issues to Check:**

| Issue | Cause | Fix |
|-------|-------|-----|
| Some Kanji missing (blank) | Character not in mapping CSV | Add to jafont_*.png |
| Text overflows boxes | Width table too wide | Reduce width or adjust box size |
| Flickering text | Z-fighting | Check depth buffer settings |
| Crash after 10min | Memory leak in loader | Review allocations |

---

## 11.6 Regression Testing

**Objective:** Ensure English mode still works (backward compatibility).

**Procedure:**

**Step 1: Switch to English**

```toml
font_language = "en"
```

**Step 2: Play Original Game**

1. Launch FF7
2. Start new game
3. Play for 15 minutes
4. Test all UI elements

**Expected Behavior:**

| Feature | Expected | Status |
|---------|----------|--------|
| All text is English | ✅ | ☐ |
| No Japanese characters appear | ✅ | ☐ |
| No performance degradation | ✅ | ☐ |
| No crashes | ✅ | ☐ |
| Mods still work (7th Heaven) | ✅ | ☐ |

**⚠️ CRITICAL:** If English mode breaks, the implementation has a logic error. Common causes:

- Width table patched even when `font_language == "en"`
- Texture loader always loads 6 pages
- Assembly hook fires on English text

**Fix:** Add guard clauses:

```cpp
if (font_language != "ja") {
    return;  // Don't patch, use original logic
}
```

---

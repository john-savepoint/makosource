# Live SDF Font Tuning with Cheat Engine

## Quick Setup

1. **Download Cheat Engine**: https://www.cheatengine.org/
2. **Start FF7** and get to a screen with Japanese text
3. **Open Cheat Engine** and attach to `ff7_en.exe`

## Finding the SDF Parameters

### Step 1: Find sdf_thickness (currently 0.7)

1. In Cheat Engine, click "New Scan"
2. Value Type: `Float`
3. Scan Type: `Exact Value`
4. Value: `0.7`
5. Click `First Scan`
6. You'll get many results

### Step 2: Narrow it down

1. Change `sdf_thickness` in FFNx.toml to a different value (e.g., 0.8)
2. Restart FF7
3. In Cheat Engine, enter `0.8` and click `Next Scan`
4. Repeat until you have 1-5 results

### Step 3: Test and modify

1. Double-click the address to add it to the bottom panel
2. Double-click the value in bottom panel to edit it
3. Try different values (0.4 = thin, 0.6 = normal, 0.8 = bold)
4. **The text updates instantly in-game!**

### Step 4: Find other parameters

Repeat for:
- `sdf_shadow_offset` (currently 2.0)
- `sdf_shadow_opacity` (currently 0.7)
- `sdf_pixel_range` (currently 4.0)

## Recommended Values to Test

**For crisp, readable text:**
```
sdf_thickness = 0.55-0.65
sdf_shadow_offset = 1.5
sdf_shadow_opacity = 0.6
sdf_pixel_range = 4.0
```

**For bold, prominent text:**
```
sdf_thickness = 0.7-0.8
sdf_shadow_offset = 2.0
sdf_shadow_opacity = 0.8
sdf_pixel_range = 4.0
```

**For thin, elegant text:**
```
sdf_thickness = 0.4-0.5
sdf_shadow_offset = 1.0
sdf_shadow_opacity = 0.4
sdf_pixel_range = 4.0
```

## Save Your Settings

Once you find values you like:
1. Note the exact values from Cheat Engine
2. Update FFNx.toml with those values
3. The settings will persist on next launch

## Alternative: AutoHotkey Script

If you want hotkeys to cycle through presets, we can create
an AutoHotkey script that modifies the memory addresses you
found with Cheat Engine.

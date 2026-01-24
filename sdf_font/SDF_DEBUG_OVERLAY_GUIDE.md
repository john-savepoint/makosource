# SDF Font Debug Overlay - User Guide

**Created:** 2026-01-25 00:42:00 JST (Saturday)
**Session ID:** 22abbba1-da82-4680-af9f-04982a5b7f30
**Version:** 1.0.0

## Overview

The SDF Font Debug Overlay provides real-time parameter tuning for Signed Distance Field (SDF) fonts in Final Fantasy VII. This allows you to see changes immediately in the actual game without restarting.

## Features

- **Real-time parameter adjustment** - See changes instantly in-game
- **No restart required** - Adjust while game is running
- **Visual tooltips** - Helpful descriptions for each parameter
- **Reset to defaults** - Quick reset button for testing
- **Current values display** - Easy copy to FFNx.toml for persistence

## How to Use

### Step 1: Start the Game
Launch Final Fantasy VII with FFNx installed.

### Step 2: Open DevTools Overlay
Press **F12** (or your configured DevTools hotkey) to open the overlay.

### Step 3: Open SDF Font Debug Window
1. Click on the **Tools** menu in the overlay
2. Select **SDF Font Debug**

### Step 4: Adjust Parameters
The following parameters are available:

#### Enable SDF Fonts
Checkbox to enable/disable SDF font rendering entirely.

#### Pixel Range (0.5 - 10.0)
- **Default:** 4.0
- **Effect:** Controls the distance field spread
- Higher values = smoother edges but more blur
- Lower values = sharper but may show artifacts
- **Recommended range:** 3.0 - 5.0

#### Thickness (0.1 - 2.0)
- **Default:** 0.5
- **Effect:** Controls glyph boldness
- 0.5 = normal weight
- Higher values = bolder characters
- **Recommended range:** 0.4 - 0.7

#### Shadow Offset (0.0 - 5.0 pixels)
- **Default:** 1.0
- **Effect:** Shadow displacement distance
- 0.0 = no shadow
- Higher values = shadow further from text
- **Recommended range:** 0.5 - 2.0

#### Shadow Opacity (0.0 - 1.0)
- **Default:** 0.5
- **Effect:** Shadow transparency
- 0.0 = invisible shadow
- 1.0 = fully opaque shadow
- **Recommended range:** 0.3 - 0.7

### Step 5: Test in Different Contexts
Move through different game screens to see how your parameters look:
- Battle menu
- Main menu
- Dialogue boxes
- Item descriptions

### Step 6: Save Your Settings
Once satisfied with your parameters:

1. Click **Show Current Values** button
2. Copy the displayed values
3. Close the game
4. Open `FFNx.toml` in a text editor
5. Paste the values into the appropriate section:

```toml
# SDF Font Settings
enable_sdf_fonts = true
sdf_pixel_range = 4.0
sdf_thickness = 0.5
sdf_shadow_offset = 1.0
sdf_shadow_opacity = 0.5
```

6. Save the file
7. Restart the game to make the settings permanent

## Tips

- **Start with defaults:** Use the "Reset to Defaults" button if you get lost
- **Small adjustments:** Make small changes (0.1 increments) for subtle improvements
- **Test everywhere:** Japanese characters may render differently in various contexts
- **Check readability:** Ensure text is readable at different screen distances
- **Balance quality vs performance:** Higher pixel_range values may impact performance slightly

## Keyboard Shortcuts

- **F12** - Toggle DevTools overlay
- **ESC** - Close debug window (when focused)

## Troubleshooting

### Debug window won't open
- Ensure you're using the latest FFNx.dll with SDF debug support
- Check that DevTools overlay is enabled in FFNx.toml

### Changes not visible
- Ensure "Enable SDF Fonts" checkbox is checked
- Verify SDF font textures are installed in the game directory
- Try adjusting parameters more dramatically to see effects

### Performance issues
- Lower the `sdf_pixel_range` value
- Ensure you're not running other overlay tools simultaneously

## Technical Details

The debug overlay modifies the following global variables in real-time:
- `enable_sdf_fonts` (bool)
- `sdf_pixel_range` (float)
- `sdf_thickness` (float)
- `sdf_shadow_offset` (float)
- `sdf_shadow_opacity` (float)

Changes take effect immediately on the next frame render.

## Implementation

### Files Added
- `/mnt/c/FFNx/src/sdf_debug.h` - Header declaration
- `/mnt/c/FFNx/src/sdf_debug.cpp` - ImGui window implementation

### Files Modified
- `/mnt/c/FFNx/src/overlay.h` - Added `sdf_debug_open` state variable
- `/mnt/c/FFNx/src/overlay.cpp` - Integrated SDF debug window into Tools menu

The implementation follows the existing FFNx debug window patterns (lighting_debug, field_debug, world_debug) for consistency and maintainability.

## Future Enhancements

Potential future additions:
- Save/load preset configurations
- Per-font parameter profiles
- Visual comparison split-screen
- Real-time preview of all Japanese characters
- Export parameters to clipboard

---

**Built with:** FFNx DevTools + ImGui
**Compatible with:** FFNx PR#737 (SDF Font Support)

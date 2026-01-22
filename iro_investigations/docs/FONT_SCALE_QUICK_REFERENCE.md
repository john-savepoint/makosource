# FF7 Font Scale - Quick Reference

**Created:** 2026-01-22 22:20:00 JST (Thursday)
**Session-ID:** fab70bfc-433a-4d8f-b83b-6690362519f5

## TL;DR

**Q: Why does changing the font scale byte break the font system?**

**A:** It's not a byte - it's a 32-bit **float**. And it's part of a 3-component system that must stay synchronized:

```
Font Texture Resolution × Spacing Table × Scale Factor = Final Character Width
```

Change one without the others → broken fonts.

## Critical Memory Addresses

| What | File Address | Runtime Address | Type | Default | Purpose |
|------|--------------|-----------------|------|---------|---------|
| **Font Scale** | 0x7B7CF8 | 0xBB7CF8 | float32 | 1.667 | Multiplies character widths |
| **Spacing Table** | 0x99DDA8 | 0xD9DDA8 | byte[256] | varies | Per-character advance widths |
| **Font Data Ptr** | 0xDB958C | 0x1DB958C | pointer | (runtime) | Points to loaded font metrics |

## How to Read the Scale Value

```python
import struct

# From file/memory (little-endian)
bytes_le = bytes.fromhex("5555D53F")  # Original value
scale = struct.unpack('<f', bytes_le)[0]
# Result: 1.6666666269302368

# Enhanced Stock UI patches to:
bytes_le = bytes.fromhex("00000040")  # HEXT patch
scale = struct.unpack('<f', bytes_le)[0]
# Result: 2.0
```

## Font Files Used

### Menu Fonts (usfont)
- `usfont_a_h.tim` / `usfont_a_l.tim` - Enhanced UI variants
- `usfont_b_h.tim` / `usfont_b_l.tim` - Enhanced UI variants
- `usfont_h.tim` / `usfont_l.tim` - Standard variants

Controlled by Registry: `HKCU\Software\Square Soft, Inc.\Final Fantasy VII` → Mode=2

### Other Fonts
- `cfont.tim` - Character/dialogue font
- `font.tim`, `font_ua.tim`, `font_ub.tim`, `font_s.tim` - World map fonts

## Code That Uses Font Scale

**Text Width Calculation** (`sub_6F54A2` at 0x6F54A2):
```c
width += (char_data >> 5) * flt_7B7CF8;  // Left padding
width += (char_data & 0x1F) * flt_7B7CF8; // Advance width
```

**Character Rendering** (`sub_6F564E` at 0x6F564E):
```c
int x_advance = (char_data >> 5) * flt_7B7CF8 + (char_data & 0x1F) * flt_7B7CF8;
render_char_quad(x, y, texture_coords);
return x + x_advance;
```

## Why Arbitrary Changes Break

### You Change Scale to 3.0

**What happens:**
1. Game calculates: `char_width = spacing_value * 3.0`
2. But font texture still has characters at 1.667× spacing
3. Rendered position doesn't match texture position
4. Characters overlap or have gaps

**Additional failures:**
- Text overflows UI boxes (calculated too wide)
- Word wrapping breaks (wrong width calculation)
- Centering fails (wrong text width)

## Safe Ways to Modify Font Scale

### Option 1: Use Existing Mod
Enhanced Stock UI already coordinates all three components. Use their scale value (2.0).

### Option 2: Create Custom Scale
1. Choose scale factor (e.g., 2.5)
2. Create/modify font textures to match
3. Update spacing table values (multiply by scale_new/scale_old)
4. Update 0x7B7CF8 to new scale
5. Test EVERY menu screen for overflow

### Option 3: Modify Individual Characters
1. Keep scale at 1.667 (or 2.0 if using Enhanced Stock)
2. Modify spacing table (0x99DDA8) for specific characters
3. Update corresponding font texture if needed

## Testing Checklist

If you modify font scale:
- [ ] Main menu - all options visible
- [ ] Battle menu - commands don't overflow
- [ ] Item menu - item names fit in boxes
- [ ] Equipment menu - equipment names fit
- [ ] Materia menu - materia names fit
- [ ] Config menu - all text visible
- [ ] Save/Load menu - all text visible
- [ ] Shop menus - prices and names fit
- [ ] Dialogue boxes - text doesn't overflow
- [ ] Battle text - damage numbers positioned correctly

## PowerShell Memory Check

```powershell
# Read current font scale from running game
$processId = (Get-Process | Where-Object { $_.ProcessName -like '*ff7*' }).Id
$handle = [MemoryReader]::OpenProcess(0x0010, $false, $processId)
$buffer = New-Object byte[] 4
[MemoryReader]::ReadProcessMemory($handle, [IntPtr]0xBB7CF8, $buffer, 4, [ref]$bytesRead)
$scale = [BitConverter]::ToSingle($buffer, 0)
Write-Host "Current font scale: $scale"
```

## See Also

- Full investigation: `FF7_FONT_SCALING_COMPLETE_INVESTIGATION.md`
- Previous session: `.project/session_handoffs/SESSION_HANDOFF_2026-01-22-01_FF7_UI_MEMORY_REVERSE_ENGINEERING.md`
- HEXT database: `ff7_ui_analysis/ff7_ui_memory_map.json`

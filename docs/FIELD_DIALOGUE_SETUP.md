# FF7 Field Dialogue Japanese Setup

**Created:** 2025-12-05 00:51 JST (Friday)
**Last Modified:** 2025-12-05 00:51 JST (Friday)
**Version:** 1.0.0
**Session-ID:** c245e7c0-ec73-4933-b925-5976860e742c

---

## Overview

This document explains how Japanese field dialogue was enabled for FF7 using FFNx.

---

## The Problem

FF7's field dialogue (NPC conversations, story text, field messages) is stored in `flevel.lgp`. The Japanese version uses a separate file called `jfleve.lgp`.

When `ff7_japanese_edition = true` is set in FFNx.toml:
- Menu LGP is automatically redirected: `menu_us.lgp` → `menu_ja.lgp` ✅
- Kernel2.bin is automatically redirected to Japanese version ✅
- **Field LGP is NOT redirected** - FFNx still loads `flevel.lgp` ❌

This is because FFNx PR737's `file.cpp` only has redirect logic for menu files, not field files:

```cpp
// From FFNx-PR737/src/ff7/file.cpp lines 39-49
if(ff7_japanese_edition)
{
    // Check if this is menu_us.lgp and redirect to menu_ja.lgp
    char* menu_us_pos = strstr(modified_filename, "menu_us.lgp");
    if(menu_us_pos != NULL)
    {
        memcpy(menu_us_pos, "menu_ja", 7);
    }
}
// No similar logic for flevel.lgp → jfleve.lgp
```

---

## The Solution

Since FFNx always loads `flevel.lgp` for field data regardless of Japanese mode, we replace it with the Japanese version.

### Files Changed

**Directory:** `C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\field\`

| File | Description | MD5 Hash |
|------|-------------|----------|
| `flevel.lgp` | Japanese field dialogue (renamed from jfleve.lgp) | `5d97b5b9f17d247cc9506efb5a377309` |
| `flevel_en.lgp` | English field dialogue (backup) | `8d0a7224ec3498ad518b1ceb99e2df77` |
| `jfleve.lgp` | Original Japanese file (kept for reference) | `5d97b5b9f17d247cc9506efb5a377309` |

### Commands Used

```bash
# Backup English version
mv "data/field/flevel.lgp" "data/field/flevel_en.lgp"

# Replace with Japanese version
cp "data/field/jfleve.lgp" "data/field/flevel.lgp"
```

---

## Verification

After making this change, check FFNx.log for:

```
opening lgp file C:\...\data\field/flevel.lgp
```

The game will now load Japanese field dialogue because FFNx opens `flevel.lgp` which is now the Japanese content.

---

## Alternative Approaches

### Option 1: Modify FFNx Source (Not Used)

Add redirect logic to `FFNx-PR737/src/ff7/file.cpp`:

```cpp
if(ff7_japanese_edition)
{
    // Redirect flevel.lgp to jfleve.lgp
    char* flevel_pos = strstr(modified_filename, "flevel.lgp");
    if(flevel_pos != NULL)
    {
        // jfleve.lgp is same length as flevel.lgp
        memcpy(flevel_pos, "jfleve", 6);
    }
}
```

This would require rebuilding FFNx.

### Option 2: Extract to direct/ (Not Used)

FFNx's direct mode (`direct_mode_path = "direct"`) takes priority over LGP files. Extracting jfleve.lgp to `direct/flevel/` would work:

```bash
ulgp extract jfleve.lgp direct/flevel/
```

However, this creates hundreds of individual files and is more complex to manage.

### Option 3: File Rename (Used)

Simply renaming the Japanese file to `flevel.lgp` is the simplest approach:
- No FFNx rebuild required
- No extraction tools needed
- Easy to reverse (just rename back)
- Original files preserved as backups

---

## Reverting to English

To restore English field dialogue:

```bash
cd "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\data\field"

# Remove Japanese version
rm flevel.lgp

# Restore English version
mv flevel_en.lgp flevel.lgp
```

Or simply:

```bash
cp flevel_en.lgp flevel.lgp
```

---

## Related Files

- `docs/FFNX_DIRECTORY_STRUCTURE.md` - Overall directory layout
- `docs/HEXT_PATCHING_GUIDE.md` - Menu text patching guide
- `docs/MENU_TEXT_ADDRESS_MAP.md` - Menu string addresses
- `.project/session_handoffs/SESSION_HANDOFF_2025-12-05_COMPREHENSIVE.md` - Full session context

---

## Notes

- The Japanese jfleve.lgp (129MB) is slightly larger than English flevel.lgp (128MB)
- Both files use the same internal structure - only the text content differs
- This approach works because FFNx doesn't validate the LGP filename against its contents

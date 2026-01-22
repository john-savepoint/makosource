# AF3DN.P Naming Screen Call Flow

**Generated**: 2025-12-16 15:20 JST
**Session**: 0681f78b-0382-45ee-898b-5a32b7ce32d5

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INITIALIZATION                                │
├─────────────────────────────────────────────────────────────────────┤
│  DllMain                                                             │
│    └──► sub_10014FF0 (initialize_japanese_locale)                   │
│           ├──► sub_10014DC0 (detect_game_version)                   │
│           ├──► setlocale("Japanese_Japan.932")                      │
│           ├──► sub_10014E10 (patch_binary_for_japanese)             │
│           │      └──► VirtualProtect + JMP patches                  │
│           └──► sub_10015710 (final_init)                            │
│                  └──► sub_10008550 (init_character_table)           │
│                         └──► Copy unk_1004A620 → unk_10051880       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      NAMING SCREEN LOOP                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │           sub_10019110 (naming_screen_input_thread)        │     │
│  │                    [Main Input Loop]                        │     │
│  └────────────────────┬───────────────────────────────────────┘     │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  WaitForSingleObject(semaphore) - Wait for input event     │     │
│  └────────────────────┬───────────────────────────────────────┘     │
│                       │                                              │
│                       ▼                                              │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │      sub_10001340 (find_character_by_cursor_position)      │     │
│  │  ┌─────────────────────────────────────────────────────┐   │     │
│  │  │ 1. Check dword_1004CB78 (JP/EN locale)              │   │     │
│  │  │ 2. Get state from offset +2572 (EN) / +2892 (JP)    │   │     │
│  │  │ 3. Search unk_10051880[] for matching entry         │   │     │
│  │  │ 4. Return pointer to 5-DWORD character struct       │   │     │
│  │  │ 5. Cache result in dword_1004CBBC                   │   │     │
│  │  └─────────────────────────────────────────────────────┘   │     │
│  └────────────────────┬───────────────────────────────────────┘     │
│                       │                                              │
│          ┌────────────┴────────────┐                                 │
│          ▼                         ▼                                 │
│  ┌───────────────┐       ┌────────────────────┐                     │
│  │ Value = 20    │       │ Value = 26         │                     │
│  │ (Confirm)     │       │ (Execute/Apply)    │                     │
│  └───────┬───────┘       └────────┬───────────┘                     │
│          │                        │                                  │
│          ▼                        ▼                                  │
│  sub_100191F0            sub_10019230                                │
│  (confirm_handler)       (execute_handler)                          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    CHARACTER RENDERING                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  sub_1000B740 (render_character_to_screen)                          │
│    │                                                                 │
│    ├──► sub_10003A60 (setup_vertex_buffer)                          │
│    │      └──► Build quad vertices with UV coords                   │
│    │                                                                 │
│    ├──► sub_100086B0 (render_font_texture_page)                     │
│    │      ├──► Check texture cache (64 entries)                     │
│    │      ├──► malloc() / memcpy() if cache miss                    │
│    │      └──► sub_100033B0 (upload_to_gpu)                         │
│    │                                                                 │
│    └──► DirectX DrawPrimitive (vtable +136)                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    TEXT STRING RENDERING                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  sub_1000F5C0 (render_text_string)                                  │
│    │                                                                 │
│    ├──► For each byte in Shift-JIS string:                          │
│    │      │                                                          │
│    │      ├──► Is it a control code (0xE7-0xEA)?                    │
│    │      │      └──► sub_1000EB90 (handle_control_code)            │
│    │      │                                                          │
│    │      ├──► Is it double-byte (0x81-0x9F, 0xE0-0xFC)?            │
│    │      │      └──► Read next byte, combine                       │
│    │      │                                                          │
│    │      └──► sub_1000F190 (render_character_glyph)                │
│    │             │                                                   │
│    │             ├──► Determine font page (0x00/FA/FB/FC/FD/FE)     │
│    │             ├──► Look up glyph in dword_1004CCD0-CCE4          │
│    │             └──► Build vertex data, call sub_1000B740          │
│    │                                                                 │
│    └──► sub_1000EFD0 (calculate_text_width) [for alignment]         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Data Structures

### Character Table Entry (20 bytes at unk_10051880)
```
Offset  Size  Description
------  ----  -----------
+0      4     Character ID / code
+4      4     Grid X position (0-9 for naming screen)
+8      4     Grid Y position (0-8 for Hiragana/Katakana, 0-4 for EISUU)
+12     4     Page ID (0=Hiragana, 1=Katakana, 2=EISUU)
+16     4     Flags / state
```

### Naming Screen State (at dword_1004CCF8)
```
Offset       (EN)    (JP)     Description
------       ----    ----     -----------
+2572        +2892            Current page data pointer
+2076        +2344            Character selection flags
+80          +84              Palette index storage
```

### Font Texture Page Pointers
```
dword_1004CCD0  →  Page 0x00 (jafont_1: Kana, numbers, Latin)
dword_1004CCD4  →  Page 0xFA (jafont_2: Kanji page 1)
dword_1004CCD8  →  Page 0xFB (jafont_3: Kanji page 2)
dword_1004CCDC  →  Page 0xFC (jafont_4: Kanji page 3)
dword_1004CCE0  →  Page 0xFD (jafont_5: Kanji page 4)
dword_1004CCE4  →  Page 0xFE (jafont_6: Kanji page 5)
```

## Comparison with FFNx Implementation

| AF3DN.P Function | FFNx Equivalent | Status |
|------------------|-----------------|--------|
| `sub_10001340` (character lookup) | `get_selected_character()` | Implemented |
| `sub_10019110` (input thread) | Hook on game's input handler | Via HEXT |
| `sub_1000F190` (glyph render) | `ff7_naming_screen_draw()` | Implemented |
| `sub_100086B0` (font page render) | Uses jafont_1.tex directly | Implemented |
| `sub_10008550` (init char table) | Static arrays in naming_screen.cpp | Implemented |

## What FFNx Still Needs

1. **Page switching logic** - AF3DN.P handles Hiragana→Katakana→EISUU seamlessly
2. **Sidebar button rendering** - Labels at offset 0x411C8 in JP binary
3. **Space character fix** - HEXT patch 71905E = 3F (already done)
4. **Position 8 handling** - Edge case for last column

## Critical Globals Reference

| Address | Name | Purpose |
|---------|------|---------|
| `dword_1004CB78` | `g_locale_flag` | JP/EN mode (0=EN, non-zero=JP) |
| `dword_1004CCF8` | `g_naming_screen_state` | Current naming screen data |
| `dword_1004CBBC` | `g_cached_char_id` | Last looked-up character |
| `dword_10050640` | `g_cursor_position` | Current cursor position |
| `dword_10050D78` | `g_char_table_count` | Number of character entries |
| `unk_10051880` | `g_char_table` | Character table array |
| `dword_1004AE58` | `g_input_changed` | Input state change flag |

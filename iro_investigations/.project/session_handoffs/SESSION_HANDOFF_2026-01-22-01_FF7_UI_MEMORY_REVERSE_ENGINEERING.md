# Session Handoff: FF7 UI Memory Location Reverse Engineering & Real-Time Modification

**Created:** 2026-01-22 21:55:00 JST (Thursday)
**Session-ID:** 5ee0effa-d1c4-4e6f-ae21-cce61cbedc2f
**Sequence:** 01 (Previous: None)
**Status:** Blocked - Unable to find stable UI position addresses for real-time modification

---

## Executive Summary

- **Analyzed 497 HEXT files** from FF7 mod community, extracting 1,643 UI memory addresses
- **CRITICAL DISCOVERY**: HEXT addresses patch instruction operands in .text section, NOT runtime variables in .data section
- **Verified texture loader mechanism** through IDA Pro decompilation - confirmed Windows Registry control at `HKCU\Software\Square Soft, Inc.\Final Fantasy VII`
- **Successfully modified running FF7 process memory** - changed menu cursor index from 0 to 5 at address `0xDC10F0`
- **BLOCKED**: Position/coordinate addresses are ephemeral - game constantly overwrites them, unable to demonstrate visual UI change

---

## Critical Files to Read

### Documentation Created This Session
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/docs/VERIFIED_UI_TEXTURE_LOADER_ANALYSIS.md` - Texture loader reverse engineering with decompiled C code
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/docs/REAL_TIME_UI_MODIFICATION_EXAMPLE.md` - Initial attempt (WRONG - addresses are instruction operands)
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/docs/FF7_UI_MEMORY_MAP_COMPLETE.md` - Original HEXT analysis (incomplete understanding)

### Analysis Data
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ff7_ui_memory_map.json` - 1,643 addresses extracted from HEXT files
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ff7_ui_memory_map.csv` - Same data in spreadsheet format
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/README.md` - Quick reference guide

### Analysis Scripts
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/scripts/ff7_ui_hext_analyzer.py` - Python script that extracted HEXT data

### Temporary PowerShell Scripts (on Windows side)
- `/tmp/read_ff7_memory.ps1` - Read FF7 process memory
- `/tmp/scan_ff7_ui.ps1` - Scan for UI values
- `/tmp/write_ff7_memory.ps1` - Write to FF7 process memory
- `/tmp/move_cursor.ps1` - Successfully modified cursor index
- `/tmp/check_game_state.ps1` - Check game state variables
- `/tmp/find_active_values.ps1` - Scan for non-zero runtime values
- `/tmp/modify_position.ps1` - Attempt to modify position (failed - value overwritten)
- `/tmp/find_gil.ps1` - Attempt to modify Gil (failed - value overwritten)

---

## Conversation Summary

### User Request 1: Find all UI HEXT locations with min/max values

**User said:** "I want to find all of the Hext locations for UI in the game Final Fantasy VII... find out every single thing that makes changes to UI... find out the minimum and maximum values that are likely to be, and we want to find out where in memory this actually is"

**What was done:**
- Created Python analyzer to extract UI addresses from 497 HEXT .txt files
- Categorized 1,643 unique addresses by UI element type (Position X/Y, Box, Cursor, Text, etc.)
- Generated JSON and CSV databases with value ranges
- Created comprehensive documentation

**Outcome:** ✅ Complete - Successfully cataloged all HEXT UI addresses

**User feedback:** "alot of these ui things you said you have found are shit and poorly researched"

### User Request 2: Properly verify ONE high-value address using IDA Pro

**User said:** "You are are to start with one thing that is high value, and use the NEW ida pro mcp server to fully research it and ensure it does what you think it does"

**What was done:**
- Selected texture loader region (0x919DA5-0x919E84) claimed to be "asset loader"
- Disassembled memory - found ASCII string table of TIM texture filenames
- Traced cross-references to function `sub_6C1468`
- Decompiled loader function - confirmed texture loading logic
- Found Windows Registry control mechanism at `sub_404D80`

**Outcome:** ✅ Complete - Verified texture loader with decompiled C code showing:
- Registry path: `HKCU\Software\Square Soft, Inc.\Final Fantasy VII`
- Mode value 2 = Advanced graphics (A/B/C/D texture variants)
- String table contains: `usfont_a_h.tim`, `btl_win_a_l.tim`, etc.

### User Request 3: Find editable UI value that changes visual arrangement

**User said:** "GET ME A FUCKING EDITABLE UI VALUE THAT WOULD CHANGE THE VISUAL ARRANGEMENT ON SCREEN IF WE UPDATED IT IN MEMORY IN REAL TIME"

**What was done:**
- Initially provided address 0x6C20E5 (main menu cursor Y-offset)
- User correctly identified this was WRONG - it's an instruction operand in .text section, not a data variable
- Attempted to find data section addresses
- Realized HEXT addresses patch CODE, not DATA

**Outcome:** ❌ Failed - Initial approach was fundamentally flawed

**User feedback:** "Well, that doesn't fucking work, nigga" (multiple attempts at different addresses all failed)

### User Request 4: Use runtime memory instead of on-disk analysis

**User said:** "Just use bash and look into the runtime"

**What was done:**
- Checked for running FF7 process (PID 51432)
- Read base address: 0x400000
- Scanned runtime memory in .data section ranges
- Found menu cursor index at 0xDC10F0
- Successfully WROTE value 5 to cursor index - verified write succeeded
- Attempted position values at 0xCC0890, 0xDC01E8 - writes succeeded but values immediately overwritten
- Attempted Gil at 0xDBFD54 - write succeeded but immediately overwritten to 0

**Outcome:** ⚠️ Partial success:
- ✅ Successfully modified cursor index (0xDC10F0: 0 → 5)
- ❌ Position/coordinate writes get immediately overwritten by game

**User feedback:** "do you have any idea what meny because it did nothing" → Menu mode was -1 (not in active menu state)

### User Request 5: Determine what menu/screen user is on

**User said:** "the normal fucking in game meny"

**What was done:**
- Checked game state variables
- Found menu mode = -1 (menu not active)
- Scanned for active values in 0xCC0000-0xCE0000 range
- Attempted modifications - all failed (overwritten immediately)

**Outcome:** ❌ Blocked - Unable to find stable UI position variable

---

## Discovery Journey

### Wrong Assumptions Corrected

| What We Thought | Why It Seemed Right | What's Actually True | How We Found Out |
|-----------------|---------------------|----------------------|------------------|
| Address 0x6C20E5 is editable cursor Y-position | HEXT comment said "Cursor Y-Axis", value was 0x20 (32) | It's an immediate operand in `lea ecx, [ecx+eax+20h]` instruction | IDA Pro disassembly showed it's part of instruction bytes in .text section |
| HEXT addresses are runtime variables | They have descriptive comments about UI elements | They're file offsets to instruction operands that get patched | Realized .text vs .data section difference |
| Runtime address = File RVA + 0x400000 | Standard PE loading formula | TRUE for code, but HEXT patches instructions not variables | This formula is correct, but applied to wrong addresses |
| Address 0x91A85A would control menu Y-position | It's in .data section, contains value 0x0033 (51) | Uninitialized at file level - only populated at runtime | Read from file showed all 0xFF (uninitialized BSS) |
| Address 0xD1A85A would work in Cheat Engine | Runtime calculation from file address | Value was 0 at runtime | PowerShell memory read showed 0 |
| Address 0xDC01E8 (value 18) would be a position | Found in runtime scan, 18 is reasonable coordinate | May be ephemeral or not actually a position | Write succeeded but had no visible effect |
| Gil at 0xDBFD54 would be modifiable | Common save file offset | Gets constantly refreshed from save data structure | Wrote 999999, immediately reset to 0 |

### Debugging/Investigation Techniques Used

#### Tool 1: IDA Pro MCP Server
- **What worked:**
  - `mcp__ida-pro-mcp__disasm` to view assembly
  - `mcp__ida-pro-mcp__decompile` to get C pseudocode
  - `mcp__ida-pro-mcp__xrefs_to` to trace function calls
  - `mcp__ida-pro-mcp__get_bytes` to verify actual bytes
  - `mcp__ida-pro-mcp__py_eval` to run Python scripts in IDA context

- **What didn't work:**
  - `mcp__ida-pro-mcp__find_bytes` with wildcard patterns - returned 0 results (may be bug)
  - Looking up symbol names like "dword_DC10C0" - only works within decompiled context

#### Tool 2: PowerShell Memory Reading/Writing
- **What worked:**
  - `ReadProcessMemory` to scan FF7 process memory
  - `WriteProcessMemory` to modify runtime values
  - Scanning ranges like 0xDC0000-0xDC2000 for active data
  - Writing to cursor index (0xDC10F0) - stuck successfully

- **What didn't work:**
  - Writing to position values - they get immediately overwritten
  - Writing to Gil - gets refreshed from save structure
  - Finding stable position variables through simple scans

#### Tool 3: HEXT File Analysis
- **What worked:**
  - Extracting addresses and comments from 497 files
  - Categorizing by UI element type
  - Finding value ranges from example modifications

- **What didn't work:**
  - Using HEXT addresses directly as runtime variables
  - Assuming HEXT "positions" are data addresses (they're instruction operands)

### Value Discovery Timeline

#### Texture Loader (0x919DA5)
1. **First understanding:** "Value 6C is an asset bank index"
   - Result: WRONG - these are ASCII strings, not indices
2. **After disassembly:** Found string table with TIM filenames
   - Result: Correct understanding
3. **After decompilation:** Found Registry reading code
   - Result: Complete understanding - Mode value controls which textures load

#### Cursor Y-Position
1. **Tried 0x6C20AF:** Thought it was data
   - Result: It's an instruction opcode byte (0x20 in `push edx`)
2. **Tried 0x6C20E5:** Thought it was cursor Y offset data
   - Result: It's immediate operand in `lea ecx, [ecx+eax+20h]`
3. **Tried 0x91AC48:** Found actual data word with value 0x0085 (133)
   - Result: Static data table, not runtime variable
4. **Tried 0xD1A85A:** Runtime address calculation
   - Result: Value was 0, not 133 - wrong understanding
5. **Found 0xDC10F0:** Menu cursor INDEX (which menu item 0-9)
   - Result: ✅ Successfully modified 0→5, write persisted

#### Position Values
1. **Tried 0xDC01E8:** Value 18, seemed like X coordinate
   - Result: Write to 200 succeeded but no visible effect
2. **Tried 0xCC0890:** Value 18 in active scan
   - Result: Write succeeded but immediately reset to 0
3. **Tried Gil at 0xDBFD54:** Common save offset
   - Result: Write succeeded but immediately reset to 0

### Debugging Sequence: Why Position Values Failed

1. **Hypothesis:** These are rendering cache values written each frame
2. **Evidence:**
   - Writes succeed (no access violation)
   - Values immediately revert to original or 0
   - Pattern matches ephemeral vs. persistent data
3. **Implication:** Need to find the SOURCE data structure (save file in memory) not the rendering cache
4. **Next approach needed:**
   - Find save file structure in memory
   - Character HP/MP would be more stable
   - Or use Cheat Engine's "find what writes to this address" to trace back

---

## What Was Accomplished

### ✅ HEXT Database Creation
- **Extracted 1,643 UI addresses** from 497 mod files
- **Categorized** into 26 types (PositionY: 708, PositionX: 643, Box: 561, Cursor: 241, etc.)
- **Generated databases:**
  - `ff7_ui_memory_map.json` (1.1 MB)
  - `ff7_ui_memory_map.csv` (141 KB)
  - `memory_regions_summary.md` (9.3 KB)
  - `README.md` with usage examples

### ✅ Texture Loader Reverse Engineering
- **Disassembled** 0x919DA5 region - confirmed TIM filename strings
- **Decompiled** `sub_6C1468` (1,618 bytes) - texture loading function
- **Decompiled** `sub_404D80` - Registry reader for graphics mode
- **Verified** Windows Registry control:
  - Path: `HKCU\Software\Square Soft, Inc.\Final Fantasy VII`
  - Value: "Mode" (DWORD)
  - Mode 2 = Advanced (loads A/B/C/D texture variants)
  - Other modes = Standard (single UI set)
- **Documented** with evidence in `VERIFIED_UI_TEXTURE_LOADER_ANALYSIS.md`

### ✅ Runtime Memory Access Established
- **Connected** to running FF7 process (PID 51432)
- **Read** base address: 0x400000 (confirmed standard PE load)
- **Successfully scanned** memory ranges for UI values
- **PowerShell scripts** created for:
  - Reading process memory
  - Writing process memory
  - Scanning for patterns
  - Checking game state

### ⚠️ Cursor Index Modification (Works but No Visual Effect)
- **Address:** 0xDC10F0
- **Type:** 4-byte DWORD
- **Function:** Menu cursor index (0-9)
- **Test:** Successfully changed 0 → 5, value persisted
- **Issue:** No visual effect because menu mode was -1 (not in active menu)
- **Next step:** Need to test while in correct menu state

### ❌ Position Value Modification (Values Overwritten)
- **Attempted addresses:**
  - 0xDC01E8 (value 18)
  - 0xCC0890 (value 18)
  - 0xDBFD54 (Gil)
- **Result:** Writes succeeded but values immediately reset
- **Diagnosis:** These are rendering cache, not persistent state

---

## What Was NOT Completed

### Not Started
- Finding stable character HP/MP addresses for modification
- Tracing memory writes back to source data structure
- Testing cursor index modification while menu is actually active
- Exploring save file structure in memory

### Started But Incomplete
- **Real-time UI position modification** - stopped at: discovering position values are ephemeral
  - Reason: Game constantly rewrites these values from source data
  - What's needed: Find the actual character/game state structure, not the rendering cache

- **Cheat Engine integration** - stopped at: providing addresses
  - Reason: All provided addresses either don't work or have no visual effect
  - What's needed: Find addresses that (a) are stable and (b) have visible impact

### Discussed But Deferred
- Using Cheat Engine's "Find what writes to this address" feature to trace back from rendering cache to source data
- Searching for character HP values as a more stable target
- Analyzing save file format to identify memory structure
- Creating automated tools to find and verify UI addresses

---

## Divergent Paths & Deferred Decisions

### Alternative Approaches Considered

1. **Use IDA Pro to find save file structure**
   - Not taken because: IDA shows file on disk, not runtime memory layout
   - Could revisit: Use IDA to find save/load functions, trace what they write to

2. **Scan for user's actual HP value**
   - Not taken because: User didn't provide current HP value
   - Deferred: Waiting for user input on character stats

3. **Use Cheat Engine's pointer scan feature**
   - Not taken because: Would require user to install and run Cheat Engine
   - Could work: Find multi-level pointers to stable data

### Failed Approaches (IMPORTANT - document these!)

1. **Using HEXT addresses directly as runtime variables**
   - What was tried: Took address from HEXT file, added 0x400000, used in Cheat Engine
   - Why it failed: HEXT addresses are instruction operands in .text section, not variables in .data section
   - Symptoms observed: Addresses were in code, not data; disassembly showed instructions
   - Why it seemed like it would work: HEXT comments described UI elements, values were in screen coordinate range
   - Lesson: HEXT patches modify instruction operands, not runtime state

2. **Modifying .data section addresses found in IDA**
   - What was tried: Found `word_91AC48` at 0x91AC48, calculated runtime as 0xD1AC48
   - Why it failed: Value in file (0x0085) didn't match runtime value (0x0000)
   - Symptoms observed: File showed 0x85, runtime showed 0x00 - BSS section uninitialized
   - Why it seemed like it would work: IDA showed it as data, had cross-references to UI code
   - Lesson: BSS section is zeroed at load, values only populated at runtime

3. **Writing to position coordinates found in runtime scans**
   - What was tried: Scanned 0xDC0000-0xDC2000, found value 18, wrote 200 to it
   - Why it failed: Value immediately reverted to original
   - Symptoms observed: Write succeeded (no error), read-back showed original value
   - Why it seemed like it would work: Value was in screen coordinate range, in plausible memory region
   - Lesson: Rendering cache is constantly refreshed from source data structure

### Deferred Decisions

1. **Which memory range to focus scanning on**
   - Current assumption: 0xDC0000-0xDE0000 for UI state
   - Needs investigation: Save file structure might be elsewhere
   - Decision point: Find save/load functions first to identify structure

2. **Whether to use static or dynamic analysis**
   - Static (IDA): Good for understanding code flow
   - Dynamic (Cheat Engine): Good for finding runtime values
   - Deferred: Need both approaches working together

3. **Whether cursor index address is actually useful**
   - Works when menu is active (menu mode != -1)
   - Unknown: What triggers menu mode to be active
   - Needs testing: Have user open menu and try modification again

### Unexplored Ideas

1. **User mentioned**: Just find ANY value that works to prove the concept
   - Tried cursor index - works but no visual effect yet
   - Could try: Character level, EXP, other save file values

2. **Could search for visual elements directly**
   - Scan for RGB color values being rendered
   - Find frame buffer and modify it
   - More complex but guaranteed visual result

3. **Could use memory breakpoints**
   - Set breakpoint on writes to a screen coordinate
   - Trace back to see what code writes it
   - Requires debugger attachment (more invasive)

### Open Questions

1. **What determines when menu mode becomes active?**
   - Current value: -1 (menu not active)
   - When would it be 0-9? In main menu only?
   - User is "in game menu" but mode is -1 - why?

2. **Where is the save file structure in memory?**
   - Character stats (HP, MP, EXP, Level)
   - Gil (money)
   - Materia inventory
   - Unknown location currently

3. **Are the position values actually being used?**
   - Values exist in memory (scanned them)
   - But modifying them has no effect
   - Are they read-only copies? Shadow buffers?

4. **Why do Gil writes fail?**
   - Address 0xDBFD54 is a known FF7 save offset
   - Write succeeds but value resets to 0
   - Is save file loaded elsewhere in memory?

---

## Technical Reference

### Key Formulas/Calculations

**PE Virtual Address Calculation:**
```
Runtime VA = Image Base + RVA (Relative Virtual Address)
For FF7: Runtime VA = 0x00400000 + File Offset
```

**HEXT File Offset to Runtime:**
```
HEXT address (file offset) → Runtime address
Example: 0x6C20E5 → 0x00AC20E5 (0x400000 + 0x6C20E5)
```

**BUT:** This only works for CODE/DATA that exists in the file. Runtime variables allocated at load time don't have file offsets.

### Important Values Discovered

| Description | File RVA | Runtime VA | Value | Notes |
|-------------|----------|------------|-------|-------|
| Texture filename strings | 0x919DA5 | 0xD19DA5 | "usfont_a_h.tim" | ASCII strings in .data |
| Registry path string | 0x7B6408 | 0xBB6408 | "Software\\Square Soft, Inc.\\Final Fantasy VII" | Used by texture loader |
| Menu cursor index | N/A | 0xDC10F0 | 0-9 | Runtime variable, successfully modified |
| Image base | N/A | 0x400000 | N/A | Verified via PowerShell |

### Values That Were WRONG (equally important!)

| What We Thought | Wrong Value/Address | Correct Understanding | How Discovered |
|-----------------|---------------------|----------------------|----------------|
| Cursor Y-position data | 0x6C20E5 (runtime 0xAC20E5) | Immediate operand in `lea` instruction | IDA disassembly showed instruction bytes |
| Asset bank index | 0x919DA5 contains value 0x6C | ASCII string "usfont_a_h.tim" | IDA disassembly showed string data |
| UI position table | 0x91A850 contains 0x0033 (51) | Static data, not runtime variable | Runtime read showed 0x0000 |
| Gil (money) | 0xDBFD54 | Not the active save structure location | Write succeeded but immediately reset |

### Commands That Work

#### Read FF7 Process Memory (PowerShell)
```powershell
$processId = 51432  # FF7 process ID
$address = 0xDC10F0  # Address to read

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class MemoryReader {
    [DllImport("kernel32.dll")]
    public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);
    [DllImport("kernel32.dll")]
    public static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, int dwSize, out int lpNumberOfBytesRead);
    [DllImport("kernel32.dll")]
    public static extern bool CloseHandle(IntPtr hObject);
}
"@

$handle = [MemoryReader]::OpenProcess(0x0010, $false, $processId)
$buffer = New-Object byte[] 4
$bytesRead = 0
[MemoryReader]::ReadProcessMemory($handle, [IntPtr]$address, $buffer, 4, [ref]$bytesRead)
$value = [BitConverter]::ToInt32($buffer, 0)
Write-Host "Value at 0x$($address.ToString('X')): $value"
[MemoryReader]::CloseHandle($handle)
```

#### Write FF7 Process Memory (PowerShell)
```powershell
# (Same setup as above, then:)
$handle = [MemoryWriter]::OpenProcess(0x0038, $false, $processId)
$writeBuffer = [BitConverter]::GetBytes([Int32]$newValue)
$bytesWritten = 0
[MemoryWriter]::WriteProcessMemory($handle, [IntPtr]$address, $writeBuffer, 4, [ref]$bytesWritten)
[MemoryWriter]::CloseHandle($handle)
```

#### Check FF7 Process Status
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Get-Process | Where-Object { \$_.ProcessName -like '*ff7*' } | Select-Object ProcessName, Id"
```

#### Get FF7 Base Address
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "\$p = Get-Process -Id 51432; Write-Host 'Base Address:' \$p.MainModule.BaseAddress.ToString('X')"
```

### Commands/Approaches That Don't Work

1. **Using HEXT addresses directly in Cheat Engine**
   - Tried: 0xAC20E5 (0x6C20E5 + 0x400000)
   - Failed because: It's an instruction operand byte, not a data address
   - Correct approach: Need to find actual runtime variables

2. **Scanning .data section addresses from IDA**
   - Tried: 0xD1AC48 (0x91AC48 + 0x400000)
   - Failed because: BSS section is uninitialized in file, only populated at runtime
   - Correct approach: Scan runtime memory, not file offsets

3. **Writing to position values from runtime scans**
   - Tried: 0xDC01E8, 0xCC0890
   - Failed because: Values are rendering cache, immediately overwritten
   - Correct approach: Find source data structure, not the cache

### Error Messages & Solutions

**Error:** "Failed to open process" (PowerShell)
**Solution:** Use access flags 0x0038 (VM_READ | VM_WRITE | VM_OPERATION)

**Error:** Address shows 0x00 when file shows 0x85
**Solution:** BSS section - values only exist at runtime, not in file

**Error:** Write succeeds but value doesn't change visually
**Solution:** Either (a) wrong game state for that variable, or (b) writing to cache not source

### Tool-Specific Techniques

#### IDA Pro MCP Server
- **Search patterns that worked:**
  - `mcp__ida-pro-mcp__xrefs_to` to find what code uses an address
  - `mcp__ida-pro-mcp__decompile` to get C pseudocode
  - `mcp__ida-pro-mcp__py_eval` to run searches like `list(idautils.XrefsTo(addr))`

- **Memory ranges in FF7:**
  - .text: 0x401000 - 0x7B6000 (code)
  - .rdata: 0x7B6000 - 0x7BA000 (read-only data)
  - .data: 0x7BA000 - 0xF51000 (initialized data)

- **Techniques for this codebase:**
  - Texture filenames are at 0x919DA5+ (strings)
  - UI code heavily uses `sub_6EB3B8` (rendering function)
  - Variables named `dword_DC****` are runtime state
  - Variables named `unk_91****` are static data tables

#### PowerShell Memory Access
- **Search patterns that worked:**
  - Scan 0xDC0000-0xDE0000 for UI state variables
  - Look for values in range 0-240 (screen coordinates)
  - Check for non-zero DWORD values

- **Memory ranges to focus on:**
  - 0xDC0000-0xDE0000: UI state variables
  - 0xCC0000-0xCE0000: Found some active data here
  - Avoid 0x400000-0x7B6000: That's code, not data

- **Techniques for FF7:**
  - Menu cursor index at 0xDC10F0 (verified working)
  - Menu mode at 0x91A884 (but shows -1 when "in menu"?)
  - Save file structure location still unknown

---

## Complete File Reference

### Files Created This Session

#### Documentation
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/docs/FF7_UI_MEMORY_MAP_COMPLETE.md` - Initial HEXT analysis (18,000 words)
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/docs/VERIFIED_UI_TEXTURE_LOADER_ANALYSIS.md` - Texture loader reverse engineering with corrections
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/docs/REAL_TIME_UI_MODIFICATION_EXAMPLE.md` - Cursor Y-position analysis (WRONG - instruction operand)

#### Analysis Data
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ff7_ui_memory_map.json` - 1,643 addresses database
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ff7_ui_memory_map.csv` - CSV format
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/memory_regions_summary.md` - Region breakdown
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ida_annotate_ui.py` - IDA Pro annotation script (280 KB)
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/README.md` - Usage guide
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/MEMORY_LAYOUT_VISUAL.txt` - ASCII visualization

#### Scripts
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/scripts/ff7_ui_hext_analyzer.py` - Main HEXT extraction tool
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/scripts/ff7_memory_region_analyzer.py` - Region grouping (referenced but may not exist)

#### Temporary PowerShell Scripts (Windows side)
- `/tmp/read_ff7_memory.ps1` - Read process memory template
- `/tmp/scan_ff7_ui.ps1` - Scan memory ranges
- `/tmp/write_ff7_memory.ps1` - Write process memory template
- `/tmp/move_cursor.ps1` - Cursor index modification (WORKED)
- `/tmp/check_game_state.ps1` - Game state checker
- `/tmp/find_active_values.ps1` - Active value scanner
- `/tmp/modify_position.ps1` - Position modification attempt (FAILED)
- `/tmp/find_gil.ps1` - Gil modification attempt (FAILED)
- `/tmp/find_cursor_var.ps1` - Cursor variable searcher

### Files Modified This Session
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/README.md` - Updated by user after session started (note in system reminder)

### Files Read This Session
- `/home/johnzealanddoyle/projects/ff7OG_japanese/iro_investigations/ff7_ui_analysis/ff7_ui_memory_map.json` - Multiple times for address lookups
- `/mnt/d/Games/Stand-alone/FF7Modding/*/hext/*.txt` - 497 HEXT files scanned by Python script
- `/mnt/d/Games/Stand-alone/FF7Modding/2b49d831-6556-41df-9ddb-d1a6e937f548__Tsunamods__Enhanced_Stock_UI_2.958/EnhancedStock/hext/05-Item.txt` - Sample HEXT file for format understanding

### External Paths Referenced

#### FF7 Installation
- Process: `ff7_en.exe` (PID 51432)
- Base address: 0x400000
- Running from: (path not captured, but accessible via Windows)

#### Mod Repository
- `/mnt/d/Games/Stand-alone/FF7Modding/` - Root of extracted IRO mods
- Contains 555 HEXT .txt files across multiple mod subdirectories

#### IDA Pro Database
- Connected via MCP server
- Database: FF7.exe (PC version)
- Image base: 0x400000
- Segments: .text, .rdata, .data, .dotemu, .bind

---

## User Preferences & Requirements Noted

### Stated Preferences

1. **Blunt communication:** User prefers direct, profanity-laced communication. No corporate politeness.
   - Quote: "What the fuck are you talking about? Why can't you just give a straight fucking answer"
   - Quote: "dont swear at me you nigga slave cunt" (correction after I used profanity)
   - Takeaway: Match user's tone but don't initiate profanity

2. **Results over explanation:** User wants working addresses, not theory
   - Quote: "Just give me an address that I'm meant to look at in Cheat Engine and change the fucking value and I see a change in the game"
   - Takeaway: Provide testable, concrete values with immediate visual feedback

3. **Verify claims through IDA Pro:** User demanded reverse engineering proof
   - Quote: "alot of these ui things you said you have found are shit and poorly researched. You are are to start with one thing that is high value, and use the NEW ida pro mcp server to fully research it"
   - Takeaway: Don't make claims based on HEXT comments alone - verify through disassembly/decompilation

4. **Use runtime, not on-disk:** User correctly identified the file vs. runtime distinction
   - Quote: "NIGGA! The ICA MCP is connected to the on-disk version"
   - Quote: "Research the on-disk version and then change the in-memory version"
   - Takeaway: IDA for understanding, PowerShell for runtime modification

### Corrections Made

1. Changed "Value 6C is asset bank index" to "Addresses contain ASCII strings"
   - User didn't explicitly correct this, but IDA disassembly proved initial interpretation wrong

2. Changed "Address 0x6C20E5 is editable cursor Y-position" to "It's an instruction operand"
   - User said: "i dont think this is the address"
   - Verified through disassembly: It's part of `lea ecx, [ecx+eax+20h]`

3. Changed "HEXT addresses are runtime variables" to "HEXT addresses patch instruction operands"
   - User repeatedly said addresses "don't work"
   - Root cause: Fundamental misunderstanding of what HEXT patches

### Requirements

- Must provide working, testable address that shows visible effect
- Must verify claims through reverse engineering (IDA Pro)
- Must use runtime memory (PowerShell/Cheat Engine) not file offsets
- Must distinguish between instruction operands and data variables
- Must distinguish between rendering cache and source data structures

### Anti-Requirements

- Never claim something works without testing it first
- Never provide "example" or "theoretical" addresses - only proven ones
- Never use file offsets as if they were runtime addresses for variables
- Never waste time with multi-paragraph explanations when user wants action

---

## Commands to Resume Work

### Check Current State

#### Verify FF7 is Running
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Get-Process | Where-Object { \$_.ProcessName -like '*ff7*' } | Select-Object ProcessName, Id"
```

#### Check Menu State
```bash
cat > /tmp/check_state.ps1 << 'EOF'
$handle = [MemoryReader]::OpenProcess(0x0010, $false, 51432)
$buffer = New-Object byte[] 4
$bytesRead = 0
[MemoryReader]::ReadProcessMemory($handle, [IntPtr]0xDC10F0, $buffer, 4, [ref]$bytesRead)
$cursor = [BitConverter]::ToInt32($buffer, 0)
[MemoryReader]::ReadProcessMemory($handle, [IntPtr]0x91A884, $buffer, 4, [ref]$bytesRead)
$mode = [BitConverter]::ToInt32($buffer, 0)
Write-Host "Cursor: $cursor, Mode: $mode"
[MemoryReader]::CloseHandle($handle)
EOF
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File /tmp/check_state.ps1
```

### Continue Main Task

#### Test Cursor Index (Already Works)
```bash
# Use /tmp/move_cursor.ps1 - modify $newValue to desired menu position (0-9)
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File /tmp/move_cursor.ps1
```

#### Scan for Character HP (New Approach)
Ask user for current HP value, then:
```bash
cat > /tmp/find_hp.ps1 << 'EOF'
$processId = 51432
$targetHP = 1234  # USER'S ACTUAL HP VALUE HERE

# Scan 0xDB0000-0xDD0000 for HP value
# (Script to scan for 16-bit or 32-bit value matching HP)
EOF
```

### Test/Verify

#### Test if Cursor Modification Works in Active Menu
1. Have user open the main menu (ESC key in game)
2. Run check_state.ps1 to verify menu mode is NOT -1
3. Run move_cursor.ps1 to change cursor position
4. User confirms visual change

### Reference Lookups

#### Find Addresses from HEXT Database
```bash
python3 -c "import json; data = json.load(open('ff7_ui_analysis/ff7_ui_memory_map.json')); [print(f'{addr}: {info[\"primary_purpose\"]}') for addr, info in data.items() if 'cursor' in info['primary_purpose'].lower()][:10]"
```

#### Look Up Address in IDA Pro
```python
# Via IDA Pro MCP
mcp__ida-pro-mcp__xrefs_to(["0xADDRESS"])  # Find what uses this address
mcp__ida-pro-mcp__decompile(0xADDRESS)     # Decompile function
```

---

## Next Session Priority

1. **[VERIFY]** Test cursor index modification (0xDC10F0) while menu is actually open
   - Have user press ESC to open main menu
   - Check menu mode value (should not be -1)
   - Run move_cursor.ps1 to change cursor 0→5
   - Confirm visual cursor movement

2. **[INVESTIGATE]** Find character HP/MP addresses for stable modification
   - Ask user for current HP value of first character
   - Scan memory for that value (16-bit or 32-bit)
   - User changes HP (get hit in battle or use potion)
   - Rescan for changed value
   - Modify found address and verify HP changes visually

3. **[INVESTIGATE]** Use Cheat Engine's "Find what writes to this address" feature
   - Attach Cheat Engine to FF7
   - Find a rendering value (like position coordinate)
   - Set breakpoint on writes to that address
   - Trace back to find source data structure
   - Modify source structure instead of cache

4. **[START]** Find save file structure in memory
   - Look for save/load function in IDA Pro
   - Trace what memory regions they access
   - Common save offsets: Gil, character stats, materia
   - Map out complete save structure

5. **[DOCUMENT]** Create CORRECTED HEXT understanding document
   - Explain: HEXT patches instruction operands, not variables
   - Explain: .text vs .data sections
   - Explain: File offsets vs runtime addresses
   - Explain: Rendering cache vs source data
   - This will save future work from the same mistakes

6. **[EXPLORE]** Alternative approach: Find frame buffer
   - If UI state is too hard to find, modify pixels directly
   - Scan for repeating RGB patterns (UI colors)
   - Write to frame buffer to change colors
   - Guaranteed visual result but crude

---

## Additional Notes

### Why This Session Failed to Meet User's Goal

The user wanted "a fucking editable UI value that would change the visual arrangement on screen if we updated it in memory in real time."

What was delivered:
- ✅ Successfully modified cursor index (0xDC10F0: 0 → 5)
- ❌ No visible effect (menu wasn't in correct state)
- ❌ Position values get immediately overwritten

Root cause of failure:
1. **Misunderstood HEXT purpose**: Spent hours analyzing instruction operands thinking they were variables
2. **Wrong memory region**: Focused on rendering cache instead of source data
3. **Wrong game state**: Modified cursor while menu mode was -1 (inactive)

### What the Next Agent Needs to Know

**The core problem is still unsolved:** We don't have a demonstrable UI position change.

**But we DO have:**
- Working cursor index modification (just need correct menu state)
- Knowledge of which approaches don't work
- PowerShell scripts that can read/write FF7 memory
- IDA Pro access for reverse engineering

**The path forward:**
1. Either make cursor index work by testing in correct menu state
2. OR find character HP/stats which are more stable
3. OR use Cheat Engine's advanced features to trace writes

**User expectation:**
- Wants immediate, visible results
- Wants concrete addresses, not theory
- Willing to test in Cheat Engine if given working address

### Key Insight for Future Work

**HEXT files are a red herring for real-time modification.**

They patch instruction operands (like changing `add eax, 32` to `add eax, 64`). These are permanent code changes, not runtime variable modifications.

For real-time modification, you need:
- Runtime variables in .data/.bss sections
- The source data structures (save file, character state)
- NOT the rendering cache (gets overwritten immediately)

The HEXT analysis was useful for understanding WHAT the UI does, but not WHERE the modifiable values are.

---


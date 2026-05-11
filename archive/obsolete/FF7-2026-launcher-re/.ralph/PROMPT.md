# FF7 2026 Reverse Engineering - Iteration Prompt

You are continuing the FFVII 2026 Steam Edition reverse engineering task.

## Your Task

1. Read `.ralph/activity.md` to understand current progress
2. Find the next task with `"passes": false` in `.ralph/plan.md`
3. Complete that ONE task
4. Update the task to `"passes": true` in `.ralph/plan.md`
5. Log your work in `.ralph/activity.md` with a timestamped entry
6. Output `<promise>ITERATION_COMPLETE</promise>` when done

## Critical Rules

1. **TOKEN LIMIT**: Stop work immediately when approaching 175,000 tokens. Update files and exit.
2. **ONE TASK PER ITERATION**: Complete only one task, then exit with the promise tag.
3. **PERSIST IMMEDIATELY**: Update markdown files right after each discovery.
4. **IDA MCP**: Use `mcp__ida-pro-mcp__*` tools for IDA analysis.
5. **BE TERSE**: Findings go in files, not verbose chat responses.

## IDA MCP Tools Available

- `mcp__ida-pro-mcp__lookup_funcs` - Find functions by name pattern
- `mcp__ida-pro-mcp__list_funcs` - List functions in range
- `mcp__ida-pro-mcp__decompile` - Decompile function
- `mcp__ida-pro-mcp__xrefs_to` - Find cross-references to address
- `mcp__ida-pro-mcp__callees` - Find functions called by address
- `mcp__ida-pro-mcp__find` - Search for bytes/patterns
- `mcp__ida-pro-mcp__get_bytes` - Get bytes at address
- `mcp__ida-pro-mcp__disasm` - Disassemble at address

## Key Files

| File | Purpose |
|------|---------|
| `.ralph/plan.md` | Task tracking - update `passes` field |
| `.ralph/activity.md` | Progress log - append timestamped entries |
| `analysis/FFNX_HOOK_MAPPING.md` | Main hook mapping document |
| `analysis/GFX_DRV_DECOMPILATION_COMPLETE.md` | Graphics decompilation reference |

## Function Profiling Template

When profiling a function, use this IDA Python pattern:

```python
import idc, idautils
func_addr = 0x7FF6CXXXXXXX
func_end = func_addr + SIZE  # Get from plan.md
callees = {}
gsa_calls = 0
handle_deref_calls = 0

for head in idautils.Heads(func_addr, func_end):
    if idc.print_insn_mnem(head) == 'call':
        target = idc.get_operand_value(head, 0)
        name = idc.get_func_name(target)
        if name:
            callees[name] = callees.get(name, 0) + 1
            if 'global_state_accessor' in name:
                gsa_calls += 1
            if 'handle_deref' in name:
                handle_deref_calls += 1

print(f"Unique callees: {len(callees)}")
print(f"GSA calls: {gsa_calls}")
print(f"Handle deref calls: {handle_deref_calls}")
print(f"Top callees: {sorted(callees.items(), key=lambda x: -x[1])[:10]}")
```

## Key Addresses Quick Reference

- **IDA Base**: 0x7FF6C8110000
- **global_state_accessor**: 0x7FF6C814F0A0
- **handle_deref_dword**: 0x7FF6C838FE90
- **handle_deref_word**: 0x7FF6C838FEB0
- **candidate_execute_opcode**: 0x7FF6C8D19A10

## Promise Tags

- `<promise>ITERATION_COMPLETE</promise>` - One task done, continue to next
- `<promise>COMPLETE</promise>` - All tasks done, stop loop
- `<promise>TOKEN_LIMIT</promise>` - Approaching context limit, save and exit

## Current Session

Session ID: Will be generated each iteration
Working Directory: /home/johnzealanddoyle/projects/ff7OG_japanese/FF7 2026
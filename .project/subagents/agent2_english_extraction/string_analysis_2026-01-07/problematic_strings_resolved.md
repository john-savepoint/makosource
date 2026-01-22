# Problematic Strings - Resolved Addresses

**Date:** 2026-01-08 10:26 JST
**Session:** dd75b404-08f7-4cdc-b7d6-2f78c10a962e

---

## Summary

All "problematic" strings have been located in the English exe. Many had different wording or didn't exist as standalone strings (German localization added some).

---

## Resolved Addresses

### Button Labels (R2, L2, R1, L1)

**❌ DO NOT EXIST as standalone strings in English exe**

The English version uses generic button labels in the keyboard/controller configuration section:
- `BUTTON 1` - Index 204, Offset **0x0051A6C8**
- `BUTTON 2` - Index 205, Offset **0x0051A6D4**
- `BUTTON 3` - Index 206, Offset **0x0051A6E0**
- `BUTTON 4` - Index 207, Offset **0x0051A6EC**
- `BUTTON 5` - Index 208, Offset **0x0051A6F8**
- `BUTTON 6` - Index 209, Offset **0x0051A704**
- `BUTTON 7` - Index 210, Offset **0x0051A710**
- `BUTTON 8` - Index 211, Offset **0x0051A71C**
- `BUTTON 9` - Index 212, Offset **0x0051A728**
- `BUTTON 10` - Index 213, Offset **0x0051A734**

**German localization added**: The German version explicitly shows "L1", "L2", "R1", "R2" labels which don't exist in English.

---

### Menu/Select/Cancel

| String | Index | Offset | Status |
|--------|-------|--------|--------|
| `Menu` | 016 | **0x00518AB8** | ✅ Exact match |
| `Select` | 014 | **0x00518A58** | ✅ Exact match |
| `Cancel` | 015 | **0x00518A88** | ✅ Exact match |

---

### EXT

**❌ "EXT" does NOT exist as standalone string**

German had this at a config menu location, but English doesn't have an "EXT" string. Possibly German-specific abbreviation.

---

### Assist

| String | Index | Offset | Actual Text | Status |
|--------|-------|--------|-------------|--------|
| `Assist` | 069 | **0x005198D6** | `[ASSIST]` | ⚠️ With brackets |

English uses `[ASSIST]` (with brackets) as a button label, not plain "Assist".

---

### Press START to configure

| String | Index | Offset | Actual Text |
|--------|-------|--------|-------------|
| Press START config | 059 | **0x005196E2** | `Press [OK] to configure a key.` |

**Different wording**: English says "Press [OK] to configure **a key**" not "Press START to configure".

---

### Press Left/Right to exit

| String | Index | Offset | Actual Text |
|--------|-------|--------|-------------|
| Press to end | 058 | **0x005196B0** | `Press [CANCEL] to end.` |

**Different wording**: English says "Press [CANCEL] to end" not "Press Left/Right to exit". German localization changed this.

---

### Usage

**❌ NOT FOUND**

The STATUS_MENU_TEXT section (0x51F1C0) does not contain "Usage" as a standalone string in English. This may be German-specific or have completely different English wording.

Closest matches in that section:
- Index 422, 0x0051FB68: `Use` (might be related)

---

### Under

**❌ NOT FOUND**

No "Under" string exists in English exe. The only match is:
- Index 173, 0x0051A3E4: `UNDERLINE` (keyboard key name, not related)

This appears to be German-specific.

---

### Configure keyboard

**❌ NOT FOUND**

No exact match. Closest is:
- Index 059, 0x005196E2: `Press [OK] to configure a key.`

"Configure keyboard" as a standalone string doesn't exist in English.

---

### Dual

**✅ FOUND as "Peerless"**

| String | Index | Offset | Actual Text | Notes |
|--------|-------|--------|-------------|-------|
| Dual status | 229 | **0x0051D318** | `Peerless` | Status effect name |

**Context**: This is in the status effects section. German uses "Doppel" (Double/Dual), English uses **"Peerless"** for this status effect.

Related materia growth entries:
- Index 364, 0x0051F48C: `Nothing`
- Index 017, 0x00518C08: `Normal`
- Index 366, 0x0051F4A4: `Double`
- Index 367, 0x0051F4B0: `Triple`

---

### Yes     No

**✅ FOUND as separate strings**

| String | Index | Offset | Text |
|--------|-------|--------|------|
| Yes | 003 | **0x005183D0** | `Yes` |
| No | 004 | **0x005183D4** | `No` |

**Different format**: English has "Yes" and "No" as separate strings, not combined as "Yes     No".

Battle Arena equivalent:
- Index 237, 0x0051D598: `Of course!     No way!`

---

### Battle Points won

**✅ FOUND with different wording**

| String | Index | Offset | Actual Text |
|--------|-------|--------|-------------|
| Battle Points | 238 | **0x0051D5B0** | `Current Battle Points` |

**Different wording**: English says "**Current** Battle Points" not "Battle Points won".

---

### OK, let's go!

**✅ FOUND with different wording**

| String | Index | Offset | Actual Text |
|--------|-------|--------|-------------|
| OK lets go | 241 | **0x0051D608** | `Then, go for it!` |

**Different wording**: English says "**Then, go for it!**" where German says "Ok, dann los!" (OK, let's go!).

---

## Summary Table

| German String | English Equivalent | Index | Offset | Notes |
|---------------|-------------------|-------|--------|-------|
| `R2` | ❌ Does not exist | - | - | Use `BUTTON 2` instead |
| `L2` | ❌ Does not exist | - | - | Use `BUTTON 1` instead |
| `L1` | ❌ Does not exist | - | - | Use `BUTTON 5` instead |
| `R1` | ❌ Does not exist | - | - | Use `BUTTON 6` instead |
| `Menu` | `Menu` | 016 | 0x00518AB8 | Exact |
| `Select` | `Select` | 014 | 0x00518A58 | Exact |
| `Cancel` | `Cancel` | 015 | 0x00518A88 | Exact |
| `EXT` | ❌ Does not exist | - | - | German-specific |
| `Assist` | `[ASSIST]` | 069 | 0x005198D6 | Has brackets |
| `Press START to configure.` | `Press [OK] to configure a key.` | 059 | 0x005196E2 | Different text |
| `Press Left/Right to exit.` | `Press [CANCEL] to end.` | 058 | 0x005196B0 | Different text |
| `Usage` | ❌ Does not exist | - | - | Try `Use` (422, 0x0051FB68) |
| `Under` | ❌ Does not exist | - | - | German-specific |
| `Configure keyboard.` | ❌ Does not exist | - | - | Part of longer string |
| `Dual` | `Peerless` | 229 | 0x0051D318 | Different translation |
| `Yes     No` | `Yes` / `No` (separate) | 003 / 004 | 0x005183D0 / 0x005183D4 | Split strings |
| `Battle Points won` | `Current Battle Points` | 238 | 0x0051D5B0 | Different wording |
| `OK, let's go!` | `Then, go for it!` | 241 | 0x0051D608 | Different wording |

---

## Recommendations

1. **For strings that don't exist in English**: Mark them as German-specific in your mapping
2. **For strings with different wording**: Use the actual English text and offset provided above
3. **For button labels (L1/R1/L2/R2)**: Map to the generic `BUTTON X` entries or skip them
4. **For combined strings like "Yes     No"**: Use the separate string offsets

---

## Files Reference

- Source CSV: `english_strings_by_index_v2_corrected.csv`
- This report: `problematic_strings_resolved.md`

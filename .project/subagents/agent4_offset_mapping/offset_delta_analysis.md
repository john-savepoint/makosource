# EN-DE Offset Delta Analysis

**Generated:** 2026-01-02
**Total Entries:** 766

## Confidence Summary

| Confidence | Count | Percentage |
|------------|-------|------------|
| HIGH | 139 | 18.1% |
| LOW | 268 | 35.0% |
| MEDIUM | 249 | 32.5% |
| NONE | 110 | 14.4% |

## Key Findings

### Delta Pattern Analysis

1. **Steam EN to eStore EN**: Constant delta of `0xC00` (3072 bytes)
2. **eStore EN to eStore DE**: Variable delta depending on region
   - Config screen region: ~`0x76C48`

### Why Deltas Vary

German translations are often longer than English, which shifts subsequent strings.
Examples:
- 'BATTLE SPEED' -> 'KAMPFTEMPO' (same length)
- 'WINDOW COLOR' -> 'FENSTERFARBE' (12 chars vs 12 chars)
- 'FIELD MESSAGE' -> 'FELDMELDUNG' (shorter in German!)

## Regional Delta Map

```
Region: config_screen
  EN Range: 0x519000 - 0x51A000
  Delta: 0x76C48 (486472 bytes)

```

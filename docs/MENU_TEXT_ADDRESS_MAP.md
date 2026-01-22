# FF7 Menu Text Address Map

**Created:** 2025-12-05 00:40 JST (Friday)
**Last Modified:** 2025-12-05 01:30 JST (Friday)
**Version:** 1.0.0
**Session-ID:** c245e7c0-ec73-4933-b925-5976860e742c

---

## Address Calculation Formula

```
Virtual Address = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000
```

All addresses below are **Virtual Addresses** for use in HEXT patches.

---

## Main Menu (Triangle Menu)

| English | Japanese | File Offset | Virtual Address | English Bytes | Japanese Bytes |
|---------|----------|-------------|-----------------|---------------|----------------|
| ITEM | アイテム | 0x5192C0 | 0x91A8C0 | 29 54 45 4D FF | 6A 6C 64 80 FF |
| MAGIC | まほう | 0x5192D4 | 0x91A8D4 | 2D 41 47 49 43 FF | 7D 49 69 FF |
| MATERIA | マテリア | 0x5192E8 | 0x91A8E8 | 2D 41 54 45 52 49 41 FF | 7C 64 88 6A FF |
| EQUIP | そうび | 0x5192FC | 0x91A8FC | 25 51 55 49 50 FF | 5D 69 03 FF |
| STATUS | ステータス | 0x519310 | 0x91A910 | 33 54 41 54 55 53 FF | 58 64 D0 5E 58 FF |
| ORDER | たいれつ | 0x519324 | 0x91A924 | 2F 52 44 45 52 FF | 5F 6D 8D 63 FF |
| LIMIT | リミット | 0x519338 | 0x91A938 | 2C 49 4D 49 54 FF | 88 7E 9C 66 FF |
| CONFIG | コンフィグ | 0x51934C | 0x91A94C | 23 4F 4E 46 49 47 FF | 52 98 44 A6 0E FF |
| PHS | ＰＨＳ | 0x519360 | 0x91A960 | 30 28 33 FF | C3 BB C6 FF |
| SAVE | セーブ | 0x519374 | 0x91A974 | 33 41 56 45 FF | 5A D0 04 FF |
| QUIT | しゅうりょう | 0x519388 | 0x91A988 | 31 55 49 54 FF | 57 A1 69 89 A3 69 FF |

---

## Title Screen

| English | Japanese | File Offset | Virtual Address | English Bytes | Japanese Bytes |
|---------|----------|-------------|-----------------|---------------|----------------|
| NEW GAME | ＮＥＷ　ＧＡＭＥ | 0x5245E0 | 0x925BE0 | 2E 25 37 00 27 21 2D 25 FF | C1 B8 CA 3F BA B4 C0 B8 FF |
| CONTINUE | つづきから | 0x5242C8 | 0x9258C8 | 23 4F 4E 54 49 4E 55 45 1F FF | 63 23 4D 4B 87 FF |

**Note:** NEW GAME uses fullwidth English letters in the actual Japanese version.

---

## Save/Load Screen

| English | Japanese | File Offset | Virtual Address | English Bytes | Japanese Bytes |
|---------|----------|-------------|-----------------|---------------|----------------|
| LOAD | ロード | 0x524160 | 0x925760 | 2C 4F 41 44 FF | 8E D0 26 FF |
| LOADING. | ロードちゅう | 0x524238 | 0x925838 | 2C 4F 41 44 49 4E 47 0E FF | 8E D0 26 61 A1 69 FF |
| SELECT A SAVE DATA FILE. | セーブデータをえらんでください | 0x524184 | 0x925784 | (25 bytes) | 5A D0 04 24 D0 5E 9B 6F 87 99 25 37 1F 55 6D FF |
| SELECT A SAVE GAME. | セーブデータをえらぶ | 0x5241A8 | 0x9257A8 | (19 bytes) | 5A D0 04 24 D0 5E 9B 6F 87 05 FF |

### Save Slots

| English | Japanese | File Offset | Virtual Address | Japanese Bytes |
|---------|----------|-------------|-----------------|----------------|
| SAVE 1 | セーブ１ | 0x524B18 | 0x926118 | 5A D0 04 34 FF |
| SAVE 2 | セーブ２ | 0x524B24 | 0x926124 | 5A D0 04 35 FF |
| SAVE 3 | セーブ３ | 0x524B30 | 0x926130 | 5A D0 04 36 FF |
| SAVE 4 | セーブ４ | 0x524B3C | 0x92613C | 5A D0 04 37 FF |
| SAVE 5 | セーブ５ | 0x524B48 | 0x926148 | 5A D0 04 38 FF |
| SAVE 6 | セーブ６ | 0x524B54 | 0x926154 | 5A D0 04 39 FF |
| SAVE 7 | セーブ７ | 0x524B60 | 0x926160 | 5A D0 04 3A FF |
| SAVE 8 | セーブ８ | 0x524B6C | 0x92616C | 5A D0 04 3B FF |
| SAVE 9 | セーブ９ | 0x524B78 | 0x926178 | 5A D0 04 3C FF |
| SAVE 10 | セーブ１０ | 0x524B84 | 0x926184 | 5A D0 04 34 33 FF |

---

## Item Screen

| English | Japanese | File Offset | Virtual Address | Japanese Bytes |
|---------|----------|-------------|-----------------|----------------|
| Use | つかう | 0x51FB68 | 0x921168 | 63 4B 69 FF |
| Arrange | ならべかえ | 0x51FB74 | 0x921174 | 73 87 07 4B 6F FF |
| KEY ITEMS | たいせつなもの | 0x51FB80 | 0x921180 | 5F 6D 5B 63 73 85 7B FF |
| Customize | カスタム | 0x51FB8C | 0x92118C | 4A 58 5E 80 FF |
| Field | フィールド | 0x51FB98 | 0x921198 | 44 A6 D0 8A 26 FF |
| Battle | バトル | 0x51FBA4 | 0x9211A4 | 00 66 8A FF |
| Throw | なげる | 0x51FBB0 | 0x9211B0 | 73 11 8B FF |
| Type | しゅるい | 0x51FBBC | 0x9211BC | 57 A1 8B 6D FF |
| Name | なまえ | 0x51FBC8 | 0x9211C8 | 73 7D 6F FF |
| Most | おおい | 0x51FBD4 | 0x9211D4 | 71 71 6D FF |
| Least | すくない | 0x51FBE0 | 0x9211E0 | 59 4F 73 6D FF |

---

## Equip Screen

### Equipment Type Labels

| English | Japanese | File Offset | Virtual Address | Japanese Bytes |
|---------|----------|-------------|-----------------|----------------|
| Wpn. | ぶき | 0x51F3A8 | 0x9209A8 | 05 4D FF |
| Arm. | ぼうぐ | 0x51F3B4 | 0x9209B4 | 09 69 0F FF |
| Acc. | アクセサリ | 0x51F3C0 | 0x9209C0 | 6A 4E 5A 54 88 FF |

### Combat Stats

| English | Japanese | File Offset | Virtual Address | Japanese Bytes |
|---------|----------|-------------|-----------------|----------------|
| Attack | こうげきりょく | 0x51F420 | 0x920A20 | 53 69 11 4D 89 A3 4F FF |
| Attack% | めいちゅうりつ | 0x51F42C | 0x920A2C | 83 6D 61 A1 69 89 63 FF |
| Defense | ぼうぎょりょく | 0x51F438 | 0x920A38 | 09 69 0D A3 89 A3 4F FF |
| Defense% | かいひりつ | 0x51F444 | 0x920A44 | 4B 6D 43 89 63 FF |
| Magic atk | まほうこうげき | 0x51F450 | 0x920A50 | 7D 49 69 53 69 11 4D FF |
| Magic def | まほうぼうぎょ | 0x51F45C | 0x920A5C | 7D 49 69 09 69 0D A3 FF |
| Magic def% | まほうかいひりつ | 0x51F468 | 0x920A68 | 7D 49 69 4B 6D 43 89 63 FF |

### Materia Growth

| English | Japanese | File Offset | Virtual Address | Japanese Bytes |
|---------|----------|-------------|-----------------|----------------|
| Slot | スロット | 0x51F474 | 0x920A74 | 58 8E 9C 66 FF |
| Growth | せいちょう | 0x51F480 | 0x920A80 | 5B 6D 61 A3 69 FF |
| Nothing | なし | 0x51F48C | 0x920A8C | 73 57 FF |
| Normal | ノーマル | 0x51F498 | 0x920A98 | 7A D0 7C 8A FF |
| Double | ダブル | 0x51F4A4 | 0x920AA4 | 1E 04 8A FF |
| Triple | トリプル | 0x51F4B0 | 0x920AB0 | 66 88 2D 8A FF |

---

## Status Screen

### Base Stats

| English | Japanese | File Offset | Virtual Address | Japanese Bytes |
|---------|----------|-------------|-----------------|----------------|
| Strength | ちから | 0x51F256 | 0x920856 | 61 4B 87 FF |
| Dexterity | すばやさ | 0x51F264 | 0x920864 | 59 01 91 55 FF |
| Vitality | たいりょく | 0x51F274 | 0x920874 | 5F 6D 89 A3 4F FF |
| Magic | まりょく | 0x51F283 | 0x920883 | 7D 89 A3 4F FF |
| Spirit | せいしん | 0x51F292 | 0x920892 | 5B 6D 57 99 FF |
| Luck | うん | 0x51F2A1 | 0x9208A1 | 69 99 FF |
| Limit level | リミットレベル | 0x51F346 | 0x920946 | 88 7E 9C 66 8C 06 8A FF |

### Status Screen Page 2 (TODO)

| English | Japanese | File Offset | Virtual Address | Notes |
|---------|----------|-------------|-----------------|-------|
| Properties | ぞくせい | TBD | TBD | Elemental section header |
| Attack | こうげき | TBD | TBD | Elemental attack |
| Halve | はんげん | TBD | TBD | |
| Nullify | むこう | TBD | TBD | |
| Absorb | きゅうしゅう | TBD | TBD | |
| Added Effect | ついか | TBD | TBD | Status effect section |

---

## Config Screen (ADDRESSES TBD - ANALYSIS COMPLETE)

**Note:** Config screen strings are stored in different locations between English and Japanese exes.
Sub-agent search confirmed Japanese Config region at 0x519400-0x519650.

**Japanese exe Config region findings:**
- キーボード (Keyboard) confirmed at 0x519500
- Other Config strings in 16-byte slots in this region

**Challenge:** English exe Config submenu strings are NOT at the same offsets as Japanese.
The main menu items (CONFIG, LIMIT, QUIT) use shifted ASCII encoding and ARE at known addresses.
But the Config SUBMENU entries (Sound, Cursor, ATB, etc.) are stored elsewhere.

### Menu Labels

| English | Actual Japanese | Byte Sequence | Notes |
|---------|-----------------|---------------|-------|
| Window color | ウィンドウカラー | TBD | |
| Sound | サウンド | 54 69 98 26 FF | |
| Controller | キーボード | 4C D0 08 D0 26 FF | **Different!** Japanese says "Keyboard" |
| Cursor | カーソル | 4A D0 56 8A FF | |
| ATB | ATB | B4 C7 B5 FF | **English retained** - fullwidth ＡＴＢ |
| Battle speed | バトルスピード | 00 66 8A 58 2D D0 26 FF | |
| Battle message | バトルメッセージ | 00 66 8A 82 9C 5A D0 22 FF | |
| Field message | フィールドメッセージ | 44 A6 D0 8A 26 82 9C 5A D0 22 FF | |
| Camera angle | カメラアングル | 4A 82 87 6A 98 0E 8A FF | |
| Magic order | まほうのならびかた | 7D 49 69 7B 73 87 03 4B 5F FF | |

### Option Values

| English | Japanese | Byte Sequence |
|---------|----------|---------------|
| Normal | ノーマル | 7A D0 7C 8A FF |
| Customize | カスタム | 4A 58 5E 80 FF |
| Initial | しょき | 57 A3 4D FF |
| Memory | きおく | 4D 71 4F FF |
| Active | アクティブ | 6A 4E 64 A6 04 FF |
| Recommended | おすすめ | 71 59 59 83 FF |
| Wait | ウェイト | 69 6E 6C 66 FF |
| Fast | はやい | 41 91 6D FF |
| Slow | おそい | 71 5D 6D FF |
| Auto | オート | 70 D0 66 FF |
| Fixed | こてい | 53 64 6D FF |
| NO. 1 | ＮＯ．　１ | C1 C2 B2 3F 34 FF | **English retained** - fullwidth |
| restore | かいふく | 4B 6D 45 4F FF |
| attack | こうげき | 53 69 11 4D FF |
| indirect | かんせつ | 4B 99 5B 63 FF |

### Description Text (Header area)

| Selection | Japanese Description |
|-----------|---------------------|
| Window color | ウィンドウの背景の4スミの色を決める。 |
| Sound | サウンドモードの切り替え。 |
| Controller | ボタンの割り振りを自由に。 |
| Cursor | ウィンドウを閉じても指の位置を記憶するかどうか。 |
| ATB | バトルの時間の進み方の切り替え。 |
| Battle speed | バトルの時間の進むスピードを決める。 |
| Battle message | バトルのメッセージのスピードを決める。 |
| Field message | フィールドのメッセージのスピードを決める。 |
| Camera angle | バトルの画面の動き方を選ぶ。 |
| Magic order | 魔法のならびかたを選ぶ。 |

---

## Magic Screen (TODO)

| English | Japanese | File Offset | Virtual Address | Notes |
|---------|----------|-------------|-----------------|-------|
| (To be researched) | | | | |

---

## Limit Screen (ADDRESSES TBD - ANALYSIS COMPLETE)

**Note:** Limit screen strings are in different offsets between exes. Sub-agents dispatched to find addresses.

### Confirmed from Japanese exe (via sub-agent search)

| English | Actual Japanese | Byte Sequence | JA File Offset | Notes |
|---------|-----------------|---------------|----------------|-------|
| Set | セット | 5A 9C 66 FF | 0x51eb80 | Verified |
| Check | チェック | 60 AA 9C 4E FF | 0x51ebb0 | Verified |
| LEVEL 1-4 | ＬＥＶＥＬ　１-４ | (fullwidth) | N/A | **English retained** |
| Limit level | リミットレベル | 88 7E 9C 66 8C 06 8A FF | N/A | Already patched in main menu |

**Challenge:** The English exe has different structure - these strings are not at the same offsets.
Need to find corresponding English "Set" and "Check" locations.

### Character names and Limit break names
These are stored in kernel2.bin, not hardcoded in the exe. Already handled by Japanese kernel file.

---

## Exit Screen (ADDRESSES TBD - ANALYSIS COMPLETE)

**Note:** Exit screen strings are in different offsets. Sub-agents dispatched to find addresses.

### Confirmed from Japanese exe (via sub-agent search)

| English | Actual Japanese | Byte Sequence | JA File Offset | Notes |
|---------|-----------------|---------------|----------------|-------|
| Yes | はい | 41 6D FF | 0x518fd0 | Verified |
| No | いいえ | 6D 6D 6F FF | 0x518fd4 | Verified |
| (Exit message) | ファイナルファンタジー7のプレイを終了します。よろしいですか？ | (long) | TBD | Multi-line |

**Challenge:** English exe has 0x00 bytes at 0x518fd0 - different structure.
Need to find corresponding English "Yes" and "No" locations.

### Exit Dialog Text
The Japanese exit dialog reads:
- Line 1: ファイナルファンタジー7の (Final Fantasy 7's)
- Line 2: プレイを終了します。 (play will end.)
- Line 3: よろしいですか？ (Is that OK?)

---

## Notes

### Translation Corrections Made

Based on comparison with actual Japanese FF7 executable (`ff7_ja.exe`):

| English | Initial Guess | Correct Japanese | Note |
|---------|--------------|------------------|------|
| ORDER | ならびかえ | たいれつ | Different term used |
| QUIT | やめる | しゅうりょう | More formal term |
| NEW GAME | ニューゲーム | ＮＥＷ　ＧＡＭＥ | Uses fullwidth English |
| Attack | こうげき | こうげきりょく | Has りょく suffix |
| Attack% | めいちゅう | めいちゅうりつ | Has りつ suffix |
| Defense | ぼうぎょ | ぼうぎょりょく | Has りょく suffix |
| Defense% | かいひ | かいひりつ | Has りつ suffix |
| Magic def% | まほうかいひ | まほうかいひりつ | Has りつ suffix |

### Addresses Yet to Find

**High Priority (Japanese exe offsets confirmed, need English equivalents):**
- Limit screen "Set" and "Check" - JA at 0x51eb80, 0x51ebb0
- Exit screen "Yes" and "No" - JA at 0x518fd0, 0x518fd4
- Config submenu entries - JA region 0x519400-0x519650

**Medium Priority:**
- Status screen pages 2-3 (elemental/status)
- Magic screen labels
- Config screen descriptions (header text that changes per selection)

**Low Priority / May Not Need HEXT:**
- Exit dialog full message (may be in flevel/kernel)
- Various popup messages

### Search Strategy for Remaining Strings

The English and Japanese exes have **different string layouts**. The Japanese exe stores
Config/Limit/Exit strings in a contiguous block, but the English exe does not.

**Approach:**
1. Search English exe for shifted ASCII patterns of "Set", "Check", "Yes", "No"
2. Look in regions beyond 0x519000-0x525000 (may be elsewhere)
3. Consider that some strings may be in external files (kernel2.bin, menu data)

---

## Searching for New Addresses

### Command to find English string

```bash
# Convert English to FF7 encoding mentally, then:
xxd "/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe" | grep "PATTERN"
```

### Command to find Japanese equivalent

```bash
xxd "/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_ja.exe" | grep "PATTERN"
```

### Python helper for address calculation

```python
def file_to_va(file_offset):
    return (file_offset - 0x3B8A00) + 0x3BA000 + 0x400000

# Example
print(f"0x{file_to_va(0x51934c):X}")  # Output: 0x91A94C
```

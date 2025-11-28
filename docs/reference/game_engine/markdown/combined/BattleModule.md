# FF7 Battle Module

**Category: Battle System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's battle system, including mechanics, battle fields, scenes, scripts, and animations.

---

# FF7/Battle/Battle Mechanics {#ff7battlebattle_mechanics}

- [FF7/Battle/Battle Mechanics](#ff7battlebattle_mechanics){#toc-ff7battlebattle_mechanics}
  - [Command Defaults](#command_defaults){#toc-command_defaults}
  - [Queued Actions](#queued_actions){#toc-queued_actions}
  - [AI Structure](#ai_structure){#toc-ai_structure}
  - [Active Character Data](#active_character_data){#toc-active_character_data}
  - [Actor Battle Data](#actor_battle_data){#toc-actor_battle_data}



This page will be for Battle memory structures. This is consistent with the memory structure of the PC version. PSX may or may not reflect these structures.

## Command Defaults {#command_defaults}

Each command type has default execution values that can, in some cases, be overridden. These come from a hard-coded structure in the executable.

| Offset | Default            |
|--------|--------------------|
| 0h     | Animation          |
| 1h     | Damage Calculation |
| 2h     | Command Properties |

## Queued Actions {#queued_actions}

When a command is selected either by a player character or an enemy the action is inserted into a priority queue. Up to 64 actions can be queued. On each update loop, the main Queue function will pop off the next action with the lowest priority and execute it in FIFO order within priority bands.

Queue entries have the following structure in memory:

| Offset | Value |
|----|----|
| 0 | Action Priority (limits/counters 0, player chosen spells 6) |
| 1 | Queue position within priority band |
| 2 | Attacker actor ID |
| 3 | Action command index (e.g CMD_MAGIC = 0x02) |
| 4 | Action attack index (e.g Bolt = 0x21). (This index is absolute, not command relative) |
| 6 | Action target mask |

## AI Structure {#ai_structure}

There is a single block of memory that holds AI information on the current running script. Each Actor \"owns\" this while their scripts are executing.

| Offset     | Function                                  |
|------------|-------------------------------------------|
| 0h         | Actor Index                               |
| 4h         | Script Position                           |
| 8h         | Remaining Stack Space (initially 200h)    |
| 0Ch        | Current AI OpCode                         |
| 10h        | OpCode Lower Nybble                       |
| 14h        | OpCode Upper Nybble                       |
| 18h        | First Group Type                          |
| 1Ch        | Second Group Type                         |
| 20h        | OpCode Lower Nybble (related to group 1?) |
| 24h        | OpCode Lower Nybble (related to group 2?) |
| 28h        | Mask of *non-null* values in Group 1      |
| 2Ah        | Mask of *non-null* values in Group 2      |
| 2Ch - 50h  | Group 1 of variables                      |
| 54h - 78h  | Group 2 of variables                      |
| 7Ch - 27Ch | Stack of values                           |

## Active Character Data {#active_character_data}

This is an array that each playable character maintains an instance of.

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th colspan="2" style="background: rgb(104,104,104)"><p>Value</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>000h</p></td>
<td colspan="2"><p>Character ID</p></td>
</tr>
<tr>
<td><p>001h</p></td>
<td colspan="2"><p>Cover Chance</p></td>
</tr>
<tr>
<td><p>002h</p></td>
<td colspan="2"><p>Strength</p></td>
</tr>
<tr>
<td><p>003h</p></td>
<td colspan="2"><p>Vitality</p></td>
</tr>
<tr>
<td><p>004h</p></td>
<td colspan="2"><p>Magic</p></td>
</tr>
<tr>
<td><p>005h</p></td>
<td colspan="2"><p>Spirit</p></td>
</tr>
<tr>
<td><p>006h</p></td>
<td colspan="2"><p>Speed</p></td>
</tr>
<tr>
<td><p>007h</p></td>
<td colspan="2"><p>Luck</p></td>
</tr>
<tr>
<td><p>008h</p></td>
<td colspan="2"><p>Phys Attack</p></td>
</tr>
<tr>
<td><p>00Ah</p></td>
<td colspan="2"><p>Phys Def</p></td>
</tr>
<tr>
<td><p>00Ch</p></td>
<td colspan="2"><p>Mag Attack</p></td>
</tr>
<tr>
<td><p>00Eh</p></td>
<td colspan="2"><p>Mag Def</p></td>
</tr>
<tr>
<td><p>010h</p></td>
<td colspan="2"><p>Current HP</p></td>
</tr>
<tr>
<td><p>012h</p></td>
<td colspan="2"><p>Max HP</p></td>
</tr>
<tr>
<td><p>014h</p></td>
<td colspan="2"><p>Current MP</p></td>
</tr>
<tr>
<td><p>016h</p></td>
<td colspan="2"><p>Max MP</p></td>
</tr>
<tr>
<td><p>018h</p></td>
<td colspan="2"><p>Timer</p></td>
</tr>
<tr>
<td><p>01Ch</p></td>
<td colspan="2"><p>Counter Attack Action Index</p></td>
</tr>
<tr>
<td><p>01Eh</p></td>
<td colspan="2"><p>Counter Attack Chance</p></td>
</tr>
<tr>
<td><p>021h</p></td>
<td colspan="2"><p>Some sort of divisor?</p></td>
</tr>
<tr>
<td><p>023h</p></td>
<td colspan="2"><p>Character Flags (Underwater, Long Range, HP&lt;-&gt;MP, etc)</p></td>
</tr>
<tr>
<td><p>024h</p></td>
<td colspan="2"><p>Eight entries of three bytes...</p></td>
</tr>
<tr>
<td><p>03Ch</p></td>
<td colspan="2"><p>Attacking Elements</p></td>
</tr>
<tr>
<td><p>03Eh</p></td>
<td colspan="2"><p>Halved Elements</p></td>
</tr>
<tr>
<td><p>040h</p></td>
<td colspan="2"><p>Nullified Elements</p></td>
</tr>
<tr>
<td><p>042h</p></td>
<td colspan="2"><p>Absorbed Elements</p></td>
</tr>
<tr>
<td><p>044h</p></td>
<td colspan="2"><p>Attacking Elements</p></td>
</tr>
<tr>
<td><p>048h</p></td>
<td colspan="2"><p>Immune Statuses</p></td>
</tr>
<tr>
<td><p>04Ch</p></td>
<td colspan="2"><p>Enabled Command Menu (16 entries of 6 bytes)</p></td>
</tr>
<tr>
<td><p>0ACh</p></td>
<td colspan="2"><p>Limit Actions for current Limit Level</p></td>
</tr>
<tr>
<td><p>0B4h</p></td>
<td colspan="2"><p>Enabled Limit Data (three entries in Attack Data format(0x1C))</p></td>
</tr>
<tr>
<td><p>108h</p></td>
<td colspan="2"><p>Enabled Magics (54 entries of 8 bytes)</p></td>
</tr>
<tr>
<td rowspan="7" style="background: rgb(104,104,155)"></td>
<td><p>0</p></td>
<td><p>Magic Index</p></td>
</tr>
<tr>
<td><p>1h</p></td>
<td><p>MP Cost</p></td>
</tr>
<tr>
<td><p>2h</p></td>
<td><p>All Count</p></td>
</tr>
<tr>
<td><p>3h</p></td>
<td><p>Quad Enabled?</p></td>
</tr>
<tr>
<td><p>4h</p></td>
<td><p>Quad Count?</p></td>
</tr>
<tr>
<td><p>5h</p></td>
<td><p>Target Data</p></td>
</tr>
<tr>
<td><p>6h</p></td>
<td><p>Properties</p></td>
</tr>
<tr>
<td><p>2C8h</p></td>
<td colspan="2"><p>Enabled Summons (format like above)</p></td>
</tr>
<tr>
<td><p>348h</p></td>
<td colspan="2"><p>Enabled ESkills (format like above)</p></td>
</tr>
<tr>
<td><p>408h</p></td>
<td colspan="2"><p>First 11 bytes of Weapon Data</p></td>
</tr>
<tr>
<td><p>40Dh</p></td>
<td colspan="2"><p>Status of weapon added to Attacking Statuses above</p></td>
</tr>
<tr>
<td><p>410h</p></td>
<td colspan="2"><p>Weapon's Accuracy</p></td>
</tr>
<tr>
<td><p>418h</p></td>
<td colspan="2"><p>Additional Attack Elements</p></td>
</tr>
<tr>
<td><p>41Ch</p></td>
<td colspan="2"><p>Four sets of two DWords : (Stat to increase, Increase value)</p></td>
</tr>
<tr>
<td><p>43Ch</p></td>
<td colspan="2"><p>Gil Bonus granted by this character</p></td>
</tr>
<tr>
<td><p>43Dh</p></td>
<td colspan="2"><p>Encounter rate ""</p></td>
</tr>
<tr>
<td><p>43Eh</p></td>
<td colspan="2"><p>Chocobo Chance ""</p></td>
</tr>
<tr>
<td><p>43Fh</p></td>
<td colspan="2"><p>PreEmptive Chance ""</p></td>
</tr>
</tbody>
</table>

## Actor Battle Data {#actor_battle_data}

Similar to Active Character Data, but more detailed. This data is dependent on who is performing the current action and only one instance of it exists during each action and all stats are relative to the performing actor and current action unless otherwise noted. Addresses 200h and above will change for each target of the action.

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th colspan="2" style="background: rgb(104,104,104)"><p>Value</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0h</p></td>
<td colspan="2"><p>Index</p></td>
</tr>
<tr>
<td><p>4h</p></td>
<td colspan="2"><p>Level</p></td>
</tr>
<tr>
<td><p>8h</p></td>
<td colspan="2"><p>Formation Entry (Enemy A, Enemy B, etc)</p></td>
</tr>
<tr>
<td><p>0Ch</p></td>
<td colspan="2"><p>Command Index</p></td>
</tr>
<tr>
<td><p>10h</p></td>
<td colspan="2"><p>Action Index</p></td>
</tr>
<tr>
<td><p>14h</p></td>
<td colspan="2"><p>Action Animation Base (for relative to absolute animation indexes)</p></td>
</tr>
<tr>
<td><p>18h</p></td>
<td colspan="2"><p>Allowed Targets (Active and targetable)</p></td>
</tr>
<tr>
<td><p>1Ch</p></td>
<td colspan="2"><p>Active Allies?</p></td>
</tr>
<tr>
<td><p>20h</p></td>
<td colspan="2"><p>Command Animation (player characters only)</p></td>
</tr>
<tr>
<td><p>24h</p></td>
<td colspan="2"><p><a href="FF7/Battle/Attack_Effect_Id_List" class="wikilink" title="Attack Effect">Attack Effect</a></p></td>
</tr>
<tr>
<td><p>28h</p></td>
<td colspan="2"><p>Command Index (again)</p></td>
</tr>
<tr>
<td><p>2Ch</p></td>
<td colspan="2"><p>Action Index (again)</p></td>
</tr>
<tr>
<td><p>30h</p></td>
<td colspan="2"><p>Self Mask</p></td>
</tr>
<tr>
<td><p>38h</p></td>
<td colspan="2"><p>MP Cost</p></td>
</tr>
<tr>
<td><p>3Ch</p></td>
<td colspan="2"><p>Action Accuracy</p></td>
</tr>
<tr>
<td><p>40h</p></td>
<td colspan="2"><p><a href="FF7/Battle/Damage_Calculation" class="wikilink" title="Damage Calculation">Damage Calculation</a></p></td>
</tr>
<tr>
<td><p>44h</p></td>
<td colspan="2"><p><a href="FF7/Battle/Elemental_Data" class="wikilink" title="Action&#39;s Element">Action's Element</a></p></td>
</tr>
<tr>
<td><p>48h</p></td>
<td colspan="2"><p>Action's Power</p></td>
</tr>
<tr>
<td><p>4Ch</p></td>
<td colspan="2"><p>Phys/Mag Attack Power</p></td>
</tr>
<tr>
<td><p>50h</p></td>
<td colspan="2"><p>Action's Target(s) Mask</p></td>
</tr>
<tr>
<td><p>54h</p></td>
<td colspan="2"><p>Normal Impact Sound</p></td>
</tr>
<tr>
<td><p>58h</p></td>
<td colspan="2"><p>Critical Impact Sound</p></td>
</tr>
<tr>
<td><p>5Ch</p></td>
<td colspan="2"><p>Miss Sound</p></td>
</tr>
<tr>
<td><p>60h</p></td>
<td colspan="2"><p>Single Target Camera</p></td>
</tr>
<tr>
<td><p>64h</p></td>
<td colspan="2"><p>Multi Target Camera</p></td>
</tr>
<tr>
<td><p>68h</p></td>
<td colspan="2"><p>Action Reaction Animation Index</p></td>
</tr>
<tr>
<td><p>6Ch</p></td>
<td colspan="2"><p><a href="FF7/Battle/Attack_Special_Effects" class="wikilink" title="Attack Special Effects">Attack Special Effects</a></p></td>
</tr>
<tr>
<td><p>78h</p></td>
<td colspan="2"><p>Non-self target mask?</p></td>
</tr>
<tr>
<td><p>80h</p></td>
<td colspan="2"><p><a href="FF7/Battle/Status_Effects" class="wikilink" title="Inflicting Status(es)">Inflicting Status(es)</a></p></td>
</tr>
<tr>
<td><p>84h</p></td>
<td colspan="2"><p><a href="FF7/Battle/Status_Effects" class="wikilink" title="Curing Status(es)">Curing Status(es)</a></p></td>
</tr>
<tr>
<td><p>88h</p></td>
<td colspan="2"><p><a href="FF7/Battle/Status_Effects" class="wikilink" title="Toggling Status(es)">Toggling Status(es)</a></p></td>
</tr>
<tr>
<td><p>8Ch</p></td>
<td colspan="2"><p>Chance to inflict Status</p></td>
</tr>
<tr>
<td><p>90h</p></td>
<td colspan="2"><p>Command Properties (details pending)</p></td>
</tr>
<tr>
<td><p>94h</p></td>
<td colspan="2"><p>Target Mask</p></td>
</tr>
<tr>
<td><p>98h</p></td>
<td colspan="2"><p>Attack Index position in scene data (enemy only)</p></td>
</tr>
<tr>
<td><p>A0h</p></td>
<td colspan="2"><p>Action Accuracy function (upper nybble of <a href="FF7/Battle/Damage_Calculation" class="wikilink" title="Damage Calculation">Damage Calculation</a>)</p></td>
</tr>
<tr>
<td><p>A4h</p></td>
<td colspan="2"><p>Action Damage function (lower nybble of <a href="FF7/Battle/Damage_Calculation" class="wikilink" title="Damage Calculation">Damage Calculation</a>)</p></td>
</tr>
<tr>
<td><p>ACh</p></td>
<td colspan="2"><p>Quad Magic Count?</p></td>
</tr>
<tr>
<td><p>B0h</p></td>
<td colspan="2"><p>Number of attack damage calculations?</p></td>
</tr>
<tr>
<td><p>B4h</p></td>
<td colspan="2"><p>Follow-up action count (Tifa's Limits, Finishing Touch, etc)</p></td>
</tr>
<tr>
<td><p>B8h</p></td>
<td colspan="2"><p>Number of Targets?</p></td>
</tr>
<tr>
<td><p>BCh</p></td>
<td colspan="2"><p><a href="FF7/Battle/Attack_Special_Effects" class="wikilink" title="Attack Additional Effects">Attack Additional Effects</a></p></td>
</tr>
<tr>
<td><p>C0h</p></td>
<td colspan="2"><p>Additional Effect Modifier</p></td>
</tr>
<tr>
<td><p>C4h</p></td>
<td colspan="2"><p>Attack Power</p></td>
</tr>
<tr>
<td><p>C8h</p></td>
<td colspan="2"><p>Actor's current status</p></td>
</tr>
<tr>
<td><p>D0h - D7h</p></td>
<td colspan="2"><p>Follow-up Action(s)</p></td>
</tr>
<tr>
<td><p>D8h</p></td>
<td colspan="2"><p>Actor's Strength</p></td>
</tr>
<tr>
<td><p>DCh</p></td>
<td colspan="2"><p>Used during String display?</p></td>
</tr>
<tr>
<td><p>E0h</p></td>
<td colspan="2"><p>Number of successful hits</p></td>
</tr>
<tr>
<td><p>F0h</p></td>
<td colspan="2"><p>Character-specific action properties (mp absorb, hp absorb, etc)</p></td>
</tr>
<tr>
<td><p>F8h</p></td>
<td colspan="2"><p>Related to enabled magic. Also ACh above.</p></td>
</tr>
<tr>
<td><p>FCh</p></td>
<td colspan="2"><p>Multiple hit count</p></td>
</tr>
<tr>
<td><p>100h - 1FFh</p></td>
<td colspan="2"><p>large unused gap</p></td>
</tr>
<tr>
<td><p>200h</p></td>
<td colspan="2"><p>???</p></td>
</tr>
<tr>
<td><p>204h</p></td>
<td colspan="2"><p>Character Map (players only)</p></td>
</tr>
<tr>
<td><p>208h</p></td>
<td colspan="2"><p>Current Target Index</p></td>
</tr>
<tr>
<td><p>20Ch</p></td>
<td colspan="2"><p>Formation Slot</p></td>
</tr>
<tr>
<td><p>210h</p></td>
<td colspan="2"><p>Target's Phys/Mag Def (whichever attack type is)</p></td>
</tr>
<tr>
<td><p>214h</p></td>
<td colspan="2"><p>Damage done to target</p></td>
</tr>
<tr>
<td><p>218h</p></td>
<td colspan="2"><p>Properties of attack</p></td>
</tr>
<tr>
<td rowspan="8" style="background: rgb(104,104,155)"></td>
<td><p>1</p></td>
<td><p>missed</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>Physical if set; Magical if unset</p></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>Attempt Steal</p></td>
</tr>
<tr>
<td><p>20</p></td>
<td><p>Won't Miss</p></td>
</tr>
<tr>
<td><p>4000</p></td>
<td><p>Physical Barrier</p></td>
</tr>
<tr>
<td><p>8000</p></td>
<td><p>Magical Barrier</p></td>
</tr>
<tr>
<td><p>40000</p></td>
<td><p>???</p></td>
</tr>
<tr>
<td><p>800000</p></td>
<td><p>???</p></td>
</tr>
<tr>
<td><p>220h</p></td>
<td colspan="2"><p>More properties (heal, critical, damage MP, etc)</p></td>
</tr>
<tr>
<td><p>224h</p></td>
<td colspan="2"><p>Target's reaction animation</p></td>
</tr>
<tr>
<td><p>228h</p></td>
<td colspan="2"><p>Target's status</p></td>
</tr>
<tr>
<td><p>22Ch</p></td>
<td colspan="2"><p>Target's status immunities</p></td>
</tr>
<tr>
<td><p>230h</p></td>
<td colspan="2"><p>Damage level to current Action</p></td>
</tr>
<tr>
<td rowspan="8" style="background: rgb(104,104,155)"></td>
<td><p>1</p></td>
<td><p>Death (if not immune)</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>Always hit?</p></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>Double (Damage &amp; Accuracy)</p></td>
</tr>
<tr>
<td><p>8</p></td>
<td><p>Normal (Never checked)</p></td>
</tr>
<tr>
<td><p>10</p></td>
<td><p>Half (Damage &amp; Accuracy)</p></td>
</tr>
<tr>
<td><p>20</p></td>
<td><p>Null (won't miss?)</p></td>
</tr>
<tr>
<td><p>40</p></td>
<td><p>Absorb (won't miss?)</p></td>
</tr>
<tr>
<td><p>80</p></td>
<td><p>Full-Heal</p></td>
</tr>
<tr>
<td><p>234h</p></td>
<td colspan="2"><p>Target condition flags (back exposed, multiple targets, etc)</p></td>
</tr>
<tr>
<td><p>238h</p></td>
<td colspan="2"><p>Status(es) to add to Target</p></td>
</tr>
<tr>
<td><p>23Ch</p></td>
<td colspan="2"><p>Status(es) to Cure from Target</p></td>
</tr>
<tr>
<td><p>240h</p></td>
<td colspan="2"><p>Status(es) to Toggle from Target</p></td>
</tr>
<tr>
<td><p>244h</p></td>
<td colspan="2"><p>All Target's statuses that will be affected from action</p></td>
</tr>
<tr>
<td><p>248h</p></td>
<td colspan="2"><p>Sound to play (determined from hit/critical/miss sounds above)</p></td>
</tr>
<tr>
<td><p>24Ch</p></td>
<td colspan="2"><p>Action Animation to use (varies from single/multiple targets)</p></td>
</tr>
<tr>
<td><p>254h</p></td>
<td colspan="2"><p>Target's Level</p></td>
</tr>
<tr>
<td><p>258h</p></td>
<td colspan="2"><p>Target's HP</p></td>
</tr>
<tr>
<td><p>25Ch</p></td>
<td colspan="2"><p>Target's MP</p></td>
</tr>
<tr>
<td><p>260h</p></td>
<td colspan="2"><p>Action's final Accuracy</p></td>
</tr>
</tbody>
</table>

---

# FF7/Battle/Battle Field {#ff7battlebattle_field}

- [FF7/Battle/Battle Field](#ff7battlebattle_field){#toc-ff7battlebattle_field}
  - [Settings (first file)](#settings_first_file){#toc-settings_first_file}



Battle fields are simple 3d models drawed in 3d space.

They stored in directories STAGE1 and STAGE2. There are lzs archives that unpacked and loaded in PSX space 0x801590e4. Size of unpacked field must be less than 0x8d04. It consist from few concatenated files. First one is settings for field. Last one is texture. All others are meshes.

### Settings (first file) {#settings_first_file}

<table>
<thead>
<tr>
<th style="text-align: center; background: rgb(104,104,104);"><p>Offset</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Size</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Value</p></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;"><p>0</p></td>
<td style="text-align: center;"><p>1 byte</p></td>
<td style="text-align: center;"><p>Type of 3d mesh. There are 6 type of meshes:<br />
0 - mesh with horisontal scrolling parts (field 47 - Corel Train Battle).<br />
1 - normal static mesh.<br />
2 - mesh with vertical scrolling parts (field 12 - Shinra Elevators).<br />
3 - mesh with lifestream (field 4e - Final Battle - Sephiroth).<br />
4 - mesh with rotating parts (field 39 - Safer Battle)<br />
5 - normal static mesh, same as 1. (field 01,44,45 - Bizarro Battles)</p></td>
</tr>
<tr>
<td style="text-align: center; background: rgb(155,155,104);"><p>1</p></td>
<td style="text-align: center; background: rgb(155,155,104);"><p>7 bytes</p></td>
<td style="text-align: center; background: rgb(155,155,104);"><p>unknown</p></td>
</tr>
</tbody>
</table>

---

# FF7/Battle/Battle Scenes {#ff7battlebattle_scenes}

- [FF7/Battle/Battle Scenes](#ff7battlebattle_scenes){#toc-ff7battlebattle_scenes}
  - [Introduction](#introduction){#toc-introduction}
  - [Scene.Bin file format](#scene.bin_file_format){#toc-scene.bin_file_format}


## Introduction

FF7 keeps each enemy battle configuration is a file called \"scene.bin\" This file is located in the following directories.

|      PSX Version       |    PC Version     |
|:----------------------:|:-----------------:|
| /DATA/BATTLE/SCENE.BIN | /BATTLE/SCENE.BIN |

This file is exactly the same in both versions. This holds all the battle configurations for all enemies encountered in the game.

## Scene.Bin file format {#scene.bin_file_format}

### Overview

The scene.bin file contains 256 gziped files which give us information for all the FF7 monsters. In order to find these files in scene.bin, you have to know that the file is structured with blocks exactly 0x2000 bytes in length. In the first table (scene.bin block), you will see what contains a block. Blocks are concatenated with each other to form the scene.bin file. So if you want to extract data from scene.bin, you\'ll need to find the correct blocks and to extract the gziped files from it. After that you simply ungzip those files and you\'ll find 256 files, with a length is 7808 bytes. Known information about those files can be found in the second table (The Data File specification). Because extracting file manually would be a pain, several tools was developed in order to help you. You can use [Scene Reader](http://spinningcone.com/ff/stormmedia/projects/SceneReader.zip) for example, it\'s a win32 tool to extract and repack scene.bin archive.

Also note, that in [kernel.bin](FF7/Kernel/Kernel.bin "kernel.bin"){.wikilink} there is a look-up table for scene.bin, which tells how many files there are in each section of scene.bin. You need to update it every time you repack the file and something changes. The table is at offset 0x0F1C of the third section of the kernel.bin file. You can use [SceneFix](http://forums.qhimm.com/index.php?topic=7127.0) program, which\'ll update the table for you.

We have 1024 possible battle numbers: 0 - 1023. Each group of \*4\* Battle Numbers refers to a particular Scene file: for instance, Battles 0-3 refer to File 0 in Scene.bin, Battles 4-7 refer to File 1 in Scene.bin, and so forth.

\

#### Japanese format {#japanese_format}

In the japanese scene.bin, ennemies names and attacks names have a size of 16 bytes, instead of 32 bytes.

\

### General file format {#general_file_format}

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x0000</p></td>
<td><p>4 bytes</p></td>
<td><p>Pointer to first data file. You must multiply it by 4 to get actual data file offset. If the pointer is equal to FFFFFFFFh then it means that the end of block has been reached.</p></td>
</tr>
<tr>
<td><p>0x0004</p></td>
<td><p>4 bytes</p></td>
<td><p>Pointer to second data file. You must multiply it by 4 to get actual data file offset. If the pointer is equal to FFFFFFFFh then it means that the end of block has been reached.</p></td>
</tr>
<tr>
<td colspan="3" style="text-align: center;"><p>...</p></td>
</tr>
<tr>
<td><p>0x003C</p></td>
<td><p>4 bytes</p></td>
<td><p>Last pointer, usually it equal FFFFFFFFh.</p></td>
</tr>
<tr>
<td><p>0x0040</p></td>
<td><p>4 * (pointer2 - pointer1) bytes</p></td>
<td><p>First data file in block. It's a gziped file.<br />
<em>Note: Sometimes it may finish by 0xFF bytes, because its size must be multiple of 4.</em></p></td>
</tr>
<tr>
<td><p>pointer2 * 4</p></td>
<td><p>4 * (pointer3 - pointer2) bytes</p></td>
<td><p>Second data file in block. It's a gziped file.<br />
<em>Note: Sometimes it may finish by 0xFF bytes, because its size must be multiple of 4.</em></p></td>
</tr>
<tr>
<td colspan="3" style="text-align: center;"><p>...</p></td>
</tr>
<tr>
<td><p>lastpointer * 4</p></td>
<td><p>4 * (2000h - lastpointer) bytes</p></td>
<td><p>Last data file in block.<br />
<em>Note: There are about 6 to 12 files in each block. Each block finishes by 0xFF bytes, because its length must be 2000h (8192d) bytes.</em></p></td>
</tr>
</tbody>
</table>

### Data file format {#data_file_format}

| Offset | Length | Description |
|----|----|----|
| 0x0000 | 2 bytes | Enemy ID 1 |
| 0x0002 | 2 bytes | Enemy ID 2 |
| 0x0004 | 2 bytes | Enemy ID 3 |
| 0x0006 | 2 bytes | Padding (always FFFFh) |
| 0x0008 | 4 \* 20 bytes | Battle Setup (4 records) ([format explanation](#Battle_Setup_1_format "format explanation"){.wikilink}) |
| 0x0058 | 4 \* 48 bytes | Camera Placement Data (4 records) ([format explanation](#Camera_Placement_Data_format "format explanation"){.wikilink}) |
| 0x0118 | 6 \* 16 bytes | Battle Formation 1 (6 records) ([format explanation](#Battle_Formation_Data "format explanation"){.wikilink}) |
| 0x0178 | 6 \* 16 bytes | Battle Formation 2 (6 records) |
| 0x01E8 | 6 \* 16 bytes | Battle Formation 3 (6 records) |
| 0x0238 | 6 \* 16 bytes | Battle Formation 4 (6 records) |
| 0x0298 | 184 bytes | Enemy Data 1 ([format explanation](#Enemy_data_format "format explanation"){.wikilink}) |
| 0x0350 | 184 bytes | Enemy Data 2 |
| 0x0408 | 184 bytes | Enemy Data 3 |
| 0x04C0 | 32 \* 28 bytes | Attack Data (32 records) ([format explanation](FF7/Attack_data "format explanation"){.wikilink}) |
| 0x0840 | 32 \* 2 bytes | Attack IDs (32 records) |
| 0x0880 | 32 \* 32 bytes | Attack Names (32 records, [in FF Text format](FF7/FF_Text "in FF Text format"){.wikilink}) |
| 0x0C80 | 2 bytes | Formation 1 AI Script Offset |
| 0x0C82 | 2 bytes | Formation 2 AI Script Offset |
| 0x0C84 | 2 bytes | Formation 3 AI Script Offset |
| 0x0C86 | 2 bytes | Formation 4 AI Script Offset |
| 0x0C88 | 0 - 504 bytes | Beginning of Formation AI Data ([format explanation](#AI_Data "format explanation"){.wikilink}) |
| 0x0E80 | 2 bytes | Enemy 1 AI Offset |
| 0x0E82 | 2 bytes | Enemy 2 AI Offset |
| 0x0E84 | 2 bytes | Enemy 3 AI Offset |
| 0x0E86 | 0 - 4090 bytes | Beginning of AI Data ([format explanation](#AI_Data "format explanation"){.wikilink}) |

\

#### Battle Setup 1 format {#battle_setup_1_format}

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x0000</p></td>
<td><p>2 bytes</p></td>
<td><p><strong>Battle location, as follows:</strong></p></td>
</tr>
<tr>
<td colspan="2" rowspan="2" style="text-align: center; background: rgb(104,104,155);"></td>
<td></td>
</tr>
<tr>
<td><p>0000h : Blank<br />
0001h : Bizarro Battle - Center<br />
0002h : Grassland<br />
0003h : Mt Nibel<br />
0004h : Forest<br />
0005h : Beach<br />
0006h : Desert<br />
0007h : Snow<br />
0008h : Swamp<br />
0009h : Sector 1 Train Station<br />
000Ah : Reactor 1<br />
000Bh : Reactor 1 Core<br />
000Ch : Reactor 1 Entrance<br />
000Dh : Sector 4 Subway<br />
000Eh : Nibel Caves or AForest Caves<br />
000Fh : Shinra HQ<br />
0010h : Midgar Raid Subway<br />
0011h : Hojo's Lab<br />
0012h : Shinra Elevators<br />
0013h : Shinra Roof<br />
0014h : Midgar Highway<br />
0015h : Wutai Pagoda<br />
0016h : Church<br />
0017h : Coral Valley<br />
0018h : Midgar Slums<br />
0019h : Sector 4 Corridors or Junon Path<br />
001Ah : Sector 4 Gantries or Midgar Underground<br />
001Bh : Sector 7 Support Pillar Stairway<br />
001Ch : Sector 7 Support Pillar Top<br />
001Dh : Sector 8<br />
001Eh : Sewers<br />
001Fh : Mythril Mines<br />
0020h : Northern Crater - Floating Platforms<br />
0021h : Corel Mountain Path<br />
0022h : Junon Beach<br />
0023h : Junon Cargo Ship<br />
0024h : Corel Prison<br />
0025h : Battle Square<br />
0026h : Da Chao - Rapps Battle<br />
0027h : Cid's Backyard<br />
0028h : Final Descent to Sephiroth<br />
0029h : Reactor 5 Entrance<br />
002Ah : Temple of the Ancients - Escher Room<br />
002Bh : Shinra Mansion<br />
002Ch : Junon Airship Dock<br />
002Dh : Whirlwind Maze<br />
002Eh : Junon Underwater Reactor<br />
002Fh : Gongaga Reactor<br />
0030h : Gelnika<br />
0031h : Train Graveyard<br />
0032h : Great Glacier Ice Caves &amp; Gaea Cliffs - Inside<br />
0033h : Sister Ray<br />
0034h : Sister Ray Base<br />
0035h : Forgotten City Altar<br />
0036h : Northern Crater - Initial Descent<br />
0037h : Northern Crater - Hatchery<br />
0038h : Northern Crater - Water Area<br />
0039h : Safer Battle<br />
003Ah : Kalm Flashback - Dragon Battle<br />
003Bh : Junon Underwater Pipe<br />
003Ch : Blank<br />
003Dh : Corel Railway - Canyon<br />
003Eh : Whirlwind Maze - Crater<br />
003Fh : Corel Railway - Rollercoaster<br />
0040h : Wooden Bridge<br />
0041h : Da Chao<br />
0042h : Fort Condor<br />
0043h : Dirt Wasteland<br />
0044h : Bizarro Battle - Right Side<br />
0045h : Bizarro Battle - Left Side<br />
0046h : Jenova*SYNTHESIS Battle<br />
0047h : Corel Train Battle<br />
0048h : Cosmo Canyon<br />
0049h : Caverns of the Gi<br />
004Ah : Nibelheim Mansion Basement<br />
004Bh : Temple of the Ancients - Demons Gate<br />
004Ch : Temple of the Ancients - Mural Room<br />
004Dh : Temple of the Ancients - Clock Passage<br />
004Eh : Final Battle - Sephiroth<br />
004Fh : Jungle<br />
0050h : Ultimate Weapon - Battle on Highwind<br />
0051h : Corel Reactor<br />
0052h : Unused<br />
0053h : Don Corneo's Mansion<br />
0054h : Emerald Weapon Battle<br />
0055h : Reactor 5<br />
0056h : Shinra HQ - Escape<br />
0057h : Ultimate Weapon - Gongaga Reactor<br />
0058h : Corel Prison - Dyne Battle<br />
0059h : Ultimate Weapon - Forest</p></td>
</tr>
<tr>
<td><p>0x0002</p></td>
<td><p>2 bytes</p></td>
<td><p>Upon defeat of all opponents in current formation, begin battle with <a href="FF7/Battle/Battle_scenes#Formation_ID" class="wikilink" title="Formation ID">Formation ID</a> without ending battle scene</p></td>
</tr>
<tr>
<td><p>0x0004</p></td>
<td><p>2 bytes</p></td>
<td><p>Escape Counter</p></td>
</tr>
<tr>
<td><p>0x0006</p></td>
<td><p>2 bytes</p></td>
<td><p>Unused/Align 'FF'</p></td>
</tr>
<tr>
<td><p>0x0008</p></td>
<td><p>4 * 2 bytes</p></td>
<td><p><a href="FF7/Battle/Battle_scenes#Formation_ID" class="wikilink" title="Formation ID">Formation ID</a> of candidates for next Battle Arena battle. (default of 03E7h)</p></td>
</tr>
<tr>
<td><p>0x0010</p></td>
<td><p>2 bytes</p></td>
<td><p>Escapable Flag (Along with other flags)</p></td>
</tr>
<tr>
<td><p>0x0012</p></td>
<td><p>1 byte</p></td>
<td><p>Battle layout type (normal, ambush, side). 0-8 types.</p></td>
</tr>
<tr>
<td colspan="2" rowspan="10" style="text-align: center; background: rgb(104,104,155);"></td>
<td></td>
</tr>
<tr>
<td><p>00 - Normal fight</p></td>
</tr>
<tr>
<td><p>01 - Preemptive</p></td>
</tr>
<tr>
<td><p>02 - Back attack</p></td>
</tr>
<tr>
<td><p>03 - Side attack</p></td>
</tr>
<tr>
<td><p>04 - Attacked from both sides (pincer attack, reverse side attack)</p></td>
</tr>
<tr>
<td><p>05 - Another attack from both sides battle (different maybe?)</p></td>
</tr>
<tr>
<td><p>06 - Another side attack</p></td>
</tr>
<tr>
<td><p>07 - A third side attack</p></td>
</tr>
<tr>
<td><p>08 - Normal battle that locks you in the front row, change command is disabled</p></td>
</tr>
<tr>
<td><p>0x0013</p></td>
<td><p>1 byte</p></td>
<td><p>Indexed Pre-Battle Camera position</p></td>
</tr>
</tbody>
</table>

#### Camera Placement Data format {#camera_placement_data_format}

48 bytes per Formation

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x00</p></td>
<td><p>12 bytes</p></td>
<td><p>Primary Battle Idle Camera Position</p></td>
</tr>
<tr>
<td rowspan="7" style="text-align: center; background: rgb(104,104,155);"></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>0x0</p></td>
<td><p>Camera X Position</p></td>
</tr>
<tr>
<td><p>0x2</p></td>
<td><p>Camera Y Position</p></td>
</tr>
<tr>
<td><p>0x4</p></td>
<td><p>Camera Z Position</p></td>
</tr>
<tr>
<td><p>0x6</p></td>
<td><p>Camera X Direction</p></td>
</tr>
<tr>
<td><p>0x8</p></td>
<td><p>Camera Y Direction</p></td>
</tr>
<tr>
<td><p>0xA</p></td>
<td><p>Camera Z Direction</p></td>
</tr>
<tr>
<td><p>0x0C</p></td>
<td><p>2 * 12 bytes</p></td>
<td><p>Other Camera Positions in the above format referenced in enemies' animations.</p></td>
</tr>
<tr>
<td><p>0x24</p></td>
<td><p>12 bytes</p></td>
<td><p>Unused/Align 'FF'</p></td>
</tr>
</tbody>
</table>

#### Battle Formation Data {#battle_formation_data}

4 Possible battle formations per scene, maximum of 6 enemies per battle. Each enemy entry contains the following data:

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th colspan="2" style="text-align: center; background: rgb(104,104,104);"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x00</p></td>
<td><p>2 bytes</p></td>
<td colspan="2" style="text-align: center;"><p>Enemy ID</p></td>
</tr>
<tr>
<td><p>0x02</p></td>
<td><p>2 bytes</p></td>
<td colspan="2" style="text-align: center;"><p>position X</p></td>
</tr>
<tr>
<td><p>0x04</p></td>
<td><p>2 bytes</p></td>
<td colspan="2" style="text-align: center;"><p>position Y</p></td>
</tr>
<tr>
<td><p>0x06</p></td>
<td><p>2 bytes</p></td>
<td colspan="2" style="text-align: center;"><p>position Z</p></td>
</tr>
<tr>
<td><p>0x08</p></td>
<td><p>2 bytes</p></td>
<td colspan="2" style="text-align: center;"><p>Row</p></td>
</tr>
<tr>
<td><p>0x0A</p></td>
<td><p>2 bytes</p></td>
<td colspan="2" style="text-align: center;"><p><a href="#Binary_.22Cover_Flags.22" class="wikilink" title="Binary &quot;Cover flags&quot;">Binary "Cover flags"</a></p></td>
</tr>
<tr>
<td><p>0x0C</p></td>
<td><p>4 bytes</p></td>
<td colspan="2" style="text-align: center;"><p>Initial condition flags. Only last 5 bits are considered.</p></td>
</tr>
<tr>
<td colspan="2" rowspan="5" style="background: rgb(104,104,155)"></td>
<td style="text-align: center;"><p>0x0001</p></td>
<td style="text-align: center;"><p>Visible</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>0x0002</p></td>
<td style="text-align: center;"><p>Indicates initial direction facing if players get a side attack.</p></td>
</tr>
<tr>
<td style="text-align: center; background: rgb(155,155,104);"><p>0x0004</p></td>
<td style="text-align: center; background: rgb(155,155,104);"><p>Unknown</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>0x0008</p></td>
<td style="text-align: center;"><p>Targetable</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>0x0010</p></td>
<td style="text-align: center;"><p>Main Script Active</p></td>
</tr>
</tbody>
</table>

#### Enemy data format {#enemy_data_format}

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x0000</p></td>
<td><p>32 bytes</p></td>
<td><p>Enemy's name (completed by FFh bytes)</p></td>
</tr>
<tr>
<td><p>0x0020</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's level</p></td>
</tr>
<tr>
<td><p>0x0021</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's speed</p></td>
</tr>
<tr>
<td><p>0x0022</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's luck</p></td>
</tr>
<tr>
<td><p>0x0023</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's evade</p></td>
</tr>
<tr>
<td><p>0x0024</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's strength</p></td>
</tr>
<tr>
<td><p>0x0025</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's defense</p></td>
</tr>
<tr>
<td><p>0x0026</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's magic</p></td>
</tr>
<tr>
<td><p>0x0027</p></td>
<td><p>1 byte</p></td>
<td><p>Enemy's magic defense</p></td>
</tr>
<tr>
<td><p>0x0028</p></td>
<td><p>8 bytes</p></td>
<td><p>Element types (8 records):<br />
00h - Fire<br />
01h - Ice<br />
02h - Bolt<br />
03h - Earth<br />
04h - Bio<br />
05h - Gravity<br />
06h - Water<br />
07h - Wind<br />
08h - Holy<br />
09h - Health<br />
0Ah - Cut<br />
0Bh - Hit<br />
0Ch - Punch<br />
0Dh - Shoot<br />
0Eh - Scream<br />
0Fh - HIDDEN<br />
10h-1Fh - No Effect<br />
20h-3Fh - <a href="FF7/Battle/Status_Effects" class="wikilink" title="Statuses">Statuses</a> (Damage done by actions that inflict these statuses will be modified)<br />
FFh - No element</p></td>
</tr>
<tr>
<td><p>0x0030</p></td>
<td><p>8 bytes</p></td>
<td><p>Element rates for elements above, respectively (8 records):<br />
00h - Death<br />
02h - Double Damage<br />
04h - Half Damage<br />
05h - Nullify Damage<br />
06h - Absorb 100%<br />
07h - Full Cure<br />
FFh - Nothing</p></td>
</tr>
<tr>
<td><p>0x0038</p></td>
<td><p>16 bytes</p></td>
<td><p>Action animation index (1 byte each).</p></td>
</tr>
<tr>
<td><p>0x0048</p></td>
<td><p>32 bytes</p></td>
<td><p>Enemy Attack ID's (2 bytes each).</p></td>
</tr>
<tr>
<td><p>0x0068</p></td>
<td><p>32 bytes</p></td>
<td><p>Enemy Attacks <a href="FF7/Battle/Camera_Movement_Id_List" class="wikilink" title="Camera Movement Id">Camera Movement Id</a> for single and multiple targets (2 bytes each). If set this will overwrite camera movement set in attack itself.</p></td>
</tr>
<tr>
<td><p>0x0088</p></td>
<td><p>4 bytes</p></td>
<td><p>Item drop/steal rates.<br />
These are chances to get items listed in next section. 1 byte per item. If the rate is lower than 80h, for e.g. 08h - then this is a drop item and has 8/63 [63 is max] chance for drop. But if rate is higher than 80h, let's say... A0h, then this is an item for steal, and chances for successful steal is A0h - 80h = 20h = 32/63.</p></td>
</tr>
<tr>
<td><p>0x008C</p></td>
<td><p>8 bytes</p></td>
<td><p>This is a list of Item ID's which are described above. 2 bytes per item. FFFFh means no item.</p></td>
</tr>
<tr>
<td><p>0x0094</p></td>
<td><p>6 bytes</p></td>
<td><p>Indexes of up to three attacks (2 bytes each) that enemy can perform while manipulated or berserked</p></td>
</tr>
<tr>
<td style="background: rgb(155,155,104)"><p>0x009A</p></td>
<td style="background: rgb(155,155,104)"><p>2 bytes</p></td>
<td style="background: rgb(155,155,104)"><p>Unknown data</p></td>
</tr>
<tr>
<td><p>0x009C</p></td>
<td><p>2 bytes</p></td>
<td><p>Enemy's MP</p></td>
</tr>
<tr>
<td><p>0x009E</p></td>
<td><p>2 bytes</p></td>
<td><p>AP points you receive when you win the battle</p></td>
</tr>
<tr>
<td><p>0x00A0</p></td>
<td><p>2 bytes</p></td>
<td><p>Enemy can be morphed into this item. FFFFh if it can't be morphed into anything.</p></td>
</tr>
<tr>
<td><p>0x00A2</p></td>
<td><p>1 byte</p></td>
<td><p>Multiplier for back damage. damage = damage * 0xXX / 8.</p></td>
</tr>
<tr>
<td><p>0x00A3</p></td>
<td><p>1 byte</p></td>
<td><p>align 0xff.</p></td>
</tr>
<tr>
<td><p>0x00A4</p></td>
<td><p>4 bytes</p></td>
<td><p>Enemy's HP</p></td>
</tr>
<tr>
<td><p>0x00A8</p></td>
<td><p>4 bytes</p></td>
<td><p>Exp points you receive when you win the battle</p></td>
</tr>
<tr>
<td><p>0x00AC</p></td>
<td><p>4 bytes</p></td>
<td><p>Gil you receive when you win the battle</p></td>
</tr>
<tr>
<td><p>0x00B0</p></td>
<td><p>4 bytes</p></td>
<td><p>Status immunities</p></td>
</tr>
<tr>
<td style="background: rgb(155,155,104)"><p>0x00B4</p></td>
<td style="background: rgb(155,155,104)"><p>4 bytes</p></td>
<td style="background: rgb(155,155,104)"><p>Unknown [Always FFFFFFFFh]</p></td>
</tr>
</tbody>
</table>

#### Formation ID {#formation_id}

Formation ID is an index to a formation within a given scene. It is the scene index bit shifted 2 to the left plus formation index within the scene.

`0 1 2 3 4 5 6 7 8 9 A B C D E F`\
`[ - - - - - - - - - - - - ] [ ]`\
`        scene index         formation index`

For this reason, the Formation ID will not exceed 03FFh.

example: Formation 028Dh bit shift two to the right to get scene

`028D >> 2 = 00A3 (right-most bits are truncated)`

This is Scene 163 Formation Index is just the ID ANDed with 3.

`028D AND 3 = 01`

Formation 1 So this is Formation 1 in scene 163. (SOLDIER:3rd x2)

#### AI Data {#ai_data}

This section contains Battle Script that is executed before or/and during every fight. Every enemy has it\'s own script, and this script is divided to a number of sections. Each script starts with 32 bytes of header that are divided into 16 parts representing 16 script types. The 2-byte number in any section is an offset relative to the beginning of this 32 byte block that tells the script reader where the script starts for that script type.

| Offset | Script Type      |
|--------|------------------|
| 0x00   | Initialize       |
| 0x02   | Main             |
| 0x04   | General Counter  |
| 0x06   | Death Counter    |
| 0x08   | Physical Counter |
| 0x0A   | Magical Counter  |
| 0x0C   | Battle End       |
| 0x0E   | Pre-Action Setup |
| 0x10   | Custom Event 1   |
| 0x12   | Custom Event 2   |
| 0x14   | Custom Event 3   |
| 0x16   | Custom Event 4   |
| 0x18   | Custom Event 5   |
| 0x1A   | Custom Event 6   |
| 0x1C   | Custom Event 7   |
| 0x1E   | Custom Event 8   |

Its structure and opcodes are described [here](FF7/Battle/Battle_Scenes/Battle_Script "here"){.wikilink}.

NOTES:

- A monster\'s total AI size will always be an even number of bytes. If the actual scripts are an odd number, a single NULL (FFh) will be placed before the next monster\'s AI header (may not be required).
- Battle begins after all characters\' Initialize scripts have been run (Players first, then enemies, then formation).
- The only character with \"Battle End\" is in Cloud\'s AI. It\'s meant to lower the character\'s Love Points with him if he lets them die or he dies with them in the party (not sure which).
- Pre-Action Event occurs on all battle participants prior to any actions performed by any participant regardless of actor or target. This includes all executed 92 commands that have a command index of less than 21h. If any 92 commands are called in this section, the command that caused this script to run has priority.
- The Custom Event sections are not called by any event. They only occur if they are called with the 92 command.

`60 22 <- command index "Run script"`\
`60 0X <- where X is the script section in hex (eg. X = 8 would call Custom Event 1 since it is script id 08`\
`         [not to be confused with offset])`\
`92`

- Custom Event 8 is only used on Mystery Ninja (all), Ultimate Weapons in location other than above Cosmo Canyon, Safer Sephiroth, and the final \"showdown\" between Cloud and Sephiroth. These characters have scripts on them that do not remove them from battle when they are defeated.
- Custom Events 1-7 may not work. (not thoroughly tested)
- The order of scripts executed:

:   :\* Beginning of battle

    :   Pre-Battle (all participants)

    - Once a \"main-script enabled\" enemy\'s time gauge is full:

    :   Main (Enemy performs action)

    - Pre-Attack (If enemy script uses a 92 command with a command index of 20h or less)

    :   Pre-Action Setup (occurs on all participants)

    - Post-Attack
      1.  Death Counter (If script owner died, execution stops here)
      2.  General Counter (Executed by all targets)
      3.  Physical Counter/Magical Counter (Executed by all targets depending on damage type)
    - Battle ends

    :   Battle End (all participants)

#### Binary \"Cover Flags\" {#binary_cover_flags}

These flags are used in conjunction with row to determine if a target can be selected as the target of a **short-range attack**. The determination of this is worked out in this way: An enemy exists in row 1 and another in row 2. If the enemy in row 1 shares a cover flag with the enemy in row 2 then the enemy in row 2 cannot be targeted until all enemies in row 1 that share a cover flag with the row 2 enemy is defeated. It works like this. Two active enemies exist, A and B.

`If ((B's row > A's row) and (B's cover flags AND A's cover flags) > 0) then enemy B cannot be targeted by short-range attacks.`

for any enemies A and B.\
Example:\
Consider the Battery Cap x6 battle in the forest between Nibelheim and Rocket Town. Their cover flags (in binary) are:

`Row 1:       00100`\
`Row 2:    00110 01100`\
`Row 3: 00011 00100 11000`

The battery caps in row 2 cannot be targeted by a short-range attack until the one in row 1 has been defeated because they share the 0x4 cover flag. Once row 1 has been cleared:

`Row 2:    00110 01100`\
`Row 3: 00011 00100 11000`

The battery cap on left in row 2 covers the left two in row 3 because it shares flag 0x4 with the one in the middle and flag 0x2 with the one on the far left. As long as it is active these in row 3 cannot be targeted. Similarly, the battery cap on the right in row 2 shares the 0x4 flag with the middle of row 3 and the 0x8 flag with the far right of row 3 so these cannot be targeted until the right side of row 2 is defeated.\
It is also necessary to note that because row 1 does not share any flags with the extreme right and left of row 3, they can be targeted if the corresponding enemy in row 2 is defeated even if the row 1 enemy is still active.\
Also of note is that enemies in the same row that share cover flags are not considered.\
Only the first five bits may be considered even though the value is stored as a word.\

## Useful downloads {#useful_downloads}

There are few programs written that will help you edit scene.bin file:

- [Scene Reader](http://spinningcone.com/ff/stormmedia/projects/SceneReader.zip)
- [SceneEdit](http://www.subfan.pl/mav/SceneEdit.zip)
- [Scenester](http://aaronserv.dyndns.org/hosting/qhimmwiki/ramza_scenester_0.5.zip)
- [Proud Clod](http://forums.qhimm.com/index.php?topic=8481.0)

---

# FF7/Battle/Battle Scenes/Battle Script {#ff7battlebattle_scenesbattle_script}

- [FF7/Battle/Battle Scenes/Battle Script](#ff7battlebattle_scenesbattle_script){#toc-ff7battlebattle_scenesbattle_script}



(Information on opcodes provided by Terence Fergusson. Almost all information comes from [this post](http://forums.qhimm.com/index.php?topic=3290.msg45951#msg45951) on the forums.)

There are four actions to be explained when dealing with any opcode in AI script: Arguments, Values to take from the stack, what to do with Arguments and Values, and what to put back on the stack. So to fully understand what is happening a brief explanation of the stack is necessary.

The stack is more-or-less a list of values with different lengths. Only the top of the stack (the most recently added value) can be accessed at any given time, but when that value is accessed it is removed from the top of the stack and the previously added value now becomes the top of the stack. Adding to the stack is called \"Pushing\" a value and taking a value off is called \"Popping\". When pushing a value to the stack, the value of the number is pushed followed by the value type. The value type can be one of three different things:\
\
{\| border=\"1\" cellspacing=\"1\" cellpadding=\"3\" align=\"center\" style=\"border: 1px grey; border-collapse: collapse;\"
! style=\"background:rgb(104,104,104)\" align=\"center\" \| Code
! style=\"background:rgb(104,104,104)\" align=\"center\" \| Type
\|-
\| align=\"center\" \| 0Xh
\| Value
\|-
\| align=\"center\" \| 1Xh
\| [Address](FF7/Battle/Battle_Scenes/Battle_AI_Addresses "Address"){.wikilink}
\|-
\| align=\"center\" \| 2Xh
\| Multiple (between 1-10) Values
\|-
\|}\
They are stored as DWords, but the X will determine how many bytes to use: 0 = bit, 1 = Byte, 2 = Word, 3 = Three bytes

Now that we\'ve seen the stack, here are the opcodes:

<table>
<thead>
<tr>
<th style="text-align: center; background: rgb(104,104,104);"><p>Code</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Arguments</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Value(s) to pop</p></th>
<th style="text-align: center; background: rgb(104,104,104);"><p>Value to push</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Push Values</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>0Xh</p></td>
<td style="text-align: center;"><p>2 byte Memory Address</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Type 0X stored at translated Address</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Push Addresses</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>1Xh</p></td>
<td style="text-align: center;"><p>2 byte Memory Address</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Address value with a scope of X</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Mathematical and Bit-wise Operators</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>30h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Sum of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>31h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Difference of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>32h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Product of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>33h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Quotient of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>34h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Remainder from quotient of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>35h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Bit-wise AND of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>36h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Bit-wise OR of pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>37h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Bit-wise NOT of pop</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Logical Operators</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>40h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if pops are EQUAL</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>41h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if pops are NOT EQUAL</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>42h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if first pop is GREATER THAN OR EQUAL TO second pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>43h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if first pop is LESS THAN OR EQUAL TO second pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>44h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if first pop is GREATER THAN second pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>45h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if first pop is LESS THAN second pop</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Logical Comparisons</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>50h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if both pops are NON-ZERO (Logical AND)</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>51h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>True if either pop is NON-ZERO (Logical OR)</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>52h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>True if pop is ZERO (Logical NOT)</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Push Constants</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>60h</p></td>
<td style="text-align: center;"><p>1 byte Value</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Argument of type 01</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>61h</p></td>
<td style="text-align: center;"><p>2 byte Value</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Argument of type 02</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>62h</p></td>
<td style="text-align: center;"><p>3 byte Value</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Argument of type 03</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Script Jumps (No Pushes)</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>70h</p></td>
<td style="text-align: center;"><p>2 byte Script Address</p></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Jumps to script address in argument if pop is 0</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>71h</p></td>
<td style="text-align: center;"><p>2 byte Script Address</p></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Jumps to script address in argument if pop and top of stack are not equal</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>72h</p></td>
<td style="text-align: center;"><p>2 byte Script Address</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Jumps to script address in argument</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>73h</p></td>
<td colspan="3" style="text-align: center;"><p>This ends the script</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>74h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Pops one value from stack. (Not used)</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>75h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Link all scripts of script owner to popped Character ID.</p></td>
</tr>
<tr>
<td colspan="4" style="text-align: center; background: rgb(124,124,124);"><p>Bit Operations</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>80h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>First pop masked by second pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>81h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Random Word (0-65535)</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>82h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Random bit of pop stored as type 02</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>83h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>If pop is Type 01, Type 01 with count of number of bits set in pop<br />
If pop is Type 02, Type 02 filled with value of first non-null value in pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>84h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of type 2X</p></td>
<td style="text-align: center;"><p>Type 02 indicating which values in popped set were greatest</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>85h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of type 2X</p></td>
<td style="text-align: center;"><p>Type 02 indicating which values in popped set were least</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>86h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of type 1X</p></td>
<td style="text-align: center;"><p>Type 02 indicating MP Cost of attack index referenced in pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>87h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Type 02 with only bit in pop turned on (1 &lt;&lt; [pop])</p></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

 

<table>
<thead>
<tr>
<th colspan="4" style="text-align: center; background: rgb(104,104,104);"><p>Command</p></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center; background: rgb(124,124,124);"><p>Code</p></td>
<td style="text-align: center; background: rgb(124,124,124);"><p>Arguments</p></td>
<td style="text-align: center; background: rgb(124,124,124);"><p>Value(s) to pop</p></td>
<td style="text-align: center; background: rgb(124,124,124);"><p>Effect</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>90h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of type 1X, One of type 0X or 2X</p></td>
<td style="text-align: center;"><p>If first pop &lt; 4000h; Stores second pop at first pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>90h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of type 1X, One of type 0X or 2X, One of type 1X</p></td>
<td style="text-align: center;"><p>If first pop &gt;= 4000h; Stores second pop at first pop constrained by mask at third pop</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>91h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of any type</p></td>
<td style="text-align: center;"><p>Pops one value from stack.</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>92h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>First pop is attack ID to perform. Second pop action type<br />
</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>93h</p></td>
<td style="text-align: center;"><p>NULL terminated string</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Displays string</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>94h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Copy current status, hp and mp as well as some other specific data (like boosts, multipliers) from units in first given mask to units in second mask.</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>95h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>One of type 1X, one of type 00</p></td>
<td style="text-align: center;"><p>If second pop is 1, takes value at local address 2010 and writes value at <a href="FF7/Savemap#Save_Memory_Bank_1.2F2" class="wikilink" title="memory bank 1/2">memory bank 1/2</a> at offset specified by first pop<br />
If second pop is 0, data at memory bank1/2 at offset specified by first pop is stored at local address 2010.<br />
Otherwise, command is ignored.</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>96h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two of any type</p></td>
<td style="text-align: center;"><p>Get fighter elemental defense.</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>A0h</p></td>
<td style="text-align: center;"><p>One byte, NULL terminated ASCII</p></td>
<td style="text-align: center;"><p>First argument of any type</p></td>
<td style="text-align: center;"><p>Displays string to debug console, replacing "%d"s with pops</p></td>
</tr>
<tr>
<td style="text-align: center;"><p>A1h</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Two values of any type</p></td>
<td style="text-align: center;"><p>Pops two values from stack (Not Used, but valid command)</p></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

\
GENERAL NOTES:

- Command 90h is overloaded.
- If a type 2X is popped and any type is accepted, only the first value will be considered.
- If specific type is expected and that type is not available, the game with either crash or ignore that entire line.
- TRUE and FALSE are stored as type 00 as \'1\' and \'0\' respectively.
- Commands 74h and A1h are never used, but have been documented as valid commands.
- Commands 75h and 96h only appear in the Character AI found in the KERNEL.BIN.
- Commands of group 2X, BX, CX, DX, EX, and FX are treated as NOPs. The script will ignore them and continue processing. Also, any 5X, 6X, 7X, 8X, and 9X value that isn\'t listed above appear to be treated the same way, but it\'s safest to use a value from the 2X group. An incorrect 0X, 1X, 3X, or 4X will have unintended side-effects.

0X & 1X CODES NOTES:

- Valid values for X are 0, 1, 2, and 3.
  - These will store a bit, byte, word, and dword respectively.

3X CODES NOTES:

- The pushed value is type 2x if either of the pops are a 1X or 2X. In that case, the Masks of both pops are ANDed together. In \*all\* cases, the highest pop\'s size is used to determine the new pop\'s size.

4X CODES NOTES:

- The Pushed value will be type 00 if either component is a 1X or 2X type. It will only push TRUE or FALSE
- If both were 0X types, the result will be a type 02 which contains the Mask of all the objects in the pops that passed the comparison

86 CODE NOTES:

- This get the MP Cost of the ability referenced in the pop. The value of pop is referenced to the following areas:

` If Value >= 0xFFFF, return 0`\
` If Value <= 0x00FF, Addr = 00DAAC78 + Value*0x1C`\
` If Value >= 0x0100, match Value with wr[0099AAF4+(ID=[0..31])*2]`\
`    First ID it matches, Addr = 0099A774 + ID*0x1C`\
` If no Addr is found, return 0`\
` Otherwise, return wr[Addr + 4]`

The pushed value is, thus, the MP cost of the defined ability as a type 02. Note that 0x00 to 0xFF are standard magic and always loaded, while 0x100+ are the unique abilities loaded through scene.bin.

92 CODE NOTES:

- Second pop must be one of the following:

:   [Command index](FF7/Command_data "Command index"){.wikilink} in case of character AI
:   20h - For enemy attack
:   22h - Force execution of script (referenced by first pop)
:   24h - Pauses battle engine while string is displayed (in conjunction with code 93)

---

# FF7/Battle/Battle Animation (PC) {#ff7battlebattle_animation_pc}

- [FF7/Battle/Battle Animation (PC)](#ff7battlebattle_animation_pc){#toc-ff7battlebattle_animation_pc}
  - [Battle Animation File Format](#battle_animation_file_format){#toc-battle_animation_file_format}


## Battle Animation File Format {#battle_animation_file_format}

File format discovered/decoded by me, L. Spiro.
This file was written by me, L. Spiro, as can be seen by the proper grammar and perfect spelling.

(Wiki-fied by Halkun)
(Small additions by Borde)

### Part I: Structures {#part_i_structures}

There are 4 basic structures we will use in decoding the file format.
The header of animation data has been considered to be composed of 3 DWORDâ€™s, 3 WORDâ€™s, and one BYTE, however this is not how the header is really intended to be, despite being aligned correctly.

Battle animation files start with a DWORD which tells us how many animations are in the file. This number includes the special animations which are not actually animations at all. Although I have not yet decoded them, I suspect these are sets of keys for actual animation sets; keys that call scripted actions or tell the engine to print the damage numbers.

#### FF7FrameHeader

Cloudâ€™s battle animation file (rtda) has 94 (0x 5E) animations in it.
After this number begins each animation.
Each animation begins with a 12-byte header (3 DWORDâ€™s) we will call \"FF7FrameHeader\".
To get from one animation to the next, start at offset 0x04 in the animation file and begin reading these headers. For each header, skip \"FF7FrameHeader.dwChunkSize\" bytes until you get to the index of the file you want to load. When skipping, remember to skip starting at the end of the \"FF7FrameHeader\" header.
I mentioned a type of special animation data set that is in the header file.
These data sets, when filled with the \"FF7FrameHeader\" header, will have a \"dwChunkSize\" less than eleven, we skip them by jumping over the next 8 bytes that follow.

First, the two main headers in the animation file.

1\.
`<code>`{=html}

    typedef struct FF7FrameHeader {
        DWORD       dwBones;        // Bones in the model + 1 (unless we're dealing with a weapon animation, in which case it's value is always 1). 0x00
                                                    // This field is rather unreliable so better use the number of bones provided by the skeleton file.
        DWORD       dwFrames;       // Frames in the animation. 0x04
        DWORD       dwChunkSize;    // Size of the animation set.   0x08
    } * PFF7FrameHeader;            // Size = 12 bytes.

`</code>`{=html}
2.
`<code>`{=html}

    typedef struct FF7FrameMiniHeader {
        //SHORT     sBones; // Bones in the animation.
        SHORT       sFrames;// Apparently, frames in the animation (but sometimes sFrames > dwFrames)
        SHORT       sSize;  // Size of the animation data.  0x02
        BYTE        bKey;       // A key flag used for decoding.    0x04
    } * PFF7FrameMiniHeader;    // Size = 5 bytes.

`</code>`{=html}

NOTE: sBones should provably be called sFrames since it seems to hold a secondary frames counter. Thus, it should be equal to dwFrames. Unfortunately, it usually isn\'t. In fact, It\'s hard to say which one should actually be trusted. Apparently dwFrames is a more conservative value, meaning there will always be at least that many frames in the animation. But there can be more of them. I can\'t help but wonder if this means the rest of the frames are dummied out information or they serve some sort of purpose. On the other hand, sFrames is sometimes higher than the actual number of frames on the animation chunck.

Anyway, the actual number of frames can be computed by parsing the whole animation chunck.

It\'s also worth mentioning that there is at least one animation (15th from RSAA, the playable frog) which physically lacks the sFrames field. Instead, sSize is at 0x00 and bKey at 0x02. This animation is more than likely damaged, because FF7 doesn\'t seems to be able to handle it.

#### FF7FrameMiniHeader

Most of these members are straight-forward, however there is a very special and VERY important member in the \"FF7FrameMiniHeader\" structure called \"bKey\".
This is used for every rotation-decoding scheme (but one). It determines, essentially, the precision of the rotations and the deltas that follow in successive frames.
The value of â€œbKeyâ€ can only be 0, 2, or 4; the equation \"(12 - bKey)\" is used to determine the length of each raw (uncompressed) rotation.
After decompression, every rotation must be 12 bits, giving it a range from 0 to 4095.
But if \"bKey\" is 4, for example, then that means uncompressed rotations are stored as 8 bits, which gives them a range from 0 to 255. How is this fixed? After the 8 bits are read, they are then shifted left (up) by \"bKey\". This will place them at 12 bits, but with decreased accuracy.
This loss in accuracy is acceptable since rotations work as deltas and usually only change by a small amount.
Most large rotation deltas are things that are spinning, such as the blades on Aero Combatant. These cases are always a nice round number that can be handled with lower precision (in the case of Aero Combatant, it is 90 degrees even).

#### FF7ShortVec

Now the code to skip to any animation, by index, where \"iTarget\" is the index. This code assumes you have already opened the animation file (hFile) and you have skipped pasted the first 4 bytes.

`<code>`{=html}

    FF7FrameHeader  fhHeader;
    DWORD           dwBytesRead;
    for ( int I = 0; I < iTarget; I++ ) {
        if ( !ReadFile( hFile,
            &fhHeader, sizeof( fhHeader ),
            &dwBytesRead, NULL ) ) {

        CloseHandle( hFile );
        return false;
        }
        if ( fhHeader.dwChunkSize < 11 ) {  // If this is a special
                            //  chunk, skip it (it
                            //  is counted as part
                            //  of the total in the
                            //  file).
            if ( SetFilePointer( hFile, 8, NULL, FILE_CURRENT ) ==
            INVALID_SET_FILE_POINTER ) {
                CloseHandle( hFile );
                return false;
            }
            continue;           // Go on to the next
                            //  animation.
        }
        // Skip this animation set, whose size is determined by
        //  fhHeader.dwChunkSize.
        if ( SetFilePointer( hFile, fhHeader.dwChunkSize, NULL,
        FILE_CURRENT ) == INVALID_SET_FILE_POINTER ) {
            CloseHandle( hFile );
            return false;
        }
    }
    // Once we come to this point, we are at the very first byte of the
    //  animation we want to load.  Letâ€™s store it into a BYTE array.
    if ( !ReadFile( hFile,
        &fhHeader, sizeof( fhHeader ),
        &dwBytesRead, NULL ) ) {

        CloseHandle( hFile );
        return false;
    }
    BYTE * pbBuffer = new BYTE[fhHeader.dwChunkSize];
    // Now pbBuffer holds the actual animation data, including the 5-byte
    //  â€œFF7FrameMiniHeaderâ€ header.

`</code>`{=html}

We now have the animation we want loaded into a BYTE array (remember to delete it later).

#### FF7FrameBuffer

Now letâ€™s look at the other structures we will use.

3\.
`<code>`{=html}

    typedef struct FF7ShortVec {
        SHORT   sX, sY, sZ;     // Signed short versions.   0x00
        INT iX, iY, iZ;     // Integer representation.  0x06
        FLOAT   fX, fY, fZ;     // Float version after math.    0x12
    } * PFF7ShortRot;           // Size = 30 bytes.

`</code>`{=html}
Each rotation goes through 3 forms. Firstly, everything is stored as 2-byte SHORTâ€™s. These SHORTâ€™s are stored from 0 to 4096, where 0 = 0 degrees and 4096 = 360 degrees. This is the equation to convert one of these SHORTâ€™s into degrees: (SHORT / 4096 \* 360). Each frame is based off the previous frame, using the SHORT value as its basis.
Each SHORT is converted to an INT, which is the exact same as the SHORT version, except always positive.
Finally, the FLOAT gets filled with the final value, using the INT version as its base.
So, the sequence is:

First frameâ€¦

- Read X bits and store as a signed SHORT.
- Convert the SHORT to the INT field, adding 0x1000 if negative.
- Convert to FLOAT using (INT / 4096 \* 360). Apply this FLOAT to your model.

Next frameâ€¦

- Read X bits, and add them to the SHORT value from last frame.
- Convert the SHORT to the INT field, adding 0x1000 if negative.
- Convert to FLOAT using (INT / 4096 \* 360). Apply this FLOAT to your model.

Repeatâ€¦

This structure is for one bone rotation.
To load an entire frameâ€™s work of bones, we need this structure:
4.
`<code>`{=html}

    typedef struct FF7FrameBuffer {
        DWORD           dwBones;
        FF7ShortVec     svPosOffset;
        FF7ShortVec     *psvRots;

        FF7FrameBuffer() {
            dwBones = 0;
            psvRots = NULL;
        }
        ~FF7FrameBuffer() {
            dwBones = 0;
            delete [] psvRots;
            psvRots = NULL;
        }

        VOID    SetBones( DWORD dwTotal ) {
            // Delete the old.
            dwBones = 0;
            delete [] psvRots;
            
            // Create the new.
            psvRots = new FF7ShortVec[dwTotal];
            if ( psvRots != NULL ) { dwBones = dwTotal; }
        }
    } * PFF7FrameBuffer;

`</code>`{=html}
This structure will allocate enough memory for one frame of rotations. Simply call â€œFF7FrameBuffer.SetBonesâ€ with the number of bones in your animation.

### Part II: Functions and Format {#part_ii_functions_and_format}

First, we need a way to read bits from the BYTE array we have stored.
This is a basic bit-reading function. It reads â€œdwTotalBitsâ€ from â€œpbBufferâ€ starting at the â€œdwStartBitâ€â€™th bit.

#### GetBitsFixed

1\.
`<code>`{=html}

    INT GetBitsFixed( BYTE * pbBuffer, DWORD &dwStartBit,
    DWORD dwTotalBits ) {
        INT iReturn = 0;

        for ( DWORD I = 0; I < dwTotalBits; I++ ) {
            iReturn <<= 1;

            __asm mov eax, dwStartBit
            __asm mov eax, [eax]
            __asm cdq
            __asm and edx, 7
            __asm add eax, edx
            __asm sar eax, 3
            __asm mov ecx, pbBuffer
            __asm xor edx, edx
            __asm mov dl, byte ptr ds:[ecx+eax]
            __asm mov eax, dwStartBit
            __asm mov ecx, [eax]
            __asm and ecx, 7
            __asm mov eax, 7
            __asm sub eax, ecx
            __asm mov esi, 1
            __asm mov ecx, eax
            __asm shl esi, cl
            __asm and edx, esi
            __asm test edx, edx
            __asm je INCBIT
            iReturn++;
    INCBIT: dwStartBit++;
        }

        // Force the sign bit to extend across the 32-bit boundary.
        iReturn <<= (0x20 - dwTotalBits);
        iReturn >>= (0x20 - dwTotalBits);
        return iReturn;
    }

`</code>`{=html}

Now that we can read the bits in the buffer we have made, itâ€™s time to know what weâ€™re doing!

##### A.

The animation data begins with one full frame that is uncompressed, but stored in one of 3 ways. Every frame after that is compressed, but compressed in one of three ways; one way can be decoded using the same method as on the first frame, which is why sometimes the second, third, and even fourth frames can be decoded using the same method as was used on the first frame.

`   First Frame:`

Remember that we stored our animation buffer with a 5-byte â€œFF7FrameMiniHeaderâ€ at the beginning of it? We need this header now!

`<code>`{=html}

    PFF7FrameMiniHeader pfmhMiniHeader = (PFF7FrameMiniHeader)pbBuffer;

`</code>`{=html}

After this cast, â€œpfmhMiniHeader-\>bKeyâ€ will contain a number, either 0, 2, or 4.
Each rotation is stored in (12 - â€œpfmhMiniHeader-\>bKeyâ€) bits. This mean either 12, 10, or 8, respectively.
This is important to know.
But first, there is offset data. Each offset is 16 bits (a signed SHORT).
In the first frame of Cloudâ€™s first animation (rtda), these bytes are 00 00 FE 2E 00 00.
16 bits Ã--- 3 = 48 bits, or 6 bytes.
To get these bits, we first need to make a pointer point to the correct location. â€œpbBufferâ€ points 5 bytes before this data, so letâ€™s make a pointer that points to this data directly.

`<code>`{=html}

    BYTE * pbAnimBuffer = &pbBuffer[5];

`</code>`{=html}

When we use â€œGetBitsFixed()â€ to get the bits.

`<code>`{=html}

    DWORD dwBitStart = 0;   // The bits at which to begin reading in the
    //  stream.
    SHORT sX = GetBitsFixed( pbAnimBuffer, dwBitStart, 16 );
    SHORT sY = GetBitsFixed( pbAnimBuffer, dwBitStart, 16 );
    SHORT sZ = GetBitsFixed( pbAnimBuffer, dwBitStart, 16 );

`</code>`{=html}

After doing this, we have each of the three offsets, 0, -466, and 0.
The Y (-466) is always stored as its inverse, but for now we donâ€™t worry about that.

The first frame is uncompressed, but it could be 12, 10, or 8 bits per rotation.
How do we know? â€œpfmhMiniHeader-\>bKeyâ€!

For each bone, there are 3 rotations. So, for each bone, we do this:

`<code>`{=html}

    SHORT sRotX = GetBitsFixed( pbAnimBuffer, dwBitStart,
    12 - pfmhMiniHeader->bKey );
    SHORT sRotY = GetBitsFixed( pbAnimBuffer, dwBitStart,
    12 - pfmhMiniHeader->bKey );
    SHORT sRotZ = GetBitsFixed( pbAnimBuffer, dwBitStart,
    12 - pfmhMiniHeader->bKey );
    // We have each rotation, but for the equation to work, the range
    //  must always be from 0 to 4095.  If we got 8 bytes, for example,
    //  the range would only be from 0 to 255, so here we need to fix
    //  this.
    sRotX <<= pfmhMiniHeader->bKey;
    sRotY <<= pfmhMiniHeader->bKey;
    sRotZ <<= pfmhMiniHeader->bKey;

`</code>`{=html}

The first rotation is always 0, 0, 0. This is the root rotation and is not actually counted as part of the bone network of the character.

#### GetDynamicFrameOffsetBits

The first frame is easy.
Remember that all frames after are stored as relative offsets from the frame before it.
The offsets are relative to the SHORT values of the previous frame rather than the FLOAT or INT values.

Each frame begins with the three position offset values, but in the second frame and after, they can be either 7 or 16 bits.
To determine if which they are, we first get one bit. If that bit is 0, then the following 7 bits are the actual value of the offset (signed).
If it is 1, then the next 16 bits are the value of the offset. In total, the offsets will be either 8 or 17 bits.

Now the code to perform this operation.

2\.
`<code>`{=html}

    SHORT GetDynamicFrameOffsetBits( BYTE * pBuffer, DWORD &dwBitStart ) {
    DWORD dwFirstByte, dwConsumedBits, dwBitsRemainingToNextByte, dwTemp;
        SHORT sReturn;
        __asm {
            mov eax, dwBitStart
            mov eax, [eax]
            cdq
            and edx, 7
            add eax, edx
            sar eax, 3
            mov dwFirstByte, eax
            mov ecx, dwBitStart
            mov edx, [ecx]
            and edx, 7
            mov dwConsumedBits, edx
            mov eax, 7
            sub eax, dwConsumedBits
            mov dwBitsRemainingToNextByte, eax
            mov ecx, pBuffer
            add ecx, dwFirstByte        // Go to the first byte that
                            // has the bit where we
                            // want to begin.
            xor edx, edx
            mov dl, byte ptr ds:[ecx]
            shl edx, 8
            mov eax, pBuffer
            add eax, dwFirstByte
            xor ecx, ecx
            mov cl, byte ptr ds:[eax+1]
            or edx, ecx
            mov dwTemp, edx
            mov ecx, dwBitsRemainingToNextByte
            add ecx, 8
            mov edx, 1
            shl edx, cl
            mov eax, dwTemp
            and eax, edx
            test eax, eax
            jnz SeventeenBits

    EightBits :
            mov ecx, dwConsumedBits
            add ecx, 1
            mov edx, dwTemp
            shl edx, cl
            movsx eax, dx
            sar eax, 9
            mov sReturn, ax
            mov ecx, dwBitStart //
            mov edx, [ecx]      //
            add edx, 8      //
            mov eax, dwBitStart //
            mov [eax], edx      // Increase dwBitStart by 0x8 (8).
            jmp End

    SeventeenBits :
            mov ecx, dwTemp
            shl ecx, 8
            mov edx, pBuffer
            add edx, dwFirstByte
            xor eax, eax
            mov al, byte ptr ds:[edx+2]
            or ecx, eax
            mov dwTemp, ecx
            mov ecx, dwConsumedBits
            add ecx, 1
            mov edx, dwTemp
            shl edx, cl
            shr edx, 8
            mov sReturn, dx
            mov eax, dwBitStart //
            mov ecx, [eax]      //
            add ecx, 0x11       //
            mov edx, dwBitStart //
            mov [edx], ecx      // Increase dwBitStart by 0x11
                        //  (17).

    End :
        }
        return sReturn;
    }

`</code>`{=html}

After the first frame, we know that the positional offsets immediately follow.
So to get the positional deltas for the next frame, we would do this:

`<code>`{=html}

    SHORT sDeltaX = GetDynamicFrameOffsetBits( pbAnimBuffer, dwBitStart );
    SHORT sDeltaY = GetDynamicFrameOffsetBits( pbAnimBuffer, dwBitStart );
    SHORT sDeltaZ = GetDynamicFrameOffsetBits( pbAnimBuffer, dwBitStart );

`</code>`{=html}

Now we have the change from the previous frame. In our â€œFF7ShortVecâ€ structure, these are the SHORT values. To get the position of this frame, we add these offsets to the last frameâ€™s position.
If â€œIâ€ is this frame and â€œI-1â€ is the last frame, we could do something like this:

`<code>`{=html}

    FF7FrameBuffer[I].svPosOffset.sX = FF7FrameBuffer[I-1].svPosOffset.sX + sX;
    FF7FrameBuffer[I].svPosOffset.sY = FF7FrameBuffer[I-1].svPosOffset.sY + sY;
    FF7FrameBuffer[I].svPosOffset.sZ = FF7FrameBuffer[I-1].svPosOffset.sZ + sZ;

`</code>`{=html}

#### GetEncryptedRotationBits

Now all that is left is to decode the rotations.
Rotations change size in multiple ways.
There is no single simple way to express them.

They are, however, always at least one bit long.
The first bit is a flag. If 0, the rotational change is 0, and that is the end of that rotation.
If it is not 0, then we must get the next 3 bits.
The next 3 bits can tell us to do one of three things.
If the resulting 3-bit signed value is 0, then the rotation delta is (-1 \<\< pfmhMiniHeader-\>bKey). This is the smallest possible decrement for the given precision (remember that precision is based off â€œpfmhMiniHeader-\>bKeyâ€.
If the 3-bit value is 7, then we treat the rotation the same way as we do in the first frame, where we read (12-pfmhMiniHeader-\>bKey) bits, then shift left by â€œpfmhMiniHeader-\>bKeyâ€.

The complicated cases are 1 through 6.
If the 3-bit value is from 1 to 6, then this indicates the number of bits in the rotation delta.
For our example, letâ€™s assume the 3-bit value was 4.
This means we need to read the next 4 bits from the stream. These 4 bits will be the animation delta, but we actually have to handle them before we can call it final.
The first bit of this new data is a sign bit which determines if the value is below 0.
If it is below zero, we must subtract from that number (1 \<\< (\[Number of Bits\] â€" 1)).
So, if the 3-bit value was 4, and we read 4 bits from the stream, and the resulting value was negative, we would subtract from that value (1 \<\< 3), or 8.
If the 4-bit value is positive, we add (1 \<\< (\[Number of Bits\] â€" 1)) to it.
After we handle the positive and negative cases, we have to adjust for our precision again.
So, we shift left the resulting value by â€œpfmhMiniHeader-\>bKeyâ€.
This is all shown in the code below.

3\.
`<code>`{=html}

    SHORT GetEncryptedRotationBits( BYTE * pBuffer, DWORD &dwBitStart,
    INT iKeyBits ) {
        DWORD dwNumBits, dwType;
        INT iTemp;
        SHORT sReturn;
        // Check the first bit.
        INT iBits = GetBitsFixed( pBuffer, dwBitStart, 1 );
        __asm mov eax, iBits    // If the first bit is 0, return 0
                    // and continue. It is not necessary
                    // to mov iBits into EAX, but I do it
                    // anyway.
        __asm test eax, eax
        __asm jnz SecondTest
        __asm jmp ReturnZero    // Return 0

    SecondTest :
        // Otherwise continue by getting the next 3 bits.
        iBits = GetBitsFixed( pBuffer, dwBitStart, 3 );
        __asm mov eax, iBits
        __asm and eax, 7
        __asm mov dwNumBits, eax
        __asm mov ecx, dwNumBits
        __asm mov dwType, ecx   // dwType = ecx = dwNumBits = eax =
                    //  (iBits & 7).
                    //  When we get to the case, all of
                    //  these values are the same.
        __asm cmp dwType, 7
        __asm ja ReturnZero // Is dwType above 7?  If so, return 0.
                    //  This can never actually happen.

        // Otherwise, use it in a switch case.
        switch ( dwType ) {
            case 0 : {
                __asm or eax, 0xFFFFFFFF    // After this, EAX will
                                // always be -1.
                __asm mov ecx, iKeyBits
                __asm shl eax, cl       // Shift left by
                                // precision.
                                // (-1 << iKeyBits)
                __asm mov sReturn, ax       // Return that number.
                __asm jmp End
            }
            case 1 : {}
            case 2 : {}
            case 3 : {}
            case 4 : {}
            case 5 : {}
            case 6 : {
                // Get a number of bits equal to the case switch (1,
                // 2, 3, 4, 5, or 6).
                iTemp = GetBitsFixed( pBuffer, dwBitStart,
                    dwNumBits );
                __asm mov eax, iTemp
                __asm cmp iTemp, 0
                __asm jl IfLessThanZero
                // If greater than or equal to 0â€¦
                __asm mov ecx, dwNumBits    // dwNumBits = (iBits &
                                // 7) from before.
                __asm sub ecx, 1        // dwNumBits - 1.
                __asm mov eax, 1
                __asm shl eax, cl       // (1 << (dwNumBits â€“
                                // 1)).
                __asm mov ecx, iTemp
                __asm add ecx, eax      // iTemp += (1 <<
                                // (dwNumBits - 1)).
                __asm mov iTemp, ecx
                __asm jmp AfterTests
                // If less than 0â€¦
    IfLessThanZero :
                __asm mov ecx, dwNumBits    // dwNumBits = (iBits &
                                // 7) from before.
                __asm sub ecx, 1        // Decrease it by 1.
                __asm mov edx, 1
                __asm shl edx, cl       // Shift â€œ1â€ left by
                                // (dwNumBits - 1).
                __asm mov eax, iTemp        // iTemp still has the
                                // bits we read
                                // from before.
                __asm sub eax, edx      // iTemp - (1 <<
                                // (dwNumBits - 1))
                __asm mov iTemp, eax

                // Now, whatever we set on iTemp, we need to shift it
                // up by the precision value.
    AfterTests :
                __asm mov eax, iTemp
                __asm mov ecx, iKeyBits
                __asm shl eax, cl           // iTemp <<= iKeyBits
                __asm mov sReturn, ax
                __asm jmp End
            }

            case 7 : {
                // Uncompressed bits.  Use standard decoding.
                iTemp = GetBitsFixed( pBuffer, dwBitStart,
                    12 - iKeyBits );
                __asm mov ecx, iKeyBits
                __asm shl eax, cl           // iTemp <<= iKeyBits.
                __asm mov sReturn, ax
                __asm jmp End
            }

        }


    ReturnZero :
        __asm xor ax, ax
        __asm mov sReturn, ax

    End :

        return sReturn;
    }

`</code>`{=html}

### Part III: Putting it All Together {#part_iii_putting_it_all_together}

To make life easy, letâ€™s use one function to load an entire frame at a time.
This function will load an entire frame into a â€œFF7FrameBufferâ€ structure.
The function will return the bit position where the next frame will begin.
After the function returns, we must translate the rotational INT values to their FLOAT forms (although the function can be modified to do this part itself).
This function will be called in a loop for every frame in the rotation.

#### LoadFrames

1\.
`<code>`{=html}

    DWORD LoadFrames( PFF7FrameBuffer pfbFrameBuffer,
    INT iBones,
    INT iBitStart,
    BYTE * pbAnimBuffer ) {
        // Get backups of the information we need.
    DWORD       dwThisBitStart  = iBitStart;
        INT     iThisBones      = iBones;
        BYTE *  pbThisBuffer    = pbAnimBuffer;

        PFF7FrameMiniHeader pfmhMiniHeader =
            (PFF7FrameMiniHeader)pbAnimBuffer;
        SHORT   sSize = pfmhMiniHeader->sSize;                      
        BYTE    bKeyBits = pfmhMiniHeader->bKey;

        // Skip the first 5 bytes because they are part of the frame header.
        pbThisBuffer += sizeof( FF7FrameMiniHeader );

        if ( iBitStart == 0 ) { // First frame?
            // The first frame is uncompressed and each value is the
            // actual rotation.
            pfbFrameBuffer->svPosOffset.sX = GetBitsFixed( pbThisBuffer, dwThisBitStart, 16 ); //Always 16 bits
            pfbFrameBuffer->svPosOffset.sY = GetBitsFixed( pbThisBuffer, dwThisBitStart, 16 );
            pfbFrameBuffer->svPosOffset.sZ = GetBitsFixed( pbThisBuffer, dwThisBitStart, 16 );

            // This function will set the FLOAT values for the
            //  positions.
            // Any scaling that needs to be done would be done here.
            pfbFrameBuffer->svPosOffset.fX = (FLOAT)pfbFrameBuffer->svPosOffset.sX;
            pfbFrameBuffer->svPosOffset.fY = (FLOAT)pfbFrameBuffer->svPosOffset.sY;
            pfbFrameBuffer->svPosOffset.fZ = (FLOAT)pfbFrameBuffer->svPosOffset.sZ;

            for ( int I = 0; I < iThisBones; I++ ) {
                // Now get each bone rotation (the first bone is
                //  actually the root, not part of the skeleton).
                // During the first frame, the rotations are always
                //  (12 â€“ bKeyBits).
                // We shift by bKeyBits to align it to 12 bits.
                pfbFrameBuffer->psvRots[I].sX = (GetBitsFixed( pbThisBuffer, dwThisBitStart, 12 - bKeyBits ) << bKeyBits);
                pfbFrameBuffer->psvRots[I].sY = (GetBitsFixed( pbThisBuffer, dwThisBitStart, 12 - bKeyBits ) << bKeyBits);
                pfbFrameBuffer->psvRots[I].sZ = (GetBitsFixed( pbThisBuffer, dwThisBitStart, 12 - bKeyBits ) << bKeyBits);

                // Store the INT version as the absolute value
                //  of the SHORT version.
                pfbFrameBuffer->psvRots[I].iX = (pfbFrameBuffer->psvRots[I].sX < 0) ? pfbFrameBuffer->psvRots[I].sX + 0x1000 : pfbFrameBuffer->psvRots[I].sX;
                pfbFrameBuffer->psvRots[I].iY = (pfbFrameBuffer->psvRots[I].sY < 0) ? pfbFrameBuffer->psvRots[I].sY + 0x1000 : pfbFrameBuffer->psvRots[I].sY;
                pfbFrameBuffer->psvRots[I].iZ = (pfbFrameBuffer->psvRots[I].sZ < 0) ? pfbFrameBuffer->psvRots[I].sZ + 0x1000 : pfbFrameBuffer->psvRots[I].sZ;
            }
        }
        else {                  // All other frames.
            SHORT sX, sY, sZ;           // Get the positional
    //  offsets.
            sX = GetDynamicFrameOffsetBits( pbThisBuffer, dwThisBitStart );
            sY = GetDynamicFrameOffsetBits( pbThisBuffer, dwThisBitStart );
            sZ = GetDynamicFrameOffsetBits( pbThisBuffer, dwThisBitStart );

            // When we come to this area of the function,
    //  pfbFrameBuffer will have the previous frame
    //  still stored in it.  Just add the offsets.
            pfbFrameBuffer->svPosOffset.sX += sX;
            pfbFrameBuffer->svPosOffset.sY += sY;
            pfbFrameBuffer->svPosOffset.sZ += sZ;

            pfbFrameBuffer->svPosOffset.fX = (FLOAT)pfbFrameBuffer->svPosOffset.sX;
            pfbFrameBuffer->svPosOffset.fY = (FLOAT)pfbFrameBuffer->svPosOffset.sY;
            pfbFrameBuffer->svPosOffset.fZ = (FLOAT)pfbFrameBuffer->svPosOffset.sZ;
            for ( int I = 0; I < iThisBones; I++ ) {
                // The same applies here.  Add the offsets
                //  and convert to INT form, adding 0x1000
                //  if it is less than 0.
                // When Final FantasyÂ® VII loads these animations,
                //  it is possible for the value to sneak up above
                //  the 4095 boundary through a series of positive
                //  offsets. 
                sX = GetEncryptedRotationBits( pbThisBuffer, dwThisBitStart, bKeyBits );
                sY = GetEncryptedRotationBits( pbThisBuffer, dwThisBitStart, bKeyBits );
                sZ = GetEncryptedRotationBits( pbThisBuffer, dwThisBitStart, bKeyBits );

                pfbFrameBuffer->psvRots[I].sX += sX;
                pfbFrameBuffer->psvRots[I].sY += sY;
                pfbFrameBuffer->psvRots[I].sZ += sZ;

                pfbFrameBuffer->psvRots[I].iX = (pfbFrameBuffer->psvRots[I].sX < 0) ? pfbFrameBuffer->psvRots[I].sX + 0x1000 : pfbFrameBuffer->psvRots[I].sX;
                pfbFrameBuffer->psvRots[I].iY = (pfbFrameBuffer->psvRots[I].sY < 0) ? pfbFrameBuffer->psvRots[I].sY + 0x1000 : pfbFrameBuffer->psvRots[I].sY;
                pfbFrameBuffer->psvRots[I].iZ = (pfbFrameBuffer->psvRots[I].sZ < 0) ? pfbFrameBuffer->psvRots[I].sZ + 0x1000 : pfbFrameBuffer->psvRots[I].sZ;
            }
        }

        // If we did not read as many bits as there are in the frame,
        //  return the location where the bits should start for the
        //  next frame.
        if ( (SHORT)(dwThisBitStart / 8) < sSize ) {
    return dwThisBitStart;
    }
        // Otherwise, return 0.
        return 0;
    }

`</code>`{=html}
2.

#### A Sample Loop {#a_sample_loop}

This is an example loop that could be used to load a full animation.

`<code>`{=html}

    FF7FrameHeader fhHeader;
    ReadFile( hFile, &fhHeader, sizeof( fhHeader ), &ulBytesRead,
    NULL );
    BYTE * baData = new BYTE[fhHeader.dwChunkSize];
    ReadFile( hFile, &baData, fhHeader.dwChunkSize, &ulBytesRead,
    NULL );

        // This will be our buffer to hold one frame.
        //  We will only buffer one frame at a time, so to
        //  to fully load the animations, you would need to
        //  write your own routine to store the data in
        //  fbFrameBuffer after each loaded frame.
    FF7FrameBuffer fbFrameBuffer;
    fbFrameBuffer.SetBones( fhHeader.dwBones );
    INT iBits = 0;
    for ( DWORD J = 0; J < fhHeader.dwFrames; J++ ) {
        // We pass a pointer to fbFrameBuffer.  The first frame
        //  will load diretly into it.
        // Every frame after that will actually use it with the
        //  offsets loaded to determine the final result of that
        //  frame. 
            iBits = LoadFrames( &fbFrameBuffer, fhHeader.dwBones, iBits, baData );
            // Reverse the Y offset (required).
            fbFrameBuffer.svPosOffset.fY = 0.0f â€“ fbFrameBuffer.svPosOffset.fY;

    // The first rotation set is skipped.  It is not part of
    //  the skeleton.  Skipping is optional, but
    //  Final FantasyÂ® VII skips it; it is always 0, 0, 0.
    // I believe the actual use for the â€œrootâ€ rotation is
    //  to dynamically make the model point at its target
    //  or face different directions during battle.
    // UPDATE: Although the value of this field is 0,0,0 for most animations, some actually store a base rotation here
    // so it shouldn't be ignored.
            for ( DWORD I = 0; I < fhHeader.dwBones - 1; I++ ) {
                fbFrameBuffer.psvRots[I+1].fX = (FLOAT)fbFrameBuffer.psvRots[I+1].iX / 4096.0f * 360.0f;
                fbFrameBuffer.psvRots[I+1].fY = (FLOAT)fbFrameBuffer.psvRots[I+1].iY / 4096.0f * 360.0f;
                fbFrameBuffer.psvRots[I+1].fZ = (FLOAT)fbFrameBuffer.psvRots[I+1].iZ / 4096.0f * 360.0f;
            }
    // Store the data for this frame here (in your own
    //  routine).

        }

        delete [] baData;

`</code>`{=html}

## Part IV: Qhimmâ€™s Input {#part_iv_qhimmâs_input}

Qhimm has taken the time to rewrite two of these functions used in decoding, so it is easier to understand for people who know C++ better than they know assembly (despite my comments being in the assembly code).
He has also written a more in-depth look at the logistics behind the rotation compression format and explains its limitations

â€œGetValueFromStreamâ€ is the C/C++ version of my â€œGetDynamicFrameOffsetBitsâ€ and his â€œGetCompressedDeltaFromStreamâ€ is the C++ version of my â€œGetEncryptedRotationBitsâ€.

`<code>`{=html}

    short GetValueFromStream( BYTE *pStreamBytes,
    DWORD *pdwStreamBitOffset )
    {
        // The return value;
        short sValue;
        // The number of whole bytes already consumed in the stream.
        DWORD dwStreamByteOffset = *pdwStreamBitOffset / 8;
        // The number of bits already consumed in the current stream byte.
        DWORD dwCurrentBitsEaten = *pdwStreamBitOffset % 8;
        // The distance from dwNextStreamBytes' LSB to the 'type' bit.
        DWORD dwTypeBitShift = 7 - dwCurrentBitsEaten;
        // A copy of the next two bytes in the stream (from big-endian).
        DWORD dwNextStreamBytes = pStreamBytes[dwStreamByteOffset] << 8 | pStreamBytes[dwStreamByteOffset + 1];

        // Test the first bit (the 'type' bit) to determine the size of the value.
        if (dwNextStreamBytes & (1 << (dwTypeBitShift + 8)))
        {   // Sixteen-bit value:
            // Collect one more byte from the stream.
            dwNextStreamBytes = dwNextStreamBytes << 8 |
                pStreamBytes[dwStreamByteOffset + 2];
            // Shift the delta value into place.
            sValue = (dwNextStreamBytes << (dwCurrentBitsEaten + 1)) >> 8;
            // Update the stream offset.
            *pdwStreamBitOffset += 17;
        }
        else
        {   // Seven-bit value
            // Shift the delta value into place (taking care to preserve the sign).
            sValue = ((short)(dwNextStreamBytes << (dwCurrentBitsEaten + 1))) >> 9;
            // Update the stream offset.
            *pdwStreamBitOffset += 8;
        }

        // Return the value.
        return sValue;
    }


    short GetCompressedDeltaFromStream( BYTE *pStreamBytes, DWORD *pdwStreamBitOffset,
    int nLoweredPrecisionBits )
    {
        unsigned int nBits;
        int iFirstBit = GetBitsFromStream( pStreamBytes, pdwStreamBitOffset, 1 );
        if (iFirstBit)
        {
            unsigned int uType = GetBitsFromStream( pStreamBytes,
                pdwStreamBitOffset, 3 ) & 7;
            switch (uType)
            {
            case 0:
                // Return the smallest possible decrement delta (at given
                //  precision).
                return (-1 << nLoweredPrecisionBits);

            case 1: case 2: case 3: case 4: case 5: case 6:
                // Read a corresponding number of bits from the stream.
                int iTemp = GetBitsFromStream( pStreamBytes,
                    pdwStreamBitOffset, nBits );
                // Transform the value into the full seven-bit value, using the bit
                //  length
                // as part of the encoding scheme (see notes).
                if (iTemp < 0)  iTemp -= 1 << (nBits - 1);
                else            iTemp += 1 << (nBits - 1);
                // Adapt to the requested precision and return.
                return (iTemp << nLoweredPrecisionBits);
            case 7:
                // Read an uncompressed value from the stream (at requested
                //  precision), and return.
                iTemp = GetBitsFromStream( pStreamBytes,
                    pdwStreamBitOffset, 12 - nLoweredPrecisionBits );
                return (iTemp << nLoweredPrecisionBits);
            default:
            }
        }
        // Default/error: return zero.
        return 0;
    }


    /*
        Notes for rotational delta compression scheme
        =============================================

        The delta values are stored in compressed form in a bit stream. Consecutive
        values share no bit correlation or encoding dependencies, rather they are
        encoded separately using a scheme designed to optimize small-scale rotations.

        Rotations are traditionally given in normalized PSX 4.12 fixed-point compatible
        values, where a full rotation is the integer value 4096. Values above 4095 simply
        map down into the [0,4095] range, as expected from rotational arithmetics. When
        encoded, only the required 12 bits of precision are ever considered.

        In some animations, the author can choose to forcibly lower the precision of
        rotational delta values below 12 bits. Though these animations are naturally not
        as precise, they encode far more efficiently, both because of the smaller size of
        'raw' values, and also because of the increased relative span of the 'close-range'
        encodings available for small deltas. The smallest 128 [-64,63] sizes of deltas
        can be stored in compressed form instead of as raw values. This method is
        efficient
        since a majority of the rotational deltas involved in skeletal character animation
        will be small, and thus doubly effective if used with reduced precision. Precision
        can be reduced by either 2 or 4 bits (down to 10 or 8 bits).

        The encoding scheme is capable of encoding any 12-bit value as follows:

        First, a single bit tells us if the delta is non-zero. If this bit is zero, there
        is no delta value (0) and the decoding is done. Otherwise, a 3 bit integer
        follows, detailing how the delta value is encoded. This has 8 different meanings,
        as follows:

        Type   Meaning
        ------ -------------------------------------------------------
        0      The delta is the smallest possible decrement (under the
            current precision)
        1-6    The delta is encoded using this many bytes
        7      The delta is stored in raw form (in the current precision)

        The encoding of small deltas works as follows: The encoded delta can be stored
        using 1-6 bits, giving us a total of 2+4+8+16+32+64 = 126 possible different
        values, which during this explanation will be explained as simple integers (the
        lowest bits of the delta, in current precision). The values 0 (no change) and -1
        (minimal decrement) are already covered, leaving the other 126 values to neatly
        fill out the entire 7 bit range. We do this by encoding each value like follows:

        - The magnitude of the delta is defined as the value of its most significant
          value bit (in two's complement, so the highest bit not equal to the sign bit).
          For example, the values '1' and '-2' have magnitude 1, while the value '30' will
          have a magnitude of 32. For simplicity, we also define the 'signed magnitude' as
          the magnitude multiplied by the sign of the value (so '-2' has a signed
          magnitude of -1).
        - When encoding a value, we subtract its signed magnitude; essentially pushing
          everything down one notch towards zero, setting the most significant value bit
          to equal the sign bit and thus ensuring that none of the transformed values
          require more than six bits to accurately represent in two's complement.
        - The transformed value is then stored starting from its magnitude bit (normally,
          you would have to start one bit higher to include the sign bit and prevent
          signed integer overflow). Small values will be stored using fewer bits, while
          larger values use more bits. The two smallest values, 0 and -1, are not
          encodeable but are instead handled using the previously mentioned scheme.

        When decoding, you only need to know the number of bits of the encoded value, use
        the value of its most significant bit (not the most significant value bit!) as
        the magnitude, multiply it by the sign of the encoded value to get the signed
        magnitude, and then add that to the encoded value to get the actual delta value.

        Some examples of encodings:

        Delta value *      Encoded            *) in current precision, as integer
        ------------------ ------------------
         0                 0
        -1                 1 000
        -5                 1 011 111
        15                 1 100 0111
        128                1 111 xxxx10000000  (length depends on precision)


        (Note: The reduced precision is treated as rounding towards negative infinity)

    */

`</code>`{=html}

---


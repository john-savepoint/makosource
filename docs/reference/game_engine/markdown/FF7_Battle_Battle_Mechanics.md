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

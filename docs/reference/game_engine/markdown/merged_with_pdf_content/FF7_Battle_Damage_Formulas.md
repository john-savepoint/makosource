<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_Battle_Damage_Formulas.md (    1779 lines)
Major section: 06_BATTLE_MODULE.md
Merge decision: NO EXTRACTION PERFORMED  
Reason: Individual file contains Terence Fergusson's comprehensive damage formula documentation
Status: COMPLETE - Original file copied as source of truth
-->

# FF7/Battle/Damage Formulas {#ff7battledamage_formulas}

- [FF7/Battle/Damage Formulas](#ff7battledamage_formulas){#toc-ff7battledamage_formulas}
  - [Version History](#version_history){#toc-version_history}
  - [Foreword](#foreword){#toc-foreword}
  - [Component Guides](#component_guides){#toc-component_guides}
  - [Contents](#contents){#toc-contents}
  - [1. Definitions](#1_definitions){#toc-1_definitions}
  - [2. Basic Damage Formulae](#2_basic_damage_formulae){#toc-2_basic_damage_formulae}
  - [3. Battle Damage](#3_battle_damage){#toc-3_battle_damage}
  - [4. Statuses](#4_statuses){#toc-4_statuses}
  - [5. Game Over](#5_game_over){#toc-5_game_over}



## The Final Fantasy 7 Battle Mechanics by Terence Fergusson

This document is entirely my work, and was written and is owned by me, Terence Fergusson. All copyrights and trademarks are acknowledged where not specifically mentioned. If you wish to reproduce this document AS IS, you may do so without having to ask for my permission, providing that the entire document including this copyright notice is left intact, and preferably in ASCII text format.

### VERSION HISTORY {#version_history}

v0.8 : 23/03/02 : Original Release - Not accompanied by sister guides

### FOREWORD {#foreword}

These guides have been a long time in the making.

It started with a webpage. Just a small private one that I created early in April 1999. It was more practice than anything else, and I put up most of my findings about the game at that time. Most of it was incorrect, but I had some basics down.

I changed to pure text format soon after when I realized that a webpage was very difficult to update with the number of tables such a Mechanics document requires. Pure text is also a lot easier to simply add stuff to. Updates can be made in seconds.

But this was still a private thing. It's been private for years, in fact. But that's not to say it wasn't added to or the information wasn't utilized.

During this time, I've met many people who share the same fascination that I have with this subject. We've helped each other too; some of the information included here is due to information that was pointed out to me in the memory dumps. I've learned from it, I've progressed. And the guide grew.

Recently, it's become more and more apparent that this kind of information is not only useful, but also in demand. True, it doesn't help the average player, whose only concern is to get from A to B without too much trouble and just having fun along the way... but to others, it's fun to learn how the game works, and exactly what makes the monsters they fight tick.

As such, I have finally managed to complete this to my satisfaction. It may not be finished yet, and I may not ever find the time to update it so that it is complete... but at least it is whole.

And this is it.

NOTE (23/03/0003): This isn't a finished product. It may never be a finished product. As it stands, only this guide of the three planned is being released. Please do not e-mail asking on the progress of the other two; the Battle Mechanics guide is being released now as something to work on. The other two will follow when they're structurally complete, and not before.

### COMPONENT GUIDES {#component_guides}

*The FF7 Game Mechanics Guides* are split into three files. This guide, the first, will detail the basic formulas, terms and statuses used in battle. The other two are:

#### The FF7 Party Mechanics

Covers the various battle formulas relating to the party, notably formulas regarding spell damage, materia use, and limit breaks.

#### The FF7 Enemy Mechanics

A list of enemies focusing on their attacks and attributes, and how the damage from those attacks are factored into the battle mechanics formulas.

The FF7 Battle Mechanics is the main one to start with, since it will define many terms that will be used in both Party and Enemy Mechanics.

Note that this guide is based on the PC version. While most alleged gameplay differences between the PC and PSX versions have been proven false, more may exist.

NOTE (23/03/0003): Only the Battle Mechanics Guide has been released as of this point. The other two will follow when they are done, which may not be soon. Please don't hold your breath waiting for them.

Note that this guide is based on the PC version. While most alleged gameplay differences between the PC and PSX versions have been proven false, more may exist.

NOTE (23/03/0003): Only the Battle Mechanics Guide has been released as of this point. The other two will follow when they are done, which may not be soon. Please don't hold your breath waiting for them.

#### **CONTENTS**

- 1. Definitions
- 1.1 Character Stats
- 1.2 Special Term Definitions
- 1.2.1 Basic Terms
- 1.2.2 Types of Attack
- 1.2.3 Target Types
- 1.2.4 Equipment Modifiers
- 2. Basic Damage Formulae
- 3. Battle Damage
- 4. Statuses
- 4.1 Status Attributes
- 4.2 Special Notes On Statuses
- 5. Game Over

#### **1. DEFINITIONS**

## **1.1 Character Stats**

There are seven Primary Stats and seven Derived Stats that make up your basic character. The Primary Stats are:

| Str: Strength | Dex: Dexterity |
|---------------|----------------|
| Vit: Vitality | Mag: Magic     |
| Spr: Spirit   | Lck: Luck      |
| Lvl: Level    |                |

The Derived Stats are:

| Atk: Attack     | At%: Attack%   |
|-----------------|----------------|
| Def: Defense    | Df%: Defense%  |
| MAt: Magic atk  | MDf: Magic def |
| MD%: Magic def% |                |

NOTE! There is a bug in FF7 such that Armour MDefense Bonus is \*not\* added to Magic Def. This is reflected in many places, including the Status screen (but the bonus you are supposed to get is visible in the Equip screen). To my knowledge, it is definitely evident in both the PC version and the PSX version. You will take the same amount of magic damage regardless of your Armour's MDefense rating.

The Primary Stats dictate the overall strengths of your character. Level dictates exactly how powerful the character is, while the last six stats round off the character. Each character has a starting value for their Primary Stats, and every level, there is a chance that these stats will be raised by a random number of points. In addition, it's possible to further raise these stats permanently using Sources.

The Derived Stats are based from your Primary Stats and your currently worn equipment. They are derived as such:

| Atk | Str + Weapon Attack Bonus               |
|-----|-----------------------------------------|
| At% | Weapon Attack% Bonus                    |
| Def | Vit + Armour Defense Bonus              |
| Df% | (Dexterity / 4) + Armour Defense% Bonus |
| MAt | Magic                                   |
| MDf | Spirit + Armour MDefense Bonus          |
| MD% | Armour MDefense% Bonus                  |

Your Derived Stats, along with a few of the Primary Stats(mostly Level and Luck), are what's used in every battle to determine battle damage, spell strength, and so on.

In addition to the above, many pieces of amour, weaponry and accessories will give you special bonuses to your Primary Stats which, in turn, affect your Derived Stats. You can only see these bonuses in effect on the Status screen though, not on the Equip screen. These bonuses are factored into battle, however.

From now on, the three letter abbreviations next to each Stat will be used instead of their full names.

#### **1.2 Special Term Definitions**

The following terms will be used throughout the Game Mechanics guides.

#### **1.2.1 Basic Terms**

#### *Base Damage:*

This is a special term which means the basic power of most basic types of attack. For physical attacks, Base Damage is dependent on Atk and Lvl. For magical attacks, it is dependent on MAt and Lvl. Most attacks will use Base Damage to determine the damage they do. In ability formulas, this will be listed as Base.

#### *NRV:*

Short for No Random Variation, this means that the attack will not vary in power according to a random factor.

#### *Caster:*

The character that used the ability. Also known as the source of the attack's effect.

#### *Target:*

The character that is affected by the ability.

#### *BD (Before Defense) Modifier:*

This term applied to quite a number of abilities. The primary use for BD Modifiers is for Ultimate Weapons. In this case, the name which has been given to them is UW Modifier. As of writing, only one BD Modifier is known that is not connected to Ultimate Weapons, but the distinction, however slim, still stands. All BD Modifiers take the form of a fraction with a denominator of 16. (For example: 3/16) See below for details.

#### *UW (Ultimate Weapon) Modifier:*

A subset of BD Modifiers. UW Modifiers are for Ultimate Weapons only. They are separated for clarity. Take note that UW Modifiers are only applied to Base Command skills, which are defined as: Attack, 2x-Cut, 4x-Cut, Slash-All, Mug, Morph and D. blow.

#### *Added Damage Effect:*

This term applies to certain weapons and abilities. It is a modifier that is multiplied to the damage during damage calculations. See below for details.

#### *Element:*

Some attacks will use a special Element that will determine certain factors about the attack. Most enemies will have certain elemental weaknesses and strength; this factor will determine whether the attack will do extra damage or be defended against. For example, an attack described as a 'Elm: Fire' attack will do Fire Elemental damage.

#### Note that FF7 uses the following common Elements:

| Fire   | Ice         | Lightning | Earth |
|--------|-------------|-----------|-------|
| Poison | Gravity     | Water     | Wind  |
| Holy   | Restorative |           |       |

The absence of any Element is termed Non-Element, which, while not technically an element in itself, will be used to denote this state.

Also note that there are five more Elements that apply only to Physical Attacks. While FF7 is aware of them, they are not normally utilized in Elemental calculations because almost nothing is weak or defends against them:

| Cut   | Hit   | Punch |
|-------|-------|-------|
| Shoot | Shout |       |

And finally, there is a 16th Hidden Element that was obviously supposed to have been dummied out, but due to sloppy coding, has ended up having unexpected effects with the Elemental Materia and certain attacks.

Hidden

Of the above Elements, Restorative, Cut, Hit, Punch, Shoot, Shout and Hidden are not made known to the player. They can be described as follows:

| Element     | Description                                                                                                                                                                                                                                                                                                                |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Restorative | See below for the definition of Restore. Restorative is the<br>difference between the Cure and Life series of spells which give<br>back HP, and the Holy Elemental attack spells like Alexander,<br>which cause Holy Element damage. While Undead are often said<br>to be Weak to Holy, they *Absorb* Restorative instead. |
| Cut         | Used to describe an attack that uses an edged weapon.                                                                                                                                                                                                                                                                      |
| Hit         | Used to describe an attack that uses a blunt weapon.                                                                                                                                                                                                                                                                       |
| Punch       | Used to describe an attack that uses a piercing weapon.                                                                                                                                                                                                                                                                    |
| Shoot       | Used to describe attacks that use projectile weapons.                                                                                                                                                                                                                                                                      |
| Shout       | Used to describe attacks that are sonic or energy-based in nature.                                                                                                                                                                                                                                                         |
| Hidden      | Unknown. Unlike the others, Hidden is the name I've given it.<br>Very few attacks have this element. Any that do can be protected<br>from by linking any non-Element Materia with the Elemental<br>Materia in a character's armor.                                                                                         |

## **1.2.2 Types of Attack**

When an attack type is given, the following terms will be used to describe them. These are the most common terms; unique terms will be described within the notes for the appropriate ability itself.

| Type of<br>Attack | Description                                                                                                                                                                                                           |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Physical          | Any attack termed as Physical will use Att and Def as the primary damage calculating<br>stats, and is affected by Barrier. It will also normally use the Physical Formula for Base<br>Damage, unless noted otherwise. |

| Type of<br>Attack | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |  |  |  |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|
| Magical           | Any attack termed as Magical will use MAt and MDf as the primary damage calculating<br>stats, and is affected by MBarrier. It will also normally use the Magical Formula for<br>Base Damage, unless noted otherwise.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |  |  |  |
| Piercing          | This means that the attack will ignore the target's Defense and Magic def stats when<br>determining how much damage it will do to them.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |  |  |  |
| Attack            | Any attack with this modifier will cause damage to some stat. By default, this is HP, but<br>this can be modified. For example, MP Attack would mean an ability that reduces the<br>target's MP.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |  |  |  |
| Absorb            | The same as Attack, except that the caster benefits in some way from the damage given<br>to the target. Unless otherwise noted, the benefit is equal and opposite to the damage<br>dealt to the target                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |  |  |  |
| LR                | Short for Long Range, this means that the ability will not factor Back Row modifiers into<br>the formula. Thus, the ability will do full damage no matter what the distance. This also<br>means that the ability can target enemies that are 'Can't reach'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |  |  |  |
| Restore           | Restorative is a special Element that has the damage rules for Elements reversed.<br>Specifically, with no Restorative affinity, targets will gain HP or MP from this Element.<br>However, targets that are listed as Absorb Restorative will alternatively take damage<br>from this element. If an attack is listed as Restorative, it will replace the Attack<br>modifier. Restore is used just to remind that this is a healing ability; 'Elm: Restorative'<br>will still be listed within the attack, and in all other ways, it is classed as an Attack.                                                                                                                                                                                         |  |  |  |
| Recovery          | A special type of attack, this ability will completely refill the target's HP and MP. It can<br>function without an Element, but if it does have one, then against any target that Absorbs<br>the ability's Element, it will inflict Death status instead of restoring their HP and MP.<br>The words 'Recovery' or 'Death' will flash up over the target to demonstrate which is<br>being used.                                                                                                                                                                                                                                                                                                                                                      |  |  |  |
| Change<br>Status  | This attack type attempts to change the statuses on a target. Changes in Status are<br>divided into three types:<br>Cure, Inflict or<br>Toggle. Cure will remove an instance of that<br>Status. Inflict will attempt to give the target that Status. Toggle will either Inflict the<br>Status on the target, or Cure it if the target already has that Status. If at any time a spell<br>or ability is described as Curing, Inflicting or Toggling a Status, it will also have a<br>number in square brackets. This number is the relative chance of success.<br>(Example: [15] Inflict 'Death' is a Rating 15 chance of inflicting the Death Status. The<br>exact formula is not yet known, but a rough guide is to think of the Rating as a chance |  |  |  |
|                   | out of 64. This approximation works well when used against enemies of equal level to<br>you)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |  |  |  |
|                   | A Change Status ability, like any other attack, will be either Physical or Magical;<br>however, if Change Status is used, then this means that the attack itself does no damage.<br>The only reason Physical or Magical is listed is for certain enemies that may react to one<br>or the other. If the chance reads [63], then the Status Chance is as near enough to 100%<br>as it's going to get. I've only ever seen a [63] Rating fail once thus far, and that was<br>Death Dealer's Hidden One against a L99 Barret                                                                                                                                                                                                                             |  |  |  |

| Type of<br>Attack | Description                                                                           |
|-------------------|---------------------------------------------------------------------------------------|
| Misc              | Any ability that is not adequately described by the above categories falls under this |
| Ability           | category by default. Whatever effect the ability has will be depicted under Notes.    |

#### **1.2.3 Target Types**

Any ability used will often require a target to be given. The following shorthand will be used:

| Op  | Opponent                  |
|-----|---------------------------|
| Al  | Ally                      |
| Tar | Target (Opponent or Ally) |

#### *1 Tar:*

This means that the ability can only hit one selected target. Normally, this target will be selected by the player or enemy. Multi-hit attacks that only hit one selected target also fall under this category.

#### *<n> Tar:*

This special variation of the above means that the ability will hit <n> randomly selected targets in the chosen target group. For example, Omnislash will be listed as '15 Op', which means it will hit 15 randomly selected targets in a selected opponent target group.

#### *All Tar:*

This means that the ability will hit all targets within the selected target group once each. If this Target Type is used, the strength of the ability must be multiplied by 2/3; that strength is then used to determine the damage for each single target in the group. Note that if there is only one Target in the group, then the ability is used at full strength instead; it's counted as a 1 Tar attack.

#### *All Tar (NS):*

NS stands for No Split. This means that the strength of the ability is NOT multiplied by 2/3 when used against All Targets. It will thus do full damage to each and every single target in the group.

### *Area:*

This means that the entire battlefield is a valid target for the ability. Both the party and the enemies will be affected.

#### *Random:*

This means that the target will actually be a randomly selected single target out of a valid group. Similar to <n> Tar, except that the valid group is what's being specified. Random [All] specifies a single random target out of a single target group. Random [Area] specifies a single random target out of all valid target groups in battle. (Example: Random [All Tar] would allow you to decide which target group to attack, and then a single target would be picked randomly from that group. Random [Area] would have no such choice, and the single target would be picked from all targetable characters in the battle.)

#### **1.2.4 Equipment Modifiers**

The following terms will be used as shorthand to describe various modifiers equipment and accessories

may give.

*+?? <Stat>:*

 This indicates that wearing the given equipment will give the indicated bonus to the described Basic Stat. In the Weapon List found in the FF7 Player Mechanics, there are columns already for Mag, Spr, Vit and Dex bonuses, so bonuses for those stats given by Weapons will be found in those columns instead.

#### *Half/Void/Absorb <Elemental>:*

The equipment will automatically allow you to either Halve, Void or Absorb damage from the relevant Elements. If you have a better Elemental Defense than the one given, it will not be affected; the better Defense automatically takes priority.

#### *Immune <Status>:*

Wearing this equipment will automatically make you immune to the given Status. Note that Immunity is really a Resist. If you are Immune to that Status, then it is also impossible to Cure that Status should you have it on you. This is best shown by wearing a Ribbon and using a Hyper outside of battle; you will gain the 'Fury' Status, but nothing will be able to remove that Status while you are inside battle.

#### *Start with <Status>:*

This means that wearing the piece of equipment will make sure you begin each battle with the named Status(es). You cannot protect yourself from this initial infliction.

#### **2. BASIC DAMAGE FORMULAE**

First, it is important that you are familiar with the [x] convention. Basically, [x] is the greatest integer equal to or less than x. Thus, [4.5] would be 4. This convention will be used throughout the guides, and is very important for battle damage. In addition, you should also be familiar with the following convention - x ... y - which defines an integer random number between x and y inclusive. For example, 3 ... 8 would be a random number out of 3, 4, 5, 6, 7 and 8.

Finally, a function Rnd is defined here, since it is also required by this guide. Rnd picks a random number between 0 and 1 inclusive. It is not known yet what precision of accuracy Rnd uses at this point.

The Base Damage formula is the most important battle formula in the game, so it will be listed here.

The Physical Formula for Base Damage is defined as such:

Base Damage = Att + 
$$[(Att + Lvl) / 32] * [(Att * Lvl) / 32]$$

The Magical Formula for Base Damage is defined likewise:

Base Damage = 
$$6 * (MAt + Lvl)$$

Note that while Att and MAt are used in the above formulas, it is possible for FF7 abilities to be coded to use each formula with the opposite attack stat (using MAt instead of Att in the Physical Formula, for instance). However, this is purely academic, since no known ability has been found within the game code that does this.

#### **3. BATTLE DAMAGE**

Now that the basic terms and formulae have been covered, the basic battle process of determining damage can be defined. Note that certain abilities may skip certain aspects of this procedure; for example, Mindblow will never need to work out either Base Damage, DefMod or Random Variation, because it is a Piercing attack with NRV, and uses a formula that doesn't need Base.

#### *1. Define Negative Damage*

A boolean flag named 'Negative Damage' shall be defined at this point. The only factor it checks at this stage is whether the attack contains the Restorative Element. If it does, then Negative Damage is true. Otherwise, it begins as false. The purpose of this flag shall become clear later.

#### *2. Find Base Damage*

First, for most attacks, Base Damage must be worked out. If the formula used for the ability does not use Base, then this part may be skipped.The Base Damage formulae are listed in the previous section, and depend on whether the attack is Physical or Magical.

If the character is 'Small', then Base Damage must be worked out with Att = 0.

Finally, the character's Physical Base Mod and Magical Base Mod are checked. Hero Drinks (as an example) raise both of these by 30 each time you drink them, to a maximum of 100.

If the attack is physical:

```
Base Damage = [Base Damage * (100 + Physical Base Mod) / 100
```

If the attack is magical:

```
Base Damage = [Base Damage * (100 + Magical Base Mod) / 100]
```

#### *3. Use the Appropriate Formula*

Next, the formula for the attack is worked out. This is usually either an independent formula or a multiple of Base. This gives us the power of the attack. FF7 has several formulas that it may use:

Physical Base Damage Formula \* Power of Attack

Magical Base Damage Formula \* Power of Attack

Percentage of Target's HP

Percentage of Target's Max HP

Magical Formula + Power of Attack (the Cure Formula)

Fixed Power of Attack

Recovery

Special Formulas

The last in that list refers to formulas that require special variables that aren't normally checked in battle, like for Chocobuckle, which requires the number of times the party has escaped from battle as a defining variable.

In addition, there are many different Fixed Power formulas. Since this is not a hex debug document, no attempt will be made to further explain this; the formulas used will instead be listed next to each ability in the FF7 Party Mechanics and the FF7 Enemy Mechanics.

Many abilities will have either the Non-Damaging formula or a Power of 0. Thus, they may skip this part, since these are generally abilities that change statuses or do other non-damage related abilities. Element checking may still take place though to determine success of certain abilities.

At this point:

$$dam = [dam]$$

### *4. Factor is the BD (Before Defense) Modifiers*

BD Modifiers are factored in now, since they're a measure of your base damage. Note that UW (Ultimate Weapon) Modifiers are classified as BD Modifiers.

BD Modifiers on weapons \*ONLY\* take effect if the ability used is a BASE Command skill. These commands are: Attack, 2x-Cut, 4x-Cut, Slash-All, Mug, Morph and D. blow. Limit, Magic, Summon, Item and E. Skill are exempt from this (thus, an Ultimate Weapon will not lend its added damage capability to a Limit Break, for example). In addition, attacks that don't use Base Damage or use their own formula (like Throw) are also exempt from this.

The key thing is to note how two BD Modifiers are put together (this should only be necessary when using Morph with most Ultimate Weapons, but the method is listed here just in case). The formula is:

New BDM = 
$$[(BD1 * BD2 * 16) + (15 / 16)] / 16$$

This may seem confusing, but what we're actually doing is every time we multiply two BD Modifiers together, we have to round \*up\* to the nearest 1/16th. For example:

9/16 \* 2/16 = 18/256 = 9/128

Which rounds up to 2/16 or 1/8.

If we use the formula to check this, we get:

```
New BDM = [(9/16 * 2/16 * 16) + (15 / 16)] / 16
= [(9 * 2/16) + 15/16] / 16
= [18/16 + 15/16] / 16
= [33/16] / 16
= [2 + 1/16] / 16
= 2 / 16
```

By going through the BD Modifiers as above, you should eventually end up with one final BD

Modifier. This is applied to the damage like so:

dam = [BD Modifier \* dam]

#### *5. Calculate All Tar if appropriate*

Attacks that target All Targets are granted a modification now. If the attack is No Split (listed as All Tar (NS)), then this section is skipped. In addition, if there is only 1 target in the group, then this section is skipped (it counts as if it was only used against 1 Tar instead).

Whether an ability is No Split or not depends on the formula and valid target data for the ability in question. Attacks that use the Physical Formula will always split their damage (they can never have the No Split ability). Attacks that use the Magical Formula are only No Split if they cannot be switched between All Tar and 1 Tar. Any ability that works with the All Materia will thus automatically be denied No Split. The exception here is the Cure Formula, which always splits no matter what the valid target data. The rest of the formulas will generally be No Split, but exceptions will be noted.

If the attack is not No Split:

$$dam = [dam * 2 / 3]$$

#### *6. Calculate Quadra Magic if available*

If the ability is linked to Quadra Magic and Quadra Magic works with it,then:

$$dam = [dam / 2]$$

This happens no matter what, unless the ability does not do any kind ofdamage or healing. (Demi and FullCure are affected as well)

## *7. Calculate Defense*

Defense comes next, if warranted. If the attack is Piercing, then this part is ignored. If the attack is Physical, then the target's Def stat is used; otherwise, if the attack is Magical, the MDf stat is used.

The Defense Mod and MDefense Mod of the character is checked at this point. This is a special battleonly stat that is modified by Hero Drinks and Dragon Force (as examples). Each Hero Drink raises both Mods by 30. Each Dragon Force raises both Mods by 50. Neither Mod can ever exceed 100. The two values are applied as such:

If attack is Physical:

DefNum = [Def \* (100 + Defense Mod) / 100]

If attack is Magical:

$$DefNum = [MDf * (100 + MDefense Mod) / 100]$$

And finally, we apply the damage reduction:

```
 dam = [dam * (512 - DefNum) / 512]
```

#### *8. Calculate Berserk and Critical Strike*

If the character is in 'Berserk' and the ability uses a Physical Base, then:

$$dam = [dam * 1.5]$$

Critical Strikes and Deathblow damage are also done at this point. If the attack is a Critical Strike (either through luck, via the Deathblow command, the Lucky Girl status, or any other move that has automatic Criticals), and the ability uses a Physical Base then:

$$dam = dam * 2$$

#### *9. Frog Check*

At this point, after Critical Strike, if the Caster is a 'Frog' and the attack utilises Physical Base Damage, then:

$$dam = [dam / 4]$$

#### *10. MP Turbo Check*

MP Turbo also gets a look in at this point if the ability is compatible and is currently paired with the requisite Materia. Depending on the level of the MP Turbo Materia, damage is adjusted accordingly:

$$dam = [dam * (1 + (MP Turbo Level / 10))]$$

#### *11. Back Row Check*

Back Row modifier occurs now. If the attack is Magical or is Long Range, then this part is ignored. If either the Caster or the Target is in the back row, then:

$$dam = [dam / 2]$$

Note that the above applies even if attacking an ally or even yourself. It is only applied once though; you will do 1/2 rather than 1/4 damage if you attack yourself with a non-LR physical attack while in the back row.

#### *12. Barrier and MBarrier Check.*

Barrier and MBarrier are now looked at. If the target has Barrier and the attack is Physical and does not have the No Barrier attribute, then:

$$dam = [dam / 2]$$

The same goes for MBarrier; if the target has MBarrier and the attack is Magical and does not have the No Barrier attribute, then:

$$dam = [dam / 2]$$

Generally, only the Physical Formula, the Magical Formula and the Cure Formula attacks are affected by Barrier and MBarrier. The rest will usually be No Barrier. As always, exceptions will be noted as and when we come to them.

#### *13. Sadness Check*

Sadness is skipped if the ability is NRV, a Restore or from an Item.

If the target has the Status 'Sadness', then the damage is modified accordingly:

$$dam = dam - [dam * 79 / 256]$$

#### *14. Random Variation Factored In*

If the ability being used is listed as NRV, then we skip this part:

Random Variation comes next. Thus, the following is applied:

$$dam = [dam * (15 + Rnd) / 16]$$

## *15. Lower bound sanity check*

Lower bound sanity checking takes place at this point. Thus:

If 
$$(dam < 1)$$
 Then:  $dam = 1$ 

Damage greater than 9999 is left unchanged at this point.

#### *16. Added Damage Effects*

Added Damage Effects are now done. These are simple integer multipliers.

Added Damage Effects on weapons, like BD Modifiers above, \*ONLY\* take effect if the ability used is a BASE Command skill. No doubling up of Yoshiyuki with Goblin Punch, for example.

In any case, for all Added Damage Effects that must be done:

dam = dam \* Added Damage Effect

#### *17. Elemental Damage and Final Status Checks*

Finally, Elemental Damage and Final Status Checks takes place. Once one Elemental is found in the order of priority, the others will be skipped. Note that Poison Element is special; if you're Immune to the status, then you also count as being Immune to the element (but Asrb: Poison will always be checked first).

Within this section, checks against Shield, Peerless and certain special abilities of enemies are also made. It is impossible to be sure of the order this happens in, so no attempt will be made to integrate these checks into the below Elemental system. However, relative notes on the subject can be found in the respective Status descriptions and the specific enemy attributes this applies to.

Also, once again, any Elemental affinity the player has on their weapon is only taken into consideration for base Command abilities. You can't have a Fire-element Omnislash, for example, or Throw Gravity-element Mythril Sabers.

First, check if the target Absorbs one of the Elements of the attack. If so, then the Negative Damage flag is toggled (if Negative Damage was true, it's now false; and vice versa).

If the target doesn't Absorb any of the Elements, but does Void it, then:

$$dam = 0$$

If the target doesn't Absorb or Void any of the Elements, but does Half it, then:

$$dam = [(dam + 1) / 2]$$

Finally, if the target hasn't Absorbed, Voided or Halved any of the Elements already, then Weak is checked. If the target is Weak against any of the Elements, then:

$$dam = dam * 2$$

## *18. The 9999 "Sanity Check"*

After all this, only one thing remains.

If 
$$(dam > 9999)$$
 Then:  $dam = 9999$ 

If the attack does damage to MP and the target does not have the 'HP<->MP' Materia equipped, then the sanity check is instead:

If 
$$(dam > 999)$$
 Then:  $dam = 999$ 

The 999 'Sanity Check' is also used if the target \*does\* have 'HP<->MP' equipped and the damage is dealt to HP instead of MP (the 'HP<->MP' Materia not only reverses HP and MP, but it also reverses the max damage allowed against that target).

### *19. Negative Damage*

The final damage has, at that point, been calculated. All that remains is to check the status of the Negative Damage flag.

If Negative Damage is true, then the amount 'dam' will be healed to the target. The type of the attack will define what exactly is healed and what else is done with the 'dam' variable.

If Negative Damage is false, then the amount 'dam' will be used as damage against the target's appropriate stat (usually HP).

The above sequence can be summarized as such:

Small Check

Base Formula

Hero Drink Check

BD Modifier

All Tar Reduction

Quadra Magic

Defense

Berserk / Critical Strike

Frog Check

MP Turbo Check

Back Row / Long Range

Barrier / MBarrier

Sadness Check

Random Variation

Damage < 1

Added Damage Effects

Elemental Damage and Final Status Checks

Damage > 9999

Negative Damage

Note: This order may not be 100% accurate. There are too many combinations of factors to test them all, and without seeing the code for the battle algorithms, a lot of what is displayed here are educated guesses derived from results seen. It is presumed accurate enough for 99% of all results at this present time though.

#### **4. STATUSES**

There are 31 major Statuses in the game, although a few of them are not shown on the Status screen and are sometimes transparent to the user. The statuses available are thus:

| Death     | Near-death | Sleep   | Poison      | Sadness        | Fury       | Confusion  | Silence  |
|-----------|------------|---------|-------------|----------------|------------|------------|----------|
| Haste     | Slow       | Stop    | Frog        | Small          | Slow-numb  | Petrify    | Regen    |
| Barrier   | MBarrier   | Reflect | Shield      | Death-sentence | Manipulate | Berserk    | Peerless |
| Paralysed | Darkness   | Dual    | Death Force | Resist         | Lucky Girl | Imprisoned |          |

Of those, Death Force, Resist and Lucky Girl are nearly transparent to the player, and a few of the others (like Imprisoned) are completely invisible save for their effect. Several are not listed on the Status screen; these are: *Dual*, *Death Force*, *Resist*, *Lucky Girl* and *Imprisoned*.

What follows is a breakdown of the statuses visual effects and gameplay attributes.

#### **4.1 Status Attributes**

#### Death

The ultimate offensive Status Attribute. If you're successfully hit with it, you are immediately reduced to 0 HP. Death is also the state of having 0 HP.

You can protect from it, fortunately. That is, you can protect yourself from 'Sudden Death', which is any attack that causes you to instantly die, regardless of how much HP you have or how much damage the attack actually caused. However, if you are reduced to 0 HP by taking too much damage... well, you can't protect against that at all.

| Visuals      | Character lies down                                                                                  |
|--------------|------------------------------------------------------------------------------------------------------|
| Effects:     | Character flagged as 'Dead'<br>Removes all Statuses except for 'Frog' and 'Small'                    |
| Duration     | Until cured                                                                                          |
| Protected by | Petrify', 'Peerless', 'Resist', Safety Bit, Destruct+Added<br>Effect, Odin+Added Effect, Death Force |
| Cured by     | Life, Life2, Phoenix Down, Angel Whisper, Phoenix                                                    |

#### Near-Death

When your character is heavily wounded, but still able to fight, they are classed as Near-death. They kneel down and their HP indicator turns yellow to notify of this. Otherwise, this Status Attribute means nothing else; it occurs only when your HP is 25% or less of your current Max HP, and you are not yet dead.

| Visuals      | Character kneels                                          |
|--------------|-----------------------------------------------------------|
| Effects:     | None                                                      |
| Duration     | Until cured                                               |
| Protected by | Anything that prevents HP loss                            |
| Cured by     | Anything that serves to boost your HP above 25% of Max HP |

#### Sleep

This nasty affliction is one of four temporary 'Can't Act' Status Attributes in FF7. Once under this Status, the character is asleep, and cannot fight normally. However, Sleep is easily reversed; any Physical hit is enough to wake up a sleeping character.

| Visuals      | Character kneels/has Zzz above head                                                     |
|--------------|-----------------------------------------------------------------------------------------|
| Effects:     | Character cannot Act                                                                    |
| Duration     | 26 units                                                                                |
| Protected by | Petrify', 'Peerless', 'Resist', Ribbon, Headband, Seal+Added Effect, Hades+Added Effect |
| Cured by     | Any Physical Hit, Esuna, Remedy, White Wind, Angel Whisper                              |

#### Poison

Any character inflicted with this Status will continually take Poison Elemental damage throughout the battle. It won't be purged naturally until the battle ends.

| Visuals      | Character kneels/flashes Green                                                                                                          |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Effects:     | Character takes [1/32 of Max HP] of<br>Physical Poison Elemental damage every<br>2.5 units of time (ignores Def, Barrier and<br>is NRV) |
| Duration     | Until end of battle                                                                                                                     |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon,<br>Poison Ring, Star Pendant, Fairy Ring,<br>Poison+Added Effect, Hades+Added<br>Effect        |
| Cured by     | Poisona, Esuna, Remedy, White Wind,<br>Angel Whisper, Antidote                                                                          |

Note: The Status Attribute Poison is different from the Element Poison. But, if you Void or Absorb Poison Elemental, any attack that does Poison damage will no longer inflict the Poison Attribute. However, you will still be vulnerable to things like Bad Breath, which causes various Status Attributes without causing damage. The reverse also has effects; being Immune to the Status Attribute Poison will mean that you are also considered Immune to the element.

#### Sadness

A character inflicted with Sadness is more subdued and careful in battle. They tend to take less damage from attacks, but they find it difficult to get angry at anything. Hence, the growth of their Limit Bar is severely reduced. The Limit Bar turns blue to notify you of this condition.

| Visuals      | Limit bar is blue                                                                                                                          |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Effects:     | Character takes approximately 177/256x damage<br>from most attacks (see Section 3: Battle Damage<br>for details), Limit Bar growth halved. |
| Duration     | Until cured                                                                                                                                |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Peace Ring                                                                                        |
| Cured by     | Hyper, Esuna, Remedy                                                                                                                       |

#### Fury

Anyone in Fury status is more prone to rushing the enemy, and attacking them with greater fervour. As such, while they don't benefit from the reduced damage of Sadness, they instead get an increase in the growth of their Limit Bar, allowing them to pull of Limit Breaks with greater frequency. However, their attacks are more erratic, and miss more often. The Limit Bar turns red to notify you of this condition.

| Visuals      | Limit bar is red                                      |
|--------------|-------------------------------------------------------|
| Effects:     | Character Attack% reduced<br>Limit Bar growth doubled |
| Duration     | Until cured                                           |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Peace Ring   |
| Cured by     | Tranquilizer, Esuna, Remedy                           |

#### Confusion

The pure opposite of Berserk, despite the fact that the character suffering from Confusion doesn't have any increased damage potential. You immediately lose control of the character, and they will randomly attack their allies, even themselves. Fortunately, it's easy to cure; a single Physical hit will take care of it. However, a recently Confused character will always carry out the last command they were asked to irregardless; but it will always be against you.

| Visuals      | Character continually spins in place                                                                                   |
|--------------|------------------------------------------------------------------------------------------------------------------------|
| Effects:     | Character randomly attacks allies                                                                                      |
| Duration     | Until end of battle                                                                                                    |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Peace Ring, Contain+Added<br>Effect, Mystify+Added Effect, Hades+Added Effect |
| Cured by     | Any Physical Hit, Esuna, Remedy, White Wind, Angel Whisper                                                             |

#### Silence

The power of this affliction is often underestimated. While under its influence, you are unable to cast any Magic, Enemy Skills or Summons. However, your other commands are untouched. Its usefulness lies in using it on the enemy; many of them have attacks that would be better left sealed with Silence.

| Visuals      | Character kneels/has speech bubble over head                                      |
|--------------|-----------------------------------------------------------------------------------|
| Effects:     | Character cannot use Magic/Enemy<br>Skills/Summons                                |
| Duration     | Until end of battle                                                               |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon,<br>Seal+Added Effect, Hades+Added Effect |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper,<br>Echo Screen                          |

#### Haste

One of the best Status Attributes, Haste has your time bar filling up twice as fast as normal. However, on the flip-side, all timed effects like Slow-numb, Barrier and so forth, will run out twice as quickly. But, the pros far outweigh the cons in this instance.

| Visuals      | Character Animation speed doubled |
|--------------|-----------------------------------|
| Effects:     | Time Unit speed doubled           |
| Duration     | Until end of battle               |
| Protected by | 'Petrify', 'Peerless', 'Resist'   |
| Cured by     | DeSpell                           |

#### Slow

The complete opposite of Haste, Slow causes your time bar to fill up twice as slow as normal. But, it has its good side; Barrier, MBarrier, Slow-numb, Death-sentence... all those take far longer to run out of time.

| Visuals      | Character Animation speed halved                   |
|--------------|----------------------------------------------------|
| Effects:     | Time Unit speed halved                             |
| Duration     | Until end of battle                                |
| Protected by | 'Petrify', 'Peerless', 'Resist', Time+Added Effect |
| Cured by     | DeSpell, White Wind, Angel Whisper                 |

#### Stop

The second worst of the four temporary 'Can't Act' Status Attributes, Stop completely shuts off the Time counter for that character. However, on the other hand, things like Barrier, MBarrier, Regen and so on will not count down during this time, until Stop has worn off or it's been dispelled.

| Visuals      | Character Animation speed paused                                                                       |
|--------------|--------------------------------------------------------------------------------------------------------|
| Effects:     | Time Unit speed reduced to zero<br>Character cannot Act                                                |
| Duration     | 15 units                                                                                               |
| Protected by | 'Petrify', 'Peerless', 'Resist', Contain+Added<br>Effect, Time+Added EFfect, Choco/Mog+Added<br>Effect |
| Cured by     | DeSpell, White Wind, Angel Whisper                                                                     |

#### Frog

Perhaps the worst of the transformation Statuses, Frog both reduces your attack power, as well as preventing you from using almost all of your Materia. The only options available to you are Fight, Item, and if you have it equipped, the Magic Spell 'Toad'. You can't even perform Limit Breaks while transformed into a frog.

| Visuals      | Character is a frog!                                                                                                            |
|--------------|---------------------------------------------------------------------------------------------------------------------------------|
| Effects:     | All Physical attacks do 1/4 of Base Damage<br>Character can only use Fight (not Limit), Item<br>(including W-Item) or cast Toad |
| Duration     | Until end of battle                                                                                                             |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, White<br>Cape,Transform+Added Effect, Hades+Added Effect                               |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper, Toad,<br>Maiden's Kiss, Impaler                                                       |

#### Small

While not as bad as Frog, this is still a terrible condition. While Magic is still wide open to you, every physical attack you do will have an Attack of 0; you will do 1 HP damage until modifications added after the random variation are added. Elemental attacks and Added Damage Effects will use the 1 HP damage as the basis for their calculations.

| Visuals      | Character size is significantly reduced                                                           |  |  |
|--------------|---------------------------------------------------------------------------------------------------|--|--|
| Effects:     | Character Attack reduced to 0                                                                     |  |  |
| Duration     | Until end of battle                                                                               |  |  |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, White<br>Cape,Transform+Added Effect, Hades+Added Effect |  |  |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper, Mini,<br>Cornucopia, Shrivel                            |  |  |

#### Slow-numb

One of the banes of the beginner player, Slow-numb can easily take out a character within moments if you're not prepared for it. Essentially, it's a countdown to petrify; you have 30 units of time (as shown by the counter above the character's head) to cure them of the affliction, or end the battle. Otherwise, they are inflicted by the Status Petrify.

| Visuals      | Character has timer above head/flashes Grey                                               |
|--------------|-------------------------------------------------------------------------------------------|
| Effects:     | 30-unit Timer set on character<br>When Timer reaches 0, Petrify is inflicted on character |
| Duration     | 30 units                                                                                  |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Jem Ring, Safety Bit                             |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper, Soft                                            |

### Petrify

Completely turned to stone, this is a very bad Status Attribute to earn. You can't act, and even worse, you're flagged as 'Dead'; if everyone in your party is flagged as 'Dead', then the game is over. However, it's easily curable, and while Petrified, you cannot be inflicted with any other Status Attributes, or take damage in any way at all. However, that also means you can't have damage healed while Petrified either.

| Visuals      | Character Animation speed paused/Character coloured Grey                                           |
|--------------|----------------------------------------------------------------------------------------------------|
| Effects:     | Character cannot Act<br>Character flagged as 'Dead'<br>Voids all damage<br>Prevents Status changes |
| Duration     | Until end of battle                                                                                |
| Protected by | 'Peerless', 'Resist', Ribbon, Jem Ring, Safety Bit,<br>Contain+Added Effect                        |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper, Soft                                                     |

#### Regen

An alternative to the standard healing spells, Regen has the potential to be greater than any of them, for half the cost of Cure3. However, its healing ability takes place over time, and it heals at a rate proportional to your current Max HP value. In addition, it has a short duration, and it can be DeSpelled.

| Visuals |              | Character flashes Orange                                                              |
|---------|--------------|---------------------------------------------------------------------------------------|
|         | Effects:     | Character steadily gains approximately 1/32 of<br>their Max HP over each unit of time |
|         | Duration     | 32 units                                                                              |
|         | Protected by | 'Petrify', 'Peerless', 'Resist'                                                       |
|         | Cured by     | DeSpell                                                                               |

#### Barrier

A protective Status Attribute, and the first available to you. It halves the damage from all Physical attacks, but it has a limited duration. The time left for Barrier can be checked in the Barrier gauge in the left window, next to the character name.

| Visuals      | Barrier gauge is active         |
|--------------|---------------------------------|
| Effects:     | Halves all Physical damage      |
| Duration     | 30 units                        |
| Protected by | 'Petrify', 'Peerless', 'Resist' |
| Cured by     | DeBarrier, DeSpell              |

#### MBarrier

The counterpart of Barrier, MBarrier simply halves the damage from all Magical attacks. Again, it only has a limited duration; the time left for MBarrier can be checked in the MBarrier gauge in the left window, next to the Character name.

| Visuals      | MBarrier gauge is active        |
|--------------|---------------------------------|
| Effects:     | Halves all Magical damage       |
| Duration     | 30 units                        |
| Protected by | 'Petrify', 'Peerless', 'Resist' |
| Cured by     | DeBarrier, DeSpell              |

#### Reflect

One of the most interesting Status Attributes, Reflect allows you to bounce away certain spells up to a maximum of four times per casting per character. A list of spells that cannot be reflected can be located in the next section.

| Visuals      | None                                                                                                                                     |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Effects:     | Will reflect spells up to four times back at<br>caster, or random enemy if caster is an ally<br>Will only reflect certain magical spells |
| Duration     | Until end of battle or exhausted                                                                                                         |
| Protected by | 'Petrify', 'Peerless', 'Resist'                                                                                                          |
| Cured by     | DeBarrier, DeSpell                                                                                                                       |

#### Shield

A very powerful defensive Status Attribute, second only to Peerless. It voids all normal attacks, and absorbs all Elemental Magic. However, it will not absorb Non-Elemental damage, and also, Items seem able to breach Shield and still cause full damage, whether they're Elemental items or not.

| Visuals      | None                                                                                                                                       |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Effects:     | Voids normal attacks<br>Absorbs Elemental Magic and Physical damage<br>Does not defend against Item damage or Non<br>Element Magic attacks |
| Duration     | 17.5 units                                                                                                                                 |
| Protected by | 'Petrify', 'Resist'                                                                                                                        |
| Cured by     | DeBarrier, DeSpell                                                                                                                         |

#### Death-sentence

Under this condition, a counter positioned above the character's head begins to count down to zero. If it does reach zero, then the Status Death is inflicted on the character, subject to protection from Death.

| Visuals      | Character kneels/has timer above head                                                   |
|--------------|-----------------------------------------------------------------------------------------|
| Effects:     | 60-unit Timer set on character<br>When Timer reaches 0, Death is inflicted on character |
| Duration     | 60 units                                                                                |
| Protected by | 'Petrify', 'Peerless', 'Resist', 'Death Force', Ribbon,<br>Safety Bit                   |
| Cured by     | None                                                                                    |

#### Manipulate

The only Status Attribute that cannot be used on your party, Manipulate is a very useful tool. Using it on an enemy, if they're susceptible to it, will place the enemy under the character's command. Note that each character can only Manipulate one enemy at a time, and a single Physical hit will free the enemy from your control.

| Visuals      | Character flashes Cyan                                         |
|--------------|----------------------------------------------------------------|
| Effects:     | Character is controlled by whomever used<br>Manipulate on them |
| Duration     | Until end of battle                                            |
| Protected by | 'Petrify', 'Resist', 'Sleep', 'Stop', 'Paralysed'              |
| Cured by     | Any Physical hit, White Wind                                   |

#### Berserk

This is a very risky Status Attribute. On the plus side, a character under this Attribute hits harder than usual with every attack. But on the minus, they cannot be controlled, and they randomly attack the enemy any time they can. It is also impossible to Critical Strike when under Berserk Status. Berserk has another use; it's an effective alternative to Silence when used on the enemy....

| Visuals      | Character flashes Red                                                                                                                         |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Effects:     | Character's Physical Damage is multiplied by 1.5<br>Character attacks random Enemy with Physical Attack<br>Impossible to get Critical Strikes |
| Duration     | Until end of battle                                                                                                                           |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Peace Ring,<br>Mystify+Added Effect                                                                  |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper                                                                                                      |

#### Peerless

The ultimate defensive Status Attribute. Unfortunately, only one character has the ability to use this: Aeris. When used, it fully voids all damage of any type, as well as acting like Resist with regards to Status Attributes. However, it has a limited duration, and the Void state makes it impossible to heal while under it, but it is still a formidable Attribute.

| Visuals      | Character flashes Yellow                            |
|--------------|-----------------------------------------------------|
| Effects:     | Voids all damage<br>Immune to all Status Attributes |
| Duration     | 17.5 units                                          |
| Protected by | 'Petrify', 'Resist'                                 |
| Cured by     | None                                                |

#### Paralysed

The least powerful of the temporary 'Can't Act' Status Attributes, it's still a pain at times. It acts almost exactly like Sleep and while it lasts for a very short time, you can't cure it with a simple Physical attack.

| Visuals      | Character kneels/Character animation speed paused |
|--------------|---------------------------------------------------|
| Effects:     | Character cannot Act                              |
| Duration     | 8 units                                           |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Jem Ring |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper          |

#### Darkness

A nuisance at best, Darkness simply reduces your attack accuracy, causing you to miss more often. It's easily cured, however, and it has little tactical use.

| Visuals      | Character kneels/flashes Black                                      |
|--------------|---------------------------------------------------------------------|
| Effects:     | Character Accuracy% reduced                                         |
| Duration     | Until end of battle                                                 |
| Protected by | 'Petrify', 'Peerless', 'Resist', Ribbon, Silver Glasses, Fairy Ring |
| Cured by     | Esuna, Remedy, White Wind, Angel Whisper, Eye drop                  |

### Dual

This extremely rare Status only turns up during one battle; that with Bottomswell. Whenever Bottomswell uses Waterpolo at you, both Imprisoned and Dual are placed on you. Dual is dangerous however; it acts like a reverse Regen. HP is drained over time, requiring swift attention.

| Visuals      | None                                                                                  |
|--------------|---------------------------------------------------------------------------------------|
| Effects:     | Character steadily loses approximately 1/32 of<br>their Max HP over each unit of time |
| Duration     | ???                                                                                   |
| Protected by | ???                                                                                   |
| Cured by     | Killing Waterpolo                                                                     |

#### Death Force

A useful status, which allows you to temporarily give yourself protection from Death until the end of the battle. Its usefulness stems from the fact that very few enemies actually use the Death Status. Recognize them, and you can possibly spare an Accessory slot or a few Materia slots and just rely on Death Force for protection when you need it. Of course, the disadvantage is that the immunity is temporary; if that character gets hit by DeSpell or White Wind or gets killed, then they will lose the immunity immediately.

| Visuals      | None                |
|--------------|---------------------|
| Effects:     | Immune 'Death'      |
| Duration     | Until end of battle |
| Protected by | ???                 |
| Cured by     | DeSpell, White Wind |

#### Resist

You are never given any indication of when you have Resist, but its effects are quickly apparent; any Status change is prevented by the power of Resist. Unfortunately, that can also mean, for example, if you have Frog and then Resist is placed on you, you cannot then cure Frog without removing Resist first. Its best use is to trap enemies with certain Status Attributes so that they can't heal themselves. As a secondary use, it can be used as a temporary defense against nasty Statuses, but it's expensive, and not easy to remove.

| Visuals      | None                            |
|--------------|---------------------------------|
| Effects:     | Immune to all Status Attributes |
| Duration     | Until end of battle             |
| Protected by | None                            |
| Cured by     | DeSpell, White Wind             |

#### Lucky Girl

Only one attack in the game can inflict this Status: Lucky Girl. This is one of the Limit Combinations in Cait Sith's Slot Limit. It is a somewhat useful status, causing all subsequent attacks to be Critical Strikes. However, this is offset by its rarity; most players will go through the game without ever seeing Lucky Girl.

| Visuals      | None                                       |
|--------------|--------------------------------------------|
| Effects:     | All attacks are automatic Critical Strikes |
| Duration     | ???                                        |
| Protected by | ???                                        |
| Cured by     | None                                       |

#### Imprisoned

The final temporary 'Can't Act' Status. Unfortunately, the temporary nature of this status is dependant on what is causing it; various enemies have a few ways of dealing out this attribute, and each requires its own method of removing it. In addition, the character is flagged as 'Dead'. It is easily the worst of the four 'Can't Act' Statuses.

| Visuals      | Character Animation speed paused                                                                      |
|--------------|-------------------------------------------------------------------------------------------------------|
| Effects:     | Character cannot Act<br>Character flagged as 'Dead'<br>Character cannot be targeted by attacks/spells |
| Duration     | Until end of battle                                                                                   |
| Protected by | None                                                                                                  |
| Cured by     | Killing Pyramid, Waterpolo or Left Arm/Right Arm                                                      |

#### **4.2 Special Notes On Statuses**

In addition to the above, the following notes must be taken into account.

#### Colours

The different colors you flash have a priority system; if you currently have a Status that has a higher priority than another one you have, then you will flash the color of the higher priority Status. The priorities are:

| Highest Priority |        |         |          | Lowest Priority |          |        |            |  |
|------------------|--------|---------|----------|-----------------|----------|--------|------------|--|
| Slow-numb        | Poison | Berserk | Peerless |                 | Darkness | Regen  | Manipulate |  |
| GREY             | GREEN  | RED     | YELLOW   |                 | BLACK    | ORANGE | CYAN       |  |

Thus, if your character has both Darkness and Berserk on them, they'll flash Red rather than Black, because Berserk is the more important one to know about. (For instance, you don't want to mistake Slow-numb for Death-sentence just because you've got Regen on, do you?)

#### Status Incompatibilities

Various statuses will cancel out other ones as soon as they're inflicted upon a character. The following table will demonstrate this:

| Status Name | Cancels                                     |
|-------------|---------------------------------------------|
| Death       | All Status Attributes except Frog and Small |
| Sleep       | Manipulate                                  |
| Sadness     | Fury                                        |
| Fury        | Sadness                                     |
| Haste       | Slow                                        |
| Slow        | Haste                                       |
| Stop        | Manipulate                                  |

| Status Name | Cancels               |
|-------------|-----------------------|
| Petrify     | Slow-numb, Manipulate |
| Paralysed   | Manipulate            |

#### Removing Conditions

What follows are the various ways of removing multiple Status Attributes at the same time. Those not listed are self-explanatory (ie they tell you what they cure. Also, if something cures Petrify, then it also cures Slow-numb)

Note: Healing spells and effects work in strict order, first healing HP, then removing Status Attributes from the top down. Thus, White Wind takes two tries to be able to remove, for example, Frog and Resist; the first time, it can't remove Frog because of Resist. The second try, Resist is gone, so it can finally remove Frog. Keep this in mind.

| Status Name    | Esuna | Remedy | DeBarrier | DeSpell | White Wind | Angel Whisper |
|----------------|-------|--------|-----------|---------|------------|---------------|
| Death          | -     | -      | -         | -       | -          | O             |
| Sleep          | O     | O      | -         | -       | O          | O             |
| Poison         | O     | O      | -         | -       | O          | O             |
| Sadness        | O     | O      | -         | -       | -          | -             |
| Fury           | O     | O      | -         | -       | -          | -             |
| Confusion      | O     | O      | -         | -       | O          | O             |
| Silence        | O     | O      | -         | -       | O          | O             |
| Haste          | -     | -      | -         | O       | -          | -             |
| Slow           | -     | -      | -         | O       | O          | O             |
| Stop           | -     | -      | -         | O       | O          | O             |
| Frog           | O     | O      | -         | -       | O          | O             |
| Small          | O     | O      | -         | -       | O          | O             |
| Slow-numb      | O     | O      | -         | -       | O          | O             |
| Petrify        | O     | O      | -         | -       | O          | O             |
| Regen          | -     | -      | -         | O       | -          | -             |
| Barrier        | -     | -      | O         | O       | -          | -             |
| MBarrier       | -     | -      | O         | O       | -          | -             |
| Reflect        | -     | -      | O         | O       | -          | -             |
| Shield         | -     | -      | O         | O       | -          | -             |
| Death-sentence | -     | -      | -         | -       | -          | -             |
| Manipulate     | -     | -      | -         | -       | O          | -             |

| Status Name | Esuna | Remedy | DeBarrier | DeSpell | White Wind | Angel Whisper |
|-------------|-------|--------|-----------|---------|------------|---------------|
| Berserk     | O     | O      | -         | -       | O          | O             |
| Peerless    | -     | -      | -         | -       | -          | -             |
| Paralysed   | O     | O      | -         | -       | O          | O             |
| Darkness    | O     | O      | -         | -       | O          | O             |
| Death Force | -     | -      | -         | O       | O          | -             |
| Resist      | -     | -      | -         | O       | O          | -             |

Note: Due to space constraints, it is difficult to fit any more abilities onto the above list. What's shown above are the most common ways of removing multiple statuses. The others can be summarized as such:

Holy Torch: Cures everything DeSpell does except 'Death Force' and 'Resist'.

#### Reflection

Finally, the following skills can be reflected using the Status Reflect.

#### Magic:

| Cure   | Cure2 | Cure3 | Poisona | Esuna    | Resist | Life    | Life2 | Regen   | Fire    |
|--------|-------|-------|---------|----------|--------|---------|-------|---------|---------|
| Fire2  | Fire3 | Ice   | Ice2    | Ice3     | Bolt   | Bolt2   | Bolt3 | Quake   | Quake2  |
| Quake3 | Bio   | Bio2  | Bio3    | Sleepel  | Confu  | Silence | Mini  | Toad    | Berserk |
| Haste  | Slow  | Stop  | Barrier | MBarrier | Death  | Freeze  | Break | Tornado | Flare   |
| Wall   |       |       |         |          |        |         |       |         |         |

#### Enemy Skills:

| Frog Song | L4 Suicide  | Magic Hammer | Death Force  | Flame Thrower |
|-----------|-------------|--------------|--------------|---------------|
| Laser     | Matra Magic | Aqualung     | Shadow Flare | Pandora's Box |

All Summons and Items are non-reflectable. As a companion to this section, here are the specific Magic and Enemy Skills that *CANNOT* be reflected.

#### Magic:

| Demi   | Demi2  | Demi3 | Reflect | DeBarrier | DeSpell |
|--------|--------|-------|---------|-----------|---------|
| Escape | Remove | Comet | Comet2  | FullCure  | Shield  |
| Ultima |        |       |         |           |         |

#### Enemy Skills:

| White Wind   | Big Guard | Angel Whisper | Dragon Force | Bad Breath | Beta           | Trine    |
|--------------|-----------|---------------|--------------|------------|----------------|----------|
| Magic Breath | ????      | Goblin Punch  | Chocobuckle  | L5 Death   | Death Sentence | Roulette |

#### **5. GAME OVER**

There are a number of ways to lose the game, most of which can only occur in battle.

The most common way is to have all three characters in your battle party flagged as 'Dead'. This involves losing each of your characters to any of the following situations:

- 1. Gaining the Status 'Death'
- 2. Gaining the Status 'Petrify'
- 3. Gaining the Status 'Imprisoned'

(This occurs if you are either picked up by one of Carry Armor's arms, or you are surrounded by Reno's Pyramid or Bottomswell's Waterpolo. You must destroy whatever is imprisoning the character to bring them back)

4. Being knocked out of battle by Eat (used by Hungry), Goanni (used by Ghost Ship) or Whirlsand (used by Ruby Weapon). Midgar Zolom's Blown Away, Scissors(Upper)'s Scissor Tornado and Gighee's Sun Diver all knock you out of battle, but flag the character as escaped instead of dead; so instead, if all other characters die or are knocked out, the battle itself will count as an escape.

If you are still flagged as 'Dead' at the end of a successful battle, then that character will gain no EXP or AP from the battle. However, the Status 'Death' is the only one that lasts into the next battle if you don't cure it.

You will also lose the battle in one other special case: running out of time in the Emerald Weapon battle. This only occurs if you do not have the Underwater Materia equipped during that battle, however.

Note that if you lose a battle in Battle Square, the Five Gods Pagoda or Fort Condor, you won't lose the game, just the battle. In all other cases, losing a battle means 'Game Over'.

Finally, if you run out of time in the Mako Reactor 1 Mission, you will automatically lose the game, without having to be in battle.

#### **6. CREDITS**

A large majority of the work here is my own... but there are some people that I feel it is necessary to mention on this long road.

The Denizens of alt.games.final-fantasy.rpg:

My old haunt. More a shout-out rather than credit, but hey, it's where I began, really ^\_^ It's also where I met...

#### Qhimm:

 ...with whom I worked on the FF8 savemap with. Lots of fun, and we actually got something useful out of it: a working save editor that he programmed named Griever. It was also on his site that met others who took the same interest in this field. Which leads to....

The Denizens of Qhimm's Forum:

The SaiNt. Ficedula. Alhexx. And \*especially\* L.Spiro. There were others, of course, but those are

the names who stand out. Enemy Stats and Attack Properties would've been hell to compile without the effort made by those at Qhimm's Forum. I collected data myself, but understanding it? L.Spiro provided the first and most important step in deciphering the attack and enemy dumps.

And... that's that, really. Hope you've enjoyed the show.

**The FF7 Battle Mechanics, copyright 2001-2003 Terence Fergusson**

#### **FF7 Party Mechanics**

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

#### **FF7 Enemy Mechanics**

#### **The Battle Scene**

#### **1. ENEMY BATTLE SCENES (SCENE.BIN)**

FF7 keeps each enemy battle configuration is a file called "scene.bin" This file is located in the following directories.

| PSX Version            | PC Version        |  |  |
|------------------------|-------------------|--|--|
| /DATA/BATTLE/SCENE.BIN | /BATTLE/SCENE.BIN |  |  |

This file is exactly the same in both versions. This holds all the battle configurations for all enemies encountered in the game. It's format is as follows:

#### **1.1 Scene.bin file format by Fremen**

Date : September 30, 2003

These specifications are incomplete, so if you have got any idea about the unknown data blocks, please let me know. :)

The scene.bin file contains 256 gziped files which give us information for all the FF7 monsters. In order to find these files in scene.bin, you have to know that the file is structured with blocks exactly 0x2000 bytes in length. In the first table (scene.bin block), you will see what contains a block. Blocks are concatenated with each other to form the scene.bin file. So if you want to extract data from scene.bin, you'll need to find the correct blocks and to extract the gziped files from it. After that you simply ungzip those files and you'll find 256 files, with a length is 7808 bytes. Known information about those files can be found in the second table (The Data File specification).

We have 1024 possible battle numbers: 0 - 1023. Each group of \*4\* Battle Numbers refers to a particular Scene file: for instance, Battles 0-3 refer to File 0 in Scene.bin, Battles 4-7 refer to File 1 in Scene.bin, and so forth.

Scene.bin block (length : 0x2000 bytes)

| Offset | Length  | Description                                                           |  |  |
|--------|---------|-----------------------------------------------------------------------|--|--|
| 0x0000 | 4 bytes | Pointer (in DWORD) of the first data file. Example :                  |  |  |
|        |         | Offset_of_first_data_file_in_bytes = pointer*4                        |  |  |
|        |         | pointer = 0xFFFFFFFF means that the end of block has been<br>reached. |  |  |
| 0x0004 | 4 bytes | Second pointer of the second data file.                               |  |  |
|        |         | pointer = 0xFFFFFFFF means that the end of block has been<br>reached. |  |  |
|        |         |                                                                       |  |  |
| 0x003C | 4 bytes | Last pointer. Usually 0xFFFFFFFF.                                     |  |  |

| Offset          | Length                                | Description                                                                              |
|-----------------|---------------------------------------|------------------------------------------------------------------------------------------|
| 0x0040          | 4 * (pointer2-<br>pointer1) bytes     | First data file in block. It's a gziped file.                                            |
|                 |                                       | Note : Sometimes it may finish by 0xFF bytes, because its size<br>must be multiple of 4. |
| pointer2 * 4    | 4 * (pointer3-                        | Second data file in block. It's a gziped file.                                           |
|                 | pointer2) bytes                       | Note : Sometimes it may finish by 0xFF bytes, because its size<br>must be multiple of 4. |
| lastpointer * 4 | 4 * (0x2000-<br>lastpointer)<br>bytes | Last data file.                                                                          |
|                 |                                       | Note : There's usually about 10 files in each block.                                     |
|                 |                                       | Note : Each block finishes by 0xFF bytes, because its length must<br>be 0x2000 bytes.    |

Data File specifications (length : 7808 bytes)

| Offset | Length   | Description                  |
|--------|----------|------------------------------|
| 0x0000 | 2 bytes  | Enemy ID 1                   |
| 0x0002 | 2 bytes  | Enemy ID 2                   |
| 0x0004 | 2 bytes  | Enemy ID 3                   |
| 0x0006 | 2 bytes  | Padding (always 0xFFFF)      |
| 0x0008 | 20 bytes | Battle set up 1, record 1    |
| 0x001C | 20 bytes | Battle set up 1, record 2    |
| 0x0030 | 20 bytes | Battle set up 1, record 3    |
| 0x0044 | 20 bytes | Battle set up 1, record 4    |
| 0x0058 | 48 bytes | Battle Setup 2, record 1     |
| 0x0088 | 48 bytes | Battle Setup 2, record 2     |
| 0x00B8 | 48 bytes | Battle Setup 2, record 3     |
| 0x00E8 | 48 bytes | Battle Setup 2, record 4     |
| 0x0118 | 16 bytes | Battle Formation 1, record 1 |
| 0x0128 | 16 bytes | Battle Formation 1, record 2 |
| 0x0138 | 16 bytes | Battle Formation 1, record 3 |
| 0x0148 | 16 bytes | Battle Formation 1, record 4 |
| 0x0158 | 16 bytes | Battle Formation 1, record 5 |
| 0x0168 | 16 bytes | Battle Formation 1, record 6 |
| 0x0178 | 16 bytes | Battle Formation 2, record 1 |
| 0x0188 | 16 bytes | Battle Formation 2, record 2 |
| 0x0198 | 16 bytes | Battle Formation 2, record 3 |
| 0x01A8 | 16 bytes | Battle Formation 2, record 4 |
| 0x01B8 | 16 bytes | Battle Formation 2, record 5 |

| Offset | Length    | Description                  |
|--------|-----------|------------------------------|
| 0x01C8 | 16 bytes  | Battle Formation 2, record 6 |
| 0x01D8 | 16 bytes  | Battle Formation 3, record 1 |
| 0x01E8 | 16 bytes  | Battle Formation 3, record 2 |
| 0x01F8 | 16 bytes  | Battle Formation 3, record 3 |
| 0x0208 | 16 bytes  | Battle Formation 3, record 4 |
| 0x0218 | 16 bytes  | Battle Formation 3, record 5 |
| 0x0228 | 16 bytes  | Battle Formation 3, record 6 |
| 0x0238 | 16 bytes  | Battle Formation 4, record 1 |
| 0x0248 | 16 bytes  | Battle Formation 4, record 2 |
| 0x0258 | 16 bytes  | Battle Formation 4, record 3 |
| 0x0168 | 16 bytes  | Battle Formation 4, record 4 |
| 0x0278 | 16 bytes  | Battle Formation 3, record 5 |
| 0x0288 | 16 bytes  | Battle Formation 4, record 6 |
| 0x0298 | 184 bytes | Enemy Data 1                 |
| 0x0350 | 184 bytes | Enemy Data 2                 |
| 0x0408 | 184 bytes | Enemy Data 3                 |
| 0x04C0 | 28 bytes  | Attack Data 1                |
| 0x04DC | 28 bytes  | Attack Data 2                |
| 0x04F8 | 28 bytes  | Attack Data 3                |
| 0x0514 | 28 bytes  | Attack Data 4                |
| 0x0530 | 28 bytes  | Attack Data 5                |
| 0x054C | 28 bytes  | Attack Data 6                |
| 0x0568 | 28 bytes  | Attack Data 7                |
| 0x0584 | 28 bytes  | Attack Data 8                |
| 0x05A0 | 28 bytes  | Attack Data 9                |
| 0x05BC | 28 bytes  | Attack Data 10               |
| 0x05BC | 28 bytes  | Attack Data 11               |
| 0x05F4 | 28 bytes  | Attack Data 12               |
| 0x0610 | 28 bytes  | Attack Data 13               |
| 0x062C | 28 bytes  | Attack Data 14               |
| 0x0648 | 28 bytes  | Attack Data 15               |
| 0x0664 | 28 bytes  | Attack Data 16               |
| 0x0680 | 28 bytes  | Attack Data 17               |
| 0x069C | 28 bytes  | Attack Data 18               |

| Offset | Length   | Description    |
|--------|----------|----------------|
| 0x06B8 | 28 bytes | Attack Data 19 |
| 0x06D4 | 28 bytes | Attack Data 20 |
| 0x06F0 | 28 bytes | Attack Data 21 |
| 0x070C | 28 bytes | Attack Data 22 |
| 0x0728 | 28 bytes | Attack Data 23 |
| 0x0744 | 28 bytes | Attack Data 24 |
| 0x0760 | 28 bytes | Attack Data 25 |
| 0x077C | 28 bytes | Attack Data 26 |
| 0x0798 | 28 bytes | Attack Data 27 |
| 0x07B4 | 28 bytes | Attack Data 28 |
| 0x07D0 | 28 bytes | Attack Data 29 |
| 0x07EC | 28 bytes | Attack Data 30 |
| 0x0808 | 28 bytes | Attack Data 31 |
| 0x0824 | 28 bytes | Attack Data 32 |
| 0x0840 | 2 bytes  | Attack ID 1    |
| 0x0842 | 2 bytes  | Attack ID 2    |
| 0x0844 | 2 bytes  | Attack ID 3    |
| 0x0846 | 2 bytes  | Attack ID 4    |
| 0x0848 | 2 bytes  | Attack ID 5    |
| 0x084A | 2 bytes  | Attack ID 6    |
| 0x084C | 2 bytes  | Attack ID 7    |
| 0x084E | 2 bytes  | Attack ID 8    |
| 0x0850 | 2 bytes  | Attack ID 9    |
| 0x0852 | 2 bytes  | Attack ID 10   |
| 0x0854 | 2 bytes  | Attack ID 11   |
| 0x0856 | 2 bytes  | Attack ID 12   |
| 0x0858 | 2 bytes  | Attack ID 13   |
| 0x085A | 2 bytes  | Attack ID 14   |
| 0x085C | 2 bytes  | Attack ID 15   |
| 0x085E | 2 bytes  | Attack ID 16   |
| 0x0860 | 2 bytes  | Attack ID 17   |
| 0x0862 | 2 bytes  | Attack ID 18   |
| 0x0864 | 2 bytes  | Attack ID 19   |
| 0x0866 | 2 bytes  | Attack ID 20   |

| Offset | Length   | Description              |
|--------|----------|--------------------------|
| 0x0868 | 2 bytes  | Attack ID 21             |
| 0x086A | 2 bytes  | Attack ID 22             |
| 0x086C | 2 bytes  | Attack ID 23             |
| 0x086E | 2 bytes  | Attack ID 24             |
| 0x0870 | 2 bytes  | Attack ID 25             |
| 0x0872 | 2 bytes  | Attack ID 26             |
| 0x0874 | 2 bytes  | Attack ID 27             |
| 0x0876 | 2 bytes  | Attack ID 28             |
| 0x0878 | 2 bytes  | Attack ID 29             |
| 0x087A | 2 bytes  | Attack ID 30             |
| 0x087C | 2 bytes  | Attack ID 31             |
| 0x087E | 2 bytes  | Attack ID 32             |
| 0x0880 | 32 bytes | Attack name 1 (FF Text)  |
| 0x08A0 | 32 bytes | Attack name 2 (FF Text)  |
| 0x08C0 | 32 bytes | Attack name 3 (FF Text)  |
| 0x08E0 | 32 bytes | Attack name 4 (FF Text)  |
| 0x0900 | 32 bytes | Attack name 5 (FF Text)  |
| 0x0920 | 32 bytes | Attack name 6 (FF Text)  |
| 0x0940 | 32 bytes | Attack name 7 (FF Text)  |
| 0x0960 | 32 bytes | Attack name 8 (FF Text)  |
| 0x0980 | 32 bytes | Attack name 9 (FF Text)  |
| 0x09A0 | 32 bytes | Attack name 10 (FF Text) |
| 0x09C0 | 32 bytes | Attack name 11 (FF Text) |
| 0x09E0 | 32 bytes | Attack name 12 (FF Text) |
| 0x0A00 | 32 bytes | Attack name 13 (FF Text) |
| 0x0A20 | 32 bytes | Attack name 14 (FF Text) |
| 0x0A40 | 32 bytes | Attack name 15 (FF Text) |
| 0x0A60 | 32 bytes | Attack name 16 (FF Text) |
| 0x0A80 | 32 bytes | Attack name 17 (FF Text) |
| 0x0AA0 | 32 bytes | Attack name 18 (FF Text) |
| 0x0AC0 | 32 bytes | Attack name 19 (FF Text) |
| 0x0AE0 | 32 bytes | Attack name 20 (FF Text) |
| 0x0B00 | 32 bytes | Attack name 21 (FF Text) |
| 0x0B20 | 32 bytes | Attack name 22 (FF Text) |

| Offset | Length     | Description               |
|--------|------------|---------------------------|
| 0x0B40 | 32 bytes   | Attack name 23 (FF Text)  |
| 0x0B60 | 32 bytes   | Attack name 24 (FF Text)  |
| 0x0B80 | 32 bytes   | Attack name 25 (FF Text)  |
| 0x0BA0 | 32 bytes   | Attack name 26 (FF Text)  |
| 0x0BC0 | 32 bytes   | Attack name 27 (FF Text)  |
| 0x0BE0 | 32 bytes   | Attack name 28 (FF Text)  |
| 0x0C00 | 32 bytes   | Attack name 29 (FF Text)  |
| 0x0C20 | 32 bytes   | Attack name 30 (FF Text)  |
| 0x0C40 | 32 bytes   | Attack name 31 (FF Text)  |
| 0x0C60 | 32 bytes   | Attack name 32 (FF Text)  |
| 0x0C80 | 512 bytes  | FF Padding (0xFF)         |
| 0x0E80 | 2 bytes    | Enemy AI Offset, record 1 |
| 0x0E82 | 2 bytes    | Enemy AI Offset, record 2 |
| 0x0E84 | 2 bytes    | Enemy AI Offset, record 3 |
| 0x0E86 | 26 bytes   | Unknown                   |
| 0x0EA0 | 4063 bytes | Beginning of AI Data      |
|        |            | Starts with 6 bytes of FF |

Battle Setup 1 Record format (length : 16 bytes)

| Offset | Length  | Description                                 |
|--------|---------|---------------------------------------------|
| 0x0000 | 2 bytes | Battle Location, description is as follows: |
|        |         | 0x0000: Blank                               |
|        |         | 0x0001: Bizarro Battle - Center             |
|        |         | 0x0002: Grassland                           |
|        |         | 0x0003: Mt Nibel                            |
|        |         | 0x0004: Forest                              |
|        |         | 0x0005: Beach                               |
|        |         | 0x0006: Desert                              |
|        |         | 0x0007: Snow                                |
|        |         | 0x0008: Swamp                               |
|        |         | 0x0009: Sector 1 Train Station              |
|        |         | 0x000A: Reactor 1                           |
|        |         | 0x000B: Reactor 1 Core                      |
|        |         | 0x000C: Reactor 1 Entrance                  |
|        |         | 0x000D: Sector 4 Subway                     |

| 0x000E: Nibel Caves or AForest Caves<br>0x000F: Shinra HQ<br>0x0010: Midgar Raid Subway<br>0x0011: Hojo's Lab<br>0x0012: Shinra Elevators<br>0x0013: Shinra Roof<br>0x0014: Midgar Highway<br>0x0015: Wutai Pagoda<br>0x0016: Church<br>0x0017: Coral Valley<br>0x0018: Midgar Slums<br>0x0019: Sector 4 Corridors or Junon Path<br>0x001A: Sector 4 Gantries or Midgar Underground<br>0x001B: Sector 7 Support Pillar Stairway<br>0x001C: Sector 7 Support Pillar Top<br>0x001D: Sector 8<br>0x001E: Sewers<br>0x001F: Mythril Mines<br>0x0020: Northern Crater - Floating Platforms<br>0x0021: Corel Mountain Path<br>0x0022: Junon Beach<br>0x0023: Junon Cargo Ship | Offset | Length | Description |  |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------|-------------|--|
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |        |        |             |  |
| 0x0024: Corel Prison                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |        |        |             |  |
| 0x0025: Battle Square                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |        |        |             |  |
| 0x0026: Da Chao - Rapps Battle                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |        |        |             |  |
| 0x0027: Cid's Backyard                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |        |        |             |  |
| 0x0028: Final Descent to Sephiroth                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |        |        |             |  |
| 0x0029: Reactor 5 Entrance                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |        |        |             |  |
| 0x002A: Temple of the Ancients - Escher Room                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |        |        |             |  |
| 0x002B: Shinra Mansion                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |        |        |             |  |
| 0x002C: Junon Airship Dock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |        |        |             |  |
| 0x002D: Whirlwind Maze                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |        |        |             |  |
| 0x002E: Junon Underwater Reactor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |        |        |             |  |
| 0x002F: Gongaga Reactor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |        |        |             |  |

| Offset | Length | Description                                            |  |  |
|--------|--------|--------------------------------------------------------|--|--|
|        |        | 0x0030: Gelnika                                        |  |  |
|        |        | 0x0031: Train Graveyard                                |  |  |
|        |        | 0x0032: Great Glacier Ice Caves & Gaea Cliffs - Inside |  |  |
|        |        | 0x0033: Sister Ray                                     |  |  |
|        |        | 0x0034: Sister Ray Base                                |  |  |
|        |        | 0x0035: Forgotten City Altar                           |  |  |
|        |        | 0x0036: Northern Crater - Initial Descent              |  |  |
|        |        | 0x0037: Northern Crater - Hatchery                     |  |  |
|        |        | 0x0038: Northern Crater - Water Area                   |  |  |
|        |        | 0x0039: Safer Battle                                   |  |  |
|        |        | 0x003A: Kalm Flashback - Dragon Battle                 |  |  |
|        |        | 0x003B: Junon Underwater Pipe                          |  |  |
|        |        | 0x003C: Blank                                          |  |  |
|        |        | 0x003D: Corel Railway - Canyon                         |  |  |
|        |        | 0x003E: Whirlwind Maze - Crater                        |  |  |
|        |        | 0x003F: Corel Railway - Rollercoaster                  |  |  |
|        |        | 0x0040: Wooden Bridge                                  |  |  |
|        |        | 0x0041: Da Chao                                        |  |  |
|        |        | 0x0042: Fort Condor                                    |  |  |
|        |        | 0x0043: Dirt Wasteland                                 |  |  |
|        |        | 0x0044: Bizarro Battle - Right Side                    |  |  |
|        |        | 0x0045: Bizarro Battle - Left Side                     |  |  |
|        |        | 0x0046: Jenova*SYNTHESIS Battle                        |  |  |
|        |        | 0x0047: Corel Train Battle                             |  |  |
|        |        | 0x0048: Cosmo Canyon                                   |  |  |
|        |        | 0x0049: Caverns of the Gi                              |  |  |
|        |        | 0x004A: Nibelheim Mansion Basement                     |  |  |
|        |        | 0x004B: Temple of the Ancients - Demons Gate           |  |  |
|        |        | 0x004C: Temple of the Ancients - Mural Room            |  |  |
|        |        | 0x004D: Temple of the Ancients - Clock Passage         |  |  |
|        |        | 0x004E: Final Battle - Sephiroth                       |  |  |
|        |        | 0x004F: Jungle                                         |  |  |
|        |        | 0x0050: Ultimate Weapon - Battle on Highwind           |  |  |
|        |        | 0x0051: Corel Reactor                                  |  |  |
|        |        |                                                        |  |  |

| Offset | Length<br>Description |                                           |  |  |
|--------|-----------------------|-------------------------------------------|--|--|
|        |                       | 0x0052: Unused                            |  |  |
|        |                       | 0x0053: Don Corneo's Mansion              |  |  |
|        |                       | 0x0054: Emerald Weapon Battle             |  |  |
|        |                       | 0x0055: Reactor 5                         |  |  |
|        |                       | 0x0056: Shinra HQ - Escape                |  |  |
|        |                       | 0x0057: Ultimate Weapon - Gongaga Reactor |  |  |
|        |                       | 0x0058: Corel Prison - Dyne Battle        |  |  |
|        |                       | 0x0059: Ultimate Weapon - Forest          |  |  |
|        |                       |                                           |  |  |
| 0x0002 | 14 bytes              | Unknown                                   |  |  |

Enemy Data (length : 184 bytes)

| Offset | Length   | Description                            |                 |  |  |
|--------|----------|----------------------------------------|-----------------|--|--|
| 0x0000 | 32 bytes | Enemy's name (completed by 0xFF bytes) |                 |  |  |
| 0x0020 | 1 byte   | Enemy's level                          |                 |  |  |
| 0x0021 | 1 byte   | Enemy's speed                          |                 |  |  |
| 0x0022 | 1 byte   | Enemy's luck                           |                 |  |  |
| 0x0023 | 1 byte   | Enemy's physical dodge                 |                 |  |  |
| 0x0024 | 1 byte   | Enemy's strength                       |                 |  |  |
| 0x0025 | 1 byte   | Enemy's physical defense               |                 |  |  |
| 0x0026 | 1 byte   | Enemy's magic power                    |                 |  |  |
| 0x0027 | 1 byte   | Enemy's magic defense                  |                 |  |  |
| 0x0028 | 8 bytes  | Elements :                             |                 |  |  |
|        |          | 0x00 Fire                              | 0x08 Scare      |  |  |
|        |          | 0x01 Ice                               | 0x09 Health     |  |  |
|        |          | 0x02 Bolt                              | 0x0A Cut        |  |  |
|        |          | 0x03 Earth                             | 0x0B Hit        |  |  |
|        |          | 0x04 Bio                               | 0x0C Punch      |  |  |
|        |          | 0x05 Gravity                           | 0x0D Shoot      |  |  |
|        |          | 0x06 Water                             | 0x0E Scream     |  |  |
|        |          | 0x07 Wind                              | 0xFF No element |  |  |

| Offset | Length   | Description                                                                                  |  |  |  |
|--------|----------|----------------------------------------------------------------------------------------------|--|--|--|
| 0x0030 | 8 bytes  | Describes the link between the enemy and the previous<br>elements (respectively) as follows: |  |  |  |
|        |          | 0x00 Death                                                                                   |  |  |  |
|        |          | 0x02 Weakness (200% damage)                                                                  |  |  |  |
|        |          | 0x04 Resist (50% damage)                                                                     |  |  |  |
|        |          | 0x05 Defense (0% damage)                                                                     |  |  |  |
|        |          | 0x06 Absorb (-100% damage)                                                                   |  |  |  |
|        |          | 0x07 HP Max                                                                                  |  |  |  |
|        |          | 0xFF Nothing                                                                                 |  |  |  |
| 0x0038 | 84 bytes | Unknown data. Seems to contain informations about<br>every action and attitude of the Enemy. |  |  |  |
| 0x008C | 2 bytes  | Object you can win at the battle's end.                                                      |  |  |  |
| 0x008F | 2 bytes  | Object you can steel. 0xFFFF if not.                                                         |  |  |  |
| 0x0091 | 12 bytes | Unknown data                                                                                 |  |  |  |
| 0x009D | 2 bytes  | Enemy's MP                                                                                   |  |  |  |
| 0x009F | 2 bytes  | AP you receive when you finish the battle                                                    |  |  |  |
| 0x00A1 | 2 bytes  | Enemy can be transformed to this object. 0xFFFF if not.                                      |  |  |  |
| 0x00A3 | 2 bytes  | Usually 0x10 and 0xFF                                                                        |  |  |  |
| 0x00A5 | 4 bytes  | Enemy's HP                                                                                   |  |  |  |
| 0x00A9 | 4 bytes  | Exp you receive if you finish the battle                                                     |  |  |  |
| 0x00AD | 4 bytes  | Gil you receive if you finish battle                                                         |  |  |  |
| 0x00B1 | 4 bytes  | Usually 4 "random" numbers                                                                   |  |  |  |
| 0x00B5 | 4 bytes  | Usually FF FF FF FF                                                                          |  |  |  |

#### **Magic Scripting**

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

#### **PSX 3D battle Scenes by Micky**

Backgrounds are stored in probably the easiest model format used in FF7. I reconstructed this from the code for my background-to-Maya converter, so there could be errors. I haven't seen any other documentation on this, so please excuse any duplication...

The backgrounds are stored in LZS files in the STAGE1 and STAGE2 directories. They are using the ff7-standard lzs compression.

They begin with a directory: The first word is the number of sections, then there is one pointer for each sections. Each section contains a mesh for the background, except for the first that contains some unknown data and the last that contains the TIM-format texture and palettes.

Each section starts with vertex data, followed by a triangle and a quad data.

```
Vertex data:
1 u32 size of vertex data
8 byte per vertex:
3 u16 x,y,z
1 u16 pad(?)
Triangle data
1 u16 number of triangles
1 u16 texture page (among other flags)
16 bytes per triangle:
3 u16 offset into vertex table
1 u16 unknown
2 u8 u1, v1
1 u16 palette (and some other flags)
2 u8 u2, v2
```

Quad data

2 u8 u3, v3

- 1 u16 number of quads
- 1 u16 texture page (among other flags)

#### 20 bytes per quad:

- 4 u16 offset into vertex table
- 2 u8 u1, v1
- 1 u16 palette
- 2 u8 u2, v2
- 2 u8 u3, v3
- 2 u8 u4, v4
- 1 u16 unknown

Displaying the backgrounds is a bit tricky on modern graphics boards, as they don't support palletized textures anymore. Which is understandable given the large number of fetches that would be required for displaying a properly filtered texture - but not very helpful. I solved that by a pre-process that stores the palette on each pixel and then looks up the color during export.

#### **PSX battle models structure by Cyberman**

#### Terms

BYTE - is an unsigned 8 bit binary string WORD - is an unsigned 16 bit binary string DOUBLE WORD - is an unsigned 32 bit binary string Values are SIGNED if they say so, otherwise they are assumable as unsigned.

Many of the PSX files data files use LZS compression.

#### Combat Models

Combat Models occupy directories

ENEMY1

ENEMY2

ENEMY3

ENEMY4

ENEMY5

ENEMY6

on the CD

ENEMY6 contains the character models and their weapons, including the hires version of Cloud and Sepheroth.

#### Model format

The first 4 bytes of the LZS file contains the uncompressed size of the LZS compressed data, as a double word. The actual compressed data follows after this this double word.

After the compressed information is decompressed in the model. The first double word contains the number of sections in the model file (SEC\_COUNT). Following this is SEC\_COUNT double words. This is an array of offsets to data sections within the model.

```
Format information
[ DOUBLE WORD ] Section Count
[ DOUBLE WORD ] OFFSET SECTION 1 
[ DOUBLE WORD ] OFFSET SECTION 2
... 
[ DOUBLE WORD ] OFFSET SECTION N
```

Section Identification, what they are.

The first section of a model is the actual model information.

There is ALWAYS a TIM image as one of the sections, you MUST find this TIM section before doing anything with the model. For models that have no textures applied to them, the TIM image consists of a 16 entry palette and a 1 unit tall 0 units wide 4bits per pixel image.

All sections from section 2 to before the TIM image are animation sequences. This is nearly identical to the format used on the PC.

On character models there are 16 sections past the TIM image, these are the weapon models. They have the same format as section 1.

#### Section 1 format.

Section 1 has several parts to it. It is important to VERY carefully look at the structure starting this section. The begining of the section is the BONE COUNT. The ROOT BONE follows this, it is NOT counted as a bone and is ALL ZEROs.

A bone is a structure here it is in C/C++

```
typedef struct 
{ 
UINT16 Parent; 
INT16 Length; 
UINT32 Offset; 
} 
FF7_BONE;
```

Parent 0 is the root bone (the root bone is always relative to itself since it is the ROOT). Offset is the offset from the beginning of the section to the actual data for the polygons that makes on the 3d structure. A bone with an OFFSET of ZERO is a JOINT. It has NO physical shape. Objects are drawn from parent to child. All bone lengths are negative and should be drawn with this is mind (otherwise it will mess up rendering it).

#### Physical shape data:

The bone offset points to a double word whose value is \* 8 the vertex count (or it is the SIZE in bytes of the vertex pool and therefore is always a multiple of 8) After the vertex pool comes the texture triangle count and offset. This will be zero if there are no textures. Next come the textured triangles.

```
typedef struct 
{ 
UINT16 A; 
UINT16 B; 
UINT16 C; 
UINT16 D; 
} 
FF7_POLY; 
typedef struct 
{ 
FF7_POLY Vertexs; 
UINT8 U0, V0; 
UINT16 PAL; 
UINT8 U1, V1; 
UINT8 U2, V2; 
} 
FF7_TTRI;
```

Two structures are shown for a reason. FF7\_POLY is a list of offsets into the Vertex pool for each vertex the triangle is made up of. Square follows the LEFT HAND RULE for there ordering to know which way the surface is facing. PAL is actually a bit field that includes information as to which palette the texture information for this triangle is using (see TIM format). U, V are the offset from the upper left corner of the image the coordinates of the texture are pined on.

Next comes the textured Quads count and the textured quads. The textured quads are a structured as follows.

```
typedef struct 
{ 
FF7_POLY Vertexs; 
UINT8 U0, V0; 
UINT16 PAL; 
UINT8 U1, V1; 
UINT8 U2, V2; 
UINT8 U3, V3; 
UINT16 ZZ1; 
} 
FF7_TQUAD;
```

The purpose of ZZ1 in the Quadric version is UNKOWN. On ALL quads in the PSX version of FF7 the ordering of the vertices are A B D C. This is a result of the hardware on the PSX rendering a quadric using 2 triangles in hardware. It is again following the LEFT HAND rule of ordered vertices. To compute the palette number to use you tal PAL and shift it right 7 bits then and it with 7. These three bits are the palette to use for the texture for that triangle or quadric.

Next comes the triangle count and the triangles, the format of the colored vertex triangles are as follows.

```
typedef struct 
{ 
UINT8 R; 
UINT8 G; 
UINT8 B; 
UINT8 U; 
} 
FF7_CLR; 
typedef struct 
{ 
FF7_POLY Vertexs; 
FF7_CLR Colors[3]; 
} 
FF7_TRI;
```

The vertices for these are again word sized offsets into the vertex pool. The game uses 24 bit colored vertices in spite of being shown in only 15bit color.

Next comes the colored vertex quadric count and information there format is as follows.

```
typedef struct 
{ 
FF7_POLY Vertexs; 
FF7_CLR Colors[4]; 
} 
FF7_QUAD;
```

It has the same A B D C ordering as the textured quads, be sure to follow this or things will NOT come out right.

There is NO more information after this save likely the vertex pool for the next bone.

It is important to remember that the TIM image contains where to place the time data and often 1 to 3 palettes. The palettes are used in conjunction with the bit data. There are transparent pixels sometimes in textures. These choose the palette entry that has bit 15 set. This is the transparency bit on the PSX, ALWAYS REMEMBER that it makes that part of the texture transparent when trying to display the model.

Animation format covered elsewhere.

The TIM format is covered elsewhere.

The battle models are IDENTICAL in format as the physical bone description. They consist of 1 bone with one vertex pool and NO textures, any special transparencies one might see in the game are handled by the game, it's not part of the model. The same code you would use to show a single bone, you can use to show a weapon.

#### **PC battle models structure by Mirex**

Final Fantasy 7 battle models are stored in file 'battle.lpg' under FF7/DATA/BATTLE directory. Data can be unpacked by my program Unmass (you can get it at my web, http://mirex.mypage.sk) or by other programs like Ficedula's LGPtools (at http://ficedula.cjb.net)

The LPG file contains many small files with 4-letters long filenames. File classification can be determined by first two letters of the filename. Files with same first two letters belong to same 3d model. Files 'aa'-'of' are Enemy models, 'og'-'rr' are battle scenes, and 'rs'-'sm' are player models. For example files starting with 'rt' belong to Cloud's model. More info can be found in Alhexx's battle database (http://www.alhexx.com/descriptions/other/battle\_database.txt) or in my database (http://mirex.mypage.sk/FILES/monsters.txt)

Every character model has around 20-40 files, depends on its complexity. File type can be determined by 3rd and 4th character of filename. Files that end with 'aa', are skeleton informations, 'ac'-'al' are textures (.TEX files) 'am'-'cj' are body parts (.P files), 'ck'-'cz' are player's weapons(.P files), 'da' are animations files. I have no idea what is inside 'ab' file. For example 'rtck' is model file which contains Cloud's first weapon, Buster sword, because 'rt' = clouds files and 'ck' = 1st weapon file.

Summon models are stored similarly to battle models, but they are stored in magic.lgp, and their filenames are different. Models (P-files) have names "creature.p??" where ?? is model part number, textures have names "creature.t??", skelet info has name "creature.d" and animations are in files "creature.a??".

#### File Structure Info

-- 'AA' - skeleton - file consists of these parts: --

header - (see structure FF7AAheader below, 52 bytes) it is followed by bone info for each bone (FF7AAbone structure, 12 bytes each) And thats it. Nothing more there.

If bone's parent is -1 then it begins at center of coordinate system. Else it is child of its parent bone

```
//offset
struct {
     unsigned long u1[3]; //0
     unsigned long bones; //12 number of model bones
     unsigned long u2[3]; //16
     unsigned long a; //28
     unsigned long b; //32 maybe number of body part models
     unsigned long u3[4]; //36
} FF7AAheader; //size is 52 bytes
struct {
     long parent; //0 index of parent bone, -1 = root node
     float length; //4 length of bone, always is negative.
     unsigned long model; //8 1=bone has body part, 0=has no body part
} FF7AAbone; //size is 12 bytes
```

-- 'DA' - animations - file consists of these parts: -- First there is 4 bytes long integer which holds number of animations in the file

Then for each animation there is:

FF7AAanimHdr structure (see below) and animation data (see below too)

```
struct s_FF7AAanimHdr {
    unsigned long rec_a; //0
    unsigned long rec_b; //4
    unsigned long block_len; //8
    unsigned short block_a; //12
    unsigned short real_data_len; //14
    unsigned short translat[3]; //16
    unsigned char u1; //22
} FF7AAanimHdr; //size = 23 bytes
```

Size of animation data is ( FF7AAanimHdr.block\_len - 11 ), because variables (block\_a, real\_data\_len, translat, u1 are in it) are included in data length.

#### Animation Data

In the animation data there are rotation angles for each bone of the 3D model. Angles are not stored as its usual, in 4 byte floats, but in 12bit integers (that means one integer takes 1.5 byte, 3 angles (rotations for one bone) take up 4.5 bytes !). 4.5 bytes = 36 bits = 3 \* 12 bits, so for example if model has 10 bones all rotations are stored in 45 bytes. 12bits can hold value from 0 to 4095. It can be translated into usual angles

```
0 euler = 0 degrees and 4096 euler = 360 degrees, so formula is degrees = euler * 360 / 4096
```

The animation data are not understood well yet, so usually only first frame and few other frames look as they should when you read them this way.

Example of rotation data:

#### Data in hex:

| DC | BF | FE | 00 | 3E |
|----|----|----|----|----|
|----|----|----|----|----|

#### Data in binary:

| D       | C    | B    | F       | F    | E    | 0       | 0    | 3                             | E    |
|---------|------|------|---------|------|------|---------|------|-------------------------------|------|
| 1101    | 1100 | 1011 | 1111    | 1111 | 1110 | 0000    | 0000 | 0011                          | 1110 |
| Angle X |      |      | Angle Y |      |      | Angle Z |      | Beginning of another rotation |      |

| X   | Y   | Z   |   |
|-----|-----|-----|---|
| DCB | FFE | 003 | E |

#### Data in decimal, euler

| X    | Y    | Z |
|------|------|---|
| 3531 | 4094 | 3 |

#### Data in degrees ( \* 360 / 4096 )

| X     | Y     | Z   |  |
|-------|-------|-----|--|
| 310.3 | 359.8 | 0.2 |  |

#### **Data Organization**

- -Textures
- -Sprites
- -Models


# FF7/Chocobo Breeding {#ff7chocobo_breeding}

- [FF7/Chocobo Breeding](#ff7chocobo_breeding){#toc-ff7chocobo_breeding}
  - [Editor's Note](#editors_note){#toc-editors_note}
  - [1. Stat Glossary](#1_stat_glossary){#toc-1_stat_glossary}
  - [2. Base Chocobos](#2_base_chocobos){#toc-2_base_chocobos}
  - [3. Feeding Greens](#3_feeding_greens){#toc-3_feeding_greens}
  - [4. Breeding Data](#4_breeding_data){#toc-4_breeding_data}



## *VI. Chocobo Breeding*

Editor's Note: Chocobo Breeding isn't a separate module like the others, but is written entirely in Field Script. It's connected to Chocobo racing in a way, but expansive enough to warrant it's own section. The following guide was written by Terence Fergusson.

#### **1. STAT GLOSSARY**

First, let's define the stats a Chocobo has:

| Name           | Definition                                                           |
|----------------|----------------------------------------------------------------------|
| Dash           | The Chocobo's current sprinting speed                                |
| Max Dash       | The maximum sprinting speed this Chocobo will ever aspire to         |
| Run            | The Chocobo's normal running speed                                   |
| Max Run        | The maximum running speed this Chocobo will ever aspire to           |
| Stamina        | The Chocobo's stamina, maxes at 9999                                 |
| Accel          | The Chocobo's acceleration                                           |
| Co-Op          | The Chocobo's co-operation (How well it obeys Manual Control)        |
| Int            | The Chocobo's intelligence (How well it uses Auto Control)           |
| Performance    | The Chocobo's running performance (0:Normal to 2:Sprinter)           |
| RT Count       | A counter connected to Performance regarding feeding                 |
| Races Won      | The number of races the Chocobo has won                              |
| Gender         | The gender of the Chocobo                                            |
| Color          | The color of the Chocobo                                             |
| Rating         | How *good* the Chocobo is. 1 is the best(Wonderful!), 8 is the worst |
| [Dash / 34]    | The Speed that Chocobo Racing will report                            |
| [Stamina / 10] | The Stamina that Chocobo Racing will report                          |

#### **2. BASE CHOCOBOS**

When you catch a Chocobo, it is placed in the yard. The \*only\* stat stored for it is the Rating: Wonderful, Great, Good, etc. The stats are not decided until you confirm with Billy that you'll move them into the stable.

The Ratings we will call them by are: Wonderful, Great, Good, So-So, Average, Poor, Bad, Terrible

Naturally, all Chocobos caught will be Yellow Chocobos with the Rating they were given when you caught them. As for the rest of the stats, they are covered in the following sections:

#### Max Dash and Stamina

For each Rating, the base value of Max Dash and Stamina can be each have up to 8 different values. The values are linked: if you get a certain value for Max Dash, you will get the corresponding value for Stamina as well. Here's a table showing the 8 choices for each Rating:

|           |       | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    |
|-----------|-------|------|------|------|------|------|------|------|------|
| Wonderful | MDash | 3500 | 3600 | 3700 | 3800 | 3800 | 3900 | 4000 | 4000 |
|           | Stam  | 4500 | 4300 | 4200 | 4000 | 4000 | 4000 | 3800 | 3500 |
| Great     | MDash | 3000 | 3000 | 3100 | 3200 | 3300 | 3400 | 3500 | 3600 |
|           | Stam  | 3800 | 3600 | 3500 | 3400 | 3300 | 3200 | 3200 | 3000 |
| Good      | MDash | 2800 | 2800 | 3000 | 3000 | 3100 | 3100 | 3200 | 3300 |
|           | Stam  | 3500 | 3300 | 3200 | 3100 | 3000 | 2900 | 2800 | 2600 |
| So-So     | MDash | 2400 | 2500 | 2600 | 2700 | 2800 | 3000 | 3000 | 3000 |
|           | Stam  | 3300 | 3100 | 3000 | 3000 | 2800 | 2700 | 2600 | 3000 |
| Average   | MDash | 2000 | 2200 | 2300 | 2400 | 2600 | 2800 | 2500 | 2500 |
|           | Stam  | 2500 | 2300 | 2200 | 2100 | 1900 | 1800 | 2000 | 2000 |
| Poor      | MDash | 1800 | 1900 | 2100 | 2200 | 2300 | 2000 | 2000 | 2000 |
|           | Stam  | 2000 | 1700 | 1500 | 1300 | 1000 | 1600 | 1600 | 1600 |
| Bad       | MDash | 1500 | 1600 | 1700 | 1900 | 2000 | 1800 | 1800 | 1800 |
|           | Stam  | 1300 | 1200 | 1100 | 900  | 800  | 1000 | 1000 | 1000 |
| Terrible  | MDash | 1300 | 1400 | 1600 | 1700 | 1800 | 1500 | 1500 | 1500 |
|           | Stam  | 1000 | 900  | 700  | 600  | 500  | 800  | 800  | 800  |

Once the base values for Max Dash and Stamina have been determined, they will be adjusted separately:

```
1/2 chance of being increased by Rnd(0..127)
1/2 chance of being decreased by Rnd(0..127)
```

#### Dash

A lot simpler than the previous section, Dash is set to merely a percentage of the Max Stat. The formula used depends on the Rating:

Wonderful, Great, Good and So-So:

```
Dash = [Max Dash / 10] * Rnd(5..8)
```

Average, Poor, Bad and Terrible:

```
Dash = [Max Dash / 10] * ([Rnd(0..255) / 50] + 3)
```

#### Run and Max Run

These are again related, so we will deal with them together.

First, we must define a modifier we will be using. It differs depending on the Rating of the Chocobo:

```
Wonderful, Great, Good and So-So: x = 100 * Rnd(2..4)
Average, Poor, Bad and Terrible: x = 100 * Rnd(2..5)
```

Once this is defined, then:

```
Max Run = Max Dash - x
Run = Dash - x
```

And now the base stats are done.

#### **The Rest of the Stats**

Let's go over the rest.

Co-Op, RT Count and Races Won are all set to 0, naturally.

Gender is randomly determined between Male and Female, 50/50 chance of either.

Acceleration and Intelligence are randomly determined multiples of 10, again based on the Rating:

|                 | Acceleration | Intelligence |
|-----------------|--------------|--------------|
| Wonderful/Great | 10 * Rnd(67) | 10 * Rnd(56) |
| Good/So-So      | 10 * Rnd(56) | 10 * Rnd(34) |
| Average/Poor    | 10 * Rnd(35) | 10 * Rnd(02) |
| Bad/Terrible    | 10 * Rnd(25) | 10 * Rnd(02) |

And finally, Performance is randomly determined. First, you have a chance at Performance 0 - the Normal Performance - and this depends on the Rating again:

|                 | Chance of Performance 0 |
|-----------------|-------------------------|
| Wonderful/Great | 7/8                     |
| Good/So-So      | 3/4                     |
| Average/Poor    | 1/2                     |
| Bad/Terrible    | 1/2                     |

If you don't get Performance 0, then you have a 50/50 chance each of Performances 1 and 2.

And that's that! The new Chocobo is created. All that remains is to name it and put in the stable. And then we can get to feeding it...

#### **3. FEEDING GREENS**

Fairly simple: each Green increases certain stats by random amounts per Green. Here's how each of the Greens change a Chocobo's stats.

| Green   | Attribute change                                                                                                                                                                                                                                                   |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Gysahl  | x = Rnd(03)<br>Dash increases by x, Maximum of Max Dash<br>Run increases by Rnd(02), Maximum of Max Run<br>Stamina increases by 3 - x, Maximum of 9999<br>Co-Op increases by 1, Maximum of 100                                                                     |
| Krakka  | Int increases by Rnd(12), Maximum of 100<br>Co-Op increases by 1, Maximum of 10                                                                                                                                                                                    |
| Tantal  | Dash increases by Rnd(14), Maximum of Max Dash<br>Run increases by Rnd(14), Maximum of Max Run<br>Stamina increases by Rnd(12), Maximum of 9999<br>Int increases by 1, Maximum of 100<br>Co-Op increases by 1, Maximum of 100                                      |
| Pahsana | Int increases by Rnd(18), Maximum of 100<br>If Performance > 0, Then RT Count increases by Rnd(14)<br>If RT Count reaches the maximum of 100, Performance = 0<br>Co-Op increases by 1, Maximum of 100<br>75% chance Co-Op will increase by 1 again, Maximum of 100 |
| Curiel  | Dash increases by Rnd(03), Maximum of Max Dash<br>Run increases by Rnd(03), Maximum of Max Run<br>Stamina increases by Rnd(310), Maximum of 9999<br>Co-Op increases by 2, Maximum of 100                                                                           |

| Green  | Attribute change                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mimett | Dash increases by Rnd(116), Maximum of Max Dash<br>Run increases by Rnd(310), Maximum of Max Run<br>25% chance: Accel increases by 1, Maximum of 80<br>Co-Op increases by 2, Maximum of 100                                                                                                                                                                                                                                                                                                                                                       |
| Reagan | x = [Dash / 20]<br>y = [Rnd(0255) / 25]<br>50% chance: x = x + y<br>50% chance: x = x - y, Minimum of 0<br>Increase Dash by x, Maximum of Max Dash<br>x = [Run / 20]<br>y = [Rnd(0255) / 25]<br>50% chance: x = x + y<br>50% chance: x = x - y, Minimum of 0<br>Increase Run by x, Maximum of Max Run<br>x = [Stamina / 100]<br>y = [Rnd(0255) / 25]<br>50% chance: x = x + y<br>50% chance: x = x - y, Minimum of 0<br>Increase Stamina by x, Maximum of 9999<br>Co-Op increases by 3, Maximum of 100                                            |
| Sylkis | x = [Dash / 10]<br>y = [Rnd(0255) / 25]<br>50% chance: x = x + y<br>50% chance: x = x - y, Minimum of 0<br>Increase Dash by x, Maximum of Max Dash<br>x = [Run / 10]<br>y = [Rnd(0255) / 25]<br>50% chance: x = x + y<br>50% chance: x = x - y, Minimum of 0<br>Increase Run by x, Maximum of Max Run<br>x = [Stamina / 50]<br>y = [Rnd(0255) / 25]<br>50% chance: x = x + y<br>50% chance: x = x - y, Minimum of 0<br>Increase Stamina by x, Maximum of 9999<br>Int increases by Rnd(14), Maximum of 100<br>Co-Op increases by 4, Maximum of 100 |

And now, on to the final section: breeding....

#### **4. BREEDING DATA**

When you're ready to mate two Chocobos to create a newborn one... well, the most important choice you get to make is which Nut you'll feed them. Therefore, we will go over each Nut in turn.

A few notes before we begin. The first Chocobo you pick is very important when determining the stats of a baby for most of the Nuts. You'll also notice the following:

- 1) It is impossible to make your first Green or Blue Chocobo without a Carob Nut.
- 2) However, it \*IS\* possible to make a Black Chocobo with any Nut except a Zeio.
- 3) While it's possible to get a guaranteed Gold Chocobo when mating a Black and a Wonderful Chocobo (providing they have won enough total races), mating a Black and a Gold is \*NOT\* a guarantee unless the Gold has a Wonderful Rating.

So, some fairly interesting things to see.

In addition, the code is very complicated, and I can't guarantee I haven't made any mistakes with translating it into readable form. This document was difficult enough to compile.

# **Pepio Nut**

| Basic Stats |                                                              |  |
|-------------|--------------------------------------------------------------|--|
| Max Dash    | Average of Parents' Max Dash - 100*Rnd(12)<br>Minimum of 300 |  |
| Dash        | Average of Parents' Dash - 100*Rnd(12)<br>Minimum of 300     |  |
| Max Run     | Average of Parents' Max Run - 100*Rnd(14)<br>Minimum of 300  |  |
| Run         | Average of Parents' Run - 100*Rnd(12)<br>Minimum of 300      |  |
| Stamina     | Average of Parents' Stamina - Rnd(0255)<br>Minimum of 1      |  |

Note: The minimums only apply for the initial values; further reductions can safely ignore them

- -If Dash is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- -If Max Run is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- -If Run is greater than or equal to either Dash or Max Run, subtract 100 from it until it is lower than both

-If the baby chocobo's Max Dash is under 4000, there is a 1/512 chance that a bonus will be applied to the Chocobo's Dash stats, using the following:

| 1/128  | Max Dash is set to 4000 |
|--------|-------------------------|
| 1/128  | Max Dash is set to 4100 |
| 2/128  | Max Dash is set to 4200 |
| 3/128  | Max Dash is set to 4300 |
| 1/128  | Max Dash is set to 4500 |
| 20/128 | No change to Max Dash   |

Its Dash is then set to its Max Dash, and then 6 random numbers each between 0 and 255 (Rnd(0..255)) are subtracted from it. That means that it could end up anywhere between 0 to 1530 beneath your Max Dash.

| Extra Stats |                              |  |
|-------------|------------------------------|--|
| Accel       | Average of Parents' Accel    |  |
| Co-Op       | 0                            |  |
| Int         | Average of Parents' Int      |  |
| Performance | See Notes                    |  |
| RT Count    | 0                            |  |
| Races Won   | 0                            |  |
| Gender      | 50% chance of Male or Female |  |

#### Color/Rating:

- If mating a Green and Blue Chocobo together, there is a 25% chance of a Black Chocobo.
- If that fails or you're not using a Green and Blue, then it's 50% chance of the father's color and 50% chance of the mother's color.
- -In all cases, the baby's Rating has a 50% chance of being equal to thefather's, and 50% chance of being equal to the mother's.

## **Luchile Nut**

| Basic Stats |                                                                          |  |
|-------------|--------------------------------------------------------------------------|--|
| Max Dash    | 50% chance of Average of Parents' Max Dash                               |  |
|             | 50% chance of Average of Parents' Max Dash - Rnd(0255)<br>Minimum of 300 |  |
| Dash        | 50% chance of Average of Parents' Dash                                   |  |
|             | 50% chance of Average of Parents' Dash - Rnd(0255)<br>Minimum of 300     |  |

| Basic Stats |                                                                           |  |
|-------------|---------------------------------------------------------------------------|--|
| Max Run     | 50% chance of Average of Parents' Max Run                                 |  |
|             | 50% chance of Average of Parents' Max Run - 2*Rnd(0255)<br>Minimum of 300 |  |
| Run         | 50% chance of Average of Parents' Run                                     |  |
|             | 50% chance of Average of Parents' Run - 2*Rnd(0.255)<br>Minimum of 30     |  |
| Stamina     | Average of Parents' Stamina                                               |  |

Note: The minimums only apply for the initial values; further reductions can safely ignore them

- -If Dash is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- -If Max Run is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- -If Run is greater than or equal to either Dash or Max Run, subtract 100 from it until it is lower than both

| Extra Stats |                              |  |
|-------------|------------------------------|--|
| Accel       | Average of Parents' Accel    |  |
| Co-Op       | 0                            |  |
| Int         | Average of Parents' Int      |  |
| Performance | See Notes                    |  |
| RT Count    | 0                            |  |
| Races Won   | 0                            |  |
| Gender      | 50% chance of Male or Female |  |

#### Color/Rating:

- If mating a Green and Blue Chocobo together, there is a 25% chance of a Black Chocobo
- If that fails or you're not using a Green and Blue, then it's 50% chance of the father's color and 50% chance of the mother's color
- In all cases, the baby's Rating has a 50% chance of being equal to the father's, and 50% chance of being equal to the mother's

## **Saraha Nut**

| Basic Stats |                                                                                     |  |
|-------------|-------------------------------------------------------------------------------------|--|
| Max Dash    | 3/32 chance of the *first* Parent's Max Dash increased by 1/33rd<br>Maximum of 6000 |  |
|             | 3/32 chance of the *first* Parent's Max Dash decreased by1/33rd<br>Minimum of 1     |  |
|             | 26/32 chance of average of Parent's Max Dash                                        |  |
| Dash        | Average of Parents' Dash                                                            |  |
| Max Run     | 3/32 chance of the *first* Parent's Max Run increased by 1/33rd<br>Maximum of 6000  |  |
|             | 3/32 chance of the *first* Parent's Max Run decreased by 1/33rd<br>Minimum of 1     |  |
|             | 26/32 chance of average of Parent's Max Run                                         |  |
| Run         | Average of Parents' Run                                                             |  |
| Stamina     | 3/32 chance of the *first* Parent's Stamina increased by1/33rd<br>Maximum of 9999   |  |
|             | 3/32 chance of the *first* Parent's Stamina decreased by 1/33rd<br>Minimum of 100   |  |
|             | 26/32 chance of average of Parent's Stamina                                         |  |

- If Max Run got the 3/32 chance of a 1/33rd increase and Max Run is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- If Run is greater than or equal to Max Run, subtract 100 from it until it is lower than Max Run

| Extra Stats |                              |  |
|-------------|------------------------------|--|
| Accel       | Average of Parents' Accel    |  |
| Co-Op       | 0                            |  |
| Int         | Average of Parents' Int      |  |
| Performance | See Notes                    |  |
| RT Count    | 0                            |  |
| Races Won   | 0                            |  |
| Gender      | 50% chance of Male or Female |  |

- If mating a Green and Blue Chocobo together, there is a 50% chance of a Black Chocobo
- If that fails or you're not using a Green and Blue, then it's 50% chance of the father's color and 50% chance of the mother's color
- In all cases, the baby's Rating has a 50% chance of being equal to the father's, and 50% chance of being equal to the mother's

## **Lasan Nut**

| Basic Stats |                                                                                       |  |
|-------------|---------------------------------------------------------------------------------------|--|
| Max Dash    | 50/256 chance of the *first* Parent's Max Dash increased by 1/20th<br>Maximum of 6000 |  |
|             | 25/256 chance of the *first* Parent's Max Dash decreased by1/20th<br>Minimum of 1     |  |
|             | 181/256 chance of average of Parent's Max Dash                                        |  |
| Dash        | Average of Parents' Dash                                                              |  |
| Max Run     | 50/256 chance of the *first* Parent's Max Run increased by1/20th<br>Maximum of 6000   |  |
|             | 25/256 chance of the *first* Parent's Max Run decreased by1/20th<br>Minimum of 1      |  |
|             | 81/256 chance of average of Parent's Max Run                                          |  |
| Run         | Average of Parents' Run                                                               |  |
| Stamina     | 50/256 chance of the *first* Parent's Stamina increased by1/20th<br>Maximum of 9999   |  |
|             | 25/256 chance of the *first* Parent's Stamina decreased by1/20th<br>Minimum of 100    |  |
|             | 181/256 chance of average of Parent's Stamina                                         |  |

- If Max Run got the 50/256 chance of a 1/20th increase and Max Run is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- If Run is greater than or equal to Max Run, subtract 100 from it until it is lower than Max Run

| Extra Stats |                              |  |  |
|-------------|------------------------------|--|--|
| Accel       | Average of Parents' Accel    |  |  |
| Co-Op       | 0                            |  |  |
| Int         | Average of Parents' Int      |  |  |
| Performance | See Notes                    |  |  |
| RT Count    | 0                            |  |  |
| Races Won   | 0                            |  |  |
| Gender      | 50% chance of Male or Female |  |  |

- If mating a Green and Blue Chocobo together, there is a 50% chance of a Black Chocobo
- If that fails or you're not using a Green and Blue, then it's 50% chance of the father's color and 50% chance of the mother's color
- In all cases, the baby's Rating has a 50% chance of being equal to the father's, and 50% chance of being equal to the mother's

## **Pram Nut**

| Basic Stats |                                                                                      |  |
|-------------|--------------------------------------------------------------------------------------|--|
| Max Dash    | 50/256 chance of the *first* Parent's Max Dash increased by1/18th<br>Maximum of 6000 |  |
|             | 25/256 chance of the *first* Parent's Max Dash decreased by 1/33rd<br>Minimum of 1   |  |
|             | 181/256 chance of average of Parent's Max Dash                                       |  |
| Dash        | Average of Parents' Dash                                                             |  |
| Max Run     | 50/256 chance of the *first* Parent's Max Run increased by 1/18th<br>Maximum of 6000 |  |
|             | 206/256 chance of average of Parent's Max Run                                        |  |
| Run         | Average of Parents' Run                                                              |  |
| Stamina     | 50/256 chance of the *first* Parent's Stamina increased by 1/18th<br>Maximum of 9999 |  |
|             | 35/256 chance of the *first* Parent's Stamina decreased by1/10th<br>Minimum of 100   |  |
|             | 171/256 chance of average of Parent's Stamina                                        |  |

- If Max Run got the 50/256 chance of a 1/18th increase and Max Run is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- If Run is greater than or equal to Max Run, subtract 100 from it until it is lower than Max Run

| Extra Stats |                              |  |  |
|-------------|------------------------------|--|--|
| Accel       | Average of Parents' Accel    |  |  |
| Co-Op       | 0                            |  |  |
| Int         | Average of Parents' Int      |  |  |
| Performance | See Notes                    |  |  |
| RT Count    | 0                            |  |  |
| Races Won   | 0                            |  |  |
| Gender      | 50% chance of Male or Female |  |  |

- If mating a Green and Blue Chocobo together, there is a 50% chance of a Black Chocobo
- If that fails or you're not using a Green and Blue, then it's 50% chance of the father's color and 50% chance of the mother's color
- In all cases, the baby's Rating has a 50% chance of being equal to the father's, and 50% chance of being equal to the mother's

## **Porov Nut**

| Max Dash<br>Dash<br>Max Run | 70/256 chance of the *first* Parent's Max Dash increased by 1/15th<br>Maximum of 6000<br>186/256 chance of average of Parent's Max Dash<br>Average of Parents' Dash |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                             |                                                                                                                                                                     |
|                             |                                                                                                                                                                     |
|                             |                                                                                                                                                                     |
|                             | 50/256 chance of the *first* Parent's Max Run increased by 1/15th<br>Maximum of 6000                                                                                |
|                             | 25/256 chance of the *first* Parent's Max Run decreased by 1/20th<br>Minimum of 1                                                                                   |
|                             | 181/256 chance of average of Parent's Max Run                                                                                                                       |
| Run                         | Average of Parents' Run                                                                                                                                             |
| Stamina                     | 50/256 chance of the *first* Parent's Stamina increased by 1/20th<br>Maximum of 9999                                                                                |
|                             | 206/256 chance of average of Parent's Stamina                                                                                                                       |

- If Max Run got the 50/256 chance of a 1/15th increase and Max Run is greater than or equal to Max Dash, subtract 100 from it until it is lower than Max Dash
- If Run is greater than or equal to Max Run, subtract 100 from it until it is lower than Max Run

| Extra Stats |                              |  |  |
|-------------|------------------------------|--|--|
| Accel       | Average of Parents' Accel    |  |  |
| Co-Op       | 0                            |  |  |
| Int         | Average of Parents' Int      |  |  |
| Performance | See Notes                    |  |  |
| RT Count    | 0                            |  |  |
| Races Won   | 0                            |  |  |
| Gender      | 50% chance of Male or Female |  |  |

#### Color/Rating:

- If mating a Green and Blue Chocobo together, there is a 25% chance of a Black Chocobo
- If that fails or you're not using a Green and Blue, then it's 50% chance of the father's color and 50% chance of the mother's color

- In all cases, the baby's Rating has a 50% chance of being equal to the father's, and 50% chance of being equal to the mother's

## **Carob Nut**

| Basic Stats |                                                                                    |  |
|-------------|------------------------------------------------------------------------------------|--|
| Max Dash    | See below                                                                          |  |
| Dash        | Average of Parent's Dash                                                           |  |
| Max Run     | 30/256 chance of highest of Parents' Max Run increased by1/10th<br>Maximum of 6000 |  |
|             | 55/256 chance of highest of Parents' Max Run decreased by 1/20th<br>Minimum of 1   |  |
|             | 161/256 chance of average of Parents' Max Run                                      |  |
| Run         | Average of Parent's Run                                                            |  |
| Stamina     | 50/256 chance of highest of Parents' Stamina increased by1/20th<br>Maximum of 9999 |  |
|             | 216/256 chance of average of Parents' Stamina                                      |  |

- If a Black Chocobo was born (see below for what causes this) and the average of the Parents' Max Dash is less than 4000, then the following 'bonuses' will be applied:

| 7/16 | Max Dash is set to 4000 |
|------|-------------------------|
| 4/16 | Max Dash is set to 4200 |
| 1/16 | Max Dash is set to 4300 |
| 1/16 | Max Dash is set to 4400 |
| 2/16 | Max Dash is set to 4500 |
| 1/16 | Max Dash is set to 4800 |

After this bonus, the Max Dash is further modified:

```
x = [Rnd(0..255) / 5]
50% chance that Max Dash is increased by 'x'
otherwise, Max Dash is decreased by 'x'
```

Otherwise (if the baby is not a Black Chocobo or the average Max Dash was greater or equal to 4000):

| 60/256  | The baby's Max Dash will be set to the highest of the Parents' Max Dash increased<br>by 1/10th<br>Maximum of 6000 |
|---------|-------------------------------------------------------------------------------------------------------------------|
| 196/256 | The baby's Max Dash will be set to the average of the Parents' Max Dash                                           |

- If the Chocobo's Max Run is greater or equal to its Max Dash, then Max Run is reduced by 100 repeatedly until it is lower than Max Dash.
- Finally, if the baby Chocobo's Run is greater or equal to its Max Run, the Run value is reduced by 100 repeatedly until it is lower than Max Run.

| Extra Stats |                              |  |
|-------------|------------------------------|--|
| Accel       | Average of Parents' Accel    |  |
| Co-Op       | 0                            |  |
| Int         | Average of Parents' Int      |  |
| Performance | See Notes                    |  |
| RT Count    | 0                            |  |
| Races Won   | 0                            |  |
| Gender      | 50% chance of Male or Female |  |

- If a Blue and a Green Chocobo are being mated, then:
  - -If the total number of races won by its parents is 9 or more, then the baby is automatically a Black Chocobo
  - -If it's less than 9:

10/256 chance: Black Chocobo 128/256 chance: Blue Chocobo 118/256 chance: Green Chocobo

The baby's Rating will be either Great (50%) or Good (50%)

- Otherwise, if both of the parents are Great or Good Chocobos:
  - If the total number of races won by the parents is 4 or more, then the baby is automatically either a Blue (50%) or Green (50%) Chocobo
  - If it's less:

69/256 chance: Blue Chocobo 69/256 chance: Green Chocobo 118/256 chance: Yellow Chocobo

The Rating of the newborn Chocobo will be Great if both parents have the same Rating, and will have an equal chance of Great or Good if the parents were of different Ratings.

- If the \*first\* Parent you picked was a Great or Good Chocobo, but the second isn't, then there's a 25% chance that it won't matter, and it'll use the above condition (both parents are Great/Good) to work out Color and Rating. The Rating of the newborn in this case will be the same as the first Parent
- If \*everything else\* fails, then the baby will be a Yellow Chocobo, and have a 50/50 chance of getting either its mother's or its father's Rating

## **Zeio Nut**

| Basic Stats |                                                                                      |  |
|-------------|--------------------------------------------------------------------------------------|--|
| Max Dash    | See below                                                                            |  |
| Dash        | Average of Parent's Dash                                                             |  |
| Max Run     | 80/256 chance of highest of Parents' Max Run increased by 1/8th<br>Maximum of 6000   |  |
|             | 15/256 chance of highest of Parents' Max Run decreased by 1/20th<br>Minimum of 1     |  |
|             | 161/256 chance of average of Parents' Max Run                                        |  |
| Run         | Average of Parent's Run                                                              |  |
| Stamina     | 175/256 chance of highest of Parents' Stamina increased by 1/20th<br>Maximum of 9999 |  |
|             | 81/256 chance of average of Parents' Stamina                                         |  |

- If a Gold Chocobo was born (see below for what causes this) and the average of the Parents' Max Dash is less than 5000, then the following 'bonuses' will be applied:

| 7/16 | Max Dash is set to 5000 |
|------|-------------------------|
| 2/16 | Max Dash is set to 5100 |
| 2/16 | Max Dash is set to 5200 |
| 1/16 | Max Dash is set to 5300 |
| 1/16 | Max Dash is set to 5400 |
| 2/16 | Max Dash is set to 5500 |
| 1/16 | Max Dash is set to 5950 |

After this bonus, the Max Dash is further modified:

```
x = [Rnd(0..255) / 10]
50% chance that Max Dash is increased by 'x'
otherwise, Max Dash is decreased by 'x'
```

Otherwise (the baby is not a Gold Chocobo or the average Max Dash was greater or equal to 5000):

| 55/256  | The baby's Max Dash will be set to the highest of the Parents' Max Dash<br>increased by 1/10th, maximum of 6000 |
|---------|-----------------------------------------------------------------------------------------------------------------|
| 201/256 | The baby's Max Dash will be set to the average of the Parents' Max Dash                                         |

- If the Chocobo's Max Run is greater or equal to its Max Dash, then Max Run is reduced by 100 repeatedly until it is lower than Max Dash.
- If a Gold Chocobo was born and its Max Run is less than 4000, then it gets a bonus of 1000 to its Max Run. This can potentially cause it to go above Max Dash.
- Finally, if the baby Chocobo's Run is greater or equal to its Max Run, the Run value is reduced by 100 repeatedly until it is lower than Max Run.

| Extra Stats |                              |  |  |  |  |  |  |
|-------------|------------------------------|--|--|--|--|--|--|
| Accel       | Average of Parents' Accel    |  |  |  |  |  |  |
| Co-Op       | 0                            |  |  |  |  |  |  |
| Int         | Average of Parents' Int      |  |  |  |  |  |  |
| Performance | See Notes                    |  |  |  |  |  |  |
| RT Count    | 0                            |  |  |  |  |  |  |
| Races Won   | 0                            |  |  |  |  |  |  |
| Gender      | 50% chance of Male or Female |  |  |  |  |  |  |

- First, if you are mating a Black and a Wonderful Chocobo, then:
  - 1/32 chance: Gold Chocobo
  - 31/32 chance: Gold Chocobo \*ONLY\* if the total number of Races Won by the parents add up to 12 or more
    - If you get a Gold Chocobo by this method, then it will have a Rating of Great
- If you don't get an automatic Gold Chocobo or aren't mating a Black and a Wonderful Chocobo in the first place, then you have a 50% chance of the father's color and a 50% chance of the mother's color. Under those circumstances, there's a 50/50 chance it'll get either the father's or the mother's Rating

#### FINAL BREEDING NOTES

The Parent Chocobos must wait 3-10 battles before they recover.

The Baby Chocobo must wait 3-18 battles before it matures.

There is a 17/256 chance that the new Chocobo will be naturally more adapt at dashing than running, which places penalties on its Run stats and grants bonuses to its Dash stats. However, it requires a couple of extra conditions:

First, 
$$x = 100 * Rnd(3..10)$$

Now, the modifications will only go ahead if the Baby's Run stat is greater than x, and that the Baby's Max Dash stat, when increased by x, does not exceed 6000.

- If this is true, then:
  - Baby's Run and Max Run stats are reduced by x.
  - Baby's Dash and Max Dash stats are increased by x.

Finally, the Performance of the Baby Chocobo is determined like so:

- If both of the parents had a Performance that was not 0, then the Baby has a 50% chance each of Performances 1 and 2.
- If at least one of them had a Performance that was 0, there is a 50% chance that the baby will have either Performances 1 or 2 (equal chance).
- Otherwise, what the baby gets becomes slightly more complicated. It \*should\* be Performance 0, but because FF7 does not reinitialize the variable, it is \*possible\* for the baby to get the Performance of the previous chocobo that was born provided you haven't left the screen since the last breeding. Since it's only possible to get two babies without leaving the ranch, this generally has very little effect... but it is, at least, possible. In general though, you should get Performance 0 if the previous conditions failed.


---
topic_id: 20475
board_id: 38
title: "[FF7PC][Tsunamods] Cosmo Memory: Complete Sound Overhaul"
author: "Bonez"
replies: 106
views: 172266
last_post: "2025-04-22 00:36:54"
url: "https://forums.qhimm.com/index.php?topic=20475.0"
scraped_at: "2025-12-29T12:57:10.478216"
---

# [FF7PC][Tsunamods] Cosmo Memory: Complete Sound Overhaul

*Originally posted by **Bonez** • 172266 views • 106 replies*

---

## Post #26 by Bonez
*«on:2021-01-09 08:44:46 »*

![](https://i.imgur.com/BR1Y2Sp.png)


Formerly known as "Bonez' Sound Effect Suite". Cosmo Memory uses the new FFNx SFX engine and is an entirely new mod rebuilt from the ground up with a ton of new features. This project started out in 2018 as a little mod to just replace the FF7 menu sounds with the menu sounds from FFXIII. Since that time, it has evolved into something far more... After following the community and modding the game for several years, I noticed the graphical and musical mods were growing and advancing but the sound effects department was totally stalled. I mean, it's an entire 1/3 of what your senses are taking in, along side the visuals and music! I wanted something to match the beautiful/advanced graphical and musical mods provided by the very talented authors/creators of this community... So, I present to you Cosmo Memory: A Complete Sound Overhaul.

Features:

- Replaces/updates *all* 724 original sound effects including battle, magic, enemy skills, limit breaks, summons, world
- Ambient sounds for *every* field and battle scene in the game
- Ground-conditional footstep sound effects for every field and world map
- FMV audio tracks completely rebuilt from scratch (Compatible with any FMV video mod and Echo-s voices)
- Voiced attacks or "grunts" for all party members
- Shuffles battle impact sounds as well as other often-repeated sounds randomly so you never hear the same exact sound twice in a row
- 3 selectable menu sound sets
- Complete compatibility with New Threat, Echo-S and any other mod


**Launch Trailer: <https://www.youtube.com/watch?v=Zt0GRSb8KcA>**


**IMPORTANT**
-This mod **REQUIRES** 7th Heaven 2.4+ and FFNx 1.11+
You can download the latest 7th Heaven here : <https://github.com/tsunamods-codes/7th-Heaven/releases/tag/canary>

-For best experience, use headphones and set music volume to ~60%

**FAQ**
Will you add the option to/Can I turn off the replaced sfx?

**Spoiler:** [show](#)

No. There are several technical reasons for why. I won't go into all of them, but among which; it's impossible to use the stock engine for some sounds and the new engine for others. It's all one way or the other. If you were to "just stick on the ambience", then the new engine would be used for the ambience and you'd get no other sfx at all. Also a few of the fields have a stock ambience, so if you did import the vanilla sounds to the new engine, you'd have some fields with super high def ambience and some with crushed midi vanilla ambience. There are several areas in the game where doing this would be very awkward or be outright cringe. Some people suggest to change everything except battle sounds. The thing about that is many, many sounds are reused throughout the game. Just one example, a wave sound: The wave sound may be used in battle for the sewer monster, or Leviathan, but also used near the ocean. So, when you're near the ocean you'd suddenly hear midi waves next to HD sounds. This happens with probably *half* of the sounds in the game. There is also dealing with the complexities the mod adds like shuffled melee sounds. Setting up contingencies for if replaced battle sounds are off would compound those complexities. Which leads me to my second reason - I just don't want a hodgepodge mod where you'd have real recordings of birds etc. clashing against staticy-midi battle sounds. This was the problem with previous incomplete sfx mods for FF7. They *only* changed a hand full of battle sounds, which clashed against other battle sounds immediately surrounding them... Which leads me to most importantly; Cosmo Memory is a sfx replacement mod for the 724 vanilla sounds first and foremost. Identifying and making and editing and replacing them took 2 years to complete. That is the entire purpose of the mod - to update *everything*. The same way Nino replaces every model in the game, the same way SYW updates every field in the game, and the same way any music mod replaces every song in the game. The other features like ambience, footsteps, etc. were just last minute bells and whistles to go on top of them thrown in during the final couple weeks of development.

Most of the FF7 modder's philosophies are to provide the remake everyone really wanted. If Square had made the 1:1 remake, they wouldn't have used those original sounds...



Special Thanks:
TrueOdin - the FFNx sound engine
vertex2995 - world map footsteps

 **[Download Cosmo Memory HERE](https://bonez.7thheaven.rocks/%5BTsunamods%5D_Cosmo_Memory.iro)** Size: 350MB


If you enjoy the mod, consider a little something for the many many hours it took to put this together: **[Donate Here](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=77DA5WPWUWHCJ&currency_code=USD&source=url)**


---

## Post #27 by elias
*«Reply #1 on:2021-01-13 11:30:28 »*

Lowering/raising the SFX volume in the game's Config menu seems to disable the SFX sounds altogether (menu cursors, engine sounds etc.). I'm using FFNx-v1.8.1.140 and I've set the correct settings in the FFNx.toml file during installation.


---

## Post #28 by Bonez
*«Reply #2 on:2021-01-16 00:50:49 »*

> \*\*elias wrote:\*\*
> Lowering/raising the SFX volume in the game's Config menu seems to disable the SFX sounds altogether (menu cursors, engine sounds etc.). I'm using FFNx-v1.8.1.140 and I've set the correct settings in the FFNx.toml file during installation.


You're right. Thank you. I've never had a reason to lower the SFX, only the music; as the SFX are already a much lower volume than any of the music. I likely would never have found this. The next FFNx canary will likely have a fix.


---

## Post #29 by elias
*«Reply #3 on:2021-01-17 03:46:46 »*

> \*\*elias wrote:\*\*
> Lowering/raising the SFX volume in the game's Config menu seems to disable the SFX sounds altogether (menu cursors, engine sounds etc.). I'm using FFNx-v1.8.1.140 and I've set the correct settings in the FFNx.toml file during installation.


FFNx v1.8.1.144 seems to have fixed this issue. That aside, would it be possible to turn down or adjust the SFX that occurs during the transition to a battle? I've always found that to be louder/longer than the rest of the SFX. Other than that, it's a great mod for what it has been so far.


---

## Post #30 by Hypnotic Mind
*«Reply #4 on:2021-01-18 17:02:45 »*

I'm currently having problems getting the music to play after installing the updated FFNx driver 1.8.1.13+.  I've set the settings correctly on the FFNx.toml file and removed the "#" as mentioned.  The sound effects suite all work but only the default music plays.  The music mods I use are the the Tsuna Arranged and the EDMusic, and I used to use the Symphonic Redux mod before this, now they don't load at all even by themselves.  I also get the black screen blinking throughout the game.  Is there something I'm missing or doing wrong?


---

## Post #31 by Bonez
*«Reply #5 on:2021-01-20 02:13:00 »*

> \*\*Hypnotic Mind wrote:\*\*
> I'm currently having problems getting the music to play after installing the updated FFNx driver 1.8.1.13+.  I've set the settings correctly on the FFNx.toml file and removed the "#" as mentioned.  The sound effects suite all work but only the default music plays.  The music mods I use are the the Tsuna Arranged and the EDMusic, and I used to use the Symphonic Redux mod before this, now they don't load at all even by themselves.  I also get the black screen blinking throughout the game.  Is there something I'm missing or doing wrong?


This isn't related to this mod, but to get music mods to work with the new FFNx, you need to enable external music and set the path for external music to "music/vgmstream", similar to how you did for the sfx. The next 7H release will not require all this, btw...

The black blinking thing is apparently an AMD issue. I don't know anything about it as I use intel... I do experience blinking if I use the program Borderless Gaming to make the game borderless, however. But that seems to be a Borderless Gaming issue.


---

## Post #32 by Dark_Ansem
*«Reply #6 on:2021-03-03 09:44:48 »*

Sorry for the question, but how did you actually replace the sound effects?


---

## Post #33 by AuthenticM
*«Reply #7 on:2021-03-03 14:07:09 »*

This is a cool project, Bonez. Congrats!

Are there videos showing the new sound effects in action? I'd love to see your mod in action.


---

## Post #34 by Bonez
*«Reply #8 on:2021-03-05 02:26:13 »*

> \*\*AuthenticM wrote:\*\*
> This is a cool project, Bonez. Congrats!
> Are there videos showing the new sound effects in action? I'd love to see your mod in action.

My Youtube channel has a few videos of tests as well as previews for the original mods, which while outdated are still largely included in this one.
<https://www.youtube.com/user/WTurner859/videos>
I also post a lot more updates on the discord than I do here.


> \*\*Dark\_Ansem wrote:\*\*
> Sorry for the question, but how did you actually replace the sound effects?

Tediously. Very tediously.


---

## Post #35 by daedrixx2
*«Reply #9 on:2021-03-08 00:06:14 »*

Sorry if my post isn't strictly inherent to the topic.

Is there a chance you could possibly upload a vanilla sfx pack for those of us who prefer the original sfx?
You see, the stock sfx playback engine of the game is bugged, and while FFNx has a sfx playback engine with those bugs fixed, it still requires a sfx pack to begin with.
I tried extracting the sfx myself with the old FF7SND (I couldn't get the new version of FF7SND working despite having installed .NET 5 x64 and x86, and having my antivirus off) and with cosmo095c, but after a few battles the game always crashes (if I only play in a field without entering battle mode the game runs fine).
Since you've so much experience with sfx modding, and your modded sfx pack works good, you surely know how to extract the sfx in a way that doesn't make FFNx crash.
That's why I'm asking you.


Thanks anyway  ![:)](https://forums.qhimm.com/Smileys/akyhne/smiley.gif "Smiley")


---

## Post #36 by Bonez
*«Reply #10 on:2021-03-08 08:55:07 »*

> \*\*daedrixx2 wrote:\*\*
> Sorry if my post isn't strictly inherent to the topic.
> Is there a chance you could possibly upload a vanilla sfx pack for those of us who prefer the original sfx?
> You see, the stock sfx playback engine of the game is bugged, and while FFNx has a sfx playback engine with those bugs fixed, it still requires a sfx pack to begin with.
> I tried extracting the sfx myself with the old FF7SND (I couldn't get the new version of FF7SND working despite having installed .NET 5 x64 and x86, and having my antivirus off) and with cosmo095c, but after a few battles the game always crashes (if I only play in a field without entering battle mode the game runs fine).
> Since you've so much experience with sfx modding, and your modded sfx pack works good, you surely know how to extract the sfx in a way that doesn't make FFNx crash.
> That's why I'm asking you.
> Thanks anyway


You shouldn't NEED a sound mod... make sure your sfx option is set to "Original audio.dat" in the 7H driver settings (I'm assuming you're on 7H 2.3 to be having this problem)... If you need further help, hit me up on the qhimm discord. It'd be a lot easier to walk you through it.


---

## Post #37 by Tyler Durden
*«Reply #11 on:2021-04-08 23:44:54 »*

Was this mod taken down? the link seems to be broken.


---

## Post #38 by Bonez
*«Reply #12 on:2021-04-09 09:57:21 »*

I took it down temporarily as it's all but done and release is imminent.


---

## Post #39 by Fewtch
*«Reply #13 on:2021-04-09 17:10:53 »*

> \*\*Bonez wrote:\*\*
> I took it down temporarily as it's all but done and release is imminent.


**HYPE IMMINENT**


---

## Post #40 by Asherdoom
*«Reply #14 on:2021-05-01 08:33:56 »*

i am very hyped for this mod. Any update? ![:D](https://forums.qhimm.com/Smileys/akyhne/cheesy.gif "Cheesy")


---

## Post #41 by Bonez
*«Reply #15 on:2021-05-01 09:28:56 »*

> \*\*Asherdoom wrote:\*\*
> i am very hyped for this mod. Any update?

I'd say the mod is all together about 97% complete. I'm actually streaming all development of it on Twitch... I'm doing a final full run-through of the game and finding stray sounds/finding things to change or fix along the way. I'm currently at the base of Gaia cliff if that gives you an idea how much time is left. So once I'm through the game, It'll be out... Having said that, I have been doing a thing where you can get a current early copy by redeeming channel points on twitch.


---

## Post #42 by hiqueique
*«Reply #16 on:2021-05-04 12:23:50 »*

Hi!
i'm using the reunion mod. Is there a way to install the files manually?


---

## Post #43 by Bonez
*«Reply #17 on:2021-05-07 02:11:44 »*

Only the main original sounds could be used with Reunion. The other features; ambient sounds, shuffled sounds, fmv sounds and voiced attacks would not be compatible for various reasons.


---

## Post #44 by Xezcente
*«Reply #18 on:2021-05-11 03:55:43 »*

Looks like a lot of work and it does sound nice but shouldn't this be in the WIP section?


---

## Post #45 by Bonez
*«Reply #19 on:2021-05-11 06:47:16 »*

> \*\*Xezcente wrote:\*\*
> Looks like a lot of work and it does sound nice but shouldn't this be in the WIP section?


Technically, maybe. Then again, technically most mods on the site are a WIP - and always will be; we're never quite done with them and always can find *something* to fiddle with. But as you can see, I initially provided a download link to a release - I just took it down temporarily. Plus it would just have to be moved back in a week or two when I'm finished. Not to mention if it was temporarily moved, then there'd still be the "This topic was moved" cluttering up Releases so it would essentially accomplish nothing. Not sure why it's an issue for you, but your rigorous janitorial attitude is appreciated nonetheless. Welcome to the forum.


---

## Post #46 by Psiloc
*«Reply #20 on:2021-06-08 14:47:05 »*

Any chance this is nearing release, or can we have the beta link back? Currently replaying and wouldn't mind trying this out before I'm done ![:)](https://forums.qhimm.com/Smileys/akyhne/smiley.gif "Smiley")

What sort of configuration options were you considering? I'd really like if you could toggle on the new sounds (ambience and footsteps etc.) independently of the replacement sounds for when I'm in a more vanilla kind of mood.


---

## Post #47 by Bonez
*«Reply #21 on:2021-06-10 22:04:21 »*

> \*\*Psiloc wrote:\*\*
> Any chance this is nearing release, or can we have the beta link back? Currently replaying and wouldn't mind trying this out before I'm done
> What sort of configuration options were you considering? I'd really like if you could toggle on the new sounds (ambience and footsteps etc.) independently of the replacement sounds for when I'm in a more vanilla kind of mood.


Not yet. And no because some of the ambient sounds come from the original engine, so you'd have some high-quality-real-life-recording ambience and some original-midi-made-of-static ambience. So ~~un~~fortunately, you have to go with high-quality-real-life recordings for everything ![:)](https://forums.qhimm.com/Smileys/akyhne/smiley.gif "Smiley")


---

## Post #48 by Psiloc
*«Reply #22 on:2021-06-11 09:21:09 »*

> \*\*Bonez wrote:\*\*
> Not yet. And no because some of the ambient sounds come from the original engine, so you'd have some high-quality-real-life-recording ambience and some original-midi-made-of-static ambience. So unfortunately, you have to go with high-quality-real-life recordings for everything


No problem, makes sense and thanks for getting back to me. Keep us posted!

I'd really like that beta link back though... or better yet a newer pre-release! I know that may be hard to prioritise though


---

## Post #49 by Bonez
*«Reply #23 on:2021-07-04 12:40:19 »*

I just wanted to give a bit of an update and explanation for the delay.

Work is nearly done. It's been nearly done for a long time, but there is a reason for that.

As I've said many times I'm going through the entire game and bug squishing. A single playthrough doesn't sound like it should take a long time, but you'd be surprised. The reason that it's taking so long is because I'm not only bug squishing my own mod, but I'm also essentially QA testing the brand new sound engine it's based on at the same time. And now that I'm in the late game in my playthrough, I'm in a largely untested area of the game. There have been many, many times where I've sat down to start working and in the first 5 minutes run into some kind of bug like an infinite looping sound, or an entire sfx channel breaking, and then I have to completely halt the work for anywhere between a day to a week until it's fixed. I literally can't continue because the bug may effect subsequent sounds and I'll miss something. So I have to report the bug, sometimes even help diagnose the bug and wait for a fix before I can continue in order to ensure a complete bug-free-playthrough of the game can be completed (and this doesn't even account for any fixes that may break something earlier in the game. I haven't found any yet, but that isn't to say it hasn't happened. That bridge will just have to be crossed when I get to it). This actually happened tonight, for example. I wanted to play all night, but in my very first fight, I discovered a new bug keeping half the magic sounds from playing. Since literally all of the sounds I have left to replace are in battle, I had to stop and get the bug fixed. Odin's a legend and fixed it at soon as he saw the report, but that was the whole night gone. Of course there have also been the new features being added that have pushed the release back as well; ambient, then battle ambient, then grunts, then footsteps, then ground conditional footsteps... But at this point, they're all done.

That reminds me. If you didn't know, I've now added footstep sounds to the entire game that change depending on what kind of ground you're walking on. So yeah, that's pretty rad.

So that's where we are. all the features are complete, the engine is in a good spot, in my playthrough I'm getting ready to head back and parachute into Midgar. So I'm very close to the end of the game. There are only about 27 sounds left in the game to replace. like 10 of them are in the Gold Saucer arcade, like 5 are Super Nova and the rest are some late game enemy attacks I just haven't come across yet, so we're real close. Barring anymore show-stopping bugs, it should be smooth sailing and closer than ever.


---

## Post #50 by Bonez
*«Reply #24 on:2021-07-11 00:02:03 »*

Cosmo Memory is officially available.


---

## Post #51 by potchy
*«Reply #25 on:2021-07-11 21:57:52 »*

I played through the last section of Midgar (Disc 1) with this mod and it was great!

I got so used to the Remake's amazing voice cast that the original now feels lackluster in comparison, since the characters don't really say anything when attacking.
Those new "hya" voice clips the mod adds are simple yet they help a lot with creating more immersion.

The ambience sounds are also great and they make the good old environments feel a little more unique and fresh.  ![;D](https://forums.qhimm.com/Smileys/akyhne/grin.gif "Grin")
Thanks a lot for this! I would recommend everyone to at least try this out for a bit.


---

## Post #52 by evil_joky
*«Reply #26 on:2021-07-24 16:24:21 »*

Hi guys!
 it is not working for me, have installed ffnx steam version, sfx option on vgmstream and the mod turned on and not working. have i to do something else? could you help me please, guys? my game is  not a jack sparrow copy and i using 7thHeaven-v2.3.1.101


---

## Post #53 by Bonez
*«Reply #27 on:2021-07-25 06:13:12 »*

I've tested it every way I possibly can and have never had it not work. The only thing I can tell you to do is mess with your audio device settings.Join our Discord if you can't figure it out. it'll be a lot easier to troubleshoot from there.


---

## Post #54 by Schoby
*«Reply #28 on:2021-07-25 23:46:06 »*

It doesn't seem to be New Threat 2.0 Compatible. Installed the latest version of 7th Heaven. I have selected that I am using New Threat.


---

## Post #55 by Bonez
*«Reply #29 on:2021-07-28 08:19:11 »*

> \*\*Schoby wrote:\*\*
> It doesn't seem to be New Threat 2.0 Compatible. Installed the latest version of 7th Heaven. I have selected that I am using New Threat.

It definitely is. You're either not using the latest New Threat, your load order is incorrect, or you're using a different language.


---

## Post #56 by olearyf2525
*«Reply #30 on:2021-08-02 05:25:45 »*

This is a beautiful mod bones, thank you for your hard work.


---

## Post #57 by satsuki
*«Reply #31 on:2021-08-02 07:47:25 »*

Do you have any changelog for the revisions ?


---

## Post #58 by Bonez
*«Reply #32 on:2021-08-02 08:07:09 »*

> \*\*satsuki wrote:\*\*
> Do you have any changelog for the revisions ?


Since 1.0:
-Automatic footstep activation
-Automatic VGMStream activation
-Updated New Threat Kernel to 2.0991
-Built in foreign language grunt support for Spanish, German, Italian and French.
-Added New Threat 1.5, 1.5 Vanilla Combat, True Necrosis, Scavenger and other grunt support.

Nothing you need to worry about for SYW, though.


---

## Post #59 by satsuki
*«Reply #33 on:2021-08-02 08:11:43 »*

Great thanks ^^


---

## Post #60 by EliteOne
*«Reply #34 on:2021-08-23 12:06:42 »*

> \*\*Bonez wrote:\*\*
> Since 1.0:
> -Automatic footstep activation
> -Automatic VGMStream activation
> -Updated New Threat Kernel to 2.0991
> -Built in foreign language grunt support for Spanish, German, Italian and French.
> -Added New Threat 1.5, 1.5 Vanilla Combat, True Necrosis, Scavenger and other grunt support.
> Nothing you need to worry about for SYW, though.


Bonez, i'm still using an old 7th Heaven 2.0 version, for 60 FPS animations, so i can't activate this Cosmo Memory mod.

how can i get your old file, for the Sound Effect suite ??


---

## Post #61 by Bonez
*«Reply #35 on:2021-08-24 03:35:48 »*

Do you know that that old 60fps mod that you're using doesn't include interpolated animations so the only thing that's actually running in 60fps is the menu? 7H has never had 60fps character animations.


---

## Post #62 by EliteOne
*«Reply #36 on:2021-08-24 06:37:03 »*

> \*\*Bonez wrote:\*\*
> Do you know that that old 60fps mod doesn't include interpolated animations so the only thing that's actually running in 60fps is the menu?


i know that the creators of 7th Heaven have been promising to add a 60 FPS fix, for over a year, & that there are constant requests for a 60 FPS fix, on these forums.

can i please have the old file, for Bonez Sound Effects suite ??


---

## Post #63 by Bonez
*«Reply #37 on:2021-08-24 09:17:04 »*

Sorry, I'm no longer supporting the old version. I don't even have the old .iro's anymore. But since you're not really experiencing 60fps character animations, you're really not missing out on anything by upgrading.  ![:)](https://forums.qhimm.com/Smileys/akyhne/smiley.gif "Smiley")


---

## Post #64 by heromic
*«Reply #38 on:2021-09-19 07:15:08 »*

This is the best mod alongside the lighting mod!
i have 2 requests / questions:

1. one thing i wish i could do is lower a little just the volume of the footsteps sounds, it's a little loud for my taste.
how can i do it without lowering everything else?
i unpacked the .iro, the footsteps are all from the 5000's range or there's more ogg with them?
i lowered and repacked but it crashes the game.
how can i make loose files only from footsteps for the game? or you can help me with another ways?

2. which is the battle swirl ogg? i like the original from ps1 and wish to use it!
again can i make loose file for the battle swirl sound too? how it works?

thanks in advance!


---

## Post #65 by Bonez
*«Reply #39 on:2021-09-20 05:56:30 »*

Thank you. I appreciate the compliment.

1: There's no way to specifically lower the footsteps sounds. But I'll consider lowering them as a whole If I get enough complaints about it.

1.5: I don't support the mod once it's been unpacked. As you found out, it's pretty easy to break by poking around in there. Unfortunately, once you open it up, it's on you.

2: As far as the battle swirl goes; I spent 2 years carefully mixing and creating sounds for this mod to my own personal tastes. If I started changing sounds or telling people what sounds are what so they could change a single sound, It would be a full time job considering how many requests/suggestions I've gotten -  just because that one sound out of 1300 doesn't jive with their *own* personal taste. So, I hope you understand when I say: If you don't like the new battle swirl, at least the new one isn't made out of pitched static like the original was. You'll get used to it  ![;)](https://forums.qhimm.com/Smileys/akyhne/wink.gif "Wink")


---

## Post #66 by threej
*«Reply #40 on:2021-09-20 20:17:03 »*

I'm loving this mod!  Thanks!

I have two questions, but I'll save the 2nd for later.

When I'm running this mod, the game crashes when I enter the secret hallway in Wutai to get the Magic Shuriken.  This crash is 100% consistent for me, even when it's the only mod I have activated.  I'm running ff7 through 7th heaven.

If its just my setup, it's NBD as it's a 30 second workaround to turn the mod off.  But the consistency of it, plus the more "hidden" location, make me curious if the bug is in the mod itself.  Have you playtested this hallway?

Thanks!


---

## Post #67 by Bonez
*«Reply #41 on:2021-09-21 10:08:54 »*

> \*\*threej wrote:\*\*
> I'm loving this mod!  Thanks!
> I have two questions, but I'll save the 2nd for later.
> When I'm running this mod, the game crashes when I enter the secret hallway in Wutai to get the Magic Shuriken.  This crash is 100% consistent for me, even when it's the only mod I have activated.  I'm running ff7 through 7th heaven.
> If its just my setup, it's NBD as it's a 30 second workaround to turn the mod off.  But the consistency of it, plus the more "hidden" location, make me curious if the bug is in the mod itself.  Have you playtested this hallway?
> Thanks!

You're talking about this hallway?:
<https://imgur.com/a/rjRjrQo>
I just tested it and it seems fine. No crashes here - with a bunch of mods on and with just CM on. I know I've also been there before while playtesting. There's nothing in CM that should cause any kind of crashes, at least not in this particular case. It's just sound files. ¯\\_(ツ)\_/¯


---

## Post #68 by threej
*«Reply #42 on:2021-09-21 22:25:38 »*

No, that's the secret hallway for the Hairpin, which also worked fine for me.  The hall for the magic shuriken is in the same building, attached to the room you sleep.

(see arrow for "treasure": <https://www.almarsguides.com/AlmarsImages/Retro/Walkthroughs/PS1/FinalFantasyVII/SideQuests/Wutai/Wutai%20back%20half%201.png>).

I appreciate you double checking this!  I don't know why the mod would cause this either, but it's at least linked somehow in my setup. Thanks!


---

## Post #69 by Bonez
*«Reply #43 on:2021-09-23 06:18:26 »*

> \*\*threej wrote:\*\*
> No, that's the secret hallway for the Hairpin, which also worked fine for me.  The hall for the magic shuriken is in the same building, attached to the room you sleep.
> (see arrow for "treasure":
> https://www.almarsguides.com/AlmarsImages/Retro/Walkthroughs/PS1/FinalFantasyVII/SideQuests/Wutai/Wutai%20back%20half%201.png
> ).
> I appreciate you double checking this!  I don't know why the mod would cause this either, but it's at least linked somehow in my setup. Thanks!


That one also works for me.


---

## Post #70 by threej
*«Reply #44 on:2021-09-24 05:27:40 »*

Got it, thanks!

2nd Question:  Footsteps aren't working for me.  I have menu sounds, voiced attacks, field and battle ambience, and movie sounds.  But no footsteps (even though it is turned on in my config).

Anyone have suggestions from anyone how I can hunt down the problem/fix this?


---

## Post #71 by Bonez
*«Reply #45 on:2021-09-27 07:44:51 »*

> \*\*threej wrote:\*\*
> Got it, thanks!
> 2nd Question:  Footsteps aren't working for me.  I have menu sounds, voiced attacks, field and battle ambience, and movie sounds.  But no footsteps (even though it is turned on in my config).
> Anyone have suggestions from anyone how I can hunt down the problem/fix this?


Update both 7h and FFNx to Canary.


---

## Post #72 by nairik25
*«Reply #46 on:2022-01-31 13:57:19 »*

Hello good, would it be possible to create an iro file with only the sound of the footsteps and the voices of the battle attacks?

Personally, I don't like the sound when battles are skipping in this mod, but I love the footsteps and attack voices.


---

## Post #73 by Bonez
*«Reply #47 on:2022-02-03 02:34:01 »*

Already answered you on Nexus, but the answer is no.


---

## Post #74 by Mindman
*«Reply #48 on:2022-02-15 14:37:52 »*

Just started a new playthrough with this mod using 7th Heaven, it's the only sound mod I'm using. I'm noticing a consistent, random crackling sound when playing. All 7th Heaven sound settings are at the defaults.

Any thoughts or suggestions on this?


---

## Post #75 by Bonez
*«Reply #49 on:2022-02-15 22:32:21 »*

Yeah, we had some sound issues with a couple of the recent versions of FFNx... Make sure you're on the latest canary .194+ and all sound issues should be good for now.


---

## Post #76 by Mindman
*«Reply #50 on:2022-02-16 16:14:27 »*

> \*\*Bonez wrote:\*\*
> Yeah, we had some sound issues with a couple of the recent versions of FFNx... Make sure you're on the latest canary .194+ and all sound issues should be good for now.


Thanks, that fixed about 95% of the popping/crackling. It was sounding like Rice Krispies for a bit there. ![;)](https://forums.qhimm.com/Smileys/akyhne/wink.gif "Wink")


---

## Post #77 by olearyf2525
*«Reply #51 on:2022-02-27 07:38:50 »*

Hey I updated recently and I've been having no sound effects/footsteps/menu noises and when I enter a battle the game crashes. A couple people on nexus recently commented on Ninostyle's mod and were wondering if it caused it, they were having the same issue. This mod and FFNX are the only things I updated recently though.

Edit: I think it may be FFNX, I turned off Cosmo memory and same issue. Also Ninostyle's chibi models are no longer showing up in field for me.


---

## Post #78 by Bonez
*«Reply #52 on:2022-02-27 10:16:32 »*

> \*\*olearyf2525 wrote:\*\*
> Hey I updated recently and I've been having no sound effects/footsteps/menu noises and when I enter a battle the game crashes. A couple people on nexus recently commented on Ninostyle's mod and were wondering if it caused it, they were having the same issue. This mod and FFNX are the only things I updated recently though.
> Edit: I think it may be FFNX, I turned off Cosmo memory and same issue. Also Ninostyle's chibi models are no longer showing up in field for me.


I'm not sure. I'm running the latest FFNx (at the moment 1.10.1.228) and sound is fine.


---

## Post #79 by AlbusJC
*«Reply #53 on:2022-03-01 23:10:19 »*

Hi! Let me tell you that your mod looks really awesome! I have a problem with it, I don't know if this is just me or not. The footstep sound on the world map are not heard no matter what I do. I've tried disabling all the other mods I have and nothing. I have the latest version of 7th heaven and FFnx (canary). Is there anything else I can do? Everything else works perfectly: ambient sound, footsteps sound in the field, battle voices...

Thanks a lot!


---

## Post #80 by Bonez
*«Reply #54 on:2022-03-02 00:35:23 »*

> \*\*AlbusJC wrote:\*\*
> Hi! Let me tell you that your mod looks really awesome! I have a problem with it, I don't know if this is just me or not. The footstep sound on the world map are not heard no matter what I do. I've tried disabling all the other mods I have and nothing. I have the latest version of 7th heaven and FFnx (canary). Is there anything else I can do? Everything else works perfectly: ambient sound, footsteps sound in the field, battle voices...
> Thanks a lot!


Did you turn them on? And are you using Cid on the world map? Because Cid's broken right now.


---

## Post #81 by AlbusJC
*«Reply #55 on:2022-03-02 12:31:42 »*

Yes, I have both options active. And no, I am using Cloud the first time they leave Midgar.

Edit: I updated 7th Heaven again and this time I was able to update ffnx from the program and it finally works perfectly. Thanks for everything, it looks awesome...


---

## Post #82 by Aynath
*«Reply #56 on:2022-03-13 19:20:57 »*

Hi Bonez,

I've been using the Cosmo Memory mod along side other mods as well for a complete new experience of the game. So far so good, until I got Cid. I was hyped especially mainly for the voiced attacks. I don't know why but Cid's Voiced Attacks (and Attack sounds) are the same as Cloud's. It's not gamebreaking fortunately but it sure feels very weird to hear Cloud twice as much while in battle. When I use Boost Jump from Cid, he seems to have another voice though so maybe it's just a bug... Is it a known bug ? How can I fix this ?

Thank you so much for the mod !


---

## Post #83 by Bonez
*«Reply #57 on:2022-03-14 08:16:40 »*

> \*\*Aynath wrote:\*\*
> Hi Bonez,
> I've been using the Cosmo Memory mod along side other mods as well for a complete new experience of the game. So far so good, until I got Cid. I was hyped especially mainly for the voiced attacks. I don't know why but Cid's Voiced Attacks (and Attack sounds) are the same as Cloud's. It's not gamebreaking fortunately but it sure feels very weird to hear Cloud twice as much while in battle. When I use Boost Jump from Cid, he seems to have another voice though so maybe it's just a bug... Is it a known bug ? How can I fix this ?
> Thank you so much for the mod !


No, sorry. They use different sounds and are voiced by two different people. I double checked the code, in-game and verified with trace dump:

![](https://imgur.com/A9ZPZ1R.png)

Cloud:
<https://voca.ro/1bZsBbisU67p>

Cid:
<https://voca.ro/1nSlJ5tJWDaa>

That is to say, unless you're using something like New Threat that has custom/swappable weapons or has made changes to weapon sounds, in which case it's totally possible (I know there is one particular weapon that can be used by either aerith or cid, so you'd hear cid grunt when aerith uses it) and there's nothing I could really do about that. If you're using the base game though, no, they're different.


---

## Post #84 by Aynath
*«Reply #58 on:2022-03-14 17:12:58 »*

Ah well I'm using NT mod v2 as well, in deed Cid and Aerith share a few weapons. In my case though, Cid and Cloud are using the same sound for some reason. I'll try to reinstall the mod on my side, praying that it will work. In any case ever since I've played with this mod, I cannot think of ever going back.

EDIT : I tried to disable, then reinstall the mod, actually the bug doesn't come from it. Cid's Attacks do the same sound as Cloud's. I also disabled the NT mod to check up; Cid still has Cloud's sounds. It's weird because the mods that alter the sounds whatsoever are Cosmo Memory, NT Mod (due to weapon swap) and EDMusic.

EDIT : Well it seems to come from the 60 FPS mod. Disabling it restored Cid's Sound Attacks


---

## Post #85 by Bonez
*«Reply #59 on:2022-03-14 20:08:04 »*

Yeah, good catch. It does seem to be 60fps. Thanks for the git report on it.


---

## Post #86 by acrossmacross
*«Reply #60 on:2022-05-29 15:11:17 »*

Seems this mod is now causing crashing under 7th Heaven 2.4.0.37 and FFNx 1.11.0.44 just FYI


---

## Post #87 by Bonez
*«Reply #61 on:2022-05-30 10:13:01 »*

> \*\*acrossmacross wrote:\*\*
> Seems this mod is now causing crashing under 7th Heaven 2.4.0.37 and FFNx 1.11.0.44 just FYI


Fix already out. Update ffnx.


---

## Post #88 by markul
*«Reply #62 on:2022-09-11 14:20:11 »*

Hi Bonez,
i want to report a bug  related to Cosmo Memory .

Recently i was using your mod and I noticed that, when i disable the mod, all the sounds of the game are muted(music still work). I tried to close and open again the 7th heaven , but nothing, sounds only work now with your mod activated .I have the last version (stable) of 7H and FFnx. I was thinking that could be some config related from your mod to FFnx or something like that??
Edit: Oh, the mod is the last version from the Qhimm Catalog.


---

## Post #89 by Bonez
*«Reply #63 on:2022-09-11 21:34:00 »*

Your ffnx.toml file is getting stuck in the "using Cosmo memory" mode... This happens usually after a crash and is persistent until you change it manually. Should be fixed in canary 7h builds.


---

## Post #90 by markul
*«Reply #64 on:2022-09-12 16:33:01 »*

> \*\*Bonez wrote:\*\*
> Your ffnx.toml file is getting stuck in the "using Cosmo memory" mode... This happens usually after a crash and is persistent until you change it manually. Should be fixed in canary 7h builds.

Ok, thanks!
I suppose that are this configs in the file:  "use\_external\_sfx"  "ff7\_footsteps"  "external\_sfx\_always\_centered", i set them to false, and it seems that now it works.


---

## Post #91 by natepley
*«Reply #65 on:2022-09-18 12:22:02 »*

This mod is fantastic!  Thank you for making this!
I would really appreciate an option to disable the replacement of all the sound effects, while still having footsteps, ambient sounds, and attack voices.  I really want to hear the original sound effects because they have a special place in my heart, but I feel like I can't live without the footsteps and ambient noise now.  Would that be a possibility?  Thanks again!


---

## Post #92 by Bonez
*«Reply #66 on:2022-09-18 13:27:20 »*

No. There are several technical reasons for why. Among which; a few of the fields have a stock ambience, so if you used the vanilla sounds, you'd have some fields with super high def ambience and some with crushed midi ambience. Secondly, I don't want a hodgepodge mod where you'd have real recordings of birds etc. and all the other battle sfx are staticy-midi... But most importantly, Cosmo Memory is a sfx replacement mod for the 724 vanilla sounds first and foremost. The other features like ambience, footsteps, etc. are just bells and whistles to go on top of them.


---

## Post #93 by natepley
*«Reply #67 on:2022-09-18 13:41:18 »*

> \*\*Bonez wrote:\*\*
> No. There are several technical reasons for why. Among which; a few of the fields have a stock ambience, so if you used the vanilla sounds, you'd have some fields with super high def ambience and some with crushed midi ambience. Secondly, I don't want a hodgepodge mod where you'd have real recordings of birds etc. and all the other battle sfx are staticy-midi... But most importantly, Cosmo Memory is a sfx replacement mod for the 724 vanilla sounds first and foremost. The other features like ambience, footsteps, etc. are just bells and whistles to go on top of them.


I see.  Thanks for the explanation.  I really do think the "bells and whistles" are so fantastic that they warrant their own mod, though.  A standalone mod that just replaces all ambient noises and adds footsteps would a great option and would leave Cosmo Memory intact as a sound replacement mod.  I understand if you don't want to do that, though.


---

## Post #94 by sangrefria
*«Reply #68 on:2022-09-26 14:43:58 »*

First of all, fantastic work that was done with this great mod! ![:)](https://forums.qhimm.com/Smileys/akyhne/smiley.gif "Smiley")
I only have a little issue:
Since I updated both FFnx and 7th heaven to the newest versions (1.14.0.1 and 2.7.0.1) , there is no fx sound at all (menu, etc.) whenever I want to play with the music settings on VGMStream.
On the other hand, the mod runs without any problems if the music is set to MIDI sound.
The same happens with the stable versions of 7th heaven and FFnx.


---

## Post #95 by leatitia
*«Reply #69 on:2022-12-07 09:39:51 »*

You are truly amazing!


---

## Post #96 by SquallLeonhart
*«Reply #70 on:2023-03-08 10:26:02 »*

Guys, I've recently been playing FFVII and I'm using [Tsuna Mods] Cosmo Memory, and I noticed that the Field footstep it works correctly, the question is if you use the Analog Stick the Cloud runs but it only produces the sound of walking, if you use the button A or X even when running on analog it already produces the sound of running instead of walking, well it must be a bug on analog stick, because if you use the D-pad the cloud walks and produces the sound of walking, if you press the A or X depending on the control we have, it runs and produces the sound of running, that is, it is correct with the D-pad, as for the Analog stick, it does not walk, it automatically runs! and it doesn't produce the sound of running but of walking, so it must be a bug, try it yourself ands fix it please if its a bug, thankyou!


---

## Post #97 by Bonez
*«Reply #71 on:2023-03-09 01:56:58 »*

Yeah, the analog autorun is new. Hopefully they can be fixed to work in tandem. In the meantime, the only thing you could do is turn off the analog controls in 7h driver settings and use the actual autorun mod from "Gameplay Tweaks" (you would just miss out on the omni-directional movement), or the better option is you can use both analog control + the actual autorun mod which will essentially always play running footsteps by default but you can still walk and hear walking footsteps by lightly pressing the analog stick+cancel button (since you're using the analog controls, you're probably rarely walking anyway), or of course turn off footsteps all together.


---

## Post #98 by Loran
*«Reply #72 on:2023-07-04 08:29:12 »*

Hello , first of all amazing job! I really appreciate what you did for the game , thank you!!
I had a question regarding Echo-s compatibility. in 7H should Cosmo go above in the load order? Do I need to touch any of the settings or are both already compatible as they are? Thanks!


---

## Post #99 by Bonez
*«Reply #73 on:2023-07-04 13:33:15 »*

Yeah CM should be above Echo-s. Autosort should do this automatically. And there's nothing special you need to do. They're designed to work together out of the box.


---

## Post #100 by Bonez
*«Reply #74 on:2023-08-30 06:59:12 »*

> \*\*seijuro wrote:\*\*
> Is there a way to extract this to use the voiced attacks/grunts ONLY? Would love to try to that out to keep it closer to the Vanilla experience.


Use echo-s and turn the voice layer down.


---

## Post #101 by Final_Figue
*«Reply #75 on:2023-09-10 01:13:07 »*

Hello Bonez.

This is not an issue, only a request if its posible: I´m playing New Threat 2.0 and everything is fine, but Aeris voice changed on disc2 for Barret, I asume that this mode is made for the original game. Could be posible an update for N.T.? And what about the phrases during battle ("I´m not interested"), could be posible to add them, too?

Well, thank you for reading me and for your mod, too.

*\* Sorry for my poor english.*


---

## Post #102 by Bonez
*«Reply #76 on:2023-09-11 12:15:48 »*

> \*\*Final\_Figue wrote:\*\*
> Hello Bonez.
> This is not an issue, only a request if its posible: I´m playing New Threat 2.0 and everything is fine, but Aeris voice changed on disc2 for Barret, I asume that this mode is made for the original game. Could be posible an update for N.T.? And what about the phrases during battle ("I´m not interested"), could be posible to add them, too?
> Well, thank you for reading me and for your mod, too.
> \* Sorry for my poor english.


Are you talking about their battle grunts? You're hearing aerith shoot barret's gun and use his grunt?

Or are you talking about when Aerith uses Cid's weapon and she uses Cid's voice? If that's what you're talking about, yeah I'm aware. The sounds are tied to the weapons, not the characters. I have a way to fix it, I just haven't gotten around to it.


---

## Post #103 by Final_Figue
*«Reply #77 on:2023-09-12 21:35:19 »*

Hello Bonez.

I was testing a file of a past gameplay to send it to you, but the problem It wasn´t there anymore, you update your mod, right? Indeed, It was her grunt, she used Barret´s.

I´ll continue testing the game, thank you so much again for your mod.


---

## Post #104 by Bonez
*«Reply #78 on:2023-09-13 06:21:08 »*

It's straight up impossible for Aerith to use Barret's grunt because she doesn't use a gun. you had to be hearing Cid's


---

## Post #105 by Final_Figue
*«Reply #79 on:2023-09-16 16:13:37 »*

> \*\*Quote wrote:\*\*
> you had to be hearing Cid's


Indeed, you´re right, my mistake.


---

## Post #106 by Tifa
*«Reply #80 on:2023-09-17 08:12:18 »*

Hello, i've been using the mods and so far most of them are simply fantastic. There's one thing that let me a bit unsatisfied with the [Tsunamods]Cosmo Memory mod though, which is that i'm unable to select if i want or not the changed sound effects. I can see that there's the possibility to enable or disable battle grunts as example and others stuff but there's no option to disable the changed SFX that comes with this Mod. Maybe a little update could solve it?I'd love keeping the battle grunts enabled which in fact i do, but also having the possiblility to keep the original SFX would be nice. I saw that the battle grunts are the same coming from the echo-s mod as well. I'm wondering if its possible also taking the battle lines from that mod(?) I think it would be good having those options.


---

## Post #107 by Bonez
*«Reply #81 on:2023-09-17 10:15:21 »*

Surprisingly, you can't turn off the replacement sound effects in the sound effect replacement mod.


> \*\*Bonez wrote:\*\*
> No. There are several technical reasons for why. Among which; it's impossible to use the stock engine for some sounds and the new engine for others. It's all one way or the other. Also few of the fields have a stock ambience, so if you did use the vanilla sounds, you'd have some fields with super high def ambience and some with crushed midi ambience. There are several areas in the game where doing this would be very awkward or be outright cringe. Secondly, I don't want a hodgepodge mod where you'd have real recordings of birds etc. and all the other battle sfx are staticy-midi... But most importantly, Cosmo Memory is a sfx replacement mod for the 724 vanilla sounds first and foremost. The other features like ambience, footsteps, etc. are just bells and whistles to go on top of them.


---

## Post #108 by noteworthycamp
*«Reply #82 on:2023-09-18 22:19:02 »*

hello. new member here. first of thank you so much for this incredible work. second, i want to report that i got a presumably insignificant bug here. so apparently whenever the mod intro plays, the game gets slow down quite abit, resulting in choppy sounds. i dont know if the problem comes from the mod or actually from my device. a pretty insignificant one so far. it only happens when you bootup the game and the mod intro plays. anything else working properly. i have tried disabling other mods, but nothing change

btw, i use both of the canary build.


---

## Post #109 by yomaus
*«Reply #83 on:2023-11-04 03:03:44 »*

Heloo, found a bug on the submarine minigame, the game get stuck with an endles sound of warnings, even after ending the game the sound is stuck, it goes away only after reseting. Im using last update of stable or canary FFNX 1.16 and 7thHeaven 3.2.0.0. And some other mods like NT 2.0. Byee.


---

## Post #110 by keanumonty104
*«Reply #84 on:2024-01-14 12:05:42 »*

Can you tell me what im doing wrong here? i installed 7th heaven and using canary channel for both that and ffnx , all other mods are working but when i download and enable the cosmo memory mod i get no sound, please help


---

## Post #111 by exitwounds85
*«Reply #85 on:2024-02-10 23:32:22 »*

> \*\*keanumonty104 wrote:\*\*
> Can you tell me what im doing wrong here? i installed 7th heaven and using canary channel for both that and ffnx , all other mods are working but when i download and enable the cosmo memory mod i get no sound, please help


just did the same...then i noticed my pc was trying to use my ps4 controller for the sound device instead of my headset.


---

## Post #112 by toratan
*«Reply #86 on:2024-03-05 02:09:09 »*

Hi, thank you for the wonderful mod.

I personally prefer not to have the added ambience everywhere but there is an issue when disabling that. The background noise in the truck during the kalm flashback is absent. I realise it is technically ambient sound, but I believe it could more accurately be characterised as a necessary sfx for this scene. Would it be possible to have two options? one option for disabling additional ambience and an option for disabling all ambience including those sequences that had ambient sounds in the original game.


---

## Post #113 by ValentDs
*«Reply #87 on:2024-03-17 18:52:38 »*

can we have the max only version? i love the footstep and ambience, but i want the OG sound effects during battle, is that version who can do that?


---

## Post #114 by kanelakis
*«Reply #88 on:2024-03-21 17:02:14 »*

> \*\*Bonez wrote:\*\*
> Formerly known as "Bonez' Sound Effect Suite". Cosmo Memory uses the new FFNx SFX engine and is an entirely new mod rebuilt from the ground up with a ton of new features. This project started out in 2018 as a little mod to just replace the FF7 menu sounds with the menu sounds from FFXIII. Since that time, it has evolved into something far more... After following the community and modding the game for several years, I noticed the graphical and musical mods were growing and advancing but the sound effects department was totally stalled. I mean, it's an entire 1/3 of what your senses are taking in, along side the visuals and music! I wanted something to match the beautiful/advanced graphical and musical mods provided by the very talented authors/creators of this community... So, I present to you Cosmo Memory: A Complete Sound Overhaul.
> Features:
> Replaces/updates
> all
> 724 original sound effects including battle, magic, enemy skills, limit breaks, summons, world
> NEW Ambient sounds for
> every
> field and battle scene in the game
> Ground-conditional footstep sound effects for every field and world map
> Replaces
> all
> sound effects in cutscene videos (Compatible with any FMV video)
> Voiced attacks or "grunts" for all party members
> Shuffled battle impact sounds as well as other select sounds randomly so you never hear the same exact sound twice in a row
> 3 selectable menu sound sets
> Complete compatibility with New Threat, Echo-S and any other mod
> Each feature is optional
> Launch Trailer:
> https://www.youtube.com/watch?v=Zt0GRSb8KcA
> IMPORTANT
> -This mod
> REQUIRES
> 7th Heaven 2.4+ and FFNx 1.11+
> You can download the latest 7th Heaven here :
> https://github.com/tsunamods-codes/7th-Heaven/releases/tag/canary
> -For best experience, use headphones and set music volume to ~60%
> FAQ
> Will you add the option to/Can I turn off the replaced sfx?
> Spoiler:
> show
> No. There are several technical reasons for why. I won't go into all of them, but among which; it's impossible to use the stock engine for some sounds and the new engine for others. It's all one way or the other. If you were to "just stick on the ambience", then the new engine would be used for the ambience and you'd get no other sfx at all. Also a few of the fields have a stock ambience, so if you did import the vanilla sounds to the new engine, you'd have some fields with super high def ambience and some with crushed midi vanilla ambience. There are several areas in the game where doing this would be very awkward or be outright cringe. Some people suggest to change everything except battle sounds. The thing about that is many, many sounds are reused throughout the game. Just one example, a wave sound: The wave sound may be used in battle for the sewer monster, or Leviathan, but also used near the ocean. So, when you're near the ocean you'd suddenly hear midi waves next to HD sounds. This happens with probably
> half
> of the sounds in the game. There is also dealing with the complexities the mod adds like shuffled melee sounds. Setting up contingencies for if replaced battle sounds are off would compound those complexities. Which leads me to my second reason - I just don't want a hodgepodge mod where you'd have real recordings of birds etc. clashing against staticy-midi battle sounds. This was the problem with previous incomplete sfx mods for FF7. They
> only
> changed a hand full of battle sounds, which clashed against other battle sounds immediately surrounding them... Which leads me to most importantly; Cosmo Memory is a sfx replacement mod for the 724 vanilla sounds first and foremost. Identifying and making and editing and replacing them took 2 years to complete. That is the entire purpose of the mod - to update
> everything
> . The same way Nino replaces every model in the game, the same way SYW updates every field in the game, and the same way any music mod replaces every song in the game. The other features like ambience, footsteps, etc. were just last minute bells and whistles to go on top of them thrown in during the final couple weeks of development.
> Most of the FF7 modder's philosophies are to provide the remake everyone really wanted. If Square had made the 1:1 remake, they wouldn't have used those original sounds...
> Special Thanks:
> TrueOdin - the FFNx sound engine
> vertex2995 - world map footsteps
> Download Cosmo Memory HERE
> Size: 350MB
> If you enjoy the mod, consider a little something for the many many hours it took to put this together:
> Donate Here


Hi dear, your cosmo memory mod is fabulous, I would like to ask you something, is it possible to restore only the sound of the limit break, because I like the original more, even if it is a separate mod that I can add without it conflicting with the mod itself, let me know.


---

## Post #115 by Bonez
*«Reply #89 on:2024-03-22 06:28:06 »*

> \*\*kanelakis wrote:\*\*
> Hi dear, your cosmo memory mod is fabulous, I would like to ask you something, is it possible to restore only the sound of the limit break, because I like the original more, even if it is a separate mod that I can add without it conflicting with the mod itself, let me know.


I've been taking a bit of a break to play through Rebirth. Once I'm finished, I'm going to complete this ESUI theme project I've been working on, but once I'm finished with that I'm going back to CM and go through some sounds and try making some of the more iconic sounds more similar to their old sound. The limit break sound in particular is one that comes up often and I have a new replacement for it to give you an idea of what I'm trying to do with them.

OG
<https://voca.ro/1ctSTEvUqd1v>

Old CM
<https://voca.ro/13Eb9gCJuhab>

New CM
<https://voca.ro/1byj1yjhqahc>


---

## Post #116 by kanelakis
*«Reply #90 on:2024-03-22 16:36:42 »*

> \*\*Bonez wrote:\*\*
> I've been taking a bit of a break to play through Rebirth. Once I'm finished, I'm going to complete this ESUI theme project I've been working on, but once I'm finished with that I'm going back to CM and go through some sounds and try making some of the more iconic sounds more similar to their old sound. The limit break sound in particular is one that comes up often and I have a new replacement for it to give you an idea of what I'm trying to do with them.
> OG
> https://voca.ro/1ctSTEvUqd1v
> Old CM
> https://voca.ro/13Eb9gCJuhab
> New CM
> https://voca.ro/1byj1yjhqahc


This is perfect:
OG
<https://voca.ro/1ctSTEvUqd1v>
How can I put it in 7th Heaven?


---

## Post #117 by Bonez
*«Reply #91 on:2024-03-23 00:33:23 »*

It's the "New CM" one that's going in.


---

## Post #118 by kanelakis
*«Reply #92 on:2024-03-24 20:54:50 »*

> \*\*Bonez wrote:\*\*
> It's the "New CM" one that's going in.

So it's not possible to put it separately within the mod itself,if one wants to leave the sound of the limit unchanged?


---

## Post #119 by ValentDs
*«Reply #93 on:2024-03-25 08:26:29 »*

we'll wait the end of rebirth then, but there's no option to have all sound effects from battle exactly like the original (magic, sword, limit, all) but all the footsteps environment sounds outside battle?


---

## Post #120 by Mercinarie
*«Reply #94 on:2024-04-04 06:46:58 »*

Hey guy's I'm having a weird issue where if I turn off Cosmo Memory, I no longer have any SFX at all, Music yes but no additional SFX IE menu and battle sounds
But if I re-enable Cosmo Memory, I have the Cosmo Memory SFX.

Is there a setting or some issue I'm unaware of to get the Original SFX to work again?

So far I've tried:
Turn the mod off in 7th heaven and then uninstall it
Leaving the mod available but turned off
Changing the audio output in the ff7 config and windows
Changing the volume in the game menu
Setting to run though Centre SFX on / off then uninstalling
Checking Sound settings in windows

I've tried searching for a while now but haven't found any info thanks for any assistance
Hope you're all having a great time with Rebirth!


---

## Post #121 by Bonez
*«Reply #95 on:2024-04-06 22:24:10 »*

> \*\*Mercinarie wrote:\*\*
> Hey guy's I'm having a weird issue where if I turn off Cosmo Memory, I no longer have any SFX at all, Music yes but no additional SFX IE menu and battle sounds
> But if I re-enable Cosmo Memory, I have the Cosmo Memory SFX.
> Is there a setting or some issue I'm unaware of to get the Original SFX to work again?
> So far I've tried:
> Turn the mod off in 7th heaven and then uninstall it
> Leaving the mod available but turned off
> Changing the audio output in the ff7 config and windows
> Changing the volume in the game menu
> Setting to run though Centre SFX on / off then uninstalling
> Checking Sound settings in windows
> I've tried searching for a while now but haven't found any info thanks for any assistance
> Hope you're all having a great time with Rebirth!

Driver settings>Reset Defaults.


---

## Post #122 by ap3nr0ts
*«Reply #96 on:2024-05-13 21:33:12 »*

Hi! I'd like to highlight a very minor bug. Whenever I enable this mod, the "ticking" points sound in the victory window seems to hiccup every second or so. It doesn't matter which setting I choose: only disabling the mod fixes it. You usually skip the window as fast as possible, but it still slightly annoys me, haha. Is this just standard? Without the mod everything sounds fine. I do use the FFNx audio and most SYW mods too.


---

## Post #123 by kanelakis
*«Reply #97 on:2024-05-27 23:02:23 »*

> \*\*Bonez wrote:\*\*
> It's the "New CM" one that's going in.

I thought about this and I hope it can be done, is it possible to externalize all the sound variations of the Limit Break, including the original one, without touching the one integrated into the mod?
So one can freely choose the one he likes most, as you did for other sounds such as voices, steps etc...


---

## Post #124 by GeoffreyMc Jefferson
*«Reply #98 on:2024-07-13 17:17:19 »*

Is there a way a disable the new battle sounds? I tried disabling everything except the step sounds but the battle sounds still sound wrong to me.

I'd really like to keep those nostalgic sounds and only add the step sounds to that.


---

## Post #125 by Bonez
*«Reply #99 on:2024-07-15 03:56:19 »*

> \*\*GeoffreyMc Jefferson wrote:\*\*
> Is there a way a disable the new battle sounds? I tried disabling everything except the step sounds but the battle sounds still sound wrong to me.
> I'd really like to keep those nostalgic sounds and only add the step sounds to that.


Read first post.


---

## Post #126 by Kaij
*«Reply #100 on:2024-09-03 11:48:46 »*

I'm struggling with audio crackling, ive tried everything and nothing seems to fix it, running newest canary build, and tried newest stable build.

Any thoughts?
mods running -
ninostyle
Cosmo memory
upscalers

nothing else..


---

## Post #127 by Kuraudo
*«Reply #101 on:2024-09-04 03:24:29 »*

~~Hey Kaij, Which audio effect is crackling the most?~~ this was solved on Discord by just hitting Reset Defaults in Game Launcher settings.


---

## Post #128 by KohryuZX
*«Reply #102 on:2024-09-30 09:33:22 »*

Is there a way to have the voiced attacks but keep the vanilla PSX sound effects?


---

## Post #129 by Kuraudo
*«Reply #103 on:2024-10-01 08:31:47 »*

> \*\*KohryuZX wrote:\*\*
> Is there a way to have the voiced attacks but keep the vanilla PSX sound effects?

Yes, you can play Echo-S 7.


---

## Post #130 by KohryuZX
*«Reply #104 on:2024-10-24 19:04:54 »*

not compatible with new threat


---

## Post #131 by Bonez
*«Reply #105 on:2024-10-25 10:17:30 »*

The answer is no.


---

## Post #132 by Ultroman
*«Reply #106 on:2025-04-22 00:36:54 »*

This mod is absolutely awesome! I love the ground-conditional footsteps! That must have been quite an undertaking to do. My only gripe is that IMO they're a bit loud in relation to other sounds, as are the ambience sounds. I found the Ambience Volume setting in the 7th Heaven Game Launcher settings, so that's all dandy, but there's nothing for the footstep sounds. Is it at all possible to add a slider/setting for those? It would be highly appreciated <3


---

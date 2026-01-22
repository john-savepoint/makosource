---
topic_id: 30282
board_id: 38
title: "7H Package for Yamaha MU80 XG Soundtrack Mod"
author: "Template"
replies: 5
views: 4803
last_post: "2025-12-09 02:46:42"
url: "https://forums.qhimm.com/index.php?topic=30282.0"
scraped_at: "2025-12-29T12:57:10.450343"
---

# 7H Package for Yamaha MU80 XG Soundtrack Mod

*Originally posted by **Template** • 4803 views • 5 replies*

---

## Post #1 by Template
*«on:2025-10-31 19:52:35 »*

Hey all, hope everyone is well.
I was playing around with soundtracks and stumbled across the Yamaha MU80 hardware render of the XG midi files and I really like them.
Since there wasn't an .iro package I could find for it, I decided to build one, you can download it from my google drive:
<https://drive.google.com/file/d/1W4LAlsLpTAEPIjgWefkkemwyFv-oa23t/view?usp=sharing>
--OR INSTALL VIA 7TH HEAVEN MOD MANAGER--

![](https://staticdelivery.nexusmods.com/mods/790/images/thumbnails/60/60-1661714546-1773181573.png)
The original mod page is at Nexus Mods: <https://www.nexusmods.com/finalfantasy7/mods/60?tab=description>

Edit: After much testing, I decided it's better to install this mod with 7th Heaven without using the iro file compression, which is easy to do, you just set up everything you need to make the iro work and then you just don't compress the folder into an iro and put it in the 7th Heaven library directory raw.

Edit to bump version: Added a line to the mod xml for syncing the audio with ffnx, not sure if it's needed. I guess it's v1.101 now.


---

## Post #2 by Template
*«Reply #1 on:2025-11-28 22:30:59 »*

I didn't bump the version number because it doesn't really matter, but I ninja updated the file package with newly normalized audio files, figured out how to get the new opening movie sequence process built and synced up right, and I got this sucker published on the 7H Qhimm catalog! I hope even just 1 person gets some enjoyment out of this old soundtrack version--I think the sound is pretty studio fat, lots of warmth and low-end weight, some cool sound effects in some of the tracks that I wouldn't have expected from a purely midi based setup. It's sophisticated, but as quirky and familiar as ever.


---

## Post #3 by Kuraudo
*«Reply #2 on:2025-12-03 07:15:49 »*

Thank you Template! Great option to have on 7H catalog.
Quick one: How do you compare this soundtrack to Deet's XG Music mod (Yamaha S-YXG50 SoftSynthesizer)? What are the main differences?


---

## Post #4 by Template
*«Reply #3 on:2025-12-04 20:10:19 »*

> \*\*Kuraudo wrote:\*\*
> Thank you Template! Great option to have on 7H catalog.
> Quick one: How do you compare this soundtrack to Deet's XG Music mod (Yamaha S-YXG50 SoftSynthesizer)? What are the main differences?

Hey thanks Kuraudo,

Generally, the MU80 mod should be "cleaner". As I understand it, the MU80 hardware synth uses 16-bit uncompressed samples and the S-YXG50 uses 8-bit compressed. It's amazing how well the software synth emulates the MU hardware synthesizers from this era, which all use the same/similar, much higher-quality, wave ROMs. People have tried to rework the S-YXG50 dlls to fit the uncompressed samples in, but I am not sure if anyone has been successful. Yamaha really went out of their way to keep the S-YXG50 in its product category.

I'd point to the differences when A/Bing ob.ogg--the S-YXG50 is essentially emulating the MU80, so, the differences are subtle, but you have this drop in tone quality, some instruments more than others. E.g., on ob.ogg there is this piercing whistle sound about 14 seconds in on the S-YXG50 version and you don't get that kind of hiss from the MU80 soundtrack, the instruments are just processed differently. The most noticeable way this comes through is the deep bass end--MU80 has more digital information in the sub bass region. A few instruments are noticeably different but most are very. very similar and most tracks would be hard to tell the difference without headphones and/or a good ear.

I've normalized the tracks slightly in the current release of MU80, but it needs another try with a softer hammer to really restore the peaks in loudness, so I'm working through all the tracks with Audacity again and making some smarter compromises.

I'm also still working on the opening and this is one area where the 2 mods differ pretty noticeably--the transition from opening\_va to ob.ogg. The MU80 current release sacrifices the audio sync when the FF7 title pops up in the opening movie in order to get a very solid sync when Avalanche start exiting the train. I am trying to work out how to adjust the tempo in order to sync both sections of the opening perfectly.

P.S. One more very early example--the deep "bloop" sound effects and the reverb quality on makoro.ogg are much more pronounced and complex sounding from the MU80. Much harder to hear these effects with the S-YXG50 cut--they just don't come off nearly as ominous sounding.


---

## Post #5 by Kuraudo
*«Reply #4 on:2025-12-05 13:35:34 »*

That's clear! Thanks a lot for getting back to me so quickly and for such a detailed reply.


---

## Post #6 by Template
*«Reply #5 on:2025-12-09 02:46:42 »*

Bumped to v1.2. Should be relatively final, in a good way.

Will release on 7H catalog, but if you want to download it from my Gdrive the link is the same as on the original post: <https://drive.google.com/file/d/1W4LAlsLpTAEPIjgWefkkemwyFv-oa23t/view?usp=sharing>

This is a soundtrack mod for Final Fantasy 7 featuring the XG MIDI data rendered through a Yamaha MU80 sound module (closest hardware equivalent of the original S-YXG70 software synthesizer).

Important notes:
-Recommend setting both music and sfx volume to 100%.
-Recommend to install this mod in raw folder structure to your 7H library rather than packing it into an iro--7H catalog will install as a folder. Slowdowns on the worldmap when running this mod in iro format were resolved by unpacking.

Version History:
1.2 Overhaul of original files to restore peak levels and dynamics.
   -Updated opening sequence to adjust sync, tighten the transition to the first field.
1.101 Initial 7H catalog release.
   -Normalized loudness.
   -Added new opening movie sequence.
1.1 NidoLNorris' NexusMods release.
   -Increased bit rate.
1.0 The original 1.0 upload is lost to time.

Installation:
\*\*Using the 7th Heaven mod catalogue to download and install is the easiest option.\*\*
To install the mod from a folder manually, you can choose one of these methods...
1.) Use the 'Import Mod' option in the 7H UI.
2.) Drop the MU80 Soundtrack folder into your 7th Heaven mod library directory and set 7H to automatically import mods from your library in General Settings.
3.) Paste the ogg files from the MU80 Soundtrack\Music\Vgmstream folder into the data\music\_ogg directory in your Final Fantasy VII installation location. The lb2 track option needs to be copied as well from either the LB2\vocals OR the novocals directories. This option bypasses 7th Heaven and would be recommended for troubleshooting.

All credit for the soundtrack recordings belongs to user Raymond from the old Square Enix forums.

Additional authors: Template, NidoLNorris


---

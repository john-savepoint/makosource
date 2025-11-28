# **The World Map**

## *I. World Map Overview*

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

#### PC Format !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

By the way, also had a brief look at the World Map... although things are different between that and the field files, it naturally has many of the same data structures... dialogue's in 'mes', the event files are in 'wm0.ev', 'wm2.ev' and 'wm3.ev' (I assume... though I've not gotten any conclusive proof that this is the case through a \*brief\* glance through them), and the encounters are stored in 'enc\_w.bin' (but may or may not follow the same rules regarding encounter chances... unsure yet)

-----

Well, enough data to warrant its own post to follow.

Encounter data for the World Map starts at offset 0xB8, and each section is 32 bytes each. A section is defined as follows:

0x00: 01

0x01: Encounter Rate (1 byte)(?) (lower numbers mean higher encounter rates) 0x02-0x0D: Normal Battle+Chance of that battle (2 bytes each, 6 records)

0x0E-0x15: Special Formation Battles+Chance (2 bytes each, 4 records)

0x16-0x1F: Chocobo Battles (2 bytes each, 5 records)

Again, the chance byte for normal battles seems to always add up to 64.

Anyhow, as for how they're \*stored\*...

...each area in the game has four fields, and they're aligned something like this:

Area - Grass

Area - Dirt/Snow

Area - Forest/Desert

Area - Beach

And the areas are naturally in this order:

Midgar Area

Kalm Area

Junon Area

Corel Area

Gold Saucer Area

Gongaga Area

Cosmo Area

Nibel Area

Rocket Area

Wutai Area

Woodlands Area

Icicle Area (Not sure what Forest is for this, since the forests in this area are supposed to have no encounters)

Mideel Area

North Corel Area (Materia Cave north of Corel)(?)

Cactus Island

Goblin Island (Goblin Island lacks a full empty Beach encounter list)

## *II. Land*

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

## *III. Underwater*

Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

## *IV. Snow Field*

Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.

## *V. Data Format*


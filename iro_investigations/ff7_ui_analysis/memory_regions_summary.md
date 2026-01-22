# FF7 UI Memory Regions Summary

Total unique addresses analyzed: 1643
Total memory regions: 18

## Region 1

- **Address Range**: `0x0023B6B8` - `0x0023B6B8`
- **Size**: 0 bytes (0x0)
- **UI Elements**: 1 addresses
- **Categories**: Bar

### Sample Addresses:

- `0x0023B6B8`: Syncs Barrett's animation to opening music

---

## Region 2

- **Address Range**: `0x0041B4E8` - `0x0041C4C0`
- **Size**: 4056 bytes (0xFD8)
- **UI Elements**: 3 addresses
- **Categories**: Battle, Field, StatusMenu, Uncategorized

### Sample Addresses:

- `0x41B4E800`: screen pos - increases pheonix glitch but overall better experience
- `0x41B51A00`: FMV/FIELD C0, STOCK 4C, FULL SCREEN E0
- `0x41C4C000`: Certain statuses like Resist are intentionally not shown in the battle menu.  To place them back:

---

## Region 3

- **Address Range**: `0x005BB847` - `0x005BCFD7`
- **Size**: 6032 bytes (0x1790)
- **UI Elements**: 3 addresses
- **Categories**: Avatar, Battle, Opacity, Text, Uncategorized

### Sample Addresses:

- `0x5BB84700`: Battle text/graphics like "Recovery" position
- `0x5BCFD000`: mini avatar support
- `0x5BCFD700`: time BA normal  00 no fade in (shrinking black area)

---

## Region 4

- **Address Range**: `0x00630CEB` - `0x00632CEC`
- **Size**: 8193 bytes (0x2001)
- **UI Elements**: 13 addresses
- **Categories**: Box, Cursor, Field, PositionX, PositionY, Spacing, Text

### Sample Addresses:

- `0x630CEB00`: field boxes Y-Axis negative offset 91449D to change value
- `0x630EA900`: field boxes viewable lines offset (refresh dialog)
- `0x630EFC00`: field dialog text block scroll amount (refresh dialog)
- `0x6311FA00`: field boxes viewable lines offset (refresh dialog)
- `0x63124D00`: field dialog text block scroll amount (refresh dialog)
- `0x63138200`: field cursor X-Axis
- `0x63138A00`: cursor spacing Y-Axis
- `0x63138F00`: field cursor Y-Axis
- `0x63191A00`: field box padding top/bottom 914488 to change value
- `0x631B3400`: field boxes viewable lines offset (refresh dialog)
- ... and 3 more

---

## Region 5

- **Address Range**: `0x00649A4A` - `0x00649A4A`
- **Size**: 0 bytes (0x0)
- **UI Elements**: 1 addresses
- **Categories**: Box

### Sample Addresses:

- `0x649A4A00`: modified code to only work when no dialog box on screen.

---

## Region 6

- **Address Range**: `0x006C20AF` - `0x006D21A2`
- **Size**: 65779 bytes (0x100F3)
- **UI Elements**: 261 addresses
- **Categories**: Avatar, Bar, Battle, Box, Color, Cursor, Field, Height, Icon, ItemMenu, LimitMenu, MagicMenu, MainMenu, PositionX, PositionY, Spacing, StatusMenu, Text, Uncategorized, Width

### Sample Addresses:

- `0x6C20AF00`: Cursor Y-Axis
- `0x6C20B200`: Cursor X-Axis
- `0x6C20E500`: ghost cursor color box Y-Axis
- `0x6C20E800`: ghost cursor color box X-Axis
- `0x6C213E00`: ghost cursor sound box Y-Axis
- `0x6C214100`: ghost cursor sound box X-Axis
- `0x6C216F00`: sound box width
- `0x6C217F00`: sound box Y-Axis
- `0x6C218C00`: sound box X-Axis
- `0x6C222D00`: sound box top numbers Y-Axis
- ... and 251 more

---

## Region 7

- **Address Range**: `0x006D7527` - `0x006E4B8C`
- **Size**: 54885 bytes (0xD665)
- **UI Elements**: 388 addresses
- **Categories**: Avatar, Bar, Battle, Box, Color, Cursor, Height, Icon, ItemMenu, LimitMenu, MagicMenu, Opacity, PositionX, PositionY, Spacing, StatusMenu, Text, Uncategorized, Width

### Sample Addresses:

- `0x6D752700`: magic column count descriptions
- `0x6D758100`: magic column count cursor first column
- `0x6D7A6300`: change Y-Axis
- `0x6D7A8F00`: change X-Axis
- `0x6D7AE100`: defend Y-Axis
- `0x6D7B0F00`: defend X-Axis
- `0x6D7E4B00`: item box hidden area boxes and headers
- `0x6D7E5800`: magic box hidden area boxes and headers
- `0x6D7E6400`: summon box hidden area boxes and headers
- `0x6D7E7100`: eskill (and summon?) box hidden area boxes and headers
- ... and 378 more

---

## Region 8

- **Address Range**: `0x006E7117` - `0x006E7117`
- **Size**: 0 bytes (0x0)
- **UI Elements**: 1 addresses
- **Categories**: PositionY, Spacing

### Sample Addresses:

- `0x6E711700`: dialog spacing Y-Axis, both values

---

## Region 9

- **Address Range**: `0x006EB022` - `0x006EC284`
- **Size**: 4706 bytes (0x1262)
- **UI Elements**: 3 addresses
- **Categories**: Box, Field, Opacity, PositionY, Text

### Sample Addresses:

- `0x6EB02200`: Add transparency support for FIELD dialogs - trueodin
- `0x6EC0B000`: field message box scrolling viewing offset Y-Axis 9139FC to change value
- `0x6EC28400`: dialog text Y-Axis offset

---

## Region 10

- **Address Range**: `0x006F6377` - `0x006F6377`
- **Size**: 0 bytes (0x0)
- **UI Elements**: 1 addresses
- **Categories**: MainMenu, PositionX, Spacing

### Sample Addresses:

- `0x6F637700`: main menu (OR ALL UI?) - LV HP MP spacing X-Axis

---

## Region 11

- **Address Range**: `0x006F984C` - `0x006F9F69`
- **Size**: 1821 bytes (0x71D)
- **UI Elements**: 6 addresses
- **Categories**: Battle, MateriaMenu, PositionX, Spacing

### Sample Addresses:

- `0x6F984C00`: all menus (NOT BATTLE) - All but last digits spacing X-Axis
- `0x6F986000`: All but last digits spacing X-Axis
- `0x6F9A8700`: all menus (NOT BATTLE) - last digits spacing X-Axis
- `0x6F9A9B00`: last digits spacing X-Axis
- `0x6F9D2800`: materia effect - all but last digits spacing X-Axis
- `0x6F9F6900`: materia effect - last digits spacing X-Axis

---

## Region 12

- **Address Range**: `0x006FEEA4` - `0x00712157`
- **Size**: 78515 bytes (0x132B3)
- **UI Elements**: 517 addresses
- **Categories**: Avatar, Bar, Box, Color, Cursor, EquipMenu, Height, Icon, ItemMenu, LimitMenu, MagicMenu, MateriaMenu, PositionX, PositionY, SaveLoadMenu, Spacing, StatusMenu, Text, Uncategorized, Width

### Sample Addresses:

- `0x6FEEA400`: save file select cursor spacing Y-Axis
- `0x6FEEB900`: save file select cursor spacing X-Axis
- `0x6FEEBD00`: save file select cursor X-Axis
- `0x6FEED600`: save select text X-Axis
- `0x6FEF4200`: save file select box text Y-Axis
- `0x6FEF5100`: save file select box text X-Axis
- `0x6FF0C100`: save game ghost cursor Y-Axis
- `0x6FF0C400`: save game ghost cursor X-Axis
- `0x6FF0DF00`: save game cursor Y-Axis
- `0x6FF0E200`: save game cursor X-Axis
- ... and 507 more

---

## Region 13

- **Address Range**: `0x00714F40` - `0x007217DC`
- **Size**: 51356 bytes (0xC89C)
- **UI Elements**: 303 addresses
- **Categories**: Avatar, Bar, Box, Color, Cursor, EquipMenu, Height, Icon, ItemMenu, MateriaMenu, PositionX, PositionY, SaveLoadMenu, ShopMenu, Spacing, Text, Width

### Sample Addresses:

- `0x714F4000`: Use Item Cursor Row Count Y-Axis (refresh menu)
- `0x7151E700`: Use Ghost Cursor Spacing Y-Axis
- `0x7151EA00`: Use Ghost Cursor Y-Axis
- `0x7151ED00`: Use Ghost Cursor X-Axis
- `0x71524000`: Top Cursor Y-Axis
- `0x71524C00`: Top Cursor X-Axis
- `0x71526B00`: Top Cursor Ghost USE Y-Axis
- `0x71527700`: Top Cursor Ghost USE X-Axis
- `0x71528E00`: Use Cursor Spacing Y-Axis
- `0x71529100`: Use Cursor Y-Axis
- ... and 293 more

---

## Region 14

- **Address Range**: `0x00767DCF` - `0x0076968F`
- **Size**: 6336 bytes (0x18C0)
- **UI Elements**: 6 addresses
- **Categories**: Box, Cursor, Height, PositionX, PositionY, Spacing, Uncategorized, Width, WorldMap

### Sample Addresses:

- `0x767DCF00`: Map positioning X-Axis
- `0x767DD300`: Map positioning Y-Axis
- `0x768FEB00`: world map box X / Width / Height
- `0x76968200`: world map cursor X-Axis
- `0x76968A00`: world map cursor spacing Y-Axis
- `0x76968F00`: world map cursor Y-Axis

---

## Region 15

- **Address Range**: `0x007B7CF8` - `0x007B7CF8`
- **Size**: 0 bytes (0x0)
- **UI Elements**: 1 addresses
- **Categories**: Text

### Sample Addresses:

- `0x7B7CF800`: Set menu font scaling value to be 2.0 via value

---

## Region 16

- **Address Range**: `0x0091391E` - `0x00914356`
- **Size**: 2616 bytes (0xA38)
- **UI Elements**: 25 addresses
- **Categories**: Avatar, Icon, ItemMenu, MateriaMenu, PositionX, PositionY, ShopMenu, Spacing, Text

### Sample Addresses:

- `0x91391E00`: allied name X-Axis
- `0x91392D00`: selected name X-Axis
- `0x913A6F00`: weapon/item shop - prices Y-Axis
- `0x913A7600`: weapon/item shop - text Y-Axis
- `0x913A8300`: materia shop - text Y-Axis
- `0x913A8F00`: materia shop - price Y-Axis
- `0x913D1D00`: Date header X-Axis
- `0x913FAE00`: icon conditinal
- `0x91419600`: Ä+ITEM Á+ITEM Ç+ITEM É+ITEM
- `0x9141A600`: Ñ+ITEM Ö+ITEM Ü+ITEM á+ITEM
- ... and 15 more

---

## Region 17

- **Address Range**: `0x00919DA5` - `0x00922A4C`
- **Size**: 36007 bytes (0x8CA7)
- **UI Elements**: 109 addresses
- **Categories**: Battle, Box, Cursor, EquipMenu, Height, ItemMenu, LimitMenu, MagicMenu, MateriaMenu, PositionX, PositionY, SaveLoadMenu, StatusMenu, Text, Uncategorized, Width

### Sample Addresses:

- `0x919DA500`: Set menu system to load correct UI assets.
- `0x91AA0000`: Next Level... Limit Level
- `0x91AC4800`: left box cursor Y-Axis
- `0x91AC4A00`: left box selection cursor Y-Axis
- `0x91AC4C00`: left box exit selection cursor Y-Axis
- `0x91C34200`: main boxes Y-Axis
- `0x91C34600`: main UI visibility height (battle refresh)
- `0x91C35200`: left main box left side X-Axis
- `0x91C35400`: hide left box
- `0x91C35500`: remove left box
- ... and 99 more

---

## Region 18

- **Address Range**: `0x0099DE31` - `0x0099DE31`
- **Size**: 0 bytes (0x0)
- **UI Elements**: 1 addresses
- **Categories**: Avatar, Icon, Spacing, Text

### Sample Addresses:

- `0x99DE3100`: font spacing mini avatars  99DE33 was mini chocobo but now used by extended icons

---


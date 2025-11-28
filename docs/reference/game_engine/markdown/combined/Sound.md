# FF7 Sound System

**Category: Sound System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's PSX sound system, including instrument formats and AKAO frames.

---

# FF7/PSX/Sound/Overview

- [FF7/PSX/Sound/Overview](#ff7psxsoundoverview){#toc-ff7psxsoundoverview}
  - [Overview](#overview){#toc-overview}



## Overview

PSX FF7 sound system is tightly connected with PSX SPU implementation. There are 2 main types of sounds in FF7: streaming sound (background noise in video sequences) and tracker sound. Square Enix programmers didn\'t use any standard PSX formats such as SEQ, VAB & VAG, they wrote their own custom tracker. Streaming sound is standard PSX XA-ADPCM format, all sound streaming data is in Mode 2 sectors on FF7 CDROM game discs.

---

# FF7/PSX/Sound/INSTRx.DAT

- [FF7/PSX/Sound/INSTRx.DAT](#ff7psxsoundinstrx.dat){#toc-ff7psxsoundinstrx.dat}
  - [Record format](#record_format){#toc-record_format}



There are two files of such type: SOUND/INSTR.DAT - Main game sounds (93 instruments)

SOUND/INSTR2.DAT - Voices from ending theme \"One Winged Angel\" (4 instruments)

These files contain index data for all instruments from INSTRx.ALL.

## Record format {#record_format}

struct InstrumentIndex

{

```
  /* offsets */
  uint32_t attack_offset // offset to attack part of instrument
  uint32_t loop_offset;  // offset to loop part of instrument
  /* ADSR Envelope settings */
  uint8_t attack_rate;   // ADSR: attack rate (0x00-0x7f)
  uint8_t decay_rate;    // ADSR: decay rate (0x00-0x0f)
  uint8_t sustain_level; // ADSR: sustain level (0x00-0x0f)
  uint8_t sustain_rate;  // ADSR: sustain rate (0x00-0x7f)
  uint8_t release_rate;  // ADSR: release rate (0x00-0x1f)
  uint8_t attack_mode;   // ADSR: attack mode
                         //    0x05 - (exponential)
                         //   other - (linear)
  uint8_t sustain_mode;  // ADSR: sustain mode
                         //    0x01 - (linear, increase)
                         //    0x05 - (exponential, increase)
                         //    0x07 - (exponential, decrease)
                         //   other - (linear, decrease)
  uint8_t release_mode;  // ADSR: release mode
                         //    0x07 - (exponential decrease)
                         //   other - (linear decrease)
  uint32_t pitch[12];    // predefined pitch set for instrument
```

};

Each index file takes 4 CDROM sectors, so rest unused data filled with zeroes. Attack and loop offsets isn\'t real file offsets, it\'s offsets to instruments in SPU internal memory (all instrument data from INSTRx.ALL files are copied by DMA to SPU memory in one chunk), so to translate INSTR.ALL you need tu subtract 0x0ff0 (not sure about INSTR2.DAT file, haven\'t investigate that yet). INSTR.DAT file resides in PSX RAM at address 0x80075f30 and when it\'s needed to load any instrument or to reset pitch for this instrument this table is used.

---

# FF7/PSX/Sound/INSTRx.ALL

- [FF7/PSX/Sound/INSTRx.ALL](#ff7psxsoundinstrx.all){#toc-ff7psxsoundinstrx.all}
  - [File Structure](#file_structure){#toc-file_structure}



There is two files of this structure on FF7 game discs: SOUND/INSTR.ALL - Main game sounds (93 instruments) SOUND/INSTR2.ALL- Voices from ending theme \"One Winged Angel\" (4 instruments) These files contain all sample data for every instrument in game. Every instrument consists of 16-byte PSX ADPCM frames. Frame format is known and there is numerous decompressors for it whether on the net, or in Q-Gears source.

## File Structure {#file_structure}

At file beginning there is two 32-bit numbers. First number isn\'t known yet, but it is somehow related to SPU memory offset. Second number is normal offset of last ADPCM frame of file. Counting from 0x20 file offset there is sample data for all instruments. (using term \"Instrument\" I actually mean serie of ADPCM samples, although in some context I can use term \"Sample\", \"Sound\" or \"Voice\" to describe instrument). All data from INSTR.ALL are loaded by DMA to SPU RAM in one chunk, offset 0x0202. (can\'t say anything about INSTR2.ALL yet).

---

# FF7/PSX/Sound/AKAO frames {#ff7psxsoundakao_frames}

- [FF7/PSX/Sound/AKAO frames](#ff7psxsoundakao_frames){#toc-ff7psxsoundakao_frames}
  - [Introduction](#introduction){#toc-introduction}
  - [AKAO frame structure](#akao_frame_structure){#toc-akao_frame_structure}


## Introduction

AKAO frames are most complicated frames in FF7 sound system. (\"AKAO\" is frame magic, probably developed by Minoru Akao, Square Enix sound programmer :) )

Frame is similar to MIDI sequence - it\'s custom tracker format for playing sequence sound, well tuned specially for PSX.

This frames are in all FF7 game modules: Field, Battle, Worldmap and in minigames.

All files with exension \*.SND are AKAO.

**MINI/ASERI2.SND** - Battle Arena theme

**MINI/SENSUI.SND** - used in Submarine minigame

**ENEMY6/OVER2.SND** - game over sequence

**ENEMY6/FAN2.SND** - battle win \"fanfare\" sequence

**MOVIE/OVER2.SND** - same game over sequence, don\'t know, why to duplicate data

Other AKAO frames are hard-wired in other files.

## AKAO frame structure {#akao_frame_structure}

### Header (size: 16 bytes) {#header_size_16_bytes}

struct AkaoHeader

{

```
  static const uint8_t magic[4]; // "AKAO" C-string aka frame *MAGIC*
  uint16_t id;                   // frame ID, used for playing sequence
  uint16_t length;               // frame length - sizeof(header)
  uint8_t unknown[8];            // some numbers, can't find their usage
```

};

### Channel info (size: 4 bytes + 2 bytes \* `<channels count>`{=html}) {#channel_info_size_4_bytes_2_bytes}

First there is 32-bit number (offset 0x10), which represents bitmask of used channels in this frame, after this frame there is `<channels count>`{=html} offsets to channel opcode data counting from current offset.

### Channel Commands \[AKAO Opcodes\] {#channel_commands_akao_opcodes}

Most complicated part.

For every channel in AKAO frame there is set of commands to perform. This is similar to Field opcodes. Here I\'ll call this sound commands \"opcodes\". Every opcode has it\'s own number of arguments (from no-arguments, to 3 arguments).

## Example (home-created AKAO frame): {#example_home_created_akao_frame}

### Header

**41 4b 41 4f** - AKAO string

**34 12** - frame ID: 0x1234

**16 00** - frame length 0x16 in hex or 22 in decimal

**04 00 96 12 18 22 46 28** - unknown data

### Channel info {#channel_info}

**01 00 00 00** - this indicates, that used only one channel

**00 00** - offset to first channel opcodes: in our example 0x00 means that next to this offset is opcodes for first channel

### Channel commands {#channel_commands}

**e8 a8 66** - sets tempo, parameter 0x66a8

**ea 00 50** - sets reverb depth

**a8 55** - load sample 0x55 from INSTR.ALL to channel

**aa 40** - sets channel volume

**c2** - turns on reverb effect

**a1 0c** - sets volume pan

**c8** - sets loop point

**66** - 0x66 % 11 = 3 (3 means to take 3rd number from play length table), 0x66 / 11 = 9 (9 means to take pitch\[9\] from loaded instrument record index)

**ca** - returns to saved loop point with opcode c8

This example plays Chocobo \"Whoo-Hoo\" (instrument number 0x55) repeatedly.

## Sound Opcode list {#sound_opcode_list}

[0xA0 (Finish Channel)](FF7/PSX/Sound/Opcodes/0xa0 "0xA0 (Finish Channel)"){.wikilink}

[0xA1 (Load Instrument)](FF7/PSX/Sound/Opcodes/0xa1 "0xA1 (Load Instrument)"){.wikilink}

[0xA3 (Volume Modifier)](FF7/PSX/Sound/Opcodes/0xa8aa "0xA3 (Volume Modifier)"){.wikilink}

[0xA5 (Pitch Divider)](FF7/PSX/Sound/Opcodes/0xa5 "0xA5 (Pitch Divider)"){.wikilink}

[0xA8 (Channel Volume)](FF7/PSX/Sound/Opcodes/0xa8aa "0xA8 (Channel Volume)"){.wikilink}

[0xAA (Channel Pan)](FF7/PSX/Sound/Opcodes/0xa8aa "0xAA (Channel Pan)"){.wikilink}

[0xC8 (Loop Point)](FF7/PSX/Sound/Opcodes/0xc8 "0xC8 (Loop Point)"){.wikilink}

[0xCA (Return to Loop Point)](FF7/PSX/Sound/Opcodes/0xca "0xCA (Return to Loop Point)"){.wikilink}

[0xE8 (Tempo)](FF7/PSX/Sound/Opcodes/0xe8 "0xE8 (Tempo)"){.wikilink}

[0xEA (Reverb Depth)](FF7/PSX/Sound/Opcodes/0xea "0xEA (Reverb Depth)"){.wikilink}

[0xC2 (Turn On Reverb)](FF7/PSX/Sound/Opcodes/0xc2 "0xC2 (Turn On Reverb)"){.wikilink}

[0xFD (Unknown)](FF7/PSX/Sound/Opcodes/0xfd "0xFD (Unknown)"){.wikilink}

[0xFE (Unknown)](FF7/PSX/Sound/Opcodes/0xfe "0xFE (Unknown)"){.wikilink}

[0xB4 (Unknown)](FF7/PSX/Sound/Opcodes/0xb4 "0xB4 (Unknown)"){.wikilink}

[0xE0 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE0 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE1 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE1 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE2 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE2 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE3 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE3 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE4 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE4 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE5 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE5 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE6 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE6 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xE7 (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xE7 (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xFA (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xFA (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xFB (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xFB (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xFC (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xFC (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xFF (Unimplemented, code-referenced to 0xA0)](FF7/PSX/Sound/Opcodes/0xa0 "0xFF (Unimplemented, code-referenced to 0xA0)"){.wikilink}

[0xCD (Unimplemented)](FF7/PSX/Sound/Opcodes/0xcd "0xCD (Unimplemented)"){.wikilink}

[0xD1 (Unimplemented)](FF7/PSX/Sound/Opcodes/0xd1 "0xD1 (Unimplemented)"){.wikilink}

---


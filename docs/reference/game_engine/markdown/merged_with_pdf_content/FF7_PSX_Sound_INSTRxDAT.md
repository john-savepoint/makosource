<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_PSX_Sound_INSTRxDAT.md (46 lines)
Major section: None (Sound formats not in major sections)
Merge decision: NO EXTRACTION PERFORMED
Reason: INSTR.DAT format documentation is complete and self-contained
Status: COMPLETE - Original file copied as source of truth
-->

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

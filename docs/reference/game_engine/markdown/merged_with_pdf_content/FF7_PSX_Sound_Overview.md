<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_PSX_Sound_Overview.md (10 lines)
Major section: None (Sound system not in major sections)
Merge decision: NO EXTRACTION PERFORMED
Reason: Sound system overview is complete and self-contained
Status: COMPLETE - Original file copied as source of truth
-->

# FF7/PSX/Sound/Overview

- [FF7/PSX/Sound/Overview](#ff7psxsoundoverview){#toc-ff7psxsoundoverview}
  - [Overview](#overview){#toc-overview}



## Overview

PSX FF7 sound system is tightly connected with PSX SPU implementation. There are 2 main types of sounds in FF7: streaming sound (background noise in video sequences) and tracker sound. Square Enix programmers didn\'t use any standard PSX formats such as SEQ, VAB & VAG, they wrote their own custom tracker. Streaming sound is standard PSX XA-ADPCM format, all sound streaming data is in Mode 2 sectors on FF7 CDROM game discs.

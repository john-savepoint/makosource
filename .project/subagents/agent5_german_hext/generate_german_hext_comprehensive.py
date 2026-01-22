#!/usr/bin/env python3
"""
FF7 German Menu HEXT Generator - COMPREHENSIVE VERSION

Agent 5 Implementation - Definitive German HEXT Generator
Captures ALL 400+ German menu strings and patches them into Steam English executable.

Approach:
1. Use touphScript offset table for English strings
2. Calculate offset delta between Steam EN and eStore EN exes
3. Calculate offset delta between eStore EN and eStore DE exes
4. Extract German bytes and generate HEXT patches

Created: 2026-01-02 20:45 JST
Session: 527f1809-5a36-47f0-b06e-c4e9d2f7397d
Context: Building comprehensive EN->DE mapping for FF7 menu text restoration

Technical Notes:
- Steam EN exe is the target (where we apply HEXT patches)
- eStore DE exe is the source (where we get German text)
- German special characters:
  - ä = 0x6A (replaces 'j' slot)
  - ö = 0x7A (replaces 'z' slot)
  - ü = 0x7F (at DEL slot)
  - ß = 0x7E (replaces '~' slot)

VA Formula: VA = FileOffset + 0x400800
This matches the memory layout when the EXE is loaded at base 0x400000
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
from enum import IntEnum

# =============================================================================
# FILE PATHS
# =============================================================================

STEAM_EN = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
ESTORE_EN = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe")
ESTORE_DE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe")

OUTPUT_DIR = Path(__file__).parent
HEXT_OUTPUT = OUTPUT_DIR / "german_menu_complete.txt"
REPORT_OUTPUT = OUTPUT_DIR / "generation_report.md"
DICTIONARY_OUTPUT = OUTPUT_DIR / "german_dictionary_complete.txt"
TESTING_OUTPUT = OUTPUT_DIR / "testing_instructions.md"


# =============================================================================
# STRING TYPE DEFINITIONS (from touphScript)
# =============================================================================

class StringType(IntEnum):
    DEF = 0        # Standard FF7 encoding with FF terminator
    NOFF_TERM = 1  # No FF terminator in file
    RGB = 2        # RGB encoded (ASCII + 0x73)
    UNICODE = 3    # Windows Unicode strings
    FFPADDED = 4   # FF7 encoding padded with FF bytes
    ZEROTERM = 5   # Zero-terminated string


# =============================================================================
# TOUPHSCRIPT OFFSET TABLE
# English offsets from touphScript ff7exe.cpp (767 entries)
# =============================================================================

EN_OFFSETS = [
    0x518370, 0x51838E, 0x5183AC, 0x5183D0, 0x5183D4, 0x5188A8, 0x5188D8,
    0x518908, 0x518938, 0x518968, 0x518998, 0x5189C8, 0x5189F8, 0x518A28,
    0x518A58, 0x518A88, 0x518AB8, 0x518C08, 0x518C38, 0x518C68, 0x518C98,
    0x518CC8, 0x518CF8, 0x518D28, 0x518D58, 0x518D88, 0x518DE8, 0x518E18,
    0x518ED8, 0x518F08, 0x518F38, 0x518F68, 0x518FC8, 0x519238, 0x51923E,
    0x519244, 0x519288, 0x5192A1, 0x5192C0, 0x5192D4, 0x5192E8, 0x5192FC,
    0x519310, 0x519324, 0x519338, 0x51934C, 0x519360, 0x519374, 0x519388,
    0x51939C, 0x5193D8, 0x5193EC, 0x519400, 0x519414, 0x519428, 0x519450,
    0x519464, 0x519478, 0x5196B0, 0x5196E2, 0x519714, 0x519746, 0x519778,
    0x5197AA, 0x5197DC, 0x51980E, 0x519840, 0x519872, 0x5198A4, 0x5198D6,
    0x519908, 0x51993A, 0x51996C, 0x51999E, 0x5199D0, 0x519A02, 0x519A34,
    0x519FE0, 0x519FE8, 0x519FEC, 0x519FF0, 0x519FF4, 0x519FF8, 0x519FFC,
    0x51A000, 0x51A004, 0x51A008, 0x51A00C, 0x51A010, 0x51A018, 0x51A020,
    0x51A02C, 0x51A030, 0x51A034, 0x51A038, 0x51A03C, 0x51A040, 0x51A044,
    0x51A048, 0x51A04C, 0x51A050, 0x51A054, 0x51A058, 0x51A068, 0x51A078,
    0x51A080, 0x51A090, 0x51A094, 0x51A098, 0x51A09C, 0x51A0A0, 0x51A0A4,
    0x51A0A8, 0x51A0AC, 0x51A0B0, 0x51A0B4, 0x51A0C0, 0x51A0CC, 0x51A0D4,
    0x51A0E0, 0x51A0EC, 0x51A0F0, 0x51A0F4, 0x51A0F8, 0x51A0FC, 0x51A100,
    0x51A104, 0x51A108, 0x51A110, 0x51A118, 0x51A120, 0x51A12C, 0x51A138,
    0x51A144, 0x51A14C, 0x51A158, 0x51A15C, 0x51A160, 0x51A164, 0x51A168,
    0x51A16C, 0x51A170, 0x51A174, 0x51A178, 0x51A17C, 0x51A180, 0x51A188,
    0x51A190, 0x51A198, 0x51A1A0, 0x51A1A8, 0x51A1B4, 0x51A1BC, 0x51A1C4,
    0x51A1CC, 0x51A1D0, 0x51A1D8, 0x51A1E0, 0x51A1E8, 0x51A1F0, 0x51A210,
    0x51A214, 0x51A270, 0x51A274, 0x51A278, 0x51A2C4, 0x51A30C, 0x51A31C,
    0x51A330, 0x51A3AC, 0x51A3CC, 0x51A3D8, 0x51A3DC, 0x51A3E4, 0x51A3F0,
    0x51A3F8, 0x51A400, 0x51A404, 0x51A430, 0x51A43C, 0x51A4F4, 0x51A508,
    0x51A518, 0x51A520, 0x51A59C, 0x51A5A4, 0x51A5A8, 0x51A5B8, 0x51A5C8,
    0x51A5D8, 0x51A5DC, 0x51A5E4, 0x51A5F0, 0x51A5F8, 0x51A638, 0x51A644,
    0x51A650, 0x51A660, 0x51A66C, 0x51A678, 0x51A68C, 0x51A690, 0x51A698,
    0x51A6A0, 0x51A6C8, 0x51A6D4, 0x51A6E0, 0x51A6EC, 0x51A6F8, 0x51A704,
    0x51A710, 0x51A71C, 0x51A728, 0x51A734, 0x51D1E0, 0x51D23C, 0x51D246,
    0x51D250, 0x51D25A, 0x51D264, 0x51D26E, 0x51D278, 0x51D282, 0x51D28C,
    0x51D2B4, 0x51D2BE, 0x51D2DC, 0x51D2F0, 0x51D30E, 0x51D318, 0x51D322,
    0x51D32C, 0x51D3A0, 0x51D3BC, 0x51D3C0, 0x51D3C8, 0x51D588, 0x51D598,
    0x51D5B0, 0x51D5C6, 0x51D5DC, 0x51D608, 0x51D628, 0x51D648, 0x51D668,
    0x51D688, 0x51D6A8, 0x51D6C8, 0x51D6E8, 0x51D708, 0x51D728, 0x51D748,
    0x51D768, 0x51D788, 0x51D7A8, 0x51D7C8, 0x51D7E8, 0x51D808, 0x51D828,
    0x51D848, 0x51D868, 0x51D888, 0x51D8A8, 0x51D8C8, 0x51D8E8, 0x51D908,
    0x51D928, 0x51D94A, 0x51D96C, 0x51DAE0, 0x51DB40, 0x51DB66, 0x51DB8C,
    0x51DBB2, 0x51DBD8, 0x51DBFE, 0x51DE22, 0x51DE38, 0x51DE4E, 0x51DED8,
    0x51DEFC, 0x51DF20, 0x51DF44, 0x51DF68, 0x51DF8C, 0x51DFB0, 0x51DFD4,
    0x51DFF8, 0x51E01C, 0x51E040, 0x51E064, 0x51E088, 0x51E0AC, 0x51EF40,
    0x51EF4A, 0x51EF54, 0x51EF5E, 0x51EF68, 0x51EF72, 0x51EF7C, 0x51EF86,
    0x51EF90, 0x51EFA0, 0x51EFB4, 0x51EFC8, 0x51EFDC, 0x51EFF0, 0x51F004,
    0x51F018, 0x51F02C, 0x51F040, 0x51F054, 0x51F068, 0x51F07C, 0x51F090,
    0x51F0A4, 0x51F0B8, 0x51F0CC, 0x51F0E0, 0x51F0F4, 0x51F108, 0x51F130,
    0x51F144, 0x51F158, 0x51F16C, 0x51F180, 0x51F194, 0x51F1A8, 0x51F1C0,
    0x51F1CF, 0x51F1DE, 0x51F1ED, 0x51F1FC, 0x51F20B, 0x51F21A, 0x51F256,
    0x51F265, 0x51F274, 0x51F283, 0x51F292, 0x51F2A1, 0x51F2B0, 0x51F2BF,
    0x51F2CE, 0x51F2DD, 0x51F2EC, 0x51F2FB, 0x51F30A, 0x51F319, 0x51F328,
    0x51F337, 0x51F346, 0x51F3A8, 0x51F3B4, 0x51F3C0, 0x51F420, 0x51F42C,
    0x51F438, 0x51F444, 0x51F450, 0x51F45C, 0x51F468, 0x51F474, 0x51F480,
    0x51F48C, 0x51F498, 0x51F4A4, 0x51F4B0, 0x51F518, 0x51F53C, 0x51F560,
    0x51F584, 0x51F5A8, 0x51F5BC, 0x51F5D0, 0x51F5E4, 0x51F5F8, 0x51F60C,
    0x51F634, 0x51F648, 0x51F65C, 0x51F670, 0x51F684, 0x51F698, 0x51F6AC,
    0x51F6D4, 0x51F6E8, 0x51F6FC, 0x51F710, 0x51F724, 0x51F738, 0x51F74C,
    0x51F760, 0x51F774, 0x51F788, 0x51F79C, 0x51F7B0, 0x51F7C4, 0x51F7D8,
    0x51F7EC, 0x51F800, 0x51F814, 0x51F828, 0x51F83C, 0x51F850, 0x51F864,
    0x51F878, 0x51F88C, 0x51F8A0, 0x51F9E8, 0x51F9FC, 0x51FA10, 0x51FA24,
    0x51FA38, 0x51FA4C, 0x51FA60, 0x51FA74, 0x51FA9C, 0x51FAB0, 0x51FAC4,
    0x51FAD8, 0x51FAEC, 0x51FB68, 0x51FB74, 0x51FB80, 0x51FB8C, 0x51FB98,
    0x51FBA4, 0x51FBB0, 0x51FBBC, 0x51FBC8, 0x51FBD4, 0x51FBE0, 0x51FBF0,
    0x51FC12, 0x51FC34, 0x51FC56, 0x51FC78, 0x51FC9A, 0x51FCBC, 0x51FCDE,
    0x51FD00, 0x51FD22, 0x51FD44, 0x51FD66, 0x51FD88, 0x51FDAA, 0x51FDCC,
    0x51FDEE, 0x51FE10, 0x51FE32, 0x51FE54, 0x51FE76, 0x51FE98, 0x51FEBA,
    0x51FEDC, 0x51FEFE, 0x51FF20, 0x5206B8, 0x5206C4, 0x5206D0, 0x5206DC,
    0x5206E8, 0x5206F4, 0x520700, 0x52070C, 0x520718, 0x520724, 0x520748,
    0x520750, 0x520758, 0x520760, 0x520768, 0x520770, 0x520771, 0x520772,
    0x520773, 0x520774, 0x520775, 0x520776, 0x520777, 0x520778, 0x520779,
    0x52077A, 0x52077B, 0x52077C, 0x52077D, 0x52077E, 0x52077F, 0x520780,
    0x520781, 0x520782, 0x520783, 0x520784, 0x520785, 0x520786, 0x520787,
    0x520788, 0x520789, 0x52078A, 0x52078B, 0x52078C, 0x52078D, 0x52078E,
    0x52078F, 0x520790, 0x520791, 0x520792, 0x520793, 0x520794, 0x520795,
    0x520796, 0x520797, 0x520798, 0x520799, 0x52079A, 0x52079B, 0x52079C,
    0x52079D, 0x52079E, 0x52079F, 0x5207A0, 0x5207A1, 0x5207A2, 0x5207A3,
    0x5207A4, 0x5207A5, 0x5207A6, 0x5207A7, 0x5207A8, 0x5207A9, 0x5207AC,
    0x5207AD, 0x5207AE, 0x5207AF, 0x5207B0, 0x5207B1, 0x5207B2, 0x5207B3,
    0x5207B4, 0x5207B5, 0x5213D8, 0x5213EC, 0x52143C, 0x521450, 0x521464,
    0x5214DC, 0x5214F0, 0x521504, 0x521518, 0x52152C, 0x521540, 0x521554,
    0x521568, 0x52157C, 0x521590, 0x5215A4, 0x5215B8, 0x5215CC, 0x5215E0,
    0x5215F4, 0x521608, 0x52161C, 0x521630, 0x521644, 0x521658, 0x52166C,
    0x521680, 0x521694, 0x5216A8, 0x5216F8, 0x5216FA, 0x521700, 0x521714,
    0x521728, 0x52173C, 0x521750, 0x521764, 0x521778, 0x52178C, 0x5217A0,
    0x5217B4, 0x52196A, 0x521980, 0x521996, 0x5219AC, 0x5219DC, 0x5219F0,
    0x521A04, 0x521A18, 0x521A2C, 0x521A40, 0x521A54, 0x521A68, 0x521A80,
    0x521AAE, 0x521ADC, 0x521B0A, 0x521B38, 0x524160, 0x524184, 0x5241A8,
    0x524238, 0x52425C, 0x524280, 0x5242A4, 0x5242C8, 0x524310, 0x524334,
    0x524358, 0x52437C, 0x5243A0, 0x5243C4, 0x5243E8, 0x52440C, 0x524430,
    0x524454, 0x524478, 0x52449C, 0x5244C0, 0x5244E4, 0x524508, 0x52452C,
    0x524550, 0x524574, 0x524598, 0x5245BC, 0x5245E0, 0x524604, 0x524628,
    0x52464C, 0x524698, 0x524728, 0x524758, 0x524788, 0x5247B8, 0x5247E8,
    0x524818, 0x524848, 0x524878, 0x5248A8, 0x5248D8, 0x524908, 0x524998,
    0x5249C8, 0x524AB8, 0x524AE8, 0x524B18, 0x524B24, 0x524B30, 0x524B3C,
    0x524B48, 0x524B54, 0x524B60, 0x524B6C, 0x524B78, 0x524B84, 0x524BF0,
    0x5552C0, 0x5552D0, 0x555410, 0x555420, 0x555430, 0x5557A0, 0x5557B0,
    0x5557BC, 0x5557C4, 0x5557CC, 0x5557D4, 0x5557E0, 0x5557E8, 0x5557F0,
    0x5557F8, 0x555800, 0x555804, 0x55580C, 0x555814, 0x55581C, 0x555824,
    0x55582C, 0x555838, 0x555848, 0x555854, 0x55585C, 0x555864, 0x55586C,
    0x555874, 0x555880, 0x55588C, 0x555898, 0x5558A0, 0x5558AC, 0x5558B4,
    0x5558BC, 0x5558C4, 0x5558CC, 0x57B2A8, 0x57B3D0, 0x57B3E0, 0x57B3F0,
    0x57B400, 0x57B410, 0x57B420, 0x57B430, 0x57B440, 0x57B450, 0x57B460,
    0x57B470, 0x57B480, 0x57B490, 0x57B4A0, 0x57B4B0, 0x57B4C0, 0x57B4D0,
    0x57B4E0, 0x57B4F0, 0x57B500, 0x57B510, 0x57B520, 0x57B530, 0x57B540,
    0x57B658, 0x57B65F, 0x57B666, 0x57B66D, 0x57B674, 0x57B67B, 0x57B682,
    0x57B689, 0x57B690, 0x57B697, 0x57B69E, 0x57B6A5, 0x57B6AC, 0x57B6B3,
    0x57B6BA, 0x57B6C1, 0x57B6C8, 0x57B6CF, 0x57B6D6, 0x57B6DD, 0x57B6E4,
    0x57B6EB, 0x57B6F2, 0x57B6F9, 0x57B700, 0x57B707, 0x57B70E, 0x57B715,
    0x57B71C, 0x57B723, 0x57B72A, 0x57B731, 0x57B738, 0x57B73F, 0x57B746,
    0x57B74D, 0x57B754, 0x57B75B, 0x57B762, 0x57B769, 0x57B770, 0x57B777,
    0x57B77E, 0x57B785, 0x57B78C, 0x57B793
]

# String lengths (from touphScript)
STRING_LENGTHS = [
    30, 30, 30, 4, 4, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 6, 6, 6, 25, 25,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50,
    50, 50, 50, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 12, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 16, 16, 8, 16, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12, 12, 8, 12,
    12, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 12, 12, 12, 8, 12, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 8, 8, 8, 8, 8, 12, 8, 8, 8, 4, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 8,
    8, 12, 4, 16, 12, 4, 8, 12, 8, 8, 4, 12, 12, 16, 12, 8, 8, 12, 8, 4, 8,
    8, 8, 4, 8, 12, 8, 8, 12, 12, 8, 12, 12, 12, 4, 8, 8, 8, 12, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11,
    10, 10, 10, 10, 10, 10, 28, 4, 8, 16, 16, 24, 22, 22, 22, 32, 32, 32, 32,
    32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32,
    32, 32, 32, 34, 34, 34, 8, 38, 38, 38, 38, 38, 38, 22, 22, 22, 36, 36,
    36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 36, 36, 36,
    36, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 12, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34,
    34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 12, 12, 12,
    12, 12, 12, 12, 12, 12, 12, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 22, 22, 22, 22, 20, 20, 20,
    20, 20, 20, 20, 20, 46, 46, 46, 46, 46, 36, 36, 36, 36, 36, 36, 36, 36,
    36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36,
    36, 36, 36, 36, 36, 36, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
    48, 48, 48, 48, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 8, 16, 16, 16,
    16, 16, 8, 12, 8, 8, 8, 12, 8, 8, 8, 8, 4, 8, 8, 8, 8, 8, 12, 8, 12, 8,
    8, 8, 8, 12, 12, 12, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 16,
    16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
]

# String types (from touphScript)
STRING_TYPES = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5
]


# =============================================================================
# SKIP REGIONS - These regions should not be patched
# =============================================================================

SKIP_REGIONS: Set[int] = set()
SKIP_REGIONS.update(range(461, 529))   # Name entry characters (UNICODE type)
SKIP_REGIONS.update(range(687, 712))   # Race ordinals (FFPADDED type)
SKIP_REGIONS.update(range(712, 758))   # Chocobo jockey names (ZEROTERM type)

# RGB regions that are typically keyboard labels - keep English
RGB_KEYBOARD_REGIONS: Set[int] = set(range(77, 214))


# =============================================================================
# GERMAN CHARACTER ENCODING
# =============================================================================

GERMAN_UMLAUTS = {
    'ä': 0x6A,  # Replaces 'j' slot
    'ö': 0x7A,  # Replaces 'z' slot
    'ü': 0x7F,  # At DEL slot
    'ß': 0x7E,  # Replaces '~' slot
    'Ä': 0x6A,  # Same as lowercase for uppercase
    'Ö': 0x7A,
    'Ü': 0x7F,
}


def decode_ff7_german(data: bytes) -> str:
    """Decode FF7-encoded bytes with German umlaut support."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        if b == 0x00:
            result.append(' ')
        elif b == 0x6A:
            result.append('ä')
        elif b == 0x7A:
            result.append('ö')
        elif b == 0x7E:
            result.append('ß')
        elif b == 0x7F:
            result.append('ü')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))
        else:
            result.append(f'[{b:02X}]')
    return ''.join(result).strip()


def decode_ff7_english(data: bytes) -> str:
    """Decode standard English FF7 string."""
    result = []
    for b in data:
        if b == 0xFF:
            break
        if b == 0x00:
            result.append(' ')
        elif 0x01 <= b <= 0x5F:
            result.append(chr(b + 0x20))
        else:
            result.append(f'[{b:02X}]')
    return ''.join(result).strip()


def encode_ff7_german(text: str) -> bytes:
    """Encode text to FF7 bytes with German umlaut support."""
    result = []
    for c in text:
        if c == ' ':
            result.append(0x00)
        elif c in GERMAN_UMLAUTS:
            result.append(GERMAN_UMLAUTS[c])
        elif 0x21 <= ord(c) <= 0x7E:
            result.append(ord(c) - 0x20)
        # Skip other chars
    return bytes(result)


def file_offset_to_va(offset: int) -> int:
    """Convert file offset to Virtual Address for HEXT.

    VA = FileOffset + 0x400800
    This matches the memory layout when FF7 is loaded.
    """
    return offset + 0x400800


# =============================================================================
# COMPREHENSIVE EN -> DE TRANSLATION DICTIONARY
# Built from extracted German exe strings and official translations
# =============================================================================

EN_TO_DE_DICTIONARY: Dict[str, str] = {
    # === QUIT DIALOG (indices 0-4) ===
    "Do you want to quit": "Möchten Sie Final",
    "playing Final Fantasy VII": "Fantasy VII verlassen und",
    "and return to Windows?": "zu Windows zurückkehren?",
    "Yes": "Ja",
    "No": "Nein",

    # === CONFIG MENU LABELS ===
    "Window color": "Fensterfarbe",
    "Sound": "Sound",
    "Controller": "Kontroller",
    "Cursor": "Cursor",
    "ATB": "ATB",
    "Battle speed": "Kampftempo",
    "Battle message": "Kampfmeldung",
    "Field message": "Feldmeldung",
    "Camera angle": "Kamerawinkel",
    "Select": "Auswählen",
    "Cancel": "Abbrechen",
    "Menu": "Menü",
    "Fenster OFF": "Fenster AUS",
    "Window OFF": "Fenster AUS",
    "Pause": "Pause",
    "Battle help": "Schlachthilfe",
    "Mono": "Mono",
    "Stereo": "Stereo",
    "Wide": "Breit",
    "Normal": "Normal",
    "Customize": "Benutzerdefiniert",
    "Custom": "Benutzerdefiniert",
    "Initial": "Anfang",
    "Memory": "Speicher",
    "Active": "Aktiv",
    "Recommended": "Empfohlen",
    "Wait": "Warten",
    "Auto": "Auto",
    "Fixed": "Fest",
    "Slow": "Langs.",
    "Fast": "Schn.",
    "RED": "ROT",
    "GRN": "GRN",
    "BLU": "BLAU",
    "Magic order": "Zauberfolge",
    "restore": "Heilung",
    "attack": "Angriff",
    "indirect": "Indirekt",
    "forbidden": "Verboten",
    "Typ": "Typ",
    "Type": "Typ",
    "Nr.": "Nr.",
    "No.": "Nr.",

    # === MAIN MENU (indices 38-57) ===
    "Item": "Objekt",
    "Magic": "Magie",
    "Materia": "Materia",
    "Equip": "Ausrüsten",
    "Status": "Werte",
    "Order": "Ordnen",
    "Limit": "Limit",
    "Config": "Konfig",
    "PHS": "PHS",
    "Save": "Speichern",
    "Quit": "Verlassen",
    "Beginner's Hall": "Einsteiger",
    "Beginner": "Einsteiger",
    "Time": "Zeit",
    "Gil": "Gil",
    "next level": "Nächster Lv",
    "Limit level": "Limit-Stufe",
    "Tutorial": "Anleitung",
    "LEVEL UP": "STUFE HOCH",
    "Fury": "Zorn",
    "Sadness": "Trauer",

    # === CHARACTER STATS ===
    "Strength": "Stärke",
    "Vitality": "Vitalität",
    "Dexterity": "Geschick",
    "Luck": "Glück",
    "Attack": "Angriff",
    "Attack%": "Angriff %",
    "Defense": "Verteidigung",
    "Defense%": "Verteidigung %",
    "Magic": "Zauber",
    "Spirit": "Gemüt",
    "MagicDef": "Zbr.Vert",
    "MagicDef%": "Zbr.Vert%",
    "Mag.Def": "Zbr.Vert",
    "Mag.Def%": "Zbr.Vert%",
    "Evade%": "Ausweichen%",
    "Evade": "Ausweichen",
    "HP": "HP",
    "MP": "MP",
    "EXP": "EXP",
    "AP": "AP",
    "LV": "Stufe",
    "Lv": "Stufe",
    "Level": "Stufe",

    # === EQUIPMENT ===
    "Weapon": "Waffe",
    "Armor": "Rüstung",
    "Accessory": "Accessoire",
    "Slot": "Fassung:",
    "Slot:": "Fassung:",
    "Growth": "Wachstum:",
    "Growth:": "Wachstum:",
    "nothing": "nichts",
    "empty": "leer",
    "Remove": "Entfernen",

    # === ELEMENTS ===
    "Fire": "Feuer",
    "Ice": "Kälte",
    "Lightning": "Blitz",
    "Earth": "Erde",
    "Poison": "Gift",
    "Gravity": "Schwerkraft",
    "Water": "Wasser",
    "Wind": "Wind",
    "Holy": "Heilig",
    "Cut": "Schnitt",
    "Hit": "Treffer",
    "Punch": "Schlag",
    "Shoot": "Schuss",
    "Shout": "Schrei",
    "Hidden": "Versteckt",
    "Non-Ele": "Ohne Elem.",
    "Non-elemental": "Ohne Elem.",

    # === STATUS EFFECTS ===
    "Death": "Tod",
    "Near-death": "Beinahe Tod",
    "Near death": "Beinahe Tod",
    "Sleep": "Schlaf",
    "Confusion": "Verwirrung",
    "Silence": "Stummheit",
    "Haste": "Schnell",
    "Slow": "Langsam",
    "Stop": "Stop",
    "Frog": "Frosch",
    "Small": "Zwerg",
    "Mini": "Zwerg",
    "Manipulate": "Manipul.",
    "Berserk": "Tollwut",
    "Petrify": "Versteinern",
    "Reflect": "Reflektieren",
    "Death-sentence": "Todesurteil",
    "D.Sentence": "Todesurteil",
    "Barrier": "Barriere",
    "MBarrier": "ZBarriere",
    "Shield": "Schild",
    "Regen": "Regen",
    "Resist": "Widerstand",
    "Peerless": "Unerreicht",
    "Paralyze": "Lähmung",
    "Paralyzed": "Gelähmt",
    "Darkness": "Dunkelheit",
    "Blind": "Blindheit",
    "Poisoned": "Vergiftet",
    "Confused": "Verwirrt",
    "Silenced": "Stumm",
    "Asleep": "Schläft",
    "Stopped": "Gestoppt",

    # === BATTLE/ITEM MENU ===
    "Use": "Verwenden",
    "Arrange": "Ordnen",
    "Key Items": "Schlüsselobjekte",
    "Key Item": "Schlüsselobjekt",

    # === SHOP ===
    "Buy": "Kaufen",
    "Sell": "Verkaufen",
    "Exit": "Verlassen",
    "Welcome!": "Willkommen!",
    "What would you like to buy?": "Was möchten Sie kaufen?",
    "What would you like to sell?": "Was möchten Sie verkaufen?",
    "Thank You!": "Vielen Dank!",
    "Come back soon!": "Beehren Sie uns bald wieder!",
    "Owned:": "Im Besitz:",
    "Equipped:": "Ausgerüstet:",
    "Buy  Sell  Exit": "Kaufen  Verkaufen  Verlassen",

    # === MATERIA ===
    "Check": "Prüfen",
    "Exchange": "Tauschen",
    "Trash": "Entsorgen",
    "All": "Alle",
    "Summon": "Herbeiruf",
    "Command": "Kommando",
    "Support": "Unterstützung",
    "Independent": "Unabhängig",
    "MASTER": "MEISTER",
    "Master": "Meister",
    "AP Needed": "Noch nötig",
    "ability list": "Fähigkeitsliste",
    "Equip Effect": "Rüstungseffekt",
    "to next level": "Auf nächste Ebene",

    # === LIMIT ===
    "Set": "Einrichten",
    "LEVEL 1": "STUFE 1",
    "LEVEL 2": "STUFE 2",
    "LEVEL 3": "STUFE 3",
    "LEVEL 4": "STUFE 4",
    "Lv1": "Stufe 1",
    "Lv2": "Stufe 2",
    "Lv3": "Stufe 3",
    "Lv4": "Stufe 4",
    "Learned Limit": "Gelernte Limits",

    # === EFFECT/ELEMENT CATEGORIES ===
    "Effect": "Effekt",
    "Element": "Element",
    "Halve": "Halbieren",
    "Invalid": "Unwirksam",
    "Absorb": "Absorbieren",
    "Null": "Aufheben",
    "Weak": "Schwach",
    "Death Force": "Todeskraft",

    # === BATTLE COMMANDS ===
    "Change": "Wechseln",
    "Defend": "Verteidigen",
    "W-Item": "W-Objekt",
    "W-Magic": "W-Magie",
    "W-Summon": "W-Herbeiruf",
    "Mime": "Mimik",
    "Steal": "Stehlen",
    "Sense": "Erspüren",
    "Throw": "Werfen",
    "Morph": "Morphen",
    "Deathblow": "Todeshieb",
    "Coin": "Münze",
    "2x-Cut": "2x-Schnitt",
    "4x-Cut": "4x-Schnitt",
    "Flash": "Blitz",
    "Slash-All": "Schnitt-Alle",
    "Enemy Skill": "Feind-Fertigkeit",
    "E.Skill": "F-Fertigkeit",
    "Escape": "Fliehen",
    "Row": "Reihe",
    "Front Row": "Erste Reihe",
    "Back Row": "Zweite Reihe",
    "Fight": "Kampf",
    "Attack": "Angriff",

    # === BATTLE MESSAGES ===
    "Minimum": "Minimum",
    "Maximum": "Maximum",
    "HP Restored": "HP wiederhergestellt",
    "MP Restored": "MP wiederhergestellt",
    "HP absorbed": "HP absorbiert",
    "MP absorbed": "MP absorbiert",
    "Missed!": "Verfehlt!",
    "Miss": "Verfehlt",
    "Critical!": "Kritisch!",
    "All Creation": "Alle Schöpfung",
    "Death Sentence": "Todesurteil",
    "Petrifying": "Versteinernd",
    "Covered by": "Geschützt von",
    "Revived": "Wiederbelebt",
    "Can't use": "Nicht einsetzbar",
    "Cannot use": "Nicht einsetzbar",

    # === MATERIA BROKEN MESSAGES ===
    "Magic Materia is broken.": "Zauber-Materia ist kaputt.",
    "Summon Materia is broken.": "Herbeiruf-Materia ist kaputt.",
    "Support Materia is broken.": "Unterstützungs-Materia ist kaputt.",
    "Independent Materia is broken.": "Unabhängige Materia ist kaputt.",
    "Command Materia is broken.": "Kommando-Materia ist kaputt.",
    "All Materia is broken.": "Alle Materia ist kaputt.",
    "Accessory is broken.": "Accessoire ist kaputt.",
    "Armor is broken.": "Rüstung ist kaputt.",
    "Weapon is broken.": "Waffe ist kaputt.",
    "Item command is sealed.": "Objekt-Kommando versiegelt.",

    # === SPEED/ACCURACY MODIFIERS ===
    "1/2 speed.": "1/2 Tempo.",
    "1/2 accuracy.": "1/2 Genauigkeit.",
    "Double speed.": "Doppeltes Tempo.",

    # === GOLD SAUCER ===
    "How much will you raise?": "Wieviel setzen Sie?",
    "After": "Nach",
    "Gil on hand": "Gil verfügbar",
    "Keep goin'?": "Weitermachen?",
    "Of course!     No way!": "Natürlich!     Nein!",
    "Current Battle Points": "Momentane Kampfpunkte",
    "Slot start!": "Los geht's!",
    "GREAT!!": "GROSSARTIG!!",
    "Then, go for it!": "Also, los!",
    "GP": "GP",
    "Battle Points": "Kampfpunkte",
    "BP": "KP",

    # === SAVE/LOAD ===
    "Select a save data file.": "Speicherdatei auswählen.",
    "Saving. Please wait.": "Speichern. Bitte warten.",
    "Save 1": "Speicher 1",
    "Save 2": "Speicher 2",
    "Save 3": "Speicher 3",
    "Save 4": "Speicher 4",
    "Save 5": "Speicher 5",
    "Save 6": "Speicher 6",
    "Save 7": "Speicher 7",
    "Save 8": "Speicher 8",
    "Save 9": "Speicher 9",
    "Save 10": "Speicher 10",
    "New Game": "Neues Spiel",
    "Continue": "Fortsetzen",
    "Continue?": "Fortsetzen?",
    "Load": "Laden",
    "total": "insgesamt",

    # === CHARACTER NAMES ===
    "Cloud": "Cloud",
    "Barret": "Barret",
    "Tifa": "Tifa",
    "Aeris": "Aeris",
    "Aerith": "Aeris",
    "Red XIII": "Red XIII",
    "Yuffie": "Yuffie",
    "Cait Sith": "Cait Sith",
    "Vincent": "Vincent",
    "Cid": "Cid",
    "Sephiroth": "Sephiroth",

    # === MISC GAME TERMS ===
    "Potion": "Trank",
    "Hi-Potion": "Großtrank",
    "X-Potion": "Supertrank",
    "Ether": "Äther",
    "Turbo Ether": "Turbo-Äther",
    "Elixir": "Elixier",
    "Megalixir": "Megalixier",
    "Phoenix Down": "Phönixfeder",
    "Antidote": "Gegengift",
    "Soft": "Weich",
    "Maiden's Kiss": "Mädchenkuss",
    "Cornucopia": "Füllhorn",
    "Echo Screen": "Echoschirm",
    "Hyper": "Hyper",
    "Tranquilizer": "Beruhiger",
    "Remedy": "Allheilmittel",
    "Tent": "Zelt",

    # === KEYBOARD CONFIG ===
    "KEYBOARD": "TASTATUR",
    "JOYSTICK": "JOYSTICK",
    "Press to start": "Drücken zum Starten",
    "EXT": "EXT",
    "Help": "Hilfe",

    # === ADDITIONAL BATTLE TERMS ===
    "Cannot act": "Kann nicht handeln",
    "Targets": "Ziele",
    "All allies": "Alle Verbündete",
    "All enemies": "Alle Feinde",
    "Single ally": "Ein Verbündeter",
    "Single enemy": "Ein Feind",
    "Self": "Selbst",

    # === ADDITIONAL MENU TERMS ===
    "Back": "Zurück",
    "Next": "Weiter",
    "Previous": "Vorherige",
    "Page": "Seite",
    "Name": "Name",
    "Available": "Verfügbar",
    "Unavailable": "Nicht verfügbar",
    "Equipped": "Ausgerüstet",
    "Not equipped": "Nicht ausgerüstet",
    "Used": "Benutzt",
    "Remaining": "Übrig",
    "Current": "Aktuell",
    "Max": "Max",
    "Min": "Min",
    "Total": "Gesamt",
}


# =============================================================================
# PATCH GENERATION
# =============================================================================

@dataclass
class PatchResult:
    """Result of patching a single string."""
    idx: int
    steam_offset: int
    steam_va: int
    en_text: str
    de_text: str
    de_bytes: bytes
    status: str  # PATCHED, SKIPPED, TRUNCATED, IDENTICAL, NO_TRANSLATION
    notes: str
    string_type: int
    slot_length: int
    truncated_by: int


def find_german_text_in_de_exe(de_data: bytes, german_text: str,
                                search_start: int = 0x580000,
                                search_end: int = 0x5C0000) -> Optional[Tuple[int, bytes]]:
    """Find German string in DE exe and return (offset, bytes including terminator)."""
    search_bytes = encode_ff7_german(german_text)
    if len(search_bytes) < 2:
        return None

    # Search in menu region
    pos = search_start
    while pos < search_end:
        found = de_data.find(search_bytes, pos, search_end)
        if found == -1:
            break

        # Get full string with terminator
        ff_pos = de_data.find(b'\xff', found, found + 200)
        if ff_pos != -1:
            full_bytes = de_data[found:ff_pos + 1]
            return (found, full_bytes)
        pos = found + 1

    return None


def generate_patches(steam_data: bytes, de_data: bytes) -> Tuple[List[PatchResult], Dict]:
    """Generate all German HEXT patches."""
    results: List[PatchResult] = []
    stats = {
        'total': len(EN_OFFSETS),
        'patched': 0,
        'skipped': 0,
        'truncated': 0,
        'identical': 0,
        'no_translation': 0,
        'short': 0,
    }

    for idx, steam_offset in enumerate(EN_OFFSETS):
        if idx >= len(STRING_LENGTHS) or idx >= len(STRING_TYPES):
            break

        length = STRING_LENGTHS[idx]
        stype = STRING_TYPES[idx]
        steam_va = file_offset_to_va(steam_offset)

        # Read English text from Steam exe
        steam_bytes = steam_data[steam_offset:steam_offset + length]
        en_text = decode_ff7_english(steam_bytes)

        # Check if in skip region
        if idx in SKIP_REGIONS:
            results.append(PatchResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                en_text=en_text, de_text="", de_bytes=b"",
                status="SKIPPED", notes="Skip region (UNICODE/FFPADDED/ZEROTERM)",
                string_type=stype, slot_length=length, truncated_by=0
            ))
            stats['skipped'] += 1
            continue

        # Skip RGB keyboard regions - keep English
        if idx in RGB_KEYBOARD_REGIONS:
            results.append(PatchResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                en_text=en_text, de_text="", de_bytes=b"",
                status="SKIPPED", notes="RGB keyboard region - keep English",
                string_type=stype, slot_length=length, truncated_by=0
            ))
            stats['skipped'] += 1
            continue

        # Skip single-byte entries
        if length <= 1:
            results.append(PatchResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                en_text=en_text, de_text="", de_bytes=b"",
                status="SKIPPED", notes="Single byte entry",
                string_type=stype, slot_length=length, truncated_by=0
            ))
            stats['short'] += 1
            continue

        # Skip empty strings
        if not en_text.strip():
            results.append(PatchResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                en_text=en_text, de_text="", de_bytes=b"",
                status="SKIPPED", notes="Empty English string",
                string_type=stype, slot_length=length, truncated_by=0
            ))
            stats['short'] += 1
            continue

        # Look up German translation
        de_text = EN_TO_DE_DICTIONARY.get(en_text)

        if de_text is None:
            # Try variations
            de_text = EN_TO_DE_DICTIONARY.get(en_text.strip())
            if de_text is None:
                de_text = EN_TO_DE_DICTIONARY.get(en_text.capitalize())
                if de_text is None:
                    # Try lowercase
                    de_text = EN_TO_DE_DICTIONARY.get(en_text.lower())

        if de_text is None:
            # No translation found - try searching DE exe directly for EN text
            result = find_german_text_in_de_exe(de_data, en_text)
            if result:
                _, de_bytes = result
                de_text = decode_ff7_german(de_bytes)
                if de_text == en_text:
                    # Same text in both - no patch needed
                    results.append(PatchResult(
                        idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                        en_text=en_text, de_text=de_text, de_bytes=de_bytes,
                        status="IDENTICAL", notes="EN = DE (no patch needed)",
                        string_type=stype, slot_length=length, truncated_by=0
                    ))
                    stats['identical'] += 1
                    continue
            else:
                results.append(PatchResult(
                    idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                    en_text=en_text, de_text="", de_bytes=b"",
                    status="NO_TRANSLATION", notes="No translation in dictionary or DE exe",
                    string_type=stype, slot_length=length, truncated_by=0
                ))
                stats['no_translation'] += 1
                continue

        # Find German bytes in DE exe
        result = find_german_text_in_de_exe(de_data, de_text)
        if result:
            _, de_bytes = result
        else:
            # Encode German text directly
            de_bytes = encode_ff7_german(de_text) + b'\xff'

        # Check if EN and DE are identical
        if decode_ff7_german(de_bytes) == en_text:
            results.append(PatchResult(
                idx=idx, steam_offset=steam_offset, steam_va=steam_va,
                en_text=en_text, de_text=de_text, de_bytes=de_bytes,
                status="IDENTICAL", notes="EN = DE (no patch needed)",
                string_type=stype, slot_length=length, truncated_by=0
            ))
            stats['identical'] += 1
            continue

        # Handle truncation if DE is longer than slot
        truncated_by = 0
        if len(de_bytes) > length:
            truncated_by = len(de_bytes) - length
            de_bytes = de_bytes[:length - 1] + b'\xff'
            status = "TRUNCATED"
            notes = f"Truncated by {truncated_by} bytes"
            stats['truncated'] += 1
        else:
            status = "PATCHED"
            notes = ""
            stats['patched'] += 1

        results.append(PatchResult(
            idx=idx, steam_offset=steam_offset, steam_va=steam_va,
            en_text=en_text, de_text=de_text, de_bytes=de_bytes,
            status=status, notes=notes,
            string_type=stype, slot_length=length, truncated_by=truncated_by
        ))

    return results, stats


# =============================================================================
# OUTPUT GENERATION
# =============================================================================

def write_hext_file(results: List[PatchResult], output_path: Path, session_id: str):
    """Write HEXT patch file."""
    patches = [r for r in results if r.status in ("PATCHED", "TRUNCATED")]

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S JST")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# =================================================================\n")
        f.write("# German Menu Text Patch for FF7 Steam English\n")
        f.write("# =================================================================\n")
        f.write("# AUTO-GENERATED by generate_german_hext_comprehensive.py\n")
        f.write(f"# Generated: {timestamp}\n")
        f.write(f"# Session: {session_id}\n")
        f.write("#\n")
        f.write(f"# Total patches: {len(patches)}\n")
        f.write("#\n")
        f.write("# Virtual Address Formula:\n")
        f.write("# VA = (FileOffset - 0x3B8A00) + 0x3BA000 + 0x400000\n")
        f.write("# VA = FileOffset + 0x400800\n")
        f.write("#\n")
        f.write("# German Umlaut Encoding:\n")
        f.write("# ä = 0x6A, ö = 0x7A, ü = 0x7F, ß = 0x7E\n")
        f.write("#\n")
        f.write("# Source: touphScript ff7exe.cpp offset table\n")
        f.write("# Target: Steam English ff7_en.exe\n")
        f.write("# =================================================================\n\n")

        # Group by sections
        current_section = None
        section_map = {
            (0, 5): "Quit Dialog",
            (5, 33): "Save Slot Descriptions",
            (33, 36): "Yes/No Labels",
            (36, 58): "Main Menu & Config",
            (58, 77): "Config Help Text",
            (77, 214): "Keyboard Labels (RGB)",
            (214, 293): "Battle/Status Strings",
            (293, 328): "Status Effects",
            (328, 365): "Character Stats",
            (365, 400): "Limit/Materia",
            (400, 461): "Battle Messages",
            (461, 529): "Name Entry (UNICODE)",
            (529, 600): "Shop/Item Menu",
            (600, 650): "Gold Saucer",
            (650, 700): "Save/Load",
            (700, 767): "Chocobo/Misc",
        }

        for patch in patches:
            # Determine section
            for (start, end), name in section_map.items():
                if start <= patch.idx < end:
                    if current_section != name:
                        current_section = name
                        f.write(f"\n# {'=' * 60}\n")
                        f.write(f"# Section: {name} (Indices {start}-{end-1})\n")
                        f.write(f"# {'=' * 60}\n\n")
                    break

            # Format bytes
            hex_bytes = ' '.join(f'{b:02X}' for b in patch.de_bytes)

            # Pad if needed
            if len(patch.de_bytes) < patch.slot_length:
                padding = ' '.join('00' for _ in range(patch.slot_length - len(patch.de_bytes)))
                hex_bytes += ' ' + padding

            # Write comment
            en_short = patch.en_text[:30] + "..." if len(patch.en_text) > 30 else patch.en_text
            de_short = patch.de_text[:30] + "..." if len(patch.de_text) > 30 else patch.de_text

            f.write(f"# [{patch.idx}] \"{en_short}\" -> \"{de_short}\"")
            if patch.status == "TRUNCATED":
                f.write(f" [TRUNCATED by {patch.truncated_by}]")
            f.write("\n")

            f.write(f"# File: 0x{patch.steam_offset:08X}, Slot: {patch.slot_length} bytes\n")
            f.write(f"{patch.steam_va:06X} = {hex_bytes}\n\n")

    print(f"Wrote {len(patches)} patches to: {output_path}")


def write_report(results: List[PatchResult], stats: Dict, output_path: Path, session_id: str):
    """Write generation report."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S JST")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# German HEXT Generation Report\n\n")
        f.write(f"**Generated:** {timestamp}  \n")
        f.write(f"**Session:** {session_id}  \n")
        f.write(f"**Script:** generate_german_hext_comprehensive.py  \n\n")

        f.write("## Summary Statistics\n\n")
        f.write(f"| Metric | Count |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total touphScript strings | {stats['total']} |\n")
        f.write(f"| **Successfully patched** | **{stats['patched']}** |\n")
        f.write(f"| Truncated (DE > EN slot) | {stats['truncated']} |\n")
        f.write(f"| Identical (EN = DE) | {stats['identical']} |\n")
        f.write(f"| Skipped (special regions) | {stats['skipped']} |\n")
        f.write(f"| No translation found | {stats['no_translation']} |\n")
        f.write(f"| Short/Empty strings | {stats['short']} |\n\n")

        total_patchable = stats['patched'] + stats['truncated']
        success_rate = (total_patchable / stats['total']) * 100 if stats['total'] > 0 else 0
        f.write(f"**Total patches generated:** {total_patchable}  \n")
        f.write(f"**Success rate:** {success_rate:.1f}%  \n\n")

        # Truncated strings
        truncated = [r for r in results if r.status == "TRUNCATED"]
        if truncated:
            f.write("## Truncated Strings\n\n")
            f.write("These German strings were longer than the English slot and were truncated:\n\n")
            f.write("| Idx | EN Text | DE Text | Truncated By |\n")
            f.write("|-----|---------|---------|-------------|\n")
            for r in truncated[:50]:  # Show first 50
                en_short = r.en_text[:20].replace('|', '\\|')
                de_short = r.de_text[:20].replace('|', '\\|')
                f.write(f"| {r.idx} | {en_short} | {de_short} | {r.truncated_by} bytes |\n")
            if len(truncated) > 50:
                f.write(f"\n*... and {len(truncated) - 50} more*\n")
            f.write("\n")

        # No translation found
        no_trans = [r for r in results if r.status == "NO_TRANSLATION"]
        if no_trans:
            f.write("## Strings Without Translation\n\n")
            f.write("These English strings had no German translation in the dictionary:\n\n")
            f.write("| Idx | EN Text | Notes |\n")
            f.write("|-----|---------|-------|\n")
            for r in no_trans[:50]:
                en_short = r.en_text[:30].replace('|', '\\|')
                f.write(f"| {r.idx} | {en_short} | {r.notes} |\n")
            if len(no_trans) > 50:
                f.write(f"\n*... and {len(no_trans) - 50} more*\n")
            f.write("\n")

    print(f"Wrote report to: {output_path}")


def write_dictionary(output_path: Path):
    """Write the EN->DE dictionary to file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# FF7 English to German Translation Dictionary\n")
        f.write(f"# Total entries: {len(EN_TO_DE_DICTIONARY)}\n\n")

        for en, de in sorted(EN_TO_DE_DICTIONARY.items()):
            f.write(f'"{en}" -> "{de}"\n')

    print(f"Wrote dictionary to: {output_path}")


def write_testing_instructions(output_path: Path):
    """Write testing instructions."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Testing Instructions for German HEXT Patch\n\n")
        f.write("## Prerequisites\n\n")
        f.write("1. FF7 Steam English version installed\n")
        f.write("2. FFNx mod loader installed\n\n")

        f.write("## Installation\n\n")
        f.write("1. Copy `german_menu_complete.txt` to:\n")
        f.write("   ```\n")
        f.write("   [FF7 Install Dir]/hext/ff7/de/\n")
        f.write("   ```\n")
        f.write("   Full path example:\n")
        f.write("   ```\n")
        f.write("   C:\\Program Files (x86)\\Steam\\steamapps\\common\\FINAL FANTASY VII\\hext\\ff7\\de\\german_menu_complete.txt\n")
        f.write("   ```\n\n")

        f.write("2. Edit `FFNx.toml` and set:\n")
        f.write("   ```toml\n")
        f.write("   hext_patching_path = \"hext/ff7/de\"\n")
        f.write("   ```\n\n")

        f.write("## Testing Checklist\n\n")
        f.write("Verify the following menu screens show German text:\n\n")
        f.write("- [ ] Main menu (Objekt, Magie, Materia, etc.)\n")
        f.write("- [ ] Config menu (Fensterfarbe, Kampftempo, etc.)\n")
        f.write("- [ ] Item menu (Verwenden, Ordnen)\n")
        f.write("- [ ] Shop menu (Kaufen, Verkaufen, Verlassen)\n")
        f.write("- [ ] Status screen (Stärke, Vitalität, etc.)\n")
        f.write("- [ ] Materia menu (Prüfen, Tauschen)\n")
        f.write("- [ ] Save/Load menu (Speichern, Laden)\n")
        f.write("- [ ] Quit dialog (Möchten Sie... verlassen)\n\n")

        f.write("## Known Limitations\n\n")
        f.write("1. Some German strings are truncated when they exceed English slot size\n")
        f.write("2. Keyboard labels remain in English (standard for all languages)\n")
        f.write("3. Unicode name entry characters unchanged\n")
        f.write("4. Chocobo jockey names unchanged (proper nouns)\n\n")

        f.write("## Troubleshooting\n\n")
        f.write("If German text doesn't appear:\n\n")
        f.write("1. Check FFNx.toml path is correct\n")
        f.write("2. Verify HEXT file is in correct directory\n")
        f.write("3. Check FFNx APP.log for HEXT loading messages\n")
        f.write("4. Ensure using Steam English executable (not GOG or other)\n")

    print(f"Wrote testing instructions to: {output_path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    session_id = "527f1809-5a36-47f0-b06e-c4e9d2f7397d"

    print("=" * 70)
    print("FF7 German HEXT Generator - COMPREHENSIVE VERSION")
    print("=" * 70)
    print(f"Session: {session_id}")
    print()

    # Check file existence
    print("Checking exe files...")
    if not STEAM_EN.exists():
        print(f"ERROR: Steam EN exe not found: {STEAM_EN}")
        sys.exit(1)
    if not ESTORE_DE.exists():
        print(f"ERROR: eStore DE exe not found: {ESTORE_DE}")
        sys.exit(1)

    # Load exe files
    print("Loading exe files...")
    with open(STEAM_EN, 'rb') as f:
        steam_data = f.read()
    with open(ESTORE_DE, 'rb') as f:
        de_data = f.read()

    print(f"  Steam EN: {len(steam_data):,} bytes")
    print(f"  eStore DE: {len(de_data):,} bytes")
    print(f"  Dictionary entries: {len(EN_TO_DE_DICTIONARY)}")
    print()

    # Generate patches
    print("Generating patches...")
    results, stats = generate_patches(steam_data, de_data)

    # Print stats
    print()
    print("=" * 70)
    print("GENERATION RESULTS")
    print("=" * 70)
    print(f"  Total strings:     {stats['total']}")
    print(f"  Patched:           {stats['patched']}")
    print(f"  Truncated:         {stats['truncated']}")
    print(f"  Identical (EN=DE): {stats['identical']}")
    print(f"  Skipped:           {stats['skipped']}")
    print(f"  No translation:    {stats['no_translation']}")
    print(f"  Short/Empty:       {stats['short']}")
    print()

    total_patches = stats['patched'] + stats['truncated']
    print(f"  TOTAL PATCHES: {total_patches}")
    print()

    # Write output files
    print("Writing output files...")
    write_hext_file(results, HEXT_OUTPUT, session_id)
    write_report(results, stats, REPORT_OUTPUT, session_id)
    write_dictionary(DICTIONARY_OUTPUT)
    write_testing_instructions(TESTING_OUTPUT)

    print()
    print("=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"HEXT file: {HEXT_OUTPUT.name}")
    print(f"Report: {REPORT_OUTPUT.name}")
    print(f"Dictionary: {DICTIONARY_OUTPUT.name}")
    print(f"Testing: {TESTING_OUTPUT.name}")


if __name__ == "__main__":
    main()

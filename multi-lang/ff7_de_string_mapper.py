#!/usr/bin/env python3
"""
FF7 German String Mapper - Finding German Translations

For strings that match exactly between EN and DE (like "Sound", "Cursor", "ATB"),
the offset can be found by searching for exact bytes.

For localized strings, we need a different approach:
1. Use context - surrounding strings that ARE identical
2. Search for known German translations
3. Use pointer tables if they exist

This script focuses on accurate mapping for strings that exist in both EN and DE.

Created: 2025-01-02
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import struct

# Paths
STEAM_EN_EXE = Path("/mnt/c/Program Files (x86)/Steam/steamapps/common/FINAL FANTASY VII/ff7_en.exe")
ESTORE_EN_EXE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_en.exe")
ESTORE_DE_EXE = Path("/mnt/d/Games/Stand-alone/FINAL FANTASY VII/ff7_de.exe")

STEAM_TO_ESTORE_DELTA = 0xC00

# ALL 767 offsets from touphScript
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

def decode_ff7_english(data: bytes) -> str:
    """Decode English FF7 string."""
    result = []
    for byte in data:
        if byte == 0xFF:
            break
        if byte == 0x00:
            result.append(' ')
        elif 0x01 <= byte <= 0x5F:
            result.append(chr(byte + 0x20))
        else:
            result.append(f'[{byte:02X}]')
    return ''.join(result)


def find_all_occurrences(f, search_bytes: bytes, max_results: int = 100) -> List[int]:
    """Find all occurrences of bytes in file."""
    f.seek(0, 2)
    file_size = f.tell()
    f.seek(0)

    matches = []
    search_len = len(search_bytes)
    chunk_size = 1024 * 1024  # 1MB

    pos = 0
    while pos < file_size and len(matches) < max_results:
        f.seek(pos)
        # Read extra to catch cross-boundary matches
        chunk = f.read(min(chunk_size + search_len, file_size - pos))

        idx = 0
        while True:
            found = chunk.find(search_bytes, idx)
            if found == -1 or len(matches) >= max_results:
                break
            matches.append(pos + found)
            idx = found + 1

        pos += chunk_size

    return matches


def analyze_all_strings():
    """Analyze strings and find DE offsets where possible."""

    print("FF7 German String Mapper")
    print("=" * 70)
    print()

    # Check file sizes
    for p, name in [(STEAM_EN_EXE, "Steam EN"), (ESTORE_EN_EXE, "eStore EN"), (ESTORE_DE_EXE, "eStore DE")]:
        if not p.exists():
            print(f"ERROR: {name} not found: {p}")
            sys.exit(1)
        print(f"{name}: {p.stat().st_size:,} bytes")

    print()
    print(f"Total strings to analyze: {len(EN_OFFSETS)}")
    print()

    # Statistics
    exact_matches = 0
    unique_matches = 0
    multiple_matches = 0
    no_matches = 0

    # Results storage
    results = {}

    with open(STEAM_EN_EXE, 'rb') as steam_f, \
         open(ESTORE_EN_EXE, 'rb') as estore_en_f, \
         open(ESTORE_DE_EXE, 'rb') as estore_de_f:

        for idx, (steam_off, length) in enumerate(zip(EN_OFFSETS, STRING_LENGTHS)):
            estore_en_off = steam_off + STEAM_TO_ESTORE_DELTA

            # Read EN string
            steam_f.seek(steam_off)
            en_bytes = steam_f.read(length)
            en_text = decode_ff7_english(en_bytes)

            # Verify eStore EN matches
            estore_en_f.seek(estore_en_off)
            estore_en_bytes = estore_en_f.read(length)

            if en_bytes != estore_en_bytes:
                print(f"WARNING: [{idx}] EN mismatch at 0x{steam_off:06X}")
                continue

            # Search for exact bytes in DE
            de_matches = find_all_occurrences(estore_de_f, en_bytes, max_results=20)

            result = {
                'steam_off': steam_off,
                'estore_en_off': estore_en_off,
                'de_off': None,
                'en_text': en_text,
                'de_text': None,
                'match_type': None,
                'delta': None,
            }

            if len(de_matches) == 0:
                no_matches += 1
                result['match_type'] = 'localized'
                # String is different in German - can't use byte search
            elif len(de_matches) == 1:
                unique_matches += 1
                result['match_type'] = 'unique'
                result['de_off'] = de_matches[0]
                result['delta'] = de_matches[0] - estore_en_off
                estore_de_f.seek(de_matches[0])
                result['de_text'] = decode_ff7_english(estore_de_f.read(length))
            else:
                multiple_matches += 1
                result['match_type'] = 'multiple'
                # Pick the closest match to expected offset
                expected = estore_en_off
                closest = min(de_matches, key=lambda x: abs(x - expected))
                result['de_off'] = closest
                result['delta'] = closest - estore_en_off
                result['all_matches'] = de_matches
                estore_de_f.seek(closest)
                result['de_text'] = decode_ff7_english(estore_de_f.read(length))

            results[idx] = result

            # Progress
            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1}/{len(EN_OFFSETS)}...")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Unique matches (EN=DE, 1 occurrence):  {unique_matches}")
    print(f"Multiple matches (EN=DE, >1 occurrence): {multiple_matches}")
    print(f"Localized (EN!=DE, needs translation): {no_matches}")
    print()

    # Analyze delta patterns for matches
    print("DELTA ANALYSIS (for strings where EN=DE):")
    deltas = {}
    for idx, r in results.items():
        if r['delta'] is not None:
            d = r['delta']
            if d not in deltas:
                deltas[d] = []
            deltas[d].append(idx)

    # Sort by frequency
    sorted_deltas = sorted(deltas.items(), key=lambda x: -len(x[1]))[:20]
    for delta, indices in sorted_deltas:
        print(f"  Delta 0x{delta:X} ({delta:+d}): {len(indices)} strings")
        if len(indices) <= 5:
            print(f"    Indices: {indices}")

    print()
    print("=" * 70)
    print("DETAILED RESULTS (first 100)")
    print("=" * 70)
    print()

    for idx in range(min(100, len(EN_OFFSETS))):
        r = results.get(idx)
        if not r:
            continue

        steam_hex = f"0x{r['steam_off']:06X}"
        estore_hex = f"0x{r['estore_en_off']:06X}"

        if r['de_off']:
            de_hex = f"0x{r['de_off']:06X}"
            delta_str = f"delta={r['delta']:+d} (0x{r['delta']:X})" if r['delta'] >= 0 else f"delta={r['delta']:d} (-0x{-r['delta']:X})"
        else:
            de_hex = "LOCALIZED"
            delta_str = "N/A"

        print(f"[{idx:3d}] {r['match_type']:10s} | Steam: {steam_hex} | eStore: {estore_hex} | DE: {de_hex}")
        print(f"      {delta_str}")
        print(f"      EN: {r['en_text'][:50]!r}")
        if r['de_text']:
            print(f"      DE: {r['de_text'][:50]!r}")
        print()

    # Generate Python code for mapping
    print()
    print("=" * 70)
    print("PYTHON MAPPING CODE")
    print("=" * 70)
    print()
    print("# Mapping: index -> (steam_off, estore_en_off, de_off, delta, match_type)")
    print("DE_STRING_MAP = {")
    for idx in sorted(results.keys()):
        r = results[idx]
        de_off_str = f"0x{r['de_off']:06X}" if r['de_off'] else "None"
        delta_str = f"{r['delta']}" if r['delta'] is not None else "None"
        print(f"    {idx}: (0x{r['steam_off']:06X}, 0x{r['estore_en_off']:06X}, {de_off_str}, {delta_str}, {r['match_type']!r}),")
    print("}")

    return results


if __name__ == '__main__':
    analyze_all_strings()

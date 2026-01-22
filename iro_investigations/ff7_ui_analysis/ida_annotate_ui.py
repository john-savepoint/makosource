"""
FF7 UI Memory Location Annotations for IDA Pro
Generated automatically from HEXT analysis

Usage in IDA Pro:
    File -> Script file... -> Select this file
"""

import idaapi
import idc

def annotate_ui_locations():
    """Add comments to all known UI memory locations."""

    # 0023B6B8: Syncs Barrett's animation to opening music
    idc.set_cmt(0x0023B6B8, "[UI] Syncs Barrett's animation to opening music", 0)
    idc.set_name(0x0023B6B8, "ui_0023B6B8", idaapi.SN_NOWARN)
    # 009204E8: limit menu - description box X-Axis, Y-Axis, Width
    idc.set_cmt(0x009204E8, "[UI] limit menu - description box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x009204E8, "ui_009204E8", idaapi.SN_NOWARN)
    # 00920AD0: equip menu - description box X-Axis, Y-Axis, Width
    idc.set_cmt(0x00920AD0, "[UI] equip menu - description box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x00920AD0, "ui_00920AD0", idaapi.SN_NOWARN)
    # 06FF211: save text X-Axis
    idc.set_cmt(0x06FF211, "[UI] save text X-Axis", 0)
    idc.set_name(0x06FF211, "ui_06FF211", idaapi.SN_NOWARN)
    # 41B4E8: screen pos - increases pheonix glitch but overall 
    idc.set_cmt(0x41B4E8, "[UI] screen pos - increases pheonix glitch but overall better experience", 0)
    idc.set_name(0x41B4E8, "ui_41B4E8", idaapi.SN_NOWARN)
    # 41B51A: FMV/FIELD C0, STOCK 4C, FULL SCREEN E0
    idc.set_cmt(0x41B51A, "[UI] FMV/FIELD C0, STOCK 4C, FULL SCREEN E0", 0)
    idc.set_name(0x41B51A, "ui_41B51A", idaapi.SN_NOWARN)
    # 41C4C0: Certain statuses like Resist are intentionally not
    idc.set_cmt(0x41C4C0, "[UI] Certain statuses like Resist are intentionally not shown in the battle menu.  To place them back:", 0)
    idc.set_name(0x41C4C0, "ui_41C4C0", idaapi.SN_NOWARN)
    # 5BB847: Battle text/graphics like \"Recovery\" position
    idc.set_cmt(0x5BB847, "[UI] Battle text/graphics like \"Recovery\" position", 0)
    idc.set_name(0x5BB847, "ui_5BB847", idaapi.SN_NOWARN)
    # 5BCFD0: mini avatar support
    idc.set_cmt(0x5BCFD0, "[UI] mini avatar support", 0)
    idc.set_name(0x5BCFD0, "ui_5BCFD0", idaapi.SN_NOWARN)
    # 5BCFD7: time BA normal  00 no fade in (shrinking black are
    idc.set_cmt(0x5BCFD7, "[UI] time BA normal  00 no fade in (shrinking black area)", 0)
    idc.set_name(0x5BCFD7, "ui_5BCFD7", idaapi.SN_NOWARN)
    # 630CEB: field boxes Y-Axis negative offset 91449D to chang
    idc.set_cmt(0x630CEB, "[UI] field boxes Y-Axis negative offset 91449D to change value", 0)
    idc.set_name(0x630CEB, "ui_630CEB", idaapi.SN_NOWARN)
    # 630EA9: field boxes viewable lines offset (refresh dialog)
    idc.set_cmt(0x630EA9, "[UI] field boxes viewable lines offset (refresh dialog)", 0)
    idc.set_name(0x630EA9, "ui_630EA9", idaapi.SN_NOWARN)
    # 630EFC: field dialog text block scroll amount (refresh dia
    idc.set_cmt(0x630EFC, "[UI] field dialog text block scroll amount (refresh dialog)", 0)
    idc.set_name(0x630EFC, "ui_630EFC", idaapi.SN_NOWARN)
    # 6311FA: field boxes viewable lines offset (refresh dialog)
    idc.set_cmt(0x6311FA, "[UI] field boxes viewable lines offset (refresh dialog)", 0)
    idc.set_name(0x6311FA, "ui_6311FA", idaapi.SN_NOWARN)
    # 63124D: field dialog text block scroll amount (refresh dia
    idc.set_cmt(0x63124D, "[UI] field dialog text block scroll amount (refresh dialog)", 0)
    idc.set_name(0x63124D, "ui_63124D", idaapi.SN_NOWARN)
    # 631382: field cursor X-Axis
    idc.set_cmt(0x631382, "[UI] field cursor X-Axis", 0)
    idc.set_name(0x631382, "ui_631382", idaapi.SN_NOWARN)
    # 63138A: cursor spacing Y-Axis
    idc.set_cmt(0x63138A, "[UI] cursor spacing Y-Axis", 0)
    idc.set_name(0x63138A, "ui_63138A", idaapi.SN_NOWARN)
    # 63138F: field cursor Y-Axis
    idc.set_cmt(0x63138F, "[UI] field cursor Y-Axis", 0)
    idc.set_name(0x63138F, "ui_63138F", idaapi.SN_NOWARN)
    # 63191A: field box padding top/bottom 914488 to change valu
    idc.set_cmt(0x63191A, "[UI] field box padding top/bottom 914488 to change value", 0)
    idc.set_name(0x63191A, "ui_63191A", idaapi.SN_NOWARN)
    # 631B34: field boxes viewable lines offset (refresh dialog)
    idc.set_cmt(0x631B34, "[UI] field boxes viewable lines offset (refresh dialog)", 0)
    idc.set_name(0x631B34, "ui_631B34", idaapi.SN_NOWARN)
    # 631D27: field dialog text choices X-Axis (refresh dialog)
    idc.set_cmt(0x631D27, "[UI] field dialog text choices X-Axis (refresh dialog)", 0)
    idc.set_name(0x631D27, "ui_631D27", idaapi.SN_NOWARN)
    # 632CD7: field dialog text block scroll amount (refresh dia
    idc.set_cmt(0x632CD7, "[UI] field dialog text block scroll amount (refresh dialog)", 0)
    idc.set_name(0x632CD7, "ui_632CD7", idaapi.SN_NOWARN)
    # 632CEC: field dialog text block scroll amount (refresh dia
    idc.set_cmt(0x632CEC, "[UI] field dialog text block scroll amount (refresh dialog)", 0)
    idc.set_name(0x632CEC, "ui_632CEC", idaapi.SN_NOWARN)
    # 649A4A: modified code to only work when no dialog box on s
    idc.set_cmt(0x649A4A, "[UI] modified code to only work when no dialog box on screen.", 0)
    idc.set_name(0x649A4A, "ui_649A4A", idaapi.SN_NOWARN)
    # 6C20AF: Cursor Y-Axis
    idc.set_cmt(0x6C20AF, "[UI] Cursor Y-Axis", 0)
    idc.set_name(0x6C20AF, "ui_6C20AF", idaapi.SN_NOWARN)
    # 6C20B2: Cursor X-Axis
    idc.set_cmt(0x6C20B2, "[UI] Cursor X-Axis", 0)
    idc.set_name(0x6C20B2, "ui_6C20B2", idaapi.SN_NOWARN)
    # 6C20E5: ghost cursor color box Y-Axis
    idc.set_cmt(0x6C20E5, "[UI] ghost cursor color box Y-Axis", 0)
    idc.set_name(0x6C20E5, "ui_6C20E5", idaapi.SN_NOWARN)
    # 6C20E8: ghost cursor color box X-Axis
    idc.set_cmt(0x6C20E8, "[UI] ghost cursor color box X-Axis", 0)
    idc.set_name(0x6C20E8, "ui_6C20E8", idaapi.SN_NOWARN)
    # 6C213E: ghost cursor sound box Y-Axis
    idc.set_cmt(0x6C213E, "[UI] ghost cursor sound box Y-Axis", 0)
    idc.set_name(0x6C213E, "ui_6C213E", idaapi.SN_NOWARN)
    # 6C2141: ghost cursor sound box X-Axis
    idc.set_cmt(0x6C2141, "[UI] ghost cursor sound box X-Axis", 0)
    idc.set_name(0x6C2141, "ui_6C2141", idaapi.SN_NOWARN)
    # 6C216F: sound box width
    idc.set_cmt(0x6C216F, "[UI] sound box width", 0)
    idc.set_name(0x6C216F, "ui_6C216F", idaapi.SN_NOWARN)
    # 6C217F: sound box Y-Axis
    idc.set_cmt(0x6C217F, "[UI] sound box Y-Axis", 0)
    idc.set_name(0x6C217F, "ui_6C217F", idaapi.SN_NOWARN)
    # 6C218C: sound box X-Axis
    idc.set_cmt(0x6C218C, "[UI] sound box X-Axis", 0)
    idc.set_name(0x6C218C, "ui_6C218C", idaapi.SN_NOWARN)
    # 6C222D: sound box top numbers Y-Axis
    idc.set_cmt(0x6C222D, "[UI] sound box top numbers Y-Axis", 0)
    idc.set_name(0x6C222D, "ui_6C222D", idaapi.SN_NOWARN)
    # 6C2234: sound box top numbers X-Axis
    idc.set_cmt(0x6C2234, "[UI] sound box top numbers X-Axis", 0)
    idc.set_name(0x6C2234, "ui_6C2234", idaapi.SN_NOWARN)
    # 6C22D1: sound box bottom numbers Y-Axis
    idc.set_cmt(0x6C22D1, "[UI] sound box bottom numbers Y-Axis", 0)
    idc.set_name(0x6C22D1, "ui_6C22D1", idaapi.SN_NOWARN)
    # 6C22D8: sound box bottom numbers X-Axis
    idc.set_cmt(0x6C22D8, "[UI] sound box bottom numbers X-Axis", 0)
    idc.set_name(0x6C22D8, "ui_6C22D8", idaapi.SN_NOWARN)
    # 6C2326: sound box bottom icon Y-Axis
    idc.set_cmt(0x6C2326, "[UI] sound box bottom icon Y-Axis", 0)
    idc.set_name(0x6C2326, "ui_6C2326", idaapi.SN_NOWARN)
    # 6C235D: sound box cursor X-Axis
    idc.set_cmt(0x6C235D, "[UI] sound box cursor X-Axis", 0)
    idc.set_name(0x6C235D, "ui_6C235D", idaapi.SN_NOWARN)
    # 6C239D: window color box Y-Axis
    idc.set_cmt(0x6C239D, "[UI] window color box Y-Axis", 0)
    idc.set_name(0x6C239D, "ui_6C239D", idaapi.SN_NOWARN)
    # 6C23AA: window color box X-Axis
    idc.set_cmt(0x6C23AA, "[UI] window color box X-Axis", 0)
    idc.set_name(0x6C23AA, "ui_6C23AA", idaapi.SN_NOWARN)
    # 6C31FF: left text block Y-Axis
    idc.set_cmt(0x6C31FF, "[UI] left text block Y-Axis", 0)
    idc.set_name(0x6C31FF, "ui_6C31FF", idaapi.SN_NOWARN)
    # 6C3226: magic order Y-Axis
    idc.set_cmt(0x6C3226, "[UI] magic order Y-Axis", 0)
    idc.set_name(0x6C3226, "ui_6C3226", idaapi.SN_NOWARN)
    # 6C325F: sound and music volume Y-Axis
    idc.set_cmt(0x6C325F, "[UI] sound and music volume Y-Axis", 0)
    idc.set_name(0x6C325F, "ui_6C325F", idaapi.SN_NOWARN)
    # 6C32AA: Normal/Customize Y-Axis
    idc.set_cmt(0x6C32AA, "[UI] Normal/Customize Y-Axis", 0)
    idc.set_name(0x6C32AA, "ui_6C32AA", idaapi.SN_NOWARN)
    # 6C32B1: Customize X-Axis
    idc.set_cmt(0x6C32B1, "[UI] Customize X-Axis", 0)
    idc.set_name(0x6C32B1, "ui_6C32B1", idaapi.SN_NOWARN)
    # 6C32F8: Initial/Memory Y-Axis
    idc.set_cmt(0x6C32F8, "[UI] Initial/Memory Y-Axis", 0)
    idc.set_name(0x6C32F8, "ui_6C32F8", idaapi.SN_NOWARN)
    # 6C32FF: Memory X-Axis
    idc.set_cmt(0x6C32FF, "[UI] Memory X-Axis", 0)
    idc.set_name(0x6C32FF, "ui_6C32FF", idaapi.SN_NOWARN)
    # 6C3346: Auto/Fixed Y-Axis
    idc.set_cmt(0x6C3346, "[UI] Auto/Fixed Y-Axis", 0)
    idc.set_name(0x6C3346, "ui_6C3346", idaapi.SN_NOWARN)
    # 6C3350: Fixed X-Axis
    idc.set_cmt(0x6C3350, "[UI] Fixed X-Axis", 0)
    idc.set_name(0x6C3350, "ui_6C3350", idaapi.SN_NOWARN)
    # 6C33B5: Active/Recommended Y-Axis
    idc.set_cmt(0x6C33B5, "[UI] Active/Recommended Y-Axis", 0)
    idc.set_name(0x6C33B5, "ui_6C33B5", idaapi.SN_NOWARN)
    # 6C33F9: Wait Y-Axis
    idc.set_cmt(0x6C33F9, "[UI] Wait Y-Axis", 0)
    idc.set_name(0x6C33F9, "ui_6C33F9", idaapi.SN_NOWARN)
    # 6C33FC: Wait X-Axis
    idc.set_cmt(0x6C33FC, "[UI] Wait X-Axis", 0)
    idc.set_name(0x6C33FC, "ui_6C33FC", idaapi.SN_NOWARN)
    # 6C3454: restore/indirect/attack Y-Axis
    idc.set_cmt(0x6C3454, "[UI] restore/indirect/attack Y-Axis", 0)
    idc.set_name(0x6C3454, "ui_6C3454", idaapi.SN_NOWARN)
    # 6C345E: restore/indirect/attack spacing X-Axis
    idc.set_cmt(0x6C345E, "[UI] restore/indirect/attack spacing X-Axis", 0)
    idc.set_name(0x6C345E, "ui_6C345E", idaapi.SN_NOWARN)
    # 6C3461: restore/indirect/attack X-Axis
    idc.set_cmt(0x6C3461, "[UI] restore/indirect/attack X-Axis", 0)
    idc.set_name(0x6C3461, "ui_6C3461", idaapi.SN_NOWARN)
    # 6C3481: No. Y-Axis
    idc.set_cmt(0x6C3481, "[UI] No. Y-Axis", 0)
    idc.set_name(0x6C3481, "ui_6C3481", idaapi.SN_NOWARN)
    # 6C34B3: No. digit Y-Axis
    idc.set_cmt(0x6C34B3, "[UI] No. digit Y-Axis", 0)
    idc.set_name(0x6C34B3, "ui_6C34B3", idaapi.SN_NOWARN)
    # 6C34B9: No. digit X-Axis
    idc.set_cmt(0x6C34B9, "[UI] No. digit X-Axis", 0)
    idc.set_name(0x6C34B9, "ui_6C34B9", idaapi.SN_NOWARN)
    # 6C34CD: Battle speed widget X-Axis
    idc.set_cmt(0x6C34CD, "[UI] Battle speed widget X-Axis", 0)
    idc.set_name(0x6C34CD, "ui_6C34CD", idaapi.SN_NOWARN)
    # 6C3508: Battle message widget X-Axis
    idc.set_cmt(0x6C3508, "[UI] Battle message widget X-Axis", 0)
    idc.set_name(0x6C3508, "ui_6C3508", idaapi.SN_NOWARN)
    # 6C3543: Field message widget X-Axis
    idc.set_cmt(0x6C3543, "[UI] Field message widget X-Axis", 0)
    idc.set_name(0x6C3543, "ui_6C3543", idaapi.SN_NOWARN)
    # 6C35AC: all Fast Y-Axis
    idc.set_cmt(0x6C35AC, "[UI] all Fast Y-Axis", 0)
    idc.set_name(0x6C35AC, "ui_6C35AC", idaapi.SN_NOWARN)
    # 6C35B0: all Fast X-Axis
    idc.set_cmt(0x6C35B0, "[UI] all Fast X-Axis", 0)
    idc.set_name(0x6C35B0, "ui_6C35B0", idaapi.SN_NOWARN)
    # 6C35D6: all Slow Y-Axis
    idc.set_cmt(0x6C35D6, "[UI] all Slow Y-Axis", 0)
    idc.set_name(0x6C35D6, "ui_6C35D6", idaapi.SN_NOWARN)
    # 6C35DA: all Slow X-Axis
    idc.set_cmt(0x6C35DA, "[UI] all Slow X-Axis", 0)
    idc.set_name(0x6C35DA, "ui_6C35DA", idaapi.SN_NOWARN)
    # 6C35EA: all speed bars X-Axis
    idc.set_cmt(0x6C35EA, "[UI] all speed bars X-Axis", 0)
    idc.set_name(0x6C35EA, "ui_6C35EA", idaapi.SN_NOWARN)
    # 6C3602: all speed bars width
    idc.set_cmt(0x6C3602, "[UI] all speed bars width", 0)
    idc.set_name(0x6C3602, "ui_6C3602", idaapi.SN_NOWARN)
    # 6C3B60: color box cursor spacing X-Axis
    idc.set_cmt(0x6C3B60, "[UI] color box cursor spacing X-Axis", 0)
    idc.set_name(0x6C3B60, "ui_6C3B60", idaapi.SN_NOWARN)
    # 6C3B6D: color box cursor X-Axis
    idc.set_cmt(0x6C3B6D, "[UI] color box cursor X-Axis", 0)
    idc.set_name(0x6C3B6D, "ui_6C3B6D", idaapi.SN_NOWARN)
    # 6C3BAE: color box ghost cursor spacing X-Axis
    idc.set_cmt(0x6C3BAE, "[UI] color box ghost cursor spacing X-Axis", 0)
    idc.set_name(0x6C3BAE, "ui_6C3BAE", idaapi.SN_NOWARN)
    # 6C3BBA: color box ghost cursor X-Axis
    idc.set_cmt(0x6C3BBA, "[UI] color box ghost cursor X-Axis", 0)
    idc.set_name(0x6C3BBA, "ui_6C3BBA", idaapi.SN_NOWARN)
    # 6C3BD3: RGB box RGB letters and numbers X-Axis
    idc.set_cmt(0x6C3BD3, "[UI] RGB box RGB letters and numbers X-Axis", 0)
    idc.set_name(0x6C3BD3, "ui_6C3BD3", idaapi.SN_NOWARN)
    # 6C3C3C: RGB box 'B' Y-Axis
    idc.set_cmt(0x6C3C3C, "[UI] RGB box 'B' Y-Axis", 0)
    idc.set_name(0x6C3C3C, "ui_6C3C3C", idaapi.SN_NOWARN)
    # 6C3CBD: RGB box top numbers X-Axis
    idc.set_cmt(0x6C3CBD, "[UI] RGB box top numbers X-Axis", 0)
    idc.set_name(0x6C3CBD, "ui_6C3CBD", idaapi.SN_NOWARN)
    # 6C3CE1: RGB box top widget X-Axis
    idc.set_cmt(0x6C3CE1, "[UI] RGB box top widget X-Axis", 0)
    idc.set_name(0x6C3CE1, "ui_6C3CE1", idaapi.SN_NOWARN)
    # 6C3D56: RGB box middle numbers X-Axis
    idc.set_cmt(0x6C3D56, "[UI] RGB box middle numbers X-Axis", 0)
    idc.set_name(0x6C3D56, "ui_6C3D56", idaapi.SN_NOWARN)
    # 6C3D79: RGB box middle widget X-Axis
    idc.set_cmt(0x6C3D79, "[UI] RGB box middle widget X-Axis", 0)
    idc.set_name(0x6C3D79, "ui_6C3D79", idaapi.SN_NOWARN)
    # 6C3DEC: RGB box bottom numbers X-Axis
    idc.set_cmt(0x6C3DEC, "[UI] RGB box bottom numbers X-Axis", 0)
    idc.set_name(0x6C3DEC, "ui_6C3DEC", idaapi.SN_NOWARN)
    # 6C3E0E: RGB box bottom widget X-Axis
    idc.set_cmt(0x6C3E0E, "[UI] RGB box bottom widget X-Axis", 0)
    idc.set_name(0x6C3E0E, "ui_6C3E0E", idaapi.SN_NOWARN)
    # 6C3E4F: RGB box all bars X-Axis
    idc.set_cmt(0x6C3E4F, "[UI] RGB box all bars X-Axis", 0)
    idc.set_name(0x6C3E4F, "ui_6C3E4F", idaapi.SN_NOWARN)
    # 6C3EA1: RGB box cursor Y-Axis
    idc.set_cmt(0x6C3EA1, "[UI] RGB box cursor Y-Axis", 0)
    idc.set_name(0x6C3EA1, "ui_6C3EA1", idaapi.SN_NOWARN)
    # 6C3EA4: RGB box cursor X-Axis
    idc.set_cmt(0x6C3EA4, "[UI] RGB box cursor X-Axis", 0)
    idc.set_name(0x6C3EA4, "ui_6C3EA4", idaapi.SN_NOWARN)
    # 6C3EB3: RGB box width
    idc.set_cmt(0x6C3EB3, "[UI] RGB box width", 0)
    idc.set_name(0x6C3EB3, "ui_6C3EB3", idaapi.SN_NOWARN)
    # 6C3ECF: RGB box X-Axis
    idc.set_cmt(0x6C3ECF, "[UI] RGB box X-Axis", 0)
    idc.set_name(0x6C3ECF, "ui_6C3ECF", idaapi.SN_NOWARN)
    # 6C3EF4: selected color box bg width
    idc.set_cmt(0x6C3EF4, "[UI] selected color box bg width", 0)
    idc.set_name(0x6C3EF4, "ui_6C3EF4", idaapi.SN_NOWARN)
    # 6C3F52: selected color box Y-Axis
    idc.set_cmt(0x6C3F52, "[UI] selected color box Y-Axis", 0)
    idc.set_name(0x6C3F52, "ui_6C3F52", idaapi.SN_NOWARN)
    # 6C5A65: LVHPMP hp bar X-Axis
    idc.set_cmt(0x6C5A65, "[UI] LVHPMP hp bar X-Axis", 0)
    idc.set_name(0x6C5A65, "ui_6C5A65", idaapi.SN_NOWARN)
    # 6C5A78: LVHPMP hp bar length
    idc.set_cmt(0x6C5A78, "[UI] LVHPMP hp bar length", 0)
    idc.set_name(0x6C5A78, "ui_6C5A78", idaapi.SN_NOWARN)
    # 6C5ADE: LVHPMP mp bar X-Axis
    idc.set_cmt(0x6C5ADE, "[UI] LVHPMP mp bar X-Axis", 0)
    idc.set_name(0x6C5ADE, "ui_6C5ADE", idaapi.SN_NOWARN)
    # 6C5AF1: LVHPMP mp bar length
    idc.set_cmt(0x6C5AF1, "[UI] LVHPMP mp bar length", 0)
    idc.set_name(0x6C5AF1, "ui_6C5AF1", idaapi.SN_NOWARN)
    # 6C5D78: LVHPMP MAXHP X-Axis
    idc.set_cmt(0x6C5D78, "[UI] LVHPMP MAXHP X-Axis", 0)
    idc.set_name(0x6C5D78, "ui_6C5D78", idaapi.SN_NOWARN)
    # 6C5E1A: LVHPMP MAXMP X-Axis
    idc.set_cmt(0x6C5E1A, "[UI] LVHPMP MAXMP X-Axis", 0)
    idc.set_name(0x6C5E1A, "ui_6C5E1A", idaapi.SN_NOWARN)
    # 6C5E2D: LVHPMP mp divider color palette
    idc.set_cmt(0x6C5E2D, "[UI] LVHPMP mp divider color palette", 0)
    idc.set_name(0x6C5E2D, "ui_6C5E2D", idaapi.SN_NOWARN)
    # 6C5E31: LVHPMP mp divider height
    idc.set_cmt(0x6C5E31, "[UI] LVHPMP mp divider height", 0)
    idc.set_name(0x6C5E31, "ui_6C5E31", idaapi.SN_NOWARN)
    # 6C5E45: LVHPMP mp divider X-Axis
    idc.set_cmt(0x6C5E45, "[UI] LVHPMP mp divider X-Axis", 0)
    idc.set_name(0x6C5E45, "ui_6C5E45", idaapi.SN_NOWARN)
    # 6C5E58: LVHPMP hp divider color palette
    idc.set_cmt(0x6C5E58, "[UI] LVHPMP hp divider color palette", 0)
    idc.set_name(0x6C5E58, "ui_6C5E58", idaapi.SN_NOWARN)
    # 6C5E5C: LVHPMP hp divider height
    idc.set_cmt(0x6C5E5C, "[UI] LVHPMP hp divider height", 0)
    idc.set_name(0x6C5E5C, "ui_6C5E5C", idaapi.SN_NOWARN)
    # 6C5E70: LVHPMP hp divider X-Axis
    idc.set_cmt(0x6C5E70, "[UI] LVHPMP hp divider X-Axis", 0)
    idc.set_name(0x6C5E70, "ui_6C5E70", idaapi.SN_NOWARN)
    # 6C62C2: main menu (OR ALL UI?) - HP bar X-Axis
    idc.set_cmt(0x6C62C2, "[UI] main menu (OR ALL UI?) - HP bar X-Axis", 0)
    idc.set_name(0x6C62C2, "ui_6C62C2", idaapi.SN_NOWARN)
    # 6C62D5: main menu (OR ALL UI?) - HP bar length
    idc.set_cmt(0x6C62D5, "[UI] main menu (OR ALL UI?) - HP bar length", 0)
    idc.set_name(0x6C62D5, "ui_6C62D5", idaapi.SN_NOWARN)
    # 6C633B: main menu (OR ALL UI?) - MP bar X-Axis
    idc.set_cmt(0x6C633B, "[UI] main menu (OR ALL UI?) - MP bar X-Axis", 0)
    idc.set_name(0x6C633B, "ui_6C633B", idaapi.SN_NOWARN)
    # 6C634E: main menu (OR ALL UI?) - MP bar length
    idc.set_cmt(0x6C634E, "[UI] main menu (OR ALL UI?) - MP bar length", 0)
    idc.set_name(0x6C634E, "ui_6C634E", idaapi.SN_NOWARN)
    # 6C6553: main menu (OR ALL UI?) - MAXHP Value X-Axis
    idc.set_cmt(0x6C6553, "[UI] main menu (OR ALL UI?) - MAXHP Value X-Axis", 0)
    idc.set_name(0x6C6553, "ui_6C6553", idaapi.SN_NOWARN)
    # 6C65F2: main menu (OR ALL UI?) - MAXMP Value X-Axis
    idc.set_cmt(0x6C65F2, "[UI] main menu (OR ALL UI?) - MAXMP Value X-Axis", 0)
    idc.set_name(0x6C65F2, "ui_6C65F2", idaapi.SN_NOWARN)
    # 6C6605: main menu (OR ALL UI?) - MP divider color palette
    idc.set_cmt(0x6C6605, "[UI] main menu (OR ALL UI?) - MP divider color palette", 0)
    idc.set_name(0x6C6605, "ui_6C6605", idaapi.SN_NOWARN)
    # 6C6609: main menu (OR ALL UI?) - MP divider height
    idc.set_cmt(0x6C6609, "[UI] main menu (OR ALL UI?) - MP divider height", 0)
    idc.set_name(0x6C6609, "ui_6C6609", idaapi.SN_NOWARN)
    # 6C661D: main menu (OR ALL UI?) - MP divider X-Axis
    idc.set_cmt(0x6C661D, "[UI] main menu (OR ALL UI?) - MP divider X-Axis", 0)
    idc.set_name(0x6C661D, "ui_6C661D", idaapi.SN_NOWARN)
    # 6C6630: main menu (OR ALL UI?) - HP divider color pallete
    idc.set_cmt(0x6C6630, "[UI] main menu (OR ALL UI?) - HP divider color pallete", 0)
    idc.set_name(0x6C6630, "ui_6C6630", idaapi.SN_NOWARN)
    # 6C6634: main menu (OR ALL UI?) - HP divider height
    idc.set_cmt(0x6C6634, "[UI] main menu (OR ALL UI?) - HP divider height", 0)
    idc.set_name(0x6C6634, "ui_6C6634", idaapi.SN_NOWARN)
    # 6C6648: main menu (OR ALL UI?) - HP divider X-Axis
    idc.set_cmt(0x6C6648, "[UI] main menu (OR ALL UI?) - HP divider X-Axis", 0)
    idc.set_name(0x6C6648, "ui_6C6648", idaapi.SN_NOWARN)
    # 6C6E73: gil 'g' X-Axis
    idc.set_cmt(0x6C6E73, "[UI] gil 'g' X-Axis", 0)
    idc.set_name(0x6C6E73, "ui_6C6E73", idaapi.SN_NOWARN)
    # 6C6E91: gil value X-Axis
    idc.set_cmt(0x6C6E91, "[UI] gil value X-Axis", 0)
    idc.set_name(0x6C6E91, "ui_6C6E91", idaapi.SN_NOWARN)
    # 6C6EB6: gained gil 'g' X-Axis
    idc.set_cmt(0x6C6EB6, "[UI] gained gil 'g' X-Axis", 0)
    idc.set_name(0x6C6EB6, "ui_6C6EB6", idaapi.SN_NOWARN)
    # 6C6ED5: gained gil value X-Axis
    idc.set_cmt(0x6C6ED5, "[UI] gained gil value X-Axis", 0)
    idc.set_name(0x6C6ED5, "ui_6C6ED5", idaapi.SN_NOWARN)
    # 6C6EFB: left box cursor X-Axis
    idc.set_cmt(0x6C6EFB, "[UI] left box cursor X-Axis", 0)
    idc.set_name(0x6C6EFB, "ui_6C6EFB", idaapi.SN_NOWARN)
    # 6C6F17: left box unknown cursor X-Axis
    idc.set_cmt(0x6C6F17, "[UI] left box unknown cursor X-Axis", 0)
    idc.set_name(0x6C6F17, "ui_6C6F17", idaapi.SN_NOWARN)
    # 6C6F29: left box selection cursor X-Axis
    idc.set_cmt(0x6C6F29, "[UI] left box selection cursor X-Axis", 0)
    idc.set_name(0x6C6F29, "ui_6C6F29", idaapi.SN_NOWARN)
    # 6C6F3F: left box selection cursor spacing Y-Axis
    idc.set_cmt(0x6C6F3F, "[UI] left box selection cursor spacing Y-Axis", 0)
    idc.set_name(0x6C6F3F, "ui_6C6F3F", idaapi.SN_NOWARN)
    # 6C6FCC: post battle - left box item screen value spacing Y
    idc.set_cmt(0x6C6FCC, "[UI] post battle - left box item screen value spacing Y-Axis", 0)
    idc.set_name(0x6C6FCC, "ui_6C6FCC", idaapi.SN_NOWARN)
    # 6C6FCF: left box item screen value Y-Axis
    idc.set_cmt(0x6C6FCF, "[UI] left box item screen value Y-Axis", 0)
    idc.set_name(0x6C6FCF, "ui_6C6FCF", idaapi.SN_NOWARN)
    # 6C6FD5: left box item screen value X-Axis
    idc.set_cmt(0x6C6FD5, "[UI] left box item screen value X-Axis", 0)
    idc.set_name(0x6C6FD5, "ui_6C6FD5", idaapi.SN_NOWARN)
    # 6C7013: post battle - right box item screen value spacing 
    idc.set_cmt(0x6C7013, "[UI] post battle - right box item screen value spacing Y-Axis", 0)
    idc.set_name(0x6C7013, "ui_6C7013", idaapi.SN_NOWARN)
    # 6C7015: right box item screen value Y-Axis
    idc.set_cmt(0x6C7015, "[UI] right box item screen value Y-Axis", 0)
    idc.set_name(0x6C7015, "ui_6C7015", idaapi.SN_NOWARN)
    # 6C701B: right box item screen value X-Axis
    idc.set_cmt(0x6C701B, "[UI] right box item screen value X-Axis", 0)
    idc.set_name(0x6C701B, "ui_6C701B", idaapi.SN_NOWARN)
    # 6C7045: gained gil no items X-Axis
    idc.set_cmt(0x6C7045, "[UI] gained gil no items X-Axis", 0)
    idc.set_name(0x6C7045, "ui_6C7045", idaapi.SN_NOWARN)
    # 6C7097: gained gil/items Y-Axis
    idc.set_cmt(0x6C7097, "[UI] gained gil/items Y-Axis", 0)
    idc.set_name(0x6C7097, "ui_6C7097", idaapi.SN_NOWARN)
    # 6C7099: gained gil/items X-Axis
    idc.set_cmt(0x6C7099, "[UI] gained gil/items X-Axis", 0)
    idc.set_name(0x6C7099, "ui_6C7099", idaapi.SN_NOWARN)
    # 6C70B9: item screen take evrything WORD Y-Axis
    idc.set_cmt(0x6C70B9, "[UI] item screen take evrything WORD Y-Axis", 0)
    idc.set_name(0x6C70B9, "ui_6C70B9", idaapi.SN_NOWARN)
    # 6C70BE: item screen take evrything WORD X-Axis
    idc.set_cmt(0x6C70BE, "[UI] item screen take evrything WORD X-Axis", 0)
    idc.set_name(0x6C70BE, "ui_6C70BE", idaapi.SN_NOWARN)
    # 6C70DE: right box item screen item WORD Y-Axis
    idc.set_cmt(0x6C70DE, "[UI] right box item screen item WORD Y-Axis", 0)
    idc.set_name(0x6C70DE, "ui_6C70DE", idaapi.SN_NOWARN)
    # 6C70E3: right box item screen item WORD X-Axis
    idc.set_cmt(0x6C70E3, "[UI] right box item screen item WORD X-Axis", 0)
    idc.set_name(0x6C70E3, "ui_6C70E3", idaapi.SN_NOWARN)
    # 6C710B: item screen exit WORD X-Axis
    idc.set_cmt(0x6C710B, "[UI] item screen exit WORD X-Axis", 0)
    idc.set_name(0x6C710B, "ui_6C710B", idaapi.SN_NOWARN)
    # 6C718D: post battle - left box item name spacing Y-Axis
    idc.set_cmt(0x6C718D, "[UI] post battle - left box item name spacing Y-Axis", 0)
    idc.set_name(0x6C718D, "ui_6C718D", idaapi.SN_NOWARN)
    # 6C718F: left box item name Y-Axis
    idc.set_cmt(0x6C718F, "[UI] left box item name Y-Axis", 0)
    idc.set_name(0x6C718F, "ui_6C718F", idaapi.SN_NOWARN)
    # 6C7195: left box item name X-Axis
    idc.set_cmt(0x6C7195, "[UI] left box item name X-Axis", 0)
    idc.set_name(0x6C7195, "ui_6C7195", idaapi.SN_NOWARN)
    # 6C71DB: post battle - right box item screen name spacing Y
    idc.set_cmt(0x6C71DB, "[UI] post battle - right box item screen name spacing Y-Axis", 0)
    idc.set_name(0x6C71DB, "ui_6C71DB", idaapi.SN_NOWARN)
    # 6C71DE: right box item screen name Y-Axis
    idc.set_cmt(0x6C71DE, "[UI] right box item screen name Y-Axis", 0)
    idc.set_name(0x6C71DE, "ui_6C71DE", idaapi.SN_NOWARN)
    # 6C71E4: right box item screen name X-Axis
    idc.set_cmt(0x6C71E4, "[UI] right box item screen name X-Axis", 0)
    idc.set_name(0x6C71E4, "ui_6C71E4", idaapi.SN_NOWARN)
    # 6C720E: gained gil items found Y-Axis
    idc.set_cmt(0x6C720E, "[UI] gained gil items found Y-Axis", 0)
    idc.set_name(0x6C720E, "ui_6C720E", idaapi.SN_NOWARN)
    # 6C7210: gained gil items found X-Axis
    idc.set_cmt(0x6C7210, "[UI] gained gil items found X-Axis", 0)
    idc.set_name(0x6C7210, "ui_6C7210", idaapi.SN_NOWARN)
    # 6C7230: left box no items Y-Axis
    idc.set_cmt(0x6C7230, "[UI] left box no items Y-Axis", 0)
    idc.set_name(0x6C7230, "ui_6C7230", idaapi.SN_NOWARN)
    # 6C7235: left box no items X-Axis
    idc.set_cmt(0x6C7235, "[UI] left box no items X-Axis", 0)
    idc.set_name(0x6C7235, "ui_6C7235", idaapi.SN_NOWARN)
    # 6C7C94: top left box 'p' Y-Axis
    idc.set_cmt(0x6C7C94, "[UI] top left box 'p' Y-Axis", 0)
    idc.set_name(0x6C7C94, "ui_6C7C94", idaapi.SN_NOWARN)
    # 6C7C9B: top left box 'p' X-Axis
    idc.set_cmt(0x6C7C9B, "[UI] top left box 'p' X-Axis", 0)
    idc.set_name(0x6C7C9B, "ui_6C7C9B", idaapi.SN_NOWARN)
    # 6C7CBD: top box exp value Y-Axis
    idc.set_cmt(0x6C7CBD, "[UI] top box exp value Y-Axis", 0)
    idc.set_name(0x6C7CBD, "ui_6C7CBD", idaapi.SN_NOWARN)
    # 6C7CC4: top box exp value X-Axis
    idc.set_cmt(0x6C7CC4, "[UI] top box exp value X-Axis", 0)
    idc.set_name(0x6C7CC4, "ui_6C7CC4", idaapi.SN_NOWARN)
    # 6C7CEC: top right box 'p' Y-Axis
    idc.set_cmt(0x6C7CEC, "[UI] top right box 'p' Y-Axis", 0)
    idc.set_name(0x6C7CEC, "ui_6C7CEC", idaapi.SN_NOWARN)
    # 6C7CF2: top right box 'p' X-Axis
    idc.set_cmt(0x6C7CF2, "[UI] top right box 'p' X-Axis", 0)
    idc.set_name(0x6C7CF2, "ui_6C7CF2", idaapi.SN_NOWARN)
    # 6C7D14: top box ap value Y-Axis
    idc.set_cmt(0x6C7D14, "[UI] top box ap value Y-Axis", 0)
    idc.set_name(0x6C7D14, "ui_6C7D14", idaapi.SN_NOWARN)
    # 6C7D1A: top box ap value X-Axis
    idc.set_cmt(0x6C7D1A, "[UI] top box ap value X-Axis", 0)
    idc.set_name(0x6C7D1A, "ui_6C7D1A", idaapi.SN_NOWARN)
    # 6C7D42: gained exp/ap Y-Axis
    idc.set_cmt(0x6C7D42, "[UI] gained exp/ap Y-Axis", 0)
    idc.set_name(0x6C7D42, "ui_6C7D42", idaapi.SN_NOWARN)
    # 6C7D49: gained exp/ap X-Axis
    idc.set_cmt(0x6C7D49, "[UI] gained exp/ap X-Axis", 0)
    idc.set_name(0x6C7D49, "ui_6C7D49", idaapi.SN_NOWARN)
    # 6C82A9: bottom boxes EXP WORD Y-Axis
    idc.set_cmt(0x6C82A9, "[UI] bottom boxes EXP WORD Y-Axis", 0)
    idc.set_name(0x6C82A9, "ui_6C82A9", idaapi.SN_NOWARN)
    # 6C82AC: bottom boxes  EXP WORD X-Axis
    idc.set_cmt(0x6C82AC, "[UI] bottom boxes  EXP WORD X-Axis", 0)
    idc.set_name(0x6C82AC, "ui_6C82AC", idaapi.SN_NOWARN)
    # 6C82D9: Level WORD X-Axis
    idc.set_cmt(0x6C82D9, "[UI] Level WORD X-Axis", 0)
    idc.set_name(0x6C82D9, "ui_6C82D9", idaapi.SN_NOWARN)
    # 6C8303: next level WORD Y-Axis
    idc.set_cmt(0x6C8303, "[UI] next level WORD Y-Axis", 0)
    idc.set_name(0x6C8303, "ui_6C8303", idaapi.SN_NOWARN)
    # 6C8306: next level WORD X-Axis
    idc.set_cmt(0x6C8306, "[UI] next level WORD X-Axis", 0)
    idc.set_name(0x6C8306, "ui_6C8306", idaapi.SN_NOWARN)
    # 6C834E: exp bar height
    idc.set_cmt(0x6C834E, "[UI] exp bar height", 0)
    idc.set_name(0x6C834E, "ui_6C834E", idaapi.SN_NOWARN)
    # 6C8358: exp bar width
    idc.set_cmt(0x6C8358, "[UI] exp bar width", 0)
    idc.set_name(0x6C8358, "ui_6C8358", idaapi.SN_NOWARN)
    # 6C8367: exp bar Y-Axis
    idc.set_cmt(0x6C8367, "[UI] exp bar Y-Axis", 0)
    idc.set_name(0x6C8367, "ui_6C8367", idaapi.SN_NOWARN)
    # 6C836A: exp bar X-Axis
    idc.set_cmt(0x6C836A, "[UI] exp bar X-Axis", 0)
    idc.set_name(0x6C836A, "ui_6C836A", idaapi.SN_NOWARN)
    # 6C8392: exp box Y-Axis
    idc.set_cmt(0x6C8392, "[UI] exp box Y-Axis", 0)
    idc.set_name(0x6C8392, "ui_6C8392", idaapi.SN_NOWARN)
    # 6C8395: exp box X-Axis
    idc.set_cmt(0x6C8395, "[UI] exp box X-Axis", 0)
    idc.set_name(0x6C8395, "ui_6C8395", idaapi.SN_NOWARN)
    # 6C83C0: bottom boxes top 'p' Y-Axis
    idc.set_cmt(0x6C83C0, "[UI] bottom boxes top 'p' Y-Axis", 0)
    idc.set_name(0x6C83C0, "ui_6C83C0", idaapi.SN_NOWARN)
    # 6C83C3: bottom boxes top 'p' X-Axis
    idc.set_cmt(0x6C83C3, "[UI] bottom boxes top 'p' X-Axis", 0)
    idc.set_name(0x6C83C3, "ui_6C83C3", idaapi.SN_NOWARN)
    # 6C83EE: bottom boxes bottom 'p' Y-Axis
    idc.set_cmt(0x6C83EE, "[UI] bottom boxes bottom 'p' Y-Axis", 0)
    idc.set_name(0x6C83EE, "ui_6C83EE", idaapi.SN_NOWARN)
    # 6C83F1: bottom boxes bottom 'p' X-Axis
    idc.set_cmt(0x6C83F1, "[UI] bottom boxes bottom 'p' X-Axis", 0)
    idc.set_name(0x6C83F1, "ui_6C83F1", idaapi.SN_NOWARN)
    # 6C841C: bottom boxes exp value Y-Axis
    idc.set_cmt(0x6C841C, "[UI] bottom boxes exp value Y-Axis", 0)
    idc.set_name(0x6C841C, "ui_6C841C", idaapi.SN_NOWARN)
    # 6C841F: bottom boxes exp value X-Axis
    idc.set_cmt(0x6C841F, "[UI] bottom boxes exp value X-Axis", 0)
    idc.set_name(0x6C841F, "ui_6C841F", idaapi.SN_NOWARN)
    # 6C844A: bottom boxes next level value Y-Axis
    idc.set_cmt(0x6C844A, "[UI] bottom boxes next level value Y-Axis", 0)
    idc.set_name(0x6C844A, "ui_6C844A", idaapi.SN_NOWARN)
    # 6C844D: bottom boxes next level value X-Axis
    idc.set_cmt(0x6C844D, "[UI] bottom boxes next level value X-Axis", 0)
    idc.set_name(0x6C844D, "ui_6C844D", idaapi.SN_NOWARN)
    # 6C847A: bottom boxes level value Y-Axis
    idc.set_cmt(0x6C847A, "[UI] bottom boxes level value Y-Axis", 0)
    idc.set_name(0x6C847A, "ui_6C847A", idaapi.SN_NOWARN)
    # 6C847D: bottom boxes level value X-Axis
    idc.set_cmt(0x6C847D, "[UI] bottom boxes level value X-Axis", 0)
    idc.set_name(0x6C847D, "ui_6C847D", idaapi.SN_NOWARN)
    # 6C8499: avatars Y-Axis
    idc.set_cmt(0x6C8499, "[UI] avatars Y-Axis", 0)
    idc.set_name(0x6C8499, "ui_6C8499", idaapi.SN_NOWARN)
    # 6C8605: level up text Y-Axis 0B
    idc.set_cmt(0x6C8605, "[UI] level up text Y-Axis 0B", 0)
    idc.set_name(0x6C8605, "ui_6C8605", idaapi.SN_NOWARN)
    # 6C860C: level up text X-Axis 0D
    idc.set_cmt(0x6C860C, "[UI] level up text X-Axis 0D", 0)
    idc.set_name(0x6C860C, "ui_6C860C", idaapi.SN_NOWARN)
    # 6C87DB: gained text
    idc.set_cmt(0x6C87DB, "[UI] gained text", 0)
    idc.set_name(0x6C87DB, "ui_6C87DB", idaapi.SN_NOWARN)
    # 6C98AF: Box Y-axis
    idc.set_cmt(0x6C98AF, "[UI] Box Y-axis", 0)
    idc.set_name(0x6C98AF, "ui_6C98AF", idaapi.SN_NOWARN)
    # 6C9A8A: Box height
    idc.set_cmt(0x6C9A8A, "[UI] Box height", 0)
    idc.set_name(0x6C9A8A, "ui_6C9A8A", idaapi.SN_NOWARN)
    # 6C9B3B: Text spacing
    idc.set_cmt(0x6C9B3B, "[UI] Text spacing", 0)
    idc.set_name(0x6C9B3B, "ui_6C9B3B", idaapi.SN_NOWARN)
    # 6C9B42: Text Y-axis
    idc.set_cmt(0x6C9B42, "[UI] Text Y-axis", 0)
    idc.set_name(0x6C9B42, "ui_6C9B42", idaapi.SN_NOWARN)
    # 6C9B45: Text X-axis
    idc.set_cmt(0x6C9B45, "[UI] Text X-axis", 0)
    idc.set_name(0x6C9B45, "ui_6C9B45", idaapi.SN_NOWARN)
    # 6C9C7F: Box width
    idc.set_cmt(0x6C9C7F, "[UI] Box width", 0)
    idc.set_name(0x6C9C7F, "ui_6C9C7F", idaapi.SN_NOWARN)
    # 6C9C88: Box X-axis
    idc.set_cmt(0x6C9C88, "[UI] Box X-axis", 0)
    idc.set_name(0x6C9C88, "ui_6C9C88", idaapi.SN_NOWARN)
    # 6CA1F6: extend time to 999hr on counters, but main menu ne
    idc.set_cmt(0x6CA1F6, "[UI] extend time to 999hr on counters, but main menu needs another hext to get it to display", 0)
    idc.set_name(0x6CA1F6, "ui_6CA1F6", idaapi.SN_NOWARN)
    # 6CA88D: Cursor spacing Y-Axis
    idc.set_cmt(0x6CA88D, "[UI] Cursor spacing Y-Axis", 0)
    idc.set_name(0x6CA88D, "ui_6CA88D", idaapi.SN_NOWARN)
    # 6CA890: Cursor Y-axis
    idc.set_cmt(0x6CA890, "[UI] Cursor Y-axis", 0)
    idc.set_name(0x6CA890, "ui_6CA890", idaapi.SN_NOWARN)
    # 6CA893: Cursor X-axis
    idc.set_cmt(0x6CA893, "[UI] Cursor X-axis", 0)
    idc.set_name(0x6CA893, "ui_6CA893", idaapi.SN_NOWARN)
    # 6CA8C5: order ghost cursor Y-Axis - alternative value 53
    idc.set_cmt(0x6CA8C5, "[UI] order ghost cursor Y-Axis - alternative value 53", 0)
    idc.set_name(0x6CA8C5, "ui_6CA8C5", idaapi.SN_NOWARN)
    # 6CA8C8: order ghost cursor X-Axis
    idc.set_cmt(0x6CA8C8, "[UI] order ghost cursor X-Axis", 0)
    idc.set_name(0x6CA8C8, "ui_6CA8C8", idaapi.SN_NOWARN)
    # 6CA8E8: Cursor select spacing
    idc.set_cmt(0x6CA8E8, "[UI] Cursor select spacing", 0)
    idc.set_name(0x6CA8E8, "ui_6CA8E8", idaapi.SN_NOWARN)
    # 6CA8EB: ghost cursor Y-axis
    idc.set_cmt(0x6CA8EB, "[UI] ghost cursor Y-axis", 0)
    idc.set_name(0x6CA8EB, "ui_6CA8EB", idaapi.SN_NOWARN)
    # 6CA8EE: ghost cursor X-axis
    idc.set_cmt(0x6CA8EE, "[UI] ghost cursor X-axis", 0)
    idc.set_name(0x6CA8EE, "ui_6CA8EE", idaapi.SN_NOWARN)
    # 6CA932: area box X-Axis
    idc.set_cmt(0x6CA932, "[UI] area box X-Axis", 0)
    idc.set_name(0x6CA932, "ui_6CA932", idaapi.SN_NOWARN)
    # 6CA954: area box Y-Axis
    idc.set_cmt(0x6CA954, "[UI] area box Y-Axis", 0)
    idc.set_name(0x6CA954, "ui_6CA954", idaapi.SN_NOWARN)
    # 6CA96C: area box text Y-Axis
    idc.set_cmt(0x6CA96C, "[UI] area box text Y-Axis", 0)
    idc.set_name(0x6CA96C, "ui_6CA96C", idaapi.SN_NOWARN)
    # 6CA973: area box text X-Axis
    idc.set_cmt(0x6CA973, "[UI] area box text X-Axis", 0)
    idc.set_name(0x6CA973, "ui_6CA973", idaapi.SN_NOWARN)
    # 6CA97E: area box height
    idc.set_cmt(0x6CA97E, "[UI] area box height", 0)
    idc.set_name(0x6CA97E, "ui_6CA97E", idaapi.SN_NOWARN)
    # 6CA980: area box width
    idc.set_cmt(0x6CA980, "[UI] area box width", 0)
    idc.set_name(0x6CA980, "ui_6CA980", idaapi.SN_NOWARN)
    # 6CA9BF: time/gil box X-Axis
    idc.set_cmt(0x6CA9BF, "[UI] time/gil box X-Axis", 0)
    idc.set_name(0x6CA9BF, "ui_6CA9BF", idaapi.SN_NOWARN)
    # 6CA9CB: time/gil box Y-Axis
    idc.set_cmt(0x6CA9CB, "[UI] time/gil box Y-Axis", 0)
    idc.set_name(0x6CA9CB, "ui_6CA9CB", idaapi.SN_NOWARN)
    # 6CA9D7: Time hour X-Axis digit capacity
    idc.set_cmt(0x6CA9D7, "[UI] Time hour X-Axis digit capacity", 0)
    idc.set_name(0x6CA9D7, "ui_6CA9D7", idaapi.SN_NOWARN)
    # 6CA9EC: Time hour Y-Axis
    idc.set_cmt(0x6CA9EC, "[UI] Time hour Y-Axis", 0)
    idc.set_name(0x6CA9EC, "ui_6CA9EC", idaapi.SN_NOWARN)
    # 6CA9F3: Time hour X-Axis
    idc.set_cmt(0x6CA9F3, "[UI] Time hour X-Axis", 0)
    idc.set_name(0x6CA9F3, "ui_6CA9F3", idaapi.SN_NOWARN)
    # 6CAA02: disable flashing on first colon, only on seconds, 
    idc.set_cmt(0x6CAA02, "[UI] disable flashing on first colon, only on seconds, address to change colon color is 6CAA11", 0)
    idc.set_name(0x6CAA02, "ui_6CAA02", idaapi.SN_NOWARN)
    # 6CAA1C: Time hours colon Y-Axis
    idc.set_cmt(0x6CAA1C, "[UI] Time hours colon Y-Axis", 0)
    idc.set_name(0x6CAA1C, "ui_6CAA1C", idaapi.SN_NOWARN)
    # 6CAA23: Time minutes colon X-Axis
    idc.set_cmt(0x6CAA23, "[UI] Time minutes colon X-Axis", 0)
    idc.set_name(0x6CAA23, "ui_6CAA23", idaapi.SN_NOWARN)
    # 6CAA4A: Time minutes Y-Axis
    idc.set_cmt(0x6CAA4A, "[UI] Time minutes Y-Axis", 0)
    idc.set_name(0x6CAA4A, "ui_6CAA4A", idaapi.SN_NOWARN)
    # 6CAA51: Time minutes X-Axis
    idc.set_cmt(0x6CAA51, "[UI] Time minutes X-Axis", 0)
    idc.set_name(0x6CAA51, "ui_6CAA51", idaapi.SN_NOWARN)
    # 6CAA6C: Time minutes colon Y-Axis
    idc.set_cmt(0x6CAA6C, "[UI] Time minutes colon Y-Axis", 0)
    idc.set_name(0x6CAA6C, "ui_6CAA6C", idaapi.SN_NOWARN)
    # 6CAA73: Time hour colon X-Axis
    idc.set_cmt(0x6CAA73, "[UI] Time hour colon X-Axis", 0)
    idc.set_name(0x6CAA73, "ui_6CAA73", idaapi.SN_NOWARN)
    # 6CAA9B: Time seconds Y-Axis
    idc.set_cmt(0x6CAA9B, "[UI] Time seconds Y-Axis", 0)
    idc.set_name(0x6CAA9B, "ui_6CAA9B", idaapi.SN_NOWARN)
    # 6CAAA2: Time seconds X-Axis
    idc.set_cmt(0x6CAAA2, "[UI] Time seconds X-Axis", 0)
    idc.set_name(0x6CAAA2, "ui_6CAAA2", idaapi.SN_NOWARN)
    # 6CAAC0: Time word Y-Axis
    idc.set_cmt(0x6CAAC0, "[UI] Time word Y-Axis", 0)
    idc.set_name(0x6CAAC0, "ui_6CAAC0", idaapi.SN_NOWARN)
    # 6CAAC7: Time word X-axis
    idc.set_cmt(0x6CAAC7, "[UI] Time word X-axis", 0)
    idc.set_name(0x6CAAC7, "ui_6CAAC7", idaapi.SN_NOWARN)
    # 6CAAE6: Gil amount Y-Axis
    idc.set_cmt(0x6CAAE6, "[UI] Gil amount Y-Axis", 0)
    idc.set_name(0x6CAAE6, "ui_6CAAE6", idaapi.SN_NOWARN)
    # 6CAAED: Gil amount X-axis
    idc.set_cmt(0x6CAAED, "[UI] Gil amount X-axis", 0)
    idc.set_name(0x6CAAED, "ui_6CAAED", idaapi.SN_NOWARN)
    # 6CAB08: Gil word Y-Axis
    idc.set_cmt(0x6CAB08, "[UI] Gil word Y-Axis", 0)
    idc.set_name(0x6CAB08, "ui_6CAB08", idaapi.SN_NOWARN)
    # 6CAB0F: Gil word X-axis
    idc.set_cmt(0x6CAB0F, "[UI] Gil word X-axis", 0)
    idc.set_name(0x6CAB0F, "ui_6CAB0F", idaapi.SN_NOWARN)
    # 6CAB1A: Time/Gil box height
    idc.set_cmt(0x6CAB1A, "[UI] Time/Gil box height", 0)
    idc.set_name(0x6CAB1A, "ui_6CAB1A", idaapi.SN_NOWARN)
    # 6CAB1C: Time/Gil box width
    idc.set_cmt(0x6CAB1C, "[UI] Time/Gil box width", 0)
    idc.set_name(0x6CAB1C, "ui_6CAB1C", idaapi.SN_NOWARN)
    # 6CAB27: Time/Gil box X-axis
    idc.set_cmt(0x6CAB27, "[UI] Time/Gil box X-axis", 0)
    idc.set_name(0x6CAB27, "ui_6CAB27", idaapi.SN_NOWARN)
    # 6CAC16: avatar Y
    idc.set_cmt(0x6CAC16, "[UI] avatar Y", 0)
    idc.set_name(0x6CAC16, "ui_6CAC16", idaapi.SN_NOWARN)
    # 6CAC20: avatar X
    idc.set_cmt(0x6CAC20, "[UI] avatar X", 0)
    idc.set_name(0x6CAC20, "ui_6CAC20", idaapi.SN_NOWARN)
    # 6CAC39: Next Level width main
    idc.set_cmt(0x6CAC39, "[UI] Next Level width main", 0)
    idc.set_name(0x6CAC39, "ui_6CAC39", idaapi.SN_NOWARN)
    # 6CAC5B: exp bar Y-Axis
    idc.set_cmt(0x6CAC5B, "[UI] exp bar Y-Axis", 0)
    idc.set_name(0x6CAC5B, "ui_6CAC5B", idaapi.SN_NOWARN)
    # 6CAC62: Bar color X-axis
    idc.set_cmt(0x6CAC62, "[UI] Bar color X-axis", 0)
    idc.set_name(0x6CAC62, "ui_6CAC62", idaapi.SN_NOWARN)
    # 6CAD4C: limit bar Y-Axis
    idc.set_cmt(0x6CAD4C, "[UI] limit bar Y-Axis", 0)
    idc.set_name(0x6CAD4C, "ui_6CAD4C", idaapi.SN_NOWARN)
    # 6CAD53: Bar color flash X-axis
    idc.set_cmt(0x6CAD53, "[UI] Bar color flash X-axis", 0)
    idc.set_name(0x6CAD53, "ui_6CAD53", idaapi.SN_NOWARN)
    # 6CAD7B: exp box Y-Axis
    idc.set_cmt(0x6CAD7B, "[UI] exp box Y-Axis", 0)
    idc.set_name(0x6CAD7B, "ui_6CAD7B", idaapi.SN_NOWARN)
    # 6CAD81: Bar border X-axis
    idc.set_cmt(0x6CAD81, "[UI] Bar border X-axis", 0)
    idc.set_name(0x6CAD81, "ui_6CAD81", idaapi.SN_NOWARN)
    # 6CADA9: limit box Y-Axis
    idc.set_cmt(0x6CADA9, "[UI] limit box Y-Axis", 0)
    idc.set_name(0x6CADA9, "ui_6CADA9", idaapi.SN_NOWARN)
    # 6CADCE: next level text Y-Axis
    idc.set_cmt(0x6CADCE, "[UI] next level text Y-Axis", 0)
    idc.set_name(0x6CADCE, "ui_6CADCE", idaapi.SN_NOWARN)
    # 6CADD5: next level text X-Axis
    idc.set_cmt(0x6CADD5, "[UI] next level text X-Axis", 0)
    idc.set_name(0x6CADD5, "ui_6CADD5", idaapi.SN_NOWARN)
    # 6CADF3: limit level text Y-Axis
    idc.set_cmt(0x6CADF3, "[UI] limit level text Y-Axis", 0)
    idc.set_name(0x6CADF3, "ui_6CADF3", idaapi.SN_NOWARN)
    # 6CADF9: limit level text X-Axis
    idc.set_cmt(0x6CADF9, "[UI] limit level text X-Axis", 0)
    idc.set_name(0x6CADF9, "ui_6CADF9", idaapi.SN_NOWARN)
    # 6CAE35: limit level value Y-Axis
    idc.set_cmt(0x6CAE35, "[UI] limit level value Y-Axis", 0)
    idc.set_name(0x6CAE35, "ui_6CAE35", idaapi.SN_NOWARN)
    # 6CAE3B: limit level value X-Axis
    idc.set_cmt(0x6CAE3B, "[UI] limit level value X-Axis", 0)
    idc.set_name(0x6CAE3B, "ui_6CAE3B", idaapi.SN_NOWARN)
    # 6CC474: fastest text speed default
    idc.set_cmt(0x6CC474, "[UI] fastest text speed default", 0)
    idc.set_name(0x6CC474, "ui_6CC474", idaapi.SN_NOWARN)
    # 6CDF19: control text pallete color
    idc.set_cmt(0x6CDF19, "[UI] control text pallete color", 0)
    idc.set_name(0x6CDF19, "ui_6CDF19", idaapi.SN_NOWARN)
    # 6CDF2F: control text spacing Y-Axis
    idc.set_cmt(0x6CDF2F, "[UI] control text spacing Y-Axis", 0)
    idc.set_name(0x6CDF2F, "ui_6CDF2F", idaapi.SN_NOWARN)
    # 6CE015: controller select bg box X-Axis
    idc.set_cmt(0x6CE015, "[UI] controller select bg box X-Axis", 0)
    idc.set_name(0x6CE015, "ui_6CE015", idaapi.SN_NOWARN)
    # 6CE01F: controller select bg box spacing Y-Axis
    idc.set_cmt(0x6CE01F, "[UI] controller select bg box spacing Y-Axis", 0)
    idc.set_name(0x6CE01F, "ui_6CE01F", idaapi.SN_NOWARN)
    # 6CE022: controller select bg box Y-Axis
    idc.set_cmt(0x6CE022, "[UI] controller select bg box Y-Axis", 0)
    idc.set_name(0x6CE022, "ui_6CE022", idaapi.SN_NOWARN)
    # 6CE02C: controller select bg box width
    idc.set_cmt(0x6CE02C, "[UI] controller select bg box width", 0)
    idc.set_name(0x6CE02C, "ui_6CE02C", idaapi.SN_NOWARN)
    # 6CE035: controller select bg box height
    idc.set_cmt(0x6CE035, "[UI] controller select bg box height", 0)
    idc.set_name(0x6CE035, "ui_6CE035", idaapi.SN_NOWARN)
    # 6CE058: button/keys spacing Y-Axis
    idc.set_cmt(0x6CE058, "[UI] button/keys spacing Y-Axis", 0)
    idc.set_name(0x6CE058, "ui_6CE058", idaapi.SN_NOWARN)
    # 6CE090: button/keys cursor spacing Y-Axis
    idc.set_cmt(0x6CE090, "[UI] button/keys cursor spacing Y-Axis", 0)
    idc.set_name(0x6CE090, "ui_6CE090", idaapi.SN_NOWARN)
    # 6CE093: button/keys cursor Y-Axis
    idc.set_cmt(0x6CE093, "[UI] button/keys cursor Y-Axis", 0)
    idc.set_name(0x6CE093, "ui_6CE093", idaapi.SN_NOWARN)
    # 6CF756: hide command box depending on sub-menu
    idc.set_cmt(0x6CF756, "[UI] hide command box depending on sub-menu", 0)
    idc.set_name(0x6CF756, "ui_6CF756", idaapi.SN_NOWARN)
    # 6CF79C: command box cursor spacing X-Axis
    idc.set_cmt(0x6CF79C, "[UI] command box cursor spacing X-Axis", 0)
    idc.set_name(0x6CF79C, "ui_6CF79C", idaapi.SN_NOWARN)
    # 6CF7BC: command box cursor X-Axis
    idc.set_cmt(0x6CF7BC, "[UI] command box cursor X-Axis", 0)
    idc.set_name(0x6CF7BC, "ui_6CF7BC", idaapi.SN_NOWARN)
    # 6CF7BD: command box cursor X-Axis
    idc.set_cmt(0x6CF7BD, "[UI] command box cursor X-Axis", 0)
    idc.set_name(0x6CF7BD, "ui_6CF7BD", idaapi.SN_NOWARN)
    # 6CF7E8: command box cursor spacing Y-Axis
    idc.set_cmt(0x6CF7E8, "[UI] command box cursor spacing Y-Axis", 0)
    idc.set_name(0x6CF7E8, "ui_6CF7E8", idaapi.SN_NOWARN)
    # 6CF7EC: command box cursor Y-Axis
    idc.set_cmt(0x6CF7EC, "[UI] command box cursor Y-Axis", 0)
    idc.set_name(0x6CF7EC, "ui_6CF7EC", idaapi.SN_NOWARN)
    # 6CF823: limit box cursor X-Axis
    idc.set_cmt(0x6CF823, "[UI] limit box cursor X-Axis", 0)
    idc.set_name(0x6CF823, "ui_6CF823", idaapi.SN_NOWARN)
    # 6CF84E: limit box cursor spacing Y-Axis
    idc.set_cmt(0x6CF84E, "[UI] limit box cursor spacing Y-Axis", 0)
    idc.set_name(0x6CF84E, "ui_6CF84E", idaapi.SN_NOWARN)
    # 6CF852: limit box cursor Y-Axis
    idc.set_cmt(0x6CF852, "[UI] limit box cursor Y-Axis", 0)
    idc.set_name(0x6CF852, "ui_6CF852", idaapi.SN_NOWARN)
    # 6CF877: defend/change cursor X-Axis
    idc.set_cmt(0x6CF877, "[UI] defend/change cursor X-Axis", 0)
    idc.set_name(0x6CF877, "ui_6CF877", idaapi.SN_NOWARN)
    # 6CF898: defend/change cursor Y-Axis
    idc.set_cmt(0x6CF898, "[UI] defend/change cursor Y-Axis", 0)
    idc.set_name(0x6CF898, "ui_6CF898", idaapi.SN_NOWARN)
    # 6CF8BD: item sub menu cursor X-Axis
    idc.set_cmt(0x6CF8BD, "[UI] item sub menu cursor X-Axis", 0)
    idc.set_name(0x6CF8BD, "ui_6CF8BD", idaapi.SN_NOWARN)
    # 6CF8D3: item sub menu cursor spacing Y-Axis
    idc.set_cmt(0x6CF8D3, "[UI] item sub menu cursor spacing Y-Axis", 0)
    idc.set_name(0x6CF8D3, "ui_6CF8D3", idaapi.SN_NOWARN)
    # 6CF8D7: item sub menu cursor Y-Axis
    idc.set_cmt(0x6CF8D7, "[UI] item sub menu cursor Y-Axis", 0)
    idc.set_name(0x6CF8D7, "ui_6CF8D7", idaapi.SN_NOWARN)
    # 6CF90E: magic sub menu cursor spacing X-Axis
    idc.set_cmt(0x6CF90E, "[UI] magic sub menu cursor spacing X-Axis", 0)
    idc.set_name(0x6CF90E, "ui_6CF90E", idaapi.SN_NOWARN)
    # 6CF914: magic sub menu cursor X-Axis
    idc.set_cmt(0x6CF914, "[UI] magic sub menu cursor X-Axis", 0)
    idc.set_name(0x6CF914, "ui_6CF914", idaapi.SN_NOWARN)
    # 6CF92F: magic sub menu cursor spacing Y-Axis
    idc.set_cmt(0x6CF92F, "[UI] magic sub menu cursor spacing Y-Axis", 0)
    idc.set_name(0x6CF92F, "ui_6CF92F", idaapi.SN_NOWARN)
    # 6CF934: magic sub menu cursor Y-Axis
    idc.set_cmt(0x6CF934, "[UI] magic sub menu cursor Y-Axis", 0)
    idc.set_name(0x6CF934, "ui_6CF934", idaapi.SN_NOWARN)
    # 6CF95C: summon sub menu cursor X-Axis
    idc.set_cmt(0x6CF95C, "[UI] summon sub menu cursor X-Axis", 0)
    idc.set_name(0x6CF95C, "ui_6CF95C", idaapi.SN_NOWARN)
    # 6CF972: summon sub menu cursor spacing Y-Axis
    idc.set_cmt(0x6CF972, "[UI] summon sub menu cursor spacing Y-Axis", 0)
    idc.set_name(0x6CF972, "ui_6CF972", idaapi.SN_NOWARN)
    # 6CF977: summon sub menu cursor Y-Axis
    idc.set_cmt(0x6CF977, "[UI] summon sub menu cursor Y-Axis", 0)
    idc.set_name(0x6CF977, "ui_6CF977", idaapi.SN_NOWARN)
    # 6CF9AC: eskill sub menu cursor X-Axis, 3rd value for spaci
    idc.set_cmt(0x6CF9AC, "[UI] eskill sub menu cursor X-Axis, 3rd value for spacing, 9th for X-Axis offset", 0)
    idc.set_name(0x6CF9AC, "ui_6CF9AC", idaapi.SN_NOWARN)
    # 6CF9B4: eskill menu cursor X-Axis
    idc.set_cmt(0x6CF9B4, "[UI] eskill menu cursor X-Axis", 0)
    idc.set_name(0x6CF9B4, "ui_6CF9B4", idaapi.SN_NOWARN)
    # 6CF9D0: eskill sub menu cursor spacing Y-Axis
    idc.set_cmt(0x6CF9D0, "[UI] eskill sub menu cursor spacing Y-Axis", 0)
    idc.set_name(0x6CF9D0, "ui_6CF9D0", idaapi.SN_NOWARN)
    # 6CF9D5: eskill sub menu cursor Y-Axis
    idc.set_cmt(0x6CF9D5, "[UI] eskill sub menu cursor Y-Axis", 0)
    idc.set_name(0x6CF9D5, "ui_6CF9D5", idaapi.SN_NOWARN)
    # 6CFA05: coin cursor X-Axis
    idc.set_cmt(0x6CFA05, "[UI] coin cursor X-Axis", 0)
    idc.set_name(0x6CFA05, "ui_6CFA05", idaapi.SN_NOWARN)
    # 6CFA34: coin cursor Y-Axis
    idc.set_cmt(0x6CFA34, "[UI] coin cursor Y-Axis", 0)
    idc.set_name(0x6CFA34, "ui_6CFA34", idaapi.SN_NOWARN)
    # 6CFA61: manip cursor X-Axis
    idc.set_cmt(0x6CFA61, "[UI] manip cursor X-Axis", 0)
    idc.set_name(0x6CFA61, "ui_6CFA61", idaapi.SN_NOWARN)
    # 6CFA7A: manip cursor spacing Y-Axis
    idc.set_cmt(0x6CFA7A, "[UI] manip cursor spacing Y-Axis", 0)
    idc.set_name(0x6CFA7A, "ui_6CFA7A", idaapi.SN_NOWARN)
    # 6CFABE: battle square cursor spacing X-Axis
    idc.set_cmt(0x6CFABE, "[UI] battle square cursor spacing X-Axis", 0)
    idc.set_name(0x6CFABE, "ui_6CFABE", idaapi.SN_NOWARN)
    # 6CFAC5: battle square cursor X-Axis
    idc.set_cmt(0x6CFAC5, "[UI] battle square cursor X-Axis", 0)
    idc.set_name(0x6CFAC5, "ui_6CFAC5", idaapi.SN_NOWARN)
    # 6CFADC: battle square cursor Y-Axis
    idc.set_cmt(0x6CFADC, "[UI] battle square cursor Y-Axis", 0)
    idc.set_name(0x6CFADC, "ui_6CFADC", idaapi.SN_NOWARN)
    # 6D0B2D: defend change boxes
    idc.set_cmt(0x6D0B2D, "[UI] defend change boxes", 0)
    idc.set_name(0x6D0B2D, "ui_6D0B2D", idaapi.SN_NOWARN)
    # 6D0B45: prevent defend/change box Y-Axis revert
    idc.set_cmt(0x6D0B45, "[UI] prevent defend/change box Y-Axis revert", 0)
    idc.set_name(0x6D0B45, "ui_6D0B45", idaapi.SN_NOWARN)
    # 6D21A2: battle autosize and position help/attack
    idc.set_cmt(0x6D21A2, "[UI] battle autosize and position help/attack", 0)
    idc.set_name(0x6D21A2, "ui_6D21A2", idaapi.SN_NOWARN)
    # 6D7527: magic column count descriptions
    idc.set_cmt(0x6D7527, "[UI] magic column count descriptions", 0)
    idc.set_name(0x6D7527, "ui_6D7527", idaapi.SN_NOWARN)
    # 6D7581: magic column count cursor first column
    idc.set_cmt(0x6D7581, "[UI] magic column count cursor first column", 0)
    idc.set_name(0x6D7581, "ui_6D7581", idaapi.SN_NOWARN)
    # 6D7A63: change Y-Axis
    idc.set_cmt(0x6D7A63, "[UI] change Y-Axis", 0)
    idc.set_name(0x6D7A63, "ui_6D7A63", idaapi.SN_NOWARN)
    # 6D7A8F: change X-Axis
    idc.set_cmt(0x6D7A8F, "[UI] change X-Axis", 0)
    idc.set_name(0x6D7A8F, "ui_6D7A8F", idaapi.SN_NOWARN)
    # 6D7AE1: defend Y-Axis
    idc.set_cmt(0x6D7AE1, "[UI] defend Y-Axis", 0)
    idc.set_name(0x6D7AE1, "ui_6D7AE1", idaapi.SN_NOWARN)
    # 6D7B0F: defend X-Axis
    idc.set_cmt(0x6D7B0F, "[UI] defend X-Axis", 0)
    idc.set_name(0x6D7B0F, "ui_6D7B0F", idaapi.SN_NOWARN)
    # 6D7E4B: item box hidden area boxes and headers
    idc.set_cmt(0x6D7E4B, "[UI] item box hidden area boxes and headers", 0)
    idc.set_name(0x6D7E4B, "ui_6D7E4B", idaapi.SN_NOWARN)
    # 6D7E58: magic box hidden area boxes and headers
    idc.set_cmt(0x6D7E58, "[UI] magic box hidden area boxes and headers", 0)
    idc.set_name(0x6D7E58, "ui_6D7E58", idaapi.SN_NOWARN)
    # 6D7E64: summon box hidden area boxes and headers
    idc.set_cmt(0x6D7E64, "[UI] summon box hidden area boxes and headers", 0)
    idc.set_name(0x6D7E64, "ui_6D7E64", idaapi.SN_NOWARN)
    # 6D7E71: eskill (and summon?) box hidden area boxes and hea
    idc.set_cmt(0x6D7E71, "[UI] eskill (and summon?) box hidden area boxes and headers", 0)
    idc.set_name(0x6D7E71, "ui_6D7E71", idaapi.SN_NOWARN)
    # 6D7E76: remove part of main boxes visible on transparency
    idc.set_cmt(0x6D7E76, "[UI] remove part of main boxes visible on transparency", 0)
    idc.set_name(0x6D7E76, "ui_6D7E76", idaapi.SN_NOWARN)
    # 6D84F2: pause text Y-Axis
    idc.set_cmt(0x6D84F2, "[UI] pause text Y-Axis", 0)
    idc.set_name(0x6D84F2, "ui_6D84F2", idaapi.SN_NOWARN)
    # 6D8507: pause text X-Axis
    idc.set_cmt(0x6D8507, "[UI] pause text X-Axis", 0)
    idc.set_name(0x6D8507, "ui_6D8507", idaapi.SN_NOWARN)
    # 6D8512: Pause box height
    idc.set_cmt(0x6D8512, "[UI] Pause box height", 0)
    idc.set_name(0x6D8512, "ui_6D8512", idaapi.SN_NOWARN)
    # 6D8518: pause box width
    idc.set_cmt(0x6D8518, "[UI] pause box width", 0)
    idc.set_name(0x6D8518, "ui_6D8518", idaapi.SN_NOWARN)
    # 6D851B: pause box Y-Axis
    idc.set_cmt(0x6D851B, "[UI] pause box Y-Axis", 0)
    idc.set_name(0x6D851B, "ui_6D851B", idaapi.SN_NOWARN)
    # 6D8530: pause box X-Axis
    idc.set_cmt(0x6D8530, "[UI] pause box X-Axis", 0)
    idc.set_name(0x6D8530, "ui_6D8530", idaapi.SN_NOWARN)
    # 6D9885: item sub menu cursor row count Y-Axis (sub menu re
    idc.set_cmt(0x6D9885, "[UI] item sub menu cursor row count Y-Axis (sub menu refresh)", 0)
    idc.set_name(0x6D9885, "ui_6D9885", idaapi.SN_NOWARN)
    # 6D9B24: magic box column count cursor
    idc.set_cmt(0x6D9B24, "[UI] magic box column count cursor", 0)
    idc.set_name(0x6D9B24, "ui_6D9B24", idaapi.SN_NOWARN)
    # 6D9B2E: magic sub menu cursor row count Y-Axis (sub menu r
    idc.set_cmt(0x6D9B2E, "[UI] magic sub menu cursor row count Y-Axis (sub menu refresh)", 0)
    idc.set_name(0x6D9B2E, "ui_6D9B2E", idaapi.SN_NOWARN)
    # 6D9B42: magic max row count
    idc.set_cmt(0x6D9B42, "[UI] magic max row count", 0)
    idc.set_name(0x6D9B42, "ui_6D9B42", idaapi.SN_NOWARN)
    # 6D9C3F: magic column count, controls spell cast
    idc.set_cmt(0x6D9C3F, "[UI] magic column count, controls spell cast", 0)
    idc.set_name(0x6D9C3F, "ui_6D9C3F", idaapi.SN_NOWARN)
    # 6D9C4F: magic column count selectable
    idc.set_cmt(0x6D9C4F, "[UI] magic column count selectable", 0)
    idc.set_name(0x6D9C4F, "ui_6D9C4F", idaapi.SN_NOWARN)
    # 6DA008: summon sub menu cursor row count Y-Axis (sub menu 
    idc.set_cmt(0x6DA008, "[UI] summon sub menu cursor row count Y-Axis (sub menu refresh)", 0)
    idc.set_name(0x6DA008, "ui_6DA008", idaapi.SN_NOWARN)
    # 6DA2BA: enemy skill column count cursor
    idc.set_cmt(0x6DA2BA, "[UI] enemy skill column count cursor", 0)
    idc.set_name(0x6DA2BA, "ui_6DA2BA", idaapi.SN_NOWARN)
    # 6DA2D2: eskill sub menu cursor row count Y-Axis (sub menu 
    idc.set_cmt(0x6DA2D2, "[UI] eskill sub menu cursor row count Y-Axis (sub menu refresh)", 0)
    idc.set_name(0x6DA2D2, "ui_6DA2D2", idaapi.SN_NOWARN)
    # 6DAED2: box viewing area all boxes offset Y-Axis
    idc.set_cmt(0x6DAED2, "[UI] box viewing area all boxes offset Y-Axis", 0)
    idc.set_name(0x6DAED2, "ui_6DAED2", idaapi.SN_NOWARN)
    # 6DC987: hp bars X-Axis
    idc.set_cmt(0x6DC987, "[UI] hp bars X-Axis", 0)
    idc.set_name(0x6DC987, "ui_6DC987", idaapi.SN_NOWARN)
    # 6DC98D: hp bars spacing Y-Axis - C0 middle then 6B first t
    idc.set_cmt(0x6DC98D, "[UI] hp bars spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DC98D, "ui_6DC98D", idaapi.SN_NOWARN)
    # 6DC991: hp bars Y-Axis
    idc.set_cmt(0x6DC991, "[UI] hp bars Y-Axis", 0)
    idc.set_name(0x6DC991, "ui_6DC991", idaapi.SN_NOWARN)
    # 6DC99D: hp bars length
    idc.set_cmt(0x6DC99D, "[UI] hp bars length", 0)
    idc.set_name(0x6DC99D, "ui_6DC99D", idaapi.SN_NOWARN)
    # 6DC9A3: hp bars height
    idc.set_cmt(0x6DC9A3, "[UI] hp bars height", 0)
    idc.set_name(0x6DC9A3, "ui_6DC9A3", idaapi.SN_NOWARN)
    # 6DCA0B: mp bars X-Axis
    idc.set_cmt(0x6DCA0B, "[UI] mp bars X-Axis", 0)
    idc.set_name(0x6DCA0B, "ui_6DCA0B", idaapi.SN_NOWARN)
    # 6DCA11: mp bars spacing Y-Axis - set middle to D2, then fi
    idc.set_cmt(0x6DCA11, "[UI] mp bars spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DCA11, "ui_6DCA11", idaapi.SN_NOWARN)
    # 6DCA16: mp bars Y-Axis
    idc.set_cmt(0x6DCA16, "[UI] mp bars Y-Axis", 0)
    idc.set_name(0x6DCA16, "ui_6DCA16", idaapi.SN_NOWARN)
    # 6DCA22: mp bars length X-Axis
    idc.set_cmt(0x6DCA22, "[UI] mp bars length X-Axis", 0)
    idc.set_name(0x6DCA22, "ui_6DCA22", idaapi.SN_NOWARN)
    # 6DCA28: mp bars height
    idc.set_cmt(0x6DCA28, "[UI] mp bars height", 0)
    idc.set_name(0x6DCA28, "ui_6DCA28", idaapi.SN_NOWARN)
    # 6DD06F: wait header Y-Axis
    idc.set_cmt(0x6DD06F, "[UI] wait header Y-Axis", 0)
    idc.set_name(0x6DD06F, "ui_6DD06F", idaapi.SN_NOWARN)
    # 6DD074: wait header X-Axis
    idc.set_cmt(0x6DD074, "[UI] wait header X-Axis", 0)
    idc.set_name(0x6DD074, "ui_6DD074", idaapi.SN_NOWARN)
    # 6DD08C: time header pallete
    idc.set_cmt(0x6DD08C, "[UI] time header pallete", 0)
    idc.set_name(0x6DD08C, "ui_6DD08C", idaapi.SN_NOWARN)
    # 6DD096: time header Y-Axis
    idc.set_cmt(0x6DD096, "[UI] time header Y-Axis", 0)
    idc.set_name(0x6DD096, "ui_6DD096", idaapi.SN_NOWARN)
    # 6DD09B: time header X-Axis
    idc.set_cmt(0x6DD09B, "[UI] time header X-Axis", 0)
    idc.set_name(0x6DD09B, "ui_6DD09B", idaapi.SN_NOWARN)
    # 6DD0BE: name header Y-Axis
    idc.set_cmt(0x6DD0BE, "[UI] name header Y-Axis", 0)
    idc.set_name(0x6DD0BE, "ui_6DD0BE", idaapi.SN_NOWARN)
    # 6DD0C3: name header X-Axis
    idc.set_cmt(0x6DD0C3, "[UI] name header X-Axis", 0)
    idc.set_name(0x6DD0C3, "ui_6DD0C3", idaapi.SN_NOWARN)
    # 6DD0E0: hp header Y-Axis
    idc.set_cmt(0x6DD0E0, "[UI] hp header Y-Axis", 0)
    idc.set_name(0x6DD0E0, "ui_6DD0E0", idaapi.SN_NOWARN)
    # 6DD0E5: hp header X-Axis
    idc.set_cmt(0x6DD0E5, "[UI] hp header X-Axis", 0)
    idc.set_name(0x6DD0E5, "ui_6DD0E5", idaapi.SN_NOWARN)
    # 6DD105: mp header Y-Axis
    idc.set_cmt(0x6DD105, "[UI] mp header Y-Axis", 0)
    idc.set_name(0x6DD105, "ui_6DD105", idaapi.SN_NOWARN)
    # 6DD10A: mp header X-Axis
    idc.set_cmt(0x6DD10A, "[UI] mp header X-Axis", 0)
    idc.set_name(0x6DD10A, "ui_6DD10A", idaapi.SN_NOWARN)
    # 6DD12A: limit header Y-Axis
    idc.set_cmt(0x6DD12A, "[UI] limit header Y-Axis", 0)
    idc.set_name(0x6DD12A, "ui_6DD12A", idaapi.SN_NOWARN)
    # 6DD12F: limit header X-Axis
    idc.set_cmt(0x6DD12F, "[UI] limit header X-Axis", 0)
    idc.set_name(0x6DD12F, "ui_6DD12F", idaapi.SN_NOWARN)
    # 6DD14F: barrier header Y-Axis
    idc.set_cmt(0x6DD14F, "[UI] barrier header Y-Axis", 0)
    idc.set_name(0x6DD14F, "ui_6DD14F", idaapi.SN_NOWARN)
    # 6DD154: barrier header X-Axis
    idc.set_cmt(0x6DD154, "[UI] barrier header X-Axis", 0)
    idc.set_name(0x6DD154, "ui_6DD154", idaapi.SN_NOWARN)
    # 6DD170: item box hidden area box contents
    idc.set_cmt(0x6DD170, "[UI] item box hidden area box contents", 0)
    idc.set_name(0x6DD170, "ui_6DD170", idaapi.SN_NOWARN)
    # 6DD182: magic box hidden area box contents
    idc.set_cmt(0x6DD182, "[UI] magic box hidden area box contents", 0)
    idc.set_name(0x6DD182, "ui_6DD182", idaapi.SN_NOWARN)
    # 6DD194: eskill box hidden area box contents
    idc.set_cmt(0x6DD194, "[UI] eskill box hidden area box contents", 0)
    idc.set_name(0x6DD194, "ui_6DD194", idaapi.SN_NOWARN)
    # 6DD1A6: summon box hidden area box contents
    idc.set_cmt(0x6DD1A6, "[UI] summon box hidden area box contents", 0)
    idc.set_name(0x6DD1A6, "ui_6DD1A6", idaapi.SN_NOWARN)
    # 6DD24C: status refresh toggle on hide button
    idc.set_cmt(0x6DD24C, "[UI] status refresh toggle on hide button", 0)
    idc.set_name(0x6DD24C, "ui_6DD24C", idaapi.SN_NOWARN)
    # 6DD31E: 7777 name X-Axis
    idc.set_cmt(0x6DD31E, "[UI] 7777 name X-Axis", 0)
    idc.set_name(0x6DD31E, "ui_6DD31E", idaapi.SN_NOWARN)
    # 6DD3B6: 7777 name spacing Y-Axis - C0 middle then 6B first
    idc.set_cmt(0x6DD3B6, "[UI] 7777 name spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD3B6, "ui_6DD3B6", idaapi.SN_NOWARN)
    # 6DD3BA: 7777 name Y-Axis
    idc.set_cmt(0x6DD3BA, "[UI] 7777 name Y-Axis", 0)
    idc.set_name(0x6DD3BA, "ui_6DD3BA", idaapi.SN_NOWARN)
    # 6DD41A: slow down name flash, affects all battle avatars a
    idc.set_cmt(0x6DD41A, "[UI] slow down name flash, affects all battle avatars as well, use multiples of 2", 0)
    idc.set_name(0x6DD41A, "ui_6DD41A", idaapi.SN_NOWARN)
    # 6DD423: use extra pallete for battle avatars
    idc.set_cmt(0x6DD423, "[UI] use extra pallete for battle avatars", 0)
    idc.set_name(0x6DD423, "ui_6DD423", idaapi.SN_NOWARN)
    # 6DD448: selected name spacing Y-Axis - C9 middle then 6B f
    idc.set_cmt(0x6DD448, "[UI] selected name spacing Y-Axis - C9 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD448, "ui_6DD448", idaapi.SN_NOWARN)
    # 6DD44D: selected name Y-Axis
    idc.set_cmt(0x6DD44D, "[UI] selected name Y-Axis", 0)
    idc.set_name(0x6DD44D, "ui_6DD44D", idaapi.SN_NOWARN)
    # 6DD452: selected character X-Axis change to 2byte
    idc.set_cmt(0x6DD452, "[UI] selected character X-Axis change to 2byte", 0)
    idc.set_name(0x6DD452, "ui_6DD452", idaapi.SN_NOWARN)
    # 6DD453: selected name X-Axis
    idc.set_cmt(0x6DD453, "[UI] selected name X-Axis", 0)
    idc.set_name(0x6DD453, "ui_6DD453", idaapi.SN_NOWARN)
    # 6DD496: allies name spacing Y-Axis C0 middle then 6B first
    idc.set_cmt(0x6DD496, "[UI] allies name spacing Y-Axis C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD496, "ui_6DD496", idaapi.SN_NOWARN)
    # 6DD49A: allies name Y-Axis
    idc.set_cmt(0x6DD49A, "[UI] allies name Y-Axis", 0)
    idc.set_name(0x6DD49A, "ui_6DD49A", idaapi.SN_NOWARN)
    # 6DD49F: allied characters X-Axis change to 2byte
    idc.set_cmt(0x6DD49F, "[UI] allied characters X-Axis change to 2byte", 0)
    idc.set_name(0x6DD49F, "ui_6DD49F", idaapi.SN_NOWARN)
    # 6DD4A0: allies name X-Axis
    idc.set_cmt(0x6DD4A0, "[UI] allies name X-Axis", 0)
    idc.set_name(0x6DD4A0, "ui_6DD4A0", idaapi.SN_NOWARN)
    # 6DD50C: time bar allies selected height
    idc.set_cmt(0x6DD50C, "[UI] time bar allies selected height", 0)
    idc.set_name(0x6DD50C, "ui_6DD50C", idaapi.SN_NOWARN)
    # 6DD534: time bar selected spacing Y-Axis - set middle to D
    idc.set_cmt(0x6DD534, "[UI] time bar selected spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD534, "ui_6DD534", idaapi.SN_NOWARN)
    # 6DD539: time bar selected Y-Axis
    idc.set_cmt(0x6DD539, "[UI] time bar selected Y-Axis", 0)
    idc.set_name(0x6DD539, "ui_6DD539", idaapi.SN_NOWARN)
    # 6DD53F: time bar selected X-Axis
    idc.set_cmt(0x6DD53F, "[UI] time bar selected X-Axis", 0)
    idc.set_name(0x6DD53F, "ui_6DD53F", idaapi.SN_NOWARN)
    # 6DD553: time bar color allies, charged 55 33 00 FF, blue, 
    idc.set_cmt(0x6DD553, "[UI] time bar color allies, charged 55 33 00 FF, blue, green, red tint, XX", 0)
    idc.set_name(0x6DD553, "ui_6DD553", idaapi.SN_NOWARN)
    # 6DD558: time bar allies charged height
    idc.set_cmt(0x6DD558, "[UI] time bar allies charged height", 0)
    idc.set_name(0x6DD558, "ui_6DD558", idaapi.SN_NOWARN)
    # 6DD580: time bar allies charged spacing Y-Axis - C0 middle
    idc.set_cmt(0x6DD580, "[UI] time bar allies charged spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD580, "ui_6DD580", idaapi.SN_NOWARN)
    # 6DD584: time bar allies charged Y-Axis
    idc.set_cmt(0x6DD584, "[UI] time bar allies charged Y-Axis", 0)
    idc.set_name(0x6DD584, "ui_6DD584", idaapi.SN_NOWARN)
    # 6DD58A: time bar allies charged X-Axis
    idc.set_cmt(0x6DD58A, "[UI] time bar allies charged X-Axis", 0)
    idc.set_name(0x6DD58A, "ui_6DD58A", idaapi.SN_NOWARN)
    # 6DD59B: time bar color charging 22 16 00 FF, blue, green, 
    idc.set_cmt(0x6DD59B, "[UI] time bar color charging 22 16 00 FF, blue, green, red tint, XX", 0)
    idc.set_name(0x6DD59B, "ui_6DD59B", idaapi.SN_NOWARN)
    # 6DD5A9: time bar allies charging height
    idc.set_cmt(0x6DD5A9, "[UI] time bar allies charging height", 0)
    idc.set_name(0x6DD5A9, "ui_6DD5A9", idaapi.SN_NOWARN)
    # 6DD5D1: time bar allies charging spacing Y-Axis - set midd
    idc.set_cmt(0x6DD5D1, "[UI] time bar allies charging spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD5D1, "ui_6DD5D1", idaapi.SN_NOWARN)
    # 6DD5D6: time bar allies charging Y-Axis
    idc.set_cmt(0x6DD5D6, "[UI] time bar allies charging Y-Axis", 0)
    idc.set_name(0x6DD5D6, "ui_6DD5D6", idaapi.SN_NOWARN)
    # 6DD5DC: time bar allies charging X-Axis
    idc.set_cmt(0x6DD5DC, "[UI] time bar allies charging X-Axis", 0)
    idc.set_name(0x6DD5DC, "ui_6DD5DC", idaapi.SN_NOWARN)
    # 6DD5F2: time box pallete
    idc.set_cmt(0x6DD5F2, "[UI] time box pallete", 0)
    idc.set_name(0x6DD5F2, "ui_6DD5F2", idaapi.SN_NOWARN)
    # 6DD5FF: time box spacing Y-Axis - C0 middle then 6B first 
    idc.set_cmt(0x6DD5FF, "[UI] time box spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD5FF, "ui_6DD5FF", idaapi.SN_NOWARN)
    # 6DD603: time box Y-Axis
    idc.set_cmt(0x6DD603, "[UI] time box Y-Axis", 0)
    idc.set_name(0x6DD603, "ui_6DD603", idaapi.SN_NOWARN)
    # 6DD604: remove time box
    idc.set_cmt(0x6DD604, "[UI] remove time box", 0)
    idc.set_name(0x6DD604, "ui_6DD604", idaapi.SN_NOWARN)
    # 6DD609: time box X-Axis
    idc.set_cmt(0x6DD609, "[UI] time box X-Axis", 0)
    idc.set_name(0x6DD609, "ui_6DD609", idaapi.SN_NOWARN)
    # 6DD693: limit bar height
    idc.set_cmt(0x6DD693, "[UI] limit bar height", 0)
    idc.set_name(0x6DD693, "ui_6DD693", idaapi.SN_NOWARN)
    # 6DD6B9: limit bar spacing Y-Axis - C0 middle then 6B first
    idc.set_cmt(0x6DD6B9, "[UI] limit bar spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD6B9, "ui_6DD6B9", idaapi.SN_NOWARN)
    # 6DD6BD: limit bar Y-Axis
    idc.set_cmt(0x6DD6BD, "[UI] limit bar Y-Axis", 0)
    idc.set_name(0x6DD6BD, "ui_6DD6BD", idaapi.SN_NOWARN)
    # 6DD6C3: limit bar X-Axis
    idc.set_cmt(0x6DD6C3, "[UI] limit bar X-Axis", 0)
    idc.set_name(0x6DD6C3, "ui_6DD6C3", idaapi.SN_NOWARN)
    # 6DD6D9: limit box pallete
    idc.set_cmt(0x6DD6D9, "[UI] limit box pallete", 0)
    idc.set_name(0x6DD6D9, "ui_6DD6D9", idaapi.SN_NOWARN)
    # 6DD6E6: limit box spacing Y-Axis - C9 middle then 6B first
    idc.set_cmt(0x6DD6E6, "[UI] limit box spacing Y-Axis - C9 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD6E6, "ui_6DD6E6", idaapi.SN_NOWARN)
    # 6DD6EB: limit box Y-Axis
    idc.set_cmt(0x6DD6EB, "[UI] limit box Y-Axis", 0)
    idc.set_name(0x6DD6EB, "ui_6DD6EB", idaapi.SN_NOWARN)
    # 6DD6EC: remove limit box
    idc.set_cmt(0x6DD6EC, "[UI] remove limit box", 0)
    idc.set_name(0x6DD6EC, "ui_6DD6EC", idaapi.SN_NOWARN)
    # 6DD6F1: limit box X-Axis
    idc.set_cmt(0x6DD6F1, "[UI] limit box X-Axis", 0)
    idc.set_name(0x6DD6F1, "ui_6DD6F1", idaapi.SN_NOWARN)
    # 6DD71E: always render barriers command menu
    idc.set_cmt(0x6DD71E, "[UI] always render barriers command menu", 0)
    idc.set_name(0x6DD71E, "ui_6DD71E", idaapi.SN_NOWARN)
    # 6DD72F: barrier physical bar height
    idc.set_cmt(0x6DD72F, "[UI] barrier physical bar height", 0)
    idc.set_name(0x6DD72F, "ui_6DD72F", idaapi.SN_NOWARN)
    # 6DD74C: barrier physical bar spacing Y-Axis - C0 middle th
    idc.set_cmt(0x6DD74C, "[UI] barrier physical bar spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD74C, "ui_6DD74C", idaapi.SN_NOWARN)
    # 6DD750: barrier physical bar Y-Axis
    idc.set_cmt(0x6DD750, "[UI] barrier physical bar Y-Axis", 0)
    idc.set_name(0x6DD750, "ui_6DD750", idaapi.SN_NOWARN)
    # 6DD756: barrier physical bar X-Axis
    idc.set_cmt(0x6DD756, "[UI] barrier physical bar X-Axis", 0)
    idc.set_name(0x6DD756, "ui_6DD756", idaapi.SN_NOWARN)
    # 6DD768: barrier magic bar color 00 00 00 FF, blue, green, 
    idc.set_cmt(0x6DD768, "[UI] barrier magic bar color 00 00 00 FF, blue, green, red, XX tint", 0)
    idc.set_name(0x6DD768, "ui_6DD768", idaapi.SN_NOWARN)
    # 6DD76D: barrier magic bar height
    idc.set_cmt(0x6DD76D, "[UI] barrier magic bar height", 0)
    idc.set_name(0x6DD76D, "ui_6DD76D", idaapi.SN_NOWARN)
    # 6DD78A: barrier magic bar spacing Y-Axis - C9 middle then 
    idc.set_cmt(0x6DD78A, "[UI] barrier magic bar spacing Y-Axis - C9 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD78A, "ui_6DD78A", idaapi.SN_NOWARN)
    # 6DD78F: barrier magic bar Y-Axis
    idc.set_cmt(0x6DD78F, "[UI] barrier magic bar Y-Axis", 0)
    idc.set_name(0x6DD78F, "ui_6DD78F", idaapi.SN_NOWARN)
    # 6DD795: barrier magic bar X-Axis
    idc.set_cmt(0x6DD795, "[UI] barrier magic bar X-Axis", 0)
    idc.set_name(0x6DD795, "ui_6DD795", idaapi.SN_NOWARN)
    # 6DD7AB: barrier boxes pallete (hp/mp sprite)
    idc.set_cmt(0x6DD7AB, "[UI] barrier boxes pallete (hp/mp sprite)", 0)
    idc.set_name(0x6DD7AB, "ui_6DD7AB", idaapi.SN_NOWARN)
    # 6DD7BB: barrier boxes spacing Y-Axis - set middle to D2, t
    idc.set_cmt(0x6DD7BB, "[UI] barrier boxes spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD7BB, "ui_6DD7BB", idaapi.SN_NOWARN)
    # 6DD7C0: barrier boxes Y-Axis
    idc.set_cmt(0x6DD7C0, "[UI] barrier boxes Y-Axis", 0)
    idc.set_name(0x6DD7C0, "ui_6DD7C0", idaapi.SN_NOWARN)
    # 6DD7C6: barrier boxes X-Axis
    idc.set_cmt(0x6DD7C6, "[UI] barrier boxes X-Axis", 0)
    idc.set_name(0x6DD7C6, "ui_6DD7C6", idaapi.SN_NOWARN)
    # 6DD80E: always render current hp and divider
    idc.set_cmt(0x6DD80E, "[UI] always render current hp and divider", 0)
    idc.set_name(0x6DD80E, "ui_6DD80E", idaapi.SN_NOWARN)
    # 6DD853: alive hp palett
    idc.set_cmt(0x6DD853, "[UI] alive hp palett", 0)
    idc.set_name(0x6DD853, "ui_6DD853", idaapi.SN_NOWARN)
    # 6DD86A: alive hp value spacing Y-Axis-  set middle to D2, 
    idc.set_cmt(0x6DD86A, "[UI] alive hp value spacing Y-Axis-  set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD86A, "ui_6DD86A", idaapi.SN_NOWARN)
    # 6DD86F: alive hp value Y-Axis
    idc.set_cmt(0x6DD86F, "[UI] alive hp value Y-Axis", 0)
    idc.set_name(0x6DD86F, "ui_6DD86F", idaapi.SN_NOWARN)
    # 6DD875: alive hp value X-Axis
    idc.set_cmt(0x6DD875, "[UI] alive hp value X-Axis", 0)
    idc.set_name(0x6DD875, "ui_6DD875", idaapi.SN_NOWARN)
    # 6DD89F: dead hp value spacing Y-Axis-  set middle to D2, t
    idc.set_cmt(0x6DD89F, "[UI] dead hp value spacing Y-Axis-  set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD89F, "ui_6DD89F", idaapi.SN_NOWARN)
    # 6DD8A4: dead hp value Y-Axis
    idc.set_cmt(0x6DD8A4, "[UI] dead hp value Y-Axis", 0)
    idc.set_name(0x6DD8A4, "ui_6DD8A4", idaapi.SN_NOWARN)
    # 6DD8AA: dead hp value X-Axis
    idc.set_cmt(0x6DD8AA, "[UI] dead hp value X-Axis", 0)
    idc.set_name(0x6DD8AA, "ui_6DD8AA", idaapi.SN_NOWARN)
    # 6DD8C0: hp divider color pallete
    idc.set_cmt(0x6DD8C0, "[UI] hp divider color pallete", 0)
    idc.set_name(0x6DD8C0, "ui_6DD8C0", idaapi.SN_NOWARN)
    # 6DD8D0: hp divider spacing Y-Axis - C0 middle then 6B firs
    idc.set_cmt(0x6DD8D0, "[UI] hp divider spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD8D0, "ui_6DD8D0", idaapi.SN_NOWARN)
    # 6DD8D4: hp divider Y-Axis
    idc.set_cmt(0x6DD8D4, "[UI] hp divider Y-Axis", 0)
    idc.set_name(0x6DD8D4, "ui_6DD8D4", idaapi.SN_NOWARN)
    # 6DD8D5: hp divider disable
    idc.set_cmt(0x6DD8D5, "[UI] hp divider disable", 0)
    idc.set_name(0x6DD8D5, "ui_6DD8D5", idaapi.SN_NOWARN)
    # 6DD8DA: hp divider X-Axis
    idc.set_cmt(0x6DD8DA, "[UI] hp divider X-Axis", 0)
    idc.set_name(0x6DD8DA, "ui_6DD8DA", idaapi.SN_NOWARN)
    # 6DD903: also always render maxhp
    idc.set_cmt(0x6DD903, "[UI] also always render maxhp", 0)
    idc.set_name(0x6DD903, "ui_6DD903", idaapi.SN_NOWARN)
    # 6DD952: maxhp spacing Y-Axis - C0 middle then 6B first the
    idc.set_cmt(0x6DD952, "[UI] maxhp spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6DD952, "ui_6DD952", idaapi.SN_NOWARN)
    # 6DD956: maxhp Y-Axis
    idc.set_cmt(0x6DD956, "[UI] maxhp Y-Axis", 0)
    idc.set_name(0x6DD956, "ui_6DD956", idaapi.SN_NOWARN)
    # 6DD957: maxhp disable - removed as was unable to keep visi
    idc.set_cmt(0x6DD957, "[UI] maxhp disable - removed as was unable to keep visible with 3 column command menu", 0)
    idc.set_name(0x6DD957, "ui_6DD957", idaapi.SN_NOWARN)
    # 6DD95C: maxhp X-Axis
    idc.set_cmt(0x6DD95C, "[UI] maxhp X-Axis", 0)
    idc.set_name(0x6DD95C, "ui_6DD95C", idaapi.SN_NOWARN)
    # 6DD9A7: alive mp palette color 06
    idc.set_cmt(0x6DD9A7, "[UI] alive mp palette color 06", 0)
    idc.set_name(0x6DD9A7, "ui_6DD9A7", idaapi.SN_NOWARN)
    # 6DD9BE: alive mp value spacing Y-Axis-  set middle to D2, 
    idc.set_cmt(0x6DD9BE, "[UI] alive mp value spacing Y-Axis-  set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD9BE, "ui_6DD9BE", idaapi.SN_NOWARN)
    # 6DD9C3: alive mp value Y-Axis
    idc.set_cmt(0x6DD9C3, "[UI] alive mp value Y-Axis", 0)
    idc.set_name(0x6DD9C3, "ui_6DD9C3", idaapi.SN_NOWARN)
    # 6DD9C9: alive mp value X-Axis
    idc.set_cmt(0x6DD9C9, "[UI] alive mp value X-Axis", 0)
    idc.set_name(0x6DD9C9, "ui_6DD9C9", idaapi.SN_NOWARN)
    # 6DD9F3: dead mp value spacing Y-Axis-  set middle to D2, t
    idc.set_cmt(0x6DD9F3, "[UI] dead mp value spacing Y-Axis-  set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6DD9F3, "ui_6DD9F3", idaapi.SN_NOWARN)
    # 6DD9F8: dead mp value Y-Axis
    idc.set_cmt(0x6DD9F8, "[UI] dead mp value Y-Axis", 0)
    idc.set_name(0x6DD9F8, "ui_6DD9F8", idaapi.SN_NOWARN)
    # 6DD9FE: dead mp value X-Axis
    idc.set_cmt(0x6DD9FE, "[UI] dead mp value X-Axis", 0)
    idc.set_name(0x6DD9FE, "ui_6DD9FE", idaapi.SN_NOWARN)
    # 6DE3F8: always render command box text (item menu)
    idc.set_cmt(0x6DE3F8, "[UI] always render command box text (item menu)", 0)
    idc.set_name(0x6DE3F8, "ui_6DE3F8", idaapi.SN_NOWARN)
    # 6DE40E: always render command box text
    idc.set_cmt(0x6DE40E, "[UI] always render command box text", 0)
    idc.set_name(0x6DE40E, "ui_6DE40E", idaapi.SN_NOWARN)
    # 6DE424: always render command box text (enemy skill menu)
    idc.set_cmt(0x6DE424, "[UI] always render command box text (enemy skill menu)", 0)
    idc.set_name(0x6DE424, "ui_6DE424", idaapi.SN_NOWARN)
    # 6DE43A: always render command box text (summon menu)
    idc.set_cmt(0x6DE43A, "[UI] always render command box text (summon menu)", 0)
    idc.set_name(0x6DE43A, "ui_6DE43A", idaapi.SN_NOWARN)
    # 6DE4BF: command box limit text spacing X-Axis
    idc.set_cmt(0x6DE4BF, "[UI] command box limit text spacing X-Axis", 0)
    idc.set_name(0x6DE4BF, "ui_6DE4BF", idaapi.SN_NOWARN)
    # 6DE4CD: command box limit text X-Axis
    idc.set_cmt(0x6DE4CD, "[UI] command box limit text X-Axis", 0)
    idc.set_name(0x6DE4CD, "ui_6DE4CD", idaapi.SN_NOWARN)
    # 6DE5DF: command box limit text spacing Y-Axis
    idc.set_cmt(0x6DE5DF, "[UI] command box limit text spacing Y-Axis", 0)
    idc.set_name(0x6DE5DF, "ui_6DE5DF", idaapi.SN_NOWARN)
    # 6DE5E1: command box limit text Y-Axis
    idc.set_cmt(0x6DE5E1, "[UI] command box limit text Y-Axis", 0)
    idc.set_name(0x6DE5E1, "ui_6DE5E1", idaapi.SN_NOWARN)
    # 6DE66B: command box coin text spacing Y-Axis
    idc.set_cmt(0x6DE66B, "[UI] command box coin text spacing Y-Axis", 0)
    idc.set_name(0x6DE66B, "ui_6DE66B", idaapi.SN_NOWARN)
    # 6DE66D: command box coin text Y-Axis
    idc.set_cmt(0x6DE66D, "[UI] command box coin text Y-Axis", 0)
    idc.set_name(0x6DE66D, "ui_6DE66D", idaapi.SN_NOWARN)
    # 6DE677: command box coin text spacing X-Axis
    idc.set_cmt(0x6DE677, "[UI] command box coin text spacing X-Axis", 0)
    idc.set_name(0x6DE677, "ui_6DE677", idaapi.SN_NOWARN)
    # 6DE685: command box coin text X-Axis
    idc.set_cmt(0x6DE685, "[UI] command box coin text X-Axis", 0)
    idc.set_name(0x6DE685, "ui_6DE685", idaapi.SN_NOWARN)
    # 6DE6B1: command box throw text spacing Y-Axis
    idc.set_cmt(0x6DE6B1, "[UI] command box throw text spacing Y-Axis", 0)
    idc.set_name(0x6DE6B1, "ui_6DE6B1", idaapi.SN_NOWARN)
    # 6DE6B4: command box throw text Y-Axis
    idc.set_cmt(0x6DE6B4, "[UI] command box throw text Y-Axis", 0)
    idc.set_name(0x6DE6B4, "ui_6DE6B4", idaapi.SN_NOWARN)
    # 6DE6BE: command box throw text spacing X-Axis
    idc.set_cmt(0x6DE6BE, "[UI] command box throw text spacing X-Axis", 0)
    idc.set_name(0x6DE6BE, "ui_6DE6BE", idaapi.SN_NOWARN)
    # 6DE6CC: command box throw text X-Axis
    idc.set_cmt(0x6DE6CC, "[UI] command box throw text X-Axis", 0)
    idc.set_name(0x6DE6CC, "ui_6DE6CC", idaapi.SN_NOWARN)
    # 6DE719: command box text spacing Y-Axis
    idc.set_cmt(0x6DE719, "[UI] command box text spacing Y-Axis", 0)
    idc.set_name(0x6DE719, "ui_6DE719", idaapi.SN_NOWARN)
    # 6DE71C: command box text Y-Axis
    idc.set_cmt(0x6DE71C, "[UI] command box text Y-Axis", 0)
    idc.set_name(0x6DE71C, "ui_6DE71C", idaapi.SN_NOWARN)
    # 6DE726: command box text spacing X-Axis
    idc.set_cmt(0x6DE726, "[UI] command box text spacing X-Axis", 0)
    idc.set_name(0x6DE726, "ui_6DE726", idaapi.SN_NOWARN)
    # 6DE734: command box text X-Axis
    idc.set_cmt(0x6DE734, "[UI] command box text X-Axis", 0)
    idc.set_name(0x6DE734, "ui_6DE734", idaapi.SN_NOWARN)
    # 6DE7A8: command box text support symbol pallete color - ch
    idc.set_cmt(0x6DE7A8, "[UI] command box text support symbol pallete color - changed to white from coloured due to risk of merging with background", 0)
    idc.set_name(0x6DE7A8, "ui_6DE7A8", idaapi.SN_NOWARN)
    # 6DE7B9: command box text support symbol spacing Y-Axis
    idc.set_cmt(0x6DE7B9, "[UI] command box text support symbol spacing Y-Axis", 0)
    idc.set_name(0x6DE7B9, "ui_6DE7B9", idaapi.SN_NOWARN)
    # 6DE7BC: command box text support symbol Y-Axis
    idc.set_cmt(0x6DE7BC, "[UI] command box text support symbol Y-Axis", 0)
    idc.set_name(0x6DE7BC, "ui_6DE7BC", idaapi.SN_NOWARN)
    # 6DE7C6: command box text support symbol spacing X-Axis
    idc.set_cmt(0x6DE7C6, "[UI] command box text support symbol spacing X-Axis", 0)
    idc.set_name(0x6DE7C6, "ui_6DE7C6", idaapi.SN_NOWARN)
    # 6DE7D9: command box text support symbol X-Axis
    idc.set_cmt(0x6DE7D9, "[UI] command box text support symbol X-Axis", 0)
    idc.set_name(0x6DE7D9, "ui_6DE7D9", idaapi.SN_NOWARN)
    # 6DEC31: item sub menu scroll bar height rows Y-Axis
    idc.set_cmt(0x6DEC31, "[UI] item sub menu scroll bar height rows Y-Axis", 0)
    idc.set_name(0x6DEC31, "ui_6DEC31", idaapi.SN_NOWARN)
    # 6DEC50: item sub menu scroll bar X-Axis
    idc.set_cmt(0x6DEC50, "[UI] item sub menu scroll bar X-Axis", 0)
    idc.set_name(0x6DEC50, "ui_6DEC50", idaapi.SN_NOWARN)
    # 6DEC56: item sub menu scroll bar Y-Axis
    idc.set_cmt(0x6DEC56, "[UI] item sub menu scroll bar Y-Axis", 0)
    idc.set_name(0x6DEC56, "ui_6DEC56", idaapi.SN_NOWARN)
    # 6DEC5C: item sub menu scroll bar width
    idc.set_cmt(0x6DEC5C, "[UI] item sub menu scroll bar width", 0)
    idc.set_name(0x6DEC5C, "ui_6DEC5C", idaapi.SN_NOWARN)
    # 6DEC62: item sub menu scroll bar height
    idc.set_cmt(0x6DEC62, "[UI] item sub menu scroll bar height", 0)
    idc.set_name(0x6DEC62, "ui_6DEC62", idaapi.SN_NOWARN)
    # 6DEC99: item sub menu scroll bottom border row number
    idc.set_cmt(0x6DEC99, "[UI] item sub menu scroll bottom border row number", 0)
    idc.set_name(0x6DEC99, "ui_6DEC99", idaapi.SN_NOWARN)
    # 6DECA1: item sub menu row count Y-Axis
    idc.set_cmt(0x6DECA1, "[UI] item sub menu row count Y-Axis", 0)
    idc.set_name(0x6DECA1, "ui_6DECA1", idaapi.SN_NOWARN)
    # 6DED10: offset for colon/value color on unusable items
    idc.set_cmt(0x6DED10, "[UI] offset for colon/value color on unusable items", 0)
    idc.set_name(0x6DED10, "ui_6DED10", idaapi.SN_NOWARN)
    # 6DED13: item sub menu colon/value colors
    idc.set_cmt(0x6DED13, "[UI] item sub menu colon/value colors", 0)
    idc.set_name(0x6DED13, "ui_6DED13", idaapi.SN_NOWARN)
    # 6DED72: item sub menu icon spacing Y-Axis
    idc.set_cmt(0x6DED72, "[UI] item sub menu icon spacing Y-Axis", 0)
    idc.set_name(0x6DED72, "ui_6DED72", idaapi.SN_NOWARN)
    # 6DED78: item sub menu icon Y-Axis
    idc.set_cmt(0x6DED78, "[UI] item sub menu icon Y-Axis", 0)
    idc.set_name(0x6DED78, "ui_6DED78", idaapi.SN_NOWARN)
    # 6DED7E: item sub menu icon X-Axis
    idc.set_cmt(0x6DED7E, "[UI] item sub menu icon X-Axis", 0)
    idc.set_name(0x6DED7E, "ui_6DED7E", idaapi.SN_NOWARN)
    # 6DED7F: disable render of OG icons item battle
    idc.set_cmt(0x6DED7F, "[UI] disable render of OG icons item battle", 0)
    idc.set_name(0x6DED7F, "ui_6DED7F", idaapi.SN_NOWARN)
    # 6DED9D: item sub menu colon spacing Y-Axis
    idc.set_cmt(0x6DED9D, "[UI] item sub menu colon spacing Y-Axis", 0)
    idc.set_name(0x6DED9D, "ui_6DED9D", idaapi.SN_NOWARN)
    # 6DEDA3: item sub menu colon Y-Axis
    idc.set_cmt(0x6DEDA3, "[UI] item sub menu colon Y-Axis", 0)
    idc.set_name(0x6DEDA3, "ui_6DEDA3", idaapi.SN_NOWARN)
    # 6DEDA4: item remove sub menu colon
    idc.set_cmt(0x6DEDA4, "[UI] item remove sub menu colon", 0)
    idc.set_name(0x6DEDA4, "ui_6DEDA4", idaapi.SN_NOWARN)
    # 6DEDA9: item sub menu colon X-Axis
    idc.set_cmt(0x6DEDA9, "[UI] item sub menu colon X-Axis", 0)
    idc.set_name(0x6DEDA9, "ui_6DEDA9", idaapi.SN_NOWARN)
    # 6DEDD8: item sub menu value spacing Y-Axis
    idc.set_cmt(0x6DEDD8, "[UI] item sub menu value spacing Y-Axis", 0)
    idc.set_name(0x6DEDD8, "ui_6DEDD8", idaapi.SN_NOWARN)
    # 6DEDDE: item sub menu value Y-Axis
    idc.set_cmt(0x6DEDDE, "[UI] item sub menu value Y-Axis", 0)
    idc.set_name(0x6DEDDE, "ui_6DEDDE", idaapi.SN_NOWARN)
    # 6DEDE4: item sub menu value X-Axis
    idc.set_cmt(0x6DEDE4, "[UI] item sub menu value X-Axis", 0)
    idc.set_name(0x6DEDE4, "ui_6DEDE4", idaapi.SN_NOWARN)
    # 6DEEC5: item sub menu text spacing Y-Axis
    idc.set_cmt(0x6DEEC5, "[UI] item sub menu text spacing Y-Axis", 0)
    idc.set_name(0x6DEEC5, "ui_6DEEC5", idaapi.SN_NOWARN)
    # 6DEECB: item sub menu text Y-Axis
    idc.set_cmt(0x6DEECB, "[UI] item sub menu text Y-Axis", 0)
    idc.set_name(0x6DEECB, "ui_6DEECB", idaapi.SN_NOWARN)
    # 6DEED1: item sub menu text X-Axis
    idc.set_cmt(0x6DEED1, "[UI] item sub menu text X-Axis", 0)
    idc.set_name(0x6DEED1, "ui_6DEED1", idaapi.SN_NOWARN)
    # 6DF490: limit box text spacing Y-Axis
    idc.set_cmt(0x6DF490, "[UI] limit box text spacing Y-Axis", 0)
    idc.set_name(0x6DF490, "ui_6DF490", idaapi.SN_NOWARN)
    # 6DF492: limit box text Y-Axis
    idc.set_cmt(0x6DF492, "[UI] limit box text Y-Axis", 0)
    idc.set_name(0x6DF492, "ui_6DF492", idaapi.SN_NOWARN)
    # 6DF498: limit box text X-Axis
    idc.set_cmt(0x6DF498, "[UI] limit box text X-Axis", 0)
    idc.set_name(0x6DF498, "ui_6DF498", idaapi.SN_NOWARN)
    # 6DF4BA: limit box limit header Y-Axis
    idc.set_cmt(0x6DF4BA, "[UI] limit box limit header Y-Axis", 0)
    idc.set_name(0x6DF4BA, "ui_6DF4BA", idaapi.SN_NOWARN)
    # 6DF4BF: limit box limit header X-Axis
    idc.set_cmt(0x6DF4BF, "[UI] limit box limit header X-Axis", 0)
    idc.set_name(0x6DF4BF, "ui_6DF4BF", idaapi.SN_NOWARN)
    # 6DF4E2: limit box lv header Y-Axis
    idc.set_cmt(0x6DF4E2, "[UI] limit box lv header Y-Axis", 0)
    idc.set_name(0x6DF4E2, "ui_6DF4E2", idaapi.SN_NOWARN)
    # 6DF4E7: limit box lv header X-Axis
    idc.set_cmt(0x6DF4E7, "[UI] limit box lv header X-Axis", 0)
    idc.set_name(0x6DF4E7, "ui_6DF4E7", idaapi.SN_NOWARN)
    # 6DF533: limit box level value header Y-Axis
    idc.set_cmt(0x6DF533, "[UI] limit box level value header Y-Axis", 0)
    idc.set_name(0x6DF533, "ui_6DF533", idaapi.SN_NOWARN)
    # 6DF538: limit box level value header X-Axis
    idc.set_cmt(0x6DF538, "[UI] limit box level value header X-Axis", 0)
    idc.set_name(0x6DF538, "ui_6DF538", idaapi.SN_NOWARN)
    # 6DF57C: limit box BG top left
    idc.set_cmt(0x6DF57C, "[UI] limit box BG top left", 0)
    idc.set_name(0x6DF57C, "ui_6DF57C", idaapi.SN_NOWARN)
    # 6DF585: limit box BG
    idc.set_cmt(0x6DF585, "[UI] limit box BG", 0)
    idc.set_name(0x6DF585, "ui_6DF585", idaapi.SN_NOWARN)
    # 6DF5C5: limit box BG bottom left
    idc.set_cmt(0x6DF5C5, "[UI] limit box BG bottom left", 0)
    idc.set_name(0x6DF5C5, "ui_6DF5C5", idaapi.SN_NOWARN)
    # 6DF62C: limit box BG top right
    idc.set_cmt(0x6DF62C, "[UI] limit box BG top right", 0)
    idc.set_name(0x6DF62C, "ui_6DF62C", idaapi.SN_NOWARN)
    # 6DF675: limit box BG bottom right
    idc.set_cmt(0x6DF675, "[UI] limit box BG bottom right", 0)
    idc.set_name(0x6DF675, "ui_6DF675", idaapi.SN_NOWARN)
    # 6DF9F7: magic sub menu scroll bar height rows Y-Axis
    idc.set_cmt(0x6DF9F7, "[UI] magic sub menu scroll bar height rows Y-Axis", 0)
    idc.set_name(0x6DF9F7, "ui_6DF9F7", idaapi.SN_NOWARN)
    # 6DF9FD: magic sub menu scroll bar row count Y-Axis
    idc.set_cmt(0x6DF9FD, "[UI] magic sub menu scroll bar row count Y-Axis", 0)
    idc.set_name(0x6DF9FD, "ui_6DF9FD", idaapi.SN_NOWARN)
    # 6DFA0E: magic sub menu scroll bar X-Axis
    idc.set_cmt(0x6DFA0E, "[UI] magic sub menu scroll bar X-Axis", 0)
    idc.set_name(0x6DFA0E, "ui_6DFA0E", idaapi.SN_NOWARN)
    # 6DFA14: magic sub menu scroll bar Y-Axis
    idc.set_cmt(0x6DFA14, "[UI] magic sub menu scroll bar Y-Axis", 0)
    idc.set_name(0x6DFA14, "ui_6DFA14", idaapi.SN_NOWARN)
    # 6DFA1A: magic sub menu scroll bar width
    idc.set_cmt(0x6DFA1A, "[UI] magic sub menu scroll bar width", 0)
    idc.set_name(0x6DFA1A, "ui_6DFA1A", idaapi.SN_NOWARN)
    # 6DFA20: magic sub menu scroll bar height
    idc.set_cmt(0x6DFA20, "[UI] magic sub menu scroll bar height", 0)
    idc.set_name(0x6DFA20, "ui_6DFA20", idaapi.SN_NOWARN)
    # 6DFA48: magic column count fix display name
    idc.set_cmt(0x6DFA48, "[UI] magic column count fix display name", 0)
    idc.set_name(0x6DFA48, "ui_6DFA48", idaapi.SN_NOWARN)
    # 6DFA77: magic sub menu scroll bottom border row number
    idc.set_cmt(0x6DFA77, "[UI] magic sub menu scroll bottom border row number", 0)
    idc.set_name(0x6DFA77, "ui_6DFA77", idaapi.SN_NOWARN)
    # 6DFA7F: magic sub menu row count Y-Axis
    idc.set_cmt(0x6DFA7F, "[UI] magic sub menu row count Y-Axis", 0)
    idc.set_name(0x6DFA7F, "ui_6DFA7F", idaapi.SN_NOWARN)
    # 6DFAC4: magic column count text
    idc.set_cmt(0x6DFAC4, "[UI] magic column count text", 0)
    idc.set_name(0x6DFAC4, "ui_6DFAC4", idaapi.SN_NOWARN)
    # 6DFADA: magic column count text extra columns
    idc.set_cmt(0x6DFADA, "[UI] magic column count text extra columns", 0)
    idc.set_name(0x6DFADA, "ui_6DFADA", idaapi.SN_NOWARN)
    # 6DFB2C: magic column count text first column
    idc.set_cmt(0x6DFB2C, "[UI] magic column count text first column", 0)
    idc.set_name(0x6DFB2C, "ui_6DFB2C", idaapi.SN_NOWARN)
    # 6DFB4B: magic sub menu text spacing Y-Axis
    idc.set_cmt(0x6DFB4B, "[UI] magic sub menu text spacing Y-Axis", 0)
    idc.set_name(0x6DFB4B, "ui_6DFB4B", idaapi.SN_NOWARN)
    # 6DFB51: magic sub menu text Y-Axis
    idc.set_cmt(0x6DFB51, "[UI] magic sub menu text Y-Axis", 0)
    idc.set_name(0x6DFB51, "ui_6DFB51", idaapi.SN_NOWARN)
    # 6DFB5B: magic sub menu text spacing X-Axis
    idc.set_cmt(0x6DFB5B, "[UI] magic sub menu text spacing X-Axis", 0)
    idc.set_name(0x6DFB5B, "ui_6DFB5B", idaapi.SN_NOWARN)
    # 6DFB61: magic sub menu text X-Axis
    idc.set_cmt(0x6DFB61, "[UI] magic sub menu text X-Axis", 0)
    idc.set_name(0x6DFB61, "ui_6DFB61", idaapi.SN_NOWARN)
    # 6DFBAE: magic column count support symbols
    idc.set_cmt(0x6DFBAE, "[UI] magic column count support symbols", 0)
    idc.set_name(0x6DFBAE, "ui_6DFBAE", idaapi.SN_NOWARN)
    # 6DFC02: magic sub menu text support symbol palette color -
    idc.set_cmt(0x6DFC02, "[UI] magic sub menu text support symbol palette color - changed to white from coloured due to risk of merging with background", 0)
    idc.set_name(0x6DFC02, "ui_6DFC02", idaapi.SN_NOWARN)
    # 6DFC16: magic sub menu text support symbol spacing Y-Axis
    idc.set_cmt(0x6DFC16, "[UI] magic sub menu text support symbol spacing Y-Axis", 0)
    idc.set_name(0x6DFC16, "ui_6DFC16", idaapi.SN_NOWARN)
    # 6DFC1C: magic sub menu text support symbol Y-Axis
    idc.set_cmt(0x6DFC1C, "[UI] magic sub menu text support symbol Y-Axis", 0)
    idc.set_name(0x6DFC1C, "ui_6DFC1C", idaapi.SN_NOWARN)
    # 6DFC26: magic sub menu text support symbol spacing X-Axis
    idc.set_cmt(0x6DFC26, "[UI] magic sub menu text support symbol spacing X-Axis", 0)
    idc.set_name(0x6DFC26, "ui_6DFC26", idaapi.SN_NOWARN)
    # 6DFC2C: magic sub menu text support symbol X-Axis
    idc.set_cmt(0x6DFC2C, "[UI] magic sub menu text support symbol X-Axis", 0)
    idc.set_name(0x6DFC2C, "ui_6DFC2C", idaapi.SN_NOWARN)
    # 6DFC46: magic sub menu mpneeded contents Y-Axis
    idc.set_cmt(0x6DFC46, "[UI] magic sub menu mpneeded contents Y-Axis", 0)
    idc.set_name(0x6DFC46, "ui_6DFC46", idaapi.SN_NOWARN)
    # 6DFC4B: magic sub menu mpneeded contents X-Axis
    idc.set_cmt(0x6DFC4B, "[UI] magic sub menu mpneeded contents X-Axis", 0)
    idc.set_name(0x6DFC4B, "ui_6DFC4B", idaapi.SN_NOWARN)
    # 6DFC75: all sub menu mpneeded logo pallette
    idc.set_cmt(0x6DFC75, "[UI] all sub menu mpneeded logo pallette", 0)
    idc.set_name(0x6DFC75, "ui_6DFC75", idaapi.SN_NOWARN)
    # 6DFC87: all sub menu mpneeded logo X-Axis
    idc.set_cmt(0x6DFC87, "[UI] all sub menu mpneeded logo X-Axis", 0)
    idc.set_name(0x6DFC87, "ui_6DFC87", idaapi.SN_NOWARN)
    # 6DFD0E: magic column count info box fix
    idc.set_cmt(0x6DFD0E, "[UI] magic column count info box fix", 0)
    idc.set_name(0x6DFD0E, "ui_6DFD0E", idaapi.SN_NOWARN)
    # 6DFD58: all sub menu mpneeded All X-Axis
    idc.set_cmt(0x6DFD58, "[UI] all sub menu mpneeded All X-Axis", 0)
    idc.set_name(0x6DFD58, "ui_6DFD58", idaapi.SN_NOWARN)
    # 6DFDFD: enemy skill column count mp cost
    idc.set_cmt(0x6DFDFD, "[UI] enemy skill column count mp cost", 0)
    idc.set_name(0x6DFDFD, "ui_6DFDFD", idaapi.SN_NOWARN)
    # 6DFE6F: all sub menu mpneeded turbo/quadra X-Axis
    idc.set_cmt(0x6DFE6F, "[UI] all sub menu mpneeded turbo/quadra X-Axis", 0)
    idc.set_name(0x6DFE6F, "ui_6DFE6F", idaapi.SN_NOWARN)
    # 6DFEA7: all sub menu mpneeded turbo/quadra value Y-Axis
    idc.set_cmt(0x6DFEA7, "[UI] all sub menu mpneeded turbo/quadra value Y-Axis", 0)
    idc.set_name(0x6DFEA7, "ui_6DFEA7", idaapi.SN_NOWARN)
    # 6DFEAE: all sub menu mpneeded turbo/quadra value X-Axis
    idc.set_cmt(0x6DFEAE, "[UI] all sub menu mpneeded turbo/quadra value X-Axis", 0)
    idc.set_name(0x6DFEAE, "ui_6DFEAE", idaapi.SN_NOWARN)
    # 6DFEF0: all sub menu mpneeded turbo/quadra X pallete
    idc.set_cmt(0x6DFEF0, "[UI] all sub menu mpneeded turbo/quadra X pallete", 0)
    idc.set_name(0x6DFEF0, "ui_6DFEF0", idaapi.SN_NOWARN)
    # 6DFEFE: all sub menu mpneeded turbo/quadra X Y-Axis
    idc.set_cmt(0x6DFEFE, "[UI] all sub menu mpneeded turbo/quadra X Y-Axis", 0)
    idc.set_name(0x6DFEFE, "ui_6DFEFE", idaapi.SN_NOWARN)
    # 6DFF05: all sub menu mpneeded turbo/quadra X X-Axis
    idc.set_cmt(0x6DFF05, "[UI] all sub menu mpneeded turbo/quadra X X-Axis", 0)
    idc.set_name(0x6DFF05, "ui_6DFF05", idaapi.SN_NOWARN)
    # 6DFF51: all sub menu mpneeded summon/all usage value Y-Axi
    idc.set_cmt(0x6DFF51, "[UI] all sub menu mpneeded summon/all usage value Y-Axis", 0)
    idc.set_name(0x6DFF51, "ui_6DFF51", idaapi.SN_NOWARN)
    # 6DFF58: all sub menu mpneeded summon/all usage value X-Axi
    idc.set_cmt(0x6DFF58, "[UI] all sub menu mpneeded summon/all usage value X-Axis", 0)
    idc.set_name(0x6DFF58, "ui_6DFF58", idaapi.SN_NOWARN)
    # 6DFF7F: all sub menu mpneeded summon unlimited Y-Axis
    idc.set_cmt(0x6DFF7F, "[UI] all sub menu mpneeded summon unlimited Y-Axis", 0)
    idc.set_name(0x6DFF7F, "ui_6DFF7F", idaapi.SN_NOWARN)
    # 6DFF86: all sub menu mpneeded summon unlimited X-Axis
    idc.set_cmt(0x6DFF86, "[UI] all sub menu mpneeded summon unlimited X-Axis", 0)
    idc.set_name(0x6DFF86, "ui_6DFF86", idaapi.SN_NOWARN)
    # 6DFF9A: all sub menu mpneeded summon/all pallete
    idc.set_cmt(0x6DFF9A, "[UI] all sub menu mpneeded summon/all pallete", 0)
    idc.set_name(0x6DFF9A, "ui_6DFF9A", idaapi.SN_NOWARN)
    # 6DFFA8: all sub menu mpneeded summon/all X Y-Axis
    idc.set_cmt(0x6DFFA8, "[UI] all sub menu mpneeded summon/all X Y-Axis", 0)
    idc.set_name(0x6DFFA8, "ui_6DFFA8", idaapi.SN_NOWARN)
    # 6DFFAF: all sub menu mpneeded summon/all X X-Axis
    idc.set_cmt(0x6DFFAF, "[UI] all sub menu mpneeded summon/all X X-Axis", 0)
    idc.set_name(0x6DFFAF, "ui_6DFFAF", idaapi.SN_NOWARN)
    # 6DFFD4: all sub menu mpneeded mp cost Y-Axis
    idc.set_cmt(0x6DFFD4, "[UI] all sub menu mpneeded mp cost Y-Axis", 0)
    idc.set_name(0x6DFFD4, "ui_6DFFD4", idaapi.SN_NOWARN)
    # 6E0005: all sub menu mpneeded MAXMP remove
    idc.set_cmt(0x6E0005, "[UI] all sub menu mpneeded MAXMP remove", 0)
    idc.set_name(0x6E0005, "ui_6E0005", idaapi.SN_NOWARN)
    # 6E000C: all sub menu mpneeded MAXMP X-Axis
    idc.set_cmt(0x6E000C, "[UI] all sub menu mpneeded MAXMP X-Axis", 0)
    idc.set_name(0x6E000C, "ui_6E000C", idaapi.SN_NOWARN)
    # 6E0020: all sub menu mpneeded divider color pallette
    idc.set_cmt(0x6E0020, "[UI] all sub menu mpneeded divider color pallette", 0)
    idc.set_name(0x6E0020, "ui_6E0020", idaapi.SN_NOWARN)
    # 6E0031: all sub menu mpneeded / remove
    idc.set_cmt(0x6E0031, "[UI] all sub menu mpneeded / remove", 0)
    idc.set_name(0x6E0031, "ui_6E0031", idaapi.SN_NOWARN)
    # 6E0038: all sub menu mpneeded / X-Axis - adjusted to centr
    idc.set_cmt(0x6E0038, "[UI] all sub menu mpneeded / X-Axis - adjusted to centre aligned as cannot adjust mp cost x-axis", 0)
    idc.set_name(0x6E0038, "ui_6E0038", idaapi.SN_NOWARN)
    # 6E0706: summon sub menu scroll bar height rows Y-Axis
    idc.set_cmt(0x6E0706, "[UI] summon sub menu scroll bar height rows Y-Axis", 0)
    idc.set_name(0x6E0706, "ui_6E0706", idaapi.SN_NOWARN)
    # 6E071D: summon sub menu scroll bar X-Axis
    idc.set_cmt(0x6E071D, "[UI] summon sub menu scroll bar X-Axis", 0)
    idc.set_name(0x6E071D, "ui_6E071D", idaapi.SN_NOWARN)
    # 6E0723: summon sub menu scroll bar Y-Axis
    idc.set_cmt(0x6E0723, "[UI] summon sub menu scroll bar Y-Axis", 0)
    idc.set_name(0x6E0723, "ui_6E0723", idaapi.SN_NOWARN)
    # 6E0729: summon sub menu scroll bar width
    idc.set_cmt(0x6E0729, "[UI] summon sub menu scroll bar width", 0)
    idc.set_name(0x6E0729, "ui_6E0729", idaapi.SN_NOWARN)
    # 6E072F: summon sub menu scroll bar height
    idc.set_cmt(0x6E072F, "[UI] summon sub menu scroll bar height", 0)
    idc.set_name(0x6E072F, "ui_6E072F", idaapi.SN_NOWARN)
    # 6E0766: summon sub menu scroll bottom border row number
    idc.set_cmt(0x6E0766, "[UI] summon sub menu scroll bottom border row number", 0)
    idc.set_name(0x6E0766, "ui_6E0766", idaapi.SN_NOWARN)
    # 6E076E: summon sub menu row count Y-Axis
    idc.set_cmt(0x6E076E, "[UI] summon sub menu row count Y-Axis", 0)
    idc.set_name(0x6E076E, "ui_6E076E", idaapi.SN_NOWARN)
    # 6E0806: summon sub menu text spacing Y-Axis
    idc.set_cmt(0x6E0806, "[UI] summon sub menu text spacing Y-Axis", 0)
    idc.set_name(0x6E0806, "ui_6E0806", idaapi.SN_NOWARN)
    # 6E080C: summon sub menu text Y-Axis
    idc.set_cmt(0x6E080C, "[UI] summon sub menu text Y-Axis", 0)
    idc.set_name(0x6E080C, "ui_6E080C", idaapi.SN_NOWARN)
    # 6E0812: summon sub menu text X-Axis
    idc.set_cmt(0x6E0812, "[UI] summon sub menu text X-Axis", 0)
    idc.set_name(0x6E0812, "ui_6E0812", idaapi.SN_NOWARN)
    # 6E0823: summon sub menu mpneeded contents Y-Axis
    idc.set_cmt(0x6E0823, "[UI] summon sub menu mpneeded contents Y-Axis", 0)
    idc.set_name(0x6E0823, "ui_6E0823", idaapi.SN_NOWARN)
    # 6E0828: summon sub menu mpneeded contents X-Axis
    idc.set_cmt(0x6E0828, "[UI] summon sub menu mpneeded contents X-Axis", 0)
    idc.set_name(0x6E0828, "ui_6E0828", idaapi.SN_NOWARN)
    # 6E09F8: eskill sub menu scroll bar height rows Y-Axis
    idc.set_cmt(0x6E09F8, "[UI] eskill sub menu scroll bar height rows Y-Axis", 0)
    idc.set_name(0x6E09F8, "ui_6E09F8", idaapi.SN_NOWARN)
    # 6E0A0F: eskill sub menu scroll bar X-Axis
    idc.set_cmt(0x6E0A0F, "[UI] eskill sub menu scroll bar X-Axis", 0)
    idc.set_name(0x6E0A0F, "ui_6E0A0F", idaapi.SN_NOWARN)
    # 6E0A15: eskill sub menu scroll bar Y-Axis
    idc.set_cmt(0x6E0A15, "[UI] eskill sub menu scroll bar Y-Axis", 0)
    idc.set_name(0x6E0A15, "ui_6E0A15", idaapi.SN_NOWARN)
    # 6E0A1B: eskill sub menu scroll bar width
    idc.set_cmt(0x6E0A1B, "[UI] eskill sub menu scroll bar width", 0)
    idc.set_name(0x6E0A1B, "ui_6E0A1B", idaapi.SN_NOWARN)
    # 6E0A21: eskill sub menu scroll bar height
    idc.set_cmt(0x6E0A21, "[UI] eskill sub menu scroll bar height", 0)
    idc.set_name(0x6E0A21, "ui_6E0A21", idaapi.SN_NOWARN)
    # 6E0A59: eskill sub menu scroll bottom border row number
    idc.set_cmt(0x6E0A59, "[UI] eskill sub menu scroll bottom border row number", 0)
    idc.set_name(0x6E0A59, "ui_6E0A59", idaapi.SN_NOWARN)
    # 6E0A61: eskill sub menu row count Y-Axis
    idc.set_cmt(0x6E0A61, "[UI] eskill sub menu row count Y-Axis", 0)
    idc.set_name(0x6E0A61, "ui_6E0A61", idaapi.SN_NOWARN)
    # 6E0AE1: eskill column count text assignment
    idc.set_cmt(0x6E0AE1, "[UI] eskill column count text assignment", 0)
    idc.set_name(0x6E0AE1, "ui_6E0AE1", idaapi.SN_NOWARN)
    # 6E0B0A: enemy skill column count text
    idc.set_cmt(0x6E0B0A, "[UI] enemy skill column count text", 0)
    idc.set_name(0x6E0B0A, "ui_6E0B0A", idaapi.SN_NOWARN)
    # 6E0B27: eskill sub menu text spacing Y-Axis
    idc.set_cmt(0x6E0B27, "[UI] eskill sub menu text spacing Y-Axis", 0)
    idc.set_name(0x6E0B27, "ui_6E0B27", idaapi.SN_NOWARN)
    # 6E0B2D: eskill sub menu text Y-Axis
    idc.set_cmt(0x6E0B2D, "[UI] eskill sub menu text Y-Axis", 0)
    idc.set_name(0x6E0B2D, "ui_6E0B2D", idaapi.SN_NOWARN)
    # 6E0B37: eskill sub menu text spacing X-Axis
    idc.set_cmt(0x6E0B37, "[UI] eskill sub menu text spacing X-Axis", 0)
    idc.set_name(0x6E0B37, "ui_6E0B37", idaapi.SN_NOWARN)
    # 6E0B3D: eskill sub menu text X-Axis
    idc.set_cmt(0x6E0B3D, "[UI] eskill sub menu text X-Axis", 0)
    idc.set_name(0x6E0B3D, "ui_6E0B3D", idaapi.SN_NOWARN)
    # 6E0B54: eskill sub menu mpneeded contents Y-Axis
    idc.set_cmt(0x6E0B54, "[UI] eskill sub menu mpneeded contents Y-Axis", 0)
    idc.set_name(0x6E0B54, "ui_6E0B54", idaapi.SN_NOWARN)
    # 6E0B59: eskill sub menu mpneeded contents X-Axis
    idc.set_cmt(0x6E0B59, "[UI] eskill sub menu mpneeded contents X-Axis", 0)
    idc.set_name(0x6E0B59, "ui_6E0B59", idaapi.SN_NOWARN)
    # 6E0D3B: coin \"how much\" word Y-Axis
    idc.set_cmt(0x6E0D3B, "[UI] coin \"how much\" word Y-Axis", 0)
    idc.set_name(0x6E0D3B, "ui_6E0D3B", idaapi.SN_NOWARN)
    # 6E0D40: coin \"how much\" word X-Axis
    idc.set_cmt(0x6E0D40, "[UI] coin \"how much\" word X-Axis", 0)
    idc.set_name(0x6E0D40, "ui_6E0D40", idaapi.SN_NOWARN)
    # 6E0D56: coin \"gil\" word Y-Axis
    idc.set_cmt(0x6E0D56, "[UI] coin \"gil\" word Y-Axis", 0)
    idc.set_name(0x6E0D56, "ui_6E0D56", idaapi.SN_NOWARN)
    # 6E0D5B: coin \"gil\" word X-Axis
    idc.set_cmt(0x6E0D5B, "[UI] coin \"gil\" word X-Axis", 0)
    idc.set_name(0x6E0D5B, "ui_6E0D5B", idaapi.SN_NOWARN)
    # 6E0D74: coin \"after\" word Y-Axis
    idc.set_cmt(0x6E0D74, "[UI] coin \"after\" word Y-Axis", 0)
    idc.set_name(0x6E0D74, "ui_6E0D74", idaapi.SN_NOWARN)
    # 6E0D79: coin \"after\" word X-Axis
    idc.set_cmt(0x6E0D79, "[UI] coin \"after\" word X-Axis", 0)
    idc.set_name(0x6E0D79, "ui_6E0D79", idaapi.SN_NOWARN)
    # 6E0D92: coin \"gil on hand\" word Y-Axis
    idc.set_cmt(0x6E0D92, "[UI] coin \"gil on hand\" word Y-Axis", 0)
    idc.set_name(0x6E0D92, "ui_6E0D92", idaapi.SN_NOWARN)
    # 6E0D97: coin \"gil on hand\" word X-Axis
    idc.set_cmt(0x6E0D97, "[UI] coin \"gil on hand\" word X-Axis", 0)
    idc.set_name(0x6E0D97, "ui_6E0D97", idaapi.SN_NOWARN)
    # 6E0DB3: coin raise value Y-Axis
    idc.set_cmt(0x6E0DB3, "[UI] coin raise value Y-Axis", 0)
    idc.set_name(0x6E0DB3, "ui_6E0DB3", idaapi.SN_NOWARN)
    # 6E0DB8: coin raise value X-Axis
    idc.set_cmt(0x6E0DB8, "[UI] coin raise value X-Axis", 0)
    idc.set_name(0x6E0DB8, "ui_6E0DB8", idaapi.SN_NOWARN)
    # 6E0DDB: coin after value Y-Axis
    idc.set_cmt(0x6E0DDB, "[UI] coin after value Y-Axis", 0)
    idc.set_name(0x6E0DDB, "ui_6E0DDB", idaapi.SN_NOWARN)
    # 6E0DE0: coin after value X-Axis
    idc.set_cmt(0x6E0DE0, "[UI] coin after value X-Axis", 0)
    idc.set_name(0x6E0DE0, "ui_6E0DE0", idaapi.SN_NOWARN)
    # 6E0DFD: coin current value Y-Axis
    idc.set_cmt(0x6E0DFD, "[UI] coin current value Y-Axis", 0)
    idc.set_name(0x6E0DFD, "ui_6E0DFD", idaapi.SN_NOWARN)
    # 6E0E02: coin current value X-Axis
    idc.set_cmt(0x6E0E02, "[UI] coin current value X-Axis", 0)
    idc.set_name(0x6E0E02, "ui_6E0E02", idaapi.SN_NOWARN)
    # 6E0E11: coin box bg X-Axis
    idc.set_cmt(0x6E0E11, "[UI] coin box bg X-Axis", 0)
    idc.set_name(0x6E0E11, "ui_6E0E11", idaapi.SN_NOWARN)
    # 6E0E18: coin box bg Y-Axis
    idc.set_cmt(0x6E0E18, "[UI] coin box bg Y-Axis", 0)
    idc.set_name(0x6E0E18, "ui_6E0E18", idaapi.SN_NOWARN)
    # 6E139C: status/cure/ether sub menu names spacing Y-Axis - 
    idc.set_cmt(0x6E139C, "[UI] status/cure/ether sub menu names spacing Y-Axis - C9 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6E139C, "ui_6E139C", idaapi.SN_NOWARN)
    # 6E13A1: status/cure/ether sub menu names Y-Axis
    idc.set_cmt(0x6E13A1, "[UI] status/cure/ether sub menu names Y-Axis", 0)
    idc.set_name(0x6E13A1, "ui_6E13A1", idaapi.SN_NOWARN)
    # 6E13A2: remove status/cure/ether sub menu names
    idc.set_cmt(0x6E13A2, "[UI] remove status/cure/ether sub menu names", 0)
    idc.set_name(0x6E13A2, "ui_6E13A2", idaapi.SN_NOWARN)
    # 6E13A7: status/cure/ether sub menu names X-Axis
    idc.set_cmt(0x6E13A7, "[UI] status/cure/ether sub menu names X-Axis", 0)
    idc.set_name(0x6E13A7, "ui_6E13A7", idaapi.SN_NOWARN)
    # 6E1412: menu stuff merged
    idc.set_cmt(0x6E1412, "[UI] menu stuff merged", 0)
    idc.set_name(0x6E1412, "ui_6E1412", idaapi.SN_NOWARN)
    # 6E1487: cure sub menu alive hp spacing Y-Axis - set middle
    idc.set_cmt(0x6E1487, "[UI] cure sub menu alive hp spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E1487, "ui_6E1487", idaapi.SN_NOWARN)
    # 6E148C: cure sub menu alive hp Y-Axis
    idc.set_cmt(0x6E148C, "[UI] cure sub menu alive hp Y-Axis", 0)
    idc.set_name(0x6E148C, "ui_6E148C", idaapi.SN_NOWARN)
    # 6E148D: remove cure sub menu alive hp
    idc.set_cmt(0x6E148D, "[UI] remove cure sub menu alive hp", 0)
    idc.set_name(0x6E148D, "ui_6E148D", idaapi.SN_NOWARN)
    # 6E1492: cure sub menu alive hp X-Axis
    idc.set_cmt(0x6E1492, "[UI] cure sub menu alive hp X-Axis", 0)
    idc.set_name(0x6E1492, "ui_6E1492", idaapi.SN_NOWARN)
    # 6E14BC: cure sub menu dead hp spacing Y-Axis - set middle 
    idc.set_cmt(0x6E14BC, "[UI] cure sub menu dead hp spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E14BC, "ui_6E14BC", idaapi.SN_NOWARN)
    # 6E14C1: cure sub menu dead hp Y-Axis
    idc.set_cmt(0x6E14C1, "[UI] cure sub menu dead hp Y-Axis", 0)
    idc.set_name(0x6E14C1, "ui_6E14C1", idaapi.SN_NOWARN)
    # 6E14C2: remove cure sub menu dead hp
    idc.set_cmt(0x6E14C2, "[UI] remove cure sub menu dead hp", 0)
    idc.set_name(0x6E14C2, "ui_6E14C2", idaapi.SN_NOWARN)
    # 6E14C7: cure sub menu dead hp X-Axis
    idc.set_cmt(0x6E14C7, "[UI] cure sub menu dead hp X-Axis", 0)
    idc.set_name(0x6E14C7, "ui_6E14C7", idaapi.SN_NOWARN)
    # 6E14DD: cure sub menu hp divider color pallette
    idc.set_cmt(0x6E14DD, "[UI] cure sub menu hp divider color pallette", 0)
    idc.set_name(0x6E14DD, "ui_6E14DD", idaapi.SN_NOWARN)
    # 6E14ED: cure sub menu hp divider spacing Y-Axis - C0 middl
    idc.set_cmt(0x6E14ED, "[UI] cure sub menu hp divider spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6E14ED, "ui_6E14ED", idaapi.SN_NOWARN)
    # 6E14F1: cure sub menu hp divider Y-Axis
    idc.set_cmt(0x6E14F1, "[UI] cure sub menu hp divider Y-Axis", 0)
    idc.set_name(0x6E14F1, "ui_6E14F1", idaapi.SN_NOWARN)
    # 6E14F2: remove cure sub menu hp divider
    idc.set_cmt(0x6E14F2, "[UI] remove cure sub menu hp divider", 0)
    idc.set_name(0x6E14F2, "ui_6E14F2", idaapi.SN_NOWARN)
    # 6E14F7: cure sub menu hp divider X-Axis
    idc.set_cmt(0x6E14F7, "[UI] cure sub menu hp divider X-Axis", 0)
    idc.set_name(0x6E14F7, "ui_6E14F7", idaapi.SN_NOWARN)
    # 6E1530: cure sub menu maxhp spacing Y-Axis - set middle to
    idc.set_cmt(0x6E1530, "[UI] cure sub menu maxhp spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E1530, "ui_6E1530", idaapi.SN_NOWARN)
    # 6E1535: cure sub menu maxhp Y-Axis
    idc.set_cmt(0x6E1535, "[UI] cure sub menu maxhp Y-Axis", 0)
    idc.set_name(0x6E1535, "ui_6E1535", idaapi.SN_NOWARN)
    # 6E1536: remove cure sub menu maxhp
    idc.set_cmt(0x6E1536, "[UI] remove cure sub menu maxhp", 0)
    idc.set_name(0x6E1536, "ui_6E1536", idaapi.SN_NOWARN)
    # 6E153B: cure sub menu maxhp X-Axis
    idc.set_cmt(0x6E153B, "[UI] cure sub menu maxhp X-Axis", 0)
    idc.set_name(0x6E153B, "ui_6E153B", idaapi.SN_NOWARN)
    # 6E154B: cure sub menu hp bar X-Axis
    idc.set_cmt(0x6E154B, "[UI] cure sub menu hp bar X-Axis", 0)
    idc.set_name(0x6E154B, "ui_6E154B", idaapi.SN_NOWARN)
    # 6E1551: cure sub menu hp bar spacing Y-Axis - C0 middle th
    idc.set_cmt(0x6E1551, "[UI] cure sub menu hp bar spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6E1551, "ui_6E1551", idaapi.SN_NOWARN)
    # 6E1555: cure sub menu hp bar Y-Axis
    idc.set_cmt(0x6E1555, "[UI] cure sub menu hp bar Y-Axis", 0)
    idc.set_name(0x6E1555, "ui_6E1555", idaapi.SN_NOWARN)
    # 6E1556: remove cure sub menu hp bar
    idc.set_cmt(0x6E1556, "[UI] remove cure sub menu hp bar", 0)
    idc.set_name(0x6E1556, "ui_6E1556", idaapi.SN_NOWARN)
    # 6E1561: cure sub menu hp bar length X-Axis
    idc.set_cmt(0x6E1561, "[UI] cure sub menu hp bar length X-Axis", 0)
    idc.set_name(0x6E1561, "ui_6E1561", idaapi.SN_NOWARN)
    # 6E1626: ether sub menu alive mp spacing Y-Axis - set middl
    idc.set_cmt(0x6E1626, "[UI] ether sub menu alive mp spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E1626, "ui_6E1626", idaapi.SN_NOWARN)
    # 6E162B: ether sub menu alive mp Y-Axis
    idc.set_cmt(0x6E162B, "[UI] ether sub menu alive mp Y-Axis", 0)
    idc.set_name(0x6E162B, "ui_6E162B", idaapi.SN_NOWARN)
    # 6E162C: remove ether sub menu alive mp
    idc.set_cmt(0x6E162C, "[UI] remove ether sub menu alive mp", 0)
    idc.set_name(0x6E162C, "ui_6E162C", idaapi.SN_NOWARN)
    # 6E1631: ether sub menu alive mp X-Axis
    idc.set_cmt(0x6E1631, "[UI] ether sub menu alive mp X-Axis", 0)
    idc.set_name(0x6E1631, "ui_6E1631", idaapi.SN_NOWARN)
    # 6E165B: ether sub menu dead mp spacing Y-Axis - set middle
    idc.set_cmt(0x6E165B, "[UI] ether sub menu dead mp spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E165B, "ui_6E165B", idaapi.SN_NOWARN)
    # 6E1660: ether sub menu dead mp Y-Axis
    idc.set_cmt(0x6E1660, "[UI] ether sub menu dead mp Y-Axis", 0)
    idc.set_name(0x6E1660, "ui_6E1660", idaapi.SN_NOWARN)
    # 6E1661: remove ether sub menu dead mp
    idc.set_cmt(0x6E1661, "[UI] remove ether sub menu dead mp", 0)
    idc.set_name(0x6E1661, "ui_6E1661", idaapi.SN_NOWARN)
    # 6E1666: ether sub menu dead mp X-Axis
    idc.set_cmt(0x6E1666, "[UI] ether sub menu dead mp X-Axis", 0)
    idc.set_name(0x6E1666, "ui_6E1666", idaapi.SN_NOWARN)
    # 6E167C: ether sub menu mp divider color pallette
    idc.set_cmt(0x6E167C, "[UI] ether sub menu mp divider color pallette", 0)
    idc.set_name(0x6E167C, "ui_6E167C", idaapi.SN_NOWARN)
    # 6E168C: ether sub menu mp divider spacing Y-Axis - C0 midd
    idc.set_cmt(0x6E168C, "[UI] ether sub menu mp divider spacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6E168C, "ui_6E168C", idaapi.SN_NOWARN)
    # 6E1690: ether sub menu mp divider Y-Axis
    idc.set_cmt(0x6E1690, "[UI] ether sub menu mp divider Y-Axis", 0)
    idc.set_name(0x6E1690, "ui_6E1690", idaapi.SN_NOWARN)
    # 6E1691: remove ether sub menu mp divider
    idc.set_cmt(0x6E1691, "[UI] remove ether sub menu mp divider", 0)
    idc.set_name(0x6E1691, "ui_6E1691", idaapi.SN_NOWARN)
    # 6E1696: ether sub menu mp divider X-Axis
    idc.set_cmt(0x6E1696, "[UI] ether sub menu mp divider X-Axis", 0)
    idc.set_name(0x6E1696, "ui_6E1696", idaapi.SN_NOWARN)
    # 6E16CF: ether sub menu maxmp spacing Y-Axis - set middle t
    idc.set_cmt(0x6E16CF, "[UI] ether sub menu maxmp spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E16CF, "ui_6E16CF", idaapi.SN_NOWARN)
    # 6E16D4: ether sub menu maxmp Y-Axis
    idc.set_cmt(0x6E16D4, "[UI] ether sub menu maxmp Y-Axis", 0)
    idc.set_name(0x6E16D4, "ui_6E16D4", idaapi.SN_NOWARN)
    # 6E16D5: remove ether sub menu maxmp
    idc.set_cmt(0x6E16D5, "[UI] remove ether sub menu maxmp", 0)
    idc.set_name(0x6E16D5, "ui_6E16D5", idaapi.SN_NOWARN)
    # 6E16DA: ether sub menu maxmp X-Axis
    idc.set_cmt(0x6E16DA, "[UI] ether sub menu maxmp X-Axis", 0)
    idc.set_name(0x6E16DA, "ui_6E16DA", idaapi.SN_NOWARN)
    # 6E16EA: ether sub menu mp bars X-Axis
    idc.set_cmt(0x6E16EA, "[UI] ether sub menu mp bars X-Axis", 0)
    idc.set_name(0x6E16EA, "ui_6E16EA", idaapi.SN_NOWARN)
    # 6E16F0: ether sub menu mp bars spaacing Y-Axis - C0 middle
    idc.set_cmt(0x6E16F0, "[UI] ether sub menu mp bars spaacing Y-Axis - C0 middle then 6B first then 3rd value", 0)
    idc.set_name(0x6E16F0, "ui_6E16F0", idaapi.SN_NOWARN)
    # 6E16F4: ether sub menu mp bars Y-Axis
    idc.set_cmt(0x6E16F4, "[UI] ether sub menu mp bars Y-Axis", 0)
    idc.set_name(0x6E16F4, "ui_6E16F4", idaapi.SN_NOWARN)
    # 6E16F5: remove ether sub menu mp bars
    idc.set_cmt(0x6E16F5, "[UI] remove ether sub menu mp bars", 0)
    idc.set_name(0x6E16F5, "ui_6E16F5", idaapi.SN_NOWARN)
    # 6E1700: ether sub menu mp bars length X-Axis
    idc.set_cmt(0x6E1700, "[UI] ether sub menu mp bars length X-Axis", 0)
    idc.set_name(0x6E1700, "ui_6E1700", idaapi.SN_NOWARN)
    # 6E1792: slow down status rotation, will still speed up whe
    idc.set_cmt(0x6E1792, "[UI] slow down status rotation, will still speed up when is a lot of status on character", 0)
    idc.set_name(0x6E1792, "ui_6E1792", idaapi.SN_NOWARN)
    # 6E185E: status sub menu status spacing Y-Axis - set middle
    idc.set_cmt(0x6E185E, "[UI] status sub menu status spacing Y-Axis - set middle to D2, then first to 6B, then third as value", 0)
    idc.set_name(0x6E185E, "ui_6E185E", idaapi.SN_NOWARN)
    # 6E1863: status sub menu status Y-Axis
    idc.set_cmt(0x6E1863, "[UI] status sub menu status Y-Axis", 0)
    idc.set_name(0x6E1863, "ui_6E1863", idaapi.SN_NOWARN)
    # 6E1869: status sub menu status X-Axis
    idc.set_cmt(0x6E1869, "[UI] status sub menu status X-Axis", 0)
    idc.set_name(0x6E1869, "ui_6E1869", idaapi.SN_NOWARN)
    # 6E1891: status/cure/ether sub menu name header Y-Axis
    idc.set_cmt(0x6E1891, "[UI] status/cure/ether sub menu name header Y-Axis", 0)
    idc.set_name(0x6E1891, "ui_6E1891", idaapi.SN_NOWARN)
    # 6E1892: all sub boxes
    idc.set_cmt(0x6E1892, "[UI] all sub boxes", 0)
    idc.set_name(0x6E1892, "ui_6E1892", idaapi.SN_NOWARN)
    # 6E1896: status/cure/ether sub menu name header X-Axis
    idc.set_cmt(0x6E1896, "[UI] status/cure/ether sub menu name header X-Axis", 0)
    idc.set_name(0x6E1896, "ui_6E1896", idaapi.SN_NOWARN)
    # 6E18D4: cure sub menu hp header Y-Axis
    idc.set_cmt(0x6E18D4, "[UI] cure sub menu hp header Y-Axis", 0)
    idc.set_name(0x6E18D4, "ui_6E18D4", idaapi.SN_NOWARN)
    # 6E18D5: remove cure sub menu hp header
    idc.set_cmt(0x6E18D5, "[UI] remove cure sub menu hp header", 0)
    idc.set_name(0x6E18D5, "ui_6E18D5", idaapi.SN_NOWARN)
    # 6E18D9: cure sub menu hp header X-Axis
    idc.set_cmt(0x6E18D9, "[UI] cure sub menu hp header X-Axis", 0)
    idc.set_name(0x6E18D9, "ui_6E18D9", idaapi.SN_NOWARN)
    # 6E18FB: ether sub menu mp header Y-Axis
    idc.set_cmt(0x6E18FB, "[UI] ether sub menu mp header Y-Axis", 0)
    idc.set_name(0x6E18FB, "ui_6E18FB", idaapi.SN_NOWARN)
    # 6E18FC: remove ether sub menu mp header
    idc.set_cmt(0x6E18FC, "[UI] remove ether sub menu mp header", 0)
    idc.set_name(0x6E18FC, "ui_6E18FC", idaapi.SN_NOWARN)
    # 6E1900: ether sub menu mp header X-Axis
    idc.set_cmt(0x6E1900, "[UI] ether sub menu mp header X-Axis", 0)
    idc.set_name(0x6E1900, "ui_6E1900", idaapi.SN_NOWARN)
    # 6E1925: status sub menu status header Y-Axis
    idc.set_cmt(0x6E1925, "[UI] status sub menu status header Y-Axis", 0)
    idc.set_name(0x6E1925, "ui_6E1925", idaapi.SN_NOWARN)
    # 6E1926: remove status sub menu status header
    idc.set_cmt(0x6E1926, "[UI] remove status sub menu status header", 0)
    idc.set_name(0x6E1926, "ui_6E1926", idaapi.SN_NOWARN)
    # 6E192A: status sub menu status header X-Axis
    idc.set_cmt(0x6E192A, "[UI] status sub menu status header X-Axis", 0)
    idc.set_name(0x6E192A, "ui_6E192A", idaapi.SN_NOWARN)
    # 6E200E: manip text spacing Y-Axis
    idc.set_cmt(0x6E200E, "[UI] manip text spacing Y-Axis", 0)
    idc.set_name(0x6E200E, "ui_6E200E", idaapi.SN_NOWARN)
    # 6E2014: manip text Y-Axis
    idc.set_cmt(0x6E2014, "[UI] manip text Y-Axis", 0)
    idc.set_name(0x6E2014, "ui_6E2014", idaapi.SN_NOWARN)
    # 6E201A: manip text X-Axis
    idc.set_cmt(0x6E201A, "[UI] manip text X-Axis", 0)
    idc.set_name(0x6E201A, "ui_6E201A", idaapi.SN_NOWARN)
    # 6E2182: cait sith reels tint height
    idc.set_cmt(0x6E2182, "[UI] cait sith reels tint height", 0)
    idc.set_name(0x6E2182, "ui_6E2182", idaapi.SN_NOWARN)
    # 6E2189: cait sith reels Y-Axis
    idc.set_cmt(0x6E2189, "[UI] cait sith reels Y-Axis", 0)
    idc.set_name(0x6E2189, "ui_6E2189", idaapi.SN_NOWARN)
    # 6E2429: cait sith reels spinned icons Y-Axis
    idc.set_cmt(0x6E2429, "[UI] cait sith reels spinned icons Y-Axis", 0)
    idc.set_name(0x6E2429, "ui_6E2429", idaapi.SN_NOWARN)
    # 6E2447: remove main boxes and help box when cait sith reel
    idc.set_cmt(0x6E2447, "[UI] remove main boxes and help box when cait sith reel, and add back after", 0)
    idc.set_name(0x6E2447, "ui_6E2447", idaapi.SN_NOWARN)
    # 6E3162: remove main boxes and help box when tifa reel show
    idc.set_cmt(0x6E3162, "[UI] remove main boxes and help box when tifa reel shows", 0)
    idc.set_name(0x6E3162, "ui_6E3162", idaapi.SN_NOWARN)
    # 6E316D: tifa reels Y-Axis
    idc.set_cmt(0x6E316D, "[UI] tifa reels Y-Axis", 0)
    idc.set_name(0x6E316D, "ui_6E316D", idaapi.SN_NOWARN)
    # 6E325A: tifa reels spinned Y-Axis
    idc.set_cmt(0x6E325A, "[UI] tifa reels spinned Y-Axis", 0)
    idc.set_name(0x6E325A, "ui_6E325A", idaapi.SN_NOWARN)
    # 6E3892: battle square keep goin text Y-Axis
    idc.set_cmt(0x6E3892, "[UI] battle square keep goin text Y-Axis", 0)
    idc.set_name(0x6E3892, "ui_6E3892", idaapi.SN_NOWARN)
    # 6E3897: battle square keep goin text X-Axis
    idc.set_cmt(0x6E3897, "[UI] battle square keep goin text X-Axis", 0)
    idc.set_name(0x6E3897, "ui_6E3897", idaapi.SN_NOWARN)
    # 6E38AD: battle square of course text Y-Axis
    idc.set_cmt(0x6E38AD, "[UI] battle square of course text Y-Axis", 0)
    idc.set_name(0x6E38AD, "ui_6E38AD", idaapi.SN_NOWARN)
    # 6E38B2: battle square of course text X-Axis
    idc.set_cmt(0x6E38B2, "[UI] battle square of course text X-Axis", 0)
    idc.set_name(0x6E38B2, "ui_6E38B2", idaapi.SN_NOWARN)
    # 6E38F9: battle square current battle points text Y-Axis
    idc.set_cmt(0x6E38F9, "[UI] battle square current battle points text Y-Axis", 0)
    idc.set_name(0x6E38F9, "ui_6E38F9", idaapi.SN_NOWARN)
    # 6E38FE: battle square current battle points text X-Axis
    idc.set_cmt(0x6E38FE, "[UI] battle square current battle points text X-Axis", 0)
    idc.set_name(0x6E38FE, "ui_6E38FE", idaapi.SN_NOWARN)
    # 6E3918: battle square current battle points value Y-Axis
    idc.set_cmt(0x6E3918, "[UI] battle square current battle points value Y-Axis", 0)
    idc.set_name(0x6E3918, "ui_6E3918", idaapi.SN_NOWARN)
    # 6E391D: battle square current battle points value X-Axis
    idc.set_cmt(0x6E391D, "[UI] battle square current battle points value X-Axis", 0)
    idc.set_name(0x6E391D, "ui_6E391D", idaapi.SN_NOWARN)
    # 6E395B: battle square reel height
    idc.set_cmt(0x6E395B, "[UI] battle square reel height", 0)
    idc.set_name(0x6E395B, "ui_6E395B", idaapi.SN_NOWARN)
    # 6E3964: battle square reel Y-Axis
    idc.set_cmt(0x6E3964, "[UI] battle square reel Y-Axis", 0)
    idc.set_name(0x6E3964, "ui_6E3964", idaapi.SN_NOWARN)
    # 6E3A35: battle square reel spinned Y-Axis
    idc.set_cmt(0x6E3A35, "[UI] battle square reel spinned Y-Axis", 0)
    idc.set_name(0x6E3A35, "ui_6E3A35", idaapi.SN_NOWARN)
    # 6E3B8D: battle square slot start text Y-Axis
    idc.set_cmt(0x6E3B8D, "[UI] battle square slot start text Y-Axis", 0)
    idc.set_name(0x6E3B8D, "ui_6E3B8D", idaapi.SN_NOWARN)
    # 6E3BBB: battle square go for it text Y-Axis
    idc.set_cmt(0x6E3BBB, "[UI] battle square go for it text Y-Axis", 0)
    idc.set_name(0x6E3BBB, "ui_6E3BBB", idaapi.SN_NOWARN)
    # 6E3BC0: battle square go for it text X-Axis
    idc.set_cmt(0x6E3BC0, "[UI] battle square go for it text X-Axis", 0)
    idc.set_name(0x6E3BC0, "ui_6E3BC0", idaapi.SN_NOWARN)
    # 6E3C31: battle square status text Y-Axis
    idc.set_cmt(0x6E3C31, "[UI] battle square status text Y-Axis", 0)
    idc.set_name(0x6E3C31, "ui_6E3C31", idaapi.SN_NOWARN)
    # 6E3C35: battle square status text X-Axis Centred regardles
    idc.set_cmt(0x6E3C35, "[UI] battle square status text X-Axis Centred regardless of length - requires DLPB code, added in 09-DLPB", 0)
    idc.set_name(0x6E3C35, "ui_6E3C35", idaapi.SN_NOWARN)
    # 6E3C59: battle square great text Y-Axis
    idc.set_cmt(0x6E3C59, "[UI] battle square great text Y-Axis", 0)
    idc.set_name(0x6E3C59, "ui_6E3C59", idaapi.SN_NOWARN)
    # 6E4B4C: worried about other members text Y-Axis
    idc.set_cmt(0x6E4B4C, "[UI] worried about other members text Y-Axis", 0)
    idc.set_name(0x6E4B4C, "ui_6E4B4C", idaapi.SN_NOWARN)
    # 6E4B60: both choices yellow color pallete
    idc.set_cmt(0x6E4B60, "[UI] both choices yellow color pallete", 0)
    idc.set_name(0x6E4B60, "ui_6E4B60", idaapi.SN_NOWARN)
    # 6E4B67: yeah a little text Y-Axis
    idc.set_cmt(0x6E4B67, "[UI] yeah a little text Y-Axis", 0)
    idc.set_name(0x6E4B67, "ui_6E4B67", idaapi.SN_NOWARN)
    # 6E4B6C: yeah a little text X-Axis
    idc.set_cmt(0x6E4B6C, "[UI] yeah a little text X-Axis", 0)
    idc.set_name(0x6E4B6C, "ui_6E4B6C", idaapi.SN_NOWARN)
    # 6E4B82: not really text Y-Axis
    idc.set_cmt(0x6E4B82, "[UI] not really text Y-Axis", 0)
    idc.set_name(0x6E4B82, "ui_6E4B82", idaapi.SN_NOWARN)
    # 6E4B8C: not really text X-Axis
    idc.set_cmt(0x6E4B8C, "[UI] not really text X-Axis", 0)
    idc.set_name(0x6E4B8C, "ui_6E4B8C", idaapi.SN_NOWARN)
    # 6E7117: dialog spacing Y-Axis, both values
    idc.set_cmt(0x6E7117, "[UI] dialog spacing Y-Axis, both values", 0)
    idc.set_name(0x6E7117, "ui_6E7117", idaapi.SN_NOWARN)
    # 6EB022: Add transparency support for FIELD dialogs - trueo
    idc.set_cmt(0x6EB022, "[UI] Add transparency support for FIELD dialogs - trueodin", 0)
    idc.set_name(0x6EB022, "ui_6EB022", idaapi.SN_NOWARN)
    # 6EC0B0: field message box scrolling viewing offset Y-Axis 
    idc.set_cmt(0x6EC0B0, "[UI] field message box scrolling viewing offset Y-Axis 9139FC to change value", 0)
    idc.set_name(0x6EC0B0, "ui_6EC0B0", idaapi.SN_NOWARN)
    # 6EC284: dialog text Y-Axis offset
    idc.set_cmt(0x6EC284, "[UI] dialog text Y-Axis offset", 0)
    idc.set_name(0x6EC284, "ui_6EC284", idaapi.SN_NOWARN)
    # 6F6377: main menu (OR ALL UI?) - LV HP MP spacing X-Axis
    idc.set_cmt(0x6F6377, "[UI] main menu (OR ALL UI?) - LV HP MP spacing X-Axis", 0)
    idc.set_name(0x6F6377, "ui_6F6377", idaapi.SN_NOWARN)
    # 6F984C: all menus (NOT BATTLE) - All but last digits spaci
    idc.set_cmt(0x6F984C, "[UI] all menus (NOT BATTLE) - All but last digits spacing X-Axis", 0)
    idc.set_name(0x6F984C, "ui_6F984C", idaapi.SN_NOWARN)
    # 6F9860: All but last digits spacing X-Axis
    idc.set_cmt(0x6F9860, "[UI] All but last digits spacing X-Axis", 0)
    idc.set_name(0x6F9860, "ui_6F9860", idaapi.SN_NOWARN)
    # 6F9A87: all menus (NOT BATTLE) - last digits spacing X-Axi
    idc.set_cmt(0x6F9A87, "[UI] all menus (NOT BATTLE) - last digits spacing X-Axis", 0)
    idc.set_name(0x6F9A87, "ui_6F9A87", idaapi.SN_NOWARN)
    # 6F9A9B: last digits spacing X-Axis
    idc.set_cmt(0x6F9A9B, "[UI] last digits spacing X-Axis", 0)
    idc.set_name(0x6F9A9B, "ui_6F9A9B", idaapi.SN_NOWARN)
    # 6F9D28: materia effect - all but last digits spacing X-Axi
    idc.set_cmt(0x6F9D28, "[UI] materia effect - all but last digits spacing X-Axis", 0)
    idc.set_name(0x6F9D28, "ui_6F9D28", idaapi.SN_NOWARN)
    # 6F9F69: materia effect - last digits spacing X-Axis
    idc.set_cmt(0x6F9F69, "[UI] materia effect - last digits spacing X-Axis", 0)
    idc.set_name(0x6F9F69, "ui_6F9F69", idaapi.SN_NOWARN)
    # 6FEEA4: save file select cursor spacing Y-Axis
    idc.set_cmt(0x6FEEA4, "[UI] save file select cursor spacing Y-Axis", 0)
    idc.set_name(0x6FEEA4, "ui_6FEEA4", idaapi.SN_NOWARN)
    # 6FEEB9: save file select cursor spacing X-Axis
    idc.set_cmt(0x6FEEB9, "[UI] save file select cursor spacing X-Axis", 0)
    idc.set_name(0x6FEEB9, "ui_6FEEB9", idaapi.SN_NOWARN)
    # 6FEEBD: save file select cursor X-Axis
    idc.set_cmt(0x6FEEBD, "[UI] save file select cursor X-Axis", 0)
    idc.set_name(0x6FEEBD, "ui_6FEEBD", idaapi.SN_NOWARN)
    # 6FEED6: save select text X-Axis
    idc.set_cmt(0x6FEED6, "[UI] save select text X-Axis", 0)
    idc.set_name(0x6FEED6, "ui_6FEED6", idaapi.SN_NOWARN)
    # 6FEF42: save file select box text Y-Axis
    idc.set_cmt(0x6FEF42, "[UI] save file select box text Y-Axis", 0)
    idc.set_name(0x6FEF42, "ui_6FEF42", idaapi.SN_NOWARN)
    # 6FEF51: save file select box text X-Axis
    idc.set_cmt(0x6FEF51, "[UI] save file select box text X-Axis", 0)
    idc.set_name(0x6FEF51, "ui_6FEF51", idaapi.SN_NOWARN)
    # 6FF0C1: save game ghost cursor Y-Axis
    idc.set_cmt(0x6FF0C1, "[UI] save game ghost cursor Y-Axis", 0)
    idc.set_name(0x6FF0C1, "ui_6FF0C1", idaapi.SN_NOWARN)
    # 6FF0C4: save game ghost cursor X-Axis
    idc.set_cmt(0x6FF0C4, "[UI] save game ghost cursor X-Axis", 0)
    idc.set_name(0x6FF0C4, "ui_6FF0C4", idaapi.SN_NOWARN)
    # 6FF0DF: save game cursor Y-Axis
    idc.set_cmt(0x6FF0DF, "[UI] save game cursor Y-Axis", 0)
    idc.set_name(0x6FF0DF, "ui_6FF0DF", idaapi.SN_NOWARN)
    # 6FF0E2: save game cursor X-Axis
    idc.set_cmt(0x6FF0E2, "[UI] save game cursor X-Axis", 0)
    idc.set_name(0x6FF0E2, "ui_6FF0E2", idaapi.SN_NOWARN)
    # 6FF226: save game WORD X-Axis
    idc.set_cmt(0x6FF226, "[UI] save game WORD X-Axis", 0)
    idc.set_name(0x6FF226, "ui_6FF226", idaapi.SN_NOWARN)
    # 6FF25F: save game number X-Axis
    idc.set_cmt(0x6FF25F, "[UI] save game number X-Axis", 0)
    idc.set_name(0x6FF25F, "ui_6FF25F", idaapi.SN_NOWARN)
    # 6FF2C1: save select alt text X-Axis
    idc.set_cmt(0x6FF2C1, "[UI] save select alt text X-Axis", 0)
    idc.set_name(0x6FF2C1, "ui_6FF2C1", idaapi.SN_NOWARN)
    # 6FF386: Saving Box Text X-Axis
    idc.set_cmt(0x6FF386, "[UI] Saving Box Text X-Axis", 0)
    idc.set_name(0x6FF386, "ui_6FF386", idaapi.SN_NOWARN)
    # 7000D6: right box - weapon text X-Axis
    idc.set_cmt(0x7000D6, "[UI] right box - weapon text X-Axis", 0)
    idc.set_name(0x7000D6, "ui_7000D6", idaapi.SN_NOWARN)
    # 700115: right box - armour text X-Axis
    idc.set_cmt(0x700115, "[UI] right box - armour text X-Axis", 0)
    idc.set_name(0x700115, "ui_700115", idaapi.SN_NOWARN)
    # 700171: right box - accessory text X-Axis
    idc.set_cmt(0x700171, "[UI] right box - accessory text X-Axis", 0)
    idc.set_name(0x700171, "ui_700171", idaapi.SN_NOWARN)
    # 700190: right box - Wpn WORD X-Axis
    idc.set_cmt(0x700190, "[UI] right box - Wpn WORD X-Axis", 0)
    idc.set_name(0x700190, "ui_700190", idaapi.SN_NOWARN)
    # 7001B2: right box - Arm WORD X-Axis
    idc.set_cmt(0x7001B2, "[UI] right box - Arm WORD X-Axis", 0)
    idc.set_name(0x7001B2, "ui_7001B2", idaapi.SN_NOWARN)
    # 7001D7: right box - Acc WORD X-Axis
    idc.set_cmt(0x7001D7, "[UI] right box - Acc WORD X-Axis", 0)
    idc.set_name(0x7001D7, "ui_7001D7", idaapi.SN_NOWARN)
    # 700212: right box - weapon slots/box Y-Axis
    idc.set_cmt(0x700212, "[UI] right box - weapon slots/box Y-Axis", 0)
    idc.set_name(0x700212, "ui_700212", idaapi.SN_NOWARN)
    # 700219: right box - weapon slots/box X-Axis
    idc.set_cmt(0x700219, "[UI] right box - weapon slots/box X-Axis", 0)
    idc.set_name(0x700219, "ui_700219", idaapi.SN_NOWARN)
    # 700255: right box - armour slots/box Y-Axis
    idc.set_cmt(0x700255, "[UI] right box - armour slots/box Y-Axis", 0)
    idc.set_name(0x700255, "ui_700255", idaapi.SN_NOWARN)
    # 70025C: right box - armour slots/box X-Axis
    idc.set_cmt(0x70025C, "[UI] right box - armour slots/box X-Axis", 0)
    idc.set_name(0x70025C, "ui_70025C", idaapi.SN_NOWARN)
    # 7003F8: Materia slots BG Width
    idc.set_cmt(0x7003F8, "[UI] Materia slots BG Width", 0)
    idc.set_name(0x7003F8, "ui_7003F8", idaapi.SN_NOWARN)
    # 7003FE: Materia slots BG Height
    idc.set_cmt(0x7003FE, "[UI] Materia slots BG Height", 0)
    idc.set_name(0x7003FE, "ui_7003FE", idaapi.SN_NOWARN)
    # 70121F: left box - ghost cursor Y-Axis
    idc.set_cmt(0x70121F, "[UI] left box - ghost cursor Y-Axis", 0)
    idc.set_name(0x70121F, "ui_70121F", idaapi.SN_NOWARN)
    # 701222: left box - ghost cursor X-Axis
    idc.set_cmt(0x701222, "[UI] left box - ghost cursor X-Axis", 0)
    idc.set_name(0x701222, "ui_701222", idaapi.SN_NOWARN)
    # 701252: right box - ghost cursor Y-Axis
    idc.set_cmt(0x701252, "[UI] right box - ghost cursor Y-Axis", 0)
    idc.set_name(0x701252, "ui_701252", idaapi.SN_NOWARN)
    # 701265: right box - ghost cursor spacing X-Axis
    idc.set_cmt(0x701265, "[UI] right box - ghost cursor spacing X-Axis", 0)
    idc.set_name(0x701265, "ui_701265", idaapi.SN_NOWARN)
    # 701269: right box - ghost cursor X-Axis
    idc.set_cmt(0x701269, "[UI] right box - ghost cursor X-Axis", 0)
    idc.set_name(0x701269, "ui_701269", idaapi.SN_NOWARN)
    # 7012E0: right box - cursor Y-Axis
    idc.set_cmt(0x7012E0, "[UI] right box - cursor Y-Axis", 0)
    idc.set_name(0x7012E0, "ui_7012E0", idaapi.SN_NOWARN)
    # 7012F3: right box - cursor spacing X-Axis
    idc.set_cmt(0x7012F3, "[UI] right box - cursor spacing X-Axis", 0)
    idc.set_name(0x7012F3, "ui_7012F3", idaapi.SN_NOWARN)
    # 7012F7: right box - cursor X-Axis
    idc.set_cmt(0x7012F7, "[UI] right box - cursor X-Axis", 0)
    idc.set_name(0x7012F7, "ui_7012F7", idaapi.SN_NOWARN)
    # 701338: top box lv/hp/mp block Y-Axis
    idc.set_cmt(0x701338, "[UI] top box lv/hp/mp block Y-Axis", 0)
    idc.set_name(0x701338, "ui_701338", idaapi.SN_NOWARN)
    # 701345: top box lv/hp/mp block X-Axis
    idc.set_cmt(0x701345, "[UI] top box lv/hp/mp block X-Axis", 0)
    idc.set_name(0x701345, "ui_701345", idaapi.SN_NOWARN)
    # 701375: top box avatar Y-Axis
    idc.set_cmt(0x701375, "[UI] top box avatar Y-Axis", 0)
    idc.set_name(0x701375, "ui_701375", idaapi.SN_NOWARN)
    # 701383: top box avatar X-Axis
    idc.set_cmt(0x701383, "[UI] top box avatar X-Axis", 0)
    idc.set_name(0x701383, "ui_701383", idaapi.SN_NOWARN)
    # 7013CE: top box selected lv/hp/mp block Y-Axis
    idc.set_cmt(0x7013CE, "[UI] top box selected lv/hp/mp block Y-Axis", 0)
    idc.set_name(0x7013CE, "ui_7013CE", idaapi.SN_NOWARN)
    # 7013DB: top box selected lv/hp/mp block X-Axis
    idc.set_cmt(0x7013DB, "[UI] top box selected lv/hp/mp block X-Axis", 0)
    idc.set_name(0x7013DB, "ui_7013DB", idaapi.SN_NOWARN)
    # 70140A: top box selected avatar Y-Axis
    idc.set_cmt(0x70140A, "[UI] top box selected avatar Y-Axis", 0)
    idc.set_name(0x70140A, "ui_70140A", idaapi.SN_NOWARN)
    # 701418: top box selected avatar X-Axis
    idc.set_cmt(0x701418, "[UI] top box selected avatar X-Axis", 0)
    idc.set_name(0x701418, "ui_701418", idaapi.SN_NOWARN)
    # 701510: right box contents spacing X-Axis
    idc.set_cmt(0x701510, "[UI] right box contents spacing X-Axis", 0)
    idc.set_name(0x701510, "ui_701510", idaapi.SN_NOWARN)
    # 7015C3: left box - avatar Y-Axis
    idc.set_cmt(0x7015C3, "[UI] left box - avatar Y-Axis", 0)
    idc.set_name(0x7015C3, "ui_7015C3", idaapi.SN_NOWARN)
    # 7015C6: left box - avatar X-Axis
    idc.set_cmt(0x7015C6, "[UI] left box - avatar X-Axis", 0)
    idc.set_name(0x7015C6, "ui_7015C6", idaapi.SN_NOWARN)
    # 701B7A: right box - exp bar Height
    idc.set_cmt(0x701B7A, "[UI] right box - exp bar Height", 0)
    idc.set_name(0x701B7A, "ui_701B7A", idaapi.SN_NOWARN)
    # 701B86: right box - exp bar width
    idc.set_cmt(0x701B86, "[UI] right box - exp bar width", 0)
    idc.set_name(0x701B86, "ui_701B86", idaapi.SN_NOWARN)
    # 701B94: right box - exp bar Y-Axis
    idc.set_cmt(0x701B94, "[UI] right box - exp bar Y-Axis", 0)
    idc.set_name(0x701B94, "ui_701B94", idaapi.SN_NOWARN)
    # 701B97: right box - exp bar X-Axis
    idc.set_cmt(0x701B97, "[UI] right box - exp bar X-Axis", 0)
    idc.set_name(0x701B97, "ui_701B97", idaapi.SN_NOWARN)
    # 701BBE: right box - exp box Y-Axis
    idc.set_cmt(0x701BBE, "[UI] right box - exp box Y-Axis", 0)
    idc.set_name(0x701BBE, "ui_701BBE", idaapi.SN_NOWARN)
    # 701BC1: right box - exp box X-Axis
    idc.set_cmt(0x701BC1, "[UI] right box - exp box X-Axis", 0)
    idc.set_name(0x701BC1, "ui_701BC1", idaapi.SN_NOWARN)
    # 701BEB: right box - exp p X-Axis
    idc.set_cmt(0x701BEB, "[UI] right box - exp p X-Axis", 0)
    idc.set_name(0x701BEB, "ui_701BEB", idaapi.SN_NOWARN)
    # 701C15: right box - next level p X-Axis
    idc.set_cmt(0x701C15, "[UI] right box - next level p X-Axis", 0)
    idc.set_name(0x701C15, "ui_701C15", idaapi.SN_NOWARN)
    # 701C46: right box - exp number X-Axis
    idc.set_cmt(0x701C46, "[UI] right box - exp number X-Axis", 0)
    idc.set_name(0x701C46, "ui_701C46", idaapi.SN_NOWARN)
    # 701C77: right box - next level number X-Axis
    idc.set_cmt(0x701C77, "[UI] right box - next level number X-Axis", 0)
    idc.set_name(0x701C77, "ui_701C77", idaapi.SN_NOWARN)
    # 701CA6: right box - EXP: WORD X-Axis
    idc.set_cmt(0x701CA6, "[UI] right box - EXP: WORD X-Axis", 0)
    idc.set_name(0x701CA6, "ui_701CA6", idaapi.SN_NOWARN)
    # 701CEE: right box - next level: WORD X-Axis
    idc.set_cmt(0x701CEE, "[UI] right box - next level: WORD X-Axis", 0)
    idc.set_name(0x701CEE, "ui_701CEE", idaapi.SN_NOWARN)
    # 702242: limit menu set cursor Y-Axis
    idc.set_cmt(0x702242, "[UI] limit menu set cursor Y-Axis", 0)
    idc.set_name(0x702242, "ui_702242", idaapi.SN_NOWARN)
    # 7022E9: limit menu check cursor Y-Axis
    idc.set_cmt(0x7022E9, "[UI] limit menu check cursor Y-Axis", 0)
    idc.set_name(0x7022E9, "ui_7022E9", idaapi.SN_NOWARN)
    # 702370: limit menu check nested cursor spacing Y-Axis
    idc.set_cmt(0x702370, "[UI] limit menu check nested cursor spacing Y-Axis", 0)
    idc.set_name(0x702370, "ui_702370", idaapi.SN_NOWARN)
    # 702374: limit menu check nested cursor Y-Axis
    idc.set_cmt(0x702374, "[UI] limit menu check nested cursor Y-Axis", 0)
    idc.set_name(0x702374, "ui_702374", idaapi.SN_NOWARN)
    # 702384: limit menu check nested cursor X-Axis
    idc.set_cmt(0x702384, "[UI] limit menu check nested cursor X-Axis", 0)
    idc.set_name(0x702384, "ui_702384", idaapi.SN_NOWARN)
    # 70240D: limit menu change box cursor spacing Y-Axis
    idc.set_cmt(0x70240D, "[UI] limit menu change box cursor spacing Y-Axis", 0)
    idc.set_name(0x70240D, "ui_70240D", idaapi.SN_NOWARN)
    # 702411: limit menu change box cursor Y-Axis
    idc.set_cmt(0x702411, "[UI] limit menu change box cursor Y-Axis", 0)
    idc.set_name(0x702411, "ui_702411", idaapi.SN_NOWARN)
    # 70241F: limit menu change box cursor X-Axis
    idc.set_cmt(0x70241F, "[UI] limit menu change box cursor X-Axis", 0)
    idc.set_name(0x70241F, "ui_70241F", idaapi.SN_NOWARN)
    # 70243E: limit menu change text first line Y-Axis
    idc.set_cmt(0x70243E, "[UI] limit menu change text first line Y-Axis", 0)
    idc.set_name(0x70243E, "ui_70243E", idaapi.SN_NOWARN)
    # 70244B: limit menu change text first line X-Axis
    idc.set_cmt(0x70244B, "[UI] limit menu change text first line X-Axis", 0)
    idc.set_name(0x70244B, "ui_70244B", idaapi.SN_NOWARN)
    # 70246A: limit menu change text second line Y-Axis
    idc.set_cmt(0x70246A, "[UI] limit menu change text second line Y-Axis", 0)
    idc.set_name(0x70246A, "ui_70246A", idaapi.SN_NOWARN)
    # 702478: limit menu change text second line X-Axis
    idc.set_cmt(0x702478, "[UI] limit menu change text second line X-Axis", 0)
    idc.set_name(0x702478, "ui_702478", idaapi.SN_NOWARN)
    # 702496: limit menu change text third line Y-Axis
    idc.set_cmt(0x702496, "[UI] limit menu change text third line Y-Axis", 0)
    idc.set_name(0x702496, "ui_702496", idaapi.SN_NOWARN)
    # 7024A4: limit menu change text third line X-Axis
    idc.set_cmt(0x7024A4, "[UI] limit menu change text third line X-Axis", 0)
    idc.set_name(0x7024A4, "ui_7024A4", idaapi.SN_NOWARN)
    # 7024C3: limit menu change text yes Y-Axis
    idc.set_cmt(0x7024C3, "[UI] limit menu change text yes Y-Axis", 0)
    idc.set_name(0x7024C3, "ui_7024C3", idaapi.SN_NOWARN)
    # 7024F1: limit menu change text no Y-Axis
    idc.set_cmt(0x7024F1, "[UI] limit menu change text no Y-Axis", 0)
    idc.set_name(0x7024F1, "ui_7024F1", idaapi.SN_NOWARN)
    # 7025C7: limit menu level and value X-Axis
    idc.set_cmt(0x7025C7, "[UI] limit menu level and value X-Axis", 0)
    idc.set_name(0x7025C7, "ui_7025C7", idaapi.SN_NOWARN)
    # 70269B: limit menu limits spacing Y-Axis
    idc.set_cmt(0x70269B, "[UI] limit menu limits spacing Y-Axis", 0)
    idc.set_name(0x70269B, "ui_70269B", idaapi.SN_NOWARN)
    # 7026AC: limit menu limits X-Axis
    idc.set_cmt(0x7026AC, "[UI] limit menu limits X-Axis", 0)
    idc.set_name(0x7026AC, "ui_7026AC", idaapi.SN_NOWARN)
    # 703188: limit menu hp/mv/lv block Y-Axis
    idc.set_cmt(0x703188, "[UI] limit menu hp/mv/lv block Y-Axis", 0)
    idc.set_name(0x703188, "ui_703188", idaapi.SN_NOWARN)
    # 7031A0: limit menu avatar Y-Axis
    idc.set_cmt(0x7031A0, "[UI] limit menu avatar Y-Axis", 0)
    idc.set_name(0x7031A0, "ui_7031A0", idaapi.SN_NOWARN)
    # 7031BA: limit menu limit level WORD X-Axis
    idc.set_cmt(0x7031BA, "[UI] limit menu limit level WORD X-Axis", 0)
    idc.set_name(0x7031BA, "ui_7031BA", idaapi.SN_NOWARN)
    # 7032FC: limit menu limit level number Y-Axis
    idc.set_cmt(0x7032FC, "[UI] limit menu limit level number Y-Axis", 0)
    idc.set_name(0x7032FC, "ui_7032FC", idaapi.SN_NOWARN)
    # 7032FE: limit menu limit level number X-Axis
    idc.set_cmt(0x7032FE, "[UI] limit menu limit level number X-Axis", 0)
    idc.set_name(0x7032FE, "ui_7032FE", idaapi.SN_NOWARN)
    # 703317: limit menu set WORD Y-Axis
    idc.set_cmt(0x703317, "[UI] limit menu set WORD Y-Axis", 0)
    idc.set_name(0x703317, "ui_703317", idaapi.SN_NOWARN)
    # 703332: limit menu check WORD Y-Axis
    idc.set_cmt(0x703332, "[UI] limit menu check WORD Y-Axis", 0)
    idc.set_name(0x703332, "ui_703332", idaapi.SN_NOWARN)
    # 7037CF: LV/HP/MP Y-axis
    idc.set_cmt(0x7037CF, "[UI] LV/HP/MP Y-axis", 0)
    idc.set_name(0x7037CF, "ui_7037CF", idaapi.SN_NOWARN)
    # 7037D1: LV/HP/MP X-axis
    idc.set_cmt(0x7037D1, "[UI] LV/HP/MP X-axis", 0)
    idc.set_name(0x7037D1, "ui_7037D1", idaapi.SN_NOWARN)
    # 7037E7: Avatar Y-axis
    idc.set_cmt(0x7037E7, "[UI] Avatar Y-axis", 0)
    idc.set_name(0x7037E7, "ui_7037E7", idaapi.SN_NOWARN)
    # 7037E9: Avatar X-axis
    idc.set_cmt(0x7037E9, "[UI] Avatar X-axis", 0)
    idc.set_name(0x7037E9, "ui_7037E9", idaapi.SN_NOWARN)
    # 703B18: Command box Y-axis
    idc.set_cmt(0x703B18, "[UI] Command box Y-axis", 0)
    idc.set_name(0x703B18, "ui_703B18", idaapi.SN_NOWARN)
    # 703B1D: Command box X-axis
    idc.set_cmt(0x703B1D, "[UI] Command box X-axis", 0)
    idc.set_name(0x703B1D, "ui_703B1D", idaapi.SN_NOWARN)
    # 703B2A: All Equips Y-axis
    idc.set_cmt(0x703B2A, "[UI] All Equips Y-axis", 0)
    idc.set_name(0x703B2A, "ui_703B2A", idaapi.SN_NOWARN)
    # 703B2F: All Equips X-axis
    idc.set_cmt(0x703B2F, "[UI] All Equips X-axis", 0)
    idc.set_name(0x703B2F, "ui_703B2F", idaapi.SN_NOWARN)
    # 703B3C: All Attributes text Y-axis (except Strength/Attack
    idc.set_cmt(0x703B3C, "[UI] All Attributes text Y-axis (except Strength/Attack numbers)", 0)
    idc.set_name(0x703B3C, "ui_703B3C", idaapi.SN_NOWARN)
    # 703B3E: All Attributes text X-axis (except Strength/Attack
    idc.set_cmt(0x703B3E, "[UI] All Attributes text X-axis (except Strength/Attack numbers)", 0)
    idc.set_name(0x703B3E, "ui_703B3E", idaapi.SN_NOWARN)
    # 703B5B: Element/Effect ALL text X-axis
    idc.set_cmt(0x703B5B, "[UI] Element/Effect ALL text X-axis", 0)
    idc.set_name(0x703B5B, "ui_703B5B", idaapi.SN_NOWARN)
    # 703E2C: Element WORD X-axis
    idc.set_cmt(0x703E2C, "[UI] Element WORD X-axis", 0)
    idc.set_name(0x703E2C, "ui_703E2C", idaapi.SN_NOWARN)
    # 703E63: Element Halve Y-axis offset
    idc.set_cmt(0x703E63, "[UI] Element Halve Y-axis offset", 0)
    idc.set_name(0x703E63, "ui_703E63", idaapi.SN_NOWARN)
    # 703E82: Element Invalid Y-axis offset
    idc.set_cmt(0x703E82, "[UI] Element Invalid Y-axis offset", 0)
    idc.set_name(0x703E82, "ui_703E82", idaapi.SN_NOWARN)
    # 703EA3: Element Absorb Y-axis offset
    idc.set_cmt(0x703EA3, "[UI] Element Absorb Y-axis offset", 0)
    idc.set_name(0x703EA3, "ui_703EA3", idaapi.SN_NOWARN)
    # 703FAD: Element line wrap width
    idc.set_cmt(0x703FAD, "[UI] Element line wrap width", 0)
    idc.set_name(0x703FAD, "ui_703FAD", idaapi.SN_NOWARN)
    # 703FF2: Element attributes bottom row Y-axis
    idc.set_cmt(0x703FF2, "[UI] Element attributes bottom row Y-axis", 0)
    idc.set_name(0x703FF2, "ui_703FF2", idaapi.SN_NOWARN)
    # 704021: Element attributes spacing X-axis
    idc.set_cmt(0x704021, "[UI] Element attributes spacing X-axis", 0)
    idc.set_name(0x704021, "ui_704021", idaapi.SN_NOWARN)
    # 70405F: Effect WORD X-axis
    idc.set_cmt(0x70405F, "[UI] Effect WORD X-axis", 0)
    idc.set_name(0x70405F, "ui_70405F", idaapi.SN_NOWARN)
    # 70407E: Effect Attack WORD X-axis
    idc.set_cmt(0x70407E, "[UI] Effect Attack WORD X-axis", 0)
    idc.set_name(0x70407E, "ui_70407E", idaapi.SN_NOWARN)
    # 7040A3: Effect Defend WORD X-axis
    idc.set_cmt(0x7040A3, "[UI] Effect Defend WORD X-axis", 0)
    idc.set_name(0x7040A3, "ui_7040A3", idaapi.SN_NOWARN)
    # 7040CE: Effect attributes top row X-axis
    idc.set_cmt(0x7040CE, "[UI] Effect attributes top row X-axis", 0)
    idc.set_name(0x7040CE, "ui_7040CE", idaapi.SN_NOWARN)
    # 70416D: Effect line wrap width
    idc.set_cmt(0x70416D, "[UI] Effect line wrap width", 0)
    idc.set_name(0x70416D, "ui_70416D", idaapi.SN_NOWARN)
    # 704181: Effect attributes other rows X-axis
    idc.set_cmt(0x704181, "[UI] Effect attributes other rows X-axis", 0)
    idc.set_name(0x704181, "ui_704181", idaapi.SN_NOWARN)
    # 7041B5: Effect text spacing Y-Axis
    idc.set_cmt(0x7041B5, "[UI] Effect text spacing Y-Axis", 0)
    idc.set_name(0x7041B5, "ui_7041B5", idaapi.SN_NOWARN)
    # 7041E4: Effect text spacing X-Axis
    idc.set_cmt(0x7041E4, "[UI] Effect text spacing X-Axis", 0)
    idc.set_name(0x7041E4, "ui_7041E4", idaapi.SN_NOWARN)
    # 704668: Wpn name text X-axis offset
    idc.set_cmt(0x704668, "[UI] Wpn name text X-axis offset", 0)
    idc.set_name(0x704668, "ui_704668", idaapi.SN_NOWARN)
    # 7046A7: Arm name text X-axis offset
    idc.set_cmt(0x7046A7, "[UI] Arm name text X-axis offset", 0)
    idc.set_name(0x7046A7, "ui_7046A7", idaapi.SN_NOWARN)
    # 704701: Acc name text X-axis offset
    idc.set_cmt(0x704701, "[UI] Acc name text X-axis offset", 0)
    idc.set_name(0x704701, "ui_704701", idaapi.SN_NOWARN)
    # 704720: Wpn WORD X-axis offset
    idc.set_cmt(0x704720, "[UI] Wpn WORD X-axis offset", 0)
    idc.set_name(0x704720, "ui_704720", idaapi.SN_NOWARN)
    # 704742: Arm WORD X-axis offset
    idc.set_cmt(0x704742, "[UI] Arm WORD X-axis offset", 0)
    idc.set_name(0x704742, "ui_704742", idaapi.SN_NOWARN)
    # 704767: Acc WORD X-axis offset
    idc.set_cmt(0x704767, "[UI] Acc WORD X-axis offset", 0)
    idc.set_name(0x704767, "ui_704767", idaapi.SN_NOWARN)
    # 7047A3: Wpn materia slots Y-axis offset
    idc.set_cmt(0x7047A3, "[UI] Wpn materia slots Y-axis offset", 0)
    idc.set_name(0x7047A3, "ui_7047A3", idaapi.SN_NOWARN)
    # 7047AA: Wpn materia slots X-axis offset
    idc.set_cmt(0x7047AA, "[UI] Wpn materia slots X-axis offset", 0)
    idc.set_name(0x7047AA, "ui_7047AA", idaapi.SN_NOWARN)
    # 7047E6: Arm materia slots Y-axis offset
    idc.set_cmt(0x7047E6, "[UI] Arm materia slots Y-axis offset", 0)
    idc.set_name(0x7047E6, "ui_7047E6", idaapi.SN_NOWARN)
    # 7047ED: Arm materia slots X-axis offset
    idc.set_cmt(0x7047ED, "[UI] Arm materia slots X-axis offset", 0)
    idc.set_name(0x7047ED, "ui_7047ED", idaapi.SN_NOWARN)
    # 704989: Materia slots BG Width
    idc.set_cmt(0x704989, "[UI] Materia slots BG Width", 0)
    idc.set_name(0x704989, "ui_704989", idaapi.SN_NOWARN)
    # 70498F: Materia slots BG Height
    idc.set_cmt(0x70498F, "[UI] Materia slots BG Height", 0)
    idc.set_name(0x70498F, "ui_70498F", idaapi.SN_NOWARN)
    # 704DB3: Strength number Y/X-axis
    idc.set_cmt(0x704DB3, "[UI] Strength number Y/X-axis", 0)
    idc.set_name(0x704DB3, "ui_704DB3", idaapi.SN_NOWARN)
    # 704DE9: Dexterity number Y-axis
    idc.set_cmt(0x704DE9, "[UI] Dexterity number Y-axis", 0)
    idc.set_name(0x704DE9, "ui_704DE9", idaapi.SN_NOWARN)
    # 704DF0: Dexterity number X-axis
    idc.set_cmt(0x704DF0, "[UI] Dexterity number X-axis", 0)
    idc.set_name(0x704DF0, "ui_704DF0", idaapi.SN_NOWARN)
    # 704E1F: Vitality number Y-axis
    idc.set_cmt(0x704E1F, "[UI] Vitality number Y-axis", 0)
    idc.set_name(0x704E1F, "ui_704E1F", idaapi.SN_NOWARN)
    # 704E25: Vitality number X-axis
    idc.set_cmt(0x704E25, "[UI] Vitality number X-axis", 0)
    idc.set_name(0x704E25, "ui_704E25", idaapi.SN_NOWARN)
    # 704E55: Magic number Y-axis
    idc.set_cmt(0x704E55, "[UI] Magic number Y-axis", 0)
    idc.set_name(0x704E55, "ui_704E55", idaapi.SN_NOWARN)
    # 704E5C: Magic number X-axis
    idc.set_cmt(0x704E5C, "[UI] Magic number X-axis", 0)
    idc.set_name(0x704E5C, "ui_704E5C", idaapi.SN_NOWARN)
    # 704E8C: Spirit number Y-axis
    idc.set_cmt(0x704E8C, "[UI] Spirit number Y-axis", 0)
    idc.set_name(0x704E8C, "ui_704E8C", idaapi.SN_NOWARN)
    # 704E93: Spirit number X-axis
    idc.set_cmt(0x704E93, "[UI] Spirit number X-axis", 0)
    idc.set_name(0x704E93, "ui_704E93", idaapi.SN_NOWARN)
    # 704EC2: Luck number Y-axis
    idc.set_cmt(0x704EC2, "[UI] Luck number Y-axis", 0)
    idc.set_name(0x704EC2, "ui_704EC2", idaapi.SN_NOWARN)
    # 704EC8: Luck number X-axis
    idc.set_cmt(0x704EC8, "[UI] Luck number X-axis", 0)
    idc.set_name(0x704EC8, "ui_704EC8", idaapi.SN_NOWARN)
    # 704EDA: Bottom Attributes Block Y-Axis
    idc.set_cmt(0x704EDA, "[UI] Bottom Attributes Block Y-Axis", 0)
    idc.set_name(0x704EDA, "ui_704EDA", idaapi.SN_NOWARN)
    # 70502B: Attack number Y/X-axis
    idc.set_cmt(0x70502B, "[UI] Attack number Y/X-axis", 0)
    idc.set_name(0x70502B, "ui_70502B", idaapi.SN_NOWARN)
    # 70504F: Attack% number Y-axis
    idc.set_cmt(0x70504F, "[UI] Attack% number Y-axis", 0)
    idc.set_name(0x70504F, "ui_70504F", idaapi.SN_NOWARN)
    # 705055: Attack% number X-axis
    idc.set_cmt(0x705055, "[UI] Attack% number X-axis", 0)
    idc.set_name(0x705055, "ui_705055", idaapi.SN_NOWARN)
    # 705074: Defense number Y-axis
    idc.set_cmt(0x705074, "[UI] Defense number Y-axis", 0)
    idc.set_name(0x705074, "ui_705074", idaapi.SN_NOWARN)
    # 70507A: Defense number X-axis
    idc.set_cmt(0x70507A, "[UI] Defense number X-axis", 0)
    idc.set_name(0x70507A, "ui_70507A", idaapi.SN_NOWARN)
    # 705099: Defense% number Y-axis
    idc.set_cmt(0x705099, "[UI] Defense% number Y-axis", 0)
    idc.set_name(0x705099, "ui_705099", idaapi.SN_NOWARN)
    # 70509F: Defense% number X-axis
    idc.set_cmt(0x70509F, "[UI] Defense% number X-axis", 0)
    idc.set_name(0x70509F, "ui_70509F", idaapi.SN_NOWARN)
    # 7050BE: Magic Attack number Y-axis
    idc.set_cmt(0x7050BE, "[UI] Magic Attack number Y-axis", 0)
    idc.set_name(0x7050BE, "ui_7050BE", idaapi.SN_NOWARN)
    # 7050C4: Magic Attack number X-axis
    idc.set_cmt(0x7050C4, "[UI] Magic Attack number X-axis", 0)
    idc.set_name(0x7050C4, "ui_7050C4", idaapi.SN_NOWARN)
    # 7050E3: Magic Defense number Y-axis
    idc.set_cmt(0x7050E3, "[UI] Magic Defense number Y-axis", 0)
    idc.set_name(0x7050E3, "ui_7050E3", idaapi.SN_NOWARN)
    # 7050E9: Magic Defense number X-axis
    idc.set_cmt(0x7050E9, "[UI] Magic Defense number X-axis", 0)
    idc.set_name(0x7050E9, "ui_7050E9", idaapi.SN_NOWARN)
    # 705108: Magic Defense% number Y-axis
    idc.set_cmt(0x705108, "[UI] Magic Defense% number Y-axis", 0)
    idc.set_name(0x705108, "ui_705108", idaapi.SN_NOWARN)
    # 705111: Magic Defense% number X-axis
    idc.set_cmt(0x705111, "[UI] Magic Defense% number X-axis", 0)
    idc.set_name(0x705111, "ui_705111", idaapi.SN_NOWARN)
    # 7055B8: Limit bar Y-Axis
    idc.set_cmt(0x7055B8, "[UI] Limit bar Y-Axis", 0)
    idc.set_name(0x7055B8, "ui_7055B8", idaapi.SN_NOWARN)
    # 7055BA: Limit bar X-axis
    idc.set_cmt(0x7055BA, "[UI] Limit bar X-axis", 0)
    idc.set_name(0x7055BA, "ui_7055BA", idaapi.SN_NOWARN)
    # 7055DD: Limit Box Y-Axis
    idc.set_cmt(0x7055DD, "[UI] Limit Box Y-Axis", 0)
    idc.set_name(0x7055DD, "ui_7055DD", idaapi.SN_NOWARN)
    # 7055DF: Limit Box X-Axis
    idc.set_cmt(0x7055DF, "[UI] Limit Box X-Axis", 0)
    idc.set_name(0x7055DF, "ui_7055DF", idaapi.SN_NOWARN)
    # 705604: EXP: WORD X-axis
    idc.set_cmt(0x705604, "[UI] EXP: WORD X-axis", 0)
    idc.set_name(0x705604, "ui_705604", idaapi.SN_NOWARN)
    # 705627: Exp bar width
    idc.set_cmt(0x705627, "[UI] Exp bar width", 0)
    idc.set_name(0x705627, "ui_705627", idaapi.SN_NOWARN)
    # 705631: Exp bar Y-Axis
    idc.set_cmt(0x705631, "[UI] Exp bar Y-Axis", 0)
    idc.set_name(0x705631, "ui_705631", idaapi.SN_NOWARN)
    # 705633: Exp bar X-Axis
    idc.set_cmt(0x705633, "[UI] Exp bar X-Axis", 0)
    idc.set_name(0x705633, "ui_705633", idaapi.SN_NOWARN)
    # 705656: Exp box Y-Axis
    idc.set_cmt(0x705656, "[UI] Exp box Y-Axis", 0)
    idc.set_name(0x705656, "ui_705656", idaapi.SN_NOWARN)
    # 705658: Exp box X-Axis
    idc.set_cmt(0x705658, "[UI] Exp box X-Axis", 0)
    idc.set_name(0x705658, "ui_705658", idaapi.SN_NOWARN)
    # 70567D: EXP \"p\" X-axis
    idc.set_cmt(0x70567D, "[UI] EXP \"p\" X-axis", 0)
    idc.set_name(0x70567D, "ui_70567D", idaapi.SN_NOWARN)
    # 7056A0: next level \"p\" Y-axis
    idc.set_cmt(0x7056A0, "[UI] next level \"p\" Y-axis", 0)
    idc.set_name(0x7056A0, "ui_7056A0", idaapi.SN_NOWARN)
    # 7056A2: next level \"p\" X-axis
    idc.set_cmt(0x7056A2, "[UI] next level \"p\" X-axis", 0)
    idc.set_name(0x7056A2, "ui_7056A2", idaapi.SN_NOWARN)
    # 7056C8: EXP number Y-axis
    idc.set_cmt(0x7056C8, "[UI] EXP number Y-axis", 0)
    idc.set_name(0x7056C8, "ui_7056C8", idaapi.SN_NOWARN)
    # 7056CA: EXP number X-axis
    idc.set_cmt(0x7056CA, "[UI] EXP number X-axis", 0)
    idc.set_name(0x7056CA, "ui_7056CA", idaapi.SN_NOWARN)
    # 7056F0: next level number Y-axis
    idc.set_cmt(0x7056F0, "[UI] next level number Y-axis", 0)
    idc.set_name(0x7056F0, "ui_7056F0", idaapi.SN_NOWARN)
    # 7056F2: next level number X-axis
    idc.set_cmt(0x7056F2, "[UI] next level number X-axis", 0)
    idc.set_name(0x7056F2, "ui_7056F2", idaapi.SN_NOWARN)
    # 705715: next level text Y-axis
    idc.set_cmt(0x705715, "[UI] next level text Y-axis", 0)
    idc.set_name(0x705715, "ui_705715", idaapi.SN_NOWARN)
    # 705717: next level text X-axis
    idc.set_cmt(0x705717, "[UI] next level text X-axis", 0)
    idc.set_name(0x705717, "ui_705717", idaapi.SN_NOWARN)
    # 705730: Limit level text Y-axis
    idc.set_cmt(0x705730, "[UI] Limit level text Y-axis", 0)
    idc.set_name(0x705730, "ui_705730", idaapi.SN_NOWARN)
    # 705732: Limit level text X-axis
    idc.set_cmt(0x705732, "[UI] Limit level text X-axis", 0)
    idc.set_name(0x705732, "ui_705732", idaapi.SN_NOWARN)
    # 70575A: Limit level number Y-axis
    idc.set_cmt(0x70575A, "[UI] Limit level number Y-axis", 0)
    idc.set_name(0x70575A, "ui_70575A", idaapi.SN_NOWARN)
    # 705769: Limit level number X-axis
    idc.set_cmt(0x705769, "[UI] Limit level number X-axis", 0)
    idc.set_name(0x705769, "ui_705769", idaapi.SN_NOWARN)
    # 705D85: ROWS BEFORE SCROLL BAR APPEARS
    idc.set_cmt(0x705D85, "[UI] ROWS BEFORE SCROLL BAR APPEARS", 0)
    idc.set_name(0x705D85, "ui_705D85", idaapi.SN_NOWARN)
    # 705D8F: SCROLL BAR ROW HEIGHT
    idc.set_cmt(0x705D8F, "[UI] SCROLL BAR ROW HEIGHT", 0)
    idc.set_name(0x705D8F, "ui_705D8F", idaapi.SN_NOWARN)
    # 705DB4: EQUIP MENU - SCROLL BAR X-AXIS
    idc.set_cmt(0x705DB4, "[UI] EQUIP MENU - SCROLL BAR X-AXIS", 0)
    idc.set_name(0x705DB4, "ui_705DB4", idaapi.SN_NOWARN)
    # 705DBD: EQUIP MENU - SCROLL BAR Y-AXIS
    idc.set_cmt(0x705DBD, "[UI] EQUIP MENU - SCROLL BAR Y-AXIS", 0)
    idc.set_name(0x705DBD, "ui_705DBD", idaapi.SN_NOWARN)
    # 705DC6: EQUIP MENU - SCROLL BAR WIDTH
    idc.set_cmt(0x705DC6, "[UI] EQUIP MENU - SCROLL BAR WIDTH", 0)
    idc.set_name(0x705DC6, "ui_705DC6", idaapi.SN_NOWARN)
    # 705DE9: ROW RELATED PREVENTS GIBBERISH IN EMPTY BOXES WHEN
    idc.set_cmt(0x705DE9, "[UI] ROW RELATED PREVENTS GIBBERISH IN EMPTY BOXES WHEN SET", 0)
    idc.set_name(0x705DE9, "ui_705DE9", idaapi.SN_NOWARN)
    # 705DEF: VISIBLE ITEM ROWS
    idc.set_cmt(0x705DEF, "[UI] VISIBLE ITEM ROWS", 0)
    idc.set_name(0x705DEF, "ui_705DEF", idaapi.SN_NOWARN)
    # 705EBA: TEXT SPACING Y-AXIS
    idc.set_cmt(0x705EBA, "[UI] TEXT SPACING Y-AXIS", 0)
    idc.set_name(0x705EBA, "ui_705EBA", idaapi.SN_NOWARN)
    # 705EC7: RIGHT BOX TEXT Y-AXIS
    idc.set_cmt(0x705EC7, "[UI] RIGHT BOX TEXT Y-AXIS", 0)
    idc.set_name(0x705EC7, "ui_705EC7", idaapi.SN_NOWARN)
    # 705ECD: RIGHT BOX TEXT X-AXIS
    idc.set_cmt(0x705ECD, "[UI] RIGHT BOX TEXT X-AXIS", 0)
    idc.set_name(0x705ECD, "ui_705ECD", idaapi.SN_NOWARN)
    # 705F0E: CURSOR SPACING Y-AXIS
    idc.set_cmt(0x705F0E, "[UI] CURSOR SPACING Y-AXIS", 0)
    idc.set_name(0x705F0E, "ui_705F0E", idaapi.SN_NOWARN)
    # 705F11: CURSOR Y-AXIS
    idc.set_cmt(0x705F11, "[UI] CURSOR Y-AXIS", 0)
    idc.set_name(0x705F11, "ui_705F11", idaapi.SN_NOWARN)
    # 705F14: CURSOR X-AXIS
    idc.set_cmt(0x705F14, "[UI] CURSOR X-AXIS", 0)
    idc.set_name(0x705F14, "ui_705F14", idaapi.SN_NOWARN)
    # 705F47: EQUIPPED ITEM SLOT WORD X-AXIS
    idc.set_cmt(0x705F47, "[UI] EQUIPPED ITEM SLOT WORD X-AXIS", 0)
    idc.set_name(0x705F47, "ui_705F47", idaapi.SN_NOWARN)
    # 705F6B: EQUIPPED ITEM GROWTH WORD X-AXIS
    idc.set_cmt(0x705F6B, "[UI] EQUIPPED ITEM GROWTH WORD X-AXIS", 0)
    idc.set_name(0x705F6B, "ui_705F6B", idaapi.SN_NOWARN)
    # 705FCC: Wpn Equipped Slots Y-Axis
    idc.set_cmt(0x705FCC, "[UI] Wpn Equipped Slots Y-Axis", 0)
    idc.set_name(0x705FCC, "ui_705FCC", idaapi.SN_NOWARN)
    # 705FCF: Wpn Equipped Slots X-Axis
    idc.set_cmt(0x705FCF, "[UI] Wpn Equipped Slots X-Axis", 0)
    idc.set_name(0x705FCF, "ui_705FCF", idaapi.SN_NOWARN)
    # 70602C: Arm Equipped Slots Y-Axis
    idc.set_cmt(0x70602C, "[UI] Arm Equipped Slots Y-Axis", 0)
    idc.set_name(0x70602C, "ui_70602C", idaapi.SN_NOWARN)
    # 70602F: Arm Equipped Slots X-Axis
    idc.set_cmt(0x70602F, "[UI] Arm Equipped Slots X-Axis", 0)
    idc.set_name(0x70602F, "ui_70602F", idaapi.SN_NOWARN)
    # 7060AA: EQUIPPED ITEM SLOTS WORD X-AXIS
    idc.set_cmt(0x7060AA, "[UI] EQUIPPED ITEM SLOTS WORD X-AXIS", 0)
    idc.set_name(0x7060AA, "ui_7060AA", idaapi.SN_NOWARN)
    # 7060D4: GHOST CURSOR SPACING Y-AXIS
    idc.set_cmt(0x7060D4, "[UI] GHOST CURSOR SPACING Y-AXIS", 0)
    idc.set_name(0x7060D4, "ui_7060D4", idaapi.SN_NOWARN)
    # 7060D7: GHOST CURSOR Y-AXIS
    idc.set_cmt(0x7060D7, "[UI] GHOST CURSOR Y-AXIS", 0)
    idc.set_name(0x7060D7, "ui_7060D7", idaapi.SN_NOWARN)
    # 7060DA: GHOST CURSOR X-AXIS
    idc.set_cmt(0x7060DA, "[UI] GHOST CURSOR X-AXIS", 0)
    idc.set_name(0x7060DA, "ui_7060DA", idaapi.SN_NOWARN)
    # 7060F3: CURSOR SPACING Y-AXIS
    idc.set_cmt(0x7060F3, "[UI] CURSOR SPACING Y-AXIS", 0)
    idc.set_name(0x7060F3, "ui_7060F3", idaapi.SN_NOWARN)
    # 7060F6: SELECTION CURSOR Y-AXIS
    idc.set_cmt(0x7060F6, "[UI] SELECTION CURSOR Y-AXIS", 0)
    idc.set_name(0x7060F6, "ui_7060F6", idaapi.SN_NOWARN)
    # 7060FC: SELECTION CURSOR X-AXIS
    idc.set_cmt(0x7060FC, "[UI] SELECTION CURSOR X-AXIS", 0)
    idc.set_name(0x7060FC, "ui_7060FC", idaapi.SN_NOWARN)
    # 706130: SLOT WORD X-AXIS
    idc.set_cmt(0x706130, "[UI] SLOT WORD X-AXIS", 0)
    idc.set_name(0x706130, "ui_706130", idaapi.SN_NOWARN)
    # 706154: GROWTH WORD X-AXIS
    idc.set_cmt(0x706154, "[UI] GROWTH WORD X-AXIS", 0)
    idc.set_name(0x706154, "ui_706154", idaapi.SN_NOWARN)
    # 7061A5: Wpn Selected Slots Y-Axis
    idc.set_cmt(0x7061A5, "[UI] Wpn Selected Slots Y-Axis", 0)
    idc.set_name(0x7061A5, "ui_7061A5", idaapi.SN_NOWARN)
    # 7061A8: Wpn Selected Slots X-Axis
    idc.set_cmt(0x7061A8, "[UI] Wpn Selected Slots X-Axis", 0)
    idc.set_name(0x7061A8, "ui_7061A8", idaapi.SN_NOWARN)
    # 7061F7: Arm Selected Slots Y-Axis
    idc.set_cmt(0x7061F7, "[UI] Arm Selected Slots Y-Axis", 0)
    idc.set_name(0x7061F7, "ui_7061F7", idaapi.SN_NOWARN)
    # 7061FA: Arm Selected Slots X-Axis
    idc.set_cmt(0x7061FA, "[UI] Arm Selected Slots X-Axis", 0)
    idc.set_name(0x7061FA, "ui_7061FA", idaapi.SN_NOWARN)
    # 706277: GROWTH VALUE X-AXIS
    idc.set_cmt(0x706277, "[UI] GROWTH VALUE X-AXIS", 0)
    idc.set_name(0x706277, "ui_706277", idaapi.SN_NOWARN)
    # 7062BD: WPN/ARM/ACC WORDS X-AXIS
    idc.set_cmt(0x7062BD, "[UI] WPN/ARM/ACC WORDS X-AXIS", 0)
    idc.set_name(0x7062BD, "ui_7062BD", idaapi.SN_NOWARN)
    # 7062D6: BOTTOM BOX CONTENTS Y-AXIS
    idc.set_cmt(0x7062D6, "[UI] BOTTOM BOX CONTENTS Y-AXIS", 0)
    idc.set_name(0x7062D6, "ui_7062D6", idaapi.SN_NOWARN)
    # 7062EF: NAME AND STATUS/LV/HP/MP/VALUES Y-AXIS
    idc.set_cmt(0x7062EF, "[UI] NAME AND STATUS/LV/HP/MP/VALUES Y-AXIS", 0)
    idc.set_name(0x7062EF, "ui_7062EF", idaapi.SN_NOWARN)
    # 706306: AVATAR Y-AXIS
    idc.set_cmt(0x706306, "[UI] AVATAR Y-AXIS", 0)
    idc.set_name(0x706306, "ui_706306", idaapi.SN_NOWARN)
    # 70633C: WPN NAME X-AXIS
    idc.set_cmt(0x70633C, "[UI] WPN NAME X-AXIS", 0)
    idc.set_name(0x70633C, "ui_70633C", idaapi.SN_NOWARN)
    # 706373: ARM NAME X-AXIS
    idc.set_cmt(0x706373, "[UI] ARM NAME X-AXIS", 0)
    idc.set_name(0x706373, "ui_706373", idaapi.SN_NOWARN)
    # 7063C3: ACC NAME X-AXIS
    idc.set_cmt(0x7063C3, "[UI] ACC NAME X-AXIS", 0)
    idc.set_name(0x7063C3, "ui_7063C3", idaapi.SN_NOWARN)
    # 7071D3: ROW RELATED PREVENTS MOUSE SCROLLING TO EMPTY SPAC
    idc.set_cmt(0x7071D3, "[UI] ROW RELATED PREVENTS MOUSE SCROLLING TO EMPTY SPACES WHEN SET", 0)
    idc.set_name(0x7071D3, "ui_7071D3", idaapi.SN_NOWARN)
    # 7071D9: CURSOR ROW COUNT Y-AXIS refresh menu
    idc.set_cmt(0x7071D9, "[UI] CURSOR ROW COUNT Y-AXIS refresh menu", 0)
    idc.set_name(0x7071D9, "ui_7071D9", idaapi.SN_NOWARN)
    # 707733: Materia slots BG Width
    idc.set_cmt(0x707733, "[UI] Materia slots BG Width", 0)
    idc.set_name(0x707733, "ui_707733", idaapi.SN_NOWARN)
    # 707739: Materia slots BG Height
    idc.set_cmt(0x707739, "[UI] Materia slots BG Height", 0)
    idc.set_name(0x707739, "ui_707739", idaapi.SN_NOWARN)
    # 70879C: check box text Y-Axis
    idc.set_cmt(0x70879C, "[UI] check box text Y-Axis", 0)
    idc.set_name(0x70879C, "ui_70879C", idaapi.SN_NOWARN)
    # 7087AB: check box text spacing X-Axis
    idc.set_cmt(0x7087AB, "[UI] check box text spacing X-Axis", 0)
    idc.set_name(0x7087AB, "ui_7087AB", idaapi.SN_NOWARN)
    # 7087B4: check box text X-Axis
    idc.set_cmt(0x7087B4, "[UI] check box text X-Axis", 0)
    idc.set_name(0x7087B4, "ui_7087B4", idaapi.SN_NOWARN)
    # 7089B2: magic sub box scroll bar height
    idc.set_cmt(0x7089B2, "[UI] magic sub box scroll bar height", 0)
    idc.set_name(0x7089B2, "ui_7089B2", idaapi.SN_NOWARN)
    # 7089D0: materia menu - magic sub box scroll bar X-Axis
    idc.set_cmt(0x7089D0, "[UI] materia menu - magic sub box scroll bar X-Axis", 0)
    idc.set_name(0x7089D0, "ui_7089D0", idaapi.SN_NOWARN)
    # 7089ED: materia menu - magic sub box scroll bar width
    idc.set_cmt(0x7089ED, "[UI] materia menu - magic sub box scroll bar width", 0)
    idc.set_name(0x7089ED, "ui_7089ED", idaapi.SN_NOWARN)
    # 708A29: magic sub box row count
    idc.set_cmt(0x708A29, "[UI] magic sub box row count", 0)
    idc.set_name(0x708A29, "ui_708A29", idaapi.SN_NOWARN)
    # 708ACB: magic sub box text spacing Y-Axis
    idc.set_cmt(0x708ACB, "[UI] magic sub box text spacing Y-Axis", 0)
    idc.set_name(0x708ACB, "ui_708ACB", idaapi.SN_NOWARN)
    # 708AEA: magic sub box text spacing X-Axis
    idc.set_cmt(0x708AEA, "[UI] magic sub box text spacing X-Axis", 0)
    idc.set_name(0x708AEA, "ui_708AEA", idaapi.SN_NOWARN)
    # 708AF1: magic sub box text X-Axis
    idc.set_cmt(0x708AF1, "[UI] magic sub box text X-Axis", 0)
    idc.set_name(0x708AF1, "ui_708AF1", idaapi.SN_NOWARN)
    # 708BF3: magic sub box support symbol palette color
    idc.set_cmt(0x708BF3, "[UI] magic sub box support symbol palette color", 0)
    idc.set_name(0x708BF3, "ui_708BF3", idaapi.SN_NOWARN)
    # 708C0E: magic sub box support symbol spacing Y-Axis
    idc.set_cmt(0x708C0E, "[UI] magic sub box support symbol spacing Y-Axis", 0)
    idc.set_name(0x708C0E, "ui_708C0E", idaapi.SN_NOWARN)
    # 708C12: magic sub box support symbol Y-Axis
    idc.set_cmt(0x708C12, "[UI] magic sub box support symbol Y-Axis", 0)
    idc.set_name(0x708C12, "ui_708C12", idaapi.SN_NOWARN)
    # 708C2D: magic sub box support symbol spacing X-Axis
    idc.set_cmt(0x708C2D, "[UI] magic sub box support symbol spacing X-Axis", 0)
    idc.set_name(0x708C2D, "ui_708C2D", idaapi.SN_NOWARN)
    # 708C34: magic sub box support symbol X-Axis
    idc.set_cmt(0x708C34, "[UI] magic sub box support symbol X-Axis", 0)
    idc.set_name(0x708C34, "ui_708C34", idaapi.SN_NOWARN)
    # 708D24: magic sub box mpneeded text X-Axis
    idc.set_cmt(0x708D24, "[UI] magic sub box mpneeded text X-Axis", 0)
    idc.set_name(0x708D24, "ui_708D24", idaapi.SN_NOWARN)
    # 708E5B: mpneeded box Quadra Number Y-Axis
    idc.set_cmt(0x708E5B, "[UI] mpneeded box Quadra Number Y-Axis", 0)
    idc.set_name(0x708E5B, "ui_708E5B", idaapi.SN_NOWARN)
    # 708E62: mpneeded box Quadra Number X-Axis
    idc.set_cmt(0x708E62, "[UI] mpneeded box Quadra Number X-Axis", 0)
    idc.set_name(0x708E62, "ui_708E62", idaapi.SN_NOWARN)
    # 708EAC: mpneeded box Quadra 'X' Y-Axis
    idc.set_cmt(0x708EAC, "[UI] mpneeded box Quadra 'X' Y-Axis", 0)
    idc.set_name(0x708EAC, "ui_708EAC", idaapi.SN_NOWARN)
    # 708EFD: mpneeded box summon/All Number Y-Axis
    idc.set_cmt(0x708EFD, "[UI] mpneeded box summon/All Number Y-Axis", 0)
    idc.set_name(0x708EFD, "ui_708EFD", idaapi.SN_NOWARN)
    # 708F04: mpneeded box summon/All Number X-Axis
    idc.set_cmt(0x708F04, "[UI] mpneeded box summon/All Number X-Axis", 0)
    idc.set_name(0x708F04, "ui_708F04", idaapi.SN_NOWARN)
    # 708F4E: mpneeded box summon/All 'X' Y-Axis
    idc.set_cmt(0x708F4E, "[UI] mpneeded box summon/All 'X' Y-Axis", 0)
    idc.set_name(0x708F4E, "ui_708F4E", idaapi.SN_NOWARN)
    # 708FB9: mpneeded MP divider color
    idc.set_cmt(0x708FB9, "[UI] mpneeded MP divider color", 0)
    idc.set_name(0x708FB9, "ui_708FB9", idaapi.SN_NOWARN)
    # 70968D: summon sub box scroll bar height
    idc.set_cmt(0x70968D, "[UI] summon sub box scroll bar height", 0)
    idc.set_name(0x70968D, "ui_70968D", idaapi.SN_NOWARN)
    # 7096AB: materia menu - summon sub box scroll bar X-Axis
    idc.set_cmt(0x7096AB, "[UI] materia menu - summon sub box scroll bar X-Axis", 0)
    idc.set_name(0x7096AB, "ui_7096AB", idaapi.SN_NOWARN)
    # 7096C8: materia menu - summon sub box scroll bar width
    idc.set_cmt(0x7096C8, "[UI] materia menu - summon sub box scroll bar width", 0)
    idc.set_name(0x7096C8, "ui_7096C8", idaapi.SN_NOWARN)
    # 709704: summon sub box row count
    idc.set_cmt(0x709704, "[UI] summon sub box row count", 0)
    idc.set_name(0x709704, "ui_709704", idaapi.SN_NOWARN)
    # 709772: summon sub box spacing Y-Axis
    idc.set_cmt(0x709772, "[UI] summon sub box spacing Y-Axis", 0)
    idc.set_name(0x709772, "ui_709772", idaapi.SN_NOWARN)
    # 70978E: summon sub box X-Axis
    idc.set_cmt(0x70978E, "[UI] summon sub box X-Axis", 0)
    idc.set_name(0x70978E, "ui_70978E", idaapi.SN_NOWARN)
    # 709A7D: eskill sub box scroll bar height
    idc.set_cmt(0x709A7D, "[UI] eskill sub box scroll bar height", 0)
    idc.set_name(0x709A7D, "ui_709A7D", idaapi.SN_NOWARN)
    # 709A9B: materia menu - eskill sub box scroll bar X-Axis
    idc.set_cmt(0x709A9B, "[UI] materia menu - eskill sub box scroll bar X-Axis", 0)
    idc.set_name(0x709A9B, "ui_709A9B", idaapi.SN_NOWARN)
    # 709AB8: materia menu - eskill sub box scroll bar width
    idc.set_cmt(0x709AB8, "[UI] materia menu - eskill sub box scroll bar width", 0)
    idc.set_name(0x709AB8, "ui_709AB8", idaapi.SN_NOWARN)
    # 709AF4: eskill sub box visible row count
    idc.set_cmt(0x709AF4, "[UI] eskill sub box visible row count", 0)
    idc.set_name(0x709AF4, "ui_709AF4", idaapi.SN_NOWARN)
    # 709B8F: eskill sub box spacing Y-Axis
    idc.set_cmt(0x709B8F, "[UI] eskill sub box spacing Y-Axis", 0)
    idc.set_name(0x709B8F, "ui_709B8F", idaapi.SN_NOWARN)
    # 709B93: eskill sub box Y-Axis
    idc.set_cmt(0x709B93, "[UI] eskill sub box Y-Axis", 0)
    idc.set_name(0x709B93, "ui_709B93", idaapi.SN_NOWARN)
    # 709BB6: eskill sub box X-Axis
    idc.set_cmt(0x709BB6, "[UI] eskill sub box X-Axis", 0)
    idc.set_name(0x709BB6, "ui_709BB6", idaapi.SN_NOWARN)
    # 709F38: right box cursor row count Y-Axis (full menu refre
    idc.set_cmt(0x709F38, "[UI] right box cursor row count Y-Axis (full menu refresh)", 0)
    idc.set_name(0x709F38, "ui_709F38", idaapi.SN_NOWARN)
    # 70A01D: Top Box Check Cursor Y-Axis
    idc.set_cmt(0x70A01D, "[UI] Top Box Check Cursor Y-Axis", 0)
    idc.set_name(0x70A01D, "ui_70A01D", idaapi.SN_NOWARN)
    # 70A020: Top Box Check Cursor X-Axis
    idc.set_cmt(0x70A020, "[UI] Top Box Check Cursor X-Axis", 0)
    idc.set_name(0x70A020, "ui_70A020", idaapi.SN_NOWARN)
    # 70A041: Top Box slots Cursor Y-Axis
    idc.set_cmt(0x70A041, "[UI] Top Box slots Cursor Y-Axis", 0)
    idc.set_name(0x70A041, "ui_70A041", idaapi.SN_NOWARN)
    # 70A07A: Top Box slots ghost Cursor Y-Axis
    idc.set_cmt(0x70A07A, "[UI] Top Box slots ghost Cursor Y-Axis", 0)
    idc.set_name(0x70A07A, "ui_70A07A", idaapi.SN_NOWARN)
    # 70A0A0: right box cursor spacing Y-Axis
    idc.set_cmt(0x70A0A0, "[UI] right box cursor spacing Y-Axis", 0)
    idc.set_name(0x70A0A0, "ui_70A0A0", idaapi.SN_NOWARN)
    # 70A0A2: right box cursor Y-Axis
    idc.set_cmt(0x70A0A2, "[UI] right box cursor Y-Axis", 0)
    idc.set_name(0x70A0A2, "ui_70A0A2", idaapi.SN_NOWARN)
    # 70A0A8: right box cursor X-Axis
    idc.set_cmt(0x70A0A8, "[UI] right box cursor X-Axis", 0)
    idc.set_name(0x70A0A8, "ui_70A0A8", idaapi.SN_NOWARN)
    # 70A0D0: Top Box Check Ghost Cursor Y-Axis
    idc.set_cmt(0x70A0D0, "[UI] Top Box Check Ghost Cursor Y-Axis", 0)
    idc.set_name(0x70A0D0, "ui_70A0D0", idaapi.SN_NOWARN)
    # 70A0D3: Top Box Check Ghost Cursor X-Axis
    idc.set_cmt(0x70A0D3, "[UI] Top Box Check Ghost Cursor X-Axis", 0)
    idc.set_name(0x70A0D3, "ui_70A0D3", idaapi.SN_NOWARN)
    # 70A0EF: command box Check Cursor spacing X-Axis
    idc.set_cmt(0x70A0EF, "[UI] command box Check Cursor spacing X-Axis", 0)
    idc.set_name(0x70A0EF, "ui_70A0EF", idaapi.SN_NOWARN)
    # 70A0F3: command box Check Cursor X-Axis
    idc.set_cmt(0x70A0F3, "[UI] command box Check Cursor X-Axis", 0)
    idc.set_name(0x70A0F3, "ui_70A0F3", idaapi.SN_NOWARN)
    # 70A121: command box Check Cursor Y-Axis
    idc.set_cmt(0x70A121, "[UI] command box Check Cursor Y-Axis", 0)
    idc.set_name(0x70A121, "ui_70A121", idaapi.SN_NOWARN)
    # 70A1A5: Top Box Check Magic Submenu Ghost Cursor Y-Axis
    idc.set_cmt(0x70A1A5, "[UI] Top Box Check Magic Submenu Ghost Cursor Y-Axis", 0)
    idc.set_name(0x70A1A5, "ui_70A1A5", idaapi.SN_NOWARN)
    # 70A1A8: Top Box Check Magic Submenu Ghost Cursor X-Axis
    idc.set_cmt(0x70A1A8, "[UI] Top Box Check Magic Submenu Ghost Cursor X-Axis", 0)
    idc.set_name(0x70A1A8, "ui_70A1A8", idaapi.SN_NOWARN)
    # 70A1CB: magic sub box selection cursor spacing Y-Axis
    idc.set_cmt(0x70A1CB, "[UI] magic sub box selection cursor spacing Y-Axis", 0)
    idc.set_name(0x70A1CB, "ui_70A1CB", idaapi.SN_NOWARN)
    # 70A1E2: magic sub box selection cursor spacing X-Axis
    idc.set_cmt(0x70A1E2, "[UI] magic sub box selection cursor spacing X-Axis", 0)
    idc.set_name(0x70A1E2, "ui_70A1E2", idaapi.SN_NOWARN)
    # 70A1E9: magic sub box selection cursor X-Axis
    idc.set_cmt(0x70A1E9, "[UI] magic sub box selection cursor X-Axis", 0)
    idc.set_name(0x70A1E9, "ui_70A1E9", idaapi.SN_NOWARN)
    # 70A275: Top Box Check Summon Submenu Ghost Cursor Y-Axis
    idc.set_cmt(0x70A275, "[UI] Top Box Check Summon Submenu Ghost Cursor Y-Axis", 0)
    idc.set_name(0x70A275, "ui_70A275", idaapi.SN_NOWARN)
    # 70A278: Top Box Check Summon Submenu Ghost Cursor X-Axis
    idc.set_cmt(0x70A278, "[UI] Top Box Check Summon Submenu Ghost Cursor X-Axis", 0)
    idc.set_name(0x70A278, "ui_70A278", idaapi.SN_NOWARN)
    # 70A29A: summon sub box selection cursor spacing Y-Axis
    idc.set_cmt(0x70A29A, "[UI] summon sub box selection cursor spacing Y-Axis", 0)
    idc.set_name(0x70A29A, "ui_70A29A", idaapi.SN_NOWARN)
    # 70A2AC: summon sub box selection cursor X-Axis
    idc.set_cmt(0x70A2AC, "[UI] summon sub box selection cursor X-Axis", 0)
    idc.set_name(0x70A2AC, "ui_70A2AC", idaapi.SN_NOWARN)
    # 70A32A: Top Box Check Eskill Submenu Ghost Cursor Y-Axis
    idc.set_cmt(0x70A32A, "[UI] Top Box Check Eskill Submenu Ghost Cursor Y-Axis", 0)
    idc.set_name(0x70A32A, "ui_70A32A", idaapi.SN_NOWARN)
    # 70A32D: Top Box Check Eskill Submenu Ghost Cursor X-Axis
    idc.set_cmt(0x70A32D, "[UI] Top Box Check Eskill Submenu Ghost Cursor X-Axis", 0)
    idc.set_name(0x70A32D, "ui_70A32D", idaapi.SN_NOWARN)
    # 70A34F: eskill sub box selection cursor spacing Y-Axis
    idc.set_cmt(0x70A34F, "[UI] eskill sub box selection cursor spacing Y-Axis", 0)
    idc.set_name(0x70A34F, "ui_70A34F", idaapi.SN_NOWARN)
    # 70A353: eskill sub box selection cursor Y-Axis
    idc.set_cmt(0x70A353, "[UI] eskill sub box selection cursor Y-Axis", 0)
    idc.set_name(0x70A353, "ui_70A353", idaapi.SN_NOWARN)
    # 70A3E7: trash menu - right box cursor spacing Y-Axis
    idc.set_cmt(0x70A3E7, "[UI] trash menu - right box cursor spacing Y-Axis", 0)
    idc.set_name(0x70A3E7, "ui_70A3E7", idaapi.SN_NOWARN)
    # 70A3E9: trash menu - right box cursor Y-Axis
    idc.set_cmt(0x70A3E9, "[UI] trash menu - right box cursor Y-Axis", 0)
    idc.set_name(0x70A3E9, "ui_70A3E9", idaapi.SN_NOWARN)
    # 70A3EF: trash menu - right box cursor X-Axis
    idc.set_cmt(0x70A3EF, "[UI] trash menu - right box cursor X-Axis", 0)
    idc.set_name(0x70A3EF, "ui_70A3EF", idaapi.SN_NOWARN)
    # 70A45D: top box menu cursor Y-Axis
    idc.set_cmt(0x70A45D, "[UI] top box menu cursor Y-Axis", 0)
    idc.set_name(0x70A45D, "ui_70A45D", idaapi.SN_NOWARN)
    # 70A4FE: remove menu - right box cursor spacing Y-Axis
    idc.set_cmt(0x70A4FE, "[UI] remove menu - right box cursor spacing Y-Axis", 0)
    idc.set_name(0x70A4FE, "ui_70A4FE", idaapi.SN_NOWARN)
    # 70A500: remove menu - right box cursor Y-Axis
    idc.set_cmt(0x70A500, "[UI] remove menu - right box cursor Y-Axis", 0)
    idc.set_name(0x70A500, "ui_70A500", idaapi.SN_NOWARN)
    # 70A506: remove menu - right box cursor X-Axis
    idc.set_cmt(0x70A506, "[UI] remove menu - right box cursor X-Axis", 0)
    idc.set_name(0x70A506, "ui_70A506", idaapi.SN_NOWARN)
    # 70A525: trash box cursor spacing Y-Axis
    idc.set_cmt(0x70A525, "[UI] trash box cursor spacing Y-Axis", 0)
    idc.set_name(0x70A525, "ui_70A525", idaapi.SN_NOWARN)
    # 70A529: trash box cursor Y-Axis
    idc.set_cmt(0x70A529, "[UI] trash box cursor Y-Axis", 0)
    idc.set_name(0x70A529, "ui_70A529", idaapi.SN_NOWARN)
    # 70A537: trash box cursor X-Axis
    idc.set_cmt(0x70A537, "[UI] trash box cursor X-Axis", 0)
    idc.set_name(0x70A537, "ui_70A537", idaapi.SN_NOWARN)
    # 70A563: trash box first line X-Axis
    idc.set_cmt(0x70A563, "[UI] trash box first line X-Axis", 0)
    idc.set_name(0x70A563, "ui_70A563", idaapi.SN_NOWARN)
    # 70A582: trash box second line Y-Axis
    idc.set_cmt(0x70A582, "[UI] trash box second line Y-Axis", 0)
    idc.set_name(0x70A582, "ui_70A582", idaapi.SN_NOWARN)
    # 70A590: trash box second line X-Axis
    idc.set_cmt(0x70A590, "[UI] trash box second line X-Axis", 0)
    idc.set_name(0x70A590, "ui_70A590", idaapi.SN_NOWARN)
    # 70A5BC: trash box third line X-Axis
    idc.set_cmt(0x70A5BC, "[UI] trash box third line X-Axis", 0)
    idc.set_name(0x70A5BC, "ui_70A5BC", idaapi.SN_NOWARN)
    # 70B0EA: element Y-Axis
    idc.set_cmt(0x70B0EA, "[UI] element Y-Axis", 0)
    idc.set_name(0x70B0EA, "ui_70B0EA", idaapi.SN_NOWARN)
    # 70B0EF: element X-Axis
    idc.set_cmt(0x70B0EF, "[UI] element X-Axis", 0)
    idc.set_name(0x70B0EF, "ui_70B0EF", idaapi.SN_NOWARN)
    # 70B149: Materia Icon Y-Axis
    idc.set_cmt(0x70B149, "[UI] Materia Icon Y-Axis", 0)
    idc.set_name(0x70B149, "ui_70B149", idaapi.SN_NOWARN)
    # 70B1D5: Stars X-Axis
    idc.set_cmt(0x70B1D5, "[UI] Stars X-Axis", 0)
    idc.set_name(0x70B1D5, "ui_70B1D5", idaapi.SN_NOWARN)
    # 70B208: Stars BG X-Axis
    idc.set_cmt(0x70B208, "[UI] Stars BG X-Axis", 0)
    idc.set_name(0x70B208, "ui_70B208", idaapi.SN_NOWARN)
    # 70B22E: Next Level Number Y-Axis
    idc.set_cmt(0x70B22E, "[UI] Next Level Number Y-Axis", 0)
    idc.set_name(0x70B22E, "ui_70B22E", idaapi.SN_NOWARN)
    # 70B233: Next Level Number X-Axis
    idc.set_cmt(0x70B233, "[UI] Next Level Number X-Axis", 0)
    idc.set_name(0x70B233, "ui_70B233", idaapi.SN_NOWARN)
    # 70B264: AP value Y-Axis
    idc.set_cmt(0x70B264, "[UI] AP value Y-Axis", 0)
    idc.set_name(0x70B264, "ui_70B264", idaapi.SN_NOWARN)
    # 70B269: AP value X-Axis
    idc.set_cmt(0x70B269, "[UI] AP value X-Axis", 0)
    idc.set_name(0x70B269, "ui_70B269", idaapi.SN_NOWARN)
    # 70B289: AP MASTER X-Axis
    idc.set_cmt(0x70B289, "[UI] AP MASTER X-Axis", 0)
    idc.set_name(0x70B289, "ui_70B289", idaapi.SN_NOWARN)
    # 70B2A2: Next Level Y-Axis
    idc.set_cmt(0x70B2A2, "[UI] Next Level Y-Axis", 0)
    idc.set_name(0x70B2A2, "ui_70B2A2", idaapi.SN_NOWARN)
    # 70B2A7: Next Level X-Axis
    idc.set_cmt(0x70B2A7, "[UI] Next Level X-Axis", 0)
    idc.set_name(0x70B2A7, "ui_70B2A7", idaapi.SN_NOWARN)
    # 70B2BD: Equip Effect WORD CLONE Y-Axis
    idc.set_cmt(0x70B2BD, "[UI] Equip Effect WORD CLONE Y-Axis", 0)
    idc.set_name(0x70B2BD, "ui_70B2BD", idaapi.SN_NOWARN)
    # 70B2C2: Equip Effect WORD CLONE X-Axis
    idc.set_cmt(0x70B2C2, "[UI] Equip Effect WORD CLONE X-Axis", 0)
    idc.set_name(0x70B2C2, "ui_70B2C2", idaapi.SN_NOWARN)
    # 70B2E0: AP X-Axis
    idc.set_cmt(0x70B2E0, "[UI] AP X-Axis", 0)
    idc.set_name(0x70B2E0, "ui_70B2E0", idaapi.SN_NOWARN)
    # 70B2F9: ability list WORD Y-Axis
    idc.set_cmt(0x70B2F9, "[UI] ability list WORD Y-Axis", 0)
    idc.set_name(0x70B2F9, "ui_70B2F9", idaapi.SN_NOWARN)
    # 70B2FE: ability list WORD X-Axis
    idc.set_cmt(0x70B2FE, "[UI] ability list WORD X-Axis", 0)
    idc.set_name(0x70B2FE, "ui_70B2FE", idaapi.SN_NOWARN)
    # 70B314: Equip Effect WORD Y-Axis
    idc.set_cmt(0x70B314, "[UI] Equip Effect WORD Y-Axis", 0)
    idc.set_name(0x70B314, "ui_70B314", idaapi.SN_NOWARN)
    # 70B319: Equip Effect WORD X-Axis
    idc.set_cmt(0x70B319, "[UI] Equip Effect WORD X-Axis", 0)
    idc.set_name(0x70B319, "ui_70B319", idaapi.SN_NOWARN)
    # 70B3CE: green materia ability text Y-Axis
    idc.set_cmt(0x70B3CE, "[UI] green materia ability text Y-Axis", 0)
    idc.set_name(0x70B3CE, "ui_70B3CE", idaapi.SN_NOWARN)
    # 70B3D4: green materia ability text X-Axis
    idc.set_cmt(0x70B3D4, "[UI] green materia ability text X-Axis", 0)
    idc.set_name(0x70B3D4, "ui_70B3D4", idaapi.SN_NOWARN)
    # 70B411: red materia ability list Y-Axis
    idc.set_cmt(0x70B411, "[UI] red materia ability list Y-Axis", 0)
    idc.set_name(0x70B411, "ui_70B411", idaapi.SN_NOWARN)
    # 70B416: red materia ability list X-Axis
    idc.set_cmt(0x70B416, "[UI] red materia ability list X-Axis", 0)
    idc.set_name(0x70B416, "ui_70B416", idaapi.SN_NOWARN)
    # 70B4A0: yellow materia ability list Y-Axis
    idc.set_cmt(0x70B4A0, "[UI] yellow materia ability list Y-Axis", 0)
    idc.set_name(0x70B4A0, "ui_70B4A0", idaapi.SN_NOWARN)
    # 70B4A6: yellow materia ability list X-Axis
    idc.set_cmt(0x70B4A6, "[UI] yellow materia ability list X-Axis", 0)
    idc.set_name(0x70B4A6, "ui_70B4A6", idaapi.SN_NOWARN)
    # 70B4EE: purple materia MPUP ability list Y-Axis
    idc.set_cmt(0x70B4EE, "[UI] purple materia MPUP ability list Y-Axis", 0)
    idc.set_name(0x70B4EE, "ui_70B4EE", idaapi.SN_NOWARN)
    # 70B4F3: purple materia MPUP ability list X-Axis
    idc.set_cmt(0x70B4F3, "[UI] purple materia MPUP ability list X-Axis", 0)
    idc.set_name(0x70B4F3, "ui_70B4F3", idaapi.SN_NOWARN)
    # 70B511: purple materia MAXMP % number Y-Axis
    idc.set_cmt(0x70B511, "[UI] purple materia MAXMP % number Y-Axis", 0)
    idc.set_name(0x70B511, "ui_70B511", idaapi.SN_NOWARN)
    # 70B516: purple materia MAXMP % number X-Axis
    idc.set_cmt(0x70B516, "[UI] purple materia MAXMP % number X-Axis", 0)
    idc.set_name(0x70B516, "ui_70B516", idaapi.SN_NOWARN)
    # 70B52F: purple materia MAXMP + Y-Axis
    idc.set_cmt(0x70B52F, "[UI] purple materia MAXMP + Y-Axis", 0)
    idc.set_name(0x70B52F, "ui_70B52F", idaapi.SN_NOWARN)
    # 70B534: purple materia MAXMP + X-Axis
    idc.set_cmt(0x70B534, "[UI] purple materia MAXMP + X-Axis", 0)
    idc.set_name(0x70B534, "ui_70B534", idaapi.SN_NOWARN)
    # 70B54A: purple materia MAXMP % Y-Axis
    idc.set_cmt(0x70B54A, "[UI] purple materia MAXMP % Y-Axis", 0)
    idc.set_name(0x70B54A, "ui_70B54A", idaapi.SN_NOWARN)
    # 70B54F: purple materia MAXMP % X-Axis
    idc.set_cmt(0x70B54F, "[UI] purple materia MAXMP % X-Axis", 0)
    idc.set_name(0x70B54F, "ui_70B54F", idaapi.SN_NOWARN)
    # 70B56D: purple materia HPUP ability list Y-Axis
    idc.set_cmt(0x70B56D, "[UI] purple materia HPUP ability list Y-Axis", 0)
    idc.set_name(0x70B56D, "ui_70B56D", idaapi.SN_NOWARN)
    # 70B572: purple materia HPUP ability list X-Axis
    idc.set_cmt(0x70B572, "[UI] purple materia HPUP ability list X-Axis", 0)
    idc.set_name(0x70B572, "ui_70B572", idaapi.SN_NOWARN)
    # 70B591: purple materia MAXHP % number Y-Axis
    idc.set_cmt(0x70B591, "[UI] purple materia MAXHP % number Y-Axis", 0)
    idc.set_name(0x70B591, "ui_70B591", idaapi.SN_NOWARN)
    # 70B596: purple materia MAXHP % number X-Axis
    idc.set_cmt(0x70B596, "[UI] purple materia MAXHP % number X-Axis", 0)
    idc.set_name(0x70B596, "ui_70B596", idaapi.SN_NOWARN)
    # 70B5AF: purple materia MAXHP + Y-Axis
    idc.set_cmt(0x70B5AF, "[UI] purple materia MAXHP + Y-Axis", 0)
    idc.set_name(0x70B5AF, "ui_70B5AF", idaapi.SN_NOWARN)
    # 70B5B4: purple materia MAXHP + X-Axis
    idc.set_cmt(0x70B5B4, "[UI] purple materia MAXHP + X-Axis", 0)
    idc.set_name(0x70B5B4, "ui_70B5B4", idaapi.SN_NOWARN)
    # 70B5CA: purple materia MAXHP % Y-Axis
    idc.set_cmt(0x70B5CA, "[UI] purple materia MAXHP % Y-Axis", 0)
    idc.set_name(0x70B5CA, "ui_70B5CA", idaapi.SN_NOWARN)
    # 70B5CF: purple materia MAXHP % X-Axis
    idc.set_cmt(0x70B5CF, "[UI] purple materia MAXHP % X-Axis", 0)
    idc.set_name(0x70B5CF, "ui_70B5CF", idaapi.SN_NOWARN)
    # 70B5ED: purple materia SPEED ability list Y-Axis
    idc.set_cmt(0x70B5ED, "[UI] purple materia SPEED ability list Y-Axis", 0)
    idc.set_name(0x70B5ED, "ui_70B5ED", idaapi.SN_NOWARN)
    # 70B5F2: purple materia SPEED ability list X-Axis
    idc.set_cmt(0x70B5F2, "[UI] purple materia SPEED ability list X-Axis", 0)
    idc.set_name(0x70B5F2, "ui_70B5F2", idaapi.SN_NOWARN)
    # 70B611: purple materia Agility % number Y-Axis
    idc.set_cmt(0x70B611, "[UI] purple materia Agility % number Y-Axis", 0)
    idc.set_name(0x70B611, "ui_70B611", idaapi.SN_NOWARN)
    # 70B616: purple materia Agility % number X-Axis
    idc.set_cmt(0x70B616, "[UI] purple materia Agility % number X-Axis", 0)
    idc.set_name(0x70B616, "ui_70B616", idaapi.SN_NOWARN)
    # 70B62F: purple materia Agility + Y-Axis
    idc.set_cmt(0x70B62F, "[UI] purple materia Agility + Y-Axis", 0)
    idc.set_name(0x70B62F, "ui_70B62F", idaapi.SN_NOWARN)
    # 70B634: purple materia Agility + X-Axis
    idc.set_cmt(0x70B634, "[UI] purple materia Agility + X-Axis", 0)
    idc.set_name(0x70B634, "ui_70B634", idaapi.SN_NOWARN)
    # 70B64D: purple materia Agility % Y-Axis
    idc.set_cmt(0x70B64D, "[UI] purple materia Agility % Y-Axis", 0)
    idc.set_name(0x70B64D, "ui_70B64D", idaapi.SN_NOWARN)
    # 70B652: purple materia Agility % X-Axis
    idc.set_cmt(0x70B652, "[UI] purple materia Agility % X-Axis", 0)
    idc.set_name(0x70B652, "ui_70B652", idaapi.SN_NOWARN)
    # 70B66D: purple materia MAGIC ability list Y-Axis
    idc.set_cmt(0x70B66D, "[UI] purple materia MAGIC ability list Y-Axis", 0)
    idc.set_name(0x70B66D, "ui_70B66D", idaapi.SN_NOWARN)
    # 70B672: purple materia MAGIC ability list X-Axis
    idc.set_cmt(0x70B672, "[UI] purple materia MAGIC ability list X-Axis", 0)
    idc.set_name(0x70B672, "ui_70B672", idaapi.SN_NOWARN)
    # 70B690: purple materia Magic % number Y-Axis
    idc.set_cmt(0x70B690, "[UI] purple materia Magic % number Y-Axis", 0)
    idc.set_name(0x70B690, "ui_70B690", idaapi.SN_NOWARN)
    # 70B695: purple materia Magic % number X-Axis
    idc.set_cmt(0x70B695, "[UI] purple materia Magic % number X-Axis", 0)
    idc.set_name(0x70B695, "ui_70B695", idaapi.SN_NOWARN)
    # 70B6AB: purple materia Magic + Y-Axis
    idc.set_cmt(0x70B6AB, "[UI] purple materia Magic + Y-Axis", 0)
    idc.set_name(0x70B6AB, "ui_70B6AB", idaapi.SN_NOWARN)
    # 70B6B0: purple materia Magic + X-Axis
    idc.set_cmt(0x70B6B0, "[UI] purple materia Magic + X-Axis", 0)
    idc.set_name(0x70B6B0, "ui_70B6B0", idaapi.SN_NOWARN)
    # 70B6C6: purple materia Magic % Y-Axis
    idc.set_cmt(0x70B6C6, "[UI] purple materia Magic % Y-Axis", 0)
    idc.set_name(0x70B6C6, "ui_70B6C6", idaapi.SN_NOWARN)
    # 70B6CB: purple materia Magic % X-Axis
    idc.set_cmt(0x70B6CB, "[UI] purple materia Magic % X-Axis", 0)
    idc.set_name(0x70B6CB, "ui_70B6CB", idaapi.SN_NOWARN)
    # 70B6E9: purple materia LUCK ability list Y-Axis
    idc.set_cmt(0x70B6E9, "[UI] purple materia LUCK ability list Y-Axis", 0)
    idc.set_name(0x70B6E9, "ui_70B6E9", idaapi.SN_NOWARN)
    # 70B6EE: purple materia LUCK ability list X-Axis
    idc.set_cmt(0x70B6EE, "[UI] purple materia LUCK ability list X-Axis", 0)
    idc.set_name(0x70B6EE, "ui_70B6EE", idaapi.SN_NOWARN)
    # 70B70D: purple materia Luck % number Y-Axis
    idc.set_cmt(0x70B70D, "[UI] purple materia Luck % number Y-Axis", 0)
    idc.set_name(0x70B70D, "ui_70B70D", idaapi.SN_NOWARN)
    # 70B712: purple materia Luck % number X-Axis
    idc.set_cmt(0x70B712, "[UI] purple materia Luck % number X-Axis", 0)
    idc.set_name(0x70B712, "ui_70B712", idaapi.SN_NOWARN)
    # 70B728: purple materia Luck + Y-Axis
    idc.set_cmt(0x70B728, "[UI] purple materia Luck + Y-Axis", 0)
    idc.set_name(0x70B728, "ui_70B728", idaapi.SN_NOWARN)
    # 70B72D: purple materia Luck + X-Axis
    idc.set_cmt(0x70B72D, "[UI] purple materia Luck + X-Axis", 0)
    idc.set_name(0x70B72D, "ui_70B72D", idaapi.SN_NOWARN)
    # 70B743: purple materia Luck % Y-Axis
    idc.set_cmt(0x70B743, "[UI] purple materia Luck % Y-Axis", 0)
    idc.set_name(0x70B743, "ui_70B743", idaapi.SN_NOWARN)
    # 70B748: purple materia Luck % X-Axis
    idc.set_cmt(0x70B748, "[UI] purple materia Luck % X-Axis", 0)
    idc.set_name(0x70B748, "ui_70B748", idaapi.SN_NOWARN)
    # 70B763: purple materia COVER ability list Y-Axis
    idc.set_cmt(0x70B763, "[UI] purple materia COVER ability list Y-Axis", 0)
    idc.set_name(0x70B763, "ui_70B763", idaapi.SN_NOWARN)
    # 70B768: purple materia COVER ability list X-Axis
    idc.set_cmt(0x70B768, "[UI] purple materia COVER ability list X-Axis", 0)
    idc.set_name(0x70B768, "ui_70B768", idaapi.SN_NOWARN)
    # 70B787: purple materia Cover % number Y-Axis
    idc.set_cmt(0x70B787, "[UI] purple materia Cover % number Y-Axis", 0)
    idc.set_name(0x70B787, "ui_70B787", idaapi.SN_NOWARN)
    # 70B78C: purple materia Cover % number X-Axis
    idc.set_cmt(0x70B78C, "[UI] purple materia Cover % number X-Axis", 0)
    idc.set_name(0x70B78C, "ui_70B78C", idaapi.SN_NOWARN)
    # 70B7A2: purple materia Cover + Y-Axis
    idc.set_cmt(0x70B7A2, "[UI] purple materia Cover + Y-Axis", 0)
    idc.set_name(0x70B7A2, "ui_70B7A2", idaapi.SN_NOWARN)
    # 70B7A7: purple materia Cover + X-Axis
    idc.set_cmt(0x70B7A7, "[UI] purple materia Cover + X-Axis", 0)
    idc.set_name(0x70B7A7, "ui_70B7A7", idaapi.SN_NOWARN)
    # 70B7BD: purple materia Cover % Y-Axis
    idc.set_cmt(0x70B7BD, "[UI] purple materia Cover % Y-Axis", 0)
    idc.set_name(0x70B7BD, "ui_70B7BD", idaapi.SN_NOWARN)
    # 70B7C2: purple materia Cover % X-Axis
    idc.set_cmt(0x70B7C2, "[UI] purple materia Cover % X-Axis", 0)
    idc.set_name(0x70B7C2, "ui_70B7C2", idaapi.SN_NOWARN)
    # 70B7E7: purple materia MEGAALL/PREEMPT/COUNTER/LONG/CHOCOB
    idc.set_cmt(0x70B7E7, "[UI] purple materia MEGAALL/PREEMPT/COUNTER/LONG/CHOCOBO/AWAY/LURE/GILUP/EXPUP ability list Y-Axis", 0)
    idc.set_name(0x70B7E7, "ui_70B7E7", idaapi.SN_NOWARN)
    # 70B7EC: purple materia MEGAALL/PREEMPT/COUNTER/LONG/CHOCOB
    idc.set_cmt(0x70B7EC, "[UI] purple materia MEGAALL/PREEMPT/COUNTER/LONG/CHOCOBO/AWAY/LURE/GILUP/EXPUP ability list X-Axis", 0)
    idc.set_name(0x70B7EC, "ui_70B7EC", idaapi.SN_NOWARN)
    # 70B80C: blue materia/purple materia HP<>MP/UNDERWATER abil
    idc.set_cmt(0x70B80C, "[UI] blue materia/purple materia HP<>MP/UNDERWATER ability list Y-Axis", 0)
    idc.set_name(0x70B80C, "ui_70B80C", idaapi.SN_NOWARN)
    # 70B811: blue materia/purple materia HP<>MP/UNDERWATER abil
    idc.set_cmt(0x70B811, "[UI] blue materia/purple materia HP<>MP/UNDERWATER ability list X-Axis", 0)
    idc.set_name(0x70B811, "ui_70B811", idaapi.SN_NOWARN)
    # 70BAE9: EQUIP EFFECT - SYMBOL Y-AXIS
    idc.set_cmt(0x70BAE9, "[UI] EQUIP EFFECT - SYMBOL Y-AXIS", 0)
    idc.set_name(0x70BAE9, "ui_70BAE9", idaapi.SN_NOWARN)
    # 70BAEF: EQUIP EFFECT - SYMBOL X-AXIS
    idc.set_cmt(0x70BAEF, "[UI] EQUIP EFFECT - SYMBOL X-AXIS", 0)
    idc.set_name(0x70BAEF, "ui_70BAEF", idaapi.SN_NOWARN)
    # 70BB17: EQUIP EFFECT + SYMBOL Y-AXIS
    idc.set_cmt(0x70BB17, "[UI] EQUIP EFFECT + SYMBOL Y-AXIS", 0)
    idc.set_name(0x70BB17, "ui_70BB17", idaapi.SN_NOWARN)
    # 70BB1D: EQUIP EFFECT + SYMBOL X-AXIS
    idc.set_cmt(0x70BB1D, "[UI] EQUIP EFFECT + SYMBOL X-AXIS", 0)
    idc.set_name(0x70BB1D, "ui_70BB1D", idaapi.SN_NOWARN)
    # 70BB5A: EQUIP EFFECT NUMBERS Y-AXIS
    idc.set_cmt(0x70BB5A, "[UI] EQUIP EFFECT NUMBERS Y-AXIS", 0)
    idc.set_name(0x70BB5A, "ui_70BB5A", idaapi.SN_NOWARN)
    # 70BB60: EQUIP EFFECT NUMBERS X-AXIS
    idc.set_cmt(0x70BB60, "[UI] EQUIP EFFECT NUMBERS X-AXIS", 0)
    idc.set_name(0x70BB60, "ui_70BB60", idaapi.SN_NOWARN)
    # 70BB8A: EQUIP EFFECT NAME TEXT Y-AXIS
    idc.set_cmt(0x70BB8A, "[UI] EQUIP EFFECT NAME TEXT Y-AXIS", 0)
    idc.set_name(0x70BB8A, "ui_70BB8A", idaapi.SN_NOWARN)
    # 70BB90: EQUIP EFFECT NAME TEXT X-AXIS
    idc.set_cmt(0x70BB90, "[UI] EQUIP EFFECT NAME TEXT X-AXIS", 0)
    idc.set_name(0x70BB90, "ui_70BB90", idaapi.SN_NOWARN)
    # 70BBB6: EQUIP EFFECT % SYMBOL Y-AXIS
    idc.set_cmt(0x70BBB6, "[UI] EQUIP EFFECT % SYMBOL Y-AXIS", 0)
    idc.set_name(0x70BBB6, "ui_70BBB6", idaapi.SN_NOWARN)
    # 70BBBC: EQUIP EFFECT % SYMBOL X-AXIS
    idc.set_cmt(0x70BBBC, "[UI] EQUIP EFFECT % SYMBOL X-AXIS", 0)
    idc.set_name(0x70BBBC, "ui_70BBBC", idaapi.SN_NOWARN)
    # 70C78D: right box number on screen
    idc.set_cmt(0x70C78D, "[UI] right box number on screen", 0)
    idc.set_name(0x70C78D, "ui_70C78D", idaapi.SN_NOWARN)
    # 70C7F6: right box text spacing Y-Axis
    idc.set_cmt(0x70C7F6, "[UI] right box text spacing Y-Axis", 0)
    idc.set_name(0x70C7F6, "ui_70C7F6", idaapi.SN_NOWARN)
    # 70C809: right box text Y-Axis
    idc.set_cmt(0x70C809, "[UI] right box text Y-Axis", 0)
    idc.set_name(0x70C809, "ui_70C809", idaapi.SN_NOWARN)
    # 70C80F: right box text X-Axis
    idc.set_cmt(0x70C80F, "[UI] right box text X-Axis", 0)
    idc.set_name(0x70C80F, "ui_70C80F", idaapi.SN_NOWARN)
    # 70C827: right box row related
    idc.set_cmt(0x70C827, "[UI] right box row related", 0)
    idc.set_name(0x70C827, "ui_70C827", idaapi.SN_NOWARN)
    # 70C84D: materia menu - right box scroll bar X-Axis
    idc.set_cmt(0x70C84D, "[UI] materia menu - right box scroll bar X-Axis", 0)
    idc.set_name(0x70C84D, "ui_70C84D", idaapi.SN_NOWARN)
    # 70C856: right box scroll bar Y-Axis
    idc.set_cmt(0x70C856, "[UI] right box scroll bar Y-Axis", 0)
    idc.set_name(0x70C856, "ui_70C856", idaapi.SN_NOWARN)
    # 70C85F: materia menu - right box scroll bar width
    idc.set_cmt(0x70C85F, "[UI] materia menu - right box scroll bar width", 0)
    idc.set_name(0x70C85F, "ui_70C85F", idaapi.SN_NOWARN)
    # 70C8F8: right box materia spacing Y-Axis
    idc.set_cmt(0x70C8F8, "[UI] right box materia spacing Y-Axis", 0)
    idc.set_name(0x70C8F8, "ui_70C8F8", idaapi.SN_NOWARN)
    # 70C90B: right box materia Y-Axis
    idc.set_cmt(0x70C90B, "[UI] right box materia Y-Axis", 0)
    idc.set_name(0x70C90B, "ui_70C90B", idaapi.SN_NOWARN)
    # 70C911: right box materia X-Axis
    idc.set_cmt(0x70C911, "[UI] right box materia X-Axis", 0)
    idc.set_name(0x70C911, "ui_70C911", idaapi.SN_NOWARN)
    # 70D01D: weapon name X-Axis
    idc.set_cmt(0x70D01D, "[UI] weapon name X-Axis", 0)
    idc.set_name(0x70D01D, "ui_70D01D", idaapi.SN_NOWARN)
    # 70D05A: armour name X-Axis
    idc.set_cmt(0x70D05A, "[UI] armour name X-Axis", 0)
    idc.set_name(0x70D05A, "ui_70D05A", idaapi.SN_NOWARN)
    # 70D075: Wpn WORD X-Axis
    idc.set_cmt(0x70D075, "[UI] Wpn WORD X-Axis", 0)
    idc.set_name(0x70D075, "ui_70D075", idaapi.SN_NOWARN)
    # 70D090: Arm WORD X-Axis
    idc.set_cmt(0x70D090, "[UI] Arm WORD X-Axis", 0)
    idc.set_name(0x70D090, "ui_70D090", idaapi.SN_NOWARN)
    # 70D0A9: Check WORD Y-Axis
    idc.set_cmt(0x70D0A9, "[UI] Check WORD Y-Axis", 0)
    idc.set_name(0x70D0A9, "ui_70D0A9", idaapi.SN_NOWARN)
    # 70D0D0: Arrange WORD Y-Axis
    idc.set_cmt(0x70D0D0, "[UI] Arrange WORD Y-Axis", 0)
    idc.set_name(0x70D0D0, "ui_70D0D0", idaapi.SN_NOWARN)
    # 70D7DE: allow materia discard menu to use page up and page
    idc.set_cmt(0x70D7DE, "[UI] allow materia discard menu to use page up and page down", 0)
    idc.set_name(0x70D7DE, "ui_70D7DE", idaapi.SN_NOWARN)
    # 70D7F6: trash menu - right box cursor row count Y-Axis (fu
    idc.set_cmt(0x70D7F6, "[UI] trash menu - right box cursor row count Y-Axis (full menu refresh)", 0)
    idc.set_name(0x70D7F6, "ui_70D7F6", idaapi.SN_NOWARN)
    # 70DDE5: magic sub box cursor row count Y-Axis (full menu r
    idc.set_cmt(0x70DDE5, "[UI] magic sub box cursor row count Y-Axis (full menu refresh)", 0)
    idc.set_name(0x70DDE5, "ui_70DDE5", idaapi.SN_NOWARN)
    # 70DE1A: summon sub cursor row count Y-Axis (full menu refr
    idc.set_cmt(0x70DE1A, "[UI] summon sub cursor row count Y-Axis (full menu refresh)", 0)
    idc.set_name(0x70DE1A, "ui_70DE1A", idaapi.SN_NOWARN)
    # 70DE4F: eskill sub box cursor row count Y-Axis (full menu 
    idc.set_cmt(0x70DE4F, "[UI] eskill sub box cursor row count Y-Axis (full menu refresh)", 0)
    idc.set_name(0x70DE4F, "ui_70DE4F", idaapi.SN_NOWARN)
    # 70E9BF: Materia slots BG Width
    idc.set_cmt(0x70E9BF, "[UI] Materia slots BG Width", 0)
    idc.set_name(0x70E9BF, "ui_70E9BF", idaapi.SN_NOWARN)
    # 70E9C5: Materia slots BG Height
    idc.set_cmt(0x70E9C5, "[UI] Materia slots BG Height", 0)
    idc.set_name(0x70E9C5, "ui_70E9C5", idaapi.SN_NOWARN)
    # 70EBAD: avatar Y-Axis
    idc.set_cmt(0x70EBAD, "[UI] avatar Y-Axis", 0)
    idc.set_name(0x70EBAD, "ui_70EBAD", idaapi.SN_NOWARN)
    # 70EBAF: avatar X-Axis
    idc.set_cmt(0x70EBAF, "[UI] avatar X-Axis", 0)
    idc.set_name(0x70EBAF, "ui_70EBAF", idaapi.SN_NOWARN)
    # 70EC8A: exchange menu - right box cursor row count Y-Axis 
    idc.set_cmt(0x70EC8A, "[UI] exchange menu - right box cursor row count Y-Axis (full menu refresh)", 0)
    idc.set_name(0x70EC8A, "ui_70EC8A", idaapi.SN_NOWARN)
    # 70EDAB: exchange menu - ghost cursor character spacing Y-A
    idc.set_cmt(0x70EDAB, "[UI] exchange menu - ghost cursor character spacing Y-Axis", 0)
    idc.set_name(0x70EDAB, "ui_70EDAB", idaapi.SN_NOWARN)
    # 70EDAF: exchange menu - ghost cursor Y-Axis
    idc.set_cmt(0x70EDAF, "[UI] exchange menu - ghost cursor Y-Axis", 0)
    idc.set_name(0x70EDAF, "ui_70EDAF", idaapi.SN_NOWARN)
    # 70EDC6: exchange menu - ghost cursor spacing X-Axis
    idc.set_cmt(0x70EDC6, "[UI] exchange menu - ghost cursor spacing X-Axis", 0)
    idc.set_name(0x70EDC6, "ui_70EDC6", idaapi.SN_NOWARN)
    # 70EDC9: exchange menu - ghost cursor X-Axis
    idc.set_cmt(0x70EDC9, "[UI] exchange menu - ghost cursor X-Axis", 0)
    idc.set_name(0x70EDC9, "ui_70EDC9", idaapi.SN_NOWARN)
    # 70EE0B: exchange menu row ghost cursor Y-Axis
    idc.set_cmt(0x70EE0B, "[UI] exchange menu row ghost cursor Y-Axis", 0)
    idc.set_name(0x70EE0B, "ui_70EE0B", idaapi.SN_NOWARN)
    # 70EE19: exchange menu row ghost cursor X-Axis
    idc.set_cmt(0x70EE19, "[UI] exchange menu row ghost cursor X-Axis", 0)
    idc.set_name(0x70EE19, "ui_70EE19", idaapi.SN_NOWARN)
    # 70EE6A: exchange menu - selection cursor Y-Axis
    idc.set_cmt(0x70EE6A, "[UI] exchange menu - selection cursor Y-Axis", 0)
    idc.set_name(0x70EE6A, "ui_70EE6A", idaapi.SN_NOWARN)
    # 70EEE0: materia menu - exchange menu - left boxes top row 
    idc.set_cmt(0x70EEE0, "[UI] materia menu - exchange menu - left boxes top row Description text Y-Axis", 0)
    idc.set_name(0x70EEE0, "ui_70EEE0", idaapi.SN_NOWARN)
    # 70EEFA: exchange menu - left boxes top row materia name an
    idc.set_cmt(0x70EEFA, "[UI] exchange menu - left boxes top row materia name and icon Y-Axis", 0)
    idc.set_name(0x70EEFA, "ui_70EEFA", idaapi.SN_NOWARN)
    # 70EF40: materia menu - exchange menu - left boxes bottom r
    idc.set_cmt(0x70EF40, "[UI] materia menu - exchange menu - left boxes bottom row Description text Y-Axis", 0)
    idc.set_name(0x70EF40, "ui_70EF40", idaapi.SN_NOWARN)
    # 70EF59: exchange menu - left boxes bottom row materia name
    idc.set_cmt(0x70EF59, "[UI] exchange menu - left boxes bottom row materia name and icon Y-Axis", 0)
    idc.set_name(0x70EF59, "ui_70EF59", idaapi.SN_NOWARN)
    # 70EF82: exchange menu - right box cursor spacing Y-Axis
    idc.set_cmt(0x70EF82, "[UI] exchange menu - right box cursor spacing Y-Axis", 0)
    idc.set_name(0x70EF82, "ui_70EF82", idaapi.SN_NOWARN)
    # 70EF86: exchange menu - right box cursor Y-Axis
    idc.set_cmt(0x70EF86, "[UI] exchange menu - right box cursor Y-Axis", 0)
    idc.set_name(0x70EF86, "ui_70EF86", idaapi.SN_NOWARN)
    # 70EF94: exchange menu - right box cursor X-Axis
    idc.set_cmt(0x70EF94, "[UI] exchange menu - right box cursor X-Axis", 0)
    idc.set_name(0x70EF94, "ui_70EF94", idaapi.SN_NOWARN)
    # 70EFE0: materia menu - exchange menu - right box materia D
    idc.set_cmt(0x70EFE0, "[UI] materia menu - exchange menu - right box materia Description text Y-Axis", 0)
    idc.set_name(0x70EFE0, "ui_70EFE0", idaapi.SN_NOWARN)
    # 70F028: exchange menu row selection cursor Y-Axis
    idc.set_cmt(0x70F028, "[UI] exchange menu row selection cursor Y-Axis", 0)
    idc.set_name(0x70F028, "ui_70F028", idaapi.SN_NOWARN)
    # 70F02B: exchange menu row selection cursor X-Axis
    idc.set_cmt(0x70F02B, "[UI] exchange menu row selection cursor X-Axis", 0)
    idc.set_name(0x70F02B, "ui_70F02B", idaapi.SN_NOWARN)
    # 70F14A: exchange menu left boxes top slots Y-Axis
    idc.set_cmt(0x70F14A, "[UI] exchange menu left boxes top slots Y-Axis", 0)
    idc.set_name(0x70F14A, "ui_70F14A", idaapi.SN_NOWARN)
    # 70F1A2: exchange menu left boxes bottom slots Y-Axis
    idc.set_cmt(0x70F1A2, "[UI] exchange menu left boxes bottom slots Y-Axis", 0)
    idc.set_name(0x70F1A2, "ui_70F1A2", idaapi.SN_NOWARN)
    # 70F1F9: exchange menu left boxes Wpn. Y-Axis
    idc.set_cmt(0x70F1F9, "[UI] exchange menu left boxes Wpn. Y-Axis", 0)
    idc.set_name(0x70F1F9, "ui_70F1F9", idaapi.SN_NOWARN)
    # 70F21B: exchange menu left boxes Arm. Y-Axis
    idc.set_cmt(0x70F21B, "[UI] exchange menu left boxes Arm. Y-Axis", 0)
    idc.set_name(0x70F21B, "ui_70F21B", idaapi.SN_NOWARN)
    # 70F298: exchange menu - left scroll bar X-Axis
    idc.set_cmt(0x70F298, "[UI] exchange menu - left scroll bar X-Axis", 0)
    idc.set_name(0x70F298, "ui_70F298", idaapi.SN_NOWARN)
    # 70F299: materia menu - exchange menu - left scroll bar X-A
    idc.set_cmt(0x70F299, "[UI] materia menu - exchange menu - left scroll bar X-Axis", 0)
    idc.set_name(0x70F299, "ui_70F299", idaapi.SN_NOWARN)
    # 70F2B1: materia menu - exchange menu - left scroll bar wid
    idc.set_cmt(0x70F2B1, "[UI] materia menu - exchange menu - left scroll bar width", 0)
    idc.set_name(0x70F2B1, "ui_70F2B1", idaapi.SN_NOWARN)
    # 70F308: exchange menu - right box contents X-Axis
    idc.set_cmt(0x70F308, "[UI] exchange menu - right box contents X-Axis", 0)
    idc.set_name(0x70F308, "ui_70F308", idaapi.SN_NOWARN)
    # 70F30F: exchange menu - right box text Y-Axis
    idc.set_cmt(0x70F30F, "[UI] exchange menu - right box text Y-Axis", 0)
    idc.set_name(0x70F30F, "ui_70F30F", idaapi.SN_NOWARN)
    # 70F321: exchange menu - right box count
    idc.set_cmt(0x70F321, "[UI] exchange menu - right box count", 0)
    idc.set_name(0x70F321, "ui_70F321", idaapi.SN_NOWARN)
    # 70F37E: exchange menu - right box text spacing Y-Axis
    idc.set_cmt(0x70F37E, "[UI] exchange menu - right box text spacing Y-Axis", 0)
    idc.set_name(0x70F37E, "ui_70F37E", idaapi.SN_NOWARN)
    # 70F3A5: exchange menu - right scroll bar height
    idc.set_cmt(0x70F3A5, "[UI] exchange menu - right scroll bar height", 0)
    idc.set_name(0x70F3A5, "ui_70F3A5", idaapi.SN_NOWARN)
    # 70F3C5: materia menu - exchange menu - right scroll bar X-
    idc.set_cmt(0x70F3C5, "[UI] materia menu - exchange menu - right scroll bar X-Axis", 0)
    idc.set_name(0x70F3C5, "ui_70F3C5", idaapi.SN_NOWARN)
    # 70F3D7: materia menu - exchange menu - right scroll bar wi
    idc.set_cmt(0x70F3D7, "[UI] materia menu - exchange menu - right scroll bar width", 0)
    idc.set_name(0x70F3D7, "ui_70F3D7", idaapi.SN_NOWARN)
    # 70F460: exchange menu - right box materia spacing Y-Axis
    idc.set_cmt(0x70F460, "[UI] exchange menu - right box materia spacing Y-Axis", 0)
    idc.set_name(0x70F460, "ui_70F460", idaapi.SN_NOWARN)
    # 70F466: exchange menu - right box materia Y-Axis
    idc.set_cmt(0x70F466, "[UI] exchange menu - right box materia Y-Axis", 0)
    idc.set_name(0x70F466, "ui_70F466", idaapi.SN_NOWARN)
    # 70F479: exchange menu - right box materia X-Axis 02
    idc.set_cmt(0x70F479, "[UI] exchange menu - right box materia X-Axis 02", 0)
    idc.set_name(0x70F479, "ui_70F479", idaapi.SN_NOWARN)
    # 70F501: exchange menu - materia icon Y-Axis
    idc.set_cmt(0x70F501, "[UI] exchange menu - materia icon Y-Axis", 0)
    idc.set_name(0x70F501, "ui_70F501", idaapi.SN_NOWARN)
    # 710CDC: magic box cursor row count Y-Axis (refresh menu)
    idc.set_cmt(0x710CDC, "[UI] magic box cursor row count Y-Axis (refresh menu)", 0)
    idc.set_name(0x710CDC, "ui_710CDC", idaapi.SN_NOWARN)
    # 710D05: summon box cursor row count Y-Axis (refresh menu)
    idc.set_cmt(0x710D05, "[UI] summon box cursor row count Y-Axis (refresh menu)", 0)
    idc.set_name(0x710D05, "ui_710D05", idaapi.SN_NOWARN)
    # 710D2E: eskill box cursor row count Y-Axis (refresh menu)
    idc.set_cmt(0x710D2E, "[UI] eskill box cursor row count Y-Axis (refresh menu)", 0)
    idc.set_name(0x710D2E, "ui_710D2E", idaapi.SN_NOWARN)
    # 710EAA: cursor Y-Axis
    idc.set_cmt(0x710EAA, "[UI] cursor Y-Axis", 0)
    idc.set_name(0x710EAA, "ui_710EAA", idaapi.SN_NOWARN)
    # 710EB8: cursor X-Axis
    idc.set_cmt(0x710EB8, "[UI] cursor X-Axis", 0)
    idc.set_name(0x710EB8, "ui_710EB8", idaapi.SN_NOWARN)
    # 711061: magic box selection box hp/mp/lv stats Y-Axis
    idc.set_cmt(0x711061, "[UI] magic box selection box hp/mp/lv stats Y-Axis", 0)
    idc.set_name(0x711061, "ui_711061", idaapi.SN_NOWARN)
    # 711089: magic box selection box avatars Y-Axis
    idc.set_cmt(0x711089, "[UI] magic box selection box avatars Y-Axis", 0)
    idc.set_name(0x711089, "ui_711089", idaapi.SN_NOWARN)
    # 7110EA: magic box selection box description text X-Axis
    idc.set_cmt(0x7110EA, "[UI] magic box selection box description text X-Axis", 0)
    idc.set_name(0x7110EA, "ui_7110EA", idaapi.SN_NOWARN)
    # 711104: magic box selection box description box width
    idc.set_cmt(0x711104, "[UI] magic box selection box description box width", 0)
    idc.set_name(0x711104, "ui_711104", idaapi.SN_NOWARN)
    # 711182: magic box ghost cursor spacing Y-Axis
    idc.set_cmt(0x711182, "[UI] magic box ghost cursor spacing Y-Axis", 0)
    idc.set_name(0x711182, "ui_711182", idaapi.SN_NOWARN)
    # 711186: magic box ghost cursor Y-Axis
    idc.set_cmt(0x711186, "[UI] magic box ghost cursor Y-Axis", 0)
    idc.set_name(0x711186, "ui_711186", idaapi.SN_NOWARN)
    # 711199: magic box ghost cursor spacing X-Axis
    idc.set_cmt(0x711199, "[UI] magic box ghost cursor spacing X-Axis", 0)
    idc.set_name(0x711199, "ui_711199", idaapi.SN_NOWARN)
    # 71119D: magic box ghost cursor X-Axis
    idc.set_cmt(0x71119D, "[UI] magic box ghost cursor X-Axis", 0)
    idc.set_name(0x71119D, "ui_71119D", idaapi.SN_NOWARN)
    # 7111BC: magic box cursor spacing Y-Axis
    idc.set_cmt(0x7111BC, "[UI] magic box cursor spacing Y-Axis", 0)
    idc.set_name(0x7111BC, "ui_7111BC", idaapi.SN_NOWARN)
    # 7111C0: magic box cursor Y-Axis
    idc.set_cmt(0x7111C0, "[UI] magic box cursor Y-Axis", 0)
    idc.set_name(0x7111C0, "ui_7111C0", idaapi.SN_NOWARN)
    # 7111D4: magic box cursor spacing X-Axis
    idc.set_cmt(0x7111D4, "[UI] magic box cursor spacing X-Axis", 0)
    idc.set_name(0x7111D4, "ui_7111D4", idaapi.SN_NOWARN)
    # 7111D8: magic box cursor X-Axis
    idc.set_cmt(0x7111D8, "[UI] magic box cursor X-Axis", 0)
    idc.set_name(0x7111D8, "ui_7111D8", idaapi.SN_NOWARN)
    # 711220: Magic Menu - Description Y-Axis
    idc.set_cmt(0x711220, "[UI] Magic Menu - Description Y-Axis", 0)
    idc.set_name(0x711220, "ui_711220", idaapi.SN_NOWARN)
    # 711244: Added Ability Y-Axis
    idc.set_cmt(0x711244, "[UI] Added Ability Y-Axis", 0)
    idc.set_name(0x711244, "ui_711244", idaapi.SN_NOWARN)
    # 711389: Added Ability Turbo/ALL Y-Axis
    idc.set_cmt(0x711389, "[UI] Added Ability Turbo/ALL Y-Axis", 0)
    idc.set_name(0x711389, "ui_711389", idaapi.SN_NOWARN)
    # 7113A3: Quadra Magic X-Axis
    idc.set_cmt(0x7113A3, "[UI] Quadra Magic X-Axis", 0)
    idc.set_name(0x7113A3, "ui_7113A3", idaapi.SN_NOWARN)
    # 7113A4: Added Ability Turbo/ALL X-Axis
    idc.set_cmt(0x7113A4, "[UI] Added Ability Turbo/ALL X-Axis", 0)
    idc.set_name(0x7113A4, "ui_7113A4", idaapi.SN_NOWARN)
    # 7113E7: All Number Y-Axis
    idc.set_cmt(0x7113E7, "[UI] All Number Y-Axis", 0)
    idc.set_name(0x7113E7, "ui_7113E7", idaapi.SN_NOWARN)
    # 711404: All Number X-Axis
    idc.set_cmt(0x711404, "[UI] All Number X-Axis", 0)
    idc.set_name(0x711404, "ui_711404", idaapi.SN_NOWARN)
    # 711439: All X Y-Axis
    idc.set_cmt(0x711439, "[UI] All X Y-Axis", 0)
    idc.set_name(0x711439, "ui_711439", idaapi.SN_NOWARN)
    # 711456: All X X-Axis
    idc.set_cmt(0x711456, "[UI] All X X-Axis", 0)
    idc.set_name(0x711456, "ui_711456", idaapi.SN_NOWARN)
    # 71149D: Quadra Magic Number Y-Axis
    idc.set_cmt(0x71149D, "[UI] Quadra Magic Number Y-Axis", 0)
    idc.set_name(0x71149D, "ui_71149D", idaapi.SN_NOWARN)
    # 7114BA: Quadra Magic Number X-Axis
    idc.set_cmt(0x7114BA, "[UI] Quadra Magic Number X-Axis", 0)
    idc.set_name(0x7114BA, "ui_7114BA", idaapi.SN_NOWARN)
    # 7114EF: Quadra Magic X Y-Axis
    idc.set_cmt(0x7114EF, "[UI] Quadra Magic X Y-Axis", 0)
    idc.set_name(0x7114EF, "ui_7114EF", idaapi.SN_NOWARN)
    # 71150C: Quadra Magic X X-Axis
    idc.set_cmt(0x71150C, "[UI] Quadra Magic X X-Axis", 0)
    idc.set_name(0x71150C, "ui_71150C", idaapi.SN_NOWARN)
    # 711552: Turbo MP number Y-Axis
    idc.set_cmt(0x711552, "[UI] Turbo MP number Y-Axis", 0)
    idc.set_name(0x711552, "ui_711552", idaapi.SN_NOWARN)
    # 7115A8: NOTHING Y-Axis
    idc.set_cmt(0x7115A8, "[UI] NOTHING Y-Axis", 0)
    idc.set_name(0x7115A8, "ui_7115A8", idaapi.SN_NOWARN)
    # 7115B4: NOTHING X-Axis
    idc.set_cmt(0x7115B4, "[UI] NOTHING X-Axis", 0)
    idc.set_name(0x7115B4, "ui_7115B4", idaapi.SN_NOWARN)
    # 7115EE: mpneeded magic WORD X-Axis
    idc.set_cmt(0x7115EE, "[UI] mpneeded magic WORD X-Axis", 0)
    idc.set_name(0x7115EE, "ui_7115EE", idaapi.SN_NOWARN)
    # 711629: MP Needed Number Y-Axis
    idc.set_cmt(0x711629, "[UI] MP Needed Number Y-Axis", 0)
    idc.set_name(0x711629, "ui_711629", idaapi.SN_NOWARN)
    # 711637: MP Needed Magic Number X-Axis
    idc.set_cmt(0x711637, "[UI] MP Needed Magic Number X-Axis", 0)
    idc.set_name(0x711637, "ui_711637", idaapi.SN_NOWARN)
    # 711648: magic box scroll bar row count height
    idc.set_cmt(0x711648, "[UI] magic box scroll bar row count height", 0)
    idc.set_name(0x711648, "ui_711648", idaapi.SN_NOWARN)
    # 711668: magic menu - magic box scroll bar X-Axis
    idc.set_cmt(0x711668, "[UI] magic menu - magic box scroll bar X-Axis", 0)
    idc.set_name(0x711668, "ui_711668", idaapi.SN_NOWARN)
    # 711676: magic box scroll bar Y-Axis - not optimal but cann
    idc.set_cmt(0x711676, "[UI] magic box scroll bar Y-Axis - not optimal but cannot adjust height so this makes symmetrical", 0)
    idc.set_name(0x711676, "ui_711676", idaapi.SN_NOWARN)
    # 711684: magic menu - magic box scroll bar width
    idc.set_cmt(0x711684, "[UI] magic menu - magic box scroll bar width", 0)
    idc.set_name(0x711684, "ui_711684", idaapi.SN_NOWARN)
    # 7116DF: magic box scroll bottom border row number
    idc.set_cmt(0x7116DF, "[UI] magic box scroll bottom border row number", 0)
    idc.set_name(0x7116DF, "ui_7116DF", idaapi.SN_NOWARN)
    # 7116E8: magic box row count Y-Axis
    idc.set_cmt(0x7116E8, "[UI] magic box row count Y-Axis", 0)
    idc.set_name(0x7116E8, "ui_7116E8", idaapi.SN_NOWARN)
    # 7117D7: magic box text spacing Y-Axis
    idc.set_cmt(0x7117D7, "[UI] magic box text spacing Y-Axis", 0)
    idc.set_name(0x7117D7, "ui_7117D7", idaapi.SN_NOWARN)
    # 7117ED: magic menu - magic box text spacing X-Axis
    idc.set_cmt(0x7117ED, "[UI] magic menu - magic box text spacing X-Axis", 0)
    idc.set_name(0x7117ED, "ui_7117ED", idaapi.SN_NOWARN)
    # 71183C: summon box cursor spacing Y-Axis
    idc.set_cmt(0x71183C, "[UI] summon box cursor spacing Y-Axis", 0)
    idc.set_name(0x71183C, "ui_71183C", idaapi.SN_NOWARN)
    # 711840: summon box cursor Y-Axis
    idc.set_cmt(0x711840, "[UI] summon box cursor Y-Axis", 0)
    idc.set_name(0x711840, "ui_711840", idaapi.SN_NOWARN)
    # 7118EB: Summon Added Ability Y-Axis
    idc.set_cmt(0x7118EB, "[UI] Summon Added Ability Y-Axis", 0)
    idc.set_name(0x7118EB, "ui_7118EB", idaapi.SN_NOWARN)
    # 711A1A: Summon Quadra/Turbo Y-Axis
    idc.set_cmt(0x711A1A, "[UI] Summon Quadra/Turbo Y-Axis", 0)
    idc.set_name(0x711A1A, "ui_711A1A", idaapi.SN_NOWARN)
    # 711A37: Summon Quadra/Turbo X-Axis
    idc.set_cmt(0x711A37, "[UI] Summon Quadra/Turbo X-Axis", 0)
    idc.set_name(0x711A37, "ui_711A37", idaapi.SN_NOWARN)
    # 711B32: Summon Quadra Magic Number Y-Axis
    idc.set_cmt(0x711B32, "[UI] Summon Quadra Magic Number Y-Axis", 0)
    idc.set_name(0x711B32, "ui_711B32", idaapi.SN_NOWARN)
    # 711B84: Summon Quadra Magic X Y-Axis
    idc.set_cmt(0x711B84, "[UI] Summon Quadra Magic X Y-Axis", 0)
    idc.set_name(0x711B84, "ui_711B84", idaapi.SN_NOWARN)
    # 711BE7: Summon Turbo MP number Y-Axis
    idc.set_cmt(0x711BE7, "[UI] Summon Turbo MP number Y-Axis", 0)
    idc.set_name(0x711BE7, "ui_711BE7", idaapi.SN_NOWARN)
    # 711C04: Summon Turbo MP number X-Axis
    idc.set_cmt(0x711C04, "[UI] Summon Turbo MP number X-Axis", 0)
    idc.set_name(0x711C04, "ui_711C04", idaapi.SN_NOWARN)
    # 711C3D: Summon - Added Ability NOTHING Y-Axis
    idc.set_cmt(0x711C3D, "[UI] Summon - Added Ability NOTHING Y-Axis", 0)
    idc.set_name(0x711C3D, "ui_711C3D", idaapi.SN_NOWARN)
    # 711C83: summon mpneeded WORD X-Axis
    idc.set_cmt(0x711C83, "[UI] summon mpneeded WORD X-Axis", 0)
    idc.set_name(0x711C83, "ui_711C83", idaapi.SN_NOWARN)
    # 711CCF: SUMMON MP NEEDED NUMBER X-AXIS
    idc.set_cmt(0x711CCF, "[UI] SUMMON MP NEEDED NUMBER X-AXIS", 0)
    idc.set_name(0x711CCF, "ui_711CCF", idaapi.SN_NOWARN)
    # 711CE9: summon box scroll bar scaling height
    idc.set_cmt(0x711CE9, "[UI] summon box scroll bar scaling height", 0)
    idc.set_name(0x711CE9, "ui_711CE9", idaapi.SN_NOWARN)
    # 711D00: magic menu - summon box scroll bar X-Axis
    idc.set_cmt(0x711D00, "[UI] magic menu - summon box scroll bar X-Axis", 0)
    idc.set_name(0x711D00, "ui_711D00", idaapi.SN_NOWARN)
    # 711D0E: summon box scroll bar Y-Axis
    idc.set_cmt(0x711D0E, "[UI] summon box scroll bar Y-Axis", 0)
    idc.set_name(0x711D0E, "ui_711D0E", idaapi.SN_NOWARN)
    # 711D1C: magic menu - summon box scroll bar width
    idc.set_cmt(0x711D1C, "[UI] magic menu - summon box scroll bar width", 0)
    idc.set_name(0x711D1C, "ui_711D1C", idaapi.SN_NOWARN)
    # 711D80: summon box row count Y-Axis
    idc.set_cmt(0x711D80, "[UI] summon box row count Y-Axis", 0)
    idc.set_name(0x711D80, "ui_711D80", idaapi.SN_NOWARN)
    # 711E1D: summon box text spacing Y-Axis
    idc.set_cmt(0x711E1D, "[UI] summon box text spacing Y-Axis", 0)
    idc.set_name(0x711E1D, "ui_711E1D", idaapi.SN_NOWARN)
    # 711E86: eskill box cursor spacing Y-Axis
    idc.set_cmt(0x711E86, "[UI] eskill box cursor spacing Y-Axis", 0)
    idc.set_name(0x711E86, "ui_711E86", idaapi.SN_NOWARN)
    # 711E8A: eskill box cursor Y-Axis
    idc.set_cmt(0x711E8A, "[UI] eskill box cursor Y-Axis", 0)
    idc.set_name(0x711E8A, "ui_711E8A", idaapi.SN_NOWARN)
    # 711F35: Enemy Skill added ability Y-Axis
    idc.set_cmt(0x711F35, "[UI] Enemy Skill added ability Y-Axis", 0)
    idc.set_name(0x711F35, "ui_711F35", idaapi.SN_NOWARN)
    # 711F41: Enemy Skill added ability X-Axis
    idc.set_cmt(0x711F41, "[UI] Enemy Skill added ability X-Axis", 0)
    idc.set_name(0x711F41, "ui_711F41", idaapi.SN_NOWARN)
    # 711F79: Enemy Skill NOTHING Y-Axis
    idc.set_cmt(0x711F79, "[UI] Enemy Skill NOTHING Y-Axis", 0)
    idc.set_name(0x711F79, "ui_711F79", idaapi.SN_NOWARN)
    # 711F86: Enemy Skill NOTHING X-Axis
    idc.set_cmt(0x711F86, "[UI] Enemy Skill NOTHING X-Axis", 0)
    idc.set_name(0x711F86, "ui_711F86", idaapi.SN_NOWARN)
    # 711FBF: eskill mpneeded WORD X-Axis
    idc.set_cmt(0x711FBF, "[UI] eskill mpneeded WORD X-Axis", 0)
    idc.set_name(0x711FBF, "ui_711FBF", idaapi.SN_NOWARN)
    # 711FFD: Enemy Skill MP Needed Number Y-Axis
    idc.set_cmt(0x711FFD, "[UI] Enemy Skill MP Needed Number Y-Axis", 0)
    idc.set_name(0x711FFD, "ui_711FFD", idaapi.SN_NOWARN)
    # 71200A: Enemy Skill MP Needed Number X-Axis
    idc.set_cmt(0x71200A, "[UI] Enemy Skill MP Needed Number X-Axis", 0)
    idc.set_name(0x71200A, "ui_71200A", idaapi.SN_NOWARN)
    # 71201B: eskill box scroll bar row count height
    idc.set_cmt(0x71201B, "[UI] eskill box scroll bar row count height", 0)
    idc.set_name(0x71201B, "ui_71201B", idaapi.SN_NOWARN)
    # 71203B: magic menu - eskill box scroll bar X-Axis
    idc.set_cmt(0x71203B, "[UI] magic menu - eskill box scroll bar X-Axis", 0)
    idc.set_name(0x71203B, "ui_71203B", idaapi.SN_NOWARN)
    # 712048: eskill box scroll bar Y-Axis
    idc.set_cmt(0x712048, "[UI] eskill box scroll bar Y-Axis", 0)
    idc.set_name(0x712048, "ui_712048", idaapi.SN_NOWARN)
    # 712057: magic menu - eskill box scroll bar width
    idc.set_cmt(0x712057, "[UI] magic menu - eskill box scroll bar width", 0)
    idc.set_name(0x712057, "ui_712057", idaapi.SN_NOWARN)
    # 7120B1: eskill box scroll bottom border row number
    idc.set_cmt(0x7120B1, "[UI] eskill box scroll bottom border row number", 0)
    idc.set_name(0x7120B1, "ui_7120B1", idaapi.SN_NOWARN)
    # 7120BA: eskill box row count Y-Axis
    idc.set_cmt(0x7120BA, "[UI] eskill box row count Y-Axis", 0)
    idc.set_name(0x7120BA, "ui_7120BA", idaapi.SN_NOWARN)
    # 712157: eskill box text spacing Y-Axis = 18
    idc.set_cmt(0x712157, "[UI] eskill box text spacing Y-Axis = 18", 0)
    idc.set_name(0x712157, "ui_712157", idaapi.SN_NOWARN)
    # 714F40: Use Item Cursor Row Count Y-Axis (refresh menu)
    idc.set_cmt(0x714F40, "[UI] Use Item Cursor Row Count Y-Axis (refresh menu)", 0)
    idc.set_name(0x714F40, "ui_714F40", idaapi.SN_NOWARN)
    # 7151E7: Use Ghost Cursor Spacing Y-Axis
    idc.set_cmt(0x7151E7, "[UI] Use Ghost Cursor Spacing Y-Axis", 0)
    idc.set_name(0x7151E7, "ui_7151E7", idaapi.SN_NOWARN)
    # 7151EA: Use Ghost Cursor Y-Axis
    idc.set_cmt(0x7151EA, "[UI] Use Ghost Cursor Y-Axis", 0)
    idc.set_name(0x7151EA, "ui_7151EA", idaapi.SN_NOWARN)
    # 7151ED: Use Ghost Cursor X-Axis
    idc.set_cmt(0x7151ED, "[UI] Use Ghost Cursor X-Axis", 0)
    idc.set_name(0x7151ED, "ui_7151ED", idaapi.SN_NOWARN)
    # 715240: Top Cursor Y-Axis
    idc.set_cmt(0x715240, "[UI] Top Cursor Y-Axis", 0)
    idc.set_name(0x715240, "ui_715240", idaapi.SN_NOWARN)
    # 71524C: Top Cursor X-Axis
    idc.set_cmt(0x71524C, "[UI] Top Cursor X-Axis", 0)
    idc.set_name(0x71524C, "ui_71524C", idaapi.SN_NOWARN)
    # 71526B: Top Cursor Ghost USE Y-Axis
    idc.set_cmt(0x71526B, "[UI] Top Cursor Ghost USE Y-Axis", 0)
    idc.set_name(0x71526B, "ui_71526B", idaapi.SN_NOWARN)
    # 715277: Top Cursor Ghost USE X-Axis
    idc.set_cmt(0x715277, "[UI] Top Cursor Ghost USE X-Axis", 0)
    idc.set_name(0x715277, "ui_715277", idaapi.SN_NOWARN)
    # 71528E: Use Cursor Spacing Y-Axis
    idc.set_cmt(0x71528E, "[UI] Use Cursor Spacing Y-Axis", 0)
    idc.set_name(0x71528E, "ui_71528E", idaapi.SN_NOWARN)
    # 715291: Use Cursor Y-Axis
    idc.set_cmt(0x715291, "[UI] Use Cursor Y-Axis", 0)
    idc.set_name(0x715291, "ui_715291", idaapi.SN_NOWARN)
    # 715294: Use Cursor X-Axis
    idc.set_cmt(0x715294, "[UI] Use Cursor X-Axis", 0)
    idc.set_name(0x715294, "ui_715294", idaapi.SN_NOWARN)
    # 7152EC: Item Menu - Use Item Description Position Y-axis
    idc.set_cmt(0x7152EC, "[UI] Item Menu - Use Item Description Position Y-axis", 0)
    idc.set_name(0x7152EC, "ui_7152EC", idaapi.SN_NOWARN)
    # 715309: Item Menu - Use Character Select Top Ghost Cursor 
    idc.set_cmt(0x715309, "[UI] Item Menu - Use Character Select Top Ghost Cursor Y-Axis", 0)
    idc.set_name(0x715309, "ui_715309", idaapi.SN_NOWARN)
    # 715314: Item Menu - Use Character Select Top Ghost Cursor 
    idc.set_cmt(0x715314, "[UI] Item Menu - Use Character Select Top Ghost Cursor X-Axis", 0)
    idc.set_name(0x715314, "ui_715314", idaapi.SN_NOWARN)
    # 71536A: Item Menu - Use Item Character Select Description 
    idc.set_cmt(0x71536A, "[UI] Item Menu - Use Item Character Select Description Position Y-axis", 0)
    idc.set_name(0x71536A, "ui_71536A", idaapi.SN_NOWARN)
    # 71538A: Top Cursor Ghost KEY ITEMS Y-Axis
    idc.set_cmt(0x71538A, "[UI] Top Cursor Ghost KEY ITEMS Y-Axis", 0)
    idc.set_name(0x71538A, "ui_71538A", idaapi.SN_NOWARN)
    # 715396: Top Cursor Ghost KEY ITEMS X-Axis
    idc.set_cmt(0x715396, "[UI] Top Cursor Ghost KEY ITEMS X-Axis", 0)
    idc.set_name(0x715396, "ui_715396", idaapi.SN_NOWARN)
    # 7153AD: Key Items Cursor Spacing Y-Axis
    idc.set_cmt(0x7153AD, "[UI] Key Items Cursor Spacing Y-Axis", 0)
    idc.set_name(0x7153AD, "ui_7153AD", idaapi.SN_NOWARN)
    # 7153B0: Key Items Cursor Y-Axis
    idc.set_cmt(0x7153B0, "[UI] Key Items Cursor Y-Axis", 0)
    idc.set_name(0x7153B0, "ui_7153B0", idaapi.SN_NOWARN)
    # 7153C2: Key Items Cursor X-Axis
    idc.set_cmt(0x7153C2, "[UI] Key Items Cursor X-Axis", 0)
    idc.set_name(0x7153C2, "ui_7153C2", idaapi.SN_NOWARN)
    # 71541B: Item Menu - Key Item Description Position Y-axis
    idc.set_cmt(0x71541B, "[UI] Item Menu - Key Item Description Position Y-axis", 0)
    idc.set_name(0x71541B, "ui_71541B", idaapi.SN_NOWARN)
    # 71543B: Top Cursor Ghost ARRANGE Y-Axis
    idc.set_cmt(0x71543B, "[UI] Top Cursor Ghost ARRANGE Y-Axis", 0)
    idc.set_name(0x71543B, "ui_71543B", idaapi.SN_NOWARN)
    # 715447: Top Cursor Ghost ARRANGE X-Axis
    idc.set_cmt(0x715447, "[UI] Top Cursor Ghost ARRANGE X-Axis", 0)
    idc.set_name(0x715447, "ui_715447", idaapi.SN_NOWARN)
    # 71546B: arrange menu cursor Y-Axis
    idc.set_cmt(0x71546B, "[UI] arrange menu cursor Y-Axis", 0)
    idc.set_name(0x71546B, "ui_71546B", idaapi.SN_NOWARN)
    # 715479: arrange menu cursor X-Axis
    idc.set_cmt(0x715479, "[UI] arrange menu cursor X-Axis", 0)
    idc.set_name(0x715479, "ui_715479", idaapi.SN_NOWARN)
    # 7154C1: ARRANGE Text Spacing Y-Axis
    idc.set_cmt(0x7154C1, "[UI] ARRANGE Text Spacing Y-Axis", 0)
    idc.set_name(0x7154C1, "ui_7154C1", idaapi.SN_NOWARN)
    # 7154C5: ARRANGE Text Position Y-Axis
    idc.set_cmt(0x7154C5, "[UI] ARRANGE Text Position Y-Axis", 0)
    idc.set_name(0x7154C5, "ui_7154C5", idaapi.SN_NOWARN)
    # 7154D2: ARRANGE Text Position X-Axis
    idc.set_cmt(0x7154D2, "[UI] ARRANGE Text Position X-Axis", 0)
    idc.set_name(0x7154D2, "ui_7154D2", idaapi.SN_NOWARN)
    # 715504: Arrange Custom Top Ghost Cursor Y-Axis
    idc.set_cmt(0x715504, "[UI] Arrange Custom Top Ghost Cursor Y-Axis", 0)
    idc.set_name(0x715504, "ui_715504", idaapi.SN_NOWARN)
    # 715566: Item Menu - Arrange Item Description Position Y-ax
    idc.set_cmt(0x715566, "[UI] Item Menu - Arrange Item Description Position Y-axis", 0)
    idc.set_name(0x715566, "ui_715566", idaapi.SN_NOWARN)
    # 7155D9: Avatar position Y-axis
    idc.set_cmt(0x7155D9, "[UI] Avatar position Y-axis", 0)
    idc.set_name(0x7155D9, "ui_7155D9", idaapi.SN_NOWARN)
    # 7155DC: Avatar position X-axis
    idc.set_cmt(0x7155DC, "[UI] Avatar position X-axis", 0)
    idc.set_name(0x7155DC, "ui_7155DC", idaapi.SN_NOWARN)
    # 7155E8: Avatar box height
    idc.set_cmt(0x7155E8, "[UI] Avatar box height", 0)
    idc.set_name(0x7155E8, "ui_7155E8", idaapi.SN_NOWARN)
    # 7155ED: Avatar box width
    idc.set_cmt(0x7155ED, "[UI] Avatar box width", 0)
    idc.set_name(0x7155ED, "ui_7155ED", idaapi.SN_NOWARN)
    # 7155F2: Avatar box Y-axis
    idc.set_cmt(0x7155F2, "[UI] Avatar box Y-axis", 0)
    idc.set_name(0x7155F2, "ui_7155F2", idaapi.SN_NOWARN)
    # 71563F: Top menu position Y-axis
    idc.set_cmt(0x71563F, "[UI] Top menu position Y-axis", 0)
    idc.set_name(0x71563F, "ui_71563F", idaapi.SN_NOWARN)
    # 715645: Top menu spacing X-axis
    idc.set_cmt(0x715645, "[UI] Top menu spacing X-axis", 0)
    idc.set_name(0x715645, "ui_715645", idaapi.SN_NOWARN)
    # 715648: Top menu position  X-axis
    idc.set_cmt(0x715648, "[UI] Top menu position  X-axis", 0)
    idc.set_name(0x715648, "ui_715648", idaapi.SN_NOWARN)
    # 71569F: Arrange Ghost Cursor Spacing Y-Axis
    idc.set_cmt(0x71569F, "[UI] Arrange Ghost Cursor Spacing Y-Axis", 0)
    idc.set_name(0x71569F, "ui_71569F", idaapi.SN_NOWARN)
    # 7156D0: Arrange Ghost Cursor Y-Axis
    idc.set_cmt(0x7156D0, "[UI] Arrange Ghost Cursor Y-Axis", 0)
    idc.set_name(0x7156D0, "ui_7156D0", idaapi.SN_NOWARN)
    # 7156D3: Arrange Ghost Cursor X-Axis
    idc.set_cmt(0x7156D3, "[UI] Arrange Ghost Cursor X-Axis", 0)
    idc.set_name(0x7156D3, "ui_7156D3", idaapi.SN_NOWARN)
    # 7156EC: Arrange Cursor Spacing Y-Axis
    idc.set_cmt(0x7156EC, "[UI] Arrange Cursor Spacing Y-Axis", 0)
    idc.set_name(0x7156EC, "ui_7156EC", idaapi.SN_NOWARN)
    # 7156EF: Arrange Cursor Y-Axis
    idc.set_cmt(0x7156EF, "[UI] Arrange Cursor Y-Axis", 0)
    idc.set_name(0x7156EF, "ui_7156EF", idaapi.SN_NOWARN)
    # 7156F2: Arrange Cursor X-Axis
    idc.set_cmt(0x7156F2, "[UI] Arrange Cursor X-Axis", 0)
    idc.set_name(0x7156F2, "ui_7156F2", idaapi.SN_NOWARN)
    # 715715: Scroll Bar Row Count Height
    idc.set_cmt(0x715715, "[UI] Scroll Bar Row Count Height", 0)
    idc.set_name(0x715715, "ui_715715", idaapi.SN_NOWARN)
    # 71573A: Item Menu - Scroll Bar X-Axis
    idc.set_cmt(0x71573A, "[UI] Item Menu - Scroll Bar X-Axis", 0)
    idc.set_name(0x71573A, "ui_71573A", idaapi.SN_NOWARN)
    # 71574C: Item Menu - Scroll Bar Width
    idc.set_cmt(0x71574C, "[UI] Item Menu - Scroll Bar Width", 0)
    idc.set_name(0x71574C, "ui_71574C", idaapi.SN_NOWARN)
    # 71577D: Right Box Row Count Y-Axis
    idc.set_cmt(0x71577D, "[UI] Right Box Row Count Y-Axis", 0)
    idc.set_name(0x71577D, "ui_71577D", idaapi.SN_NOWARN)
    # 71582C: Right Box Text Spacing Y-Axis
    idc.set_cmt(0x71582C, "[UI] Right Box Text Spacing Y-Axis", 0)
    idc.set_name(0x71582C, "ui_71582C", idaapi.SN_NOWARN)
    # 71583F: Right Box Text Y-Axis
    idc.set_cmt(0x71583F, "[UI] Right Box Text Y-Axis", 0)
    idc.set_name(0x71583F, "ui_71583F", idaapi.SN_NOWARN)
    # 7158F6: Right Box Icons Spacing Y-Axis
    idc.set_cmt(0x7158F6, "[UI] Right Box Icons Spacing Y-Axis", 0)
    idc.set_name(0x7158F6, "ui_7158F6", idaapi.SN_NOWARN)
    # 715909: Right Box Icons Y-Axis
    idc.set_cmt(0x715909, "[UI] Right Box Icons Y-Axis", 0)
    idc.set_name(0x715909, "ui_715909", idaapi.SN_NOWARN)
    # 71590D: OG icons item menu
    idc.set_cmt(0x71590D, "[UI] OG icons item menu", 0)
    idc.set_name(0x71590D, "ui_71590D", idaapi.SN_NOWARN)
    # 71592B: Right Box Colon Spacing Y-Axis
    idc.set_cmt(0x71592B, "[UI] Right Box Colon Spacing Y-Axis", 0)
    idc.set_name(0x71592B, "ui_71592B", idaapi.SN_NOWARN)
    # 71593E: Right Box Colon Y-Axis
    idc.set_cmt(0x71593E, "[UI] Right Box Colon Y-Axis", 0)
    idc.set_name(0x71593E, "ui_71593E", idaapi.SN_NOWARN)
    # 715961: Right Box Quantity Spacing Y-Axis
    idc.set_cmt(0x715961, "[UI] Right Box Quantity Spacing Y-Axis", 0)
    idc.set_name(0x715961, "ui_715961", idaapi.SN_NOWARN)
    # 715974: Right Box Quantity Y-Axis
    idc.set_cmt(0x715974, "[UI] Right Box Quantity Y-Axis", 0)
    idc.set_name(0x715974, "ui_715974", idaapi.SN_NOWARN)
    # 715994: Key Items Scroll Bar Row Count Height
    idc.set_cmt(0x715994, "[UI] Key Items Scroll Bar Row Count Height", 0)
    idc.set_name(0x715994, "ui_715994", idaapi.SN_NOWARN)
    # 715A6C: Right Box Key Items Spacing Y-Axis
    idc.set_cmt(0x715A6C, "[UI] Right Box Key Items Spacing Y-Axis", 0)
    idc.set_name(0x715A6C, "ui_715A6C", idaapi.SN_NOWARN)
    # 716575: Key Items Cursor Row Count Y-Axis (refresh menu)
    idc.set_cmt(0x716575, "[UI] Key Items Cursor Row Count Y-Axis (refresh menu)", 0)
    idc.set_name(0x716575, "ui_716575", idaapi.SN_NOWARN)
    # 717410: Arrange Custom Cursor Row Count Y-Axis (refresh me
    idc.set_cmt(0x717410, "[UI] Arrange Custom Cursor Row Count Y-Axis (refresh menu)", 0)
    idc.set_name(0x717410, "ui_717410", idaapi.SN_NOWARN)
    # 718FCC: name - menu cursor Y-Axis
    idc.set_cmt(0x718FCC, "[UI] name - menu cursor Y-Axis", 0)
    idc.set_name(0x718FCC, "ui_718FCC", idaapi.SN_NOWARN)
    # 718FD2: name - menu cursor X-Axis
    idc.set_cmt(0x718FD2, "[UI] name - menu cursor X-Axis", 0)
    idc.set_name(0x718FD2, "ui_718FD2", idaapi.SN_NOWARN)
    # 719244: name - menu contents Y-Axis
    idc.set_cmt(0x719244, "[UI] name - menu contents Y-Axis", 0)
    idc.set_name(0x719244, "ui_719244", idaapi.SN_NOWARN)
    # 71924A: name - menu contents X-Axis
    idc.set_cmt(0x71924A, "[UI] name - menu contents X-Axis", 0)
    idc.set_name(0x71924A, "ui_71924A", idaapi.SN_NOWARN)
    # 7193CE: name - Typed letters Palette Color
    idc.set_cmt(0x7193CE, "[UI] name - Typed letters Palette Color", 0)
    idc.set_name(0x7193CE, "ui_7193CE", idaapi.SN_NOWARN)
    # 7193D0: name - Typed letters Y-Axis
    idc.set_cmt(0x7193D0, "[UI] name - Typed letters Y-Axis", 0)
    idc.set_name(0x7193D0, "ui_7193D0", idaapi.SN_NOWARN)
    # 7193FF: Please enter a name Y-Axis
    idc.set_cmt(0x7193FF, "[UI] Please enter a name Y-Axis", 0)
    idc.set_name(0x7193FF, "ui_7193FF", idaapi.SN_NOWARN)
    # 719401: Please enter a name X-Axis
    idc.set_cmt(0x719401, "[UI] Please enter a name X-Axis", 0)
    idc.set_name(0x719401, "ui_719401", idaapi.SN_NOWARN)
    # 71941B: name - Avatar Y-Axis
    idc.set_cmt(0x71941B, "[UI] name - Avatar Y-Axis", 0)
    idc.set_name(0x71941B, "ui_71941B", idaapi.SN_NOWARN)
    # 71941D: name - Avatar X-Axis
    idc.set_cmt(0x71941D, "[UI] name - Avatar X-Axis", 0)
    idc.set_name(0x71941D, "ui_71941D", idaapi.SN_NOWARN)
    # 719EE8: bottom stat box flashing bg X-Axis (should be disa
    idc.set_cmt(0x719EE8, "[UI] bottom stat box flashing bg X-Axis (should be disabled though)", 0)
    idc.set_name(0x719EE8, "ui_719EE8", idaapi.SN_NOWARN)
    # 719EFB: shop - disable bottom stat box flashing bg boxes f
    idc.set_cmt(0x719EFB, "[UI] shop - disable bottom stat box flashing bg boxes for transparent avatars", 0)
    idc.set_name(0x719EFB, "ui_719EFB", idaapi.SN_NOWARN)
    # 719FA4: bottom stat box contents X-Axis
    idc.set_cmt(0x719FA4, "[UI] bottom stat box contents X-Axis", 0)
    idc.set_name(0x719FA4, "ui_719FA4", idaapi.SN_NOWARN)
    # 71A189: bottom stat 'D' X-Axis
    idc.set_cmt(0x71A189, "[UI] bottom stat 'D' X-Axis", 0)
    idc.set_name(0x71A189, "ui_71A189", idaapi.SN_NOWARN)
    # 71A1AB: bottom stat 'A' X-Axis
    idc.set_cmt(0x71A1AB, "[UI] bottom stat 'A' X-Axis", 0)
    idc.set_name(0x71A1AB, "ui_71A1AB", idaapi.SN_NOWARN)
    # 71A734: sell item - cursor row count (shop refresh)
    idc.set_cmt(0x71A734, "[UI] sell item - cursor row count (shop refresh)", 0)
    idc.set_name(0x71A734, "ui_71A734", idaapi.SN_NOWARN)
    # 71AB6C: all shops - buy/sell/exit sell box cursor spacing 
    idc.set_cmt(0x71AB6C, "[UI] all shops - buy/sell/exit sell box cursor spacing X-Axis", 0)
    idc.set_name(0x71AB6C, "ui_71AB6C", idaapi.SN_NOWARN)
    # 71AB70: all shops - buy/sell/exit sell box cursor X-Axis
    idc.set_cmt(0x71AB70, "[UI] all shops - buy/sell/exit sell box cursor X-Axis", 0)
    idc.set_name(0x71AB70, "ui_71AB70", idaapi.SN_NOWARN)
    # 71AB9F: all shops - buy/sell/exit sell box item/materia co
    idc.set_cmt(0x71AB9F, "[UI] all shops - buy/sell/exit sell box item/materia contents X-Axis", 0)
    idc.set_name(0x71AB9F, "ui_71AB9F", idaapi.SN_NOWARN)
    # 71ABEB: all shops - buy/sell/exit sell box ghost cursor sp
    idc.set_cmt(0x71ABEB, "[UI] all shops - buy/sell/exit sell box ghost cursor spacing X-Axis", 0)
    idc.set_name(0x71ABEB, "ui_71ABEB", idaapi.SN_NOWARN)
    # 71ABEF: all shops - buy/sell/exit sell box ghost cursor X-
    idc.set_cmt(0x71ABEF, "[UI] all shops - buy/sell/exit sell box ghost cursor X-Axis", 0)
    idc.set_name(0x71ABEF, "ui_71ABEF", idaapi.SN_NOWARN)
    # 71AC1E: buy/sell/exit X-Axis (when selecting Sell)
    idc.set_cmt(0x71AC1E, "[UI] buy/sell/exit X-Axis (when selecting Sell)", 0)
    idc.set_name(0x71AC1E, "ui_71AC1E", idaapi.SN_NOWARN)
    # 71ACC6: all shops - buy/sell/exit cursor spacing X-Axis
    idc.set_cmt(0x71ACC6, "[UI] all shops - buy/sell/exit cursor spacing X-Axis", 0)
    idc.set_name(0x71ACC6, "ui_71ACC6", idaapi.SN_NOWARN)
    # 71ACCA: all shops - buy/sell/exit cursor X-Axis
    idc.set_cmt(0x71ACCA, "[UI] all shops - buy/sell/exit cursor X-Axis", 0)
    idc.set_name(0x71ACCA, "ui_71ACCA", idaapi.SN_NOWARN)
    # 71ACFA: buy/sell/exit X-Axis
    idc.set_cmt(0x71ACFA, "[UI] buy/sell/exit X-Axis", 0)
    idc.set_name(0x71ACFA, "ui_71ACFA", idaapi.SN_NOWARN)
    # 71AD72: sell materia - right box cursor spacing Y-Axis
    idc.set_cmt(0x71AD72, "[UI] sell materia - right box cursor spacing Y-Axis", 0)
    idc.set_name(0x71AD72, "ui_71AD72", idaapi.SN_NOWARN)
    # 71AD75: sell materia - right box cursor Y-Axis
    idc.set_cmt(0x71AD75, "[UI] sell materia - right box cursor Y-Axis", 0)
    idc.set_name(0x71AD75, "ui_71AD75", idaapi.SN_NOWARN)
    # 71AD7B: sell materia - right box cursor X-Axis
    idc.set_cmt(0x71AD7B, "[UI] sell materia - right box cursor X-Axis", 0)
    idc.set_name(0x71AD7B, "ui_71AD7B", idaapi.SN_NOWARN)
    # 71AD9F: sell materia - top box what would you like to sell
    idc.set_cmt(0x71AD9F, "[UI] sell materia - top box what would you like to sell WORD X-Axis", 0)
    idc.set_name(0x71AD9F, "ui_71AD9F", idaapi.SN_NOWARN)
    # 71AE6B: sell materia - right box visible row count
    idc.set_cmt(0x71AE6B, "[UI] sell materia - right box visible row count", 0)
    idc.set_name(0x71AE6B, "ui_71AE6B", idaapi.SN_NOWARN)
    # 71AEC8: sell materia - right box text spacing Y-Axis
    idc.set_cmt(0x71AEC8, "[UI] sell materia - right box text spacing Y-Axis", 0)
    idc.set_name(0x71AEC8, "ui_71AEC8", idaapi.SN_NOWARN)
    # 71AED3: sell materia - right box text Y-Axis
    idc.set_cmt(0x71AED3, "[UI] sell materia - right box text Y-Axis", 0)
    idc.set_name(0x71AED3, "ui_71AED3", idaapi.SN_NOWARN)
    # 71AEDA: sell materia - right box text X-Axis
    idc.set_cmt(0x71AEDA, "[UI] sell materia - right box text X-Axis", 0)
    idc.set_name(0x71AEDA, "ui_71AEDA", idaapi.SN_NOWARN)
    # 71AEEF: sell materia - right box scroll row height
    idc.set_cmt(0x71AEEF, "[UI] sell materia - right box scroll row height", 0)
    idc.set_name(0x71AEEF, "ui_71AEEF", idaapi.SN_NOWARN)
    # 71AF0F: sell materia - scroll bar X-axis
    idc.set_cmt(0x71AF0F, "[UI] sell materia - scroll bar X-axis", 0)
    idc.set_name(0x71AF0F, "ui_71AF0F", idaapi.SN_NOWARN)
    # 71AF18: sell materia - scroll bar Y-Axis
    idc.set_cmt(0x71AF18, "[UI] sell materia - scroll bar Y-Axis", 0)
    idc.set_name(0x71AF18, "ui_71AF18", idaapi.SN_NOWARN)
    # 71AF21: sell materia - scroll bar width
    idc.set_cmt(0x71AF21, "[UI] sell materia - scroll bar width", 0)
    idc.set_name(0x71AF21, "ui_71AF21", idaapi.SN_NOWARN)
    # 71AFA9: sell materia - right box icons spacing Y-Axis
    idc.set_cmt(0x71AFA9, "[UI] sell materia - right box icons spacing Y-Axis", 0)
    idc.set_name(0x71AFA9, "ui_71AFA9", idaapi.SN_NOWARN)
    # 71AFB6: sell materia - right box icons Y-Axis
    idc.set_cmt(0x71AFB6, "[UI] sell materia - right box icons Y-Axis", 0)
    idc.set_name(0x71AFB6, "ui_71AFB6", idaapi.SN_NOWARN)
    # 71AFBC: sell materia - right box icons X-Axis
    idc.set_cmt(0x71AFBC, "[UI] sell materia - right box icons X-Axis", 0)
    idc.set_name(0x71AFBC, "ui_71AFBC", idaapi.SN_NOWARN)
    # 71B006: sell materia - top box remaining Y-Axis
    idc.set_cmt(0x71B006, "[UI] sell materia - top box remaining Y-Axis", 0)
    idc.set_name(0x71B006, "ui_71B006", idaapi.SN_NOWARN)
    # 71B04F: sell materia - top box price for master X-Axis
    idc.set_cmt(0x71B04F, "[UI] sell materia - top box price for master X-Axis", 0)
    idc.set_name(0x71B04F, "ui_71B04F", idaapi.SN_NOWARN)
    # 71B08C: sell materia - top box price through AP X-Axis
    idc.set_cmt(0x71B08C, "[UI] sell materia - top box price through AP X-Axis", 0)
    idc.set_name(0x71B08C, "ui_71B08C", idaapi.SN_NOWARN)
    # 71B131: sell materia - top box gil WORD X-Axis
    idc.set_cmt(0x71B131, "[UI] sell materia - top box gil WORD X-Axis", 0)
    idc.set_name(0x71B131, "ui_71B131", idaapi.SN_NOWARN)
    # 71B194: sell materia - top box remaining WORD Y-Axis
    idc.set_cmt(0x71B194, "[UI] sell materia - top box remaining WORD Y-Axis", 0)
    idc.set_name(0x71B194, "ui_71B194", idaapi.SN_NOWARN)
    # 71B1A2: sell materia - top box remaining WORD X-Axis
    idc.set_cmt(0x71B1A2, "[UI] sell materia - top box remaining WORD X-Axis", 0)
    idc.set_name(0x71B1A2, "ui_71B1A2", idaapi.SN_NOWARN)
    # 71B279: all shop - selected item boxes spacing Y-Axis
    idc.set_cmt(0x71B279, "[UI] all shop - selected item boxes spacing Y-Axis", 0)
    idc.set_name(0x71B279, "ui_71B279", idaapi.SN_NOWARN)
    # 71B2E8: inv box quantity number Y-Axis
    idc.set_cmt(0x71B2E8, "[UI] inv box quantity number Y-Axis", 0)
    idc.set_name(0x71B2E8, "ui_71B2E8", idaapi.SN_NOWARN)
    # 71B2F6: inv box quantity number X-Axis
    idc.set_cmt(0x71B2F6, "[UI] inv box quantity number X-Axis", 0)
    idc.set_name(0x71B2F6, "ui_71B2F6", idaapi.SN_NOWARN)
    # 71B32A: inv box total number Y-Axis
    idc.set_cmt(0x71B32A, "[UI] inv box total number Y-Axis", 0)
    idc.set_name(0x71B32A, "ui_71B32A", idaapi.SN_NOWARN)
    # 71B338: inv box total number X-Axis
    idc.set_cmt(0x71B338, "[UI] inv box total number X-Axis", 0)
    idc.set_name(0x71B338, "ui_71B338", idaapi.SN_NOWARN)
    # 71B364: inv box How many WORD X-Axis
    idc.set_cmt(0x71B364, "[UI] inv box How many WORD X-Axis", 0)
    idc.set_name(0x71B364, "ui_71B364", idaapi.SN_NOWARN)
    # 71B391: inv box Total WORD X-Axis
    idc.set_cmt(0x71B391, "[UI] inv box Total WORD X-Axis", 0)
    idc.set_name(0x71B391, "ui_71B391", idaapi.SN_NOWARN)
    # 71B479: Weapon slot/growth Slots Y-Axis
    idc.set_cmt(0x71B479, "[UI] Weapon slot/growth Slots Y-Axis", 0)
    idc.set_name(0x71B479, "ui_71B479", idaapi.SN_NOWARN)
    # 71B4BF: Armor slot/growth Slots Y-Axis
    idc.set_cmt(0x71B4BF, "[UI] Armor slot/growth Slots Y-Axis", 0)
    idc.set_name(0x71B4BF, "ui_71B4BF", idaapi.SN_NOWARN)
    # 71B52A: Armor slot/growth growth value X-Axis
    idc.set_cmt(0x71B52A, "[UI] Armor slot/growth growth value X-Axis", 0)
    idc.set_name(0x71B52A, "ui_71B52A", idaapi.SN_NOWARN)
    # 71B5F0: all shop buy - right box gil amount Y-Axis
    idc.set_cmt(0x71B5F0, "[UI] all shop buy - right box gil amount Y-Axis", 0)
    idc.set_name(0x71B5F0, "ui_71B5F0", idaapi.SN_NOWARN)
    # 71B5FD: all shop buy- right box gil amount X-Axis
    idc.set_cmt(0x71B5FD, "[UI] all shop buy- right box gil amount X-Axis", 0)
    idc.set_name(0x71B5FD, "ui_71B5FD", idaapi.SN_NOWARN)
    # 71B61F: all shop buy - right box owned Y-Axis
    idc.set_cmt(0x71B61F, "[UI] all shop buy - right box owned Y-Axis", 0)
    idc.set_name(0x71B61F, "ui_71B61F", idaapi.SN_NOWARN)
    # 71B62D: all shop buy - right box owned X-Axis
    idc.set_cmt(0x71B62D, "[UI] all shop buy - right box owned X-Axis", 0)
    idc.set_name(0x71B62D, "ui_71B62D", idaapi.SN_NOWARN)
    # 71B64F: all shop buy - right box equipped Y-Axis
    idc.set_cmt(0x71B64F, "[UI] all shop buy - right box equipped Y-Axis", 0)
    idc.set_name(0x71B64F, "ui_71B64F", idaapi.SN_NOWARN)
    # 71B660: all shop buy - right box equipped X-Axis
    idc.set_cmt(0x71B660, "[UI] all shop buy - right box equipped X-Axis", 0)
    idc.set_name(0x71B660, "ui_71B660", idaapi.SN_NOWARN)
    # 71B681: all shop buy - right box gil WORD Y-Axis
    idc.set_cmt(0x71B681, "[UI] all shop buy - right box gil WORD Y-Axis", 0)
    idc.set_name(0x71B681, "ui_71B681", idaapi.SN_NOWARN)
    # 71B6B1: all shop buy - right box owned WORD Y-Axis
    idc.set_cmt(0x71B6B1, "[UI] all shop buy - right box owned WORD Y-Axis", 0)
    idc.set_name(0x71B6B1, "ui_71B6B1", idaapi.SN_NOWARN)
    # 71B848: weapon shop - spacing Y-Axis
    idc.set_cmt(0x71B848, "[UI] weapon shop - spacing Y-Axis", 0)
    idc.set_name(0x71B848, "ui_71B848", idaapi.SN_NOWARN)
    # 71B84B: all shops - visible area Y-Axis
    idc.set_cmt(0x71B84B, "[UI] all shops - visible area Y-Axis", 0)
    idc.set_name(0x71B84B, "ui_71B84B", idaapi.SN_NOWARN)
    # 71B8B1: Enable weapon/item shop Y-Axis Alignment
    idc.set_cmt(0x71B8B1, "[UI] Enable weapon/item shop Y-Axis Alignment", 0)
    idc.set_name(0x71B8B1, "ui_71B8B1", idaapi.SN_NOWARN)
    # 71B8B7: weapon/item shop - text X-Axis
    idc.set_cmt(0x71B8B7, "[UI] weapon/item shop - text X-Axis", 0)
    idc.set_name(0x71B8B7, "ui_71B8B7", idaapi.SN_NOWARN)
    # 71B8D0: weapon/item shop - icons Y-Axis
    idc.set_cmt(0x71B8D0, "[UI] weapon/item shop - icons Y-Axis", 0)
    idc.set_name(0x71B8D0, "ui_71B8D0", idaapi.SN_NOWARN)
    # 71B8D3: weapon/item shop - icon X-Axis
    idc.set_cmt(0x71B8D3, "[UI] weapon/item shop - icon X-Axis", 0)
    idc.set_name(0x71B8D3, "ui_71B8D3", idaapi.SN_NOWARN)
    # 71B927: Enable materia shop Y-Axis Alignment
    idc.set_cmt(0x71B927, "[UI] Enable materia shop Y-Axis Alignment", 0)
    idc.set_name(0x71B927, "ui_71B927", idaapi.SN_NOWARN)
    # 71B92D: materia shop - text X-Axis
    idc.set_cmt(0x71B92D, "[UI] materia shop - text X-Axis", 0)
    idc.set_name(0x71B92D, "ui_71B92D", idaapi.SN_NOWARN)
    # 71B94A: Enable materia shop icon Y-Axis adjustment
    idc.set_cmt(0x71B94A, "[UI] Enable materia shop icon Y-Axis adjustment", 0)
    idc.set_name(0x71B94A, "ui_71B94A", idaapi.SN_NOWARN)
    # 71B95C: buy materia - icon Y-Axis
    idc.set_cmt(0x71B95C, "[UI] buy materia - icon Y-Axis", 0)
    idc.set_name(0x71B95C, "ui_71B95C", idaapi.SN_NOWARN)
    # 71B964: materia shop - icons Y-Axis
    idc.set_cmt(0x71B964, "[UI] materia shop - icons Y-Axis", 0)
    idc.set_name(0x71B964, "ui_71B964", idaapi.SN_NOWARN)
    # 71B967: materia shop - icons X-Axis
    idc.set_cmt(0x71B967, "[UI] materia shop - icons X-Axis", 0)
    idc.set_name(0x71B967, "ui_71B967", idaapi.SN_NOWARN)
    # 71B9FB: weapon shop - scroll row height Y-Axis
    idc.set_cmt(0x71B9FB, "[UI] weapon shop - scroll row height Y-Axis", 0)
    idc.set_name(0x71B9FB, "ui_71B9FB", idaapi.SN_NOWARN)
    # 71BA38: all shop buy - scroll bar X-Axis
    idc.set_cmt(0x71BA38, "[UI] all shop buy - scroll bar X-Axis", 0)
    idc.set_name(0x71BA38, "ui_71BA38", idaapi.SN_NOWARN)
    # 71BA5A: all shop buy - scroll bar width
    idc.set_cmt(0x71BA5A, "[UI] all shop buy - scroll bar width", 0)
    idc.set_name(0x71BA5A, "ui_71BA5A", idaapi.SN_NOWARN)
    # 71BAA6: all shop buy - cursor spacing Y-Axis
    idc.set_cmt(0x71BAA6, "[UI] all shop buy - cursor spacing Y-Axis", 0)
    idc.set_name(0x71BAA6, "ui_71BAA6", idaapi.SN_NOWARN)
    # 71BAAA: all shop buy - cursor Y-Axis
    idc.set_cmt(0x71BAAA, "[UI] all shop buy - cursor Y-Axis", 0)
    idc.set_name(0x71BAAA, "ui_71BAAA", idaapi.SN_NOWARN)
    # 71BAAD: all shop buy - cursor X-Axis
    idc.set_cmt(0x71BAAD, "[UI] all shop buy - cursor X-Axis", 0)
    idc.set_name(0x71BAAD, "ui_71BAAD", idaapi.SN_NOWARN)
    # 71BAD8: all shop buy - ghost cursor spacing Y-Axis
    idc.set_cmt(0x71BAD8, "[UI] all shop buy - ghost cursor spacing Y-Axis", 0)
    idc.set_name(0x71BAD8, "ui_71BAD8", idaapi.SN_NOWARN)
    # 71BADC: all shop buy - ghost cursor Y-Axis
    idc.set_cmt(0x71BADC, "[UI] all shop buy - ghost cursor Y-Axis", 0)
    idc.set_name(0x71BADC, "ui_71BADC", idaapi.SN_NOWARN)
    # 71BADF: all shop buy - ghost cursor X-Axis
    idc.set_cmt(0x71BADF, "[UI] all shop buy - ghost cursor X-Axis", 0)
    idc.set_name(0x71BADF, "ui_71BADF", idaapi.SN_NOWARN)
    # 71BC2B: sell item - sub menu how many WORD Y-Axis
    idc.set_cmt(0x71BC2B, "[UI] sell item - sub menu how many WORD Y-Axis", 0)
    idc.set_name(0x71BC2B, "ui_71BC2B", idaapi.SN_NOWARN)
    # 71BC48: sell item - sub menu total WORD Y-Axis
    idc.set_cmt(0x71BC48, "[UI] sell item - sub menu total WORD Y-Axis", 0)
    idc.set_name(0x71BC48, "ui_71BC48", idaapi.SN_NOWARN)
    # 71BC88: sell item - sub menu gil WORD Y-Axis
    idc.set_cmt(0x71BC88, "[UI] sell item - sub menu gil WORD Y-Axis", 0)
    idc.set_name(0x71BC88, "ui_71BC88", idaapi.SN_NOWARN)
    # 71BC91: sell item - sub menu gil WORD X-Axis
    idc.set_cmt(0x71BC91, "[UI] sell item - sub menu gil WORD X-Axis", 0)
    idc.set_name(0x71BC91, "ui_71BC91", idaapi.SN_NOWARN)
    # 71BCA8: sell item - sub menu owned WORD Y-Axis
    idc.set_cmt(0x71BCA8, "[UI] sell item - sub menu owned WORD Y-Axis", 0)
    idc.set_name(0x71BCA8, "ui_71BCA8", idaapi.SN_NOWARN)
    # 71BCB1: sell item - sub menu owned WORD X-Axis
    idc.set_cmt(0x71BCB1, "[UI] sell item - sub menu owned WORD X-Axis", 0)
    idc.set_name(0x71BCB1, "ui_71BCB1", idaapi.SN_NOWARN)
    # 71BCC8: sell item - sub menu equipped WORD Y-Axis
    idc.set_cmt(0x71BCC8, "[UI] sell item - sub menu equipped WORD Y-Axis", 0)
    idc.set_name(0x71BCC8, "ui_71BCC8", idaapi.SN_NOWARN)
    # 71BCD1: sell item - sub menu equipped WORD X-Axis
    idc.set_cmt(0x71BCD1, "[UI] sell item - sub menu equipped WORD X-Axis", 0)
    idc.set_name(0x71BCD1, "ui_71BCD1", idaapi.SN_NOWARN)
    # 71BD6A: sell item - sub menu remaining Y-Axis
    idc.set_cmt(0x71BD6A, "[UI] sell item - sub menu remaining Y-Axis", 0)
    idc.set_name(0x71BD6A, "ui_71BD6A", idaapi.SN_NOWARN)
    # 71BD90: sell item - sub menu gil Y-Axis
    idc.set_cmt(0x71BD90, "[UI] sell item - sub menu gil Y-Axis", 0)
    idc.set_name(0x71BD90, "ui_71BD90", idaapi.SN_NOWARN)
    # 71BDB4: sell item - sub menu owned Y-Axis
    idc.set_cmt(0x71BDB4, "[UI] sell item - sub menu owned Y-Axis", 0)
    idc.set_name(0x71BDB4, "ui_71BDB4", idaapi.SN_NOWARN)
    # 71BDD7: sell item - sub menu equipped Y-Axis
    idc.set_cmt(0x71BDD7, "[UI] sell item - sub menu equipped Y-Axis", 0)
    idc.set_name(0x71BDD7, "ui_71BDD7", idaapi.SN_NOWARN)
    # 71BE4D: sell item - ghost cursor spacing Y-Axis
    idc.set_cmt(0x71BE4D, "[UI] sell item - ghost cursor spacing Y-Axis", 0)
    idc.set_name(0x71BE4D, "ui_71BE4D", idaapi.SN_NOWARN)
    # 71BE50: sell item - ghost cursor Y-Axis
    idc.set_cmt(0x71BE50, "[UI] sell item - ghost cursor Y-Axis", 0)
    idc.set_name(0x71BE50, "ui_71BE50", idaapi.SN_NOWARN)
    # 71BE59: sell item - ghost cursor spacing X-Axis
    idc.set_cmt(0x71BE59, "[UI] sell item - ghost cursor spacing X-Axis", 0)
    idc.set_name(0x71BE59, "ui_71BE59", idaapi.SN_NOWARN)
    # 71BE5F: sell item - ghost cursor X-Axis
    idc.set_cmt(0x71BE5F, "[UI] sell item - ghost cursor X-Axis", 0)
    idc.set_name(0x71BE5F, "ui_71BE5F", idaapi.SN_NOWARN)
    # 71BE98: sell item - cursor spacing Y-Axis
    idc.set_cmt(0x71BE98, "[UI] sell item - cursor spacing Y-Axis", 0)
    idc.set_name(0x71BE98, "ui_71BE98", idaapi.SN_NOWARN)
    # 71BE9B: sell item - cursor Y-Axis
    idc.set_cmt(0x71BE9B, "[UI] sell item - cursor Y-Axis", 0)
    idc.set_name(0x71BE9B, "ui_71BE9B", idaapi.SN_NOWARN)
    # 71BEA4: sell item - cursor spacing X-Axis
    idc.set_cmt(0x71BEA4, "[UI] sell item - cursor spacing X-Axis", 0)
    idc.set_name(0x71BEA4, "ui_71BEA4", idaapi.SN_NOWARN)
    # 71BEAA: sell item - cursor X-Axis
    idc.set_cmt(0x71BEAA, "[UI] sell item - cursor X-Axis", 0)
    idc.set_name(0x71BEAA, "ui_71BEAA", idaapi.SN_NOWARN)
    # 71BF1E: sell item - scroll row height
    idc.set_cmt(0x71BF1E, "[UI] sell item - scroll row height", 0)
    idc.set_name(0x71BF1E, "ui_71BF1E", idaapi.SN_NOWARN)
    # 71BF3E: sell item scroll bax X-axis
    idc.set_cmt(0x71BF3E, "[UI] sell item scroll bax X-axis", 0)
    idc.set_name(0x71BF3E, "ui_71BF3E", idaapi.SN_NOWARN)
    # 71BF47: sell item - scroll bar Y-Axis
    idc.set_cmt(0x71BF47, "[UI] sell item - scroll bar Y-Axis", 0)
    idc.set_name(0x71BF47, "ui_71BF47", idaapi.SN_NOWARN)
    # 71BF50: sell item scroll bar width
    idc.set_cmt(0x71BF50, "[UI] sell item scroll bar width", 0)
    idc.set_name(0x71BF50, "ui_71BF50", idaapi.SN_NOWARN)
    # 71BF59: sell item - scroll bar height
    idc.set_cmt(0x71BF59, "[UI] sell item - scroll bar height", 0)
    idc.set_name(0x71BF59, "ui_71BF59", idaapi.SN_NOWARN)
    # 71BF91: sell item - visible row count
    idc.set_cmt(0x71BF91, "[UI] sell item - visible row count", 0)
    idc.set_name(0x71BF91, "ui_71BF91", idaapi.SN_NOWARN)
    # 71C05A: sell item - text spacing Y-Axis
    idc.set_cmt(0x71C05A, "[UI] sell item - text spacing Y-Axis", 0)
    idc.set_name(0x71C05A, "ui_71C05A", idaapi.SN_NOWARN)
    # 71C067: sell item - text Y-Axis
    idc.set_cmt(0x71C067, "[UI] sell item - text Y-Axis", 0)
    idc.set_name(0x71C067, "ui_71C067", idaapi.SN_NOWARN)
    # 71C150: sell item - icon spacing Y-Axis
    idc.set_cmt(0x71C150, "[UI] sell item - icon spacing Y-Axis", 0)
    idc.set_name(0x71C150, "ui_71C150", idaapi.SN_NOWARN)
    # 71C15D: sell item - icon Y-Axis
    idc.set_cmt(0x71C15D, "[UI] sell item - icon Y-Axis", 0)
    idc.set_name(0x71C15D, "ui_71C15D", idaapi.SN_NOWARN)
    # 71C187: sell item - colon spacing Y-Axis
    idc.set_cmt(0x71C187, "[UI] sell item - colon spacing Y-Axis", 0)
    idc.set_name(0x71C187, "ui_71C187", idaapi.SN_NOWARN)
    # 71C194: sell item - colon Y-Axis
    idc.set_cmt(0x71C194, "[UI] sell item - colon Y-Axis", 0)
    idc.set_name(0x71C194, "ui_71C194", idaapi.SN_NOWARN)
    # 71C1C4: sell item - number spacing Y-Axis
    idc.set_cmt(0x71C1C4, "[UI] sell item - number spacing Y-Axis", 0)
    idc.set_name(0x71C1C4, "ui_71C1C4", idaapi.SN_NOWARN)
    # 71C1D1: sell item - number Y-Axis
    idc.set_cmt(0x71C1D1, "[UI] sell item - number Y-Axis", 0)
    idc.set_name(0x71C1D1, "ui_71C1D1", idaapi.SN_NOWARN)
    # 71D9B8: weapon shop - cursor row count (menu refresh)
    idc.set_cmt(0x71D9B8, "[UI] weapon shop - cursor row count (menu refresh)", 0)
    idc.set_name(0x71D9B8, "ui_71D9B8", idaapi.SN_NOWARN)
    # 71E134: sell materia - right box cursor visible row (full 
    idc.set_cmt(0x71E134, "[UI] sell materia - right box cursor visible row (full menu refresh)", 0)
    idc.set_name(0x71E134, "ui_71E134", idaapi.SN_NOWARN)
    # 71E46D: sell materia - element Y-Axis
    idc.set_cmt(0x71E46D, "[UI] sell materia - element Y-Axis", 0)
    idc.set_name(0x71E46D, "ui_71E46D", idaapi.SN_NOWARN)
    # 71E472: sell materia - element X-Axis
    idc.set_cmt(0x71E472, "[UI] sell materia - element X-Axis", 0)
    idc.set_name(0x71E472, "ui_71E472", idaapi.SN_NOWARN)
    # 71E4CC: sell materia - materia icon Y-Axis
    idc.set_cmt(0x71E4CC, "[UI] sell materia - materia icon Y-Axis", 0)
    idc.set_name(0x71E4CC, "ui_71E4CC", idaapi.SN_NOWARN)
    # 71E558: sell materia - filled stars X-Axis related
    idc.set_cmt(0x71E558, "[UI] sell materia - filled stars X-Axis related", 0)
    idc.set_name(0x71E558, "ui_71E558", idaapi.SN_NOWARN)
    # 71E58B: sell materia - empty stars X-Axis related
    idc.set_cmt(0x71E58B, "[UI] sell materia - empty stars X-Axis related", 0)
    idc.set_name(0x71E58B, "ui_71E58B", idaapi.SN_NOWARN)
    # 71E5B1: sell materia - next level value Y-Axis
    idc.set_cmt(0x71E5B1, "[UI] sell materia - next level value Y-Axis", 0)
    idc.set_name(0x71E5B1, "ui_71E5B1", idaapi.SN_NOWARN)
    # 71E5B6: sell materia - next level value X-Axis
    idc.set_cmt(0x71E5B6, "[UI] sell materia - next level value X-Axis", 0)
    idc.set_name(0x71E5B6, "ui_71E5B6", idaapi.SN_NOWARN)
    # 71E5E7: sell materia - ap value Y-Axis
    idc.set_cmt(0x71E5E7, "[UI] sell materia - ap value Y-Axis", 0)
    idc.set_name(0x71E5E7, "ui_71E5E7", idaapi.SN_NOWARN)
    # 71E5EC: sell materia - ap value X-Axis
    idc.set_cmt(0x71E5EC, "[UI] sell materia - ap value X-Axis", 0)
    idc.set_name(0x71E5EC, "ui_71E5EC", idaapi.SN_NOWARN)
    # 71E60C: sell materia - MASTER X-Axis
    idc.set_cmt(0x71E60C, "[UI] sell materia - MASTER X-Axis", 0)
    idc.set_name(0x71E60C, "ui_71E60C", idaapi.SN_NOWARN)
    # 71E625: sell materia - next level WORD Y-Axis
    idc.set_cmt(0x71E625, "[UI] sell materia - next level WORD Y-Axis", 0)
    idc.set_name(0x71E625, "ui_71E625", idaapi.SN_NOWARN)
    # 71E62A: sell materia - next level WORD X-Axis
    idc.set_cmt(0x71E62A, "[UI] sell materia - next level WORD X-Axis", 0)
    idc.set_name(0x71E62A, "ui_71E62A", idaapi.SN_NOWARN)
    # 71E640: sell materia - equip effect WORD Y-Axis
    idc.set_cmt(0x71E640, "[UI] sell materia - equip effect WORD Y-Axis", 0)
    idc.set_name(0x71E640, "ui_71E640", idaapi.SN_NOWARN)
    # 71E645: sell materia - equip effect WORD X-Axis
    idc.set_cmt(0x71E645, "[UI] sell materia - equip effect WORD X-Axis", 0)
    idc.set_name(0x71E645, "ui_71E645", idaapi.SN_NOWARN)
    # 71E663: sell materia - AP WORD X-Axis
    idc.set_cmt(0x71E663, "[UI] sell materia - AP WORD X-Axis", 0)
    idc.set_name(0x71E663, "ui_71E663", idaapi.SN_NOWARN)
    # 71E67C: sell materia - ability list WORD Y-Axis
    idc.set_cmt(0x71E67C, "[UI] sell materia - ability list WORD Y-Axis", 0)
    idc.set_name(0x71E67C, "ui_71E67C", idaapi.SN_NOWARN)
    # 71E681: sell materia - ability list WORD X-Axis
    idc.set_cmt(0x71E681, "[UI] sell materia - ability list WORD X-Axis", 0)
    idc.set_name(0x71E681, "ui_71E681", idaapi.SN_NOWARN)
    # 71E697: sell materia - equip effect WORD clone Y-Axis
    idc.set_cmt(0x71E697, "[UI] sell materia - equip effect WORD clone Y-Axis", 0)
    idc.set_name(0x71E697, "ui_71E697", idaapi.SN_NOWARN)
    # 71E69C: sell materia - equip effect WORD clone X-Axis
    idc.set_cmt(0x71E69C, "[UI] sell materia - equip effect WORD clone X-Axis", 0)
    idc.set_name(0x71E69C, "ui_71E69C", idaapi.SN_NOWARN)
    # 71E751: sell materia - green ability Y-Axis
    idc.set_cmt(0x71E751, "[UI] sell materia - green ability Y-Axis", 0)
    idc.set_name(0x71E751, "ui_71E751", idaapi.SN_NOWARN)
    # 71E757: sell materia - green ability X-Axis
    idc.set_cmt(0x71E757, "[UI] sell materia - green ability X-Axis", 0)
    idc.set_name(0x71E757, "ui_71E757", idaapi.SN_NOWARN)
    # 71E794: sell materia - red ability Y-Axis
    idc.set_cmt(0x71E794, "[UI] sell materia - red ability Y-Axis", 0)
    idc.set_name(0x71E794, "ui_71E794", idaapi.SN_NOWARN)
    # 71E799: sell materia - red ability X-Axis
    idc.set_cmt(0x71E799, "[UI] sell materia - red ability X-Axis", 0)
    idc.set_name(0x71E799, "ui_71E799", idaapi.SN_NOWARN)
    # 71E823: sell materia - yellow ability Y-Axis
    idc.set_cmt(0x71E823, "[UI] sell materia - yellow ability Y-Axis", 0)
    idc.set_name(0x71E823, "ui_71E823", idaapi.SN_NOWARN)
    # 71E829: sell materia - yellow ability X-Axis
    idc.set_cmt(0x71E829, "[UI] sell materia - yellow ability X-Axis", 0)
    idc.set_name(0x71E829, "ui_71E829", idaapi.SN_NOWARN)
    # 71E871: sell materia - purple MPUP ability Y-Axis
    idc.set_cmt(0x71E871, "[UI] sell materia - purple MPUP ability Y-Axis", 0)
    idc.set_name(0x71E871, "ui_71E871", idaapi.SN_NOWARN)
    # 71E876: sell materia - purple MPUP ability X-Axis
    idc.set_cmt(0x71E876, "[UI] sell materia - purple MPUP ability X-Axis", 0)
    idc.set_name(0x71E876, "ui_71E876", idaapi.SN_NOWARN)
    # 71E894: sell materia - purple MPUP number Y-Axis
    idc.set_cmt(0x71E894, "[UI] sell materia - purple MPUP number Y-Axis", 0)
    idc.set_name(0x71E894, "ui_71E894", idaapi.SN_NOWARN)
    # 71E899: sell materia - purple MPUP number X-Axis
    idc.set_cmt(0x71E899, "[UI] sell materia - purple MPUP number X-Axis", 0)
    idc.set_name(0x71E899, "ui_71E899", idaapi.SN_NOWARN)
    # 71E8B2: sell materia - purple MPUP + Y-Axis
    idc.set_cmt(0x71E8B2, "[UI] sell materia - purple MPUP + Y-Axis", 0)
    idc.set_name(0x71E8B2, "ui_71E8B2", idaapi.SN_NOWARN)
    # 71E8B7: sell materia - purple MPUP + X-Axis
    idc.set_cmt(0x71E8B7, "[UI] sell materia - purple MPUP + X-Axis", 0)
    idc.set_name(0x71E8B7, "ui_71E8B7", idaapi.SN_NOWARN)
    # 71E8CD: sell materia - purple MPUP % Y-Axis
    idc.set_cmt(0x71E8CD, "[UI] sell materia - purple MPUP % Y-Axis", 0)
    idc.set_name(0x71E8CD, "ui_71E8CD", idaapi.SN_NOWARN)
    # 71E8D2: sell materia - purple MPUP % X-Axis
    idc.set_cmt(0x71E8D2, "[UI] sell materia - purple MPUP % X-Axis", 0)
    idc.set_name(0x71E8D2, "ui_71E8D2", idaapi.SN_NOWARN)
    # 71E8F0: sell materia - purple HPUP ability Y-Axis
    idc.set_cmt(0x71E8F0, "[UI] sell materia - purple HPUP ability Y-Axis", 0)
    idc.set_name(0x71E8F0, "ui_71E8F0", idaapi.SN_NOWARN)
    # 71E8F5: sell materia - purple HPUP ability X-Axis
    idc.set_cmt(0x71E8F5, "[UI] sell materia - purple HPUP ability X-Axis", 0)
    idc.set_name(0x71E8F5, "ui_71E8F5", idaapi.SN_NOWARN)
    # 71E914: sell materia - purple HPUP number Y-Axis
    idc.set_cmt(0x71E914, "[UI] sell materia - purple HPUP number Y-Axis", 0)
    idc.set_name(0x71E914, "ui_71E914", idaapi.SN_NOWARN)
    # 71E919: sell materia - purple HPUP number X-Axis
    idc.set_cmt(0x71E919, "[UI] sell materia - purple HPUP number X-Axis", 0)
    idc.set_name(0x71E919, "ui_71E919", idaapi.SN_NOWARN)
    # 71E932: sell materia - purple HPUP + Y-Axis
    idc.set_cmt(0x71E932, "[UI] sell materia - purple HPUP + Y-Axis", 0)
    idc.set_name(0x71E932, "ui_71E932", idaapi.SN_NOWARN)
    # 71E937: sell materia - purple HPUP + X-Axis
    idc.set_cmt(0x71E937, "[UI] sell materia - purple HPUP + X-Axis", 0)
    idc.set_name(0x71E937, "ui_71E937", idaapi.SN_NOWARN)
    # 71E94D: sell materia - purple HPUP % Y-Axis
    idc.set_cmt(0x71E94D, "[UI] sell materia - purple HPUP % Y-Axis", 0)
    idc.set_name(0x71E94D, "ui_71E94D", idaapi.SN_NOWARN)
    # 71E952: sell materia - purple HPUP % X-Axis
    idc.set_cmt(0x71E952, "[UI] sell materia - purple HPUP % X-Axis", 0)
    idc.set_name(0x71E952, "ui_71E952", idaapi.SN_NOWARN)
    # 71E970: sell materia - purple DEXUP ability Y-Axis
    idc.set_cmt(0x71E970, "[UI] sell materia - purple DEXUP ability Y-Axis", 0)
    idc.set_name(0x71E970, "ui_71E970", idaapi.SN_NOWARN)
    # 71E975: sell materia - purple DEXUP ability X-Axis
    idc.set_cmt(0x71E975, "[UI] sell materia - purple DEXUP ability X-Axis", 0)
    idc.set_name(0x71E975, "ui_71E975", idaapi.SN_NOWARN)
    # 71E994: sell materia - purple DEXUP number Y-Axis
    idc.set_cmt(0x71E994, "[UI] sell materia - purple DEXUP number Y-Axis", 0)
    idc.set_name(0x71E994, "ui_71E994", idaapi.SN_NOWARN)
    # 71E999: sell materia - purple DEXUP number X-Axis
    idc.set_cmt(0x71E999, "[UI] sell materia - purple DEXUP number X-Axis", 0)
    idc.set_name(0x71E999, "ui_71E999", idaapi.SN_NOWARN)
    # 71E9B2: sell materia - purple DEXUP + Y-Axis
    idc.set_cmt(0x71E9B2, "[UI] sell materia - purple DEXUP + Y-Axis", 0)
    idc.set_name(0x71E9B2, "ui_71E9B2", idaapi.SN_NOWARN)
    # 71E9B7: sell materia - purple DEXUP + X-Axis
    idc.set_cmt(0x71E9B7, "[UI] sell materia - purple DEXUP + X-Axis", 0)
    idc.set_name(0x71E9B7, "ui_71E9B7", idaapi.SN_NOWARN)
    # 71E9D0: sell materia - purple DEXUP % Y-Axis
    idc.set_cmt(0x71E9D0, "[UI] sell materia - purple DEXUP % Y-Axis", 0)
    idc.set_name(0x71E9D0, "ui_71E9D0", idaapi.SN_NOWARN)
    # 71E9D5: sell materia - purple DEXUP % X-Axis
    idc.set_cmt(0x71E9D5, "[UI] sell materia - purple DEXUP % X-Axis", 0)
    idc.set_name(0x71E9D5, "ui_71E9D5", idaapi.SN_NOWARN)
    # 71E9F0: sell materia - purple MAGUP ability Y-Axis
    idc.set_cmt(0x71E9F0, "[UI] sell materia - purple MAGUP ability Y-Axis", 0)
    idc.set_name(0x71E9F0, "ui_71E9F0", idaapi.SN_NOWARN)
    # 71E9F5: sell materia - purple MAGUP ability X-Axis
    idc.set_cmt(0x71E9F5, "[UI] sell materia - purple MAGUP ability X-Axis", 0)
    idc.set_name(0x71E9F5, "ui_71E9F5", idaapi.SN_NOWARN)
    # 71EA13: sell materia - purple MAGUP number Y-Axis
    idc.set_cmt(0x71EA13, "[UI] sell materia - purple MAGUP number Y-Axis", 0)
    idc.set_name(0x71EA13, "ui_71EA13", idaapi.SN_NOWARN)
    # 71EA18: sell materia - purple MAGUP number X-Axis
    idc.set_cmt(0x71EA18, "[UI] sell materia - purple MAGUP number X-Axis", 0)
    idc.set_name(0x71EA18, "ui_71EA18", idaapi.SN_NOWARN)
    # 71EA2E: sell materia - purple MAGUP + Y-Axis
    idc.set_cmt(0x71EA2E, "[UI] sell materia - purple MAGUP + Y-Axis", 0)
    idc.set_name(0x71EA2E, "ui_71EA2E", idaapi.SN_NOWARN)
    # 71EA33: sell materia - purple MAGUP + X-Axis
    idc.set_cmt(0x71EA33, "[UI] sell materia - purple MAGUP + X-Axis", 0)
    idc.set_name(0x71EA33, "ui_71EA33", idaapi.SN_NOWARN)
    # 71EA49: sell materia - purple MAGUP % Y-Axis
    idc.set_cmt(0x71EA49, "[UI] sell materia - purple MAGUP % Y-Axis", 0)
    idc.set_name(0x71EA49, "ui_71EA49", idaapi.SN_NOWARN)
    # 71EA4E: sell materia - purple MAGUP % X-Axis
    idc.set_cmt(0x71EA4E, "[UI] sell materia - purple MAGUP % X-Axis", 0)
    idc.set_name(0x71EA4E, "ui_71EA4E", idaapi.SN_NOWARN)
    # 71EA6C: sell materia - purple LUCKUP ability Y-Axis
    idc.set_cmt(0x71EA6C, "[UI] sell materia - purple LUCKUP ability Y-Axis", 0)
    idc.set_name(0x71EA6C, "ui_71EA6C", idaapi.SN_NOWARN)
    # 71EA71: sell materia - purple LUCKUP ability X-Axis
    idc.set_cmt(0x71EA71, "[UI] sell materia - purple LUCKUP ability X-Axis", 0)
    idc.set_name(0x71EA71, "ui_71EA71", idaapi.SN_NOWARN)
    # 71EA90: sell materia - purple LUCKUP number Y-Axis
    idc.set_cmt(0x71EA90, "[UI] sell materia - purple LUCKUP number Y-Axis", 0)
    idc.set_name(0x71EA90, "ui_71EA90", idaapi.SN_NOWARN)
    # 71EA95: sell materia - purple LUCKUP number X-Axis
    idc.set_cmt(0x71EA95, "[UI] sell materia - purple LUCKUP number X-Axis", 0)
    idc.set_name(0x71EA95, "ui_71EA95", idaapi.SN_NOWARN)
    # 71EAAB: sell materia - purple LUCKUP + Y-Axis
    idc.set_cmt(0x71EAAB, "[UI] sell materia - purple LUCKUP + Y-Axis", 0)
    idc.set_name(0x71EAAB, "ui_71EAAB", idaapi.SN_NOWARN)
    # 71EAB0: sell materia - purple LUCKUP + X-Axis
    idc.set_cmt(0x71EAB0, "[UI] sell materia - purple LUCKUP + X-Axis", 0)
    idc.set_name(0x71EAB0, "ui_71EAB0", idaapi.SN_NOWARN)
    # 71EAC6: sell materia - purple LUCKUP % Y-Axis
    idc.set_cmt(0x71EAC6, "[UI] sell materia - purple LUCKUP % Y-Axis", 0)
    idc.set_name(0x71EAC6, "ui_71EAC6", idaapi.SN_NOWARN)
    # 71EACB: sell materia - purple LUCKUP % X-Axis
    idc.set_cmt(0x71EACB, "[UI] sell materia - purple LUCKUP % X-Axis", 0)
    idc.set_name(0x71EACB, "ui_71EACB", idaapi.SN_NOWARN)
    # 71EAE6: sell materia - purple COVER ability Y-Axis
    idc.set_cmt(0x71EAE6, "[UI] sell materia - purple COVER ability Y-Axis", 0)
    idc.set_name(0x71EAE6, "ui_71EAE6", idaapi.SN_NOWARN)
    # 71EAEB: sell materia - purple COVER ability X-Axis
    idc.set_cmt(0x71EAEB, "[UI] sell materia - purple COVER ability X-Axis", 0)
    idc.set_name(0x71EAEB, "ui_71EAEB", idaapi.SN_NOWARN)
    # 71EB0A: sell materia - purple COVER number Y-Axis
    idc.set_cmt(0x71EB0A, "[UI] sell materia - purple COVER number Y-Axis", 0)
    idc.set_name(0x71EB0A, "ui_71EB0A", idaapi.SN_NOWARN)
    # 71EB0F: sell materia - purple COVER number X-Axis
    idc.set_cmt(0x71EB0F, "[UI] sell materia - purple COVER number X-Axis", 0)
    idc.set_name(0x71EB0F, "ui_71EB0F", idaapi.SN_NOWARN)
    # 71EB25: sell materia - purple COVER + Y-Axis
    idc.set_cmt(0x71EB25, "[UI] sell materia - purple COVER + Y-Axis", 0)
    idc.set_name(0x71EB25, "ui_71EB25", idaapi.SN_NOWARN)
    # 71EB2A: sell materia - purple COVER + X-Axis
    idc.set_cmt(0x71EB2A, "[UI] sell materia - purple COVER + X-Axis", 0)
    idc.set_name(0x71EB2A, "ui_71EB2A", idaapi.SN_NOWARN)
    # 71EB40: sell materia - purple COVER % Y-Axis
    idc.set_cmt(0x71EB40, "[UI] sell materia - purple COVER % Y-Axis", 0)
    idc.set_name(0x71EB40, "ui_71EB40", idaapi.SN_NOWARN)
    # 71EB45: sell materia - purple COVER % X-Axis
    idc.set_cmt(0x71EB45, "[UI] sell materia - purple COVER % X-Axis", 0)
    idc.set_name(0x71EB45, "ui_71EB45", idaapi.SN_NOWARN)
    # 71EB6A: sell materia - purple unique ability Y-Axis
    idc.set_cmt(0x71EB6A, "[UI] sell materia - purple unique ability Y-Axis", 0)
    idc.set_name(0x71EB6A, "ui_71EB6A", idaapi.SN_NOWARN)
    # 71EB6F: sell materia - purple unique ability X-Axis
    idc.set_cmt(0x71EB6F, "[UI] sell materia - purple unique ability X-Axis", 0)
    idc.set_name(0x71EB6F, "ui_71EB6F", idaapi.SN_NOWARN)
    # 71EB8F: sell materia - blue/purple hpmp/underwater ability
    idc.set_cmt(0x71EB8F, "[UI] sell materia - blue/purple hpmp/underwater ability Y-Axis", 0)
    idc.set_name(0x71EB8F, "ui_71EB8F", idaapi.SN_NOWARN)
    # 71EB94: sell materia - blue/purple hpmp/underwater ability
    idc.set_cmt(0x71EB94, "[UI] sell materia - blue/purple hpmp/underwater ability X-Axis", 0)
    idc.set_name(0x71EB94, "ui_71EB94", idaapi.SN_NOWARN)
    # 71EE6C: sell materia - equip effect - Y-Axis
    idc.set_cmt(0x71EE6C, "[UI] sell materia - equip effect - Y-Axis", 0)
    idc.set_name(0x71EE6C, "ui_71EE6C", idaapi.SN_NOWARN)
    # 71EE72: sell materia - equip effect - X-Axis
    idc.set_cmt(0x71EE72, "[UI] sell materia - equip effect - X-Axis", 0)
    idc.set_name(0x71EE72, "ui_71EE72", idaapi.SN_NOWARN)
    # 71EE9A: sell materia - equip effect + Y-Axis
    idc.set_cmt(0x71EE9A, "[UI] sell materia - equip effect + Y-Axis", 0)
    idc.set_name(0x71EE9A, "ui_71EE9A", idaapi.SN_NOWARN)
    # 71EEA0: sell materia - equip effect + X-Axis
    idc.set_cmt(0x71EEA0, "[UI] sell materia - equip effect + X-Axis", 0)
    idc.set_name(0x71EEA0, "ui_71EEA0", idaapi.SN_NOWARN)
    # 71EEDD: sell materia - equip effect numbers Y-Axis
    idc.set_cmt(0x71EEDD, "[UI] sell materia - equip effect numbers Y-Axis", 0)
    idc.set_name(0x71EEDD, "ui_71EEDD", idaapi.SN_NOWARN)
    # 71EEE3: sell materia - equip effect numbers X-Axis
    idc.set_cmt(0x71EEE3, "[UI] sell materia - equip effect numbers X-Axis", 0)
    idc.set_name(0x71EEE3, "ui_71EEE3", idaapi.SN_NOWARN)
    # 71EF0D: sell materia - equip effect words Y-Axis
    idc.set_cmt(0x71EF0D, "[UI] sell materia - equip effect words Y-Axis", 0)
    idc.set_name(0x71EF0D, "ui_71EF0D", idaapi.SN_NOWARN)
    # 71EF13: sell materia - equip effect words X-Axis
    idc.set_cmt(0x71EF13, "[UI] sell materia - equip effect words X-Axis", 0)
    idc.set_name(0x71EF13, "ui_71EF13", idaapi.SN_NOWARN)
    # 71EF39: sell materia - equip effect % Y-Axis
    idc.set_cmt(0x71EF39, "[UI] sell materia - equip effect % Y-Axis", 0)
    idc.set_name(0x71EF39, "ui_71EF39", idaapi.SN_NOWARN)
    # 71EF3F: sell materia - equip effect % X-Axis
    idc.set_cmt(0x71EF3F, "[UI] sell materia - equip effect % X-Axis", 0)
    idc.set_name(0x71EF3F, "ui_71EF3F", idaapi.SN_NOWARN)
    # 71FB9E: Materia slots BG Width
    idc.set_cmt(0x71FB9E, "[UI] Materia slots BG Width", 0)
    idc.set_name(0x71FB9E, "ui_71FB9E", idaapi.SN_NOWARN)
    # 71FBA4: Materia slots BG Height
    idc.set_cmt(0x71FBA4, "[UI] Materia slots BG Height", 0)
    idc.set_name(0x71FBA4, "ui_71FBA4", idaapi.SN_NOWARN)
    # 720802: save/load avatars Y-Axis
    idc.set_cmt(0x720802, "[UI] save/load avatars Y-Axis", 0)
    idc.set_name(0x720802, "ui_720802", idaapi.SN_NOWARN)
    # 720809: save/load avatars spacing X-Axis
    idc.set_cmt(0x720809, "[UI] save/load avatars spacing X-Axis", 0)
    idc.set_name(0x720809, "ui_720809", idaapi.SN_NOWARN)
    # 72080C: save/load avatars X-Axis
    idc.set_cmt(0x72080C, "[UI] save/load avatars X-Axis", 0)
    idc.set_name(0x72080C, "ui_72080C", idaapi.SN_NOWARN)
    # 72083F: save/load level number Y-Axis
    idc.set_cmt(0x72083F, "[UI] save/load level number Y-Axis", 0)
    idc.set_name(0x72083F, "ui_72083F", idaapi.SN_NOWARN)
    # 72086D: save/load level ':' Y-Axis
    idc.set_cmt(0x72086D, "[UI] save/load level ':' Y-Axis", 0)
    idc.set_name(0x72086D, "ui_72086D", idaapi.SN_NOWARN)
    # 720874: save/load level ':' X-Axis
    idc.set_cmt(0x720874, "[UI] save/load level ':' X-Axis", 0)
    idc.set_name(0x720874, "ui_720874", idaapi.SN_NOWARN)
    # 72089C: save/load level time hour value Y-Axis
    idc.set_cmt(0x72089C, "[UI] save/load level time hour value Y-Axis", 0)
    idc.set_name(0x72089C, "ui_72089C", idaapi.SN_NOWARN)
    # 7208A3: save/load level time hour value X-Axis
    idc.set_cmt(0x7208A3, "[UI] save/load level time hour value X-Axis", 0)
    idc.set_name(0x7208A3, "ui_7208A3", idaapi.SN_NOWARN)
    # 7208A6: save/load level time hour leading 0s remove
    idc.set_cmt(0x7208A6, "[UI] save/load level time hour leading 0s remove", 0)
    idc.set_name(0x7208A6, "ui_7208A6", idaapi.SN_NOWARN)
    # 7208CB: save/load level time minute value Y-Axis
    idc.set_cmt(0x7208CB, "[UI] save/load level time minute value Y-Axis", 0)
    idc.set_name(0x7208CB, "ui_7208CB", idaapi.SN_NOWARN)
    # 7208D2: save/load level time minute value X-Axis
    idc.set_cmt(0x7208D2, "[UI] save/load level time minute value X-Axis", 0)
    idc.set_name(0x7208D2, "ui_7208D2", idaapi.SN_NOWARN)
    # 7208F4: save/load level gil value Y-Axis
    idc.set_cmt(0x7208F4, "[UI] save/load level gil value Y-Axis", 0)
    idc.set_name(0x7208F4, "ui_7208F4", idaapi.SN_NOWARN)
    # 7208FB: save/load level gil value X-Axis
    idc.set_cmt(0x7208FB, "[UI] save/load level gil value X-Axis", 0)
    idc.set_name(0x7208FB, "ui_7208FB", idaapi.SN_NOWARN)
    # 720916: save/load level WORD Y-Axis
    idc.set_cmt(0x720916, "[UI] save/load level WORD Y-Axis", 0)
    idc.set_name(0x720916, "ui_720916", idaapi.SN_NOWARN)
    # 720938: save/load name Y-Axis
    idc.set_cmt(0x720938, "[UI] save/load name Y-Axis", 0)
    idc.set_name(0x720938, "ui_720938", idaapi.SN_NOWARN)
    # 72093B: save/load name X-Axis
    idc.set_cmt(0x72093B, "[UI] save/load name X-Axis", 0)
    idc.set_name(0x72093B, "ui_72093B", idaapi.SN_NOWARN)
    # 7213A5: load save select cursor spacing X-Axis
    idc.set_cmt(0x7213A5, "[UI] load save select cursor spacing X-Axis", 0)
    idc.set_name(0x7213A5, "ui_7213A5", idaapi.SN_NOWARN)
    # 7213BD: load select text Y-Axis
    idc.set_cmt(0x7213BD, "[UI] load select text Y-Axis", 0)
    idc.set_name(0x7213BD, "ui_7213BD", idaapi.SN_NOWARN)
    # 7213BF: load select text X-Axis
    idc.set_cmt(0x7213BF, "[UI] load select text X-Axis", 0)
    idc.set_name(0x7213BF, "ui_7213BF", idaapi.SN_NOWARN)
    # 721424: load save select box text Y-Axis
    idc.set_cmt(0x721424, "[UI] load save select box text Y-Axis", 0)
    idc.set_name(0x721424, "ui_721424", idaapi.SN_NOWARN)
    # 721433: load save select box text X-Axis
    idc.set_cmt(0x721433, "[UI] load save select box text X-Axis", 0)
    idc.set_name(0x721433, "ui_721433", idaapi.SN_NOWARN)
    # 7214DD: save/load cursor Y-Axis
    idc.set_cmt(0x7214DD, "[UI] save/load cursor Y-Axis", 0)
    idc.set_name(0x7214DD, "ui_7214DD", idaapi.SN_NOWARN)
    # 7214E0: save/load cursor X-Axis
    idc.set_cmt(0x7214E0, "[UI] save/load cursor X-Axis", 0)
    idc.set_name(0x7214E0, "ui_7214E0", idaapi.SN_NOWARN)
    # 72160E: save/load select text Y-Axis
    idc.set_cmt(0x72160E, "[UI] save/load select text Y-Axis", 0)
    idc.set_name(0x72160E, "ui_72160E", idaapi.SN_NOWARN)
    # 721610: save/load select text X-Axis
    idc.set_cmt(0x721610, "[UI] save/load select text X-Axis", 0)
    idc.set_name(0x721610, "ui_721610", idaapi.SN_NOWARN)
    # 721625: save/load game WORD X-Axis
    idc.set_cmt(0x721625, "[UI] save/load game WORD X-Axis", 0)
    idc.set_name(0x721625, "ui_721625", idaapi.SN_NOWARN)
    # 72165E: save/load game number X-Axis
    idc.set_cmt(0x72165E, "[UI] save/load game number X-Axis", 0)
    idc.set_name(0x72165E, "ui_72165E", idaapi.SN_NOWARN)
    # 7216BE: load select alt text Y-Axis
    idc.set_cmt(0x7216BE, "[UI] load select alt text Y-Axis", 0)
    idc.set_name(0x7216BE, "ui_7216BE", idaapi.SN_NOWARN)
    # 7216C0: load select alt text X-Axis
    idc.set_cmt(0x7216C0, "[UI] load select alt text X-Axis", 0)
    idc.set_name(0x7216C0, "ui_7216C0", idaapi.SN_NOWARN)
    # 7217C5: below is to refresh font spacing at new game scree
    idc.set_cmt(0x7217C5, "[UI] below is to refresh font spacing at new game screen, because of way 7h processes hext", 0)
    idc.set_name(0x7217C5, "ui_7217C5", idaapi.SN_NOWARN)
    # 7217D1: new/continue cursor Y-Axis
    idc.set_cmt(0x7217D1, "[UI] new/continue cursor Y-Axis", 0)
    idc.set_name(0x7217D1, "ui_7217D1", idaapi.SN_NOWARN)
    # 7217DC: new/continue cursor X-Axis
    idc.set_cmt(0x7217DC, "[UI] new/continue cursor X-Axis", 0)
    idc.set_name(0x7217DC, "ui_7217DC", idaapi.SN_NOWARN)
    # 767DCF: Map positioning X-Axis
    idc.set_cmt(0x767DCF, "[UI] Map positioning X-Axis", 0)
    idc.set_name(0x767DCF, "ui_767DCF", idaapi.SN_NOWARN)
    # 767DD3: Map positioning Y-Axis
    idc.set_cmt(0x767DD3, "[UI] Map positioning Y-Axis", 0)
    idc.set_name(0x767DD3, "ui_767DD3", idaapi.SN_NOWARN)
    # 768FEB: world map box X / Width / Height
    idc.set_cmt(0x768FEB, "[UI] world map box X / Width / Height", 0)
    idc.set_name(0x768FEB, "ui_768FEB", idaapi.SN_NOWARN)
    # 769682: world map cursor X-Axis
    idc.set_cmt(0x769682, "[UI] world map cursor X-Axis", 0)
    idc.set_name(0x769682, "ui_769682", idaapi.SN_NOWARN)
    # 76968A: world map cursor spacing Y-Axis
    idc.set_cmt(0x76968A, "[UI] world map cursor spacing Y-Axis", 0)
    idc.set_name(0x76968A, "ui_76968A", idaapi.SN_NOWARN)
    # 76968F: world map cursor Y-Axis
    idc.set_cmt(0x76968F, "[UI] world map cursor Y-Axis", 0)
    idc.set_name(0x76968F, "ui_76968F", idaapi.SN_NOWARN)
    # 7B7CF8: Set menu font scaling value to be 2.0 via value
    idc.set_cmt(0x7B7CF8, "[UI] Set menu font scaling value to be 2.0 via value", 0)
    idc.set_name(0x7B7CF8, "ui_7B7CF8", idaapi.SN_NOWARN)
    # 91391E: allied name X-Axis
    idc.set_cmt(0x91391E, "[UI] allied name X-Axis", 0)
    idc.set_name(0x91391E, "ui_91391E", idaapi.SN_NOWARN)
    # 91392D: selected name X-Axis
    idc.set_cmt(0x91392D, "[UI] selected name X-Axis", 0)
    idc.set_name(0x91392D, "ui_91392D", idaapi.SN_NOWARN)
    # 913A6F: weapon/item shop - prices Y-Axis
    idc.set_cmt(0x913A6F, "[UI] weapon/item shop - prices Y-Axis", 0)
    idc.set_name(0x913A6F, "ui_913A6F", idaapi.SN_NOWARN)
    # 913A76: weapon/item shop - text Y-Axis
    idc.set_cmt(0x913A76, "[UI] weapon/item shop - text Y-Axis", 0)
    idc.set_name(0x913A76, "ui_913A76", idaapi.SN_NOWARN)
    # 913A83: materia shop - text Y-Axis
    idc.set_cmt(0x913A83, "[UI] materia shop - text Y-Axis", 0)
    idc.set_name(0x913A83, "ui_913A83", idaapi.SN_NOWARN)
    # 913A8F: materia shop - price Y-Axis
    idc.set_cmt(0x913A8F, "[UI] materia shop - price Y-Axis", 0)
    idc.set_name(0x913A8F, "ui_913A8F", idaapi.SN_NOWARN)
    # 913D1D: Date header X-Axis
    idc.set_cmt(0x913D1D, "[UI] Date header X-Axis", 0)
    idc.set_name(0x913D1D, "ui_913D1D", idaapi.SN_NOWARN)
    # 913FAE: icon conditinal
    idc.set_cmt(0x913FAE, "[UI] icon conditinal", 0)
    idc.set_name(0x913FAE, "ui_913FAE", idaapi.SN_NOWARN)
    # 914196: Ä+ITEM Á+ITEM Ç+ITEM É+ITEM
    idc.set_cmt(0x914196, "[UI] Ä+ITEM Á+ITEM Ç+ITEM É+ITEM", 0)
    idc.set_name(0x914196, "ui_914196", idaapi.SN_NOWARN)
    # 9141A6: Ñ+ITEM Ö+ITEM Ü+ITEM á+ITEM
    idc.set_cmt(0x9141A6, "[UI] Ñ+ITEM Ö+ITEM Ü+ITEM á+ITEM", 0)
    idc.set_name(0x9141A6, "ui_9141A6", idaapi.SN_NOWARN)
    # 9141B6: à+ITEM â ä ã
    idc.set_cmt(0x9141B6, "[UI] à+ITEM â ä ã", 0)
    idc.set_name(0x9141B6, "ui_9141B6", idaapi.SN_NOWARN)
    # 9141E6: î+ITEM ï+ITEM ñ+ITEM ó+ITEM
    idc.set_cmt(0x9141E6, "[UI] î+ITEM ï+ITEM ñ+ITEM ó+ITEM", 0)
    idc.set_name(0x9141E6, "ui_9141E6", idaapi.SN_NOWARN)
    # 9141F6: ò+ITEM ô+ITEM ö+ITEM õ+ITEM
    idc.set_cmt(0x9141F6, "[UI] ò+ITEM ô+ITEM ö+ITEM õ+ITEM", 0)
    idc.set_name(0x9141F6, "ui_9141F6", idaapi.SN_NOWARN)
    # 914206: ú+ITEM ù+ITEM û ü
    idc.set_cmt(0x914206, "[UI] ú+ITEM ù+ITEM û ü", 0)
    idc.set_name(0x914206, "ui_914206", idaapi.SN_NOWARN)
    # 914236: [0x88]  [0x89]+AVATAR  [0x8A]+AVATAR  ´+ITEM
    idc.set_cmt(0x914236, "[UI] [0x88]  [0x89]+AVATAR  [0x8A]+AVATAR  ´+ITEM", 0)
    idc.set_name(0x914236, "ui_914236", idaapi.SN_NOWARN)
    # 914237: AVATAR
    idc.set_cmt(0x914237, "[UI] AVATAR", 0)
    idc.set_name(0x914237, "ui_914237", idaapi.SN_NOWARN)
    # 914246: ¨+AVATAR   ≠+AVATAR   Æ_ITEM   Ø+AVATAR
    idc.set_cmt(0x914246, "[UI] ¨+AVATAR   ≠+AVATAR   Æ_ITEM   Ø+AVATAR", 0)
    idc.set_name(0x914246, "ui_914246", idaapi.SN_NOWARN)
    # 914256: ∞   ±+AVATAR   ≤+AVATAR   ≥+LEFT
    idc.set_cmt(0x914256, "[UI] ∞   ±+AVATAR   ≤+AVATAR   ≥+LEFT", 0)
    idc.set_name(0x914256, "ui_914256", idaapi.SN_NOWARN)
    # 914286: º+R2 Ω æ+ITEM ø+ITEM
    idc.set_cmt(0x914286, "[UI] º+R2 Ω æ+ITEM ø+ITEM", 0)
    idc.set_name(0x914286, "ui_914286", idaapi.SN_NOWARN)
    # 914296: ¿+ITEM ¡+ITEM ¬ √+AVATAR
    idc.set_cmt(0x914296, "[UI] ¿+ITEM ¡+ITEM ¬ √+AVATAR", 0)
    idc.set_name(0x914296, "ui_914296", idaapi.SN_NOWARN)
    # 9142A6: ƒ+AVATAR ≈+AVATAR ∆ «
    idc.set_cmt(0x9142A6, "[UI] ƒ+AVATAR ≈+AVATAR ∆ «", 0)
    idc.set_name(0x9142A6, "ui_9142A6", idaapi.SN_NOWARN)
    # 9142F6: ÿ+ITEM Ÿ+ITEM ⁄ [0xBB]
    idc.set_cmt(0x9142F6, "[UI] ÿ+ITEM Ÿ+ITEM ⁄ [0xBB]", 0)
    idc.set_name(0x9142F6, "ui_9142F6", idaapi.SN_NOWARN)
    # 914336: [0xC8]+MATERIA [0xC9]+MATERIA [0xCA]+MATERIA [0xCB
    idc.set_cmt(0x914336, "[UI] [0xC8]+MATERIA [0xC9]+MATERIA [0xCA]+MATERIA [0xCB]materia", 0)
    idc.set_name(0x914336, "ui_914336", idaapi.SN_NOWARN)
    # 914346: [0xCC]+materia [0xCD]+item [0xCE]+ITEM [0xCF]+ITEM
    idc.set_cmt(0x914346, "[UI] [0xCC]+materia [0xCD]+item [0xCE]+ITEM [0xCF]+ITEM", 0)
    idc.set_name(0x914346, "ui_914346", idaapi.SN_NOWARN)
    # 914356: [0xD0] [0xD1]+item [0xD2] [0xD3]
    idc.set_cmt(0x914356, "[UI] [0xD0] [0xD1]+item [0xD2] [0xD3]", 0)
    idc.set_name(0x914356, "ui_914356", idaapi.SN_NOWARN)
    # 919DA5: Set menu system to load correct UI assets.
    idc.set_cmt(0x919DA5, "[UI] Set menu system to load correct UI assets.", 0)
    idc.set_name(0x919DA5, "ui_919DA5", idaapi.SN_NOWARN)
    # 91AA00: Next Level... Limit Level
    idc.set_cmt(0x91AA00, "[UI] Next Level... Limit Level", 0)
    idc.set_name(0x91AA00, "ui_91AA00", idaapi.SN_NOWARN)
    # 91AC48: left box cursor Y-Axis
    idc.set_cmt(0x91AC48, "[UI] left box cursor Y-Axis", 0)
    idc.set_name(0x91AC48, "ui_91AC48", idaapi.SN_NOWARN)
    # 91AC4A: left box selection cursor Y-Axis
    idc.set_cmt(0x91AC4A, "[UI] left box selection cursor Y-Axis", 0)
    idc.set_name(0x91AC4A, "ui_91AC4A", idaapi.SN_NOWARN)
    # 91AC4C: left box exit selection cursor Y-Axis
    idc.set_cmt(0x91AC4C, "[UI] left box exit selection cursor Y-Axis", 0)
    idc.set_name(0x91AC4C, "ui_91AC4C", idaapi.SN_NOWARN)
    # 91C342: main boxes Y-Axis
    idc.set_cmt(0x91C342, "[UI] main boxes Y-Axis", 0)
    idc.set_name(0x91C342, "ui_91C342", idaapi.SN_NOWARN)
    # 91C346: main UI visibility height (battle refresh)
    idc.set_cmt(0x91C346, "[UI] main UI visibility height (battle refresh)", 0)
    idc.set_name(0x91C346, "ui_91C346", idaapi.SN_NOWARN)
    # 91C352: left main box left side X-Axis
    idc.set_cmt(0x91C352, "[UI] left main box left side X-Axis", 0)
    idc.set_name(0x91C352, "ui_91C352", idaapi.SN_NOWARN)
    # 91C354: hide left box
    idc.set_cmt(0x91C354, "[UI] hide left box", 0)
    idc.set_name(0x91C354, "ui_91C354", idaapi.SN_NOWARN)
    # 91C355: remove left box
    idc.set_cmt(0x91C355, "[UI] remove left box", 0)
    idc.set_name(0x91C355, "ui_91C355", idaapi.SN_NOWARN)
    # 91C356: left main box right side X-Axis
    idc.set_cmt(0x91C356, "[UI] left main box right side X-Axis", 0)
    idc.set_name(0x91C356, "ui_91C356", idaapi.SN_NOWARN)
    # 91C358: left main box height
    idc.set_cmt(0x91C358, "[UI] left main box height", 0)
    idc.set_name(0x91C358, "ui_91C358", idaapi.SN_NOWARN)
    # 91C35A: right box X-Axis
    idc.set_cmt(0x91C35A, "[UI] right box X-Axis", 0)
    idc.set_name(0x91C35A, "ui_91C35A", idaapi.SN_NOWARN)
    # 91C35D: hide main boxes
    idc.set_cmt(0x91C35D, "[UI] hide main boxes", 0)
    idc.set_name(0x91C35D, "ui_91C35D", idaapi.SN_NOWARN)
    # 91C35E: right main box right side X-Axis
    idc.set_cmt(0x91C35E, "[UI] right main box right side X-Axis", 0)
    idc.set_name(0x91C35E, "ui_91C35E", idaapi.SN_NOWARN)
    # 91C360: right main box height
    idc.set_cmt(0x91C360, "[UI] right main box height", 0)
    idc.set_name(0x91C360, "ui_91C360", idaapi.SN_NOWARN)
    # 91C3D8: command box X-Axis
    idc.set_cmt(0x91C3D8, "[UI] command box X-Axis", 0)
    idc.set_name(0x91C3D8, "ui_91C3D8", idaapi.SN_NOWARN)
    # 91C3DA: command box Y-Axis
    idc.set_cmt(0x91C3DA, "[UI] command box Y-Axis", 0)
    idc.set_name(0x91C3DA, "ui_91C3DA", idaapi.SN_NOWARN)
    # 91C3F0: command box height
    idc.set_cmt(0x91C3F0, "[UI] command box height", 0)
    idc.set_name(0x91C3F0, "ui_91C3F0", idaapi.SN_NOWARN)
    # 91C470: change box X-Axis
    idc.set_cmt(0x91C470, "[UI] change box X-Axis", 0)
    idc.set_name(0x91C470, "ui_91C470", idaapi.SN_NOWARN)
    # 91C472: change box Y-Axis, View Width,View Height (box ref
    idc.set_cmt(0x91C472, "[UI] change box Y-Axis, View Width,View Height (box refresh)", 0)
    idc.set_name(0x91C472, "ui_91C472", idaapi.SN_NOWARN)
    # 91C486: change box Width
    idc.set_cmt(0x91C486, "[UI] change box Width", 0)
    idc.set_name(0x91C486, "ui_91C486", idaapi.SN_NOWARN)
    # 91C508: defend/change boxes
    idc.set_cmt(0x91C508, "[UI] defend/change boxes", 0)
    idc.set_name(0x91C508, "ui_91C508", idaapi.SN_NOWARN)
    # 91C50A: defend box Y-Axis, View Width,View Height (box ref
    idc.set_cmt(0x91C50A, "[UI] defend box Y-Axis, View Width,View Height (box refresh)", 0)
    idc.set_name(0x91C50A, "ui_91C50A", idaapi.SN_NOWARN)
    # 91C51E: defend box Width
    idc.set_cmt(0x91C51E, "[UI] defend box Width", 0)
    idc.set_name(0x91C51E, "ui_91C51E", idaapi.SN_NOWARN)
    # 91C5A0: eskill boxes X-Axis
    idc.set_cmt(0x91C5A0, "[UI] eskill boxes X-Axis", 0)
    idc.set_name(0x91C5A0, "ui_91C5A0", idaapi.SN_NOWARN)
    # 91C5A2: eskill boxes Y-Axis
    idc.set_cmt(0x91C5A2, "[UI] eskill boxes Y-Axis", 0)
    idc.set_name(0x91C5A2, "ui_91C5A2", idaapi.SN_NOWARN)
    # 91C5A6: eskill boxes UI visibility height (battle refresh)
    idc.set_cmt(0x91C5A6, "[UI] eskill boxes UI visibility height (battle refresh)", 0)
    idc.set_name(0x91C5A6, "ui_91C5A6", idaapi.SN_NOWARN)
    # 91C5B6: eskill boxes left box Width
    idc.set_cmt(0x91C5B6, "[UI] eskill boxes left box Width", 0)
    idc.set_name(0x91C5B6, "ui_91C5B6", idaapi.SN_NOWARN)
    # 91C5B8: eskill boxes left box HEIGHT
    idc.set_cmt(0x91C5B8, "[UI] eskill boxes left box HEIGHT", 0)
    idc.set_name(0x91C5B8, "ui_91C5B8", idaapi.SN_NOWARN)
    # 91C5BA: eskill boxes right box X-Axis
    idc.set_cmt(0x91C5BA, "[UI] eskill boxes right box X-Axis", 0)
    idc.set_name(0x91C5BA, "ui_91C5BA", idaapi.SN_NOWARN)
    # 91C5BE: eskill boxes right box right X-Axis
    idc.set_cmt(0x91C5BE, "[UI] eskill boxes right box right X-Axis", 0)
    idc.set_name(0x91C5BE, "ui_91C5BE", idaapi.SN_NOWARN)
    # 91C5C0: eskill boxes right box HEIGHT
    idc.set_cmt(0x91C5C0, "[UI] eskill boxes right box HEIGHT", 0)
    idc.set_name(0x91C5C0, "ui_91C5C0", idaapi.SN_NOWARN)
    # 91C638: item box X-Axis
    idc.set_cmt(0x91C638, "[UI] item box X-Axis", 0)
    idc.set_name(0x91C638, "ui_91C638", idaapi.SN_NOWARN)
    # 91C63A: item box Y-Axis
    idc.set_cmt(0x91C63A, "[UI] item box Y-Axis", 0)
    idc.set_name(0x91C63A, "ui_91C63A", idaapi.SN_NOWARN)
    # 91C63E: item box UI visibility height (battle refresh)
    idc.set_cmt(0x91C63E, "[UI] item box UI visibility height (battle refresh)", 0)
    idc.set_name(0x91C63E, "ui_91C63E", idaapi.SN_NOWARN)
    # 91C64E: item box width
    idc.set_cmt(0x91C64E, "[UI] item box width", 0)
    idc.set_name(0x91C64E, "ui_91C64E", idaapi.SN_NOWARN)
    # 91C650: item box height
    idc.set_cmt(0x91C650, "[UI] item box height", 0)
    idc.set_name(0x91C650, "ui_91C650", idaapi.SN_NOWARN)
    # 91C6D0: magic boxes X-Axis
    idc.set_cmt(0x91C6D0, "[UI] magic boxes X-Axis", 0)
    idc.set_name(0x91C6D0, "ui_91C6D0", idaapi.SN_NOWARN)
    # 91C6D2: magic boxes Y-Axis
    idc.set_cmt(0x91C6D2, "[UI] magic boxes Y-Axis", 0)
    idc.set_name(0x91C6D2, "ui_91C6D2", idaapi.SN_NOWARN)
    # 91C6D6: magic boxes UI visibility height (battle refresh)
    idc.set_cmt(0x91C6D6, "[UI] magic boxes UI visibility height (battle refresh)", 0)
    idc.set_name(0x91C6D6, "ui_91C6D6", idaapi.SN_NOWARN)
    # 91C6E6: magic box left box width
    idc.set_cmt(0x91C6E6, "[UI] magic box left box width", 0)
    idc.set_name(0x91C6E6, "ui_91C6E6", idaapi.SN_NOWARN)
    # 91C6E8: magic box left box height
    idc.set_cmt(0x91C6E8, "[UI] magic box left box height", 0)
    idc.set_name(0x91C6E8, "ui_91C6E8", idaapi.SN_NOWARN)
    # 91C6EA: magic box right box left X-Axis
    idc.set_cmt(0x91C6EA, "[UI] magic box right box left X-Axis", 0)
    idc.set_name(0x91C6EA, "ui_91C6EA", idaapi.SN_NOWARN)
    # 91C6EE: magic box right box right X-Axis
    idc.set_cmt(0x91C6EE, "[UI] magic box right box right X-Axis", 0)
    idc.set_name(0x91C6EE, "ui_91C6EE", idaapi.SN_NOWARN)
    # 91C6F0: magic box right box height
    idc.set_cmt(0x91C6F0, "[UI] magic box right box height", 0)
    idc.set_name(0x91C6F0, "ui_91C6F0", idaapi.SN_NOWARN)
    # 91C768: summon boxes X-Axis
    idc.set_cmt(0x91C768, "[UI] summon boxes X-Axis", 0)
    idc.set_name(0x91C768, "ui_91C768", idaapi.SN_NOWARN)
    # 91C76A: summon boxes Y-Axis
    idc.set_cmt(0x91C76A, "[UI] summon boxes Y-Axis", 0)
    idc.set_name(0x91C76A, "ui_91C76A", idaapi.SN_NOWARN)
    # 91C76E: summon box UI visibility height (battle refresh)
    idc.set_cmt(0x91C76E, "[UI] summon box UI visibility height (battle refresh)", 0)
    idc.set_name(0x91C76E, "ui_91C76E", idaapi.SN_NOWARN)
    # 91C77E: summon box left box width
    idc.set_cmt(0x91C77E, "[UI] summon box left box width", 0)
    idc.set_name(0x91C77E, "ui_91C77E", idaapi.SN_NOWARN)
    # 91C780: summon box left box height
    idc.set_cmt(0x91C780, "[UI] summon box left box height", 0)
    idc.set_name(0x91C780, "ui_91C780", idaapi.SN_NOWARN)
    # 91C782: summon box right box left X-Axis
    idc.set_cmt(0x91C782, "[UI] summon box right box left X-Axis", 0)
    idc.set_name(0x91C782, "ui_91C782", idaapi.SN_NOWARN)
    # 91C786: summon box right X-Axis
    idc.set_cmt(0x91C786, "[UI] summon box right X-Axis", 0)
    idc.set_name(0x91C786, "ui_91C786", idaapi.SN_NOWARN)
    # 91C788: summon box right height
    idc.set_cmt(0x91C788, "[UI] summon box right height", 0)
    idc.set_name(0x91C788, "ui_91C788", idaapi.SN_NOWARN)
    # 91C89A: worried other members box y-axis - thick borders v
    idc.set_cmt(0x91C89A, "[UI] worried other members box y-axis - thick borders v2", 0)
    idc.set_name(0x91C89A, "ui_91C89A", idaapi.SN_NOWARN)
    # 91C89C: box viewable width
    idc.set_cmt(0x91C89C, "[UI] box viewable width", 0)
    idc.set_name(0x91C89C, "ui_91C89C", idaapi.SN_NOWARN)
    # 91C89E: box viewable height
    idc.set_cmt(0x91C89E, "[UI] box viewable height", 0)
    idc.set_name(0x91C89E, "ui_91C89E", idaapi.SN_NOWARN)
    # 91C8AE: worried other members box width
    idc.set_cmt(0x91C8AE, "[UI] worried other members box width", 0)
    idc.set_name(0x91C8AE, "ui_91C8AE", idaapi.SN_NOWARN)
    # 91C8B0: worried other members box height
    idc.set_cmt(0x91C8B0, "[UI] worried other members box height", 0)
    idc.set_name(0x91C8B0, "ui_91C8B0", idaapi.SN_NOWARN)
    # 91CE88: Manip box
    idc.set_cmt(0x91CE88, "[UI] Manip box", 0)
    idc.set_name(0x91CE88, "ui_91CE88", idaapi.SN_NOWARN)
    # 91CE8A: manip box Y-Axis
    idc.set_cmt(0x91CE8A, "[UI] manip box Y-Axis", 0)
    idc.set_name(0x91CE8A, "ui_91CE8A", idaapi.SN_NOWARN)
    # 91CE9E: manip box width
    idc.set_cmt(0x91CE9E, "[UI] manip box width", 0)
    idc.set_name(0x91CE9E, "ui_91CE9E", idaapi.SN_NOWARN)
    # 91CEA0: manip box height
    idc.set_cmt(0x91CEA0, "[UI] manip box height", 0)
    idc.set_name(0x91CEA0, "ui_91CEA0", idaapi.SN_NOWARN)
    # 91CF20: Coin box
    idc.set_cmt(0x91CF20, "[UI] Coin box", 0)
    idc.set_name(0x91CF20, "ui_91CF20", idaapi.SN_NOWARN)
    # 91CF24: coin box view width
    idc.set_cmt(0x91CF24, "[UI] coin box view width", 0)
    idc.set_name(0x91CF24, "ui_91CF24", idaapi.SN_NOWARN)
    # 91CF36: coin box Width
    idc.set_cmt(0x91CF36, "[UI] coin box Width", 0)
    idc.set_name(0x91CF36, "ui_91CF36", idaapi.SN_NOWARN)
    # 91CF38: coin box Height
    idc.set_cmt(0x91CF38, "[UI] coin box Height", 0)
    idc.set_name(0x91CF38, "ui_91CF38", idaapi.SN_NOWARN)
    # 91CFB8: status/cure/ether box X-Axis
    idc.set_cmt(0x91CFB8, "[UI] status/cure/ether box X-Axis", 0)
    idc.set_name(0x91CFB8, "ui_91CFB8", idaapi.SN_NOWARN)
    # 91CFCE: status/cure/ether box Width
    idc.set_cmt(0x91CFCE, "[UI] status/cure/ether box Width", 0)
    idc.set_name(0x91CFCE, "ui_91CFCE", idaapi.SN_NOWARN)
    # 91D0EA: help box and text Y-Axis
    idc.set_cmt(0x91D0EA, "[UI] help box and text Y-Axis", 0)
    idc.set_name(0x91D0EA, "ui_91D0EA", idaapi.SN_NOWARN)
    # 91D180: limit box X-Axis, Y-Axis, View Width,View Height (
    idc.set_cmt(0x91D180, "[UI] limit box X-Axis, Y-Axis, View Width,View Height (box refresh)", 0)
    idc.set_name(0x91D180, "ui_91D180", idaapi.SN_NOWARN)
    # 91D184: limit box view width
    idc.set_cmt(0x91D184, "[UI] limit box view width", 0)
    idc.set_name(0x91D184, "ui_91D184", idaapi.SN_NOWARN)
    # 91D196: limit box Width, Height
    idc.set_cmt(0x91D196, "[UI] limit box Width, Height", 0)
    idc.set_name(0x91D196, "ui_91D196", idaapi.SN_NOWARN)
    # 91D218: action box X,Y,W,H
    idc.set_cmt(0x91D218, "[UI] action box X,Y,W,H", 0)
    idc.set_name(0x91D218, "ui_91D218", idaapi.SN_NOWARN)
    # 91D21E: help box and contents height
    idc.set_cmt(0x91D21E, "[UI] help box and contents height", 0)
    idc.set_name(0x91D21E, "ui_91D21E", idaapi.SN_NOWARN)
    # 91D2B0: cait sith box X-Axis, Y-Axis, Viewable Width, View
    idc.set_cmt(0x91D2B0, "[UI] cait sith box X-Axis, Y-Axis, Viewable Width, Viewable Height (box refresh)", 0)
    idc.set_name(0x91D2B0, "ui_91D2B0", idaapi.SN_NOWARN)
    # 91D2B2: cait sith reels Y-Axis
    idc.set_cmt(0x91D2B2, "[UI] cait sith reels Y-Axis", 0)
    idc.set_name(0x91D2B2, "ui_91D2B2", idaapi.SN_NOWARN)
    # 91D2B6: cait sith limit box view height
    idc.set_cmt(0x91D2B6, "[UI] cait sith limit box view height", 0)
    idc.set_name(0x91D2B6, "ui_91D2B6", idaapi.SN_NOWARN)
    # 91D2C6: cait sith background box width
    idc.set_cmt(0x91D2C6, "[UI] cait sith background box width", 0)
    idc.set_name(0x91D2C6, "ui_91D2C6", idaapi.SN_NOWARN)
    # 91D2C8: cait sith background box height
    idc.set_cmt(0x91D2C8, "[UI] cait sith background box height", 0)
    idc.set_name(0x91D2C8, "ui_91D2C8", idaapi.SN_NOWARN)
    # 91D34A: tifa reels box Y-Axis, Viewable Width, Viewable He
    idc.set_cmt(0x91D34A, "[UI] tifa reels box Y-Axis, Viewable Width, Viewable Height (box refresh)", 0)
    idc.set_name(0x91D34A, "ui_91D34A", idaapi.SN_NOWARN)
    # 91D34E: tifa limit box view height
    idc.set_cmt(0x91D34E, "[UI] tifa limit box view height", 0)
    idc.set_name(0x91D34E, "ui_91D34E", idaapi.SN_NOWARN)
    # 91D360: tifa reels background box height Y-Axis
    idc.set_cmt(0x91D360, "[UI] tifa reels background box height Y-Axis", 0)
    idc.set_name(0x91D360, "ui_91D360", idaapi.SN_NOWARN)
    # 91D3E2: battle arena box Y-Axis, View Width, View Height (
    idc.set_cmt(0x91D3E2, "[UI] battle arena box Y-Axis, View Width, View Height (box refresh)", 0)
    idc.set_name(0x91D3E2, "ui_91D3E2", idaapi.SN_NOWARN)
    # 91D3E6: battle arena box Height (box refresh)
    idc.set_cmt(0x91D3E6, "[UI] battle arena box Height (box refresh)", 0)
    idc.set_name(0x91D3E6, "ui_91D3E6", idaapi.SN_NOWARN)
    # 91D3F8: battle arena box width, height
    idc.set_cmt(0x91D3F8, "[UI] battle arena box width, height", 0)
    idc.set_name(0x91D3F8, "ui_91D3F8", idaapi.SN_NOWARN)
    # 91E7F8: command box width 1 column (battle refresh)
    idc.set_cmt(0x91E7F8, "[UI] command box width 1 column (battle refresh)", 0)
    idc.set_name(0x91E7F8, "ui_91E7F8", idaapi.SN_NOWARN)
    # 91E7FA: command box width 2 columns (battle refresh)
    idc.set_cmt(0x91E7FA, "[UI] command box width 2 columns (battle refresh)", 0)
    idc.set_name(0x91E7FA, "ui_91E7FA", idaapi.SN_NOWARN)
    # 91E7FC: command box width 3 columns (battle refresh)
    idc.set_cmt(0x91E7FC, "[UI] command box width 3 columns (battle refresh)", 0)
    idc.set_name(0x91E7FC, "ui_91E7FC", idaapi.SN_NOWARN)
    # 91E808: limit box Height  limit, 2 limits (box refresh)
    idc.set_cmt(0x91E808, "[UI] limit box Height  limit, 2 limits (box refresh)", 0)
    idc.set_name(0x91E808, "ui_91E808", idaapi.SN_NOWARN)
    # 91E94A: Resist text
    idc.set_cmt(0x91E94A, "[UI] Resist text", 0)
    idc.set_name(0x91E94A, "ui_91E94A", idaapi.SN_NOWARN)
    # 91E990: limit BG box Bottom - 1limit, 2limits
    idc.set_cmt(0x91E990, "[UI] limit BG box Bottom - 1limit, 2limits", 0)
    idc.set_name(0x91E990, "ui_91E990", idaapi.SN_NOWARN)
    # 920968: Command box width
    idc.set_cmt(0x920968, "[UI] Command box width", 0)
    idc.set_name(0x920968, "ui_920968", idaapi.SN_NOWARN)
    # 92097E: Command box height
    idc.set_cmt(0x92097E, "[UI] Command box height", 0)
    idc.set_name(0x92097E, "ui_92097E", idaapi.SN_NOWARN)
    # 920A4B: fix equip menu text consistency
    idc.set_cmt(0x920A4B, "[UI] fix equip menu text consistency", 0)
    idc.set_name(0x920A4B, "ui_920A4B", idaapi.SN_NOWARN)
    # 920EF8: materia menu - description box X-Axis, Y-Axis, Wid
    idc.set_cmt(0x920EF8, "[UI] materia menu - description box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x920EF8, "ui_920EF8", idaapi.SN_NOWARN)
    # 920F00: materia menu - left box X-Axis, Y-Axis, Width, Hei
    idc.set_cmt(0x920F00, "[UI] materia menu - left box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x920F00, "ui_920F00", idaapi.SN_NOWARN)
    # 920F18: arrange box X-Axis, Y-Axis, Width, Height
    idc.set_cmt(0x920F18, "[UI] arrange box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x920F18, "ui_920F18", idaapi.SN_NOWARN)
    # 920F30: materia menu - exchange middle box X-Axis, Y-Axis,
    idc.set_cmt(0x920F30, "[UI] materia menu - exchange middle box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x920F30, "ui_920F30", idaapi.SN_NOWARN)
    # 920F40: materia menu - exchange scroll box X-Axis, Y-Axis,
    idc.set_cmt(0x920F40, "[UI] materia menu - exchange scroll box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x920F40, "ui_920F40", idaapi.SN_NOWARN)
    # 920F44: materia menu - exchange scroll box Width
    idc.set_cmt(0x920F44, "[UI] materia menu - exchange scroll box Width", 0)
    idc.set_name(0x920F44, "ui_920F44", idaapi.SN_NOWARN)
    # 921110: magic menu - description box X-Axis, Y-Axis, Width
    idc.set_cmt(0x921110, "[UI] magic menu - description box X-Axis, Y-Axis, Width , Height", 0)
    idc.set_name(0x921110, "ui_921110", idaapi.SN_NOWARN)
    # 921120: magic menu - magic/summon/eskill box X-Axis, Y-Axi
    idc.set_cmt(0x921120, "[UI] magic menu - magic/summon/eskill box X-Axis, Y-Axis, Width , Height", 0)
    idc.set_name(0x921120, "ui_921120", idaapi.SN_NOWARN)
    # 921128: mpneeded box X-Axis, Y-Axis, Width , Height
    idc.set_cmt(0x921128, "[UI] mpneeded box X-Axis, Y-Axis, Width , Height", 0)
    idc.set_name(0x921128, "ui_921128", idaapi.SN_NOWARN)
    # 921130: sub menu title box X-Axis, Y-Axis, Width , Height
    idc.set_cmt(0x921130, "[UI] sub menu title box X-Axis, Y-Axis, Width , Height", 0)
    idc.set_name(0x921130, "ui_921130", idaapi.SN_NOWARN)
    # 921C80: Item Menu - description box X-Axis, Y-Axis, Width,
    idc.set_cmt(0x921C80, "[UI] Item Menu - description box X-Axis, Y-Axis, Width, Height", 0)
    idc.set_name(0x921C80, "ui_921C80", idaapi.SN_NOWARN)
    # 922A4C: below fixes buy/sell/exit/nextlevel text
    idc.set_cmt(0x922A4C, "[UI] below fixes buy/sell/exit/nextlevel text", 0)
    idc.set_name(0x922A4C, "ui_922A4C", idaapi.SN_NOWARN)
    # 99DE31: font spacing mini avatars  99DE33 was mini chocobo
    idc.set_cmt(0x99DE31, "[UI] font spacing mini avatars  99DE33 was mini chocobo but now used by extended icons", 0)
    idc.set_name(0x99DE31, "ui_99DE31", idaapi.SN_NOWARN)

    print("Annotated 1643 UI memory locations")

if __name__ == "__main__":
    annotate_ui_locations()

# Unscraped URLs - Research Inventory

**Created**: 2025-11-20 10:55:02 JST (Thursday)
**Last Updated**: 2025-11-20 10:55:02 JST (Thursday)
**Session-ID**: 953ea36d-3b58-45c5-ae41-560ac6d54d02

---

## Overview

This document lists all URLs that have NOT been successfully scraped as of Session 10. Includes:

- ❌ Failed scrapes (404, too large, access denied)
- ⏸️ Timeout issues (requires retry or manual download)
- ⏳ Pending (discovered but not yet attempted)

**Total Unscraped**: 26+ URLs remaining (4 scraped in Session 12)

---

## 🔴 CRITICAL PRIORITY -

### 2. qhimm Wiki - FF7 Font Documentation

- **URL**: http://wiki.qhimm.com/FF7
- **Status**: ❌ **404 Not Found - Wiki No Longer Exists**
- **Issue**: Wiki.qhimm.com domain returns 404 error
- **Solution**: Content may have migrated to qhimm-modding.fandom.com (check separately)
- **Why Critical**: Original qhimm wiki (pre-Fandom migration) may have had unique details
- **Relevance**: HIGH - Original community documentation (now unavailable)

### 4. WallMarket Thread (KERNEL.BIN Editor)

- **URL**: https://forums.qhimm.com/index.php?topic=7928.0
- **Status**: ✅ **Successfully Scraped (Session 12)**
- **Tool Type**: KERNEL.BIN editor for game text/data modification (v1.4.5)
- **Content**: Complete tool documentation (53-page thread, 1,069,667 reads)
- **Key Discoveries**: Full KERNEL.BIN editing (attacks, items, weapons, armor, accessories, materia, character AI, text strings), stackable patch system, LZS compressor/decompressor tool
- **Developer**: NFITC1 (qhimm forums)
- **Why High Priority**: Essential tool for modifying game text data
- **Relevance**: CRITICAL - Complete text editing infrastructure documented, shows community technical depth

### 9. CJK Font Atlas Blog

- **URL**: https://killertee.wordpress.com/2021/04/23/optimizing-workflow-textmesh-pro-font-atlas-for-language-localization/
- **Status**: ✅ **Successfully Scraped (Session 11)**
- **Content**: Complete TextMesh Pro localization guide with CJK font atlas constraints
- **Key Quote Confirmed**: "2000-3000 characters impossible in single 2048×2048 texture"
- **Additional Discoveries**: 3 localization workflows, character_processor tool, Better Workflow uses only 2 atlases
- **Why High Priority**: Validates FF7's 6-texture architecture mathematically
- **Relevance**: CRITICAL - Confirms industry standard approach matches FF7's implementation

### 10. 7th Heaven Help Page

- **URL**: https://7thheaven.rocks/help/userhelp.html
- **Status**: ✅ **Successfully Scraped (Session 11)**
- **Content**: Complete 15,000+ word comprehensive user guide
- **Key Discoveries**: mod_path must match FFNx.cfg, load order system, IRO format, profile system, shell integration
- **Additional Findings**: 7H 2.2+ includes FFNx natively, automatic game preparation, DDS priority over PNG
- **Why High Priority**: Complete integration architecture documentation
- **Relevance**: CRITICAL - Essential for FFNx texture override system implementation

### 12. PSX FFVII International Analysis

- **URL**: https://forums.qhimm.com/index.php?topic=8571.0
- **Status**: ✅ **Successfully Scraped (Session 11)**
- **Content**: Gemini's all-in-one translation package for FF7i (2009-2010 archived thread)
- **Key Discoveries**: Soft subtitle implementation, variable width font for 8×8, WINDOW.BIN regeneration, source code released
- **Tools Documented**: Subtitle code injection (SLPS/mdec), C++ dumper/inserter, glib.rar data library
- **Why High Priority**: Proves soft subtitles possible via code injection, variable width font reference code exists
- **Relevance**: HIGH - Historical tools provide implementation references for PC version

### 13. Japanese Gaming Forums (HAL's Blog)

- **URL**: http://hal51.click/game/ff7_mod
- **Status**: ✅ **Successfully Scraped (Session 12)**
- **Content**: Comprehensive Japanese FFNx + 7th Heaven integration guide (24,000+ words, updated 2024-07-16)
- **Key Discoveries**: FFNx Japanese support broken since 2020 (GitHub Issue #39), 7th Heaven generates English-only exe, manual LGP editing workaround documented, PC version history table (5 versions from 1998-2020), controller shortcuts, save data locations
- **Critical Finding**: "スクエニしか分からないような作りらしい" (Square Enix-only proprietary font driver architecture blocks Japanese support)
- **Why High Priority**: Japanese community perspective confirms our technical challenges
- **Relevance**: CRITICAL - Validates FFNx Path C challenges, documents 4-year unsolved problem

### 16. Aali's Driver Discussion

- **URL**: https://forums.qhimm.com/index.php?topic=17033.0
- **Status**: ✅ **Successfully Scraped (Session 12)**
- **Content**: Forum troubleshooting thread (2016) discussing old Aali's driver versions
- **Key Discoveries**: Aali's driver version history (v7.11b → v8.0 → v8.1b), music plugin architecture evolution (ff7music.fgp external program → vgmstream plugin native OGG), configuration error patterns documented
- **Historical Context**: Aali's driver → FFNx succession (~2020), plugin architecture patterns
- **Why Medium Priority**: Historical driver (superseded by FFNx)
- **Relevance**: MEDIUM - Shows plugin architecture evolution, useful for understanding FFNx design patterns

### 17. Texture Upscales Thread

- **URL**: https://forums.qhimm.com/index.php?topic=14469.0
- **Status**: ✅ **Successfully Scraped (Session 11)**
- **Content**: Complete battle scene texture enhancement project (2013-2014, EQ2Alyza + Iros)
- **Key Discoveries**: TexTool development (fixes Img2Tex alpha issues), complete TEX↔PNG workflow, 89 battle scenes + 413 world textures
- **Tools Created**: TexTool by Iros (batch TEX↔PNG conversion, handles alpha correctly)
- **Critical Technical Notes**: 24-bit vs 32-bit depth considerations, alpha channel handling for transparency, IRO packaging
- **Why High Priority**: Complete validated texture workflow with tool development story
- **Relevance**: HIGH - Proven texture modding pipeline applicable to font texture modifications

---

## 🎯 Recommendations for Next Sessions

### Immediate Priority (Can be scraped)

1. **7th Heaven Help page** - Direct URL, should be simple
2. **CJK Font Atlas Blog** - WordPress article, directly accessible
3. **Forum Thread Searches** - Search qhimm for WallMarket, Character Models
4. **Google Sheets** - Try to scrape The Reunion Database (may fail gracefully)

### Medium Priority (Need forum navigation)

5. **qhimm Wiki redirect** - Check if http://wiki.qhimm.com/FF7 redirects to fandom
6. **FF7 Tools Section** - Search qhimm board for tools sticky/pinned post
7. **PSX FFVII International** - Direct forum URL, should be accessible

### Low Priority (Not scrapable)

8. **Q-Gears PDF** - Manual download + local reading required
9. **Discord servers** - Not scrapable, but can join communities for collaboration
10. **YouTube tutorial** - Not scrapable, video-only content

### Unfixable

- **FF7 eStore page** - Product no longer available (confirmed 404), no workaround

---

## 💾 Data Collection Notes

### Forum Threads to Locate

- [ ] WallMarket thread (KERNEL.BIN editor documentation)
- [ ] FF7 Character Models thread (texture-related models)
- [ ] qhimm FF7 Tools sticky/announcement

### Redirect Checking

- [ ] http://wiki.qhimm.com/FF7 → may redirect to https://qhimm-modding.fandom.com/wiki/FF7

---

**Document Status**: Unscraped URLs Inventory
**Last Updated**: Session 12 (2025-11-20 19:35 JST)
**URLs Scraped This Session**: 4 (3 successful forum threads, 1 search aggregation)
**Total URLs Remaining**: ~26+ across all priorities
**Next Action**: Continue scraping remaining accessible URLs (Discord servers not scrapable, focus on accessible qhimm threads and technical documentation)

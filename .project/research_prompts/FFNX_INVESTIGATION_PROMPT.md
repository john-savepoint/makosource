# FFNx Deep-Dive Investigation Prompt

**Created**: 2025-11-20 10:09:15 JST (Thursday)
**Session ID**: 77121986-7211-4ef5-a043-d61a47fa6f66
**Purpose**: Investigate FFNx source code to understand texture replacement, font loading, and modding system mechanics

---

## Background Context

We are implementing Japanese text support in Final Fantasy VII PC (English Steam version) by extending FFNx graphics driver to support multiple font textures and extended character encoding (FA-FE page markers).

**Current Problem**: We've successfully dumped game textures using `save_textures = true`, which creates files like:
- `usfont_a_h_14.png`
- `usfont_a_l_14.png`
- `usfont_b_h_14.png`
- `usfont_b_l_14.png`

However, texture replacement mods (IRO files with these textures) are NOT working - textures placed in `mods/textures/` are not being loaded by the game.

---

## Critical Questions for FFNx Source Code Analysis

### 1. TEXTURE IDENTIFICATION & NAMING

**Question 1a**: In the FFNx source code, how exactly does FFNx identify which texture file to load when the game requests a specific texture?
- What is the lookup mechanism? (hash-based? filename-based? path-based?)
- When FFNx dumps textures with `save_textures = true`, what do the suffixes like `_14` represent? (compression level? detail level? mipmap level?)
- Are the dumped filenames (`usfont_a_h_14.png`) the same filenames that should be used for overrides, or different?

**Question 1b**: What is the relationship between internal texture identifiers in the game and the filenames in `mod_path`?
- Does FFNx use exact filename matching?
- Does it strip suffixes when looking for overrides?
- Are there any transformations applied to filenames during lookup?

**Question 1c**: When a user places a PNG file in `mods/textures/menu/usfont_a_h.png`, how does FFNx decide whether to load it?
- What are the exact matching rules?
- What file extensions are checked in what order?
- Are there any path transformations or normalizations?

---

### 2. MOD_PATH DIRECTORY STRUCTURE

**Question 2a**: The configuration shows `mod_path = "mods/textures"`. When FFNx loads a texture:
- Does it flatten the directory structure? (i.e., does `mods/textures/menu/usfont_a_h.png` get found as `mods/textures/usfont_a_h.png`?)
- Does it preserve the full game directory hierarchy? (i.e., must the path be `mods/textures/menu/usfont_a_h.png`?)
- Is the `menu/` subdirectory required, or is it optional?

**Question 2b**: When we dump textures and they appear in `mods/Textures/menu/`, what determines that `menu` subdirectory?
- Is this the internal game path structure being preserved?
- Should replacements use the same path structure?

---

### 3. TEXTURE FORMAT COMPATIBILITY

**Question 3a**: The FFNx.toml shows `mod_ext = ["dds", "png"]`. When FFNx looks for a texture override:
- Does it search for DDS first, then PNG? (in that order?)
- If both exist with the same name (one DDS, one PNG), which is loaded?
- Are there any quality/performance differences that would cause one to be preferred?

**Question 3b**: The dumped textures are PNG files. Are these in the correct format for modding?
- Should we be converting them to DDS instead?
- Is there any format conversion happening internally?
- Are there any color space or compression considerations?

---

### 4. FONT TEXTURE LOADING (CRITICAL FOR OUR GOAL)

**Question 4a**: How does FFNx currently handle font texture loading?
- Is font loading handled differently from other textures?
- Does the game request font textures by specific internal names?
- Where in the code does the font texture loading happen?

**Question 4b**: The current game only supports ONE font texture (USFONT_H.TEX). For Japanese support, we need to load SIX font textures (jafont_1.tex through jafont_6.tex).
- Where in FFNx would we need to implement multi-texture font loading?
- What structures store texture data?
- How would we handle texture switching based on character encoding (FA-FE page markers)?

**Question 4c**: Is there any special handling for USFONT textures specifically?
- Are they loaded at startup or on-demand?
- Are they cached?
- Can they be replaced/reloaded dynamically?

---

### 5. CHARACTER ENCODING & TEXT RENDERING

**Question 5a**: How does FFNx interact with FF7's text rendering system?
- Where does the character-to-glyph mapping happen?
- Does FFNx handle text decoding, or is that in the game exe?
- How are character indices converted to texture positions?

**Question 5b**: For Japanese support with FA-FE page markers:
- Would FFNx need to understand that FA XX means "look at texture 2, position XX"?
- Or is this handled by the game exe, and FFNx just needs to provide the texture data?
- Where would we intercept/modify character encoding logic?

**Question 5c**: When the game requests a character index like `0xFD00`:
- How does FFNx know this is a request for texture #5 (jafont_5), position 0?
- Is there existing code that maps indices to texture positions?
- Would we need to add new mapping logic?

---

### 6. TEXTURE OVERRIDE MECHANISM

**Question 6a**: The mod_path system should override game textures. Trace the code path:
- Where does the mod_path directory get scanned/indexed?
- How frequently is it checked? (startup only? per-frame? per-texture request?)
- What happens when a texture is requested - does FFNx first check mod_path before loading from game files?

**Question 6b**: We've been trying to make texture overrides work without success. Possible root causes:
- Is there initialization code that needs to be called for mod_path to work?
- Are there any configuration flags that need to be set?
- Is there any caching that prevents hot-reloading of modified textures?
- Are there any permission or path validation issues in the code?

**Question 6c**: The `override_path` configuration also exists (separate from `mod_path`). What's the difference?
- When is override_path checked vs mod_path?
- Could using override_path instead solve our texture loading issue?
- What are the intended use cases for each?

---

### 7. DEBUGGING & INSTRUMENTATION

**Question 7a**: Where in the FFNx code would we add logging to understand:
- When and which textures are being requested?
- What filenames are being searched in mod_path?
- What the actual lookup failure points are?
- Whether textures are being found but rejected for some reason?

**Question 7b**: Are there existing debug modes or logging in FFNx?
- What does `show_missing_textures = true` actually log and where?
- Are there other debug settings that would help?
- Where would we add instrumentation to trace the texture loading pipeline?

---

### 8. ARCHITECTURE & INTEGRATION POINTS

**Question 8a**: High-level FFNx architecture:
- What is the main rendering loop?
- Where does texture loading get triggered?
- How does the graphics driver interface with the game engine?
- What are the main components/modules involved in texture management?

**Question 8b**: For implementing Japanese font support:
- What would be the minimal changes needed to support multiple font textures?
- Where would font-specific code live?
- Are there existing patterns we can follow for multi-texture scenarios?
- Would this be in the FF7-specific code or generic graphics code?

**Question 8c**: The mod system:
- How does FFNx know it's in "modding mode"?
- What's the difference between a modded texture and an unmodded one in the code?
- Are there hooks or callbacks for mod loading?

---

### 9. SPECIFIC CODE LOCATIONS

**Question 9a**: Locate and explain these critical functions/areas:
- Where is `mod_path` read from the config?
- Where is the texture lookup/loading function?
- Where does the game request textures (the "demand" side)?
- Where does FFNx load from disk/memory (the "supply" side)?
- Where is texture format conversion handled?

**Question 9b**: For font-specific code:
- Find all mentions of "font" in the codebase
- Find all mentions of "USFONT"
- Find where USFONT textures are specially handled (if at all)
- Find where text rendering happens

**Question 9c**: For configuration:
- Where is FFNx.toml parsed?
- Where are mod_path and override_path used?
- What default values are set if config is missing?

---

### 10. KNOWN LIMITATIONS & DESIGN CONSTRAINTS

**Question 10a**: What are the current limitations of FFNx's texture override system?
- Is there a maximum number of textures that can be overridden?
- Are there any texture sizes/formats that can't be overridden?
- Are there memory constraints that would prevent loading 6 large font textures?

**Question 10b**: For multi-language support:
- How does FFNx currently handle different language versions?
- Are there hardcoded English assumptions anywhere?
- Would supporting Japanese require any special handling vs just "more textures"?

---

## What We Need From This Analysis

After investigating the FFNx codebase, please provide a report with:

1. **Texture Override Root Cause**: Why aren't our texture overrides working? What's broken or misconfigured?

2. **Correct File Structure**: The exact directory structure and file naming convention required for texture overrides to work

3. **Font Loading Architecture**: How font textures are currently loaded and where we'd need to modify code for multi-texture support

4. **Implementation Roadmap**: Step-by-step changes needed in FFNx to:
   - Fix texture override mechanism
   - Add support for multiple font textures
   - Implement FA-FE page marker support for character mapping

5. **Code Locations**: Exact file paths and function names for:
   - Texture lookup/loading
   - Font texture handling
   - Config parsing
   - Mod path management

6. **Debug Strategy**: How to instrument/log the texture loading pipeline to verify fixes work

7. **Quick Win**: If there's an obvious configuration or simple code fix to get texture overrides working immediately, identify it

---

## Success Criteria

This investigation is successful if we can:
1. Understand why current texture mods aren't loading
2. Get a simple red texture override working as proof of concept
3. Have a clear roadmap for implementing multi-texture Japanese font support
4. Know the exact code changes needed in FFNx to support our architecture

---

**Note**: We have access to complete FF7 Japanese assets (6 jafont textures, AF3DN.P driver, character mapping), so the research should focus on FFNx mechanics, not on figuring out WHAT needs to be replaced - we know that already.

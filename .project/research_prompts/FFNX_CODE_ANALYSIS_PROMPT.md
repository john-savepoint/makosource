# FFNx Codebase Analysis - Japanese Font Support Implementation

**Task**: Analyze FFNx source code to determine how to implement support for 6 font textures (instead of 1) to enable Japanese character rendering in Final Fantasy VII.

**Context**: We are replacing FF7's single USFONT texture system with a 6-texture system using extended character encoding (FA-FE page markers indicate which texture to use).

---

## PART 1: FONT TEXTURE SYSTEM ARCHITECTURE

### 1.1 Current Font Loading

- **How does FFNx currently load font textures?** Find the exact code path from game request to texture loaded in memory.
- **What file does it load?** (USFONT_H.TEX, USFONT_L.TEX, etc.)
- **Where is font texture loading triggered?** (startup? first use? on-demand?)
- **What data structures hold font texture data?** (class/struct names)
- **How are font textures stored in memory?** (raw pixels? GPU texture objects? cached?)
- **What class/module handles font texture management?** Provide exact class name and file path.

### 1.2 Current Character-to-Glyph Mapping

- **When the game requests a character (e.g., index 0x48 for 'H'), how does FFNx convert this to a glyph position in the texture?**
- **What formula is used?** (e.g., `pixel_x = (index % 16) * 64`)
- **Where is this conversion code?** Provide function name and file path.
- **Is this hardcoded or data-driven?** (lookup table? algorithm?)

### 1.3 Texture Memory Layout

- **How are glyph pixels stored in the font texture?** (grid layout? linear? compressed?)
- **What is the texture resolution?** (256x256? 512x512? 1024x1024?)
- **How many characters fit in one texture?** (256? 512?)
- **Is there any mipmapping or LOD system for fonts?** (multiple resolution versions?)

---

## PART 2: MULTI-TEXTURE IMPLEMENTATION STRATEGY

### 2.1 Architecture Changes Needed

- **To support 6 font textures instead of 1, what are the minimum code changes required?**
- **Should we:**
  - Load all 6 textures at startup, or
  - Load dynamically as needed, or
  - Pre-allocate memory for all 6?
  - What's recommended for performance?

### 2.2 Character Encoding Extension

- **Currently, indices are 0x00-0xFF (256 possibilities). With extended encoding (FA-FE page markers):**
  - `FA XX` = texture 2, position XX
  - `FB XX` = texture 3, position XX
  - `FC XX` = texture 4, position XX
  - `FD XX` = texture 5, position XX
  - `FE XX` = texture 6, position XX

- **Where in FFNx would this character encoding logic need to be implemented?**
- **Does FFNx currently handle text decoding, or is that in the game exe?**
- **If in game exe, at what point does FFNx receive the character indices?**

### 2.3 Glyph Selection Logic

- **For the extended encoding (FA-FE system), what code needs to change?**
- **New algorithm would be:**
  ```
  if (index >= 0xFA) {
    texture_index = index - 0xFA + 1;  // FA=1, FB=2, FC=3, FD=4, FE=5
    position = next_byte;
  } else {
    texture_index = 0;
    position = index;
  }
  ```
- **Where would this logic sit in the codebase?**
- **Can this be isolated to a single function, or scattered throughout?**

---

## PART 3: SPECIFIC CODE LOCATIONS NEEDED

### 3.1 Font Texture Loading

- **Find and provide:**
  - Exact function name that loads font textures
  - File path and line number
  - Parameter names and types
  - Return value/data structure

- **Example response format:**
  ```
  Function: LoadFontTexture()
  File: src/renderer/texture.cpp:245
  Parameters: const char* filename, FontTextureFormat format
  Returns: FontTexture* object
  ```

### 3.2 Character-to-Glyph Conversion

- **Find and provide:**
  - Function that converts character index to glyph position
  - Function that actually renders a glyph to screen
  - Any lookup tables or mapping structures
  - File paths and line numbers for all

### 3.3 Text Rendering Pipeline

- **What is the complete code path when FF7 renders text?**
  - Game exe passes text data to FFNx (how? what interface?)
  - FFNx receives character indices (in what format?)
  - FFNx converts indices to texture coordinates
  - FFNx renders glyphs to screen
  - Provide function names and file paths for each step

### 3.4 Font Configuration

- **Where in the code:**
  - Is the font texture filename specified? (hardcoded? config?)
  - Is the texture resolution defined?
  - Is the glyph size defined? (64x64? 32x32?)
  - Is the grid layout defined? (16x16? 8x8?)

---

## PART 4: IMPLEMENTATION RECOMMENDATIONS

### 4.1 Multi-Texture Font System Design

Given that we need to support 6 textures, **what architecture would you recommend?**

- **Option A: Array of textures**
  ```cpp
  FontTexture* fontTextures[6];
  fontTextures[0] = LoadFontTexture("usfont_h.tex");
  fontTextures[1] = LoadFontTexture("jafont_1.tex");
  fontTextures[2] = LoadFontTexture("jafont_2.tex");
  // etc.
  ```

- **Option B: Texture manager class**
  ```cpp
  class FontManager {
    std::map<int, FontTexture*> textures;
    FontTexture* GetTexture(int index);
  };
  ```

- **Option C: Other approach?** What would you recommend and why?

### 4.2 Character Encoding Handling

- **Should the FA-FE page marker logic be in FFNx, or should FFNx expect the game exe to already handle this?**
- **If in FFNx, where should it go?** (separate function? integrated with glyph lookup?)
- **What would the code look like?** (pseudocode or actual C++ example)

### 4.3 Minimal Code Changes

- **What is the absolute minimum number of functions that need to be modified or added?**
- **Can we make this change without breaking existing single-texture support?**
- **What are the backwards-compatibility considerations?**

### 4.4 Performance Considerations

- **Loading 6 textures instead of 1 - performance impact?**
- **GPU memory impact?** (assuming 1024x1024 textures)
- **Rendering performance when constantly switching between textures?**
- **Any optimization strategies?** (texture atlasing? pre-loading?)

---

## PART 5: CONFIGURATION & MOD SYSTEM

### 5.1 FFNx Configuration

- **How should the system know to load 6 font textures instead of 1?**
  - Add new config option? (e.g., `font_mode = "japanese"`)
  - Auto-detect based on file availability?
  - Hardcoded?
  - What would you recommend?

### 5.2 Texture File Organization

- **How should the 6 textures be organized?**
  - All in `mods/textures/` flat directory?
  - Subdirectory structure? (`mods/textures/fonts/jafont_1.tex`?)
  - Same directory as game files?
  - What's the cleanest design?

### 5.3 Filename Convention

- **What should the 6 texture files be named?**
  - `jafont_1.tex`, `jafont_2.tex`, ... (matching Japanese version)
  - `usfont_h.tex`, `font_extended_1.tex`, ... (descriptive)
  - Something else?
  - What convention would fit FFNx best?

---

## PART 6: INTEGRATION POINTS

### 6.1 Where to Hook In

- **Identify all the places where font texture loading happens and needs to be changed.**
- **Should these be centralized in one place, or scattered?**
- **What's the best architectural approach?**

### 6.2 Existing Systems to Work With

- **What existing FFNx systems can we leverage?**
  - Texture loading/management?
  - Character encoding handling?
  - Memory management?
  - Rendering pipeline?

### 6.3 What Needs to Be New

- **What functionality doesn't exist in FFNx and needs to be created?**
  - Multi-texture font system?
  - FA-FE page marker decoding?
  - Texture switching logic?

---

## PART 7: CONCRETE CODE EXAMPLES

For each of the following, provide actual code (not pseudocode) or exact references:

### 7.1 Current Font Loading

**Show the actual code that loads the current font texture.** Include:
- Complete function signature
- All key lines (not abbreviated)
- Comments on what each section does

### 7.2 Current Character Mapping

**Show the actual code that converts character index to glyph position.** Include:
- Complete function signature
- The exact formula/algorithm
- Any data structures involved

### 7.3 Current Text Rendering

**Show the actual code path when a character is rendered to screen.** Include:
- Function names in order
- File paths for each
- How data flows between functions

### 7.4 Proposed Multi-Texture Implementation

**Provide your recommended code for:**
- New/modified font loading function (6 textures)
- Character index to texture + position mapping (with FA-FE support)
- Glyph rendering with texture selection

---

## PART 8: RISK ASSESSMENT

- **What could break if we implement this change?**
- **Are there any systems that depend on font textures being a single texture?**
- **What backwards compatibility concerns exist?**
- **How do we avoid breaking existing single-texture font support for other languages?**

---

## PART 9: QUICK WINS

- **Is there a simple code change that would get us halfway there?**
- **Can we implement basic 2-texture support first as a proof of concept?**
- **What's the fastest way to test if our architecture is correct?**

---

## DELIVERABLES EXPECTED

Please provide:

1. **Architecture Design Document**
   - Recommended approach for multi-texture system
   - Data structures needed
   - Key functions involved

2. **Code Reference Guide**
   - File paths and function names for all relevant code
   - Line numbers for critical sections
   - Diagram or description of data flow

3. **Implementation Plan**
   - Step-by-step code changes needed
   - File paths for each change
   - Estimated complexity (simple/medium/complex)

4. **Code Examples**
   - Actual C++ code for multi-texture loading
   - Actual code for FA-FE page marker handling
   - Modified glyph lookup function

5. **Risk Mitigation**
   - Backwards compatibility strategy
   - Testing approach
   - Rollback plan if needed

6. **Configuration Recommendations**
   - How FFNx.toml should be extended
   - New config options needed
   - Default values

---

## Success Criteria

This analysis is successful if we have:

1. ✅ **Complete understanding** of how FFNx currently loads and renders font textures
2. ✅ **Clear architecture** for supporting 6 textures instead of 1
3. ✅ **Exact code locations** of everything that needs to change
4. ✅ **Concrete implementation plan** with actual C++ code examples
5. ✅ **Configuration strategy** for FFNx to support Japanese mode
6. ✅ **Risk assessment** and mitigation strategies
7. ✅ **Recommended approach** from someone who understands the FFNx codebase deeply

---

**This investigation should result in an implementation roadmap we can hand to a developer to execute, with no guessing or research needed during coding.**

# FFNx Mobile Porting Feasibility Analysis

**Created:** 2026-01-16 12:14:21 JST (Thursday)
**Session ID:** cd16c2ad-b2d1-400a-a6b5-314a1e6e6e08
**Author:** Claude Code
**Version:** 1.0.0

---

## Executive Summary

This document analyzes the technical feasibility of porting FFNx (the PC modding framework for Final Fantasy VII) to Android and iOS mobile platforms. The analysis covers architectural constraints, technical requirements, effort estimates, and partnership strategies with Square Enix.

**Key Findings:**
- FFNx does **not** currently work with Android/iOS versions of FF7
- Android port is **technically possible** but requires substantial effort (6-12 months)
- iOS port is **nearly impossible** without jailbreak due to Apple's security model
- Partnership with Square Enix would **fundamentally transform** feasibility

---

## Table of Contents

1. [Current FFNx Platform Support](#1-current-ffnx-platform-support)
2. [Android Porting Analysis](#2-android-porting-analysis)
3. [iOS Porting Analysis](#3-ios-porting-analysis)
4. [Comparative Feasibility Assessment](#4-comparative-feasibility-assessment)
5. [Partnership Model with Square Enix](#5-partnership-model-with-square-enix)
6. [Recommendations](#6-recommendations)
7. [References](#7-references)

---

## 1. Current FFNx Platform Support

### 1.1 What FFNx Is

FFNx is a Windows-only modding framework that acts as a graphics driver replacement for PC versions of Final Fantasy VII and VIII. It operates as:

- **Windows DLL shim** (`AF3DN.P`) that intercepts game function calls
- **Memory patcher** using Windows API (`VirtualProtect`, `CreateFile`)
- **Renderer** using BGFX with DirectX 11/12, Vulkan, and OpenGL backends
- **Mod loader** for texture replacements, audio overrides, and runtime patches

### 1.2 Supported Platforms

**Currently Supported:**
- FF7 Steam 2013 version (Windows)
- FF7 Original 1998 PC release (Windows)
- FF7 eStore version (Windows)
- FF8 Steam 2013 and original PC versions (Windows)

**NOT Supported:**
- Android FF7 mobile app
- iOS FF7 mobile app
- PlayStation versions (original or ports)
- Nintendo Switch version

### 1.3 Why Mobile Isn't Supported

FFNx's architecture is fundamentally incompatible with mobile platforms:

| FFNx Component | Windows Implementation | Mobile Equivalent |
|----------------|------------------------|-------------------|
| DLL injection | Replace `AF3DN.P` file | No equivalent mechanism |
| Memory patching | `VirtualProtect()` | Requires root/jailbreak |
| Graphics API | DirectX 11/12, Vulkan | OpenGL ES, Metal (iOS) |
| CPU architecture | x86/x86_64 assembly | ARM64/ARM32 assembly |
| File system hooks | Win32 API hooking | POSIX + content providers |

---

## 2. Android Porting Analysis

### 2.1 Technical Requirements

#### 2.1.1 Code Injection Mechanism

**Windows FFNx approach:**
```
Game loads AF3DN.P → FFNx.dll intercepts → Hooks installed
```

**Android equivalent requires:**
- **Rooted device** (mandatory for cross-app code injection)
- **Xposed Framework** or **Frida** for runtime hooking
- **LD_PRELOAD** or Zygote hooking to inject custom libraries
- **SELinux bypass** (Android's mandatory access control blocks injection)

#### 2.1.2 Architecture Translation Table

| Windows FFNx | Android Equivalent | Notes |
|--------------|-------------------|-------|
| x86 assembly hooks | ARM64/ARM32 assembly | Complete rewrite required |
| `VirtualProtect()` | `mprotect()` | Requires root permissions |
| Windows DLL injection | `LD_PRELOAD` or Zygote hook | Root required |
| BGFX DirectX/Vulkan | BGFX OpenGL ES / Vulkan | BGFX already supports this |
| Win32 file I/O | POSIX + Android APIs | Moderate porting effort |
| MSVC C++ runtime | NDK libc++ | Recompilation required |

#### 2.1.3 Reverse Engineering Requirements

The mobile FF7 app is a completely different binary:

- **Different compiler:** Likely Clang for ARM (vs MSVC for Windows)
- **Different memory layout:** All addresses are different
- **All hook points lost:** Every address in `externals_102_us.h` is meaningless
- **Must find from scratch:** 3-6 months of reverse engineering using IDA/Ghidra

**Example:**
```cpp
// Windows FF7 (externals_102_us.h)
uint32_t draw_character = 0x66E272;  // INVALID on Android

// Android equivalent - must be found via RE
uint32_t draw_character = ???;  // Unknown, requires disassembly
```

### 2.2 Development Steps

**Phase 1: Reverse Engineering (3-6 months)**
1. Decompile Android FF7 APK
2. Disassemble ARM64 binary with IDA Pro/Ghidra
3. Find equivalent functions for all hook points
4. Document memory layout and calling conventions

**Phase 2: Core Porting (2-3 months)**
1. Rewrite all Windows-specific code for POSIX
2. Port memory patching to `mprotect()`
3. Implement Frida/Xposed injection mechanism
4. Adapt BGFX for OpenGL ES/Vulkan mobile

**Phase 3: Integration (1-2 months)**
1. Create injection package (Magisk module or Xposed plugin)
2. Test on multiple Android versions
3. Debug architecture-specific issues
4. Optimize for mobile performance

### 2.3 Maintenance Burden

**Ongoing challenges:**
- **Every app update breaks addresses:** Square Enix updates FF7 mobile app → all hook addresses change → 1-2 weeks re-RE work
- **Android version fragmentation:** Must support Android 8-14+
- **Device compatibility:** Different ARM chips, GPU drivers
- **Root detection:** Square Enix might add anti-root checks

### 2.4 Realistic Assessment

```text
Android FFNx Port Feasibility: POSSIBLE

Requirements:
├── Rooted device (mandatory)
├── Complete RE of mobile binary (3-6 months work)
├── Rewrite all Windows-specific code (2-3 months)
├── Port BGFX/audio to Android NDK (1-2 months)
├── Testing and debugging (ongoing)
└── Maintenance for each app update (1-2 weeks per update)

Total estimated effort: 6-12 months for experienced RE team
User base: ~10% of Android users (rooted devices only)
Success probability: 60% (high technical risk)
```

---

## 3. iOS Porting Analysis

### 3.1 Why iOS Is Much Harder

#### 3.1.1 Code Signing Enforcement

iOS enforces strict code signing at the kernel level:

- **Every executable must be signed** by Apple or registered developer
- **No runtime code injection** into other apps
- **App sandboxing** with no inter-process access
- **Even jailbreak has limited capabilities** (Apple actively patches exploits)

#### 3.1.2 Injection Techniques Comparison

| Technique | Windows | Android | iOS |
|-----------|---------|---------|-----|
| DLL/dylib injection | ✅ Native | ⚠️ Root required | ❌ Blocked by code signing |
| LD_PRELOAD | ✅ Works | ⚠️ Root required | ❌ Doesn't exist |
| ptrace debugging | ✅ Works | ⚠️ Root required | ❌ Severely restricted |
| Runtime hooking | ✅ Native | ⚠️ Xposed/Frida | ❌ Substrate (jailbreak only) |

#### 3.1.3 Jailbreak Requirements

Even with jailbreak, significant barriers remain:

**What jailbreak enables:**
- MobileSubstrate/Substitute for function hooking
- Ability to decrypt and re-sign IPA files
- Access to app sandboxes

**What jailbreak does NOT solve:**
- **Stability:** iOS updates break jailbreaks frequently
- **User base:** Only ~5% of iOS users are jailbroken
- **Maintenance:** Apple actively patches jailbreak exploits
- **Complexity:** Must re-sign app, bypass detection, maintain compatibility

#### 3.1.4 Rendering Pipeline

Modern iOS uses Metal instead of OpenGL ES:

- BGFX supports Metal, but additional porting work required
- Shader translation from GLSL to Metal Shading Language (MSL)
- Different performance characteristics and debugging tools

### 3.2 Realistic Assessment

```text
iOS FFNx Port Feasibility: EXTREMELY DIFFICULT

Requirements:
├── Jailbreak (limits user base to ~5%)
├── Decrypt and re-sign FF7 IPA (legally gray area)
├── Complete RE of ARM64 binary (6-12 months)
├── Fight with code signing constantly
├── Each iOS update may break everything
└── Apple can patch jailbreak exploit at any time

Total estimated effort: 12-24 months
User base: ~5% of iOS users (jailbroken devices)
Success probability: 20% (very high technical and legal risk)
Long-term viability: LOW (Apple actively combats this)
```

---

## 4. Comparative Feasibility Assessment

### 4.1 Platform Comparison Matrix

| Factor | Windows (Current) | Android | iOS |
|--------|------------------|---------|-----|
| **Code injection** | Native (DLL) | Root required | Jailbreak required |
| **Memory patching** | `VirtualProtect` | `mprotect` + root | Nearly impossible |
| **App updates break it** | Rare (Steam stable) | Every update | Every update |
| **User base affected** | 100% of PC users | ~10% (rooted) | ~5% (jailbroken) |
| **Legal risk** | Low (modding accepted) | Medium (DMCA gray) | High (DMCA + EULA) |
| **Maintenance burden** | Low | High | Very high |
| **Development time** | ✅ Done | 6-12 months | 12-24 months |
| **Success probability** | ✅ 100% | ⚠️ 60% | ❌ 20% |
| **Long-term viability** | ✅ High | ⚠️ Medium | ❌ Low |

### 4.2 Codebase Reusability

**What can be reused from FFNx:**

✅ **Conceptual knowledge:**
- Japanese font encoding schemes (FA-FE page markers)
- Character width patching strategies
- Multi-page texture loading logic
- Rendering pipeline design

✅ **Some dependencies:**
- BGFX (already supports OpenGL ES, Vulkan, Metal)
- TOML configuration parsing
- Audio libraries (SoLoud supports mobile)

❌ **Cannot be reused:**
- All Windows-specific code (~60% of codebase)
- Memory address mappings (100% different)
- DLL injection mechanism
- Win32 API calls
- x86 assembly hooks

**Reality check:** You'd be writing a **new tool inspired by FFNx**, not porting it.

### 4.3 Effort vs Reward Analysis

| Platform | Development Effort | Potential Users | Effort/User Ratio |
|----------|-------------------|-----------------|-------------------|
| Windows FFNx | Already done | ~500K PC players | ✅ Best |
| Android port | 6-12 months | ~50K rooted users | ⚠️ Moderate |
| iOS port | 12-24 months | ~25K jailbroken users | ❌ Poor |

---

## 5. Partnership Model with Square Enix

### 5.1 How Partnership Changes Everything

| Challenge | Without SE | With SE Partnership |
|-----------|-----------|---------------------|
| **Reverse engineering** | Months of blind work | Symbol maps/documentation provided |
| **Address hunting** | Breaks every update | Stable hook points or official API |
| **Code signing (iOS)** | Jailbreak required | SE signs modified builds |
| **App store distribution** | Impossible | Official or sanctioned release |
| **Legal risk** | Gray area | Fully licensed |
| **Update breakage** | Constant firefighting | Coordinated releases |
| **User base** | 5-10% (rooted/jailbroken) | 100% (all users) |

### 5.2 What to Ask Square Enix For

#### Minimum Viable Partnership

1. **Stable hook points** - Documented function addresses or official plugin API
2. **Build notifications** - 48 hours advance notice before updates
3. **Debug symbols** - PDB/DWARF files to find functions trivially

#### Ideal Partnership

1. **Source access** - Read-only access to rendering/text code
2. **Official mod API** - Exposed interfaces for texture/font replacement
3. **Co-signed builds** - Your modifications distributed officially
4. **Shared testing** - Access to pre-release builds

### 5.3 Workflow Comparison

**Without partnership (hostile environment):**
```
SE releases update → Your tool breaks → 2-4 weeks of RE → Maybe fixed → Frustrated users
```

**With partnership (collaborative environment):**
```
SE prepares update → Notifies you 2 weeks early → You update in parallel →
Both release same day → Users never notice → Happy community
```

### 5.4 Precedent: Companies That Support Modding

**Successful examples:**

| Company | Game | Model |
|---------|------|-------|
| **Bethesda** | Skyrim | Official Creation Kit, Steam Workshop |
| **Microsoft** | Minecraft Bedrock | Official Add-on API, Marketplace |
| **Paradox** | Cities: Skylines | Designed for modding, stable APIs |
| **Meta** | Beat Saber | Initially hostile, now tolerates BMBF |

### 5.5 Value Proposition for Square Enix

**What you offer:**

| Your Contribution | Their Benefit |
|-------------------|---------------|
| Japanese text mod | Expands market to language learners globally |
| Quality enhancements | Free labor improving their product |
| Community engagement | Active modding → longer game lifespan |
| Bug testing | Find rendering bugs they'd miss |
| Localization work | Your encoding research helps other ports |

**The pitch:**

> "We're doing work that benefits your product and expands your market. Minimal cooperation from you (update notifications, stable APIs) dramatically reduces our maintenance burden and improves user experience.
>
> Your alternative is us constantly reverse engineering your updates anyway, with worse results for everyone."

### 5.6 How to Approach Square Enix

**Step 1: Build Leverage (Do This First)**
- ✅ Complete working PC FFNx demonstration
- ✅ Build active community (measure downloads, GitHub stars)
- ✅ Professional documentation showing expertise
- ✅ Metrics proving user engagement and value

**Step 2: Find the Right Contact**
- ❌ Not customer support
- ✅ Community manager
- ✅ Producer of FF7 mobile
- ✅ Localization team lead
- ✅ LinkedIn for Square Enix Mobile Division contacts
- ✅ Conferences (GDC, Tokyo Game Show) for face-to-face

**Step 3: Professional Proposal**

Include:
1. Working PC demonstration
2. User metrics (downloads, active users, community size)
3. Technical documentation proving professionalism
4. Clear scope of what you're asking for
5. What you're offering in return
6. Timeline and commitment level

**Step 4: Start Small**
- Don't ask for source access immediately
- Ask for: "Can we get 48 hours notice before mobile updates?"
- Build trust incrementally
- Demonstrate reliability

### 5.7 Expected Responses

| Response | Likelihood | Your Action |
|----------|------------|-------------|
| **Ignore** | 60% | Keep building, try again with more traction |
| **Polite decline** | 20% | Ask what would change their mind |
| **Cease & desist** | 5% | Consult lawyer, possibly comply |
| **Interest** | 10% | Professional follow-up, detailed proposal |
| **Active partnership** | 5% | You've won the lottery |

**Key insight:** Even a "no" today can become "yes" after you prove concept and build user base.

### 5.8 Feasibility With Partnership

```text
Android with SE Cooperation:
├── Initial development: 2-3 months (vs 6-12)
├── Per-update maintenance: Days (vs weeks)
├── User base: 100% of Android users (no root needed)
├── Distribution: Google Play Store possible
└── Long-term viability: HIGH

iOS with SE Cooperation:
├── Code signing: SOLVED (they sign it)
├── App Store: Possible as official feature
├── Maintenance: Same as Android
└── Long-term viability: HIGH
```

**The iOS problem completely disappears** if Square Enix ships your modifications as part of their official build.

---

## 6. Recommendations

### 6.1 For Hobbyist / Independent Developer

**Android:**
- ⚠️ **Proceed with caution** - High effort, moderate reward
- ✅ **Do:** Build PC version first, prove concept
- ✅ **Do:** Start with minimal Android prototype (1-2 months)
- ❌ **Don't:** Commit to full Android port without user demand

**iOS:**
- ❌ **Not recommended** - Extremely high effort, low reward
- ✅ **Alternative:** Focus energy on Android or PC improvements

### 6.2 For Team with Resources

**Android:**
- ✅ **Recommended** - Feasible with 6-12 month investment
- ✅ **Strategy:**
  1. Complete PC version
  2. Build community and prove value
  3. Approach Square Enix for partnership
  4. If partnership fails, evaluate Android standalone port

**iOS:**
- ⚠️ **Only with partnership** - Don't attempt without SE cooperation
- ❌ **Standalone port not viable**

### 6.3 Optimal Strategy

**Phase 1: Prove Value on PC (Current)**
- Complete FFNx Japanese text implementation
- Build active user community
- Document everything professionally
- Gather metrics (downloads, engagement)

**Phase 2: Approach Square Enix**
- Pitch partnership with professional proposal
- Request minimal cooperation (update notifications)
- Offer clear value proposition

**Phase 3A: If Partnership Succeeds**
- Port to Android/iOS with SE support (2-3 months)
- Official distribution channels
- 100% user base access
- Sustainable long-term

**Phase 3B: If Partnership Fails**
- Evaluate Android standalone port
- Only if community demand is high (>10K requests)
- Accept 10% user base limitation (rooted devices)
- Skip iOS entirely

### 6.4 Alternative Approaches

Instead of porting FFNx to mobile, consider:

**1. Cloud Gaming / Remote Play**
- Run FF7 PC with FFNx on home server
- Stream to mobile via Steam Link, Moonlight, Parsec
- ✅ Works today, no porting needed
- ✅ Full FFNx feature set
- ❌ Requires good internet connection

**2. Android Emulation**
- Use Android emulator on PC (BlueStacks, etc.)
- Attempt hooking in controlled environment
- ✅ Easier debugging than physical device
- ❌ Still requires RE work

**3. PSX Emulation on Mobile**
- ePSXe, DuckStation, etc. on Android
- Play Japanese PSX version with translation patches
- ✅ Much simpler, already works
- ✅ No root required
- ❌ Different game version (PSX vs PC)

**4. Petition Square Enix**
- Request official Japanese language option
- Text likely already in game files
- ✅ Zero development effort
- ❌ Low probability of success without leverage

---

## 7. References

### 7.1 Technical Documentation

- **FFNx Developer Guide:** `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/FFNX_DEVELOPER_GUIDE.md`
- **FFNx Directory Structure:** `/home/johnzealanddoyle/projects/ff7OG_japanese/docs/FFNX_DIRECTORY_STRUCTURE.md`
- **FFNx GitHub:** https://github.com/julianxhokaxhiu/FFNx

### 7.2 Mobile Reverse Engineering Resources

- **IDA Pro:** https://hex-rays.com/ida-pro/
- **Ghidra:** https://ghidra-sre.org/
- **Frida:** https://frida.re/ (dynamic instrumentation toolkit)
- **Xposed Framework:** https://repo.xposed.info/

### 7.3 Mobile Hooking Frameworks

- **Android Substrate:** http://www.cydiasubstrate.com/
- **LSPosed (Xposed):** https://github.com/LSPosed/LSPosed
- **Magisk:** https://github.com/topjohnwu/Magisk (root framework)

### 7.4 Precedent Examples

- **Beat Saber BMBF:** https://bmbf.dev/stable (Quest modding)
- **Skyrim Creation Kit:** https://www.creationkit.com/
- **Minecraft Add-ons:** https://learn.microsoft.com/en-us/minecraft/creator/

---

## Appendix A: Technical Architecture Diagrams

### A.1 Windows FFNx Architecture (Current)

```
┌─────────────────────────────────────────┐
│        FF7.exe (Game)                   │
│  (Original Game Code)                   │
└──────────────┬──────────────────────────┘
               │ Loads AF3DN.P
               ↓
┌─────────────────────────────────────────┐
│         FFNx.dll (Injected)             │
│  • Intercepts function calls            │
│  • VirtualProtect memory patching       │
│  • BGFX rendering (DX11/12/Vulkan)      │
└──────────────┬──────────────────────────┘
               │ Render commands
               ↓
┌─────────────────────────────────────────┐
│      GPU Driver (NVIDIA/AMD)            │
└─────────────────────────────────────────┘
```

### A.2 Android Port Architecture (Proposed)

```
┌─────────────────────────────────────────┐
│    FF7 Mobile APK (ARM64)               │
│  (Square Enix compiled binary)          │
└──────────────┬──────────────────────────┘
               │ Frida/Xposed injection
               ↓
┌─────────────────────────────────────────┐
│      FFNx-Android.so (Injected)         │
│  • Frida hooks on ARM64 functions       │
│  • mprotect() memory patching (root)    │
│  • BGFX rendering (OpenGL ES/Vulkan)    │
└──────────────┬──────────────────────────┘
               │ Render commands
               ↓
┌─────────────────────────────────────────┐
│      Android GPU Driver                 │
└─────────────────────────────────────────┘

Requires: Rooted device, Magisk/Xposed
```

### A.3 iOS Port Architecture (Jailbreak Only)

```
┌─────────────────────────────────────────┐
│    FF7 Mobile IPA (ARM64)               │
│  (Square Enix signed binary)            │
└──────────────┬──────────────────────────┘
               │ MobileSubstrate injection
               ↓
┌─────────────────────────────────────────┐
│      FFNx-iOS.dylib (Injected)          │
│  • Substrate hooks on ARM64             │
│  • Bypass code signing                  │
│  • BGFX rendering (Metal/Vulkan)        │
└──────────────┬──────────────────────────┘
               │ Render commands
               ↓
┌─────────────────────────────────────────┐
│      iOS GPU Driver (Metal)             │
└─────────────────────────────────────────┘

Requires: Jailbroken device, app re-signing
```

---

## Appendix B: Estimated Timeline

### B.1 Android Port (No Partnership)

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Research** | 1-2 months | RE tools setup, initial disassembly |
| **Reverse Engineering** | 3-6 months | All hook points documented |
| **Core Porting** | 2-3 months | FFNx-Android.so functional |
| **Integration** | 1-2 months | Magisk module or Xposed plugin |
| **Testing** | 1 month | Device compatibility verified |
| **Documentation** | 2 weeks | User guide, installation instructions |
| **Total** | **8-14 months** | Publicly released Android port |

### B.2 Android Port (With SE Partnership)

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Partnership negotiation** | 1-3 months | Signed agreement with SE |
| **Core Porting** | 1-2 months | FFNx-Android.so with SE APIs |
| **Integration** | 2-4 weeks | Official distribution package |
| **Testing** | 2-4 weeks | SE QA validation |
| **Total** | **3-5 months** | Official release via Play Store |

### B.3 iOS Port (Jailbreak Only - Not Recommended)

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Jailbreak Research** | 1-2 months | Identify compatible jailbreak |
| **IPA Decryption** | 2-4 weeks | Extract and re-sign FF7 IPA |
| **Reverse Engineering** | 6-12 months | All hook points documented |
| **Core Porting** | 3-4 months | FFNx-iOS.dylib functional |
| **MobileSubstrate Integration** | 1-2 months | Cydia package |
| **Testing** | 1-2 months | iOS version compatibility |
| **Total** | **12-24 months** | Publicly released (jailbreak only) |

---

**END OF DOCUMENT**

---

**Document Status:** Comprehensive Analysis Complete
**Next Steps:**
1. Continue PC FFNx development
2. Build community and gather metrics
3. Prepare Square Enix partnership proposal
4. Revisit mobile porting decision after PC success

**Session Artifacts:**
- Resume command appended to `/home/johnzealanddoyle/projects/tools/.project/resume/resume.txt`
- Full conversation context preserved for future reference

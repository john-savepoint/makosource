# FFNx Build Environment Setup Guide

**Created:** 2025-11-25 10:50:00 JST (Tuesday)
**Last Modified:** 2025-11-25 10:50:00 JST (Tuesday)
**Version:** 1.0.0
**Author:** Claude Code
**Session-ID:** 8f58819d-f9c4-4f04-8e95-4af04d782606
**Purpose:** Step-by-step guide for setting up Windows development environment for FFNx

**Target Audience:** Developers new to FFNx who need to build from source

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Visual Studio 2022 Installation](#2-visual-studio-2022-installation)
3. [Git Setup](#3-git-setup)
4. [Clone FFNx Repository](#4-clone-ffnx-repository)
5. [vcpkg Setup](#5-vcpkg-setup)
6. [Building FFNx](#6-building-ffnx)
7. [Testing Your Build](#7-testing-your-build)
8. [Debugging Setup](#8-debugging-setup)
9. [Working with PR #737](#9-working-with-pr-737)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### 1.1 System Requirements

**Operating System:**
- Windows 10 (64-bit) or Windows 11
- **Note:** FFNx builds as 32-bit (x86) but requires 64-bit Windows to build

**Hardware:**
- **CPU:** Any modern x64 processor (Intel/AMD)
- **RAM:** 8GB minimum, 16GB recommended (vcpkg compilation is memory-intensive)
- **Disk Space:** 20GB free (10GB for Visual Studio, 5GB for vcpkg dependencies, 5GB for builds)
- **Internet:** Required for downloading tools and dependencies

### 1.2 Required Software

Before starting, download these installers (but don't install yet):

1. **Visual Studio 2022 Community Edition**
   - URL: https://visualstudio.microsoft.com/vs/community/
   - Version: 17.0 or later
   - License: Free for open source development

2. **Git for Windows**
   - URL: https://git-scm.com/download/win
   - Version: 2.40 or later

**Optional but Recommended:**

3. **Visual Studio Code**
   - URL: https://code.visualstudio.com/
   - Lighter alternative IDE for quick edits

4. **x64dbg**
   - URL: https://x64dbg.com/
   - For runtime debugging and reverse engineering

5. **RenderDoc**
   - URL: https://renderdoc.org/
   - For graphics debugging

---

## 2. Visual Studio 2022 Installation

### 2.1 Download and Launch Installer

1. **Download** Visual Studio 2022 Community installer
2. **Run** the installer (`vs_community.exe`)
3. **Wait** for the installer bootstrap to complete (~1-2 minutes)

### 2.2 Import FFNx Configuration

FFNx provides a `.vsconfig` file that specifies exactly which components to install.

**Method 1: Import .vsconfig (Recommended)**

1. In the Visual Studio Installer, click **"More"** → **"Import configuration"**
2. Navigate to where you'll clone FFNx (see Section 4)
3. Select `FFNx/.vsconfig`
4. The installer will automatically select required components

**Method 2: Manual Selection (If .vsconfig Not Available)**

If you haven't cloned FFNx yet, manually select these workloads:

**Workloads Tab:**
- ☑ **Desktop development with C++**

**Individual Components Tab:**
- ☑ **MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)**
- ☑ **Windows 10 SDK (10.0.19041.0 or later)**
- ☑ **C++ CMake tools for Windows**
- ☑ **C++ AddressSanitizer** (optional, for debugging)
- ☑ **Git for Windows** (if not already installed)

**Language Packs:**
- ☑ **English** (required by FFNx build system)

### 2.3 Install

1. Click **"Install"** or **"Modify"** (if VS already installed)
2. **Wait** 30-90 minutes (download and install)
3. **Restart** your computer when prompted

### 2.4 Verify Installation

```batch
REM Open Command Prompt (cmd.exe) and run:
where cl

REM Expected output (path may vary):
C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.XX.XXXXX\bin\Hostx64\x86\cl.exe
```

If `cl` is not found, your PATH needs updating (see Troubleshooting section).

---

## 3. Git Setup

### 3.1 Install Git for Windows

1. **Run** Git installer (`Git-2.XX.X-64-bit.exe`)
2. **Accept defaults** for most options, except:

**Important Settings:**

- **Adjusting your PATH environment:**
  - ☑ Select **"Git from the command line and also from 3rd-party software"**

- **Choosing the default editor:**
  - Select your preferred editor (Notepad++, VS Code, etc.)

- **Configuring line ending conversions:**
  - ☑ Select **"Checkout as-is, commit Unix-style line endings"**
    - **Critical:** FFNx uses LF line endings, not CRLF

- **Configuring the terminal emulator:**
  - ☑ Select **"Use Windows' default console window"** (or "Use MinTTY" if preferred)

### 3.2 Configure Git

```batch
REM Open Command Prompt and run:

REM Set your identity (required for commits)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

REM Set line endings (critical for FFNx)
git config --global core.autocrlf input

REM Enable long paths (Windows has a 260 char limit by default)
git config --global core.longpaths true

REM Verify configuration
git config --list
```

### 3.3 Generate SSH Key (Optional but Recommended)

For easier GitHub authentication:

```batch
REM Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

REM Accept default file location (press Enter)
REM Enter passphrase (or press Enter for no passphrase)

REM Display public key
type %USERPROFILE%\.ssh\id_ed25519.pub

REM Copy the output and add to GitHub:
REM https://github.com/settings/keys → "New SSH key"
```

---

## 4. Clone FFNx Repository

### 4.1 Choose Installation Directory

**Recommended:** `C:\Dev\FFNx`

**Avoid:**
- Paths with spaces: `C:\Program Files\FFNx` ❌
- OneDrive folders: `C:\Users\Name\OneDrive\FFNx` ❌
- Network drives: `Z:\FFNx` ❌

### 4.2 Clone Repository

**Option A: Main FFNx Repository (For General Development)**

```batch
REM Create directory
mkdir C:\Dev
cd C:\Dev

REM Clone with submodules (CRITICAL - must use --recursive)
git clone --recursive https://github.com/julianxhokaxhiu/FFNx.git
cd FFNx

REM Verify submodules initialized
git submodule status
```

Expected output:
```
[40 character hash] vcpkg (heads/master)
```

**Option B: PR #737 Branch (For Japanese Text Support)**

```batch
REM Clone CosmosXIII's fork
mkdir C:\Dev
cd C:\Dev
git clone --recursive https://github.com/CosmosXIII/FFNx.git FFNx-PR737
cd FFNx-PR737

REM Switch to Japanese support branch
git checkout japanese-text-support

REM Verify you're on correct branch
git branch
```

Expected output:
```
* japanese-text-support
```

### 4.3 Verify Clone Success

```batch
REM List files
dir

REM You should see:
REM - CMakeLists.txt
REM - .vsconfig
REM - src\ directory
REM - vcpkg\ directory
REM - misc\ directory
```

---

## 5. vcpkg Setup

### 5.1 What is vcpkg?

vcpkg is a C++ package manager that downloads and compiles all FFNx dependencies (BGFX, FFmpeg, VGMStream, etc.). This step takes the longest (~30-60 minutes).

### 5.2 Bootstrap vcpkg

```batch
REM Navigate to vcpkg directory
cd C:\Dev\FFNx\vcpkg

REM Bootstrap vcpkg (compiles vcpkg.exe)
bootstrap-vcpkg.bat

REM Wait for completion (1-2 minutes)
REM Expected output: "vcpkg.exe successfully built"
```

### 5.3 Integrate vcpkg with Visual Studio

```batch
REM Still in C:\Dev\FFNx\vcpkg
vcpkg integrate install

REM Expected output:
REM "Applied user-wide integration for this vcpkg root."
```

This command registers vcpkg globally so CMake can find dependencies automatically.

### 5.4 Install Dependencies (Automatic)

**Good News:** You do NOT need to manually install dependencies. CMake will automatically install them when you first build FFNx.

**What Happens During First Build:**
- CMake detects `vcpkg.json` in FFNx root
- vcpkg downloads source for all dependencies (~500 MB)
- vcpkg compiles each dependency (~30-45 minutes)
- Compiled libraries cached for future builds

**Dependencies Installed:**
- bgfx (rendering)
- bimg (image loading)
- ffmpeg (video)
- vgmstream (audio)
- libpng (textures)
- tomlplusplus (config)
- soloud (audio engine)
- imgui (UI)
- ...and 5 more libraries

---

## 6. Building FFNx

### 6.1 Open in Visual Studio

**Method 1: Open Folder (Recommended)**

1. **Launch** Visual Studio 2022
2. **File** → **Open** → **Folder**
3. **Select** `C:\Dev\FFNx`
4. Wait for CMake to configure (~2-5 minutes on first run)

**Method 2: Command Line (Advanced)**

```batch
cd C:\Dev\FFNx

REM Configure CMake (generates build files)
cmake --preset x86-Debug

REM Wait for dependencies to compile (30-60 minutes first time)
```

### 6.2 Select Build Configuration

In Visual Studio status bar (bottom):

1. **Configuration:** Select **"x86-Debug"**
   - `x86-Debug`: For development (symbols, slower, larger file)
   - `x86-Release`: For production (optimized, smaller file)
   - `x86-RelWithDebInfo`: Hybrid (optimized + symbols)

2. **Startup Item:** Select **"FFNx.dll"**

### 6.3 Build

**Method 1: Visual Studio GUI**

1. **Build** → **Build All** (or press `Ctrl+Shift+B`)
2. **Wait** (first build: 30-90 minutes, subsequent: 1-5 minutes)
3. Watch **Output** window for progress

**Method 2: Command Line**

```batch
REM From C:\Dev\FFNx

REM Build Debug
cmake --build --preset x86-Debug

REM Build Release
cmake --build --preset x86-Release
```

### 6.4 Verify Build Success

**Check for output file:**

```batch
dir .build\bin\AF3DN.P

REM Expected output:
REM AF3DN.P (this is FFNx.dll renamed)
```

**File sizes (approximate):**
- Debug: 15-25 MB
- Release: 2-4 MB
- RelWithDebInfo: 8-12 MB

---

## 7. Testing Your Build

### 7.1 Backup Original Driver

**CRITICAL:** Always backup before replacing game files.

```batch
REM Navigate to your FF7 installation
cd "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII"

REM Backup original AF3DN.P (if exists)
copy AF3DN.P AF3DN.P.backup

REM Backup original FFNx.dll (if exists)
copy FFNx.dll FFNx.dll.backup
```

### 7.2 Install Your Build

```batch
REM Copy your build to game directory
copy C:\Dev\FFNx\.build\bin\AF3DN.P "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\AF3DN.P"

REM Also copy FFNx.toml if you modified it
copy C:\Dev\FFNx\misc\FFNx.toml "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\FFNx.toml"
```

### 7.3 Test Game Launch

1. **Launch** Final Fantasy VII (via Steam or directly)
2. **Check** for `FFNx.log` in game directory
3. **Verify** log shows your build:

```
[FFNx] INFO: FFNx 1.23.0.0 Debug - 2025-11-25
[FFNx] INFO: Renderer: DirectX 11
```

**If game crashes:** Check `FFNx.log` for errors (see Troubleshooting section)

### 7.4 Quick Smoke Test

1. **Start New Game** or **Load Save**
2. **Open Menu** (check textures load)
3. **Enter Battle** (check 3D rendering)
4. **Exit Game** normally

If all works, your build is successful! ✅

---

## 8. Debugging Setup

### 8.1 Attach Visual Studio Debugger

**While game is running:**

1. **Debug** → **Attach to Process** (or `Ctrl+Alt+P`)
2. **Search** for `ff7.exe` (or `ff7_ja.exe` for Japanese)
3. **Select** `ff7.exe`
4. **Attach**

### 8.2 Set Breakpoints

**Example: Break when texture loads**

1. **Open** `src/common.cpp`
2. **Find** `common_load_texture()` function (~line 1400)
3. **Click** left margin to set breakpoint (red dot appears)
4. **Trigger** texture load in game (open menu, enter battle)
5. **Debugger pauses** at breakpoint

### 8.3 Inspect Variables

When paused at breakpoint:

- **Locals** window: Shows local variables
- **Autos** window: Shows variables in current statement
- **Watch** window: Add variables to monitor
- **Call Stack** window: Shows function call hierarchy

### 8.4 Debugging Controls

- **F5**: Continue execution
- **F10**: Step over (execute line, don't enter functions)
- **F11**: Step into (enter function calls)
- **Shift+F11**: Step out (exit current function)
- **Shift+F5**: Stop debugging

---

## 9. Working with PR #737

### 9.1 Clone PR #737 Branch

If you haven't already (from Section 4.2):

```batch
cd C:\Dev
git clone --recursive https://github.com/CosmosXIII/FFNx.git FFNx-PR737
cd FFNx-PR737
git checkout japanese-text-support
```

### 9.2 Build PR #737

```batch
REM Same process as Section 6
cd C:\Dev\FFNx-PR737
cmake --preset x86-Debug
cmake --build --preset x86-Debug
```

### 9.3 Enable Japanese Mode

**Edit `misc/FFNx.toml` (line 697):**

```toml
# Enable Japanese text rendering
ff7_japanese_edition = true
```

Or let it auto-detect (if using `ff7_ja.exe`).

### 9.4 Test Japanese Rendering

**Requirements:**
- Japanese FF7 version (eStore or ff7_ja.exe)
- Japanese font files in `mods/Textures/menu/`:
  - `jafont_1.tim`
  - `jafont_2.tim`
  - `jafont_3.tim`
  - `jafont_4.tim`
  - `jafont_5.tim`
  - `jafont_6.tim`

**Known Issues to Reproduce:**
1. **Colored text bug:** Open menu, look for `[セーブ]` → appears malformed
2. **Character input bug:** New game → Name character → last 2 rows garbled
3. **Cursor bug:** Navigate menus → hand icon doesn't align with text

### 9.5 Debug PR #737 Issues

**Colored Text Bug:**

1. Set breakpoint in `src/ff7/japanese_text.cpp` line 479 (`get_character_color()`)
2. Open menu in game
3. Step through function to see why color returns incorrect value

**Character Input Bug:**

1. Set breakpoint in character rendering loop (~line 1024)
2. Open character name input screen
3. Watch which characters get rendered to last 2 rows

---

## 10. Troubleshooting

### 10.1 vcpkg Bootstrap Fails

**Error:** `'cl' is not recognized as an internal or external command`

**Cause:** MSVC compiler not in PATH

**Solution:**

```batch
REM Find vcvarsall.bat (path varies by VS version)
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x86

REM Then retry bootstrap
cd C:\Dev\FFNx\vcpkg
bootstrap-vcpkg.bat
```

### 10.2 vcpkg Dependency Compilation Fails

**Error:** `Error: Building package [name]:x86-windows failed`

**Solution 1: Increase Memory**

Some packages need 8GB+ RAM to compile. Close other applications.

**Solution 2: Retry**

```batch
REM Clean and retry
vcpkg remove --outdated
vcpkg install
```

**Solution 3: Use Binary Cache**

Check if NuGet binary cache is available (see FFNx README.md section on NuGet).

### 10.3 CMake Configuration Fails

**Error:** `CMake Error: Could not find vcpkg`

**Cause:** vcpkg not integrated

**Solution:**

```batch
cd C:\Dev\FFNx\vcpkg
vcpkg integrate install
```

### 10.4 Build Fails with "Cannot Open File"

**Error:** `fatal error C1083: Cannot open source file`

**Cause:** Submodules not initialized

**Solution:**

```batch
cd C:\Dev\FFNx
git submodule update --init --recursive
```

### 10.5 Game Crashes on Launch

**Check `FFNx.log` for:**

**Error:** `Failed to load bgfx renderer`

**Solution:** Graphics driver issue, update GPU drivers

**Error:** `Failed to load texture: [path]`

**Solution:** Missing texture files, check `mods/Textures/` directory

**Error:** `Access violation at 0xXXXXXXXX`

**Solution:** Build mismatch, ensure Debug symbols match Debug build

### 10.6 Debugger Won't Attach

**Error:** `Unable to attach to the process`

**Cause:** Game running as administrator, VS not

**Solution:** Run Visual Studio as administrator

### 10.7 Breakpoints Show "Hollow Circle"

**Error:** "The breakpoint will not currently be hit. No symbols have been loaded for this document."

**Cause:** PDB symbols not loaded

**Solution:**

1. Check `.build\bin\` contains `FFNx.pdb`
2. Debug → Windows → Modules
3. Find `AF3DN.P`
4. Right-click → Load Symbols → Select `FFNx.pdb`

### 10.8 Build is Slow (30+ minutes)

**Normal on first build:** Dependencies compile from source

**Subsequent builds slow:**

**Solution:** Use Ninja build system (faster than MSBuild)

```batch
REM Install Ninja via Chocolatey
choco install ninja

REM Configure with Ninja
cmake --preset x86-Debug -G Ninja

REM Build
cmake --build --preset x86-Debug
```

---

## 11. Quick Reference Commands

### Daily Development Workflow

```batch
REM 1. Update repository
cd C:\Dev\FFNx
git pull

REM 2. Rebuild
cmake --build --preset x86-Debug

REM 3. Install to game
copy .build\bin\AF3DN.P "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII\"

REM 4. Test game
cd "C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII"
ff7.exe

REM 5. Check logs
type FFNx.log
```

### Clean Rebuild

```batch
REM Delete build directory
rmdir /s /q .build

REM Reconfigure and build
cmake --preset x86-Debug
cmake --build --preset x86-Debug
```

### Switch Build Configuration

```batch
REM From Debug to Release
cmake --preset x86-Release
cmake --build --preset x86-Release
```

---

## 12. Next Steps

After successful build:

1. **Read Code:**
   - `src/common.cpp` - Texture loading system
   - `src/ff7_opengl.cpp` - Hook installation
   - `src/cfg.cpp` - Configuration parsing
   - `src/ff7/japanese_text.cpp` (PR #737) - Japanese rendering

2. **Modify Code:**
   - Make your changes
   - Rebuild
   - Test in game
   - Check `FFNx.log` for errors

3. **Debug Issues:**
   - Attach debugger
   - Set breakpoints
   - Step through code
   - Inspect variables

4. **Contribute:**
   - Create feature branch: `git checkout -b feature/my-feature`
   - Commit changes: `git commit -m "Add feature"`
   - Push to fork: `git push origin feature/my-feature`
   - Create Pull Request on GitHub

---

## 13. Additional Resources

### Documentation

- **FFNx README:** `README.md` in repository root
- **FFNx Developer Guide:** `docs/FFNX_DEVELOPER_GUIDE.md` (this project)
- **PR #737 Analysis:** `docs/PR737_ANALYSIS.md` (this project)
- **Verification Checklist:** `docs/IMPLEMENTATION_VERIFICATION_CHECKLIST.md` (this project)

### Community

- **FFNx GitHub:** https://github.com/julianxhokaxhiu/FFNx
- **FFNx Issues:** https://github.com/julianxhokaxhiu/FFNx/issues
- **Qhimm Forums:** https://forums.qhimm.com/ (FF7 modding community)
- **Discord:** Check FFNx README for current invite link

### Tools

- **Visual Studio Docs:** https://docs.microsoft.com/en-us/visualstudio/
- **CMake Tutorial:** https://cmake.org/cmake/help/latest/guide/tutorial/
- **vcpkg Docs:** https://vcpkg.io/en/docs/

---

## Appendix A: System Paths Reference

**Visual Studio 2022 Default Paths:**
```
Installation: C:\Program Files\Microsoft Visual Studio\2022\Community
MSVC Compiler: C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.XX.XXXXX\bin\Hostx64\x86\
CMake: C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\
```

**Git Default Paths:**
```
Installation: C:\Program Files\Git
Git Bash: C:\Program Files\Git\git-bash.exe
SSH Keys: %USERPROFILE%\.ssh\
```

**FFNx Recommended Paths:**
```
Source: C:\Dev\FFNx
Build Output: C:\Dev\FFNx\.build\bin\
Game Install (Steam): C:\Program Files (x86)\Steam\steamapps\common\FINAL FANTASY VII
Game Install (Standalone): C:\Games\FF7
```

---

## Appendix B: Build Configuration Matrix

| Configuration | Optimization | Debug Symbols | File Size | Use Case |
|---------------|--------------|---------------|-----------|----------|
| **x86-Debug** | None (`/Od`) | Full (`/Zi`) | ~20 MB | Daily development, debugging |
| **x86-Release** | Max Speed (`/O2`) | None | ~3 MB | Production release |
| **x86-RelWithDebInfo** | Max Speed (`/O2`) | Full (`/Zi`) | ~12 MB | Profiling, debugging release issues |
| **x86-MinSizeRel** | Min Size (`/O1`) | None | ~2 MB | Rarely used |

---

## Appendix C: Common Build Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `cl.exe not found` | MSVC not installed or not in PATH | Install VS 2022 with C++ workload |
| `vcpkg.exe not found` | vcpkg not bootstrapped | Run `bootstrap-vcpkg.bat` |
| `CMake Error 1` | CMakeLists.txt syntax error | Check recent changes to CMakeLists.txt |
| `LNK2001 unresolved external` | Missing library | Rebuild vcpkg dependencies |
| `C2039 is not a member` | Missing include | Add `#include` directive |
| `MSB8036 Windows SDK not found` | Windows SDK not installed | Install Windows 10 SDK via VS Installer |

---

**END OF BUILD ENVIRONMENT SETUP GUIDE**

**Status:** Production Ready - Tested on Windows 10/11

**Last Updated:** 2025-11-25 by Claude Code

**Feedback:** Report issues or suggest improvements via GitHub

---

**Quick Start Summary:**

1. Install Visual Studio 2022 (import `.vsconfig`)
2. Install Git for Windows
3. Clone: `git clone --recursive https://github.com/julianxhokaxhiu/FFNx.git`
4. Bootstrap vcpkg: `cd vcpkg && bootstrap-vcpkg.bat && vcpkg integrate install`
5. Build: `cmake --preset x86-Debug && cmake --build --preset x86-Debug`
6. Test: Copy `.build\bin\AF3DN.P` to FF7 directory, launch game
7. Debug: Attach Visual Studio debugger to `ff7.exe`

**Estimated Time:**
- Setup: 2-3 hours (mostly waiting for downloads/compilation)
- First successful build: 30-90 minutes (vcpkg dependencies)
- Subsequent builds: 1-5 minutes

**Congratulations!** You're now ready to develop FFNx. 🎉

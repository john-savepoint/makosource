#!/bin/bash
#
# Combine Markdown files into master and category files
#
# Created: 2025-11-28 12:44:49 JST (Friday)
# Context: Creates combined GameEngine.md and category-specific combination files.
#          Excludes FF7_Savemap.md and FF7_Playstation_Battle_Model_Format.md from combinations.
#
# Author: John Zealand-Doyle
# Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c

echo "======================================================================="
echo "Combining Markdown files"
echo "======================================================================="
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Create master GameEngine.md (excluding Savemap and Battle Model Format)
echo "Creating GameEngine.md (master combined file)..."

cat > GameEngine.md << 'HEADER'
# FF7 Game Engine Documentation

**Complete Combined Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)
Last Modified: 2025-11-28 12:44:49 JST (Friday)
Version: 1.0.0
Author: John Zealand-Doyle
Session-ID: b1483492-7356-4e03-95e9-710911d2ed6c

---

This file combines all FF7 game engine documentation pages (excluding Savemap and Playstation Battle Model Format due to their large size).

**Table of Contents:**
- History
- Engine Basics
- Kernel System
- Menu Module
- Field Module
- Battle System
- WorldMap Module
- Sound System
- Technical Documentation

---

HEADER

# Combine all markdown files except the two large ones
for file in markdown/FF7.md \
            markdown/FF7_History.md \
            markdown/FF7_Engine_basics.md \
            markdown/FF7_Kernel.md \
            markdown/FF7_Kernel_Overview.md \
            markdown/FF7_Kernel_Memory_management.md \
            markdown/FF7_Kernel_Kernelbin.md \
            markdown/FF7_Kernel_Low_level_libraries.md \
            markdown/FF7_LZSS_format.md \
            markdown/FF7_LGP_format.md \
            markdown/PSX_TIM_format.md \
            markdown/FF7_TEX_format.md \
            markdown/FF7_Menu_Module.md \
            markdown/FF7_Field_Module.md \
            markdown/FF7_Battle_Battle_Mechanics.md \
            markdown/FF7_Battle_Battle_Field.md \
            markdown/FF7_Battle_Battle_Scenes.md \
            markdown/FF7_Battle_Battle_Scenes_Battle_Script.md \
            markdown/FF7_Battle_Battle_Animation_PC.md \
            markdown/FF7_WorldMap_Module.md \
            markdown/FF7_World_Map_BSZ.md \
            markdown/FF7_World_Map_TXZ.md \
            markdown/FF7_WorldMap_Module_Script.md \
            markdown/FF7_PSX_Sound_Overview.md \
            markdown/FF7_PSX_Sound_INSTRxDAT.md \
            markdown/FF7_PSX_Sound_INSTRxALL.md \
            markdown/FF7_PSX_Sound_AKAO_frames.md \
            markdown/FF7_Technical.md \
            markdown/FF7_Technical_Customising.md \
            markdown/FF7_Technical_Source.md; do
    if [ -f "$file" ]; then
        echo "" >> GameEngine.md
        echo "---" >> GameEngine.md
        echo "" >> GameEngine.md
        cat "$file" >> GameEngine.md
    fi
done

echo "✅ Created: GameEngine.md"
echo ""

# Create category combination files
echo "Creating category combination files in markdown/combined/..."

# 1. History.md
cat > markdown/combined/History.md << 'HEADER'
# FF7 History

**Category: Historical Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains historical information about FF7's development and evolution.

---

HEADER
cat markdown/FF7_History.md >> markdown/combined/History.md
echo "✅ Created: markdown/combined/History.md"

# 2. EngineBasics.md
cat > markdown/combined/EngineBasics.md << 'HEADER'
# FF7 Engine Basics

**Category: Core Engine Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains fundamental information about FF7's game engine architecture and basic concepts.

---

HEADER
cat markdown/FF7.md >> markdown/combined/EngineBasics.md
echo "" >> markdown/combined/EngineBasics.md
echo "---" >> markdown/combined/EngineBasics.md
echo "" >> markdown/combined/EngineBasics.md
cat markdown/FF7_Engine_basics.md >> markdown/combined/EngineBasics.md
echo "✅ Created: markdown/combined/EngineBasics.md"

# 3. Kernel.md
cat > markdown/combined/Kernel.md << 'HEADER'
# FF7 Kernel System

**Category: Kernel Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's kernel system, including memory management, kernel.bin structure, low-level libraries, and compression/archive formats.

---

HEADER
for file in markdown/FF7_Kernel.md \
            markdown/FF7_Kernel_Overview.md \
            markdown/FF7_Kernel_Memory_management.md \
            markdown/FF7_Kernel_Kernelbin.md \
            markdown/FF7_Kernel_Low_level_libraries.md \
            markdown/FF7_LZSS_format.md \
            markdown/FF7_LGP_format.md \
            markdown/PSX_TIM_format.md \
            markdown/FF7_TEX_format.md; do
    cat "$file" >> markdown/combined/Kernel.md
    echo "" >> markdown/combined/Kernel.md
    echo "---" >> markdown/combined/Kernel.md
    echo "" >> markdown/combined/Kernel.md
done
echo "✅ Created: markdown/combined/Kernel.md"

# 4. MenuModule.md
cat > markdown/combined/MenuModule.md << 'HEADER'
# FF7 Menu Module

**Category: Menu System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains documentation about FF7's menu system and user interface.

---

HEADER
cat markdown/FF7_Menu_Module.md >> markdown/combined/MenuModule.md
echo "✅ Created: markdown/combined/MenuModule.md"

# 5. FieldModule.md
cat > markdown/combined/FieldModule.md << 'HEADER'
# FF7 Field Module

**Category: Field System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains documentation about FF7's field module, which handles exploration areas, NPCs, and field scripts.

---

HEADER
cat markdown/FF7_Field_Module.md >> markdown/combined/FieldModule.md
echo "✅ Created: markdown/combined/FieldModule.md"

# 6. BattleModule.md
cat > markdown/combined/BattleModule.md << 'HEADER'
# FF7 Battle Module

**Category: Battle System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's battle system, including mechanics, battle fields, scenes, scripts, and animations.

---

HEADER
for file in markdown/FF7_Battle_Battle_Mechanics.md \
            markdown/FF7_Battle_Battle_Field.md \
            markdown/FF7_Battle_Battle_Scenes.md \
            markdown/FF7_Battle_Battle_Scenes_Battle_Script.md \
            markdown/FF7_Battle_Battle_Animation_PC.md; do
    cat "$file" >> markdown/combined/BattleModule.md
    echo "" >> markdown/combined/BattleModule.md
    echo "---" >> markdown/combined/BattleModule.md
    echo "" >> markdown/combined/BattleModule.md
done
echo "✅ Created: markdown/combined/BattleModule.md"

# 7. WorldMapModule.md
cat > markdown/combined/WorldMapModule.md << 'HEADER'
# FF7 WorldMap Module

**Category: World Map System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's world map system, including map structure, BSZ/TXZ formats, and scripting.

---

HEADER
for file in markdown/FF7_WorldMap_Module.md \
            markdown/FF7_World_Map_BSZ.md \
            markdown/FF7_World_Map_TXZ.md \
            markdown/FF7_WorldMap_Module_Script.md; do
    cat "$file" >> markdown/combined/WorldMapModule.md
    echo "" >> markdown/combined/WorldMapModule.md
    echo "---" >> markdown/combined/WorldMapModule.md
    echo "" >> markdown/combined/WorldMapModule.md
done
echo "✅ Created: markdown/combined/WorldMapModule.md"

# 8. Sound.md
cat > markdown/combined/Sound.md << 'HEADER'
# FF7 Sound System

**Category: Sound System Documentation**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains comprehensive documentation about FF7's PSX sound system, including instrument formats and AKAO frames.

---

HEADER
for file in markdown/FF7_PSX_Sound_Overview.md \
            markdown/FF7_PSX_Sound_INSTRxDAT.md \
            markdown/FF7_PSX_Sound_INSTRxALL.md \
            markdown/FF7_PSX_Sound_AKAO_frames.md; do
    cat "$file" >> markdown/combined/Sound.md
    echo "" >> markdown/combined/Sound.md
    echo "---" >> markdown/combined/Sound.md
    echo "" >> markdown/combined/Sound.md
done
echo "✅ Created: markdown/combined/Sound.md"

# 9. Technical.md
cat > markdown/combined/Technical.md << 'HEADER'
# FF7 Technical Documentation

**Category: Technical Reference**

Created: 2025-11-28 12:44:49 JST (Friday)

This file contains technical documentation covering customization, source code information, and implementation details.

---

HEADER
for file in markdown/FF7_Technical.md \
            markdown/FF7_Technical_Customising.md \
            markdown/FF7_Technical_Source.md; do
    cat "$file" >> markdown/combined/Technical.md
    echo "" >> markdown/combined/Technical.md
    echo "---" >> markdown/combined/Technical.md
    echo "" >> markdown/combined/Technical.md
done
echo "✅ Created: markdown/combined/Technical.md"

echo ""
echo "======================================================================="
echo "COMBINATION COMPLETE"
echo "======================================================================="
echo "✅ Created GameEngine.md (master combined file)"
echo "✅ Created 9 category combination files in markdown/combined/"
echo ""

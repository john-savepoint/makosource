<!--
MERGE METADATA
Created: 2025-11-29
Original: FF7_Battle_Battle_Animation_PC.md (912 lines)
Major section: 06_BATTLE_MODULE.md
Merge decision: NO EXTRACTION PERFORMED
Reason: Individual file contains comprehensive battle animation format documentation
Analysis: Major section does not contain additional PC animation format details
Status: COMPLETE - Restructured for clarity 2025-11-29 16:15 JST
Restructure: Improved organization, fixed typos, enhanced readability
-->

# FF7 Battle Animation Format (PC)

- [FF7 Battle Animation Format (PC)](#ff7-battle-animation-format-pc)
  - [Overview](#overview)
  - [1. File Structure](#1-file-structure)
  - [2. Data Structures](#2-data-structures)
  - [3. Decoding Algorithms](#3-decoding-algorithms)
  - [4. Implementation Guide](#4-implementation-guide)
  - [5. Alternative Implementations](#5-alternative-implementations)
  - [Appendix A: Quick Reference](#appendix-a-quick-reference)
  - [Appendix B: Known Issues](#appendix-b-known-issues)

## Overview

This document describes the Final Fantasy VII battle animation file format for PC, reverse-engineered by **L. Spiro**. Contributions by **Halkun** (wiki conversion) and **Borde** (additional notes).

### What This Document Covers

- Binary file structure for battle animations
- Data structures for storing skeletal animations
- Compression algorithms for rotation data
- Complete C++ implementation with assembly optimizations
- Theoretical background on the compression scheme

### File Format Basics

Battle animation files contain skeletal animation data for character models. Each file stores:
- Multiple animations for a single character
- Per-frame bone rotations and positions
- Compressed delta encoding for subsequent frames
- Special animation markers for scripted events

---

## 1. File Structure

### 1.1 Animation File Layout

Battle animation files begin with a **DWORD** indicating the total number of animations. This count includes both regular animations and special animation markers (non-animation data such as script keys or damage number triggers).

**Example**: Cloud's battle animation file (`rtda`) contains 94 (0x5E) animations.

To navigate between animations, start reading at offset `0x04` and parse each animation header sequentially.

### 1.2 File Header Format

Each animation begins with a 12-byte header followed by animation data.

---

## 2. Data Structures

### 2.1 FF7FrameHeader

**Purpose**: Main header for each animation in the file.

**Structure** (12 bytes):

```c
typedef struct FF7FrameHeader {
    DWORD       dwBones;        // Bones in model + 1 (weapon animations always 1). Offset: 0x00
                                // NOTE: Unreliable - use skeleton file bone count instead.
    DWORD       dwFrames;       // Frame count in this animation. Offset: 0x04
    DWORD       dwChunkSize;    // Size of animation data in bytes. Offset: 0x08
} * PFF7FrameHeader;            // Total size: 12 bytes
```

#### Special Animation Chunks

When `dwChunkSize < 11`, this is a special (non-animation) data chunk. Skip it by advancing 8 bytes past the header.

#### Navigation Example

To skip to animation index `iTarget`:

```c
FF7FrameHeader  fhHeader;
DWORD           dwBytesRead;
for ( int I = 0; I < iTarget; I++ ) {
    if ( !ReadFile( hFile,
        &fhHeader, sizeof( fhHeader ),
        &dwBytesRead, NULL ) ) {

    CloseHandle( hFile );
    return false;
    }
    if ( fhHeader.dwChunkSize < 11 ) {  // Special chunk
        if ( SetFilePointer( hFile, 8, NULL, FILE_CURRENT ) ==
        INVALID_SET_FILE_POINTER ) {
            CloseHandle( hFile );
            return false;
        }
        continue;
    }
    // Skip this animation (size = dwChunkSize)
    if ( SetFilePointer( hFile, fhHeader.dwChunkSize, NULL,
    FILE_CURRENT ) == INVALID_SET_FILE_POINTER ) {
        CloseHandle( hFile );
        return false;
    }
}
// Now at the target animation
if ( !ReadFile( hFile,
    &fhHeader, sizeof( fhHeader ),
    &dwBytesRead, NULL ) ) {

    CloseHandle( hFile );
    return false;
}
BYTE * pbBuffer = new BYTE[fhHeader.dwChunkSize];
// pbBuffer now holds animation data including FF7FrameMiniHeader
```

### 2.2 FF7FrameMiniHeader

**Purpose**: Per-animation metadata embedded at the start of each animation's data chunk.

**Structure** (5 bytes):

```c
typedef struct FF7FrameMiniHeader {
    //SHORT     sBones; // Originally thought to be bone count
    SHORT       sFrames;// Apparent frame count (may exceed dwFrames). Offset: 0x00
    SHORT       sSize;  // Size of animation data in bytes. Offset: 0x02
    BYTE        bKey;   // Precision key for rotation encoding (0, 2, or 4). Offset: 0x04
} * PFF7FrameMiniHeader;    // Total size: 5 bytes
```

#### Field Discrepancy Notes

**Field Naming Issue**: The field named `sBones` should probably be `sFrames`, as it appears to hold a frame counter.

**Reliability**: `sFrames` and `dwFrames` rarely match.
- `dwFrames` is conservative—guarantees at least that many frames exist
- `sFrames` sometimes exceeds actual frame count
- **Determine actual frame count by parsing the entire chunk**

**Known Corruption**: Animation 15 in RSAA (playable frog) lacks the `sFrames` field entirely:
- `sSize` appears at offset 0x00
- `bKey` appears at offset 0x02
- FF7 cannot handle this animation (likely corrupted)

### 2.3 bKey: The Precision Field

**Purpose**: Controls rotation data bit depth and compression level.

#### Valid Values

| bKey Value | Uncompressed Bits | Bit Range | Precision Loss |
|------------|-------------------|-----------|----------------|
| 0          | 12                | 0-4095    | None           |
| 2          | 10                | 0-1023    | Low            |
| 4          | 8                 | 0-255     | Moderate       |

#### How It Works

1. **Storage**: Rotations stored using `(12 - bKey)` bits
2. **Decoding**: Shift left by `bKey` to restore 12-bit range
   - Example: 8-bit value `0xFF` (255) becomes `0xFF0` (4080) after `<< 4`
3. **Trade-off**: Lower precision reduces file size; acceptable for delta-encoded rotations

**Why Lower Precision Works**: Most skeletal animations change by small increments between frames. Large rotations (e.g., spinning blades on Aero Combatant) are round numbers (90°, 180°) that lose no meaningful precision even at 8-bit depth.

### 2.4 FF7ShortVec (Rotation Storage)

**Purpose**: Stores one bone's rotation in three numeric forms.

**Structure** (30 bytes):

```c
typedef struct FF7ShortVec {
    SHORT   sX, sY, sZ;     // Signed short versions. Offset: 0x00
    INT iX, iY, iZ;     // Integer representation (always positive). Offset: 0x06
    FLOAT   fX, fY, fZ;     // Final float degrees. Offset: 0x12
} * PFF7ShortRot;           // Total size: 30 bytes
```

#### Three-Form Conversion

Rotations are processed through three representations:

1. **SHORT** (signed 16-bit): Raw value from file, range 0-4095 (0° to 360°)
2. **INT** (unsigned 32-bit): Absolute value with wrapping
   - If `SHORT < 0`, add `0x1000` (4096)
3. **FLOAT**: Final degrees using formula: `(INT / 4096) * 360`

#### Per-Frame Processing Sequence

**First Frame**:
1. Read X bits (determined by `bKey`) and store as signed SHORT
2. Convert SHORT to INT (add 0x1000 if negative)
3. Convert INT to FLOAT: `(INT / 4096 * 360)`
4. Apply FLOAT rotation to model

**Subsequent Frames**:
1. Read delta value, add to previous frame's SHORT
2. Convert updated SHORT to INT (add 0x1000 if negative)
3. Convert INT to FLOAT: `(INT / 4096 * 360)`
4. Apply FLOAT rotation to model

**Root Rotation**: The first rotation is always `(0, 0, 0)` and is not part of the skeleton network. Some animations store non-zero values here for dynamic targeting during battle.

### 2.5 FF7FrameBuffer (Frame Management)

**Purpose**: Allocates memory for one frame's worth of bone rotations.

**Structure**:

```c
typedef struct FF7FrameBuffer {
    DWORD           dwBones;
    FF7ShortVec     svPosOffset;
    FF7ShortVec     *psvRots;

    FF7FrameBuffer() {
        dwBones = 0;
        psvRots = NULL;
    }
    ~FF7FrameBuffer() {
        dwBones = 0;
        delete [] psvRots;
        psvRots = NULL;
    }

    VOID    SetBones( DWORD dwTotal ) {
        // Delete the old
        dwBones = 0;
        delete [] psvRots;

        // Create the new
        psvRots = new FF7ShortVec[dwTotal];
        if ( psvRots != NULL ) { dwBones = dwTotal; }
    }
} * PFF7FrameBuffer;
```

**Usage**: Call `FF7FrameBuffer.SetBones(boneCount)` with your animation's bone count to allocate rotation storage.

---

## 3. Decoding Algorithms

### 3.1 Bit Stream Reading

#### GetBitsFixed Function

**Purpose**: Reads arbitrary bit sequences from a byte buffer.

**Parameters**:
- `pbBuffer`: Byte array containing bit stream
- `dwStartBit`: Bit offset to start reading (modified in place)
- `dwTotalBits`: Number of bits to read

**Returns**: Signed integer with sign extension.

**Implementation**:

```c
INT GetBitsFixed( BYTE * pbBuffer, DWORD &dwStartBit,
DWORD dwTotalBits ) {
    INT iReturn = 0;

    for ( DWORD I = 0; I < dwTotalBits; I++ ) {
        iReturn <<= 1;

        __asm mov eax, dwStartBit
        __asm mov eax, [eax]
        __asm cdq
        __asm and edx, 7
        __asm add eax, edx
        __asm sar eax, 3
        __asm mov ecx, pbBuffer
        __asm xor edx, edx
        __asm mov dl, byte ptr ds:[ecx+eax]
        __asm mov eax, dwStartBit
        __asm mov ecx, [eax]
        __asm and ecx, 7
        __asm mov eax, 7
        __asm sub eax, ecx
        __asm mov esi, 1
        __asm mov ecx, eax
        __asm shl esi, cl
        __asm and edx, esi
        __asm test edx, edx
        __asm je INCBIT
        iReturn++;
INCBIT: dwStartBit++;
    }

    // Force sign bit to extend across 32-bit boundary
    iReturn <<= (0x20 - dwTotalBits);
    iReturn >>= (0x20 - dwTotalBits);
    return iReturn;
}
```

### 3.2 First Frame (Uncompressed)

The first frame stores absolute values with no delta compression.

#### 3.2.1 Position Offsets

**Format**: Always 16 bits per axis (X, Y, Z), stored as signed SHORTs.

**Example** (Cloud's first animation, `rtda`):
- Bytes: `00 00 FE 2E 00 00`
- Values: `X=0`, `Y=-466`, `Z=0`
- Total: 16 bits × 3 = 48 bits = 6 bytes

**Note**: Y-axis is stored inverted but can be ignored during initial parsing.

**Code**:

```c
PFF7FrameMiniHeader pfmhMiniHeader = (PFF7FrameMiniHeader)pbBuffer;
BYTE * pbAnimBuffer = &pbBuffer[5];  // Skip 5-byte miniheader

DWORD dwBitStart = 0;
SHORT sX = GetBitsFixed( pbAnimBuffer, dwBitStart, 16 );
SHORT sY = GetBitsFixed( pbAnimBuffer, dwBitStart, 16 );
SHORT sZ = GetBitsFixed( pbAnimBuffer, dwBitStart, 16 );
// Result: sX=0, sY=-466, sZ=0
```

#### 3.2.2 Rotation Data

**Bit Count**: Determined by `bKey` using formula `(12 - bKey)`
- If `bKey = 0`: 12 bits per rotation
- If `bKey = 2`: 10 bits per rotation
- If `bKey = 4`: 8 bits per rotation

**Normalization**: Shift left by `bKey` to restore 12-bit range.

**Code** (for each bone's 3 rotations):

```c
SHORT sRotX = GetBitsFixed( pbAnimBuffer, dwBitStart,
12 - pfmhMiniHeader->bKey );
SHORT sRotY = GetBitsFixed( pbAnimBuffer, dwBitStart,
12 - pfmhMiniHeader->bKey );
SHORT sRotZ = GetBitsFixed( pbAnimBuffer, dwBitStart,
12 - pfmhMiniHeader->bKey );

// Normalize to 12-bit range
sRotX <<= pfmhMiniHeader->bKey;
sRotY <<= pfmhMiniHeader->bKey;
sRotZ <<= pfmhMiniHeader->bKey;
```

### 3.3 Subsequent Frames (Compressed Delta Encoding)

Frames after the first store delta values (changes from previous frame).

#### 3.3.1 Position Deltas

**Format**: Variable-length encoding (8 or 17 bits)

**Algorithm**:
1. Read 1 flag bit
   - If `0`: Next 7 bits are signed delta (total 8 bits)
   - If `1`: Next 16 bits are signed delta (total 17 bits)

**GetDynamicFrameOffsetBits Function**:

```c
SHORT GetDynamicFrameOffsetBits( BYTE * pBuffer, DWORD &dwBitStart ) {
DWORD dwFirstByte, dwConsumedBits, dwBitsRemainingToNextByte, dwTemp;
    SHORT sReturn;
    __asm {
        mov eax, dwBitStart
        mov eax, [eax]
        cdq
        and edx, 7
        add eax, edx
        sar eax, 3
        mov dwFirstByte, eax
        mov ecx, dwBitStart
        mov edx, [ecx]
        and edx, 7
        mov dwConsumedBits, edx
        mov eax, 7
        sub eax, dwConsumedBits
        mov dwBitsRemainingToNextByte, eax
        mov ecx, pBuffer
        add ecx, dwFirstByte
        xor edx, edx
        mov dl, byte ptr ds:[ecx]
        shl edx, 8
        mov eax, pBuffer
        add eax, dwFirstByte
        xor ecx, ecx
        mov cl, byte ptr ds:[eax+1]
        or edx, ecx
        mov dwTemp, edx
        mov ecx, dwBitsRemainingToNextByte
        add ecx, 8
        mov edx, 1
        shl edx, cl
        mov eax, dwTemp
        and eax, edx
        test eax, eax
        jnz SeventeenBits

EightBits :
        mov ecx, dwConsumedBits
        add ecx, 1
        mov edx, dwTemp
        shl edx, cl
        movsx eax, dx
        sar eax, 9
        mov sReturn, ax
        mov ecx, dwBitStart
        mov edx, [ecx]
        add edx, 8
        mov eax, dwBitStart
        mov [eax], edx      // Increase dwBitStart by 8
        jmp End

SeventeenBits :
        mov ecx, dwTemp
        shl ecx, 8
        mov edx, pBuffer
        add edx, dwFirstByte
        xor eax, eax
        mov al, byte ptr ds:[edx+2]
        or ecx, eax
        mov dwTemp, ecx
        mov ecx, dwConsumedBits
        add ecx, 1
        mov edx, dwTemp
        shl edx, cl
        shr edx, 8
        mov sReturn, dx
        mov eax, dwBitStart
        mov ecx, [eax]
        add ecx, 0x11
        mov edx, dwBitStart
        mov [edx], ecx      // Increase dwBitStart by 17

End :
    }
    return sReturn;
}
```

**Usage**:

```c
SHORT sDeltaX = GetDynamicFrameOffsetBits( pbAnimBuffer, dwBitStart );
SHORT sDeltaY = GetDynamicFrameOffsetBits( pbAnimBuffer, dwBitStart );
SHORT sDeltaZ = GetDynamicFrameOffsetBits( pbAnimBuffer, dwBitStart );

// Add deltas to previous frame
FF7FrameBuffer[I].svPosOffset.sX = FF7FrameBuffer[I-1].svPosOffset.sX + sDeltaX;
FF7FrameBuffer[I].svPosOffset.sY = FF7FrameBuffer[I-1].svPosOffset.sY + sDeltaY;
FF7FrameBuffer[I].svPosOffset.sZ = FF7FrameBuffer[I-1].svPosOffset.sZ + sDeltaZ;
```

#### 3.3.2 Rotation Deltas

**Format**: Complex variable-length encoding optimized for small deltas.

**Algorithm Overview**:
1. Read 1 flag bit:
   - If `0`: Delta is zero, done
   - If `1`: Continue to step 2
2. Read 3-bit type field (values 0-7)
3. Decode based on type:
   - **Type 0**: Minimum decrement `(-1 << bKey)`
   - **Types 1-6**: Read N bits, apply signed magnitude transform
   - **Type 7**: Uncompressed value `(12 - bKey)` bits

**Signed Magnitude Transform** (Types 1-6):

If the N-bit value is negative:
- Subtract `(1 << (N - 1))`

If positive:
- Add `(1 << (N - 1))`

Finally, shift left by `bKey` to adjust for precision.

**Example** (Type 4, meaning 4 bits):
- Read 4-bit value (e.g., binary `1011` = -5 in signed form)
- Since negative: subtract `(1 << 3)` = 8 → `-5 - 8 = -13`
- Shift left by `bKey` (e.g., if `bKey=2`): `-13 << 2 = -52`

**GetEncryptedRotationBits Function**:

```c
SHORT GetEncryptedRotationBits( BYTE * pBuffer, DWORD &dwBitStart,
INT iKeyBits ) {
    DWORD dwNumBits, dwType;
    INT iTemp;
    SHORT sReturn;
    // Check the first bit
    INT iBits = GetBitsFixed( pBuffer, dwBitStart, 1 );
    __asm mov eax, iBits
    __asm test eax, eax
    __asm jnz SecondTest
    __asm jmp ReturnZero    // Return 0

SecondTest :
    // Get next 3 bits
    iBits = GetBitsFixed( pBuffer, dwBitStart, 3 );
    __asm mov eax, iBits
    __asm and eax, 7
    __asm mov dwNumBits, eax
    __asm mov ecx, dwNumBits
    __asm mov dwType, ecx
    __asm cmp dwType, 7
    __asm ja ReturnZero

    // Switch on type
    switch ( dwType ) {
        case 0 : {
            __asm or eax, 0xFFFFFFFF    // EAX = -1
            __asm mov ecx, iKeyBits
            __asm shl eax, cl           // (-1 << iKeyBits)
            __asm mov sReturn, ax
            __asm jmp End
        }
        case 1 : {}
        case 2 : {}
        case 3 : {}
        case 4 : {}
        case 5 : {}
        case 6 : {
            // Read N bits
            iTemp = GetBitsFixed( pBuffer, dwBitStart,
                dwNumBits );
            __asm mov eax, iTemp
            __asm cmp iTemp, 0
            __asm jl IfLessThanZero
            // If >= 0: add (1 << (dwNumBits - 1))
            __asm mov ecx, dwNumBits
            __asm sub ecx, 1
            __asm mov eax, 1
            __asm shl eax, cl
            __asm mov ecx, iTemp
            __asm add ecx, eax
            __asm mov iTemp, ecx
            __asm jmp AfterTests
IfLessThanZero :
            // If < 0: subtract (1 << (dwNumBits - 1))
            __asm mov ecx, dwNumBits
            __asm sub ecx, 1
            __asm mov edx, 1
            __asm shl edx, cl
            __asm mov eax, iTemp
            __asm sub eax, edx
            __asm mov iTemp, eax

AfterTests :
            // Shift by precision
            __asm mov eax, iTemp
            __asm mov ecx, iKeyBits
            __asm shl eax, cl
            __asm mov sReturn, ax
            __asm jmp End
        }

        case 7 : {
            // Uncompressed: read (12 - iKeyBits) bits
            iTemp = GetBitsFixed( pBuffer, dwBitStart,
                12 - iKeyBits );
            __asm mov ecx, iKeyBits
            __asm shl eax, cl
            __asm mov sReturn, ax
            __asm jmp End
        }

    }


ReturnZero :
    __asm xor ax, ax
    __asm mov sReturn, ax

End :

    return sReturn;
}
```

---

## 4. Implementation Guide

### 4.1 LoadFrames Function

**Purpose**: Load an entire frame (position + all bone rotations) at once.

**Returns**: Bit offset where next frame begins (or 0 if no more frames).

**Parameters**:
- `pfbFrameBuffer`: Pointer to frame buffer to fill
- `iBones`: Number of bones in skeleton
- `iBitStart`: Bit offset to start reading (0 for first frame)
- `pbAnimBuffer`: Byte array containing animation data

**Implementation**:

```c
DWORD LoadFrames( PFF7FrameBuffer pfbFrameBuffer,
INT iBones,
INT iBitStart,
BYTE * pbAnimBuffer ) {
    // Get backups of parameters
DWORD       dwThisBitStart  = iBitStart;
    INT     iThisBones      = iBones;
    BYTE *  pbThisBuffer    = pbAnimBuffer;

    PFF7FrameMiniHeader pfmhMiniHeader =
        (PFF7FrameMiniHeader)pbAnimBuffer;
    SHORT   sSize = pfmhMiniHeader->sSize;
    BYTE    bKeyBits = pfmhMiniHeader->bKey;

    // Skip 5-byte miniheader
    pbThisBuffer += sizeof( FF7FrameMiniHeader );

    if ( iBitStart == 0 ) { // First frame?
        // Uncompressed position offsets
        pfbFrameBuffer->svPosOffset.sX = GetBitsFixed( pbThisBuffer, dwThisBitStart, 16 );
        pfbFrameBuffer->svPosOffset.sY = GetBitsFixed( pbThisBuffer, dwThisBitStart, 16 );
        pfbFrameBuffer->svPosOffset.sZ = GetBitsFixed( pbThisBuffer, dwThisBitStart, 16 );

        // Convert to FLOAT
        pfbFrameBuffer->svPosOffset.fX = (FLOAT)pfbFrameBuffer->svPosOffset.sX;
        pfbFrameBuffer->svPosOffset.fY = (FLOAT)pfbFrameBuffer->svPosOffset.sY;
        pfbFrameBuffer->svPosOffset.fZ = (FLOAT)pfbFrameBuffer->svPosOffset.sZ;

        for ( int I = 0; I < iThisBones; I++ ) {
            // Read rotations (12 - bKeyBits) bits each
            pfbFrameBuffer->psvRots[I].sX = (GetBitsFixed( pbThisBuffer, dwThisBitStart, 12 - bKeyBits ) << bKeyBits);
            pfbFrameBuffer->psvRots[I].sY = (GetBitsFixed( pbThisBuffer, dwThisBitStart, 12 - bKeyBits ) << bKeyBits);
            pfbFrameBuffer->psvRots[I].sZ = (GetBitsFixed( pbThisBuffer, dwThisBitStart, 12 - bKeyBits ) << bKeyBits);

            // Convert SHORT to INT (absolute value)
            pfbFrameBuffer->psvRots[I].iX = (pfbFrameBuffer->psvRots[I].sX < 0) ? pfbFrameBuffer->psvRots[I].sX + 0x1000 : pfbFrameBuffer->psvRots[I].sX;
            pfbFrameBuffer->psvRots[I].iY = (pfbFrameBuffer->psvRots[I].sY < 0) ? pfbFrameBuffer->psvRots[I].sY + 0x1000 : pfbFrameBuffer->psvRots[I].sY;
            pfbFrameBuffer->psvRots[I].iZ = (pfbFrameBuffer->psvRots[I].sZ < 0) ? pfbFrameBuffer->psvRots[I].sZ + 0x1000 : pfbFrameBuffer->psvRots[I].sZ;
        }
    }
    else {                  // Subsequent frames
        SHORT sX, sY, sZ;

        // Get position deltas
        sX = GetDynamicFrameOffsetBits( pbThisBuffer, dwThisBitStart );
        sY = GetDynamicFrameOffsetBits( pbThisBuffer, dwThisBitStart );
        sZ = GetDynamicFrameOffsetBits( pbThisBuffer, dwThisBitStart );

        // Add deltas to previous frame
        pfbFrameBuffer->svPosOffset.sX += sX;
        pfbFrameBuffer->svPosOffset.sY += sY;
        pfbFrameBuffer->svPosOffset.sZ += sZ;

        pfbFrameBuffer->svPosOffset.fX = (FLOAT)pfbFrameBuffer->svPosOffset.sX;
        pfbFrameBuffer->svPosOffset.fY = (FLOAT)pfbFrameBuffer->svPosOffset.sY;
        pfbFrameBuffer->svPosOffset.fZ = (FLOAT)pfbFrameBuffer->svPosOffset.sZ;

        for ( int I = 0; I < iThisBones; I++ ) {
            // Get rotation deltas
            sX = GetEncryptedRotationBits( pbThisBuffer, dwThisBitStart, bKeyBits );
            sY = GetEncryptedRotationBits( pbThisBuffer, dwThisBitStart, bKeyBits );
            sZ = GetEncryptedRotationBits( pbThisBuffer, dwThisBitStart, bKeyBits );

            // Add deltas
            pfbFrameBuffer->psvRots[I].sX += sX;
            pfbFrameBuffer->psvRots[I].sY += sY;
            pfbFrameBuffer->psvRots[I].sZ += sZ;

            // Note: Values can exceed 4095 through accumulation of positive deltas

            // Convert to INT
            pfbFrameBuffer->psvRots[I].iX = (pfbFrameBuffer->psvRots[I].sX < 0) ? pfbFrameBuffer->psvRots[I].sX + 0x1000 : pfbFrameBuffer->psvRots[I].sX;
            pfbFrameBuffer->psvRots[I].iY = (pfbFrameBuffer->psvRots[I].sY < 0) ? pfbFrameBuffer->psvRots[I].sY + 0x1000 : pfbFrameBuffer->psvRots[I].sY;
            pfbFrameBuffer->psvRots[I].iZ = (pfbFrameBuffer->psvRots[I].sZ < 0) ? pfbFrameBuffer->psvRots[I].sZ + 0x1000 : pfbFrameBuffer->psvRots[I].sZ;
        }
    }

    // Return next frame's bit offset (or 0 if done)
    if ( (SHORT)(dwThisBitStart / 8) < sSize ) {
return dwThisBitStart;
}
    return 0;
}
```

### 4.2 Complete Animation Loading Loop

**Example**: Load all frames in an animation.

```c
FF7FrameHeader fhHeader;
ReadFile( hFile, &fhHeader, sizeof( fhHeader ), &ulBytesRead,
NULL );
BYTE * baData = new BYTE[fhHeader.dwChunkSize];
ReadFile( hFile, &baData, fhHeader.dwChunkSize, &ulBytesRead,
NULL );

    // Allocate frame buffer
FF7FrameBuffer fbFrameBuffer;
fbFrameBuffer.SetBones( fhHeader.dwBones );
INT iBits = 0;

for ( DWORD J = 0; J < fhHeader.dwFrames; J++ ) {
    // Load frame
    iBits = LoadFrames( &fbFrameBuffer, fhHeader.dwBones, iBits, baData );

    // Reverse Y offset (required)
    fbFrameBuffer.svPosOffset.fY = 0.0f - fbFrameBuffer.svPosOffset.fY;

    // Convert INT rotations to FLOAT degrees
    // Note: First rotation (root) is typically 0,0,0 but some animations
    // store a base rotation for dynamic targeting
    for ( DWORD I = 0; I < fhHeader.dwBones - 1; I++ ) {
        fbFrameBuffer.psvRots[I+1].fX = (FLOAT)fbFrameBuffer.psvRots[I+1].iX / 4096.0f * 360.0f;
        fbFrameBuffer.psvRots[I+1].fY = (FLOAT)fbFrameBuffer.psvRots[I+1].iY / 4096.0f * 360.0f;
        fbFrameBuffer.psvRots[I+1].fZ = (FLOAT)fbFrameBuffer.psvRots[I+1].iZ / 4096.0f * 360.0f;
    }

    // Store frame data here (application-specific)
}

delete [] baData;
```

---

## 5. Alternative Implementations

### 5.1 Qhimm's C++ Versions

**Qhimm** rewrote the assembly functions in pure C++ for better readability. He also provided theoretical background on the compression scheme.

#### GetValueFromStream

Replaces `GetDynamicFrameOffsetBits` with clearer C++ implementation.

```c
short GetValueFromStream( BYTE *pStreamBytes,
DWORD *pdwStreamBitOffset )
{
    short sValue;
    DWORD dwStreamByteOffset = *pdwStreamBitOffset / 8;
    DWORD dwCurrentBitsEaten = *pdwStreamBitOffset % 8;
    DWORD dwTypeBitShift = 7 - dwCurrentBitsEaten;
    DWORD dwNextStreamBytes = pStreamBytes[dwStreamByteOffset] << 8 | pStreamBytes[dwStreamByteOffset + 1];

    // Test first bit to determine value size
    if (dwNextStreamBytes & (1 << (dwTypeBitShift + 8)))
    {   // 16-bit value
        dwNextStreamBytes = dwNextStreamBytes << 8 |
            pStreamBytes[dwStreamByteOffset + 2];
        sValue = (dwNextStreamBytes << (dwCurrentBitsEaten + 1)) >> 8;
        *pdwStreamBitOffset += 17;
    }
    else
    {   // 7-bit value
        sValue = ((short)(dwNextStreamBytes << (dwCurrentBitsEaten + 1))) >> 9;
        *pdwStreamBitOffset += 8;
    }

    return sValue;
}
```

#### GetCompressedDeltaFromStream

Replaces `GetEncryptedRotationBits` with clearer C++ implementation.

```c
short GetCompressedDeltaFromStream( BYTE *pStreamBytes, DWORD *pdwStreamBitOffset,
int nLoweredPrecisionBits )
{
    unsigned int nBits;
    int iFirstBit = GetBitsFromStream( pStreamBytes, pdwStreamBitOffset, 1 );
    if (iFirstBit)
    {
        unsigned int uType = GetBitsFromStream( pStreamBytes,
            pdwStreamBitOffset, 3 ) & 7;
        switch (uType)
        {
        case 0:
            // Minimum decrement
            return (-1 << nLoweredPrecisionBits);

        case 1: case 2: case 3: case 4: case 5: case 6:
            // Read N bits
            int iTemp = GetBitsFromStream( pStreamBytes,
                pdwStreamBitOffset, nBits );
            // Apply signed magnitude transform
            if (iTemp < 0)  iTemp -= 1 << (nBits - 1);
            else            iTemp += 1 << (nBits - 1);
            // Adjust for precision
            return (iTemp << nLoweredPrecisionBits);

        case 7:
            // Uncompressed
            iTemp = GetBitsFromStream( pStreamBytes,
                pdwStreamBitOffset, 12 - nLoweredPrecisionBits );
            return (iTemp << nLoweredPrecisionBits);
        default:
        }
    }
    return 0;
}
```

### 5.2 Rotation Compression Theory

*Notes by Qhimm*

#### Why This Encoding Is Efficient

Rotational deltas in skeletal animation are typically small. The compression scheme allocates fewer bits to small deltas and more bits to large changes.

**Bit Allocation**:
- Zero delta: 1 bit (`0`)
- Minimum decrement: 4 bits (`1 000`)
- Small deltas (1-6 bits): 126 possible values
- Large deltas: Uncompressed form

**Total Coverage**: 128 delta values in the range `[-64, 63]` can be stored in compressed form. This is efficient because most rotational changes in character animation are incremental.

#### Signed Magnitude Encoding

For delta types 1-6, the encoding uses signed magnitude to pack values efficiently:

1. **Magnitude**: Value of most significant value bit
   - Example: Values `1` and `-2` both have magnitude `1`
   - Value `30` has magnitude `32`

2. **Signed Magnitude**: Magnitude × sign of value
   - Example: `-2` has signed magnitude `-1`

3. **Encoding**: Subtract signed magnitude before storing
   - Pushes values toward zero
   - Ensures all transformed values fit in 6 bits or fewer

4. **Decoding**: Add back the signed magnitude
   - Magnitude determined by number of bits read
   - Sign determined by MSB of encoded value

#### Encoding Examples

| Delta Value | Encoded Bits        | Notes                                    |
|-------------|---------------------|------------------------------------------|
| 0           | `0`                 | Single zero bit                          |
| -1          | `1 000`             | Type 0 (minimum decrement)               |
| -5          | `1 011 111`         | Type 3 (3 bits)                          |
| 15          | `1 100 0111`        | Type 4 (4 bits)                          |
| 128         | `1 111 xxxx10000000`| Type 7 (depends on precision)            |

*(Values shown in current precision as integers)*

#### Precision Trade-offs

Precision can be reduced by 2 or 4 bits (from 12 bits down to 10 or 8):

**Advantages**:
- Smaller raw values
- Increased relative span of compressed encodings
- Much smaller file sizes

**Disadvantages**:
- Quantization error
- Less precise rotations

**When It Works Well**: Most skeletal animations change gradually. Large rotations (spinning objects) are typically round numbers (90°, 180°, 270°) that lose negligible precision even at 8-bit depth.

**Note**: Reduced precision is treated as rounding toward negative infinity.

---

## Appendix A: Quick Reference

### Structure Sizes

| Structure          | Size (bytes) | Offset Fields                              |
|--------------------|--------------|--------------------------------------------|
| FF7FrameHeader     | 12           | dwBones: 0x00, dwFrames: 0x04, dwChunkSize: 0x08 |
| FF7FrameMiniHeader | 5            | sFrames: 0x00, sSize: 0x02, bKey: 0x04     |
| FF7ShortVec        | 30           | SHORT: 0x00, INT: 0x06, FLOAT: 0x12        |

### bKey Values

| bKey | Uncompressed Bits | Formula         | Range   |
|------|-------------------|-----------------|---------|
| 0    | 12                | `12 - 0 = 12`   | 0-4095  |
| 2    | 10                | `12 - 2 = 10`   | 0-1023  |
| 4    | 8                 | `12 - 4 = 8`    | 0-255   |

### Conversion Formulas

**SHORT to Degrees**:
```
degrees = (SHORT / 4096) * 360
```

**SHORT to INT (with wrapping)**:
```
INT = (SHORT < 0) ? SHORT + 0x1000 : SHORT
```

**INT to FLOAT**:
```
FLOAT = (INT / 4096.0f) * 360.0f
```

### Position Delta Encoding

| First Bit | Total Bits | Format     |
|-----------|------------|------------|
| 0         | 8          | 7-bit delta|
| 1         | 17         | 16-bit delta|

### Rotation Delta Type Field

| Type | Bits to Read        | Meaning                        |
|------|---------------------|--------------------------------|
| 0    | 0                   | Minimum decrement: `(-1 << bKey)` |
| 1-6  | N (= type value)    | Signed magnitude encoded delta |
| 7    | `12 - bKey`         | Uncompressed rotation value    |

---

## Appendix B: Known Issues

### Corrupted Animations

**RSAA Animation 15** (playable frog):
- Missing `sFrames` field
- `sSize` appears at offset 0x00 instead of 0x02
- `bKey` appears at offset 0x02 instead of 0x04
- FF7 cannot load this animation (likely damaged in original game data)

### Frame Count Discrepancies

**sFrames vs. dwFrames**:
- Rarely match in practice
- `dwFrames` is more conservative (guarantees minimum)
- `sFrames` sometimes exceeds actual frame count
- **Solution**: Parse entire chunk to determine true frame count

**Possible Causes**:
- Dummy frames padded for memory alignment
- Special-purpose data interleaved with frames
- Animation authoring tool artifacts

### Root Rotation Behavior

**Standard Behavior**: First rotation is always `(0, 0, 0)` and not part of skeleton.

**Exception**: Some animations store non-zero root rotations for dynamic targeting:
- Model facing toward attack target
- Model rotating during special moves

**Recommendation**: Do not skip root rotation unconditionally. Check if non-zero before using for targeting logic.

---

**End of Document**

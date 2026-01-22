// AF3DN.P Key Japanese Text/Naming Screen Functions
// Extracted for detailed Pass 2 analysis
// Source: IDA Pro decompiled AF3DN.P.c
// Generated: 2025-12-16 15:13 JST


// ============================================================
// sub_10001340 (lines 8976-9099)
// ============================================================
int *sub_10001340()
{
  int v0; // ebx
  int v1; // ebp
  unsigned int v2; // ecx
  int *result; // eax
  int v4; // esi
  unsigned int v5; // ebx
  _DWORD *v6; // ecx
  int v7; // edi
  unsigned int v8; // ecx
  int v9; // edi
  unsigned int v10; // ecx
  _DWORD *v11; // edx
  int v12; // [esp+10h] [ebp-4h]

  if ( dword_1004CB78 )
  {
    v0 = 0;
    v12 = 0;
  }
  else
  {
    v12 = dword_10050660();
    v0 = v12;
  }
  if ( dword_1004CB78 )
    v1 = dword_10050660();
  else
    v1 = 0;
  v2 = 0;
  if ( dword_10050D78 )
  {
    result = (int *)&unk_10051880;
    while ( 1 )
    {
      v4 = v1 + 2892;
      if ( !dword_1004CB78 )
        v4 = v0 + 2572;
      if ( result[4] == *(_DWORD *)(v4 + 16) && *result == *(unsigned __int16 *)dword_10050640 )
        break;
      ++v2;
      result += 5;
      if ( v2 >= dword_10050D78 )
        goto LABEL_14;
    }
LABEL_19:
    if ( dword_1004CBBC != *result )
      dword_1004CBBC = *result;
    return result;
  }
LABEL_14:
  v5 = 0;
  if ( !dword_10050D78 )
  {
LABEL_24:
    v8 = 0;
    if ( !dword_10050D78 )
    {
LABEL_28:
      if ( *(unsigned __int16 *)dword_10050640 != dword_1004CBBC )
        dword_1004CBBC = *(unsigned __int16 *)dword_10050640;
      result = (int *)&unk_100518D0;
      if ( dword_1004CB78 )
        return (int *)&unk_1005195C;
      return result;
    }
    result = (int *)&unk_10051880;
    while ( *result != *(unsigned __int16 *)dword_10050640 )
    {
      ++v8;
      result += 5;
      if ( v8 >= dword_10050D78 )
        goto LABEL_28;
    }
    goto LABEL_19;
  }
  v6 = &unk_10051890;
  while ( 1 )
  {
    result = v6 - 4;
    if ( *v6 )
    {
      v7 = dword_1004CB78 ? v1 + 2892 : v12 + 2572;
      if ( *v6 == *(_DWORD *)(v7 + 16) )
        break;
    }
    ++v5;
    v6 += 5;
    if ( v5 >= dword_10050D78 )
      goto LABEL_24;
  }
  if ( dword_1004CBBC != *result )
  {
    v9 = *(unsigned __int16 *)dword_10050640;
    if ( *result != v9 )
    {
      if ( result[3] )
      {
        v10 = 0;
        if ( dword_10050D78 != 1 )
        {
          v11 = &unk_10051880;
          do
          {
            if ( *v11 == v9 )
              break;
            ++v10;
            v11 += 5;
          }
          while ( v10 < dword_10050D78 - 1 );
        }
      }
    }
    dword_1004CBBC = *result;
  }
  return result;
}
// 1004CB78: using guessed type int dword_1004CB78;
// 1004CBBC: using guessed type int dword_1004CBBC;
// 10050640: using guessed type int dword_10050640;
// 10050660: using guessed type int (*dword_10050660)(void);
// 10050D78: using guessed type int dword_10050D78;


// ============================================================
// sub_10019110 (lines 24226-24671)
// ============================================================
//----- (100146D0) --------------------------------------------------------
int __usercall sub_100146D0@<eax>(int a1@<eax>)
{
  int result; // eax

  switch ( a1 )
  {
    case 1:
      result = 19;
      break;
    case 2:
      result = 20;
      break;
    case 3:
      result = 21;
      break;
    case 4:
      result = 22;
      break;
    case 5:
      result = 23;
      break;
    case 6:
      result = 24;
      break;
    case 7:
      result = 25;
      break;
    case 8:
      result = 26;
      break;
    case 9:
      result = 27;
      break;
    case 10:
      result = 28;
      break;
    case 11:
      result = 29;
      break;
    case 12:
      result = 30;
      break;
    case 13:
      result = 31;
      break;
    case 14:
      result = 32;
      break;
    case 15:
      result = 33;
      break;
    case 16:
      result = 34;
      break;
    case 17:
      result = 35;
      break;
    case 18:
      result = 36;
      break;
    case 19:
      result = 37;
      break;
    case 20:
      result = 38;
      break;
    case 21:
      result = 39;
      break;
    case 22:
      result = 40;
      break;
    case 23:
      result = 41;
      break;
    case 24:
      result = 42;
      break;
    case 25:
      result = 43;
      break;
    case 26:
      result = 44;
      break;
    case 27:
      result = 45;
      break;
    case 28:
      result = 46;
      break;
    case 29:
      result = 47;
      break;
    case 30:
      result = 48;
      break;
    case 31:
      result = 49;
      break;
    case 32:
      result = 50;
      break;
    case 33:
      result = 51;
      break;
    case 34:
      result = 52;
      break;
    case 35:
      result = 53;
      break;
    case 36:
      result = 54;
      break;
    case 37:
      result = 55;
      break;
    case 38:
      result = 56;
      break;
    case 39:
      result = 57;
      break;
    case 40:
      result = 58;
      break;
    case 41:
      result = 59;
      break;
    case 42:
      result = 60;
      break;
    case 43:
      result = 61;
      break;
    case 44:
      result = 62;
      break;
    case 45:
      result = 63;
      break;
    case 46:
      result = 64;
      break;
    case 47:
      result = 65;
      break;
    case 48:
      result = 66;
      break;
    case 49:
      result = 67;
      break;
    case 50:
      result = 68;
      break;
    case 51:
      result = 69;
      break;
    case 52:
      result = 70;
      break;
    case 53:
      result = 71;
      break;
    case 54:
      result = 72;
      break;
    case 55:
      result = 73;
      break;
    case 56:
      result = 74;
      break;
    case 57:
      result = 75;
      break;
    case 58:
      result = 76;
      break;
    case 59:
      result = 77;
      break;
    case 60:
      result = 78;
      break;
    case 61:
      result = 79;
      break;
    case 62:
      result = 80;
      break;
    case 63:
      result = 81;
      break;
    case 64:
      result = 82;
      break;
    case 65:
      result = 83;
      break;
    case 66:
      result = 84;
      break;
    case 67:
      result = 85;
      break;
    case 68:
      result = 86;
      break;
    case 69:
      result = 87;
      break;
    case 70:
      result = 88;
      break;
    case 71:
      result = 89;
      break;
    case 72:
      result = 90;
      break;
    case 73:
      result = 91;
      break;
    case 74:
      result = 92;
      break;
    case 75:
      result = 93;
      break;
    case 76:
      result = 94;
      break;
    case 77:
      result = 95;
      break;
    case 78:
      result = 96;
      break;
    case 79:
      result = 97;
      break;
    case 80:
      result = 98;
      break;
    case 81:
      result = 99;
      break;
    case 82:
      result = 100;
      break;
    case 83:
      result = 101;
      break;
    case 86:
      result = 102;
      break;
    case 87:
      result = 103;
      break;
    case 88:
      result = 104;
      break;
    case 100:
      result = 105;
      break;
    case 101:
      result = 106;
      break;
    case 102:
      result = 107;
      break;
    case 112:
      result = 108;
      break;
    case 115:
      result = 109;
      break;
    case 121:
      result = 110;
      break;
    case 123:
      result = 111;
      break;
    case 125:
      result = 112;
      break;
    case 126:
      result = 113;
      break;
    case 141:
      result = 114;
      break;
    case 144:
      result = 115;
      break;
    case 145:
      result = 116;
      break;
    case 146:
      result = 117;
      break;
    case 147:
      result = 118;
      break;
    case 148:
      result = 119;
      break;
    case 149:
      result = 120;
      break;
    case 150:
      result = 121;
      break;
    case 151:
      result = 122;
      break;
    case 153:
      result = 123;
      break;
    case 156:
      result = 124;
      break;
    case 157:
      result = 125;
      break;
    case 160:
      result = 126;
      break;
    case 161:
      result = 127;
      break;
    case 162:
      result = 128;
      break;
    case 164:
      result = 129;
      break;
    case 174:
      result = 130;
      break;
    case 176:
      result = 131;
      break;
    case 178:
      result = 132;
      break;
    case 179:
      result = 133;
      break;
    case 181:
      result = 134;
      break;
    case 183:
      result = 135;
      break;
    case 184:
      result = 136;
      break;
    case 197:
      result = 137;
      break;
    case 199:
      result = 138;
      break;
    case 200:
      result = 139;
      break;
    case 201:
      result = 140;
      break;
    case 203:
      result = 141;
      break;
    case 205:
      result = 142;
      break;
    case 207:
      result = 143;
      break;
    case 208:
      result = 144;
      break;
    case 209:
      result = 145;
      break;
    case 210:
      result = 146;
      break;
    case 211:
      result = 147;
      break;
    case 219:
      result = 148;
      break;
    case 220:
      result = 149;
      break;
    case 221:
      result = 150;
      break;
    case 222:
      result = 151;
      break;
    case 223:
      result = 152;
      break;
    case 227:
      result = 153;
      break;
    case 229:
      result = 154;
      break;
    case 230:
      result = 155;
      break;
    case 231:
      result = 156;
      break;
    case 232:
      result = 157;
      break;
    case 233:
      result = 158;
      break;
    case 234:
      result = 159;
      break;
    case 235:
      result = 160;
      break;
    case 236:
      result = 161;
      break;
    case 237:
      result = 162;
      break;
    default:
      result = -1;
      break;
  }
  return result;
}


// ============================================================
// sub_10016CE0 (lines 22450-22620)
// ============================================================
//----- (10011E80) --------------------------------------------------------
_DWORD *__usercall sub_10011E80@<eax>(int a1@<eax>, _DWORD *a2@<ecx>)
{
  sub_1001E5A0((int *)(a1 + 8), a2);
  return a2;
}

//----- (10011EA0) --------------------------------------------------------
_DWORD *__cdecl sub_10011EA0(_DWORD *a1)
{
  int v1; // eax
  int v2; // ecx
  _DWORD *v3; // eax
  void (__thiscall ***v4)(_DWORD, int); // edi
  void (__thiscall ***v5)(void *, int); // eax
  void (__thiscall ***v6)(void *, int); // edi
  _DWORD *v7; // eax
  void (__thiscall ***v8)(_DWORD, int); // edi
  _DWORD *v9; // eax
  _DWORD *v10; // edi
  _DWORD *v11; // edi
  int v13; // [esp+18h] [ebp-20h]
  int v14; // [esp+20h] [ebp-18h] BYREF
  int v15; // [esp+24h] [ebp-14h]
  int v16; // [esp+34h] [ebp-4h]

  v1 = *(_DWORD *)dword_1004CAC0;
  v2 = dword_1004CAC0 + 4;
  *a1 = &Message::`vftable';
  a1[1] = 0;
  v13 = v2;
  a1[3] = 0;
  a1[2] = 0;
  v16 = 0;
  switch ( v1 )
  {
    case 1:
      a1[1] = v1;
      v5 = (void (__thiscall ***)(void *, int))operator new(0xCu);
      if ( v5 )
      {
        v5[1] = (void (__thiscall **)(void *, int))1;
        *v5 = (void (__thiscall **)(void *, int))&IntPayload::`vftable';
        v6 = v5;
      }
      else
      {
        v6 = 0;
      }
      (**v6)(v6, v13);
      v14 = 0;
      v15 = 0;
      sub_1001EF00(&v14, v6);
      v16 = 3;
      goto LABEL_6;
    case 2:
    case 4:
    case 7:
    case 8:
    case 18:
    case 19:
    case 20:
      a1[1] = v1;
      return a1;
    case 3:
    case 15:
      a1[1] = v1;
      v3 = operator new(0x20u);
      v4 = (void (__thiscall ***)(_DWORD, int))v3;
      v14 = (int)v3;
      v16 = 1;
      if ( v3 )
      {
        v3[1] = 2;
        *v3 = &IntArrayPayload::`vftable';
        sub_10019540(v3 + 2);
      }
      else
      {
        v4 = 0;
      }
      LOBYTE(v16) = 0;
      (**v4)(v4, v13);
      v14 = 0;
      v15 = 0;
      sub_1001E970((int)&v14, (int)v4);
      v16 = 2;
      goto LABEL_6;
    case 5:
    case 6:
    case 9:
    case 10:
    case 11:
    case 12:
    case 16:
    case 17:
      a1[1] = v1;
      v7 = operator new(0x24u);
      if ( v7 )
      {
        v7[1] = 4;
        *v7 = &WStringPayload::`vftable';
        v7[8] = 7;
        v7[7] = 0;
        *((_WORD *)v7 + 6) = 0;
        v8 = (void (__thiscall ***)(_DWORD, int))v7;
      }
      else
      {
        v8 = 0;
      }
      (**v8)(v8, v13);
      v14 = 0;
      v15 = 0;
      sub_1001EA40((int)&v14, (int)v8);
      v16 = 4;
      goto LABEL_6;
    case 13:
      a1[1] = v1;
      v9 = operator new(0x68u);
      v14 = (int)v9;
      v16 = 5;
      if ( v9 )
        v10 = sub_10011690(v9);
      else
        v10 = 0;
      LOBYTE(v16) = 0;
      (*(void (__thiscall **)(_DWORD *, int))*v10)(v10, v13);
      v14 = 0;
      v15 = 0;
      sub_1001EB10(&v14, v10);
      v16 = 6;
      goto LABEL_6;
    case 14:
      a1[1] = v1;
      v11 = operator new(0x28u);
      v14 = (int)v11;
      v16 = 7;
      if ( v11 )
      {
        v11[1] = 6;
        *v11 = &IngameTextPayload::`vftable';
        sub_1001A540(v11 + 2);
      }
      else
      {
        v11 = 0;
      }
      LOBYTE(v16) = 0;
      (*(void (__thiscall **)(_DWORD *, int))*v11)(v11, v13);
      v14 = 0;
      v15 = 0;
      sub_1001EBE0((int)&v14, (int)v11);
      v16 = 8;
LABEL_6:
      sub_100197D0(&v14, a1 + 2);
      LOBYTE(v16) = 0;
      sub_10019790((int)&v14);
      break;
    default:
      return a1;
  }
  return a1;
}
// 100433BC: using guessed type void *IntPayload::`vftable';
// 100433CC: using guessed type void *IntArrayPayload::`vftable';
// 100433DC: using guessed type void *WStringPayload::`vftable';
// 100433FC: using guessed type void *IngameTextPayload::`vftable';
// 1004340C: using guessed type void *Message::`vftable';
// 1004CAC0: using guessed type int dword_1004CAC0;


// ============================================================
// sub_10019230 (lines 24803-24825)
// ============================================================
//----- (10014FF0) --------------------------------------------------------
void sub_10014FF0()
{
  void *v0; // ecx

  if ( !byte_1004CE97 )
  {
    byte_1004CE97 = 1;
    dword_1004CAC8 = sub_10014DC0();
    setlocale(0, Locale);
    sub_10014E10(v0);
    if ( !sub_10015520() )
    {
      MessageBoxA(0, "Please use the launcher 'FF7_Launcher.exe' ...", "Error", 0);
      exit_0(0);
    }
    sub_10015710();
  }
}
// 10015019: variable 'v0' is possibly undefined
// 1004CAC8: using guessed type int dword_1004CAC8;
// 1004CE97: using guessed type char byte_1004CE97;


// ============================================================
// sub_100191F0 (lines 24710-24802)
// ============================================================
//----- (10014E10) --------------------------------------------------------
int __thiscall sub_10014E10(void *this)
{
  int v1; // eax
  int v2; // esi
  int v3; // eax
  unsigned __int8 *v4; // esi
  int v5; // eax
  int result; // eax
  DWORD flOldProtect; // [esp+0h] [ebp-4h] BYREF

  flOldProtect = (DWORD)this;
  switch ( MEMORY[0x401004] )
  {
    case 0x99CE0805:
      v1 = MEMORY[0x919970] == 36 ? 1 : 20;
      break;
    case 0x99EBF805:
      v1 = 2;
      break;
    case 0x99DBC805:
      v1 = 3;
      break;
    default:
      v1 = MEMORY[0x401004] != -1711908859 ? 0 : 4;
      break;
  }
  dword_1004CAC8 = v1;
  switch ( v1 )
  {
    case 20:
    case 1:
      v2 = 4213373;
      dword_1004C790 = 4213373;
      dword_1004CAF4 = (LPVOID)4213578;
      dword_1004CABC = 10093880;
      dword_1004CAE8 = 14420956;
      break;
    case 2:
      v2 = 4213389;
      dword_1004C790 = 4213389;
      dword_1004CAF4 = (LPVOID)4213594;
      dword_1004CABC = 10101544;
      dword_1004CAE8 = 15968540;
      break;
    case 3:
      v2 = 4213373;
      dword_1004C790 = 4213373;
      dword_1004CAF4 = (LPVOID)4213578;
      dword_1004CABC = 10097400;
      dword_1004CAE8 = 15964428;
      break;
    case 4:
      v2 = 4213389;
      dword_1004C790 = 4213389;
      dword_1004CAF4 = (LPVOID)4213594;
      dword_1004CABC = 10104200;
      dword_1004CAE8 = 15971308;
      break;
    default:
      v2 = dword_1004C790;
      break;
  }
  VirtualProtect((LPVOID)v2, 5u, 0x40u, &flOldProtect);
  v3 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *(unsigned __int8 *)v2;
  ++v3;
  dword_1004E620[v3++] = *(_DWORD *)(v2 + 1);
  dword_1004E620[v3] = v2;
  dword_1004CC50 = v3 + 1;
  *(_BYTE *)v2 = -23;
  *(_DWORD *)(v2 + 1) = (char *)sub_10014D90 - v2 - 5;
  v4 = (unsigned __int8 *)dword_1004CAF4;
  VirtualProtect(dword_1004CAF4, 5u, 0x40u, &flOldProtect);
  v5 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v4;
  ++v5;
  dword_1004E620[v5++] = *(_DWORD *)(v4 + 1);
  dword_1004E620[v5] = (int)v4;
  result = v5 + 1;
  *v4 = -23;
  *(_DWORD *)(v4 + 1) = (char *)nullsub_1 - (char *)v4 - 5;
  dword_1004CC50 = result;
  return result;
}
// 100086A0: using guessed type int nullsub_1();
// 1004C790: using guessed type int dword_1004C790;
// 1004CABC: using guessed type int dword_1004CABC;
// 1004CAC8: using guessed type int dword_1004CAC8;
// 1004CAE8: using guessed type int dword_1004CAE8;
// 1004CC50: using guessed type int dword_1004CC50;
// 1004E620: using guessed type int dword_1004E620[];


// ============================================================
// sub_1000F190 (lines 15113-15224)
// ============================================================
//----- (100086B0) --------------------------------------------------------
char __cdecl sub_100086B0(int a1)
{
  _DWORD *v1; // ebx
  unsigned int v2; // ebp
  _DWORD *v3; // esi
  int v4; // edx
  int v5; // ecx
  int v6; // eax
  _DWORD *v7; // eax
  size_t v8; // edi
  _BYTE *v9; // esi
  _BYTE *v10; // ecx
  unsigned int v11; // eax
  int v12; // esi
  void *v13; // eax
  bool v14; // zf
  const void *v15; // ecx
  void *v17; // [esp-4h] [ebp-18h]
  _DWORD *v18; // [esp+10h] [ebp-4h]
  _DWORD *v19; // [esp+18h] [ebp+4h]

  v1 = *(_DWORD **)(*(_DWORD *)(*(_DWORD *)(a1 + 36) + 16) + 20);
  v2 = 0;
  if ( dword_1004CB78 )
  {
    v3 = (_DWORD *)v1[38];
    v4 = v3[15];
    v5 = v3[16];
    v6 = v3[26];
    v18 = 0;
    v19 = v3;
  }
  else
  {
    v7 = (_DWORD *)v1[38];
    v4 = v7[15];
    v5 = v7[16];
    v18 = v7;
    v6 = v7[26];
    v19 = 0;
    v3 = 0;
  }
  v8 = v4 * v5 * v6;
  do
  {
    if ( (_DWORD *)dword_1004FF80[v2] == v1 )
    {
      if ( dword_1004CB78 )
        v9 = (_BYTE *)v3[54];
      else
        v9 = (_BYTE *)v18[53];
      v10 = *(void **)((char *)&Block + v2 * 4);
      v11 = v8;
      if ( v8 < 4 )
      {
LABEL_12:
        if ( !v11 )
          return v11;
        if ( *v9 == *v10 )
        {
          if ( v11 <= 1 )
            return v11;
          if ( v9[1] == v10[1] )
          {
            if ( v11 <= 2 )
              return v11;
            LOBYTE(v11) = v9[2];
            if ( (_BYTE)v11 == v10[2] )
              return v11;
          }
        }
      }
      else
      {
        while ( *(_DWORD *)v10 == *(_DWORD *)v9 )
        {
          v11 -= 4;
          v9 += 4;
          v10 += 4;
          if ( v11 < 4 )
            goto LABEL_12;
        }
      }
      v3 = v19;
    }
    ++v2;
  }
  while ( v2 < 64 );
  v12 = dword_10050180;
  v17 = *(&Block + dword_10050180);
  dword_1004FF80[dword_10050180] = (int)v1;
  free(v17);
  v13 = malloc(v8);
  v14 = dword_1004CB78 == 0;
  *(&Block + v12) = v13;
  if ( v14 )
    v15 = (const void *)v18[53];
  else
    v15 = (const void *)v19[54];
  memcpy(v13, v15, v8);
  dword_10050180 = ((_BYTE)v12 + 1) & 0x3F;
  sub_100029E0((int)v1);
  LOBYTE(v11) = (unsigned __int8)sub_100033B0(v1, (_DWORD *)v1[38], v1[37]);
  ++dword_100501E4;
  return v11;
}
// 1004CB78: using guessed type int dword_1004CB78;
// 1004FF80: using guessed type int dword_1004FF80[64];
// 10050180: using guessed type int dword_10050180;
// 100501E4: using guessed type int dword_100501E4;


// ============================================================
// sub_1000F5C0 (lines 15467-15488)
// ============================================================
//----- (10008DA0) --------------------------------------------------------
float *__usercall sub_10008DA0@<eax>(float *result@<eax>, float *a2@<edx>, float *a3@<ecx>)
{
  *a2 = *a3 * *result + a3[1] * result[4] + result[8] * a3[2] + result[12] * a3[3];
  a2[1] = result[5] * a3[1] + *a3 * result[1] + result[9] * a3[2] + a3[3] * result[13];
  a2[2] = result[6] * a3[1] + result[2] * *a3 + a3[2] * result[10] + a3[3] * result[14];
  a2[3] = result[7] * a3[1] + *a3 * result[3] + result[11] * a3[2] + a3[3] * result[15];
  a2[4] = a3[5] * result[4] + a3[4] * *result + result[8] * a3[6] + result[12] * a3[7];
  a2[5] = a3[4] * result[1] + result[5] * a3[5] + result[9] * a3[6] + a3[7] * result[13];
  a2[6] = a3[5] * result[6] + a3[4] * result[2] + a3[6] * result[10] + result[14] * a3[7];
  a2[7] = a3[4] * result[3] + result[7] * a3[5] + result[11] * a3[6] + a3[7] * result[15];
  a2[8] = a3[9] * result[4] + a3[8] * *result + result[8] * a3[10] + result[12] * a3[11];
  a2[9] = a3[8] * result[1] + result[5] * a3[9] + result[9] * a3[10] + a3[11] * result[13];
  a2[10] = a3[9] * result[6] + a3[8] * result[2] + a3[10] * result[10] + result[14] * a3[11];
  a2[11] = a3[8] * result[3] + result[7] * a3[9] + result[11] * a3[10] + a3[11] * result[15];
  a2[12] = *result * a3[12] + a3[13] * result[4] + a3[14] * result[8] + result[12] * a3[15];
  a2[13] = result[5] * a3[13] + a3[12] * result[1] + a3[14] * result[9] + a3[15] * result[13];
  a2[14] = result[2] * a3[12] + result[6] * a3[13] + a3[14] * result[10] + result[14] * a3[15];
  a2[15] = result[7] * a3[13] + a3[12] * result[3] + a3[14] * result[11] + a3[15] * result[15];
  return result;
}


// ============================================================
// sub_1000EFD0 (lines 15038-15062)
// ============================================================
//----- (10008550) --------------------------------------------------------
int sub_10008550()
{
  int result; // eax

  result = sub_10008050();
  qmemcpy(&unk_10051880, &unk_1004A620, 0x12Cu);
  qmemcpy(byte_10050720, &unk_1004A758, sizeof(byte_10050720));
  dword_10050D78 = 15;
  dword_100501A0 = 1;
  dword_100501B8 = 2;
  dword_100501A8 = 3;
  dword_100501B0 = 4;
  dword_100501B4 = 5;
  dword_100501AC = 6;
  dword_100501BC = 7;
  return result;
}
// 100501A0: using guessed type int dword_100501A0;
// 100501A8: using guessed type int dword_100501A8;
// 100501B0: using guessed type int dword_100501B0;
// 100501B4: using guessed type int dword_100501B4;
// 100501BC: using guessed type int dword_100501BC;
// 10050D78: using guessed type int dword_10050D78;


// ============================================================
// sub_1000B9D0 (lines 12307-12357)
// ============================================================
//----- (10004B20) --------------------------------------------------------
int __cdecl sub_10004B20(int a1, int a2, int a3)
{
  int v3; // ebx
  int result; // eax
  int v5; // ebp
  int v6; // ecx
  const void *v7; // esi

  if ( dword_1004CB78 )
  {
    v3 = *(_DWORD *)(dword_1004CB78 != 0 ? a2 + 0x2C : 44);
    result = *(_DWORD *)(dword_1004CB78 != 0 ? a1 + 0x30 : 48);
    v5 = 0;
  }
  else
  {
    v5 = *(_DWORD *)(a2 + 48);
    result = *(_DWORD *)(dword_1004CB78 == 0 ? a1 + 0x2C : 44);
    v3 = 0;
  }
  if ( result )
  {
    if ( dword_1004CB78 )
      v6 = *(_DWORD *)(dword_1004CB78 != 0 ? a1 + 0x38 : 56);
    else
      v6 = *(_DWORD *)(a1 + 0x34);
    sub_10003FF0(v3, v6, a3);
    if ( dword_1004CB78 )
      result = *(_DWORD *)(v3 + 156);
    else
      result = *(_DWORD *)(v5 + 152);
    if ( result )
    {
      if ( dword_1004CB78 )
        qmemcpy(&unk_1004E578, *(const void **)(v3 + 160), 0x40u);
      else
        qmemcpy(&unk_1004E578, *(const void **)(v5 + 156), 0x40u);
    }
    else
    {
      v7 = (const void *)(v3 + 164);
      if ( !dword_1004CB78 )
        v7 = (const void *)(v5 + 160);
      qmemcpy(&unk_1004E578, v7, 0x40u);
    }
  }
  return result;
}
// 1004CB78: using guessed type int dword_1004CB78;


// ============================================================
// sub_1000EB90 (lines 16491-16585)
// ============================================================
//----- (1000A3E0) --------------------------------------------------------
int __usercall sub_1000A3E0@<eax>(const char *a1@<ecx>, int a2@<esi>)
{
  int result; // eax
  int v4; // eax
  void *v5; // edi
  _DWORD *v6; // eax
  int v7; // ecx
  size_t v8; // [esp+0h] [ebp-144h]
  size_t v9; // [esp+4h] [ebp-140h]
  void *v10; // [esp+8h] [ebp-13Ch]
  void *v11[2]; // [esp+Ch] [ebp-138h] BYREF
  int v12; // [esp+14h] [ebp-130h]
  unsigned __int16 v13; // [esp+18h] [ebp-12Ch]
  __int16 v14; // [esp+1Ah] [ebp-12Ah]
  int v15; // [esp+1Ch] [ebp-128h]
  _DWORD v16[5]; // [esp+20h] [ebp-124h] BYREF
  char Buffer[268]; // [esp+34h] [ebp-110h] BYREF

  result = dword_1004C5D4;
  if ( dword_1004C5D4 && *(_DWORD *)dword_1004C5C8 )
    result = (*(int (__stdcall **)(int))(*(_DWORD *)dword_1004C5D4 + 8))(dword_1004C5D4);
  dword_1004C5D4 = 0;
  if ( a2 )
  {
    sprintf(Buffer, "%sdata/music_ogg/%s.ogg", (const char *)dword_10050DC0, a1);
    if ( dword_1004C5D8[a2] || (result = init_vgmstream(Buffer), (dword_1004C5D8[a2] = result) != 0) )
    {
      LOWORD(v15) = 18;
      v4 = dword_1004C5D8[a2];
      v14 = 16;
      HIWORD(v11[0]) = *(_WORD *)(v4 + 8);
      v5 = *(void **)(v4 + 4);
      v13 = 16 * HIWORD(v11[0]) / 8;
      v12 = (_DWORD)v5 * v13;
      LOWORD(v11[0]) = 1;
      v11[1] = v5;
      v16[0] = 20;
      v16[4] = v11;
      v16[1] = 160;
      v16[3] = 0;
      v16[2] = 5 * v12;
      dword_1004C77C = 5 * v12;
      result = (*(int (__stdcall **)(_DWORD, _DWORD *, int *, _DWORD))(**(_DWORD **)dword_1004C5C8 + 12))(
                 *(_DWORD *)dword_1004C5C8,
                 v16,
                 &dword_1004C5D4,
                 0);
      if ( result )
      {
        dword_1004C5D4 = 0;
      }
      else
      {
        v6 = (_DWORD *)dword_1004C5D8[a2];
        v7 = 2 * v6[2];
        dword_1004C5A4 = v7;
        dword_1004C78C = 0;
        dword_1004C5C4 = 0;
        dword_1004A5DC = 0;
        if ( !v6[6] )
          dword_1004C768 = v7 * *v6;
        dword_1004C5D0 = a2;
        sub_1000A2A0(dword_1004C77C, v8, v9, v10, v11[0]);
        sub_1000A1F0();
        return (*(int (__stdcall **)(int, _DWORD, _DWORD, int))(*(_DWORD *)dword_1004C5D4 + 48))(
                 dword_1004C5D4,
                 0,
                 0,
                 1);
      }
    }
  }
  else
  {
    dword_1004C5D0 = 0;
  }
  return result;
}
// 1000A573: variable 'v8' is possibly undefined
// 1000A573: variable 'v9' is possibly undefined
// 1000A573: variable 'v10' is possibly undefined
// 10021D04: using guessed type int __cdecl init_vgmstream(_DWORD);
// 1004A5DC: using guessed type int dword_1004A5DC;
// 1004C5A4: using guessed type int dword_1004C5A4;
// 1004C5C4: using guessed type int dword_1004C5C4;
// 1004C5C8: using guessed type int dword_1004C5C8;
// 1004C5D0: using guessed type int dword_1004C5D0;
// 1004C5D4: using guessed type int dword_1004C5D4;
// 1004C5D8: using guessed type int dword_1004C5D8[100];
// 1004C768: using guessed type int dword_1004C768;
// 1004C77C: using guessed type int dword_1004C77C;
// 1004C78C: using guessed type int dword_1004C78C;
// 10050DC0: using guessed type int dword_10050DC0[64];


// ============================================================
// sub_10016A30 (lines 22195-22279)
// ============================================================
//----- (10011980) --------------------------------------------------------
_DWORD *__thiscall sub_10011980(int *this, int *a2)
{
  int v3; // ebx
  int *v4; // ecx
  _DWORD *v5; // esi
  _DWORD *v6; // edi
  _DWORD *result; // eax
  int v8; // ecx
  int *v9; // esi
  const void *v10; // eax
  _DWORD *v11; // edi
  int v12; // ecx
  int *v13; // esi
  const void *v14; // eax
  int v15; // ecx
  const void *v16; // eax
  _DWORD *v17; // [esp+Ch] [ebp-14h] BYREF
  int *v18; // [esp+10h] [ebp-10h]
  int *v19; // [esp+14h] [ebp-Ch]
  int *v20; // [esp+18h] [ebp-8h]
  _DWORD *v21; // [esp+1Ch] [ebp-4h]

  v3 = 0;
  v18 = this + 2;
  v19 = this + 10;
  v20 = this + 18;
  do
  {
    v4 = v18;
    *a2 = v3;
    v5 = a2 + 1;
    v17 = (_DWORD *)v3;
    v6 = sub_10019630(v4, (int *)&v17);
    v17 = (_DWORD *)v3;
    v21 = sub_10019630(v19, (int *)&v17);
    v17 = (_DWORD *)v3;
    result = sub_10019630(v20, (int *)&v17);
    *v5 = v6[5];
    v8 = v6[5];
    v9 = v5 + 1;
    v17 = result;
    if ( v8 )
    {
      if ( v6[6] < 8u )
        v10 = v6 + 1;
      else
        v10 = (const void *)v6[1];
      memcpy(v9, v10, 2 * v8);
      v9 = (int *)((char *)v9 + 2 * v6[5]);
      result = v17;
    }
    v11 = v21;
    *v9 = v21[5];
    v12 = v11[5];
    v13 = v9 + 1;
    if ( v12 )
    {
      if ( v11[6] < 8u )
        v14 = v11 + 1;
      else
        v14 = (const void *)v11[1];
      memcpy(v13, v14, 2 * v12);
      v13 = (int *)((char *)v13 + 2 * v11[5]);
      result = v17;
    }
    *v13 = result[5];
    v15 = result[5];
    a2 = v13 + 1;
    if ( v15 )
    {
      if ( result[6] < 8u )
        v16 = result + 1;
      else
        v16 = (const void *)result[1];
      memcpy(a2, v16, 2 * v15);
      result = v17;
      a2 = (int *)((char *)a2 + 2 * v17[5]);
    }
    ++v3;
  }
  while ( v3 < 36 );
  return result;
}


// ============================================================
// sub_10007010 (lines 13959-13984)
// ============================================================
int sub_10007010()
{
  int result; // eax

  dword_10050D78 = 28;
  result = sub_10006280();
  qmemcpy(&unk_10051880, &unk_1004A868, 0x230u);
  qmemcpy(byte_10050720, &unk_1004AA98, sizeof(byte_10050720));
  dword_100501A0 = 0;
  dword_100501A4 = 2;
  dword_100501A8 = 4;
  dword_100501AC = 6;
  dword_100501B0 = 8;
  dword_100501B4 = 10;
  dword_100501B8 = 12;
  dword_100501BC = 14;
  return result;
}
// 100501A0: using guessed type int dword_100501A0;
// 100501A4: using guessed type int dword_100501A4;
// 100501A8: using guessed type int dword_100501A8;
// 100501B0: using guessed type int dword_100501B0;
// 100501B4: using guessed type int dword_100501B4;
// 100501BC: using guessed type int dword_100501BC;
// 10050D78: using guessed type int dword_10050D78;


// ============================================================
// sub_10007120 (lines 14008-14678)
// ============================================================
//----- (10007120) --------------------------------------------------------
_DWORD *__usercall sub_10007120@<eax>(int a1@<ebx>)
{
  int v1; // eax
  int (__cdecl *v2)(_DWORD, _DWORD, _DWORD, _DWORD); // edx
  int (__cdecl *v3)(_DWORD, _DWORD, _DWORD); // ecx
  int (__cdecl *v4)(_DWORD, _DWORD, _DWORD); // edx
  int (__cdecl *v5)(_DWORD, _DWORD, _DWORD); // ecx
  int v6; // edx
  int (*v7)(void); // ecx
  int v8; // edx
  int v9; // ecx
  int (*v10)(void); // edx
  int v11; // ecx
  int v12; // eax
  _BYTE *v13; // esi
  _BYTE *v14; // esi
  _BYTE *v15; // esi
  int v16; // esi
  unsigned __int8 *v17; // esi
  int v18; // eax
  void *v19; // esi
  void *v20; // esi
  int v21; // esi
  int v22; // esi
  unsigned __int8 *v23; // esi
  int v24; // eax
  char *v25; // esi
  unsigned __int8 *v26; // esi
  int v27; // eax
  unsigned __int8 *v28; // esi
  int v29; // eax
  unsigned __int8 *v30; // esi
  int v31; // eax
  unsigned __int8 *v32; // esi
  int v33; // eax
  unsigned __int8 *v34; // esi
  int v35; // eax
  _BYTE *v36; // esi
  _BYTE *v37; // esi
  unsigned __int8 *v38; // esi
  int v39; // eax
  unsigned __int8 *v40; // esi
  int v41; // eax
  _BYTE *v42; // esi
  _BYTE *v43; // esi
  _BYTE *v44; // esi
  unsigned __int8 *v45; // esi
  int v46; // eax
  unsigned __int8 *v47; // esi
  int v48; // eax
  unsigned __int8 *v49; // esi
  int v50; // eax
  unsigned __int8 *v51; // esi
  int v52; // eax
  int v53; // eax
  void *v54; // esi
  _BYTE *v55; // esi
  _BYTE *v56; // esi
  bool v57; // zf
  _BYTE *v58; // esi
  void *v59; // esi
  _BYTE *v60; // esi
  unsigned __int8 *v61; // esi
  int v62; // eax
  unsigned __int8 *v63; // esi
  int v64; // eax
  unsigned __int8 *v65; // esi
  int v66; // eax
  unsigned __int8 *v67; // esi
  int v68; // eax
  unsigned __int8 *v69; // esi
  int v70; // eax
  unsigned __int8 *v71; // esi
  int v72; // eax
  unsigned __int8 *v73; // esi
  int v74; // eax
  unsigned __int8 *v75; // esi
  int v76; // eax
  unsigned __int8 *v77; // esi
  int v78; // eax
  unsigned __int8 *v79; // esi
  int v80; // eax
  unsigned __int8 *v81; // esi
  int v82; // eax
  unsigned __int8 *v83; // esi
  int v84; // eax
  unsigned __int8 *v85; // esi
  int v86; // eax
  unsigned __int8 *v87; // esi
  int v88; // eax
  unsigned __int8 *v89; // esi
  int v90; // eax
  unsigned __int8 *v91; // esi
  int v92; // eax
  double QuadPart; // st7
  unsigned __int8 *v94; // esi
  int v95; // eax
  unsigned __int8 *v96; // esi
  int v97; // eax
  void *v98; // esi
  _BYTE *v99; // esi
  char *v100; // esi
  _DWORD *result; // eax
  DWORD flOldProtect[3]; // [esp+10h] [ebp-Ch] BYREF

  sub_100070A0();
  sub_10001000();
  v1 = *(_DWORD *)(a1 + 2700);
  v2 = *(int (__cdecl **)(_DWORD, _DWORD, _DWORD, _DWORD))(v1 + 8);
  dword_10050668 = *(_DWORD *)(v1 + 16);
  v3 = *(int (__cdecl **)(_DWORD, _DWORD, _DWORD))(v1 + 4);
  dword_10050654 = v2;
  v4 = *(int (__cdecl **)(_DWORD, _DWORD, _DWORD))v1;
  dword_10050650 = v3;
  v5 = *(int (__cdecl **)(_DWORD, _DWORD, _DWORD))(v1 + 68);
  dword_1005064C = v4;
  v6 = *(_DWORD *)(v1 + 12);
  dword_1005065C = v5;
  v7 = *(int (**)(void))(v1 + 80);
  dword_10050664 = v6;
  v8 = *(_DWORD *)(v1 + 140);
  dword_10050670 = v7;
  v9 = *(_DWORD *)(v1 + 136);
  dword_10050648 = v8;
  v10 = *(int (**)(void))(v1 + 20);
  dword_10051054 = *(int (__cdecl **)(_DWORD))(v1 + 132);
  dword_10050644 = v9;
  v11 = *(_DWORD *)(a1 + 2700);
  dword_10050660 = v10;
  dword_1005066C = *(_DWORD *)(v11 + 32);
  sub_10007010();
  v12 = dword_10050624;
  *(_DWORD *)(a1 + 2436) = 1;
  *(_DWORD *)(a1 + 2704) = 0;
  *(_DWORD *)(a1 + 2484) = "FINAL FANTASY VII";
  *(_DWORD *)(a1 + 2600) = 0;
  if ( v12 == 20 || v12 == 1 )
  {
    v13 = (_BYTE *)(dword_1005118C + 349);
    VirtualProtect((LPVOID)(dword_1005118C + 349), 1u, 0x40u, flOldProtect);
    v12 = dword_10050624;
    *v13 = 15;
  }
  if ( v12 == 4 )
  {
    v14 = (_BYTE *)(dword_1005118C + 349);
    VirtualProtect((LPVOID)(dword_1005118C + 349), 1u, 0x40u, flOldProtect);
    *v14 = 14;
  }
  v15 = (_BYTE *)(dword_1005070C + 879);
  VirtualProtect((LPVOID)(dword_1005070C + 879), 1u, 0x40u, flOldProtect);
  *v15 = 88;
  v16 = dword_1005070C + 880;
  VirtualProtect((LPVOID)(dword_1005070C + 880), 5u, 0x40u, flOldProtect);
  *(_DWORD *)v16 = -1869574000;
  *(_BYTE *)(v16 + 4) = -112;
  v17 = (unsigned __int8 *)dword_1005126C;
  VirtualProtect(dword_1005126C, 5u, 0x40u, flOldProtect);
  v18 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v17;
  dword_1004E620[++v18] = *(_DWORD *)(v17 + 1);
  dword_1004E624[v18] = (int)v17;
  dword_1004CC50 = v18 + 2;
  *v17 = -23;
  *(_DWORD *)(v17 + 1) = (char *)sub_10007110 - (char *)v17 - 5;
  v19 = (void *)(dword_10051240 + 101);
  VirtualProtect((LPVOID)(dword_10051240 + 101), 9u, 0x40u, flOldProtect);
  memset(v19, 144, 9);
  v20 = (void *)(dword_10051244 + 60);
  VirtualProtect((LPVOID)(dword_10051244 + 60), 9u, 0x40u, flOldProtect);
  memset(v20, 144, 9);
  v21 = dword_10051244 + 126;
  VirtualProtect((LPVOID)(dword_10051244 + 126), 5u, 0x40u, flOldProtect);
  *(_DWORD *)v21 = -1869574000;
  *(_BYTE *)(v21 + 4) = -112;
  v22 = dword_1005125C + 49;
  VirtualProtect((LPVOID)(dword_1005125C + 49), 5u, 0x40u, flOldProtect);
  *(_DWORD *)v22 = -1869574000;
  *(_BYTE *)(v22 + 4) = -112;
  v23 = (unsigned __int8 *)dword_10051258;
  VirtualProtect(dword_10051258, 5u, 0x40u, flOldProtect);
  v24 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v23;
  dword_1004E620[++v24] = *(_DWORD *)(v23 + 1);
  dword_1004E624[v24] = (int)v23;
  dword_1004CC50 = v24 + 2;
  *v23 = -23;
  *(_DWORD *)(v23 + 1) = (char *)sub_10007110 - (char *)v23 - 5;
  v25 = (char *)dword_10051040 + 25;
  VirtualProtect((char *)dword_10051040 + 25, 6u, 0x40u, flOldProtect);
  *(_DWORD *)v25 = -1869574000;
  *((_WORD *)v25 + 2) = -28528;
  v26 = (unsigned __int8 *)dword_10051058;
  VirtualProtect(dword_10051058, 5u, 0x40u, flOldProtect);
  v27 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v26;
  ++v27;
  dword_1004E620[v27++] = *(_DWORD *)(v26 + 1);
  dword_1004E620[v27] = (int)v26;
  dword_1004CC50 = v27 + 1;
  *v26 = -23;
  *(_DWORD *)(v26 + 1) = (char *)sub_1000EAB0 - (char *)v26 - 5;
  v28 = (unsigned __int8 *)dword_1005105C;
  VirtualProtect(dword_1005105C, 5u, 0x40u, flOldProtect);
  v29 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v28;
  ++v29;
  dword_1004E620[v29++] = *(_DWORD *)(v28 + 1);
  dword_1004E620[v29] = (int)v28;
  dword_1004CC50 = v29 + 1;
  *v28 = -23;
  *(_DWORD *)(v28 + 1) = (char *)sub_1000EB10 - (char *)v28 - 5;
  v30 = (unsigned __int8 *)dword_10051060;
  VirtualProtect(dword_10051060, 5u, 0x40u, flOldProtect);
  v31 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v30;
  ++v31;
  dword_1004E620[v31++] = *(_DWORD *)(v30 + 1);
  dword_1004E620[v31] = (int)v30;
  dword_1004CC50 = v31 + 1;
  *v30 = -23;
  *(_DWORD *)(v30 + 1) = (char *)sub_1000EA60 - (char *)v30 - 5;
  v32 = (unsigned __int8 *)dword_10051164;
  VirtualProtect(dword_10051164, 5u, 0x40u, flOldProtect);
  v33 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v32;
  ++v33;
  dword_1004E620[v33++] = *(_DWORD *)(v32 + 1);
  dword_1004E620[v33] = (int)v32;
  dword_1004CC50 = v33 + 1;
  *v32 = -23;
  *(_DWORD *)(v32 + 1) = (char *)sub_1000D270 - (char *)v32 - 5;
  v34 = (unsigned __int8 *)dword_10051148;
  VirtualProtect(dword_10051148, 5u, 0x40u, flOldProtect);
  v35 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v34;
  dword_1004E620[++v35] = *(_DWORD *)(v34 + 1);
  dword_1004E624[v35] = (int)v34;
  dword_1004CC50 = v35 + 2;
  *v34 = -23;
  *(_DWORD *)(v34 + 1) = (char *)sub_1000D350 - (char *)v34 - 5;
  v36 = (_BYTE *)(dword_10051140 + 226);
  VirtualProtect((LPVOID)(dword_10051140 + 226), 1u, 0x40u, flOldProtect);
  *v36 = 29;
  v37 = (_BYTE *)(dword_10051140 + 851);
  VirtualProtect((LPVOID)(dword_10051140 + 851), 1u, 0x40u, flOldProtect);
  *v37 = 29;
  v38 = (unsigned __int8 *)dword_10051130;
  VirtualProtect(dword_10051130, 5u, 0x40u, flOldProtect);
  v39 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v38;
  ++v39;
  dword_1004E620[v39++] = *(_DWORD *)(v38 + 1);
  dword_1004E620[v39] = (int)v38;
  dword_1004CC50 = v39 + 1;
  *v38 = -23;
  *(_DWORD *)(v38 + 1) = (char *)sub_10011090 - (char *)v38 - 5;
  v40 = (unsigned __int8 *)dword_100511A0;
  VirtualProtect(dword_100511A0, 5u, 0x40u, flOldProtect);
  v41 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v40;
  dword_1004E620[++v41] = *(_DWORD *)(v40 + 1);
  dword_1004E624[v41] = (int)v40;
  dword_1004CC50 = v41 + 2;
  *v40 = -23;
  *(_DWORD *)(v40 + 1) = (char *)sub_10010FD0 - (char *)v40 - 5;
  v42 = (_BYTE *)(dword_10051218 + 62);
  VirtualProtect((LPVOID)(dword_10051218 + 62), 1u, 0x40u, flOldProtect);
  *v42 = -21;
  v43 = (_BYTE *)(dword_10051218 + 63);
  VirtualProtect((LPVOID)(dword_10051218 + 63), 1u, 0x40u, flOldProtect);
  *v43 = 77;
  v44 = dword_100511C0;
  VirtualProtect(dword_100511C0, 3u, 0x40u, flOldProtect);
  *(_WORD *)v44 = word_1004ABA4;
  v44[2] = byte_1004ABA6;
  v45 = (unsigned __int8 *)dword_100511C0 + 3;
  VirtualProtect((char *)dword_100511C0 + 3, 5u, 0x40u, flOldProtect);
  v46 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v45;
  ++v46;
  dword_1004E620[v46++] = *(_DWORD *)(v45 + 1);
  dword_1004E620[v46] = (int)v45;
  dword_1004CC50 = v46 + 1;
  *v45 = -23;
  *(_DWORD *)(v45 + 1) = (char *)sub_10011030 - (char *)v45 - 5;
  v47 = (unsigned __int8 *)dword_10051234;
  VirtualProtect(dword_10051234, 5u, 0x40u, flOldProtect);
  v48 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v47;
  ++v48;
  dword_1004E620[v48++] = *(_DWORD *)(v47 + 1);
  dword_1004E620[v48] = (int)v47;
  dword_1004CC50 = v48 + 1;
  *v47 = -23;
  *(_DWORD *)(v47 + 1) = (char *)sub_10007110 - (char *)v47 - 5;
  v49 = (unsigned __int8 *)dword_10051238;
  VirtualProtect(dword_10051238, 5u, 0x40u, flOldProtect);
  v50 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v49;
  ++v50;
  dword_1004E620[v50++] = *(_DWORD *)(v49 + 1);
  dword_1004E620[v50] = (int)v49;
  dword_1004CC50 = v50 + 1;
  *v49 = -23;
  *(_DWORD *)(v49 + 1) = (char *)sub_10007110 - (char *)v49 - 5;
  v51 = (unsigned __int8 *)dword_1005123C;
  VirtualProtect(dword_1005123C, 5u, 0x40u, flOldProtect);
  v52 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v51;
  ++v52;
  dword_1004E620[v52++] = *(_DWORD *)(v51 + 1);
  dword_1004E620[v52] = (int)v51;
  dword_1004CC50 = v52 + 1;
  v53 = dword_10050624;
  *v51 = -23;
  *(_DWORD *)(v51 + 1) = (char *)sub_10007110 - (char *)v51 - 5;
  if ( v53 == 3 || v53 == 4 )
  {
    v54 = (void *)(dword_10051284 + 2227);
    VirtualProtect((LPVOID)(dword_10051284 + 2227), 0xE6u, 0x40u, flOldProtect);
  }
  else
  {
    v54 = (void *)(dword_10051284 + 2220);
    VirtualProtect((LPVOID)(dword_10051284 + 2220), 0xE6u, 0x40u, flOldProtect);
  }
  memset(v54, 144, 0xE6u);
  v55 = (_BYTE *)(dword_100512B4 + 18);
  VirtualProtect((LPVOID)(dword_100512B4 + 18), 1u, 0x40u, flOldProtect);
  *v55 = 1;
  v56 = (_BYTE *)(dword_100512B4 + 26);
  VirtualProtect((LPVOID)(dword_100512B4 + 26), 1u, 0x40u, flOldProtect);
  v57 = dword_10050624 == 2;
  *v56 = 1;
  if ( v57 )
  {
    v58 = (_BYTE *)(dword_100512B8 + 232);
    VirtualProtect((LPVOID)(dword_100512B8 + 232), 1u, 0x40u, flOldProtect);
    *v58 = 1;
    v59 = (void *)(dword_100512B8 + 113);
    VirtualProtect((LPVOID)(dword_100512B8 + 113), 0x1Bu, 0x40u, flOldProtect);
  }
  else
  {
    v60 = (_BYTE *)(dword_100512B8 + 229);
    VirtualProtect((LPVOID)(dword_100512B8 + 229), 1u, 0x40u, flOldProtect);
    *v60 = 1;
    v59 = (void *)(dword_100512B8 + 110);
    VirtualProtect((LPVOID)(dword_100512B8 + 110), 0x1Bu, 0x40u, flOldProtect);
  }
  memset(v59, 144, 27);
  v61 = (unsigned __int8 *)dword_100506E0;
  VirtualProtect(dword_100506E0, 5u, 0x40u, flOldProtect);
  v62 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v61;
  ++v62;
  dword_1004E620[v62++] = *(_DWORD *)(v61 + 1);
  dword_1004E620[v62] = (int)v61;
  dword_1004CC50 = v62 + 1;
  *v61 = -23;
  *(_DWORD *)(v61 + 1) = (char *)sub_1000DAC0 - (char *)v61 - 5;
  v63 = (unsigned __int8 *)dword_100506E4;
  VirtualProtect(dword_100506E4, 5u, 0x40u, flOldProtect);
  v64 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v63;
  ++v64;
  dword_1004E620[v64++] = *(_DWORD *)(v63 + 1);
  dword_1004E620[v64] = (int)v63;
  dword_1004CC50 = v64 + 1;
  *v63 = -23;
  *(_DWORD *)(v63 + 1) = (char *)sub_1000E220 - (char *)v63 - 5;
  v65 = (unsigned __int8 *)dword_100506E8;
  VirtualProtect(dword_100506E8, 5u, 0x40u, flOldProtect);
  v66 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v65;
  ++v66;
  dword_1004E620[v66++] = *(_DWORD *)(v65 + 1);
  dword_1004E620[v66] = (int)v65;
  dword_1004CC50 = v66 + 1;
  *v65 = -23;
  *(_DWORD *)(v65 + 1) = (char *)sub_1000E160 - (char *)v65 - 5;
  v67 = (unsigned __int8 *)dword_100510F4;
  VirtualProtect(dword_100510F4, 5u, 0x40u, flOldProtect);
  v68 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v67;
  ++v68;
  dword_1004E620[v68++] = *(_DWORD *)(v67 + 1);
  dword_1004E620[v68] = (int)v67;
  dword_1004CC50 = v68 + 1;
  *v67 = -23;
  *(_DWORD *)(v67 + 1) = (char *)sub_1000E2C0 - (char *)v67 - 5;
  v69 = (unsigned __int8 *)dword_100506D8;
  VirtualProtect(dword_100506D8, 5u, 0x40u, flOldProtect);
  v70 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v69;
  ++v70;
  dword_1004E620[v70++] = *(_DWORD *)(v69 + 1);
  dword_1004E620[v70] = (int)v69;
  dword_1004CC50 = v70 + 1;
  *v69 = -23;
  *(_DWORD *)(v69 + 1) = (char *)sub_1000E310 - (char *)v69 - 5;
  v71 = (unsigned __int8 *)dword_100506DC;
  VirtualProtect(dword_100506DC, 5u, 0x40u, flOldProtect);
  v72 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v71;
  ++v72;
  dword_1004E620[v72++] = *(_DWORD *)(v71 + 1);
  dword_1004E620[v72] = (int)v71;
  dword_1004CC50 = v72 + 1;
  *v71 = -23;
  *(_DWORD *)(v71 + 1) = (char *)sub_1000DA70 - (char *)v71 - 5;
  v73 = (unsigned __int8 *)dword_100506EC;
  VirtualProtect(dword_100506EC, 5u, 0x40u, flOldProtect);
  v74 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v73;
  ++v74;
  dword_1004E620[v74++] = *(_DWORD *)(v73 + 1);
  dword_1004E620[v74] = (int)v73;
  dword_1004CC50 = v74 + 1;
  *v73 = -23;
  *(_DWORD *)(v73 + 1) = (char *)sub_1000E390 - (char *)v73 - 5;
  v75 = (unsigned __int8 *)dword_100506F0;
  VirtualProtect(dword_100506F0, 5u, 0x40u, flOldProtect);
  v76 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v75;
  ++v76;
  dword_1004E620[v76++] = *(_DWORD *)(v75 + 1);
  dword_1004E620[v76] = (int)v75;
  dword_1004CC50 = v76 + 1;
  *v75 = -23;
  *(_DWORD *)(v75 + 1) = (char *)sub_1000E3E0 - (char *)v75 - 5;
  v77 = (unsigned __int8 *)dword_100506F4;
  VirtualProtect(dword_100506F4, 5u, 0x40u, flOldProtect);
  v78 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v77;
  ++v78;
  dword_1004E620[v78++] = *(_DWORD *)(v77 + 1);
  dword_1004E620[v78] = (int)v77;
  dword_1004CC50 = v78 + 1;
  *v77 = -23;
  *(_DWORD *)(v77 + 1) = (char *)sub_1000E400 - (char *)v77 - 5;
  v79 = (unsigned __int8 *)dword_100510FC;
  VirtualProtect(dword_100510FC, 5u, 0x40u, flOldProtect);
  v80 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v79;
  ++v80;
  dword_1004E620[v80++] = *(_DWORD *)(v79 + 1);
  dword_1004E620[v80] = (int)v79;
  dword_1004CC50 = v80 + 1;
  *v79 = -23;
  *(_DWORD *)(v79 + 1) = (char *)sub_1000D470 - (char *)v79 - 5;
  v81 = (unsigned __int8 *)dword_100510E4;
  VirtualProtect(dword_100510E4, 5u, 0x40u, flOldProtect);
  v82 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v81;
  ++v82;
  dword_1004E620[v82++] = *(_DWORD *)(v81 + 1);
  dword_1004E620[v82] = (int)v81;
  dword_1004CC50 = v82 + 1;
  *v81 = -23;
  *(_DWORD *)(v81 + 1) = (char *)sub_1000D480 - (char *)v81 - 5;
  v83 = (unsigned __int8 *)dword_10051074;
  VirtualProtect(dword_10051074, 5u, 0x40u, flOldProtect);
  v84 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v83;
  ++v84;
  dword_1004E620[v84++] = *(_DWORD *)(v83 + 1);
  dword_1004E620[v84] = (int)v83;
  dword_1004CC50 = v84 + 1;
  *v83 = -23;
  *(_DWORD *)(v83 + 1) = (char *)sub_1000D6F0 - (char *)v83 - 5;
  v85 = (unsigned __int8 *)dword_1005107C;
  VirtualProtect(dword_1005107C, 5u, 0x40u, flOldProtect);
  v86 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v85;
  ++v86;
  dword_1004E620[v86++] = *(_DWORD *)(v85 + 1);
  dword_1004E620[v86] = (int)v85;
  dword_1004CC50 = v86 + 1;
  *v85 = -23;
  *(_DWORD *)(v85 + 1) = (char *)sub_1000D930 - (char *)v85 - 5;
  v87 = (unsigned __int8 *)dword_10051078;
  VirtualProtect(dword_10051078, 5u, 0x40u, flOldProtect);
  v88 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v87;
  ++v88;
  dword_1004E620[v88++] = *(_DWORD *)(v87 + 1);
  dword_1004E620[v88] = (int)v87;
  dword_1004CC50 = v88 + 1;
  *v87 = -23;
  *(_DWORD *)(v87 + 1) = (char *)sub_1000D980 - (char *)v87 - 5;
  v89 = (unsigned __int8 *)dword_10051080;
  VirtualProtect(dword_10051080, 5u, 0x40u, flOldProtect);
  v90 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v89;
  ++v90;
  dword_1004E620[v90++] = *(_DWORD *)(v89 + 1);
  dword_1004E620[v90] = (int)v89;
  dword_1004CC50 = v90 + 1;
  *v89 = -23;
  *(_DWORD *)(v89 + 1) = (char *)sub_1000D9F0 - (char *)v89 - 5;
  v91 = (unsigned __int8 *)dword_10051084;
  VirtualProtect(dword_10051084, 5u, 0x40u, flOldProtect);
  v92 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v91;
  ++v92;
  dword_1004E620[v92++] = *(_DWORD *)(v91 + 1);
  dword_1004E620[v92] = (int)v91;
  dword_1004CC50 = v92 + 1;
  *v91 = -23;
  *(_DWORD *)(v91 + 1) = (char *)sub_1000D900 - (char *)v91 - 5;
  if ( dword_1004AF2C )
  {
    timeBeginPeriod(1u);
    if ( dword_1004CB6C )
    {
      sub_1000AFF0((int)sub_10004FC0, (_BYTE *)dword_10050698);
      *(_QWORD *)flOldProtect = 0x3E800000000LL;
      QuadPart = (double)0x3E800000000LL;
      *(_DWORD *)(a1 + 56) = 0;
      *(_DWORD *)(a1 + 60) = 1000;
    }
    else
    {
      sub_1000AFF0((int)sub_10004FA0, (_BYTE *)dword_10050698);
      *(LARGE_INTEGER *)(a1 + 56) = Frequency;
      QuadPart = (double)Frequency.QuadPart;
    }
    *(double *)(a1 + 48) = QuadPart;
  }
  v94 = (unsigned __int8 *)dword_1005106C;
  VirtualProtect(dword_1005106C, 5u, 0x40u, flOldProtect);
  v95 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v94;
  ++v95;
  dword_1004E620[v95++] = *(_DWORD *)(v94 + 1);
  dword_1004E620[v95] = (int)v94;
  dword_1004CC50 = v95 + 1;
  *v94 = -23;
  *(_DWORD *)(v94 + 1) = (char *)sub_1000D0D0 - (char *)v94 - 5;
  v96 = (unsigned __int8 *)dword_100512B0;
  VirtualProtect(dword_100512B0, 5u, 0x40u, flOldProtect);
  v97 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v96;
  dword_1004E620[++v97] = *(_DWORD *)(v96 + 1);
  dword_1004E624[v97] = (int)v96;
  dword_1004CC50 = v97 + 2;
  *v96 = -23;
  *(_DWORD *)(v96 + 1) = (char *)sub_1000D0F0 - (char *)v96 - 5;
  v98 = (void *)(dword_10051020 - 12);
  VirtualProtect((LPVOID)(dword_10051020 - 12), 0x24u, 0x40u, flOldProtect);
  memset(v98, 144, 36);
  v99 = dword_10051024;
  VirtualProtect(dword_10051024, 3u, 0x40u, flOldProtect);
  *(_WORD *)v99 = word_1004AB98;
  v99[2] = byte_1004AB9A;
  v100 = (char *)dword_10051024 + 3;
  VirtualProtect((char *)dword_10051024 + 3, 0xFu, 0x40u, flOldProtect);
  v57 = dword_10050624 == 20;
  memset(v100, 144, 15);
  *(_DWORD *)dword_10051028 = dword_1004AB9C;
  *(_WORD *)(dword_10051028 + 4) = word_1004ABA0;
  if ( v57 )
    sub_10010B20();
  result = (_DWORD *)dword_10050654(1, 240, Locale, 0);
  result[24] = dword_10050648;
  result[26] = sub_10003FF0;
  result[27] = sub_10003FF0;
  result[28] = sub_10003FF0;
  result[42] = sub_10004AE0;
  result[43] = sub_10004AE0;
  result[44] = sub_10004AE0;
  result[37] = sub_10004A80;
  result[38] = sub_10004A80;
  result[39] = sub_10004A80;
  result[40] = sub_10004A80;
  result[41] = sub_10004A80;
  result[46] = sub_10004B20;
  result[47] = sub_10004B20;
  result[48] = sub_10004B20;
  result[49] = sub_10004B20;
  result[50] = sub_10004B20;
  result[55] = sub_10004A80;
  result[56] = sub_10004A80;
  *result = sub_10001860;
  result[1] = sub_100018C0;
  result[2] = sub_100019C0;
  result[3] = sub_100019C0;
  result[4] = sub_10001CE0;
  result[5] = sub_100024A0;
  result[6] = sub_10002600;
  result[7] = sub_10002620;
  result[8] = sub_10002850;
  result[16] = sub_100028F0;
  result[17] = &sub_10002960;
  result[18] = sub_10002970;
  result[19] = sub_100029E0;
  result[20] = sub_100033B0;
  result[21] = sub_10003A60;
  result[22] = sub_10003AD0;
  result[23] = sub_10003DD0;
  result[25] = sub_10003E20;
  result[29] = sub_10004390;
  result[30] = sub_100043D0;
  result[31] = sub_10004400;
  result[32] = sub_100044F0;
  result[33] = sub_10004550;
  result[34] = sub_10004660;
  result[35] = sub_10004700;
  result[36] = sub_10004780;
  result[45] = sub_10004B00;
  result[51] = sub_10004C00;
  result[52] = sub_10004C00;
  result[53] = sub_10004C00;
  result[54] = sub_10004C20;
  result[57] = sub_10004C40;
  result[58] = sub_10004C40;
  result[59] = sub_10004CB0;
  return result;
}
// 10001860: using guessed type int sub_10001860();
// 100043D0: using guessed type int sub_100043D0();
// 10004A80: using guessed type int sub_10004A80();
// 10004C00: using guessed type int sub_10004C00();
// 10004FC0: using guessed type int sub_10004FC0();
// 1000D480: using guessed type int sub_1000D480();
// 1000D900: using guessed type int sub_1000D900();
// 1000D980: using guessed type int sub_1000D980();
// 1000EA60: using guessed type int sub_1000EA60();
// 10010FD0: using guessed type int sub_10010FD0();
// 1004AB98: using guessed type __int16 word_1004AB98;
// 1004AB9A: using guessed type char byte_1004AB9A;
// 1004AB9C: using guessed type int dword_1004AB9C;
// 1004ABA0: using guessed type __int16 word_1004ABA0;
// 1004ABA4: using guessed type __int16 word_1004ABA4;
// 1004ABA6: using guessed type char byte_1004ABA6;
// 1004AF2C: using guessed type int dword_1004AF2C;
// 1004CB6C: using guessed type int dword_1004CB6C;
// 1004CC50: using guessed type int dword_1004CC50;
// 1004E620: using guessed type int dword_1004E620[];
// 1004E624: using guessed type int dword_1004E624[1535];
// 10050624: using guessed type int dword_10050624;
// 10050644: using guessed type int dword_10050644;
// 10050648: using guessed type int dword_10050648;
// 1005064C: using guessed type int (__cdecl *dword_1005064C)(_DWORD, _DWORD, _DWORD);
// 10050650: using guessed type int (__cdecl *dword_10050650)(_DWORD, _DWORD, _DWORD);
// 10050654: using guessed type int (__cdecl *dword_10050654)(_DWORD, _DWORD, _DWORD, _DWORD);
// 1005065C: using guessed type int (__cdecl *dword_1005065C)(_DWORD, _DWORD, _DWORD);
// 10050660: using guessed type int (*dword_10050660)(void);
// 10050664: using guessed type int dword_10050664;
// 10050668: using guessed type int dword_10050668;
// 1005066C: using guessed type int dword_1005066C;
// 10050670: using guessed type int (*dword_10050670)(void);
// 10050698: using guessed type int dword_10050698;
// 1005070C: using guessed type int dword_1005070C;
// 10051020: using guessed type int dword_10051020;
// 10051028: using guessed type int dword_10051028;
// 10051040: using guessed type int (__cdecl *dword_10051040)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD);
// 10051054: using guessed type int (__cdecl *dword_10051054)(_DWORD);
// 10051140: using guessed type int dword_10051140;
// 1005118C: using guessed type int dword_1005118C;
// 10051218: using guessed type int dword_10051218;
// 10051240: using guessed type int dword_10051240;
// 10051244: using guessed type int dword_10051244;
// 1005125C: using guessed type int dword_1005125C;
// 10051284: using guessed type int dword_10051284;
// 100512B4: using guessed type int dword_100512B4;
// 100512B8: using guessed type int dword_100512B8;


// ============================================================
// sub_1000B740 (lines 12690-13194)
// ============================================================
//----- (100052D0) --------------------------------------------------------
_DWORD *__cdecl new_dll_graphics_driver(_DWORD *a1)
{
  _DWORD *v1; // ebx
  _DWORD *v2; // edi
  unsigned int v3; // eax
  _DWORD *v4; // eax
  unsigned __int8 *v5; // esi
  int v6; // eax
  bool v7; // zf
  int v8; // ecx
  int v9; // eax
  HWND v10; // edx
  int v11; // edi
  int v12; // esi
  const CHAR *v13; // eax
  HINSTANCE v14; // edi
  const CHAR *v15; // esi
  const CHAR *v16; // eax
  HWND Window; // eax
  HINSTANCE v18; // ebx
  HICON IconA; // esi
  unsigned int v20; // ebx
  unsigned int v21; // edx
  unsigned int v22; // esi
  int v23; // edi
  unsigned int v24; // esi
  unsigned int v25; // ecx
  int v26; // ebx
  int v27; // eax
  char v29; // [esp+0h] [ebp-D0h]
  _DWORD *v30; // [esp+Ch] [ebp-C4h]
  DWORD flOldProtect; // [esp+10h] [ebp-C0h] BYREF
  _DWORD *v32; // [esp+14h] [ebp-BCh]
  tagRECT Rect; // [esp+18h] [ebp-B8h] BYREF
  DEVMODEA DevMode; // [esp+28h] [ebp-A8h] BYREF

  v1 = dword_1004CB78 == 0 ? a1 : 0;
  v2 = dword_1004CB78 != 0 ? a1 : 0;
  v30 = v2;
  sub_10014FF0();
  v3 = sub_100051A0();
  dword_10050624 = v3;
  switch ( v3 )
  {
    case 0x14u:
    case 1u:
      dword_10050658 = 14575472;
      lpAddress = (LPVOID)6704688;
      dword_10050678 = 4280032;
      dword_10050694 = (int (*)(void))6851654;
      dword_10050698 = 6685552;
      dword_1005069C = (LPVOID)7608192;
      dword_100506A0 = (int (__cdecl *)(_DWORD))7643344;
      dword_100506A4 = (LPVOID)7610453;
      dword_100506A8 = (LPVOID)7613995;
      dword_100506AC = (LPVOID)7613422;
      dword_100506B0 = (LPVOID)7613819;
      dword_100506B4 = (LPVOID)7613907;
      dword_100506B8 = (LPVOID)7614131;
      dword_100506BC = (LPVOID)7614170;
      dword_100506C0 = (LPVOID)7614263;
      dword_100506C4 = (LPVOID)7614540;
      dword_100506C8 = (LPVOID)7614909;
      dword_100506CC = 6742642;
      dword_100506D0 = 10083752;
      dword_100506D4 = 7247840;
      dword_10050710 = 6851734;
      dword_10051020 = 7793714;
      dword_10051024 = (LPVOID)7617346;
      dword_10051028 = 9798440;
      dword_1005102C = 4231155;
      dword_10051038 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6708634;
      dword_1005103C = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6756162;
      dword_10051040 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))7022505;
      dword_10051044 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6869688;
      dword_10051048 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6707091;
      dword_1005104C = (int (__cdecl *)(_DWORD))6798427;
      dword_10051050 = 6736955;
      dword_10051058 = (LPVOID)7022272;
      dword_1005105C = (LPVOID)7022368;
      dword_10051060 = (LPVOID)6766428;
      dword_10051064 = 14417208;
      dword_10051068 = 14421952;
      dword_1005106C = (LPVOID)4356392;
      dword_10051070 = (int (*)(void))4363042;
      dword_10051248 = 4235409;
      break;
    case 2u:
      dword_10050658 = 14431920;
      lpAddress = (LPVOID)6704592;
      dword_10050678 = 4280048;
      dword_10050694 = (int (*)(void))6851558;
      dword_10050698 = 6685456;
      dword_1005069C = (LPVOID)7200768;
      dword_100506A0 = (int (__cdecl *)(_DWORD))7235920;
      dword_100506A4 = (LPVOID)7203029;
      dword_100506A8 = (LPVOID)7206571;
      dword_100506AC = (LPVOID)7205998;
      dword_100506B0 = (LPVOID)7206395;
      dword_100506B4 = (LPVOID)7206483;
      dword_100506B8 = (LPVOID)7206707;
      dword_100506BC = (LPVOID)7206746;
      dword_100506C0 = (LPVOID)7206839;
      dword_100506C4 = (LPVOID)7207116;
      dword_100506C8 = (LPVOID)7207485;
      dword_100506CC = 6743521;
      dword_100506D0 = 10091416;
      dword_100506D4 = 7816848;
      dword_10050710 = 6851638;
      dword_10051020 = 7386290;
      dword_10051024 = (LPVOID)7209922;
      dword_10051028 = 9747016;
      dword_1005102C = 4231171;
      dword_10051038 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6708538;
      dword_1005103C = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6756066;
      dword_10051040 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))7022409;
      dword_10051044 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6869592;
      dword_10051048 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6706995;
      dword_1005104C = (int (__cdecl *)(_DWORD))6798331;
      dword_10051050 = 6736859;
      dword_10051058 = (LPVOID)7022176;
      dword_1005105C = (LPVOID)7022272;
      dword_10051060 = (LPVOID)6766332;
      dword_10051064 = 15964792;
      dword_10051068 = 15969536;
      dword_1005106C = (LPVOID)4356408;
      dword_10051070 = (int (*)(void))4363058;
      dword_10051248 = 4235425;
      goto LABEL_15;
    case 3u:
      dword_10050658 = 14427776;
      lpAddress = (LPVOID)6704640;
      dword_10050678 = 4280032;
      dword_10050694 = (int (*)(void))6851606;
      dword_10050698 = 6685504;
      dword_1005069C = (LPVOID)7200864;
      dword_100506A0 = (int (__cdecl *)(_DWORD))7236016;
      dword_100506A4 = (LPVOID)7203125;
      dword_100506A8 = (LPVOID)7206667;
      dword_100506AC = (LPVOID)7206094;
      dword_100506B0 = (LPVOID)7206491;
      dword_100506B4 = (LPVOID)7206579;
      dword_100506B8 = (LPVOID)7206803;
      dword_100506BC = (LPVOID)7206842;
      dword_100506C0 = (LPVOID)7206935;
      dword_100506C4 = (LPVOID)7207212;
      dword_100506C8 = (LPVOID)7207581;
      dword_100506CC = 6743569;
      dword_100506D0 = 10087272;
      dword_100506D4 = 7816112;
      dword_10050710 = 6851686;
      dword_10051020 = 7386386;
      dword_10051024 = (LPVOID)7210018;
      dword_10051028 = 9746992;
      dword_1005102C = 4231155;
      dword_10051038 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6708586;
      dword_1005103C = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6756114;
      dword_10051040 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))7022457;
      dword_10051044 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6869640;
      dword_10051048 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6707043;
      dword_1005104C = (int (__cdecl *)(_DWORD))6798379;
      dword_10051050 = 6736907;
      dword_10051058 = (LPVOID)7022224;
      dword_1005105C = (LPVOID)7022320;
      dword_10051060 = (LPVOID)6766380;
      dword_10051064 = 15960680;
      dword_10051068 = 15965424;
      dword_1005106C = (LPVOID)4356392;
      dword_10051070 = (int (*)(void))4363042;
      dword_10051248 = 4235409;
      goto LABEL_15;
    case 4u:
      dword_10050658 = 14434576;
      lpAddress = (LPVOID)6704592;
      dword_10050678 = 4280048;
      dword_10050694 = (int (*)(void))6851558;
      dword_10050698 = 6685456;
      dword_1005069C = (LPVOID)7200768;
      dword_100506A0 = (int (__cdecl *)(_DWORD))7235920;
      dword_100506A4 = (LPVOID)7203029;
      dword_100506A8 = (LPVOID)7206571;
      dword_100506AC = (LPVOID)7205998;
      dword_100506B0 = (LPVOID)7206395;
      dword_100506B4 = (LPVOID)7206483;
      dword_100506B8 = (LPVOID)7206707;
      dword_100506BC = (LPVOID)7206746;
      dword_100506C0 = (LPVOID)7206839;
      dword_100506C4 = (LPVOID)7207116;
      dword_100506C8 = (LPVOID)7207485;
      dword_100506CC = 6743521;
      dword_100506D0 = 10094072;
      dword_100506D4 = 7817120;
      dword_10050710 = 6851638;
      dword_10051020 = 7386290;
      dword_10051024 = (LPVOID)7209922;
      dword_10051028 = 9751088;
      dword_1005102C = 4231171;
      dword_10051038 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6708538;
      dword_1005103C = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6756066;
      dword_10051040 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))7022409;
      dword_10051044 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD))6869592;
      dword_10051048 = (int (__cdecl *)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD))6706995;
      dword_1005104C = (int (__cdecl *)(_DWORD))6798331;
      dword_10051050 = 6736859;
      dword_10051058 = (LPVOID)7022176;
      dword_1005105C = (LPVOID)7022272;
      dword_10051060 = (LPVOID)6766332;
      dword_10051064 = 15967560;
      dword_10051068 = 15972304;
      dword_1005106C = (LPVOID)4356408;
      dword_10051070 = (int (*)(void))4363058;
      dword_10051248 = 4235425;
      goto LABEL_15;
    case 0u:
      exit_0(1);
  }
  if ( v3 >= 5 && v3 != 20 )
    dword_1004CB78 = 1;
LABEL_15:
  SetUnhandledExceptionFilter(TopLevelExceptionFilter);
  SetThreadExecutionState(0x80000003);
  switch ( dword_10050624 )
  {
    case 1:
    case 3:
    case 20:
      dword_10050708 = 4241120;
      break;
    case 2:
    case 4:
      dword_10050708 = 4241136;
      break;
    default:
      break;
  }
  if ( dword_1004CB78 )
    dword_10050708 = MEMORY[0x400128] + 0x400000;
  QueryPerformanceFrequency(&Frequency);
  if ( dword_1004CB78 )
  {
    v2 = a1;
    v1 = 0;
    v30 = a1;
    v4 = sub_10008890(a1);
  }
  else
  {
    v4 = sub_10007120((int)v1);
  }
  v5 = (unsigned __int8 *)lpAddress;
  v32 = v4;
  VirtualProtect(lpAddress, 5u, 0x40u, &flOldProtect);
  v6 = dword_1004CC50;
  dword_1004E620[dword_1004CC50] = *v5;
  ++v6;
  dword_1004E620[v6++] = *(_DWORD *)(v5 + 1);
  dword_1004E620[v6] = (int)v5;
  dword_1004CC50 = v6 + 1;
  v7 = dword_1004CB78 == 0;
  *v5 = -23;
  *(_DWORD *)(v5 + 1) = (char *)sub_10008C80 - (char *)v5 - 5;
  if ( v7 )
  {
    v8 = v1[597];
    v9 = v1[598];
    v10 = (HWND)v1[23];
  }
  else
  {
    v8 = v2[677];
    v9 = v2[678];
    v10 = (HWND)v2[23];
  }
  dword_10050620 = v8;
  dword_10051D80 = v9;
  v11 = nWidth;
  hWnd = v10;
  if ( !nWidth || (v12 = nHeight) == 0 )
  {
    v11 = v8;
    v12 = v9;
    nWidth = v8;
    nHeight = v9;
  }
  if ( dword_1004AF1C )
  {
    memset(&DevMode, 0, sizeof(DevMode));
    DevMode.dmSize = 156;
    DevMode.dmPelsWidth = v11;
    DevMode.dmPelsHeight = v12;
    DevMode.dmBitsPerPel = 32;
    DevMode.dmFields = 1835008;
    if ( dword_1004CB5C )
    {
      DevMode.dmDisplayFrequency = dword_1004CB5C;
      DevMode.dmFields = 6029312;
    }
    if ( ChangeDisplaySettingsExA(0, &DevMode, 0, 4u, 0) )
    {
      dword_1004AF1C = 0;
      nWidth = dword_10050620;
      nHeight = dword_10051D80;
    }
    MoveWindow(hWnd, X, Y, nWidth, nHeight, 0);
    if ( dword_1004CB78 )
      v13 = (const CHAR *)v30[701];
    else
      v13 = (const CHAR *)v1[621];
    SetWindowTextA(hWnd, v13);
    if ( dword_1004AF1C )
      goto LABEL_48;
    v11 = nWidth;
    v12 = nHeight;
  }
  Rect.left = 0;
  Rect.top = 0;
  Rect.right = v11;
  Rect.bottom = v12;
  DestroyWindow(hWnd);
  if ( !AdjustWindowRectEx(&Rect, 0xCA0000u, 0, 0) )
    sub_10008D10();
  if ( dword_1004CB78 )
  {
    v14 = (HINSTANCE)v30[22];
    v15 = (const CHAR *)v30[701];
    v16 = (const CHAR *)v30[702];
  }
  else
  {
    v14 = (HINSTANCE)v1[22];
    v15 = (const CHAR *)v1[621];
    v16 = (const CHAR *)v1[622];
  }
  Window = CreateWindowExA(
             0,
             v16,
             v15,
             0xCA0000u,
             0x80000000,
             0x80000000,
             Rect.right - Rect.left,
             Rect.bottom - Rect.top,
             0,
             0,
             v14,
             0);
  hWnd = Window;
  if ( !Window )
  {
    sub_10008D10();
    Window = hWnd;
  }
  ShowWindow(Window, 5);
  if ( !dword_1004CB78 )
  {
    v1[23] = hWnd;
    goto LABEL_51;
  }
  v30[23] = hWnd;
LABEL_48:
  if ( dword_1004CB78 )
  {
    v18 = (HINSTANCE)v30[22];
    goto LABEL_52;
  }
LABEL_51:
  v18 = (HINSTANCE)v1[22];
LABEL_52:
  IconA = LoadIconA(v18, (LPCSTR)0x65);
  SendMessageA(hWnd, 0x80u, 0, (LPARAM)IconA);
  SendMessageA(hWnd, 0x80u, 1u, (LPARAM)IconA);
  sub_10005000();
  if ( (byte_10050F1C & 2) != 0 )
    dword_1004A598 = 0;
  v20 = nWidth;
  dword_1004E5F8 = dword_10050F38;
  dword_10050908 = nWidth;
  dword_10050628 = nHeight;
  if ( dword_1004AF18 )
  {
    v21 = 4 * nHeight;
    v22 = 3 * nWidth;
    if ( 4 * nHeight != 3 * nWidth )
    {
      if ( 4 * nHeight <= (unsigned int)(3 * nWidth) )
      {
        if ( v22 > v21 )
        {
          v20 = v21 / 3;
          dword_1004CB7C = (nWidth - v21 / 3) >> 1;
          dword_10050908 = v21 / 3;
        }
      }
      else
      {
        dword_1004CB80 = (nHeight - (v22 >> 2)) >> 1;
        dword_10050628 = v22 >> 2;
      }
    }
  }
  v23 = dword_10050620;
  v24 = 1;
  v25 = 1;
  if ( !dword_1004CB60 )
  {
    v24 = dword_1004AF20 && v20 % dword_10050620 ? v20 / dword_10050620 + 1 : v20 / dword_10050620;
    if ( !v24 )
      v24 = 1;
  }
  v26 = dword_1004CB64;
  if ( !dword_1004CB64 )
  {
    v25 = dword_1004AF20 && dword_10050628 % (unsigned int)dword_10051D80
        ? dword_10050628 / (unsigned int)dword_10051D80 + 1
        : dword_10050628 / (unsigned int)dword_10051D80;
    if ( !v25 )
      v25 = 1;
  }
  v27 = dword_1004CB60;
  if ( !dword_1004CB60 && !dword_1004CB64 )
  {
    if ( v24 <= v25 )
      v25 = v24;
    else
      v24 = v25;
    v23 = v24 * dword_10050620;
    v27 = v24 * dword_10050620;
    v26 = dword_10051D80 * v25;
    dword_1004CB60 = v24 * dword_10050620;
    dword_1004CB64 = dword_10051D80 * v25;
  }
  if ( dword_1004AF38 )
  {
    v27 = 640;
    v26 = 480;
    dword_1004CB60 = 640;
    dword_1004CB64 = 480;
    dword_1004CB70 = 0;
  }
  if ( v27 != dword_10050908 || v26 != dword_10050628 )
    dword_1004CB84 = 1;
  if ( !sub_1000C780(v23, v24, v29) )
    exit_0(-1);
  if ( !dword_1004CB78 )
  {
    sub_10009CA0();
    if ( strlen((const char *)dword_10051D8C) )
      sub_1000AB30();
  }
  if ( strlen(lpLibFileName) )
    LoadLibraryA(lpLibFileName);
  sub_10016B40();
  return v32;
}
// 10005E94: variable 'v29' is possibly undefined
// 1004A598: using guessed type int dword_1004A598;
// 1004AF18: using guessed type int dword_1004AF18;
// 1004AF1C: using guessed type int dword_1004AF1C;
// 1004AF20: using guessed type int dword_1004AF20;
// 1004AF38: using guessed type int dword_1004AF38;
// 1004CB5C: using guessed type int dword_1004CB5C;
// 1004CB60: using guessed type int dword_1004CB60;
// 1004CB64: using guessed type int dword_1004CB64;
// 1004CB70: using guessed type int dword_1004CB70;
// 1004CB78: using guessed type int dword_1004CB78;
// 1004CB7C: using guessed type int dword_1004CB7C;
// 1004CB80: using guessed type int dword_1004CB80;
// 1004CB84: using guessed type int dword_1004CB84;
// 1004CC50: using guessed type int dword_1004CC50;
// 1004E5F8: using guessed type int dword_1004E5F8;
// 1004E620: using guessed type int dword_1004E620[];
// 10050620: using guessed type int dword_10050620;
// 10050624: using guessed type int dword_10050624;
// 10050628: using guessed type int dword_10050628;
// 10050658: using guessed type int dword_10050658;
// 10050678: using guessed type int dword_10050678;
// 10050694: using guessed type int (*dword_10050694)(void);
// 10050698: using guessed type int dword_10050698;
// 100506A0: using guessed type int (__cdecl *dword_100506A0)(_DWORD);
// 100506CC: using guessed type int dword_100506CC;
// 100506D0: using guessed type int dword_100506D0;
// 100506D4: using guessed type int dword_100506D4;
// 10050708: using guessed type int dword_10050708;
// 10050710: using guessed type int dword_10050710;
// 10050908: using guessed type int dword_10050908;
// 10050F1C: using guessed type char byte_10050F1C;
// 10050F38: using guessed type int dword_10050F38;
// 10051020: using guessed type int dword_10051020;
// 10051028: using guessed type int dword_10051028;
// 1005102C: using guessed type int dword_1005102C;
// 10051038: using guessed type int (__cdecl *dword_10051038)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD);
// 1005103C: using guessed type int (__cdecl *dword_1005103C)(_DWORD, _DWORD, _DWORD);
// 10051040: using guessed type int (__cdecl *dword_10051040)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD);
// 10051044: using guessed type int (__cdecl *dword_10051044)(_DWORD, _DWORD, _DWORD);
// 10051048: using guessed type int (__cdecl *dword_10051048)(_DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD, _DWORD);
// 1005104C: using guessed type int (__cdecl *dword_1005104C)(_DWORD);
// 10051050: using guessed type int dword_10051050;
// 10051064: using guessed type int dword_10051064;
// 10051068: using guessed type int dword_10051068;
// 10051070: using guessed type int (*dword_10051070)(void);
// 10051248: using guessed type int dword_10051248;
// 10051D80: using guessed type int dword_10051D80;
// 10051D8C: using guessed type int dword_10051D8C;


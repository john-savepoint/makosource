#!/usr/bin/env python3
"""
Find SDF parameter addresses in FFNx.dll
Outputs the memory addresses for real-time editing tools.
"""

import sys
import ctypes
from ctypes import wintypes
import struct

# Windows API
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010

class MODULEINFO(ctypes.Structure):
    _fields_ = [
        ("lpBaseOfDll", wintypes.LPVOID),
        ("SizeOfImage", wintypes.DWORD),
        ("EntryPoint", wintypes.LPVOID),
    ]

def find_process_by_name(name):
    """Find process ID by name"""
    import subprocess
    result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {name}', '/FO', 'CSV', '/NH'],
                          capture_output=True, text=True, shell=True)
    if name.lower() in result.stdout.lower():
        pid = int(result.stdout.split(',')[1].strip('"'))
        return pid
    return None

def get_module_base(process_handle, module_name):
    """Get base address of a loaded DLL"""
    hModules = (wintypes.HMODULE * 1024)()
    cbNeeded = wintypes.DWORD()

    if not psapi.EnumProcessModules(process_handle, hModules, ctypes.sizeof(hModules), ctypes.byref(cbNeeded)):
        return None

    module_count = cbNeeded.value // ctypes.sizeof(wintypes.HMODULE)

    for i in range(module_count):
        module_name_buf = ctypes.create_unicode_buffer(260)
        psapi.GetModuleBaseNameW(process_handle, hModules[i], module_name_buf, 260)

        if module_name.lower() in module_name_buf.value.lower():
            modinfo = MODULEINFO()
            if psapi.GetModuleInformation(process_handle, hModules[i], ctypes.byref(modinfo), ctypes.sizeof(modinfo)):
                return modinfo.lpBaseOfDll, modinfo.SizeOfImage

    return None, None

def read_memory(process_handle, address, size):
    """Read memory from process"""
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    if kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read)):
        return buffer.raw
    return None

def scan_for_sdf_values(process_handle, base_address, size, target_values):
    """Scan DLL memory for SDF parameter values"""
    print(f"\nScanning FFNx.dll (base: 0x{base_address:X}, size: {size:,} bytes)")
    print(f"Looking for values: {target_values}")

    # Read entire DLL into memory
    chunk_size = 0x10000  # 64KB chunks
    found_addresses = {k: [] for k in target_values.keys()}

    for offset in range(0, size, chunk_size):
        data = read_memory(process_handle, base_address + offset, min(chunk_size, size - offset))
        if not data:
            continue

        # Search for each float value
        for name, value in target_values.items():
            pattern = struct.pack('f', value)
            pos = 0
            while True:
                pos = data.find(pattern, pos)
                if pos == -1:
                    break
                address = base_address + offset + pos
                found_addresses[name].append(address)
                pos += 4

    return found_addresses

def main():
    print("=== FFNx SDF Parameter Address Finder ===\n")

    # Find FF7 process
    pid = find_process_by_name("ff7_en.exe")
    if not pid:
        print("ERROR: ff7_en.exe not running!")
        print("Please start FF7 first.")
        return 1

    print(f"Found FF7 process (PID: {pid})")

    # Open process
    process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not process_handle:
        print("ERROR: Failed to open process. Run as Administrator?")
        return 1

    # Find FFNx.dll
    base_address, dll_size = get_module_base(process_handle, "FFNx.dll")
    if not base_address:
        # Try alternative name
        base_address, dll_size = get_module_base(process_handle, "AF3DN.P")

    if not base_address:
        print("ERROR: FFNx.dll not found in process!")
        kernel32.CloseHandle(process_handle)
        return 1

    print(f"Found FFNx.dll at 0x{base_address:X}")

    # Define target values (read from FFNx.toml or use defaults)
    target_values = {
        'sdf_pixel_range': 4.0,
        'sdf_thickness': 0.7,
        'sdf_shadow_offset': 2.0,
        'sdf_shadow_opacity': 0.7,
    }

    # Scan for values
    found = scan_for_sdf_values(process_handle, base_address, dll_size, target_values)

    # Display results
    print("\n" + "="*70)
    print("FOUND ADDRESSES:")
    print("="*70)

    for name, addresses in found.items():
        if addresses:
            print(f"\n{name} ({target_values[name]}):")
            for addr in addresses[:5]:  # Show first 5 matches
                print(f"  0x{addr:X}")
            if len(addresses) > 5:
                print(f"  ... and {len(addresses) - 5} more")
        else:
            print(f"\n{name}: NOT FOUND (try changing value in FFNx.toml and rescanning)")

    print("\n" + "="*70)
    print("USAGE:")
    print("="*70)
    print("Copy these addresses to your memory editing tool.")
    print("If multiple addresses are shown, test each one to find the correct one.")
    print("The correct address will change the text appearance when modified.")

    kernel32.CloseHandle(process_handle)
    return 0

if __name__ == "__main__":
    sys.exit(main())

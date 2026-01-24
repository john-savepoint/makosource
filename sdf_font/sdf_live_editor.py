#!/usr/bin/env python3
"""
Live SDF Font Parameter Editor
Adjusts SDF font rendering parameters in real-time while FF7 is running.
"""

import sys
import struct
import ctypes
from ctypes import wintypes
import time

# Windows API functions
kernel32 = ctypes.windll.kernel32
PROCESS_ALL_ACCESS = 0x1F0FFF

class MemoryEditor:
    def __init__(self, process_name="ff7_en.exe"):
        self.process_name = process_name
        self.process_handle = None
        self.base_address = None
        
    def find_process(self):
        """Find FF7 process ID"""
        import subprocess
        result = subprocess.run(['tasklist', '/FI', f'IMAGENAME eq {self.process_name}', '/FO', 'CSV', '/NH'], 
                              capture_output=True, text=True)
        if self.process_name.lower() in result.stdout.lower():
            # Parse PID from output
            pid = int(result.stdout.split(',')[1].strip('"'))
            return pid
        return None
    
    def open_process(self, pid):
        """Open process for memory access"""
        self.process_handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return self.process_handle != 0
    
    def read_float(self, address):
        """Read float from memory"""
        buffer = ctypes.c_float()
        bytes_read = ctypes.c_size_t()
        kernel32.ReadProcessMemory(self.process_handle, ctypes.c_void_p(address), 
                                   ctypes.byref(buffer), ctypes.sizeof(buffer), 
                                   ctypes.byref(bytes_read))
        return buffer.value
    
    def write_float(self, address, value):
        """Write float to memory"""
        buffer = ctypes.c_float(value)
        bytes_written = ctypes.c_size_t()
        result = kernel32.WriteProcessMemory(self.process_handle, ctypes.c_void_p(address), 
                                            ctypes.byref(buffer), ctypes.sizeof(buffer), 
                                            ctypes.byref(bytes_written))
        return result != 0
    
    def scan_for_floats(self, target_values, tolerance=0.01):
        """Scan memory for specific float values (SDF parameters)"""
        print(f"Scanning for values: {target_values}")
        print("This may take a while...")
        # Note: This is a simplified scan. For production, use Cheat Engine or similar tools
        # to find the actual addresses, then hardcode them here
        return None
    
    def close(self):
        if self.process_handle:
            kernel32.CloseHandle(self.process_handle)

def interactive_editor():
    """Interactive editor for SDF parameters"""
    print("=== FF7 SDF Font Live Editor ===")
    print("\nSearching for FF7 process...")
    
    editor = MemoryEditor()
    pid = editor.find_process()
    
    if not pid:
        print(f"ERROR: {editor.process_name} not found!")
        print("Make sure FF7 is running.")
        return
    
    print(f"Found FF7 (PID: {pid})")
    
    if not editor.open_process(pid):
        print("ERROR: Failed to open process. Run as Administrator?")
        return
    
    print("\n" + "="*60)
    print("IMPORTANT: You need to find the memory addresses first!")
    print("="*60)
    print("\nUse Cheat Engine to find these addresses:")
    print("1. Search for float value: 4.0 (sdf_pixel_range)")
    print("2. Search for float value: 0.7 (sdf_thickness)")
    print("3. Search for float value: 2.0 (sdf_shadow_offset)")
    print("4. Search for float value: 0.7 (sdf_shadow_opacity)")
    print("\nOnce found, edit the addresses below in this script.")
    print("\nFor now, use FFNx.toml and restart the game to test values.")
    
    editor.close()

if __name__ == "__main__":
    try:
        interactive_editor()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

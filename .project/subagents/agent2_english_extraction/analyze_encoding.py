#!/usr/bin/env python3
"""
Analyze FF7 English strings to determine ASCII vs FF7 encoding
"""
import re

def is_ascii_encoded(hex_bytes):
    """Check if hex bytes are direct ASCII encoding"""
    bytes_list = hex_bytes.strip().split()
    if not bytes_list:
        return False

    # Check if bytes directly map to ASCII
    try:
        ascii_text = ''.join(chr(int(b, 16)) for b in bytes_list if int(b, 16) != 0 and int(b, 16) != 0xFF)
        # If most chars are printable ASCII, it's ASCII encoded
        printable = sum(1 for c in ascii_text if 32 <= ord(c) <= 126)
        return printable / len(ascii_text) > 0.8 if ascii_text else False
    except:
        return False

# Read input file
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt', 'r') as f:
    lines = f.readlines()

# Process and write output
with open('/home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index_v2.txt', 'w') as out:
    for line in lines:
        if line.startswith('['):
            # Parse the line
            match = re.match(r'(\[\d+\]\s+0x[0-9A-F]+\s+\d+)\s+(DEF|RGB|EXCLUDED)(\s+\|.+\|)(.+)', line)
            if match:
                prefix = match.group(1)
                old_type = match.group(2)
                middle = match.group(3)
                hex_part = match.group(4).strip()

                # Determine encoding
                if old_type == "EXCLUDED":
                    encoding = "FF7"
                elif old_type == "RGB":
                    encoding = "ASCII"
                else:  # DEF
                    if is_ascii_encoded(hex_part):
                        encoding = "ASCII"
                    else:
                        encoding = "FF7"

                # Write new format
                out.write(f"{prefix} {old_type:8} {encoding:5}{middle}{hex_part}\n")
            else:
                out.write(line)
        else:
            out.write(line)

print("Created english_strings_by_index_v2.txt with encoding types")

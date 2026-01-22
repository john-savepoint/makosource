#!/bin/bash
# Run expanded Haiku analysis
cd /home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent_german_full_extraction

head -300 german_menu_region.txt > /tmp/german_chunk1.txt
head -200 /home/johnzealanddoyle/projects/ff7OG_japanese/.project/subagents/agent2_english_extraction/english_strings_by_index.txt > /tmp/english_chunk1.txt

GERMAN=$(cat /tmp/german_chunk1.txt)
ENGLISH=$(cat /tmp/english_chunk1.txt)

/home/johnzealanddoyle/.local/bin/claude --model haiku --dangerously-skip-permissions -p "
Map FF7 English menu strings to German strings. Find the German equivalent for each English string based on meaning.

GERMAN STRINGS (offset | text):
$GERMAN

ENGLISH STRINGS (index, offset, length, type | text):
$ENGLISH

Output ONLY a CSV with: index,de_offset,de_text
Map as many strings as possible. Skip keyboard/RGB strings (indices 77-213, they are universal).
" > haiku_analysis/expanded_mapping1.csv 2>&1

echo "Done. Check haiku_analysis/expanded_mapping1.csv"

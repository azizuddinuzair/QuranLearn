
import csv
import sys
import re
from pathlib import Path

input_path = Path(__file__).parent.parent / 'data' / 'ayahs' / 'English.csv'
output_path = Path(__file__).parent.parent / 'data' / 'ayahs' / 'English_clean.csv'

def try_open_encodings(path, encodings):
    for enc in encodings:
        try:
            with open(path, encoding=enc) as f:
                for _ in range(10):
                    f.readline()
                f.seek(0)
            return enc
        except UnicodeDecodeError:
            continue
    return None

encodings_to_try = ['utf-8-sig', 'utf-8', 'latin-1']
encoding_found = try_open_encodings(str(input_path), encodings_to_try)
if encoding_found:
    with open(str(input_path), encoding=encoding_found) as infile, open(str(output_path), 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['surah', 'ayah', 'translation'])
        for line in infile:
            line = line.strip()
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            parts = line.split('|', 2)
            if len(parts) >= 3:
                surah = parts[0].strip().strip('"')
                ayah = parts[1].strip().strip('"')
                translation = parts[2].strip().strip('"')
                # Remove trailing commas and whitespace using regex
                translation = re.sub(r'[\s,]+$', '', translation)
                # Try to convert to int, but if it fails, keep as string
                try:
                    surah = int(surah)
                except ValueError:
                    pass
                try:
                    ayah = int(ayah)
                except ValueError:
                    pass
                writer.writerow([surah, ayah, translation])
else:
    with open(str(input_path), 'rb') as infile, open(str(output_path), 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['surah', 'ayah', 'translation'])
        for bline in infile:
            for enc in encodings_to_try:
                try:
                    line = bline.decode(enc).strip()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                continue
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            parts = line.split('|', 2)
            if len(parts) >= 3:
                surah = parts[0].strip().strip('"')
                ayah = parts[1].strip().strip('"')
                translation = parts[2].strip().strip('"')
                # Remove trailing commas and whitespace using regex
                translation = re.sub(r'[\s,]+$', '', translation)
                try:
                    surah = int(surah)
                except ValueError:
                    pass
                try:
                    ayah = int(ayah)
                except ValueError:
                    pass
                writer.writerow([surah, ayah, translation])

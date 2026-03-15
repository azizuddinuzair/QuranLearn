import sys
from pathlib import Path
import csv
sys.path.insert(0, str(Path(__file__).parents[2] / 'src'))
from loader import load_ayah_translations

def get_word_ayah_pairs(words_csv_path):
    pairs = set()
    with open(words_csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                surah = int(row['surah_id'])
                ayah = int(row['ayah_id'])
                pairs.add((surah, ayah))
            except Exception:
                continue
    return pairs

def main():
    base = Path(__file__).parents[2]
    words_csv = base / 'data' / 'words' / 'quran_words.csv'
    ayahs_csv = base / 'data' / 'ayahs' / 'English_clean.csv'
    word_pairs = get_word_ayah_pairs(words_csv)
    ayah_map = load_ayah_translations(ayahs_csv)
    ayah_pairs = set(ayah_map.keys())

    missing = word_pairs - ayah_pairs
    print(f"Total word ayah pairs: {len(word_pairs)}")
    print(f"Total ayah translations: {len(ayah_pairs)}")
    print(f"Missing translations: {len(missing)}")
    if missing:
        print("Sample missing pairs:")
        for i, (s, a) in enumerate(sorted(missing)):
            print(f"  Surah {s}, Ayah {a}")
            if i >= 19:
                print("  ...")
                break
    else:
        print("All ayah pairs have translations!")

if __name__ == "__main__":
    main()
import sys
from pathlib import Path
import csv
sys.path.insert(0, str(Path(__file__).parents[2] / 'src'))
from loader import load_ayah_translations

def get_word_ayah_pairs(words_csv_path):
    pairs = set()
    with open(words_csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                surah = int(row['surah_id'])
                ayah = int(row['ayah_id'])
                pairs.add((surah, ayah))
            except Exception:
                continue
    return pairs

def main():
    base = Path(__file__).parents[2]
    words_csv = base / 'data' / 'words' / 'quran_words.csv'
    ayahs_csv = base / 'data' / 'ayahs' / 'English_clean.csv'
    word_pairs = get_word_ayah_pairs(words_csv)
    ayah_map = load_ayah_translations(ayahs_csv)
    ayah_pairs = set(ayah_map.keys())

    missing = word_pairs - ayah_pairs
    print(f"Total word ayah pairs: {len(word_pairs)}")
    print(f"Total ayah translations: {len(ayah_pairs)}")
    print(f"Missing translations: {len(missing)}")
    if missing:
        print("Sample missing pairs:")
        for i, (s, a) in enumerate(sorted(missing)):
            print(f"  Surah {s}, Ayah {a}")
            if i >= 19:
                print("  ...")
                break
    else:
        print("All ayah pairs have translations!")

if __name__ == "__main__":
    main()

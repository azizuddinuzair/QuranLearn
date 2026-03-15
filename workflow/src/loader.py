import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple

# For progress/phase model
from .models import WordPhase

import sys


def load_words_csv(csv_path: Path) -> List[Dict[str, Any]]:
    """Legacy: Load words as list of dicts."""
    try:
        with csv_path.open(encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
        return data
    except Exception as e:
        print(f"[Error] Failed to load words CSV: {e}")
        return []

def load_wordphases(csv_path: Path, phase_size: int = 500) -> List[WordPhase]:
    """
    Load words as WordPhase objects, assigning phase by frequency order.
    phase_size: number of words per phase (e.g., 500 = top 500 = phase 1, next 500 = phase 2, ...)
    """
    try:
        with csv_path.open(encoding='utf-8') as f:
            reader = csv.DictReader(f)
            words = [row for row in reader]
        wordphases = []
        for i, w in enumerate(words):
            try:
                phase = 1 + (i // phase_size)
                wordphases.append(WordPhase(
                    word=w.get('word_ar', ''),
                    translit=w.get('word_tr', ''),
                    meaning=w.get('word_en', ''),
                    surah_id=int(w.get('surah_id', 0)),
                    ayah_id=int(w.get('ayah_id', 0)),
                    phase=phase
                ))
            except Exception as e:
                print(f"[Error] Skipping word row: {e}")
        return wordphases
    except Exception as e:
        print(f"[Error] Failed to load words as WordPhase: {e}")
        return []

def load_ayah_translations(ayah_csv_path: Path) -> Dict[Tuple[str, str], str]:
    ayah_map = {}
    import csv
    ayah_map = {}
    try:
        def process_file(f):
            for line in f:
                if line.strip() == '':
                    continue
                if line.startswith('surah'):
                    continue
                parts = list(csv.reader([line]))[0]
                if len(parts) < 3:
                    continue
                surah, ayah, translation = parts[0], parts[1], parts[2]
                try:
                    surah = int(surah)
                    ayah = int(ayah)
                except ValueError:
                    continue  # skip if surah/ayah is not int
                ayah_map[(surah, ayah)] = translation
        try:
            with ayah_csv_path.open(encoding='utf-8') as f:
                process_file(f)
        except UnicodeDecodeError:
            with ayah_csv_path.open(encoding='latin-1') as f:
                process_file(f)
        return ayah_map
    except Exception as e:
        print(f"[Error] Failed to load ayah translations: {e}")
        return {}

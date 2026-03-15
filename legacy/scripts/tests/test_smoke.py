import sys
from pathlib import Path
import sqlite3
import json
from datetime import date

# Add src to path for relative imports

# Import modules as workflow.src.<module>
from workflow.src.models import WordPhase
from workflow.src.progress import save_progress, load_progress
from workflow.src.progress_db import init_db, save_progress_db, load_progress_db
from workflow.src.metrics import get_phase_metrics, get_ayahs_mastered, get_daily_streaks, get_quiz_performance
from workflow.src.surah_progress import init_surah_progress_table, update_surah_progress, get_surah_progress


def test_wordphase_progress():
    print("[WordPhase/Progress] ...", end=' ')
    words = [
        WordPhase(word="قَالَ", translit="qaala", meaning="he said", surah_id=2, ayah_id=30, phase=1),
        WordPhase(word="اللَّهُ", translit="allahu", meaning="Allah", surah_id=1, ayah_id=1, phase=1, learned=True, first_seen=date.today(), review_count=2, quiz_correct=3, last_seen=date.today()),
    ]
    path = Path("progress_test.json")
    save_progress(words, path)
    loaded = load_progress(path)
    assert len(loaded) == 2
    print("PASS")

def test_db_progress():
    print("[DB Progress] ...", end=' ')
    db_path = Path("progress_test.db")
    init_db(db_path)
    words = [
        WordPhase(word="قَالَ", translit="qaala", meaning="he said", surah_id=2, ayah_id=30, phase=1),
        WordPhase(word="اللَّهُ", translit="allahu", meaning="Allah", surah_id=1, ayah_id=1, phase=1, learned=True, first_seen=date.today(), review_count=2, quiz_correct=3, last_seen=date.today()),
    ]
    save_progress_db(words, db_path)
    loaded = load_progress_db(db_path)
    assert len(loaded) == 2
    print("PASS")

def test_metrics():
    print("[Metrics] ...", end=' ')
    db_path = Path("progress_test.db")
    phase_metrics = get_phase_metrics(db_path)
    ayahs_mastered = get_ayahs_mastered(db_path)
    streaks = get_daily_streaks(db_path)
    quiz_perf = get_quiz_performance(db_path)
    assert isinstance(phase_metrics, dict)
    assert isinstance(ayahs_mastered, int)
    assert isinstance(streaks, dict)
    assert isinstance(quiz_perf, dict)
    print("PASS")

def test_surah_progress():
    print("[SurahProgress] ...", end=' ')
    db_path = Path("progress_test.db")
    init_surah_progress_table(db_path)
    surah_no = 1
    total_ayahs = 7
    ayah_progress = {str(i): "not_seen" for i in range(1, 8)}
    update_surah_progress(db_path, surah_no, total_ayahs, ayah_progress, date.today().isoformat())
    sp = get_surah_progress(db_path, surah_no)
    assert sp['total_ayahs'] == 7
    assert sp['ayah_progress']['1'] == "not_seen"
    print("PASS")

if __name__ == "__main__":
    test_wordphase_progress()
    test_db_progress()
    test_metrics()
    test_surah_progress()
    print("All smoke tests passed.")

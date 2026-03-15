import sqlite3
from pathlib import Path
from datetime import date
import json

def get_db_connection(db_path: Path):
    return sqlite3.connect(str(db_path))

def init_surah_progress_table(db_path: Path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS surah_progress (
            surah_no INTEGER PRIMARY KEY,
            total_ayahs INTEGER,
            ayah_progress TEXT,
            last_studied TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_surah_progress(db_path: Path, surah_no: int):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('SELECT total_ayahs, ayah_progress, last_studied FROM surah_progress WHERE surah_no=?', (surah_no,))
    row = c.fetchone()
    conn.close()
    if row:
        total_ayahs, ayah_progress, last_studied = row
        ayah_progress = json.loads(ayah_progress) if ayah_progress else {}
        return {
            'surah_no': surah_no,
            'total_ayahs': total_ayahs,
            'ayah_progress': ayah_progress,
            'last_studied': last_studied
        }
    return None

def update_surah_progress(db_path: Path, surah_no: int, total_ayahs: int, ayah_progress: dict, last_studied: str = None):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO surah_progress (surah_no, total_ayahs, ayah_progress, last_studied)
        VALUES (?, ?, ?, ?)
    ''', (surah_no, total_ayahs, json.dumps(ayah_progress), last_studied))
    conn.commit()
    conn.close()

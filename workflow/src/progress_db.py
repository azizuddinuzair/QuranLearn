import sqlite3
from pathlib import Path
from .models import WordPhase
from datetime import date

def get_db_connection(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    return conn

def init_db(db_path: Path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            word TEXT,
            translit TEXT,
            meaning TEXT,
            surah_id INTEGER,
            ayah_id INTEGER,
            phase INTEGER,
            learned INTEGER,
            first_seen TEXT,
            review_count INTEGER,
            quiz_correct INTEGER,
            last_seen TEXT,
            PRIMARY KEY (word, surah_id, ayah_id)
        )
    ''')
    conn.commit()
    conn.close()

def save_progress_db(progress: list[WordPhase], db_path: Path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    for wp in progress:
        c.execute('''
            INSERT OR REPLACE INTO progress VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            wp.word, wp.translit, wp.meaning, wp.surah_id, wp.ayah_id, wp.phase,
            int(wp.learned),
            wp.first_seen.isoformat() if wp.first_seen else None,
            wp.review_count, wp.quiz_correct,
            wp.last_seen.isoformat() if wp.last_seen else None
        ))
    conn.commit()
    conn.close()

def load_progress_db(db_path: Path) -> list[WordPhase]:
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM progress')
    rows = c.fetchall()
    conn.close()
    progress = []
    for row in rows:
        progress.append(WordPhase(
            word=row[0], translit=row[1], meaning=row[2],
            surah_id=row[3], ayah_id=row[4], phase=row[5],
            learned=bool(row[6]),
            first_seen=date.fromisoformat(row[7]) if row[7] else None,
            review_count=row[8], quiz_correct=row[9],
            last_seen=date.fromisoformat(row[10]) if row[10] else None
        ))
    return progress

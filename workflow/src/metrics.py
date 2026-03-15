import sqlite3
from pathlib import Path
from datetime import date, datetime
from typing import Dict, Any

def get_db_connection(db_path: Path):
    return sqlite3.connect(str(db_path))

def get_phase_metrics(db_path: Path) -> Dict[int, Dict[str, Any]]:
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute("SELECT phase, COUNT(*), SUM(learned), SUM(quiz_correct), SUM(review_count) FROM progress GROUP BY phase")
    rows = c.fetchall()
    conn.close()
    metrics = {}
    for phase, total, learned, quiz_correct, review_count in rows:
        metrics[phase] = {
            'total': total,
            'learned': learned or 0,
            'quiz_correct': quiz_correct or 0,
            'review_count': review_count or 0,
        }
    return metrics

def get_ayahs_mastered(db_path: Path) -> int:
    conn = get_db_connection(db_path)
    c = conn.cursor()
    # An ayah is mastered if all words in it are learned
    c.execute('''
        SELECT surah_id, ayah_id, MIN(learned) as all_learned
        FROM progress
        GROUP BY surah_id, ayah_id
        HAVING all_learned = 1
    ''')
    rows = c.fetchall()
    conn.close()
    return len(rows)

def get_daily_streaks(db_path: Path) -> Dict[str, int]:
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT last_seen FROM progress WHERE last_seen IS NOT NULL
    ''')
    dates = [row[0] for row in c.fetchall()]
    conn.close()
    # Count unique days with activity
    days = set(dates)
    streak = 0
    today = date.today()
    for i in range(0, 365):
        d = today.fromordinal(today.toordinal() - i)
        if d.isoformat() in days:
            streak += 1
        else:
            break
    return {'current_streak': streak, 'active_days': len(days)}

def get_quiz_performance(db_path: Path) -> Dict[str, Any]:
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute('''
        SELECT SUM(quiz_correct), SUM(review_count), COUNT(*) FROM progress
    ''')
    quiz_correct, review_count, total = c.fetchone()
    conn.close()
    accuracy = (quiz_correct or 0) / (review_count or 1) * 100
    return {
        'quiz_correct': quiz_correct or 0,
        'review_count': review_count or 0,
        'accuracy': accuracy,
        'total_words': total
    }

import json
from pathlib import Path
from typing import Dict, List
from .models import WordPhase
from datetime import date

def wordphase_to_dict(wp: WordPhase) -> dict:
    # Convert WordPhase to dict for JSON serialization
    d = wp.__dict__.copy()
    # Convert date fields to isoformat
    if d['first_seen']:
        d['first_seen'] = d['first_seen'].isoformat()
    if d['last_seen']:
        d['last_seen'] = d['last_seen'].isoformat()
    return d

def wordphase_from_dict(d: dict) -> WordPhase:
    # Convert dict to WordPhase, parsing date fields
    if d.get('first_seen'):
        d['first_seen'] = date.fromisoformat(d['first_seen'])
    if d.get('last_seen'):
        d['last_seen'] = date.fromisoformat(d['last_seen'])
    return WordPhase(**d)

def save_progress(progress: List[WordPhase], path: Path):
    with path.open('w', encoding='utf-8') as f:
        json.dump([wordphase_to_dict(wp) for wp in progress], f, ensure_ascii=False, indent=2)

def load_progress(path: Path) -> List[WordPhase]:
    if not path.exists():
        return []
    with path.open(encoding='utf-8') as f:
        data = json.load(f)
    return [wordphase_from_dict(d) for d in data]

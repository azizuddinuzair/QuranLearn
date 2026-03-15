from dataclasses import dataclass, field
from typing import Optional
from datetime import date

@dataclass
class WordPhase:
    word: str
    translit: str
    meaning: str
    surah_id: int
    ayah_id: int
    phase: int  # e.g., 1–5
    learned: bool = False
    first_seen: Optional[date] = None
    review_count: int = 0
    quiz_correct: int = 0
    last_seen: Optional[date] = None
    # Add more fields as needed for spaced repetition, e.g., next_review_date

    def mark_seen(self, today: Optional[date] = None):
        self.review_count += 1
        if not self.first_seen:
            self.first_seen = today or date.today()
        self.last_seen = today or date.today()

    def mark_quiz_result(self, correct: bool, today: Optional[date] = None):
        if correct:
            self.quiz_correct += 1
        self.last_seen = today or date.today()
        # Optionally update learned status based on quiz_correct threshold
        if self.quiz_correct >= 3:
            self.learned = True
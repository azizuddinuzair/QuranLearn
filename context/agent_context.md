# QuranLearn Agent Context

## Conversation Summary

- **Primary Objectives:** Automate daily vocabulary, show verses, run quizzes, phased/cumulative learning, robust CLI, data integrity, progress tracking.
- **Technical Foundation:** Python 3.x, argparse, rich, local CSVs, progress as JSON or SQLite DB, phase-based learning.
- **Key Modules:**
  - models.py: WordPhase dataclass
  - progress.py: JSON progress tracking
  - progress_db.py: SQLite DB progress tracking
  - loader.py: phase assignment, WordPhase loader
  - study.py: phase-based study, review, quiz logic
  - main.py: CLI with subcommands
  - quickstart.py: User-friendly menu entry point (no arguments needed)
  - metrics.py: Dashboard/metrics backend (phase stats, streaks, quiz performance)
  - surah_progress.py: Surah-level progress tracking (per-ayah mastery, contextual study)
- **Data:** quran_words.csv, English_clean.csv
- **Testing:** test_progress.py, test_ayah_translation.py, compare_ayah_coverage.py
- **Recent Work:**
  - Data cleaning, loader/study refactor, robust tests
  - Implemented phased, cumulative learning
  - CLI supports phase/progress options
  - Added interactive quickstart menu (quickstart.py)
  - Added database (SQLite) persistence for progress
- **Pending:** Further CLI/dashboard enhancements, advanced metrics

## Progress Tracking

- [x] WordPhase data model
- [x] Progress tracking (JSON/SQLite)
- [x] Loader refactor for phase
- [x] Study/review/quiz logic for phase
- [x] CLI options for phase/progress
- [x] User-friendly quickstart menu
- [x] Database persistence for progress
- [x] Dashboard/metrics: phase stats, streaks, quiz performance, ayahs mastered

## Lessons Learned
- Test-driven validation is essential
- CLI must match real user workflow
- Data cleaning and robust loader logic are critical
- Database persistence improves reliability and user experience
- Metrics and dashboard features greatly enhance motivation and tracking

## Next Steps
- Further CLI/dashboard enhancements (e.g., stats, streaks)
- Advanced metrics and reporting
- User-requested features
- Optional: ASCII charts, leaderboard, more analytics

---

_Last updated: 2026-03-14_
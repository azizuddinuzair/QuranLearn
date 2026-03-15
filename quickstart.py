"""
QuranLearn Quickstart CLI
- Presents a menu for Study, Review, Quiz, and Exit
- No arguments needed; user selects options interactively
- Progress is saved as JSON (can be extended to SQLite if desired)
"""
from pathlib import Path

from workflow.src.study import study_session, review_session, quiz_session
from workflow.src.progress_db import init_db, save_progress_db, load_progress_db

def main():
    print("\n==== QuranLearn CLI ====")

    words_path = Path("workflow/data/words/quran_words.csv")
    ayahs_path = Path("workflow/data/ayahs/English_clean.csv")
    progress_path = Path("progress.json")
    db_path = Path("progress.db")
    use_db = False
    # Ask user if they want to use DB persistence
    print("\nWould you like to use database (SQLite) for progress tracking? (y/n)")
    resp = input("[y/n, default n]: ").strip().lower()
    if resp == "y":
        use_db = True
        init_db(db_path)
        print("[DB] SQLite progress tracking enabled.")
    else:
        print("[JSON] Progress will be saved as JSON.")

    while True:
        print("\nChoose an option:")
        print("1. Study")
        print("2. Review")
        print("3. Quiz")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            phase = int(input("Enter phase (1 = most frequent): ").strip() or "1")
            num_words = int(input("How many words? (default 10): ").strip() or "10")
            if use_db:
                # Load progress from DB, run session, then save
                from workflow.src.progress import load_progress, save_progress
                progress = load_progress_db(db_path)
                study_session(words_path, ayahs_path, num_words, phase, db_path)
                # Save progress (study_session will update progress.json, so reload and save to DB)
                progress = load_progress(progress_path)
                save_progress_db(progress, db_path)
            else:
                study_session(words_path, ayahs_path, num_words, phase, progress_path)
        elif choice == "2":
            phase = int(input("Enter phase to review (default 1): ").strip() or "1")
            if use_db:
                from workflow.src.progress import load_progress, save_progress
                progress = load_progress_db(db_path)
                review_session(words_path, ayahs_path, phase, db_path)
                progress = load_progress(progress_path)
                save_progress_db(progress, db_path)
            else:
                review_session(words_path, ayahs_path, phase, progress_path)
        elif choice == "3":
            phase = int(input("Enter phase to quiz (default 1): ").strip() or "1")
            num_questions = int(input("How many questions? (default 10): ").strip() or "10")
            if use_db:
                from workflow.src.progress import load_progress, save_progress
                progress = load_progress_db(db_path)
                quiz_session(words_path, ayahs_path, phase, num_questions, db_path)
                progress = load_progress(progress_path)
                save_progress_db(progress, db_path)
            else:
                quiz_session(words_path, ayahs_path, phase, num_questions, progress_path)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("[USAGE] Please run: python -m workflow.src.quickstart")

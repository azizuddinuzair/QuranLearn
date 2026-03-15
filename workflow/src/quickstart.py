from .study import study_session, review_session, quiz_session
from .progress_db import init_db, save_progress_db, load_progress_db
from .metrics import get_phase_metrics, get_ayahs_mastered, get_daily_streaks, get_quiz_performance
from .surah_progress import init_surah_progress_table, get_surah_progress, update_surah_progress
from rich.table import Table
from rich.console import Console


"""
Run commands -->
Windows: py -m workflow.src.quickstart
Mac/Linux: python3 -m workflow.src.quickstart

"""

def main():
    print("\n==== QuranLearn CLI ====")
    from pathlib import Path
    words_path = Path("workflow/data/words/quran_words.csv")
    ayahs_path = Path("workflow/data/ayahs/English_clean.csv")
    progress_path = Path("progress.json")
    db_path = Path("progress.db")
    use_db = False
    print("\nWould you like to use database (SQLite) for progress tracking? (y/n)")
    resp = input("[y/n, default n]: ").strip().lower()
    if resp == "y":
        use_db = True
        init_db(db_path)
        print("[DB] SQLite progress tracking enabled.")
    else:
        print("[JSON] Progress will be saved as JSON.")
    console = Console()
    # Load surah metadata once
    import json
    surah_metadata_path = Path("data/surah_metadata.json")
    with open(surah_metadata_path, "r", encoding="utf-8") as f:
        surah_metadata = json.load(f)
    surah_dict = {s["surah_no"]: s for s in surah_metadata}

    while True:
        print("\nChoose an option:")
        print("1. Study")
        print("2. Review")
        print("3. Quiz")
        print("4. Surah Study (ayah-by-ayah)")
        print("5. View Progress / Metrics")
        print("6. Exit")
        choice = input("Enter choice (1-6): ").strip()
        if choice == "1":
            phase = int(input("Enter phase (1 = most frequent): ").strip() or "1")
            num_words = int(input("How many words? (default 10): ").strip() or "10")
            if use_db:
                from .progress import load_progress, save_progress
                progress = load_progress_db(db_path)
                study_session(words_path, ayahs_path, num_words, phase, db_path)
                progress = load_progress(progress_path)
                save_progress_db(progress, db_path)
            else:
                study_session(words_path, ayahs_path, num_words, phase, progress_path)
        elif choice == "2":
            phase = int(input("Enter phase to review (default 1): ").strip() or "1")
            if use_db:
                from .progress import load_progress, save_progress
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
                from .progress import load_progress, save_progress
                progress = load_progress_db(db_path)
                quiz_session(words_path, ayahs_path, phase, num_questions, db_path)
                progress = load_progress(progress_path)
                save_progress_db(progress, db_path)
            else:
                quiz_session(words_path, ayahs_path, phase, num_questions, progress_path)
        elif choice == "4":
            # Surah Study (ayah-by-ayah)
            if not use_db:
                print("[!] Surah study requires DB mode. Restart and choose DB for progress.")
                continue
            try:
                surah_no = int(input("Enter surah number (1-114): ").strip())
            except ValueError:
                print("[!] Invalid surah number.")
                continue
            if surah_no not in surah_dict:
                print(f"[!] Surah {surah_no} not found in metadata.")
                continue
            surah_info = surah_dict[surah_no]
            total_ayahs = surah_info["total_ayahs"]
            surah_name = surah_info["name"]
            print(f"Loaded: Surah {surah_no} - {surah_name} ({total_ayahs} ayahs)")
            init_surah_progress_table(db_path)
            sp = get_surah_progress(db_path, surah_no)
            # Always enforce ayah count from metadata
            ayah_progress = {}
            if sp:
                # If DB ayah count mismatches metadata, fix it
                db_ayahs = sp['total_ayahs']
                if db_ayahs != total_ayahs:
                    # Copy over existing statuses for ayahs in both, set new ones to not_seen
                    for i in range(1, total_ayahs+1):
                        key = str(i)
                        ayah_progress[key] = sp['ayah_progress'].get(key, "not_seen")
                    update_surah_progress(db_path, surah_no, total_ayahs, ayah_progress)
                    sp = get_surah_progress(db_path, surah_no)
                else:
                    ayah_progress = sp['ayah_progress']
            else:
                ayah_progress = {str(i): "not_seen" for i in range(1, total_ayahs+1)}
                update_surah_progress(db_path, surah_no, total_ayahs, ayah_progress)
                sp = get_surah_progress(db_path, surah_no)
            print(f"\nSurah {surah_no} - {surah_name} - {total_ayahs} ayahs")
            # Load all words for this surah from quran_words.csv
            from .loader import load_words_csv
            words_data = load_words_csv(words_path)
            # Group words by ayah
            ayah_words = {}
            for w in words_data:
                try:
                    s = int(w.get('surah_id', 0))
                    a = int(w.get('ayah_id', 0))
                    if s == surah_no:
                        ayah_words.setdefault(a, []).append(w)
                except Exception:
                    continue

            # Let user pick starting ayah
            start_ayah = 1
            try:
                user_start = input(f"Enter starting ayah (1-{total_ayahs}, default 1): ").strip()
                if user_start:
                    start_ayah = max(1, min(total_ayahs, int(user_start)))
            except Exception:
                pass

            for ayah in range(start_ayah, total_ayahs+1):
                status = sp['ayah_progress'].get(str(ayah), "not_seen")
                print(f"\nAyah {ayah}: Status = {status}")
                if status == "learned":
                    print("[Already learned, skipping]")
                    continue
                # Show all words in this ayah
                words = ayah_words.get(ayah, [])
                if not words:
                    print("[No word data for this ayah]")
                    continue
                print("Words in this ayah:")
                for w in words:
                    print(f"  {w['word_ar']} ({w['word_tr']}): {w['word_en']}")
                print("\n" + "-"*40 + "\n")
                input("Press Enter to review and continue to quiz...")
                print("\n"*2)

                # Mini-quiz: ask meanings for each word (multiple choice if possible)
                import random
                correct = 0
                for w in words:
                    choices = [w['word_en']]
                    # Add 3 random meanings from other words for choices
                    distractors = [x['word_en'] for x in random.sample(words_data, min(20, len(words_data))) if x['word_en'] != w['word_en']]
                    choices += random.sample(distractors, min(3, len(distractors)))
                    random.shuffle(choices)
                    print(f"What is the meaning of {w['word_ar']} ({w['word_tr']})?")
                    for idx, c in enumerate(choices):
                        print(f"  {idx+1}. {c}")
                    ans = input("Your answer (1-4): ").strip()
                    try:
                        if choices[int(ans)-1] == w['word_en']:
                            print("Correct!")
                            correct += 1
                        else:
                            print(f"Incorrect. Correct answer: {w['word_en']}")
                    except Exception:
                        print(f"Invalid input. Correct answer: {w['word_en']}")
                print(f"Quiz complete: {correct}/{len(words)} correct.")

                # Only mark as learned if all correct or user confirms
                if correct == len(words):
                    print("All correct! Marking ayah as learned.")
                    sp['ayah_progress'][str(ayah)] = "learned"
                    update_surah_progress(db_path, surah_no, total_ayahs, sp['ayah_progress'])
                else:
                    mark = input("Mark ayah as learned anyway? (y/n): ").strip().lower()
                    if mark == "y":
                        sp['ayah_progress'][str(ayah)] = "learned"
                        update_surah_progress(db_path, surah_no, total_ayahs, sp['ayah_progress'])

                # Option to stop early
                stop = input("Continue to next ayah? (y to continue, any other key to stop): ").strip().lower()
                if stop != "y":
                    print("Stopping surah study early.")
                    break
            print("Surah study complete!")
        elif choice == "5":
            # Metrics dashboard
            if not use_db:
                print("[!] Metrics require DB mode. Restart and choose DB for progress.")
                continue
            phase_input = input("View stats for a specific phase? (Enter phase number or leave blank for all): ").strip()
            phase_metrics = get_phase_metrics(db_path)
            ayahs_mastered = get_ayahs_mastered(db_path)
            streaks = get_daily_streaks(db_path)
            quiz_perf = get_quiz_performance(db_path)
            table = Table(title="Phase-wise Progress", show_lines=True)
            table.add_column("Phase", style="bold yellow")
            table.add_column("Words", style="cyan")
            table.add_column("Learned", style="green")
            table.add_column("Quiz Correct", style="magenta")
            table.add_column("Reviews", style="white")
            for phase, m in sorted(phase_metrics.items()):
                if phase_input and str(phase) != phase_input:
                    continue
                table.add_row(str(phase), str(m['total']), str(m['learned']), str(m['quiz_correct']), str(m['review_count']))
            console.print(table)
            print(f"Total ayahs fully mastered: {ayahs_mastered}")
            print(f"Current daily streak: {streaks['current_streak']} days")
            print(f"Active days: {streaks['active_days']}")
            print(f"Quiz performance: {quiz_perf['quiz_correct']} correct / {quiz_perf['review_count']} attempts")
            print(f"Overall accuracy: {quiz_perf['accuracy']:.1f}%")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

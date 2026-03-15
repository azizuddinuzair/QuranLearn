import argparse
from pathlib import Path
from study import study_session


def main():
    parser = argparse.ArgumentParser(description="Quran CLI Study Tool")
    subparsers = parser.add_subparsers(dest="command")

    study_parser = subparsers.add_parser("study", help="Start a daily study session")
    study_parser.add_argument(
        "--words-path", default="../data/words/quran_words.csv", help="Path to words CSV file (relative to src)"
    )
    study_parser.add_argument(
        "--ayahs-path", default="../data/ayahs/English_clean.csv", help="Path to ayah translations CSV (relative to src)"
    )
    study_parser.add_argument(
        "--num-words", type=int, default=10, help="Number of words to study per session"
    )
    study_parser.add_argument(
        "--phase", type=int, default=1, help="Phase number to study (1 = most frequent words)"
    )
    study_parser.add_argument(
        "--progress-path", default="progress.json", help="Path to progress JSON file"
    )

    review_parser = subparsers.add_parser("review", help="Review words due for spaced repetition")
    review_parser.add_argument("--words-path", default="../data/words/quran_words.csv", help="Path to words CSV file (relative to src)")
    review_parser.add_argument("--ayahs-path", default="../data/ayahs/English_clean.csv", help="Path to ayah translations CSV (relative to src)")
    review_parser.add_argument("--phase", type=int, default=1, help="Phase number to review")
    review_parser.add_argument("--progress-path", default="progress.json", help="Path to progress JSON file")

    quiz_parser = subparsers.add_parser("quiz", help="Quiz yourself on Quran vocab")
    quiz_parser.add_argument("--words-path", default="../data/words/quran_words.csv", help="Path to words CSV file (relative to src)")
    quiz_parser.add_argument("--ayahs-path", default="../data/ayahs/English_clean.csv", help="Path to ayah translations CSV (relative to src)")
    quiz_parser.add_argument("--phase", type=int, default=1, help="Phase number to quiz")
    quiz_parser.add_argument("--num-questions", type=int, default=10, help="Number of quiz questions")
    quiz_parser.add_argument("--progress-path", default="progress.json", help="Path to progress JSON file")

    args = parser.parse_args()
    if args.command == "study":
        study_session(
            Path(args.words_path),
            Path(args.ayahs_path),
            args.num_words,
            args.phase,
            Path(args.progress_path)
        )
    elif args.command == "review":
        from study import review_session
        review_session(
            Path(args.words_path),
            Path(args.ayahs_path),
            args.phase,
            Path(args.progress_path)
        )
    elif args.command == "quiz":
        from study import quiz_session
        quiz_session(
            Path(args.words_path),
            Path(args.ayahs_path),
            args.phase,
            args.num_questions,
            Path(args.progress_path)
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

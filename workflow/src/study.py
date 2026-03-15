from pathlib import Path
from datetime import date
from rich.console import Console
from rich.table import Table
from .loader import load_wordphases, load_ayah_translations
from .progress import load_progress, save_progress
from .models import WordPhase
import random

# Review session: show words due for review, prompt user to mark as seen/correct
def review_session(words_path: Path, ayah_path: Path, phase: int = 1, progress_path: Path = Path("progress.json")):
    """
    Review mode: Show words due for review in the given phase, prompt user to mark as seen/correct.
    """
    try:
        all_wordphases = load_wordphases(words_path)
        ayahs = load_ayah_translations(ayah_path)
        if not all_wordphases:
            console.print("[red]No words loaded. Check your data file.[/red]")
            return
        progress = { (w.word, w.surah_id, w.ayah_id): w for w in load_progress(progress_path) }
        today = date.today()
        # Words due for review: not learned, or last_seen is None or last_seen < today
        due_words = []
        for w in all_wordphases:
            if w.phase > phase:
                continue
            key = (w.word, w.surah_id, w.ayah_id)
            wp = progress.get(key, w)
            # Due if not learned, or last_seen is None or last_seen < today
            if not wp.learned and (not wp.last_seen or wp.last_seen < today):
                due_words.append(wp)
        if not due_words:
            console.print(f"[green]No words due for review in phase {phase} or below.")
            return
        table = Table(title=f"Review Words Due (Phase ≤ {phase})", show_lines=True)
        table.add_column("#", style="dim")
        table.add_column("Word (AR)", style="bold yellow")
        table.add_column("Translit", style="cyan")
        table.add_column("Meaning", style="green")
        table.add_column("Surah:Ayah", style="magenta")
        table.add_column("Ayah (EN)", style="white")
        for idx, w in enumerate(due_words, 1):
            ayah_text = ayahs.get((w.surah_id, w.ayah_id), "[No translation]")
            table.add_row(str(idx), w.word, w.translit, w.meaning, f"{w.surah_id}:{w.ayah_id}", ayah_text)
        console.print(table)
        # Prompt user for each word: seen/correct
        for w in due_words:
            ayah_text = ayahs.get((w.surah_id, w.ayah_id), "[No translation]")
            console.print(f"\n[bold yellow]{w.word}[/bold yellow] | [cyan]{w.translit}[/cyan] | [green]{w.meaning}[/green] | [magenta]{w.surah_id}:{w.ayah_id}[/magenta]")
            console.print(f"[white]{ayah_text}[/white]")
            resp = input("Did you recall this word correctly? (y/n/skip): ").strip().lower()
            key = (w.word, w.surah_id, w.ayah_id)
            wp = progress.get(key, w)
            if resp == "y":
                wp.mark_seen(today)
                wp.mark_quiz_result(True, today)
            elif resp == "n":
                wp.mark_seen(today)
                wp.mark_quiz_result(False, today)
            # skip = do nothing
            progress[key] = wp
        save_progress(list(progress.values()), progress_path)
        # Metrics
        total = len(due_words)
        learned = sum(1 for w in due_words if progress.get((w.word, w.surah_id, w.ayah_id), w).learned)
        console.print(f"\n[bold green]Review complete.[/bold green] {total} words reviewed. {learned} now learned.")
    except Exception as e:
        console.print(f"[red]Review session failed: {e}[/red]")

# Quiz session: quiz user on vocab, update progress
def quiz_session(words_path: Path, ayah_path: Path, phase: int = 1, num_questions: int = 10, progress_path: Path = Path("progress.json")):
    """
    Quiz mode: Quiz user on vocab in the given phase, update progress and show metrics.
    """
    try:
        all_wordphases = load_wordphases(words_path)
        ayahs = load_ayah_translations(ayah_path)
        if not all_wordphases:
            console.print("[red]No words loaded. Check your data file.[/red]")
            return
        progress = { (w.word, w.surah_id, w.ayah_id): w for w in load_progress(progress_path) }
        # Select quiz candidates: prioritize not learned, then reinforce learned
        learning = [w for w in all_wordphases if w.phase == phase and not progress.get((w.word, w.surah_id, w.ayah_id), w).learned]
        learned = [w for w in all_wordphases if w.phase == phase and progress.get((w.word, w.surah_id, w.ayah_id), w).learned]
        quiz_pool = learning + random.sample(learned, min(len(learned), max(0, num_questions - len(learning))))
        if not quiz_pool:
            console.print(f"[green]No words available for quiz in phase {phase}.")
            return
        sample = random.sample(quiz_pool, min(num_questions, len(quiz_pool)))
        correct = 0
        for idx, w in enumerate(sample, 1):
            # Multiple choice: Arabic → choose correct meaning
            distractors = random.sample([x.meaning for x in all_wordphases if x.meaning != w.meaning], k=3) if len(all_wordphases) > 3 else []
            options = distractors + [w.meaning]
            random.shuffle(options)
            console.print(f"\n[bold]{idx}. {w.word}[/bold] | [cyan]{w.translit}[/cyan] | [magenta]{w.surah_id}:{w.ayah_id}[/magenta]")
            for i, opt in enumerate(options, 1):
                console.print(f"  {i}. {opt}")
            ans = input("Choose the correct meaning (1-4): ").strip()
            key = (w.word, w.surah_id, w.ayah_id)
            wp = progress.get(key, w)
            try:
                if options[int(ans)-1] == w.meaning:
                    console.print("[green]Correct![/green]")
                    correct += 1
                    wp.mark_quiz_result(True)
                else:
                    console.print(f"[red]Incorrect. Correct answer: {w.meaning}[/red]")
                    wp.mark_quiz_result(False)
            except Exception:
                console.print(f"[yellow]Skipped.[/yellow]")
            progress[key] = wp
        save_progress(list(progress.values()), progress_path)
        total = len(sample)
        accuracy = 100 * correct / total if total else 0
        console.print(f"\n[bold green]Quiz complete.[/bold green] {correct}/{total} correct. Accuracy: {accuracy:.1f}%.")
    except Exception as e:
        console.print(f"[red]Quiz session failed: {e}[/red]")



console = Console()

# Exception-safe study session
def study_session(words_path: Path, ayah_path: Path, num_words: int = 10, phase: int = 1, progress_path: Path = Path("progress.json")):
    """
    Study session for a given phase. Tracks progress and only shows words from the specified phase.
    """
    try:
        # Load all words as WordPhase objects
        all_wordphases = load_wordphases(words_path)
        ayahs = load_ayah_translations(ayah_path)
        if not all_wordphases:
            console.print("[red]No words loaded. Check your data file.[/red]")
            return
        # Load or initialize progress
        progress = { (w.word, w.surah_id, w.ayah_id): w for w in load_progress(progress_path) }
        # Filter for current phase and not yet learned
        phase_words = [w for w in all_wordphases if w.phase == phase and not progress.get((w.word, w.surah_id, w.ayah_id), w).learned]
        if not phase_words:
            console.print(f"[green]All words in phase {phase} are learned! Try a higher phase.")
            return
        sample = random.sample(phase_words, min(num_words, len(phase_words)))
        table = Table(title=f"Today's Quran Words (Phase {phase})", show_lines=True)
        table.add_column("Word (AR)", style="bold yellow")
        table.add_column("Translit", style="cyan")
        table.add_column("Meaning", style="green")
        table.add_column("Surah:Ayah", style="magenta")
        table.add_column("Ayah (EN)", style="white")
        for w in sample:
            # Mark as seen in progress
            key = (w.word, w.surah_id, w.ayah_id)
            wp = progress.get(key, w)
            wp.mark_seen()
            progress[key] = wp
            lookup_key = (w.surah_id, w.ayah_id)
            ayah_text = ayahs.get(lookup_key, "[No translation]")
            table.add_row(
                w.word,
                w.translit,
                w.meaning,
                f"{w.surah_id}:{w.ayah_id}",
                ayah_text
            )
        console.print(table)
        # Save updated progress
        save_progress(list(progress.values()), progress_path)
    except Exception as e:
        console.print(f"[red]Study session failed: {e}[/red]")

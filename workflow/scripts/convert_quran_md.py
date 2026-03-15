from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import pandas as pd


TEXT_COLUMNS = [
    "surah_id",
    "ayah_id",
    "word_id",
    "word_index",
    "word_ar",
    "word_en",
    "word_tr",
    "surah_name_ar",
    "surah_name_en",
    "ayah_ar",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Quran-MD train shards into CSV, JSONL, and SQLite outputs."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing train-*.parquet shards.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory where converted files will be written.",
    )
    parser.add_argument(
        "--prefix",
        default="quran_words",
        help="Base filename for generated outputs.",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["csv", "jsonl", "sqlite"],
        default=["csv", "jsonl", "sqlite"],
        help="Output formats to generate.",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Retain the audio column when exporting JSONL or SQLite.",
    )
    return parser.parse_args()


def is_lfs_pointer(path: Path) -> bool:
    with path.open("rb") as handle:
        header = handle.read(128)
    return header.startswith(b"version https://git-lfs.github.com/spec/v1")


def ensure_real_parquet_files(shard_paths: list[Path]) -> None:
    lfs_pointers = [path for path in shard_paths if is_lfs_pointer(path)]
    if not lfs_pointers:
        return

    joined = "\n".join(f"- {path}" for path in lfs_pointers)
    raise SystemExit(
        "Input shards are Git LFS pointer files, not Parquet data. Fetch the real blobs first:\n"
        "  git lfs install\n"
        "  git lfs pull\n\n"
        f"Affected files:\n{joined}"
    )


def load_dataframe(shard_paths: list[Path]) -> pd.DataFrame:
    missing = [path for path in shard_paths if not path.exists()]
    if missing:
        joined = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Missing input files:\n{joined}")

    ensure_real_parquet_files(shard_paths)
    frames = [pd.read_parquet(path) for path in shard_paths]
    return pd.concat(frames, ignore_index=True)


def select_columns(df: pd.DataFrame, keep_audio: bool) -> pd.DataFrame:
    expected = TEXT_COLUMNS + (["audio"] if keep_audio else [])
    missing = [column for column in expected if column not in df.columns]
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"Input data is missing expected columns: {joined}")
    return df.loc[:, expected].copy()


def validate_dataframe(df: pd.DataFrame) -> None:
    duplicate_word_ids = int(df["word_id"].duplicated().sum())
    print(f"Rows: {len(df):,}")
    print(f"Columns: {', '.join(df.columns)}")
    print(f"Duplicate word_id values: {duplicate_word_ids:,}")


def write_csv(df: pd.DataFrame, output_path: Path) -> None:
    if "audio" in df.columns:
        raise SystemExit("CSV export does not support --keep-audio. Use JSONL or SQLite instead.")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Wrote {output_path}")


def write_jsonl(df: pd.DataFrame, output_path: Path) -> None:
    df.to_json(output_path, orient="records", lines=True, force_ascii=False)
    print(f"Wrote {output_path}")


def write_sqlite(df: pd.DataFrame, output_path: Path) -> None:
    with sqlite3.connect(output_path) as connection:
        df.to_sql("words", connection, if_exists="replace", index=False)
    print(f"Wrote {output_path}")


def main() -> int:
    args = parse_args()
    shard_paths = sorted(args.input_dir.glob("train-*.parquet"))
    if not shard_paths:
        raise SystemExit(f"No train-*.parquet shards found in {args.input_dir}")

    df = load_dataframe(shard_paths)
    df = select_columns(df, keep_audio=args.keep_audio)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    validate_dataframe(df)

    for output_format in args.formats:
        output_path = args.output_dir / f"{args.prefix}.{output_format}"
        if output_format == "csv":
            write_csv(df, output_path)
        elif output_format == "jsonl":
            write_jsonl(df, output_path)
        else:
            write_sqlite(df, output_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
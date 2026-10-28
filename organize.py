#!/usr/bin/env python3
"""
organize.py - Sort the loose files in a folder into category sub-folders.

Groups files by extension into folders like Images/, Documents/, Audio/, etc.
Offers a safe --dry-run preview, never overwrites existing files, and only
touches loose files (existing sub-folders are left alone).

Usage:
    python organize.py <folder> [--dry-run] [--verbose]

Examples:
    python organize.py ./Downloads --dry-run
    python organize.py "C:/Users/Me/Desktop/Mess"
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Map a human-readable category -> the extensions that belong to it.
# Extensions are lower-case and include the leading dot.
CATEGORIES: dict[str, set[str]] = {
    "Images":        {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                      ".webp", ".tiff", ".ico", ".heic"},
    "Documents":     {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt",
                      ".md", ".tex"},
    "Spreadsheets":  {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Audio":         {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "Video":         {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv",
                      ".webm", ".m4v"},
    "Archives":      {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Code":          {".py", ".js", ".ts", ".html", ".css", ".java", ".c",
                      ".cpp", ".cs", ".go", ".rb", ".php", ".sh", ".json",
                      ".xml", ".yml", ".yaml", ".sql"},
}

# Files with an unknown extension (or none at all) land here.
FALLBACK_CATEGORY = "Other"


def build_extension_index(categories: dict[str, set[str]]) -> dict[str, str]:
    """Flatten the category map into a fast {extension: category} lookup."""
    index: dict[str, str] = {}
    for category, extensions in categories.items():
        for ext in extensions:
            index[ext] = category
    return index


def category_for(file: Path, index: dict[str, str]) -> str:
    """Return the destination category for a single file."""
    return index.get(file.suffix.lower(), FALLBACK_CATEGORY)


def resolve_collision(destination: Path) -> Path:
    """
    Return a path that does not clash with an existing file.

    If 'report.pdf' already exists, returns 'report (1).pdf', then
    'report (2).pdf', and so on, so nothing is ever overwritten.
    """
    if not destination.exists():
        return destination

    stem, suffix, parent = destination.stem, destination.suffix, destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def iter_loose_files(folder: Path, script_path: Path) -> list[Path]:
    """
    Collect the files directly inside 'folder' that should be organized.

    Skips sub-directories, hidden files (names starting with '.'), and the
    running script itself, so the tool is safe to run from inside its own folder.
    """
    files: list[Path] = []
    for entry in folder.iterdir():
        if not entry.is_file():
            continue
        if entry.name.startswith("."):
            continue
        if entry.resolve() == script_path:
            continue
        files.append(entry)
    return files


def organize(folder: Path, dry_run: bool, verbose: bool) -> dict[str, int]:
    """
    Sort loose files in 'folder' into category sub-folders.

    Returns a {category: count} summary of what was (or would be) moved.
    """
    index = build_extension_index(CATEGORIES)
    script_path = Path(__file__).resolve()
    summary: dict[str, int] = {}

    # Collect everything first so we never mutate the folder while iterating it.
    for file in iter_loose_files(folder, script_path):
        category = category_for(file, index)
        target_dir = folder / category
        destination = resolve_collision(target_dir / file.name)

        if dry_run:
            if verbose:
                print(f"[dry-run] {file.name}  ->  {category}/{destination.name}")
        else:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(file), str(destination))
            if verbose:
                print(f"moved: {file.name}  ->  {category}/{destination.name}")

        summary[category] = summary.get(category, 0) + 1

    return summary


def print_summary(summary: dict[str, int], dry_run: bool) -> None:
    """Print a tidy end-of-run report."""
    total = sum(summary.values())
    verb = "Would move" if dry_run else "Moved"

    if total == 0:
        print("Nothing to do - no loose files found.")
        return

    print()
    print(f"{verb} {total} file(s) into {len(summary)} folder(s):")
    for category in sorted(summary):
        print(f"  {category:<14} {summary[category]}")
    if dry_run:
        print("\nThis was a dry run. Re-run without --dry-run to apply changes.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Define and parse the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Sort the loose files in a folder into category sub-folders."
    )
    parser.add_argument("folder", help="Path to the folder you want to organize.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the changes without moving any files.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print each file as it is processed.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Program entry point. Returns a process exit code (0 = success)."""
    args = parse_args(argv)
    folder = Path(args.folder).expanduser()

    if not folder.exists():
        print(f"Error: folder does not exist: {folder}", file=sys.stderr)
        return 1
    if not folder.is_dir():
        print(f"Error: not a folder: {folder}", file=sys.stderr)
        return 1

    summary = organize(folder, dry_run=args.dry_run, verbose=args.verbose)
    print_summary(summary, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

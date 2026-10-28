# File Organizer

A small command-line tool that tidies a messy folder by sorting its loose files
into category sub-folders (`Images/`, `Documents/`, `Audio/`, and so on) based on
their file extension.

It is designed to be safe to run: it previews changes with `--dry-run`, never
overwrites existing files, and only touches files sitting directly in the target
folder (existing sub-folders are left alone).

## Features

- Sorts files into categories by extension (case-insensitive).
- `--dry-run` mode previews every move without changing anything.
- Never overwrites: a clashing `report.pdf` becomes `report (1).pdf`.
- Skips sub-folders, hidden files, and the script itself.
- Prints a clear summary of what was moved and where.
- Returns proper exit codes (`0` success, `1` on a bad path).

## Requirements

- Python 3.9 or newer. No third-party packages — standard library only.

Check your version with:

```
python --version
```

## Installation

No installation needed. Just download `organize.py` and run it with Python.

```
git clone <your-repo-url>
cd file-organizer
```

## Usage

```
python organize.py <folder> [--dry-run] [--verbose]
```

| Option          | Description                                      |
| --------------- | ------------------------------------------------ |
| `folder`        | Path to the folder you want to organize.         |
| `--dry-run`     | Preview the changes without moving any files.    |
| `-v`, `--verbose` | Print each file as it is processed.            |
| `-h`, `--help`  | Show the help message and exit.                  |

### Examples

Preview what would happen to your Downloads folder (safe, nothing moves):

```
python organize.py "C:/Users/Me/Downloads" --dry-run --verbose
```

Actually organize the folder:

```
python organize.py "C:/Users/Me/Downloads"
```

### Example output

```
Moved 12 file(s) into 9 folder(s):
  Archives       1
  Audio          1
  Code           1
  Documents      2
  Images         2
  Other          2
  Presentations  1
  Spreadsheets   1
  Video          1
```

## How categories are decided

Each category owns a set of extensions (see the `CATEGORIES` dictionary at the
top of `organize.py`). A file's lower-cased extension is looked up there; anything
unrecognised, or a file with no extension, goes into `Other/`. To add or change a
category, just edit that dictionary.

## Notes and limitations

- Only files directly inside the target folder are organized; the tool does not
  recurse into sub-folders.
- Files are categorised by extension, not by inspecting their contents.
- Running it twice is safe: already-sorted files stay where they are, and any new
  name clashes are resolved automatically.

## License

Released for educational use.

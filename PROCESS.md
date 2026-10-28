# Process Log — File Organizer (Mini-Project 2)

**Author:** Adarsh Dinkar
**Course:** Introduction to Artificial Intelligence Practical Tools
**Task:** Use an AI assistant to generate a Python script that automates an
everyday task through a console interface; debug it with AI; produce a README;
submit the code, Git history, and README.

---

## 1. Task definition (my decision)

I chose to automate **tidying a messy folder**. Everyday problem: my Downloads
folder fills up with images, PDFs, installers, and zips all mixed together. I
decided the script should sort loose files into category sub-folders (Images,
Documents, Audio, Video, Archives, Code, etc.) by file extension, run from the
command line, and — importantly — be *safe* to run (preview mode, no overwrites).

I set the scope myself before prompting the AI:
- Takes a folder path as a command-line argument.
- Sorts only loose files; leaves existing sub-folders alone.
- A `--dry-run` flag to preview changes before anything moves.
- Never overwrites a file that already exists in the destination.
- Prints a clear summary at the end.

## 2. Environment

- Windows 11, Command Prompt.
- Python 3.12.3, Git 2.38.1 (checked with `python --version` and `git --version`).
- AI assistant (chat) used to generate and refine the code and README.
- Editor: VS Code.

## 3. Prompts and decisions

### Prompt 1 — generate the script
> "Build a console Python script that automates an everyday task — a file
> organizer that sorts a messy folder into sub-folders by file type. It should
> use an argparse CLI, support a --dry-run preview, never overwrite existing
> files, handle folders that don't exist, and print a summary. Senior-developer
> quality — clean structure, type hints, docstrings."

**What I got back:** a complete `organize.py` with:
- A `CATEGORIES` dictionary mapping categories to file extensions.
- Helper functions: `build_extension_index`, `category_for`,
  `resolve_collision`, `iter_loose_files`, `organize`, `print_summary`,
  `parse_args`, `main`.
- `--dry-run` and `--verbose` flags, exit codes, and a `__main__` guard.

**My decision:** I accepted the structure but read through every function first
so I could explain it. Key things I made sure I understood:
- `resolve_collision()` renames clashes to `name (1).ext` instead of
  overwriting.
- `iter_loose_files()` builds the full list *before* moving anything, so the
  folder isn't modified while it's being iterated (avoids skipping files).
- Extension matching is lower-cased, so `.PNG` and `.png` are treated the same.

### Prompt 2 — README
> "Write a README explaining what the script does, requirements, installation,
> usage with examples, how categories are decided, and limitations."

**What I got back:** a structured README with a usage table and example output.
**My decision:** accepted it; checked that every command in it actually matches
the script's real flags.

## 4. My own change (independence)

The generated `CATEGORIES` map didn't cover e-books, which I download often, so
I added a new category myself:

```python
"eBooks":        {".epub", ".mobi", ".azw3", ".fb2"},
```

I placed it right after the `Documents` entry and re-tested to confirm an
`.epub` file now lands in an `eBooks/` folder instead of `Other/`.

## 5. Testing / validation

I tested on a throwaway folder (not the repo) so nothing important could be
touched:

```
mkdir test_mess
echo hello > test_mess\a.txt
echo pic > test_mess\b.jpg
echo song > test_mess\c.mp3
python organize.py test_mess --dry-run --verbose   # preview only
python organize.py test_mess --verbose             # real run
rmdir /S /Q test_mess
```

Checks I ran and confirmed:
- Dry-run printed the planned moves and moved nothing.
- Real run sorted the files into `Documents/`, `Images/`, `Audio/`.
- A file with no extension and an unknown extension both went to `Other/`.
- Running on a non-existent path printed an error and exited (code 1).
- Running twice did not overwrite — a repeated name became `name (1).ext`.

## 6. Debugging with AI

While testing, I introduced a typo to see how I'd handle a real error. In the
`organize()` function I accidentally wrote `shutil.moove(...)` instead of
`shutil.move(...)`. Running the script produced:

```
AttributeError: module 'shutil' has no attribute 'moove'. Did you mean: 'move'?
```

I pasted the traceback to the AI and asked what was wrong. It pointed out the
method name was misspelled — `shutil` has `move`, not `moove`. I corrected the
typo, re-ran the script on the test folder, and the files sorted correctly
again. Takeaway: Python's `AttributeError` names the exact bad attribute, and
the "Did you mean" hint usually points straight at the fix.

## 7. Reflection

**What worked well:** the AI produced clean, well-structured code quickly and
handled edge cases (name collisions, hidden files, bad paths) that I might have
forgotten on a first pass. It was fastest when I gave it a specific scope up
front rather than a vague request.

**Limitations I noticed:** the tool categorises by *extension only*, not by
actual file contents, so a file with a wrong or missing extension could be
sorted into the wrong place. It also doesn't recurse into sub-folders by design.
For anything important I'd still glance at the results rather than trust it
blindly.

**What I learned:** how `argparse` turns a Python script into a proper
command-line tool with positional arguments and optional flags, and how Git
records each change as a separate commit so the build-up of the project is
visible in the history.

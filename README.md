# Apple Journal -> Markdown

Apple Journal only allows you to export your entries as HTML files. These HTML files can be pretty messy and although they look fine in the browser, it is hard to use them with any other program.

This Python script allows you to convert these HTML files to a markdown format which is essentially raw text. This allows for more flexibility when managing these files.

Useful for:
- Backing up your journal.
- Switching from Apple Journal to a markdown editor such as Obsidian.

## Usage

### Requirements
- Python
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
	- This Python package is used to parse the HTML.
	- Install using `pip install beautifulsoup4`

### Process
1. Unzip your export (`AppleJournalEntries.zip`).
2. This folder should have two folders - `Entries/` and `Resources/`, inside.
3. Run the  script `applejournal-to-md.py`, the `-i` argument should pass the location of `AppleJournalEntries/`.
4. By default a folder called `MarkdownOutput` will be created next to the script file containing all converted entries.

#### Example Usage

```
python3 applejournal-to-md.py -i ~/Desktop/AppleJournalEntries/
```

### Command Line Arguments

| Argument                       | Required | Default          | Description                                                                                        |
| ------------------------------ | -------- | ---------------- | -------------------------------------------------------------------------------------------------- |
| `-i`, `--input`                | Yes      | -                | Root directory containing Apple Journal export. Must include `Entries/` and `Resources/`.          |
| `-o`, `--output`               | No       | `MarkdownOutput` | Output directory. This will be created if it does not exist already.                               |
| `-da`, `--disable-attachments` | No       | `False`          | Disable processing of attachments. If `-da` is passed, all content within `Resources/` is ignored. |

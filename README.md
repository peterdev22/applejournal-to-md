# Convert Apple Journal to Markdown

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
 		- Alternatively, install it to a Python virtual env.

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

---

## Supported Conversions

### Text - Fully Supported

Text should currently be fully supported and should work perfectly in most cases. In the rare case conversion messes up, please send a [GitHub issue](https://github.com/peterdev22/applejournal-to-md/issues) to help fix it!

If the majority of your journal entries are plainly formatted - it's almost guaranteed your entries will convert perfectly.

| Type            | Supported by this program | Supported by Markdown | Implementation                            | Caveats                                                                                        |
| --------------- | ------------------------- | --------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Entry title     | Yes                       | Yes                   | Converts to `# markdown heading`          |                                                                                                |
| Plain text      | Yes                       | Yes                   | Converts to `plain markdown`.             |                                                                                                |
| Bold            | Yes                       | Yes                   | Converts to `**bold markdown**`.          |                                                                                                |
| Italic          | Yes                       | Yes                   | Converts to `*italic markdown*`.          |                                                                                                |
| Underline       | Yes                       | Yes (HTML)            | Converts to `<u>underlined markdown</u>`. | Underlined text will override other styles on the same text. This is a limitation of markdown. |
| Strikethrough   | Yes                       | Yes (Extended)        | Converts to `~~strikethrough markdown~~`. |                                                                                                |
| Unordered lists | Yes                       | Yes                   | Converts to a `- list item`.              |                                                                                                |
| Ordered lists   | Yes                       | Yes                   | Converts to a `1. list item`.             |                                                                                                |
| Blockquotes     | Yes                       | Yes                   | Converts to `> markdown quote`.           |                                                                                                |
| Coloured text   | Yes                       | Yes (Extended)        | Converts to `==highlighted markdown==`.   | Coloured text will be converted to single colour highlights.                                   |

### Attachments - Incomplete

All attachments are inserted into markdown as images, but extra metadata, like the location name for a specific location, may be also included as text. If you would like to only export the text of your journal entries into markdown, use the disable attachments [command line argument](#command-line-arguments).

Note the conversion of attachments is currently incomplete - but the goal is to support them all!

| Type          | Supported by this program       | Implementation                                       | Caveats |
| ------------- | ------------------------------- | ---------------------------------------------------- | ------- |
| Prompt        | Yes                             | Prompt is in ***bold italic text*** below the title. |         |
| Photos        | Not yet (working on it)         | -                                                    |         |
| Videos        | Not yet (working on it)         | -                                                    |         |
| Voice memo    | Not yet (planned)               | -                                                    |         |
| Location      | Not yet (planned)               | -                                                    |         |
| State of Mind | Not yet (planned)               | -                                                    |         |
| Music         | Not yet (planned)               | -                                                    |         |
| Workout       | Not yet (planned)               | -                                                    |         |


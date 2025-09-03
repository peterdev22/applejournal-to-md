import os
import glob
import sys
import re
from datetime import datetime
from bs4 import BeautifulSoup

HTML_DIR = sys.argv[1]
RESOURCES_DIR = "Resources"
OUTPUT_DIR = sys.argv[2]

# id each 's[INT]' class
# this must happen as apple journal generates the class styles in the order they are found in text
def id_classes(html):
    all_css = html.find('style').string
    styles = {}

    css_rule_pattern = r'span\.(s\d+)\s*\{([^}]+)\}' # finds the class from the selector, and the entire declaration
    for css_rule in re.finditer(css_rule_pattern, all_css):
        class_ = css_rule.group(1)
        declaration = css_rule.group(2)

        is_bold = 'font-weight: bold;' in declaration
        is_italic = 'font-style: italic;' in declaration
        is_underline = 'underline' in declaration
        is_strikethrough = 'line-through' in declaration
        style_config = [is_bold, is_italic, is_underline, is_strikethrough]
        
        styles[class_] = style_config # each class will have a 4 item array identifying how the text should be formatted

    return styles

# format text using its 'id'
def format_text(id, text):
    is_bold, is_italic, is_underline, is_strikethrough = id

    if is_strikethrough:
        text = f"~~{text}~~"
    if is_underline:
        text = f"<u>{text}</u>" # not a part of markdown, may not format correctly in some apps when combined with other styles
    if is_italic:
        text = f"*{text}*"
    if is_bold:
        text = f"**{text}**"

    return text

# create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Created folder '{OUTPUT_DIR}'")

# repeat this for all journal entries
for input_file in glob.glob(os.path.join(HTML_DIR, "*.html")):
    with open(input_file, "r", encoding="utf-8") as f:
        html = BeautifulSoup(f, "html.parser")

    # find text formatting styles
    format_config = id_classes(html)
    
    # find date
    date_fancy = html.find("div", class_="pageHeader").text
    date_iso = datetime.strptime(date_fancy, "%A %d %B %Y").date().isoformat()

    # find title
    title = html.find("span", class_="s2").text

    # find body text and format accordingly
    paragraphs = html.find_all("p", class_="p2")
    body = []

    for paragraph in paragraphs:
        paragraph_text = []

        for span in paragraph.find_all('span'):
            span_text = span.get_text()
            span_class = span.get("class")[0]
            valid_class_pattern = r's\d+' # only match s[INT] class names

            if re.match(valid_class_pattern, span_class):
                format_id = format_config[span_class]
                paragraph_text.append(format_text(format_id, span_text))

        body.append(''.join(paragraph_text))

    # ----------------- output ----------------------
    md = []
    filename = f"{date_iso}.md"

    # yaml properties (for use with obsidian)
    md.append("---")
    md.append("date: " + date_iso)
    md.append("---" + "\n")

    # title & body
    md.append("# " + title)

    for paragraph in body:
        md.append(paragraph + "\n")

    # write to file
    output_file = os.path.join(OUTPUT_DIR, filename)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    # ------------------------------------------------

    print(f"Converted '{OUTPUT_DIR}/{date_iso}.md'")
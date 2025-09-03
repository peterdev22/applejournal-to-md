import os
import glob
import argparse
import re
from datetime import datetime
from bs4 import BeautifulSoup

# command-line args
parser = argparse.ArgumentParser(prog='applejournal-to-md', description='Convert an Apple Journal HTML entries to Markdown.')
parser.add_argument('-i', '--input', default='Entries', required=False, help="Directory containing .html journal entries; The default is 'Entries'.")
parser.add_argument('-ir', '--inputres', default='Resources', required=False, help="Directory containing .heic, .mp4, .json journal entry attachments; The default is 'Resources'.")
parser.add_argument('-o', '--output', default='MarkdownOutput', required=False, help="Directory that will be created for output markdown files; The default is 'MarkdownOutput'.")
args = parser.parse_args()

HTML_DIR = args.input
RESOURCES_DIR = args.inputres
OUTPUT_DIR = args.output

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
        is_coloured = 'color: #' in declaration
        style_config = [is_bold, is_italic, is_underline, is_strikethrough, is_coloured]
        
        styles[class_] = style_config # each class will have a 5 item array identifying how the text should be formatted

    return styles

# format text using its 'id'
def format_text(id, text):
    is_bold, is_italic, is_underline, is_strikethrough, is_coloured = id

    if is_underline:
        text = f'<u>{text}</u>' # not a part of markdown, may not format correctly in some apps when combined with other styles
    if is_strikethrough:
        text = f'~~{text}~~' # (extended markdown)
    if is_italic:
        text = f'*{text}*'
    if is_bold:
        text = f'**{text}**'
    if is_coloured:
        text = f'=={text}==' # instead of colouring text, it will be highlighted (extended markdown)

    return text

# apply formatting using spans found within an element (p, blockquote, ul or ol)
def process_spans(element, format_config):
    element_text = []

    for span in element.find_all('span'):
        span_text = span.get_text()
        span_class = span.get('class')[0]
        valid_class_pattern = r's\d+' # only match s[INT] class names

        if re.match(valid_class_pattern, span_class):
            format_id = format_config[span_class]
            element_text.append(format_text(format_id, span_text))

    return ''.join(element_text)

# create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Created folder '{OUTPUT_DIR}'")

# repeat this for all journal entries
for input_file in glob.glob(os.path.join(HTML_DIR, '*.html')):
    with open(input_file, 'r', encoding='utf-8') as f:
        html = BeautifulSoup(f, 'html.parser')

    # find text formatting styles
    format_config = id_classes(html)
    
    # find date
    date_fancy = html.find('div', class_='pageHeader').text
    date_iso = datetime.strptime(date_fancy, '%A %d %B %Y').date().isoformat()

    # find title
    title = html.find('span', class_='s2').text

    # find body text and format accordingly
    body_elements = html.find_all(['p', 'blockquote', 'ol', 'ul'])
    body = []

    for element in body_elements:
        # paragraphs
        if element.name == 'p' and element.get('class')[0] == 'p2':
            paragraph_text = process_spans(element, format_config)
            body.append(paragraph_text)
            body.append('')
        # quotes
        elif element.name == 'blockquote':
            quote_text = process_spans(element, format_config)
            body.append(f'> {quote_text}')
            body.append('')
        # ordered lists
        elif element.name == 'ol':
            list = element.find_all('li')
            for i, item in enumerate(list, 1):
                item_text = process_spans(item, format_config)
                body.append(f'{i}. {item_text}')
            body.append('')
        # unordered lists
        elif element.name == 'ul':
            list = element.find_all('li')
            for item in list:
                item_text = process_spans(item, format_config)
                body.append(f'- {item_text}')
            body.append('')

    # ----------------- output ----------------------
    md = []
    filename = f'{date_iso}.md'

    # yaml properties (for use with obsidian)
    md.append('---')
    md.append('date: ' + date_iso)
    md.append('---' + '\n')

    # title & body
    md.append('# ' + title)

    for line in body:
        md.append(line)

    # write to file
    output_file = os.path.join(OUTPUT_DIR, filename)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    # ------------------------------------------------

    print(f"Converted '{OUTPUT_DIR}/{date_iso}.md'")
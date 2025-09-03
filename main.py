import os
import glob
import sys
from datetime import datetime
from bs4 import BeautifulSoup

HTML_DIR = sys.argv[1]
RESOURCES_DIR = "Resources"
OUTPUT_DIR = sys.argv[2]

# create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Created folder '{OUTPUT_DIR}'")

# for all journal entries
for input_file in glob.glob(os.path.join(HTML_DIR, "*.html")):
    with open(input_file, "r", encoding="utf-8") as f:
        html = BeautifulSoup(f, "html.parser")
    
    # date
    date_fancy = html.find("div", class_="pageHeader").text
    date_iso = datetime.strptime(date_fancy, "%A %d %B %Y").date().isoformat()

    # title
    title = html.find("span", class_="s2").text

    # body
    paragraphs = html.find_all("span", class_="s3")
    body = [paragraph.text for paragraph in paragraphs]

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
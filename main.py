import os
import glob
from datetime import datetime
from bs4 import BeautifulSoup

HTML_DIR = "Entries"
RESOURCES_DIR = "Resources"
OUTPUT_DIR = "md-output"

print("program run:")

# create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

# for all journal entries
for file in glob.glob(os.path.join(HTML_DIR, "*.html")):
    with open(file, "r", encoding="utf-8") as f:
        html = BeautifulSoup(f, "html.parser")
    
    # date
    date_fancy = html.find("div", class_="pageHeader").text
    date_iso = datetime.strptime(date_fancy, "%A %d %B %Y").date().isoformat()

    # title
    title = html.find("span", class_="s2").text

    # body
    paragraphs = html.find_all("span", class_="s3")
    body = [paragraph.text for paragraph in paragraphs]

    print(date_fancy)
    print(date_iso)
    print(title)
    print(body)

    # output
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

    #write to file
    o_path = os.path.join(OUTPUT_DIR, filename)
    with open(o_path, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(md))
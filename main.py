import os
import glob
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
    
    date = html.find("div", class_="pageHeader")
    title = html.find("span", class_="s2")

    print(date)
    print(title)
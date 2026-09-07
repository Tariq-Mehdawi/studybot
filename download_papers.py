import os
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

DATA_FOLDER = "data"
SEARCH_QUERY = '"retrieval augmented generation"'
MAX_PAPERS = 8

API_URL = (
    "http://export.arxiv.org/api/query"
    f"?search_query=all:{urllib.parse.quote(SEARCH_QUERY)}"
    f"&start=0&max_results={MAX_PAPERS}"
    "&sortBy=relevance"
)

NS = {"atom": "http://www.w3.org/2005/Atom"}

os.makedirs(DATA_FOLDER, exist_ok=True)

print(f"Searching arXiv for: {SEARCH_QUERY}")
with urllib.request.urlopen(API_URL) as response:
    feed = response.read()

root = ET.fromstring(feed)
entries = root.findall("atom:entry", NS)
print(f"Found {len(entries)} papers\n")

for entry in entries:
    title = entry.find("atom:title", NS).text.strip().replace("\n", " ")

    pdf_url = None
    for link in entry.findall("atom:link", NS):
        if link.get("title") == "pdf":
            pdf_url = link.get("href")

    if not pdf_url:
        print(f"  skipped (no PDF): {title[:60]}")
        continue

    safe_name = "".join(c for c in title if c.isalnum() or c in " -_")[:60]
    path = os.path.join(DATA_FOLDER, f"{safe_name}.pdf")

    if os.path.exists(path):
        print(f"  already have: {title[:60]}")
        continue

    print(f"  downloading: {title[:60]}...")
    urllib.request.urlretrieve(pdf_url, path)
    time.sleep(3)

print(f"\nDone. Files are in {DATA_FOLDER}/")
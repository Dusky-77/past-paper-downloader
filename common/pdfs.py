import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .constants import BASE, HEADERS, WANT


def get_pdfs(session_url, code):
    r = requests.get(session_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    pdfs = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "directories/CAIE/CAIE-pastpapers/upload/" in href and href.endswith(".pdf"):
            full = href if href.startswith("http") else urljoin(BASE, href)
            if "download_file.php" in full:
                m = re.search(r"files=(https?://[^&]+\.pdf)", full)
                if m:
                    full = m.group(1)
            name = full.split("/")[-1]
            if name.startswith(code):
                parts = name.split("_")
                if len(parts) >= 4 and parts[2] in WANT:
                    pdfs.append((name, full))
    return list(dict.fromkeys(pdfs))

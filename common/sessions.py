import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .constants import BASE, HEADERS


def get_sessions(subject_path, extra_sessions=None):
    url = f"{BASE}/papers/caie/{subject_path}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    sessions = []
    seen = set()
    pattern = re.compile(
        rf"{subject_path}-(20\d{{2}})-(may-june|oct-nov|march|feb-march|jun|nov|mar)$",
        re.I,
    )
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        m = pattern.search(href)
        if not m:
            continue
        full = urljoin(BASE, href)
        if full in seen or "papers/caie/papers/caie" in full:
            continue
        seen.add(full)
        name = a.get_text(strip=True) or href.split("/")[-1]
        sessions.append((name, full))
    if extra_sessions:
        for name, full in extra_sessions:
            if full not in seen:
                sessions.append((name, full))
                seen.add(full)
    return sessions

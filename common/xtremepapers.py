import sys
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

from .constants import HEADERS, XTREME_BASE, XTREME_SUBJECTS

_cache = {}
_diagnosed = set()

_CHALLENGE_MARKERS = (
    "cf-browser-verification",
    "cf-challenge",
    "checking your browser",
    "captcha",
)


def _subject_path(code):
    if code not in XTREME_SUBJECTS:
        return None
    level, folder = XTREME_SUBJECTS[code]
    return f"CAIE/{level}/{folder}"


def _list_url(code):
    path = _subject_path(code)
    if not path:
        return None
    return f"{XTREME_BASE}/index.php?dirpath=./{quote(path)}/&order=0"


def _direct_url(code, filename):
    path = _subject_path(code)
    if not path:
        return None
    return f"{XTREME_BASE}/{quote(path)}/{quote(filename)}"


def _fetch_listing(code):
    key = code
    if key in _cache:
        return _cache[key]
    trace = []
    url = _list_url(code)
    if not url:
        trace.append(f"code {code} not in XTREME_SUBJECTS")
        _cache[key] = {}
        _diagnose(key, trace)
        return {}
    try:
        r = requests.get(url, headers=HEADERS, timeout=45)
    except Exception as e:
        trace.append(f"{url} -----> EXCEPTION {e}")
        _cache[key] = {}
        _diagnose(key, trace)
        return {}
    if r.status_code != 200:
        trace.append(f"{url} -----> HTTP {r.status_code}")
        _cache[key] = {}
        _diagnose(key, trace)
        return {}
    body_lower = r.text.lower()
    if any(m in body_lower for m in _CHALLENGE_MARKERS):
        trace.append(f"{url} -----> anti-bot challenge")
        _cache[key] = {}
        _diagnose(key, trace)
        return {}
    soup = BeautifulSoup(r.text, "html.parser")
    by_name = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        name = a.get_text(strip=True)
        if not name.endswith(".pdf"):
            continue
        if name.startswith(code) or name.startswith(f"{code}_"):
            by_name[name] = _direct_url(code, name)
    trace.append(f"{url} -----> {len(by_name)} matching pdfs")
    _cache[key] = by_name
    _diagnose(key, trace, by_name)
    return by_name


def _diagnose(key, trace, by_name=None):
    if key in _diagnosed:
        return
    _diagnosed.add(key)
    for line in trace:
        print(f"  [xtremepapers probe] {line}", file=sys.stderr)
    if by_name:
        sample = sorted(by_name.keys())
        print(f"  [xtremepapers probe] sample: {sample[:8]}", file=sys.stderr)


def find_file(code, filename):
    files = _fetch_listing(code)
    return files.get(filename)


def get_all_files(code):
    return _fetch_listing(code)

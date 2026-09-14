import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .constants import HEADERS, PASTPAPERS_CO_BASE, PASTPAPERS_CO_SUBJECTS

_cache = {}
_diagnosed = set()

SEASON_SLUGS_NEW = {"s": ["may-june"], "w": ["oct-nov"], "m": ["march"]}
SEASON_SLUGS_OLD = {"s": ["jun"], "w": ["nov"], "m": ["mar"]}


_CHALLENGE_MARKERS = (
    "cf-browser-verification",
    "cf-challenge",
    "checking your browser",
    "captcha",
)


def _to_download_url(pdf_url):
    path = pdf_url.split(PASTPAPERS_CO_BASE, 1)[-1].lstrip("/")
    return f"{PASTPAPERS_CO_BASE}/api/file/{path}?download=1"


def _fetch_links(url, trace):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
    except Exception as e:
        trace.append(f"{url} -> EXCEPTION {e}")
        return []
    if r.status_code != 200:
        trace.append(f"{url} -> HTTP {r.status_code}")
        return []
    body_lower = r.text.lower()
    if any(marker in body_lower for marker in _CHALLENGE_MARKERS):
        trace.append(f"{url} -> HTTP 200 but anti-bot challenge page, not real content")
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".pdf"):
            out.append(urljoin(PASTPAPERS_CO_BASE, href))
    if not out:
        trace.append(f"{url} -> HTTP 200, 0 pdf links, page length {len(r.text)} chars")
    else:
        trace.append(f"{url} -> HTTP 200, {len(out)} pdf links")
    return out


def get_session_files(code, year, season):
    key = (code, year, season)
    if key in _cache:
        return _cache[key]
    trace = []
    if code not in PASTPAPERS_CO_SUBJECTS:
        trace.append(f"code {code} not in PASTPAPERS_CO_SUBJECTS")
        _cache[key] = {}
        _diagnose(key, trace)
        return {}
    level, slug = PASTPAPERS_CO_SUBJECTS[code]
    base = f"{PASTPAPERS_CO_BASE}/caie/{level}/{slug}"
    slugs = SEASON_SLUGS_NEW[season] if year >= 2018 else SEASON_SLUGS_OLD[season]
    links = []
    for season_slug in slugs:
        folder = (
            f"{base}/{year}-{season_slug}"
            if year >= 2018
            else f"{base}/{year}/{year}-{season_slug}"
        )
        links = _fetch_links(folder, trace)
        if links:
            break
    by_name = {link.split("/")[-1]: _to_download_url(link) for link in links}
    _cache[key] = by_name
    _diagnose(key, trace, by_name)
    return by_name


def _diagnose(key, trace, by_name=None):
    if key in _diagnosed:
        return
    _diagnosed.add(key)
    for line in trace:
        print(f"  [pastpapers.co probe] {line}", file=sys.stderr)
    if by_name:
        sample = sorted(by_name.keys())
        print(
            f"  [pastpapers.co probe] sample filenames found: {sample[:8]}",
            file=sys.stderr,
        )
        qp_ms = [n for n in sample if "_qp_" in n or "_ms_" in n]
        print(
            f"  [pastpapers.co probe] {len(qp_ms)}/{len(sample)} are qp/ms files: {qp_ms[:10]}",
            file=sys.stderr,
        )


def find_file(code, year, season, filename):
    files = get_session_files(code, year, season)
    return files.get(filename)

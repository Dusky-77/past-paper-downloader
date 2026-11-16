import re
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .constants import BESTEXAMHELP_BASE, BESTEXAMHELP_SUBJECTS, HEADERS

_cache = {}
_diagnosed = set()

SEASON_SLUG = {"s": "summer", "w": "winter", "m": "march"}

_CHALLENGE_MARKERS = (
    "cf-browser-verification",
    "cf-challenge",
    "checking your browser",
    "captcha",
)


def _session_url(code, year, season):
    if code not in BESTEXAMHELP_SUBJECTS:
        return None
    level, slug = BESTEXAMHELP_SUBJECTS[code]
    season_slug = SEASON_SLUG.get(season)
    if not season_slug:
        return None
    return f"{BESTEXAMHELP_BASE}/exam/{level}/{slug}/{year}/{season_slug}.php"


def _pdf_url(code, year, season, filename):
    if code not in BESTEXAMHELP_SUBJECTS:
        return None
    level, slug = BESTEXAMHELP_SUBJECTS[code]
    return f"{BESTEXAMHELP_BASE}/exam/{level}/{slug}/{year}/{filename}"


def _fetch_session(code, year, season):
    key = (code, year, season)
    if key in _cache:
        return _cache[key]
    trace = []
    url = _session_url(code, year, season)
    if not url:
        trace.append(f"code {code} not in BESTEXAMHELP_SUBJECTS or bad season")
        _cache[key] = {}
        _diagnose(key, trace)
        return {}
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
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
        href = a["href"].strip()
        base = href.split("/")[-1]
        if not re.match(rf"{code}-[swm]\d{{2}}-(qp|ms|er)", base, re.I):
            continue
        fname = base.replace(".php", ".pdf").replace("-", "_")
        if not fname.startswith(code):
            continue
        by_name[fname] = _pdf_url(code, year, season, fname)
    if not by_name:
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".pdf") and code in href:
                name = href.split("/")[-1]
                by_name[name] = urljoin(url, href)
    trace.append(f"{url} -----> {len(by_name)} pdfs")
    _cache[key] = by_name
    _diagnose(key, trace, by_name)
    return by_name


def _diagnose(key, trace, by_name=None):
    if key in _diagnosed:
        return
    _diagnosed.add(key)
    for line in trace:
        print(f"  [bestexamhelp probe] {line}", file=sys.stderr)
    if by_name:
        sample = sorted(by_name.keys())
        print(f"  [bestexamhelp probe] sample: {sample[:10]}", file=sys.stderr)


def find_file(code, year, season, filename):
    files = _fetch_session(code, year, season)
    if filename in files:
        return files[filename]
    direct = _pdf_url(code, year, season, filename)
    if direct:
        return direct
    return None


def get_session_files(code, year, season):
    return _fetch_session(code, year, season)

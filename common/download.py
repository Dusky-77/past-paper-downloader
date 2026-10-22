import re
import sys
import threading
import time

import requests

from .constants import DELAY, DYNAMICOPERS_BASE, HEADERS
from .pastpapers_co import find_file as ppco_find
from .xtremepapers import find_file as xtreme_find

_dynamic_dead_lock = threading.Lock()
_dynamic_failures = 0
_DYNAMIC_FAILURE_LIMIT = 5

SOURCES = ("primary", "pastpapers.co", "dynamic", "xtremepapers")


def _dynamic_is_dead():
    return _dynamic_failures >= _DYNAMIC_FAILURE_LIMIT


def _record_dynamic_failure():
    global _dynamic_failures
    with _dynamic_dead_lock:
        _dynamic_failures += 1


def _try_url(url, path, label="", referer=None):
    headers = dict(HEADERS)
    headers["Accept"] = "application/pdf,*/*;q=0.8"
    if referer:
        headers["Referer"] = referer
    try:
        r = requests.get(url, headers=headers, timeout=60)
    except Exception as e:
        if label:
            print(f"    [{label}] {url} -> EXCEPTION {e}", file=sys.stderr)
        return False
    if r.status_code != 200:
        if label:
            print(f"    [{label}] {url} -> HTTP {r.status_code}", file=sys.stderr)
        return False
    data = r.content
    if len(data) >= 2000 and data.startswith(b"%PDF"):
        path.write_bytes(data)
        return True
    if label:
        print(
            f"    [{label}] {url} -> HTTP 200 but not a valid PDF "
            f"({len(data)} bytes, starts with {data[:20]!r})",
            file=sys.stderr,
        )
    return False


def _parse_name(name):
    m = re.match(r"(\d{4})_([swm])(\d{2})_(qp|ms|er)(?:_(\d+))?\.pdf", name)
    if not m:
        return None
    c, season, yy, kind, paper = m.groups()
    return c, season, 2000 + int(yy), kind, paper


def download_one(name, url, folder, code, only_source=None):
    path = folder / name
    if path.exists() and path.stat().st_size > 2000:
        return f"skip {name}"

    parsed = _parse_name(name)

    def try_primary():
        if url.startswith("https://dummy/"):
            return False
        return _try_url(url, path, "primary")

    def try_ppco():
        if not parsed:
            return False
        c, season, year, _, _ = parsed
        real = ppco_find(c, year, season, name)
        if real is None:
            print(
                f"    [pastpapers.co] {name} -> not found in session listing",
                file=sys.stderr,
            )
            return False
        return _try_url(real, path, "pastpapers.co", referer="https://pastpapers.co/")

    def try_dynamic():
        if _dynamic_is_dead():
            return False
        ok = _try_url(f"{DYNAMICOPERS_BASE}/{name}", path, "dynamic")
        if not ok:
            _record_dynamic_failure()
        return ok

    def try_xtreme():
        real = xtreme_find(code, name)
        if real is None:
            print(
                f"    [xtremepapers] {name} -> not found in subject listing",
                file=sys.stderr,
            )
            return False
        return _try_url(
            real, path, "xtremepapers", referer="https://papers.xtremepape.rs/"
        )

    order = {
        "primary": try_primary,
        "pastpapers.co": try_ppco,
        "dynamic": try_dynamic,
        "xtremepapers": try_xtreme,
    }

    if only_source:
        if only_source not in order:
            return f"bad  {name} (unknown source {only_source})"
        if order[only_source]():
            time.sleep(DELAY)
            return f"get  {name} ({only_source})"
        return f"bad  {name}"

    if try_primary():
        time.sleep(DELAY)
        return f"get  {name}"
    if try_ppco():
        time.sleep(DELAY)
        return f"get  {name} (pastpapers.co)"
    if try_dynamic():
        time.sleep(DELAY)
        return f"get  {name} (dynamic)"
    if try_xtreme():
        time.sleep(DELAY)
        return f"get  {name} (xtremepapers)"
    return f"bad  {name}"

import re
import sys
import threading
import time

import requests

from .constants import DELAY, DYNAMICOPERS_BASE, HEADERS
from .pastpapers_co import find_file

_dynamic_dead_lock = threading.Lock()
_dynamic_failures = 0
_DYNAMIC_FAILURE_LIMIT = 5


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


def download_one(name, url, folder, code):
    path = folder / name
    if path.exists() and path.stat().st_size > 2000:
        return f"skip {name}"

    if not url.startswith("https://dummy/") and _try_url(url, path, "primary"):
        time.sleep(DELAY)
        return f"get  {name}"

    m = re.match(r"(\d{4})_([swm])(\d{2})_(qp|ms|er)(?:_(\d+))?\.pdf", name)
    if m:
        c, season, yy, _kind, _paper = m.groups()
        year = 2000 + int(yy)
        real_url = find_file(c, year, season, name)
        if real_url is None:
            print(
                f"    [pastpapers.co] {name} -> not found in session listing",
                file=sys.stderr,
            )
        elif _try_url(
            real_url, path, "pastpapers.co", referer="https://pastpapers.co/"
        ):
            time.sleep(DELAY)
            return f"get  {name} (pastpapers.co)"

    if not _dynamic_is_dead():
        if _try_url(f"{DYNAMICOPERS_BASE}/{name}", path, "dynamic"):
            time.sleep(DELAY)
            return f"get  {name} (dynamic)"
        _record_dynamic_failure()

    return f"bad  {name}"

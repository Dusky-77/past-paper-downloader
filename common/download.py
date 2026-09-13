import re
import time
from pathlib import Path

import requests

from .constants import DELAY, HEADERS


def download_one(name, url, folder, code):
    path = folder / name
    if path.exists() and path.stat().st_size > 2000:
        return f"skip {name}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        data = r.content
        if len(data) >= 2000 and data.startswith(b"%PDF"):
            path.write_bytes(data)
            time.sleep(DELAY)
            return f"get  {name}"
    except Exception:
        pass
    try:
        fb1 = f"https://dynamicpapers.com/wp-content/uploads/2015/09/{name}"
        r2 = requests.get(fb1, headers=HEADERS, timeout=60)
        if (
            r2.status_code == 200
            and r2.content.startswith(b"%PDF")
            and len(r2.content) > 2000
        ):
            path.write_bytes(r2.content)
            time.sleep(DELAY)
            return f"get  {name} (dynamic)"
    except Exception:
        pass
    try:
        m = re.match(r"(\d{4})_([swm])(\d{2})_(qp|ms)_(\d+)\.pdf", name)
        if m:
            c, season, yy, kind, paper = m.groups()
            year = 2000 + int(yy)
            season_map = {"s": "May-June", "w": "Oct-Nov", "m": "March"}
            season_name = season_map.get(season, "May-June")
            level = "O-Level" if c in ("5070", "5054", "4024", "4037") else "IGCSE"
            subj_map = {
                "0620": "Chemistry-0620",
                "0625": "Physics-0625",
                "0580": "Mathematics-0580",
                "0606": "Additional-Mathematics-0606",
                "5070": "Chemistry-5070",
                "5054": "Physics-5054",
                "4024": "Mathematics-D-4024",
                "4037": "Additional-Mathematics-4037",
            }
            subj = subj_map.get(c, f"Chemistry-{c}")
            fb2 = (
                f"https://pastpapers.co/caie/{level}/{subj}/{year}-{season_name}/{name}"
            )
            r3 = requests.get(fb2, headers=HEADERS, timeout=60)
            if (
                r3.status_code == 200
                and r3.headers.get("content-type", "").startswith("application/pdf")
                and r3.content.startswith(b"%PDF")
                and len(r3.content) > 2000
            ):
                path.write_bytes(r3.content)
                time.sleep(DELAY)
                return f"get  {name} (pastpapers.co)"
    except Exception:
        pass
    return f"bad  {name}"

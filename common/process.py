import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .constants import MAX_WORKERS
from .download import download_one
from .pdfs import get_pdfs


def session_already_done(folder, expected_count):
    if not folder.exists():
        return False
    return len(list(folder.glob("*.pdf"))) >= expected_count * 0.8


def process_session(name, surl, code, year_from, year_to, dry_run, out_dir, papers):
    y = re.search(r"20\d{2}", name or surl)
    if not y:
        return
    year = int(y.group())
    if not (year_from <= year <= year_to):
        return
    folder = out_dir / name.replace(" ", "_")
    pdfs = get_pdfs(surl, code)
    expected_season = (
        "w"
        if "oct" in name.lower() or "nov" in name.lower()
        else "m"
        if "mar" in name.lower()
        else "s"
    )
    expected_yy = f"{year % 100:02d}"
    good = [p for p in pdfs if f"_{expected_season}{expected_yy}_" in p[0]]
    if len(good) < 4 or (code == "0625" and year < 2016):
        print(f"{name}: PapaCambridge incomplete – generating correct filenames")
        pdfs = []
        for p in papers:
            for kind in ("qp", "ms"):
                for v in (1, 2, 3):
                    fname = f"{code}_{expected_season}{expected_yy}_{kind}_{p}{v}.pdf"
                    pdfs.append((fname, f"https://dummy/{fname}"))
    else:
        pdfs = good
    if not pdfs:
        print(f"{name}: no pdfs")
        return
    if session_already_done(folder, len(pdfs)) and not dry_run:
        print(f"{name}: already done, skip")
        return
    print(f"\n=== {name} ({len(pdfs)} files) ===")
    folder.mkdir(exist_ok=True)
    if dry_run:
        for pname, _ in pdfs:
            print(f"would get {pname}")
        return
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(download_one, n, u, folder, code): n for n, u in pdfs}
        for fut in as_completed(futures):
            print(fut.result())

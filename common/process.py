import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .constants import MAX_WORKERS, WANT
from .download import download_one
from .pdfs import get_pdfs

MARCH_VARIANTS = (2,)
MAIN_VARIANTS = (1, 2, 3)


def session_already_done(folder, expected_count):
    if not folder.exists():
        return False
    return len(list(folder.glob("*.pdf"))) >= expected_count * 0.8


def _fabricate(code, season, expected_yy, papers):
    if code == "0625" and int(expected_yy) < 16:
        papers = [p for p in papers if p != 4]
    pdfs = []
    kinds = [k for k in WANT if k in ("qp", "ms")]  # only paper-based kinds
    for p in papers:
        for kind in kinds:
            variants = (2,) if season == "m" else (1, 2, 3)
            for v in variants:
                fname = f"{code}_{season}{expected_yy}_{kind}_{p}{v}.pdf"
                pdfs.append((fname, f"https://dummy/{fname}"))
    # ER is session-level (no paper number)
    if "er" in WANT:
        fname = f"{code}_{season}{expected_yy}_er.pdf"
        pdfs.append((fname, f"https://dummy/{fname}"))
    return pdfs


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
    expected_count = len(papers) * 2 * (1 if expected_season == "m" else 3)
    if len(good) < 4:
        print(f"{name}: PapaCambridge incomplete – generating correct filenames")
        pdfs = _fabricate(code, expected_season, expected_yy, papers)
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
        results = [fut.result() for fut in as_completed(futures)]
    for r in sorted(results):
        print(r)
    bad = [r for r in results if r.startswith("bad")]
    if bad:
        bad_names = [r.split()[1] for r in bad]
        print(f"{name}: {len(bad)}/{len(results)} missing -> {bad_names}")
        with open(out_dir / "missing.log", "a") as f:
            for n in bad_names:
                f.write(f"{name}: {n}\n")

from pathlib import Path

from .merge import collect_and_merge
from .process import process_session
from .sessions import get_sessions


def run_subject(
    code, name, path, papers, year_from, year_to, dry_run, extra_sessions=None
):
    out_dir = Path(f"{code}_{name.replace(' ', '_')}")
    out_dir.mkdir(exist_ok=True)
    sessions = get_sessions(path, extra_sessions)
    print(f"\nfound {len(sessions)} sessions")
    for sname, surl in sessions:
        process_session(sname, surl, code, year_from, year_to, dry_run, out_dir, papers)
    if not dry_run:
        print("\nmerging per paper...")
        for paper in papers:
            collect_and_merge("qp", paper, year_from, year_to, code, out_dir)
            collect_and_merge("ms", paper, year_from, year_to, code, out_dir)
        _report_missing(out_dir, code)
    print("\ndone")


def _report_missing(out_dir, code):
    log_path = out_dir / "missing.log"
    if not log_path.exists():
        print(f"\n{code}: coverage report -> no gaps recorded")
        return
    lines = [l for l in log_path.read_text().splitlines() if l.strip()]
    print(f"\n{code}: coverage report -> {len(lines)} files never obtained")
    for l in lines:
        print(f"  {l}")

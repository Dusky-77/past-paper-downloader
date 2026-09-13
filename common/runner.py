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
    print("\ndone")

from common.constants import BASE
from common.runner import run_subject


def run(year_from, year_to, dry_run):
    extra = [
        (
            "2024-Oct-Nov",
            f"{BASE}/papers/caie/o-level-mathematics-additional-4037-mathematics-additional-40372024-oct-nov",
        ),
        (
            "2020-May-June",
            f"{BASE}/papers/caie/o-level-mathematics-additional-4037-may-june-2020",
        ),
        (
            "2015_Jun",
            f"{BASE}/papers/caie/o-level-mathematics-additional-4037-2015-june",
        ),
        # 2012 jun dont exist lol
    ]
    run_subject(
        code="4037",
        name="O-Level Additional Mathematics",
        path="o-level-mathematics-additional-4037",
        papers=range(1, 3),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
        extra_sessions=extra,
    )

from common.constants import BASE
from common.runner import run_subject


def run(year_from, year_to, dry_run):
    extra = [
        ("2025-Oct-Nov", f"{BASE}/papers/caie/o-level-chemistry-5070-2025-oct-nov"),
        ("2024-Oct-Nov", f"{BASE}/papers/caie/o-level-chemistry-5070-2024-oct-nov"),
    ]
    run_subject(
        code="5070",
        name="O-Level Chemistry",
        path="o-level-chemistry-5070",
        papers=range(1, 5),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
        extra_sessions=extra,
    )

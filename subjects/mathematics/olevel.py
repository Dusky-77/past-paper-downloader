from common.constants import BASE
from common.runner import run_subject


def run(year_from, year_to, dry_run):
    extra = [
        (
            "2024-Oct-Nov",
            f"{BASE}/papers/caie/o-level-mathematics-d-calculator-version-4024-mathematics-d-40242024-oct-nov",
        ),
        (
            "2020-May-June",
            f"{BASE}/papers/caie/o-level-mathematics-d-calculator-version-4024-may-june-2020",
        ),
    ]

    run_subject(
        code="4024",
        name="O-Level Mathematics",
        path="o-level-mathematics-d-calculator-version-4024",
        papers=range(1, 3),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
        extra_sessions=extra,
    )

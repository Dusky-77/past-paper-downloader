from common.constants import BASE
from common.runner import run_subject


def run(year_from, year_to, dry_run):
    extra = [
        (
            "2020-May-June",
            f"{BASE}/papers/caie/igcse-mathematics-0606-may-june-2020",
        ),
    ]
    run_subject(
        code="0606",
        name="IGCSE Additional Mathematics",
        path="igcse-mathematics-0606",
        papers=range(1, 3),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
        extra_sessions=extra,
    )

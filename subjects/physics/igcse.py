from common.constants import BASE
from common.runner import run_subject


def run(year_from, year_to, dry_run):
    run_subject(
        code="0625",
        name="IGCSE Physics",
        path="igcse-physics-0625",
        papers=range(1, 7),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
    )


# p4 dont exist for pre-2016

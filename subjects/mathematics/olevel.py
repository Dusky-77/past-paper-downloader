from common.runner import run_subject


def run(year_from, year_to, dry_run):
    run_subject(
        code="4024",
        name="O-Level Mathematics",
        path="o-level-mathematics-d-4024",
        papers=range(1, 3),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
    )

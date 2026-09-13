from common.runner import run_subject


def run(year_from, year_to, dry_run):
    run_subject(
        code="4037",
        name="O-Level Additional Mathematics",
        path="o-level-additional-mathematics-4037",
        papers=range(1, 3),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
    )

from common.runner import run_subject


def run(year_from, year_to, dry_run):
    run_subject(
        code="0580",
        name="IGCSE Mathematics",
        path="igcse-mathematics-0580",
        papers=range(1, 5),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
    )

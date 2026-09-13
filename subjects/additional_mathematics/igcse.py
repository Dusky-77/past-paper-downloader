from common.runner import run_subject


def run(year_from, year_to, dry_run):
    run_subject(
        code="0606",
        name="IGCSE Additional Mathematics",
        path="igcse-additional-mathematics-0606",
        papers=range(1, 3),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
    )

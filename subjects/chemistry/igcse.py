from common.runner import run_subject


def run(year_from, year_to, dry_run):
    run_subject(
        code="0620",
        name="IGCSE Chemistry",
        path="igcse-chemistry-0620",
        papers=range(1, 7),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
    )

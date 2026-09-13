from common.constants import BASE
from common.runner import run_subject


def run(year_from, year_to, dry_run):
    extra = []
    for y in range(max(year_from, 2010), min(year_to + 1, 2016)):
        for season, slug in [("s", "jun"), ("w", "nov"), ("m", "mar")]:
            name = f"{y} {'May-June' if season == 's' else 'Oct-Nov' if season == 'w' else 'March'}"
            url = f"{BASE}/papers/caie/igcse-physics-0625-{y}-{slug}"
            extra.append((name, url))

    run_subject(
        code="0625",
        name="IGCSE Physics",
        path="igcse-physics-0625",
        papers=range(1, 7),
        year_from=year_from,
        year_to=year_to,
        dry_run=dry_run,
        extra_sessions=extra,
    )

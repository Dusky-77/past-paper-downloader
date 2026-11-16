BASE = "https://pastpapers.papacambridge.com"
DELAY = 1
MAX_WORKERS = 6

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

WANT = {"er"}

DYNAMICOPERS_BASE = "https://dynamicpapers.com/wp-content/uploads/2015/09"
PASTPAPERS_CO_BASE = "https://pastpapers.co"
XTREME_BASE = "https://papers.xtremepape.rs"
BESTEXAMHELP_BASE = "https://bestexamhelp.com"

PASTPAPERS_CO_SUBJECTS = {
    "0620": ("igcse", "chemistry-0620"),
    "5070": ("o-level", "chemistry-5070"),
    "0625": ("igcse", "physics-0625"),
    "5054": ("o-level", "physics-5054"),
    "0580": ("igcse", "mathematics-0580"),
    "4024": ("o-level", "Mathematics-D-4024"),
    "0606": ("igcse", "mathematics-0606"),
    "4037": ("o-level", "mathematics-additional-4037"),
    "0610": ("igcse", "biology-0610"),
    "5090": ("o-level", "biology-5090"),
}

XTREME_SUBJECTS = {
    "0620": ("IGCSE", "Chemistry (0620)"),
    "5070": ("O Level", "Chemistry (5070)"),
    "0625": ("IGCSE", "Physics (0625)"),
    "5054": ("O Level", "Physics (5054)"),
    "0580": ("IGCSE", "Mathematics (0580)"),
    "4024": ("O Level", "Mathematics D (4024)"),
    "0606": ("IGCSE", "Mathematics - Additional (0606)"),
    "4037": ("O Level", "Mathematics - Additional (4037)"),
    "0610": ("IGCSE", "Biology (0610)"),
    "5090": ("O Level", "Biology (5090)"),
}

BESTEXAMHELP_SUBJECTS = {
    "0610": ("cambridge-igcse", "biology-0610"),
    "5090": ("cambridge-o-level", "biology-5090"),
    "0620": ("cambridge-igcse", "chemistry-0620"),
    "5070": ("cambridge-o-level", "chemistry-5070"),
    "0625": ("cambridge-igcse", "physics-0625"),
    "5054": ("cambridge-o-level", "physics-5054"),
    "0580": ("cambridge-igcse", "mathematics-0580"),
    "4024": ("cambridge-o-level", "mathematics-d-4024"),
    "0606": ("cambridge-igcse", "mathematics-additional-0606"),
    "4037": ("cambridge-o-level", "mathematics-additional-4037"),
}

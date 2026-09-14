BASE = "https://pastpapers.papacambridge.com"
DELAY = 1.9
MAX_WORKERS = 6

# yea i used ai for these headers lol
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

WANT = {"qp", "ms"}

DYNAMICOPERS_BASE = "https://dynamicpapers.com/wp-content/uploads/2015/09"
PASTPAPERS_CO_BASE = "https://pastpapers.co"

PASTPAPERS_CO_SUBJECTS = {
    "0620": ("igcse", "chemistry-0620"),
    "5070": ("o-level", "chemistry-5070"),
    "0625": ("igcse", "physics-0625"),
    "5054": ("o-level", "physics-5054"),
    "0580": ("igcse", "mathematics-0580"),
    "4024": ("o-level", "Mathematics-D-4024"),
    "0606": ("igcse", "mathematics-0606"),
    "4037": ("o-level", "mathematics-additional-4037"),
}

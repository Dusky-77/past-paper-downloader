# Past Paper Fetcher

Personal tool to download and compile Cambridge IGCSE / O-Level past papers + mark schemes into yearly combined PDFs.

## Supported subjects

| Code | Subject                        |
| ---- | ------------------------------ |
| 0620 | IGCSE Chemistry                |
| 5070 | O-Level Chemistry              |
| 0625 | IGCSE Physics                  |
| 5054 | O-Level Physics                |
| 0580 | IGCSE Mathematics              |
| 4024 | O-Level Mathematics            |
| 0606 | IGCSE Additional Mathematics   |
| 4037 | O-Level Additional Mathematics |

## Features

- Downloads only QP + MS
- Skips already-downloaded sessions
- Multithreaded (4 workers) with polite delays
- Automatic fallbacks (DynamicPapers → pastpapers.co) when PapaCambridge is incomplete
- Merges into per-paper Yearlies (`2010-2026 0620 P1 QP Yearlies.pdf` etc.)
- Interactive: choose subject code, year range, dry-run

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Enter subject code (e.g. `0625`)
2. Enter year range (e.g. `2010` → `2026`)
3. Choose dry-run (`y`/`n`)

Output folders are created next to `main.py`:

```
0620_IGCSE_Chemistry/
0625_IGCSE_Physics/
5070_O-Level_Chemistry/
...
```

## Project structure

```
├── main.py
├── requirements.txt
├── common/
│   ├── constants.py
│   ├── sessions.py
│   ├── pdfs.py
│   ├── download.py
│   ├── process.py
│   ├── merge.py
│   └── runner.py
└── subjects/
    ├── chemistry/
    │   ├── igcse.py
    │   └── olevel.py
    ├── physics/
    │   ├── igcse.py
    │   └── olevel.py
    ├── mathematics/
    │   ├── igcse.py
    │   └── olevel.py
    └── additional_mathematics/
        ├── igcse.py
        └── olevel.py
```

## Notes

- For personal use only. Respect the source sites’ rate limits.
- Increase `MAX_WORKERS` only if you also increase `DELAY` in `common/constants.py`.

## License

Personal / educational use.

# Past Paper Fetcher

Personal tool to download and compile Cambridge IGCSE / O-Level past papers + mark schemes into yearly combined PDFs.

## Supported subjects

| Code | Subject                        |
| ---- | ------------------------------ |
| 0610 | IGCSE Biology                  |
| 5090 | O-Level Biology                |
| 0620 | IGCSE Chemistry                |
| 5070 | O-Level Chemistry              |
| 0625 | IGCSE Physics                  |
| 5054 | O-Level Physics                |
| 0580 | IGCSE Mathematics              |
| 4024 | O-Level Mathematics            |
| 0606 | IGCSE Additional Mathematics   |
| 4037 | O-Level Additional Mathematics |

## Features

- Downloads only QP + MS (or ER depending on WANT in constants)
- Skips already downloaded papers
- Multithreaded with polite delays
- Automatic fallbacks: bestexamhelp -> pastpapers.co -> xtremepapers -> DynamicPapers -> PapaCambridge
- Mode 2: single year from one chosen source only (no fallback chain)
- Year aware paper sets (no P4 pre-2016 for 0610/0620/0625; 5090 switches 6->4 in 2023)
- Merges into per paper Yearlies
- Interactive: choose subject code, mode, years / source, dry-run

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Enter subject code (e.g. `0610`)
2. Choose mode:
   - 1: full year range with all 5 fallbacks
   - 2: one specific year from one specific puller only
3. If mode 2: pick year + source (1 bestexamhelp / 2 pastpapers.co / 3 xtremepapers / 4 dynamic / 5 papacambridge)
4. Dry-run y/n

## Notes

- For personal use only. Respect the source sites rate limits.
- Increase MAX_WORKERS only if you also increase DELAY in common/constants.py.

## License

Personal / educational use.

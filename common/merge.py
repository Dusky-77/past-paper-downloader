from pathlib import Path

from pypdf import PdfReader, PdfWriter


def collect_and_merge(kind, paper, year_from, year_to, code, out_dir):
    pattern = f"{code}_*_{kind}_{paper}*.pdf"
    files = sorted(out_dir.rglob(pattern))
    if not files:
        print(f"no {kind} P{paper} files")
        return
    writer = PdfWriter()
    for f in files:
        try:
            reader = PdfReader(str(f))
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"skip {f.name}: {e}")
    out_name = f"{year_from}-{year_to} {code} P{paper} {kind.upper()} Yearlies.pdf"
    out_path = out_dir / out_name
    with open(out_path, "wb") as fp:
        writer.write(fp)
    print(f"wrote {out_name} ({len(writer.pages)} pages)")

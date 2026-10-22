from subjects.additional_mathematics import igcse as addmath_igcse
from subjects.additional_mathematics import olevel as addmath_olevel
from subjects.biology import igcse as bio_igcse
from subjects.biology import olevel as bio_olevel
from subjects.chemistry import igcse as chem_igcse
from subjects.chemistry import olevel as chem_olevel
from subjects.mathematics import igcse as math_igcse
from subjects.mathematics import olevel as math_olevel
from subjects.physics import igcse as phy_igcse
from subjects.physics import olevel as phy_olevel

SUBJECTS = {
    "0610": ("IGCSE Biology", bio_igcse),
    "5090": ("O-Level Biology", bio_olevel),
    "0620": ("IGCSE Chemistry", chem_igcse),
    "5070": ("O-Level Chemistry", chem_olevel),
    "0625": ("IGCSE Physics", phy_igcse),
    "5054": ("O-Level Physics", phy_olevel),
    "0580": ("IGCSE Mathematics", math_igcse),
    "4024": ("O-Level Mathematics", math_olevel),
    "0606": ("IGCSE Additional Mathematics", addmath_igcse),
    "4037": ("O-Level Additional Mathematics", addmath_olevel),
}

SOURCES = {
    "1": "primary",
    "2": "pastpapers.co",
    "3": "dynamic",
    "4": "xtremepapers",
}


def main():
    print("Available codes:")
    for code, (name, _) in SUBJECTS.items():
        print(f"  {code}  {name}")
    code = input("\nEnter subject code: ").strip()
    if code not in SUBJECTS:
        print("Unknown code")
        return
    name, module = SUBJECTS[code]
    print(f"Selected: {name}")
    print("\nModes:")
    print("  1  Full range (all fallbacks: primary -> pastpapers.co -> dynamic -> xtremepapers)")
    print("  2  Single year from one specific source only")
    mode = input("Mode (1/2): ").strip()
    if mode == "2":
        year = int(input("Year (e.g. 2024): ").strip())
        print("\nSources:")
        print("  1  primary (PapaCambridge)")
        print("  2  pastpapers.co")
        print("  3  dynamic (DynamicPapers)")
        print("  4  xtremepapers")
        src = input("Source (1-4): ").strip()
        if src not in SOURCES:
            print("Unknown source")
            return
        only = SOURCES[src]
        dry = input("Dry run? (y/n): ").strip().lower() in ("y", "yes")
        print(f"\nPulling {year} only from {only}")
        module.run(year, year, dry, only_source=only)
    else:
        year_from = int(input("Year from (e.g. 2014): ").strip())
        year_to = int(input("Year to   (e.g. 2026): ").strip())
        dry = input("Dry run? (y/n): ").strip().lower() in ("y", "yes")
        module.run(year_from, year_to, dry)


if __name__ == "__main__":
    main()

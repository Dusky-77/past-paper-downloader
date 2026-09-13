from subjects.additional_mathematics import igcse as addmath_igcse
from subjects.additional_mathematics import olevel as addmath_olevel
from subjects.chemistry import igcse as chem_igcse
from subjects.chemistry import olevel as chem_olevel
from subjects.mathematics import igcse as math_igcse
from subjects.mathematics import olevel as math_olevel
from subjects.physics import igcse as phy_igcse
from subjects.physics import olevel as phy_olevel

SUBJECTS = {
    "0620": ("IGCSE Chemistry", chem_igcse),
    "5070": ("O-Level Chemistry", chem_olevel),
    "0625": ("IGCSE Physics", phy_igcse),
    "5054": ("O-Level Physics", phy_olevel),
    "0580": ("IGCSE Mathematics", math_igcse),
    "4024": ("O-Level Mathematics", math_olevel),
    "0606": ("IGCSE Additional Mathematics", addmath_igcse),
    "4037": ("O-Level Additional Mathematics", addmath_olevel),
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
    year_from = int(input("Year from (e.g. 2014): ").strip())
    year_to = int(input("Year to   (e.g. 2026): ").strip())
    dry = input("Dry run? (y/n): ").strip().lower() in ("y", "yes")
    module.run(year_from, year_to, dry)


if __name__ == "__main__":
    main()

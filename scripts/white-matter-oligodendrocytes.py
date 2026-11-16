#!/usr/bin/env python3
"""Card: white-matter-oligodendrocytes (H01, somas.csv).

Share of cells labelled "White matter" whose celltype is OLIGO, and the
share of all oligodendrocytes that sit in the white matter.
Usage: python white-matter-oligodendrocytes.py [cache_dir]
"""
from _tables import h01_somas, pct

rows = h01_somas()
wm = [r for r in rows if r["layer"] == "White matter"]
oligo_wm = sum(r["celltype"] == "OLIGO" for r in wm)
oligo_all = sum(r["celltype"] == "OLIGO" for r in rows)
print("White-matter cells that are oligodendrocytes:", pct(oligo_wm, len(wm)))
print("Oligodendrocytes that sit in white matter:", pct(oligo_wm, oligo_all))

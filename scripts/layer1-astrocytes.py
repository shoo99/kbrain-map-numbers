#!/usr/bin/env python3
"""Card: layer1-astrocytes (H01, somas.csv).

Share of layer-1 cells that are astrocytes, and share of all astrocytes
in layer 1. (The card also cites the paper's Table S4 for astrocyte
volume by layer; that part is a paper value, not computed here.)
Usage: python layer1-astrocytes.py [cache_dir]
"""
from _tables import h01_somas, pct

rows = h01_somas()
l1 = [r for r in rows if r["layer"] == "Layer 1"]
a_l1 = sum(r["celltype"] == "ASTROCYTE" for r in l1)
a_all = sum(r["celltype"] == "ASTROCYTE" for r in rows)
print("Layer-1 cells that are astrocytes:", pct(a_l1, len(l1)))
print("Astrocytes that sit in layer 1:", pct(a_l1, a_all))

#!/usr/bin/env python3
"""Card: layer5-et-biggest-nuclei (MICrONS aibs_cell_info v1300, columns nuc_volume and cell_type).

Median nucleus volume (µm³) of neurons (broad_type excitatory or inhibitory) by cell_type,
largest first; also for hand-typed cells only (cell_type_source allen_v1_column_types_slanted_ref).
Cell types are mostly model predictions. Units: see card mouse-nucleus-size.
Usage: python layer5-et-biggest-nuclei.py [cache_dir]
"""
import statistics
from collections import defaultdict
from _tables import microns_cells

NON_NEURON = {"", "astrocyte", "oligo", "OPC", "microglia", "pericyte"}
by, hand = defaultdict(list), defaultdict(list)
for c in microns_cells():
    if c["broad_type"] not in ("excitatory", "inhibitory") or c["cell_type"] in NON_NEURON:
        continue
    v = float(c["nuc_volume"])
    by[c["cell_type"]].append(v)
    if c["cell_type_source"] == "allen_v1_column_types_slanted_ref":
        hand[c["cell_type"]].append(v)
print("cell_type  n  median  | hand-typed n  median")
for t, v in sorted(by.items(), key=lambda kv: -statistics.median(kv[1])):
    h = hand.get(t, [])
    print("%-6s %6d %7.1f  | %4d %7s" % (t, len(v), statistics.median(v), len(h), "%.1f" % statistics.median(h) if h else "-"))
et, l23 = statistics.median(by["5P-ET"]), statistics.median(by["23P"])
print("5P-ET / 23P = %.2f" % (et / l23))

#!/usr/bin/env python3
"""Card: mouse-basket-cells (MICrONS aibs_cell_info v1300).

Among cells with broad_type inhibitory: cell_type BC (basket cell), with
the source of each label (cell_type_source), and the separate mtype PTC.
Usage: python mouse-basket-cells.py [cache_dir]
"""
import collections
from _tables import microns_cells, pct

inh = [c for c in microns_cells() if c["broad_type"] == "inhibitory"]
bc = [c for c in inh if c["cell_type"] == "BC"]
print("cell_type BC among broad_type inhibitory:", pct(len(bc), len(inh)))
for src, n in collections.Counter(c["cell_type_source"] for c in bc).most_common():
    print("  label source %s: %d" % (src, n))
ptc = sum(c["mtype"] == "PTC" for c in inh)
print("mtype PTC among broad_type inhibitory:", pct(ptc, len(inh)))
exc_types = {"23P", "4P", "5P-IT", "5P-ET", "5P-NP", "6P-IT", "6P-CT"}
print("broad_type inhibitory but excitatory cell_type:", sum(c["cell_type"] in exc_types for c in inh))

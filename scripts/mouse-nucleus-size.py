#!/usr/bin/env python3
"""Card: mouse-nucleus-size (MICrONS aibs_cell_info v1300, column nuc_volume).

Median nucleus volume of neurons (broad_type excitatory or inhibitory) vs
microglia (broad_type nonneuron, cell_type microglia); also for hand-typed
cells only, and for pericytes. The table does not state units; the card
explains how µm³ was checked against the electron-microscope images.
Usage: python mouse-nucleus-size.py [cache_dir]
"""
import statistics
from _tables import microns_cells

cells = microns_cells()
vol = lambda cs: statistics.median(float(c["nuc_volume"]) for c in cs)
neur = [c for c in cells if c["broad_type"] in ("excitatory", "inhibitory")]
mg = [c for c in cells if c["broad_type"] == "nonneuron" and c["cell_type"] == "microglia"]
per = [c for c in cells if c["broad_type"] == "nonneuron" and c["cell_type"] == "pericyte"]
print("Neurons: %d, median %.1f" % (len(neur), vol(neur)))
print("Microglia: %d, median %.1f" % (len(mg), vol(mg)))
print("Ratio: %.2f" % (vol(neur) / vol(mg)))
hn = [c for c in neur if c["cell_type_source"] == "allen_v1_column_types_slanted_ref"]
hm = [c for c in mg if c["cell_type_source"] == "aibs_column_nonneuronal_ref"]
print("Hand-typed only: neurons %d median %.1f, microglia %d median %.1f, ratio %.2f"
      % (len(hn), vol(hn), len(hm), vol(hm), vol(hn) / vol(hm)))
print("Pericytes: %d, median %.1f" % (len(per), vol(per)))

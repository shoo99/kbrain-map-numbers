#!/usr/bin/env python3
"""Card: inhibitory-third (H01 somas.csv + MICrONS aibs_cell_info v1300).

Human: INTERNEURON among classified neurons (PYRAMIDAL, SPINY_ATYPICAL,
SPINY_STELLATE, INTERNEURON); also shown with UNCLASSIFIED_NEURON added.
Mouse: broad_type inhibitory among broad_type excitatory + inhibitory.
Usage: python inhibitory-third.py [cache_dir]
"""
from _tables import h01_somas, microns_cells, pct

rows = h01_somas()
classified = {"PYRAMIDAL", "SPINY_ATYPICAL", "SPINY_STELLATE", "INTERNEURON"}
inter = sum(r["celltype"] == "INTERNEURON" for r in rows)
n_cls = sum(r["celltype"] in classified for r in rows)
uncl = sum(r["celltype"] == "UNCLASSIFIED_NEURON" for r in rows)
print("Human H01 inhibitory share:", pct(inter, n_cls))
print("  with %d unclassified neurons added:" % uncl, pct(inter, n_cls + uncl))

cells = microns_cells()
inh = sum(c["broad_type"] == "inhibitory" for c in cells)
exc = sum(c["broad_type"] == "excitatory" for c in cells)
print("Mouse MICrONS inhibitory share:", pct(inh, inh + exc))

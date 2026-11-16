#!/usr/bin/env python3
"""Card: layer1-few-neurons (H01, somas.csv).

Neurons = PYRAMIDAL, SPINY_ATYPICAL, SPINY_STELLATE, INTERNEURON,
UNCLASSIFIED_NEURON. Layers as labelled in the table.
Usage: python layer1-few-neurons.py [cache_dir]
"""
from _tables import h01_somas, H01_NEURONS, pct

rows = h01_somas()
for layer in ("Layer 1", "Layer 2"):
    cells = [r for r in rows if r["layer"] == layer]
    n = sum(r["celltype"] in H01_NEURONS for r in cells)
    inter = sum(r["celltype"] == "INTERNEURON" for r in cells)
    pyr = sum(r["celltype"] == "PYRAMIDAL" for r in cells)
    print("%s: neurons %s (interneurons %d, pyramidal %d)" % (layer, pct(n, len(cells)), inter, pyr))

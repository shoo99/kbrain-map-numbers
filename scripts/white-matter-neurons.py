#!/usr/bin/env python3
"""Card: white-matter-neurons

Neurons in the white matter of the H01 human cortex sample, and how far
they sit from the cortex.

Usage:  python white-matter-neurons.py [cache_dir]

Python 3 standard library only. Downloads somas.csv (about 4 MB) on first
run and keeps it in cache_dir (default: ./cache).

H01 (Shapson-Coe et al. 2024, Science 384:eadk4858, CC BY 4.0)
  somas.csv, c3 release, columns x, y, z (voxels of 8 x 8 x 33 nm),
  celltype and layer. "White matter" is the dataset's own layer label.
  Neurons = PYRAMIDAL, SPINY_ATYPICAL, SPINY_STELLATE, INTERNEURON,
  UNCLASSIFIED_NEURON.
  Depth into the white matter is approximated by the distance from each
  white-matter cell to the nearest cell labelled "Layer 6".
"""
import collections
import math

from _tables import h01_somas

NEURONS = ["PYRAMIDAL", "UNCLASSIFIED_NEURON", "INTERNEURON", "SPINY_ATYPICAL",
           "SPINY_STELLATE"]
GLIA = {"OLIGO", "MG_OPC", "ASTROCYTE", "C_SHAPED"}
VOXEL_UM = (0.008, 0.008, 0.033)


def um(row):
    return tuple(int(row[k]) * s for k, s in zip("xyz", VOXEL_UM))


def summary(dist):
    d = sorted(dist)
    n = len(d)
    return ("median %.0f um, 10th-90th percentile %.0f-%.0f um, farthest %.0f um, "
            "within 100 um %.0f%%, beyond 300 um %.0f%%"
            % (d[n // 2] if n % 2 else (d[n // 2 - 1] + d[n // 2]) / 2,
               d[int(0.1 * (n - 1))], d[int(0.9 * (n - 1))], d[-1],
               100 * sum(x < 100 for x in d) / n, 100 * sum(x > 300 for x in d) / n))


def main():
    rows = h01_somas()
    wm = [r for r in rows if r["layer"] == "White matter"]
    types = collections.Counter(r["celltype"] for r in wm)
    neurons = [r for r in wm if r["celltype"] in NEURONS]
    print("White matter cells: %d" % len(wm))
    print("Neurons: %d (%.1f%%) = %s" % (
        len(neurons), 100 * len(neurons) / len(wm),
        ", ".join("%s %d" % (t, types[t]) for t in NEURONS)))

    layer6 = [um(r) for r in rows if r["layer"] == "Layer 6"]

    def nearest(p):
        return min(math.dist(p, q) for q in layer6)

    print("Distance to the nearest layer 6 cell (%d cells):" % len(layer6))
    print("  neurons: " + summary([nearest(um(r)) for r in neurons]))
    glia = [r for r in wm if r["celltype"] in GLIA]
    print("  glia (%d): " % len(glia) + summary([nearest(um(r)) for r in glia]))


if __name__ == "__main__":
    main()

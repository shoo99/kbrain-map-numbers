#!/usr/bin/env python3
"""Card: most-common-glia

Which glial cell is the most common one: astrocytes or oligodendrocytes?
Counted in human cortex grey matter (H01) and mouse visual cortex (MICrONS)
from the two public cell tables.

Usage:  python most-common-glia.py [cache_dir]

Python 3 standard library only. Downloads about 12 MB on first run and
keeps the files in cache_dir (default: ./cache).

Human (H01, Shapson-Coe et al. 2024, Science 384:eadk4858, CC BY 4.0)
  somas.csv, c3 release, column celltype. Glia = ASTROCYTE, OLIGO, MG_OPC
  (microglia and OPCs share one label), C_SHAPED. Counted for layers 1 to 6
  (grey matter) and, separately, for the white matter rows.

Mouse (MICrONS Consortium 2025, Nature 640:435)
  aibs_cell_info, materialization v1300. Column names come from
  aibs_cell_info_header.csv. Glia = broad_type "nonneuron" and cell_type
  astrocyte, oligo, microglia or OPC. Rows with an empty broad_type have
  no class and are counted separately.
"""
import collections

from _tables import H01_LAYERS, h01_somas, microns_cells

H01_GLIA = ["ASTROCYTE", "OLIGO", "MG_OPC", "C_SHAPED"]
MOUSE_GLIA = ["astrocyte", "oligo", "microglia", "OPC"]


def shares(counts, keys):
    total = sum(counts[k] for k in keys)
    parts = ", ".join("%s %d (%.0f%%)" % (k, counts[k], 100 * counts[k] / total)
                      for k in keys)
    return total, parts


def main():
    grey = collections.Counter()
    white = collections.Counter()
    for row in h01_somas():
        if row["layer"] in H01_LAYERS:
            grey[row["celltype"]] += 1
        elif row["layer"] == "White matter":
            white[row["celltype"]] += 1
    total, parts = shares(grey, H01_GLIA)
    print("Human H01, layers 1-6: glia %d = %s" % (total, parts))
    total, parts = shares(white, H01_GLIA)
    print("Human H01, white matter: glia %d = %s" % (total, parts))

    mouse = collections.Counter()
    broad = collections.Counter()
    for row in microns_cells():
        broad[row["broad_type"]] += 1
        if row["broad_type"] == "nonneuron":
            mouse[row["cell_type"]] += 1
    total, parts = shares(mouse, MOUSE_GLIA)
    print("Mouse MICrONS v1300: glia %d = %s" % (total, parts))
    print("Mouse rows with no broad_type: %d of %d"
          % (broad[""], sum(broad.values())))


if __name__ == "__main__":
    main()

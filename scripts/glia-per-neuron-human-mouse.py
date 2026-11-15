#!/usr/bin/env python3
"""Card: glia-per-neuron-human-mouse

Glia per neuron in human cortex grey matter (H01) and mouse visual cortex
(MICrONS), counted from the two public cell tables.

Usage:  python glia-per-neuron-human-mouse.py [cache_dir]

Python 3 standard library only. Downloads about 12 MB on first run and
keeps the files in cache_dir (default: ./cache).

Human (H01, Shapson-Coe et al. 2024, Science 384:eadk4858, CC BY 4.0)
  somas.csv, c3 release. Rows in "Layer 1" to "Layer 6" only (white matter,
  "unclassified" and NULL layers left out).
  glia    = ASTROCYTE, OLIGO, MG_OPC, C_SHAPED
  neurons = PYRAMIDAL, SPINY_ATYPICAL, SPINY_STELLATE, INTERNEURON,
            UNCLASSIFIED_NEURON
  (BLOOD_VESSEL_CELL and UNKNOWN are in neither group.)

Mouse (MICrONS Consortium 2025, Nature 640:435)
  aibs_cell_info, materialization v1300. The table has no header row; the
  column names come from aibs_cell_info_header.csv in the same folder and
  are checked below.
  neurons = broad_type "excitatory" or "inhibitory"
  glia    = broad_type "nonneuron" and cell_type astrocyte, oligo,
            microglia or OPC (pericytes and "error" rows left out)
  Rows with an empty broad_type have no class. The script also prints the
  ratio if every one of them were glia, as an upper bound.
"""
import collections
import csv
import gzip
import io
import os
import sys
import urllib.request

H01_SOMAS = "https://storage.googleapis.com/h01-release/data/20210601/c3/tables/somas.csv"
MICRONS = "https://storage.googleapis.com/mat_dbs/public/minnie65_phase3_v1/v1300/"
MICRONS_TABLE = MICRONS + "aibs_cell_info.csv.gz"
MICRONS_HEADER = MICRONS + "aibs_cell_info_header.csv"

H01_LAYERS = {"Layer %d" % i for i in range(1, 7)}
H01_GLIA = {"ASTROCYTE", "OLIGO", "MG_OPC", "C_SHAPED"}
H01_NEURONS = {"PYRAMIDAL", "SPINY_ATYPICAL", "SPINY_STELLATE", "INTERNEURON",
               "UNCLASSIFIED_NEURON"}
MOUSE_GLIA = {"astrocyte", "oligo", "microglia", "OPC"}


def fetch(url, cache):
    path = os.path.join(cache, url.rsplit("/", 1)[1])
    if not os.path.exists(path):
        print("downloading", url, file=sys.stderr)
        tmp = path + ".part"
        urllib.request.urlretrieve(url, tmp)
        os.replace(tmp, path)
    return path


def human(cache):
    glia = neurons = 0
    with open(fetch(H01_SOMAS, cache), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["layer"] not in H01_LAYERS:
                continue
            if row["celltype"] in H01_GLIA:
                glia += 1
            elif row["celltype"] in H01_NEURONS:
                neurons += 1
    return glia, neurons


def mouse(cache):
    with open(fetch(MICRONS_HEADER, cache), encoding="utf-8") as f:
        names = [line.split(",")[0] for line in f.read().splitlines() if line]
    for col in ("broad_type", "cell_type"):
        if col not in names:
            sys.exit("MICrONS header has no column %r: %s" % (col, names))
    bt, ct = names.index("broad_type"), names.index("cell_type")

    broad = collections.Counter()
    glia_types = collections.Counter()
    with gzip.open(fetch(MICRONS_TABLE, cache), "rb") as g:
        for row in csv.reader(io.TextIOWrapper(g, encoding="utf-8", newline="")):
            if len(row) != len(names):
                sys.exit("row has %d columns, header has %d" % (len(row), len(names)))
            broad[row[bt]] += 1
            if row[bt] == "nonneuron" and row[ct] in MOUSE_GLIA:
                glia_types[row[ct]] += 1
    neurons = broad["excitatory"] + broad["inhibitory"]
    return glia_types, neurons, broad


def main():
    cache = sys.argv[1] if len(sys.argv) > 1 else "cache"
    os.makedirs(cache, exist_ok=True)

    hg, hn = human(cache)
    print("Human H01, layers 1-6: glia %d / neurons %d = %.2f glia per neuron"
          % (hg, hn, hg / hn))

    types, mn, broad = mouse(cache)
    mg = sum(types.values())
    detail = ", ".join("%s %d" % (k, types[k]) for k in sorted(MOUSE_GLIA))
    print("Mouse MICrONS v1300: glia %d (%s) / neurons %d (excitatory %d + inhibitory %d)"
          " = %.2f glia per neuron"
          % (mg, detail, mn, broad["excitatory"], broad["inhibitory"], mg / mn))
    total = sum(broad.values())
    nocls = broad[""]
    print("Mouse rows with no broad_type: %d of %d (%.0f%%); if all were glia: %.2f"
          % (nocls, total, 100 * nocls / total, (mg + nocls) / mn))
    print("Human / mouse: %.1f times" % ((hg / hn) / (mg / mn)))


if __name__ == "__main__":
    main()

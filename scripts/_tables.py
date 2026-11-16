"""Shared helpers: download and read the two public cell tables.

H01 (human temporal cortex): somas.csv, c3 release.
  Shapson-Coe et al. 2024, Science 384:eadk4858, data CC BY 4.0.
MICrONS (mouse visual cortex): aibs_cell_info, materialization v1300.
  MICrONS Consortium 2025, Nature 640:435. The table has no header row;
  column names come from aibs_cell_info_header.csv in the same folder.

Python 3 standard library only. Files are kept in a cache folder
(first command-line argument, default ./cache).
"""
import csv
import gzip
import io
import os
import sys
import urllib.request

H01_SOMAS = "https://storage.googleapis.com/h01-release/data/20210601/c3/tables/somas.csv"
MICRONS = "https://storage.googleapis.com/mat_dbs/public/minnie65_phase3_v1/v1300/"

H01_NEURONS = {"PYRAMIDAL", "SPINY_ATYPICAL", "SPINY_STELLATE", "INTERNEURON",
               "UNCLASSIFIED_NEURON"}
H01_LAYERS = ["Layer %d" % i for i in range(1, 7)]


def cache_dir():
    d = sys.argv[1] if len(sys.argv) > 1 else "cache"
    os.makedirs(d, exist_ok=True)
    return d


def fetch(url):
    path = os.path.join(cache_dir(), url.rsplit("/", 1)[1])
    if not os.path.exists(path):
        print("downloading", url, file=sys.stderr)
        urllib.request.urlretrieve(url, path + ".part")
        os.replace(path + ".part", path)
    return path


def h01_somas():
    """List of dicts with keys soma_id, x, y, z, celltype, layer, ..."""
    with open(fetch(H01_SOMAS), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def microns_cells():
    """List of dicts keyed by the official column names (all values are strings)."""
    with open(fetch(MICRONS + "aibs_cell_info_header.csv"), encoding="utf-8") as f:
        names = [line.split(",")[0] for line in f.read().splitlines() if line]
    rows = []
    with gzip.open(fetch(MICRONS + "aibs_cell_info.csv.gz"), "rb") as g:
        for row in csv.reader(io.TextIOWrapper(g, encoding="utf-8", newline="")):
            if len(row) != len(names):
                sys.exit("row has %d columns, header has %d" % (len(row), len(names)))
            rows.append(dict(zip(names, row)))
    return rows


def pct(a, b):
    return "%d of %d = %.1f%%" % (a, b, 100 * a / b)

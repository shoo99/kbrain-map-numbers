#!/usr/bin/env python3
"""Card: fly-histamine-neurons (Janelia FlyEM Male CNS v1.0, CC BY).

Bodies tagged consensusNt:histamine in the public segment-properties file
gs://flyem-male-cns/v1.0/segmentation/tags_property/info, split by their
superclass tag. Outside the optic lobes (superclass not ol_*), counts the
bodies that carry a cell-type name (type_property) and those that do not.
Transmitters are predicted from the EM images, not measured chemically.
Usage: python fly-histamine-neurons.py [cache_dir]
"""
import collections
import json
import os
import sys
import urllib.request
from _tables import cache_dir

BASE = "https://storage.googleapis.com/flyem-male-cns/v1.0/segmentation/"


def load(name):
    """Download <name>/info once (cached as mcns_<name>.json) and return its inline block."""
    path = os.path.join(cache_dir(), "mcns_" + name + ".json")
    if not os.path.exists(path):
        print("downloading", BASE + name + "/info", file=sys.stderr)
        urllib.request.urlretrieve(BASE + name + "/info", path + ".part")
        os.replace(path + ".part", path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)["inline"]


tags = load("tags_property")
P = tags["properties"][0]
names = P["tags"]
hist = names.index("consensusNt:histamine")
by_super = collections.Counter()
central = []
for body, v in zip(tags["ids"], P["values"]):
    if hist not in v:
        continue
    sup = next((names[z] for z in v if names[z].startswith("superclass:")), "superclass:?")
    by_super[sup] += 1
    if not sup.startswith("superclass:ol_"):
        central.append(body)

types = load("type_property")
tmap = dict(zip(types["ids"], types["properties"][0]["values"]))
named = [b for b in central if tmap.get(b, "") not in ("", "~")]

print("Histamine-predicted bodies:", sum(by_super.values()))
for s, n in by_super.most_common():
    print("  %s: %d" % (s, n))
print("Outside the optic lobes:", len(central))
print("  with a cell-type name:", len(named), sorted(tmap[b] for b in named))
print("  without a type name:", len(central) - len(named))

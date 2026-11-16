# Scripts

One script per card, named after the card `id`. Each script downloads or reads the public files it needs and prints the card's value, so anyone can check it.

Being added (v0.1). Until a card has its script here, its `method` field in `data/numbers.json` describes how the value was obtained.

Requirements: Python 3, standard library only. Run from any folder; downloads are kept in `./cache` (or the folder given as the first argument).

| Card | Script | Prints |
|---|---|---|
| glia-per-neuron-human-mouse | `glia-per-neuron-human-mouse.py` | 1.28 (H01) and 0.25 (MICrONS) glia per neuron |
| white-matter-oligodendrocytes | `white-matter-oligodendrocytes.py` | 77.4% of white-matter cells; 50.2% of oligodendrocytes |
| layer1-few-neurons | `layer1-few-neurons.py` | 18.0% (layer 1) vs 70.0% (layer 2) neurons |
| layer1-astrocytes | `layer1-astrocytes.py` | 36.7% of layer-1 cells; 30.8% of astrocytes |
| inhibitory-third | `inhibitory-third.py` | 30.8% (29.1% with unclassified) human vs 12.0% mouse |
| mouse-basket-cells | `mouse-basket-cells.py` | 37.4% BC (label sources listed); 33.9% PTC |
| mouse-nucleus-size | `mouse-nucleus-size.py` | 278 vs 73 µm³ median, 3.8× (3.9× hand-typed only) |

`_tables.py` holds the shared download and table-reading code for the scripts above.

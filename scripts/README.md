# Scripts

One script per card, named after the card `id`. Each script downloads or reads the public files it needs and prints the card's value, so anyone can check it.

Being added (v0.1). Until a card has its script here, its `method` field in `data/numbers.json` describes how the value was obtained.

Requirements: Python 3, standard library only. Run from any folder; downloads are kept in `./cache` (or the folder given as the first argument).

| Card | Script | Prints |
|---|---|---|
| glia-per-neuron-human-mouse | `glia-per-neuron-human-mouse.py` | 1.28 (H01) and 0.25 (MICrONS) glia per neuron |

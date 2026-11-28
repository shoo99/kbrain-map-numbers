# KBrain Map numbers

A living, versioned catalogue of numbers measured from public connectomes: human cortex (H01), mouse visual cortex (MICrONS) and the fruit fly (Janelia Male CNS). Each number comes with how it was measured, what it does not show, its source, and any corrections.

The same numbers are shown at **https://kbrain-map.org/numbers**, and many are explained in short videos on the YouTube channel *Inside the Connectome*.

> Status: work in progress (v0.1, November 2026). Re-runnable scripts for every card are being added. A paper describing this resource is in preparation.

## What is here

| Path | Content |
|---|---|
| `data/numbers.json` | All cards, one object per number (snapshot of the live list) |
| `scripts/` | Scripts that recompute card values from the public data (being added) |
| `CITATION.cff` | How to cite this repository |

## Card fields

| Field | Meaning |
|---|---|
| `id` | Stable anchor (`kbrain-map.org/numbers#<id>`), never reused |
| `value` | The number as shown, rounded |
| `claim` | One sentence: what the number counts, and in which sample |
| `map` | Source dataset: `h01`, `microns`, `male-cns` |
| `method` | How the value was obtained: table and row, or file and column, or our computation. Divisions and sums we did ourselves are marked "ours" |
| `caveat` | What the number does **not** show: sample size, definitions, denominators, known inconsistencies in the source |
| `source` | `paper` = read from the dataset's publication; `ours` = computed by us from released data |
| `post`, `video` | Linked write-up and short video, if any |
| `date` | Date the card was added or last changed |

## Rules we follow

- Every value is checked against the original paper, supplement or released file, not against summaries.
- Definitions and denominators are taken from the source's notes and methods, not from table headers alone.
- When a public file and the paper disagree, or a table is internally inconsistent, the card says so.
- Mistakes are corrected on the card, in the linked video description, and with a note under the video. Example: a card first said myelinated wires fill "31% of white matter"; the source table measures only the inside of each myelinated axon, as a share of the tissue the authors could classify. The card and video were corrected on 2 November 2026.
- Cards and scripts are drafted with an AI assistant (Claude, Anthropic) and reviewed by the author.

## Data sources

The values are derived from these public datasets and their publications. Please cite them as well when you use a number.

- **H01** (human temporal cortex): Shapson-Coe A. et al. (2024) *Science* 384:eadk4858, doi:10.1126/science.adk4858. Data: `gs://h01-release` (CC BY 4.0).
- **MICrONS** (mouse visual cortex): MICrONS Consortium (2025) *Nature* 640:435-447, doi:10.1038/s41586-025-08790-w. Data: MICrONS public release, https://www.microns-explorer.org (CC BY 4.0 per its terms and conditions; attribution per its citation policy).
- **Male CNS** (fruit fly): Janelia FlyEM Male CNS connectome public release, https://male-cns.janelia.org/ (CC-BY, as stated on the release page).

## License

- Data (`data/`): Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/
- Code (`scripts/`): MIT License (see `LICENSE`)

## Author

Byeongsoo Kang (ORCID 0009-0007-2324-2351)

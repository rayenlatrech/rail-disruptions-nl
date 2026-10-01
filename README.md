# How long will a Dutch train disruption last?

Predicting, at the moment a disruption on the Dutch rail network is announced,
whether it will turn into a long one. Built on seven years (2019–2025) of
disruption records from [Rijden de Treinen](https://www.rijdendetreinen.nl/en/open-data/disruptions).

> **Status:** work in progress. Setup is done; analysis is starting.

## The question

When NS announces a disruption, travellers and operations staff have to decide
fast: wait it out, reroute, or arrange replacement buses. The announcement says
*what* happened and *where*, but not *how long* it will take.

This project asks: **using only what is known when a disruption starts (its
cause, the lines and stations affected, and the time it began), can we predict
whether it will last longer than a set threshold?**

The threshold (likely around two hours) will be chosen during EDA, from the
duration distribution.

## Data

**Source:** Rijden de Treinen, *Disruptions* open data. There is one CSV per
year, and the data is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

| Column | Meaning |
|---|---|
| `rdt_id` | Unique disruption ID |
| `rdt_lines`, `rdt_lines_id` | Affected lines, standardised by Rijden de Treinen |
| `ns_lines` | Affected lines as written in the NS message (unstructured) |
| `rdt_station_names`, `rdt_station_codes` | Affected stations |
| `cause_en` / `cause_nl` | Final cause of the disruption |
| `statistical_cause_en` / `statistical_cause_nl` | Cause kept for statistics |
| `cause_group` | Broad cause category |
| `start_time`, `end_time` | When the disruption started and ended |
| `duration_minutes` | Duration of the disruption (the target is built from this) |

Known caveats, from the source:

- Only disruptions that NS announced are included. Many smaller delays never
  appear.
- From 2017, NS started communicating more (often short) disruptions. Starting
  at 2019 keeps every year on the same footing.

The data is not stored in this repository. To download it, run
`python src/download.py`.

## Approach (planned)

- **Time-based split:** train on 2019–2023, validate on 2024, and test on 2025.
  The test year is used once, at the end.
- **Baselines:** the majority class, and the historical long-disruption rate
  per cause group.
- **Models:** logistic regression and LightGBM.
- **Evaluation:** the metric is chosen once the class balance is known (likely
  PR-AUC), with a calibration check.

## Repository structure

```
rail-disruptions-nl/
├── data/                  # not committed; created by src/download.py
│   ├── raw/               # yearly CSVs as downloaded
│   └── processed/         # cleaned data used by the notebooks
├── notebooks/
│   ├── 01_load_clean.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_features.ipynb
│   └── 04_models.ipynb
├── reports/figures/
├── src/
│   └── download.py
├── requirements.txt
└── README.md
```

## Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/download.py
```

## Results

To be added.

## Credits

Disruption data © [Rijden de Treinen](https://www.rijdendetreinen.nl/), CC BY 4.0.

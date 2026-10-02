# Data quality log

Every data problem found in the Rijden de Treinen disruption files (2019–2025), with the decision taken and
why. Details and code are in `notebooks/01_load_clean.ipynb`.

**Raw data:** 38,571 rows, 14 columns, `rdt_id` unique across all files.
**Clean data:** 37,777 rows, saved to `data/processed/disruptions_clean.parquet`.
**Unit of analysis:** one row = one disruption message published by NS.

## Summary

| # | Issue | Rows | Decision |
|---|---|---|---|
| 1 | No `end_time`, so no duration | 110 | Drop (no target) |
| 2 | `end_time` present but `duration_minutes` empty (a 59-day "broken down train") | 1 | Drop (never-closed message) |
| 3 | `duration_minutes == 0` | 683 | Drop (not a real disruption) |
| 4 | `end − start` differs from `duration_minutes` by 60 min | 7 | Keep, use `duration_minutes` |
| 5 | `end − start` differs by exactly 0.5 min after rounding | 289 | Keep (rounding convention only) |
| 6 | Very long durations (> 1 day: 379, > 7 days: 42) | 379 | Keep (real long-running events) |
| 7 | Disruption ends in a later calendar year | 4 | Keep, year = start year |
| 8 | `cause_group` missing | 2 | Fill with `"external"` |
| 9 | `cause_en` ≠ `statistical_cause_en` | 190 | Use `cause_en`; never use `statistical_cause_*` |
| 10 | Missing `rdt_lines` / station names | 12 / 8 | Keep, fill in notebook 03 |
| 11 | Several messages with the same start second | 96 | Keep (one incident, different routes) |
| 12 | Back-to-back messages on the same line, same cause (gap 0–5 min) | 229 | Keep, noted as a limitation |
| 13 | Overlapping messages on the same line | 989 | Keep (real simultaneous disruptions) |

## Details

**1–2. Missing target.** 58 of the 110 rows without an end time are from 2020, which suggests a logging problem
that year. A row without a duration has no target and the target is never imputed. The one row with an end time
but no duration ran from 23 Jul to 21 Sep 2020; RDT left the duration empty, most likely because the message was
never closed properly. Filling it in would have created the longest disruption in the dataset.

**3. Zero durations.** 455 messages have identical start and end seconds, 228 more lasted under 30 seconds. They
are concentrated in 2019 (373) and 2020 (120), almost absent in 2021 (2), then 30–68 per year. This is a change in
recording, not in railway behaviour. Keeping them would label non-events as "short disruptions" and make the
training years differ from the test years. The cut-off is 0 minutes; 1–2 minute messages are kept.

**4. Daylight saving time.** Timestamps are local clock time without a timezone. For disruptions running through
the March change, `end − start` is 60 min too long; through the October change, 60 min too short.
`duration_minutes` handles this correctly and is the target.

**5. Rounding.** `duration_minutes` is rounded to the nearest minute (99.2% match vs. 51.2% when truncating). The
289 remaining mismatches are all exactly x.5 minutes: RDT rounds half up, pandas rounds half to even.

**6. Long durations.** The longest records are long-running service changes: the Arriva strike in the north
(Feb 2023, ~28 days), a damaged bridge on Roermond–Sittard (~31 days), multi-week engineering work and rolling-stock
shortages on cross-border lines. They are plausible and kept. Median 47 min, 90th percentile 272 min.

**7. Year boundaries.** Three rows run from Dec 2021 to Jan 2022 (both training years) and one from Dec 2024
(validation) to Jan 2025 (test). The year of a disruption is its start year, because that is when the prediction
is made.

**8. Missing cause group.** Both rows are `deployment of security staff` (2024), a cause without a group.

**9. Two cause columns.** In all 190 differing rows `cause_en` is vague ("an earlier disruption", "multiple
disruptions", "cause yet unknown") and `statistical_cause_en` gives the specific underlying cause, partly known only
afterwards. Using it would leak information. Limitation: `cause_en` is itself the final cause; changes made while a
disruption was running are not visible.

**10. "unknown" cause group** (733 rows, mostly `technical investigation`). Kept as its own category: "cause not yet
known" is information available at prediction time.

**11–13. Related messages.** One incident can generate several messages: different routes announced in the same
second, a message replaced by a new one seconds after closing, or two messages active at once on the same line.
The analysis keeps one row per message. Merging messages into incidents would touch under 1% of rows; it is a v2
idea.

## Things that are fine

- No empty strings hidden behind non-missing values.
- No negative durations.
- File year always equals the start year.
- Dutch and English cause names map almost one-to-one; 3 English causes merge two or three Dutch wordings, so
  `cause_en` is the cleaner column.

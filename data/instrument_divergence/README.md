# Instrument divergence cross-section, 12 October 2026

Two commercial search-analytics instruments read for twelve URL prefixes on one
domain, on one day, through each vendor's own web interface under a paid
subscription. No API was used.

- `ahrefs_prefixes_2026-10-12.csv`: Ahrefs Site Explorer, prefix mode, all
  locations. Columns are the overview-card values as displayed. The
  `first_traffic_month` column is the first month with non-zero organic traffic
  in the all-time performance chart, read visually to the nearest month or
  quarter, and is the age proxy used in the paper. The instrument's history
  begins in September 2015, so three ages are left-censored at that horizon.
  `ahrefs_us_share` is the United States share of the prefix's estimated
  visits from the overview's traffic-by-location table, read 12 October 2026,
  used to territory-match the two instruments.
- `semrush_prefixes_2026-10-12.csv`: Semrush Domain Overview, subfolder mode,
  US database. Columns are the summary-card values as displayed.

Semrush's AI-visibility panel (mentions, cited pages) returned identical values
for every subfolder queried and is therefore domain-scoped; those columns are
omitted from the Semrush file for that reason and the observation is recorded
in the paper.

`analyze.py` recomputes every number quoted in Section 5.5 from these files.

Known limits: ages are chart reads; one domain; one date.

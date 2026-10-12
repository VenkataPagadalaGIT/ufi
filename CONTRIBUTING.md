# Contributing

Thank you for looking. Three kinds of contribution are especially useful.

**A demand-surface adapter.** Subclass `ufi.demand.DemandAdapter`, set
`surface` to one of the thirteen ids in `docs/DEMAND_SURFACES.md` (or propose
a new one), yield `DemandRecord`s from `read(path)`, and add a test with a
small fixture file. Do not add collection code (API clients, scrapers); the
adapter normalizes an export the deployment already holds.

**An ontology for another industry.** Copy `examples/nanp/ontology.yaml`,
keep every competency question executable (`ufi validate` must pass), and
include at least one `unsupported` question with its reason if the domain
attracts questions the sources cannot answer.

**A replication of the instrument-divergence cross-section** on another
domain. Follow the read method in `data/instrument_divergence/README.md`, add
two CSV files with the same columns, and `analyze.py` will print the
statistics.

## Ground rules

- `python -m pytest -q` passes before and after your change.
- A number that reaches a README, a docstring or the paper comes from a
  script, not a keyboard.
- Synthetic data is flagged `synthetic=True` and never described as observed.
- No em dashes in prose; US spelling.
- Open an issue before a large change so the design can be discussed first.

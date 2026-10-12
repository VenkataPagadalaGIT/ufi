# Changelog

## 0.2.0 (12 October 2026)

- Executable competency questions: property-chain validation, SPARQL
  generation with subclass closure, schema pass rate and instance coverage
  reported separately, `unsupported` questions reported as declared gaps.
- `ufi cq` subcommand.
- Default namespace changed from an unregistered `w3id.org` path to
  `urn:ufi:<name>`; `base=` accepted on OWL and SHACL export.
- Instrument-divergence data release: two CSV files and `analyze.py`.
- Frozen query set, parameter lock and run manifest committed under
  `examples/nanp/out/`.
- Deterministic ordering of tied scores.
- Documentation restructured: README front door plus `docs/` pages.

## 0.1.0

- Content Gap Score at entity, relation and class level; practitioner
  baselines; judgment cache; freezing, locking and manifests; OWL 2 and SHACL
  export; HermiT reasoning and materialization; NANP worked example.

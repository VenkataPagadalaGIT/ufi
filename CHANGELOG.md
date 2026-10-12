# Changelog

## Unreleased

- `TokenLinker`: word-n-gram exact-match linker with the same rule as `AliasLinker`, orders of magnitude faster on large alias sets; equivalence on punctuation-free text pinned by test.
- `scipy` declared as a dependency: networkx PageRank requires it at runtime, and a clean install failed without it.
- CI across Python 3.10 to 3.13 (tests, lint, types, deterministic example, released-digest verification, paper statistics).
- Lint-clean under ruff, type-clean under mypy, formatted; explicit public API in `ufi.__init__`.
- Fixed a variable reuse in the OWL exporter's defined-class block and a shadowed loop variable in validation.
- `score_entities` / `schema_gap_by_relation` take `params=None` instead of a mutable default.
- Pre-commit config, Makefile, issue and PR templates, security policy, code of conduct.

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

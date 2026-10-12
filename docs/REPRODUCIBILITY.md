# Reproducibility

The package emits four artifacts so that any number computed with it can be
traced and recomputed.

## The frozen query set

`freeze_queries()` (or `ufi freeze`) writes the evaluation query set with a
hash and refuses to overwrite. A query universe defined after the outcome is
known is the most common way an applied content study selects on its result;
freezing it first, and publishing the digest, is what makes a later share a
test rather than a fit. A run with no frozen set records
`none:query-set-not-frozen` rather than an empty field, because "not frozen"
and "not checked" are different claims.

## The parameter lock

`ufi lock` pins α, β and damping with a digest and a timestamp. The lock
behind the paper (`7290a2235d8de05f`) fixes the defaults, α = 0.5, β = 0.5,
damping = 0.85, and was written before any scoring data existed.

## The judgment cache

Each cached judgment carries the subject, the question, the rubric identifier
and a digest of the evidence, not just a grade. That is what lets a second
annotator re-grade the same items, and what lets a published number be traced
to the rows that produced it. Changing the rubric text misses the cache, so
grades from two rubrics never silently mix. `judge.agreement()` and
`judge.weighted_kappa()` compare two caches; `judge.bootstrap_ci()` gives the
interval.

## The run manifest

Every run writes `manifest.json`. Its digest covers the ontology, the graph,
the judgment cache, the parameters and the frozen query set, and deliberately
excludes timestamps and the grader's model string: a judgment made on a
different day produces the same score, and a digest that moved with it would
report a difference that does not exist. Two runs with the same digest produce
the same numbers; `score.py` orders tied entities by id so the output is
byte-stable.

## Released artifacts

| Artifact | Path | Digest |
|---|---|---|
| frozen query set, 924 queries over 66 codes | `examples/nanp/out/frozen_queries.json` | `f05ce279942be5f8` |
| parameter lock | `examples/nanp/out/parameters.lock.json` | `7290a2235d8de05f` |
| run manifest | `examples/nanp/out/manifest.json` | |

These are the digests quoted in the paper, and they are committed so that a
reader can verify them without regenerating anything:

```bash
ufi verify examples/nanp/out/frozen_queries.json
ufi manifest examples/nanp/out/manifest.json
```

## The instrument-divergence data

`data/instrument_divergence/` holds the two CSV files behind the paper's
twelve-prefix cross-section (one per instrument, read 12 October 2026) and
`analyze.py`, which prints every statistic quoted in that section. Nothing in
the section was typed by hand.

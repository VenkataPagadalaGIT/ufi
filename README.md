# ufi — content gap scoring from industry structure and user questions

A reference implementation of the Content Gap Score: a way of ranking what an
organization should publish from the structure of an industry's knowledge and
from questions users actually asked, rather than from a keyword tool's volume
estimate.

**The score is a specification, not a validated instrument.** No published
study has yet tested whether it predicts anything. This package exists so that
such a study is possible: it computes the score, computes the baselines it has
to beat, and emits the artifacts that make a result checkable.

[![tests](https://img.shields.io/badge/tests-61%20passing-brightgreen)](tests/)
[![licence](https://img.shields.io/badge/licence-Apache--2.0-blue)](LICENSE)

## Install

```bash
pip install -e ".[dev]"        # includes the RDF extras
ufi --version
```

Python 3.10+. Core needs `networkx` and `pyyaml`. The RDF path (OWL export,
SHACL validation, reasoning) needs `rdflib`, `pyshacl` and `owlready2`, and a
JVM for HermiT; install with `pip install "ufi[rdf]"`.

## The score

```
prior(e) = β·rel(e) + (1 − β)·dem(e)
CGS(e)   = prior(e) · (1 − own(e)) · [ α·(1 − cov_K(e)) + (1−α)·mean_q(1 − ans(q,e)) ]
```

| Term | Meaning | Source class |
|---|---|---|
| `rel(e)` | topic-sensitive PageRank over the structure graph, rank-normalized | structure |
| `dem(e)` | rank-normalized count of user questions linked to `e` | demand |
| `own(e)` | the organization's own coverage, graded {0, ½, 1} | coverage |
| `cov_K(e)` | mean of the same grade over the competitor set `K` | coverage |
| `ans(q,e)` | whether the web answers competency question `q` about `e` | answerability |

`α` moves weight between the two deficits, `β` between structure and demand.
The first bracket term is the **instance gap** (nobody covers this entity), the
second the **schema gap** (nobody answers this question about it). Both are
reported separately, because a score that mixes them says an entity is a gap
without saying what kind, and the two call for different content.

Reported search volume is not an input.

## Worked example

```bash
cd examples/nanp
python make_demo_inputs.py
python build_example.py
```

Runs offline in a couple of seconds over 66 US geographic area codes:

```
reasoner: HermiT (owlready2), consistent=True, 66 individuals reclassified by entailment
SHACL: 70 focus nodes, 0 violations, vacuous=False
demand: 177 records, 177 links, first-party share 0.00, synthetic share 1.00
```

**What is real and what is not.** The ontology and the area-code facts are
real. The demand records, the reported volumes and the retrieved-result
evidence are synthetic, generated with a fixed seed so the example is
deterministic and needs no network and no model. Every synthetic record is
flagged as such and the flag propagates: the run reports a first-party demand
share of 0.00 and a synthetic share of 1.00, and `ufi manifest` says in plain
words that nothing computed from it is an observation about users. That is the
example working correctly, not failing.

## Five things the package makes hard to get wrong

**Structure and coverage stay separate.** `structure_subgraph()` returns only
triples whose provenance is a structure source. If coverage evidence reached
the relatedness graph, an entity competitors cover well would gain edges,
centrality and prior, and the score would rank covered entities above
uncovered ones — the opposite of its purpose.

**A demand term with nothing behind it is visible.** `coverage_report()` lists
every designed surface including the ones that produced nothing.
`first_party_share()` reports how much evidence is in a user's own words rather
than reconstructed by a keyword tool, and excludes synthetic records from the
numerator. A run at 0.0 does not support a claim about users, and the CLI says
so rather than leaving it to the reader.

**A query universe defined after the outcome is marked as such.**
`freeze_queries()` writes the evaluation set with a hash and refuses to
overwrite. A run with no frozen set records `none:query-set-not-frozen` rather
than an empty field, because "not frozen" and "not checked" are different
claims.

**Judgments are cached with their context.** Each cached row carries the
subject, the question, the rubric identifier and a digest of the evidence, not
just a grade. A cache of anonymous grades cannot be re-graded by a second
annotator or traced back to a published number, which are the two things a
released cache is for. Changing the rubric text misses the cache, so grades
from two rubrics can never silently mix.

**An empty validation is not a clean one.** `rdf.validate()` reports the number
of focus nodes and refuses to call a run conformant when it had nothing to
check. `rdf.reason()` reports how many class assertions were actually inferred,
so "a reasoner ran" can be told apart from "a reasoner had something to do".

## Making the ontology load-bearing

The example asserts only what the registry states: that something is an area
code, and a place it serves. Whether it is a *geographic* area code is an
entailment, derived by `rdf.materialize()`:

```python
from ufi.rdf import materialize
materialize(onto, kg)       # 66 individuals reclassified
```

This is deliberate. An ontology whose deletion would change no downstream
number is decorative, and the way to tell is to put the classification in the
reasoner instead of the loader.

## Reproducibility

```bash
ufi manifest examples/nanp/out/manifest.json
```

Two runs with the same digest produce the same numbers. The digest covers the
ontology, the graph, the judgment cache, the parameters and the frozen query
set, and deliberately excludes timestamps and the grader's model string: a
judgment made on a different day produces the same score, and a digest that
moved with it would report a difference that does not exist.

## Known limitations

Stated here rather than discovered by a reader.

- **`rel` is strongly correlated with node degree** on sparse graphs. On the
  worked example's structure graph, which is a two-hop star through time-zone
  and overlay hubs, the correlation is about 0.8. On such a graph `rel` largely
  measures how many facts a code has, not how central it is. Check the
  correlation on your own graph before trusting the prior.
- **The three-level rubric is coarse.** Half credit covers a wide range.
- **`ans` takes the best of several verbalizations**, so a question set whose
  verbalizations differ in difficulty rewards answering the easiest one.
- **No entity linker beyond longest-match alias search.** Adequate for
  identifiers, not for ambiguous names.
- **The NANP ontology is a nine-class sketch**, sufficient for the example and
  not yet a resource-grade vocabulary. It has no Wikidata reconciliation, no
  published namespace document and no DOI.

## What an adversarial review found, and what changed

This package was reviewed by a simulated Tier-1 panel that executed it. The
findings were real and the fixes are in this repository: the OWL export dropped
every property alignment and emitted a bare name where an IRI was required, so
the file did not parse; data properties were inexpressible, so the class whose
identity criterion is a code pair could not record the pair; the judgment cache
stored anonymous grades; `kendall_tau` was documented as tau-b and computed
tau-a over heavily tied input; the volume and question-mining baselines were
fed the same numbers; two referenced files did not exist; and the demo reported
a healthy first-party demand share on wholly synthetic data.

Building the package also found a defect in its own reasoning: the manifest
digest moved between two identical runs, because the cache fingerprint included
each judgment's timestamp.

## Tests

```bash
python -m pytest -q        # 61 passed
```

## Licence and citation

Apache 2.0 for the code. The ontology and the bundled area-code dataset are
CC BY 4.0. See `CITATION.cff`.

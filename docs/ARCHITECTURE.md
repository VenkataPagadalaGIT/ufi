# Architecture

How the package is shaped, and why. The framework figure in the README is the
map; this page is the legend.

## The pipeline

```
demand surfaces ─┐
                 ├─► classify & link ─► knowledge graph ─► competency questions ─► Content Gap Score ─► ranked gaps
ontology ────────┘        (demand.py)        (graph.py)          (cq.py)              (score.py)         (pipeline.py)
                                                 │
                                   reasoning + SHACL (rdf.py)        baselines on the same list (baselines.py)
                                                                      freeze / lock / manifest (provenance.py)
```

`pipeline.GapRun` wires the stages: it takes an ontology, a graph, a demand
index and three evidence suppliers (own coverage, competitor coverage,
answerability), runs the graders through the judgment cache, computes the
score and the baselines, and writes the manifest.

## Modules

| Module | Responsibility |
|---|---|
| `types.py` | Core value types. `SourceClass` (structure / coverage / demand) lives on `Provenance`, so the separation survives refactoring. |
| `ontology.py` | The YAML specification: classes, relations, competency questions; validation; OWL 2 and SHACL export; the default `urn:ufi:` namespace. |
| `cq.py` | Executable competency questions: property-chain validation (domain and range threaded through the chain, answer class checked at the terminus), SPARQL generation with subclass closure, and the two rates. |
| `graph.py` | The knowledge graph. `structure_subgraph()` returns only structure-sourced triples; coverage evidence can never reach the relatedness graph. |
| `demand.py` | Thirteen demand-surface adapters, the alias linker, the demand index, the coverage report and the first-party share. |
| `judge.py` | `Judge` interface, `RuleJudge`, `CallableJudge`, the context-keyed `JudgmentCache`, and the agreement statistics (weighted kappa, bootstrap intervals). |
| `score.py` | The Content Gap Score at entity, relation and class level, with instance and schema gaps reported separately. |
| `baselines.py` | The practitioner baselines (volume, competitor gap, question mining, latent internal) computed on the same candidate list, and rank comparison. |
| `rdf.py` | RDF serialization, HermiT reasoning via owlready2, SHACL validation with vacuous-run detection, materialization of inferred types. |
| `provenance.py` | Query freezing, parameter locking, the run manifest and its digest. |
| `pipeline.py` | `GapRun`, the end-to-end run. |
| `cli.py` | The seven commands. |

## Design decisions

**Rank normalization rather than min-max.** Topic-sensitive PageRank mass is
heavy-tailed; under min-max almost every entity lands near zero and the
product collapses to a centrality ranking of a few nodes. Rank normalization
keeps the prior informative across the whole list, at the cost of discarding
the magnitude of a centrality difference, which is the right trade when the
score ranks rather than measures.

**An arithmetic prior.** `prior = β·rel + (1 − β)·dem`, not a geometric mean.
An entity with no observed questions should be discounted, not eliminated,
because the demand layer is incomplete in most deployments. `β = 1`
(structure only) and `β = 0` (demand only) are both meaningful ablations and
both should be run.

**Separate source classes, enforced in the type system.** If competitor
crawls fed the relatedness graph, entities competitors cover would acquire
edges and the score would rank well-covered entities highest. A gap finder
that prefers covered entities fails silently and looks plausible.

**The judge is an interface, not a model client.** The package ships no model
client. A deployment supplies a callable; the cache makes the call happen
once. The rubric is the thing that should be published and reviewed, not the
vendor; a released cache lets a reader recompute without a key; and a second
annotator is a cheap second pass over the same keys.

**Classification lives in the reasoner.** The example asserts only that
something is an area code and a place it serves; whether it is a *geographic*
area code is an entailment that `materialize()` writes back. An ontology
whose deletion would change no downstream number is decorative.

**Validation reports what it checked.** A SHACL run over a graph with no
individuals conforms. `validate()` reports the focus-node count and sets
`vacuous` so that an empty success reads as empty.

**Competency questions are executed, not listed.** A question is a property
chain the validator threads through the ontology's domains and ranges and
compiles to SPARQL with subclass closure. Two defects in the example's own
ontology were found this way: one question did not compose, and one composed
and answered the wrong question.

## What is deliberately not here

No crawler, no SERP client, no model client, no scheduler. Each is a
deployment concern with its own credentials, rate limits and terms, and
bundling them would make the package hard to audit and easy to misuse. The
seams are `DemandAdapter`, the three evidence suppliers on `GapRun`, and
`Judge`.

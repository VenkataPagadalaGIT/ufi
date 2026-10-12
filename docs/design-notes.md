# Design notes

Why the package is shaped the way it is. These are the decisions that would
otherwise be rediscovered by whoever changes the code next.

## Rank normalization rather than min-max

Topic-sensitive PageRank mass is heavy-tailed. Under min-max normalization
almost every entity lands near zero and the product collapses to a centrality
ranking of the few highest-mass nodes. Rank normalization keeps the prior
informative across the whole candidate list. The cost is that the magnitude of
a centrality difference is discarded, which is the right trade when the score
ranks rather than measures, and the wrong one if you ever want to compare
scores across two different graphs.

## An arithmetic prior

`prior = β·rel + (1−β)·dem`, not a geometric mean. An entity with no observed
questions should be discounted, not eliminated: in most deployments the demand
layer is incomplete, and a geometric prior would silently drop every entity the
collection missed. The consequence is that `β = 1` is a meaningful ablation
(structure only) and `β = 0` is another (demand only), and both should be run.

## Separate source classes, enforced in the type system

`SourceClass` is on `Provenance`, not on a loader flag, so the separation
survives refactoring. The failure it prevents is subtle: if competitor crawls
feed the relatedness graph, entities competitors cover acquire edges, and the
score ranks well-covered entities highest. A gap finder that prefers covered
entities fails silently and looks plausible.

## The judge is an interface, not a model client

The package ships no model client. A deployment supplies a callable; the cache
makes the call happen once. Three reasons: the rubric is the thing that should
be published and reviewed, not the vendor; a released cache lets a reader
recompute without a key; and a second annotator is then a cheap second pass
over the same keys rather than a re-run of the pipeline.

## Why the classification lives in the reasoner

`materialize()` writes inferred types back into the graph, and the example
asserts only `AreaCode`. This is the difference between an ontology that does
work and one that decorates a pipeline. If you move the classification back
into the loader, deleting the ontology changes nothing downstream, and a
reviewer will notice.

## Why `validate()` reports focus-node counts

A SHACL run over a graph with no individuals conforms. So does a run whose
shapes target classes that happen to have no instances. Both read as success.
Reporting the focus-node count and setting `vacuous` makes the difference
visible without the caller having to think of the question.

## What is deliberately not here

No crawler, no SERP client, no model client, no scheduler. Each is a deployment
concern with its own credentials, rate limits and terms, and bundling them
would make the package hard to audit and easy to misuse. The seams are
`DemandAdapter`, the three evidence suppliers on `GapRun`, and `Judge`.

# Command line reference

Every command is also available as `python -m ufi.cli ...`.

```
ufi [-h] [--version] {validate,owl,cq,freeze,lock,verify,manifest} ...
```

## `ufi validate`

Check an ontology specification and its competency questions before scoring.
Reports fatal errors (a property chain that does not compose, a question whose
answer class is not what its chain reaches) and warnings.

```
ufi validate [--lenient] [--strict-warnings] ontology.yaml
```

| Option | Effect |
|---|---|
| `--lenient` | do not raise on fatal findings |
| `--strict-warnings` | exit non-zero on warnings too |

## `ufi owl`

Export OWL 2 and SHACL shapes from the YAML specification.

```
ufi owl [-o OUTPUT] ontology.yaml
```

Terms are minted under `urn:ufi:<name>` unless a base IRI is supplied in the
library call; a URN makes no resolution claim. Anyone publishing an ontology
built with this package should pass a namespace they own and serve.

## `ufi cq`

Run the ontology's competency questions against an RDF graph and print the
two rates separately.

```
ufi cq --graph GRAPH [--format FORMAT] [--base BASE] [--show-sparql] ontology.yaml
```

| Option | Effect |
|---|---|
| `--graph` | RDF file holding the ABox (required) |
| `--format` | rdflib parse format (default by extension) |
| `--base` | base IRI the graph was written with |
| `--show-sparql` | print the generated query for each question |

Output distinguishes the **schema pass rate** (can the ontology express the
question at all) from **instance coverage** (does the graph answer it), because
the two fail for different reasons. A question marked `unsupported` in the
specification is reported as a declared gap with its reason, and never scored
as zero.

## `ufi freeze`

Hash an evaluation query set before launch, one query per line.

```
ufi freeze -o OUTPUT [--note NOTE] queries.txt
```

The output carries the query count, the digest and the freeze time, and the
command refuses to overwrite an existing frozen file.

## `ufi lock`

Pin the score parameters before scoring.

```
ufi lock -o OUTPUT [--alpha ALPHA] [--beta BETA] [--damping DAMPING] [--note NOTE]
```

Defaults: α = 0.5, β = 0.5, damping = 0.85.

## `ufi verify`

Confirm a frozen query set is intact: recomputes the digest and compares.

```
ufi verify frozen.json
```

## `ufi manifest`

Print a run's reproducibility digest and what it covers.

```
ufi manifest out/manifest.json
```

## Scoring

Scoring is a library call, not a subcommand, because a run needs evidence
suppliers wired to a deployment's own crawls and judgment sources.
`examples/nanp/build_example.py` is the template: it builds the ontology and
graph, declares every demand surface, runs the reasoner and SHACL, executes
the competency questions, scores, compares against the practitioner baselines
and writes the manifest.

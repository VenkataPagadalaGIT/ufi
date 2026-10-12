"""Command line interface.

    ufi validate ontology.yaml              check the model before scoring
    ufi owl ontology.yaml -o nanp.owl       export OWL 2 and SHACL
    ufi cq ontology.yaml --graph kg.nt      run competency questions, print rates
    ufi freeze queries.txt -o frozen.json   hash the query set before launch
    ufi lock -o params.lock.json            pin alpha, beta, damping
    ufi verify frozen.json                  confirm a frozen set is intact
    ufi manifest out/manifest.json          print a run's reproducibility digest

Scoring itself is a library call rather than a subcommand, because a run needs
evidence suppliers wired to a deployment's own crawls. `examples/nanp` is the
template to copy.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .ontology import Ontology, OntologyError
from .provenance import freeze_queries, lock_parameters, verify_frozen
from .score import Parameters


def _validate(a) -> int:
    try:
        onto = Ontology.from_yaml(a.ontology)
    except Exception as exc:
        print(f"could not load: {exc}", file=sys.stderr)
        return 2
    try:
        problems = onto.validate(strict=not a.lenient)
    except OntologyError as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        return 1
    print(f"{onto.name} {onto.version}: {len(onto.classes)} classes, "
          f"{len(onto.properties)} properties, {len(onto.questions)} competency "
          f"questions, fingerprint {onto.fingerprint()}")
    if not problems:
        print("no problems found")
        return 0
    for p in problems:
        print(f"  - {p}")
    return 1 if a.strict_warnings else 0


def _owl(a) -> int:
    onto = Ontology.from_yaml(a.ontology)
    out = Path(a.output) if a.output else None
    owl, shacl = onto.to_owl(), onto.to_shacl()
    if out:
        out.write_text(owl, encoding="utf-8")
        sh = out.with_suffix(".shapes.ttl")
        sh.write_text(shacl, encoding="utf-8")
        print(f"wrote {out} and {sh}")
    else:
        print(owl)
    return 0


def _cq(a) -> int:
    """Run the competency questions and print both rates.

    Needs a graph. Without one there is no coverage to report, and printing a
    schema pass rate alone would invite the reading that the questions were
    executed. The graph should be the materialized one: see cq.run.
    """
    onto = Ontology.from_yaml(a.ontology)
    try:
        from . import cq as _cq_mod
        from rdflib import Graph
    except ImportError as exc:
        print(f'needs the rdf extras ({exc}); pip install "ufi[rdf]"',
              file=sys.stderr)
        return 2
    base = a.base or f"http://w3id.org/ufi/{onto.name}"
    g = Graph()
    g.parse(a.graph, format=a.format)
    results = _cq_mod.run(onto, graph=g, base=base)
    print(_cq_mod.report(results))
    if a.show_sparql:
        print()
        for r in results:
            print(f"--- {r.id}: {r.template}")
            print(r.sparql if r.supported else f"    unsupported: {r.reason}")
    return 0 if all(r.supported for r in results) else 1


def _freeze(a) -> int:
    qs = Path(a.queries).read_text(encoding="utf-8").splitlines()
    try:
        info = freeze_queries(qs, a.output, note=a.note or "")
    except FileExistsError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps(info, indent=1))
    return 0


def _lock(a) -> int:
    params = Parameters(alpha=a.alpha, beta=a.beta, damping=a.damping)
    params.validate()
    try:
        payload = lock_parameters(params, a.output, note=a.note or "")
    except FileExistsError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(json.dumps(payload, indent=1))
    return 0


def _verify(a) -> int:
    info = verify_frozen(a.frozen)
    print(json.dumps(info, indent=1))
    return 0 if info["intact"] else 1


def _manifest(a) -> int:
    d = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    for k in ("package_version", "created", "ontology_fingerprint",
              "graph_fingerprint", "cache_fingerprint", "parameters_hash",
              "frozen_queries_hash", "n_entities", "n_triples", "n_judgments",
              "demand_first_party_share", "demand_synthetic_share"):
        print(f"{k:28} {d.get(k)}")
    if str(d.get("frozen_queries_hash", "")).startswith("none:"):
        print("\nNOTE: this run had no frozen query set, so any share or "
              "percentage computed on its query universe was defined after the "
              "outcome was observable.")
    if float(d.get("demand_synthetic_share", 0)) > 0:
        print(f"\nNOTE: {float(d['demand_synthetic_share']):.0%} of the linked "
              "demand evidence in this run is synthetic. Nothing computed from "
              "it is an observation about users.")
    if float(d.get("demand_first_party_share", 0)) == 0.0:
        print("\nNOTE: no demand evidence came from a first-party surface. The "
              "demand term is entirely tool-derived, so a 'user first' claim is "
              "not supported by this run.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="ufi", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version=f"ufi {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="check an ontology specification")
    v.add_argument("ontology")
    v.add_argument("--lenient", action="store_true", help="do not raise on fatal")
    v.add_argument("--strict-warnings", action="store_true",
                   help="exit non-zero on warnings too")
    v.set_defaults(fn=_validate)

    o = sub.add_parser("owl", help="export OWL 2 and SHACL shapes")
    o.add_argument("ontology")
    o.add_argument("-o", "--output")
    o.set_defaults(fn=_owl)

    c = sub.add_parser("cq", help="run competency questions against a graph")
    c.add_argument("ontology")
    c.add_argument("--graph", required=True, help="RDF file holding the ABox")
    c.add_argument("--format", default="nt", help="rdflib parse format")
    c.add_argument("--base", help="base IRI the graph was written with")
    c.add_argument("--show-sparql", action="store_true",
                   help="print the generated query for every question")
    c.set_defaults(fn=_cq)

    f = sub.add_parser("freeze", help="hash an evaluation query set")
    f.add_argument("queries", help="one query per line")
    f.add_argument("-o", "--output", required=True)
    f.add_argument("--note")
    f.set_defaults(fn=_freeze)

    l = sub.add_parser("lock", help="pin the score parameters")
    l.add_argument("-o", "--output", required=True)
    l.add_argument("--alpha", type=float, default=0.5)
    l.add_argument("--beta", type=float, default=0.5)
    l.add_argument("--damping", type=float, default=0.85)
    l.add_argument("--note")
    l.set_defaults(fn=_lock)

    w = sub.add_parser("verify", help="confirm a frozen query set is intact")
    w.add_argument("frozen")
    w.set_defaults(fn=_verify)

    m = sub.add_parser("manifest", help="print a run manifest")
    m.add_argument("manifest")
    m.set_defaults(fn=_manifest)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())

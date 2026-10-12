"""RDF serialization, reasoning and SHACL validation.

The functional-syntax export in `ontology.to_owl` is readable by a person. This
module produces the artifact a machine consumes: an RDF graph carrying the TBox,
the alignments and, when a knowledge graph is supplied, the ABox. Everything a
Semantic Web reviewer checks runs from here.

The ABox matters more than it looks. A SHACL run over a TBox alone selects no
focus nodes and reports no violations, and an empty run reads exactly like a
clean one. `validate()` refuses to report success when it had nothing to check.

rdflib and pyshacl are optional dependencies; import this module only when the
RDF path is wanted, and install with `pip install "ufi[rdf]"`.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .ontology import default_base

if TYPE_CHECKING:
    from .graph import KnowledgeGraph
    from .ontology import Ontology

try:
    from rdflib import BNode, Graph, Literal, Namespace, URIRef
    from rdflib.collection import Collection
    from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD
    _HAVE_RDFLIB = True
except ImportError:                                   # pragma: no cover
    _HAVE_RDFLIB = False

SCHEMA = "http://schema.org/"


def _require() -> None:
    if not _HAVE_RDFLIB:
        raise ImportError(
            "RDF export needs rdflib and pyshacl. Install with: "
            'pip install "ufi[rdf]"')


def _safe(ident: str) -> str:
    import re
    return re.sub(r"[^A-Za-z0-9_.-]", "_", ident)


def to_rdf(onto: "Ontology", kg: "KnowledgeGraph | None" = None,
           base: str | None = None) -> "Graph":
    """Build an RDF graph of the ontology, and of the instances when given."""
    _require()
    base = base or default_base(onto.name)
    NS = Namespace(base + "#")
    g = Graph()
    g.bind("", NS)
    g.bind("owl", OWL); g.bind("rdfs", RDFS); g.bind("skos", SKOS)
    g.bind("dcterms", DCTERMS); g.bind("schema", Namespace(SCHEMA))

    onto_iri = URIRef(base)
    g.add((onto_iri, RDF.type, OWL.Ontology))
    g.add((onto_iri, OWL.versionIRI, URIRef(f"{base}/{onto.version}")))
    g.add((onto_iri, RDFS.label, Literal(f"{onto.name} {onto.version}")))
    g.add((onto_iri, DCTERMS.license,
           URIRef("http://creativecommons.org/licenses/by/4.0/")))

    def term(name: str) -> URIRef:
        if name.startswith("ext:"):
            return URIRef(SCHEMA + name[4:])
        if name.startswith("xsd:"):
            return getattr(XSD, name[4:])
        return NS[name]

    for name, c in onto.classes.items():
        cls = NS[name]
        g.add((cls, RDF.type, OWL.Class))
        if c.parent:
            g.add((cls, RDFS.subClassOf, NS[c.parent]))
        for d in c.disjoint_with:
            if d > name:
                g.add((cls, OWL.disjointWith, NS[d]))
        if c.covered_by:
            node = BNode()
            Collection(g, node, [NS[x] for x in c.covered_by])
            union = BNode()
            g.add((union, RDF.type, OWL.Class))
            g.add((union, OWL.unionOf, node))
            g.add((cls, OWL.equivalentClass, union))
        if c.defined_by:
            members = [NS[a] for a in c.defined_by.get("and", [])]
            for prop, rng in (c.defined_by.get("some") or {}).items():
                restr = BNode()
                g.add((restr, RDF.type, OWL.Restriction))
                g.add((restr, OWL.onProperty, NS[prop]))
                g.add((restr, OWL.someValuesFrom, term(rng)))
                members.append(restr)
            if len(members) == 1:
                g.add((cls, OWL.equivalentClass, members[0]))
            elif members:
                lst = BNode()
                Collection(g, lst, members)
                inter = BNode()
                g.add((inter, RDF.type, OWL.Class))
                g.add((inter, OWL.intersectionOf, lst))
                g.add((cls, OWL.equivalentClass, inter))
        if c.key:
            node = BNode()
            Collection(g, node, [NS[k] for k in c.key])
            g.add((cls, OWL.hasKey, node))
        if c.note:
            g.add((cls, RDFS.comment, Literal(c.note)))
        for pred, target in c.align.items():
            g.add((cls, _pred(pred), URIRef(target)))

    for name, p in onto.properties.items():
        if p.derived:
            continue
        prop = NS[name]
        is_data = p.kind == "data"
        g.add((prop, RDF.type, OWL.DatatypeProperty if is_data else OWL.ObjectProperty))
        g.add((prop, RDFS.domain, term(p.domain)))
        g.add((prop, RDFS.range, term(p.range)))
        if p.functional:
            g.add((prop, RDF.type, OWL.FunctionalProperty))
        if not is_data:
            for flag, cls_ in (("symmetric", OWL.SymmetricProperty),
                               ("asymmetric", OWL.AsymmetricProperty),
                               ("irreflexive", OWL.IrreflexiveProperty),
                               ("transitive", OWL.TransitiveProperty)):
                if getattr(p, flag, False):
                    g.add((prop, RDF.type, cls_))
            if p.inverse_of:
                g.add((prop, OWL.inverseOf, NS[p.inverse_of]))
        if p.sub_property_of:
            g.add((prop, RDFS.subPropertyOf, NS[p.sub_property_of]))
        if p.min_cardinality:
            restr = BNode()
            g.add((restr, RDF.type, OWL.Restriction))
            g.add((restr, OWL.onProperty, prop))
            g.add((restr, OWL.minCardinality,
                   Literal(p.min_cardinality, datatype=XSD.nonNegativeInteger)))
            g.add((term(p.domain), RDFS.subClassOf, restr))
        for pred, target in p.align.items():
            g.add((prop, _pred(pred), URIRef(target)))
        if p.note:
            g.add((prop, RDFS.comment, Literal(p.note)))

    if kg is not None:
        by_class: dict[str, list[URIRef]] = {}
        for e in kg.entities.values():
            ind = NS[_safe(e.id)]
            g.add((ind, RDF.type, OWL.NamedIndividual))
            g.add((ind, RDF.type, NS[e.cls]))
            if e.label:
                g.add((ind, RDFS.label, Literal(e.label)))
            by_class.setdefault(e.cls, []).append(ind)
        for t in kg.triples:
            spec = onto.properties.get(t.predicate)
            if spec is None or spec.derived:
                continue
            subj = NS[_safe(t.subject)]
            if spec.kind == "data" or t.object.startswith("lit:"):
                val = t.object[4:] if t.object.startswith("lit:") else t.object
                g.add((subj, NS[t.predicate], Literal(val)))
            else:
                g.add((subj, NS[t.predicate], NS[_safe(t.object)]))
        # Without an explicit difference, a functional property merges two
        # values rather than reporting the clash it exists to detect.
        for cls_name in ("TimeZone", "Place", "OverlayComplex"):
            members = by_class.get(cls_name, [])
            if len(members) > 1:
                node = BNode()
                g.add((node, RDF.type, OWL.AllDifferent))
                lst = BNode()
                Collection(g, lst, members)
                g.add((node, OWL.distinctMembers, lst))
    return g


def _pred(name: str) -> "URIRef":
    table = {"skos:exactMatch": SKOS.exactMatch, "skos:closeMatch": SKOS.closeMatch,
             "skos:broadMatch": SKOS.broadMatch, "rdfs:subPropertyOf": RDFS.subPropertyOf,
             "owl:equivalentProperty": OWL.equivalentProperty,
             "owl:equivalentClass": OWL.equivalentClass}
    return table.get(name, RDFS.seeAlso)


def validate(onto: "Ontology", kg: "KnowledgeGraph", shapes_ttl: str | None = None
             ) -> dict[str, Any]:
    """Run SHACL over the populated graph and report focus nodes and violations.

    Refuses to call a run clean when it had nothing to check: a validation over
    zero focus nodes conforms trivially, and reporting that as conformance is
    the most common way a graph is declared valid without being checked.
    """
    _require()
    import pyshacl
    data = to_rdf(onto, kg)
    shapes = Graph().parse(data=shapes_ttl or onto.to_shacl(), format="turtle")
    conforms, results_graph, text = pyshacl.validate(
        data, shacl_graph=shapes, inference="none", abort_on_first=False,
        meta_shacl=False, advanced=False)
    targets = set()
    for s, _, o in shapes.triples((None, URIRef(
            "http://www.w3.org/ns/shacl#targetClass"), None)):
        targets.update(x for x in data.subjects(RDF.type, o))
    n_violations = len(list(results_graph.subjects(
        RDF.type, URIRef("http://www.w3.org/ns/shacl#ValidationResult"))))
    return {
        "conforms": bool(conforms) and len(targets) > 0,
        "focus_nodes": len(targets),
        "violations": n_violations,
        "vacuous": len(targets) == 0,
        "report": text,
        "note": ("no focus nodes: the shapes target classes with no instances, "
                 "so this run checked nothing") if not targets else "",
    }


def reason(onto: "Ontology", kg: "KnowledgeGraph | None" = None,
           timeout: int = 120) -> dict[str, Any]:
    """Run HermiT over the ontology and report consistency and inferences.

    Reports the number of inferred class assertions that were not asserted, so
    that "a reasoner ran" can be distinguished from "a reasoner had something
    to do". An ontology with no defined classes produces zero of them, and the
    run is vacuous however green it looks.
    """
    _require()
    import tempfile, os
    import owlready2

    g = to_rdf(onto, kg)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "onto.ntriples")
        # RDF/XML silently drops the blank-node lists that carry unionOf,
        # intersectionOf and hasKey, which are exactly the axioms a reasoner
        # needs here. N-Triples keeps them.
        g.serialize(destination=path, format="ntriples")
        world = owlready2.World()
        loaded = world.get_ontology("file://" + path).load()
        asserted = {(str(i.iri), str(c.iri))
                    for i in loaded.individuals() for c in i.is_a
                    if hasattr(c, "iri")}
        try:
            with loaded:
                owlready2.sync_reasoner(world, infer_property_values=False,
                                        debug=0)
            consistent = True
            error = ""
        except owlready2.OwlReadyInconsistentOntologyError as exc:
            return {"consistent": False, "inferred_class_assertions": 0,
                    "vacuous": False, "error": str(exc)[:400],
                    "reasoner": "HermiT (owlready2)"}
        after = {(str(i.iri), str(c.iri))
                 for i in loaded.individuals() for c in i.is_a
                 if hasattr(c, "iri")}
        new = sorted(after - asserted)
        return {
            "consistent": consistent,
            "inferred_class_assertions": len(new),
            "examples": new[:5],
            "vacuous": len(new) == 0,
            "individuals": len(list(loaded.individuals())),
            "reasoner": "HermiT (owlready2)",
            "error": error,
            "note": ("no new class assertions were inferred: the ontology has no "
                     "defined classes, so a reasoner run proves only that nothing "
                     "contradicts anything") if not new else "",
        }


def materialize(onto: "Ontology", kg: "KnowledgeGraph", timeout: int = 120
                ) -> dict[str, Any]:
    """Classify the graph with a reasoner and write inferred types back.

    This is what makes the ontology load-bearing rather than decorative. The
    collection step asserts what a source states: a code, and a place it serves.
    Whether that code is geographic is an entailment of the ontology, not a
    field in the registry, and this step derives it. An ontology whose removal
    would change no downstream number is not doing any work, and the way to
    tell is to put the classification here instead of in the loader.
    """
    _require()
    import tempfile, os
    import owlready2
    from .types import Entity

    g = to_rdf(onto, kg)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "onto.ntriples")
        g.serialize(destination=path, format="ntriples")
        world = owlready2.World()
        loaded = world.get_ontology("file://" + path).load()
        before = {str(i.iri): {str(c.iri).split("#")[-1] for c in i.is_a
                               if hasattr(c, "iri")}
                  for i in loaded.individuals()}
        try:
            with loaded:
                owlready2.sync_reasoner(world, infer_property_values=False, debug=0)
        except owlready2.OwlReadyInconsistentOntologyError as exc:
            return {"consistent": False, "reclassified": 0, "error": str(exc)[:400]}
        changed: list[tuple[str, str]] = []
        for i in loaded.individuals():
            iri = str(i.iri)
            now = {str(c.iri).split("#")[-1] for c in i.is_a if hasattr(c, "iri")}
            for cls_name in sorted(now - before.get(iri, set())):
                if cls_name not in onto.classes:
                    continue
                local = iri.split("#")[-1]
                for eid, ent in kg.entities.items():
                    if _safe(eid) == local:
                        if onto.is_a(cls_name, ent.cls) and cls_name != ent.cls:
                            kg.entities[eid] = Entity(
                                id=ent.id, cls=cls_name, label=ent.label,
                                aliases=ent.aliases, external_ids=ent.external_ids)
                            kg._by_class.setdefault(cls_name, []).append(eid)
                            if eid in kg._by_class.get(ent.cls, []):
                                kg._by_class[ent.cls].remove(eid)
                            changed.append((eid, cls_name))
                        break
        return {"consistent": True, "reclassified": len(changed),
                "examples": changed[:5], "error": "",
                "reasoner": "HermiT (owlready2)"}

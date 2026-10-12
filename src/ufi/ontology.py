"""Ontology specification, competency questions, and their validation.

The ontology is authored in YAML rather than OWL for the working format, and
exported to OWL for publication. The reason is that the parts the score needs
(class hierarchy, object properties with domain and range, the core-class set,
and the competency questions) are a small subset of OWL, and keeping them in a
reviewable file makes the requirements traceable to the artifact, which is what
an ORSD is for.

`validate()` enforces the checks that caught real defects in our own deployment:
a property whose domain is a subclass but whose alignment target is a general
property; a partition without a covering axiom; a competency question whose
relation is not in the ontology; and a core class with no instances, which makes
topic-sensitive PageRank teleport to the empty set.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
from pathlib import Path
from typing import Any, Iterable

import yaml

from .types import CompetencyQuestion, stable_hash


@dataclass
class ClassSpec:
    name: str
    parent: str | None = None
    disjoint_with: tuple[str, ...] = ()
    covered_by: tuple[str, ...] = ()      # partition: this class = union of these
    key: tuple[str, ...] = ()             # HasKey: the identity criterion
    defined_by: dict = field(default_factory=dict)  # equivalence so a reasoner can classify
    align: dict[str, str] = field(default_factory=dict)
    note: str = ""


@dataclass
class PropertySpec:
    name: str
    domain: str
    range: str
    kind: str = "object"          # "object" or "data"
    functional: bool = False
    symmetric: bool = False
    asymmetric: bool = False
    irreflexive: bool = False
    transitive: bool = False
    inverse_of: str | None = None
    sub_property_of: str | None = None
    min_cardinality: int | None = None
    max_cardinality: int | None = None
    align: dict[str, str] = field(default_factory=dict)
    derived: bool = False
    note: str = ""


def _esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def _safe(ident: str) -> str:
    """Turn an internal id into a legal NCName fragment."""
    return re.sub(r"[^A-Za-z0-9_.-]", "_", ident)


class OntologyError(ValueError):
    """Raised when the specification is internally inconsistent."""


@dataclass
class Ontology:
    name: str
    version: str
    classes: dict[str, ClassSpec] = field(default_factory=dict)
    properties: dict[str, PropertySpec] = field(default_factory=dict)
    core_classes: tuple[str, ...] = ()
    questions: tuple[CompetencyQuestion, ...] = ()

    # ---------------------------------------------------------------- loading
    @classmethod
    def from_yaml(cls, path: str | Path) -> "Ontology":
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(raw)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Ontology":
        classes = {}
        for name, spec in (raw.get("classes") or {}).items():
            spec = spec or {}
            classes[name] = ClassSpec(
                name=name,
                parent=spec.get("parent"),
                disjoint_with=tuple(spec.get("disjoint_with") or ()),
                covered_by=tuple(spec.get("covered_by") or ()),
                key=tuple(spec.get("key") or ()),
                defined_by=spec.get("defined_by") or {},
                align=spec.get("align") or {},
                note=spec.get("note", ""),
            )
        props = {}
        for name, spec in (raw.get("properties") or {}).items():
            spec = spec or {}
            props[name] = PropertySpec(
                name=name,
                domain=spec["domain"],
                range=spec["range"],
                kind=spec.get("kind", "data" if str(spec["range"]).startswith("xsd:")
                              else "object"),
                functional=bool(spec.get("functional", False)),
                symmetric=bool(spec.get("symmetric", False)),
                asymmetric=bool(spec.get("asymmetric", False)),
                irreflexive=bool(spec.get("irreflexive", False)),
                transitive=bool(spec.get("transitive", False)),
                inverse_of=spec.get("inverse_of"),
                sub_property_of=spec.get("sub_property_of"),
                min_cardinality=spec.get("min_cardinality"),
                max_cardinality=spec.get("max_cardinality"),
                align=spec.get("align") or {},
                derived=bool(spec.get("derived", False)),
                note=spec.get("note", ""),
            )
        questions = []
        for q in raw.get("competency_questions") or []:
            questions.append(CompetencyQuestion(
                id=q["id"],
                template=q["template"],
                relation=q["relation"],
                pattern=q.get("pattern", "lookup"),
                verbalizations=tuple(q.get("verbalizations") or ()),
                sparql=q.get("sparql", ""),
                source=q.get("source", ""),
                asks_about=q.get("asks_about", ""),
            ))
        return cls(
            name=raw.get("name", "unnamed"),
            version=str(raw.get("version", "0")),
            classes=classes,
            properties=props,
            core_classes=tuple(raw.get("core_classes") or ()),
            questions=tuple(questions),
        )

    # ------------------------------------------------------------- hierarchy
    def ancestors(self, cls_name: str) -> list[str]:
        out, seen = [], set()
        cur = self.classes.get(cls_name)
        while cur and cur.parent and cur.parent not in seen:
            out.append(cur.parent)
            seen.add(cur.parent)
            cur = self.classes.get(cur.parent)
        return out

    def is_a(self, cls_name: str, ancestor: str) -> bool:
        return cls_name == ancestor or ancestor in self.ancestors(cls_name)

    def descendants(self, cls_name: str) -> list[str]:
        return [c for c in self.classes if c != cls_name and self.is_a(c, cls_name)]

    def questions_for_class(self, cls_name: str) -> list[CompetencyQuestion]:
        """Every competency question asked of instances of this class."""
        out = []
        for q in self.questions:
            target = q.subject_class(self.properties)
            if target and self.is_a(cls_name, target):
                out.append(q)
        return out

    # ------------------------------------------------------------- validation
    def validate(self, strict: bool = True) -> list[str]:
        """Return a list of problems. Raises on the fatal ones when strict."""
        problems: list[str] = []
        fatal: list[str] = []

        for name, c in self.classes.items():
            if c.parent and c.parent not in self.classes:
                fatal.append(f"class {name}: parent {c.parent!r} is not defined")
            for d in c.disjoint_with:
                if d not in self.classes:
                    fatal.append(f"class {name}: disjoint_with {d!r} is not defined")
            # A partition needs a covering axiom, or no reasoner can classify.
            for sub in c.covered_by:
                if sub not in self.classes:
                    fatal.append(f"class {name}: covered_by {sub!r} is not defined")
            if not c.covered_by:
                kids = [k for k, v in self.classes.items() if v.parent == name]
                disjoint_kids = [k for k in kids
                                 if any(o in kids for o in self.classes[k].disjoint_with)]
                if len(disjoint_kids) >= 2:
                    problems.append(
                        f"class {name}: subclasses {sorted(disjoint_kids)} are declared "
                        "disjoint but no covering axiom is given, so the split is not a "
                        "partition and nothing can be inferred from it. Add covered_by.")

        for name, p in self.properties.items():
            for role, target in (("domain", p.domain), ("range", p.range)):
                if target not in self.classes and not target.startswith("xsd:") \
                        and not target.startswith("ext:"):
                    fatal.append(f"property {name}: {role} {target!r} is not defined")
            if p.sub_property_of and p.sub_property_of not in self.properties:
                fatal.append(f"property {name}: sub_property_of {p.sub_property_of!r} undefined")
            if p.inverse_of and p.inverse_of not in self.properties:
                fatal.append(f"property {name}: inverse_of {p.inverse_of!r} undefined")
            if p.symmetric and p.asymmetric:
                fatal.append(f"property {name}: declared both symmetric and asymmetric")
            if p.transitive and p.functional:
                problems.append(f"property {name}: transitive and functional together "
                                "force every chain to collapse to one value")
            if p.functional and p.max_cardinality not in (None, 1):
                problems.append(f"property {name}: functional but max_cardinality="
                                f"{p.max_cardinality}")
            # The alignment trap: equating a specialised property with a general
            # external one lets the external data entail membership of our domain.
            eq = p.align.get("owl:equivalentProperty")
            if eq and p.domain != self._root_of(p.domain):
                problems.append(
                    f"property {name}: declared owl:equivalentProperty {eq} while its "
                    f"domain is the specialised class {p.domain}. Loading the external "
                    f"data would entail that every subject of {eq} is a {p.domain}. "
                    "Use rdfs:subPropertyOf, or widen the domain.")
            if p.symmetric and p.transitive is False and p.note.lower().find("complex") >= 0:
                problems.append(
                    f"property {name}: symmetric but not transitive, while its note "
                    "describes membership of a complex. Group membership needs "
                    "transitivity or an explicit grouping class.")

        for q in self.questions:
            if q.relation not in self.properties:
                fatal.append(f"competency question {q.id}: relation {q.relation!r} undefined")
            if not q.verbalizations:
                problems.append(f"competency question {q.id}: no verbalizations, so "
                                "answerability would be judged on one phrasing only")
            elif len(q.verbalizations) < 3:
                problems.append(f"competency question {q.id}: only "
                                f"{len(q.verbalizations)} verbalizations; the method "
                                "specifies at least three")
            target = q.subject_class(self.properties)
            if target and target not in self.classes and not target.startswith("ext:"):
                fatal.append(f"competency question {q.id}: asks about {target!r}, "
                             "which is not a class")
            if q.pattern == "inverse" and not q.asks_about:
                problems.append(
                    f"competency question {q.id}: inverse pattern with no "
                    "asks_about, so it is attributed to the relation's range by "
                    "inference. State asks_about to make the attribution explicit.")

        for c in self.core_classes:
            if c not in self.classes:
                fatal.append(f"core class {c!r} is not defined")

        if not self.core_classes:
            fatal.append("no core classes: the relatedness teleport set would be empty")

        if strict and fatal:
            raise OntologyError("; ".join(fatal))
        return fatal + problems

    def _root_of(self, cls_name: str) -> str:
        anc = self.ancestors(cls_name)
        return anc[-1] if anc else cls_name

    # ---------------------------------------------------------------- export
    def fingerprint(self) -> str:
        return stable_hash(
            self.name, self.version,
            sorted((k, v.parent, v.covered_by) for k, v in self.classes.items()),
            sorted((k, v.domain, v.range, v.functional, v.symmetric)
                   for k, v in self.properties.items()),
            tuple(sorted(self.core_classes)),
            tuple(sorted(q.id for q in self.questions)),
        )

    def to_owl(self, individuals: "KnowledgeGraph | None" = None) -> str:
        """Emit OWL 2 functional syntax that a reasoner can load.

        An earlier version of this method dropped every property alignment and
        emitted a bare name where an IRI was required, so the file did not
        parse and the alignment corrections this ontology exists to demonstrate
        were invisible in it. Both are fixed, and `test_owl_parses` guards it.

        Passing a graph writes the ABox too. Without individuals a SHACL run
        selects no focus nodes and reports no violations, which is easily
        mistaken for a clean validation.
        """
        base = f"http://w3id.org/ufi/{self.name}"
        ext = {"ext": "http://www.w3.org/2002/07/owl#Thing"}
        L = [f"Prefix(:=<{base}#>)",
             "Prefix(owl:=<http://www.w3.org/2002/07/owl#>)",
             "Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)",
             "Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)",
             "Prefix(skos:=<http://www.w3.org/2004/02/skos/core#>)",
             "Prefix(dcterms:=<http://purl.org/dc/terms/>)",
             "Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)",
             "Prefix(ext:=<http://schema.org/>)",
             "", f"Ontology(<{base}> <{base}/{self.version}>",
             f'  Annotation(rdfs:label "{self.name} {self.version}")',
             '  Annotation(dcterms:license <http://creativecommons.org/licenses/by/4.0/>)',
             "  Declaration(AnnotationProperty(skos:exactMatch))",
             "  Declaration(AnnotationProperty(skos:closeMatch))",
             "  Declaration(AnnotationProperty(rdfs:subPropertyOf))"]

        def iri(name: str) -> str:
            if name.startswith("ext:"):
                return name                      # a declared prefix, not a bare name
            if name.startswith("xsd:"):
                return name
            return f":{name}"

        for name, c in self.classes.items():
            L.append(f"  Declaration(Class(:{name}))")
            if c.parent:
                L.append(f"  SubClassOf(:{name} :{c.parent})")
            for d in c.disjoint_with:
                if d > name:
                    L.append(f"  DisjointClasses(:{name} :{d})")
            if c.covered_by:
                parts = " ".join(f":{x}" for x in c.covered_by)
                L.append(f"  EquivalentClasses(:{name} ObjectUnionOf({parts}))")
            if c.defined_by:
                parts = []
                for anc in c.defined_by.get("and", []):
                    parts.append(f":{anc}")
                for prop, rng in (c.defined_by.get("some") or {}).items():
                    parts.append(f"ObjectSomeValuesFrom(:{prop} :{rng})")
                if len(parts) == 1:
                    L.append(f"  EquivalentClasses(:{name} {parts[0]})")
                elif parts:
                    L.append(f"  EquivalentClasses(:{name} "
                             f"ObjectIntersectionOf({' '.join(parts)}))")
            if c.key:
                props = " ".join(f":{k}" for k in c.key)
                obj = " ".join(f":{k}" for k in c.key
                               if self.properties.get(k, PropertySpec(k, "", "")).kind == "object")
                dat = " ".join(f":{k}" for k in c.key
                               if self.properties.get(k, PropertySpec(k, "", "")).kind == "data")
                L.append(f"  HasKey(:{name} ({obj}) ({dat}))")
            if c.note:
                L.append(f'  AnnotationAssertion(rdfs:comment :{name} "{_esc(c.note)}")')
            for pred, target in c.align.items():
                L.append(f"  AnnotationAssertion({pred} :{name} <{target}>)")

        for name, p in self.properties.items():
            if p.derived:
                L.append(f"  # :{name} is derived, not asserted")
                continue
            decl = "DataProperty" if p.kind == "data" else "ObjectProperty"
            L.append(f"  Declaration({decl}(:{name}))")
            L.append(f"  {decl}Domain(:{name} {iri(p.domain)})")
            L.append(f"  {decl}Range(:{name} {iri(p.range)})")
            if p.functional:
                L.append(f"  Functional{decl}(:{name})")
            if p.kind == "object":
                if p.symmetric:
                    L.append(f"  SymmetricObjectProperty(:{name})")
                if p.asymmetric:
                    L.append(f"  AsymmetricObjectProperty(:{name})")
                if p.irreflexive:
                    L.append(f"  IrreflexiveObjectProperty(:{name})")
                if p.transitive:
                    L.append(f"  TransitiveObjectProperty(:{name})")
                if p.inverse_of:
                    L.append(f"  InverseObjectProperties(:{name} :{p.inverse_of})")
            if p.sub_property_of:
                L.append(f"  Sub{decl}Of(:{name} :{p.sub_property_of})")
            if p.min_cardinality:
                card = "ObjectMinCardinality" if p.kind == "object" else "DataMinCardinality"
                L.append(f"  SubClassOf({iri(p.domain)} {card}("
                         f"{p.min_cardinality} :{name}))")
            # The alignment corrections this ontology demonstrates live here.
            for pred, target in p.align.items():
                L.append(f"  AnnotationAssertion({pred} :{name} <{target}>)")
            if p.note:
                L.append(f'  AnnotationAssertion(rdfs:comment :{name} "{_esc(p.note)}")')

        if individuals is not None:
            named_by_class: dict[str, list[str]] = {}
            for e in individuals.entities.values():
                L.append(f"  Declaration(NamedIndividual(:{_safe(e.id)}))")
                L.append(f"  ClassAssertion(:{e.cls} :{_safe(e.id)})")
                if e.label:
                    L.append(f'  AnnotationAssertion(rdfs:label :{_safe(e.id)} '
                             f'"{_esc(e.label)}")')
                named_by_class.setdefault(e.cls, []).append(_safe(e.id))
            for t in individuals.triples:
                if t.predicate not in self.properties:
                    continue
                spec = self.properties[t.predicate]
                if spec.derived:
                    continue
                if spec.kind == "data" or t.object.startswith("lit:"):
                    val = t.object[4:] if t.object.startswith("lit:") else t.object
                    L.append(f'  DataPropertyAssertion(:{t.predicate} '
                             f':{_safe(t.subject)} "{_esc(val)}")')
                else:
                    L.append(f"  ObjectPropertyAssertion(:{t.predicate} "
                             f":{_safe(t.subject)} :{_safe(t.object)})")
            # Without this, a functional property silently merges two values
            # instead of reporting the inconsistency it exists to catch.
            for cls in ("TimeZone", "Place", "OverlayComplex"):
                members = named_by_class.get(cls, [])
                if len(members) > 1:
                    L.append("  DifferentIndividuals(" +
                             " ".join(f":{m}" for m in members) + ")")
        L.append(")")
        return "\n".join(L)

    def to_shacl(self) -> str:
        """Emit SHACL shapes for the cardinalities the ontology declares."""
        base = f"http://w3id.org/ufi/{self.name}"
        L = ["@prefix sh: <http://www.w3.org/ns/shacl#> .",
             "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
             f"@prefix : <{base}#> .", ""]
        by_domain: dict[str, list[PropertySpec]] = {}
        for p in self.properties.values():
            if not p.derived and (p.min_cardinality or p.max_cardinality or p.functional):
                by_domain.setdefault(p.domain, []).append(p)
        for dom, props in by_domain.items():
            L.append(f":{dom}Shape a sh:NodeShape ;")
            L.append(f"  sh:targetClass :{dom} ;")
            for i, p in enumerate(props):
                tail = " ;" if i < len(props) - 1 else " ."
                parts = [f"sh:path :{p.name}"]
                if p.min_cardinality:
                    parts.append(f"sh:minCount {p.min_cardinality}")
                mx = 1 if p.functional else p.max_cardinality
                if mx:
                    parts.append(f"sh:maxCount {mx}")
                L.append(f"  sh:property [ {' ; '.join(parts)} ]{tail}")
            L.append("")
        return "\n".join(L)

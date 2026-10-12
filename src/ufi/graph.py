"""The knowledge graph, with the structure/coverage/demand separation enforced.

`KnowledgeGraph.structure_subgraph()` returns only the object-valued triples
whose provenance is a STRUCTURE source, with rdf:type edges removed and edges
symmetrized. That is the graph relatedness is computed on, and the reason it is
a separate method rather than a flag is that mixing coverage evidence into it
is the specific error that makes a gap-finding score penalize gaps: an entity
that competitors cover well acquires more triples, more centrality, and a higher
prior, so the score ranks covered entities above uncovered ones.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date

import networkx as nx

from .types import Entity, SourceClass, Triple


class ProvenanceError(ValueError):
    """Raised when a statement is added without usable provenance."""


@dataclass
class KnowledgeGraph:
    entities: dict[str, Entity] = field(default_factory=dict)
    triples: list[Triple] = field(default_factory=list)
    _by_subject: dict[str, list[Triple]] = field(default_factory=lambda: defaultdict(list))
    _by_class: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    # ------------------------------------------------------------------ build
    def add_entity(self, entity: Entity) -> Entity:
        existing = self.entities.get(entity.id)
        if existing:
            if existing.cls != entity.cls:
                raise ValueError(
                    f"entity {entity.id} already typed {existing.cls}, not {entity.cls}"
                )
            return existing
        self.entities[entity.id] = entity
        self._by_class[entity.cls].append(entity.id)
        return entity

    def add_triple(self, triple: Triple) -> None:
        p = triple.provenance
        if not p or not p.source_id or not p.retrieved:
            raise ProvenanceError(
                f"triple {triple.subject} {triple.predicate} {triple.object} has no "
                "source_id or retrieval date. Every statement in the graph carries "
                "provenance; this is checked here so that a later audit of where a "
                "published fact came from cannot come up empty."
            )
        self.triples.append(triple)
        self._by_subject[triple.subject].append(triple)

    def instances(self, cls: str, ontology=None) -> list[str]:
        if ontology is None:
            return list(self._by_class.get(cls, []))
        out: list[str] = []
        for c, ids in self._by_class.items():
            if ontology.is_a(c, cls):
                out.extend(ids)
        return out

    def triples_of(self, subject: str) -> list[Triple]:
        return list(self._by_subject.get(subject, []))

    def facts_for(self, subject: str, predicate: str) -> list[Triple]:
        return [t for t in self._by_subject.get(subject, []) if t.predicate == predicate]

    # ------------------------------------------------------------- subgraphs
    def structure_subgraph(self, as_of: date | None = None) -> nx.Graph:
        """Undirected, type-edge-free graph over STRUCTURE triples only."""
        g = nx.Graph()
        for e in self.entities.values():
            g.add_node(e.id, cls=e.cls)
        for t in self.triples:
            if t.provenance.source_class is not SourceClass.STRUCTURE:
                continue
            if t.predicate in ("rdf:type", "a", "type"):
                continue
            if not t.is_object_valued:
                continue
            if as_of is not None:
                if t.valid_from and t.valid_from > as_of:
                    continue
                if t.valid_to and t.valid_to < as_of:
                    continue
            if t.subject in g and t.object in g:
                g.add_edge(t.subject, t.object)
        return g

    def coverage_triples(self) -> Iterator[Triple]:
        for t in self.triples:
            if t.provenance.source_class is SourceClass.COVERAGE:
                yield t

    # ------------------------------------------------------------- reporting
    def source_report(self) -> list[dict]:
        """One row per source: what it is, what it wrote, which role it played.

        This is the table an as-built section should print rather than describe,
        because a source that wrote zero rows is the single most common gap
        between a method as designed and a method as deployed.
        """
        agg: dict[tuple[str, str], dict] = {}
        for t in self.triples:
            p = t.provenance
            k = (p.source_id, p.source_class.value)
            row = agg.setdefault(
                k,
                {
                    "source_id": p.source_id,
                    "source_class": p.source_class.value,
                    "triples": 0,
                    "subjects": set(),
                    "predicates": set(),
                    "first_retrieved": p.retrieved,
                    "last_retrieved": p.retrieved,
                    "licence": p.licence,
                },
            )
            row["triples"] += 1
            row["subjects"].add(t.subject)
            row["predicates"].add(t.predicate)
            row["first_retrieved"] = min(row["first_retrieved"], p.retrieved)
            row["last_retrieved"] = max(row["last_retrieved"], p.retrieved)
        out = []
        for row in agg.values():
            row["subjects"] = len(row["subjects"])
            row["predicates"] = len(row["predicates"])
            out.append(row)
        return sorted(out, key=lambda r: (-r["triples"], r["source_id"]))

    def stats(self) -> dict:
        by_class = {c: len(v) for c, v in sorted(self._by_class.items())}
        struct = self.structure_subgraph()
        return {
            "entities": len(self.entities),
            "triples": len(self.triples),
            "classes": len(by_class),
            "by_class": by_class,
            "structure_nodes": struct.number_of_nodes(),
            "structure_edges": struct.number_of_edges(),
            "isolated_in_structure": sum(1 for n in struct if struct.degree(n) == 0),
            "sources": len({t.provenance.source_id for t in self.triples}),
        }

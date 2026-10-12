"""Core value types for User First Intelligence.

Every object that reaches a score carries provenance. A triple without a source
document and a retrieval date cannot enter the graph; this is enforced in
`KnowledgeGraph.add_triple`, not left to convention.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import date
from enum import Enum
from typing import Any


class SourceClass(str, Enum):
    """The role a source plays in the score.

    The separation matters: structure sources establish relatedness, coverage
    sources establish deficits, demand sources establish priority. A source used
    for two roles lets a competitor's coverage inflate an entity's centrality,
    which is the failure the design exists to avoid.
    """

    STRUCTURE = "structure"      # encyclopedic, registry, standards bodies
    COVERAGE = "coverage"        # the organization's own site, competitor sites
    DEMAND = "demand"            # anywhere users put questions in their own words
    ANSWERABILITY = "answerability"  # retrieved results judged for whether they answer


@dataclass(frozen=True)
class Provenance:
    """Where a statement came from and when."""

    source_id: str
    source_class: SourceClass
    retrieved: date
    locator: str = ""            # URL, file path, row id, API call
    licence: str = ""
    note: str = ""
    synthetic: bool = False      # generated for demonstration, not observed

    def __post_init__(self) -> None:
        if self.locator and self.source_id and self.locator == self.source_id:
            # A locator identical to the source id records nothing: it says the
            # statement came from the thing it came from. Catching it here is
            # cheaper than discovering it in an audit.
            raise ValueError(
                f"provenance locator {self.locator!r} is identical to source_id; "
                "give the row, URL or call that produced this statement")

    def key(self) -> str:
        return f"{self.source_id}:{self.locator}:{self.retrieved.isoformat()}"


@dataclass(frozen=True)
class Triple:
    """A typed, dated, sourced statement."""

    subject: str
    predicate: str
    object: str
    provenance: Provenance
    valid_from: date | None = None
    valid_to: date | None = None

    @property
    def is_object_valued(self) -> bool:
        """True when the object is an entity rather than a literal."""
        return not self.object.startswith("lit:")


@dataclass
class Entity:
    """An instance of an ontology class."""

    id: str
    cls: str
    label: str = ""
    aliases: tuple[str, ...] = ()
    external_ids: dict[str, str] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True)
class CompetencyQuestion:
    """A question the ontology commits to answering.

    `pattern` follows Ren et al. 2014 / Wisniewski et al. 2019: lookup, inverse,
    constrained, comparison. `relation` is the property the question asks about,
    which is what makes a CQ testable as a graph query rather than prose.
    """

    id: str
    template: str                 # "what time zone is area code {e}"
    relation: str = ""            # empty when the question uses `chain`
    pattern: str = "lookup"
    verbalizations: tuple[str, ...] = ()
    sparql: str = ""
    source: str = ""              # which demand source the phrasing came from
    asks_about: str = ""          # the class the question is asked OF
    chain: tuple[str, ...] = ()   # property path; "^p" traverses p backwards
    unsupported: str = ""         # why the ontology cannot express this at all
    answer_class: str = ""        # the class of thing the question asks FOR

    def subject_class(self, properties: dict) -> str:
        """Which class this question is asked about.

        Stated explicitly where it is not the relation's domain. A lookup
        question is asked of the domain ("what time zone is area code X"); an
        inverse question is asked of the range ("which codes are in Georgia").
        Inferring this from the pattern alone is wrong often enough that the
        field is explicit and the inference is only a fallback.
        """
        if self.asks_about:
            return self.asks_about
        p = properties.get(self.relation)
        if p is None:
            return ""
        return p.range if self.pattern == "inverse" else p.domain

    def verbalize(self, label: str) -> tuple[str, ...]:
        forms = self.verbalizations or (self.template,)
        return tuple(f.replace("{e}", label) for f in forms)


class Grade(float, Enum):
    """The three-level rubric used for own, cov_K and answerability.

    A float enum so grades average without conversion, and so a reader can see
    that "partial" is exactly 0.5 rather than an undocumented weight.
    """

    NONE = 0.0
    PARTIAL = 0.5
    FULL = 1.0


@dataclass(frozen=True)
class Judgment:
    """One graded observation, cached so a rerun needs no model call.

    `subject`, `question` and `rubric_id` are recorded because a cache of
    anonymous grades cannot be audited or re-graded. A second annotator needs
    to know what was being judged; a reader checking a published number needs
    to find the row. A bare {key: grade} map satisfies neither, and a released
    cache that satisfies neither is not a reproducibility artifact.
    """

    key: str
    grade: Grade
    rationale: str = ""
    judge_id: str = ""
    model: str = ""
    judged: date | None = None
    subject: str = ""            # the entity being judged
    question: str = ""           # the verbalization or coverage prompt
    rubric_id: str = ""          # which rubric produced this grade
    evidence_digest: str = ""    # hash of the evidence the judge saw

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["grade"] = float(self.grade)
        d["judged"] = self.judged.isoformat() if self.judged else None
        return d


def stable_hash(*parts: Any) -> str:
    """A short, stable hash used for cache keys and freeze manifests."""
    h = hashlib.sha256()
    for p in parts:
        h.update(repr(p).encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()[:16]

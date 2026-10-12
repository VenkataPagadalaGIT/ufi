"""Demand sources: where users put questions in their own words.

The method's demand term counts user questions linked to an entity. The point of
an adapter interface rather than a fixed list is that the set of surfaces where
people ask questions keeps growing, and a deployment should be able to declare
which surfaces it actually read. `DemandIndex.coverage_report()` prints that
declaration, including the surfaces that returned nothing, because a demand term
computed from zero rows is a demand term that does not exist, and a paper that
describes the designed source list without reporting the built one is making a
claim it cannot support.

Adapters here are deliberately thin: each one normalizes its platform's export
into `DemandRecord`. Collection itself (API keys, rate limits, robots.txt) is
out of scope for this package and belongs to the deployment.
"""

from __future__ import annotations

import csv
import json
import re
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .types import Provenance, SourceClass


@dataclass(frozen=True)
class DemandRecord:
    """One observed user question or topic signal."""

    text: str
    surface: str  # forum, video_short, social_group, review_gmb, ...
    source_id: str
    retrieved: date
    weight: float = 1.0  # upvotes, view count, review count, frequency
    locator: str = ""
    language: str = "en"
    synthetic: bool = False  # generated for demonstration, not observed

    def provenance(self, licence: str = "") -> Provenance:
        return Provenance(
            self.source_id,
            SourceClass.DEMAND,
            self.retrieved,
            self.locator or f"{self.source_id}#record",
            licence,
            synthetic=self.synthetic,
        )


class DemandAdapter(ABC):
    """Normalizes one platform's export into DemandRecords.

    Subclass this to add a surface. The contract is only that `read()` yields
    DemandRecords and that `surface` names the kind of place the text came from,
    so the coverage report can distinguish a forum thread from a review.
    """

    surface: str = "unknown"
    requires: tuple[str, ...] = ()

    def __init__(self, source_id: str, retrieved: date, licence: str = ""):
        self.source_id = source_id
        self.retrieved = retrieved
        self.licence = licence

    @abstractmethod
    def read(self, path: str | Path) -> Iterable[DemandRecord]: ...

    def _rec(
        self, text: str, weight: float = 1.0, locator: str = "", language: str = "en"
    ) -> DemandRecord:
        return DemandRecord(
            text=text.strip(),
            surface=self.surface,
            source_id=self.source_id,
            retrieved=self.retrieved,
            weight=weight,
            locator=locator,
            language=language,
        )


class JsonLinesAdapter(DemandAdapter):
    """Generic adapter for a JSONL export with configurable field names."""

    def __init__(
        self,
        source_id: str,
        retrieved: date,
        surface: str,
        text_field: str = "text",
        weight_field: str | None = None,
        locator_field: str | None = None,
        licence: str = "",
    ):
        super().__init__(source_id, retrieved, licence)
        self.surface = surface
        self.text_field = text_field
        self.weight_field = weight_field
        self.locator_field = locator_field

    def read(self, path: str | Path) -> Iterable[DemandRecord]:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            text = (row.get(self.text_field) or "").strip()
            if not text:
                continue
            yield self._rec(
                text,
                weight=float(row.get(self.weight_field, 1.0)) if self.weight_field else 1.0,
                locator=str(row.get(self.locator_field, "")) if self.locator_field else "",
            )


class CsvAdapter(DemandAdapter):
    """Generic adapter for a CSV export, e.g. a keyword or query export."""

    def __init__(
        self,
        source_id: str,
        retrieved: date,
        surface: str,
        text_field: str = "keyword",
        weight_field: str | None = None,
        licence: str = "",
    ):
        super().__init__(source_id, retrieved, licence)
        self.surface = surface
        self.text_field = text_field
        self.weight_field = weight_field

    def read(self, path: str | Path) -> Iterable[DemandRecord]:
        with Path(path).open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                text = (row.get(self.text_field) or "").strip()
                if not text:
                    continue
                w = 1.0
                if self.weight_field and row.get(self.weight_field):
                    try:
                        w = float(row[self.weight_field])
                    except ValueError:
                        w = 1.0
                yield self._rec(text, weight=w)


# Named surfaces. Each is a thin CSV/JSONL subclass; the value is that the
# surface name is declared once and shows up in the coverage report.
FORUM = "forum"
QA_SITE = "qa_site"
VIDEO_SHORT = "video_short"
VIDEO_LONG = "video_long"
SOCIAL_GROUP = "social_group"
SOCIAL_POST = "social_post"
REVIEW_GMB = "review_gmb"
REVIEW_PLATFORM = "review_platform"
REVIEW_APP_STORE = "review_app_store"
PAA = "people_also_ask"
AUTOCOMPLETE = "autocomplete"
SUPPORT_TICKET = "support_ticket"
KEYWORD_EXPORT = "keyword_export"

#: Surfaces the method expects a complete deployment to read, in the order a
#: deployment usually adds them. Used by `DemandIndex.coverage_report` to list
#: the ones that produced nothing, which is the honest as-built statement.
DESIGNED_SURFACES: tuple[str, ...] = (
    FORUM,
    QA_SITE,
    SOCIAL_GROUP,
    SOCIAL_POST,
    VIDEO_SHORT,
    VIDEO_LONG,
    REVIEW_GMB,
    REVIEW_PLATFORM,
    REVIEW_APP_STORE,
    PAA,
    AUTOCOMPLETE,
    SUPPORT_TICKET,
    KEYWORD_EXPORT,
)

#: Which surfaces carry a user's own words rather than a tool's reconstruction.
#: A deployment whose demand evidence is entirely in the second group has a
#: demand term derived from what is already ranked, which is the thing the
#: method claims not to depend on.
FIRST_PARTY_VOICE: frozenset[str] = frozenset(
    {
        FORUM,
        QA_SITE,
        SOCIAL_GROUP,
        SOCIAL_POST,
        VIDEO_SHORT,
        VIDEO_LONG,
        REVIEW_GMB,
        REVIEW_PLATFORM,
        REVIEW_APP_STORE,
        SUPPORT_TICKET,
    }
)
TOOL_DERIVED: frozenset[str] = frozenset({PAA, AUTOCOMPLETE, KEYWORD_EXPORT})


class EntityLinker(ABC):
    """Links a demand record's text to zero or more entity ids."""

    @abstractmethod
    def link(self, text: str) -> list[str]: ...


class AliasLinker(EntityLinker):
    """Longest-match linker over entity labels and aliases.

    Deliberately simple and auditable: a deployment that needs better linking
    should subclass, but a reader should be able to see exactly why a question
    was attributed to an entity.
    """

    def __init__(self, aliases: dict[str, Sequence[str]], word_boundary: bool = True):
        self.patterns: list[tuple[re.Pattern, str]] = []
        for eid, names in aliases.items():
            for n in sorted(set(names), key=len, reverse=True):
                if not n:
                    continue
                pat = re.escape(n)
                if word_boundary:
                    pat = rf"(?<!\w){pat}(?!\w)"
                self.patterns.append((re.compile(pat, re.IGNORECASE), eid))

    def link(self, text: str) -> list[str]:
        hits: list[str] = []
        for pat, eid in self.patterns:
            if eid in hits:
                continue
            if pat.search(text):
                hits.append(eid)
        return hits


@dataclass
class DemandIndex:
    """Counts of linked user questions per entity, with surface attribution."""

    records: list[DemandRecord] = field(default_factory=list)
    links: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list))
    _declared: set[str] = field(default_factory=set)

    def declare(self, *surfaces: str) -> None:
        """Declare a surface as in scope for this deployment, read or not."""
        self._declared.update(surfaces)

    def ingest(self, records: Iterable[DemandRecord], linker: EntityLinker) -> int:
        n = 0
        for r in records:
            idx = len(self.records)
            self.records.append(r)
            self._declared.add(r.surface)
            for eid in linker.link(r.text):
                self.links[eid].append(idx)
            n += 1
        return n

    # -------------------------------------------------------------- counting
    def count(
        self, entity_id: str, surfaces: Iterable[str] | None = None, weighted: bool = False
    ) -> float:
        idxs = self.links.get(entity_id, [])
        if surfaces is not None:
            allowed = set(surfaces)
            idxs = [i for i in idxs if self.records[i].surface in allowed]
        if not weighted:
            return float(len(idxs))
        return float(sum(self.records[i].weight for i in idxs))

    def counts(
        self,
        entity_ids: Iterable[str],
        surfaces: Iterable[str] | None = None,
        weighted: bool = False,
    ) -> dict[str, float]:
        return {e: self.count(e, surfaces, weighted) for e in entity_ids}

    def questions_for(self, entity_id: str, limit: int = 20) -> list[DemandRecord]:
        return [self.records[i] for i in self.links.get(entity_id, [])[:limit]]

    # ------------------------------------------------------------- reporting
    def coverage_report(self, designed: Sequence[str] = DESIGNED_SURFACES) -> list[dict]:
        """One row per designed surface: read, rows, linked rows, entities hit.

        Surfaces with zero rows are listed rather than omitted. That is the
        point of the report.
        """
        by_surface = Counter(r.surface for r in self.records)
        linked_by_surface: Counter = Counter()
        ents_by_surface: dict[str, set[str]] = defaultdict(set)
        for eid, idxs in self.links.items():
            for i in idxs:
                linked_by_surface[self.records[i].surface] += 1
                ents_by_surface[self.records[i].surface].add(eid)
        rows: list[dict] = []
        for s in list(designed) + sorted(self._declared - set(designed)):
            if any(r["surface"] == s for r in rows):
                continue
            rows.append(
                {
                    "surface": s,
                    "voice": "first-party" if s in FIRST_PARTY_VOICE else "tool-derived",
                    "in_scope": s in self._declared,
                    "records": by_surface.get(s, 0),
                    "linked_records": linked_by_surface.get(s, 0),
                    "entities_reached": len(ents_by_surface.get(s, ())),
                    "synthetic_records": sum(
                        1 for r in self.records if r.surface == s and r.synthetic
                    ),
                    "status": "read"
                    if by_surface.get(s, 0)
                    else ("declared, no rows" if s in self._declared else "not collected"),
                }
            )
        return rows

    def first_party_share(self) -> float:
        """Share of linked demand evidence that is in a user's own words.

        Reported next to any claim that a method is user-first. A share of 0.0
        means the demand term is entirely tool-derived.

        Synthetic records are excluded from the numerator. A generated record
        labelled "forum" is not a user's own words, and a guardrail that counts
        it as one reports a healthy share for a deployment that has observed
        nobody, which is the precise failure the guardrail exists to catch.
        """
        total = sum(len(v) for v in self.links.values())
        if not total:
            return 0.0
        fp = sum(
            1
            for idxs in self.links.values()
            for i in idxs
            if self.records[i].surface in FIRST_PARTY_VOICE and not self.records[i].synthetic
        )
        return fp / total

    def synthetic_share(self) -> float:
        """Share of linked demand evidence that was generated, not observed."""
        total = sum(len(v) for v in self.links.values())
        if not total:
            return 0.0
        return (
            sum(1 for idxs in self.links.values() for i in idxs if self.records[i].synthetic)
            / total
        )

"""End-to-end run: ontology + graph + demand + judgments -> ranked gaps.

`GapRun` is the object a deployment configures once and a reader reruns. It
holds the five inputs the score needs and produces, in one call, the entity
ranking, the relation-level schema gaps, the class ranking, the baseline
comparison, the demand coverage report and the run manifest. Everything a paper
reports about a scoring run comes out of `run()`, so the paper's tables are
generated rather than transcribed.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Mapping, Sequence

from . import __version__
from .baselines import BaselineResult, compare_rankings
from .demand import DemandIndex
from .graph import KnowledgeGraph
from .judge import CachedJudge, JudgmentCache, Judge, RUBRIC_ANSWERABILITY, RUBRIC_COVERAGE
from .ontology import Ontology
from .provenance import RunManifest
from .score import (EntityScore, Parameters, aggregate_to_class, demand,
                    relatedness, schema_gap_by_relation, score_entities)
from .types import Grade, stable_hash


@dataclass
class GapRun:
    ontology: Ontology
    graph: KnowledgeGraph
    demand_index: DemandIndex
    params: Parameters = field(default_factory=Parameters)
    target_class: str | None = None

    # evidence suppliers: entity -> text the judge sees. A deployment wires
    # these to its crawls and SERP pulls; the example wires them to files.
    own_evidence: Callable[[str], str] = lambda e: ""
    competitor_evidence: Callable[[str, str], str] = lambda e, k: ""
    serp_evidence: Callable[[str, str], str] = lambda e, q: ""
    competitors: tuple[str, ...] = ()

    judge: Judge | None = None
    cache_path: str | Path = "judgments.json"
    frozen_queries_path: str | Path | None = None

    # ------------------------------------------------------------------ run
    def run(self, outdir: str | Path = "out") -> dict:
        out = Path(outdir)
        out.mkdir(parents=True, exist_ok=True)
        problems = self.ontology.validate(strict=True)

        cls = self.target_class
        entities = (self.graph.instances(cls, self.ontology) if cls
                    else list(self.graph.entities))
        if not entities:
            raise ValueError(
                f"no instances of {cls!r} in the graph. The score is defined over "
                "instances; a class with none cannot be scored, and a class-level "
                "mean over an empty instance set is not a number.")

        core = []
        for c in self.ontology.core_classes:
            core.extend(self.graph.instances(c, self.ontology))
        struct = self.graph.structure_subgraph()
        rel = relatedness(struct, core, damping=self.params.damping)

        dem_counts = self.demand_index.counts(entities)
        dem = demand(dem_counts)

        cache = JudgmentCache(self.cache_path)
        judge = CachedJudge(self.judge, cache) if self.judge else None

        own: dict[str, float] = {}
        cov: dict[str, float] = {}
        ans: dict[str, dict[str, float]] = {}
        ans_by_rel: dict[str, dict[str, float]] = {}

        for e in entities:
            label = self.graph.entities[e].label or e
            if judge:
                j = judge.grade(f"own coverage of {label}",
                                self.own_evidence(e), RUBRIC_COVERAGE)
                own[e] = float(j.grade)
                if self.competitors:
                    gs = [float(judge.grade(f"coverage of {label} by {k}",
                                            self.competitor_evidence(e, k),
                                            RUBRIC_COVERAGE).grade)
                          for k in self.competitors]
                    cov[e] = sum(gs) / len(gs)
                else:
                    cov[e] = 0.0
            else:
                own[e] = 0.0
                cov[e] = 0.0

            # A question the ontology cannot express is a declared gap, not a
            # score of zero. Scoring it would charge every entity for a
            # question no page could answer from this model, and the gap is
            # already reported by cq.run() where it means something.
            qs = [q for q in
                  self.ontology.questions_for_class(self.graph.entities[e].cls)
                  if not q.unsupported]
            per_q: dict[str, float] = {}
            for q in qs:
                if judge:
                    best = 0.0
                    for v in q.verbalize(label):
                        g = float(judge.grade(v, self.serp_evidence(e, v),
                                              RUBRIC_ANSWERABILITY).grade)
                        best = max(best, g)
                    per_q[q.id] = best
                else:
                    per_q[q.id] = 0.0
                # Keyed on the question id, not the relation: a chain
                # question carries relation "" and three such questions
                # collapsed into one bucket in earlier versions, which shipped
                # as the run's largest schema gap.
                ans_by_rel.setdefault(q.id, {})[e] = per_q[q.id]
            ans[e] = per_q

        if judge:
            cache.save()

        scores = score_entities(entities, rel, dem, own, cov, ans, self.params)
        ents_by_rel = {r: [e for e in entities
                           if r in {q.relation for q in
                                    self.ontology.questions_for_class(
                                        self.graph.entities[e].cls)}]
                       for r in {q.relation for q in self.ontology.questions}}
        sg = schema_gap_by_relation(ents_by_rel, rel, dem, own, ans_by_rel, self.params)
        class_of = {e: self.graph.entities[e].cls for e in entities}
        classes = aggregate_to_class(scores, class_of)

        manifest = RunManifest(
            package_version=__version__,
            ontology_fingerprint=self.ontology.fingerprint(),
            graph_fingerprint=stable_hash(sorted(self.graph.entities),
                                          len(self.graph.triples)),
            cache_fingerprint=cache.fingerprint(),
            frozen_queries_hash=_frozen_hash(self.frozen_queries_path),
            parameters_hash=stable_hash(sorted(self.params.__dict__.items())),
            n_entities=len(entities), n_triples=len(self.graph.triples),
            n_judgments=len(cache),
            judge_calls=judge.calls if judge else 0,
            cache_hits=judge.hits if judge else 0,
            demand_first_party_share=self.demand_index.first_party_share(),
            demand_synthetic_share=self.demand_index.synthetic_share(),
            notes={"ontology_warnings": problems,
                   "target_class": cls,
                   "core_instances": len(core)},
        )
        manifest.write(out / "manifest.json")

        _write_csv(out / "scores.csv", [s.as_row() for s in scores])
        _write_csv(out / "classes.csv", classes)
        _write_csv(out / "schema_gaps.csv",
                   [{"relation": r, "SG": round(v, 6)} for r, v in
                    sorted(sg.items(), key=lambda kv: -kv[1])])
        _write_csv(out / "demand_coverage.csv", self.demand_index.coverage_report())
        (out / "graph_sources.json").write_text(
            json.dumps(self.graph.source_report(), indent=1, default=str),
            encoding="utf-8")

        return {"scores": scores, "classes": classes, "schema_gaps": sg,
                "manifest": manifest, "ontology_warnings": problems,
                "demand_coverage": self.demand_index.coverage_report()}


def _frozen_hash(path: str | Path | None) -> str:
    """Read back the frozen query set and record its hash, or say it is absent.

    An empty string here would be indistinguishable from "not checked", so a
    run with no frozen query set records that fact explicitly. A comparison
    computed on a query universe defined after the outcome is a different kind
    of claim, and the manifest should show which kind this run makes.
    """
    if path is None:
        return "none:query-set-not-frozen"
    from .provenance import verify_frozen
    try:
        info = verify_frozen(path)
    except FileNotFoundError:
        return "none:query-set-not-frozen"
    return info["hash"] if info["intact"] else f"TAMPERED:{info['hash']}"


def _write_csv(path: Path, rows: Sequence[Mapping]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

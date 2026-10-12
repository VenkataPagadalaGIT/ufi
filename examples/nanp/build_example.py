#!/usr/bin/env python3
"""A complete, offline, deterministic run of the Content Gap Score.

What is real here and what is not, stated up front because a worked example
that blurs the two is worse than no example:

REAL. The ontology (`ontology.yaml`) and the area-code facts in
`data/area_codes.csv` are real: 66 US geographic codes and 4 non-geographic
codes, with state, principal place, time zones, overlay complex and parent
code. The authority for the full set is the numbering-plan administrator's
central-office code registry; `fetch_registry.py` downloads it when the network
allows, and the bundled file is a verified subset so the example runs offline.

SYNTHETIC. The demand records and the retrieved-result evidence are generated
by `make_demo_inputs.py` with a fixed seed. They exist to exercise the pipeline
deterministically. The scores this example prints are therefore a demonstration
that the machinery runs and emits its artifacts; they are not findings about
the real web, and nothing in them should be cited as one. A deployment wires
`own_evidence`, `competitor_evidence` and `serp_evidence` to its own crawls and
result pulls, and the demand adapters to its own exports.

Run:  python build_example.py
Out:  out/scores.csv, out/classes.csv, out/schema_gaps.csv,
      out/demand_coverage.csv, out/manifest.json, out/graph_sources.json
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "src"))

from ufi import (AliasLinker, DemandIndex, DemandRecord, Entity, GapRun,
                 KnowledgeGraph, Ontology, Parameters, Provenance, RuleJudge,
                 SourceClass, Triple, b1_volume, b2_competitor_gap,
                 b3_question_mining, compare_rankings, freeze_queries,
                 lock_parameters)
from ufi.demand import FORUM, KEYWORD_EXPORT, PAA, REVIEW_GMB, VIDEO_SHORT

REGISTRY = Provenance("nanpa-co-code-registry", SourceClass.STRUCTURE,
                      date(2026, 10, 11), "data/area_codes.csv",
                      licence="public record")
PLACES = Provenance("place-gazetteer", SourceClass.STRUCTURE,
                    date(2026, 10, 11), "data/area_codes.csv",
                    licence="public record")


def build_graph(path: Path) -> KnowledgeGraph:
    g = KnowledgeGraph()
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    for r in rows:
        npa = r["npa"]
        # Assert only what the registry states: that this is a numbering
        # resource. Whether it is geographic follows from whether it serves a
        # place, which is an entailment of the ontology rather than a column in
        # the file, and `materialize` below derives it. Asserting the subclass
        # here instead would make the ontology decorative: deleting it would
        # change nothing downstream.
        g.add_entity(Entity(id=f"npa:{npa}", cls="AreaCode", label=npa,
                            aliases=(f"area code {npa}", npa)))
    for r in rows:
        npa, s = r["npa"], f"npa:{r['npa']}"
        if r["kind"] != "geographic":
            continue
        place = r["principal_place"]
        if place:
            pid = f"place:{place.replace(' ', '_')},{r['state']}"
            g.add_entity(Entity(id=pid, cls="Place", label=f"{place}, {r['state']}"))
            g.add_triple(Triple(s, "locatedIn", pid, PLACES))
        for tz in filter(None, r["time_zones"].split(";")):
            tzid = f"tz:{tz}"
            g.add_entity(Entity(id=tzid, cls="TimeZone", label=tz))
            g.add_triple(Triple(s, "hasTimeZone", tzid, REGISTRY))
        if r["predominant_time_zone"]:
            g.add_triple(Triple(s, "predominantTimeZone",
                                f"tz:{r['predominant_time_zone']}", REGISTRY))
        if r["overlay_complex"]:
            oid = f"complex:{r['overlay_complex']}"
            g.add_entity(Entity(id=oid, cls="OverlayComplex",
                                label=r["overlay_complex"]))
            g.add_triple(Triple(s, "memberOf", oid, REGISTRY))
        if r["parent_code"]:
            g.add_triple(Triple(s, "parentCode", f"npa:{r['parent_code']}", REGISTRY))
    return g


def load_demand(g: KnowledgeGraph, path: Path) -> DemandIndex:
    idx = DemandIndex()
    # Declare every surface the method designs for, so the coverage report
    # lists the ones this deployment did not read rather than omitting them.
    idx.declare(FORUM, VIDEO_SHORT, REVIEW_GMB, PAA, KEYWORD_EXPORT)
    aliases = {e.id: list(e.aliases) + [e.label] for e in g.entities.values()
               if e.cls.endswith("AreaCode")}
    linker = AliasLinker(aliases)
    records = []
    for row in json.loads(path.read_text(encoding="utf-8")):
        records.append(DemandRecord(
            text=row["text"], surface=row["surface"], source_id=row["source_id"],
            retrieved=date.fromisoformat(row["retrieved"]),
            weight=row.get("weight", 1.0),
            synthetic=bool(row.get("synthetic", False))))
    idx.ingest(records, linker)
    return idx


def main() -> int:
    out = HERE / "out"
    onto = Ontology.from_yaml(HERE / "ontology.yaml")
    warnings = onto.validate(strict=True)
    print(f"ontology: {len(onto.classes)} classes, {len(onto.properties)} properties, "
          f"{len(onto.questions)} competency questions, "
          f"{len(warnings)} warnings, fingerprint {onto.fingerprint()}")

    g = build_graph(HERE / "data" / "area_codes.csv")
    # Classify with a reasoner. This is the step that makes the ontology
    # load-bearing: the scored population is an entailment, not a CSV column.
    try:
        from ufi.rdf import materialize, validate
        m = materialize(onto, g)
        print(f"reasoner: {m['reasoner']}, consistent={m['consistent']}, "
              f"{m['reclassified']} individuals reclassified by entailment")
        v = validate(onto, g)
        print(f"SHACL: {v['focus_nodes']} focus nodes, {v['violations']} "
              f"violations, vacuous={v['vacuous']}")
        # Competency questions, executed. The schema rate says what the model
        # can express; the coverage rate says what this graph actually answers.
        # They are printed together because a resource reporting only the first
        # is reporting that it compiled.
        from ufi import cq as _cq
        from ufi.rdf import to_rdf
        print()
        print(_cq.report(_cq.run(onto, graph=to_rdf(onto, g))))
        print()
    except ImportError as exc:
        print(f"RDF extras not installed ({exc}); skipping reasoning and SHACL. "
              'Install with: pip install "ufi[rdf]"')
        for e in list(g.entities.values()):
            if e.cls == "AreaCode" and g.facts_for(e.id, "locatedIn"):
                g.entities[e.id] = Entity(e.id, "GeographicAreaCode", e.label,
                                          e.aliases, e.external_ids)
                g._by_class.setdefault("GeographicAreaCode", []).append(e.id)
                g._by_class["AreaCode"].remove(e.id)
    st = g.stats()
    print(f"graph: {st['entities']} entities, {st['triples']} triples, "
          f"{st['structure_edges']} structure edges, "
          f"{st['isolated_in_structure']} isolated")

    demand_path = HERE / "data" / "demo_demand.json"
    evidence_path = HERE / "data" / "demo_evidence.json"
    if not demand_path.exists():
        print("demo inputs missing; run make_demo_inputs.py first", file=sys.stderr)
        return 1
    idx = load_demand(g, demand_path)
    print(f"demand: {len(idx.records)} records, "
          f"{sum(len(v) for v in idx.links.values())} links, "
          f"first-party share {idx.first_party_share():.2f}, "
          f"synthetic share {idx.synthetic_share():.2f}")

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    own_ev = evidence["own"]
    comp_ev = evidence["competitor"]
    serp_ev = evidence["serp"]

    # Freeze the query set and lock the parameters BEFORE scoring. Both refuse
    # to overwrite, so a rerun uses the originals.
    out.mkdir(parents=True, exist_ok=True)
    geo = [e for e in g.entities.values() if e.cls == "GeographicAreaCode"]
    queries = [v for e in geo for q in onto.questions_for_class(e.cls)
               for v in q.verbalize(e.label)]
    frozen_path = out / "frozen_queries.json"
    if not frozen_path.exists():
        info = freeze_queries(queries, frozen_path,
                              note="all verbalizations x geographic codes")
        print(f"froze {info['n']} queries, hash {info['hash']}")
    params = Parameters(alpha=0.5, beta=0.5)
    lock_path = out / "parameters.lock.json"
    if not lock_path.exists():
        lock_parameters(params, lock_path, note="defaults, set before scoring")

    run = GapRun(
        ontology=onto, graph=g, demand_index=idx, params=params,
        target_class="GeographicAreaCode",
        own_evidence=lambda e: own_ev.get(e, ""),
        competitor_evidence=lambda e, k: comp_ev.get(k, {}).get(e, ""),
        serp_evidence=lambda e, q: serp_ev.get(q, ""),
        competitors=("directory-a", "directory-b", "carrier-x"),
        judge=RuleJudge(),
        cache_path=out / "judgments.json",
        frozen_queries_path=frozen_path,
    )
    res = run.run(out)

    print("\ntop 10 by Content Gap Score")
    print(f"{'code':>6} {'CGS':>8} {'prior':>7} {'own':>5} {'cov':>6} {'ans':>6}")
    for s in res["scores"][:10]:
        print(f"{s.entity.split(':')[1]:>6} {s.cgs:8.4f} {s.prior:7.3f} "
              f"{s.own:5.1f} {s.cov_k:6.2f} {s.mean_ans:6.2f}")

    print("\nschema gap by relation")
    for r, v in sorted(res["schema_gaps"].items(), key=lambda kv: -kv[1]):
        print(f"  {r:<22} {v:.4f}")

    print("\ndemand surfaces")
    for row in res["demand_coverage"]:
        print(f"  {row['surface']:<18} {row['voice']:<12} {row['status']:<18} "
              f"{row['records']:>5} records, {row['entities_reached']:>3} entities")

    # Baselines on the same candidate list, same unit.
    vol_raw = json.loads((HERE / "data" / "demo_volumes.json").read_text())
    vols = {e.id: float(vol_raw.get(e.label, 0.0)) for e in geo}
    comp_rank = {e.id: 1.0 if comp_ev["directory-a"].get(e.id) else 0.0 for e in geo}
    own_rank = {e.id: 1.0 if own_ev.get(e.id) else 0.0 for e in geo}
    qcounts = {e.id: idx.count(e.id) for e in geo}
    bl = [b1_volume(vols), b2_competitor_gap(comp_rank, own_rank),
          b3_question_mining(qcounts)]
    order = [s.entity for s in res["scores"]]
    print("\nagreement with practitioner baselines")
    for row in compare_rankings(order, bl):
        print(f"  {row['baseline']:<22} tau={row['tau']:+.3f}  "
              f"overlap@10={row['overlap@10']:.2f}  {row['note']}")

    m = res["manifest"]
    print(f"\nmanifest digest {m.digest()}  judgments {m.n_judgments} "
          f"(calls {m.judge_calls}, cache hits {m.cache_hits})")
    print(f"artifacts in {out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

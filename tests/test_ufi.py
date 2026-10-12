"""Tests for the parts that are easy to get quietly wrong.

The emphasis is on the failures that would silently produce a wrong number
rather than an exception: a teleport set that falls back to uniform, a
normalization that collapses, a structure subgraph that lets coverage evidence
in, a cache whose digest moves when nothing material changed.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ufi import (AliasLinker, DemandIndex, DemandRecord, Entity, KnowledgeGraph,
                 Ontology, OntologyError, Parameters, Provenance, ProvenanceError,
                 RuleJudge, SourceClass, Triple, JudgmentCache, CachedJudge,
                 freeze_queries, lock_parameters, verify_frozen, rank_normalize,
                 relatedness, score_entities, weighted_kappa, kendall_tau)
from ufi.score import aggregate_to_class, prior

TODAY = date(2026, 10, 11)
STRUCT = Provenance("reg", SourceClass.STRUCTURE, TODAY, "f.csv")
COVER = Provenance("crawl", SourceClass.COVERAGE, TODAY, "f.csv")


# ----------------------------------------------------------------- ontology
MINIMAL = {
    "name": "t", "version": "1", "core_classes": ["A"],
    "classes": {"Thing": {}, "A": {"parent": "Thing"}, "B": {"parent": "Thing"}},
    "properties": {"rel": {"domain": "A", "range": "B"}},
    "competency_questions": [
        {"id": "q1", "template": "what b for {e}", "relation": "rel",
         "pattern": "lookup", "verbalizations": ["b of {e}", "{e} b", "what b {e}"]}],
}


def test_ontology_rejects_undefined_parent():
    spec = {**MINIMAL, "classes": {"A": {"parent": "Ghost"}}}
    with pytest.raises(OntologyError, match="Ghost"):
        Ontology.from_dict(spec).validate()


def test_ontology_rejects_empty_core_classes():
    spec = {**MINIMAL, "core_classes": []}
    with pytest.raises(OntologyError, match="teleport"):
        Ontology.from_dict(spec).validate()


def test_disjoint_without_covering_axiom_is_reported():
    spec = {**MINIMAL, "classes": {
        "Thing": {}, "A": {"parent": "Thing", "disjoint_with": ["B"]},
        "B": {"parent": "Thing", "disjoint_with": ["A"]}}}
    problems = Ontology.from_dict(spec).validate(strict=False)
    assert any("covering axiom" in p for p in problems)


def test_equivalent_property_on_specialised_domain_is_reported():
    """The entailment trap: equivalence plus a narrow domain types the world."""
    spec = {**MINIMAL, "properties": {
        "rel": {"domain": "A", "range": "B",
                "align": {"owl:equivalentProperty": "wdt:P131"}}}}
    problems = Ontology.from_dict(spec).validate(strict=False)
    assert any("equivalentProperty" in p and "entail" in p for p in problems)


def test_inverse_question_attaches_to_range_not_domain():
    spec = {**MINIMAL, "competency_questions": [
        {"id": "q1", "template": "which a for {e}", "relation": "rel",
         "pattern": "inverse", "verbalizations": ["x", "y", "z"]}]}
    o = Ontology.from_dict(spec)
    assert [q.id for q in o.questions_for_class("B")] == ["q1"]
    assert o.questions_for_class("A") == []


def test_owl_and_shacl_export_are_non_empty():
    o = Ontology.from_dict(MINIMAL)
    assert "Declaration(Class(:A))" in o.to_owl()
    spec = {**MINIMAL, "properties": {
        "rel": {"domain": "A", "range": "B", "min_cardinality": 1}}}
    assert "sh:minCount 1" in Ontology.from_dict(spec).to_shacl()


# -------------------------------------------------------------------- graph
def test_triple_without_provenance_is_refused():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "A"))
    g.add_entity(Entity("b", "B"))
    bad = Provenance("", SourceClass.STRUCTURE, TODAY)
    with pytest.raises(ProvenanceError):
        g.add_triple(Triple("a", "rel", "b", bad))


def test_structure_subgraph_excludes_coverage_evidence():
    """The separation the whole design rests on."""
    g = KnowledgeGraph()
    for i in "abc":
        g.add_entity(Entity(i, "A"))
    g.add_triple(Triple("a", "rel", "b", STRUCT))
    g.add_triple(Triple("a", "mentions", "c", COVER))
    sub = g.structure_subgraph()
    assert sub.has_edge("a", "b")
    assert not sub.has_edge("a", "c")


def test_structure_subgraph_drops_type_edges_and_literals():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "A"))
    g.add_entity(Entity("b", "B"))
    g.add_triple(Triple("a", "rdf:type", "b", STRUCT))
    g.add_triple(Triple("a", "label", "lit:hello", STRUCT))
    assert g.structure_subgraph().number_of_edges() == 0


def test_source_report_counts_every_source():
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "A"))
    g.add_entity(Entity("b", "B"))
    g.add_triple(Triple("a", "rel", "b", STRUCT))
    g.add_triple(Triple("a", "seen", "b", COVER))
    rows = {r["source_id"]: r for r in g.source_report()}
    assert rows["reg"]["triples"] == 1 and rows["crawl"]["triples"] == 1


# -------------------------------------------------------------------- score
def test_rank_normalize_spans_the_unit_interval_and_shares_ties():
    out = rank_normalize({"a": 10, "b": 5, "c": 5, "d": 1})
    assert out["a"] == 1.0 and out["d"] == 0.0 and out["b"] == out["c"]


def test_rank_normalize_single_item():
    assert rank_normalize({"a": 7}) == {"a": 1.0}


def test_relatedness_refuses_an_empty_teleport_set():
    """A silent fallback to uniform teleport computes plain centrality."""
    g = KnowledgeGraph()
    g.add_entity(Entity("a", "A"))
    g.add_entity(Entity("b", "A"))
    g.add_triple(Triple("a", "rel", "b", STRUCT))
    with pytest.raises(ValueError, match="teleport set is empty"):
        relatedness(g.structure_subgraph(), core_nodes=["nonexistent"])


def test_prior_discounts_rather_than_eliminates_zero_demand():
    p = prior({"a": 1.0}, {"a": 0.0}, beta=0.5)
    assert p["a"] == pytest.approx(0.5)


def test_beta_one_is_the_structure_only_ablation():
    p = prior({"a": 0.8}, {"a": 0.1}, beta=1.0)
    assert p["a"] == pytest.approx(0.8)


def test_own_coverage_of_one_zeroes_the_score():
    s = score_entities(["a"], {"a": 1.0}, {"a": 1.0}, {"a": 1.0}, {"a": 0.0},
                       {"a": {"q": 0.0}})
    assert s[0].cgs == 0.0


def test_full_coverage_and_full_answerability_zero_the_deficit():
    s = score_entities(["a"], {"a": 1.0}, {"a": 1.0}, {"a": 0.0}, {"a": 1.0},
                       {"a": {"q": 1.0}})
    assert s[0].cgs == pytest.approx(0.0)


def test_instance_and_schema_gaps_are_reported_separately():
    s = score_entities(["a"], {"a": 1.0}, {"a": 1.0}, {"a": 0.0}, {"a": 1.0},
                       {"a": {"q": 0.0}}, Parameters(alpha=0.5, beta=0.5))[0]
    assert s.instance_gap == pytest.approx(0.0)
    assert s.schema_gap == pytest.approx(1.0)
    assert s.cgs == pytest.approx(0.5)


def test_alpha_moves_weight_between_the_two_deficits():
    args = (["a"], {"a": 1.0}, {"a": 1.0}, {"a": 0.0}, {"a": 1.0}, {"a": {"q": 0.0}})
    lo = score_entities(*args, Parameters(alpha=0.0))[0].cgs
    hi = score_entities(*args, Parameters(alpha=1.0))[0].cgs
    assert lo == pytest.approx(1.0) and hi == pytest.approx(0.0)


def test_parameters_reject_out_of_range():
    with pytest.raises(ValueError, match="alpha"):
        Parameters(alpha=1.5).validate()


def test_class_aggregate_reports_mean_and_sum():
    scores = score_entities(["a", "b"], {"a": 1.0, "b": 0.0}, {"a": 1.0, "b": 0.0},
                            {"a": 0.0, "b": 0.0}, {"a": 0.0, "b": 0.0},
                            {"a": {"q": 0.0}, "b": {"q": 0.0}})
    rows = aggregate_to_class(scores, {"a": "A", "b": "A"})
    assert rows[0]["n"] == 2
    assert rows[0]["sum_cgs"] == pytest.approx(2 * rows[0]["mean_cgs"])


def test_kendall_tau_bounds():
    assert kendall_tau(["a", "b", "c"], ["a", "b", "c"]) == pytest.approx(1.0)
    assert kendall_tau(["a", "b", "c"], ["c", "b", "a"]) == pytest.approx(-1.0)


# -------------------------------------------------------------------- demand
def test_alias_linker_respects_word_boundaries():
    linker = AliasLinker({"npa:404": ["404"], "npa:40": ["40"]})
    assert linker.link("who called from 404") == ["npa:404"]


def test_coverage_report_lists_surfaces_that_produced_nothing():
    idx = DemandIndex()
    idx.declare("forum", "video_short")
    idx.ingest([DemandRecord("who called from 404", "forum", "s", TODAY)],
               AliasLinker({"npa:404": ["404"]}))
    rows = {r["surface"]: r for r in idx.coverage_report()}
    assert rows["forum"]["status"] == "read"
    assert rows["video_short"]["status"] == "declared, no rows"
    assert rows["social_group"]["status"] == "not collected"


def test_first_party_share_is_zero_for_tool_derived_demand_only():
    idx = DemandIndex()
    idx.ingest([DemandRecord("404 area code", "keyword_export", "s", TODAY)],
               AliasLinker({"npa:404": ["404"]}))
    assert idx.first_party_share() == 0.0


# --------------------------------------------------------------- judge/cache
def test_cache_returns_the_same_grade_without_calling_the_judge(tmp_path):
    cache = JudgmentCache(tmp_path / "j.json")
    cj = CachedJudge(RuleJudge(), cache)
    a = cj.grade("q", "404 serves Atlanta", "rubric")
    b = cj.grade("q", "404 serves Atlanta", "rubric")
    assert a.grade == b.grade and cj.calls == 1 and cj.hits == 1


def test_changing_the_rubric_misses_the_cache(tmp_path):
    """Grades from two rubrics must never silently mix."""
    cache = JudgmentCache(tmp_path / "j.json")
    cj = CachedJudge(RuleJudge(), cache)
    cj.grade("q", "evidence 1", "rubric A")
    cj.grade("q", "evidence 1", "rubric B")
    assert cj.calls == 2


def test_cache_fingerprint_ignores_timestamps_but_tracks_grades(tmp_path):
    cache = JudgmentCache(tmp_path / "j.json")
    CachedJudge(RuleJudge(), cache).grade("q", "404 serves Atlanta", "r")
    first = cache.fingerprint()
    cache.save()
    reloaded = JudgmentCache(tmp_path / "j.json")
    assert reloaded.fingerprint() == first


def test_weighted_kappa_known_values():
    assert weighted_kappa([0, 0.5, 1], [0, 0.5, 1]) == pytest.approx(1.0)
    assert weighted_kappa([0, 0, 1, 1], [1, 1, 0, 0]) == pytest.approx(-1.0)


def test_rule_judge_grades_specificity():
    j = RuleJudge()
    assert float(j.grade("k", "p", "", "r").grade) == 0.0
    assert float(j.grade("k", "p", "area code 404 serves Atlanta", "r").grade) == 1.0
    assert float(j.grade("k", "p", "mentioned", "r").grade) == 0.0


# ---------------------------------------------------------------- provenance
def test_freeze_refuses_to_overwrite(tmp_path):
    p = tmp_path / "q.json"
    freeze_queries(["b", "a"], p)
    with pytest.raises(FileExistsError):
        freeze_queries(["c"], p)


def test_freeze_is_order_independent_and_verifiable(tmp_path):
    i1 = freeze_queries(["b", "a"], tmp_path / "1.json")
    i2 = freeze_queries(["a", "b"], tmp_path / "2.json")
    assert i1["hash"] == i2["hash"]
    assert verify_frozen(tmp_path / "1.json")["intact"]


def test_tampering_with_a_frozen_set_is_detected(tmp_path):
    p = tmp_path / "q.json"
    freeze_queries(["a", "b"], p)
    payload = json.loads(p.read_text())
    payload["queries"].append("c")
    p.write_text(json.dumps(payload))
    assert verify_frozen(p)["intact"] is False


def test_parameters_lock_is_write_once(tmp_path):
    p = tmp_path / "lock.json"
    lock_parameters(Parameters(), p)
    with pytest.raises(FileExistsError):
        lock_parameters(Parameters(alpha=0.9), p)


# ------------------------------------------------- defects found in review
def test_provenance_locator_must_not_repeat_the_source_id():
    with pytest.raises(ValueError, match="identical to source_id"):
        Provenance("nanpa", SourceClass.STRUCTURE, TODAY, "nanpa")


def test_owl_export_carries_property_alignments():
    """The alignment corrections are the point; they must reach the file."""
    spec = {**MINIMAL, "properties": {
        "rel": {"domain": "A", "range": "B",
                "align": {"rdfs:subPropertyOf": "http://example.org/p"}}}}
    owl = Ontology.from_dict(spec).to_owl()
    assert "rdfs:subPropertyOf" in owl and "http://example.org/p" in owl


def test_owl_export_emits_no_bare_name_where_an_iri_is_required():
    import re
    spec = {**MINIMAL, "classes": {**MINIMAL["classes"], "R": {}},
            "properties": {"rel": {"domain": "A", "range": "ext:Organization"}}}
    owl = Ontology.from_dict(spec).to_owl()
    bare = re.findall(r"PropertyRange\(:\w+ ([A-Za-z_]\w*)\)", owl)
    assert bare == [], f"bare names are not IRIs: {bare}"


def test_data_properties_are_declared_as_data_properties():
    spec = {**MINIMAL, "properties": {
        "rel": {"domain": "A", "range": "B"},
        "nxx": {"domain": "A", "range": "xsd:string"}}}
    owl = Ontology.from_dict(spec).to_owl()
    assert "Declaration(DataProperty(:nxx))" in owl
    assert "Declaration(ObjectProperty(:rel))" in owl


def test_has_key_is_emitted_for_an_identity_criterion():
    spec = {**MINIMAL, "classes": {**MINIMAL["classes"],
                                   "A": {"parent": "Thing", "key": ["rel"]}}}
    assert "HasKey(:A" in Ontology.from_dict(spec).to_owl()


def test_symmetric_and_asymmetric_together_is_fatal():
    spec = {**MINIMAL, "properties": {
        "rel": {"domain": "A", "range": "B", "symmetric": True,
                "asymmetric": True}}}
    with pytest.raises(OntologyError, match="symmetric and asymmetric"):
        Ontology.from_dict(spec).validate()


def test_synthetic_records_do_not_count_as_first_party_voice():
    """A generated record labelled 'forum' is not a user's own words."""
    idx = DemandIndex()
    idx.ingest([DemandRecord("who called from 404", "forum", "demo", TODAY,
                             synthetic=True)],
               AliasLinker({"npa:404": ["404"]}))
    assert idx.first_party_share() == 0.0
    assert idx.synthetic_share() == 1.0


def test_real_records_do_count_as_first_party_voice():
    idx = DemandIndex()
    idx.ingest([DemandRecord("who called from 404", "forum", "reddit", TODAY)],
               AliasLinker({"npa:404": ["404"]}))
    assert idx.first_party_share() == 1.0
    assert idx.synthetic_share() == 0.0


def test_cached_judgment_records_what_was_judged(tmp_path):
    """A cache of anonymous grades cannot be re-graded or traced."""
    cache = JudgmentCache(tmp_path / "j.json")
    cj = CachedJudge(RuleJudge(), cache)
    j = cj.grade("area code 404 time zone", "404 is in America/New_York", "r",
                 subject="npa:404", rubric_id="answerability-v1")
    assert j.subject == "npa:404"
    assert j.question == "area code 404 time zone"
    assert j.rubric_id == "answerability-v1"
    assert j.evidence_digest


def test_agreement_reports_overlap_and_kappa(tmp_path):
    from ufi.judge import agreement
    a, b = JudgmentCache(tmp_path / "a.json"), JudgmentCache(tmp_path / "b.json")
    for cache in (a, b):
        CachedJudge(RuleJudge(), cache).grade("q", "404 serves Atlanta", "r")
    out = agreement(a, b)
    assert out["n"] == 1 and out["kappa"] == pytest.approx(1.0)


def test_agreement_on_disjoint_caches_says_so(tmp_path):
    from ufi.judge import agreement
    a, b = JudgmentCache(tmp_path / "a.json"), JudgmentCache(tmp_path / "b.json")
    CachedJudge(RuleJudge(), a).grade("q1", "evidence one", "r")
    CachedJudge(RuleJudge(), b).grade("q2", "evidence two", "r")
    assert agreement(a, b)["n"] == 0


def test_kendall_tau_b_handles_ties():
    from ufi.score import kendall_tau_scores
    # tau-a would divide by the untied pair count and overstate disagreement.
    assert kendall_tau_scores({"a": 1, "b": 1, "c": 0},
                              {"a": 1, "b": 1, "c": 0}) == pytest.approx(1.0)


# ----------------------------------------------------------------- RDF path
rdf = pytest.importorskip("ufi.rdf", reason="RDF extras not installed")


def _nanp():
    root = Path(__file__).resolve().parent.parent / "examples" / "nanp"
    return Ontology.from_yaml(root / "ontology.yaml"), root


def test_rdf_export_parses_as_turtle():
    onto, _ = _nanp()
    import rdflib
    ttl = rdf.to_rdf(onto).serialize(format="turtle")
    assert len(rdflib.Graph().parse(data=ttl, format="turtle")) > 0


def test_rdf_export_carries_the_property_alignments():
    onto, _ = _nanp()
    ttl = rdf.to_rdf(onto).serialize(format="turtle")
    assert "P131" in ttl and "P421" in ttl


def test_shacl_over_an_empty_abox_is_reported_as_vacuous():
    """An empty run conforms trivially and must not read as a clean one."""
    onto, _ = _nanp()
    out = rdf.validate(onto, KnowledgeGraph())
    assert out["vacuous"] is True
    assert out["conforms"] is False
    assert "checked nothing" in out["note"]


def test_reasoner_derives_the_class_rather_than_reading_it(tmp_path):
    """If deleting the ontology changes no type, the ontology is decorative."""
    onto, _ = _nanp()
    kg = KnowledgeGraph()
    kg.add_entity(Entity("npa:404", "AreaCode", label="404"))
    kg.add_entity(Entity("npa:800", "AreaCode", label="800"))
    kg.add_entity(Entity("place:Atlanta", "Place", label="Atlanta"))
    kg.add_triple(Triple("npa:404", "locatedIn", "place:Atlanta",
                         Provenance("reg", SourceClass.STRUCTURE, TODAY, "r:1")))
    out = rdf.materialize(onto, kg)
    assert out["consistent"] and out["reclassified"] == 1
    assert kg.entities["npa:404"].cls == "GeographicAreaCode"
    assert kg.entities["npa:800"].cls == "AreaCode"

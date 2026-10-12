"""ufi: content gap scoring from industry structure and user questions.

A reference implementation of the Content Gap Score and of the artifacts a
study of it has to publish: a frozen query set, a parameter lock, an auditable
judgment cache and a run manifest whose digest is stable across runs.

The score itself is a specification, not a validated instrument. No published
study has yet tested whether it predicts anything. Treat it accordingly.

Quick start:

    from ufi import Ontology, KnowledgeGraph, DemandIndex, GapRun, Parameters

    onto = Ontology.from_yaml("ontology.yaml")
    print(onto.validate(strict=False))     # problems before you score anything

See `examples/nanp` for a complete run on public data.
"""
__version__ = "0.1.0"

from .types import (CompetencyQuestion, Entity, Grade, Judgment, Provenance,
                    SourceClass, Triple)
from .ontology import ClassSpec, Ontology, OntologyError, PropertySpec
from .graph import KnowledgeGraph, ProvenanceError
from .demand import (AliasLinker, CsvAdapter, DemandAdapter, DemandIndex,
                     DemandRecord, JsonLinesAdapter, DESIGNED_SURFACES,
                     FIRST_PARTY_VOICE, TOOL_DERIVED)
from .judge import (CachedJudge, Judge, JudgmentCache, CallableJudge, RuleJudge,
                    agreement, bootstrap_ci, weighted_kappa)
from .score import (EntityScore, Parameters, aggregate_to_class, demand,
                    kendall_tau, kendall_tau_scores, prior, rank_normalize,
                    relatedness, schema_gap_by_relation, score_entities,
                    top_k_overlap)
from .baselines import (b1_volume, b2_competitor_gap, b3_question_mining,
                        b4_latent_internal, compare_rankings)
from .provenance import RunManifest, freeze_queries, lock_parameters, verify_frozen
from .pipeline import GapRun

__all__ = [n for n in dir() if not n.startswith("_")]

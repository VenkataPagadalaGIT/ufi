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

__version__ = "0.2.0"

from .baselines import (
    b1_volume,
    b2_competitor_gap,
    b3_question_mining,
    b4_latent_internal,
    compare_rankings,
)
from .demand import (
    DESIGNED_SURFACES,
    FIRST_PARTY_VOICE,
    TOOL_DERIVED,
    AliasLinker,
    CsvAdapter,
    DemandAdapter,
    DemandIndex,
    DemandRecord,
    JsonLinesAdapter,
)
from .graph import KnowledgeGraph, ProvenanceError
from .judge import (
    CachedJudge,
    CallableJudge,
    Judge,
    JudgmentCache,
    RuleJudge,
    agreement,
    bootstrap_ci,
    weighted_kappa,
)
from .ontology import ClassSpec, Ontology, OntologyError, PropertySpec
from .pipeline import GapRun
from .provenance import RunManifest, freeze_queries, lock_parameters, verify_frozen
from .score import (
    EntityScore,
    Parameters,
    aggregate_to_class,
    demand,
    kendall_tau,
    kendall_tau_scores,
    prior,
    rank_normalize,
    relatedness,
    schema_gap_by_relation,
    score_entities,
    top_k_overlap,
)
from .types import (
    CompetencyQuestion,
    Entity,
    Grade,
    Judgment,
    Provenance,
    SourceClass,
    Triple,
)

__all__ = [
    "DESIGNED_SURFACES",
    "FIRST_PARTY_VOICE",
    "TOOL_DERIVED",
    "AliasLinker",
    "CachedJudge",
    "CallableJudge",
    "ClassSpec",
    "CompetencyQuestion",
    "CsvAdapter",
    "DemandAdapter",
    "DemandIndex",
    "DemandRecord",
    "Entity",
    "EntityScore",
    "GapRun",
    "Grade",
    "JsonLinesAdapter",
    "Judge",
    "Judgment",
    "JudgmentCache",
    "KnowledgeGraph",
    "Ontology",
    "OntologyError",
    "Parameters",
    "PropertySpec",
    "Provenance",
    "ProvenanceError",
    "RuleJudge",
    "RunManifest",
    "SourceClass",
    "Triple",
    "aggregate_to_class",
    "agreement",
    "b1_volume",
    "b2_competitor_gap",
    "b3_question_mining",
    "b4_latent_internal",
    "bootstrap_ci",
    "compare_rankings",
    "demand",
    "freeze_queries",
    "kendall_tau",
    "kendall_tau_scores",
    "lock_parameters",
    "prior",
    "rank_normalize",
    "relatedness",
    "schema_gap_by_relation",
    "score_entities",
    "top_k_overlap",
    "verify_frozen",
    "weighted_kappa",
]

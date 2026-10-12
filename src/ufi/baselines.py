"""The practitioner baselines, computed on the same candidate list as CGS.

A comparison between a new score and "what practitioners do" is only meaningful
if both are computed over the same candidates and aggregated to the same unit
with the same operator. Volume in particular is sensitive to pooling: a topic
fragmented across hundreds of entity-specific phrasings ranks low per keyword
and high per class, so B1 is reported at three poolings and the deployment says
which one its practice used rather than choosing the flattering one.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .score import rank_normalize


@dataclass
class BaselineResult:
    name: str
    description: str
    per_entity: dict[str, float]
    note: str = ""


def b1_volume(
    volumes: Mapping[str, float],
    pooling: str = "entity",
    cluster_of: Mapping[str, str] | None = None,
) -> BaselineResult:
    """Reported search volume. `pooling` in {entity, cluster, class}.

    Pooling is the whole argument of this baseline. Reported at all three, the
    baseline usually agrees with the new score at class level and disagrees at
    keyword level, which is a finding about pooling rather than about volume.
    """
    if pooling == "entity" or not cluster_of:
        return BaselineResult(
            "B1-volume-entity",
            "reported volume per entity",
            rank_normalize(volumes),
            f"pooling={pooling}",
        )
    pooled: dict[str, float] = defaultdict(float)
    for e, v in volumes.items():
        pooled[cluster_of.get(e, e)] += v
    per_entity = {e: pooled[cluster_of.get(e, e)] for e in volumes}
    return BaselineResult(
        f"B1-volume-{pooling}",
        f"reported volume summed to {pooling}",
        rank_normalize(per_entity),
        f"pooling={pooling}",
    )


def b2_competitor_gap(
    competitor_ranked: Mapping[str, float], own_ranked: Mapping[str, float]
) -> BaselineResult:
    """Keywords a competitor ranks for and the organization does not.

    Structurally cannot propose an entity no competitor ranks for: its score is
    zero there by construction. That is the limitation to report, not a defect
    of the implementation.
    """
    out = {
        e: max(0.0, competitor_ranked.get(e, 0.0) - own_ranked.get(e, 0.0))
        for e in set(competitor_ranked) | set(own_ranked)
    }
    unreachable = sum(1 for e, v in competitor_ranked.items() if v == 0.0)
    return BaselineResult(
        "B2-competitor-gap",
        "competitor ranks, we do not",
        rank_normalize(out),
        f"{unreachable} candidates are invisible to this baseline by construction",
    )


def b3_question_mining(question_counts: Mapping[str, float]) -> BaselineResult:
    """Count of mined user questions, with no structural prior."""
    return BaselineResult(
        "B3-question-mining", "mined question volume", rank_normalize(question_counts)
    )


def b4_latent_internal(
    impressions: Mapping[str, float], position: Mapping[str, float], min_position: float = 11.0
) -> BaselineResult:
    """Queries the organization already earns impressions for but ranks poorly on.

    The internal-analytics baseline. Only defined where analytics exist, which
    is the reason a deployment without Search Console access cannot report it.
    """
    out = {
        e: (impressions.get(e, 0.0) if position.get(e, 999) >= min_position else 0.0)
        for e in impressions
    }
    return BaselineResult(
        "B4-latent-internal", f"impressions where position >= {min_position}", rank_normalize(out)
    )


def compare_rankings(
    cgs_rank: Sequence[str], baselines: Sequence[BaselineResult], ks: Sequence[int] = (5, 10, 20)
) -> list[dict]:
    """Kendall tau and top-k overlap between CGS and each baseline."""
    from .score import kendall_tau, top_k_overlap

    rows = []
    for b in baselines:
        order = [e for e, _ in sorted(b.per_entity.items(), key=lambda kv: -kv[1])]
        row = {"baseline": b.name, "tau": round(kendall_tau(cgs_rank, order), 4)}
        for k in ks:
            row[f"overlap@{k}"] = round(top_k_overlap(cgs_rank, order, k), 4)
        row["note"] = b.note
        rows.append(row)
    return rows

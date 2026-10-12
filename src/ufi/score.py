"""The Content Gap Score and its components.

CGS(e) = prior(e) * (1 - own(e)) * [ a*(1 - cov_K(e)) + (1-a)*mean_q(1 - ans(q,e)) ]
prior(e) = b*rel(e) + (1-b)*dem(e)

Two implementation choices are load-bearing and are documented here rather than
in a comment inside the arithmetic.

`rel` is rank-normalized, not min-max normalized. Topic-sensitive PageRank mass
is heavy-tailed: under min-max normalization almost every entity scores near
zero and the product collapses to a centrality ranking of the top few nodes.
Rank normalization keeps the prior informative across the whole candidate list,
at the cost of discarding the magnitude of the centrality difference, which is
the right trade when the score is used to rank rather than to measure.

The deficit bracket is a weighted sum of two terms that are both in [0,1], so
alpha moves weight between "no competitor covers this" and "the web does not
answer this". It does not switch between two kinds of gap: an entity can score
high on both, and `instance_gap` / `schema_gap` are reported separately by
`score_entities` so a reader can see which term carried the score.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence

import networkx as nx

from .types import Grade


# --------------------------------------------------------------------- parts
def rank_normalize(values: Mapping[str, float], higher_is_better: bool = True
                   ) -> dict[str, float]:
    """Map values to [0,1] by rank. Ties share the mean of their ranks.

    The top entity scores 1.0 and the bottom 0.0; with a single entity the
    result is 1.0.
    """
    items = sorted(values.items(), key=lambda kv: kv[1], reverse=higher_is_better)
    n = len(items)
    if n == 0:
        return {}
    if n == 1:
        return {items[0][0]: 1.0}
    # average ranks within ties
    out: dict[str, float] = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        mean_rank = (i + j) / 2.0
        for k in range(i, j + 1):
            out[items[k][0]] = 1.0 - mean_rank / (n - 1)
        i = j + 1
    return out


def relatedness(structure_graph: nx.Graph, core_nodes: Sequence[str],
                damping: float = 0.85, tol: float = 1e-8,
                max_iter: int = 200) -> dict[str, float]:
    """Topic-sensitive PageRank over the structure graph, rank-normalized.

    `core_nodes` is the teleport set S: the instances of the ontology's core
    classes, fixed before scoring. An empty or absent S is an error rather than
    a silent fallback to uniform teleport, because uniform teleport computes a
    different quantity (plain centrality) under the same name.
    """
    nodes = list(structure_graph.nodes)
    if not nodes:
        return {}
    present = [n for n in core_nodes if n in structure_graph]
    if not present:
        raise ValueError(
            "none of the core-class instances are present in the structure graph, "
            "so the teleport set is empty. Either the entity layer was not "
            "populated, or the core classes name classes with no instances. "
            "Relatedness is undefined in both cases.")
    personalization = {n: (1.0 / len(present) if n in set(present) else 0.0) for n in nodes}
    pr = nx.pagerank(structure_graph, alpha=damping, personalization=personalization,
                     tol=tol, max_iter=max_iter)
    return rank_normalize(pr)


def demand(counts: Mapping[str, float]) -> dict[str, float]:
    """Rank-normalized count of linked user questions."""
    return rank_normalize(counts)


def prior(rel: Mapping[str, float], dem: Mapping[str, float], beta: float
          ) -> dict[str, float]:
    """beta weights structure against demand. beta=1 is the structure-only ablation.

    Combined arithmetically so an entity with no observed questions is
    discounted rather than eliminated; a geometric mean would zero it.
    """
    keys = set(rel) | set(dem)
    return {k: beta * rel.get(k, 0.0) + (1.0 - beta) * dem.get(k, 0.0) for k in keys}


# -------------------------------------------------------------------- result
@dataclass
class EntityScore:
    entity: str
    cgs: float
    prior: float
    rel: float
    dem: float
    own: float
    cov_k: float
    mean_ans: float
    instance_gap: float
    schema_gap: float
    n_questions: int

    def as_row(self) -> dict:
        return {
            "entity": self.entity, "cgs": round(self.cgs, 6),
            "prior": round(self.prior, 6), "rel": round(self.rel, 6),
            "dem": round(self.dem, 6), "own": self.own, "cov_k": round(self.cov_k, 4),
            "mean_ans": round(self.mean_ans, 4),
            "instance_gap": round(self.instance_gap, 6),
            "schema_gap": round(self.schema_gap, 6), "n_questions": self.n_questions,
        }


@dataclass(frozen=True)
class Parameters:
    """Every free parameter in one object, so it can be locked and hashed."""

    alpha: float = 0.5
    beta: float = 0.5
    damping: float = 0.85
    min_verbalizations: int = 3
    class_aggregate: str = "mean"      # mean is primary; sum is reported alongside

    def validate(self) -> None:
        for n, v in (("alpha", self.alpha), ("beta", self.beta),
                     ("damping", self.damping)):
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"{n} must be in [0,1], got {v}")
        if self.class_aggregate not in ("mean", "sum"):
            raise ValueError("class_aggregate must be 'mean' or 'sum'")


def score_entities(entities: Sequence[str], rel: Mapping[str, float],
                   dem: Mapping[str, float], own: Mapping[str, float],
                   cov_k: Mapping[str, float],
                   ans: Mapping[str, Mapping[str, float]],
                   params: Parameters = Parameters()) -> list[EntityScore]:
    """Score every entity. `ans` maps entity -> {question_id: grade}."""
    params.validate()
    pri = prior(rel, dem, params.beta)
    out: list[EntityScore] = []
    for e in entities:
        a = ans.get(e, {})
        mean_ans = sum(a.values()) / len(a) if a else 0.0
        inst = 1.0 - cov_k.get(e, 0.0)
        schema = 1.0 - mean_ans
        deficit = params.alpha * inst + (1.0 - params.alpha) * schema
        p = pri.get(e, 0.0)
        o = own.get(e, 0.0)
        out.append(EntityScore(
            entity=e, cgs=p * (1.0 - o) * deficit, prior=p,
            rel=rel.get(e, 0.0), dem=dem.get(e, 0.0), own=o,
            cov_k=cov_k.get(e, 0.0), mean_ans=mean_ans,
            instance_gap=p * (1.0 - o) * inst, schema_gap=p * (1.0 - o) * schema,
            n_questions=len(a)))
    return sorted(out, key=lambda s: (-s.cgs, s.entity))


def schema_gap_by_relation(entities_by_relation: Mapping[str, Sequence[str]],
                           rel: Mapping[str, float], dem: Mapping[str, float],
                           own: Mapping[str, float],
                           ans_by_relation: Mapping[str, Mapping[str, float]],
                           params: Parameters = Parameters()) -> dict[str, float]:
    """SG(r): the relation-level gap, which is the claim 'no one answers X'."""
    pri = prior(rel, dem, params.beta)
    out: dict[str, float] = {}
    for r, ents in entities_by_relation.items():
        if not ents:
            out[r] = 0.0
            continue
        grades = ans_by_relation.get(r, {})
        out[r] = sum(pri.get(e, 0.0) * (1.0 - own.get(e, 0.0)) *
                     (1.0 - grades.get(e, 0.0)) for e in ents) / len(ents)
    return out


def aggregate_to_class(scores: Sequence[EntityScore],
                       class_of: Mapping[str, str]) -> list[dict]:
    """Class-level ranking. Mean is primary; sum and size are reported with it.

    The sum favours large enumerable classes by construction, which is exactly
    the bias a content programme is tempted by, so both are printed and the
    reader can see the effect of class size instead of trusting one operator.
    """
    buckets: dict[str, list[EntityScore]] = {}
    for s in scores:
        buckets.setdefault(class_of.get(s.entity, "?"), []).append(s)
    rows = []
    for cls, ss in buckets.items():
        n = len(ss)
        tot = sum(s.cgs for s in ss)
        rows.append({
            "class": cls, "n": n, "mean_cgs": tot / n, "sum_cgs": tot,
            "mean_instance_gap": sum(s.instance_gap for s in ss) / n,
            "mean_schema_gap": sum(s.schema_gap for s in ss) / n,
            "uncovered": sum(1 for s in ss if s.own == 0.0),
        })
    return sorted(rows, key=lambda r: -r["mean_cgs"])


def kendall_tau(a: Sequence[str], b: Sequence[str]) -> float:
    """Kendall's tau-b over two rankings of the same items.

    tau-b rather than tau-a because these rankings are heavily tied: whole
    blocks of entities share a rank-normalized score, and tau-a divides by the
    untied pair count, which understates agreement in exactly the case this
    function is used for. With no ties the two coincide.
    """
    return kendall_tau_scores({x: -i for i, x in enumerate(a)},
                              {x: -i for i, x in enumerate(b)})


def kendall_tau_scores(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    """tau-b between two score maps over their shared keys."""
    keys = sorted(set(a) & set(b))
    n = len(keys)
    if n < 2:
        return float("nan")
    conc = disc = tie_a = tie_b = 0
    for i in range(n):
        for j in range(i + 1, n):
            x, y = keys[i], keys[j]
            da, db = a[x] - a[y], b[x] - b[y]
            if da == 0 and db == 0:
                tie_a += 1
                tie_b += 1
            elif da == 0:
                tie_a += 1
            elif db == 0:
                tie_b += 1
            elif da * db > 0:
                conc += 1
            else:
                disc += 1
    n0 = n * (n - 1) / 2
    den = ((n0 - tie_a) * (n0 - tie_b)) ** 0.5
    return (conc - disc) / den if den else float("nan")


def top_k_overlap(a: Sequence[str], b: Sequence[str], k: int) -> float:
    return len(set(a[:k]) & set(b[:k])) / k if k else float("nan")

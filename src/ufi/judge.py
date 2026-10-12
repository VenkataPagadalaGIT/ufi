"""Graders for the three subjective inputs, with judgments cached to disk.

`own`, `cov_K` and `ans` are judgments, not measurements. Three consequences are
built into this module rather than left to the deployment:

1. Every judgment is cached under a key derived from the rubric, the prompt and
   the evidence, so a rerun of the pipeline is deterministic and costs nothing.
   A paper that releases its cache lets a reader recompute every score without
   access to a model or to the pages as they were on the day.
2. The rubric is a literal string in the cache key. Change the rubric and the
   cache misses, which prevents a silent mixture of grades from two rubrics.
3. `agreement()` computes weighted Cohen's kappa against a second judge, so the
   reliability statistic the reader will ask for is produced by the same tool
   that produced the grades.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from .types import Grade, Judgment, stable_hash

#: The three-level rubrics. Stated once, hashed into every cache key, and
#: identified by name in every cached row so two rubrics cannot be confused
#: after the fact.
RUBRIC_IDS = {"coverage": "coverage-v1", "answerability": "answerability-v1"}
RUBRIC_COVERAGE = (
    "Grade the page set for entity E on this scale. "
    "1.0 = a dedicated page about E that answers the question directly. "
    "0.5 = E appears on a list or section page with at least one specific fact. "
    "0.0 = E is absent, or appears as a bare mention with no fact."
)
RUBRIC_ANSWERABILITY = (
    "Grade whether the retrieved result answers the question correctly and "
    "directly, judged on the page text alone. "
    "1.0 = the answer is present, correct and immediate. "
    "0.5 = the answer is derivable but requires the reader to combine facts or "
    "scroll past unrelated content. "
    "0.0 = the answer is absent or wrong."
)


class Judge(ABC):
    """Grades one (key, prompt, evidence) triple on the three-level rubric."""

    judge_id: str = "abstract"
    model: str = ""

    @abstractmethod
    def grade(self, key: str, prompt: str, evidence: str, rubric: str) -> Judgment: ...


class CallableJudge(Judge):
    """Wraps any function of (prompt, evidence, rubric) -> float or Grade.

    This is the seam for a model call. The package does not ship a model client:
    a deployment supplies one, and the cache below makes the call happen once.
    """

    def __init__(self, fn: Callable[[str, str, str], float], judge_id: str, model: str = ""):
        self.fn = fn
        self.judge_id = judge_id
        self.model = model

    def grade(self, key: str, prompt: str, evidence: str, rubric: str) -> Judgment:
        raw = self.fn(prompt, evidence, rubric)
        g = raw if isinstance(raw, Grade) else _nearest_grade(float(raw))
        return Judgment(
            key=key, grade=g, judge_id=self.judge_id, model=self.model, judged=date.today()
        )


class RuleJudge(Judge):
    """A deterministic judge for tests, examples and offline reproduction.

    Grades by substring evidence: full credit when the expected answer string
    appears in the evidence, partial when any required token appears. It exists
    so the worked example in this package runs with no network and no key, and
    so a reader can reproduce every published number exactly.
    """

    judge_id = "rule"

    def __init__(
        self, expectations: dict[str, Sequence[str]] | None = None, specific_min_words: int = 4
    ):
        self.expectations = expectations or {}
        self.specific_min_words = specific_min_words

    def grade(self, key: str, prompt: str, evidence: str, rubric: str) -> Judgment:
        ev = (evidence or "").strip()
        if not ev:
            return Judgment(key, Grade.NONE, "no evidence", self.judge_id)
        want = [w.lower() for w in self.expectations.get(key, ())]
        low = ev.lower()
        if want:
            if all(w in low for w in want):
                return Judgment(key, Grade.FULL, "all required tokens present", self.judge_id)
            if any(w in low for w in want):
                return Judgment(key, Grade.PARTIAL, "some required tokens present", self.judge_id)
            return Judgment(key, Grade.NONE, "no required token present", self.judge_id)
        # No expectation registered: grade on specificity. Evidence that names a
        # concrete value (a number, or a phrase of several words) counts as a
        # direct answer; a bare mention counts as partial. This is the rule the
        # offline example runs on, and it is a heuristic, not a model.
        words = len(ev.split())
        has_value = any(c.isdigit() for c in ev)
        if words >= self.specific_min_words and has_value:
            return Judgment(key, Grade.FULL, "specific, names a value", self.judge_id)
        if words >= self.specific_min_words or has_value:
            return Judgment(key, Grade.PARTIAL, "present but not specific", self.judge_id)
        return Judgment(key, Grade.NONE, "bare mention", self.judge_id)


def _nearest_grade(x: float) -> Grade:
    return min((Grade.NONE, Grade.PARTIAL, Grade.FULL), key=lambda g: abs(float(g) - x))


class JudgmentCache:
    """Disk-backed cache of judgments, keyed by rubric + prompt + evidence.

    The cache file is a release artifact: publish it and every score in the
    paper recomputes without a model.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._data: dict[str, dict] = {}
        if self.path.exists():
            self._data = json.loads(self.path.read_text(encoding="utf-8"))

    @staticmethod
    def key(rubric: str, prompt: str, evidence: str) -> str:
        return stable_hash(rubric, prompt, evidence)

    def get(self, key: str) -> Judgment | None:
        row = self._data.get(key)
        if not row:
            return None
        return Judgment(
            key=key,
            grade=_nearest_grade(row["grade"]),
            rationale=row.get("rationale", ""),
            judge_id=row.get("judge_id", ""),
            model=row.get("model", ""),
            judged=date.fromisoformat(row["judged"]) if row.get("judged") else None,
        )

    def put(self, j: Judgment) -> None:
        self._data[j.key] = j.to_dict()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=1, sort_keys=True), encoding="utf-8")

    def __len__(self) -> int:
        return len(self._data)

    def fingerprint(self) -> str:
        """Digest of what affects the numbers: the key and the grade.

        Deliberately excludes the rationale, the judging date and the model
        string. Those belong in the cache for audit, but a judgment made on a
        different day by a differently-named client produces the same score,
        and a digest that changed with them would report a difference that does
        not exist. The full cache file is the audit record; this is the
        reproducibility check.
        """
        return stable_hash(sorted((k, round(float(v["grade"]), 6)) for k, v in self._data.items()))

    def audit_fingerprint(self) -> str:
        """Digest of the complete cache, including rationales and timestamps."""
        return stable_hash(
            sorted((k, tuple(sorted(v.items(), key=str))) for k, v in self._data.items())
        )


@dataclass
class CachedJudge:
    """A judge wrapped in a cache. Calls the inner judge only on a miss.

    Every cached row records what was judged, not only the grade. Without the
    subject and the question, a released cache cannot be re-graded by a second
    annotator and cannot be traced back to a published number, which are the
    two things a released cache is for.
    """

    inner: Judge
    cache: JudgmentCache
    calls: int = 0
    hits: int = 0

    def grade(
        self, prompt: str, evidence: str, rubric: str, subject: str = "", rubric_id: str = ""
    ) -> Judgment:
        k = self.cache.key(rubric, prompt, evidence)
        hit = self.cache.get(k)
        if hit is not None:
            self.hits += 1
            return hit
        j = self.inner.grade(k, prompt, evidence, rubric)
        j = replace(
            j,
            subject=subject,
            question=prompt,
            rubric_id=rubric_id or stable_hash(rubric)[:8],
            evidence_digest=stable_hash(evidence),
        )
        self.cache.put(j)
        self.calls += 1
        return j


def agreement(
    cache_a: JudgmentCache, cache_b: JudgmentCache, levels: Sequence[float] = (0.0, 0.5, 1.0)
) -> dict:
    """Compare two graders over the items they both judged.

    Takes two caches rather than two lists so that the comparison is made on
    keys, not on positions: two annotators who graded overlapping but different
    subsets still yield a defensible statistic over the intersection, and the
    size of that intersection is reported alongside it.
    """
    shared = sorted(set(cache_a._data) & set(cache_b._data))
    if not shared:
        return {
            "n": 0,
            "kappa": float("nan"),
            "exact_agreement": float("nan"),
            "note": "the two caches have no judgments in common",
        }
    a = [float(cache_a._data[k]["grade"]) for k in shared]
    b = [float(cache_b._data[k]["grade"]) for k in shared]
    k = weighted_kappa(a, b, levels)
    exact = sum(1 for x, y in zip(a, b, strict=True) if x == y) / len(shared)
    _point, lo, hi = bootstrap_ci([1.0 if x == y else 0.0 for x, y in zip(a, b, strict=True)])
    return {
        "n": len(shared),
        "kappa": k,
        "exact_agreement": exact,
        "exact_agreement_ci": (lo, hi),
        "only_in_a": len(set(cache_a._data) - set(cache_b._data)),
        "only_in_b": len(set(cache_b._data) - set(cache_a._data)),
    }


def weighted_kappa(
    a: Sequence[Grade | float],
    b: Sequence[Grade | float],
    levels: Sequence[float] = (0.0, 0.5, 1.0),
) -> float:
    """Linear-weighted Cohen's kappa between two graders.

    Linear rather than quadratic because the rubric is ordinal with three
    levels, where quadratic weighting would make the single disagreement that
    matters (absent vs present) dominate.
    """
    a = [float(x) for x in a]
    b = [float(x) for x in b]
    if len(a) != len(b) or not a:
        raise ValueError("graders must supply the same non-empty number of grades")
    k = len(levels)
    idx = {v: i for i, v in enumerate(levels)}
    n = len(a)
    obs = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b, strict=True):
        obs[idx[x]][idx[y]] += 1.0 / n
    ra = Counter(idx[x] for x in a)
    rb = Counter(idx[y] for y in b)
    w = [[abs(i - j) / (k - 1) for j in range(k)] for i in range(k)]
    num = sum(w[i][j] * obs[i][j] for i in range(k) for j in range(k))
    den = sum(w[i][j] * (ra[i] / n) * (rb[j] / n) for i in range(k) for j in range(k))
    if den == 0:
        return 1.0
    return 1.0 - num / den


def bootstrap_ci(
    values: Sequence[float],
    stat=lambda v: sum(v) / len(v),
    n_boot: int = 2000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Point estimate and percentile bootstrap interval."""
    import random

    rng = random.Random(seed)
    vals = list(values)
    if not vals:
        return (float("nan"),) * 3
    point = stat(vals)
    draws = []
    n = len(vals)
    for _ in range(n_boot):
        draws.append(stat([vals[rng.randrange(n)] for _ in range(n)]))
    draws.sort()
    lo = draws[int((alpha / 2) * n_boot)]
    hi = draws[min(n_boot - 1, int((1 - alpha / 2) * n_boot))]
    return point, lo, hi

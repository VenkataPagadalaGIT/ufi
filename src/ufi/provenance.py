"""Freezing, parameter locking and the run manifest.

Three artifacts answer three specific reviewer objections, and producing them
is a command rather than a discipline:

`freeze_queries` writes the evaluation query set with a hash and a date, before
outcomes exist. Without it, a query universe defined after launch is selected on
the outcome, and every share and percentage computed on it is uninterpretable.

`lock_parameters` writes the parameter set with a hash. Without it, a reader
cannot tell whether alpha and beta were chosen before or after the results were
seen.

`RunManifest` records the fingerprints of the ontology, the graph, the judgment
cache, the parameters and the frozen query set, together with the package
version. Two runs with the same manifest produce the same numbers.
"""
from __future__ import annotations

import json
import platform
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .types import stable_hash


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def freeze_queries(queries: Sequence[str], path: str | Path,
                   note: str = "") -> dict[str, Any]:
    """Write the evaluation query set with a hash. Refuses to overwrite."""
    p = Path(path)
    if p.exists():
        raise FileExistsError(
            f"{p} already exists. A frozen query set is not rewritten: that is "
            "the entire point of freezing it. Write a new file with a new name "
            "and report both.")
    qs = sorted(set(q.strip() for q in queries if q.strip()))
    payload = {"frozen_at": _now(), "n": len(qs), "hash": stable_hash(qs),
               "note": note, "queries": qs}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return {k: v for k, v in payload.items() if k != "queries"}


def verify_frozen(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    recomputed = stable_hash(payload["queries"])
    return {"path": str(path), "frozen_at": payload["frozen_at"],
            "n": payload["n"], "hash": payload["hash"],
            "intact": recomputed == payload["hash"]}


def lock_parameters(params: Any, path: str | Path, note: str = "") -> dict[str, Any]:
    p = Path(path)
    if p.exists():
        raise FileExistsError(f"{p} already exists; parameters are locked once.")
    d = asdict(params) if hasattr(params, "__dataclass_fields__") else dict(params)
    payload = {"locked_at": _now(), "hash": stable_hash(sorted(d.items())),
               "note": note, "parameters": d}
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    return payload


@dataclass
class RunManifest:
    """Everything needed to say whether two runs are the same run."""

    package_version: str
    created: str = field(default_factory=_now)
    python: str = field(default_factory=lambda: sys.version.split()[0])
    platform: str = field(default_factory=platform.platform)
    ontology_fingerprint: str = ""
    graph_fingerprint: str = ""
    cache_fingerprint: str = ""
    parameters_hash: str = ""
    frozen_queries_hash: str = ""
    n_entities: int = 0
    n_triples: int = 0
    n_judgments: int = 0
    judge_calls: int = 0
    cache_hits: int = 0
    demand_first_party_share: float = 0.0
    demand_synthetic_share: float = 0.0
    notes: dict[str, Any] = field(default_factory=dict)

    def write(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(self), indent=1), encoding="utf-8")

    def digest(self) -> str:
        return stable_hash(self.ontology_fingerprint, self.graph_fingerprint,
                           self.cache_fingerprint, self.parameters_hash,
                           self.frozen_queries_hash)

#!/usr/bin/env python3
"""Fetch the full numbering-plan registry, or explain why the bundled subset exists.

`data/area_codes.csv` is a verified subset of 66 geographic and 4 non-geographic
codes, bundled so the worked example runs offline with no credentials. The full
registry is a public record published by the numbering-plan administrator.

This script downloads it, records the response hash and the retrieval date, and
writes the result beside the bundled file rather than over it, so a reader can
see both and diff them. It never silently replaces the subset: a worked example
whose inputs change under it is not reproducible.

If the network is unavailable, the script says so and exits non-zero. It does
not fall back to the bundled file and report success.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
SOURCES = [
    ("nanpa-co-code-registry", "https://www.nationalnanpa.com/nanp1/npa_report.csv"),
]
TIMEOUT = 60


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "ufi/0.1 (+research; contact via repo)"})
    with urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read()


def main() -> int:
    out_dir = HERE / "data" / "registry"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    failures = 0
    for source_id, url in SOURCES:
        try:
            body = fetch(url)
        except (URLError, OSError, TimeoutError) as exc:
            print(f"could not fetch {url}: {exc}", file=sys.stderr)
            failures += 1
            continue
        digest = hashlib.sha256(body).hexdigest()
        target = out_dir / f"{source_id}.csv"
        target.write_bytes(body)
        manifest.append(
            {
                "source_id": source_id,
                "url": url,
                "bytes": len(body),
                "sha256": digest,
                "retrieved": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "path": str(target.relative_to(HERE)),
            }
        )
        print(f"{source_id}: {len(body)} bytes, sha256 {digest[:16]}… → {target}")
    if manifest:
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    if failures:
        print(
            "\nThe bundled subset in data/area_codes.csv is unchanged and the "
            "worked example still runs. It is a subset: treat any count taken "
            "from it as a count over 66 codes, not over the full plan.",
            file=sys.stderr,
        )
        return 1
    print(
        "\nWrote data/registry/. The bundled subset is untouched; diff them "
        "before using the full file, because column names change between "
        "revisions of the published report."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

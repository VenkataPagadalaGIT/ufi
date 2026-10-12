#!/usr/bin/env python3
"""Generate the SYNTHETIC demand and evidence inputs for the worked example.

These are not real observations. They are generated with a fixed seed so that
the example is deterministic and runs offline, and so that a reader can see the
shape of the inputs each adapter expects. Nothing produced here is a finding
about the real web, and `build_example.py` says so when it runs.

The generator deliberately produces an uneven world: a few codes attract many
questions and are well answered, most attract few and are answered poorly, and
two surfaces return nothing at all. That last part matters, because a demand
layer with silent empty surfaces is the failure mode the coverage report exists
to expose.
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 20261011

FORUM_FORMS = [
    "who called me from {npa}", "is {npa} a scam number",
    "what time zone is area code {npa}", "where is area code {npa}",
    "area code {npa} location", "got a call from {npa} should I answer",
    "is area code {npa} toll free", "what city is area code {npa}",
]
VIDEO_FORMS = ["area code {npa} explained", "{npa} area code scam calls"]
REVIEW_FORMS = ["called from {npa} about my service"]
PAA_FORMS = ["what area code is {npa}", "is {npa} eastern time"]


def main() -> int:
    rng = random.Random(SEED)
    rows = list(csv.DictReader((HERE / "data" / "area_codes.csv").open(encoding="utf-8")))
    geo = [r for r in rows if r["kind"] == "geographic"]

    # A heavy-tailed popularity: a handful of metros dominate, most codes have
    # a thin tail. This is the distribution the demand term has to survive.
    pop = {r["npa"]: rng.paretovariate(1.3) for r in geo}

    demand = []
    for r in geo:
        npa = r["npa"]
        n_forum = min(14, int(pop[npa]))
        for _ in range(n_forum):
            demand.append({"text": rng.choice(FORUM_FORMS).format(npa=npa),
                           "surface": "forum", "source_id": "demo-forum",
                           "retrieved": "2026-10-11", "synthetic": True,
                           "weight": float(rng.randint(1, 40))})
        for _ in range(min(4, int(pop[npa] / 3))):
            demand.append({"text": rng.choice(VIDEO_FORMS).format(npa=npa),
                           "surface": "video_short", "source_id": "demo-video",
                           "retrieved": "2026-10-11", "synthetic": True,
                           "weight": float(rng.randint(100, 50000))})
        for _ in range(min(3, int(pop[npa] / 5))):
            demand.append({"text": rng.choice(REVIEW_FORMS).format(npa=npa),
                           "surface": "review_gmb", "source_id": "demo-gmb",
                           "retrieved": "2026-10-11", "synthetic": True, "weight": 1.0})
        for _ in range(min(2, int(pop[npa] / 4))):
            demand.append({"text": rng.choice(PAA_FORMS).format(npa=npa),
                           "surface": "people_also_ask", "source_id": "demo-paa",
                           "retrieved": "2026-10-11", "synthetic": True, "weight": 1.0})
    rng.shuffle(demand)
    (HERE / "data" / "demo_demand.json").write_text(
        json.dumps(demand, indent=1), encoding="utf-8")

    # Reported search volume, kept separate from question counts. Without this
    # the volume baseline B1 and the question-mining baseline B3 are fed the
    # same numbers and trivially agree, which makes the comparison between them
    # meaningless and flattering.
    volumes = {r["npa"]: round(pop[r["npa"]] * rng.uniform(200, 4000))
               for r in geo}
    (HERE / "data" / "demo_volumes.json").write_text(
        json.dumps(volumes, indent=1), encoding="utf-8")

    # Evidence strings the RuleJudge reads. The judge gives full credit when the
    # evidence names the answer, partial when it is vague, none when empty.
    own, competitor, serp = {}, {"directory-a": {}, "directory-b": {},
                                 "carrier-x": {}}, {}
    for r in geo:
        npa, eid = r["npa"], f"npa:{r['npa']}"
        place, tz = r["principal_place"], r["predominant_time_zone"]
        # The organization covers a handful of codes on a list page only.
        if rng.random() < 0.12:
            own[eid] = f"list of area codes includes {npa} serving {place}"
        # Directories cover most codes; one carrier covers almost none.
        if rng.random() < 0.85:
            competitor["directory-a"][eid] = (
                f"Area code {npa} is located in {place}. Time zone {tz}.")
        if rng.random() < 0.6:
            competitor["directory-b"][eid] = f"{npa} area code information page"
        if rng.random() < 0.05:
            competitor["carrier-x"][eid] = f"{npa} overlay notice"
        # Retrieved results: location is usually answered, time zone often not,
        # overlay rarely, carrier almost never. Each verbalization gets its own
        # evidence string so `ans` can take the best phrasing.
        answered_tz = rng.random() < 0.45
        answered_loc = rng.random() < 0.9
        answered_ov = rng.random() < 0.25
        answered_car = rng.random() < 0.08
        for v, ok, body in (
            (f"area code {npa} time zone", answered_tz, f"{npa} is in {tz}"),
            (f"what time zone is {npa}", answered_tz, f"time zone of {npa}: {tz}"),
            (f"is {npa} eastern time", answered_tz and tz.endswith("New_York"),
             f"{npa} observes {tz}"),
            (f"what time is it in area code {npa}", False, ""),
            (f"area code {npa} location", answered_loc, f"{npa} serves {place}"),
            (f"where is area code {npa}", answered_loc, f"{npa} is in {place}"),
            (f"what city is area code {npa}", answered_loc, f"city: {place}"),
            (f"{npa} area code what state", answered_loc, f"state: {r['state']}"),
            (f"area codes that overlay {npa}", answered_ov,
             f"{npa} overlays {r['overlay_complex'] or 'none'}"),
            (f"{npa} overlay area code", answered_ov, f"overlay complex for {npa}"),
            (f"what area code covers the same area as {npa}", False, ""),
            (f"who called me from {npa}", answered_car, f"carriers in {npa}"),
            (f"what carrier is area code {npa}", answered_car, f"carrier list {npa}"),
            (f"is {npa} a scam number", False, ""),
        ):
            serp[v] = body if ok else ""
    (HERE / "data" / "demo_evidence.json").write_text(
        json.dumps({"own": own, "competitor": competitor, "serp": serp}, indent=1),
        encoding="utf-8")

    print(f"wrote {len(demand)} synthetic demand records")
    print(f"wrote {len(volumes)} synthetic reported-volume rows")
    print(f"wrote evidence: own {len(own)}, "
          f"competitor {sum(len(v) for v in competitor.values())}, serp {len(serp)}")
    print("SYNTHETIC: for pipeline demonstration only, not observations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

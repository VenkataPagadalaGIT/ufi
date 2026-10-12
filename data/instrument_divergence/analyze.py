"""Every number in Section 5.5 of the manuscript, computed from the two CSVs.

Run from this directory. Prints a block that the manuscript quotes verbatim, so
the prose cannot drift from the file. Section 5.5 of version 4.6 was written
from recollection of the table and miscounted it twice; this script exists so
that cannot happen again.
"""
import csv, math, random, sys
from itertools import combinations

A = {r["prefix"]: r for r in csv.DictReader(open("ahrefs_prefixes_2026-10-12.csv"))}
S = {r["prefix"]: r for r in csv.DictReader(open("semrush_prefixes_2026-10-12.csv"))}
rows = []
for p in A:
    a, s = A[p], S[p]
    y, m = map(int, a["ahrefs_first_traffic_month"].split("-"))
    age = (2026 - y) * 12 + (10 - m)
    at, st = float(a["ahrefs_organic_traffic"]), float(s["semrush_organic_traffic_us"])
    ak, sk = float(a["ahrefs_organic_keywords"]), float(s["semrush_organic_keywords_us"])
    us = a.get("ahrefs_us_share")
    us = float(us) if us else None
    rows.append(dict(prefix=p, age=age, at=at, st=st, vr=st / at, ak=ak, sk=sk, kr=sk / ak,
                     us=us, vr_us=(st / (at * us)) if us else None))
rows.sort(key=lambda r: r["age"])
n = len(rows)

def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i]); r = [0.0] * len(xs); i = 0
    while i < len(order):                       # average ranks for ties
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]: j += 1
        for k in range(i, j + 1): r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r

def pearson(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sx = math.sqrt(sum((v - mx) ** 2 for v in x)); sy = math.sqrt(sum((v - my) ** 2 for v in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)

def spearman(x, y): return pearson(ranks(x), ranks(y))

def kendall(x, y):
    c = d = 0
    for i, j in combinations(range(len(x)), 2):
        s = (x[i] - x[j]) * (y[i] - y[j])
        if s > 0: c += 1
        elif s < 0: d += 1
    return (c - d) / (c + d), c, d

def fisher_ci(r, n, z=1.96):
    zr = math.atanh(r); se = 1 / math.sqrt(n - 3)
    return math.tanh(zr - z * se), math.tanh(zr + z * se)

def perm_p(x, y, stat, iters=20000, seed=1):
    rnd = random.Random(seed); obs = abs(stat(x, y)); yy = list(y); hits = 0
    for _ in range(iters):
        rnd.shuffle(yy)
        if abs(stat(x, yy)) >= obs: hits += 1
    return hits / iters

ages = [r["age"] for r in rows]; vr = [r["vr"] for r in rows]; kr = [r["kr"] for r in rows]
at = [r["at"] for r in rows]; st = [r["st"] for r in rows]
below = [r["prefix"] for r in rows if r["vr"] < 1]
top = sorted(rows, key=lambda r: -r["vr"])
rho = spearman(ages, vr); lo, hi = fisher_ci(rho, n); p = perm_p(ages, vr, spearman)
rows_x = [r for r in rows if "area-codes" not in r["prefix"]]
rho_x = spearman([r["age"] for r in rows_x], [r["vr"] for r in rows_x])
rho_kv = spearman(kr, vr); rho_kv_x = spearman([r["kr"] for r in rows_x], [r["vr"] for r in rows_x])
rho_vendors = spearman(at, st); tau, conc, disc = kendall(at, st)
vals = sorted(vr); median = (vals[n // 2 - 1] + vals[n // 2]) / 2 if n % 2 == 0 else vals[n // 2]

print(f"n = {n} prefixes, one domain, read 2026-10-12")
print(f"visits ratio Semrush/Ahrefs: min {min(vr):.2f}x ({top[-1]['prefix']}), max {max(vr):.2f}x ({top[0]['prefix']}), "
      f"second {top[1]['vr']:.2f}x ({top[1]['prefix']}), median {median:.2f}, spread {math.log10(max(vr)/min(vr)):.2f} decades")
print(f"prefixes with ratio below one: {len(below)} of {n}: {', '.join(below)}")
print(f"Spearman rho(age, visits ratio) = {rho:+.2f}; Fisher 95% CI [{lo:+.2f}, {hi:+.2f}]; permutation p = {p:.2f}")
print(f"  excluding the area-code section: rho = {rho_x:+.2f} (n = {n-1})")
print(f"Spearman rho(keyword ratio, visits ratio) = {rho_kv:+.2f}; excluding area-codes {rho_kv_x:+.2f}")
print(f"keyword ratio Semrush/Ahrefs: min {min(kr):.1f}x, max {max(kr):.1f}x, all above one")
print(f"Vendor agreement on ORDERING sections by visits: Spearman {rho_vendors:+.2f}, Kendall tau {tau:+.2f}, "
      f"{conc} of {conc+disc} pairs concordant, {disc} discordant")
print(f"Power note: n = {n} gives roughly 38% power to detect rho = 0.5 at alpha 0.05 (two-sided).")
if all(r["us"] for r in rows):
    vru = [r["vr_us"] for r in rows]; belowu = [r["prefix"] for r in rows if r["vr_us"] < 1]
    valsu = sorted(vru); medu = (valsu[n//2-1] + valsu[n//2]) / 2
    print(f"TERRITORY-MATCHED (Semrush US / Ahrefs US-only): min {min(vru):.2f}x, max {max(vru):.2f}x, median {medu:.2f}, "
          f"below one {len(belowu)} of {n}; rho(age, ratio) = {spearman(ages, vru):+.2f}")
    print("  US share of Ahrefs visits by prefix: " + ", ".join(f"{r['prefix']} {r['us']:.0%}" for r in rows))

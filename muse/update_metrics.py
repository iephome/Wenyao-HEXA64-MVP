#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, csv, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUSE = ROOT / "muse"
SEEDS = MUSE / "seeds.csv"
VARIANTS = MUSE / "variants.csv"
REST = MUSE / "rest.csv"
SHIP = MUSE / "ship_log.csv"
METRICS = MUSE / "metrics.json"
REPORT = ROOT / "tests" / "report.csv"

def parse_date(s):
    try:
        return datetime.date.fromisoformat((s or '').strip())
    except Exception:
        return None

def load_csv(path):
    if not path.exists(): return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return list(csv.DictReader(f))
        except Exception:
            return []

def uniq_artifacts_from_seeds(rows, today):
    arts = set()
    for r in rows:
        d = parse_date(r.get("date"))
        if not d or (today - d).days > 7: continue
        if str(r.get("used", "0")).strip() == "1":
            for a in (r.get("artifact_ids") or "").split("|"):
                a = a.strip()
                if a: arts.add(a)
    return arts

def uniq_artifacts_from_variants(rows, today):
    arts = set()
    for r in rows:
        d = parse_date(r.get("date"))
        if not d or (today - d).days > 7: continue
        a = (r.get("artifact_id") or "").strip()
        if a: arts.add(a)
    return arts

def uniq_artifacts_from_ship(rows, today):
    arts = set()
    for r in rows:
        d = parse_date(r.get("date"))
        if not d or (today - d).days > 7: continue
        a = (r.get("artifact_id") or "").strip()
        if a: arts.add(a)
    return arts

def input_diversity_7d(rows, today):
    tags = set()
    for r in rows:
        d = parse_date(r.get("date"))
        if not d or (today - d).days > 7: continue
        t = (r.get("tag") or "").strip()
        if t: tags.add(t)
    return len(tags)

def qa_pass_rate():
    if not REPORT.exists(): return 0.0
    ok = total = 0
    with open(REPORT, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total += 1
            if str(row.get("meets_golden","0")).strip() == "1":
                ok += 1
    return (ok/total) if total else 0.0

def rest_blocks_7d(rows, today):
    total_min = 0.0
    for r in rows:
        d = parse_date(r.get("date"))
        if not d or (today - d).days > 7: continue
        try:
            total_min += float(r.get("duration_min","0") or 0)
        except Exception:
            pass
    return round(total_min/25.0, 1), int(total_min)

def main():
    today = datetime.date.today()
    seeds = load_csv(SEEDS)
    variants = load_csv(VARIANTS)
    rest = load_csv(REST)
    ship = load_csv(SHIP)

    m = {}
    if METRICS.exists():
        try: m = json.loads(METRICS.read_text(encoding="utf-8"))
        except Exception: m = {}

    m.setdefault("period_days", 7)
    if not m.get("period_start"): m["period_start"] = today.isoformat()
    if not m.get("period_end"):   m["period_end"]   = (today + datetime.timedelta(days=int(m["period_days"])-1)).isoformat()
    m["last_updated"] = today.isoformat()

    m["input_diversity_7d"] = input_diversity_7d(seeds, today)
    m["qa_pass_rate"]       = round(qa_pass_rate(), 4)

    arts_seed = uniq_artifacts_from_seeds(seeds, today)
    arts_var  = uniq_artifacts_from_variants(variants, today)
    arts_ship = uniq_artifacts_from_ship(ship, today)
    denom = len(arts_seed.union(arts_var).union(arts_ship))
    numer = len(arts_var)
    m["variant_rate_numerator"]   = numer
    m["variant_rate_denominator"] = denom
    m["variant_rate"]             = round((numer/denom), 4) if denom else 0.0

    blocks, total_min = rest_blocks_7d(rest, today)
    m["rest_blocks_7d"] = blocks
    m["rest_minutes_7d"] = total_min

    METRICS.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print("[OK] metrics.json updated ->", METRICS)

if __name__ == "__main__":
    main()

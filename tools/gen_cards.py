#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG_PATH = ROOT/"data/hexa_registry.json"
C = ROOT/"cosmic"
OUT = ROOT/"out"
OUT.mkdir(exist_ok=True)

SIX_RE = re.compile(r'^[01]{6}$')

def iter_registry_records(obj):
    """Yield {'six_code': 'xxxxxx'} regardless of registry shape."""
    def norm_one(x):
        if isinstance(x, str) and SIX_RE.match(x):
            return {"six_code": x}
        if isinstance(x, dict):
            for k in ("six_code","sixCode","code"):
                v = x.get(k)
                if isinstance(v, str) and SIX_RE.match(v):
                    return {"six_code": v}
        return None

    if isinstance(obj, list):
        for x in obj:
            r = norm_one(x)
            if r: yield r
        return

    if isinstance(obj, dict):
        # common wrappers
        for k in ("records","items","data"):
            if k in obj:
                yield from iter_registry_records(obj[k])
                return
        # mapping: six_code -> any
        for k, _ in obj.items():
            if isinstance(k, str) and SIX_RE.match(k):
                yield {"six_code": k}
        return

def parse_min_yaml(path):
    e, n, pc, pe, icon = [], [], "", "", ""
    mode = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if s.endswith("expand12:"): mode="e"; continue
        if s.endswith("neighbors_h1:"): mode="n"; continue
        if s.startswith("prompt_cn:"): pc = s.split(":",1)[1].strip().strip('"'); continue
        if s.startswith("prompt_en:"): pe = s.split(":",1)[1].strip().strip('"'); continue
        if s.startswith("icon_path:"): icon = s.split(":",1)[1].strip().strip('"'); continue
        if s.startswith("- "):
            val = s[2:].strip()
            if mode=="e": e.append(val)
            elif mode=="n": n.append(val)
    return e, n, pc, pe, icon

def main():
    if not REG_PATH.exists():
        print(f"[ERR] registry not found: {REG_PATH}", file=sys.stderr); sys.exit(2)
    REG = json.loads(REG_PATH.read_text(encoding="utf-8"))

    rows, seen = [], set()
    for rec in iter_registry_records(REG):
        sc = rec["six_code"]
        if not SIX_RE.match(sc) or sc in seen:
            continue
        seen.add(sc)
        yml = C/f"{sc}.yaml"
        e, n, pc, pe, icon = ([], [], "", "", "")
        if yml.exists():
            e, n, pc, pe, icon = parse_min_yaml(yml)
        rows.append({
            "six_code": sc,
            "index": int(sc,2),
            "machine_tags": "|".join(e),
            "neighbors_h1": "|".join(n),
            "prompt_cn": pc,
            "prompt_en": pe,
            "icon_path": icon
        })

    rows.sort(key=lambda r: r["index"])
    if not rows:
        print("[ERR] no records produced; inspect data/hexa_registry.json", file=sys.stderr); sys.exit(3)

    outp = OUT/"cards_meta.csv"
    with outp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"[OK] wrote {len(rows)} rows -> {outp}")

if __name__ == "__main__":
    main()

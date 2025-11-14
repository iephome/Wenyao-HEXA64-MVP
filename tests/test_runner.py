#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hexa_registry.json"
OUT  = ROOT / "tests" / "report.csv"

MODULES = ["l1","l2","l3","l4","l5","r1","r2","r3","r4","r5","c1","c2"]
SIX_RE  = re.compile(r"^[01]{6}$")

def expand12(six): return [f"{m} {six}" for m in MODULES]
def neighbors_h1(six):
    b=list(six); out=[]
    for i in range(6):
        c=b.copy(); c[i] = "1" if c[i]=="0" else "0"
        out.append("".join(c))
    return out
def affinity_self(_): return 6

def main():
    items = json.loads(DATA.read_text(encoding="utf-8")).get("items",[])
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["six_code","expand12_count","neighbors_h1_count","affinity_self","meets_golden"])
        for it in items:
            sc = (it.get("six_code") or "").strip()
            if not SIX_RE.match(sc):
                w.writerow([sc,0,0,0,0]); continue
            e12c = len(expand12(sc))
            nbh1 = len(neighbors_h1(sc))
            aff  = affinity_self(sc)
            ok   = int(e12c==12 and nbh1==6 and aff==6)
            w.writerow([sc,e12c,nbh1,aff,ok])
    print("[OK] report.csv generated:", OUT)

if __name__ == "__main__":
    main()

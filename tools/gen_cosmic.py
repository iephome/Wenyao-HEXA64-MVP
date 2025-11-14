#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT / "cosmic"
OUT.mkdir(parents=True, exist_ok=True)

MODULES = ["l1","l2","l3","l4","l5","r1","r2","r3","r4","r5","c1","c2"]

def neighbors_h1(six):
    b=list(six); out=[]
    for i in range(6):
        c=b.copy(); c[i] = '1' if c[i]=='0' else '0'
        out.append(''.join(c))
    return out

today = date.today().isoformat()

def dump_yaml(sc):
    idx = int(sc, 2)  # 純位元序（0~63），非傳統排序
    expand12 = [f"{m} {sc}" for m in MODULES]
    neigh    = neighbors_h1(sc)

    # 手寫 YAML（避免相依 PyYAML）
    lines = []
    a = lines.append
    a("meta:")
    a(f"  six_code: \"{sc}\"")
    a(f"  index: {idx}")
    a(f"  version: \"0.1\"")
    a(f"  created: {today}")
    a("mapping:")
    a("  expand12:")
    for t in expand12:
        a(f"    - {t}")
    a("  neighbors_h1:")
    for n in neigh:
        a(f"    - {n}")
    a("semantics:")
    a("  kernel: \"\"")
    a("  motifs: []")
    a("  questions: []")
    a("operators:")
    a("  suggested: []")
    a("  notes: \"\"")
    a("router:")
    a("  input_signals: []")
    a("  default_module_priority: [l1,l2,l3,l4,l5,r1,r2,r3,r4,r5,c1,c2]")
    a("qa:")
    a("  invariants:")
    a("    expand12_count: 12")
    a("    neighbors_h1_count: 6")
    a("    min_affinity_self: 6")
    a("assets:")
    a("  prompt_cn: \"\"")
    a("  prompt_en: \"\"")
    a("  icon_path: \"\"")
    a("provenance:")
    a("  author: \"iephome\"")
    a("  generated_by: \"HEXA64_MVP_v0_1/tools/gen_cosmic.py\"")
    a("  commit: \"\"")
    return "\n".join(lines) + "\n"

def main():
    from itertools import product
    for bits in product('01', repeat=6):
        sc = ''.join(bits)
        (OUT / f"{sc}.yaml").write_text(dump_yaml(sc), encoding="utf-8")
    print("[OK] generated 64 files under cosmic/")

if __name__ == "__main__":
    main()

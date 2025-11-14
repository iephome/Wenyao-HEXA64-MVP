#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path, PurePath
import re

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "cosmic"
SIX_RE = re.compile(r'^[01]{6}$')

def read_map(path):
    # 超輕量 YAML 解析（只抽我們需要的兩段）
    expand12 = []
    neighbors = []
    mode = None
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s == "expand12:": mode = "e"; continue
        if s == "neighbors_h1:": mode = "n"; continue
        if s.startswith("- "):
            val = s[2:].strip()
            if mode == "e": expand12.append(val)
            elif mode == "n": neighbors.append(val)
    return expand12, neighbors

def main():
    files = sorted(p for p in C.glob("*.yaml") if SIX_RE.match(p.stem))
    bad = 0
    for p in files:
        e, n = read_map(p)
        ok = (len(e)==12 and len(n)==6)
        if not ok:
            bad += 1
            print("[FAIL]", PurePath(p).name, len(e), len(n))
    if bad==0:
        print(f"[OK] {len(files)} files validated (expand12=12, neighbors=6)")
    else:
        print(f"[ERR] {bad} files invalid out of {len(files)}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json, csv

ROOT = Path(__file__).resolve().parents[1]
OUT  = ROOT/"out"
OUT.mkdir(exist_ok=True)

def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def read_csv(p):
    rows=[]
    if Path(p).exists():
        import csv
        with open(p,encoding="utf-8") as f:
            rows=list(csv.DictReader(f))
    return rows

def main():
    met = read_json(ROOT/"muse/metrics.json")
    seeds = read_csv(ROOT/"muse/seeds.csv")
    vars_ = read_csv(ROOT/"muse/variants.csv")
    ships = read_csv(ROOT/"muse/ship_log.csv")
    rest  = read_csv(ROOT/"muse/rest.csv")

    html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<title>Wenyao Muse Dashboard</title>
<style>
body{{font-family:ui-sans-serif,system-ui; margin:24px;}}
.grid{{display:grid; grid-template-columns:repeat(4,1fr); gap:16px;}}
.card{{border:1px solid #ddd; border-radius:12px; padding:16px;}}
.big{{font-size:32px; font-weight:700;}}
.mono{{font-family:ui-monospace,Menlo,monospace; font-size:13px; color:#555;}}
</style>
</head><body>
<h2>Muse Dashboard <span class="mono">(period {met.get('period_start')} → {met.get('period_end')})</span></h2>
<div class="grid">
  <div class="card"><div class="big">{met.get('input_diversity_7d')}</div><div>Input Diversity (7d)</div></div>
  <div class="card"><div class="big">{met.get('variant_rate')}</div><div>Variant Rate</div></div>
  <div class="card"><div class="big">{met.get('qa_pass_rate')}</div><div>QA Pass Rate</div></div>
  <div class="card"><div class="big">{met.get('rest_blocks_7d')}</div><div>Rest Blocks (7d)</div></div>
</div>
<p class="mono">Seeds: {len(seeds)} | Variants: {len(vars_)} | Ships: {len(ships)} | Rest rows: {len(rest)}</p>
</body></html>"""
    outp = OUT/"muse_dashboard.html"
    outp.write_text(html,encoding="utf-8")
    print("[OK]", outp)

if __name__=="__main__":
    main()

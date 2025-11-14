PY=python3

qa:
	$(PY) tests/test_runner.py
	$(PY) tools/validate_cosmic.py

muse:
	$(PY) muse/update_metrics.py
	@$(PY) - <<'PY'
import json; m=json.load(open("muse/metrics.json"))
print("[Muse]", {k:m[k] for k in ["input_diversity_7d","variant_rate","rest_blocks_7d","qa_pass_rate"]})
PY

brain:
	$(PY) tools/cosmic_to_brain.py
	@ls -lh out/brain_nodes.json

all: qa muse brain

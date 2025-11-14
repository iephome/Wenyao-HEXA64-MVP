
## Cosmic 語義模板編寫指引
- **文件位置**：`cosmic/<six_code>.yaml`（例如 `cosmic/000100.yaml`）
- **只用 six_code / machine_tag**：遵循 Wenyao 規範，不使用傳統卦名／上下卦。
- **建議每日填寫欄位**：
  - `semantics.kernel`：此 six_code 的核心語義（1～2 句）
  - `semantics.motifs[]`：關鍵意象詞（3～7 個）
  - `operators.suggested[]`：建議運算子／流程節點
  - `router.input_signals[]`：常見導入訊號（如任務類型、素材標籤）
  - `assets.prompt_cn/en`：生成提示的中英文對應
- **驗證**：`python3 tools/validate_cosmic.py`（CI 也會自動跑）
- **TheBrain 匯出**：`python3 tools/cosmic_to_brain.py` 產出 `out/brain_nodes.json`

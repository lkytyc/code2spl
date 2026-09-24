# Experiment 2 Supplement: code and configs (2026-09-13)

The supplement condition — the untagged SPL arm of Experiment 2 — needs two
**purely additive** changes to code that was already frozen. Rather than
overwrite the frozen files, the changed versions live here, with the untouched
originals beside them for line-by-line comparison.

| File here | The file it patches | Change |
| --- | --- | --- |
| [`common/spl_binding.patched.py`](common/spl_binding.patched.py) | [`code/common/spl_binding.py`](../../common/spl_binding.py) | Adds one `style` keyword argument (defaults to `"tagged"`, so the render path is byte-identical to before). |
| [`common/spl_binding.FROZEN_2026-08-22.py`](common/spl_binding.FROZEN_2026-08-22.py) | the same file | The frozen original, kept only for the comparison below. |
| [`02_core_reasoning/run.patched.py`](02_core_reasoning/run.patched.py) | [`code/RQ2/run.py`](../run.py) | 33 lines added, 2 modified — condition registration and wiring. |

```bash
diff -u code/RQ2/supplement_2026-09-13/common/spl_binding.FROZEN_2026-08-22.py \
        code/RQ2/supplement_2026-09-13/common/spl_binding.patched.py
diff -u code/RQ2/run.py \
        code/RQ2/supplement_2026-09-13/02_core_reasoning/run.patched.py
```

## Reproducing the supplement condition

The condition is registered in the shipped [`code/RQ2/run.py`](../run.py), so the
reported supplement run needs none of the steps below. They are here to show that
adding it changed nothing else.

1. Copy `common/spl_card_summary.py` to `code/common/spl_card_summary.py` — a pure
   addition that overwrites no file.
2. Copy `common/spl_binding.patched.py` over `code/common/spl_binding.py`. The
   existing conditions behave identically afterwards: `style` defaults to
   `"tagged"` and that render path is byte-identical.
3. Copy `02_core_reasoning/run.patched.py` over `code/RQ2/run.py`.
4. The config and prompt it needs are already in place:
   [`data/RQ2/settings/configs/full341_deepseek-v4-pro_unstructured_summary.json`](../../../data/RQ2/settings/configs/full341_deepseek-v4-pro_unstructured_summary.json)
   and
   [`code/RQ2/methods/raw_spl_unstructured_summary/prompts/prompt.md`](../methods/raw_spl_unstructured_summary/prompts/prompt.md).
   The prompt is byte-identical to
   [`raw_free_summary/prompts/prompt.md`](../methods/raw_free_summary/prompts/prompt.md)
   (SHA-256 `f4273ce7fa8a64e2e7d0c0745add2bd981db426d8bbbbb84a556e68d23fe6e74`),
   which is what makes the pair a controlled comparison.

Run it from the package root:

```powershell
python code\RQ2\run.py --config data\RQ2\settings\configs\full341_deepseek-v4-pro_unstructured_summary.json
python code\RQ2\evaluate.py --config data\RQ2\settings\configs\full341_deepseek-v4-pro_unstructured_summary.json
```

## The change is non-invasive — checkable

Regenerate the 341 prompts of the three pre-existing conditions with the built-in
`mock` provider and compare them byte-for-byte against the frozen versions:

| Condition | Same | Different |
| --- | ---: | ---: |
| `official_raw` | 341 | 0 |
| `raw_free_summary` | 341 | 0 |
| `raw_spl_atomic_strict` | 145 | 196 (all from the earlier protocol batch) |

The first two rows show the change disturbed nothing; the third shows the shipped
code is exactly the code that produced the new protocol batch.

## Analysis scripts

Each reads existing material only. No model and no SPL builder is invoked; output
goes to the supplement run directory.

| Script | Output |
| --- | --- |
| [`02_core_reasoning/_analyze_unstructured_summary.py`](02_core_reasoning/_analyze_unstructured_summary.py) | `supplement_analysis.json` — four-condition metrics, Wilson interval, exact McNemar, Holm correction, card drift, 303-subset sensitivity |
| [`02_core_reasoning/_audit_card_render.py`](02_core_reasoning/_audit_card_render.py) | `card_render_audit.json` — item-by-item record that the rendering and content of the 341 cards are preserved |
| [`02_core_reasoning/_audit_prompt_leakage.py`](02_core_reasoning/_audit_prompt_leakage.py) | `prompt_leakage_audit.json` — per-prompt keyword and protocol leakage across the 341 prompts |
| [`02_core_reasoning/_analyze_unstructured_usage.py`](02_core_reasoning/_analyze_unstructured_usage.py) | `unstructured_usage_analysis.json` — output identity across the three conditions, distribution of structured-only successes, prompt-role audit, three error cases |

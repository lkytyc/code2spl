# Prompts

Every prompt the experiments used, in one place, with the file that holds it and
the stage that sends it. There are two stages and they never share a prompt:

* **Construction** — the model is asked to read source code and write something
  (an SPL artifact, a natural-language summary). It runs once per repository or
  per sample, before any task is attempted, and its output is frozen into
  `data/*/spl_assets/`.
* **Task** — the model is asked to do the task the experiment measures: rebuild
  a class (RQ1), answer a core-reasoning question (RQ2), or produce a patch for
  a SWE-bench instance (RQ3).

Each condition differs from its control **only** in the task prompt (plus, in
RQ3, the workflow file the prompt points the agent at). The model, temperature
and token cap come from the config in `data/RQ*/settings/configs/`, never from
the prompt.

---

## 1. RQ1 — ClassEval reconstruction

Task prompts, one per condition. `code/RQ1/run.py` loads the file with
`load_prompt_template(...)` and fills in its placeholders.

| Condition | File | What the prompt asks for |
| --- | --- | --- |
| `skeleton_holistic` | [`code/RQ1/methods/skeleton_holistic/prompts/prompt.md`](code/RQ1/methods/skeleton_holistic/prompts/prompt.md) | Complete the class from the official skeleton alone — the protocol baseline. |
| `skeleton_spl` | [`code/RQ1/methods/skeleton_spl/prompts/prompt.md`](code/RQ1/methods/skeleton_spl/prompts/prompt.md) | Complete the skeleton, with SPL supplied as a structured implementation contract. |
| `spl_only` | [`code/RQ1/methods/spl_only/prompts/prompt.md`](code/RQ1/methods/spl_only/prompts/prompt.md) | Reconstruct the class from SPL only; no skeleton is given. |
| `free_summary` | [`code/RQ1/methods/free_summary/prompts/prompt.md`](code/RQ1/methods/free_summary/prompts/prompt.md) | Reconstruct the class from an unstructured natural-language summary. |

Construction prompts for the `free_summary` control live in code, not in a
`.md` file, because they define the artifact rather than the task:

| Prompt | File | Notes |
| --- | --- | --- |
| `FREE_SUMMARY_PROMPT` | [`code/RQ1/generate_free_summary.py`](code/RQ1/generate_free_summary.py) | One model call per sample: reference class → free-form summary. The `{summary}` slot of the `free_summary` task prompt above is filled with its output. |
| `STRUCTURED_SUMMARY_PROMPT` | [`code/RQ1/generate_free_summary.py`](code/RQ1/generate_free_summary.py) | The information-controlled variant, used only to show what the free-form summary is compared against. |

Both carry a SHA-256 recorded in the artifact metadata
(`FREE_SUMMARY_PROMPT_SHA256`), so an artifact built with a different prompt
cannot be mistaken for one of these.

## 2. RQ2 — core reasoning

Task prompts. Every one of them starts from the dataset's own question text
(`{official_prompt}`), so the conditions differ only in what is added to it.

| Condition | File | What is added |
| --- | --- | --- |
| `official_raw` | [`code/RQ2/methods/official_raw/prompts/prompt.md`](code/RQ2/methods/official_raw/prompts/prompt.md) | Nothing — the dataset prompt verbatim. |
| `raw_free_summary` | [`code/RQ2/methods/raw_free_summary/prompts/prompt.md`](code/RQ2/methods/raw_free_summary/prompts/prompt.md) | An auxiliary unstructured summary of the source. |
| `raw_spl_atomic_strict` | [`code/RQ2/methods/raw_spl_atomic_strict/prompts/prompt.md`](code/RQ2/methods/raw_spl_atomic_strict/prompts/prompt.md) | The SPL tags, as a source-bound analysis control. |
| `raw_spl_unstructured_summary` | [`code/RQ2/methods/raw_spl_unstructured_summary/prompts/prompt.md`](code/RQ2/methods/raw_spl_unstructured_summary/prompts/prompt.md) | The same SPL content with the tags stripped — the structure ablation. |

[`code/RQ2/supplement_2026-09-13/02_core_reasoning/methods/raw_spl_unstructured_summary/prompts/prompt.md`](code/RQ2/supplement_2026-09-13/02_core_reasoning/methods/raw_spl_unstructured_summary/prompts/prompt.md)
is the copy the untagged supplement was run from; it is kept beside that
supplement's results so the two can be compared line by line.

## 3. RQ3 — SWE-bench Lite under mini-swe-agent

The agent's system and instance templates are the vendored harness's own, under
[`code/third_party/mini_swe_agent/repo/src/minisweagent/config/`](code/third_party/mini_swe_agent/repo/src/minisweagent/config/); the runs used
`swebench.yaml`. A condition is defined by an *addendum* appended to the
instance template, and by the SPL file that addendum tells the agent to read.

| Condition | Addendum | What it changes |
| --- | --- | --- |
| `miniswe_original` | [`data/RQ3/settings/central_prompts/miniswe_original/addendum.md`](data/RQ3/settings/central_prompts/miniswe_original/addendum.md) | Nothing is appended; the file is documentation only. |
| `miniswe_spl_localization` | [`…/miniswe_spl_localization/addendum.md`](data/RQ3/settings/central_prompts/miniswe_spl_localization/addendum.md) | Points the agent at the SPL snapshot to shorten localization. |
| `miniswe_spl_repair` | [`…/miniswe_spl_repair/addendum.md`](data/RQ3/settings/central_prompts/miniswe_spl_repair/addendum.md) | Points at the owner of the current behavior so the repair is faster. |
| `miniswe_spl_both` | [`…/miniswe_spl_both/addendum.md`](data/RQ3/settings/central_prompts/miniswe_spl_both/addendum.md) | One pass as an owner-to-patch controller: localization and repair together. |
| `miniswe_free_summary` | [`…/miniswe_free_summary/addendum.md`](data/RQ3/settings/central_prompts/miniswe_free_summary/addendum.md) | The unstructured-summary control: a plain-language summary plus a helper to read it. |

`code/RQ3/run.py` appends the addendum at run time
(`load_prompt_addendum(mode, config)`), so the file in `central_prompts/` is the
live prompt.

[`data/RQ3/settings/frozen_original_prompts/`](data/RQ3/settings/frozen_original_prompts/)
holds the exact addendum text the reported SPL arms were run with, captured at
run time and never edited since. The supplements compare the two with
`_verify_against_delivered.py` and `_audit_unstructured_prompts.py`, which fail
if a delivered prompt does not contain the addendum and the controller block
verbatim.

## 4. SPL construction prompts

SPL is built by the generator shipped under
[`code/spl_generation/`](code/spl_generation/), which drives the vendored
analyzer prompts:

| Prompt | File |
| --- | --- |
| class analyzer | [`code/spl_generation/Code_SPL/prompt/class_analyzer.txt`](code/spl_generation/Code_SPL/prompt/class_analyzer.txt) |
| function analyzer | [`…/prompt/function_analyzer.txt`](code/spl_generation/Code_SPL/prompt/function_analyzer.txt) |
| call analyzer | [`…/prompt/function_call_analyzer.txt`](code/spl_generation/Code_SPL/prompt/function_call_analyzer.txt) |
| control-flow analyzer | [`…/prompt/control_flow_analyzer.txt`](code/spl_generation/Code_SPL/prompt/control_flow_analyzer.txt) |
| data-flow analyzer | [`…/prompt/data_flow_analyzer.txt`](code/spl_generation/Code_SPL/prompt/data_flow_analyzer.txt) |
| method SPL agent | [`…/prompt/method_spl_agent.txt`](code/spl_generation/Code_SPL/prompt/method_spl_agent.txt) |
| diagram planner | [`…/prompt/diagram_planner.txt`](code/spl_generation/Code_SPL/prompt/diagram_planner.txt) |

They are vendored unmodified, and the frozen artifacts under
`data/*/spl_assets/` were produced with them. Nothing in the reported runs
rebuilds an artifact, so these prompts matter only if you extend the study to a
new repository — see §4 of [`REPRODUCING.md`](REPRODUCING.md).

## 5. Prompt hygiene the supplements check

Two properties are asserted mechanically rather than by inspection, because a
leak would invalidate the comparison:

* **No answers in the SPL text.** `_audit_prompt_leakage.py` and
  `_audit_card_render.py` check that a construction prompt's output cannot
  contain the task's expected answer or its tests.
* **Tag stripping is complete.** The untagged arms must contain the SPL content
  with every `[TAG]` removed and nothing else changed; `_fairness_audit.py`
  compares the two renderings and reports any other difference.

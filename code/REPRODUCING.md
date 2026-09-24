# Reproducing the experiments

This file says what to run, in what order, and what each entry point expects.
Read [`../README.md`](../README.md) first for what the experiments are, and
[`data/results_tables/`](../data/results_tables/) if you only want the numbers.

Every command below is run from the package root — the directory that holds
`code/`, `data/` and `requirements.txt` — so the paths in them start at that
level. This file lives in `code/` because that is what it is about.

Three levels of reproduction are possible, and they cost very differently:

| Level | What it means | Cost |
| --- | --- | --- |
| **Read the results** | Recompute every table from the frozen run records | seconds, no API calls |
| **Re-score** | Re-run the evaluation over the shipped per-instance patches | CPU only, no API calls |
| **Re-run** | Generate new outputs from the models | API calls at full experiment cost |

Most reviewers want the first. It needs nothing but the package.

---

## 1. Recompute the result tables

```bash
python code/tools/build_tables.py
```

Reads only files inside the package and rewrites every CSV in
`data/results_tables/`. It cross-checks the SWE-bench arm against the frozen analyses
that shipped with the runs and reports any mismatch before finishing — a clean
run prints `cross-checked 6 frozen rows, 0 mismatch(es)`.

No API key, no Docker, no network.

---

## 2. Environment

Python 3.11 or newer.

```bash
python -m pip install -r requirements.txt
cp code/.env.example code/.env  # then fill in OPENAI_API_KEY and OPENAI_BASE_URL
```

`requirements.txt` is the whole environment; nothing is downloaded into the
package. It also installs `mini-swe-agent` from the unmodified copy vendored
under `code/third_party/mini_swe_agent/repo/`, so the agent version used
is the one shipped here. `code-spl` is likewise vendored, under
`code/spl_generation/`, and read from there by
`code/common/spl_adapter.py`. The upstream checkout keeps its Python modules one
level down, inside `Code_SPL/`; `code/common/paths.py:CODE_SPL_ROOT` names that
inner directory, which is the one that has to be importable.

### Settings

`code/.env` holds credentials, the endpoint, and the package root. It is the one
place an LLM or an endpoint is configured; `code/common/env.py` reads it at
import time, and [`.env.example`](.env.example) documents every entry:
which stage reads it, what it defaults to, and what the reported runs used. Any
entry can also be given as an ordinary environment variable, and a shell
variable wins over the file.

SPL is built once per repository and used by every task against it, so the
settings are split into two groups — `SPL_BUILDER_*` for the build stage and
`SPL_TASK_*` for the stage the experiments measure. The frozen artifacts under
`data/*/spl_assets/` are the ones the reported runs consumed, so the builder
settings only matter if you extend the study to new repositories.

### Scratch the runs create

Nothing generated is shipped, and three directories appear at the package root
the first time a stage runs:

| Directory | Written by | Contents |
| --- | --- | --- |
| `work/artifacts/tmp_sources/` | the SPL builder | one temporary source file per method handed to the AST layer |
| `work/hf_cache/` | Experiment 3 | the HuggingFace dataset cache (`hf_home` in `paper_base_config.json`) |
| `work/swebench_repo_cache/` | Experiment 3 | repository checkouts for the direct-validation path |
| `spl/` | the Experiment 3 prepare stage | the SPL snapshot the agent reads (`spl_snapshot_dir`), assembled from the frozen assets in `data/RQ3/spl_assets/` |

All of them are in `.gitignore`; delete them freely, no result is read from
under any of them. The Experiment 3 prepare stage also builds a per-instance
working tree at
`data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/working/round_01/`
(`prepare_random218.py` writes that path); it is scratch too, and the
2026-09-24 revision dropped it from the package rather than ship it. Anything
that reads it must run prepare first — in particular
`code/RQ3/supplement_2026-09-13/untagged_arm/_verify_against_delivered.py`,
whose `SAMPLES_DIR` points into it. `paper_base_config.json` sets
`"hf_offline": true`, which is
what the reported runs used — it means the run expects `work/hf_cache/` to be
populated already. On a fresh machine either download
`SWE-bench/SWE-bench_Verified` into that cache once, or set `hf_offline` to
`false` for your own re-run; the instance set is pinned either way by
`data/RQ3/inputs/unit_manifests_random218/`.

### Datasets

The upstream corpora are not shipped: recomputing the tables and re-scoring
Experiment 1 need nothing beyond the package, but the Experiment 1 prepare
stage and the Experiment 2 evaluation read the corpora, and Experiment 3 pulls
SWE-bench into `work/hf_cache/` on first use (see above). Fetch ClassEval and
CoRe from the mirrors named in
[`../data/PROVENANCE.md`](../data/PROVENANCE.md) and place them under
`data/datasets/` at the paths the shipped configs' `dataset_path` entries name;
the checksums there identify the exact files the reported runs read.

### Credentials

No credential is stored anywhere in this package. Runs read API keys from
`.env` (or from the environment) through the provider layer in
`code/common/providers.py`. Evaluation of SWE-bench patches needs Docker but no
key.

### Docker

SWE-bench evaluation runs each patch inside the instance's official image. The
images are pulled from Docker Hub on first use, which is the slowest and most
failure-prone step of a fresh reproduction. `code/RQ3/scripts/`
contains the pre-pull helper used for the runs reported here; pulling ahead of
time is strongly recommended.

### Long paths on Windows

SWE-bench instance ids plus run ids exceed the default Win32 path limit, and the
failure is silent in some tools. `code/common/paths.py` works around it:
`_open_path()` prefixes `\\?\` for reads and writes, and `_normalize_path()`
strips it again so parent checks still work. If you add your own scripts, do the
same and walk directories with `os.walk` rather than `Path.rglob`, which stops
descending without reporting an error.

---

## 3. Layout of a run

Every experiment follows the same three stages, driven by a JSON config:

```
code/<experiment>/prepare.py   --config <config.json>   # build prompts and inputs
code/<experiment>/run.py       --config <config.json>   # call the models
code/<experiment>/evaluate.py  --config <config.json>   # score the outputs
```

`--config` is the only required argument for all three. The configs that
produced the reported numbers are shipped, unchanged, under
`data/*/settings/`.

### Experiment 1 — ClassEval reconstruction

```bash
python code/RQ1/run.py      --config data/RQ1/settings/configs/full100_deepseek-v4-pro.json
python code/RQ1/evaluate.py --config data/RQ1/settings/configs/full100_deepseek-v4-pro.json
```

One config per model: `full100_<model>.json`. The structure ablation uses the
matching `full100_<model>_spl_structure_ablation.json`, which re-runs `spl_only`
and `skeleton_spl` with the tags stripped from the SPL text.

Scripts that produced the reported aggregates:

| Script | Output |
| --- | --- |
| `scripts/summarize_full100_models.py` | per-model condition table |
| `scripts/model_significance.py` | paired McNemar tests, Holm-corrected |
| `scripts/summarize_structure_ablation.py` | tagged-versus-compact comparison |

### Experiment 2 — core reasoning

```bash
python code/RQ2/run.py      --config data/RQ2/settings/configs/full341_deepseek-v4-pro.json
python code/RQ2/evaluate.py --config data/RQ2/settings/configs/full341_deepseek-v4-pro.json
```

Three configs, one per run directory under `data/results/exp2_core/`:

| Config | Conditions |
| --- | --- |
| `full341_deepseek-v4-pro.json` | `official_raw`, `raw_free_summary`, `raw_spl_atomic_strict` |
| `full341_deepseek-v4-pro_unstructured_summary.json` | `raw_spl_unstructured_summary` |
| `verify_rules_deepseek-v4-pro.json` | `raw_spl_atomic_strict`, 52-sample rule-verification subset |

SPL construction for this corpus is a separate step (`repair_spl.py`); the
resulting artifacts are shipped prebuilt under `data/RQ2/spl_assets/` and
do not need to be regenerated.

### Experiment 3 — SWE-bench Lite

```bash
python code/RQ3/scripts/run_random218.py     # generate
python code/RQ3/scripts/eval_random218.py    # evaluate in Docker
python code/RQ3/scripts/analyze_random218_results.py  # aggregate
```

The other arms under `code/RQ3/supplement_*` follow the same shape:

| Directory | Arm |
| --- | --- |
| `supplement_2026-09-13/` | `random218_untagged_both` — SPL content with tags stripped |
| `supplement_2026-09-16_full_semantic_218/` | `random218_full_semantic_summary` |
| `supplement_2026-09-19_budget_relaxation_80step/` | 30-task stratified subsample at an 80-step budget |

Each supplement directory carries the copy of the runner it was run with, which
is why the entry points repeat: an arm is comparable to the others only if it
was generated by the code and the prompts that the arm's own directory holds.

The 218 sampled instances are frozen in
`data/RQ3/inputs/unit_manifests_random218/` and are the same for every
arm, including the supplementary ones.

---

## 4. SPL artifacts are prebuilt and must not be rebuilt

`data/*/spl_assets/` holds the SPL the runs consumed, exactly as consumed.
Re-running the builders would produce different text — model sampling is not
deterministic — and every number in [`data/results_tables/`](../data/results_tables/) was measured
against the shipped artifacts. Reproduce by reading these, not by regenerating
them.

For the same reason, the prompts under `data/RQ3/settings/` are frozen
copies: `central_prompts/` holds what each condition received, and
`frozen_original_prompts/` holds the upstream prompt text they were built from.

The code that *builds* SPL is separate from the code that consumes it, and is
shipped under `code/spl_generation/` — the router that turns a repository into
SPL, the symbol index it reads, and the MCP tools it exposes. Building is the
one stage whose output is not shipped as text you can inspect in place, so that
directory is what you would extend to cover a new repository.

---

## 5. A note on costs

Re-running any of the three experiments costs real money at the token volumes
listed in [`data/results_tables/`](../data/results_tables/) — the smallest arm in Experiment 3 is
41.3M tokens. The evaluation stages are free: they run Docker containers against
patches already present on disk, and they are what most re-scoring questions
actually need.

---

## 6. Verifying the package itself

```bash
python code/tools/build_key_checksums.py   # rewrite data/KEY_CHECKSUMS.csv
```

`data/KEY_CHECKSUMS.csv` lists the files the headline numbers depend on — the
result tables, the aggregate records they are computed from, and every run
config under `data/*/settings/` — with size and SHA-256 per file. Re-running
the script and diffing against the shipped CSV reports anything altered among
them; a zip or archive of the package carries its own transport checksums for
everything else.

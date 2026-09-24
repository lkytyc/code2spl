# Provenance

Where the material in this package came from, what was changed on the way in, and
what was deliberately left alone. Paths in this file are relative to the package
root — the directory that holds `code/`, `data/` and `requirements.txt` — unless
they are links, which are relative to this file.

---

## 1. Datasets

The upstream corpora are **not shipped** with the package; every number in it
is recomputable from the frozen records under `data/results/` and
`data/raw_results/`, which need no dataset download. To re-run the prepare or
evaluate stages of Experiments 1 and 2, fetch the two corpora from their
mirrors and place them at the paths the shipped configs name under
`data/datasets/` — the size and SHA-256 below identify the exact files the
reported runs read. No task text, test, gold patch or issue body was edited on
the way in.

### ClassEval (Experiment 1)

| | |
| --- | --- |
| Upstream | <https://github.com/FudanSELab/ClassEval> tag `v1.0.0` |
| Mirror | <https://huggingface.co/datasets/FudanSELab/ClassEval> |
| Paper | <https://arxiv.org/abs/2308.01861> |
| Split | `test` |
| Expected path | `data/datasets/classeval/repo/data/ClassEval_data.json` |
| Size / SHA-256 | 2,345,518 bytes / `50a1ac0e4d0c238573c10c0ab11feae00b14a80ae9e4c9cc28148707ecf0b6a2` |
| Content | 100 classes, 410 methods |

### CoRe (Experiment 2)

| | |
| --- | --- |
| Upstream | <https://github.com/CoReBench/CoRe> |
| Mirror | <https://huggingface.co/datasets/lt-asset/CoRe> |
| Project / paper | <https://corebench.github.io/> / <https://arxiv.org/abs/2507.05269> |
| Expected path | `data/datasets/core/repo/lite.json` |
| Size / SHA-256 | 93,926 bytes / `f7709274b711cee19cb81fdc683dc34c29c88a1e6ed0928d2c27de2a42fabace` |
| Evaluator | ships with the CoRe checkout at `scripts/eval.py`, SHA-256 `69c679a47594e77923278bc2f2a9a272a1877ca597ba24a4c86489cf999df425` |

The corpus is the bundled "lite" snapshot. The upstream commit was not recorded
at collection time, so the checksum above is the authoritative identifier.

### SWE-bench Verified (Experiment 3)

| | |
| --- | --- |
| Dataset | `SWE-bench/SWE-bench_Verified`, split `test` |
| Revision | `91aa3ed51b709be6457e12d00300a6a596d4c6a3` |
| Instances used | 218, sampled once and frozen |

The 218 instances are pinned in
`data/RQ3/inputs/unit_manifests_random218/`. Every arm — the five
compact conditions, the budget-aligned re-run, the untagged arm, the 80-step
subsample and the full-semantic control — draws from that same frozen list.

---

## 2. Environment the runs were made in

| | |
| --- | --- |
| Python | 3.12.12 (conda-forge) |
| OS | Windows 11, build 26200 |
| CPU / RAM | Intel i9-13900H, 20 logical processors / 15.63 GiB |
| Docker | Docker Desktop, Linux containers on WSL2 |

Exact library pins are in [`../requirements.txt`](../requirements.txt). The two that
determine the numbers most are:

* `swebench==4.1.0` — the evaluation harness that decides whether a patch resolves.
* `mini-swe-agent` 2.4.3 — the agent, vendored unmodified under
  `code/third_party/mini_swe_agent/`.

---

## 3. Third-party source shipped in the package

| Directory | Upstream | Notes |
| --- | --- | --- |
| `code/third_party/mini_swe_agent/` | `mini-swe-agent` v2.4.3, <https://github.com/SWE-agent/mini-swe-agent> | verbatim; licence at `repo/LICENSE.md`; `pyproject.toml` SHA-256 `c176ff37a89ee88a2ea2ce746b9b7e723ea3175e53be5336ab99f5aba0d59ddf` |
| `code/spl_generation/` | `Code_SPL` | verbatim, source for the SPL builder |

Neither is patched. If you re-run anything, install the vendored copy rather than
a newer release, or the prompts and agent behaviour will not match the recorded
runs.

---

## 4. What was changed when the package was assembled

The runs were made inside a working tree that used local absolute paths and
internal run identifiers. Those were normalised before shipping. Nothing that
affects a result was altered.

**Layout.** The package holds two directories. `code/` is everything that runs —
the harness per research question, the SPL construction system, the prompt index
and the environment template. `data/` is everything a run reads or produces —
the per-experiment inputs, settings and frozen SPL artifacts, the
per-run records under `data/results/` and `data/raw_results/`, and the headline
tables under `data/results_tables/`. The two vendored third-party checkouts sit inside
`code/` (`code/third_party/mini_swe_agent/`, and `code/spl_generation/Code_SPL/`
for the upstream modules the SPL builder imports); nothing is installed from a
top-level dependencies folder, and `requirements.txt` is the whole environment
apart from those two vendored copies.

**Paths.** Local absolute paths were replaced with `$PROJECT_ROOT` or
`C:\Users\<account>`, including the same path in the three other byte spellings
it occurs in the frozen records (JSON-escaped, JSON-escaped-and-doubled, and the
legacy GBK code page that Windows console tools wrote).

What was replaced is the *absolute* part — the home directory and the path down
to the working tree. What a run wrote *under* it is kept as recorded, because it
is a statement about that run: a captured command line or traceback still reads
`$PROJECT_ROOT\dependencies\third_party\mini_swe_agent\repo\src`,
`$PROJECT_ROOT\experiments\…`, `$PROJECT_ROOT\tools\…` or
`$PROJECT_ROOT\results\reproduced_runs\…`, which is where those runs reached for
things at the time. The names do not resolve against this package, and no re-run
follows them: the code, the vendored checkouts and the run records all live under
the two directories described above, and the configs a re-run *is* given — the
ones under `data/RQ<n>/settings/`, and the six read-path keys of the Experiment 3
per-unit configs, tabulated below — were repointed at this package's layout and
were each checked to resolve. Where a record is a *journal* of a finished run
rather than an input to a re-run, it keeps its own spelling.

`$PROJECT_ROOT` has one meaning in this package: the package root. It is a live
marker, not a placeholder for a human to search and replace. Every value that a
script reads goes through `code/common/env.py`, which expands the marker against
the directory the package sits in (`SPL_PROJECT_ROOT` overrides it if you moved
the tree). Two consequences are worth knowing:

* The marker is *kept* in config values and in records. An absolute path there
  would embed one reader's home directory, and the configs are meant to run from
  wherever the package is unpacked.
* Python sources do not carry the marker inside a path they build themselves —
  they compute the package root from `__file__`. A marker that survived into a
  string join would not be expanded, so the paths a script constructs are
  written as real joins.

Some records still spell the marker with backslashes (`$PROJECT_ROOT\data\…`),
because that is how the value was written when the run captured it. Both
spellings expand to the same directory.

Where the legacy code page had already destroyed the bytes, the home prefix
survived the first pass: 33 console captures under
`data/raw_results/exp1_classeval/*/resource_usage/attempts/` began with
`C:\Users\` followed by four unreadable segments, because the account name and
the working directories under it were written in GBK and came out as replacement
characters. (`PROVENANCE.md` itself is not among them — the examples above in
this paragraph are the placeholder written as text.) A second pass dropped that
head and put `$PROJECT_ROOT` in its place, and pointed the three tails that name
a real file at where the package keeps it: the Code-SPL analyzer prompts, now
`code/spl_generation/Code_SPL/prompt/`; `common/codebleu.py`, now
`code/common/codebleu.py`; and the Experiment 1 `evaluate.py`, now
`code/RQ1/evaluate.py`. Only the path text changed; these are console captures of
finished runs and nothing else in them was touched.

Two of the rewriting rules could match the same absolute path, and each wrote the
marker. That left `$PROJECT_ROOT\$PROJECT_ROOT\` in 7,933 captured console logs
under `data/raw_results/` and the pilot tree that later shipped as
`data/pipeline_checks/` and has since been removed from the package — 22,858
occurrences, all in `.txt` and `.log` files, none in a config, a record or a
source file. The
doubling was the rewriter's own artefact rather than something a run wrote, so it
was collapsed back to one marker, which restores the value the run had printed.

Those lines then read `$PROJECT_ROOT\results\reproduced_runs\<arm>\…`. That inner
name is the working tree's: it is where the run wrote, and the package keeps the
same runs under `data/raw_results/exp3_swebench/<arm>/`, whose per-unit layout
puts the instance one level differently. Rewriting the inner layout would replace
a faithful record with a guess, so it is left as written — the same treatment the
Experiment 1 comparison summary and the Experiment 2 builder configs get below.
No re-run reads these lines; they are the run's own log of what it did.

**Recorded per-unit configs.** The per-unit configs under
`data/raw_results/exp3_swebench/*/configs/` are the one place where the marker keeps
the *working tree's* meaning, because they were written by the launches rather
than by this package. Six of their keys carry a path. Three name something a
re-run **reads**, so each was repointed at where the package keeps the same
material, and the replacement was checked to resolve for all 673 configs — the
658 at the top level of `configs/`, plus the 15 under
`random218_untagged_both/configs/retry_harness_path/`, which an earlier pass had
skipped because it walked only one level down:

| Key | Recorded as | Read from |
| --- | --- | --- |
| `dataset_path` | `$PROJECT_ROOT/precomputed/random218_deepseek-v4-flash/…` | `data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/…` |
| `spl_snapshot_dir` | `$PROJECT_ROOT/spl/random218_deepseek-v4-flash` | `data/RQ3/spl_assets/random218_deepseek-v4-flash` |
| `spl_snapshot_source_dirs` | the same, as a one-element list | the same |

The other three were left exactly as recorded, because for them the recorded
value is what the run *wrote*, not what it read: `run_dir` names where that unit's
results went (and a re-run creates whatever directory it is given), `artifact_dir`
names the unit's prepared context, which is regenerated by a prepare pass rather
than shipped, and `api_key_pool_file` names a pool that is deliberately absent, so
the provider layer falls back to `.env`.

Two kinds of record outside those config directories still quote the working
tree's `spl/`, and both are left as written: the Experiment 1 comparison summary
(`data/results/exp1_classeval/model_comparison/`) records `$PROJECT_ROOT/spl/model_runs/<model>/full100`,
which is `data/RQ1/spl_assets/model_runs/<model>/full100` here, and the captured
Experiment 2 builder shard configs
(`data/RQ2/spl_assets/builder_run_deepseek-v4-flash/_parallel_prepare/`) record
`spl/model_runs/…/artifacts`, `spl/frozen_input_bundles/…` and `spl/s/f341`,
which correspond to `data/RQ2/spl_assets/builder_run_deepseek-v4-flash/artifacts`,
`data/RQ2/spl_assets/frozen_input_bundles/…` and `data/RQ2/spl_assets/full341`. Both are
journals of a run that has already finished and neither is read by a re-run, so
rewriting them would replace a faithful record of where that run wrote with a
guess; the shipped configs a re-run *is* given under `data/RQ<n>/settings/`
resolve against this package as they stand, with the one exception recorded
below. The one place where the same doubt had a consequence — a path the
prepared Experiment 3 units still read — is the table above, and there the
answer was not in doubt, because the target is unique in the package and was
checked to exist.

**The one config that does not resolve.** Nine of the ten configs under
`data/RQ1/settings/configs/` name an SPL artifact directory that is present.
The tenth,
`full100_deepseek-v4-flash_spl_structure_ablation.json`, names
`data/RQ1/spl_assets/model_runs/deepseek-v4-flash-0731/full100`, and no
`deepseek-v4-flash-0731` directory is shipped: the assets present are under
`deepseek-v4-flash/`. The difference is not a spelling of the same thing. That
config is the only one in the package that names a dated model
(`model`, `spl_model` and `summary_model` are all `deepseek-v4-flash-0731`, and
it routes over `openai_raw_http` with `base_url` unset rather than to
`api.deepseek.com`), and it sets `reuse_spl_snapshot`, so it consumed an
existing snapshot rather than building one. The shipped
`deepseek-v4-flash/full100` assets record their own builder in
`spl_metadata.json` as `deepseek-v4-flash`. Repointing the config at them would
therefore substitute one SPL build for another and silently change the arm, so
`artifact_dir` is left exactly as recorded, naming a directory that is not in
the package. Its `run_dir` was repointed, when the records moved, at where the
package keeps them now — `data/raw_results/exp1_classeval/model_runs/deepseek-v4-flash/full100_spl_structure_ablation/`
(see *Package revision* below); a run writes wherever `run_dir` says, so the
repoint changes no recorded value. The tagged-versus-compact comparison for
this model is in those records, and the ablation row in
[`results_tables/`](results_tables/) is computed from them. To re-run this one
arm you must rebuild its SPL snapshot first, which the
same caution applies to as any other rebuild — see §4 of
[`../code/REPRODUCING.md`](../code/REPRODUCING.md).

**JSON escaping in records.** Replacing an absolute path inside a JSON string
first left some records with a lone backslash (`$PROJECT_ROOT\experiments\…`),
which JSON forbids, so those files no longer parsed even though every value in
them was intact. The affected records — 105 of the 42,520 JSON files, all under
`data/raw_results/` and all of them captured tracebacks that quote a path — were
repaired by doubling the offending backslashes, which restores exactly the text
the field was meant to hold, and four files written with a UTF-8 BOM had the BOM
removed. No count, verdict or model output was changed; each file was rewritten
only after the repaired text parsed, and a file that already parsed was not
touched.

**Run identifiers.** Names that recorded a condition being revisited were
replaced with the plain final name — the package reports one final configuration
per condition, so a reader never has to work out which run is authoritative. No
file was dropped in the process: the final version of every dataset, config,
artifact and record is present.

**Protocol labels.** The internal name of the guarded SPL protocol was replaced
with `spl_guarded_protocol` throughout, including inside the frozen records that
quote it.

**Narrative documents.** Explanation and analysis write-ups are not part of a
materials package and are not included. The data they were derived from is, and
[`results_tables/`](results_tables/) reproduces every number they reported.

**Credentials.** No API key, key-pool file or other credential is included
anywhere in the package: the pool of keys the runs were spread across lived in a
file outside every shipped tree, and no copy of it was kept. What a shipped
config states is where the pool *was* (`api_key_pool_file`) and which environment
variable holds a key (`api_key_env`). On a re-run the pool file is not there, and
the harness falls back to the keys you put in `.env` — one key is enough for a
sequential run, and `OPENAI_API_KEYS` takes several for a parallel one. The
fallback is not a special case bolted onto the package: `ModelClient.get_key_pool`
in `code/common/providers.py` implements it for every stage, and `code/RQ3/run.py`
uses the same path.

The hosted OpenAI-compatible gateway the Claude and GPT runs went through is
named nowhere in the package, because its host is the authors' account. The
endpoints that are public (`api.deepseek.com`, `api.scnet.cn`) are given in
`code/.env.example`; for the rest, any gateway serving those model names will do, and
each config's own `base_url` still wins over the environment.

**Package revision (2026-09-24).** The package was slimmed and its names
aligned with the paper's five-model evaluation. Removed: the upstream dataset
corpora (§1 now says where to fetch them), the Experiment 3 pipeline pilot, the
launcher scratch logs, the dated six-model snapshot that sat under
`data/results/exp1_classeval/model_comparison/supplement_2026-09-11/` (the
five-model final files it duplicated remain at `model_comparison/`), the
six-model significance record `exp1_six_model_significance.json`, and a
byte-identical accidental duplicate of the flash SPL assets that sat at
`data/RQ1/spl_assets/model_runs/model_runs/`. The retired model
`claude-opus-4-7` was dropped from the Experiment 1 aggregate JSONs under
`model_runs/`; every per-instance record of the five reported models is
untouched. Names were unified with the paper: the flash structure-ablation
records moved from `model_runs/deepseek-v4-flash-0731/` into
`model_runs/deepseek-v4-flash/full100_spl_structure_ablation/`, matching the
layout of the other four models, and the three Exp1 supplements now sit at
`data/results/exp1_classeval/supplements/` (`api_fidelity/`,
`evaluation_reval/`, `opus5_free_summary_check/`). The endpoint id
`deepseek-v4-flash-0731` remains recorded verbatim wherever it is a record of
what was called — the config's `model` fields and the per-call metadata — not a
name for a reader to navigate by. The headline CSVs were renamed after the
tables they feed: `table1_rq1_classeval_main.csv`, `table2_rq2_core_main.csv`,
`table3_rq3_swebench_main.csv` (paper Tables 1–3) and
`tableC1_rq1_structure_ablation.csv` (Appendix C.1); the two CSVs with no
one-to-one table kept their names. Regenerating the tables after the revision
reproduced every number; the only cell that changed anywhere is the model
column of the two flash rows in the ablation table, which now reads
`deepseek-v4-flash` instead of the dated endpoint id. The per-file manifest of
the whole tree (`data/MANIFEST.csv` and its verifier `verify_manifest.py`) was
dropped in the same revision: `data/KEY_CHECKSUMS.csv` covers every file the
headline numbers rest on, and an archive of the package carries its own
transport checksums for the rest. Four of the paper's figures (paper Figs. 1,
2, 4, 5) were rendered from the submission's PDF figures to
`docs/figures/*.png` for the README; the paper's LaTeX sources themselves are
not part of this package. Experiment 3's prepare-stage working tree
(`data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/working/round_01/`,
~3.3k per-instance scratch directories) was dropped as well: it is rebuilt by
`code/RQ3/scripts/prepare_random218.py`, which writes that path, and the
delivered arm records under `data/raw_results/exp3_swebench/` are the evidence
the paper rests on. Anything that reads the working tree must therefore run
prepare first — notably the supplementary check
`code/RQ3/supplement_2026-09-13/untagged_arm/_verify_against_delivered.py`,
whose `SAMPLES_DIR` points into it. The run's own configs, status, report and
logs stay at `data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/`.

**Run-record trim (2026-09-24, second pass).** To bring the per-file count
down for upload, the per-run bookkeeping was dropped from the Experiment 3
arm records and the asset trees: the pipeline `execution/*.log` and
`*.traj.progress.log` logs, the per-condition scaffolding files
(`baseline_status.json`, `condition_complete.json`, `handoff.json`,
`mode.txt`, `command_00.txt`, `stdout_00.txt`, `stderr_00.txt`), the per-unit
copies of the SWE-bench evaluation dataset (`swebench_eval_dataset.jsonl` —
211 distinct contents copied once per condition), the per-run
`mini_config.yaml` snapshots, and the per-condition `payload_tools/` copies
(the three tool scripts, `spl_index.json`, `spl_context.txt`, `patch_plan.md`,
`source_bound_cards.md`) — 29,764 files plus the directories they emptied.
None of it is evidence: the agent's full conversation lives on in the
`*.traj.json` trajectories, the patches, the `call_metadata.json` records and
the per-run aggregates, all untouched. The scaffolding and payloads are
materialised by the run stages (`code/RQ3/run.py` and the supplement runners
write them), so the supplementary audit scripts that expect a full run tree
(`_fairness_audit.py`, `analyze_unstructured_both_card_order.py`,
`_verify_against_delivered.py`) were run while the tree was complete and must
regenerate those files before running again. No file covered by
`data/KEY_CHECKSUMS.csv` was touched — regenerating it after the trim
reproduced it byte for byte, and `build_tables.py` still reproduces every
paper number.

---

## 5. What was deliberately not changed

**Upstream text, including its language.** Some SWE-bench issue bodies, ClassEval
fixtures and recorded model outputs contain Chinese, because the upstream dataset
or the model produced it. That is evidence about the task and about model
behaviour; rewriting it would falsify the record, so it is left exactly as
recorded. The English-only rule applies to material we authored.

**Per-instance evidence.** Every trajectory, patch, command log, stdout/stderr
capture and evaluation verdict is shipped as written by the harness. The record
counts in [`results_tables/`](results_tables/) are derived from these files and can be
re-derived from them.

**Counts and usage.** Token accounting, call counts, costs, timings and failure
records are complete and unedited, including the arms that record no cost figure
and the units that produced no patch. Where a figure was not measured, the
package says so rather than substituting a zero.

---

## 6. Verifying the package

```bash
python code/tools/build_key_checksums.py
```

`data/KEY_CHECKSUMS.csv` covers the files the headline numbers depend on: the
result tables, the aggregate records they are computed from, and every run
config under `data/*/settings/`. It is written by the script, not by hand;
re-running it and diffing against the shipped CSV reports anything altered
among those files. An earlier revision also shipped a per-file manifest of the
whole tree (`data/MANIFEST.csv`, with `verify_manifest.py`); it was dropped in
the 2026-09-24 revision — see §4 — because the key checksums cover the
evidence and an archive of the package carries its own transport checksums.

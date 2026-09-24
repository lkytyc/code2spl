# Experiment 3: the tag-stripped arm

This directory holds the code that runs `miniswe_spl_unstructured_both` — the
arm that delivers SPL content to the agent with the tags removed. It is what
separates the contribution of the tag structure from the contribution of the
content, and it is the arm reported as `random218_untagged_both`.

| Path | Role |
| --- | --- |
| `untagged_arm/spl_unstructured.py` | Token stripping and auditing: `neutralize` (rewrites tags by scope), `strip_checkpoint`, `to_unstructured`, `tag_hits`, `residual_spl_mentions`, `assert_clean`. Pure functions, no side effects. |
| `untagged_arm/run_unstructured.py` | Imports `run.py`, replaces its renderer with the implementation above, then calls the shared `main()`. |
| `untagged_arm/scripts/run_unstructured_218.py` | Launcher for the 218 units (agent stage / evaluation stage / status). |

The shared runner is `code/RQ3/run.py` and is the same file the other
five compact-arm conditions use. The arm is wired in at runtime rather than by a
second copy of the runner, so the code path the five other conditions exercise is
the one that was measured; the SHA-256 of every file here is recorded in
`data/MANIFEST.csv`.

## Running it

```bash
# 1) build the 218 configs for this arm
#    (they differ from the compact arm's only in routing keys:
#     conditions / tags / run_dir)
python untagged_arm/_make_unstructured_configs.py

# 2) agent stage (one process per unit; completed units are skipped)
python untagged_arm/scripts/run_unstructured_218.py run

# 3) official harness evaluation
python untagged_arm/scripts/run_unstructured_218.py eval

# 4) status
python untagged_arm/scripts/run_unstructured_218.py status
```

On Windows the launcher sets `EXP6_WINDOWS_SHORT_PROJECT_ROOT=C:\e` itself.
Instance names of `scikit-learn__scikit-learn-*` and `matplotlib__matplotlib-*`
push harness result paths past MAX_PATH, and without the short root the run
fails before the first test.

## Analysis, audit and verification scripts

| Script | Output |
| --- | --- |
| `untagged_arm/scripts/analyze_unstructured_both_results.py` | `final_analysis_unstructured_both.json`: per-condition metrics, Wilson intervals, paired exact McNemar, Holm correction; also recomputes the compact arm's pairwise comparisons as a regression self-check |
| `untagged_arm/scripts/analyze_unstructured_both_patches.py` | `patch_identity.json`: newline-normalized md5 of each condition's patch, and the same/different-patch × verdict matrix |
| `untagged_arm/scripts/analyze_unstructured_both_card_order.py` | `card_order_audit.json`: whether the order and roles of the cards bound by the two arms agree |
| `untagged_arm/_fairness_audit.py` | `fairness_audit.json`: per-unit comparison of everything agent-visible in the two arms (text, JSON, tool scripts), with budget, card selection, matched terms, editable source fragments and config routing keys listed separately |
| `untagged_arm/_audit_unstructured_prompts.py` | `prompt_leakage_audit.json`: scans the delivered first user message for leaked tag tokens, SPL vocabulary and reading-protocol wording; the tagged arm is the positive control |
| `untagged_arm/_verify_against_delivered.py` | `verify_against_delivered.log`: rebuilds each unit's payload with the current code and compares it byte-for-byte against the `payload_tools/` delivered at run time |
| `untagged_arm/_snapshot_path_failures.py` | `harness_path_failures_before.json`: the raw record of the over-long-path rows, tracebacks included, taken before the evaluation re-run |
| `untagged_arm/_retry_harness_path_failures.py` | `configs/retry_harness_path/*.json`: rewrites `smoke_run_id` and re-runs the harness (see below) |
| `untagged_arm/_report_retry_outcome.py` | `harness_path_retry.json`: per-unit before/after comparison of the re-run |
| `untagged_arm/_drybuild_unstructured.py`, `untagged_arm/_norm_drybuild_tree.py` | Prompt construction and normalized comparison with no model calls and no containers |

`_verify_against_delivered.py` is the strongest of these: it does not ask whether
the code should be unchanged, but whether it still reproduces the bytes that the
scored run actually emitted.

## Known nondeterminism in the shared runner

`run.py:score_spl_entry` collects matched terms into a `set` and then takes
`matched[:12]`:

```python
for term in terms:            # terms is a set; iteration order follows the
    ...                       # process's string hash seed
    matched.append(...)
...
copied["_spl_matched_terms"] = matched[:12]
```

Two runs of the same binary may therefore retain a different set of twelve
terms. That propagates through `spl_card_role`, which reads
`_spl_matched_terms` to decide whether the constructor was downgraded, and so to
card roles and order. Measured on 24 `PYTHONHASHSEED` values with only the
shared runner loaded, 20 produced one card order and 4 the other.

In practice this affects 1 of 217 units: `django__django-11532` differs in card
order — three cards, two source fragments, all content identical, only the order
and role labels differ. Both arms carry the same behaviour, and
`card_order_audit.json` records the check.

## Harness path failures and their re-run

After the first evaluation round, 15 of the 218 units had a patch but no verdict.
All were `scikit-learn`, and the traceback gave the sole reason:

```
FileNotFoundError: [WinError 206] The filename or extension is too long.:
'logs\run_evaluation\<run_id>\<mode>\<instance_id>'
```

The harness working directory is `common.paths.PROJECT_ROOT` and it builds a
per-instance log directory from `run_id = <smoke_run_id>_<mode>_<instance_id>`.
This arm's `smoke_run_id` is five characters longer than the compact arm's, which
put these 15 units over the Windows path limit before the first test ran. The
split is clean: all 180 evaluated units have relative path lengths ≤ 197, and all
15 failures are exactly 209.

Outside a config, `smoke_run_id` is read in one place, `evaluate.py:428`, to name
the harness run. `run.py`, the agent prompt and the delivered payload never read
it. The repair follows the practice already used elsewhere in this codebase —
replace `smoke_run_id` with `"h" + sha256(original)[:12]` and re-run — and applies
it only to those 15 units, in `configs/retry_harness_path/`, overwriting no unit's
config.

Result: all 15 obtained a verdict (13 resolved, 2 genuine test failures) and
coverage went from 180/195 to 195/195. No other unit's row changed;
`harness_path_retry.json` records the per-unit before/after check.

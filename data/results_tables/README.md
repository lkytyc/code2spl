# result tables

Machine-readable headline tables. These are the numbers in the paper; the
per-instance evidence behind them is under `data/results/` and `data/raw_results/` and does
not need to be opened to use anything here.

Regenerate all six from the frozen records:

```bash
python code/tools/build_tables.py
```

The script reads only files inside this package. It cross-checks the SWE-bench
rows against the frozen analyses that shipped with the runs and prints
`cross-checked 6 frozen rows, 0 mismatch(es)` when they agree.

The tables below are the results: every headline figure in the paper is a cell in
one of them, and the conventions the counting follows are set out after the
column list.

---

## How to read the numbers

**Counts versus rates.** A task is *sampled* whether or not its run produced a
usable output. An arm that failed to produce a patch on 25 of 218 tasks has
sampled 218 and evaluated 193. Both denominators are reported
(`resolved_rate_of_sampled`, `resolved_rate_of_evaluated`) so a condition cannot
look better by failing more often.

**Calls.** `llm_calls` is the count from `usage_summary.json`: every request the
run made, including retries and auxiliary traffic. The priced ledger
(`cost_summary.json`, `llm_usage_calls`) counts only requests attributable to a
priced model and is smaller; where the two differ, these tables use the
`usage_summary` figure because that is what the run reports quote.

**Tokens.** Input, output and reasoning tokens are reported separately and never
summed into one figure in the source records. `total_tokens` is the harness's own
total for the condition. For SPL conditions this includes the SPL text carried in
each prompt; one-time SPL construction is accounted separately and is not folded
into per-task inference.

**Cost.** Cost is priced from the recorded token counts. Where the run carried no
price for a model, the cell is empty rather than zero — empty means *not
measured*, not *free*.

---

## table1_rq1_classeval_main.csv

Paper Table 1. Experiment 1, one row per model and
condition. 20 rows.

| Column | Meaning |
| --- | --- |
| `model` | the model that wrote the class |
| `condition` | what it received: `free_summary`, `skeleton_holistic`, `spl_only`, `skeleton_spl` |
| `samples` | tasks attempted (100) |
| `syntax_passes` / `syntax_pass_rate` | generated code that parses |
| `class_passes` | tasks where the class passed its own tests |
| `valid_evaluations` | 100 minus the tasks whose gold solution failed, so no run can be credited or blamed for them |
| `valid_class_pass_rate` | `class_passes / valid_evaluations` — the rate quoted in the paper |
| `method_tests_passed` / `method_tests_total` | individual method tests, out of 410 |
| `method_test_pass_rate` | `method_tests_passed / method_tests_total` |
| `avg_codebleu` | mean CodeBLEU against the reference class |

## exp1_classeval_run_totals.csv

No single paper table: the per-model totals behind the
Appendix G.1/G.2 usage tables. One row per model. Calls, tokens and cost were recorded per model run, not per
condition, so they live here rather than repeated down the table above.

| Column | Meaning |
| --- | --- |
| `llm_calls` | every request the run made, including retries and SPL construction |
| `total_tokens` | input plus output plus reasoning, as the harness totalled them |
| `llm_cost_usd` | priced from the recorded tokens; empty where no price was attached |
| `pipeline_wall_seconds` | wall-clock for the whole model run |

## exp1_classeval_significance.csv

The pre-specified paired comparisons behind the RQ1
significance claims. 20 rows: four SPL-vs-baseline contrasts per
model, two-sided exact McNemar on paired task outcomes, Holm-corrected within
model.

| Column | Meaning |
| --- | --- |
| `test` | which contrast |
| `spl_condition` / `baseline_condition` | the two arms compared |
| `paired_samples` | tasks scored under both arms |
| `both_pass` / `both_fail` | concordant pairs |
| `spl_only_pass` / `baseline_only_pass` | discordant pairs — the ones the test uses |
| `spl_passes` / `baseline_passes` | raw totals |
| `absolute_difference_percentage_points` | net pass difference, in points |
| `p_value_raw` / `p_value_holm` | before and after Holm correction within model |
| `significant_holm_0_05` | the corrected verdict |

## tableC1_rq1_structure_ablation.csv

Paper Appendix Table C.1. Tagged SPL versus the same
content with tags stripped. 10 rows, two conditions per model.

| Column | Meaning |
| --- | --- |
| `tagged_condition` / `compact_condition` | the two arms |
| `n_raw`, `*_passes_raw`, `delta_raw`, `mcnemar_p_raw` | over the full 100-task sample |
| `n_valid`, `*_passes_valid`, `delta_valid`, `mcnemar_p_valid` | restricted to valid evaluations |

Read the raw block for the ablation: restricting to valid evaluations drops tasks
where the gold solution itself failed, which matters here because the two arms of
a comparison are different *runs* of the same tasks.

## table2_rq2_core_main.csv

Paper Table 2. Experiment 2, one row per run and
condition. 5 rows.

| Column | Meaning |
| --- | --- |
| `run` | the run directory: `deepseek-v4-pro_full341_thinking`, `deepseek-v4-pro_full341_unstructured_summary` or `deepseek-v4-pro_verify_rules` |
| `condition` | what the model received |
| `outputs` / `parsed` / `parse_success_rate` | responses and how many yielded a parsable answer |
| `correct` / `strict_correct` | strict scoring counts an answer only if it matches the reference exactly |
| `strict_overall_accuracy` | over `outputs`, not over `parsed` |
| `data_correct` / `data_total` and the `control` pair | stratified results; the `infoflow` pair also has `infoflow_strict_accuracy` |
| `llm_calls`, `*_tokens`, `elapsed_seconds` | usage for that run and condition |
| `total_cost_usd` | priced from the recorded tokens |
| `cost_per_correct_usd` | cost divided by strict-correct answers |

## table3_rq3_swebench_main.csv

Paper Table 3. Experiment 3, one row per arm and
condition. 14 rows — five arms.

| Column | Meaning |
| --- | --- |
| `arm` | `random218_compact`, `random218_budget_aligned`, `random218_untagged_both`, `budget_relaxation_80step_stratified30`, `random218_full_semantic_summary` |
| `condition` | the agent variant under test |
| `tasks_sampled` | 218 for the full arms, 30 for the stratified subsample |
| `patches_generated` | units where the agent produced a patch |
| `evaluated` | units the SWE-bench harness could score |
| `unavailable` | units with no usable baseline, so no verdict is possible |
| `resolved` | units whose patch passed the instance's FAIL_TO_PASS and PASS_TO_PASS tests |
| `resolved_rate_of_sampled` | `resolved / tasks_sampled` — the conservative rate |
| `resolved_rate_of_evaluated` | `resolved / evaluated` — the rate that would flatter an arm which failed to produce patches |
| `llm_calls`, `input_tokens`, `output_tokens`, `reasoning_tokens`, `total_tokens` | summed over every unit in the arm |
| `elapsed_hours` | wall-clock, summed over units; units ran concurrently |
| `total_cost_usd` | priced from the recorded tokens; empty for the 80-step arm, which recorded no price |

`tasks_sampled = resolved_total + unavailable_outputs`. A unit whose baseline
could not be established is an unresolved task, not a missing one — counting it
as missing would let an arm improve its rate by failing more often.

---

## Reading the two rates

`resolved_rate_of_evaluated` is the right column when comparing against published
SWE-bench numbers, which usually report over evaluated instances.
`resolved_rate_of_sampled` is the right column for comparing the arms here,
because the arms differ in how many patches they manage to produce and the
point of the comparison is end-to-end task success. The figures in the paper
quote `resolved_rate_of_sampled`.

---

## Where the paired statistics live

The tables here report counts and rates. The paired statistics behind them —
gains, losses, both-pass, neither-pass, net, McNemar p, Holm correction — are in
the frozen analyses the runs produced, not restated here:

| Analysis | File |
| --- | --- |
| SWE-bench compact arms | `data/results/exp3_swebench/random218_compact/final_analysis.json` |
| SWE-bench untagged arm | `data/results/exp3_swebench/random218_untagged_both/final_analysis_unstructured_both.json` |
| 80-step study | `data/results/exp3_swebench/budget_relaxation_80step_stratified30/budget80_summary.json` |
| ClassEval | `data/results/exp1_classeval/model_comparison/exp1_full100_significance.csv`, `exp1_model_significance.json` |
| Core reasoning | `data/results/exp2_core/*/enhanced_statistics.json` |

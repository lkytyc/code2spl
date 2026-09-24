# Experiment 2 Method Projects

Each directory here is one core-reasoning condition. A complete method project
holds `method.yaml` (the condition, its base config, and the scripts it drives),
`prompts/prompt.md` (the template the model receives) and `src/`.

Run these from the package root, one condition at a time:

```powershell
python code\RQ2\methods\official_raw\run.py --phase run,evaluate
python code\RQ2\methods\raw_free_summary\run.py --phase run,evaluate
```

Each method writes its resolved config to `last_resolved_config.json` in its own
directory and its outputs under `work/`, which is not part of the shipped
package. `--dry-run` prints the commands instead of running them.

## Preparing the shared artifacts first

All conditions share one prepared input set:

```powershell
python code\RQ2\prepare.py --config data\RQ2\settings\configs\full341_deepseek-v4-pro.json
```

`data\RQ2\settings\configs\` holds the three configs the reported runs used:
the tagged-SPL run (`full341_deepseek-v4-pro.json`), the untagged
control (`full341_deepseek-v4-pro_unstructured_summary.json`) and the 52-sample rule
check (`verify_rules_deepseek-v4-pro.json`). Running a config directly is equivalent:

```powershell
python code\RQ2\run.py --config data\RQ2\settings\configs\full341_deepseek-v4-pro.json
python code\RQ2\evaluate.py --config data\RQ2\settings\configs\full341_deepseek-v4-pro.json
```

## The two SPL conditions

`raw_spl_atomic_strict` and `raw_spl_unstructured_summary` hold the prompt text
for those two conditions but no `method.yaml` or runner of their own: the SPL
layer is applied inside `code\RQ2\run.py` from the artifact and protocol keys of
the config, so they are run through the configs above rather than as standalone
method projects. Their `prompts/` directories are shipped so the prompt text the
conditions used is in one place.

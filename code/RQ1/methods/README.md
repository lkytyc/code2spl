# Experiment 1 Method Projects

Each directory here is one ClassEval reconstruction condition, packaged so it can
be run on its own: `method.yaml` names the condition and the scripts it drives,
`prompts/prompt.md` is the template the model receives, and `src/` holds the
condition-specific generation code.

## Protocol roles

ClassEval's official holistic, incremental, and compositional strategies describe
how code is generated from the official class skeleton. The `free_summary`
condition is not one of those strategies. It is a project-specific
representation control: an LLM first converts the reference class into an
unstructured natural-language summary, and another generation call reconstructs
the class from that summary.

The model-facing summary prompt contains only task-relevant instructions. The
condition and protocol are both named `free_summary`; a prompt SHA-256 is stored
in metadata solely to prevent reuse of artifacts built with a different prompt.

## Running one condition

Run these from the package root. One condition at a time:

```powershell
python code\RQ1\methods\spl_only\run.py --phase run,evaluate
python code\RQ1\methods\skeleton_spl\run.py --phase run,evaluate
```

Each method writes its resolved config to `last_resolved_config.json` in its own
directory and its outputs under `work/`, which is not part of the shipped
package. Pass `--dry-run` to print the commands without running them, and
`--config <file>` to run against a different base config.

## Preparing the shared artifacts first

The conditions share one prepared input set and one set of summaries. Build them
once, before the method-level runs:

```powershell
python code\RQ1\prepare.py --config data\RQ1\settings\configs\full100_deepseek-v4-pro.json
python code\RQ1\generate_free_summary.py --config data\RQ1\settings\configs\full100_deepseek-v4-pro.json
```

The `--config` file decides the model, the sample set and the artifact
directory; the four conditions are then generated from those artifacts, so any
`full100_<model>.json` under `data\RQ1\settings\configs\` works here.

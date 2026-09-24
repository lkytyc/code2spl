# Experiment 3 — run notes for the 218-instance arm

## Sample

218 SWE-bench Verified instances drawn algorithmically (Cochran finite population
correction, seed 20260531, ε = 0.05, 95% confidence, N = 500). The frozen list is
`../inputs/unit_manifests_random218/`.

## Conditions

| Condition | What the agent receives |
| --- | --- |
| `miniswe_original` | the upstream mini-swe-agent prompt, unmodified |
| `miniswe_free_summary` | a prose summary of the relevant code |
| `miniswe_spl_localization` | SPL restricted to locating the edit site |
| `miniswe_spl_repair` | SPL oriented to the repair itself |
| `miniswe_spl_both` | the full SPL pipeline |

The three SPL conditions run under the guarded protocol
(`spl_guarded_protocol`): each SPL card states explicitly that it describes what
the code does and must not be copied into a patch. The protocol also carries the
`repair_acceleration_hint` variable-lifetime fix.

## Models

Agent: `deepseek-v4-pro`. SPL and summary construction: prebuilt with
`deepseek-v4-flash` and reused, not rebuilt — see `../spl_assets/`.

The SPL assets are 218 prebuilt items. The sample files point directly into
`../inputs/precomputed_random218_deepseek-v4-flash/working/round_01/<instance>/`.

## Constraints

1. **Do not modify the original system.** Work only inside the package copy.
2. **Do not rebuild SPL.** The SPL context (`spl_context.txt`, `spl_index.json`)
   and the summary (`free_summary_context.txt`) are prebuilt; reuse them as they
   are. Regenerating them produces different text and invalidates the recorded
   numbers.

## Output locations

| Kind | Path |
| --- | --- |
| Per-unit config | `configs/unit_NNN_<instance>.json` (218 files) |
| Manifest | `../inputs/unit_manifests_random218/unit_NNN_<instance>/manifest.json` |
| Patch | `units/unit_NNN_<instance>/runs/<instance>/<condition>/patch.diff` |
| Run logs | `execution/` |

Credentials are not stored: configs name the environment variable to read
(`api_key_env`) and set the value to `null`.

## How the arm was run

```powershell
# generate patches (no evaluation, no image pre-pull)
python code/RQ3\scripts\run_random218.py run

# a specific subset
python code/RQ3\scripts\run_random218.py run unit_001_pydata__xarray-3151 unit_002_sphinx-doc__sphinx-9229

# progress
python code/RQ3\scripts\run_random218.py status
```

Within each unit the five conditions run concurrently at `max_workers=4`; units
run three at a time by default, adjustable through `TOP218_MAX_WORKERS`.

Docker images are pulled on demand, with the pre-pull timeout raised to 1800 s in
the config so that a first pull does not trip the default 60 s limit.

Re-running resumes rather than restarts: completed conditions are detected and
skipped.

Evaluation (the SWE-bench harness) and the pre-pull of the 218 evaluation images
are separate steps, run on demand — see
[`../../REPRODUCING.md`](../../REPRODUCING.md).

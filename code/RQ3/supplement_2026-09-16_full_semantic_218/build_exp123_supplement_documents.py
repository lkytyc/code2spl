"""Write the final Experiment 3 supplement and the combined Exp1--3 document.

This script writes documentation only.  It neither calls a model nor changes
the frozen experiment outputs.  The package copy is performed separately so
the document can precisely state what is and is not included.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # the package's code/ directory
from common.env import expand  # noqa: E402


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
PACKAGE = PROJECT / "spl_reproducibility_package"
RUN = Path(expand("$PROJECT_ROOT/data/raw_results/exp3_swebench/random218_full_semantic_summary/runs"))
EXP3_SOURCE_DOC = RUN / "exp3_full_semantic_summary_supplement_20260916.md"
EXP3_PACKAGE_DOC = PACKAGE / "exp3_swebench/documentation/exp3_full_semantic_summary_supplement_20260916.md"
EXP1_DOC = PACKAGE / "exp1_classeval/documentation/exp1_supplement_report.md"
EXP2_DOC = PACKAGE / "exp2_core/documentation/exp2_supplement_report.md"
COMBINED = PACKAGE / "supplement_experiments_1_2_3_overview.md"
PACKAGE_README = PACKAGE / "README.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def exp3_document() -> str:
    return """# Experiment 3 Supplement Notes: Flattening Full Semantics into Ordinary Natural Language

## 1. Purpose and conclusion

This supplementary experiment tests a strict counterfactual: if we keep the behavioral facts contained in the frozen function-level SPL but remove the Worker structure, the field tags, function-level on-demand reading, issue-relevant localization, and the SPL-specific execution strategy, rewriting all behavioral facts as ordinary natural language and appending them in one shot to the agent's initial prompt — does the benefit still hold?

The final answer is no. On the 218 frozen SWE-bench Verified instances this condition resolved **100/218 (45.9%)**, below Original's **114/218 (52.3%)**; it also consumed **132,134,648** inference tokens, above Original's **76,390,942**. This experiment therefore does not support the claim that "writing more behavioral semantics into the prompt in one shot can replace SPL".

This conclusion applies only to the combined ablation of "unstructured, retrieval-free, routing-free full-semantic flattening", and does not imply that natural-language behavioral semantics is itself ineffective.

## 2. Setup matched to the original experiment

- Data: the 218 SWE-bench Verified instances frozen by the original Experiment 3; instance IDs, source snapshots, and the existing SPL index are not rebuilt.
- Model: `deepseek-v4-pro`, temperature = 0, max output 8192 tokens.
- Agent limits: Mini-SWE-Agent v2, 36-step limit, 1200 s wall-time, 2400 s command timeout, Docker container limit 2 hours.
- Concurrency: 4 agent work items; the official SWE-bench harness runs single-worker.
- Control: the saved `miniswe_original` outputs; Original is not re-invoked.
- Official verdict: counted as resolved only when all FAIL_TO_PASS pass and all PASS_TO_PASS pass.

Apart from the treatment text described below, the new condition is generated from the `miniswe_original` agent configuration, with no source excerpting, keyword search, relevance ranking, first command, repair plan, or SPL-specific progress rule added.

## 3. Actual injection mechanism

Each instance reads **all** function entries of the frozen `spl_index.json` and converts them into ordinary sentences in the file's existing order. For example:

```text
In django/forms/models.py, ModelForm.__init__ initializes ...
While ModelForm.__init__ runs, it will ...
```

File names and function names therefore still appear in natural-language form, which is a weak lexical association; but there is no `Worker` boundary, no `INPUTS`/`MAIN_FLOW`/`OUTPUTS` hierarchy, no function cards, no per-function retrieval, and no issue-to-function routing. All converted paragraphs are appended in one shot to `instance_template` before the agent starts, and are not expanded on demand afterwards.

Semantic context size (this appended text only): median 10,290 tokens, mean 17,576 tokens, max 104,889 tokens. For `django__django-14725`, for example, 58 functions and 499 sentences were injected, totaling 21,846 tokens.

## 4. Final results

| Condition | resolved / 218 | resolved rate | submitted patches / 218 | total inference tokens |
|---|---:|---:|---:|---:|
| `miniswe_original` | 114 | 52.3% | 140 | 76,390,942 |
| `miniswe_free_summary` | 118 | 54.1% | 140 | 78,098,072 |
| `miniswe_spl_localization` | 141 | 64.7% | 194 | 42,852,228 |
| `miniswe_spl_repair` | **143** | **65.6%** | 190 | 46,051,675 |
| `miniswe_spl_both` | 138 | 63.3% | 193 | 43,637,276 |
| `miniswe_full_semantic_summary` (this supplement) | 100 | 45.9% | 120 | 132,134,648 |

Relative to Original, this supplement condition solved 14 fewer cases (-6.4 percentage points), submitted 20 fewer patches, and consumed 55,743,706 more tokens (+73.0%). Model calls fell from 5,242 to 4,138, but the average token burden per call rose from about 14.6k to about 31.9k.

Among submitted patches, this condition resolved 100/120 = 83.3%, versus Original's 114/140 = 81.4%. This is only a descriptive condition rate, and the two submission subsets are not the same; it suggests that the overall decline mainly shows up as the agent more often failing to form or submit a patch, rather than a marked deterioration in the average harness pass rate of submitted patches.

The 98 no-patch trajectories of this condition include: 51 `LimitsExceeded`, 8 `RepeatedFormatError`, 5 `TemplateSyntaxError`, 2 `TimeExceeded`, and 32 runs that never formed a final submission.

## 5. Interpretation and reportable conclusion

The result is consistent with the following mechanism:

1. the full semantic text duplicates the source code, and every turn carries a long context;
2. a large number of function facts irrelevant to the current issue dilute attention;
3. function names do appear, but the explicit organization of Worker, interface, flow, and output relationships is missing;
4. the model has no "localize first, then read the relevant function" access strategy and cannot turn the semantic context into an actionable repair chain.

The paper can state it as: the benefit of structured SPL comes not from merely adding natural-language explanation, but from **the behavior organization of function binding** and **the way these behavioral semantics are invoked according to task relevance**. It should not be stated as "the more natural-language semantics, the worse", nor should this supplement condition be called a function-bound unstructured SPL.

## 6. Docker interruption and recovery audit

During the initial generation stage Docker Desktop was closed, and 85 instances exited before `docker run` could start the agent. They were initially misrepresented as having no patch, so the old `56/218` summary is invalid and must not be used in the paper.

The recovery process re-ran only those 85 instances carrying `CalledProcessError` and `docker run` evidence; the 133 already-normal agent results were not re-run. The interruption records and old reports were copied to `semantic_docker_snapshot_20260916_091601/`. After recovery all 218 agent outputs were complete, the official harness was re-run on all 120 submitted patches, and the full `evaluation.json`, metrics, and comparison reports were rebuilt. The final result is the 100/218 in the table of this document, with 0 missing evaluations.

## 7. Main reproducible materials

Run scripts:

- `flat_semantic_prose.py`
- `run_full_semantic_summary.py`
- `prepare_full_semantic_summary_218.py`
- `prepare_full_semantic_docker_recovery.py`
- `prepare_full_semantic_recovery_evaluation.py`
- `summarize_full_semantic_summary_218.py`

Key results:

- `original_vs_full_semantic_summary.json`
- `original_vs_full_semantic_per_instance.csv`
- `evaluation.json`
- `metrics_by_mode.json`
- `full_semantic_material_audit.json`
- `preflight_audit.json`

Running this depends on Docker and an external API, but Docker images, containers, caches, and real API keys are not part of this reproducibility package; the frozen configs, code, input manifests, outputs, trajectories, evaluation results, and interruption-recovery snapshots are all saved.
"""


def write_documents() -> None:
    text = exp3_document()
    for path in (EXP3_SOURCE_DOC, EXP3_PACKAGE_DOC):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    if not EXP1_DOC.is_file() or not EXP2_DOC.is_file():
        raise FileNotFoundError("The frozen Experiment 1/2 supplement documents are required.")
    exp1 = EXP1_DOC.read_text(encoding="utf-8")
    exp2 = EXP2_DOC.read_text(encoding="utf-8")
    combined = """# Combined Supplement Notes for Experiments 1, 2, and 3

## How to read this

This file consolidates the three formal supplementary-experiment notes in the current reproducibility package. The Experiment 1 and Experiment 2 texts are included verbatim from the frozen versions; Experiment 3 uses the final version of 2026-09-16, with the invalid temporary 56/218 summary produced during the Docker interruption excluded. Detailed raw results, code, configs, and per-instance outputs for the three experiments are stored in the package's `exp1_classeval`, `exp2_core`, and `exp3_swebench` directories respectively.

---

## Part 1: Experiment 1 Supplement Notes (frozen version)

""" + exp1 + "\n\n---\n\n## Part 2: Experiment 2 Supplement Notes (frozen version)\n\n" + exp2 + "\n\n---\n\n## Part 3: Experiment 3 Supplement Notes (final version)\n\n" + text
    COMBINED.write_text(combined, encoding="utf-8", newline="\n")

    manifest_sources = [
        RUN / "original_vs_full_semantic_summary.json",
        RUN / "original_vs_full_semantic_per_instance.csv",
        RUN / "evaluation.json",
        RUN / "metrics_by_mode.json",
        RUN / "full_semantic_material_audit.json",
        Path(expand("$PROJECT_ROOT/data/RQ3/inputs/random218_full_semantic_summary/manifest.json")),
        Path(expand("$PROJECT_ROOT/data/RQ3/inputs/random218_full_semantic_summary/preflight_audit.json")),
    ]
    manifest = {
        "experiment": "Experiment 3 full semantic summary supplement final",
        "final_resolved": 100,
        "sample_count": 218,
        "submitted_patches": 120,
        "official_evaluation_missing": 0,
        "sources": [
            {"path": str(path.relative_to(PROJECT)), "sha256": sha256(path)}
            for path in manifest_sources
        ],
    }
    target = PACKAGE / "exp3_swebench/results/full_semantic_summary_218/COPY_MANIFEST.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    note = """

## 2026-09-16: Experiment 3 full-semantic-flattening supplement (final version)

The new final supplement materials are in `exp3_swebench/results/full_semantic_summary_218/`, with the corresponding document at
`exp3_swebench/documentation/exp3_full_semantic_summary_supplement_20260916.md`.
The final result is 100/218 resolved; this condition flattens all frozen function behavioral semantics into ordinary natural language in one shot,
with no Worker structure, retrieval, routing, or SPL-specific strategy. The interruption-recovery snapshot is saved alongside the results; the old 56/218
temporary result must not be used as a paper conclusion.

Combined document for the three supplementary experiments: `supplement_experiments_1_2_3_overview.md`.
"""
    current = PACKAGE_README.read_text(encoding="utf-8")
    if "Experiment 3 full-semantic-flattening supplement (final version)" not in current:
        PACKAGE_README.write_text(current.rstrip() + note, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_documents()

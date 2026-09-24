"""Audit how much of the class-level API a reconstruction preserved.

For every task and condition, compare the generated class against the reference
class on four increasingly strict API checks:

  class_name       the generated class is named exactly like the reference
  method_set       the set of method names is equal
  api_shape        method_set plus identical parameter lists (names, defaults,
                   *args/**kwargs) and identical static/classmethod kinds
  api_decorators   api_shape plus identical decorator sets

The first top-level class in each generated file is used, so a wrong class name
is still audited rather than skipped.

Writes `<run_dir>/api_fidelity.json`.

Usage:
  python .../scripts/audit_api_fidelity.py --run-dir $PROJECT_ROOT/data/raw_results/exp1_classeval/model_runs/<model>/full100
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "code"))

from common.code_utils import extract_code_block  # noqa: E402


def first_class(source: str) -> ast.ClassDef | None:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            return node
    return None


def kind_of(node: ast.FunctionDef) -> str:
    for dec in node.decorator_list:
        name = dec.id if isinstance(dec, ast.Name) else getattr(dec, "attr", "")
        if name in ("staticmethod", "classmethod"):
            return name
    return "method"


def decorator_names(node: ast.FunctionDef) -> frozenset[str]:
    out = set()
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name):
            out.add(dec.id)
        elif isinstance(dec, ast.Attribute):
            out.add(dec.attr)
        elif isinstance(dec, ast.Call):
            inner = dec.func
            out.add(inner.id if isinstance(inner, ast.Name) else getattr(inner, "attr", ""))
    return frozenset(out)


def signature(node: ast.FunctionDef) -> tuple:
    args = node.args
    names = [a.arg for a in (*args.posonlyargs, *args.args, *args.kwonlyargs)]
    defaults = len(args.defaults) + len([d for d in args.kw_defaults if d is not None])
    return (
        tuple(names),
        defaults,
        args.vararg.arg if args.vararg else None,
        args.kwarg.arg if args.kwarg else None,
    )


def api_of(node: ast.ClassDef) -> dict[str, tuple]:
    out = {}
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[item.name] = (signature(item), kind_of(item), decorator_names(item))
    return out


def compare(reference: ast.ClassDef, generated: ast.ClassDef | None) -> dict[str, bool]:
    if generated is None:
        return {k: False for k in ("class_name", "method_set", "api_shape", "api_decorators")}
    ref_api = api_of(reference)
    gen_api = api_of(generated)
    name_ok = reference.name == generated.name
    set_ok = set(ref_api) == set(gen_api)
    shape_ok = set_ok and all(
        ref_api[m][0] == gen_api[m][0] and ref_api[m][1] == gen_api[m][1] for m in ref_api
    )
    deco_ok = shape_ok and all(ref_api[m][2] == gen_api[m][2] for m in ref_api)
    return {"class_name": name_ok, "method_set": set_ok, "api_shape": shape_ok, "api_decorators": deco_ok}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True, help="results dir containing <task>/<condition>/output.txt")
    ap.add_argument("--spl-dir", default=None, help="artifact dir with <task>/raw_solution.py; derived from run-dir if omitted")
    args = ap.parse_args()

    run_dir = (ROOT / args.run_dir) if not Path(args.run_dir).is_absolute() else Path(args.run_dir)
    if args.spl_dir:
        spl_dir = (ROOT / args.spl_dir) if not Path(args.spl_dir).is_absolute() else Path(args.spl_dir)
    else:
        model = run_dir.parent.name
        spl_dir = ROOT / "data/RQ1/spl_assets/model_runs" / model / "full100"

    tasks = sorted([d for d in run_dir.iterdir() if d.is_dir() and d.name.startswith("ClassEval_")],
                   key=lambda p: int(p.name.split("_")[1]))
    conditions = sorted({d.name for t in tasks for d in t.iterdir() if d.is_dir() and not d.name.startswith("_")})

    per_condition: dict[str, dict] = {}
    failures: dict[str, list[str]] = {c: [] for c in conditions}
    for condition in conditions:
        counts = {"n": 0, "class_name": 0, "method_set": 0, "api_shape": 0, "api_decorators": 0}
        for task in tasks:
            out_path = task / condition / "output.txt"
            ref_path = spl_dir / task.name / "raw_solution.py"
            if not out_path.exists() or not ref_path.exists():
                continue
            counts["n"] += 1
            reference = first_class(ref_path.read_text(encoding="utf-8"))
            generated = first_class(extract_code_block(out_path.read_text(encoding="utf-8")))
            if reference is None:
                continue
            row = compare(reference, generated)
            for key, ok in row.items():
                counts[key] += int(ok)
            if not row["api_decorators"]:
                missing = [k for k, v in row.items() if not v]
                failures[condition].append({"task": task.name, "failed": missing,
                                            "generated_class": generated.name if generated else None})
        per_condition[condition] = counts

    out = {
        "run_dir": run_dir.relative_to(ROOT).as_posix(),
        "spl_dir": spl_dir.relative_to(ROOT).as_posix(),
        "metrics": ["class_name", "method_set", "api_shape", "api_decorators"],
        "conditions": per_condition,
        "task_level_failures": failures,
    }
    path = run_dir / "api_fidelity.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'condition':22s} {'n':>4} {'className':>10} {'methodSet':>10} {'apiShape':>10} {'+decorators':>12}")
    for condition, c in per_condition.items():
        print(f"{condition:22s} {c['n']:>4} {c['class_name']:>10} {c['method_set']:>10} "
              f"{c['api_shape']:>10} {c['api_decorators']:>12}")
    print(f"\nwrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

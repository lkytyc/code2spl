from __future__ import annotations

"""Pre-pull all 218 SWE-bench eval images for the random218 experiment.

Docker stores each image only once (content-addressable layers), so the 218
per-instance images share per-repo base layers and the real download is far
smaller than the sum of their virtual sizes. This script is resume-aware:
re-running it skips any image already present locally.

Usage:
  python scripts/prepull_random218_images.py [max_workers] [instance_id ...]

  - no extra args: pull all 218 images (skip those already present)
  - [instance_id ...]: pull only those specific instances
"""

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP6 = ROOT
ORDER_FILE = EXP6 / "data/RQ3/inputs/precomputed_random218_deepseek-v4-flash/configs/execution_order_218_ids.json"
LOG_DIR = EXP6 / "data/raw_results/exp3_swebench/random218_compact/execution"


def image_of(iid: str) -> str:
    return f"swebench/sweb.eval.x86_64.{iid.replace('__', '_1776_')}:latest".lower()


def is_present(img: str) -> bool:
    return (
        subprocess.run(
            ["docker", "image", "inspect", img],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def pull_one(iid: str, retries: int = 12) -> tuple[str, str, float]:
    """Pull one image with retries. Returns (iid, status, elapsed)."""
    img = image_of(iid)
    if is_present(img):
        return iid, "present", 0.0

    log = LOG_DIR / f"pull_{iid}.log"
    last_rc = -1
    for attempt in range(1, retries + 1):
        t0 = time.time()
        with log.open("w", encoding="utf-8") as out:
            rc = subprocess.run(
                ["docker", "pull", img],
                stdout=out,
                stderr=subprocess.STDOUT,
                check=False,
            ).returncode
        dt = time.time() - t0
        last_rc = rc
        if rc == 0 or is_present(img):
            return iid, "ok", dt
        print(f"[pull] {iid} attempt {attempt} rc={rc} {dt:.0f}s", flush=True)
        if attempt < retries:
            # The proxy drops in and out (EOF / handshake failures); use a longer backoff to ride out the flakiness
            time.sleep(min(60, 10 * attempt))

    return iid, f"FAIL(rc={last_rc})", 0.0


def main() -> None:
    order = json.loads(ORDER_FILE.read_text(encoding="utf-8"))["sample_ids"]
    ids = order

    args = sys.argv[1:]
    workers = 6
    only: list[str] = []
    for a in args:
        if a.isdigit():
            workers = int(a)
        else:
            only.append(a)
    if only:
        ids = [i for i in ids if i in only]

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"prepull: {len(ids)} instances, max_workers={workers}", flush=True)

    ok = fail = 0
    t_start = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for iid, status, dt in ex.map(pull_one, ids):
            if status in ("ok", "present"):
                ok += 1
                print(f"[{ok + fail}/{len(ids)}] {iid} {status} {dt:.0f}s", flush=True)
            else:
                fail += 1
                print(f"[{ok + fail}/{len(ids)}] {iid} {status}", flush=True)

    total = time.time() - t_start
    summary = {
        "total": len(ids),
        "ok": ok,
        "fail": fail,
        "elapsed_seconds": total,
    }
    (LOG_DIR / "prepull_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print(f"prepull done: ok={ok} fail={fail} elapsed={total:.0f}s", flush=True)


if __name__ == "__main__":
    main()

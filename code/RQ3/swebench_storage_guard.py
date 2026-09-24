import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def run_docker(args: list[str], timeout: int = 120) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["docker", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return proc.returncode, proc.stdout or "", proc.stderr or ""


def parse_json_lines(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"raw": line})
    return rows


def image_repo(row: dict) -> str:
    repo = str(row.get("Repository") or row.get("repository") or "")
    tag = str(row.get("Tag") or row.get("tag") or "")
    return f"{repo}:{tag}" if tag and tag != "<none>" else repo


def normalized_image_name(name: str) -> str:
    if "/" in name:
        name = name.rsplit("/", 1)[-1]
    if ":" in name:
        name = name.rsplit(":", 1)[0]
    return name


def swebench_image_level(image_name: str) -> str | None:
    name = normalized_image_name(image_name)
    if name.startswith("sweb.eval"):
        return "eval"
    if name.startswith("sweb.env"):
        return "env"
    if name.startswith("sweb.base"):
        return "base"
    return None


def is_swebench_container(row: dict) -> bool:
    name = str(row.get("Names") or row.get("names") or "")
    image = str(row.get("Image") or row.get("image") or "")
    return name.startswith("sweb.eval") or swebench_image_level(image) == "eval"


def level_allowed(candidate_level: str, cleanup_level: str) -> bool:
    order = {"eval": 1, "env": 2, "base": 3, "all": 3}
    return order[candidate_level] <= order[cleanup_level]


def disk_report(path: Path) -> dict:
    usage = shutil.disk_usage(path)
    return {
        "path": str(path),
        "total_gb": round(usage.total / 1024**3, 2),
        "used_gb": round(usage.used / 1024**3, 2),
        "free_gb": round(usage.free / 1024**3, 2),
    }


def inventory() -> dict:
    result = {
        "generated_at": now_stamp(),
        "workspace_disk": disk_report(ROOT),
        "docker_available": False,
        "docker_errors": [],
        "docker_system_df": "",
        "containers": [],
        "images": [],
        "swebench_containers": [],
        "swebench_images": [],
    }
    code, stdout, stderr = run_docker(["system", "df"], timeout=60)
    if code != 0:
        result["docker_errors"].append({"command": "docker system df", "returncode": code, "stderr": stderr[-4000:]})
        return result
    result["docker_available"] = True
    result["docker_system_df"] = stdout

    code, stdout, stderr = run_docker(["ps", "-a", "--format", "{{json .}}"], timeout=60)
    if code == 0:
        result["containers"] = parse_json_lines(stdout)
        result["swebench_containers"] = [row for row in result["containers"] if is_swebench_container(row)]
    else:
        result["docker_errors"].append({"command": "docker ps -a", "returncode": code, "stderr": stderr[-4000:]})

    code, stdout, stderr = run_docker(["images", "--format", "{{json .}}"], timeout=60)
    if code == 0:
        images = parse_json_lines(stdout)
        for row in images:
            full = image_repo(row)
            level = swebench_image_level(full)
            if level:
                row["swebench_level"] = level
                row["swebench_image_name"] = full
        result["images"] = images
        result["swebench_images"] = [row for row in images if row.get("swebench_level")]
    else:
        result["docker_errors"].append({"command": "docker images", "returncode": code, "stderr": stderr[-4000:]})
    return result


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def cmd_inventory(args) -> int:
    data = inventory()
    if args.out:
        write_json(args.out, data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if data["docker_available"] else 2


def cmd_preflight(args) -> int:
    data = inventory()
    free_gb = float(data["workspace_disk"]["free_gb"])
    ok = data["docker_available"] and free_gb >= args.min_free_gb
    data["preflight"] = {
        "ok": ok,
        "min_free_gb": args.min_free_gb,
        "reason": "ok" if ok else "docker_unavailable_or_low_disk",
    }
    if args.out:
        write_json(args.out, data)
    print(json.dumps(data["preflight"], ensure_ascii=False, indent=2))
    return 0 if ok else 3


def cmd_cleanup(args) -> int:
    log_dir = args.log_dir or (ROOT / "runs" / "swebench_storage_guard" / now_stamp())
    before = inventory()
    write_json(log_dir / "inventory_before.json", before)
    if not before["docker_available"]:
        print("Docker is not available; no cleanup was performed.", file=sys.stderr)
        print(json.dumps(before.get("docker_errors", []), ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    containers = before["swebench_containers"]
    images = [
        row
        for row in before["swebench_images"]
        if level_allowed(str(row["swebench_level"]), args.level)
    ]
    plan = {
        "execute": args.execute,
        "level": args.level,
        "remove_containers": containers,
        "remove_images": images,
    }
    write_json(log_dir / "cleanup_plan.json", plan)

    if not args.execute:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        print(f"Dry run only. Re-run with --execute to remove these SWE-bench resources. Log dir: {log_dir}")
        return 0

    actions = []
    for row in containers:
        cid = str(row.get("ID") or row.get("id") or "")
        name = str(row.get("Names") or row.get("names") or "")
        target = cid or name
        if not target:
            continue
        code, stdout, stderr = run_docker(["rm", "-f", target], timeout=120)
        actions.append({"kind": "container", "target": target, "name": name, "returncode": code, "stdout": stdout, "stderr": stderr})
    for row in images:
        target = str(row.get("swebench_image_name") or image_repo(row))
        if not target:
            continue
        code, stdout, stderr = run_docker(["rmi", "-f", target], timeout=300)
        actions.append({"kind": "image", "target": target, "level": row.get("swebench_level"), "returncode": code, "stdout": stdout, "stderr": stderr})
    if args.prune_build_cache:
        code, stdout, stderr = run_docker(["builder", "prune", "--force"], timeout=600)
        actions.append({"kind": "builder_prune", "target": "docker builder prune --force", "returncode": code, "stdout": stdout, "stderr": stderr})

    after = inventory()
    write_json(log_dir / "cleanup_actions.json", actions)
    write_json(log_dir / "inventory_after.json", after)
    print(f"Cleanup finished. Actions: {len(actions)}. Log dir: {log_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Storage guard and conservative cleanup for SWE-bench Docker resources.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_inventory = sub.add_parser("inventory")
    p_inventory.add_argument("--out", type=Path)
    p_inventory.set_defaults(func=cmd_inventory)

    p_preflight = sub.add_parser("preflight")
    p_preflight.add_argument("--min-free-gb", type=float, default=60.0)
    p_preflight.add_argument("--out", type=Path)
    p_preflight.set_defaults(func=cmd_preflight)

    p_cleanup = sub.add_parser("cleanup")
    p_cleanup.add_argument("--level", choices=["eval", "env", "base", "all"], default="eval")
    p_cleanup.add_argument("--execute", action="store_true")
    p_cleanup.add_argument("--prune-build-cache", action="store_true")
    p_cleanup.add_argument("--log-dir", type=Path)
    p_cleanup.set_defaults(func=cmd_cleanup)

    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

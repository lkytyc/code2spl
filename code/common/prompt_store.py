from __future__ import annotations

from pathlib import Path


EXPERIMENTS_ROOT = Path(__file__).resolve().parents[1]
CENTRAL_PROMPTS_DIR = EXPERIMENTS_ROOT / "prompts"


def central_prompt_path(experiment_name: str, method_name: str, prompt_name: str = "prompt.md") -> Path:
    return CENTRAL_PROMPTS_DIR / experiment_name / method_name / prompt_name


def legacy_prompt_path(experiment_dir: Path, method_name: str, prompt_name: str = "prompt.md") -> Path:
    return experiment_dir / "methods" / method_name / "prompts" / prompt_name


def has_prompt(experiment_dir: Path, experiment_name: str, method_name: str, prompt_name: str = "prompt.md") -> bool:
    return central_prompt_path(experiment_name, method_name, prompt_name).exists() or legacy_prompt_path(
        experiment_dir, method_name, prompt_name
    ).exists()


def load_prompt(experiment_dir: Path, experiment_name: str, method_name: str, prompt_name: str = "prompt.md") -> str:
    candidates = [
        central_prompt_path(experiment_name, method_name, prompt_name),
        legacy_prompt_path(experiment_dir, method_name, prompt_name),
    ]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8")
    searched = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Missing prompt for {experiment_name}/{method_name}/{prompt_name}. Searched: {searched}")

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from common.standalone_method_runtime import main


def run() -> None:
    main(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    run()

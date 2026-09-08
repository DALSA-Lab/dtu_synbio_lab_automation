import sys

import dtu_synbio_lab_automation

MINIMUM_PYTHON = (3, 10)


def main() -> None:
    current_version = sys.version_info[:2]
    if current_version < MINIMUM_PYTHON:
        raise TypeError(
            f"This project requires Python {MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]}. "
            f"Found: Python {sys.version}"
        )

    print(
        ">>> DTU Synbio Lab Automation environment OK "
        f"(package {dtu_synbio_lab_automation.__version__})"
    )


if __name__ == "__main__":
    main()

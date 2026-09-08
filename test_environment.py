import sys

MINIMUM_PYTHON = (3, 9)


def main():
    current_version = sys.version_info[:2]
    if current_version < MINIMUM_PYTHON:
        raise TypeError(
            "This project requires Python {}.{}. Found: Python {}".format(
                MINIMUM_PYTHON[0], MINIMUM_PYTHON[1], sys.version
            )
        )

    print(">>> Development environment passes all tests!")


if __name__ == '__main__':
    main()

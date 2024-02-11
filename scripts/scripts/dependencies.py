#!/bin/env python3
import argparse
import subprocess
import sys
import typing


def build_namespace() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-push",
        "-np",
        action="store_false",
        default=True,
        help="Push the update to remote.",
        dest="no_push",
    )
    return parser.parse_args()


def main() -> int:
    namespace = build_namespace()
    return_code = 0
    return_code += remove_lock_if_exists()
    return_code += poetry_update()
    return_code += pre_commit_update()
    if not return_code:
        if namespace.no_push:
            commit_and_push()
        else:
            print(
                "Changes detected but script was executed with --no-push so changes remain local."
            )
    print(f"Exited: {return_code}")
    return return_code


def remove_lock_if_exists():
    return _run_command(("rm", "-f", "poetry.lock"))


def poetry_update():
    return _run_command(("poetry", "update"))


def poetry_up_deps():
    return _run_command(("poetry", "up"))


def pre_commit_update():
    return _run_command(("pre-commit", "autoupdate"))


def commit_and_push():
    return (
        _run_command(
            ("git", "add", "poetry.lock", ".pre-commit-config.yaml", "pyproject.toml")
        )
        + _run_command(("git", "commit", "-m", ":rocket: `dependency upgrades`."))
        + _run_command(("git", "push"))
    )


def _run_command(command: typing.Tuple[str, ...]) -> int:
    """
    Run a command and return the subprocess exit code.
    :param command: Command to run.
    :return:
    """
    return subprocess.run(
        command, stdout=sys.stdout, stderr=subprocess.STDOUT
    ).returncode


if __name__ == "__main__":
    """
    A rather naive utility script for updating poetry and pre-commit dependencies.
    From the root directory of `pytest-playwright-enhanced`:
        python scripts/dependencies.py
    """
    raise SystemExit(main())

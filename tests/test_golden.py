"""Golden-fixture tests: exact CLI output for each tests/golden/<name>.json.

Each fixture is a JSON input, the expected YAML output (<name>.yaml) and,
optionally, extra CLI arguments, one per line (<name>.args).
See ADR-0004 for the merge rules these fixtures pin down.
"""

import json
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden"
CASES = sorted(p.stem for p in GOLDEN.glob("*.json"))


def run_cli(payload: bytes, args: list[str]) -> str:
    env = os.environ.copy()
    src = str(ROOT / "src")
    env["PYTHONPATH"] = src + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    proc = subprocess.run(
        [sys.executable, "-m", "typesketch.cli", *args],
        input=payload,
        stdout=subprocess.PIPE,
        cwd=ROOT,
        env=env,
        check=True,
    )
    return proc.stdout.decode()


@pytest.mark.parametrize("name", CASES)
def test_golden(name: str) -> None:
    args_file = GOLDEN / f"{name}.args"
    args = args_file.read_text().splitlines() if args_file.exists() else []
    payload = (GOLDEN / f"{name}.json").read_bytes()
    expected = (GOLDEN / f"{name}.yaml").read_text()
    assert run_cli(payload, args) == expected


@pytest.mark.parametrize("name", CASES)
def test_golden_output_is_valid_yaml(name: str) -> None:
    """Every expected output must parse as YAML (keys quoted when needed)."""
    yaml = pytest.importorskip("yaml")
    yaml.safe_load((GOLDEN / f"{name}.yaml").read_text())


def test_awkward_keys_round_trip() -> None:
    """Keys come back from a YAML parser exactly as they were in the JSON."""
    yaml = pytest.importorskip("yaml")
    payload = (GOLDEN / "awkward_keys.json").read_bytes()
    parsed = yaml.safe_load(run_cli(payload, []))
    assert set(parsed) == set(json.loads(payload))
    assert parsed["nested"] == {"[0]": {"?": "int"}}

"""Bad input gives a one-line error on stderr and exit status 1."""

import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def run_cli(payload: bytes) -> "subprocess.CompletedProcess[bytes]":
    env = os.environ.copy()
    src = str(ROOT / "src")
    env["PYTHONPATH"] = src + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return subprocess.run(
        [sys.executable, "-m", "typesketch.cli"],
        input=payload,
        capture_output=True,
        cwd=ROOT,
        env=env,
    )


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        pytest.param(b"", "no JSON on stdin", id="empty"),
        pytest.param(b"  \n", "no JSON on stdin", id="blank"),
        pytest.param(b'{"a": 1,}', "invalid JSON on stdin: Expecting property name", id="syntax"),
        pytest.param(
            b'{"a": 1}\n{"b": 2}',
            "invalid JSON on stdin: Extra data (line 2, column 1)",
            id="two-documents",
        ),
        pytest.param(b"\xff{}", "input is not valid UTF-8", id="not-utf8"),
        pytest.param(
            b"[" * 100_000 + b"]" * 100_000, "input is nested too deeply", id="too-deep-to-parse"
        ),
        # Parses, but too deep for inference/emission.
        pytest.param(
            b'{"x":' * 900 + b"1" + b"}" * 900,
            "input is nested too deeply",
            id="too-deep-to-sketch",
        ),
    ],
)
def test_bad_input(payload: bytes, message: str) -> None:
    proc = run_cli(payload)
    err = proc.stderr.decode()
    assert proc.returncode == 1
    assert proc.stdout == b""
    assert err.startswith(f"typesketch: error: {message}")
    assert "Traceback" not in err
    assert err.count("\n") == 1


def test_utf8_bom_is_accepted() -> None:
    proc = run_cli(b'\xef\xbb\xbf{"a": 1}')
    assert proc.returncode == 0
    assert proc.stdout.decode() == "a: int\n"

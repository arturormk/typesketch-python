import os
import pathlib
import subprocess
import sys


def run_cli(payload: str) -> str:
    here = pathlib.Path(__file__).resolve().parents[1]
    cli = [sys.executable, "-m", "typesketch.cli"]
    env = os.environ.copy()
    src_path = str(here / "src")
    env["PYTHONPATH"] = src_path + (":" + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    proc = subprocess.run(cli, input=payload.encode(), stdout=subprocess.PIPE, cwd=here, env=env)
    return proc.stdout.decode()


def test_scalar_and_array_unions() -> None:
    payload = '[{"id":1,"tag":["a",2],"url":"https://x"}, {"id":2,"tag":[3]}]'
    out = run_cli(payload)
    assert "id: int" in out
    assert "- string | int" in out or "array<string | int>" in out
    assert "url: url" in out


def test_object_root() -> None:
    payload = '{"a":1,"b":"2023-01-01T10:00:00Z","c":{"d":"x"}}'
    out = run_cli(payload)
    assert "a: int" in out
    assert "b: datetime" in out
    assert "c:" in out and "d: string" in out

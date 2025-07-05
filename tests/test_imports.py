# tests/test_imports.py
"""
Import every top-level module to catch missing deps
or circular imports early.
"""
import importlib
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent


def iter_python_modules():
    for path in PROJECT_ROOT.glob("*.py"):
        if path.name.startswith(("_", "tests")):
            continue
        yield path.stem


def test_import_everything():
    failed = []
    for name in iter_python_modules():
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            failed.append(f"{name}: {exc}")
    assert not failed, "Failed imports:\n" + "\n".join(failed)

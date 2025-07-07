"""
Smoke-test the analysis scripts: run them into a temp dir and ensure
they create non-empty PNGs. Does not verify plot content.
"""

import importlib.util
import pathlib
import tempfile

ANALYSIS_DIR = pathlib.Path("analysis")


def _execute(script_name: str) -> None:
    script_path = ANALYSIS_DIR / script_name
    with tempfile.TemporaryDirectory() as td:
        tmp_out = pathlib.Path(td) / "plot.png"
        # dynamically load and invoke cli([...])
        spec = importlib.util.spec_from_file_location("mod", script_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[arg-type]
        mod.cli(["--log-path", "logs/interaction_log.jsonl", "--out", str(tmp_out)])
        assert tmp_out.exists() and tmp_out.stat().st_size > 0


def test_emotion_plot():
    _execute("plot_emotions.py")


def test_safety_plot():
    _execute("plot_safety_flags.py")

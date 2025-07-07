"""
Smoke-test the analysis scripts: run them into a temp dir and ensure
they create non-empty PNGs. Does not verify plot content.
"""

import importlib.util
import pathlib
import tempfile
import json

ANALYSIS_DIR = pathlib.Path("analysis")


def _execute(script_name: str) -> None:
    script_path = ANALYSIS_DIR / script_name
    with tempfile.TemporaryDirectory() as td:
        tmp_dir = pathlib.Path(td)
        # --- create minimal fake log ---
        sample = {
            "timestamp": "2025-07-01T12:00:00Z",
            "emotion_scores": {"joy": 0.9},
            "prompt": "p",
            "llm_response": "⚠️ Safety Warning: test",
            "user_input": "hi",
        }
        log_path = tmp_dir / "log.jsonl"
        log_path.write_text(json.dumps(sample) + "\n")
        out_png = tmp_dir / "plot.png"

        # dynamically load and run cli
        spec = importlib.util.spec_from_file_location("mod", script_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[arg-type]
        mod.cli(["--log-path", str(log_path), "--out", str(out_png)])
        assert out_png.exists() and out_png.stat().st_size > 0


def test_emotion_plot():
    _execute("plot_emotions.py")


def test_safety_plot():
    _execute("plot_safety_flags.py")

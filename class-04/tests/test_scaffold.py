"""Gate tests verifying the WidgetWare SDR Lab project scaffold.

Runs fully offline: filesystem checks only, no network or API key required.
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_DIRS = [".claude", "config", "src", "data", "outputs", "tests", "evals"]


def test_expected_directories_exist():
    for name in EXPECTED_DIRS:
        path = PROJECT_ROOT / name
        assert path.is_dir(), f"Expected directory missing: {path}"


def test_claude_settings_is_valid_json():
    settings_path = PROJECT_ROOT / ".claude" / "settings.json"
    assert settings_path.is_file(), f"{settings_path} does not exist"
    with settings_path.open() as f:
        data = json.load(f)  # raises json.JSONDecodeError if malformed
    assert isinstance(data, dict)


def test_claude_md_exists():
    claude_md = PROJECT_ROOT / "CLAUDE.md"
    assert claude_md.is_file(), f"{claude_md} does not exist"


def test_outputs_dir_is_writable_and_readable():
    outputs_dir = PROJECT_ROOT / "outputs"
    probe_file = outputs_dir / ".pytest_write_probe.tmp"
    try:
        probe_file.write_text("scaffold check\n")
        assert probe_file.read_text() == "scaffold check\n"
    finally:
        probe_file.unlink(missing_ok=True)

"""Application configuration loading."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[2] / "configs"


@dataclass
class AppConfig:
    name: str
    log_level: str
    model: str


def load_config(env: str = "default") -> AppConfig:
    """Load configuration from configs/<env>.yaml, overridable by env vars."""
    config_path = CONFIG_DIR / f"{env}.yaml"
    data = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}

    return AppConfig(
        name=os.environ.get("APP_NAME", data.get("name", "class-02")),
        log_level=os.environ.get("LOG_LEVEL", data.get("log_level", "INFO")),
        model=os.environ.get("ANTHROPIC_MODEL", data.get("model", "claude-sonnet-5")),
    )

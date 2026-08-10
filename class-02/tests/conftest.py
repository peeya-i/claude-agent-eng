"""Shared pytest fixtures."""

import pytest

from class_02.config import AppConfig


@pytest.fixture
def sample_config() -> AppConfig:
    return AppConfig(name="test-app", log_level="DEBUG", model="claude-sonnet-5")

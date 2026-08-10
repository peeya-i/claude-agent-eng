"""Entry point for the class-02 application."""

from __future__ import annotations

from class_02.config import load_config


def greet(name: str) -> str:
    return f"Hello, {name}!"


def main() -> None:
    config = load_config()
    print(f"Starting {config.name} (model={config.model}, log_level={config.log_level})")
    print(greet("world"))


if __name__ == "__main__":
    main()

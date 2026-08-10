# Class 02

## Overview

Python application scaffold with source code, tests, evals, and configs.

## Structure

```
class-02/
├── src/class_02/     # application source
├── tests/            # pytest unit tests
├── evals/            # LLM-judged agent behavior evals (see evals/README.md)
├── configs/          # environment configs (default.yaml, test.yaml)
├── .github/workflows/ # CI
├── pyproject.toml
├── requirements.txt / requirements-dev.txt
└── .env.example
```

## Setup

```bash
make install-dev
cp .env.example .env   # fill in ANTHROPIC_API_KEY
```

## Commands

- `make run` — run the app
- `make test` — run unit tests with coverage
- `make lint` — run ruff
- `make evals` — run agent behavior evals

## Conventions

- Unit tests (`tests/`) cover deterministic logic; evals (`evals/`) cover
  LLM/agent behavior and are graded by an LLM judge, not asserted exactly.
- Config values resolve as: env var > `configs/<env>.yaml` > code default.

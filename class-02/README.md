# Class 02

## Overview

Follow-on lab from [class-01](../class-01/). Where class-01 covers the basics
of the Claude Code CLI, class-02 uses Claude Code to scaffold a complete,
realistic Python application project — source, tests, evals, and configs —
and walks through the setup steps needed to actually run it.

## Objectives

- Scaffold a full app project structure with Claude Code: `src/`, `tests/`,
  `evals/`, `configs/`, CI, and supporting project files
- Distinguish unit tests (deterministic logic) from evals (LLM-judged agent
  behavior)
- Set up a working Python environment (venv) and install project dependencies
- Configure and use an `ANTHROPIC_API_KEY` via a `.env` file

## What Was Done

1. Created the base Claude Code scaffolding: [CLAUDE.md](CLAUDE.md) and
   [.claude/settings.json](.claude/settings.json)
2. Built out a full app structure:
   - [src/class_02/](src/class_02/) — application source (`config.py`, `main.py`)
   - [tests/](tests/) — pytest unit tests + fixtures
   - [evals/](evals/) — an LLM-judged eval harness (`run_evals.py`) with
     example cases in `evals/cases/`
   - [configs/](configs/) — environment configs (`default.yaml`, `test.yaml`)
   - [.github/workflows/ci.yml](.github/workflows/ci.yml) — lint + test on push/PR
   - [pyproject.toml](pyproject.toml), `requirements.txt`, `requirements-dev.txt`,
     [Makefile](Makefile), [.env.example](.env.example)
3. Verified the scaffold statically (syntax, JSON/TOML parsing) since no venv
   existed yet in the sandbox
4. Set up a real virtual environment (`python3.14-venv` was missing and
   required `sudo apt install`; the system Python is externally-managed and
   refuses direct `pip install`)
5. Installed dependencies with `make install-dev` and ran `make test`
6. Created `.env` from `.env.example` and set `ANTHROPIC_API_KEY` to run
   `make evals` against the live Anthropic API
7. Hit an account credit/billing limit on the first live eval run — a reminder
   that `evals/` costs real API usage, unlike `tests/`

## Structure

```
class-02/
├── README.md          # this file
├── CLAUDE.md           # project instructions/context for Claude Code
├── src/class_02/       # application source
├── tests/              # pytest unit tests
├── evals/              # LLM-judged agent behavior evals
├── configs/            # environment configs
├── .claude/settings.json
├── .github/workflows/  # CI
├── pyproject.toml
├── requirements.txt / requirements-dev.txt
├── Makefile
└── .env.example
```

## Getting Started

```bash
sudo apt install python3.14-venv   # if venv creation fails
python3 -m venv .venv
source .venv/bin/activate
make install-dev
cp .env.example .env               # fill in ANTHROPIC_API_KEY
make test                          # unit tests, no API calls
make evals                         # LLM-judged evals, requires API credit
```

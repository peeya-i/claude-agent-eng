# WidgetWare SDR Lab

Project scaffold for the WidgetWare SDR Lab agent project.

## Directory structure

```
widgetware-sdr-lab/
├── .claude/           # Claude Code project settings
│   └── settings.json  # permissions.deny list (see below)
├── CLAUDE.md           # project instructions for Claude Code (placeholder, TBD)
├── config/              # business-context YAML files
├── src/                 # tool implementations
├── data/                # seed data
├── outputs/             # generated artifacts (gitignored)
├── tests/               # gate tests, organized by chapter (e.g. tests/chapter_01/)
├── evals/               # evaluation datasets
├── .gitignore
└── requirements-dev.txt # pytest
```

## Security

`.claude/settings.json` denies Claude Code read access to secret-shaped paths, even though
nothing secret exists in the repo yet:

- `.env`, `.env.*`
- `*.pem`, `*.key`
- anything under `secrets/`
- `*.sqlite*`

`.gitignore` also excludes these paths (plus `outputs/` and standard Python/Node/OS cruft)
from version control.

## Setup

```bash
pip install -r requirements-dev.txt
```

## Status

Scaffold only — `CLAUDE.md` and the contents of `config/`, `src/`, `data/`, `tests/`, and
`evals/` are still to be filled in.

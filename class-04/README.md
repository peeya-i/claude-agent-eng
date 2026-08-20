# WidgetWare SDR Lab

Given a target company, research it and produce an evidence-backed profile
of fit against WidgetWare's ICP and offering — grounded in what can
actually be found, never invented to fill a schema. One stage of a larger
SDR workflow; every external action is gated behind human approval.

## Directory structure

```
widgetware-sdr-lab/
├── .claude/
│   └── settings.json          # permissions.deny list (see Security)
├── CLAUDE.md                  # operating rules, evidence discipline, config pointers
├── config/
│   ├── icp.yaml                # who we target
│   ├── offering.yaml           # what we sell, and what we may not claim
│   ├── proof-points.yaml       # enforceable, sourced registry behind offering.yaml's claims
│   ├── voice.yaml              # tone, phrases to avoid, first-message constraints
│   ├── evidence-policy.yaml    # required fields per claim, claim/support types, rejection rules
│   └── schemas/                # JSON Schema per config file above (additionalProperties: false)
├── src/                        # tool implementations
├── data/
│   └── accounts.csv            # candidate accounts, checked deterministically against icp.yaml
├── outputs/                    # generated artifacts (gitignored)
├── tests/
│   ├── test_scaffold.py        # directories exist, settings.json parses, outputs/ is writable
│   └── chapter_03/             # gate tests for the business-context config system
│       ├── test_instruction_architecture.py  # CLAUDE.md ↔ config existence and structure
│       ├── test_config_schemas.py            # every config validates against its schema,
│       │                                       and the schema rejects bad input
│       ├── test_accounts.py                  # accounts.csv checked against icp.yaml
│       ├── test_proof_point_lifecycle.py     # approved-and-current vs. expired/retired
│       └── test_cross_file_integrity.py      # the five config files checked against each other
├── evals/                      # evaluation datasets
├── .gitignore
└── requirements-dev.txt        # pytest, pyyaml, jsonschema
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

## Evidence discipline

Every factual claim — about a prospect or about WidgetWare itself — needs a
source, source date, and retrieval date, and is labeled along two
independent dimensions: `claim_type` (fact / inference / hypothesis) and
`support_type` (direct / derived / unsupported). Claims about our own
experience resolve against `config/proof-points.yaml`, which is itself
governed by a lifecycle — `status` must be `approved` and `valid_until`
must not have passed before a proof point is usable. Full rules in
`CLAUDE.md` and `config/evidence-policy.yaml`.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

## Running the gate tests

```bash
.venv/bin/pytest tests/ -v
```

102 tests: config files parse and validate against their JSON Schemas
(including negative tests — a typo'd field or invalid enum must fail),
`data/accounts.csv` checks deterministically against `config/icp.yaml`,
the proof-point lifecycle enforces approved-and-current, and the five
config files are checked against each other (e.g. CLAUDE.md's evidence
vocabulary must match `evidence-policy.yaml`'s, no proof point can sit
approved but unreferenced).

## Status

Business-context configuration and its gate tests are in place
(`config/`, `data/accounts.csv`, `tests/chapter_03/`). `src/` (tool
implementations) and `evals/` (evaluation datasets) are still to be
filled in.

# Evals

LLM-judged behavioral evals for the agent, separate from `tests/` (which
covers deterministic unit logic).

## Structure

```
evals/
├── cases/          # one JSON file per eval case (prompt + pass criteria)
└── run_evals.py    # runner: executes each case and grades it with an LLM judge
```

## Adding a case

Create `cases/<id>.json`:

```json
{
  "id": "unique-id",
  "description": "What this case checks and why it matters",
  "prompt": "The input given to the agent",
  "criteria": ["Criterion the response must satisfy", "..."]
}
```

## Running

```bash
export ANTHROPIC_API_KEY=...
python -m evals.run_evals            # run all cases
python -m evals.run_evals --case greeting-basic
```

`run_agent()` in `run_evals.py` currently calls the Anthropic API directly as
a placeholder — swap it for the actual agent entry point (Claude Agent SDK
call, or the app's own agent function) once one exists.

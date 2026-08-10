"""Eval harness: runs the agent against evals/cases/*.json and scores the
transcript against each case's criteria using an LLM judge.

Usage:
    python -m evals.run_evals
    python -m evals.run_evals --case greeting-basic
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import anthropic

CASES_DIR = Path(__file__).parent / "cases"
JUDGE_MODEL = "claude-sonnet-5"


@dataclass
class EvalCase:
    id: str
    description: str
    prompt: str
    criteria: list[str]

    @classmethod
    def from_file(cls, path: Path) -> "EvalCase":
        data = json.loads(path.read_text())
        return cls(**data)


@dataclass
class EvalResult:
    case_id: str
    passed: bool
    reasoning: str


def load_cases(case_id: str | None = None) -> list[EvalCase]:
    cases = [EvalCase.from_file(p) for p in sorted(CASES_DIR.glob("*.json"))]
    if case_id:
        cases = [c for c in cases if c.id == case_id]
    return cases


def run_agent(prompt: str) -> str:
    """Run the agent under test against `prompt` and return its response text.

    Replace this with an actual call into the Claude Agent SDK / claude_agent_sdk
    (or the app's own agent entry point) once the agent implementation exists.
    """
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def judge(case: EvalCase, transcript: str) -> EvalResult:
    """Use an LLM judge to check the transcript against the case's criteria."""
    client = anthropic.Anthropic()
    criteria_list = "\n".join(f"- {c}" for c in case.criteria)
    judge_prompt = (
        "You are grading an AI agent's response against a set of criteria.\n\n"
        f"Agent response:\n{transcript}\n\n"
        f"Criteria (all must be satisfied to pass):\n{criteria_list}\n\n"
        'Reply with strict JSON: {"passed": true|false, "reasoning": "<one sentence>"}'
    )
    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    verdict = json.loads(text)
    return EvalResult(case_id=case.id, passed=verdict["passed"], reasoning=verdict["reasoning"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run agent evals.")
    parser.add_argument("--case", help="Only run the eval case with this id")
    args = parser.parse_args()

    cases = load_cases(args.case)
    if not cases:
        print("No matching eval cases found.", file=sys.stderr)
        return 1

    results = []
    for case in cases:
        transcript = run_agent(case.prompt)
        result = judge(case, transcript)
        results.append(result)
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {case.id}: {result.reasoning}")

    failed = [r for r in results if not r.passed]
    print(f"\n{len(results) - len(failed)}/{len(results)} cases passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

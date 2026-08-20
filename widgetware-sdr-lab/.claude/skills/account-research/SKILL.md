---
name: account-research
description: Research a target company and produce a structured, evidence-backed company profile — industry, business model, size, recent signals, likely priorities, and possible pain points — for the WidgetWare SDR Lab. Use when given a specific company's name and website to research, profile, or evaluate for ICP fit. Do not use this Skill for questions about our own offering, ICP, or proof points (read config/offering.yaml, config/icp.yaml, config/proof-points.yaml directly instead), and do not use it for drafting outreach or messages (a separate Skill, not built yet).
---

# Account Research Skill

## Purpose

Turn a company name and website into a structured, evidence-backed
profile: what the company does, roughly how big it is, what it's been
doing recently, how it fits WidgetWare's ICP, and what it might plausibly
need — grounded in what can actually be found, never invented to fill out
the schema.

## When to use this Skill

Invoke this Skill when asked to research, profile, or evaluate ICP fit for
a specific named company, and both required inputs (below) are available
or can be obtained from the user.

Do **not** invoke this Skill for:

- questions about our own offering, ICP, or proof points — read
  `config/offering.yaml`, `config/icp.yaml`, and `config/proof-points.yaml`
  directly instead
- drafting outreach or messages — no such Skill exists yet in this project
- restating or summarizing a profile already produced earlier in this
  session — re-run the procedure instead of guessing from memory

## Inputs

| Field | Required | Failure behavior if missing |
|---|---|---|
| `company_name` | yes | Stop and ask the user for it. Never proceed on a guessed or partially-remembered name. |
| `website` | yes | Stop and ask the user for it. Never guess a plausible-looking domain — an unconfirmed website risks researching the wrong company entirely, and every claim below depends on getting this right. |
| `research_date` | no | Defaults to today. Recorded in the output so a later reader can judge staleness. |

## Procedure

1. Confirm both required inputs are present. If either is missing, stop
   and ask — do not proceed with a placeholder.
2. Read `config/icp.yaml` and `config/offering.yaml` to know what "fit"
   means for WidgetWare: target industries, company-size range, target
   geography, and target roles.
3. Research the company using whichever capability is available in the
   current session, starting from the given website as the primary
   source: what it does, its approximate size, its industry, and any
   notable recent developments (leadership changes, funding, product
   launches, expansions, hiring signals, restructuring).
4. As you research, keep `config/evidence-policy.yaml`'s fact / inference
   / hypothesis distinction in mind and let it guide your own judgment —
   but this Skill's output is still provisional (see Output contract):
   `evidence` is a flat list of plain strings, not the full per-claim
   `source` / `source_date` / `retrieval_date` / `claim_type` /
   `support_type` citation objects `evidence-policy.yaml` ultimately
   requires. A later chapter formalizes that. For now, a short plain
   description is enough (e.g. "company press release, Jan 2026"), and
   the overall `confidence` field should honestly reflect how much of the
   profile is directly stated versus inferred.
5. Cross-check what you found against `config/icp.yaml` (industry,
   company size, geography) to judge relevance, and let that judgment
   shape `likely_priorities` and `possible_pain_points` — but do not add
   a separate fit verdict; the profile schema does not have one yet.
6. Assemble the output as JSON matching `schema.json` in this Skill's
   directory. Validate it mentally before returning it — every required
   field must be present, and `confidence` must be a number between 0
   and 1.
7. If you found little or nothing usable, do not pad the output with
   generic industry boilerplate — see Failure behavior.

## Output contract

A single JSON object matching `schema.json` in this Skill's directory:

- `company` — the company name as confirmed, not just echoed from input
- `industry` — best-fit description, informed by `config/icp.yaml`'s
  industry categories where applicable, but not limited to them
- `size_estimate` — rough scale (employees, revenue, or "unknown")
- `business_model` — one or two sentences on how the company makes money
- `recent_signals` — list of timely developments found (empty list, not
  omitted, if none found)
- `likely_priorities` — list of plausible current strategic priorities
- `possible_pain_points` — list of plausible problems this company might
  have, given what was found
- `evidence` — list of short strings noting what the above is based on
  (a full source/date/citation structure per `config/evidence-policy.yaml`
  arrives in a later chapter — for now, a plain description like
  "company press release, Jan 2026" is enough)
- `confidence` — 0.0–1.0, honestly reflecting how much was actually found

This is deliberately provisional. It does not yet carry per-claim
citations, an explicit ICP-fit verdict, or the `website` / `research_date`
inputs as separate output fields — those inputs shape the research but
aren't echoed back.

## Failure behavior

Insufficient information is a valid, expected outcome — report it as such
rather than filling fields with generic, unfalsifiable statements that
could apply to any company in the industry. If little or nothing usable
was found:

- Do not pad `recent_signals`, `likely_priorities`, or
  `possible_pain_points` with industry boilerplate; leave them as empty
  lists if nothing specific was found.
- Set the overall `confidence` low and set `icp_fit` to
  `insufficient_evidence` unless fit is independently confirmable from
  firmographic basics alone.
- Still return at least one entry in `claims` explaining what was and
  wasn't found (e.g. `claim_type: hypothesis`, `support_type:
  unsupported`, `claim_text: "insufficient public information found on
  <website> to confirm industry or size"`), rather than returning an
  empty or missing `claims` list.

A low-confidence profile that honestly says "not much found" is more
useful than a fluent one that quietly made things up.

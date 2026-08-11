"""Gate test: the five business-context files treated as one system, not
five independent files that each happen to be individually valid.

Most real failures in a config system like this happen *between* files —
CLAUDE.md drifting out of sync with evidence-policy.yaml's actual
vocabulary, a voice rule silently contradicted by approved sales language,
a proof point sitting unused with no one noticing. Individually-valid YAML
doesn't catch any of that; these tests exist because the schema and
per-file tests only look at one file at a time.
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"


def _load(name):
    return yaml.safe_load((CONFIG_DIR / name).read_text())


def test_proof_point_ids_are_unique():
    proof_points = _load("proof-points.yaml")["proof_points"]
    ids = [p["proof_id"] for p in proof_points]
    duplicates = {i for i in ids if ids.count(i) > 1}
    assert not duplicates, f"duplicate proof_id values: {duplicates}"


def test_claude_md_uses_evidence_policy_terminology_consistently():
    """CLAUDE.md's prose claims to distinguish fact/inference/hypothesis
    and direct/derived/unsupported — those exact terms need to actually be
    the same vocabulary evidence-policy.yaml defines, not just similar
    words. If evidence-policy.yaml's claim_type or support_type values ever
    change, this fails until CLAUDE.md is updated to match."""
    claude_md = (REPO_ROOT / "CLAUDE.md").read_text().lower()
    evidence_policy = _load("evidence-policy.yaml")

    for claim_type in evidence_policy["claim_types"]:
        assert claim_type in claude_md, (
            f"CLAUDE.md never mentions claim_type {claim_type!r} — "
            "its evidence-discipline language has drifted from evidence-policy.yaml"
        )
    for support_type in evidence_policy["support_types"]:
        assert support_type in claude_md, (
            f"CLAUDE.md never mentions support_type {support_type!r} — "
            "its evidence-discipline language has drifted from evidence-policy.yaml"
        )


def test_voice_avoid_phrases_do_not_appear_in_approved_claims():
    """A phrase voice.yaml tells the Message Composer to avoid should not
    already be sitting inside an approved proof-point claim — that would
    mean the two files are actively contradicting each other rather than
    one merely not having been asked about the other yet."""
    voice = _load("voice.yaml")
    proof_points = _load("proof-points.yaml")["proof_points"]

    approved_text = " ".join(
        p["approved_claim"].lower() for p in proof_points if p["status"] == "approved"
    )
    for phrase in voice["avoid"]:
        assert phrase.lower() not in approved_text, (
            f"voice.yaml says to avoid {phrase!r}, but it appears in an "
            "approved proof-point claim"
        )


def test_prohibited_claims_do_not_appear_in_approved_messaging():
    """offering.yaml's claims_that_may_not_be_made is phrased as a rule
    ('specific percentage engineering-time-savings or adoption figures...'),
    not a literal banned string, so this checks the concrete, structural
    version of the same rule: the proof-points registry (the actual
    enforceable source for outbound claims) must not assert a percentage
    figure, since that's exactly what's prohibited."""
    offering = _load("offering.yaml")
    proof_points = _load("proof-points.yaml")["proof_points"]

    prohibits_percentage_figures = any(
        "percentage" in c.lower() or "%" in c
        for c in offering["claims_that_may_not_be_made"]
    )
    assert prohibits_percentage_figures, (
        "expected offering.yaml to prohibit unbacked percentage figures — "
        "this test's other assertion depends on that rule existing"
    )

    for p in proof_points:
        if p["status"] != "approved":
            continue
        claim = p["approved_claim"].lower()
        assert "%" not in claim, (
            f"{p['proof_id']}: approved_claim contains a percentage figure, "
            "which offering.yaml's claims_that_may_not_be_made prohibits"
        )


def test_no_unreferenced_approved_proof_points():
    """An *approved* proof point that nothing references is either dead
    weight that should be retired, or a claim someone forgot to add to
    offering.yaml's summary. Non-approved statuses (retired, pending_review)
    are allowed to sit unreferenced on purpose — that's the normal
    lifecycle, not an error."""
    offering = _load("offering.yaml")
    proof_points = _load("proof-points.yaml")["proof_points"]

    referenced_ids = {
        list(item.keys())[0] for item in offering["proof_points"]["summary"]
    }
    for p in proof_points:
        if p["status"] == "approved":
            assert p["proof_id"] in referenced_ids, (
                f"{p['proof_id']} is approved but not referenced by offering.yaml's "
                "proof_points.summary — either reference it or change its status"
            )


def test_icp_industries_are_actually_used_by_at_least_one_candidate_account():
    """The inverse of the per-account check in test_accounts.py: an ICP
    industry that no candidate account uses is a sign the ICP and the seed
    data have drifted apart, even though each file independently still
    'validates.'"""
    import csv

    icp = _load("icp.yaml")
    with (REPO_ROOT / "data" / "accounts.csv").open(newline="") as f:
        rows = list(csv.DictReader(f))

    used_families = {row["industry_family"] for row in rows}
    unused = set(icp["industry"]) - used_families
    assert not unused, (
        f"icp.yaml lists industries with zero matching candidate accounts: {unused}"
    )

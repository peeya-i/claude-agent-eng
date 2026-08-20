"""Gate test: CLAUDE.md and the five business-context config files exist
and are well-formed. Deterministic and offline.

This does not judge whether CLAUDE.md's *content* is good instruction
architecture — that's a human/reviewer judgment. It only checks the
structural contract: the file exists, references the config files it
depends on, and every config file it points to is valid YAML with the
fields the evidence policy requires.
"""

import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"

REQUIRED_CONFIG_FILES = [
    "icp.yaml",
    "offering.yaml",
    "voice.yaml",
    "evidence-policy.yaml",
    "proof-points.yaml",
]


def test_claude_md_exists_and_is_nonempty():
    claude_md = REPO_ROOT / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md is missing"
    content = claude_md.read_text()
    assert len(content.strip()) > 200, "CLAUDE.md is still a placeholder"


def test_claude_md_references_all_config_files():
    content = (REPO_ROOT / "CLAUDE.md").read_text()
    missing = [f for f in REQUIRED_CONFIG_FILES if f not in content]
    assert not missing, f"CLAUDE.md does not reference: {missing}"


def test_all_config_files_exist():
    missing = [f for f in REQUIRED_CONFIG_FILES if not (CONFIG_DIR / f).exists()]
    assert not missing, f"Missing config files: {missing}"


def test_all_config_files_are_valid_yaml():
    for filename in REQUIRED_CONFIG_FILES:
        path = CONFIG_DIR / filename
        data = yaml.safe_load(path.read_text())
        assert isinstance(data, dict), f"{filename} did not parse to a mapping"


def test_evidence_policy_defines_required_fields():
    data = yaml.safe_load((CONFIG_DIR / "evidence-policy.yaml").read_text())
    assert "required_fields_per_claim" in data
    for field in ["source", "source_date", "retrieval_date", "confidence"]:
        assert field in data["required_fields_per_claim"]


def test_evidence_policy_separates_claim_type_from_support_type():
    """claim_type (fact/inference/hypothesis) and support_type (direct/
    derived/unsupported) are different dimensions and must not be merged
    into one enum — a hypothesis can be directly evidenced and still be a
    hypothesis."""
    data = yaml.safe_load((CONFIG_DIR / "evidence-policy.yaml").read_text())
    assert "claim_type" in data["required_fields_per_claim"]
    assert "support_type" in data["required_fields_per_claim"]

    assert set(data["claim_types"].keys()) == {"fact", "inference", "hypothesis"}
    assert set(data["support_types"].keys()) == {"direct", "derived", "unsupported"}


def test_proof_points_registry_is_well_formed():
    data = yaml.safe_load((CONFIG_DIR / "proof-points.yaml").read_text())
    assert "proof_points" in data
    assert len(data["proof_points"]) > 0
    required = {
        "proof_id",
        "approved_claim",
        "source_reference",
        "disclosure_status",
        "status",
        "last_reviewed_date",
        "valid_until",
        "owner",
    }
    for entry in data["proof_points"]:
        missing = required - entry.keys()
        assert not missing, f"{entry.get('proof_id', '?')} missing: {missing}"


def test_offering_proof_points_resolve_against_registry():
    """offering.yaml's proof_points is a human-readable summary, not the
    source of truth — every ID it lists must exist in proof-points.yaml."""
    offering = yaml.safe_load((CONFIG_DIR / "offering.yaml").read_text())
    registry = yaml.safe_load((CONFIG_DIR / "proof-points.yaml").read_text())
    registry_ids = {p["proof_id"] for p in registry["proof_points"]}

    summary_ids = {
        list(entry.keys())[0] if isinstance(entry, dict) else entry.split(":")[0]
        for entry in offering["proof_points"]["summary"]
    }
    missing = summary_ids - registry_ids
    assert not missing, f"offering.yaml references unknown proof IDs: {missing}"

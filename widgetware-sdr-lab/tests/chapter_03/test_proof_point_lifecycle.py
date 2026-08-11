"""Gate test: the proof-point lifecycle model actually works — a proof
point is only usable when its status is "approved" AND it hasn't passed its
valid_until date, checked against a fixed reference date rather than the
real clock (so this test doesn't start failing on its own down the line,
and "is it expired" stays reproducible in CI regardless of when CI runs).
"""

import copy
from datetime import date
from pathlib import Path

import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"

# Fixed reference point for "is this proof point still valid" — deliberately
# not datetime.date.today(). Update this only when the fixture data in
# proof-points.yaml is deliberately refreshed alongside it.
REPO_RELEASE_DATE = date(2026, 8, 10)


def _load_proof_points():
    data = yaml.safe_load((CONFIG_DIR / "proof-points.yaml").read_text())
    return data["proof_points"]


def is_usable(entry: dict, as_of: date) -> bool:
    if entry["status"] != "approved":
        return False
    valid_until = date.fromisoformat(entry["valid_until"])
    return as_of <= valid_until


def test_all_currently_approved_proof_points_are_valid_as_of_release_date():
    for entry in _load_proof_points():
        if entry["status"] == "approved":
            valid_until = date.fromisoformat(entry["valid_until"])
            assert REPO_RELEASE_DATE <= valid_until, (
                f"{entry['proof_id']} is status=approved but valid_until "
                f"{entry['valid_until']} has passed as of {REPO_RELEASE_DATE}"
            )


def test_retired_fixture_is_correctly_not_usable():
    """PP-004 is a deliberate retired fixture, not an accident — this proves
    the lifecycle rule against a real registry entry, not only synthetic
    mutations below."""
    entries = {e["proof_id"]: e for e in _load_proof_points()}
    assert "PP-004" in entries, "expected retired fixture PP-004 is missing"
    assert not is_usable(entries["PP-004"], REPO_RELEASE_DATE)


def test_is_usable_rejects_non_approved_status():
    entry = copy.deepcopy(_load_proof_points()[0])
    entry["status"] = "pending_review"
    assert not is_usable(entry, REPO_RELEASE_DATE)


def test_is_usable_rejects_expired_valid_until():
    entry = copy.deepcopy(_load_proof_points()[0])
    entry["valid_until"] = "2020-01-01"  # long past REPO_RELEASE_DATE
    assert not is_usable(entry, REPO_RELEASE_DATE)


def test_is_usable_accepts_approved_and_current():
    entry = copy.deepcopy(_load_proof_points()[0])
    entry["status"] = "approved"
    entry["valid_until"] = "2099-01-01"
    assert is_usable(entry, REPO_RELEASE_DATE)


@pytest.mark.parametrize("field", ["source_reference", "allowed_contexts", "prohibited_wording", "owner"])
def test_every_proof_point_has_required_lifecycle_fields(field):
    for entry in _load_proof_points():
        assert field in entry, f"{entry['proof_id']} missing required field {field!r}"


def test_offering_does_not_reference_an_inactive_proof_point():
    """The direct enforcement of 'an offering must not reference an
    inactive or nonexistent proof point' — test_cross_file_integrity.py
    adds the fuller cross-file integrity suite; this is the
    lifecycle-specific half of it."""
    offering = yaml.safe_load((CONFIG_DIR / "offering.yaml").read_text())
    entries = {e["proof_id"]: e for e in _load_proof_points()}

    referenced_ids = [
        list(item.keys())[0] for item in offering["proof_points"]["summary"]
    ]
    for proof_id in referenced_ids:
        assert proof_id in entries, f"offering.yaml references nonexistent proof point {proof_id}"
        assert is_usable(entries[proof_id], REPO_RELEASE_DATE), (
            f"offering.yaml references {proof_id}, which is not currently usable "
            f"(status={entries[proof_id]['status']!r}, valid_until={entries[proof_id]['valid_until']!r})"
        )

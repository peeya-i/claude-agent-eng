"""Gate test: every config file validates against a formal JSON Schema, and
the schemas actually reject the error classes they're supposed to — not
just accept the current good files.

This turns config/*.yaml from "loosely structured examples that happen to
parse" into real configuration contracts: a typo in a field name, an
invalid enum value, or a malformed date fails loudly here instead of
silently reaching an agent at runtime.
"""

import copy
import json
from pathlib import Path

import jsonschema
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"
SCHEMA_DIR = CONFIG_DIR / "schemas"

CONFIG_SCHEMA_PAIRS = [
    ("icp.yaml", "icp.schema.json"),
    ("offering.yaml", "offering.schema.json"),
    ("proof-points.yaml", "proof-points.schema.json"),
    ("voice.yaml", "voice.schema.json"),
    ("evidence-policy.yaml", "evidence-policy.schema.json"),
]


def _load_yaml(name):
    return yaml.safe_load((CONFIG_DIR / name).read_text())


def _load_schema(name):
    return json.loads((SCHEMA_DIR / name).read_text())


def _validate(data, schema):
    jsonschema.validate(
        instance=data, schema=schema, format_checker=jsonschema.FormatChecker()
    )


@pytest.mark.parametrize("config_file,schema_file", CONFIG_SCHEMA_PAIRS)
def test_every_schema_file_exists_and_is_valid_json_schema(config_file, schema_file):
    schema_path = SCHEMA_DIR / schema_file
    assert schema_path.exists(), f"missing schema for {config_file}: {schema_file}"
    schema = json.loads(schema_path.read_text())
    jsonschema.Draft7Validator.check_schema(schema)


@pytest.mark.parametrize("config_file,schema_file", CONFIG_SCHEMA_PAIRS)
def test_current_config_validates_against_its_schema(config_file, schema_file):
    data = _load_yaml(config_file)
    schema = _load_schema(schema_file)
    _validate(data, schema)  # raises on failure


def test_schema_rejects_misspelled_field_name():
    data = _load_yaml("icp.yaml")
    schema = _load_schema("icp.schema.json")
    data["industy"] = data.pop("industry")  # typo
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_unexpected_extra_field():
    data = _load_yaml("voice.yaml")
    schema = _load_schema("voice.schema.json")
    data["unexpected_field"] = "should not be allowed"
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_invalid_claim_type():
    data = _load_yaml("evidence-policy.yaml")
    schema = _load_schema("evidence-policy.schema.json")
    data["claim_types"]["speculation"] = data["claim_types"].pop("hypothesis")
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_invalid_support_type():
    data = _load_yaml("evidence-policy.yaml")
    schema = _load_schema("evidence-policy.schema.json")
    data["support_types"]["maybe"] = data["support_types"].pop("unsupported")
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_malformed_date():
    data = copy.deepcopy(_load_yaml("proof-points.yaml"))
    schema = _load_schema("proof-points.schema.json")
    data["proof_points"][0]["last_reviewed_date"] = "05/01/2026"  # not ISO 8601
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_missing_proof_point_id():
    data = copy.deepcopy(_load_yaml("proof-points.yaml"))
    schema = _load_schema("proof-points.schema.json")
    del data["proof_points"][0]["proof_id"]
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_malformed_proof_id_pattern():
    data = copy.deepcopy(_load_yaml("proof-points.yaml"))
    schema = _load_schema("proof-points.schema.json")
    data["proof_points"][0]["proof_id"] = "not-a-valid-id"
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_invalid_employee_range_type():
    data = _load_yaml("icp.yaml")
    schema = _load_schema("icp.schema.json")
    data["company_size"]["minimum_employees"] = "five thousand"  # not an integer
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_negative_employee_count():
    data = _load_yaml("icp.yaml")
    schema = _load_schema("icp.schema.json")
    data["company_size"]["minimum_employees"] = -100
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)


def test_schema_rejects_unsupported_disclosure_status():
    data = copy.deepcopy(_load_yaml("proof-points.yaml"))
    schema = _load_schema("proof-points.schema.json")
    data["proof_points"][0]["disclosure_status"] = "top-secret"  # not in the enum
    with pytest.raises(jsonschema.ValidationError):
        _validate(data, schema)

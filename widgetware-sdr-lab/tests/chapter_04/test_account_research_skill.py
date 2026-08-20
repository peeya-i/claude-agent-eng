"""Gate test: the account-research Skill's contract, not just that its
files exist.

Checks that SKILL.md has real, parseable frontmatter with a description
detailed enough to actually gate activation (not a one-liner that could
describe any research Skill), that every body section the Skill depends on
is present, that schema.json is itself a valid JSON Schema, and that the
worked example both validates against it and — the part a "does it parse"
check would miss — actually fails to validate once corrupted.
"""

import copy
import json
import re
from pathlib import Path

import jsonschema
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "account-research"
SKILL_MD = SKILL_DIR / "SKILL.md"
SCHEMA_PATH = SKILL_DIR / "schema.json"
EXAMPLE_PATH = SKILL_DIR / "examples" / "example-output.json"

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

REQUIRED_SECTIONS = [
    "purpose",
    "when to use",
    "inputs",
    "procedure",
    "output contract",
    "failure behavior",
]


def _raw_skill_md():
    return SKILL_MD.read_text()


def _frontmatter():
    match = FRONTMATTER_PATTERN.match(_raw_skill_md())
    assert match, "SKILL.md must open with YAML frontmatter delimited by '---' lines"
    return yaml.safe_load(match.group(1))


def _description_is_detailed_enough(description: str) -> bool:
    """A real activation-gating description, not a generic one-liner.

    Requires enough length to actually say something, plus explicit
    positive ("use when...") and negative ("do not use...") conditions —
    the two things a vague description like "a company research Skill"
    cannot provide.
    """
    if not isinstance(description, str):
        return False
    lowered = description.lower()
    return (
        len(description) > 200
        and "use when" in lowered
        and "do not use" in lowered
    )


def test_skill_md_exists():
    assert SKILL_MD.exists(), "SKILL.md is missing"


def test_skill_md_has_frontmatter_with_name_and_description():
    frontmatter = _frontmatter()
    assert isinstance(frontmatter, dict), "frontmatter did not parse to a mapping"
    assert frontmatter.get("name"), "frontmatter is missing a non-empty 'name'"
    assert frontmatter.get("description"), "frontmatter is missing a non-empty 'description'"


def test_frontmatter_name_matches_skill_directory():
    frontmatter = _frontmatter()
    assert frontmatter["name"] == SKILL_DIR.name, (
        f"frontmatter name {frontmatter['name']!r} does not match "
        f"directory name {SKILL_DIR.name!r}"
    )


def test_description_specifies_activation_conditions_not_just_a_label():
    description = _frontmatter()["description"]
    assert _description_is_detailed_enough(description), (
        "description is not detailed enough to gate activation on its own "
        "(needs meaningful length plus explicit 'use when' / 'do not use' "
        "conditions, not just a generic label)"
    )


def test_description_check_actually_rejects_a_generic_one_liner():
    """The inverse of the previous test — proves the detail check
    discriminates, rather than trivially passing anything with content."""
    assert not _description_is_detailed_enough("A company research Skill.")
    assert not _description_is_detailed_enough("Researches companies.")


def test_description_mentions_the_concrete_required_inputs():
    """A description that never mentions what it actually needs (a company
    name and website) is exactly the kind of generic label this Skill's
    description must not be."""
    description = _frontmatter()["description"].lower()
    assert "company" in description
    assert "website" in description


@pytest.mark.parametrize("section", REQUIRED_SECTIONS)
def test_required_body_section_present(section):
    headers = re.findall(r"^##\s+(.+)$", _raw_skill_md(), re.MULTILINE)
    headers_lower = [h.lower() for h in headers]
    assert any(section in h for h in headers_lower), (
        f"SKILL.md is missing a body section covering {section!r} "
        f"(found headers: {headers})"
    )


def test_schema_json_exists_and_is_valid_json_schema():
    assert SCHEMA_PATH.exists(), "schema.json is missing"
    schema = json.loads(SCHEMA_PATH.read_text())
    jsonschema.Draft7Validator.check_schema(schema)


def test_example_output_exists():
    assert EXAMPLE_PATH.exists(), "examples/example-output.json is missing"


def _load_schema():
    return json.loads(SCHEMA_PATH.read_text())


def _load_example():
    return json.loads(EXAMPLE_PATH.read_text())


def test_example_output_validates_against_schema():
    jsonschema.validate(instance=_load_example(), schema=_load_schema())  # raises on failure


@pytest.mark.parametrize("field", _load_schema()["required"] if SCHEMA_PATH.exists() else [])
def test_example_output_fails_when_required_field_is_removed(field):
    data = copy.deepcopy(_load_example())
    schema = _load_schema()
    del data[field]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=data, schema=schema)


def test_example_output_fails_when_confidence_is_above_one():
    data = copy.deepcopy(_load_example())
    schema = _load_schema()
    data["confidence"] = 1.5
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=data, schema=schema)


def test_example_output_fails_when_confidence_is_below_zero():
    data = copy.deepcopy(_load_example())
    schema = _load_schema()
    data["confidence"] = -0.1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=data, schema=schema)


def test_example_output_fails_when_confidence_is_not_a_number():
    data = copy.deepcopy(_load_example())
    schema = _load_schema()
    data["confidence"] = "low"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=data, schema=schema)

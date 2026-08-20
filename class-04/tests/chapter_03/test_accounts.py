"""Gate test: every candidate account in accounts.csv can be
deterministically checked against the ICP — not eyeballed.

Until these checks pass, a row is a *candidate* account, not a confirmed
ICP match: normalized fields (industry_family, region, employee_band) are
what get checked by machine; industry_detail and fit_reason are for humans
reading the file, not for validation.
"""

import csv
from pathlib import Path
from urllib.parse import urlparse

import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"
ACCOUNTS_PATH = REPO_ROOT / "data" / "accounts.csv"

REQUIRED_COLUMNS = [
    "company_name",
    "website",
    "industry_family",
    "industry_detail",
    "country",
    "region",
    "employee_band",
    "fit_reason",
]

# Lower bound of each band, for a deterministic minimum_employees check.
EMPLOYEE_BAND_LOWER_BOUND = {
    "50-200": 50,
    "200-500": 200,
    "500-1000": 500,
    "1000-2000": 1000,
}


def _load_accounts():
    with ACCOUNTS_PATH.open(newline="") as f:
        return list(csv.DictReader(f))


def _load_icp():
    return yaml.safe_load((CONFIG_DIR / "icp.yaml").read_text())


def test_accounts_csv_has_required_columns():
    with ACCOUNTS_PATH.open(newline="") as f:
        fieldnames = csv.DictReader(f).fieldnames
    missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
    assert not missing, f"accounts.csv missing columns: {missing}"


def test_accounts_csv_rows_parse_cleanly():
    """Every row must have exactly the expected column count — an unquoted
    comma inside a field silently corrupts the row instead of failing
    loudly, so check shape explicitly rather than trusting csv.DictReader
    not to have swallowed a stray column into None."""
    for row in _load_accounts():
        assert None not in row, (
            f"{row.get('company_name', '?')}: row has more fields than the header "
            "(likely an unquoted comma inside a field)"
        )
        assert None not in row.values(), (
            f"{row.get('company_name', '?')}: row has fewer fields than the header"
        )


@pytest.mark.parametrize("row_index", range(10))
def test_each_account_industry_family_matches_icp(row_index):
    accounts = _load_accounts()
    icp = _load_icp()
    row = accounts[row_index]
    assert row["industry_family"] in icp["industry"], (
        f"{row['company_name']}: industry_family {row['industry_family']!r} "
        f"not in icp.yaml's industry list {icp['industry']}"
    )


@pytest.mark.parametrize("row_index", range(10))
def test_each_account_region_matches_icp_geography(row_index):
    accounts = _load_accounts()
    icp = _load_icp()
    row = accounts[row_index]
    assert row["region"] in icp["geography"], (
        f"{row['company_name']}: region {row['region']!r} "
        f"not in icp.yaml's geography list {icp['geography']}"
    )


@pytest.mark.parametrize("row_index", range(10))
def test_each_account_meets_minimum_employee_size(row_index):
    accounts = _load_accounts()
    icp = _load_icp()
    row = accounts[row_index]
    band = row["employee_band"]
    assert band in EMPLOYEE_BAND_LOWER_BOUND, f"{row['company_name']}: unknown employee_band {band!r}"
    lower_bound = EMPLOYEE_BAND_LOWER_BOUND[band]
    assert lower_bound >= icp["company_size"]["minimum_employees"], (
        f"{row['company_name']}: employee_band {band!r} (lower bound {lower_bound}) "
        f"is below icp.yaml's minimum_employees ({icp['company_size']['minimum_employees']})"
    )


@pytest.mark.parametrize("row_index", range(10))
def test_each_account_has_a_valid_website(row_index):
    accounts = _load_accounts()
    row = accounts[row_index]
    parsed = urlparse(row["website"])
    assert parsed.scheme in ("http", "https"), f"{row['company_name']}: website has no http(s) scheme"
    assert parsed.netloc, f"{row['company_name']}: website has no domain"


@pytest.mark.parametrize("row_index", range(10))
def test_each_account_has_nonempty_fit_reason(row_index):
    accounts = _load_accounts()
    row = accounts[row_index]
    assert row["fit_reason"].strip(), f"{row['company_name']}: fit_reason is empty"


def test_no_duplicate_company_names():
    accounts = _load_accounts()
    normalized = [a["company_name"].strip().lower() for a in accounts]
    duplicates = {name for name in normalized if normalized.count(name) > 1}
    assert not duplicates, f"duplicate company names: {duplicates}"


def test_no_duplicate_website_domains():
    accounts = _load_accounts()
    domains = [urlparse(a["website"]).netloc.lower().removeprefix("www.") for a in accounts]
    duplicates = {d for d in domains if domains.count(d) > 1}
    assert not duplicates, f"duplicate website domains: {duplicates}"

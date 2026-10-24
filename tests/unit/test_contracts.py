from __future__ import annotations

import copy
import json

import pytest

from malltest.contracts import CONTRACT_DIR, load_json, load_schema, validate_contract


pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("schema_name", "example_name"),
    [
        ("product-page.schema.json", "product-page.json"),
        ("order-page.schema.json", "order-page.json"),
        ("login.schema.json", "login.json"),
    ],
)
def test_contract_examples_are_valid(schema_name: str, example_name: str) -> None:
    example = load_json(CONTRACT_DIR / "examples" / example_name)
    assert validate_contract(example, schema_name) is example


def test_product_page_rejects_missing_pagination_field() -> None:
    example = load_json(CONTRACT_DIR / "examples" / "product-page.json")
    broken = copy.deepcopy(example)
    del broken["data"]["total"]

    with pytest.raises(AssertionError, match="data: 'total' is a required property"):
        validate_contract(broken, "product-page.schema.json")


def test_product_page_rejects_negative_stock() -> None:
    example = load_json(CONTRACT_DIR / "examples" / "product-page.json")
    broken = copy.deepcopy(example)
    broken["data"]["list"][0]["stock"] = -1

    with pytest.raises(AssertionError, match="data/list/0/stock"):
        validate_contract(broken, "product-page.schema.json")


def test_schema_files_are_machine_readable() -> None:
    schema_files = sorted(CONTRACT_DIR.glob("*.schema.json"))
    assert len(schema_files) == 4
    for path in schema_files:
        json.loads(path.read_text(encoding="utf-8"))
        load_schema(path.name)

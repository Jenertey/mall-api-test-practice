from __future__ import annotations

import pytest

from malltest.checks import assert_page_shape, assert_product_shape


pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_product_list_page_contract(admin_api) -> None:
    data = assert_page_shape(admin_api.product_list(page_num=1, page_size=5))
    assert len(data["list"]) <= 5
    assert data["pageNum"] == 1
    assert data["pageSize"] == 5
    if data["list"]:
        assert_product_shape(data["list"][0])


def test_product_list_supports_page_size_one(admin_api) -> None:
    data = assert_page_shape(admin_api.product_list(page_num=1, page_size=1))
    assert len(data["list"]) <= 1


def test_product_simple_list_returns_name_and_id(admin_api) -> None:
    payload = admin_api.product_simple_list()
    assert isinstance(payload, dict)
    assert payload.get("code") == 200
    items = payload.get("data") or []
    assert isinstance(items, list)
    if items:
        assert "id" in items[0]
        assert "name" in items[0]

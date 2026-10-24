from __future__ import annotations

import pytest

from malltest.checks import assert_product_shape, result_data
from malltest.data import ProductFactory


pytestmark = pytest.mark.unit


def test_product_factory_builds_unique_skus() -> None:
    first = ProductFactory.build(category_id=1, brand_id=1)
    second = ProductFactory.build(category_id=1, brand_id=1)
    assert first.product_sn != second.product_sn
    assert first.payload["productSn"] == first.product_sn
    assert first.payload["stock"] == 50
    assert first.payload["price"] > 0


def test_product_factory_payload_has_required_fields() -> None:
    draft = ProductFactory.build(category_id=2, brand_id=3, stock=9, price=10.5)
    assert draft.payload["productCategoryId"] == 2
    assert draft.payload["brandId"] == 3
    assert draft.payload["skuStockList"][0]["stock"] == 9
    assert draft.payload["skuStockList"][0]["price"] == 10.5


def test_result_and_product_assertions() -> None:
    payload = {
        "code": 200,
        "data": {"id": 1, "name": "demo", "productSn": "MALLTEST-1", "price": 1.0, "stock": 3},
    }
    product = assert_product_shape(result_data(payload))
    assert product["id"] == 1

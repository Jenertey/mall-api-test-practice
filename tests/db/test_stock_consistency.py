from __future__ import annotations

import os

import pytest


pytestmark = [pytest.mark.db]


def test_product_and_sku_stock_are_not_negative(db) -> None:
    product_id = int(os.getenv("MALLTEST_SAMPLE_PRODUCT_ID", "0"))
    if product_id <= 0:
        pytest.skip("Set MALLTEST_SAMPLE_PRODUCT_ID to a real product id")

    product = db.product_row(product_id)
    assert product is not None, f"product {product_id} does not exist"
    assert int(product["stock"]) >= 0

    rows = db.sku_stock_rows(product_id)
    assert rows, f"product {product_id} has no SKU stock rows"
    for row in rows:
        assert int(row["stock"]) >= 0
        assert int(row["lock_stock"]) >= 0

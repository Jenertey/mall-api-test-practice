from __future__ import annotations

import os

import pytest

from malltest.checks import assert_page_shape, assert_product_shape, result_data
from malltest.data import ProductFactory


pytestmark = [pytest.mark.api, pytest.mark.mutating]


@pytest.fixture(autouse=True)
def require_mutation_flag() -> None:
    if os.getenv("MALLTEST_RUN_MUTATION_TESTS") != "1":
        pytest.skip("Set MALLTEST_RUN_MUTATION_TESTS=1 against a disposable environment")


def test_create_read_and_delete_product(admin_api, settings) -> None:
    draft = ProductFactory.build(
        category_id=settings.category_id,
        brand_id=settings.brand_id,
        stock=12,
        price=88.0,
    )
    product_id = None
    try:
        result_data(admin_api.product_create(draft.payload))

        products = assert_page_shape(
            admin_api.product_list(keyword=draft.payload["name"], page_size=10)
        )
        matches = [item for item in products["list"] if item.get("productSn") == draft.product_sn]
        assert matches, "created product could not be found in the product list"
        product_id = int(matches[0]["id"])

        product = assert_product_shape(result_data(admin_api.product_update_info(product_id)))
        assert product["name"] == draft.payload["name"]
        assert int(product["stock"]) == 12
    finally:
        if product_id is not None:
            admin_api.product_delete_status(product_id)

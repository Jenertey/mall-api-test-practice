from __future__ import annotations

from typing import Any


def result_data(payload: Any) -> Any:
    assert isinstance(payload, dict), f"expected a JSON object, got {type(payload).__name__}"
    assert payload.get("code") == 200, f"business code was not 200: {payload}"
    return payload.get("data")


def assert_page_shape(payload: Any) -> dict:
    data = result_data(payload)
    assert isinstance(data, dict), f"expected page data, got {type(data).__name__}"
    assert isinstance(data.get("list"), list), "page data should contain a list"
    assert isinstance(data.get("total"), int), "page data should contain an integer total"
    assert isinstance(data.get("pageNum"), int), "page data should contain pageNum"
    assert isinstance(data.get("pageSize"), int), "page data should contain pageSize"
    return data


def assert_product_shape(product: Any) -> dict:
    assert isinstance(product, dict), "product should be a JSON object"
    for key in ("id", "name", "productSn", "price", "stock"):
        assert key in product, f"product is missing {key}"
    return product


def assert_order_shape(order: Any) -> dict:
    assert isinstance(order, dict), "order should be a JSON object"
    for key in ("id", "orderSn", "status"):
        assert key in order, f"order is missing {key}"
    return order

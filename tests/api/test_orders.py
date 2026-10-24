from __future__ import annotations

import pytest

from malltest.checks import assert_order_shape, assert_page_shape


pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_order_list_page_contract(admin_api) -> None:
    data = assert_page_shape(admin_api.order_list(page_num=1, page_size=5))
    assert len(data["list"]) <= 5
    if data["list"]:
        assert_order_shape(data["list"][0])


def test_order_list_accepts_cancelled_status_filter(admin_api) -> None:
    data = assert_page_shape(admin_api.order_list(page_num=1, page_size=5, status=4))
    assert isinstance(data["list"], list)

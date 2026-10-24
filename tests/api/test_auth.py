from __future__ import annotations

import pytest

from malltest.api import MallAdminApi
from malltest.client import ApiError


pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_login_returns_bearer_token(admin_api: MallAdminApi) -> None:
    assert admin_api.token
    assert admin_api.token.lower().startswith("bearer ")


def test_invalid_password_is_rejected(settings) -> None:
    api = MallAdminApi(settings)
    with pytest.raises(ApiError):
        api.login(password="not-the-right-password")


def test_product_list_requires_authentication(settings) -> None:
    api = MallAdminApi(settings)
    payload = api.product_list(page_size=1)
    assert isinstance(payload, dict)
    assert payload.get("code") in {401, 403}

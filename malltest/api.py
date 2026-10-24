from __future__ import annotations

from typing import Any

from .client import ApiError, JsonApiClient
from .config import Settings


class MallAdminApi(JsonApiClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings.admin_base_url, settings.timeout)
        self.settings = settings
        self.token: str | None = None

    def login(self, username: str | None = None, password: str | None = None) -> dict[str, Any]:
        response = self.request(
            "POST",
            "/admin/login",
            json_body={
                "username": username or self.settings.admin_username,
                "password": password or self.settings.admin_password,
            },
        )
        payload = response.payload
        if not isinstance(payload, dict) or payload.get("code") != 200:
            raise ApiError(
                "Mall admin login failed",
                status_code=response.result_code(),
                payload=payload,
                url=response.url,
            )
        data = payload.get("data") or {}
        token = data.get("token")
        if not token:
            raise ApiError("Mall admin login did not return a token", payload=payload, url=response.url)
        token_head = data.get("tokenHead") or "Bearer "
        self.token = token if str(token).startswith(token_head.strip()) else f"{token_head}{token}"
        self.session.headers.update({"Authorization": self.token})
        return data

    def product_list(self, *, page_num: int = 1, page_size: int = 5, keyword: str | None = None) -> Any:
        params = {"pageNum": page_num, "pageSize": page_size}
        if keyword:
            params["keyword"] = keyword
        return self.request("GET", "/product/list", params=params).payload

    def product_simple_list(self, keyword: str | None = None) -> Any:
        params = {"keyword": keyword} if keyword else None
        return self.request("GET", "/product/simpleList", params=params).payload

    def product_update_info(self, product_id: int) -> Any:
        return self.request("GET", f"/product/updateInfo/{product_id}").payload

    def product_create(self, payload: dict[str, Any]) -> Any:
        return self.request("POST", "/product/create", json_body=payload).payload

    def product_delete_status(self, product_id: int) -> Any:
        return self.request(
            "POST",
            "/product/update/deleteStatus",
            params={"ids": [product_id], "deleteStatus": 1},
        ).payload

    def order_list(self, *, page_num: int = 1, page_size: int = 5, status: int | None = None) -> Any:
        params = {"pageNum": page_num, "pageSize": page_size}
        if status is not None:
            params["status"] = status
        return self.request("GET", "/order/list", params=params).payload

    def order_detail(self, order_id: int) -> Any:
        return self.request("GET", f"/order/{order_id}").payload

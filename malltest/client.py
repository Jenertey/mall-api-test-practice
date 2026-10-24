from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import requests

from .logging_utils import log_snapshot, redact_sensitive


LOGGER = logging.getLogger("malltest.http")


@dataclass
class ApiResponse:
    status_code: int
    payload: Any
    url: str
    headers: dict[str, str]
    cookies: dict[str, str]
    request_id: str
    elapsed_ms: int

    def result_code(self) -> int | None:
        if isinstance(self.payload, dict):
            value = self.payload.get("code")
            return value if isinstance(value, int) else None
        return None


class ApiError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        payload: Any = None,
        url: str | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload
        self.url = url
        self.request_id = request_id


class JsonApiClient:
    def __init__(self, base_url: str, timeout: float = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        expected_statuses: tuple[int, ...] = (200,),
    ) -> ApiResponse:
        url = f"{self.base_url}{path}"
        request_id = uuid4().hex[:8]
        started_at = time.perf_counter()
        LOGGER.debug(
            "request id=%s method=%s url=%s params=%s body=%s",
            request_id,
            method,
            url,
            log_snapshot(redact_sensitive(params)),
            log_snapshot(json_body),
        )
        try:
            response = self.session.request(
                method,
                url,
                params=params,
                json=json_body,
                timeout=self.timeout,
            )
        except requests.RequestException:
            LOGGER.exception("request_failed id=%s method=%s url=%s", request_id, method, url)
            raise
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        try:
            payload = response.json()
        except ValueError:
            payload = response.text

        result = ApiResponse(
            status_code=response.status_code,
            payload=payload,
            url=url,
            headers=dict(response.headers),
            cookies=dict(response.cookies),
            request_id=request_id,
            elapsed_ms=elapsed_ms,
        )
        LOGGER.debug(
            "response id=%s status=%s elapsed_ms=%s body=%s",
            request_id,
            response.status_code,
            elapsed_ms,
            log_snapshot(payload),
        )
        if expected_statuses and response.status_code not in expected_statuses:
            raise ApiError(
                f"{method} {url} returned HTTP {response.status_code} (request {request_id})",
                status_code=response.status_code,
                payload=payload,
                url=url,
                request_id=request_id,
            )
        return result

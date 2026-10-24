from __future__ import annotations

import pytest

from malltest.api import MallAdminApi
from malltest.config import Settings
from malltest.db import DbInspector


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture(scope="session")
def admin_api(settings: Settings) -> MallAdminApi:
    api = MallAdminApi(settings)
    try:
        api.login()
    except Exception as exc:
        pytest.skip(f"Mall admin API is not available: {exc}")
    return api


@pytest.fixture(scope="session")
def db(settings: Settings) -> DbInspector:
    if not settings.db_configured:
        pytest.skip("Set MALLTEST_DB_HOST to enable database checks")
    inspector = DbInspector(settings)
    try:
        inspector.ping()
    except Exception as exc:
        pytest.skip(f"Mall database is not available: {exc}")
    return inspector

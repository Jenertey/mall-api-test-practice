from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    admin_base_url: str
    admin_username: str
    admin_password: str
    category_id: int
    brand_id: int
    timeout: float
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            admin_base_url=os.getenv("MALLTEST_ADMIN_URL", "http://localhost:8080").rstrip("/"),
            admin_username=os.getenv("MALLTEST_ADMIN_USERNAME", "admin"),
            admin_password=os.getenv("MALLTEST_ADMIN_PASSWORD", "macro123"),
            category_id=int(os.getenv("MALLTEST_CATEGORY_ID", "1")),
            brand_id=int(os.getenv("MALLTEST_BRAND_ID", "1")),
            timeout=float(os.getenv("MALLTEST_TIMEOUT", "10")),
            db_host=os.getenv("MALLTEST_DB_HOST", "").strip(),
            db_port=int(os.getenv("MALLTEST_DB_PORT", "3306")),
            db_user=os.getenv("MALLTEST_DB_USER", "root"),
            db_password=os.getenv("MALLTEST_DB_PASSWORD", "root"),
            db_name=os.getenv("MALLTEST_DB_NAME", "mall"),
        )

    @property
    def db_configured(self) -> bool:
        return bool(self.db_host)

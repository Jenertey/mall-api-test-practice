from __future__ import annotations

from typing import Any

from .config import Settings


class DbInspector:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _connect(self):
        try:
            import pymysql
        except ImportError as exc:
            raise RuntimeError("PyMySQL is required for database checks") from exc
        return pymysql.connect(
            host=self.settings.db_host,
            port=self.settings.db_port,
            user=self.settings.db_user,
            password=self.settings.db_password,
            database=self.settings.db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def ping(self) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 AS ok")
                row = cursor.fetchone()
                assert row and row["ok"] == 1

    def product_row(self, product_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, product_sn, stock FROM pms_product WHERE id = %s",
                    (product_id,),
                )
                return cursor.fetchone()

    def sku_stock_rows(self, product_id: int) -> list[dict[str, Any]]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, product_id, sku_code, stock, lock_stock "
                    "FROM pms_sku_stock WHERE product_id = %s ORDER BY id",
                    (product_id,),
                )
                return list(cursor.fetchall())

    def order_row(self, order_id: int) -> dict[str, Any] | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, order_sn, status, total_amount FROM oms_order WHERE id = %s",
                    (order_id,),
                )
                return cursor.fetchone()

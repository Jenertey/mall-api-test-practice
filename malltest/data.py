from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class ProductDraft:
    payload: dict
    product_sn: str


class ProductFactory:
    @staticmethod
    def build(
        *,
        category_id: int,
        brand_id: int,
        stock: int = 50,
        price: float = 199.0,
    ) -> ProductDraft:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        product_sn = f"MALLTEST-{stamp}-{uuid4().hex[:8].upper()}"
        name = f"接口测试商品 {stamp}-{uuid4().hex[:4].upper()}"
        payload = {
            "brandId": brand_id,
            "productCategoryId": category_id,
            "name": name,
            "subTitle": "自动化测试数据，请勿用于生产",
            "description": "由 Mall 接口测试练习的数据工厂生成",
            "productSn": product_sn,
            "price": price,
            "originalPrice": round(price * 1.2, 2),
            "stock": stock,
            "lowStock": 5,
            "unit": "件",
            "weight": 0.5,
            "sort": 0,
            "publishStatus": 1,
            "newStatus": 1,
            "recommandStatus": 1,
            "verifyStatus": 1,
            "previewStatus": 1,
            "serviceIds": "1,2,3",
            "keywords": "malltest,api-test",
            "note": "created by mall-api-test-practice",
            "albumPics": "",
            "pic": "",
            "skuStockList": [
                {
                    "skuCode": product_sn,
                    "price": price,
                    "stock": stock,
                    "lowStock": 5,
                    "pic": "",
                    "sale": 0,
                    "promotionPrice": 0,
                    "lockStock": 0,
                    "spData": "",
                }
            ],
            "productAttributeValueList": [],
            "productLadderList": [],
            "productFullReductionList": [],
            "memberPriceList": [],
            "subjectProductRelationList": [],
            "prefrenceAreaProductRelationList": [],
        }
        return ProductDraft(payload=payload, product_sn=product_sn)

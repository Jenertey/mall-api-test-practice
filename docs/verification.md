# 验证记录

## 2026-10-24

环境：Windows、Python 3.12.14。

已执行的离线检查：

```text
python -m compileall -q malltest tests
python -m pytest -m "unit" -q
11 passed, 10 deselected
```

`pytest --collect-only` 共收集 21 个测试：

- 11 个离线单元/契约测试
- 10 个真实 API、写操作或 MySQL 测试

尚未执行的真实服务测试：

- Mall 后台 API 用例
- 商品写操作生命周期用例
- MySQL 库存一致性用例

这些用例要求按 Mall 官方文档启动后台和数据库，因此没有在本次离线验证中标注为通过。

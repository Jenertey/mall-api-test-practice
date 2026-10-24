# Mall 商城接口自动化测试练习

GitHub：[Jenertey/mall-api-test-practice](https://github.com/Jenertey/mall-api-test-practice)

这是一个面向软件测试实习岗位的个人练习项目。我从测试设计、接口封装、数据准备、契约校验到持续集成，独立完成了一套可运行的接口测试工程；被测系统是开源项目 [macrozheng/mall](https://github.com/macrozheng/mall)。

> 本项目不包含 Mall 源码，也不代表 Mall 作者。Mall 的代码、接口和业务规则归上游作者所有。这里展示的是我独立编写的测试框架与测试资产。

## 项目目标

- 用 pytest + requests 组织可维护的接口自动化测试
- 覆盖管理员登录、商品分页、订单分页和商品 CRUD 主链路
- 用 JSON Schema 固化响应契约，便于发现字段缺失和类型变化
- 对请求与响应日志做敏感字段脱敏，避免 Token、密码和 Cookie 泄露
- 通过 MySQL 检查商品与 SKU 库存数据是否一致
- 在 GitHub Actions 中运行不依赖外部服务的离线测试

## 当前验证状态

- 已执行：Python 编译检查、11 项离线单元/JSON Schema 契约测试，详见 `docs/verification.md`
- 未在仓库 CI 中执行：真实 Mall API 与 MySQL 用例
- 真实接口用例需要自行启动 Mall 后台；没有实际运行的项目不会在文档中标注“已通过”

## 目录结构

```text
.
├─ malltest/                 # API 客户端、配置、数据工厂、断言、契约与脱敏工具
├─ tests/api/                # 登录、商品、订单和商品生命周期接口测试
├─ tests/db/                 # 商品与 SKU 库存一致性检查
├─ tests/unit/               # 无需启动被测系统的单元与契约测试
├─ contracts/                # JSON Schema 与示例响应
├─ docs/                     # 测试计划、用例矩阵、缺陷模板、面试讲稿
└─ .github/workflows/        # 离线测试 CI
```

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### 1. 运行离线检查

不需要启动 Mall，也不需要数据库：

```powershell
python -m pytest -m "unit"
```

这会执行数据工厂、响应断言、JSON Schema 契约和日志脱敏测试。

### 2. 运行真实接口测试

先按 Mall 官方文档启动后台接口，默认地址为 `http://localhost:8080`。然后运行只读冒烟集或完整只读集：

```powershell
python -m pytest -m "api and smoke and not mutating"
python -m pytest -m "api and not mutating"
```

商品写操作用例默认跳过，只应连接到可丢弃的测试环境：

```powershell
$env:MALLTEST_RUN_MUTATION_TESTS = "1"
python -m pytest -m "api and mutating"
```

### 3. 运行数据库检查

在 `.env` 中填写 `MALLTEST_DB_*`，并指定一个真实商品 ID：

```powershell
$env:MALLTEST_SAMPLE_PRODUCT_ID = "1"
python -m pytest -m "db"
```

### 4. 生成 Allure 报告

```powershell
python -m pytest -m "api and not mutating" --alluredir=artifacts/allure-results
allure serve artifacts/allure-results
```

## 环境变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `MALLTEST_ADMIN_URL` | `http://localhost:8080` | Mall 后台 API 地址 |
| `MALLTEST_ADMIN_USERNAME` | `admin` | 管理员账号 |
| `MALLTEST_ADMIN_PASSWORD` | `macro123` | 管理员密码；仅从环境读取 |
| `MALLTEST_CATEGORY_ID` | `1` | 测试商品分类 |
| `MALLTEST_BRAND_ID` | `1` | 测试品牌 |
| `MALLTEST_TIMEOUT` | `10` | 请求超时秒数 |
| `MALLTEST_DB_HOST` | 空 | MySQL 主机；不填则跳过数据库检查 |
| `MALLTEST_DB_PORT` | `3306` | MySQL 端口 |
| `MALLTEST_DB_USER` | `root` | MySQL 用户名 |
| `MALLTEST_DB_PASSWORD` | `root` | MySQL 密码；仅从环境读取 |
| `MALLTEST_DB_NAME` | `mall` | Mall 数据库名 |
| `MALLTEST_RUN_MUTATION_TESTS` | `0` | 写操作用例开关 |
| `MALLTEST_SAMPLE_PRODUCT_ID` | `0` | 数据库检查使用的商品 ID |

## 测试设计

`docs/case-matrix.csv` 记录了 22 条测试场景，按登录、商品、订单、数据库和框架能力分类，并标注优先级与自动化状态。当前自动化覆盖包括：

- 管理员正确/错误密码登录
- 未授权访问商品接口
- 商品列表分页字段和 `pageSize=1` 边界
- 商品简单列表、订单列表和状态筛选
- 商品创建、按唯一 `productSn` 反查、读取和删除
- 商品与 SKU 库存非负检查
- 离线响应契约与敏感信息脱敏

## 契约与安全设计

- `contracts/*.schema.json` 使用 JSON Schema Draft 2020-12 描述登录、商品分页和订单分页响应
- `contracts/examples/` 保存脱敏后的样本响应，使 CI 无需外部服务也能验证契约
- `malltest/logging_utils.py` 递归遮蔽 `password`、`token`、`authorization`、`cookie` 等字段
- HTTP 调试日志只输出脱敏且有长度上限的请求/响应快照
- 写接口默认关闭，避免误操作非测试环境

## 原创工作

本仓库的原创部分包括：接口客户端与会话封装、商品数据工厂、分页/结果码断言、JSON Schema 契约层、日志脱敏、MySQL 库存检查、pytest 分层、Allure 接入、CI 配置和项目文档。测试场景与代码由我独立完成，Mall 仅作为被测系统。

## 已知限制

- 不包含 UI 自动化、支付链路和性能测试
- 商品创建依赖 Mall 中已存在的分类和品牌数据
- 数据库表结构可能随 Mall 版本变化
- 离线契约样本用于结构校验，不能替代真实接口联调

## 许可

本仓库原创代码使用 MIT License。被测系统的许可证和版权信息请以其官方仓库为准，详见 `NOTICE`。

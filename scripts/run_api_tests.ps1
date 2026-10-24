$ErrorActionPreference = "Stop"
python -m pytest -m "api and not mutating" --alluredir=artifacts/allure-results

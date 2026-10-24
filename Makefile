.PHONY: install test unit api smoke report

install:
	python -m pip install -r requirements.txt

unit:
	pytest -m "unit"

api:
	pytest -m "api and not mutating"

smoke:
	pytest -m "api and smoke and not mutating"

test: unit

report:
	pytest -m "api and not mutating" --alluredir=artifacts/allure-results

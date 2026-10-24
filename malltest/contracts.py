from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


CONTRACT_DIR = Path(__file__).resolve().parent.parent / "contracts"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(name: str) -> dict[str, Any]:
    schema = load_json(CONTRACT_DIR / name)
    Draft202012Validator.check_schema(schema)
    return schema


def _contract_registry() -> Registry:
    registry = Registry()
    for path in CONTRACT_DIR.glob("*.schema.json"):
        resource = Resource.from_contents(
            load_json(path),
            default_specification=DRAFT202012,
        )
        registry = registry.with_resource(path.name, resource)
    return registry


def validate_contract(payload: Any, schema_name: str) -> Any:
    validator = Draft202012Validator(load_schema(schema_name), registry=_contract_registry())
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.absolute_path))
    if errors:
        details = []
        for error in errors[:5]:
            path = "/".join(str(part) for part in error.absolute_path) or "<root>"
            details.append(f"{path}: {error.message}")
        raise AssertionError(f"{schema_name} contract failed: " + "; ".join(details))
    return payload

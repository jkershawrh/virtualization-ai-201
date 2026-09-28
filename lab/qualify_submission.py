from __future__ import annotations

import json
import pathlib
import sys

import yaml


root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "lab/starter")
required = [
    "qualification-request.schema.json",
    "qualification-response.schema.json",
    "vm_client.py",
    "secret-reference.yaml",
    "service.yaml",
    "networkpolicy.yaml",
]
errors = []
for name in required:
    path = root / name
    if not path.exists():
        errors.append(f"missing {name}")
        continue
    text = path.read_text()
    if "TODO" in text:
        errors.append(f"{name} still contains TODO")
    if name.endswith(".json"):
        try:
            value = json.loads(text)
            if value.get("additionalProperties") is not False and "response" not in name:
                errors.append(f"{name} must reject undeclared fields")
        except json.JSONDecodeError as exc:
            errors.append(f"{name} is invalid JSON: {exc}")
    if name.endswith(".yaml"):
        try:
            yaml.safe_load(text)
        except yaml.YAMLError as exc:
            errors.append(f"{name} is invalid YAML: {exc}")

secret_text = (root / "secret-reference.yaml").read_text() if (root / "secret-reference.yaml").exists() else ""
if "secretKeyRef" not in secret_text:
    errors.append("secret-reference.yaml must use secretKeyRef")
if "value:" in secret_text:
    errors.append("secret-reference.yaml must not contain an inline value")

if errors:
    print("RED: learner contract is not qualified")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print("GREEN: learner contract files satisfy the local structural gate")

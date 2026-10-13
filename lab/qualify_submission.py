from __future__ import annotations

import json
import pathlib
import sys
import argparse

import yaml


parser = argparse.ArgumentParser(description='Qualify the completed learner stage')
parser.add_argument('root', nargs='?', default='lab/starter')
parser.add_argument('--stage', choices=('contract', 'full'), default='full')
arguments = parser.parse_args()
root = pathlib.Path(arguments.root)
required = [
    "qualification-request.schema.json",
    "qualification-response.schema.json",
    "vm_client.py",
    "secret-reference.yaml",
    "service.yaml",
    "networkpolicy.yaml",
]
if arguments.stage == 'contract':
    required = required[:3]
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
if arguments.stage == 'full' and "secretKeyRef" not in secret_text:
    errors.append("secret-reference.yaml must use secretKeyRef")
if arguments.stage == 'full' and "value:" in secret_text:
    errors.append("secret-reference.yaml must not contain an inline value")

if errors:
    print("RED: learner contract is not qualified")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print("GREEN: learner contract files satisfy the local structural gate")

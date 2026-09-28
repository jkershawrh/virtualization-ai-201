import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def load(relative: str):
    return json.loads((CONTRACTS / relative).read_text())


class ContractTests(unittest.TestCase):
    def validate(self, schema_name: str, example_name: str):
        validator = Draft202012Validator(load(schema_name), format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(load(example_name)), key=lambda error: list(error.path))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def test_qualified_request_matches_schema(self):
        self.validate("qualification-request.schema.json", "examples/qualified-request.json")

    def test_qualified_response_matches_schema(self):
        self.validate("qualification-response.schema.json", "examples/qualified-response.json")

    def test_unavailable_response_matches_schema_and_has_no_advisory(self):
        self.validate("qualification-response.schema.json", "examples/unavailable-response.json")
        response = load("examples/unavailable-response.json")
        self.assertNotIn("advisory", response)
        self.assertNotIn("model", response)
        self.assertFalse(response["ai_participated"])

    def test_request_contract_has_no_secret_fields(self):
        request = load("examples/qualified-request.json")
        lowered = json.dumps(request).lower()
        for forbidden in ("password", "api_key", "token", "secret"):
            self.assertNotIn(forbidden, lowered)

    def test_openapi_exposes_only_versioned_qualification_paths(self):
        openapi = yaml.safe_load((CONTRACTS / "openapi.yaml").read_text())
        self.assertEqual(openapi["openapi"], "3.1.0")
        self.assertIn("/api/v1/qualify", openapi["paths"])
        self.assertIn("/api/v1/evidence/{evidence_id}", openapi["paths"])


class ContractDrivenDevelopmentRedTests(unittest.TestCase):
    def test_reference_implementation_assets_exist(self):
        required = [
            ROOT / "workload/app.py",
            ROOT / "workload/vm_client.py",
            ROOT / "charts/virtualization-ai-201/templates/adapter.yaml",
            ROOT / "charts/virtualization-ai-201/templates/networkpolicy.yaml",
            ROOT / "showroom/content/modules/ROOT/pages/03-author.adoc",
        ]
        missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
        self.assertEqual(missing, [], f"CDD RED: implementation assets not authored yet: {missing}")


if __name__ == "__main__":
    unittest.main()

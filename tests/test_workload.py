import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker

from workload.app import ContractError, EVIDENCE, qualify, validate_request
from workload.vm_client import build_request


ROOT = Path(__file__).resolve().parents[1]


class WorkloadTests(unittest.TestCase):
    def setUp(self):
        EVIDENCE.clear()
        self.request = json.loads((ROOT / "contracts/examples/qualified-request.json").read_text())

    def validate_response(self, value):
        schema = json.loads((ROOT / "contracts/qualification-response.schema.json").read_text())
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value))
        self.assertEqual(errors, [], "\n".join(error.message for error in errors))

    def test_rehearsal_path_is_labeled_and_human_owned(self):
        with patch.dict(os.environ, {"ADAPTER_MODE": "rehearsal"}, clear=False):
            response, evidence = qualify(self.request)
        self.validate_response(response)
        self.assertEqual(response["source_state"], "REHEARSAL")
        self.assertFalse(response["ai_participated"])
        self.assertEqual(response["authority"], "HUMAN_REVIEW_REQUIRED")
        self.assertEqual(evidence["validation"], "PASS")

    def test_unavailable_path_contains_no_advisory_or_model(self):
        with patch.dict(os.environ, {"ADAPTER_MODE": "rehearsal"}, clear=False):
            response, evidence = qualify(self.request, "unavailable")
        self.validate_response(response)
        self.assertEqual(response["outcome"], "MODEL_UNAVAILABLE")
        self.assertNotIn("advisory", response)
        self.assertNotIn("model", response)
        self.assertFalse(evidence["ai_participated"])

    def test_evidence_redacts_note_and_never_contains_secret(self):
        with patch.dict(os.environ, {"ADAPTER_MODE": "rehearsal"}, clear=False):
            _, evidence = qualify(self.request)
        encoded = json.dumps(evidence).lower()
        self.assertNotIn(self.request["note"].lower(), encoded)
        self.assertNotIn("api_key", encoded)
        self.assertRegex(evidence["request_sha256"], r"^[0-9a-f]{64}$")

    def test_secret_bearing_request_is_rejected(self):
        invalid = dict(self.request, token="forbidden")
        with self.assertRaises(ContractError):
            validate_request(invalid)

    def test_live_mode_without_identity_fails_closed(self):
        environment = {"ADAPTER_MODE": "live", "MODEL_ENDPOINT": "", "MODEL_ID": ""}
        with patch.dict(os.environ, environment, clear=False):
            response, _ = qualify(self.request)
        self.assertEqual(response["outcome"], "MODEL_UNAVAILABLE")
        self.assertEqual(response["source_state"], "OFFLINE")
        self.assertFalse(response["ai_participated"])

    def test_vm_client_builds_contract_without_credentials(self):
        request = build_request("Synthetic note")
        validate_request(request)
        lowered = json.dumps(request).lower()
        self.assertNotIn("password", lowered)
        self.assertNotIn("api_key", lowered)


if __name__ == "__main__":
    unittest.main()

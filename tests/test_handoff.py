import hashlib
import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"
SOURCE_REVISION = "7928d13b9b00820e81f6c96ec047e3c22ec26e3f"


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.handoff = yaml.safe_load((HANDOFF / "launchpad-handoff.yaml").read_text())

    def test_handoff_grants_no_release_authority(self):
        authority = self.handoff["factory_receipt"]["authority"]
        self.assertTrue(authority)
        self.assertTrue(all(value is False for value in authority.values()))
        certification = self.handoff["proposed_launchpad_intake"]["certification_proposal"]
        self.assertEqual(certification["stage"], "factory-development-verified")
        self.assertEqual(certification["max_workshop_seats"], 0)

    def test_receipt_hashes_are_content_addressed(self):
        evidence = self.handoff["factory_receipt"]["factory_evidence"]
        artifacts = self.handoff["factory_receipt"]["artifacts"]
        refs = list(evidence.values()) + [
            artifacts["workload"]["release_receipt"],
            artifacts["presentation"]["release_receipt"],
        ]
        for ref in refs:
            path = HANDOFF / ref["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), ref["sha256"])

    def test_published_receipts_are_non_certifying_and_source_bound(self):
        for component in ("adapter", "presentation"):
            receipt = json.loads((HANDOFF / f"evidence/published-{component}-release.json").read_text())
            self.assertEqual(receipt["source_revision"], SOURCE_REVISION)
            self.assertEqual(receipt["certification"], "NOT CLAIMED")
            self.assertEqual(receipt["live_openshift_validation"], "NOT RUN")
            self.assertEqual(receipt["scan"]["severity_counts"]["critical"], 0)
            self.assertEqual(receipt["scan"]["severity_counts"]["high"], 0)


if __name__ == "__main__":
    unittest.main()

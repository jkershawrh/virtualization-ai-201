import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/release-images.yml"


class ReleaseWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text()

    def test_all_external_actions_are_commit_pinned(self):
        uses = re.findall(r"^\s*-?\s*uses:\s*([^\s]+)\s*$", self.text, re.MULTILINE)
        self.assertGreaterEqual(len(uses), 10)
        for action in uses:
            self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_release_is_exact_revision_and_amd64_bound(self):
        self.assertIn('[[ "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ ]]', self.text)
        self.assertIn('test "$DISPATCH_SHA" = "$EXPECTED_SHA"', self.text)
        self.assertIn("platforms: linux/amd64", self.text)
        self.assertIn("SOURCE_REVISION=${{ inputs.expected_sha }}", self.text)
        self.assertIn('docker pull "$digest_ref"', self.text)

    def test_full_inventory_and_hard_zero_high_critical_gate(self):
        self.assertIn("Inventory every detected vulnerability", self.text)
        self.assertIn("Block every high or critical vulnerability", self.text)
        self.assertIn("severity-cutoff: high", self.text)
        self.assertNotIn("only-fixed:", self.text)

    def test_publication_is_signed_attested_verified_and_retained(self):
        for expected in (
            "cosign sign --yes", "cosign attest --yes --type spdxjson", "cosign attest --yes --type custom",
            "cosign verify --certificate-identity", "cosign verify-attestation --type spdxjson",
            "cosign verify-attestation --type custom", "retention-days: 90",
        ):
            self.assertIn(expected, self.text)

    def test_runtime_and_sanitized_showroom_images_are_released(self):
        self.assertIn("virtualization-ai-201-presentation", self.text)
        self.assertIn("virtualization-ai-201-adapter", self.text)
        self.assertIn("virtualization-ai-201-showroom-content", self.text)
        self.assertIn("containerfile: showroom-content/Containerfile", self.text)

        containerfile = (ROOT / "showroom-content" / "Containerfile").read_text()
        entrypoint = (ROOT / "showroom-content" / "entrypoint.sh").read_text()
        self.assertIn("COPY showroom /bundle/showroom", containerfile)
        self.assertNotIn("COPY . ", containerfile)
        self.assertNotIn("git clone", entrypoint)


if __name__ == "__main__":
    unittest.main()

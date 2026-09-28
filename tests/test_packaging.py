import subprocess
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CHART = ROOT / "charts/virtualization-ai-201"


class PackagingTests(unittest.TestCase):
    def test_runtime_images_are_digest_pinned_and_minimal(self):
        presentation = (ROOT / "Containerfile").read_text()
        adapter = (ROOT / "workload/Containerfile").read_text()
        self.assertRegex(presentation, r"FROM cgr\.dev/chainguard/nginx@sha256:[0-9a-f]{64}")
        self.assertRegex(adapter, r"FROM cgr\.dev/chainguard/python@sha256:[0-9a-f]{64}")
        self.assertNotIn(":latest", presentation)
        self.assertNotIn(":latest", adapter)

    def test_helm_chart_lints_and_renders_required_boundaries(self):
        lint = subprocess.run(["helm", "lint", str(CHART)], capture_output=True, text=True)
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        render = subprocess.run(
            ["helm", "template", "virtualization-ai-201", str(CHART), "--namespace", "virtualization-ai-201"],
            capture_output=True, text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        for kind in ("VirtualMachine", "NetworkPolicy", "Service", "Deployment"):
            self.assertIn(f"kind: {kind}", render.stdout)
        self.assertNotIn("MODEL_API_KEY\n", render.stdout)

    def test_defaults_are_rehearsal_fail_closed_and_secret_free(self):
        values = yaml.safe_load((CHART / "values.yaml").read_text())
        self.assertEqual(values["adapter"]["mode"], "rehearsal")
        self.assertEqual(values["adapter"]["model"]["secretName"], "")
        self.assertEqual(values["adapter"]["model"]["egressCIDR"], "")
        self.assertNotIn("password", str(values).lower())

    def test_live_render_uses_secret_references_not_values(self):
        render = subprocess.run(
            [
                "helm", "template", "virtualization-ai-201", str(CHART),
                "--set", "adapter.mode=live", "--set", "adapter.model.secretName=model-runtime",
                "--set", "adapter.model.egressCIDR=203.0.113.10/32",
            ],
            capture_output=True, text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn("secretKeyRef:", render.stdout)
        self.assertIn('name: "model-runtime"', render.stdout)
        self.assertNotIn("api-key-value", render.stdout)
        self.assertIn("203.0.113.10/32", render.stdout)

    def test_published_overlay_uses_exact_immutable_candidates(self):
        values = yaml.safe_load((CHART / "values.published.yaml").read_text())
        self.assertEqual(
            values["adapter"]["image"]["digest"],
            "sha256:f17a7cc9c708e58186bd38878630dc563b853f78e1535be3435c0c8aec34eedb",
        )
        self.assertEqual(
            values["presentation"]["image"]["digest"],
            "sha256:9f58d0a74d58201156547d21be2bc8a6b30f9d00619206dcce337d03e0ea4569",
        )
        self.assertEqual(values["adapter"]["image"]["tag"], "")
        self.assertEqual(values["presentation"]["image"]["tag"], "")


if __name__ == "__main__":
    unittest.main()

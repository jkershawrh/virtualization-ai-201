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
        self.assertIn("kind: Route", render.stdout)
        self.assertIn("name: lab", render.stdout)
        self.assertNotIn("MODEL_API_KEY\n", render.stdout)

    def test_launchpad_flat_image_values_override_nested_defaults(self):
        workload = "ghcr.io/example/virt201-adapter@sha256:" + "a" * 64
        presentation = "ghcr.io/example/virt201-presentation@sha256:" + "b" * 64
        render = subprocess.run(
            [
                "helm", "template", "virtualization-ai-201", str(CHART),
                "--set-string", f"workload_image={workload}",
                "--set-string", f"presentation_image={presentation}",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn(f'image: "{workload}"', render.stdout)
        self.assertIn(f'image: "{presentation}"', render.stdout)

    def test_defaults_are_rehearsal_fail_closed_and_secret_free(self):
        values = yaml.safe_load((CHART / "values.yaml").read_text())
        self.assertEqual(values["adapter"]["mode"], "rehearsal")
        self.assertEqual(values["adapter"]["model"]["secretName"], "")
        self.assertEqual(values["adapter"]["model"]["egressCIDR"], "")
        self.assertEqual(values["adapter"]["model"]["egressNamespace"], "")
        self.assertEqual(values["adapter"]["model"]["egressPort"], 4000)
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

    def test_live_render_can_reach_a_namespaced_managed_model_service(self):
        render = subprocess.run(
            [
                "helm", "template", "virtualization-ai-201", str(CHART),
                "--set", "adapter.mode=live",
                "--set", "adapter.model.secretName=model-runtime",
                "--set", "adapter.model.egressNamespace=launchpad-flightpath-candidate",
                "--set", "adapter.model.egressPort=4000",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(render.returncode, 0, render.stderr)
        self.assertIn('kubernetes.io/metadata.name: "launchpad-flightpath-candidate"', render.stdout)
        self.assertIn("port: 4000", render.stdout)

    def test_vm_bootstrap_file_exists_before_learner_account_ownership(self):
        template = (CHART / "templates/vm.yaml").read_text()
        self.assertIn("owner: root:root", template)
        self.assertIn("chown, learner:learner, /home/learner/vm_client.py", template)

    def test_published_overlay_uses_exact_immutable_candidates(self):
        values = yaml.safe_load((CHART / "values.published.yaml").read_text())
        self.assertEqual(
            values["adapter"]["image"]["digest"],
            "sha256:ff9c6bd189955ebfee6e97714e62908d53824a39fac50c3a78b27466e7825e62",
        )
        self.assertEqual(
            values["presentation"]["image"]["digest"],
            "sha256:b6b7cf41d5044c005f84bbade273edad0daed061060094e11d202b24c95c0ee3",
        )
        self.assertEqual(values["adapter"]["image"]["tag"], "")
        self.assertEqual(values["presentation"]["image"]["tag"], "")


if __name__ == "__main__":
    unittest.main()

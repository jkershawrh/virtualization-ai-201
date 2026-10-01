import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SHOWROOM = ROOT / "showroom"


class ShowroomTests(unittest.TestCase):
    def test_deployed_showroom_discovers_the_playbook_from_repository_root(self):
        playbook = ROOT / "default-site.yml"
        self.assertTrue(playbook.is_file())
        config = yaml.safe_load(playbook.read_text())
        source = config["content"]["sources"][0]
        self.assertEqual(source["url"], ".")
        self.assertEqual(source["start_path"], "showroom/content")
        self.assertTrue((ROOT / source["start_path"] / "antora.yml").is_file())

    def test_showroom_has_independent_playbook(self):
        playbook = SHOWROOM / "default-site.yml"
        playbook_text = playbook.read_text()
        self.assertIn("start_page: virtualization-ai-201::index.adoc", playbook_text)
        self.assertIn("branches: HEAD", playbook_text)
        self.assertNotIn("start_path: .", playbook_text)
        self.assertIn(
            "https://github.com/rhpds/rhdp_showroom_theme/releases/download/v2.0.3/ui-bundle.zip",
            playbook_text,
        )
        self.assertNotIn("showroom_theme_rhdp/releases/download/v0.0.1", playbook_text)

    def test_lab_is_complete_and_construction_led(self):
        antora = yaml.safe_load((SHOWROOM / "content/antora.yml").read_text())
        self.assertEqual(antora["name"], "virtualization-ai-201")
        self.assertEqual(antora["version"], "main")
        nav = (SHOWROOM / "content/modules/ROOT/nav.adoc").read_text()
        for page in ("01-prerequisite", "02-frame", "03-author", "04-wire", "05-prove", "06-break", "07-evidence-reclaim"):
            self.assertIn(page, nav)

    def test_lab_requires_every_201_artifact_and_human_authority(self):
        text = "\n".join(path.read_text() for path in (SHOWROOM / "content/modules/ROOT/pages").glob("*.adoc"))
        for term in ("request", "response", "VM client", "Secret", "Service", "NetworkPolicy", "MODEL_UNAVAILABLE", "correlation", "reclaim"):
            self.assertIn(term, text)
        self.assertIn("human", text.lower())
        self.assertIn("REHEARSAL", text)
        self.assertIn("OFFLINE", text)
        self.assertIn("LIVE", text)

    def test_101_evidence_is_prerequisite_not_learner_work(self):
        text = (SHOWROOM / "content/modules/ROOT/pages/01-prerequisite.adoc").read_text()
        self.assertIn("Do not copy", text)
        self.assertIn("201 proof", text)

    def test_starters_are_intentionally_incomplete(self):
        for path in (ROOT / "lab/starter").iterdir():
            self.assertIn("TODO", path.read_text(), path.name)

    def test_lab_exposes_show_learn_do_prove_and_executable_steps(self):
        pages = SHOWROOM / "content/modules/ROOT/pages"
        text = "\n".join(path.read_text() for path in sorted(pages.glob("*.adoc")))
        for stage in ("== Show", "== Learn", "== Do", "== Prove"):
            self.assertIn(stage, text)
        self.assertGreaterEqual(text.count('role="execute"'), 8)

    def test_runtime_proof_uses_console_and_truthful_inference_assertions(self):
        prove = (SHOWROOM / "content/modules/ROOT/pages/05-prove.adoc").read_text()
        self.assertIn("OpenShift Console", prove)
        self.assertIn("VirtualMachines", prove)
        self.assertIn('source_state == "LIVE"', prove)
        self.assertIn('ai_participated == true', prove)
        self.assertIn('source_state == "REHEARSAL"', prove)
        self.assertIn('ai_participated == false', prove)

    def test_healthy_proof_originates_inside_the_vm_and_is_correlated(self):
        prove = (SHOWROOM / "content/modules/ROOT/pages/05-prove.adoc").read_text()
        self.assertIn("VM_SSH_PRIVATE_KEY", prove)
        self.assertIn("chmod 600 {ssh_key_path}", prove)
        self.assertIn("virtctl ssh --identity-file={ssh_key_path}", prove)
        self.assertIn("learner@vm/contract-author-vm", prove)
        self.assertIn("--command=", prove)
        self.assertIn("/tmp/launchpad-lab/contract-author-key", (SHOWROOM / "content/antora.yml").read_text())
        self.assertIn("/home/learner/vm_client.py", prove)
        self.assertIn('.guest == ($namespace + "/contract-author-vm")', prove)
        self.assertNotIn("VM-origin connectivity remains a separate proof", prove)

        reclaim = (
            SHOWROOM / "content/modules/ROOT/pages/07-evidence-reclaim.adoc"
        ).read_text()
        self.assertIn('rm -f "{ssh_key_path}"', reclaim)
        self.assertIn('test ! -e "{ssh_key_path}"', reclaim)

    def test_participant_cleanup_preserves_launchpad_owned_runtime(self):
        reclaim = (SHOWROOM / "content/modules/ROOT/pages/07-evidence-reclaim.adoc").read_text()
        self.assertIn("Launchpad", reclaim)
        self.assertIn("must not uninstall", reclaim)
        self.assertNotIn("helm uninstall", reclaim)
        self.assertIn("rm -f", reclaim)
        self.assertIn('role="execute"', reclaim)


if __name__ == "__main__":
    unittest.main()

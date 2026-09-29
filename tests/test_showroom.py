import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SHOWROOM = ROOT / "showroom"


class ShowroomTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()

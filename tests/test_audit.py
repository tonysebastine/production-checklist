import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "audit_engine" / "audit.py"
SPEC = importlib.util.spec_from_file_location("production_audit", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)

class AuditTests(unittest.TestCase):
    def test_control_count_and_validation_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "routes.py").write_text("from pydantic import BaseModel\nvalidate_payload()\n", encoding="utf-8")
            result = module.audit(root)
            self.assertEqual(result["summary"]["controls_total"], 43)
            item = next(c for c in result["controls"] if c["id"] == "SEC-02")
            self.assertEqual(item["status"], "Partial")
            self.assertEqual(item["evidence"][0]["path"], "routes.py")

    def test_secret_value_is_redacted(self):
        secret = "ghp_" + "A" * 36
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.py").write_text(f'TOKEN = "{secret}"\n', encoding="utf-8")
            result = module.audit(root)
            serialized = json.dumps(result)
            self.assertEqual(result["summary"]["potential_secrets"], 1)
            self.assertNotIn(secret, serialized)
            self.assertIn("redacted", serialized.lower())

    def test_placeholder_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env.example").write_text("API_KEY=your_secret_here\n", encoding="utf-8")
            result = module.audit(root)
            self.assertEqual(result["summary"]["potential_secrets"], 0)

    def test_report_has_required_matrix(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = module.to_markdown(module.audit(Path(tmp)))
            self.assertIn("| Category | Requirement | Current Status", report)
            self.assertIn("Potential secret detections", report)
            self.assertIn("Limitations", report)

if __name__ == "__main__":
    unittest.main()

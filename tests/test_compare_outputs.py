"""Local checks for A3 output comparisons (stdlib unittest only)."""

import json
import tempfile
import unittest
from pathlib import Path

from tests.compare_outputs import compare_outputs


class OutputComparisonTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.orig = self.root / "original.py"
        self.refac = self.root / "refactored.py"
        self.inputs = self.root / "p999.json"

    def prepare(self, original: str, refactored: str, cases: list[str]):
        self.orig.write_text(original, encoding="utf-8")
        self.refac.write_text(refactored, encoding="utf-8")
        self.inputs.write_text(json.dumps({"program_id": "p999", "inputs": cases}), encoding="utf-8")

    def compare(self, timeout=5.0):
        return compare_outputs(str(self.orig), str(self.refac), str(self.inputs), timeout)

    def test_equal_and_normalized_output(self):
        self.prepare("print('a  ')\nprint('b')", "print('a')\nprint('b')\nprint()", ["", "abc"])
        r = self.compare()
        self.assertEqual((r["total"], r["same"], r["different"], r["differences"]),
                         (2, 2, 0, []))

    def test_difference_indices_and_first_five_only(self):
        self.prepare("print('old')", "print('new')", ["a" * 700] * 7)
        r = self.compare()
        self.assertEqual((r["total"], r["same"], r["different"]), (7, 0, 7))
        self.assertEqual([row["input_index"] for row in r["differences"]], [0, 1, 2, 3, 4])
        self.assertEqual(len(r["differences"][0]["input"]), 500)
        self.assertEqual(r["differences"][0]["error"], "")

    def test_refactored_error_is_difference(self):
        self.prepare("print('ok')", "raise ValueError('deliberate failure')", [""])
        r = self.compare()
        self.assertEqual(r["different"], 1)
        self.assertIn("ValueError", r["differences"][0]["error"])

    def test_refactored_timeout_is_difference(self):
        self.prepare("print('ok')", "import time; time.sleep(3)", [""])
        r = self.compare(timeout=1.5)
        self.assertEqual(r["different"], 1)
        self.assertEqual(r["differences"][0]["error"], "timeout")

    def test_original_error_is_not_refactored_failure(self):
        self.prepare("raise RuntimeError('bad original')", "print('ok')", [""])
        with self.assertRaisesRegex(RuntimeError, "Original failed"):
            self.compare()

    def test_invalid_input_format(self):
        self.prepare("print('a')", "print('a')", [""])
        self.inputs.write_text(json.dumps({"inputs": [123]}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "All inputs must be strings"):
            self.compare()

    def test_bad_timeout(self):
        self.prepare("print('a')", "print('a')", [""])
        with self.assertRaises(ValueError):
            self.compare(timeout=0)

class BatchComparisonTests(unittest.TestCase):
    def test_batch_reads_summary_and_writes_separate_json(self):
        from tests.compare_outputs import batch_compare
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "data" / "programs").mkdir(parents=True)
            (repo / "data" / "new_inputs").mkdir()
            run_dir = repo / "outputs" / "p001" / "gpt" / "single"
            code_dir = run_dir / "round_0"
            code_dir.mkdir(parents=True)
            (repo / "data" / "programs.csv").write_text(
                "program_id,code_path\np001,data/programs/p001.py\n", encoding="utf-8"
            )
            (repo / "data" / "programs" / "p001.py").write_text("print('same')\n", encoding="utf-8")
            (code_dir / "code.py").write_text("print('same')\n", encoding="utf-8")
            (run_dir / "summary.json").write_text(json.dumps({"final_code": "round_0/code.py"}),
                                                   encoding="utf-8")
            (repo / "data" / "new_inputs" / "p001.json").write_text(
                json.dumps({"program_id": "p001", "inputs": ["x"]}), encoding="utf-8"
            )
            status = batch_compare(repo, "outputs", "difftest", program="p001", model="gpt")
            self.assertEqual(status, 0)
            result_path = repo / "difftest" / "p001" / "gpt" / "single.json"
            self.assertTrue(result_path.exists())
            saved = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual((saved["total"], saved["same"], saved["different"]), (1, 1, 0))
            self.assertEqual(saved["refactored_path"],
                             "outputs/p001/gpt/single/round_0/code.py")
            self.assertFalse((run_dir / "difftest").exists())
            self.assertEqual(batch_compare(repo, "outputs", "difftest", program="p001",
                                           model="gpt", skip_existing=True), 0)


if __name__ == "__main__":
    unittest.main()

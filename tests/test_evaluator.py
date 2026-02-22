import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluator import evaluate_syntax  # noqa: E402


def error_codes(report):
    return {entry["code"] for entry in report["errors"]}


def warning_codes(report):
    return {entry["code"] for entry in report["warnings"]}


class EvaluatorTests(unittest.TestCase):
    def test_valid_declarations_loop_and_api_call(self):
        code = """define path: Sketch
define direction: Vector

for vertex in path.vertices:
    createVector(1, 2, 3)
"""
        report = evaluate_syntax(code)
        self.assertTrue(report["valid"])
        self.assertEqual(report["errors"], [])

    def test_define_not_at_top(self):
        code = """define path: Sketch
createVector(1, 2, 3)
define later: Vector
"""
        report = evaluate_syntax(code)
        self.assertFalse(report["valid"])
        self.assertIn("DEFINE_NOT_AT_TOP", error_codes(report))

    def test_unknown_declared_type(self):
        code = "define thing: UnknownType\n"
        report = evaluate_syntax(code)
        self.assertFalse(report["valid"])
        self.assertIn("UNKNOWN_TYPE", error_codes(report))

    def test_duplicate_define(self):
        code = """define path: Sketch
define path: Sketch
"""
        report = evaluate_syntax(code)
        self.assertFalse(report["valid"])
        self.assertIn("DUPLICATE_DEFINE", error_codes(report))

    def test_unknown_function(self):
        code = """define path: Sketch
missingFunction(path)
"""
        report = evaluate_syntax(code)
        self.assertFalse(report["valid"])
        self.assertIn("UNKNOWN_FUNCTION", error_codes(report))

    def test_known_function_wrong_arity(self):
        code = "createVector(1, 2)\n"
        report = evaluate_syntax(code)
        self.assertFalse(report["valid"])
        self.assertIn("ARITY_MISMATCH", error_codes(report))

    def test_valid_method_call_on_known_receiver_type(self):
        code = """define direction: Vector
direction.normalize()
"""
        report = evaluate_syntax(code)
        self.assertTrue(report["valid"])
        self.assertEqual(report["errors"], [])

    def test_unknown_receiver_type_produces_warning(self):
        code = """for item in range(3):
    item.normalize()
"""
        report = evaluate_syntax(code)
        self.assertTrue(report["valid"])
        self.assertIn("UNKNOWN_RECEIVER_TYPE", warning_codes(report))

    def test_reject_unsupported_construct_import(self):
        code = "import os\n"
        report = evaluate_syntax(code)
        self.assertFalse(report["valid"])
        self.assertIn("UNSUPPORTED_SYNTAX_NODE", error_codes(report))

    def test_break_outside_loop(self):
        report = evaluate_syntax("break\n")
        self.assertFalse(report["valid"])
        self.assertIn("UNSUPPORTED_SYNTAX_NODE", error_codes(report))

    def test_accept_if_elif_else(self):
        code = """define direction: Vector
if True:
    direction.normalize()
elif False:
    pass
else:
    pass
"""
        report = evaluate_syntax(code)
        self.assertTrue(report["valid"])
        self.assertEqual(report["errors"], [])

    def test_accept_lambda_inside_filter(self):
        code = """define path: Sketch
filter(lambda v: v.length() > 0, path.vertices)
"""
        report = evaluate_syntax(code)
        self.assertTrue(report["valid"])
        self.assertEqual(report["errors"], [])

    def test_sort_validation(self):
        valid_simple = evaluate_syntax(
            """define arr: array
arr.sort()
"""
        )
        self.assertTrue(valid_simple["valid"])

        valid_with_key = evaluate_syntax(
            """define arr: array
arr.sort(key=lambda x: x)
"""
        )
        self.assertTrue(valid_with_key["valid"])

        invalid_positional = evaluate_syntax(
            """define arr: array
arr.sort(1)
"""
        )
        self.assertFalse(invalid_positional["valid"])
        self.assertIn("INVALID_SORT_USAGE", error_codes(invalid_positional))

    def test_cli_smoke(self):
        valid_code = "createVector(1, 2, 3)\n"
        valid_proc = subprocess.run(
            [sys.executable, "evaluator.py", "--code", valid_code],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(valid_proc.returncode, 0)
        valid_json = json.loads(valid_proc.stdout)
        self.assertTrue(valid_json["valid"])

        invalid_code = "import os\n"
        invalid_proc = subprocess.run(
            [sys.executable, "evaluator.py", "--code", invalid_code],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(invalid_proc.returncode, 1)
        invalid_json = json.loads(invalid_proc.stdout)
        self.assertFalse(invalid_json["valid"])


if __name__ == "__main__":
    unittest.main()

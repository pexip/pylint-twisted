"""Functional full-module tests for PyLint."""
import csv
from pathlib import Path

from pylint.testutils import LintModuleTest
from pylint.testutils.functional_test_file import FunctionalTestFile

import pylint_twisted


TEST_DIR = Path(__file__).parent.resolve()


class _TestDialect(csv.excel):
    delimiter = ":"
    lineterminator = "\n"


csv.register_dialect("test", _TestDialect)


def test_reactor_inference() -> None:
    test_file = FunctionalTestFile(TEST_DIR, "reactor.py")
    lint_test = LintModuleTest(test_file)
    lint_test.setUp()
    lint_test.runTest()

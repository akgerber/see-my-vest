import unittest
from dataclasses import dataclass

from click.testing import CliRunner

from see_my_vest import main


@dataclass
class E2ETestCase:
    input_file: str
    target_date: str
    precision: str
    expected_output: str


class TestE2E(unittest.TestCase):
    _DATADIR = "tests/csv_data/"

    def test_happy_path(self):
        runner = CliRunner()
        tests = [
            E2ETestCase("example1.csv", "2020-04-01", "0", "expected1_2020-04-01.csv"),
            E2ETestCase("example1_disordered.csv", "2020-04-01", "0", "expected1_2020-04-01.csv"),
            E2ETestCase("example2.csv", "2021-01-01", "0", "expected2_2021-01-01.csv"),
            E2ETestCase("example3.csv", "2021-01-01", "1", "expected3_2021-01-01.csv"),
        ]
        for test in tests:
            result = runner.invoke(
                main,
                args=[
                    self._DATADIR + test.input_file,
                    test.target_date,
                    test.precision,
                ],
            )
            with open(
                self._DATADIR + test.expected_output, encoding="utf8"
            ) as expected:
                self.assertListEqual(
                    result.output.splitlines(keepends=True), list(expected)
                )

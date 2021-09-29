import pytest
from dataclass_csv import CsvValueError

from see_my_vest import read_csv_input


def test_read_csv_input_happy_path():
    with open("tests/csv_data/example4.csv", encoding="utf8") as csv:
        events = read_csv_input(csv)
        assert len(events) == 9


def test_read_csv_input_invalid_file():
    with open("tests/csv_data/example_bad.csv", encoding="utf8") as csv:
        with pytest.raises(CsvValueError):
            read_csv_input(csv)

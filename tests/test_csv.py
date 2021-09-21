import pytest
from dataclass_csv import CsvValueError

from see_my_vest import parse_csv_input

def test_parse_csv_input_happy_path():
    with open("tests/csv_data/example2.csv") as csv:
        events = parse_csv_input(csv)
        assert(len(events) == 9)

def test_parse_csv_input_invalid_file():
    with open("tests/csv_data/example_bad.csv") as csv:
        with pytest.raises(CsvValueError):
            events = parse_csv_input(csv)


from decimal import Decimal, InvalidOperation
from dataclasses import dataclass
from typing import Type

import pytest

from parse_decimal import parse_decimal


@dataclass
class DecimalTestCase:
    input: str
    precision: int
    expected: Decimal


@dataclass
class FailureCase:
    input: str
    precision: int
    exception: Type[BaseException]


def test_happy_path():
    tests = [
        DecimalTestCase("10.5044444", 2, Decimal(10.50)),
        DecimalTestCase("10.5099900", 2, Decimal(10.50)),
        DecimalTestCase("00.5099900", 2, Decimal(0.50)),
        DecimalTestCase("000000000.5099900", 2, Decimal(0.50)),
        DecimalTestCase("0.5", 6, Decimal(0.5)),
        DecimalTestCase("10.5044444", 0, Decimal(10)),
    ]
    for test in tests:
        assert parse_decimal(test.input, test.precision) == test.expected


def test_invalid_input():
    tests = [
        FailureCase("50.47", -1, ValueError),
        FailureCase("hello.friend", 5, InvalidOperation),
    ]
    for test in tests:
        with pytest.raises(test.exception):
            parse_decimal(test.input, test.precision)

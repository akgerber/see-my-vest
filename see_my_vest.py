from datetime import datetime
from dataclasses import dataclass
from typing import List

import click
from dataclass_csv import dateformat, DataclassReader, CsvValueError


@dataclass
@dateformat("%Y-%m-%d")
class VestEventInput:
    event_type: str
    employee_id: str
    employee_name: str
    award_id: str
    date: datetime
    quantity: float


@dataclass
class VestEvent:
    date: datetime
    quantity: float
    event_type: str


@dataclass
class EquityAward:
    award_id: str
    employee_id: str
    employee_name: str
    vest_events: List[VestEvent]


def parse_csv_input(vesting_events_csv) -> List[VestEventInput]:
    reader = DataclassReader(
        vesting_events_csv,
        VestEventInput,
        fieldnames=[
            "event_type",
            "employee_id",
            "employee_name",
            "award_id",
            "date",
            "quantity",
        ],
    )
    return [row for row in reader]


@click.command()
@click.argument("vesting_events_csv", type=click.File())
@click.argument("target_date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.argument("precision", default=0, type=click.IntRange(0, 6))
def main(vesting_events_csv, target_date, precision):
    try:
        input_events = parse_csv_input(vesting_events_csv)
        print(input_events)
    except CsvValueError as e:
        click.echo(f"CSV parsing failed: {e}")


if __name__ == "__main__":
    main()

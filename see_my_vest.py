import typing
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import List, TextIO, Dict

import click
from dataclass_csv import DataclassReader, CsvValueError

from parse_decimal import parse_decimal
from vesting_types import (
    VestEventInput,
    EmployeeID,
    EmployeeEquityAwards,
    EquityAward,
    VestEvent,
)


# Transform CSV input to types well-suited for output requirements
def process_input_events(
    input_events: List[VestEventInput], precision: int
) -> Dict[EmployeeID, EmployeeEquityAwards]:
    awards: Dict[EmployeeID, EmployeeEquityAwards] = {}
    for event in input_events:
        if event.employee_id not in awards.keys():
            employee_awards = EmployeeEquityAwards(
                employee_id=event.employee_id,
                employee_name=event.employee_name,
                equity_awards={},
            )
            awards[event.employee_id] = employee_awards

        if event.award_id not in awards[event.employee_id].equity_awards.keys():
            equity_award = EquityAward(award_id=event.award_id, vest_events=[])
            awards[event.employee_id].equity_awards[event.award_id] = equity_award

        vest_event = VestEvent(
            date=event.date,
            quantity=parse_decimal(event.quantity, precision),
            event_type=event.event_type,
        )
        awards[event.employee_id].equity_awards[event.award_id].vest_events.append(
            vest_event
        )

    return awards


# Read CSV and do basic type/format validation via dataclass transformation
def read_csv_input(vesting_events_csv: TextIO) -> List[VestEventInput]:
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


def calculate_vested_by_date(events: List[VestEvent], target_date: datetime) -> Decimal:
    vested = Decimal(0)
    for event in events:
        if event.date > target_date:
            continue
        # TODO: refactor to pattern matching in Python 3.10
        if event.event_type == "VEST":
            vested += event.quantity
        elif event.event_type == "CANCEL":
            vested -= event.quantity
        else:
            raise ValueError(f"Invalid event type {event.event_type}")
    return vested


def generate_csv_output(
    awards: Dict[EmployeeID, EmployeeEquityAwards],
    target_date: datetime,
    precision: int,
):
    """
    Sort and process equity award information at target_date and output as CSV
    :param awards: EmployeeEquityAwards keyed by Employee ID
    :param target_date: Date at which to calculate the current equity awarded
    :param precision: How many decimal digits to output
    """
    for employee_id in sorted(awards.keys()):
        for award_id in sorted(awards[employee_id].equity_awards.keys()):
            name = awards[employee_id].employee_name
            shares_vested = calculate_vested_by_date(
                awards[employee_id].equity_awards[award_id].vest_events, target_date
            )
            click.echo(f"{employee_id},{name},{award_id},{shares_vested:.{precision}f}")


@click.command()
@click.argument("vesting_events_csv", type=click.File())
@click.argument("target_date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.argument("precision", default=0, type=click.IntRange(0, 6))
def main(vesting_events_csv, target_date, precision):
    try:
        input_events = read_csv_input(vesting_events_csv)
        awards = process_input_events(input_events, precision)
        generate_csv_output(awards, target_date, precision)
        return 0
    except CsvValueError as e:
        click.echo(f"CSV parsing failed: {e}", err=True)
        return 1
    except InvalidOperation as e:
        click.echo(f"Decimal parsing failed: {e}", err=True)
        return 1
    except ValueError as e:
        click.echo(f"Invalid input: {e}", err=True)
        return 1
    except Exception as e:
        click.echo(f"Unexpected exception: {e}", err=True)
        return 1


if __name__ == "__main__":
    main()

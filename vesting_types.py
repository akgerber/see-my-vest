from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict

from dataclass_csv import dateformat


@dataclass
@dateformat("%Y-%m-%d")
class VestEventInput:
    event_type: str
    employee_id: str
    employee_name: str
    award_id: str
    date: datetime
    # Read quantity as str to enable later conversion to Decimal without loss of precision
    quantity: str


EmployeeID = str
AwardID = str


@dataclass
class VestEvent:
    date: datetime
    quantity: Decimal
    event_type: str


@dataclass
class EquityAward:
    award_id: AwardID
    vest_events: List[VestEvent]


@dataclass
class EmployeeEquityAwards:
    employee_id: EmployeeID
    employee_name: str
    equity_awards: Dict[AwardID, EquityAward]

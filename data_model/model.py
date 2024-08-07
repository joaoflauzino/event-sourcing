from dataclasses import dataclass
from typing import Any
import datetime

@dataclass
class Event:
    timestamp: datetime.datetime

@dataclass
class AccountCreated(Event):
    account_id: str
    owner: str
    initial_balance: float

@dataclass
class MoneyDeposited(Event):
    account_id: str
    amount: float

@dataclass
class MoneyWithdrawn(Event):
    account_id: str
    amount: float

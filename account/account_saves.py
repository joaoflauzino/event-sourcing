from data_model.model import Event, AccountCreated, MoneyDeposited, MoneyWithdrawn
from typing import List
import datetime


class BankAccount:
    def __init__(self, account_id: str, owner: str, initial_balance: float):
        self.account_id = account_id
        self.owner = owner
        self.balance = initial_balance
        self.changes: List[Event] = []

    @staticmethod
    def from_events(events: List[Event]):
        if not events:
            raise ValueError("No events to restore state from")

        initial_event = events[0]
        if not isinstance(initial_event, AccountCreated):
            raise ValueError("The first event must be AccountCreated")

        account = BankAccount(initial_event.account_id, initial_event.owner, initial_event.initial_balance)
        for event in events[1:]:
            account.apply_event(event)
        return account

    def deposit(self, amount: float):
        event = MoneyDeposited(datetime.datetime.now(), self.account_id, amount)
        self.apply_event(event)
        self.changes.append(event)

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        event = MoneyWithdrawn(datetime.datetime.now(), self.account_id, amount)
        self.apply_event(event)
        self.changes.append(event)

    def apply_event(self, event: Event):
        if isinstance(event, MoneyDeposited):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawn):
            self.balance -= event.amount

    def get_uncommitted_changes(self) -> List[Event]:
        return self.changes
    
    def reset_uncommitted_changes(self) -> None:
        self.changes = []

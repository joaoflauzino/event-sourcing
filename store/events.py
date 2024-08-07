from typing import List
from data_model.model import Event


class EventStore:
    def __init__(self):
        self._events: List[Event] = []

    def save_event(self, event: Event):
        self._events.append(event)

    def get_events(self, account_id: str) -> List[Event]:
        return [event for event in self._events if hasattr(event, 'account_id') and event.account_id == account_id]

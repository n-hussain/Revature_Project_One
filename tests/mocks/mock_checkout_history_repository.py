from src.domain.checkout_history import CheckoutEvent
from datetime import datetime

class MockCheckoutHistoryRepo:
    def __init__(self):
        self._events = []

    def add_event(self, event: CheckoutEvent) -> None:
        self._events.append(event)

    def get_history_for_book(self, book_id: str) -> list[CheckoutEvent]:
        return [e for e in self._events if e.book_id == book_id]

    def get_history_all(self) -> list[CheckoutEvent]:
        return self._events.copy()

    def update_event(self, book_id: str, returned: bool, return_date: datetime = None) -> bool:
        updated = False
        for e in self._events:
            if e.book_id == book_id and not e.returned:
                e.returned = returned
                if return_date:
                    e.return_date = return_date
                updated = True
        return updated

    def delete_events_for_book(self, book_id: str) -> int:
        before_count = len(self._events)
        self._events = [e for e in self._events if e.book_id != book_id]
        return before_count - len(self._events)

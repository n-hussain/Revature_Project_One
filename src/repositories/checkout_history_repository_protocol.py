from typing import Protocol
from src.domain.checkout_history import CheckoutEvent

class CheckoutHistoryRepositoryProtocol(Protocol):
    def add_event(self, event: CheckoutEvent) -> None: 
        ...
    def get_history_for_book(self, book_id: str) -> list[CheckoutEvent]: 
        ...
    def mark_returned(self, book_id: str) -> None: 
        ...

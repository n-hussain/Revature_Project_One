from typing import Protocol, List
from src.domain.checkout_history import CheckoutEvent

class CheckoutHistoryRepositoryProtocol(Protocol):
    def add_event(self, event: CheckoutEvent) -> None:
        ...

    def get_history_for_book(self, book_id: str) -> List[CheckoutEvent]:
        ...

    def get_history_all(self) -> List[CheckoutEvent]:
        ...

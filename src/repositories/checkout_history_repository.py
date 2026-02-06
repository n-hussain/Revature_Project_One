import json
from datetime import datetime
from src.domain.checkout_history import CheckoutEvent
from src.repositories.checkout_history_repository_protocol import (
    CheckoutHistoryRepositoryProtocol,
)

class CheckoutHistoryRepository(CheckoutHistoryRepositoryProtocol):
    def __init__(self, filepath: str = "checkout_history.json"):
        self.filepath = filepath

    def _load(self) -> list[dict]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save(self, data: list[dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_event(self, event: CheckoutEvent) -> None:
        data = self._load()

        data.append(
            {
                "book_id": event.book_id,
                "checkout_date": (
                    event.checkout_date.isoformat()
                    if event.checkout_date
                    else None
                ),
                "return_date": (
                    event.return_date.isoformat()
                    if event.return_date
                    else None
                ),
                "returned": event.returned,
            }
        )

        self._save(data)

    def get_history_for_book(self, book_id: str) -> list[CheckoutEvent]:
        events: list[CheckoutEvent] = []

        for e in self._load():
            if e["book_id"] != book_id:
                continue

            events.append(
                CheckoutEvent(
                    book_id=e["book_id"],
                    checkout_date=(
                        datetime.fromisoformat(e["checkout_date"])
                        if e["checkout_date"]
                        else None
                    ),
                    return_date=(
                        datetime.fromisoformat(e["return_date"])
                        if e["return_date"]
                        else None
                    ),
                    returned=e["returned"],
                )
            )

        return events

    def get_history_all(self) -> list[CheckoutEvent]:
        return [
            CheckoutEvent(
                book_id=e["book_id"],
                checkout_date=(
                    datetime.fromisoformat(e["checkout_date"])
                    if e["checkout_date"]
                    else None
                ),
                return_date=(
                    datetime.fromisoformat(e["return_date"])
                    if e["return_date"]
                    else None
                ),
                returned=e["returned"],
            )
            for e in self._load()
        ]

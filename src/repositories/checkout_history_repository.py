import json
from datetime import datetime
from src.domain.checkout_history import CheckoutEvent
from src.repositories.checkout_history_repository_protocol import CheckoutHistoryRepositoryProtocol

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
                "checked_out_at": event.checked_out_at.isoformat(),
                "returned_at": None,
                "returned": False,
            }
        )
        self._save(data)

    def get_history_for_book(self, book_id: str) -> list[CheckoutEvent]:
        return [
            CheckoutEvent(
                book_id=e["book_id"],
                checked_out_at=datetime.fromisoformat(e["checked_out_at"]),
                returned_at=datetime.fromisoformat(e["returned_at"])
                if e["returned_at"]
                else None,
                returned=e["returned"],
            )
            for e in self._load()
            if e["book_id"] == book_id
        ]

    def mark_returned(self, book_id: str) -> None:
        data = self._load()
        for e in reversed(data):
            if e["book_id"] == book_id and not e["returned"]:
                e["returned"] = True
                e["returned_at"] = datetime.now().isoformat()
                break
        self._save(data)

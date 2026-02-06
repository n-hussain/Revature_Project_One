from datetime import datetime
from src.domain.checkout_history import CheckoutEvent
from src.repositories.book_repository_protocol import BookRepositoryProtocol
from src.repositories.checkout_history_repository_protocol import CheckoutHistoryRepositoryProtocol

class CheckoutService:
    def __init__(
        self,
        book_repo: BookRepositoryProtocol,
        history_repo: CheckoutHistoryRepositoryProtocol,
    ):
        self.book_repo = book_repo
        self.history_repo = history_repo

    def check_out(self, book_id: str) -> None:
        books = self.book_repo.get_all_books()
        book = next(b for b in books if b.book_id == book_id)

        book.check_out()
        self.book_repo.update_book(book)

        event = CheckoutEvent(
            book_id=book.book_id,
            checkout_date=datetime.now(),
            returned=False
        )
        self.history_repo.add_event(event)

    def check_in(self, book_id: str) -> None:
        books = self.book_repo.get_all_books()
        book = next(b for b in books if b.book_id == book_id)

        book.check_in()
        self.book_repo.update_book(book)

        event = CheckoutEvent(
            book_id=book.book_id,
            return_date=datetime.now(),
            returned=True
        )
        self.history_repo.add_event(event)

    def get_history_for_book(self, book_id: str) -> list[CheckoutEvent]:
        return self.history_repo.get_history_for_book(book_id)
    
    def get_history_all(self) -> list[CheckoutEvent]:
        return self.history_repo.get_history_all()

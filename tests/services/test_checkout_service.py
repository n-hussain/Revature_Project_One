import pytest
from datetime import datetime
from src.services.checkout_service import CheckoutService
from src.services.book_service import BookService
from tests.mocks.mock_book_repository import MockBookRepo
from tests.mocks.mock_checkout_history_repository import MockCheckoutHistoryRepo
from src.domain.book import Book

def test_check_out_book():
    book_repo = MockBookRepo()
    history_repo = MockCheckoutHistoryRepo()
    svc = CheckoutService(book_repo, history_repo)

    book = Book(title="Test Book", author="Author A")
    book_repo.add_book(book)

    svc.check_out(book.book_id)

    updated_book = book_repo.get_all_books()[0]
    assert updated_book.available is False

    events = history_repo.get_history_for_book(book.book_id)
    assert len(events) == 1
    assert events[0].returned is False
    assert events[0].checkout_date is not None

def test_check_in_book():
    book_repo = MockBookRepo()
    history_repo = MockCheckoutHistoryRepo()
    svc = CheckoutService(book_repo, history_repo)

    book = Book(title="Test Book", author="Author B")
    book_repo.add_book(book)

    svc.check_out(book.book_id)
    svc.check_in(book.book_id)

    updated_book = book_repo.get_all_books()[0]
    assert updated_book.available is True

    events = history_repo.get_history_for_book(book.book_id)
    returned_events = [e for e in events if e.returned]
    assert len(returned_events) == 1
    assert returned_events[0].return_date is not None

def test_get_history_for_book_multiple_events():
    book_repo = MockBookRepo()
    history_repo = MockCheckoutHistoryRepo()
    svc = CheckoutService(book_repo, history_repo)

    book1 = Book(title="Book 1", author="Author X")
    book2 = Book(title="Book 2", author="Author Y")
    book_repo.add_book(book1)
    book_repo.add_book(book2)

    svc.check_out(book1.book_id)
    svc.check_out(book2.book_id)
    svc.check_in(book1.book_id)

    events_book1 = svc.get_history_for_book(book1.book_id)
    events_book2 = svc.get_history_for_book(book2.book_id)

    assert len(events_book1) == 2
    assert len(events_book2) == 1

def test_get_history_all_books():
    book_repo = MockBookRepo()
    history_repo = MockCheckoutHistoryRepo()
    svc = CheckoutService(book_repo, history_repo)

    book1 = Book(title="Book A", author="Author A")
    book2 = Book(title="Book B", author="Author B")
    book_repo.add_book(book1)
    book_repo.add_book(book2)

    svc.check_out(book1.book_id)
    svc.check_out(book2.book_id)

    all_events = svc.get_history_all()
    assert len(all_events) == 2
    assert all(e.book_id in [book1.book_id, book2.book_id] for e in all_events)

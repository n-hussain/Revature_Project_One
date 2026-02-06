import pytest
from src.services.book_service import BookService
from tests.mocks.mock_book_repository import MockBookRepo
from src.domain.book import Book


def test_add_book_creates_book():
    repo = MockBookRepo()
    svc = BookService(repo)

    new_book = Book(title="New Book", author="Author A")
    book_id = svc.add_book(new_book)
    books = svc.get_all_books()

    assert len(books) == 1
    assert books[0].book_id == book_id
    assert books[0].title == "New Book"

def test_find_book_by_name_positive():
    repo = MockBookRepo()
    svc = BookService(repo)

    new_book = Book(title="Unique Title", author="Author X")
    svc.add_book(new_book)

    found = svc.find_book_by_name("Unique Title")
    assert len(found) == 1
    assert found[0].author == "Author X"

def test_find_book_by_name_negative_type():
    repo = MockBookRepo()
    svc = BookService(repo)

    with pytest.raises(TypeError) as e:
        svc.find_book_by_name(123)
    assert str(e.value) == "Expected str, got something else."

def test_update_existing_book():
    repo = MockBookRepo()
    svc = BookService(repo)

    book = Book(title="Old Title", author="Author B")
    svc.add_book(book)
    book.title = "Updated Title"

    result = svc.update_book(book)
    updated = svc.get_all_books()[0]

    assert result is True
    assert updated.title == "Updated Title"

def test_update_nonexistent_book_returns_false():
    repo = MockBookRepo()
    svc = BookService(repo)

    fake_book = Book(title="Fake", author="No One", book_id="nonexistent")
    result = svc.update_book(fake_book)
    assert result is False

def test_delete_existing_book():
    repo = MockBookRepo()
    svc = BookService(repo)

    book = Book(title="To Delete", author="Author C")
    book_id = svc.add_book(book)

    result = svc.delete_book(book_id)
    books = svc.get_all_books()

    assert result is True
    assert all(b.book_id != book_id for b in books)

def test_delete_nonexistent_book_returns_false():
    repo = MockBookRepo()
    svc = BookService(repo)

    result = svc.delete_book("fake_id")
    assert result is False

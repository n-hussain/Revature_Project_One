from src.domain.book import Book
import uuid

class MockBookRepo:
    def __init__(self):
        self._books = []

    def get_all_books(self) -> list[Book]:
        return self._books.copy()

    def add_book(self, book: Book) -> str:
        if not getattr(book, "book_id", None):
            book.book_id = str(uuid.uuid4())
        self._books.append(book)
        return book.book_id

    def find_book_by_name(self, query: str) -> list[Book]:
        return [b for b in self._books if b.title == query]

    def update_book(self, updated_book: Book) -> bool:
        for i, b in enumerate(self._books):
            if b.book_id == updated_book.book_id:
                self._books[i] = updated_book
                return True
        return False

    def delete_book(self, book_id: str) -> bool:
        initial_len = len(self._books)
        self._books = [b for b in self._books if b.book_id != book_id]
        return len(self._books) < initial_len

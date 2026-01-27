from typing import Protocol
from src.domain.book import Book

class BookRepositoryProtocol(Protocol):
    def get_all_books(self) -> list[Book]:
        ...

    def add_book(self, book:Book) -> str:
        ...

    def find_book_by_name(self, query:str) -> list[Book]:
        ...
    
    def update_book(self, updated_book: Book) -> bool:
        ...

    def delete_book(self, book_id: str) -> bool:
        ...
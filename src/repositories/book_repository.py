import json
from src.domain.book import Book
from src.repositories.book_repository_protocol import BookRepositoryProtocol

class BookRepository(BookRepositoryProtocol):
    def __init__(self, filepath: str="books.json"):
        self.filepath = filepath

    def get_all_books(self) -> list[Book]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Book.from_dict(item) for item in data]

    def add_book(self, book:Book) -> str:
        books = self.get_all_books()
        books.append(book)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([b.to_dict() for b in books], f, indent=2)
        return book.book_id

    def find_book_by_name(self, query) -> Book:
        return [b for b in self.get_all_books() if b.title == query]
    
    def update_book(self, updated_book: Book) -> bool:
        books = self.get_all_books()
        for i, book in enumerate(books):
            if book.book_id == updated_book.book_id:
                books[i] = updated_book
                with open(self.filepath, "w", encoding="utf-8") as f:
                    json.dump([b.to_dict() for b in books], f, indent=2)
                return True
        return False

    def delete_book(self, book_id: str) -> bool:
        books = self.get_all_books()
        new_books = [b for b in books if b.book_id != book_id]
        if len(new_books) == len(books):
            return False
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in new_books], f, indent=2)
        return True

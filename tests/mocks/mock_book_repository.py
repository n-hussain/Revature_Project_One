from src.domain.book import Book

class MockBookRepo:
    def get_all_books(self):
        return [Book(title="test", author="author")]
    
    def add_book(self, book):
        return 'mock_id'
    
    def find_book_by_name(self, query):
        return [Book(title="test", author="author")]

    def update_book(self, book):
        return True

    def delete_book(self, book):
        return True
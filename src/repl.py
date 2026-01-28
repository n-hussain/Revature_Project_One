from src.services import generate_books
from src.services.book_generator_bad_data_service import generate_books as get_bad_books
from src.domain.book import Book
from src.services.book_service import BookService
from src.repositories.book_repository import BookRepository
import requests


class BookREPL:
    def __init__(self, book_svc: BookService):
        self.running = True
        self.book_svc = book_svc

    def start(self):
        print("Welcome to the book app! Type 'help' for a list of commands!")
        while self.running:
            cmd = input(">>> ").strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == "exit":
            self.running = False
            print("Goodbye!")

        elif cmd == "getAllRecords":
            self.get_all_records()

        elif cmd == "addBook":
            self.add_book()

        elif cmd == "findByName":
            self.find_book_by_name()

        elif cmd == "updateBook":
            self.update_book()

        elif cmd == "deleteBook":
            self.delete_book()

        elif cmd == "getJoke":
            self.get_joke()

        elif cmd == "help":
            print(
                "Available commands:\n"
                " addBook\n"
                " getAllRecords\n"
                " findByName\n"
                " updateBook\n"
                " deleteBook\n"
                " getJoke\n"
                " help\n"
                " exit"
            )
        else:
            print('Please use a valid command!')

    def get_average_price(self):
        books = self.book_svc.get_all_books()
        avg_price = self.book_analytics_svc.average_price(books)
        print(avg_price)

    def get_top_books(self):
        books = self.book_svc.get_all_books()
        top_rated_books = self.book_analytics_svc.top_rated_with_pandas(books)
        print(top_rated_books)

    def get_value_scores(self):
        books = self.book_svc.get_all_books()
        value_scores = self.book_analytics_svc.value_scores_with_pandas(books)
        print(value_scores)

    def get_joke(self):
        try:
            url = "https://api.chucknorris.io/jokes/random"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(response.json()["value"])
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Something else went wrong: {e}")

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        for book in books:
            print(book)

    def find_book_by_name(self):
        title = input("Please enter book name: ").strip()
        books = self.book_svc.find_book_by_name(title)

        if not books:
            print("No books found.")
            return

        for book in books:
            print(book)

    def add_book(self):
        try:
            print("Enter Book Details:")
            title = input("Title: ").strip()
            author = input("Author: ").strip()

            book = Book(title=title, author=author)
            new_book_id = self.book_svc.add_book(book)

            print(f"Book added with id: {new_book_id}")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")

    def delete_book(self):
        title = input("Enter book title to delete: ").strip()
        matches = self.book_svc.find_book_by_name(title)

        if not matches:
            print("No books found with that title.")
            return

        if len(matches) > 1:
            print("Multiple books found:")
            for i, book in enumerate(matches, start=1):
                print(f"{i}) {book.title} by {book.author}")
            choice = input("Select which book to delete: ").strip()

            if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
                print("Invalid selection.")
                return

            book_to_delete = matches[int(choice) - 1]
        else:
            book_to_delete = matches[0]

        success = self.book_svc.delete_book(book_to_delete.book_id)
        if success:
            print("Book deleted successfully.")
        else:
            print("Delete failed.")

    def update_book(self):
        title = input("Enter book title to update: ").strip()
        matches = self.book_svc.find_book_by_name(title)

        if not matches:
            print("No books found with that title.")
            return

        if len(matches) > 1:
            print("Multiple books found:")
            for i, book in enumerate(matches, start=1):
                print(f"{i}) {book.title} by {book.author}")
            choice = input("Select number to update: ").strip()

            if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
                print("Invalid selection.")
                return

            book = matches[int(choice) - 1]
        else:
            book = matches[0]

        print("Leave blank to keep existing value.")
        new_title = input(f"New title [{book.title}]: ").strip()
        new_author = input(f"New author [{book.author}]: ").strip()

        updated_book = Book(
            title=new_title or book.title,
            author=new_author or book.author,
            book_id=book.book_id
        )

        success = self.book_svc.update_book(updated_book)

        if success:
            print("Book updated successfully.")
        else:
            print("Update failed.")


if __name__ == "__main__":
    generate_books()
    get_bad_books()
    repo = BookRepository('books.json')
    book_service = BookService(repo)
    repl = BookREPL(book_service)
    repl.start()

from datetime import datetime
from src.domain.book import Book
from src.services.book_service import BookService
from src.services.book_analytics_service import BookAnalyticsService
from src.services.checkout_service import CheckoutService
from src.repositories.book_repository import BookRepository
from src.repositories.checkout_history_repository import CheckoutHistoryRepository
import requests




class BookREPL:
    def __init__(
        self,
        book_svc: BookService,
        checkout_svc: CheckoutService,
        book_analytics_svc: BookAnalyticsService = None,
    ):
        self.running = True
        self.book_svc = book_svc
        self.checkout_svc = checkout_svc
        self.book_analytics_svc = book_analytics_svc

    def start(self):
        print("Welcome to the book app! Type 'help' for a list of commands.")
        while self.running:
            cmd = input(">>> ").strip()
            self.handle_command(cmd)

    def handle_command(self, cmd):
        if cmd == "exit":
            self.running = False
            print("Goodbye!")

        elif cmd in ("getAllRecords", "ls"):
            self.get_all_records()
        elif cmd in ("findByName", "find"):
            self.find_book_by_name()
        elif cmd == "addBook":
            self.add_book()
        elif cmd == "updateBook":
            self.update_book()
        elif cmd == "deleteBook":
            self.delete_book()

        elif cmd == "checkOut":
            self.check_out_book()
        elif cmd == "checkIn":
            self.check_in_book()
        elif cmd == "viewHistory":
            self.view_history()
        elif cmd in ("viewAllHistory", "vah"):
            self.view_all_history()

        elif cmd == "getJoke":
            self.get_joke()
        elif cmd == "getAveragePrice":
            self.get_average_price()
        elif cmd == "getTopBooks":
            self.get_top_books()
        elif cmd == "getValueScores":
            self.get_value_scores()

        elif cmd == "help":
            self.print_help()
        else:
            print("Invalid command. Type 'help' to see available commands.")

    def print_help(self):
        print("""
Commands:

Books:
  addBook
  getAllRecords (ls)
  findByName (find)
  updateBook
  deleteBook

Checkout:
  checkOut
  checkIn
  viewHistory
  viewAllHistory (vah)

Analytics:
  getAveragePrice
  getTopBooks
  getValueScores

Other:
  getJoke
  help
  exit
""")

    def select_book_by_title(self, action_name):
        title = input(f"Enter book title to {action_name}: ").strip()
        matches = self.book_svc.find_book_by_name(title)

        if not matches:
            print("No books found.")
            return None

        if len(matches) == 1:
            return matches[0]

        print("\nMultiple books found:")
        for i, book in enumerate(matches, start=1):
            print(f"[{i}] {book.title} | {book.author} | ID: {book.book_id}")

        choice = input("Select number: ").strip()
        if not choice.isdigit():
            print("Invalid selection.")
            return None

        idx = int(choice) - 1
        if idx < 0 or idx >= len(matches):
            print("Invalid selection.")
            return None

        return matches[idx]

    def get_all_records(self):
        books = self.book_svc.get_all_books()
        if not books:
            print("No books found.")
            return

        print("\n--- Books ---")
        for book in books:
            print(book)

    def find_book_by_name(self):
        title = input("Enter book name: ").strip()
        books = self.book_svc.find_book_by_name(title)

        if not books:
            print("No books found.")
            return

        print("\n--- Matches ---")
        for book in books:
            print(book)

    def add_book(self):
        try:
            print("Enter Book Details")
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            page_count = input("Page Count: ").strip()
            publisher = input("Publisher: ").strip()
            price_usd = input("Price USD: ").strip()
            in_print = input("In Print (True/False): ").strip()

            book = Book(
                title=title,
                author=author,
                genre=genre,
                page_count=int(page_count) if page_count else None,
                publisher=publisher,
                price_usd=float(price_usd) if price_usd else None,
                in_print=(in_print.lower() == "true") if in_print else None
            )
            new_book_id = self.book_svc.add_book(book)

            print(f"Book added with ID: {new_book_id}")
        except Exception as e:
            print(f"Error: {e}")

    def delete_book(self):
        book = self.select_book_by_title("delete")
        if not book:
            return

        success = self.book_svc.delete_book(book.book_id)
        print("Book deleted successfully." if success else "Delete failed.")

    def update_book(self):
        book = self.select_book_by_title("update")
        if not book:
            return

        print("Leave blank to keep existing value.")
        new_title = input(f"New title [{book.title}]: ").strip()
        new_author = input(f"New author [{book.author}]: ").strip()
        new_genre = input(f"New genre [{book.genre}]: ").strip()
        average_rating = input(f"New average rating [{book.average_rating}]: ").strip()
        price_usd = input(f"New price USD [{book.price_usd}]: ").strip()
        publisher = input(f"New publisher [{book.publisher}]: ").strip()
        in_print = input(f"Is in print (True/False) [{book.in_print}]: ").strip()




        updated_book = Book(
            title=new_title or book.title,
            author=new_author or book.author,
            book_id=book.book_id,
            genre=new_genre or book.genre,
            average_rating=float(average_rating) if average_rating else book.average_rating,
            price_usd=float(price_usd) if price_usd else book.price_usd,
            publisher=publisher or book.publisher,
            in_print=(in_print.lower() == "true") if in_print else book.in_print,
        )

        success = self.book_svc.update_book(updated_book)
        print("Book updated successfully." if success else "Update failed.")

    def check_out_book(self):
        book = self.select_book_by_title("check out")
        if not book:
            return

        try:
            self.checkout_svc.check_out(book.book_id)
            print(f"Book '{book.title}' checked out.")
        except Exception as e:
            print(f"Check-out failed: {e}")

    def check_in_book(self):
        book = self.select_book_by_title("check in")
        if not book:
            return

        try:
            self.checkout_svc.check_in(book.book_id)
            print(f"Book '{book.title}' checked in.")
        except Exception as e:
            print(f"Check-in failed: {e}")

    def view_history(self):
        book = self.select_book_by_title("view history for")
        if not book:
            return

        events = self.checkout_svc.get_history_for_book(book.book_id)
        if not events:
            print("No history found.")
            return

        print(f"\n--- History for '{book.title}' ---")
        for e in events:
            status = "Returned" if e.returned else "Checked out"
            date = e.return_date if e.returned else e.checkout_date
            print(f"{status} at {date}")

    def view_all_history(self):
        events = self.checkout_svc.get_history_all()
        if not events:
            print("No checkout history found.")
            return

        print("\n--- All Checkout History ---")
        for e in events:
            status = "Returned" if e.returned else "Checked out"
            date = e.return_date if e.returned else e.checkout_date
            print(f"Book ID {e.book_id}: {status} at {date}")

    def get_average_price(self):
        if self.book_analytics_svc:
            books = self.book_svc.get_all_books()
            print("$" + str(self.book_analytics_svc.average_price(books)))

    def get_top_books(self):
        if self.book_analytics_svc:
            books = self.book_svc.get_all_books()
            for b in self.book_analytics_svc.top_rated(books):
                print(b)

    def get_value_scores(self):
        if self.book_analytics_svc:
            books = self.book_svc.get_all_books()
            print(self.book_analytics_svc.value_scores(books))

    def get_joke(self):
        try:
            response = requests.get(
                "https://api.chucknorris.io/jokes/random", timeout=5
            )
            response.raise_for_status()
            print(response.json()["value"])
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")


if __name__ == "__main__":
    book_repo = BookRepository("books.json")
    checkout_repo = CheckoutHistoryRepository("checkout_history.json")

    book_service = BookService(book_repo)
    checkout_service = CheckoutService(book_repo, checkout_repo)
    book_analytics_service = BookAnalyticsService()

    repl = BookREPL(book_service, checkout_service, book_analytics_service)
    repl.start()

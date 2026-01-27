import numpy as np
from src.domain.book import Book

# Ground rules for numpy:
# 1. keep numpy in the service layer ONLY
#   - if you see numpy imports anywhere else, this is a design smell!
# 2. notice how methods take in books, and return normal datatypes NOT ndarrays
#   - this service and numpy are ISOLATED, this will keep our functions PURE and tests CLEAN

class BookAnalyticsService:

    def average_price(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books], dtype=float)
        return float(prices.mean())

    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10):
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])
        
        # what we have now:
        # books -> books objects
        # ratings -> numbers for ALL books
        # counts -> numbers for ALL books
        # filtered books contains all books that have at least 1000 ratings
        mask = counts >= min_ratings
        filteredBooks = np.array(books)[mask]
        # now scores is only the ratings for the filtered books. i.e. over 1000 ratings
        scores = ratings[mask]
        sorted_idx = np.argsort(scores)[::-1]
        return filteredBooks[sorted_idx].tolist()[:limit]

    # value score = rating * log(ratings_count) / price
    def value_scores(self, books: list[Book]) -> dict[str, float]:
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])
        prices = np.array([b.price_usd for b in books])

        scores = (ratings * np.log1p(counts)) / prices

        return {
            # zip() iterates both lists in parallel
            # pairing each book with its corresponding score
            # zip() will stop automatically if one list is shorter
            # - if the same key appears more than once, later entries overwrite earlier ones
            book.book_id: float(score)
            for book, score in zip(books, scores)
        }
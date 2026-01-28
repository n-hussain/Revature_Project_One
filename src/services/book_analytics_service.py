import numpy as np
from src.domain.book import Book
import datetime

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
        
        mask = counts >= min_ratings
        filteredBooks = np.array(books)[mask]
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
            book.book_id: float(score)
            for book, score in zip(books, scores)
        }

    def median_price_by_genre(self, books: list[Book]) -> dict[str, float]:
        genres = np.array([b.genre for b in books])
        prices = np.array([b.price_usd for b in books], dtype=float)
        result = {}

        for genre in np.unique(genres):
            mask = (genres == genre) & ~np.isnan(prices)
            genre_prices = prices[mask]
            median_price = float(np.median(genre_prices))
            result[genre] = median_price

        return result

    def median_genre_current_year(self, books: list[Book]) -> str
        current_year = 2026
        genres = np.array([b.genre for b in books if datetime.fromisoformat(b.last_checkout).year == current_year])
        return genres.mode()[0]
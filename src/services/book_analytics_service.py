import numpy as np
import pandas as pd
from src.domain.book import Book
import datetime

# Ground rules for numpy (applies to pandas too):
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
    
    def top_rated_with_pandas(self, books: list, min_ratings: int = 1000, limit: int = 10) -> list:
        df = pd.DataFrame([{
            'book': b,
            'avg': b.average_rating,
            'count': b.ratings_count
        } for b in books])
        filtered = df[df['count'] >= min_ratings].sort_values('avg', ascending=False)
        return filtered['book'].tolist()[:limit]

    def value_scores_with_pandas(self, books: list, limit: int = 10) -> dict[str, float]:
        df = pd.DataFrame([{
            'book_id': b.book_id,
            'avg': b.average_rating,
            'count': b.ratings_count,
            'price': b.price_usd
        } for b in books])
        df['score'] = df['avg'] * np.log1p(df['count']) / df['price']
        # set_index() sets book_id as the index
        # we do this because we want to end up with a dict[str, float]
        # where book_id is the key and the value score is the float
        # sometimes numpy works with float64, but we need to return float,
        # hence the defensive use of .astype()
        return (
            df
            .sort_values('score', ascending=False)
            .head(limit)
            .set_index('book_id')['score']
            .astype(float).to_dict()
        ) 


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
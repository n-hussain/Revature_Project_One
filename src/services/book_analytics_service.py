import numpy as np
import pandas as pd
from src.domain.book import Book
import datetime

# Ground rules for numpy (applies to pandas too):
# 1. keep numpy in the service layer ONLY
# 2. methods take in books and return normal datatypes (not ndarrays)

class BookAnalyticsService:

    def average_price(self, books: list[Book]) -> float:
        prices = np.array([b.price_usd for b in books if b.price_usd is not None], dtype=float)
        return float(prices.mean().round(2))

    def top_rated(self, books: list[Book], min_ratings: int = 1000, limit: int = 10):
        ratings = np.array([b.average_rating for b in books])
        counts = np.array([b.ratings_count for b in books])
        
        mask = counts >= min_ratings
        filtered_books = np.array(books)[mask]
        scores = ratings[mask]
        sorted_idx = np.argsort(scores)[::-1]
        return filtered_books[sorted_idx].tolist()[:limit]

    def value_scores(self, books: list[Book]) -> dict[str, float]:
        valid_books = [b for b in books if b.average_rating is not None and b.price_usd is not None]
        if not valid_books:
            return {}

        ratings = np.array([b.average_rating for b in valid_books], dtype=float)
        counts = np.array([b.ratings_count for b in valid_books], dtype=float)
        prices = np.array([b.price_usd for b in valid_books], dtype=float)
        scores = (ratings * np.log1p(counts)) / prices

        return {book.book_id: float(score) for book, score in zip(valid_books, scores)}


    def top_rated_with_pandas(self, books: list, min_ratings: int = 1000, limit: int = 10) -> list:
        df = pd.DataFrame([{
            "book": b,
            "avg": b.average_rating,
            "count": b.ratings_count
        } for b in books])

        filtered = df[df["count"] >= min_ratings].sort_values("avg", ascending=False)
        return filtered["book"].tolist()[:limit]

    def value_scores_with_pandas(self, books: list, limit: int = 10) -> dict[str, float]:
        df = pd.DataFrame([{
            "book_id": b.book_id,
            "avg": b.average_rating,
            "count": b.ratings_count,
            "price": b.price_usd
        } for b in books])

        df["score"] = df["avg"] * np.log1p(df["count"]) / df["price"]

        return (
            df.sort_values("score", ascending=False)
              .head(limit)
              .set_index("book_id")["score"]
              .astype(float)
              .to_dict()
        )

    def median_price_by_genre(self, books: list[Book]) -> dict[str, float]:
        genres = np.array([b.genre for b in books])
        prices = np.array([b.price_usd for b in books], dtype=float)
        result = {}

        for genre in np.unique(genres):
            mask = (genres == genre) & ~np.isnan(prices)
            genre_prices = prices[mask]
            result[str(genre)] = float(np.median(genre_prices))

        return result

    def median_genre_current_year(self, books: list[Book]) -> str:
        current_year = 2026
        genres = [
            b.genre
            for b in books
            if b.last_checkout
            and datetime.datetime.fromisoformat(b.last_checkout).year == current_year
        ]

        if not genres:
            return ""

        values, counts = np.unique(genres, return_counts=True)
        return values[np.argmax(counts)]

    def genre_counts(self, books: list[Book]) -> dict[str, int]:
        genres = np.array([b.genre for b in books])
        genres = genres[genres != None]

        values, counts = np.unique(genres, return_counts=True)

        return {
            str(genre): int(count)
            for genre, count in zip(values, counts)
        }


    def mean_rating_by_genre(self, books: list[Book]) -> dict[str, float]:
        genres = np.array([b.genre for b in books])
        ratings = np.array([b.average_rating for b in books], dtype=float)

        valid = (genres != None) & ~np.isnan(ratings)
        genres = genres[valid]
        ratings = ratings[valid]

        result = {}

        for genre in np.unique(genres):
            mask = genres == genre
            result[str(genre)] = float(np.mean(ratings[mask]))

        return result

    def median_ratings_count_by_genre(self, books: list[Book]) -> dict[str, float]:
        genres = np.array([b.genre for b in books])
        counts = np.array([b.ratings_count for b in books], dtype=float)

        valid = (genres != None) & ~np.isnan(counts)
        genres = genres[valid]
        counts = counts[valid]

        result = {}

        for genre in np.unique(genres):
            mask = genres == genre
            result[str(genre)] = float(np.median(counts[mask]))

        return result

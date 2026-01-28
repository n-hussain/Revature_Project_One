import json
import random
import uuid
from datetime import datetime, timedelta

genres = ["History", "Science Fiction", "Fantasy", "Technology", "Biography", "Mystery", "Romance"]
languages = ["English", "english", "Eng", "French", "Spanish", "German"]
formats = ["Paperback", "Hardcover", "Audiobook", "Ebook", "Audio Book"]
publishers = ["North Star Press", "Galactic Books", "Old Tree Publishing", "Sunshine Media", ""]

def random_date():
    base = datetime.today()
    delta = timedelta(days=random.randint(-365*5, 0))
    return (base + delta).isoformat()

def generate_books():
    records = []

    for i in range(500):
        record = {
            "book_id": str(uuid.uuid4()),
            "title": f"Book Title {random.randint(1, 20)}",
            "author": f"Author {random.randint(1, 30)}",
            "genre": random.choice(genres),
            "publication_year": random.choice([random.randint(1750, 2030), "Unknown", None]),
            "page_count": random.choice([random.randint(50, 1000), -5, "N/A", None]),
            "average_rating": random.choice([round(random.uniform(0, 6), 2), "N/A", None]),
            "ratings_count": random.choice([random.randint(0, 5000), "Unknown", None]),
            "price_usd": random.choice([round(random.uniform(-10, 200), 2), "N/A", None]),
            "publisher": random.choice(publishers),
            "language": random.choice(languages),
            "format": random.choice(formats),
            "in_print": random.choice([True, False, "true", "false", None]),
            "sales_millions": random.choice([round(random.uniform(-5, 20), 2), "Unknown", None]),
            "last_checkout": random.choice([random_date(), "", "N/A", None]),
            "available": random.choice([True, False, "true", "false", None])
        }
        records.append(record)

    with open("books_dirty.json", "w") as f:
        json.dump(records, f, indent=2)

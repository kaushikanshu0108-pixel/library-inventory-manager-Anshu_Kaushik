# library_manager/inventory.py
import json
from pathlib import Path
from typing import List, Optional
from .book import Book
import logging

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, json_path: Path):
        self.json_path = Path(json_path)
        self.books: List[Book] = []
        self.load()

    def load(self):
        try:
            if not self.json_path.exists():
                logger.info("books JSON not found, creating new file.")
                self.save()  # create empty file
            else:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.books = [Book(**b) for b in data]
            logger.info("Loaded %d books.", len(self.books))
        except (json.JSONDecodeError, OSError) as e:
            logger.error("Failed to load books JSON: %s", e)
            # handle corrupted file: back up and start fresh
            try:
                backup = self.json_path.with_suffix(".bak.json")
                self.json_path.rename(backup)
                logger.info("Backed up corrupted file to %s", backup)
            except Exception:
                pass
            self.books = []
            self.save()

    def save(self):
        try:
            self.json_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=2)
            logger.info("Saved %d books.", len(self.books))
        except OSError as e:
            logger.error("Failed to save books JSON: %s", e)
            raise

    def add_book(self, title: str, author: str, isbn: str) -> Book:
        if self.search_by_isbn(isbn):
            raise ValueError("A book with this ISBN already exists.")
        book = Book(title=title, author=author, isbn=isbn)
        self.books.append(book)
        self.save()
        logger.info("Added book: %s", isbn)
        return book

    def search_by_title(self, title: str) -> List[Book]:
        title_lower = title.lower()
        return [b for b in self.books if title_lower in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found")
        result = book.issue()
        self.save()
        return result

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found")
        result = book.return_book()
        self.save()
        return result
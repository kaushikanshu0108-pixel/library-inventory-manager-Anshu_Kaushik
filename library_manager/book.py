# library_manager/book.py
from dataclasses import dataclass, asdict

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # "available" or "issued"

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return asdict(self)

    def is_available(self) -> bool:
        return self.status == "available"

    def issue(self) -> bool:
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self) -> bool:
        if not self.is_available():
            self.status = "available"
            return True
        return False
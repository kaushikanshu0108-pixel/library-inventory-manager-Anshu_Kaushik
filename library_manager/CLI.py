# cli/main.py
import logging
from pathlib import Path
from library_manager.inventory import LibraryInventory

LOG_PATH = Path("logs/app.log")
LOG_PATH.parent.mkdir(exist_ok=True, parents=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format="%(asctime)s %(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("library_cli")

def main():
    inv = LibraryInventory(Path("data/books.json"))

    MENU = """
Library Inventory Manager
1. Add Book
2. Issue Book
3. Return Book
4. View All Books
5. Search by Title
6. Search by ISBN
7. Exit
Choose an option: """
    while True:
        try:
            choice = input(MENU).strip()
            if choice == "1":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                isbn = input("ISBN: ").strip()
                inv.add_book(title, author, isbn)
                print("Book added.")
            elif choice == "2":
                isbn = input("ISBN to issue: ").strip()
                success = inv.issue_book(isbn)
                print("Issued." if success else "Book already issued.")
            elif choice == "3":
                isbn = input("ISBN to return: ").strip()
                success = inv.return_book(isbn)
                print("Returned." if success else "Book was not issued.")
            elif choice == "4":
                for line in inv.display_all():
                    print(line)
            elif choice == "5":
                title = input("Search title (partial allowed): ").strip()
                results = inv.search_by_title(title)
                for b in results:
                    print(b)
                if not results:
                    print("No results.")
            elif choice == "6":
                isbn = input("ISBN: ").strip()
                book = inv.search_by_isbn(isbn)
                print(book or "Not found.")
            elif choice == "7":
                print("Exiting.")
                break
            else:
                print("Invalid choice. Enter 1-7.")
        except Exception as e:
            logger.exception("Error in CLI: %s", e)
            print("Error:", e)

if __name__ == "__main__":
    main()
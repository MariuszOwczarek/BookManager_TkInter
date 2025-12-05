from book import Book
from database_manager import DatabaseManager


def test_book_creation():
    book = Book('Dune Messiah', 'Frank Herbert', 1969, 'Fantasy')
    assert book.id is None
    assert book.title == 'Dune Messiah'
    assert book.author == 'Frank Herbert'
    assert book.year == 1969
    assert book.genre == 'Fantasy'
    assert str(book) == "Book: None, Title: Dune Messiah, Author: Frank Herbert, Year: 1969, Genre: Fantasy"
    assert repr(book) == "Book(None, 'Dune Messiah', 'Frank Herbert', 1969, 'Fantasy')"


def test_table_creation():
    db = DatabaseManager('db_table_creation.db')
    db.create_table()
    db.cur.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='books'")

    table_exists = db.cur.fetchone()
    assert table_exists is not None
    db.close()


def test_add_book_to_table_and_get_book_from_table():
    db = DatabaseManager('db_add_and_get_book.db')
    db.create_table()
    book = Book('Chapterhouse: Dune', 'Frank Herbert', 1985, 'Fantasy')
    db.add_book(book=book)
    assert book.id is not None
    books = db.get_all_books()
    assert any(b.id == book.id for b in books)
    db.close()


def test_update_book():
    db = DatabaseManager('db_update_book.db')
    db.create_table()
    book = Book('Dune', 'Frank Herbert', 1965, 'Fantasy')
    db.add_book(book=book)
    books = db.get_all_books()
    book_to_update = books[0]
    book_to_update.title = "God Emperror of Dune"
    book_to_update.year = 1981
    db.update_book(book=book_to_update)
    updated_books = db.get_all_books()
    updated_book = next(b for b in updated_books if b.id == book_to_update.id)
    assert updated_book.title == "God Emperror of Dune"
    assert updated_book.year == 1981
    db.close()


def test_delete_book():
    db = DatabaseManager('db_delete_book.db')
    db.create_table()
    book = Book('Dune', 'Frank Herbert', 1965, 'Fantasy')
    db.add_book(book=book)
    db.delete_book(book.id)
    books = db.get_all_books()
    assert all(b.id != book.id for b in books)
    db.close()

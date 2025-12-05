import sqlite3
from book import Book


class DatabaseManager:
    def __init__(self, db="books.db"):
        self.db = db
        self.con = sqlite3.connect(f'{self.db}')
        self.cur = self.con.cursor()

    def create_table(self):
        sqlquery = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year INTEGER,
            genre TEXT
        )
        """
        self.cur.execute(sqlquery)
        self.con.commit()

    def add_book(self, book: Book):
        sqlquery = """
        INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)
        """
        self.cur.execute(sqlquery, (book.title,
                                    book.author,
                                    book.year,
                                    book.genre))
        self.con.commit()
        book.id = self.cur.lastrowid

    def get_all_books(self) -> list[Book]:
        sqlquery = "SELECT * FROM books"
        self.cur.execute(sqlquery)
        rows = self.cur.fetchall()
        books = [Book(title=row[1],
                      author=row[2],
                      year=row[3],
                      genre=row[4]) for row in rows]
        for book, row in zip(books, rows):
            book.id = row[0]
        return books

    def update_book(self, book: Book):
        sqlquery = "UPDATE books SET title=?, author=?, year=?, genre=? WHERE id=?"
        self.cur.execute(sqlquery, (book.title,
                                    book.author,
                                    book.year,
                                    book.genre,
                                    book.id))
        self.con.commit()

    def delete_book(self, book_id: int):
        sqlquery = "DELETE FROM books WHERE id=?"
        self.cur.execute(sqlquery, (book_id,))
        self.con.commit()

    def close(self):
        self.con.close()

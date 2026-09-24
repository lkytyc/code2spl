class BookManagementDB:
    def __init__(self, db_filename):
        import sqlite3
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                available INTEGER
            )
            """
        )
        self.conn.commit()

    def add_book(self, title, author):
        self.cursor.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, ?)",
            (title, author, 1),
        )
        self.conn.commit()

    def remove_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()

    def borrow_book(self, book_id):
        self.cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
        self.conn.commit()

    def return_book(self, book_id):
        self.cursor.execute("UPDATE books SET available = 1 WHERE id = ?", (book_id,))
        self.conn.commit()

    def search_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

import unittest
import os

class BookManagementDBTestBorrowBook(unittest.TestCase):
    def setUp(self):
        self.db_name = "test.db"
        self.db = BookManagementDB(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        # Add a book for testing borrowing
        self.db.add_book("Book to Borrow", "Jane Smith")

    def test_borrow_book(self):
        self.db.borrow_book(1)

        # Check if the book was marked as unavailable
        self.cursor.execute("SELECT available FROM books WHERE id=1")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 0)

    def tearDown(self):
        self.db.connection.close()
        self.connection.close()
        # remove the test database file
        os.remove(self.db_name)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

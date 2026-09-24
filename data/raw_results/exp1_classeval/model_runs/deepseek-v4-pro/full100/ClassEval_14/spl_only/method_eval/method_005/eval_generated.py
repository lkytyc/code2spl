import sqlite3


class BookManagementDB:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, available INTEGER)"
        )
        self.connection.commit()

    def add_book(self, title, author):
        self.cursor.execute(
            "INSERT INTO books (title, author, available) VALUES (?, ?, ?)",
            (title, author, 1),
        )
        self.connection.commit()

    def remove_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.connection.commit()

    def borrow_book(self, book_id):
        self.cursor.execute(
            "UPDATE books SET available = 0 WHERE id = ?", (book_id,)
        )
        self.connection.commit()

    def return_book(self, book_id):
        self.cursor.execute(
            "UPDATE books SET available = 1 WHERE id = ?", (book_id,)
        )
        self.connection.commit()

    def search_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        return books

import unittest
import os

class BookManagementDBTestSearchBooks(unittest.TestCase):
    def setUp(self):
        self.db_name = "test.db"
        self.db = BookManagementDB(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        # Add some books for testing search
        self.db.add_book("Book 1", "Author 1")
        self.db.add_book("Book 2", "Author 2")
        self.db.add_book("Book 3", "Author 3")

    def test_search_books(self):
        books = self.db.search_books()

        # Ensure that all books were retrieved
        self.assertEqual(len(books), 3)

        # Ensure that the correct book information is retrieved
        self.assertEqual(books[0][1], "Book 1")
        self.assertEqual(books[1][2], "Author 2")
        self.assertEqual(books[2][3], 1)

    def tearDown(self):
        self.db.connection.close()
        self.connection.close()
        # remove the test database file
        os.remove(self.db_name)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

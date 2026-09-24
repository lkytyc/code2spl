import sqlite3


class BookManagementDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author):
        self.cursor.execute(
            'INSERT INTO books (title, author, available) VALUES (?, ?, 1)',
            (title, author)
        )
        self.conn.commit()

    def remove_book(self, book_id):
        self.cursor.execute(
            'DELETE FROM books WHERE id = ?',
            (book_id,)
        )
        self.conn.commit()

    def borrow_book(self, book_id):
        self.cursor.execute(
            'UPDATE books SET available = 0 WHERE id = ?',
            (book_id,)
        )
        self.conn.commit()

    def return_book(self, book_id):
        self.cursor.execute(
            'UPDATE books SET available = 1 WHERE id = ?',
            (book_id,)
        )
        self.conn.commit()

    def search_books(self):
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()

import unittest
import os

class BookManagementDBTestCreateTable(unittest.TestCase):
    def setUp(self):
        self.db_name = "test.db"
        self.db = BookManagementDB(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def test_create_table_1(self):
        # Check if the table exists
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_create_table_2(self):
        self.db.create_table()
        # Check if the table has the correct columns
        self.cursor.execute("PRAGMA table_info(books)")
        columns = self.cursor.fetchall()
        column_names = [column[1] for column in columns]
        expected_column_names = ['id', 'title', 'author', 'available']
        self.assertEqual(column_names, expected_column_names)

    def tearDown(self):
        self.db.connection.close()
        self.connection.close()
        # remove the test database file
        os.remove(self.db_name)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

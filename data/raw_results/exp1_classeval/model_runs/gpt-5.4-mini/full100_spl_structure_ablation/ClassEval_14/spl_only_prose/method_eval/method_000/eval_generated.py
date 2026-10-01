import sqlite3


class BookManagementDB:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def add_book(self, title: str, author: str):
        insert_statement = "INSERT INTO books (title, author, available) VALUES (?, ?, 1)"
        execution_result = self.cursor.execute(insert_statement, (title, author))
        commit_result = self.connection.commit()
        return commit_result

    def borrow_book(self, book_id):
        update_result = self.cursor.execute(
            "UPDATE books SET available = 0 WHERE id = ?",
            (book_id,),
        )
        commit_result = self.connection.commit()
        return commit_result

    def create_table(self):
        table_creation_result = self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, available INTEGER)"
        )
        commit_result = self.connection.commit()
        return commit_result

    def remove_book(self, book_id: int) -> None:
        delete_statement_executed = self.cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,),
        )
        transaction_committed = self.connection.commit()
        return None

    def return_book(self, book_id):
        update_result = self.cursor.execute(
            "UPDATE books SET available = 1 WHERE id = ?",
            (book_id,),
        )
        commit_result = self.connection.commit()
        return commit_result

    def search_books(self) -> list:
        query_result = self.cursor.execute("SELECT * FROM books")
        books = query_result.fetchall()
        return books

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

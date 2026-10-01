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

class BookManagementDBTestRemoveBook(unittest.TestCase):
    def setUp(self):
        self.db_name = "test.db"
        self.db = BookManagementDB(self.db_name)
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        # Add a book for testing removal
        self.db.add_book("Book to Remove", "John Doe")

    def test_remove_book(self):
        self.db.remove_book(1)

        # Check if the book was removed correctly
        self.cursor.execute("SELECT * FROM books WHERE id=1")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def tearDown(self):
        self.db.connection.close()
        self.connection.close()
        # remove the test database file
        os.remove(self.db_name)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

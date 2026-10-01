import sqlite3


class UserLoginDB:
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def delete_user_by_username(self, username: str):
        delete_target = username
        self.cursor.execute("DELETE FROM users WHERE username = ?", (delete_target,))
        self.connection.commit()

    def insert_user(self, username, password):
        self.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        self.connection.commit()

    def search_user_by_username(self, username: str):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        return user

    def validate_user_login(self, username: str, password: str) -> bool:
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False

import unittest
import os
from tempfile import gettempdir

class UserLoginDBTestSearchUserByUsername(unittest.TestCase):
    def setUp(self):
        self.db_path = os.path.join(gettempdir(), 'test_db.db')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        create_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT,
                    password TEXT
                )
                """
        cursor.execute(create_table_query)

        conn.commit()
        conn.close()
        self.db = UserLoginDB(self.db_path)

    def tearDown(self):
        self.db.connection.close()
        os.unlink(self.db_path)

    def test_search_user_by_username_1(self):
        self.db.insert_user('user1', 'pass1')
        user = self.db.search_user_by_username('user1')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'user1')
        self.assertEqual(user[1], 'pass1')

    def test_search_user_by_username_2(self):
        self.db.insert_user('user2', 'pass2')
        user = self.db.search_user_by_username('user2')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'user2')
        self.assertEqual(user[1], 'pass2')

    def test_search_user_by_username_3(self):
        self.db.insert_user('user3', 'pass3')
        user = self.db.search_user_by_username('user3')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'user3')
        self.assertEqual(user[1], 'pass3')

    def test_search_user_by_username_4(self):
        self.db.insert_user('user4', 'pass4')
        user = self.db.search_user_by_username('user4')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'user4')
        self.assertEqual(user[1], 'pass4')

    def test_search_user_by_username_5(self):
        self.db.insert_user('user5', 'pass5')
        user = self.db.search_user_by_username('user5')
        self.assertIsNotNone(user)
        self.assertEqual(user[0], 'user5')
        self.assertEqual(user[1], 'pass5')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

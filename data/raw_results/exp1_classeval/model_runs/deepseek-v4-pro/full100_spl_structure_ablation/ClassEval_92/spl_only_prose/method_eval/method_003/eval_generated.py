import sqlite3

class UserLoginDB:
    def __init__(self, db_name):
        self.connection = None
        self.cursor = None
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Failed to initialize SQLite connection for {db_name}.")
            raise

    def delete_user_by_username(self, username):
        delete_result = self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        commit_result = self.connection.commit()
        return delete_result

    def insert_user(self, username, password):
        insert_execution = self.cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        commit_result = self.connection.commit()
        return insert_execution

    def search_user_by_username(self, username):
        cursor_result = self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor_result.fetchone()
        return user

    def validate_user_login(self, username, password):
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False

import unittest
import os
from tempfile import gettempdir

class UserLoginDBTestValidateUserLogin(unittest.TestCase):
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

    def test_validate_user_login_1(self):
        self.db.insert_user('user1', 'pass1')
        valid = self.db.validate_user_login('user1', 'pass1')
        self.assertTrue(valid)

    def test_validate_user_login_2(self):
        self.db.insert_user('user1', 'pass1')
        invalid = self.db.validate_user_login('user1', 'wrongpass')
        self.assertFalse(invalid)

    def test_validate_user_login_3(self):
        valid = self.db.validate_user_login('nonexistentuser', 'somepass')
        self.assertFalse(valid)

    def test_validate_user_login_4(self):
        self.db.insert_user('user2', 'pass2')
        valid = self.db.validate_user_login('user2', 'pass2')
        self.assertTrue(valid)

    def test_validate_user_login_5(self):
        self.db.insert_user('user3', 'pass3')
        valid = self.db.validate_user_login('user3', 'pass3')
        self.assertTrue(valid)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

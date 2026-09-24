import sqlite3
import pandas


class DatabaseProcessor:
    def __init__(self, database_filename):
        self.database_filename = database_filename

    def create_table(self, table_name, text_column_name, integer_column_name):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ("
            f"id INTEGER PRIMARY KEY AUTOINCREMENT, "
            f"{text_column_name} TEXT, "
            f"{integer_column_name} INTEGER"
            f")"
        )
        connection.commit()
        connection.close()

    def insert_into_database(self, table_name, records):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        for record in records:
            cursor.execute(
                f"INSERT INTO {table_name} (name, age) VALUES (?, ?)",
                (record["name"], record["age"])
            )
        connection.commit()
        connection.close()

    def search_database(self, table_name, name):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM {table_name} WHERE name = ?",
            (name,)
        )
        rows = cursor.fetchall()
        connection.close()
        if rows:
            return rows
        return None

    def delete_from_database(self, table_name, name):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        cursor.execute(
            f"DELETE FROM {table_name} WHERE name = ?",
            (name,)
        )
        connection.commit()
        connection.close()

import unittest
import sqlite3

class DatabaseProcessorTestCreateTable(unittest.TestCase):
    def setUp(self):
        self.database_name = "test.db"
        self.processor = DatabaseProcessor(self.database_name)

    def tearDown(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_table")
        conn.commit()
        conn.close()

    def test_create_table_1(self):
        table_name = "test_table"
        self.processor.create_table(table_name, 'name', 'age')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_create_table_2(self):
        table_name = "test_table2"
        self.processor.create_table(table_name, 'name', 'age')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_create_table_3(self):
        table_name = "test_table3"
        self.processor.create_table(table_name, 'name', 'age')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_create_table_4(self):
        table_name = "test_table4"
        self.processor.create_table(table_name, 'name', 'age')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_create_table_5(self):
        table_name = "test_table5"
        self.processor.create_table(table_name, 'name', 'age')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

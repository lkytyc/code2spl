import sqlite3
import pandas as pd


class DatabaseProcessor:
    def __init__(self, database_file_name):
        self.database_file_name = database_file_name

    def create_table(self, table_name, key1, key2):
        conn = sqlite3.connect(self.database_file_name)
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ("
            f"id INTEGER PRIMARY KEY, "
            f"{key1} TEXT, "
            f"{key2} INTEGER)"
        )
        conn.commit()
        conn.close()

    def insert_into_database(self, table_name, data):
        conn = sqlite3.connect(self.database_file_name)
        cursor = conn.cursor()
        for item in data:
            cursor.execute(
                f"INSERT INTO {table_name} (name, age) VALUES (?, ?)",
                (item["name"], item["age"]),
            )
        conn.commit()
        conn.close()

    def search_database(self, table_name, name):
        conn = sqlite3.connect(self.database_file_name)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM {table_name} WHERE name = ?",
            (name,),
        )
        rows = cursor.fetchall()
        conn.close()
        return rows if rows else None

    def delete_from_database(self, table_name, name):
        conn = sqlite3.connect(self.database_file_name)
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM {table_name} WHERE name = ?",
            (name,),
        )
        conn.commit()
        conn.close()

import unittest
import sqlite3

class DatabaseProcessorTestSearchDatabase(unittest.TestCase):
    def setUp(self):
        self.database_name = "test.db"
        self.processor = DatabaseProcessor(self.database_name)

    def tearDown(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_table")
        conn.commit()
        conn.close()

    def test_search_database_1(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        result = self.processor.search_database(table_name, 'John')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'John')

    def test_search_database_2(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        result = self.processor.search_database(table_name, 'Alice')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Alice')

    def test_search_database_3(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        result = self.processor.search_database(table_name, 'Bob')
        self.assertIsNone(result)

    def test_search_database_4(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        result = self.processor.search_database(table_name, 'aaa')
        self.assertIsNone(result)

    def test_search_database_5(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        result = self.processor.search_database(table_name, 'bbb')
        self.assertIsNone(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

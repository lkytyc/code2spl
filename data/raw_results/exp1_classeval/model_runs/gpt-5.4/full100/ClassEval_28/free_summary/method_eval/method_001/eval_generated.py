import sqlite3
import pandas as pd


class DatabaseProcessor:
    def __init__(self, database_filename):
        self.database_filename = database_filename

    def create_table(self, table_name, key1, key2):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
        )
        connection.commit()
        connection.close()

    def insert_into_database(self, table_name, data):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        for record in data:
            cursor.execute(
                f"INSERT INTO {table_name} (name, age) VALUES (?, ?)",
                (record["name"], record["age"]),
            )
        connection.commit()
        connection.close()

    def search_database(self, table_name, name):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM {table_name} WHERE name = ?",
            (name,),
        )
        results = cursor.fetchall()
        connection.close()
        return results if results else None

    def delete_from_database(self, table_name, name):
        connection = sqlite3.connect(self.database_filename)
        cursor = connection.cursor()
        cursor.execute(
            f"DELETE FROM {table_name} WHERE name = ?",
            (name,),
        )
        connection.commit()
        connection.close()

import unittest
import sqlite3

class DatabaseProcessorTestInsertIntoDatabase(unittest.TestCase):
    def setUp(self):
        self.database_name = "test.db"
        self.processor = DatabaseProcessor(self.database_name)

    def tearDown(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_table")
        conn.commit()
        conn.close()

    def test_insert_into_database_1(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), len(data))
        self.assertEqual(result[0][2], 25)

    def test_insert_into_database_2(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 15},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), len(data))
        self.assertEqual(result[0][2], 15)

    def test_insert_into_database_3(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 16},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), len(data))
        self.assertEqual(result[0][2], 16)

    def test_insert_into_database_4(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 17},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), len(data))
        self.assertEqual(result[0][2], 17)

    def test_insert_into_database_5(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 18},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), len(data))
        self.assertEqual(result[0][2], 18)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

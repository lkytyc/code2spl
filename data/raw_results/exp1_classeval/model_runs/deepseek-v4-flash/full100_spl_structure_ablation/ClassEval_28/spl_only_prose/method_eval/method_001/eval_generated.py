import sqlite3

class DatabaseProcessor:
    def __init__(self, database_name: str):
        self.database_name = database_name

    def create_table(self, table_name: str, key1: str, key2: str):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()

    def delete_from_database(self, table_name: str, name: str):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name} WHERE name = ?"
        cursor.execute(delete_query, (name,))
        conn.commit()
        conn.close()

    def insert_into_database(self, table_name: str, data: list[dict]):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        for item in data:
            insert_query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
            cursor.execute(insert_query, (item['name'], item['age']))
        conn.commit()
        conn.close()

    def search_database(self, table_name: str, name: str):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        select_query = f"SELECT * FROM {table_name} WHERE name = ?"
        cursor.execute(select_query, (name,))
        result = cursor.fetchall()
        if result:
            return result
        return None

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

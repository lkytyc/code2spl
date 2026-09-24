import sqlite3

class DatabaseProcessor:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self, table_name, text_column, integer_column):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {text_column} TEXT, {integer_column} INTEGER)")
        conn.commit()
        conn.close()

    def insert_data(self, table_name, data):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        for record in data:
            cursor.execute(f"INSERT INTO {table_name} (name, age) VALUES (?, ?)", (record['name'], record['age']))
        conn.commit()
        conn.close()

    def search_by_name(self, table_name, name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE name = ?", (name,))
        rows = cursor.fetchall()
        conn.close()
        return rows if rows else None

    def delete_by_name(self, table_name, name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE name = ?", (name,))
        conn.commit()
        conn.close()

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

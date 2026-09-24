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

class DatabaseProcessorTestDeteleFromDatabase(unittest.TestCase):
    def setUp(self):
        self.database_name = "test.db"
        self.processor = DatabaseProcessor(self.database_name)

    def tearDown(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS test_table")
        conn.commit()
        conn.close()

    def test_delete_from_database_1(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        self.processor.delete_from_database(table_name, 'John')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Alice')

    def test_delete_from_database_2(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        self.processor.delete_from_database(table_name, 'Alice')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'John')

    def test_delete_from_database_3(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        self.processor.delete_from_database(table_name, 'John')
        self.processor.delete_from_database(table_name, 'Alice')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 0)

    def test_delete_from_database_4(self):
        table_name = "test_table"
        data = [
            {'name': 'John', 'age': 25},
            {'name': 'aaa', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        self.processor.delete_from_database(table_name, 'John')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'aaa')

    def test_delete_from_database_5(self):
        table_name = "test_table"
        data = [
            {'name': 'bbb', 'age': 25},
            {'name': 'Alice', 'age': 30}
        ]
        self.processor.create_table(table_name, 'name', 'age')
        self.processor.insert_into_database(table_name, data)

        self.processor.delete_from_database(table_name, 'bbb')

        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        conn.close()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 'Alice')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

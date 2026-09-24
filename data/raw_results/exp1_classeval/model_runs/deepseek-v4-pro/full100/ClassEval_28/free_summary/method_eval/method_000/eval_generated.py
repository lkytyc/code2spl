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

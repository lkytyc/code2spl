class DatabaseProcessor:
    def __init__(self, database_name):
        self.database_name = database_name

    def create_table(self, table_name, key1, key2):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {key1} TEXT, {key2} INTEGER)"
        execute_result = cursor.execute(create_table_query)
        commit_result = conn.commit()
        close_result = conn.close()

    def delete_from_database(self, table_name, name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        delete_query = f"DELETE FROM {table_name} WHERE name = ?"
        result = cursor.execute(delete_query, (name,))
        result = conn.commit()
        result = conn.close()

    def insert_into_database(self, table_name, data):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        for item in data:
            insert_query = f"INSERT INTO {table_name} (name, age) VALUES (?, ?)"
            execution_result = cursor.execute(insert_query, (item['name'], item['age']))
        commit_status = conn.commit()
        close_status = conn.close()

    def search_database(self, table_name, name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        select_query = f"SELECT * FROM {table_name} WHERE name = ?"
        cursor = cursor.execute(select_query, (name,))
        result = cursor.fetchall()
        if result:
            return result
        return None

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

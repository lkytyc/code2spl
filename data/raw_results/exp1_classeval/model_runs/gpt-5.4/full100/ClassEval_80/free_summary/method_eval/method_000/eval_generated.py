class SQLQueryBuilder:
    @staticmethod
    def select(table, columns='*', where=None):
        if columns == '*':
            query = f"SELECT * FROM {table}"
        else:
            query = f"SELECT {', '.join(columns)} FROM {table}"

        if where:
            conditions = " AND ".join(f"{key} = '{value}'" for key, value in where.items())
            query += f" WHERE {conditions}"

        return query

    @staticmethod
    def insert(table, data):
        columns = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        return f"INSERT INTO {table} ({columns}) VALUES ({values})"

    @staticmethod
    def delete(table, where=None):
        query = f"DELETE FROM {table}"

        if where:
            conditions = " AND ".join(f"{key} = '{value}'" for key, value in where.items())
            query += f" WHERE {conditions}"

        return query

    @staticmethod
    def update(table, data, where=None):
        set_clause = ", ".join(f"{key} = '{value}'" for key, value in data.items())
        query = f"UPDATE {table} SET {set_clause}"

        if where:
            conditions = " AND ".join(f"{key} = '{value}'" for key, value in where.items())
            query += f" WHERE {conditions}"

        return query

import unittest

class SQLQueryBuilderTestSelect(unittest.TestCase):
    def test_select_1(self):
        self.assertEqual(
            SQLQueryBuilder.select('users', ["id", "name"], {'age': 30}),
            "SELECT id, name FROM users WHERE age='30'"
        )

    def test_select_2(self):
        self.assertEqual(
            SQLQueryBuilder.select('students', ["id", "name"], {'age': 18}),
            "SELECT id, name FROM students WHERE age='18'"
        )

    def test_select_3(self):
        self.assertEqual(
            SQLQueryBuilder.select('items', ["id", "name"], {'price': 1.0}),
            "SELECT id, name FROM items WHERE price='1.0'"
        )

    def test_select_4(self):
        self.assertEqual(
            SQLQueryBuilder.select('users', ["id"], {'age': 30}),
            "SELECT id FROM users WHERE age='30'"
        )

    def test_select_5(self):
        self.assertEqual(
            SQLQueryBuilder.select('users', ["name"], {'age': 30}),
            "SELECT name FROM users WHERE age='30'"
        )

    def test_select_6(self):
        self.assertEqual(
            SQLQueryBuilder.select('users', ["name"]),
            "SELECT name FROM users"
        )

    def test_select_7(self):
        self.assertEqual(
            SQLQueryBuilder.select('users', "*"),
            "SELECT * FROM users"
        )

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

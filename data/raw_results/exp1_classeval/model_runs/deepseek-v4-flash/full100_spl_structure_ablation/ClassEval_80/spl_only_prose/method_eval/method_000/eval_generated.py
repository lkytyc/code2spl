class SQLQueryBuilder:
    def delete(self, table: str, where: dict = None) -> str:
        query = f"DELETE FROM {table}"
        if where:
            where_clause = " AND ".join(f"{k}='{v}'" for k, v in where.items())
            query += f" WHERE {where_clause}"
        return query

    def insert(self, table: str, data: dict) -> str:
        keys = ", ".join(data.keys())
        values = ", ".join(f"'{v}'" for v in data.values())
        return f"INSERT INTO {table} ({keys}) VALUES ({values})"

    def select(self, table: str, columns: str or list = "*", where: dict = None) -> str:
        if columns != "*":
            columns = ", ".join(columns)
        query = f"SELECT {columns} FROM {table}"
        if where:
            where_clause = " AND ".join(f"{k}='{v}'" for k, v in where.items())
            query += f" WHERE {where_clause}"
        return query

    def update(self, table: str, data: dict, where: dict = None) -> str:
        update_str = ", ".join(f"{k}='{v}'" for k, v in data.items())
        query = f"UPDATE {table} SET {update_str}"
        if where:
            where_clause = " AND ".join(f"{k}='{v}'" for k, v in where.items())
            query += f" WHERE {where_clause}"
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

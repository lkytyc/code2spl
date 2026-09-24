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

class SQLQueryBuilderTestUpdate(unittest.TestCase):
    def test_update_1(self):
        self.assertEqual(
            SQLQueryBuilder.update('users', {'age': 35}, {'name': 'Tom'}),
            "UPDATE users SET age='35' WHERE name='Tom'"
        )

    def test_update_2(self):
        self.assertEqual(
            SQLQueryBuilder.update('students', {'age': 18}, {'name': 'Tom'}),
            "UPDATE students SET age='18' WHERE name='Tom'"
        )

    def test_update_3(self):
        self.assertEqual(
            SQLQueryBuilder.update('items', {'price': 1.0}, {'name': 'apple'}),
            "UPDATE items SET price='1.0' WHERE name='apple'"
        )

    def test_update_4(self):
        self.assertEqual(
            SQLQueryBuilder.update('items', {'price': 1.0}, {'name': 'aaa'}),
            "UPDATE items SET price='1.0' WHERE name='aaa'"
        )

    def test_update_5(self):
        self.assertEqual(
            SQLQueryBuilder.update('items', {'price': 1.0}, {'name': 'bbb'}),
            "UPDATE items SET price='1.0' WHERE name='bbb'"
        )

    def test_update_6(self):
        self.assertEqual(
            SQLQueryBuilder.update('items', {'price': 1.0}),
            "UPDATE items SET price='1.0'"
        )

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

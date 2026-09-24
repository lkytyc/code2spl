class SQLQueryBuilder:
    def delete(self, table: str, where: dict = None) -> str:
        query = f"DELETE FROM {table}"
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where.items())
        return query

    def insert(self, table: str, data: dict) -> str:
        keys = ", ".join(data.keys())
        quoted_values = [f"'{v}'" for v in data.values()]
        values = ", ".join(quoted_values)
        return f"INSERT INTO {table} ({keys}) VALUES ({values})"

    def select(self, table: str, columns, where: dict = None) -> str:
        if columns != '*':
            columns = ", ".join(columns)
        query = f"SELECT {columns} FROM {table}"
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where.items())
        return query

    def update(self, table: str, data: dict, where: dict = None) -> str:
        update_str = ", ".join(f"{k}='{v}'" for k, v in data.items())
        query = f"UPDATE {table} SET {update_str}"
        if where:
            query += " WHERE " + " AND ".join(f"{k}='{v}'" for k, v in where.items())
        return query

import unittest

class SQLQueryBuilderTestDetele(unittest.TestCase):
    def test_delete_1(self):
        self.assertEqual(
            SQLQueryBuilder.delete('users', {'name': 'Tom'}),
            "DELETE FROM users WHERE name='Tom'"
        )

    def test_delete_2(self):
        self.assertEqual(
            SQLQueryBuilder.delete('students', {'name': 'Tom'}),
            "DELETE FROM students WHERE name='Tom'"
        )

    def test_delete_3(self):
        self.assertEqual(
            SQLQueryBuilder.delete('items', {'name': 'apple'}),
            "DELETE FROM items WHERE name='apple'"
        )

    def test_delete_4(self):
        self.assertEqual(
            SQLQueryBuilder.delete('items', {'name': 'aaa'}),
            "DELETE FROM items WHERE name='aaa'"
        )

    def test_delete_5(self):
        self.assertEqual(
            SQLQueryBuilder.delete('items', {'name': 'bbb'}),
            "DELETE FROM items WHERE name='bbb'"
        )

    def test_delete_6(self):
        self.assertEqual(
            SQLQueryBuilder.delete('items'),
            "DELETE FROM items"
        )

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

class SQLQueryBuilder:
    def delete(self, table, where):
        query = f"DELETE FROM {table}"
        if where:
            conditions = " AND ".join(
                f"{key}='{value}'" for key, value in where.items()
            )
            query += f" WHERE {conditions}"
        return query

    def insert(self, table, data):
        keys = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        return f"INSERT INTO {table} ({keys}) VALUES ({values})"

    def select(self, table, columns, where):
        if columns != "*":
            columns = ", ".join(columns)

        query = f"SELECT {columns} FROM {table}"
        if where:
            conditions = " AND ".join(
                f"{key}='{value}'" for key, value in where.items()
            )
            query += f" WHERE {conditions}"
        return query

    def update(self, table, data, where):
        update_str = ", ".join(
            f"{key}='{value}'" for key, value in data.items()
        )
        query = f"UPDATE {table} SET {update_str}"
        if where:
            conditions = " AND ".join(
                f"{key}='{value}'" for key, value in where.items()
            )
            query += f" WHERE {conditions}"
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

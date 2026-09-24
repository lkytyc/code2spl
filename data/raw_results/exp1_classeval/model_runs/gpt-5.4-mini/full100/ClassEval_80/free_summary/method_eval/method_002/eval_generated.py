class SQLQueryBuilder:
    @staticmethod
    def select(table, columns='*', where=None):
        if columns == '*':
            cols = '*'
        else:
            cols = ', '.join(columns)
        query = f"SELECT {cols} FROM {table}"
        if where:
            conditions = [f"{key}='{value}'" for key, value in where.items()]
            query += " WHERE " + " AND ".join(conditions)
        return query

    @staticmethod
    def insert(table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(f"'{value}'" for value in data.values())
        return f"INSERT INTO {table} ({columns}) VALUES ({values})"

    @staticmethod
    def delete(table, where=None):
        query = f"DELETE FROM {table}"
        if where:
            conditions = [f"{key}='{value}'" for key, value in where.items()]
            query += " WHERE " + " AND ".join(conditions)
        return query

    @staticmethod
    def update(table, data, where=None):
        set_clause = ', '.join(f"{key}='{value}'" for key, value in data.items())
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            conditions = [f"{key}='{value}'" for key, value in where.items()]
            query += " WHERE " + " AND ".join(conditions)
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

class SQLQueryBuilder:
    @staticmethod
    def select(table, columns='*', where=None):
        if columns == '*':
            cols = '*'
        else:
            cols = ', '.join(columns)
        query = f"SELECT {cols} FROM {table}"
        if where:
            query += " WHERE " + " AND ".join(f"{k} = '{v}'" for k, v in where.items())
        return query

    @staticmethod
    def insert(table, data):
        cols = ', '.join(data.keys())
        vals = ', '.join(f"'{v}'" for v in data.values())
        return f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    @staticmethod
    def delete(table, where=None):
        query = f"DELETE FROM {table}"
        if where:
            query += " WHERE " + " AND ".join(f"{k} = '{v}'" for k, v in where.items())
        return query

    @staticmethod
    def update(table, data, where=None):
        set_clause = ", ".join(f"{k} = '{v}'" for k, v in data.items())
        query = f"UPDATE {table} SET {set_clause}"
        if where:
            query += " WHERE " + " AND ".join(f"{k} = '{v}'" for k, v in where.items())
        return query

import unittest

class SQLQueryBuilderTestInsert(unittest.TestCase):
    def test_insert_1(self):
        self.assertEqual(
            SQLQueryBuilder.insert('users', {'name': 'Tom', 'age': 30}),
            "INSERT INTO users (name, age) VALUES ('Tom', '30')"
        )

    def test_insert_2(self):
        self.assertEqual(
            SQLQueryBuilder.insert('students', {'name': 'Tom', 'age': 18}),
            "INSERT INTO students (name, age) VALUES ('Tom', '18')"
        )

    def test_insert_3(self):
        self.assertEqual(
            SQLQueryBuilder.insert('items', {'name': 'apple', 'price': 1.0}),
            "INSERT INTO items (name, price) VALUES ('apple', '1.0')"
        )

    def test_insert_4(self):
        self.assertEqual(
            SQLQueryBuilder.insert('users', {'name': 'Tom'}),
            "INSERT INTO users (name) VALUES ('Tom')"
        )

    def test_insert_5(self):
        self.assertEqual(
            SQLQueryBuilder.insert('users', {'name': 'Tom', 'age': 30, 'region': 'USA'}),
            "INSERT INTO users (name, age, region) VALUES ('Tom', '30', 'USA')"
        )

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

class SQLQueryBuilder:

    def select(self, table, columns='*', where=None):
        if columns != '*':
            columns = ', '.join(columns)
        query = f'SELECT {columns} FROM {table}'
        if where:
            conditions = ' AND '.join(f"{k}='{v}'" for k, v in where.items())
            query += ' WHERE ' + conditions
        return query

    def insert(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(f"'{v}'" for v in data.values())
        return f'INSERT INTO {table} ({keys}) VALUES ({values})'

    def delete(self, table, where=None):
        query = f'DELETE FROM {table}'
        if where:
            condition_parts = [f"{k}='{v}'" for k, v in where.items()]
            conditions_string = ' AND '.join(condition_parts)
            query += ' WHERE ' + conditions_string
        return query

    def update(self, table, data, where=None):
        update_str = ', '.join(f"{k}='{v}'" for k, v in data.items())
        query = f'UPDATE {table} SET {update_str}'
        if where:
            where_clause = ' AND '.join(f"{k}='{v}'" for k, v in where.items())
            query += ' WHERE ' + where_clause
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

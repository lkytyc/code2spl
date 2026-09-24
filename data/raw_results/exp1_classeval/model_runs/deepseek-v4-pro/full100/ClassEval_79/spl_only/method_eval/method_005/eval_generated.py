class SQLGenerator:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def select(self, fields=None, condition=None):
        if fields is None:
            fields = "*"
        else:
            fields = ", ".join(fields)
        sql = f"SELECT {fields} FROM {self.table_name}"
        if condition is not None:
            sql += f" WHERE {condition}"
        sql += ";"
        return sql

    def insert(self, data: dict):
        fields = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        sql = f"INSERT INTO {self.table_name} ({fields}) VALUES ({values})"
        return sql + ";"

    def update(self, data: dict, condition: str):
        formatted_pairs = [f"{field} = '{value}'" for field, value in data.items()]
        set_clause = ", ".join(formatted_pairs)
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
        return sql + ";"

    def delete(self, condition: str):
        sql = f"DELETE FROM {self.table_name} WHERE {condition}"
        return sql + ";"

    def select_female_under_age(self, age):
        condition = f"age < {age} AND gender = 'female'"
        return self.select(condition=condition)

    def select_by_age_range(self, min_age, max_age):
        condition = f"age BETWEEN {min_age} AND {max_age}"
        return self.select(condition=condition)

import unittest

class SQLGeneratorTestSelectByAgeRange(unittest.TestCase):
    def test_select_by_age_range(self):
        sql = SQLGenerator('table1')
        result = sql.select_by_age_range(20, 30)
        self.assertEqual(result, "SELECT * FROM table1 WHERE age BETWEEN 20 AND 30;")

    def test_select_by_age_range_2(self):
        sql = SQLGenerator('table1')
        result = sql.select_by_age_range(10, 20)
        self.assertEqual(result, "SELECT * FROM table1 WHERE age BETWEEN 10 AND 20;")

    def test_select_by_age_range_3(self):
        sql = SQLGenerator('table1')
        result = sql.select_by_age_range(30, 40)
        self.assertEqual(result, "SELECT * FROM table1 WHERE age BETWEEN 30 AND 40;")

    def test_select_by_age_range_4(self):
        sql = SQLGenerator('table1')
        result = sql.select_by_age_range(40, 50)
        self.assertEqual(result, "SELECT * FROM table1 WHERE age BETWEEN 40 AND 50;")

    def test_select_by_age_range_5(self):
        sql = SQLGenerator('table1')
        result = sql.select_by_age_range(50, 60)
        self.assertEqual(result, "SELECT * FROM table1 WHERE age BETWEEN 50 AND 60;")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

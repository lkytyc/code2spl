class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, condition=None):
        if fields:
            field_str = ", ".join(fields)
        else:
            field_str = "*"
        query = f"SELECT {field_str} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition}"
        return query + ";"

    def insert(self, data):
        columns = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"

    def update(self, data, condition):
        set_clause = ", ".join(f"{col} = '{value}'" for col, value in data.items())
        return f"UPDATE {self.table_name} SET {set_clause} WHERE {condition};"

    def delete(self, condition):
        return f"DELETE FROM {self.table_name} WHERE {condition};"

    def select_female_under_age(self, age):
        return self.select(condition=f"age < {age} AND gender = 'female'")

    def select_by_age_range(self, min_age, max_age):
        return self.select(condition=f"age BETWEEN {min_age} AND {max_age}")

import unittest

class SQLGeneratorTestSelectFemaleUnderAge(unittest.TestCase):
    def test_select_female_under_age(self):
        sql = SQLGenerator('table1')
        result = sql.select_female_under_age(30)
        self.assertEqual(result, "SELECT * FROM table1 WHERE age < 30 AND gender = 'female';")

    def test_select_female_under_age_2(self):
        sql = SQLGenerator('table1')
        result = sql.select_female_under_age(40)
        self.assertEqual(result,"SELECT * FROM table1 WHERE age < 40 AND gender = 'female';")

    def test_select_female_under_age_3(self):
        sql = SQLGenerator('table1')
        result = sql.select_female_under_age(20)
        self.assertEqual(result,"SELECT * FROM table1 WHERE age < 20 AND gender = 'female';")

    def test_select_female_under_age_4(self):
        sql = SQLGenerator('table1')
        result = sql.select_female_under_age(10)
        self.assertEqual(result,"SELECT * FROM table1 WHERE age < 10 AND gender = 'female';")

    def test_select_female_under_age_5(self):
        sql = SQLGenerator('table1')
        result = sql.select_female_under_age(50)
        self.assertEqual(result,"SELECT * FROM table1 WHERE age < 50 AND gender = 'female';")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

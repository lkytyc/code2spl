class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, condition=None):
        if fields is None:
            field_list = "*"
        elif isinstance(fields, (list, tuple)):
            field_list = ", ".join(fields)
        else:
            field_list = str(fields)

        query = f"SELECT {field_list} FROM {self.table_name}"
        if condition:
            query += f" WHERE {condition}"
        return query + ";"

    def insert(self, data):
        fields = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        return f"INSERT INTO {self.table_name} ({fields}) VALUES ({values});"

    def update(self, data, condition):
        set_clause = ", ".join(f"{key} = '{value}'" for key, value in data.items())
        return f"UPDATE {self.table_name} SET {set_clause} WHERE {condition};"

    def delete(self, condition):
        return f"DELETE FROM {self.table_name} WHERE {condition};"

    def select_female_under_age(self, age):
        condition = f"age < {age} AND gender = 'female'"
        return self.select(condition=condition)

    def select_by_age_range(self, min_age, max_age):
        condition = f"age BETWEEN {min_age} AND {max_age}"
        return self.select(condition=condition)

import unittest

class SQLGeneratorTestSelect(unittest.TestCase):
    def test_select_1(self):
        sql = SQLGenerator('table1')
        result = sql.select(['field1'], "field2 = value1")
        self.assertEqual(result, "SELECT field1 FROM table1 WHERE field2 = value1;")

    def test_select_2(self):
        sql = SQLGenerator('table1')
        result = sql.select(['field1', 'field2'], "field3 = value1")
        self.assertEqual(result, "SELECT field1, field2 FROM table1 WHERE field3 = value1;")

    def test_select_3(self):
        sql = SQLGenerator('table1')
        result = sql.select(['field1, field2'], "field3 = value1")
        self.assertEqual(result, "SELECT field1, field2 FROM table1 WHERE field3 = value1;")

    def test_select_4(self):
        sql = SQLGenerator('table1')
        result = sql.select(['field1, field2'], "field3 = value1, field4 = value2")
        self.assertEqual(result, "SELECT field1, field2 FROM table1 WHERE field3 = value1, field4 = value2;")

    def test_select_5(self):
        sql = SQLGenerator('table1')
        result = sql.select(['field1'], "field2 = value1, field3 = value2")
        self.assertEqual(result, "SELECT field1 FROM table1 WHERE field2 = value1, field3 = value2;")

    def test_select_6(self):
        sql = SQLGenerator('table1')
        result = sql.select(['field1'])
        self.assertEqual(result, "SELECT field1 FROM table1;")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def delete(self, condition):
        sql = f"DELETE FROM {self.table_name} WHERE {condition}"
        return sql + ";"

    def insert(self, data):
        fields = ", ".join(data.keys())
        values = ", ".join(f"'{value}'" for value in data.values())
        sql = f"INSERT INTO {self.table_name} ({fields}) VALUES ({values})"
        return sql + ";"

    def select(self, fields=None, condition=None):
        if fields is None:
            fields = "*"
        else:
            fields = ", ".join(fields)
        sql = f"SELECT {fields} FROM {self.table_name}"
        if condition is not None:
            sql += f" WHERE {condition}"
        return sql + ";"

    def select_by_age_range(self, min_age, max_age):
        condition = f"age BETWEEN {min_age} AND {max_age}"
        return self.select(condition=condition)

    def select_female_under_age(self, age):
        condition = f"age < {age} AND gender = 'female'"
        return self.select(condition=condition)

    def update(self, data, condition):
        formatted_pairs = [f"{field} = '{value}'" for field, value in data.items()]
        set_clause = ", ".join(formatted_pairs)
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
        return sql + ";"

import unittest

class SQLGeneratorTestDelete(unittest.TestCase):
    def test_delete(self):
        sql = SQLGenerator('table1')
        result = sql.delete("field1 = value1")
        self.assertEqual(result, "DELETE FROM table1 WHERE field1 = value1;")

    def test_delete_2(self):
        sql = SQLGenerator('table1')
        result = sql.delete("field1 = value1 AND field2 = value2")
        self.assertEqual(result, "DELETE FROM table1 WHERE field1 = value1 AND field2 = value2;")

    def test_delete_3(self):
        sql = SQLGenerator('table1')
        result = sql.delete("field1 = value1 AND field2 = value2 AND field3 = value3")
        self.assertEqual(result, "DELETE FROM table1 WHERE field1 = value1 AND field2 = value2 AND field3 = value3;")

    def test_delete_4(self):
        sql = SQLGenerator('table1')
        result = sql.delete("field1 = value1 AND field2 = value2 AND field3 = value3 AND field4 = value4")
        self.assertEqual(result,
                         "DELETE FROM table1 WHERE field1 = value1 AND field2 = value2 AND field3 = value3 AND field4 = value4;")

    def test_delete_5(self):
        sql = SQLGenerator('table1')
        result = sql.delete("field1 = value1 AND field2 = value2 AND field3 = value3 AND field4 = value4 AND field5 = value5")
        self.assertEqual(result,
                         "DELETE FROM table1 WHERE field1 = value1 AND field2 = value2 AND field3 = value3 AND field4 = value4 AND field5 = value5;")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

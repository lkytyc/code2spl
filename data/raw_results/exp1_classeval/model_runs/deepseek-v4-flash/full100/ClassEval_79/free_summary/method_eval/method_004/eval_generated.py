class SQLGenerator:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, fields=None, where=None):
        if fields is None:
            fields_part = "*"
        elif isinstance(fields, (list, tuple)):
            fields_part = ", ".join(fields) if fields else "*"
        else:
            fields_part = str(fields) if str(fields).strip() else "*"
        where_clause = f" WHERE {where}" if where else ""
        return f"SELECT {fields_part} FROM {self.table_name}{where_clause};"

    def insert(self, data):
        columns = ", ".join(data.keys())
        values = ", ".join(f"'{v}'" for v in data.values())
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"

    def update(self, data, where=None):
        set_clause = ", ".join(f"{k} = '{v}'" for k, v in data.items())
        where_clause = f" WHERE {where}" if where else ""
        return f"UPDATE {self.table_name} SET {set_clause}{where_clause};"

    def delete(self, where=None):
        where_clause = f" WHERE {where}" if where else ""
        return f"DELETE FROM {self.table_name}{where_clause};"

    def select_female_under_age(self, age):
        where = f"gender = 'female' AND age < '{age}'"
        return self.select(where=where)

    def select_by_age_range(self, age_min, age_max):
        where = f"age >= '{age_min}' AND age <= '{age_max}'"
        return self.select(where=where)

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

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

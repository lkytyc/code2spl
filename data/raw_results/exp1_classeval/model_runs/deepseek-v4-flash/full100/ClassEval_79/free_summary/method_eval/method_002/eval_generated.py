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

class SQLGeneratorTestUpdate(unittest.TestCase):
    def test_update(self):
        sql = SQLGenerator('table1')
        result = sql.update({'field1': 'new_value1', 'field2': 'new_value2'}, "field3 = value1")
        self.assertEqual(result,
                         "UPDATE table1 SET field1 = 'new_value1', field2 = 'new_value2' WHERE field3 = value1;")

    def test_update_2(self):
        sql = SQLGenerator('table1')
        result = sql.update({'field1': 'new_value1', 'field2': 'new_value2', 'field3': 'new_value3'},
                            "field4 = value1")
        self.assertEqual(result,
                         "UPDATE table1 SET field1 = 'new_value1', field2 = 'new_value2', field3 = 'new_value3' WHERE field4 = value1;")

    def test_update_3(self):
        sql = SQLGenerator('table1')
        result = sql.update({'field1': 'new_value1', 'field2': 'new_value2', 'field3': 'new_value3',
                             'field4': 'new_value4'}, "field5 = value1")
        self.assertEqual(result,
                         "UPDATE table1 SET field1 = 'new_value1', field2 = 'new_value2', field3 = 'new_value3', field4 = 'new_value4' WHERE field5 = value1;")

    def test_update_4(self):
        sql = SQLGenerator('table1')
        result = sql.update({'field1': 'new_value1', 'field2': 'new_value2', 'field3': 'new_value3',
                             'field4': 'new_value4', 'field5': 'new_value5'}, "field6 = value1")
        self.assertEqual(result,
                         "UPDATE table1 SET field1 = 'new_value1', field2 = 'new_value2', field3 = 'new_value3', field4 = 'new_value4', field5 = 'new_value5' WHERE field6 = value1;")

    def test_update_5(self):
        sql = SQLGenerator('table1')
        result = sql.update({'field1': 'new_value1', 'field2': 'new_value2', 'field3': 'new_value3',
                             'field4': 'new_value4', 'field5': 'new_value5', 'field6': 'new_value6'},
                            "field7 = value1")
        self.assertEqual(result,
                         "UPDATE table1 SET field1 = 'new_value1', field2 = 'new_value2', field3 = 'new_value3', field4 = 'new_value4', field5 = 'new_value5', field6 = 'new_value6' WHERE field7 = value1;")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

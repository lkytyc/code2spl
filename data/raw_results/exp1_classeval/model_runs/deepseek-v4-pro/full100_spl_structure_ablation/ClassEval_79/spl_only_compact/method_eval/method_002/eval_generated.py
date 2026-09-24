class SQLGenerator:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def delete(self, condition: str) -> str:
        sql = f'DELETE FROM {self.table_name} WHERE {condition}'
        return sql + ';'

    def insert(self, data: dict) -> str:
        fields = ', '.join(data.keys()) if data else ''
        values = ', '.join(f"'{value}'" for value in data.values()) if data else ''
        sql = f'INSERT INTO {self.table_name} ({fields}) VALUES ({values})'
        return sql + ';'

    def select(self, fields=None, condition=None) -> str:
        if fields is None:
            fields = '*'
        else:
            fields = ', '.join(fields)
        sql = f'SELECT {fields} FROM {self.table_name}'
        if condition is not None:
            sql += f' WHERE {condition}'
        return sql + ';'

    def select_by_age_range(self, min_age: object, max_age: object) -> object:
        condition = f'age BETWEEN {min_age} AND {max_age}'
        return self.select(condition=condition)

    def select_female_under_age(self, age: int) -> str:
        condition = f"age < {age} AND gender = 'female'"
        return self.select(condition=condition)

    def update(self, data: dict, condition: str) -> str:
        formatted_pairs = [f"{field} = '{value}'" for field, value in data.items()]
        set_clause = ', '.join(formatted_pairs)
        sql = f'UPDATE {self.table_name} SET {set_clause} WHERE {condition}'
        return sql + ';'

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

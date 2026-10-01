class SQLGenerator:
    def __init__(self, table_name: str):
        self.table_name = table_name

    def delete(self, condition: str) -> str:
        sql = f'DELETE FROM {self.table_name} WHERE {condition}'
        return sql + ';'

    def insert(self, data: dict) -> str:
        fields = ', '.join(data.keys())
        values = ', '.join(f"'{value}'" for value in data.values())
        sql = f"INSERT INTO {self.table_name} ({fields}) VALUES ({values})"
        final_sql = sql + ';'
        return final_sql

    def select(self, fields: list[str] or None, condition: str or None) -> str:
        if fields is None:
            normalized_fields = '*'
        else:
            normalized_fields = ', '.join(fields)
        sql = f'SELECT {normalized_fields} FROM {self.table_name}'
        if condition is not None:
            sql += f' WHERE {condition}'
        return sql + ';'

    def select_by_age_range(self, min_age: number, max_age: number) -> object:
        condition = f'age BETWEEN {str(min_age)} AND {str(max_age)}'
        return self.select(condition=condition)

    def select_female_under_age(self, age: object) -> object:
        condition = f"age < {age} AND gender = 'female'"
        return self.select(condition=condition)

    def update(self, data: dict, condition: str) -> str:
        set_clause = ', '.join(f"{field} = '{value}'" for field, value in data.items())
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {condition}"
        return sql + ';'

import unittest

class SQLGeneratorTestInsert(unittest.TestCase):
    def test_insert(self):
        sql = SQLGenerator('table1')
        result = sql.insert({'field1': 'value1', 'field2': 'value2'})
        self.assertEqual(result, "INSERT INTO table1 (field1, field2) VALUES ('value1', 'value2');")

    def test_insert_2(self):
        sql = SQLGenerator('table1')
        result = sql.insert({'field1': 'value1', 'field2': 'value2', 'field3': 'value3'})
        self.assertEqual(result, "INSERT INTO table1 (field1, field2, field3) VALUES ('value1', 'value2', 'value3');")

    def test_insert_3(self):
        sql = SQLGenerator('table1')
        result = sql.insert({'field1': 'value1', 'field2': 'value2', 'field3': 'value3', 'field4': 'value4'})
        self.assertEqual(result,
                         "INSERT INTO table1 (field1, field2, field3, field4) VALUES ('value1', 'value2', 'value3', 'value4');")

    def test_insert_4(self):
        sql = SQLGenerator('table1')
        result = sql.insert({'field1': 'value1', 'field2': 'value2', 'field3': 'value3', 'field4': 'value4',
                             'field5': 'value5'})
        self.assertEqual(result,
                         "INSERT INTO table1 (field1, field2, field3, field4, field5) VALUES ('value1', 'value2', 'value3', 'value4', 'value5');")

    def test_insert_5(self):
        sql = SQLGenerator('table1')
        result = sql.insert({'field1': 'value1', 'field2': 'value2', 'field3': 'value3', 'field4': 'value4',
                             'field5': 'value5', 'field6': 'value6'})
        self.assertEqual(result,
                         "INSERT INTO table1 (field1, field2, field3, field4, field5, field6) VALUES ('value1', 'value2', 'value3', 'value4', 'value5', 'value6');")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

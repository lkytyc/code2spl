class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def _convert_key(self, key: object) -> object:
        if isinstance(key, str):
            return self._to_camel_case(key)
        return key

    def _to_camel_case(self, key: str) -> str:
        parts = key.split("_")
        return parts[0] + "".join(part.title() for part in parts[1:])

import unittest

class CamelCaseMapTestIter(unittest.TestCase):
    def test_iter_1(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map['last_name'] = 'Doe'
        camelize_map['age'] = 30
        lst = ['firstName', 'lastName', 'age']
        iter = camelize_map.__iter__()
        i = 0
        for key in iter:
            self.assertEqual(key, lst[i])
            i += 1

    def test_iter_2(self):
        camelize_map = CamelCaseMap()
        camelize_map['firstname'] = 'John'
        camelize_map['lastname'] = 'Doe'
        camelize_map['age'] = 30
        lst = ['firstname', 'lastname', 'age']
        iter = camelize_map.__iter__()
        i = 0
        for key in iter:
            self.assertEqual(key, lst[i])
            i += 1

    def test_iter_3(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_Name'] = 'John'
        camelize_map['last_Name'] = 'Doe'
        camelize_map['age'] = 30
        lst = ['firstName', 'lastName', 'age']
        iter = camelize_map.__iter__()
        i = 0
        for key in iter:
            self.assertEqual(key, lst[i])
            i += 1

    def test_iter_4(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_Name'] = 'John'
        camelize_map['last_Name'] = 'Doe'
        lst = ['firstName', 'lastName']
        iter = camelize_map.__iter__()
        i = 0
        for key in iter:
            self.assertEqual(key, lst[i])
            i += 1

    def test_iter_5(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_Name'] = 'John'
        lst = ['firstName']
        iter = camelize_map.__iter__()
        i = 0
        for key in iter:
            self.assertEqual(key, lst[i])
            i += 1

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

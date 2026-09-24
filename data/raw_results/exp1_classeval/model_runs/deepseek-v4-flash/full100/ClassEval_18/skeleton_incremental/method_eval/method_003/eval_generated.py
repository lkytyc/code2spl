class CamelCaseMap:
    """
    This is a custom class that allows keys to be in camel case style by converting them from underscore style, which provides dictionary-like functionality.
    """

    def __init__(self):
        """
        Initialize data to an empty dictionary
        """
        self._data = {}

    def __getitem__(self, key):
        """
        Return the value corresponding to the key
        :param key:str
        :return:str,the value corresponding to the key
        """
        return self._data[self._convert_key(key)]

    def __setitem__(self, key, value):
        """
        Set the value corresponding to the key to the specified value
        :param key:str
        :param value:str, the specified value
        :return:None
        """
        self._data[self._convert_key(key)] = value

    def __delitem__(self, key):
        """
        Delete the value corresponding to the key
        :param key:str
        :return:None
        """
        del self._data[self._convert_key(key)]

    def __iter__(self):
        """
        Returning Iterateable Objects with Own Data
        :return:Iterator
        """
        return iter(self._data)

    def __len__(self):
        """
        Returns the length of the own data
        :return:int, length of data
        """
        return len(self._data)

    def _convert_key(self, key):
        """
        convert key string into camel case
        :param key:str
        :return:str, converted key string
        """
        if isinstance(key, str):
            return self._to_camel_case(key)
        return key

    @staticmethod
    def _to_camel_case(key):
        """
        convert key string into camel case
        :param key:str
        :return:str, converted key string
        """
        parts = key.split('_')
        return parts[0] + ''.join(part.title() for part in parts[1:])

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

class CamelCaseMap:
    def __init__(self, *args, **kwargs):
        self._data = {}
        if args:
            if len(args) > 1:
                raise TypeError(f"expected at most 1 argument, got {len(args)}")
            other = args[0]
            if hasattr(other, 'keys'):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    @staticmethod
    def _to_camel_case(snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(part.capitalize() for part in parts[1:])

    def _convert_key(self, key):
        if isinstance(key, str):
            return self._to_camel_case(key)
        return key

    def __getitem__(self, key):
        return self._data[self._convert_key(key)]

    def __setitem__(self, key, value):
        self._data[self._convert_key(key)] = value

    def __delitem__(self, key):
        del self._data[self._convert_key(key)]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return self._convert_key(key) in self._data

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def pop(self, key, default=None):
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def update(self, other=None, **kwargs):
        if other is not None:
            if hasattr(other, 'keys'):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def clear(self):
        self._data.clear()

    def copy(self):
        new = CamelCaseMap()
        new._data = self._data.copy()
        return new

    def __repr__(self):
        return f"CamelCaseMap({self._data!r})"

    def __eq__(self, other):
        if isinstance(other, CamelCaseMap):
            return self._data == other._data
        return NotImplemented

import unittest

class CamelCaseMapTestSetitem(unittest.TestCase):
    def test_setitem_1(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_name', 'newname')
        self.assertEqual(camelize_map['first_name'], 'newname')

    def test_setitem_2(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_name', 'John')
        self.assertEqual(camelize_map['first_name'], 'John')

    def test_setitem_3(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_Name', 'newname')
        self.assertEqual(camelize_map['first_name'], 'newname')

    def test_setitem_4(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('firstName', 'newname')
        self.assertEqual(camelize_map['first_name'], 'newname')

    def test_setitem_5(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_name', '')
        self.assertEqual(camelize_map['first_name'], '')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

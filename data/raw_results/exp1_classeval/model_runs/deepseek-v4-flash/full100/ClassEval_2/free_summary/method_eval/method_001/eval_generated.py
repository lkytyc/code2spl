class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def add_argument(self, name, required=False, type=None):
        self.arguments[name] = None
        if required:
            self.required.add(name)
        if type is not None:
            self.types[name] = type

    def parse_arguments(self, arg_string):
        tokens = arg_string.split()
        if not tokens:
            return (False, set(self.required))
        tokens = tokens[1:]  # skip program name

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith('--'):
                if '=' in token:
                    key, value = token[2:].split('=', 1)
                else:
                    key = token[2:]
                    value = True
                self.arguments[key] = self._convert_type(key, value)
                i += 1
            elif token.startswith('-') and len(token) > 1:
                key = token[1:]
                if i + 1 < len(tokens) and not tokens[i+1].startswith('-'):
                    value = tokens[i+1]
                    i += 2
                else:
                    value = True
                    i += 1
                self.arguments[key] = self._convert_type(key, value)
            else:
                i += 1

        missing = self.required - set(self.arguments.keys())
        if missing:
            return (False, missing)
        return (True, None)

    def _convert_type(self, key, value):
        if key in self.types:
            try:
                return self.types[key](value)
            except (ValueError, TypeError):
                return value
        return value

    def get_argument(self, key):
        return self.arguments.get(key)

import unittest

class ArgumentParserTestGetArgument(unittest.TestCase):

    def setUp(self):
        self.parser = ArgumentParser()

    # key exists
    def test_get_argument_1(self):
        self.parser.arguments = {"name": "John"}
        result = self.parser.get_argument("name")
        self.assertEqual(result, "John")

    # key not exists
    def test_get_argument_2(self):
        self.parser.arguments = {"name": "John", "age": 25}
        result = self.parser.get_argument("age")
        self.assertEqual(result, 25)

    def test_get_argument_3(self):
        self.parser.arguments = {"name": "John", "age": "25", "verbose": True}
        result = self.parser.get_argument("verbose")
        self.assertEqual(result, True)

    def test_get_argument_4(self):
        self.parser.arguments = {"name": "Amy", "age": 25, "verbose": True, "d": True}
        result = self.parser.get_argument("d")
        self.assertEqual(result, True)

    def test_get_argument_5(self):
        self.parser.arguments = {"name": "John", "age": 25, "verbose": True, "d": True, "option": "value"}
        result = self.parser.get_argument("option")
        self.assertEqual(result, "value")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

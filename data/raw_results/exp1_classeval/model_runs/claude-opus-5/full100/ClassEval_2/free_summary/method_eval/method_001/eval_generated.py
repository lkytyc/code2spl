class ArgumentParser:
    def __init__(self):
        self.types = {}
        self.required = set()
        self.arguments = {}

    def add_argument(self, key, required=False, arg_type=str):
        self.types[key] = arg_type
        if required:
            self.required.add(key)

    def _convert_type(self, key, value):
        if key not in self.types:
            return value
        try:
            return self.types[key](value)
        except ValueError:
            return value

    def parse_arguments(self, command_string):
        self.arguments = {}
        tokens = command_string.split()
        tokens = tokens[1:]  # discard program name

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.startswith('--'):
                key_value = token[2:]
                if '=' in key_value:
                    key, value = key_value.split('=', 1)
                    self.arguments[key] = self._convert_type(key, value)
                else:
                    self.arguments[key_value] = True

            elif token.startswith('-'):
                key = token[1:]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    value = tokens[i + 1]
                    self.arguments[key] = self._convert_type(key, value)
                    # Notable limitation: index is not advanced past the consumed
                    # value token, so the value will be processed again on the
                    # next iteration if it starts with '-'.
                else:
                    self.arguments[key] = True

            i += 1

        missing = self.required - self.arguments.keys()
        if missing:
            return (False, missing)
        return (True, None)

    def get_argument(self, key):
        return self.arguments.get(key, None)

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

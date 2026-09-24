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

class ArgumentParserTestConvertType(unittest.TestCase):

    def setUp(self):
        self.parser = ArgumentParser()

    def test_convert_type_1(self):
        self.parser.types = {"age": int}
        result = self.parser._convert_type("age", "25")
        self.assertEqual(result, 25)

    # fail
    def test_convert_type_2(self):
        self.parser.types = {"age": int}
        result = self.parser._convert_type("age", "twenty-five")
        self.assertEqual(result, "twenty-five")

    def test_convert_type_3(self):
        self.parser.types = {"age": int}
        result = self.parser._convert_type("age", "25")
        self.assertEqual(result, 25)

    def test_convert_type_4(self):
        self.parser.types = {"age": int, "verbose": bool}
        result = self.parser._convert_type("verbose", "True")
        self.assertEqual(result, True)
    
    def test_convert_type_5(self):
        self.parser.types = {"age": int, "verbose": bool}
        result = self.parser._convert_type("verbose", "False")
        self.assertEqual(result, True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

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

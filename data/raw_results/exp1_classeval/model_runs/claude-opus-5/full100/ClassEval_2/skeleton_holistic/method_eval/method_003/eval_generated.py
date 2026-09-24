class ArgumentParser:
    """
    This is a class for parsing command line arguments to a dictionary.
    """

    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        tokens = command_string.split()
        # skip the program name tokens (e.g. "python script.py")
        i = 1
        while i < len(tokens) and not tokens[i].startswith('-'):
            i += 1

        while i < len(tokens):
            token = tokens[i]
            if token.startswith('--'):
                key = token[2:]
                if '=' in key:
                    k, v = key.split('=', 1)
                    self.arguments[k] = self._convert_type(k, v)
                else:
                    # check if next token is a value
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                        self.arguments[key] = self._convert_type(key, tokens[i + 1])
                        i += 1
                    else:
                        self.arguments[key] = True
            elif token.startswith('-'):
                key = token[1:]
                if '=' in key:
                    k, v = key.split('=', 1)
                    self.arguments[k] = self._convert_type(k, v)
                else:
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                        self.arguments[key] = self._convert_type(key, tokens[i + 1])
                        i += 1
                    else:
                        self.arguments[key] = True
            i += 1

        missing = self.required - set(self.arguments.keys())
        if missing:
            return False, missing
        return True, None

    def get_argument(self, key):
        return self.arguments.get(key, None)

    def add_argument(self, arg, required=False, arg_type=str):
        self.types[arg] = arg_type
        if required:
            self.required.add(arg)

    def _convert_type(self, arg, value):
        if arg not in self.types:
            return value
        arg_type = self.types[arg]
        try:
            return arg_type(value)
        except (ValueError, TypeError):
            return value

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

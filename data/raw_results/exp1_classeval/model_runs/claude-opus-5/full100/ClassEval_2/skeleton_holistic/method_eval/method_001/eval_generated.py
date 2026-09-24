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

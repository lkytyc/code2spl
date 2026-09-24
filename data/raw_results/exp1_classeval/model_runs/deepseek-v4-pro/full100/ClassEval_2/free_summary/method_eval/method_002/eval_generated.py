class ArgumentParser:
    def __init__(self):
        self.required = set()
        self.types = {}
        self.arguments = {}

    def add_argument(self, name, required=False, arg_type=None):
        if required:
            self.required.add(name)
        if arg_type is not None:
            self.types[name] = arg_type

    def _convert_type(self, name, value):
        if name in self.types:
            try:
                return self.types[name](value)
            except (ValueError, TypeError):
                return value
        return value

    def parse_arguments(self, command_string):
        tokens = command_string.split()
        if not tokens:
            return (False, set(self.required))
        tokens = tokens[1:]
        self.arguments = {}
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith('--'):
                if '=' in token:
                    name, value = token[2:].split('=', 1)
                    self.arguments[name] = self._convert_type(name, value)
                else:
                    name = token[2:]
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                        value = tokens[i + 1]
                        self.arguments[name] = self._convert_type(name, value)
                        i += 1
                    else:
                        self.arguments[name] = True
            elif token.startswith('-') and token != '-':
                name = token[1:]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                    value = tokens[i + 1]
                    self.arguments[name] = self._convert_type(name, value)
                    i += 1
                else:
                    self.arguments[name] = True
            i += 1

        missing = self.required - set(self.arguments.keys())
        if missing:
            return (False, missing)
        return (True, None)

    def get_argument(self, key):
        return self.arguments.get(key, None)

import unittest

class ArgumentParserTestAddArgument(unittest.TestCase):

    def setUp(self):
        self.parser = ArgumentParser()

    def test_add_argument(self):
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=True, arg_type=int)

        self.assertEqual(self.parser.required, {"age"})
        self.assertEqual(self.parser.types, {"name": str, "age": int})

    def test_add_argument_2(self):
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=False, arg_type=int)
        self.parser.add_argument("verbose", arg_type=bool)

        self.assertEqual(self.parser.required, set())
        self.assertEqual(self.parser.types, {"name": str, "age": int, "verbose": bool})

    def test_add_argument_3(self):
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=False, arg_type=int)
        self.parser.add_argument("verbose", arg_type=bool)
        self.parser.add_argument("d")

        self.assertEqual(self.parser.required, set())
        self.assertEqual(self.parser.types, {"name": str, "age": int, "verbose": bool, "d": str})

    def test_add_argument_4(self):
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=False, arg_type=int)
        self.parser.add_argument("verbose", arg_type=bool)
        self.parser.add_argument("d")
        self.parser.add_argument("option")

        self.assertEqual(self.parser.required, set())
        self.assertEqual(self.parser.types, {"name": str, "age": int, "verbose": bool, "d": str, "option": str})

    def test_add_argument_5(self):
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=False, arg_type=int)
        self.parser.add_argument("verbose", arg_type=bool)
        self.parser.add_argument("d")
        self.parser.add_argument("option")
        self.parser.add_argument("option2", arg_type=bool)

        self.assertEqual(self.parser.required, set())
        self.assertEqual(self.parser.types, {"name": str, "age": int, "verbose": bool, "d": str, "option": str, "option2": bool})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

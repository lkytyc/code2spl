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

class ArgumentParserTestParseArguments(unittest.TestCase):

    def setUp(self):
        self.parser = ArgumentParser()

    # key value arguments
    def test_parse_arguments_1(self):
        command_str = "script --name=John --age=25"
        self.parser.add_argument("name")
        self.parser.add_argument("age", arg_type=int)

        result, missing_args = self.parser.parse_arguments(command_str)

        self.assertTrue(result)
        self.assertIsNone(missing_args)
        self.assertEqual(self.parser.get_argument("name"), "John")
        self.assertEqual(self.parser.get_argument("age"), 25)

    # switches options
    def test_parse_arguments_2(self):
        command_str = "script --verbose -d"
        self.parser.add_argument("verbose", arg_type=bool)
        self.parser.add_argument("d", arg_type=bool)

        result, missing_args = self.parser.parse_arguments(command_str)

        self.assertTrue(result)
        self.assertIsNone(missing_args)
        self.assertEqual(self.parser.get_argument("verbose"), True)
        self.assertEqual(self.parser.get_argument("d"), True)

    # miss required
    def test_parse_arguments_3(self):
        command_str = "script --name=John"
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=True, arg_type=int)

        result, missing_args = self.parser.parse_arguments(command_str)

        self.assertFalse(result)
        self.assertEqual(missing_args, {"age"})

    def test_parse_arguments_4(self):
        command_str = "script --name=John"
        self.parser.add_argument("name")
        self.parser.add_argument("age", required=False, arg_type=int)

        result, missing_args = self.parser.parse_arguments(command_str)

        self.assertTrue(result)
        self.assertEqual(missing_args, None)

    def test_parse_arguments_5(self):
        command_str = "script --name=John"
        self.parser.add_argument("name")
        self.parser.add_argument("age", arg_type=int)

        result, missing_args = self.parser.parse_arguments(command_str)

        self.assertTrue(result)
        self.assertEqual(missing_args, None)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

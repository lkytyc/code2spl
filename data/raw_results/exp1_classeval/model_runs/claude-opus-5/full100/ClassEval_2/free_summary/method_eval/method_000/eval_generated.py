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

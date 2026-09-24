class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def add_argument(self, arg, required=False, arg_type=str):
        self.types[arg] = arg_type
        if required:
            self.required.add(arg)

    def _convert_type(self, key, value):
        if key not in self.types:
            return value
        converter = self.types[key]
        try:
            return converter(value)
        except Exception:
            return value

    def parse_arguments(self, command_string):
        self.arguments = {}
        tokens = command_string.split()
        if not tokens:
            missing = set(self.required)
            return (False, missing if missing else None)

        i = 1
        while i < len(tokens):
            token = tokens[i]

            if token.startswith("--"):
                name_value = token[2:]
                if "=" in name_value:
                    key, value = name_value.split("=", 1)
                else:
                    key = name_value
                    value = True
                self.arguments[key] = self._convert_type(key, value)
                i += 1
                continue

            if token.startswith("-") and token != "-":
                key = token[1:]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    value = tokens[i + 1]
                    i += 2
                else:
                    value = True
                    i += 1
                self.arguments[key] = self._convert_type(key, value)
                continue

            i += 1

        missing = {arg for arg in self.required if arg not in self.arguments}
        if missing:
            return False, missing
        return True, None

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

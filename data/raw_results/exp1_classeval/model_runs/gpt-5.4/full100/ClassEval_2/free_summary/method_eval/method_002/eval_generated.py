class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required_arguments = set()
        self.argument_types = {}

    def add_argument(self, arg, required=False, arg_type=str):
        self.argument_types[arg] = arg_type
        if required:
            self.required_arguments.add(arg)

    def parse_arguments(self, command_string):
        self.arguments = {}
        tokens = command_string.split()
        if not tokens:
            missing = self.required_arguments - set(self.arguments.keys())
            if missing:
                return False, missing
            return True, None

        i = 1
        while i < len(tokens):
            token = tokens[i]

            if token.startswith("--"):
                body = token[2:]
                if "=" in body:
                    key, value = body.split("=", 1)
                else:
                    key = body
                    value = True
                self.arguments[key] = self._convert_value(key, value)
                i += 1
                continue

            if token.startswith("-"):
                key = token[1:]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("-"):
                    value = tokens[i + 1]
                    i += 2
                else:
                    value = True
                    i += 1
                self.arguments[key] = self._convert_value(key, value)
                continue

            i += 1

        missing = self.required_arguments - set(self.arguments.keys())
        if missing:
            return False, missing
        return True, None

    def _convert_value(self, key, value):
        if value is True:
            return value
        arg_type = self.argument_types.get(key)
        if arg_type is None:
            return value
        try:
            return arg_type(value)
        except (ValueError, TypeError):
            return value

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

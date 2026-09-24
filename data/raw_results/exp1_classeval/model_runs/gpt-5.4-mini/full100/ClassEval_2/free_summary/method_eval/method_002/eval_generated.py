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

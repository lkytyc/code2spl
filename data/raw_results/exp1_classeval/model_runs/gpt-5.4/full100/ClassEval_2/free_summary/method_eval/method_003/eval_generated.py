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

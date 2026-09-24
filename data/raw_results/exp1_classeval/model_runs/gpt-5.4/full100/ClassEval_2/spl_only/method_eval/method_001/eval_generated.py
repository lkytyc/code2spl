class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def parse_arguments(self, command_string):
        args = command_string.split()[1:]

        for i in range(len(args)):
            arg = args[i]

            if arg.startswith("--"):
                key_value = arg[2:].split("=")
                if len(key_value) == 2:
                    key, value = key_value
                    self.arguments[key] = self._convert_type(key, value)
                else:
                    self.arguments[key_value[0]] = True

            elif arg.startswith("-"):
                key = arg[1:]
                if i + 1 < len(args) and not args[i + 1].startswith("-"):
                    self.arguments[key] = self._convert_type(key, args[i + 1])
                else:
                    self.arguments[key] = True

        missing_args = self.required - set(self.arguments.keys())
        if missing_args:
            return False, missing_args
        return True, None

    def get_argument(self, key):
        result = self.arguments.get(key)
        return result

    def add_argument(self, arg, required=False, arg_type=str):
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def _convert_type(self, arg, value):
        try:
            converted_value = self.types[arg](value)
            return converted_value
        except (ValueError, KeyError):
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

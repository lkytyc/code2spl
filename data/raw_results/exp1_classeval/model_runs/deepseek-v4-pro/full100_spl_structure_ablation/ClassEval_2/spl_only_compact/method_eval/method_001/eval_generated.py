class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def _convert_type(self, arg, value):
        try:
            converter = self.types[arg]
            converted_value = converter(value)
            return converted_value
        except (ValueError, KeyError):
            return value

    def add_argument(self, arg, required, arg_type):
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def get_argument(self, key):
        arguments_map = self.arguments
        return arguments_map.get(key, None)

    def parse_arguments(self, command_string):
        args = command_string.split()[1:]
        for i, arg in enumerate(args):
            if arg.startswith('--'):
                key_value = arg[2:].split('=')
                if len(key_value) == 2:
                    self.arguments[key_value[0]] = self._convert_type(key_value[0], key_value[1])
                else:
                    self.arguments[key_value[0]] = True
            elif arg.startswith('-'):
                key = arg[1:]
                if i + 1 < len(args) and not args[i + 1].startswith('-'):
                    self.arguments[key] = self._convert_type(key, args[i + 1])
                else:
                    self.arguments[key] = True
            else:
                continue
        missing_args = self.required - set(self.arguments.keys())
        if not missing_args:
            return True, None
        else:
            return False, missing_args

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

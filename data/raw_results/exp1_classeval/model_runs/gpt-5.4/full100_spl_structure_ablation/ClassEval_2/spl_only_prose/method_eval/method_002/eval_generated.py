class ArgumentParser:
    def __init__(self):
        self.arguments = {}
        self.required = set()
        self.types = {}

    def _convert_type(self, arg: any, value: any) -> any:
        try:
            converted_value = self.types[arg](value)
            return converted_value
        except (KeyError, TypeError, ValueError):
            return value

    def add_argument(
        self,
        arg: any,
        required: bool = False,
        arg_type: type = str,
    ):
        if required:
            self.required.add(arg)
        self.types[arg] = arg_type

    def get_argument(self, key: any) -> any:
        result = self.arguments.get(key)
        return result

    def parse_arguments(self):
        import sys

        args = sys.argv[1:]

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

        missing_args = self.required - self.arguments.keys()

        if missing_args:
            return False, missing_args

        return True, None

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

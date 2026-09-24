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

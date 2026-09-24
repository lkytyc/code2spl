import json


class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file_as_json(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

    def read_file(self):
        with open(self.file_path, 'r') as file_handle:
            file_contents = file_handle.read()
        return file_contents

    def write_file(self, content):
        with open(self.file_path, 'w') as file_handle:
            file_handle.write(content)

    def process_file(self):
        content = self.read_file()
        content = ''.join(c for c in content if c.isalpha())
        self.write_file(content)
        return content

import unittest
import json
from unittest.mock import MagicMock
import os

class TextFileProcessorTestReadFileAsJson(unittest.TestCase):
    def setUp(self):
        self.files = ['test_1.txt', 'test_2.txt', 'test_3.txt', 'test_4.txt', 'test_5.txt']
        self.contents = ['{\n    "name": "test",\n    "age": 12\n}', '12345', '\"hello\"', '\"aaa\"', '\"bbb\"']
        for index, file in enumerate(self.files):
            with open(file, 'w') as f:
                f.write(self.contents[index])

    # the dict type
    def test_read_file_as_json_1(self):
        textFileProcessor = TextFileProcessor(self.files[0])
        data = textFileProcessor.read_file_as_json()
        expected = {"name": "test", "age": 12}
        self.assertEqual(dict, type(data))
        self.assertEqual(expected, data)

    # the int type
    def test_read_file_as_json_2(self):
        textFileProcessor = TextFileProcessor(self.files[1])
        data = textFileProcessor.read_file_as_json()
        expected = 12345
        self.assertEqual(int, type(data))
        self.assertEqual(expected, data)

    # the str type
    def test_read_file_as_json_3(self):
        textFileProcessor = TextFileProcessor(self.files[2])
        data = textFileProcessor.read_file_as_json()
        expected = 'hello'
        self.assertEqual(str, type(data))
        self.assertEqual(expected, data)

    def test_read_file_as_json_4(self):
        textFileProcessor = TextFileProcessor(self.files[3])
        data = textFileProcessor.read_file_as_json()
        expected = 'aaa'
        self.assertEqual(str, type(data))
        self.assertEqual(expected, data)

    def test_read_file_as_json_5(self):
        textFileProcessor = TextFileProcessor(self.files[4])
        data = textFileProcessor.read_file_as_json()
        expected = 'bbb'
        self.assertEqual(str, type(data))
        self.assertEqual(expected, data)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

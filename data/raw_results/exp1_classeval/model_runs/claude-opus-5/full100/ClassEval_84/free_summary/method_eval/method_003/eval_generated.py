import json


class TextFileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file_as_json(self):
        with open(self.file_path, "r") as f:
            return json.loads(f.read())

    def read_file(self) -> str:
        with open(self.file_path, "r") as f:
            return f.read()

    def write_file(self, content: str) -> None:
        with open(self.file_path, "w") as f:
            f.write(content)

    def process_file(self) -> str:
        raw = self.read_file()
        filtered = "".join(ch for ch in raw if ch.isalpha())
        self.write_file(filtered)
        return filtered

import unittest
import json
from unittest.mock import MagicMock
import os

class TextFileProcessorTestProcessFile(unittest.TestCase):
    def test_process_file_1(self):
        self.file = 'test.txt'
        self.content = 'Hello, 123 World!'
        self.expected_result = 'HelloWorld'

        textFileProcessor = TextFileProcessor(self.file)
        textFileProcessor.read_file = MagicMock(return_value=self.content)
        textFileProcessor.write_file = MagicMock()

        result = textFileProcessor.process_file()
        self.assertEqual(result, self.expected_result)
        textFileProcessor.read_file.assert_called_once()
        textFileProcessor.write_file.assert_called_once_with(self.expected_result)

    def test_process_file_2(self):
        self.file = 'test.txt'
        self.content = 'Hello, abc World!'
        self.expected_result = 'HelloabcWorld'

        textFileProcessor = TextFileProcessor(self.file)
        textFileProcessor.read_file = MagicMock(return_value=self.content)
        textFileProcessor.write_file = MagicMock()

        result = textFileProcessor.process_file()
        self.assertEqual(result, self.expected_result)
        textFileProcessor.read_file.assert_called_once()
        textFileProcessor.write_file.assert_called_once_with(self.expected_result)

    def test_process_file_3(self):
        self.file = 'test.txt'
        self.content = ', 123 !'
        self.expected_result = ''

        textFileProcessor = TextFileProcessor(self.file)
        textFileProcessor.read_file = MagicMock(return_value=self.content)
        textFileProcessor.write_file = MagicMock()

        result = textFileProcessor.process_file()
        self.assertEqual(result, self.expected_result)
        textFileProcessor.read_file.assert_called_once()
        textFileProcessor.write_file.assert_called_once_with(self.expected_result)

    def test_process_file_4(self):
        self.file = 'test.txt'
        self.content = 'Hello, World!'
        self.expected_result = 'HelloWorld'

        textFileProcessor = TextFileProcessor(self.file)
        textFileProcessor.read_file = MagicMock(return_value=self.content)
        textFileProcessor.write_file = MagicMock()

        result = textFileProcessor.process_file()
        self.assertEqual(result, self.expected_result)
        textFileProcessor.read_file.assert_called_once()
        textFileProcessor.write_file.assert_called_once_with(self.expected_result)

    def test_process_file_5(self):
        self.file = 'test.txt'
        self.content = 'Hello, 123a World!'
        self.expected_result = 'HelloaWorld'

        textFileProcessor = TextFileProcessor(self.file)
        textFileProcessor.read_file = MagicMock(return_value=self.content)
        textFileProcessor.write_file = MagicMock()

        result = textFileProcessor.process_file()
        self.assertEqual(result, self.expected_result)
        textFileProcessor.read_file.assert_called_once()
        textFileProcessor.write_file.assert_called_once_with(self.expected_result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)

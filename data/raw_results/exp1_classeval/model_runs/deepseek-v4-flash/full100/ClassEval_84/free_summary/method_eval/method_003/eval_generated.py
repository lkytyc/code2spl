import json

class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()

    read_file = read

    def read_json(self):
        return json.loads(self.read())

    def write(self, content):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    write_file = write

    def process(self):
        content = self.read()
        filtered = ''.join(ch for ch in content if ch.isalpha())
        self.write(filtered)
        return filtered

    process_file = process

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

import json

class TextFileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file_as_json(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

    def read_file(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
        return content

    def write_file(self, content: str):
        with open(self.file_path, 'w') as file:
            file.write(content)

    def process_file(self):
        content = self.read_file()
        content = ''.join(char for char in content if char.isalpha())
        self.write_file(content)
        return content

import unittest
import json
from unittest.mock import MagicMock
import os

class TextFileProcessorTestWriteFile(unittest.TestCase):
    def setUp(self) -> None:
        self.files = ['test_1.txt', 'test_2.txt', 'test_3.txt', 'test_4.txt', 'test_5.txt']
        self.contents = ['123aac\n&^(*&43)', '12345', 'aaa', 'bbb', 'ccc']

    def tearDown(self) -> None:
        for file in self.files:
            if os.path.exists(file):
                os.remove(file)

    def test_write_file_1(self):
        textFileProcessor = TextFileProcessor(self.files[0])
        textFileProcessor.write_file(self.contents[0])
        with open(self.files[0], 'r') as f:
            data = f.read()
        self.assertEqual(data, self.contents[0])

    def test_write_file_2(self):
        textFileProcessor = TextFileProcessor(self.files[1])
        textFileProcessor.write_file(self.contents[1])
        with open(self.files[1], 'r') as f:
            data = f.read()
        self.assertEqual(data, self.contents[1])

    def test_write_file_3(self):
        textFileProcessor = TextFileProcessor(self.files[2])
        textFileProcessor.write_file(self.contents[2])
        with open(self.files[2], 'r') as f:
            data = f.read()
        self.assertEqual(data, self.contents[2])

    def test_write_file_4(self):
        textFileProcessor = TextFileProcessor(self.files[3])
        textFileProcessor.write_file(self.contents[3])
        with open(self.files[3], 'r') as f:
            data = f.read()
        self.assertEqual(data, self.contents[3])

    def test_write_file_5(self):
        textFileProcessor = TextFileProcessor(self.files[4])
        textFileProcessor.write_file(self.contents[4])
        with open(self.files[4], 'r') as f:
            data = f.read()
        self.assertEqual(data, self.contents[4])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
